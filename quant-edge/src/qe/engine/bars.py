"""qe.engine.bars — bar frames, session tagging, resampling, ex-ante daily features, synthetic bars.

Conventions (see CONVENTIONS.md):
  * A bar frame has columns ts (tz-aware UTC, bar OPEN time), open, high, low, close and optionally volume, sorted by ts,
    no duplicate ts. Bars are start-stamped: the 09:30 one-minute bar covers 09:30:00–09:30:59.
  * `tag(bars, root)` adds the session columns from `qe.sessions.tag_minutes`: ny_minute, tday_minute (minutes since the
    18:00 ET reopen), trading_day, in_session, is_rth, has_rth, is_half_day, is_roll_week, rth_close_minute,
    session_close_minute, tday_close_minute, plus day_id (0..n_days-1 integer of trading_day), bar_minutes (bar width).
  * Resampling labels by OPEN time and adds `complete_ts`: the first instant at which the resampled bar is known (open of
    its last constituent + one bar width). Nothing may use a resampled bar before `complete_ts`.
  * `daily_from_bars` builds one row per trading day; `prior_day_features` attaches day d-1's row to every bar of day d, so a
    rule can never read the closing bar of the day it is deciding.
  * Provenance: a frame that comes out of the gateway is marked by `qe.engine.run.run_registered` (attrs["registered_id"]);
    a synthetic frame is marked by `synthetic_walk` (attrs["synthetic"] = True). `qe.engine.pnl.simulate` refuses an
    unmarked frame (non-negotiable 3: no P&L on data that did not pass the door).
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from .. import sessions

REQUIRED = ("ts", "open", "high", "low", "close")
TAG_COLS = ("ny_minute", "tday_minute", "trading_day", "in_session", "is_rth", "has_rth", "is_half_day", "is_roll_week",
            "rth_close_minute", "session_close_minute", "tday_close_minute")


class BarFrameError(ValueError):
    pass


def validate(bars: pd.DataFrame) -> pd.DataFrame:
    """Check the bar-frame contract; returns the frame (sorted copy only if needed)."""
    missing = [c for c in REQUIRED if c not in bars.columns]
    if missing:
        raise BarFrameError(f"bar frame lacks columns {missing}")
    ts = bars["ts"]
    if not isinstance(ts.dtype, pd.DatetimeTZDtype) or str(ts.dt.tz) != "UTC":
        raise BarFrameError("ts must be tz-aware UTC (bar OPEN time)")
    if len(bars) == 0:
        raise BarFrameError("empty bar frame")
    if ts.dt.unit != "ns":                       # pandas >= 3 parses strings to microseconds; the engine works in ns
        attrs = dict(bars.attrs)
        bars = bars.assign(ts=ts.dt.as_unit("ns"))
        bars.attrs.update(attrs)
        ts = bars["ts"]
    if not ts.is_monotonic_increasing:
        bars = bars.sort_values("ts").reset_index(drop=True)
        ts = bars["ts"]
    if ts.duplicated().any():
        raise BarFrameError("duplicate ts in bar frame")
    o, h, l, c = (bars[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    bad = (h < np.maximum(o, c) - 1e-9) | (l > np.minimum(o, c) + 1e-9)
    if bad.any():
        raise BarFrameError(f"{int(bad.sum())} bars with high < max(open, close) or low > min(open, close); first at row {int(np.argmax(bad))}")
    if not np.isfinite(np.c_[o, h, l, c]).all():
        raise BarFrameError("non-finite prices in bar frame")
    return bars


def ts_ns(ts) -> np.ndarray:
    """UTC epoch nanoseconds (int64) of a tz-aware ts column, without an object-dtype round trip."""
    return pd.DatetimeIndex(ts).as_unit("ns").asi8


def ts_take(ts, idx) -> pd.DatetimeIndex:
    """ts[idx] as a UTC DatetimeIndex without the object-dtype round trip of Series.to_numpy()."""
    return pd.DatetimeIndex(pd.DatetimeIndex(ts).as_unit("ns").asi8[np.asarray(idx, np.int64)], tz="UTC")


def infer_bar_minutes(ts: pd.Series) -> int:
    """Bar width in minutes = the most common positive gap between consecutive timestamps (daily bars: 1440 or more)."""
    if len(ts) < 2:
        return 1
    d = np.diff(ts_ns(ts)) // 60_000_000_000
    d = d[d > 0]
    if d.size == 0:
        return 1
    vals, cnt = np.unique(d, return_counts=True)
    return int(vals[np.argmax(cnt)])


def tag(bars: pd.DataFrame, root: str = "ES") -> pd.DataFrame:
    """Attach session tags (qe.sessions) and day_id to an intraday bar frame. Idempotent."""
    bars = validate(bars)
    if all(c in bars.columns for c in TAG_COLS) and "day_id" in bars.columns:
        return bars
    tags = sessions.tag_minutes(bars["ts"], root)
    out = bars.reset_index(drop=True).copy()
    for c in TAG_COLS:
        v = tags[c].to_numpy()
        if v.dtype.kind == "i":
            v = v.astype(np.int16)
        out[c] = v
    out["bar_minutes"] = np.int16(infer_bar_minutes(out["ts"]))
    out["day_id"] = _day_ids(out["trading_day"]).astype(np.int32)
    out.attrs.update(bars.attrs)
    out.attrs["root"] = root
    return out


def tag_daily(bars: pd.DataFrame, root: str = "ES") -> pd.DataFrame:
    """Attach day tags to a daily frame (ts = the trading-day date at 00:00 UTC)."""
    bars = validate(bars)
    out = bars.reset_index(drop=True).copy()
    dates = out["ts"].dt.tz_convert("UTC").dt.tz_localize(None).dt.normalize()
    t = sessions.tag_days(dates, root)
    out["trading_day"] = t["trading_day"].to_numpy()
    out["is_half_day"] = t["is_half_day"].to_numpy()
    out["has_rth"] = t["has_rth"].to_numpy()
    out["is_roll_week"] = t["is_roll_week"].to_numpy()
    out["is_calendar_session"] = t["is_calendar_session"].to_numpy()
    out["in_session"] = True
    out["is_rth"] = True
    out["tday_minute"] = 0
    out["ny_minute"] = 0
    out["tday_close_minute"] = 1440
    out["rth_close_minute"] = 16 * 60
    out["session_close_minute"] = 17 * 60
    out["bar_minutes"] = 1440
    out["day_id"] = np.arange(len(out), dtype=np.int64)
    out.attrs.update(bars.attrs)
    out.attrs["root"] = root
    out.attrs["daily"] = True
    return out


def _day_ids(trading_day: pd.Series) -> np.ndarray:
    codes, _ = pd.factorize(pd.DatetimeIndex(trading_day), sort=True)
    return codes.astype(np.int64)


def day_index(bars: pd.DataFrame) -> pd.DatetimeIndex:
    """Sorted unique trading days aligned with day_id."""
    return pd.DatetimeIndex(np.sort(pd.DatetimeIndex(bars["trading_day"]).unique()))


# ------------------------------------------------------------------------------------------------------ resampling
def resample_intraday(bars: pd.DataFrame, minutes: int) -> pd.DataFrame:
    """Aggregate tagged one-minute bars into `minutes`-wide bars inside each trading day, labelled by OPEN time.

    Buckets are floor(tday_minute / minutes) within the trading day, so no bar straddles the 18:00 ET boundary.
    Columns: ts (open of the first constituent), open, high, low, close, volume (if present), n_bars, complete_ts
    (open of the last constituent + one source bar: the first instant the bar may be read), trading_day, day_id,
    tday_minute (of the bucket start), is_rth / in_session of the first constituent.
    """
    if "day_id" not in bars.columns:
        raise BarFrameError("resample_intraday needs a tagged frame (qe.engine.bars.tag)")
    if minutes <= 0:
        raise ValueError("minutes must be positive")
    src_w = int(bars["bar_minutes"].iloc[0])
    bucket = (bars["tday_minute"].to_numpy() // minutes).astype(np.int64)
    key = bars["day_id"].to_numpy() * 10_000 + bucket
    g = bars.groupby(key, sort=True)
    agg = {"ts": "first", "open": "first", "high": "max", "low": "min", "close": "last", "trading_day": "first",
           "day_id": "first", "is_rth": "first", "in_session": "first", "is_half_day": "first", "is_roll_week": "first",
           "has_rth": "first", "rth_close_minute": "first", "session_close_minute": "first", "tday_close_minute": "first"}
    if "volume" in bars.columns:
        agg["volume"] = "sum"
    out = g.agg(agg)
    out["n_bars"] = g.size().to_numpy()
    last_ts = g["ts"].last()
    out["complete_ts"] = last_ts + pd.Timedelta(minutes=src_w)
    out["tday_minute"] = (g["tday_minute"].first().to_numpy() // minutes) * minutes
    out["ny_minute"] = (out["tday_minute"].to_numpy() + sessions.REOPEN_NY_MINUTE) % sessions.MINUTES_PER_DAY
    out["bar_minutes"] = minutes
    out = out.reset_index(drop=True)
    out.attrs.update(bars.attrs)
    return out


def daily_from_bars(bars: pd.DataFrame, rth_only: bool = False) -> pd.DataFrame:
    """One row per trading day from a tagged intraday frame: open, high, low, close, n_bars, volume, plus the RTH
    open/close when the day has RTH bars. `close` is known only at the session close (complete_ts)."""
    if "day_id" not in bars.columns:
        raise BarFrameError("daily_from_bars needs a tagged frame")
    sub = bars[bars["is_rth"]] if rth_only else bars[bars["in_session"]]
    g = sub.groupby("day_id", sort=True)
    agg = {"trading_day": "first", "open": "first", "high": "max", "low": "min", "close": "last", "ts": "first"}
    if "volume" in sub.columns:
        agg["volume"] = "sum"
    d = g.agg(agg)
    d["n_bars"] = g.size()
    d["complete_ts"] = g["ts"].last() + pd.Timedelta(minutes=int(bars["bar_minutes"].iloc[0]))
    rth = bars[bars["is_rth"]].groupby("day_id", sort=True)
    d["rth_open"] = rth["open"].first()
    d["rth_close"] = rth["close"].last()
    d["rth_high"] = rth["high"].max()
    d["rth_low"] = rth["low"].min()
    d["is_half_day"] = g["is_half_day"].first()
    d["is_roll_week"] = g["is_roll_week"].first()
    d["ret"] = np.log(d["close"]).diff()
    d.index.name = "day_id"
    return d


def prior_day_features(bars: pd.DataFrame, daily: pd.DataFrame, cols=("open", "high", "low", "close", "ret"),
                       lag: int = 1, prefix: str = "prev_") -> pd.DataFrame:
    """Attach day (d - lag)'s daily values to every bar of day d. Values of day d itself are never visible on day d."""
    if lag < 1:
        raise ValueError("lag must be >= 1: the current day's daily bar is not known before its close")
    shifted = daily[list(cols)].shift(lag)
    out = bars.copy()
    m = shifted.reindex(out["day_id"].to_numpy())
    for c in cols:
        out[prefix + c] = m[c].to_numpy()
    out.attrs.update(bars.attrs)
    return out


def ex_ante_daily_vol(daily_ret: np.ndarray, window: int) -> np.ndarray:
    """Trailing standard deviation of the previous `window` daily returns, known at the OPEN of day d (uses days
    d-window .. d-1 only). NaN until `window` returns exist."""
    r = pd.Series(np.asarray(daily_ret, float))
    return r.rolling(window, min_periods=window).std(ddof=1).shift(1).to_numpy()


# ------------------------------------------------------------------------------------------------- synthetic bars
def synthetic_walk(start, end, *, root: str = "ES", sigma_per_min: float = 0.5, drift_per_min: float = 0.0,
                   price0: float = 4000.0, tick: float = 0.25, seed: int = 0, substeps: int = 4,
                   rth_only: bool = False, missing_frac: float = 0.0) -> pd.DataFrame:
    """A driftless (or drifting) random-walk one-minute bar frame on the real CMES/XNYS calendar, tagged, with
    attrs["synthetic"] = True. OHLC come from `substeps` sub-minute steps so high >= max(open, close) >= ... holds.
    Prices are rounded to `tick`. Used by the tests only; never a result."""
    days = sessions.day_table(start, end, root)
    if rth_only:
        days = days[days["has_rth"]]
        opens = days["rth_open_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
        closes = days["rth_close_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
    else:
        opens = days["session_open_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
        closes = days["session_close_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
    n_per_day = ((closes - opens) // 60_000_000_000).astype(np.int64)
    total = int(n_per_day.sum())
    day_start = np.repeat(opens, n_per_day)
    offsets = np.arange(total) - np.repeat(np.cumsum(n_per_day) - n_per_day, n_per_day)
    ts_ns = day_start + offsets * 60_000_000_000
    rng = np.random.default_rng(seed)
    steps = rng.standard_normal((total, substeps)) * (sigma_per_min / np.sqrt(substeps)) + drift_per_min / substeps
    path = np.cumsum(steps.ravel())
    path = (price0 + path).reshape(total, substeps)
    o = np.empty(total)
    o[0] = price0
    o[1:] = path[:-1, -1]
    c = path[:, -1]
    h = np.maximum(path.max(axis=1), o)
    l = np.minimum(path.min(axis=1), o)
    if tick:
        o, h, l, c = (np.round(x / tick) * tick for x in (o, h, l, c))
        h = np.maximum(h, np.maximum(o, c))
        l = np.minimum(l, np.minimum(o, c))
    df = pd.DataFrame({"ts": pd.to_datetime(ts_ns, utc=True), "open": o, "high": h, "low": l, "close": c,
                       "volume": rng.integers(100, 1000, size=total)})
    if missing_frac > 0:
        keep = rng.random(total) >= missing_frac
        df = df[keep].reset_index(drop=True)
    df.attrs["synthetic"] = True
    df.attrs["synthetic_params"] = dict(sigma_per_min=sigma_per_min, drift_per_min=drift_per_min, seed=seed, substeps=substeps)
    return tag(df, root)


def synthetic_daily_walk(start, end, *, root: str = "ES", sigma: float = 0.01, drift: float = 0.0, price0: float = 100.0,
                         seed: int = 0) -> pd.DataFrame:
    """A daily random-walk frame (log prices) on the CMES calendar, attrs["synthetic"] = True."""
    days = sessions.day_table(start, end, root)
    n = len(days)
    rng = np.random.default_rng(seed)
    r = rng.standard_normal(n) * sigma + drift
    c = price0 * np.exp(np.cumsum(r))
    o = np.r_[price0, c[:-1]]
    intra = np.abs(rng.standard_normal(n)) * sigma * 0.5
    h = np.maximum(o, c) * (1 + intra)
    l = np.minimum(o, c) * (1 - intra)
    df = pd.DataFrame({"ts": pd.DatetimeIndex(days.index).tz_localize("UTC"), "open": o, "high": h, "low": l, "close": c})
    df.attrs["synthetic"] = True
    return tag_daily(df, root)
