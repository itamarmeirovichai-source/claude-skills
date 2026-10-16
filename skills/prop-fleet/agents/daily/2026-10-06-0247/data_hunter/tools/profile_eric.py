import sys, glob, pandas as pd, numpy as np
d = sys.argv[1]
for sym in ["nq", "es"]:
    fs = sorted(glob.glob(f"{d}/{sym}_1m_20*.parquet"))
    df = pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    print("=====", sym, "files", len(fs), "rows", len(df))
    print("columns", list(df.columns), "dtypes", dict(df.dtypes.astype(str)))
    print(df.head(3).to_string()); print(df.tail(2).to_string())
    ts = pd.to_datetime(df["ts_event"])
    print("tz", ts.dt.tz, "first", ts.min(), "last", ts.max())
    print("dup ts", ts.duplicated().sum(), "symbols", df["symbol"].value_counts().to_dict() if "symbol" in df else None)
    print("instrument_id changes", (df["instrument_id"].diff()!=0).sum()-1)
    bad = ((df.high < df[["open","close"]].max(axis=1)) | (df.low > df[["open","close"]].min(axis=1)) | (df.low>df.high)).sum()
    print("bad ohlc", bad, "zero vol", (df.volume==0).sum(), "off-tick(0.25)", (((df[["open","high","low","close"]]*4) % 1).abs()>1e-6).any(axis=1).sum())
    ny = ts.dt.tz_convert("America/New_York")
    rth = df[(ny.dt.time >= pd.Timestamp("09:30").time()) & (ny.dt.time <= pd.Timestamp("15:59").time()) & (ny.dt.weekday < 5)].copy()
    rth["d"] = ny[rth.index].dt.date
    cnt = rth.groupby("d").size()
    print("RTH days", len(cnt), "per year", cnt.groupby(pd.to_datetime(cnt.index).year).size().to_dict())
    print("RTH days with 390 bars", (cnt==390).sum(), ">=380", (cnt>=380).sum(), "<370", (cnt<370).sum())
    has930 = rth[ny[rth.index].dt.strftime("%H:%M")=="09:30"].groupby("d").size()
    has1559 = rth[ny[rth.index].dt.strftime("%H:%M")=="15:59"].groupby("d").size()
    print("days with 09:30 bar", len(has930), "with 15:59 bar", len(has1559))
    # weekday gaps: business days with no RTH bars
    alld = pd.bdate_range(ts.min().tz_convert("America/New_York").date(), ts.max().tz_convert("America/New_York").date())
    missing = sorted(set(alld.date) - set(cnt.index))
    print("weekdays without RTH bars", len(missing), [str(x) for x in missing][:80])
    # largest gaps in continuous trading (exclude weekends)
    g = ts.diff().dt.total_seconds()/60
    big = df.loc[g > 60*3, "ts_event"]
    gg = pd.DataFrame({"after": ts.shift(1)[g>180], "before": ts[g>180], "min": g[g>180]})
    gg = gg[~((gg["after"].dt.tz_convert("America/New_York").dt.weekday==4) & (gg["min"] < 60*50))]
    print("non-weekend gaps > 3h:", len(gg)); print(gg.sort_values("min", ascending=False).head(25).to_string())
    for a,b in [("2020-05-15","2020-08-30")]:
        m = cnt[(pd.to_datetime(cnt.index) >= a) & (pd.to_datetime(cnt.index) <= b)]
        print(f"window {a}..{b}: RTH days {len(m)}, median bars {m.median()}, min {m.min()}")
    # roll dates
    rid = df.loc[df["instrument_id"].diff().fillna(0)!=0, ["ts_event","instrument_id"]]
    print("rolls (first 40):", [str(pd.Timestamp(t).tz_convert('America/New_York').date()) for t in rid.ts_event][:40])
