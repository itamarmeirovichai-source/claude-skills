#!/usr/bin/env python3
"""Statistician 2026-10-06: is SPXUSD (FutureSharks/HistData) on a New York clock with DST,
or on fixed EST (UTC-5, no DST, HistData's documented convention)? Outcome-free: reads only
|1m returns| and bar presence, no strategy R.
Run from skills/prop-fleet/scripts:  python3 ../agents/daily/2026-10-06-0247/statistician/clock_check.py"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import tjr_backtest as tj

m = tj.load_minutes()
r = np.log(m.c).diff().abs()
df = pd.DataFrame({"r": r, "hm": m.index.strftime("%H:%M"), "mo": m.index.month, "y": m.index.year})
# US DST: second Sunday of March .. first Sunday of November. Use clean months.
for name, mo in (("Jan-Feb (no DST)", [1, 2]), ("Jun-Aug (DST)", [6, 7, 8])):
    s = df[df.mo.isin(mo)].groupby("hm").r.mean()
    top = s.sort_values(ascending=False).head(6)
    print(f"{name:18s} top-6 |r| minutes: " + ", ".join(f"{k} {v*1e4:.2f}bp" for k, v in top.items()))
    for hm in ("08:30", "09:30", "15:59", "16:00", "16:14", "17:00", "18:00"):
        print(f"   {hm} mean|r| {s.get(hm, np.nan)*1e4:.2f}bp")
# daily maintenance break: first bar after the longest intraday gap, by season
idx = m.index
gap = pd.Series(idx[1:] - idx[:-1], index=idx[1:])
g = gap[(gap > pd.Timedelta(minutes=30)) & (gap < pd.Timedelta(hours=6))]
g = g[g.index.weekday < 5]
for name, mo in (("Jan-Feb", [1, 2]), ("Jun-Aug", [6, 7, 8])):
    sel = g[g.index.month.isin(mo)]
    print(f"{name}: reopen time after 30m-6h gaps (weekday), top counts:",
          sel.index.strftime("%H:%M").value_counts().head(4).to_dict())
# bars per weekday session in the 09:30..15:59 window, by season
x = m[(m.index.strftime("%H:%M") >= "09:30") & (m.index.strftime("%H:%M") <= "15:59")]
cnt = x.groupby(x.index.normalize()).size()
cnt = cnt[cnt.index.weekday < 5]
print("09:30-15:59 bars/session median by month:", cnt.groupby(cnt.index.month).median().to_dict())
