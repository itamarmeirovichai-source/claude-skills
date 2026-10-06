"""Literature scout, 2026-10-05: COST-SIDE and SAMPLE-SIZE feasibility only.

Computes NO strategy P&L, no signal-conditioned return, nothing that spends N.
1. VWAP trend (Zarattini & Aziz 2023): how often the 1m close crosses the
   session VWAP (09:30-15:59 ET) = position flips per day; turned into a
   cost per day using the board's ES round trip of 0.6 pt (day-1 run.txt),
   expressed in bp with ES ~= 10 x SPY, and next to the median |open->close|.
2. Gamma-conditioned intraday momentum (Baltussen et al. 2021): how many
   sample days have the PREVIOUS day's SqueezeMetrics GEX < 0 (lagged one day).
Inputs (sha256-pinned in daily/2026-10-04/data_fetch.py, and gex6.csv below):
  SPY 1m RTH 2019-2025  Ascensao/Intraday-momentum-strategy@5a9e956 spy_intra_data.csv
  NQ 1m 2020-08..2025-11 hindsight-finance/Silver-Bullet-AM-Session@9f00a85 nq_1m.parquet
  GEX daily 2011-05-02..2026-10-02 Fluxus-Trade-Lab/fluxus-dashboard@c1eb927 SqueezeMetrics/DIX.csv
     sha256 51bef9ea5ee13af2f72b14f4198de57eeb865a36c1d3e244a3f64b3603e9ce62
Usage: python feasibility.py <dir with asc_spy_rth.csv nq_1m_hind.parquet gex6.csv>
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(sys.argv[1])
ES_RT_PT = 0.6  # board / day-1 run.txt round-trip cost assumption for ES


def vwap_flips(df, t, o, h, l, c, v):
    df = df.copy()
    df["day"] = df[t].dt.date
    tm = df[t].dt.strftime("%H:%M")
    df = df[(tm >= "09:30") & (tm <= "15:59")]
    tp = (df[h] + df[l] + df[c]) / 3
    df["pv"] = tp * df[v]
    g = df.groupby("day")
    vw = g["pv"].cumsum() / g[v].cumsum().replace(0, np.nan)
    side = np.sign(df[c] - vw)
    side = side.replace(0, np.nan).groupby(df["day"]).ffill()
    flips = (side != side.groupby(df["day"]).shift()) & side.groupby(df["day"]).shift().notna()
    per_day = flips.groupby(df["day"]).sum()
    oc = g.apply(lambda x: abs(x[c].iloc[-1] / x[o].iloc[0] - 1) * 1e4)
    px = g[c].last()
    return per_day, oc, px


spy = pd.read_csv(D / "asc_spy_rth.csv", parse_dates=["caldt"])
f, oc, px = vwap_flips(spy, "caldt", "open", "high", "low", "close", "volume")
entries = f + 1  # first entry plus every flip
cost_bp = entries * ES_RT_PT / (10 * px) * 1e4
print("SPY 1m 2019-01-02..2025-07-18 RTH days:", len(f))
print("  VWAP entries/day  median %.0f  mean %.1f  p90 %.0f" % (entries.median(), entries.mean(), entries.quantile(.9)))
print("  cost/day at 0.6 ES pt per round trip (ES~10xSPY): median %.1f bp  mean %.1f bp" % (cost_bp.median(), cost_bp.mean()))
print("  median |open->close| %.1f bp ; mean %.1f bp" % (oc.median(), oc.mean()))
print("  by year, mean entries/day:", entries.groupby(pd.to_datetime(entries.index).year).mean().round(1).to_dict())

nq = pd.read_parquet(D / "nq_1m_hind.parquet")
nq["DateTime_ET"] = pd.to_datetime(nq["DateTime_ET"])
f2, oc2, px2 = vwap_flips(nq, "DateTime_ET", "Open", "High", "Low", "Close", "Volume")
e2 = f2 + 1
print("NQ 1m RTH 2020-08-31..2025-11-21 days:", len(f2))
print("  VWAP entries/day  median %.0f  mean %.1f  p90 %.0f" % (e2.median(), e2.mean(), e2.quantile(.9)))
print("  median |open->close| %.1f bp" % oc2.median())

gex = pd.read_csv(D / "gex6.csv", parse_dates=["date"]).set_index("date")["gex"]
lag = gex.shift(1)  # yesterday's published value -> no look-ahead
days = pd.to_datetime(pd.Index(f.index))
lg = lag.reindex(days)
print("GEX rows %d  %s..%s" % (len(gex), gex.index[0].date(), gex.index[-1].date()))
print("SPY sample days with lagged GEX available: %d ; lagged GEX<0: %d" % (lg.notna().sum(), (lg < 0).sum()))
print("  lagged GEX<0 days by year:", (lg < 0).groupby(lg.index.year).sum().to_dict())
lagall = lag[lag.index >= "2011-05-03"]
print("All 2011-05-03..2026-10-02 lagged GEX<0 days: %d of %d" % ((lagall < 0).sum(), lagall.notna().sum()))
