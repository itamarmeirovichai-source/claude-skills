"""Red team F1: why does the 5m-only S2 lift the stack (t 1.04 vs 0.74)? Compare 1m and 5m S2 per session.
usage: python3 rt_splice.py <cache dir>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
C = Path(sys.argv[1])
a = pd.read_pickle(C / "s2_m1.pkl"); b = pd.read_pickle(C / "s2_m5.pkl")
f = lambda d, c: pd.Series(np.where(d.entry.isna(), 0, (d.gross_pts - c * d.units) / d.entry) * 1e4, index=d.index)
W0, S = "2023-01-01", "2025-11-21"
A, B = a.loc[W0:S], b.loc[W0:S]
print("sessions 1m", len(A), "5m", len(B), "common", len(A.index.intersection(B.index)))
print("only in 1m:", list(A.index.difference(B.index).date)[:20])
print("only in 5m:", list(B.index.difference(A.index).date)[:20])
j = pd.DataFrame(dict(n1=f(A, .75), n5=f(B, .75), g1=f(A, 0), g5=f(B, 0), u1=A.units, u5=B.units)).dropna()
print(j.describe().T[["mean", "std"]])
print("corr net", j.n1.corr(j.n5))
d = (j.n5 - j.n1)
print("diff mean bp", d.mean(), "t", d.mean() / (d.std() / np.sqrt(len(d))))
print("largest diffs:\n", d.abs().sort_values().tail(8).index.date, d.loc[d.abs().sort_values().tail(8).index].round(1).values)
# per year
print(j.groupby(j.index.year)[["n1", "n5", "g1", "g5", "u1", "u5"]].mean().round(2))
