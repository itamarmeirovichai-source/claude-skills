"""Red team F1, check 3: do the head's imports reproduce the departments' original sleeve numbers?
D3-11 (full D3 universe, D3 Binance-perp costs, OOS 2023-01-01..2026-09-30) should be +7.32 bp/d, t 2.15/2.10.
H0022 NQ 1m 2020-09..2025-11 ex roll weeks at 0.375 pt should be +5.043 bp/d, t +1.68.

usage: CLAUDE_SCRATCH=<data dir> python3 rt_orig.py <data dir>/bin
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ensemble as E  # noqa: E402

D3 = E.D3
data = D3.load(sys.argv[1])
w1 = D3.g_tsmom(data)
D = E.vol_managed(data, w1)                      # head's copy of run.py m(w1, S, 0.20)
e = D3.evaluate([(D, data.ret, D3.C_PERP, True)], data=data)
o = D3.stats(e.loc[D3.OOS[0]:D3.OOS[1]].net.values)
print(f"D3-11 rebuilt via ensemble.vol_managed: OOS mean {o['mean_bp']:+.2f} bp/d t_iid {o['t_iid']:+.2f} "
      f"t_nw {o['t_nw']:+.2f} p5 {o['p5_bp']:+.2f} Sharpe {o['sharpe']:+.2f}  (report: +7.32, 2.15/2.10)")
sys.path.insert(0, str(E.DAILY / "w1-crypto"))
import run as R  # noqa: E402
legs, _ = R.build(data)["D3-11"]
e2 = D3.evaluate(legs, data=data)
print("max |diff| vs run.py D3-11 daily net:", float((e2.net - e.net).abs().max()))
# FTMO-coin restriction effect at D3 costs, same window (diagnostic: how much the universe cut costs)
Df = E.s1_decisions(data, "ftmo")
ef = D3.evaluate([(Df, data.ret, D3.C_PERP, True)], data=data)
of = D3.stats(ef.loc[D3.OOS[0]:D3.OOS[1]].net.values)
print(f"D3-11 on FTMO-listed coins, D3 costs, OOS: mean {of['mean_bp']:+.2f} t {of['t']:+.2f}")
for a, b in (("2023-01-01", "2026-05-07"),):
    x = D3.stats(e.loc[a:b].net.values); y = D3.stats(ef.loc[a:b].net.values)
    print(f"  window W {a}..{b}: full universe {x['mean_bp']:+.2f} (t {x['t']:+.2f}); FTMO coins {y['mean_bp']:+.2f} (t {y['t']:+.2f})")

m1 = E.L.rth(E.L.load_nq())
s = E.s2_days(m1, E.C2_FUT)
n = s.net.values * 1e4
print(f"H0022 rebuilt: n {len(n)} {s.index[0].date()}..{s.index[-1].date()} mean {n.mean():+.3f} bp "
      f"t {n.mean() / (n.std(ddof=1) / np.sqrt(len(n))):+.2f}  (report +5.043, t +1.68)")
for a, b in (("2023-01-01", "2025-11-21"), ("2020-09-01", "2022-12-31")):
    x = n[(s.index >= a) & (s.index <= b)]
    print(f"  H0022 0.375pt {a}..{b}: mean {x.mean():+.2f} t {x.mean() / (x.std(ddof=1) / np.sqrt(len(x))):+.2f} n {len(x)}")
