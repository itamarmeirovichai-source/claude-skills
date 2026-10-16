#!/usr/bin/env python3
"""Statistician 2026-10-06: does H0006 (daily/2026-10-04/hypothesis.py build_days, need list
line 56) read the trade day's own future? Entry is the 15:30 open; the need list also requires
day d's 15:59 bar. Outcome-free: counts eligibility only, no R is computed.
Also counts how often r1's prev_close comes from a session more than 4 calendar days back
(stale prior close: prev_close is the last day that HAD a 15:59 bar, line 64-72).
Run from skills/prop-fleet/scripts."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import tjr_backtest as tj

m1 = tj.load_minutes()
hm = m1.index.strftime("%H:%M")
days = m1.index.normalize()
have = {}
for k in ["09:59", "14:59", "15:29", "15:30", "15:59"]:
    have[k] = set(days[hm == k])
wk = sorted(d for d in set(days) if d.weekday() < 5)
pre = [d for d in wk if all(d in have[k] for k in ["09:59", "14:59", "15:29", "15:30"])]
full = [d for d in pre if d in have["15:59"]]
print(f"weekdays {len(wk)}; with 09:59,14:59,15:29,15:30 (all known by 15:30 entry): {len(pre)}")
print(f"  of which also have the trade day's 15:59 bar (H0006 as written): {len(full)}")
print(f"  dropped only because the 15:59 bar AFTER entry is missing: {len(pre) - len(full)} "
      f"({(len(pre) - len(full)) / len(pre):.1%})")
# stale prev_close: as written, prev_close = 15:59 close of the previous day that has a 15:59 bar
c1559 = sorted(have["15:59"])
gaps = []
prev = None
for d in c1559:
    if prev is not None and d in set(full):
        gaps.append((d - prev).days)
    prev = d
g = np.array(gaps)
print(f"H0006 as-written eligible days with prev_close > 4 calendar days back: {(g > 4).sum()} of {len(g)}; max {g.max()} days")
