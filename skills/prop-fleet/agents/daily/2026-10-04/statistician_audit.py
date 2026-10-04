#!/usr/bin/env python3
"""Statistician audit 2026-10-04: reproducible checks behind the findings.
Run from skills/prop-fleet/scripts:  python3 ../agents/daily/2026-10-04/statistician_audit.py"""
import csv, sys
from pathlib import Path
from statistics import NormalDist
import numpy as np, pandas as pd
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "scripts"))
import stack_backtest as sb, tjr_backtest as tj

led = list(csv.DictReader(open(HERE.parents[1].parent / "ledger.csv")))
print("ledger N =", sum(int(r["count"]) for r in led))
print("rows without p5:", [r["id"] for r in led if not r["result_p5_R"]])
for n in (110, 143):
    print(f"Bonferroni one-sided z for N={n}:", round(NormalDist().inv_cdf(1 - 0.05 / n), 3))

d = sb.load_spx(); stale = d.Open.round(2) == d.Close.shift(1).round(2)
print("share of opens == prior close, by year:",
      stale.groupby(d.index.year).mean().round(3).loc[2008:2015].to_dict())

m = tj.load_minutes(); r = np.log(m.c).diff().abs()
df = pd.DataFrame({"r": r, "hm": m.index.strftime("%H:%M"), "mo": m.index.month})
for name, mo in (("Jan-Feb", [1, 2]), ("Jul-Aug", [7, 8])):
    s = df[df.mo.isin(mo)].groupby("hm").r.mean()
    print(name, "most volatile minutes:", list(s.sort_values(ascending=False).index[:6]))
