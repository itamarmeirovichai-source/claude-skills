"""FX plumbing for Q-0001 / Q-0003 (Dept D, 2026-11-06): local clocks, daily 17:00 New York closes, the EWMA
volatility through the close before an instant, the CME venue cost, and the bar lookup helpers. No rule content.

HistData bars: ts = bar OPEN in UTC (manifest: clock ny_dst converted, shift 0); bid quotes; weekend rows kept.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

NY, LON, PRG = "America/New_York", "Europe/London", "Europe/Prague"
TARGET_DAILY = 0.10 / math.sqrt(252)


def ts_ns(bars: pd.DataFrame) -> np.ndarray:
    return pd.DatetimeIndex(bars["ts"]).as_unit("ns").asi8


def local_instant(date, hhmm: str, tz: str) -> pd.Timestamp:
    """UTC instant of wall-clock `hhmm` on calendar `date` in zone `tz` (zoneinfo via pandas)."""
    h, m = (int(x) for x in hhmm.split(":"))
    return pd.Timestamp(pd.Timestamp(date).date()).replace(hour=h, minute=m).tz_localize(tz).tz_convert("UTC")


def ny_closes(bars: pd.DataFrame) -> pd.DataFrame:
    """One row per New York weekday: the 17:00 NY close = close of the last bar opening before 17:00 NY that date.
    Columns: close, instant (UTC 17:00 NY of that date), r (log return vs the previous row, NaN when the previous
    close is more than 5 calendar days earlier)."""
    ts = pd.DatetimeIndex(bars["ts"]).tz_convert(NY)
    mins = ts.hour * 60 + ts.minute
    keep = (mins < 17 * 60) & (ts.dayofweek < 5)
    d = pd.DataFrame({"date": ts.normalize().tz_localize(None)[keep], "close": bars["close"].to_numpy(float)[keep]})
    c = d.groupby("date")["close"].last()
    inst = pd.DatetimeIndex(c.index).tz_localize(NY) + pd.Timedelta(hours=17)
    out = pd.DataFrame({"close": c.to_numpy(), "instant": inst.tz_convert("UTC")}, index=c.index)
    gap = out.index.to_series().diff().dt.days
    r = np.log(out["close"]).diff()
    r[gap > 5] = np.nan
    out["r"] = r
    return out


def ewm_sd(closes: pd.DataFrame, com: float) -> pd.Series:
    return closes["r"].ewm(com=com, min_periods=int(com)).std()


def value_before(closes: pd.DataFrame, series: pd.Series, instant: pd.Timestamp) -> float:
    """series value at the last close whose 17:00 NY instant is strictly before `instant`."""
    inst = pd.DatetimeIndex(closes["instant"]).as_unit("ns").asi8
    k = np.searchsorted(inst, pd.Timestamp(instant).as_unit("ns").value, side="left") - 1
    if k < 0:
        return float("nan")
    return float(series.iloc[k])


def bar_at(tsn: np.ndarray, instant: pd.Timestamp) -> int:
    """Index of the bar opening exactly at `instant`, or -1."""
    v = pd.Timestamp(instant).as_unit("ns").value
    k = np.searchsorted(tsn, v)
    return int(k) if k < tsn.size and tsn[k] == v else -1


def bar_at_or_after(tsn: np.ndarray, instant: pd.Timestamp, before: pd.Timestamp = None) -> int:
    v = pd.Timestamp(instant).as_unit("ns").value
    k = np.searchsorted(tsn, v)
    if k >= tsn.size:
        return -1
    if before is not None and tsn[k] >= pd.Timestamp(before).as_unit("ns").value:
        return -1
    return int(k)


def count_bars(tsn: np.ndarray, a: pd.Timestamp, b: pd.Timestamp) -> int:
    """Bars with open in [a, b] (both inclusive)."""
    lo = np.searchsorted(tsn, pd.Timestamp(a).as_unit("ns").value, side="left")
    hi = np.searchsorted(tsn, pd.Timestamp(b).as_unit("ns").value, side="right")
    return int(hi - lo)


# CME venue sensitivity: 1 tick + $2.50 commission per side, as a fraction of notional at the fill price.
# 6A tick $.0001 until 2020-11-21, $.00005 from 2020-11-22 (CME SER 8648); 6E $.00005 (125,000 EUR); 6B $.0001 (62,500 GBP).
CME = {"EURUSD": ("6E", 125_000), "GBPUSD": ("6B", 62_500), "AUDUSD": ("6A", 100_000)}


def cme_tick(pair: str, date) -> float:
    if pair == "EURUSD":
        return 0.00005
    if pair == "GBPUSD":
        return 0.0001
    return 0.0001 if pd.Timestamp(date) < pd.Timestamp("2020-11-22") else 0.00005


def cme_cost_frac(pair: str, date, price: float) -> float:
    size = CME[pair][1]
    return cme_tick(pair, date) / price + 2.50 / (size * price)


def tag_for_harness(bars: pd.DataFrame) -> pd.DataFrame:
    """day_id / trading_day for the qe.engine harness: the CME-style trading day (New York date of ts + 6 h, so bars
    from 18:00 NY belong to the next day). Market data untouched."""
    ny = pd.DatetimeIndex(bars["ts"]).tz_convert(NY)
    td = (ny + pd.Timedelta(hours=6)).normalize().tz_localize(None)
    out = bars[["ts", "open", "high", "low", "close"]].reset_index(drop=True).copy()
    out["trading_day"] = td
    out["day_id"] = pd.factorize(td, sort=True)[0]
    return out
