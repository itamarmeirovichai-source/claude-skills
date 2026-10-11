"""Look-ahead / future-truncation test (pre-registered): for 50 random cut days per variant, rerun every
generator on data deleted after the cut and require identical decision weights on every day <= cut."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, __import__("os").path.dirname(__file__))
from d3lib import *
from run import build

data = load(sys.argv[1])
ncut = int(sys.argv[2]) if len(sys.argv) > 2 else 50
full = build(data)
rng = np.random.default_rng(0)
days = data.close.loc["2019-03-01":"2026-09-29"].index
cuts = [pd.Timestamp(x) for x in sorted(rng.choice(days, ncut, replace=False))]
# force month-end, Sunday and month-start cuts into the set (where universe / weekly logic changes)
cuts += [pd.Timestamp("2022-05-31"), pd.Timestamp("2024-06-30"), pd.Timestamp("2023-01-01"), pd.Timestamp("2025-03-02")]
bad = {k: 0 for k in full}
for i, c in enumerate(cuts):
    part = build(data.cut(c))
    for k in full:
        if k == "D3-09" and c < OOS[0]:
            continue   # D3-09 hours are chosen on the whole IS by design; it only trades OOS
        for (Df, *_), (Dp, *_) in zip(full[k][0], part[k][0]):
            a = Df.loc[:Dp.index[-1]].values
            b = Dp.reindex(columns=Df.columns).values
            if a.shape != b.shape or not np.allclose(a, b, atol=1e-12, equal_nan=True):
                bad[k] += 1
                diff = np.argwhere(~np.isclose(a, b, atol=1e-12))
                print("MISMATCH", k, c.date(), "first diff at", Df.index[diff[0][0]] if len(diff) else "shape", flush=True)
    print(f"cut {i+1}/{len(cuts)} {pd.Timestamp(c).date()} done", flush=True)
print("RESULT", {k: ("PASS" if v == 0 else f"FAIL {v}") for k, v in bad.items()})
