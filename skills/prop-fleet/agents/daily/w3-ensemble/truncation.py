"""F1 look-ahead / truncation test (F1-00): for 50 random cut dates in W (seed 0), delete all data after
the cut, rebuild S1 decision weights (F1-01 and F1-02), the S2 daily series and the risk weights k, and
check every value up to the cut equals the full-data run.

usage: CLAUDE_SCRATCH=<data dir> python3 truncation.py <binance parquet dir>
"""
import sys

import numpy as np
import pandas as pd

import ensemble as E

data = E.D3.load(sys.argv[1])
m1, m5 = E.nq_raw()
full = {w: E.s1_decisions(data, w) for w in ("ftmo", "btceth")}
s2f = E.s2_series(m1, m5, E.C2_FTMO)
s1f = E.s1_ftmo_eval(full["ftmo"], data)
kf = E.stack(s1f, s2f)[["k1", "k2"]]
rng = np.random.default_rng(0)
days = pd.date_range(E.W0, E.W1, freq="D")
cuts = sorted(rng.choice(days, 50, replace=False))
bad = 0
for c in cuts:
    c = pd.Timestamp(c)
    dc = data.cut(c)
    ok = True
    for w in ("ftmo", "btceth"):
        d = E.s1_decisions(dc, w)
        ok &= np.allclose(d.values, full[w].loc[:c, d.columns].values, atol=1e-12, equal_nan=True)
    s2c = E.s2_series(m1, m5, E.C2_FTMO, end=c)
    ok &= np.allclose(s2c.net.values, s2f.loc[:c].net.values, atol=1e-15)
    s1c = E.s1_ftmo_eval(E.s1_decisions(dc, "ftmo"), dc)
    kc = E.stack(s1c, s2c)[["k1", "k2"]]
    kc = kc.loc[:c]
    ok &= np.allclose(kc.values, kf.loc[kc.index].values, equal_nan=True)
    bad += not ok
    print(c.date(), "identical" if ok else "DIFFERENT", flush=True)
print(f"truncation test: {len(cuts)} cuts, {bad} with differences -> {'PASS' if bad == 0 else 'FAIL'}")
