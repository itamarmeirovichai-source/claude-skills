"""Red team F1: rebuild the sleeve building blocks once with the head's own functions and cache them
(scratchpad only), plus reproduce the departments' original numbers (D3-11, H0022).

usage: CLAUDE_SCRATCH=<data dir> python3 rt_rebuild.py <data dir>/bin <cache dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ensemble as E  # noqa: E402

D3, L, V = E.D3, E.L, E.V
binp, cache = sys.argv[1], Path(sys.argv[2])
cache.mkdir(parents=True, exist_ok=True)

data = E.D3.load(binp)
m1, m5 = E.nq_raw()

# ---- S1 building blocks (cost-free pieces) for F1-01 and F1-02
for which in ("ftmo", "btceth"):
    D = E.s1_decisions(data, which)
    b = E.s1_ftmo_eval(D, data, mult=0.0)          # gross, to, gross_notional (cost=swap=0)
    v = E.s1_venue_eval(D, data)
    b["venue_net"] = v.net
    b["venue_fund"] = D3.evaluate([(D, data.ret, D3.C_PERP, True)], data=data).fund
    # per-coin held gross notional to allow coin-specific spread diagnostics
    W = D.shift(1).fillna(0.0)
    big = [c for c in ("BTC", "ETH") if c in W.columns]
    b["gn_btceth"] = W[big].abs().sum(axis=1)
    # turnover split BTC/ETH vs alts (same formula as D3.evaluate)
    R = np.nan_to_num(data.ret.reindex(D.index)[D.columns].values)
    Wv = W.values
    g = np.sum(Wv * R, axis=1)
    Wd = Wv * (1 + R) / (1 + g)[:, None]
    prev = np.vstack([np.zeros(Wv.shape[1]), Wd[:-1]])
    tom = np.abs(Wv - prev)
    isbig = np.isin(D.columns, big)
    b["to_btceth"] = tom[:, isbig].sum(axis=1)
    b["to_alts"] = tom[:, ~isbig].sum(axis=1)
    b.to_pickle(cache / f"s1_{which}.pkl")
    D.to_pickle(cache / f"D_{which}.pkl")

# BTC buy-and-hold for context
data.ret[["BTC"]].to_pickle(cache / "btc.pkl")


# ---- S2 per-session pieces (points), 1m and 5m separately, roll weeks excluded (as the head)
def s2_raw(raw, roll=True):
    days = sorted(set(raw.date))
    r = raw[~raw.date.isin(L.roll_excluded(days))] if roll else raw
    day, *_ = V.run(r, lambda p: np.full(np.shape(p), 0.0))
    day.index = pd.to_datetime(day.date)
    return day[["gross_pts", "units", "entry"]]


for nm, raw in (("m1", m1), ("m5", m5)):
    s2_raw(raw).to_pickle(cache / f"s2_{nm}.pkl")
    s2_raw(raw, roll=False).to_pickle(cache / f"s2_{nm}_noroll.pkl")

# 1m vs 5m bar-alignment check on the overlap: 5m bar t (bar-open label) vs 1m bars t..t+4
a = m1[["o", "h", "l", "c", "v"]]
b5 = m5[["o", "h", "l", "c", "v"]]
agg = a.resample("5min", label="left", closed="left").agg(dict(o="first", h="max", l="min", c="last", v="sum")).dropna()
j = b5.join(agg, rsuffix="_1m", how="inner")
lines = [f"5m vs 1m resampled bars on overlap: n={len(j)}"]
for k in "ohlc":
    d = (j[k] - j[k + "_1m"]).abs()
    lines.append(f"  {k}: median |diff| {d.median():.3f} pt, share exact {(d < 1e-9).mean():.3f}")
lines.append(f"  vol ratio median {(j.v / j.v_1m).median():.3f}")
# label-shift alternative: 5m labelled at bar close
agg2 = a.resample("5min", label="right", closed="left").agg(dict(o="first", c="last")).dropna()
j2 = b5.join(agg2, rsuffix="_1m", how="inner")
lines.append(f"  if 5m were close-labelled: open share exact {((j2.o - j2.o_1m).abs() < 1e-9).mean():.3f}")
for per in (("2023-03-01", "2023-03-10"), ("2023-07-10", "2023-07-14"), ("2025-11-03", "2025-11-07")):
    jj = j.loc[per[0]:per[1]]
    lines.append(f"  {per}: open share exact {((jj.o - jj.o_1m).abs() < 1e-9).mean():.3f} n {len(jj)}")
print("\n".join(lines))
(cache / "bar_check.txt").write_text("\n".join(lines) + "\n")
print("1m sessions", min(m1.date), max(m1.date), " 5m sessions", min(m5.date), max(m5.date))
