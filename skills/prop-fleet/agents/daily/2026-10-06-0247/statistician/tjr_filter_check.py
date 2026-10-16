#!/usr/bin/env python3
"""Statistician 2026-10-06: size of the trade-day look-ahead in tjr_backtest.run (line 241-244:
len(m1[18:00 prev .. 11:00 today]) >= 300 is read before setups that can trigger from 03:00).
Outcome-free first part: counts days whose eligibility changes if the bar count stops at 03:00
(the window start) with the threshold scaled to the 540-minute pre-window span.
Second part re-reads the EXISTING base-variant trades file (tjr_base_trades.csv, written by
tjr_backtest.main on 29 Sep) only to report how many already-reported trades sit on such days.
No new strategy variant is run.
Run from skills/prop-fleet/scripts."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import tjr_backtest as tj

m1 = tj.load_minutes()
days = sorted(set(m1.index.normalize()))
rows = []
for d in days:
    if d.weekday() >= 5:
        continue
    day = d.date()
    a0 = pd.Timestamp(day) - pd.Timedelta(days=1) + pd.Timedelta(hours=20)
    asia = m1.loc[a0:a0 + pd.Timedelta(hours=3, minutes=59)]
    if len(asia) < 120:
        continue
    full = len(m1.loc[pd.Timestamp(day) - pd.Timedelta(hours=6): pd.Timestamp(f"{day} 11:00")])
    pre = len(m1.loc[pd.Timestamp(day) - pd.Timedelta(hours=6): pd.Timestamp(f"{day} 02:59")])
    win = len(m1.loc[pd.Timestamp(f"{day} 03:00"): pd.Timestamp(f"{day} 11:00")])
    rows.append((pd.Timestamp(day), full, pre, win))
t = pd.DataFrame(rows, columns=["day", "full", "pre", "win"])
as_written = t.full >= 300
print(f"weekdays passing the asia>=120 test: {len(t)}")
print(f"pass tjr filter (>=300 bars 18:00..11:00, reads up to 11:00): {as_written.sum()}  fail: {(~as_written).sum()}")
# a day fails the full test but would pass an ex-ante pre-window test scaled 300*540/1020=159
ex_ante = t.pre >= 159
print(f"ex-ante (>=159 of 540 bars 18:00..02:59): pass {ex_ante.sum()}")
print(f"  fail as-written but pass ex-ante (look-ahead drops): {(ex_ante & ~as_written).sum()}")
print(f"  pass as-written but fail ex-ante: {(~ex_ante & as_written).sum()}")
dropped = t[ex_ante & ~as_written]
print("  dropped days, window (03:00-11:00) bars: min/median/max",
      dropped.win.min() if len(dropped) else None, dropped.win.median() if len(dropped) else None,
      dropped.win.max() if len(dropped) else None)
print("  dropped days list (first 15):", [str(x.date()) for x in dropped.day[:15]])
f = tj.SCRATCH / "tjr_base_trades.csv"
if f.exists():
    tr = pd.read_csv(f, parse_dates=["day"])
    print(f"existing base trades file: n={len(tr)}  mean R {tr.R.mean():+.4f}")
