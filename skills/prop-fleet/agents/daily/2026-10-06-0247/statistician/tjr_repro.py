#!/usr/bin/env python3
"""Statistician 2026-10-06: reproduce two TJR numbers that no committed script prints:
(a) H0004 gross +0.007R 90% [-0.07,+0.09] (references/tjr.md:57) and
(b) H0010 slice risk >= 4 pt: +0.057R n=266, halves +0.004/+0.079, 90% [-0.09,+0.20] (tjr.md:71-73).
Reads ONLY the base-variant trade file written by tjr_backtest.main on 29 Sep
(SCRATCH/tjr/tjr_base_trades.csv). No new variant, no new rule, nothing re-run.
Also prints the rule-3 bound at the current N for both, with ledger_gate.one_sided_lb.
Run from skills/prop-fleet/scripts."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
here = Path(__file__).resolve()
sys.path.insert(0, str(here.parents[4] / "scripts"))
sys.path.insert(0, str(here.parents[1].parent / "2026-10-05" / "eng_head"))
import tjr_backtest as tj
from ledger_gate import ledger_n, one_sided_lb, alpha_z

N = ledger_n(here.parents[3] / "ledger.csv")
t = pd.read_csv(tj.SCRATCH / "tjr_base_trades.csv", parse_dates=["day"])
print(f"base trades n={len(t)}  net mean {t.R.mean():+.4f}R  (tjr-run.txt:4 says n=860 -0.203R)")
g = (t.pts + tj.COST_PTS) / t.risk
lo, _, hi = tj.boot_mean(g.values)
print(f"(a) gross mean {g.mean():+.4f}R  boot_mean 5/95 [{lo:+.3f}, {hi:+.3f}]  mean cost {(tj.COST_PTS / t.risk).mean():.3f}R")
s = t[t.risk >= 4.0]
lo, _, hi = tj.boot_mean(s.R.values)
h1 = s[s.day.dt.year <= 2014].R.mean(); h2 = s[s.day.dt.year >= 2015].R.mean()
print(f"(b) risk>=4: n={len(s)} net mean {s.R.mean():+.4f}R  5/95 [{lo:+.3f}, {hi:+.3f}]  2010-14 {h1:+.4f}  2015-18 {h2:+.4f}")
a, z = alpha_z(N)
print(f"N={N} alpha={a:.3e} z={z:.3f}")
for name, x, d in (("H0004 base net", t.R.values, t.day.dt.date.astype(str).values),
                   ("H0004 base gross", g.values, t.day.dt.date.astype(str).values),
                   ("H0010 slice net", s.R.values, s.day.dt.date.astype(str).values)):
    lb, draws = one_sided_lb(x, d, N)
    nb = x.mean() - z * x.std(ddof=1) / np.sqrt(x.size)
    print(f"  {name:18s} rule-3 LB boot {lb:+.4f} ({draws} draws)  normal {nb:+.4f}")
