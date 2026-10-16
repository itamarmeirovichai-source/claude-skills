import sys; sys.path.insert(0, '.')
import numpy as np, pandas as pd, loaders as L
s = L.load_spy(); r = L.rth(s)
g = r.groupby("date"); o = g.o.first(); c = g.c.last()
gap = np.log(o / c.shift(1))
print("first close", c.iloc[0], "2019-01-02 (raw SPY close was 250.18)")
print("last close", c.iloc[-1], "2025-07-18 (raw ~627.04)")
# SPY ex-div dates (approx: Friday before/after 3rd Friday of Mar/Jun/Sep/Dec)
ex = ["2019-03-15","2019-06-21","2019-09-20","2019-12-20","2020-03-20","2020-06-19","2020-09-18","2020-12-18",
      "2021-03-19","2021-06-18","2021-09-17","2021-12-17","2022-03-18","2022-06-17","2022-09-16","2022-12-16",
      "2023-03-17","2023-06-16","2023-09-15","2023-12-15","2024-03-15","2024-06-21","2024-09-20","2024-12-20",
      "2025-03-21","2025-06-20"]
ex = [pd.Timestamp(x).date() for x in ex]
gx = gap.reindex(ex).dropna()
print("mean gap ex-div days (bp)", round(gx.mean()*1e4,1), "n", len(gx), "| all days", round(gap.mean()*1e4,2), "sd", round(gap.std()*1e4,1))
print((gx*1e4).round(1).to_dict())
