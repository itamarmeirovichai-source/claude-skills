"""Diagnostic only: re-run the 12 REGISTERED rules with calendar corrections found by the red team.
No new variant. Corrections: (1) January ISM moved to the actual release day (red-team recollection:
ISM releases the December report on the 2nd/3rd business day); (2) April RETAIL annual-revision dates
dropped; (3) FOMC_MINUTES rows that are not minutes (2019-10-11, 2020-03-03, 2020-03-23) dropped;
(4) 2026-10-11 artifact rows dropped."""
import sys; sys.path.insert(0, '.')
import numpy as np, pandas as pd
import events_bt as E
ev = pd.read_csv(E.HERE / "events.csv", parse_dates=["date"])
JAN = {2019: "2019-01-03", 2020: "2020-01-03", 2021: "2021-01-05", 2022: "2022-01-04",
       2023: "2023-01-04", 2024: "2024-01-03", 2025: "2025-01-03"}
m = (ev.event == "ISM") & (ev.date.dt.month == 1) & ev.date.dt.year.isin(JAN)
ev.loc[m, "date"] = ev.loc[m, "date"].dt.year.map(lambda y: pd.Timestamp(JAN[y]))
ev = ev[~((ev.event == "RETAIL") & ev.date.isin(pd.to_datetime(
    ["2021-04-26", "2022-04-25", "2023-04-24", "2024-04-23", "2025-04-25"])))]
ev = ev[~((ev.event == "FOMC_MINUTES") & ev.date.isin(pd.to_datetime(["2019-10-11", "2020-03-03", "2020-03-23"])))]
ev = ev[ev.date < "2026-10-11"]

def cal2():
    e = ev[ev.scheduled.astype(str) == "True"].copy()
    e["d"] = e.date.dt.date; e["t"] = e.time_et.map(E.mins)
    kinds = e.groupby("d").event.apply(set).to_dict()
    fomc_t = {r.d: r.t for r in e[e.event == "FOMC"].itertuples()}
    black = {}
    for r in e[e.event.isin(E.RTH_EVENTS)].itertuples():
        if 570 <= r.t <= 960: black.setdefault(r.d, []).append(r.t)
    return kinds, fomc_t, black

D = {k: E.build_days(k) for k in ("SPY", "NQ")}
for label, cal in (("as run", E.calendar()), ("corrected", cal2())):
    R = {k: E.run_market(k, D[k], cal, 1.0, 0)[0] for k in D}
    print(label)
    for v in E.VARIANTS:
        p = E.pool([R["SPY"][v], R["NQ"][v]])
        print(f"  {v}: n {len(p):4d} mean {p.mean():+7.2f} t {E.tstat(p):+5.2f}")
