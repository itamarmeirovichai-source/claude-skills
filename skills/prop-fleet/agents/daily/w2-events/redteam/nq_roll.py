import sys; sys.path.insert(0, '.')
import numpy as np, pandas as pd
import loaders as L
raw = L.load_nq()
j = np.log(raw.o / raw.c.shift(1))
big = j[j.abs() > 0.004]
print("bar-to-bar |jump|>40bp:", len(big))
print(big.groupby([big.index.hour, big.index.minute]).size())
print(big.sort_values().round(4).to_string()[:3000])
# 00:00 bar presence on weekdays
d = pd.Series(raw.index.normalize().unique())
wk = d[d.dt.dayofweek < 5]
has0 = set(raw.index[(raw.index.hour==0)&(raw.index.minute==0)].normalize())
r = L.rth(raw); sess = set(pd.to_datetime(sorted(set(r.date))))
miss = sorted(s for s in sess if s not in has0)
print("RTH sessions without 00:00 bar:", len(miss), [str(x.date()) for x in miss][:30])
for t in ["2021-04-02","2023-04-07","2024-03-29","2025-04-18"]:
    print(t, (raw.index.normalize()==pd.Timestamp(t)).sum())
