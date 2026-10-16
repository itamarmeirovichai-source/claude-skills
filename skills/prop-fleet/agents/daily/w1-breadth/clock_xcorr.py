#!/usr/bin/env python3
"""Outcome-free clock check for the HistData files: for each month, the shift (in minutes,
-120..+120) of the HistData series as stored by fetch.py. clock_xcorr.txt = first run, when fetch.py still added a fixed +5h (EST);
clock_xcorr_after.txt = re-run after fetch.py was corrected to New York time with DST that maximizes the correlation of its
1-minute returns with an Oanda market on the verified UTC clock. 0 = fetch.py's fixed-EST
assumption is right that month."""
import numpy as np, pandas as pd
from common import load

PAIRS = [("SPXUSD", "SPX500_USD"), ("JPXJPY", "JP225_USD"), ("GRXEUR", "FR40_EUR"), ("ETXEUR", "FR40_EUR")]

def r1(m):
    d = load(m).c
    d = d[(d.index >= "2011-01-01") & (d.index < "2019-01-01")]
    r = np.log(d).diff()
    ok = d.index.to_series().diff() == pd.Timedelta(minutes=1)
    return r[ok.values]

for h, o in PAIRS:
    a, b = r1(h), r1(o)
    out = {}
    for per, ga in a.groupby(a.index.to_period("M")):
        gb = b[(b.index >= ga.index[0] - pd.Timedelta(hours=3)) & (b.index <= ga.index[-1] + pd.Timedelta(hours=3))]
        best, bc = None, -1
        for s in range(-120, 121, 60):
            x = ga.copy(); x.index = x.index + pd.Timedelta(minutes=s)
            j = x.index.intersection(gb.index)
            if len(j) < 2000: continue
            cc = np.corrcoef(x[j].values, gb[j].values)[0, 1]
            if cc > bc: best, bc = s, cc
        out[str(per)] = (best, round(bc, 2))
    s = pd.Series({k: v[0] for k, v in out.items()})
    print(f"{h} vs {o}: best shift (min) counts {s.value_counts().to_dict()}")
    print("   months with shift != 0:", {k: v for k, v in out.items() if v[0] != 0})
