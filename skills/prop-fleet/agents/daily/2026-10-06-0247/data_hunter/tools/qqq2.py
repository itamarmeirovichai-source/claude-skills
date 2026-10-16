import sys, pandas as pd, numpy as np
S = sys.argv[1]
q = pd.read_csv(f"{S}/d6/qqq/qqq_1min_mario.csv")
q["ts"] = pd.to_datetime(q["datetime"], utc=True); q["et"] = q.ts.dt.tz_convert("America/New_York")
late = q[q.et.dt.strftime("%H:%M") > "15:59"]
print("bars after 15:59:", len(late), "days", late.et.dt.date.nunique(), late.datetime.head(3).tolist())
a = pd.read_parquet(f"{S}/intraday/qqq_sip.parquet").reset_index()
a["ts"] = pd.to_datetime(a["datetime"], utc=True)
for lag in [-2,-1,0,1,2]:
    b = a[["ts","close"]].copy(); b["ts"] = b.ts + pd.Timedelta(minutes=lag)
    m = q.merge(b.rename(columns={"close":"ca"}), on="ts")
    print("lag", lag, "median |diff|", round(float((m.close-m.ca).abs().median()),4), "exact-to-cent frac", round(float(((m.close-m.ca).abs()<0.0051).mean()),4))
m = q.merge(a[["ts","open","close","volume"]].rename(columns={"open":"oa","close":"ca","volume":"va"}), on="ts")
m["diff"] = m.close - m.ca
print("median diff by month:", m.groupby(m.et.dt.strftime("%Y-%m"))["diff"].median().round(4).to_dict())
print(m[["datetime","close","ca","open","oa","volume","va"]].head(8).to_string())
# daily close (15:59) comparison
d = m[m.et.dt.strftime("%H:%M")=="15:59"]
print("15:59 close diff quantiles", d["diff"].quantile([0.05,0.5,0.95]).round(4).to_dict())
