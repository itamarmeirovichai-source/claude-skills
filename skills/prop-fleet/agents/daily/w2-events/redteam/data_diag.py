import sys; sys.path.insert(0, '..'); sys.path.insert(0, '.')
import numpy as np, pandas as pd
import loaders as L
for name in ("SPY","NQ"):
    raw = {"SPY":L.load_spy,"NQ":L.load_nq}[name]()
    print(name, raw.index.min(), raw.index.max(), "tz", raw.index.tz)
    r = L.rth(raw)
    g = r.groupby("date")
    n = g.size(); first = g.hm.min(); last = g.hm.max()
    print(" sessions", len(n), "bars/session describe", n.describe().round(1).to_dict())
    print(" first!=930:", (first!=930).sum(), " last!=1559:", (last!=1559).sum())
    print(" last bar distribution (non-1559):", last[last!=1559].value_counts().head(10).to_dict())
    print(" short sessions (<300 bars):", [(str(d), int(x), int(last[d])) for d,x in n[n<300].items()])
    # bars at 15:59 / 9:59 / 10:03 presence
    for hm in (930,931,959,1003,1357,1359,1400,1415,1430,1530,1559):
        print(f"  missing {hm}: {(~g.hm.apply(lambda s: hm in set(s.values))).sum()}")
    # zero / negative prices
    print(" nonpos", (raw[['o','h','l','c']]<=0).sum().sum(), "h<l", (raw.h<raw.l).sum())
