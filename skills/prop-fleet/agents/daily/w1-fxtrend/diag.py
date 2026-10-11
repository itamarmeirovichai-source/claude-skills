#!/usr/bin/env python3
"""D2 diagnostics for a variant (default the headline D2-08; arg: variant id), run after fxtrend.py. Not strategies,
not counted: they explain the headline result.

1. OOS Sharpe before costs, without swap markup, and without the SNB day (2015-01-15).
2. Is the prop expected value an edge or the fee option? The same prop rules run on
   the OOS returns with their mean removed (zero edge) and shifted by +/- 2 bp/day.
"""
import sys

import numpy as np

import data as D
import fxtrend as F

d = D.panel()
VID = sys.argv[1] if len(sys.argv) > 1 else "D2-08"
df, _ = F.run(VID, d)
oos = F.active(df).loc[F.OOS_START:]
sh = lambda x: x.mean() / x.std() * np.sqrt(F.TD)
print(f"{VID} OOS, lag1 1x cost, 10% vol")
print(f"  net Sharpe {sh(oos['net']):.2f}; before any cost {sh(oos['gross']):.2f}; "
      f"trading cost only (no swap markup) {sh(oos['gross'] - oos['cost']):.2f}")
x = oos["net"].drop("2015-01-15")
print(f"  net Sharpe without 2015-01-15 (SNB) {sh(x):.2f}; that day {oos.loc['2015-01-15','net']*100:+.2f}%")
print(f"  t needed at 13.6y for the bar: Sharpe >= {F.Z_BAR/np.sqrt(len(oos)/F.TD):.2f}")

idx = F.boot_paths(len(oos), 10_000, 1522, seed=0)
mg = oos["margin"].values
print("\nprop EV at 10% vol vs the strategy's OOS mean (same bootstrap paths)")
for shift in (None, -2, 0, 2, 4):
    r = oos["net"].values.copy()
    if shift is not None:
        r = r - r.mean() + shift / 1e4
    o = F.prop_sim(r, mg, 1.0, idx)
    lab = "actual OOS" if shift is None else f"mean set to {shift:+d} bp/day"
    print(f"  {lab:24s} pass {o['p_pass']:.3f} blow {o['p_blow_eval']:.3f} "
          f"funded 2y survival {o['funded_survival']:.3f} E[net/attempt] ${o['exp_net']:,.0f}")
