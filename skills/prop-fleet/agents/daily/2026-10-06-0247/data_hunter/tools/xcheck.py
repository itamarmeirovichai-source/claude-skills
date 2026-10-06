import glob, sys, pandas as pd, numpy as np
S = sys.argv[1]
def load(sym):
    return pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{S}/d6/eric/{sym}_1m_20*.parquet"))], ignore_index=True)
es = load("es"); nq = load("nq")
# 1) ES Eric vs Warrenn (both Databento ES.c.0)
w = pd.read_parquet(f"{S}/d5f/intraday/es_1m_databento.parquet")
w["ts_event"] = pd.to_datetime(w["ts_event"], utc=True)
m = es.merge(w, on="ts_event", suffixes=("", "_w"))
print("ES Eric vs Warrenn overlap rows", len(m), "of Warrenn", len(w))
for c in ["open","high","low","close","volume","instrument_id"]:
    print("  equal", c, round(float((m[c]==m[c+"_w"]).mean()), 6))
# 2) ES Eric RTH close vs FirstRate RTH (ET naive)
fr = pd.read_parquet(f"{S}/d5f/intraday/es_1m_rth.parquet")
print("FirstRate cols", list(fr.columns)[:8])
tcol = [c for c in fr.columns if "date" in c.lower() or "time" in c.lower() or c=="ts"]
fr = fr.reset_index() if not tcol else fr
tcol = [c for c in fr.columns if "date" in c.lower() or "time" in c.lower() or c in ("ts","index")][0]
fr["et"] = pd.to_datetime(fr[tcol])
es["et"] = es.ts_event.dt.tz_convert("America/New_York").dt.tz_localize(None)
cc = [c for c in fr.columns if c.lower()=="close"][0]
j = es.merge(fr[["et", cc]].rename(columns={cc:"close_fr"}), on="et")
j["d"] = j.et.dt.date
dd = (j.close - j.close_fr).groupby(j.d).median()
print("ES Eric vs FirstRate RTH joined minutes", len(j), "days", len(dd), "days median diff 0:", int((dd==0).sum()), "exact close frac", round(float((j.close==j.close_fr).mean()),4))
print("  nonzero-day years", pd.Series([d.year for d in dd[dd!=0].index]).value_counts().sort_index().to_dict())
# 3) NQ Eric vs hindsight NQ 1m
h = pd.read_parquet(f"{S}/dh/nq_1m_hind.parquet")
print("hindsight cols", list(h.columns))
tc = [c for c in h.columns if "utc" in c.lower()] or [c for c in h.columns if "time" in c.lower() or "date" in c.lower()]
h["ts_event"] = pd.to_datetime(h[tc[0]], utc=True)
hc = [c for c in h.columns if c.lower()=="close"][0]
k = nq.merge(h[["ts_event", hc]].rename(columns={hc:"close_h"}), on="ts_event")
k["d"] = k.ts_event.dt.tz_convert("America/New_York").dt.date
kd = (k.close - k.close_h).groupby(k.d).median()
print("NQ Eric vs hindsight joined", len(k), "days", len(kd), "days median diff 0:", int((kd==0).sum()), "exact close frac", round(float((k.close==k.close_h).mean()),4))
print("  nonzero days sample", {str(a): float(b) for a, b in kd[kd!=0].head(12).items()})
# 4) roll-week flag: days in the 8 calendar days before the c.0 roll where RTH volume is low vs median
for name, df in [("ES", es), ("NQ", nq)]:
    ny = df.ts_event.dt.tz_convert("America/New_York")
    r = df[(ny.dt.strftime("%H:%M")>="09:30") & (ny.dt.strftime("%H:%M")<="15:59")]
    vol = r.groupby(ny[r.index].dt.date)["volume"].sum()
    roll = df.loc[df.instrument_id.diff().fillna(0)!=0, "ts_event"].dt.tz_convert("America/New_York").dt.date.tolist()
    ratios = []
    for rd in roll:
        pre = vol[(pd.to_datetime(vol.index) < pd.Timestamp(rd)) & (pd.to_datetime(vol.index) >= pd.Timestamp(rd) - pd.Timedelta(days=10))]
        base = vol[(pd.to_datetime(vol.index) < pd.Timestamp(rd) - pd.Timedelta(days=14)) & (pd.to_datetime(vol.index) >= pd.Timestamp(rd) - pd.Timedelta(days=44))].median()
        ratios.append((pre / base).round(2).tolist())
    print(name, "RTH volume / prior-month median, last ~7 sessions before each c.0 roll (first 4 rolls):", ratios[:4])
