import sys, pandas as pd, numpy as np
S = sys.argv[1]
q = pd.read_csv(f"{S}/d6/qqq/qqq_1min_mario.csv")
print("columns", list(q.columns), "rows", len(q))
q["ts"] = pd.to_datetime(q["datetime"], utc=True)
q["et"] = q.ts.dt.tz_convert("America/New_York")
print("first", q.et.min(), "last", q.et.max(), "dup", q.ts.duplicated().sum())
print("time-of-day min/max", q.et.dt.strftime("%H:%M").min(), q.et.dt.strftime("%H:%M").max())
offs = q["datetime"].str[-6:].value_counts().to_dict(); print("offsets", offs)
q["d"] = q.et.dt.date
cnt = q.groupby("d").size()
print("days", len(cnt), "per year", cnt.groupby(pd.to_datetime(cnt.index).year).size().to_dict())
print("bars/day: ==390", (cnt==390).sum(), "==210", (cnt==210).sum(), "<380", (cnt<380).sum(), "median", cnt.median())
print("short days (not 210/390), first 30:", {str(k): int(v) for k, v in cnt[(cnt!=390)&(cnt!=210)].head(30).items()})
alld = pd.bdate_range(cnt.index.min(), cnt.index.max())
miss = sorted(set(alld.date) - set(cnt.index))
print("weekdays missing", len(miss)); 
# missing weekdays that are not NYSE holidays: crude list printing by year
print([str(x) for x in miss])
bad = ((q.high < q[["open","close"]].max(axis=1)) | (q.low > q[["open","close"]].min(axis=1))).sum()
print("bad ohlc", bad, "zero vol", (q.volume==0).sum())
dec = (q.close*100 - (q.close*100).round()).abs() > 1e-6
print("close not on 1-cent grid frac", round(float(dec.mean()),4), "by year", dec.groupby(q.et.dt.year).mean().round(3).to_dict())
# compare to raw sources: Alpaca SIP QQQ (raw) and IBKR
a = pd.read_parquet(f"{S}/intraday/qqq_sip.parquet")
print("alpaca cols", list(a.columns)[:10], a.index.name)
a = a.reset_index()
tc = [c for c in a.columns if "time" in c.lower() or "date" in c.lower() or c=="index"][0]
a["ts"] = pd.to_datetime(a[tc], utc=True)
cc = [c for c in a.columns if c.lower() in ("close","c")][0]
m = q.merge(a[["ts", cc]].rename(columns={cc:"close_a"}), on="ts")
m["ratio"] = m.close / m.close_a
r = m.groupby(m.et.dt.to_period("M"))["ratio"].agg(["min","max","count"])
print("ratio mario/alpaca by month:"); print(r.round(5).to_string())
print("1m ret corr", round(float(np.corrcoef(m.close.pct_change().iloc[1:], m.close_a.pct_change().iloc[1:])[0,1]),4))
i = pd.read_csv(f"{S}/d5f/intraday/qqq_1m_ibkr.csv")
i["ts"] = pd.to_datetime(i["date"], utc=True)
mi = q.merge(i[["ts","close","volume"]].rename(columns={"close":"close_i","volume":"vol_i"}), on="ts")
print("vs IBKR rows", len(mi), "ratio min/max", round(float((mi.close/mi.close_i).min()),5), round(float((mi.close/mi.close_i).max()),5), "vol ratio median", round(float((mi.volume/mi.vol_i).median()),3))
