import sys; sys.path.insert(0, '.')
import pandas as pd, loaders as L
raw = L.load_nq()
for t in ["2021-04-02","2023-04-07"]:
    x = raw[raw.index.normalize()==pd.Timestamp(t)]
    print(t, x.index.min(), x.index.max(), len(x), "v sum", x.v.sum())
    print(x.between_time("09:28","09:35"))
    print(x.between_time("15:55","16:59").tail(3))
r = L.rth(raw); print(sorted(set(r.date))[:0])
print([d for d in ["2021-04-02","2023-04-07"] if pd.Timestamp(d).date() in set(r.date)])
