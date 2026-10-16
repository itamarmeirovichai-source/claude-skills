#!/usr/bin/env python3
"""Data hunter 2026-10-05: profile two more sources and cross-check them.

  es_intraday_warrenn.parquet  Warrenn/ibkr-bull-call@ff3cc44f research/data/dataset-v1/es_intraday.parquet
                               (Databento GLBX.MDP3 ES.c.0 ohlcv-1m per docs/data-inventory.md)
  spy_ibkr.csv / qqq_ibkr.csv  kfhoo88/ibkr-scalper@da900822 data/historical/{SPY,QQQ}_IBKR_1min_1year_20251110.csv
  es1_rth.parquet              jimmuell/mes-orb-strategy@48993b9c api/data/ES_full_1min_rth.parquet
  intraday/spy_rth.csv         daily/2026-10-04/data_fetch.py spy_rth

    python3 second_sources.py <scratch_dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

d = Path(sys.argv[1])


def sessions(idx):
    s = pd.Series(1, index=idx)
    return s.groupby(idx.normalize()).size()


w = pd.read_parquet(d / "es_intraday_warrenn.parquet")
print("== Warrenn ES parquet: columns", list(w.columns), "index", w.index.dtype, w.index.name)
print(w.head(3).to_string()); print(w.tail(2).to_string())
tcol = None
if not isinstance(w.index, pd.DatetimeIndex):
    tcol = [c for c in w.columns if "ts" in c.lower() or "time" in c.lower() or "date" in c.lower()][0]
    w = w.set_index(tcol)
idx = pd.DatetimeIndex(w.index)
if idx.tz is None:
    idx = idx.tz_localize("UTC")
w.index = idx.tz_convert("America/New_York").tz_localize(None)
w = w[~w.index.duplicated()]
print("rows", len(w), "first", w.index.min(), "last", w.index.max())
es = pd.read_parquet(d / "es1_rth.parquet")
j = es.join(w[["close", "volume"]], how="inner")
diff = j["Close"] - j["close"]
print("joined RTH minutes vs FirstRate", len(j), "close exact-match frac %.4f" % (diff.abs() < 1e-9).mean())
bd = diff.groupby(j.index.normalize()).median()
print("days", len(bd), "days median diff 0:", int((bd == 0).sum()))
print("non-zero days:", bd[bd != 0].round(2).to_dict())
print("volume equal frac %.4f" % (j["Volume"] == j["volume"]).mean())

for name in ["spy_ibkr.csv", "qqq_ibkr.csv"]:
    x = pd.read_csv(d / name)
    x.index = pd.to_datetime(x["date"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    s = sessions(x.index)
    t = x.index.time
    print(f"\n== {name}: rows {len(x)} first {x.index.min()} last {x.index.max()} sessions {len(s)}")
    print("columns", list(x.columns))
    print("bars/session: full390", int((s == 390).sum()), "short", s[s < 390].to_dict())
    print("time range", min(t), max(t))
    bad = ((x.high < x[["open", "close"]].max(axis=1)) | (x.low > x[["open", "close"]].min(axis=1))).sum()
    print("bad ohlc", int(bad), "zero vol", int((x.volume == 0).sum()))
    bd_ = pd.bdate_range(s.index.min(), s.index.max())
    print("missing weekdays", [str(z.date()) for z in bd_.difference(s.index)])
    if name == "spy_ibkr.csv":
        a = pd.read_csv(d / "intraday/spy_rth.csv", parse_dates=["caldt"]).set_index("caldt")
        k = x[["close", "volume"]].join(a[["close", "volume"]], rsuffix="_asc", how="inner")
        ratio = k["close_asc"] / k["close"]
        print("overlap with Ascensao SPY:", len(k), k.index.min(), "..", k.index.max())
        print("price ratio Ascensao/IBKR by month (min,max):")
        print(ratio.groupby(k.index.to_period("M")).agg(["min", "max"]).round(4).to_string())
        print("1m return corr %.4f" % np.log(k["close"]).diff().corr(np.log(k["close_asc"]).diff()))
        print("volume ratio IBKR/Ascensao median %.3f" % (k["volume"] / k["volume_asc"]).median())
