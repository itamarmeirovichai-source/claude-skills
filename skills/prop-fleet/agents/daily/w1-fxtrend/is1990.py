#!/usr/bin/env python3
"""IS Sharpe on the pre-registered window 1990-01-02..2012-12-31 (fxtrend.py's IS
started where positions first appear, 1988-89). Checks the headline choice."""
import numpy as np
import data as D
import fxtrend as F

d = D.panel()
R = d["R"]
core = [c for c in R if d["meta"].loc[c, "cls"] != "BOND"]
sc = F.ewmac_scalars(F.ewmac_raw(R[core]), F.eligible(R[core]))
for v, name in F.VARIANTS.items():
    df, _ = F.run(v, d, sc)
    x = df.loc["1990-01-02":F.IS_END, "net"]
    print(f"{v} {name:28s} IS(1990-2012) net Sharpe {x.mean()/x.std()*np.sqrt(F.TD):.2f}")
