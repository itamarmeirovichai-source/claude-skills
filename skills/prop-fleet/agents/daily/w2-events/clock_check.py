#!/usr/bin/env python3
"""Clock check (reads no trade outcome, never a direction): across scheduled FOMC days, the
median |1m close-to-close return| of the bar opening at T+k (k = -5..+5, T = events.csv time)
divided by that day's median |r| over 12:00-15:30. The statement bar must stand out at k = 0
(or k = 1 if the print lands in the last seconds). Done per time group, before any backtest."""
import numpy as np
import pandas as pd
import loaders as L

ev = pd.read_csv("events.csv", parse_dates=["date"])
f = ev[(ev.event == "FOMC") & ev.scheduled].copy()
ks = range(-5, 6)
for name, ld in (("SPX", L.load_spx), ("SPY", L.load_spy), ("NQ", L.load_nq)):
    m = L.rth(ld())
    m["r"] = (m.c / m.c.shift(1) - 1).abs()
    by = {d: g for d, g in m.groupby("date")}
    for tm, grp in f.groupby("time_et"):
        rows = []
        for _, e in grp.iterrows():
            g = by.get(e.date.date())
            if g is None or len(g) < 300:
                continue
            base = g[(g.hm >= 1200) & (g.hm <= 1530)].r.median()
            T = pd.Timestamp(f"{e.date.date()} {tm}")
            rows.append([g.r.get(T + pd.Timedelta(minutes=k), np.nan) / base for k in ks])
        if not rows:
            continue
        med = np.nanmedian(np.array(rows), axis=0)
        print(f"{name} T={tm} n={len(rows):3d}  " + "  ".join(f"{k:+d}:{v:5.1f}" for k, v in zip(ks, med)))
