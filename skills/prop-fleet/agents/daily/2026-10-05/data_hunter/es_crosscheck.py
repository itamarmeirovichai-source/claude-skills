#!/usr/bin/env python3
"""Data hunter 2026-10-05: cross-check the newly found ES 1m RTH file.

Inputs (all in scratch, never in the repo):
  es1_rth.parquet  jimmuell/mes-orb-strategy@48993b9c api/data/ES_full_1min_rth.parquet
                   (FirstRateData ES continuous UNadjusted, ET naive, RTH 09:30-15:59)
  intraday/spy_rth.csv    daily/2026-10-04/data_fetch.py spy_rth (SPY 1m RTH, ET naive)
  intraday/es_1m_2026.csv daily/2026-10-04/data_fetch.py es_1m_2026 (TopstepX ES 1m, UTC)

    python3 es_crosscheck.py <scratch_dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

d = Path(sys.argv[1])
es = pd.read_parquet(d / "es1_rth.parquet")
es.columns = [c.lower() for c in es.columns]

# ---- 1. ES (FirstRate via jimmuell) vs ES (TopstepX via axb0306), same minutes
tx = pd.read_csv(d / "intraday/es_1m_2026.csv")
tcol = tx.columns[0]
tx.index = (pd.to_datetime(tx[tcol], utc=True).dt.tz_convert("America/New_York")
            .dt.tz_localize(None))
tx = tx[~tx.index.duplicated()]
j = es.join(tx[["close", "volume"]], rsuffix="_tx", how="inner")
diff = (j["close"] - j["close_tx"])
print("== ES FirstRate vs ES TopstepX (ET), overlapping RTH minutes")
print("rows joined", len(j), "first", j.index.min(), "last", j.index.max())
print("close exact-match frac %.4f" % (diff.abs() < 1e-9).mean())
by_day = diff.groupby(j.index.normalize()).median()
print("days", len(by_day), "days with median diff 0:", int((by_day == 0).sum()))
print("non-zero median-diff days:\n", by_day[by_day != 0].to_string())
vr = (j["volume"] / j["volume_tx"]).replace([np.inf, -np.inf], np.nan)
print("volume ratio FirstRate/TopstepX median %.3f" % vr.median())

# ---- 2. ES vs SPY 2019-01-02..2025-07-18
spy = pd.read_csv(d / "intraday/spy_rth.csv", parse_dates=["caldt"]).set_index("caldt")
spy = spy[~spy.index.duplicated()]
k = es[["open", "close"]].join(spy[["open", "close"]], rsuffix="_spy", how="inner")
print("\n== ES vs SPY, shared RTH minutes")
print("rows", len(k), "first", k.index.min(), "last", k.index.max())
r_es = np.log(k["close"]).diff()
r_sp = np.log(k["close_spy"]).diff()
same_day = pd.Series(k.index.normalize(), index=k.index).eq(
    pd.Series(k.index.normalize(), index=k.index).shift())
m = same_day & r_es.notna() & r_sp.notna()
print("1m log-return corr (intraday only): %.4f" % np.corrcoef(r_es[m], r_sp[m])[0, 1])

day = k.groupby(k.index.normalize()).agg(
    es_o=("open", "first"), es_c=("close", "last"),
    sp_o=("open_spy", "first"), sp_c=("close_spy", "last"))
oc_es = np.log(day.es_c / day.es_o)
oc_sp = np.log(day.sp_c / day.sp_o)
print("sessions", len(day))
print("daily open->close corr %.4f ; mean |diff| %.5f" % (
    oc_es.corr(oc_sp), (oc_es - oc_sp).abs().mean()))
g_es = np.log(day.es_o / day.es_c.shift())
g_sp = np.log(day.sp_o / day.sp_c.shift())
gd = (g_es - g_sp).dropna()
print("overnight gap (09:30 open vs prior 15:59 close) corr %.4f" % g_es.corr(g_sp))
print("gap diff ES-SPY: median %.5f, p95 |diff| %.5f" % (gd.median(), gd.abs().quantile(.95)))
big = gd[gd.abs() > 0.005]
print("sessions with |ES gap - SPY gap| > 0.5%%: %d" % len(big))
print(big.round(4).to_string())
