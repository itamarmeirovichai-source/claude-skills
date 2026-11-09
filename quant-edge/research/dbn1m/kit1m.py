"""Shared plumbing for the Databento 1-minute rows Q-0017..Q-0021 (written after their registration commit 56c0f6f).

A frame per root: sorted 1m bars with naive America/New_York bar-open times (`et`), open/close/volume/iid arrays.
Price conventions are the registered ones:
- P(T)        = CLOSE of the latest bar opening in [T-5min, T-1min] (last trade before T), else NaN.
- open_at(T)  = OPEN of the first bar opening in [T, T+5min) (first trade at or after T), else NaN.
- exit_px(T)  = CLOSE of the latest bar opening before T (no 5-minute limit; used where the row says an exit in a halt
                uses the last bar before it).
Every price comes with its instrument_id so the roll rule (same instrument_id on both legs) can be applied.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))
sys.path.insert(0, str(HERE.parent / "dbn1h"))
from qe import gateway  # noqa: E402
import kit  # noqa: E402  (gate statistics, sessions, ewma_prev, cost_frac, verdict, power_line)

NY = "America/New_York"
MIN = np.timedelta64(1, "m")
POINT = {"ES": 50.0, "GC": 100.0, "MES": 5.0}


class Frame:
    def __init__(self, df: pd.DataFrame):
        df = df.sort_values("ts").drop_duplicates("ts")
        self.df = df.reset_index(drop=True)
        self.et = df["ts"].dt.tz_convert(NY).dt.tz_localize(None).to_numpy("datetime64[ns]")
        self.open = df["open"].to_numpy(float)
        self.close = df["close"].to_numpy(float)
        self.vol = df["volume"].to_numpy(float)
        self.iid = df["instrument_id"].to_numpy().astype(np.int64)

    def subset(self, mask):
        f = Frame.__new__(Frame)
        f.df = None
        f.et, f.open, f.close, f.vol, f.iid = self.et[mask], self.open[mask], self.close[mask], self.vol[mask], self.iid[mask]
        return f

    def P(self, T):
        T = np.asarray(T, "datetime64[ns]")
        i = np.searchsorted(self.et, T - MIN, side="right") - 1
        ok = (i >= 0)
        i2 = np.where(ok, i, 0)
        ok &= self.et[i2] >= T - 5 * MIN
        return np.where(ok, self.close[i2], np.nan), np.where(ok, self.iid[i2], -1)

    def open_at(self, T):
        T = np.asarray(T, "datetime64[ns]")
        i = np.searchsorted(self.et, T, side="left")
        ok = i < len(self.et)
        i2 = np.where(ok, i, 0)
        ok &= self.et[i2] < T + 5 * MIN
        return np.where(ok, self.open[i2], np.nan), np.where(ok, self.iid[i2], -1)

    def exit_px(self, T):
        T = np.asarray(T, "datetime64[ns]")
        i = np.searchsorted(self.et, T, side="left") - 1
        ok = i >= 0
        i2 = np.where(ok, i, 0)
        return np.where(ok, self.close[i2], np.nan), np.where(ok, self.iid[i2], -1)

    def vol_between(self, T0, T1):
        """Sum of volume of bars opening in [T0, T1)."""
        c = np.concatenate([[0.0], np.cumsum(self.vol)])
        a = np.searchsorted(self.et, np.asarray(T0, "datetime64[ns]"), side="left")
        b = np.searchsorted(self.et, np.asarray(T1, "datetime64[ns]"), side="left")
        return c[b] - c[a]


def load(rid, datasets, windows):
    """One gateway read per dataset per window (each logged); returns {root: Frame}."""
    out = {}
    for ds in datasets:
        parts = [gateway.load(rid, w, dataset=ds) for w in windows]
        df = pd.concat(parts, ignore_index=True)
        out[ds.rsplit("_", 1)[-1]] = Frame(df)
    return out


def at(days, hhmm):
    """Naive ET datetime64 for each date at HH:MM."""
    h, m = map(int, hhmm.split(":"))
    return (pd.to_datetime(pd.Series(days)) + pd.Timedelta(hours=h, minutes=m)).to_numpy("datetime64[ns]")


def full_days(start, end):
    days, early = kit.sessions(start, end)
    return [d for d in days if d not in early], early, days


def cost(price, slip, root, mult=1.0):
    return kit.cost_frac(price, slip, POINT[root], 2.50, mult)


def crit7(x, dates, terc_vals, terc_bounds, neighbours, delay_mean):
    """PARAMETERS.md criteria 4 and 7 on a net-1x series; returns (ok, detail dict)."""
    s = pd.Series(np.asarray(x, float), index=pd.to_datetime(pd.Series(dates)).values)
    yr = s.groupby(s.index.year).sum()
    pos_share = float((yr > 0).mean()) if len(yr) else 0.0
    tot = float(s.sum())
    max_year_share = float(yr.max() / tot) if tot > 0 else float("nan")
    lo, hi = terc_bounds
    tv = np.asarray(terc_vals, float)
    terc = [float(s.values[tv <= lo].sum()), float(s.values[(tv > lo) & (tv <= hi)].sum()), float(s.values[tv > hi].sum())]
    d = {"years_positive_share": pos_share, "max_year_share": max_year_share, "tercile_sums": terc,
         "neighbours": neighbours, "delay_mean": delay_mean}
    ok = (pos_share >= 0.70 and tot > 0 and max_year_share <= 0.50 and sum(t > 0 for t in terc) >= 2
          and all(v > 0 for v in neighbours.values()) and delay_mean > 0)
    return ok, d


def trailing_sd_daily(close_by_day: pd.Series, window=20):
    """Trailing s.d. of daily log returns through d-1 (for volatility terciles)."""
    r = np.log(close_by_day).diff()
    return r.rolling(window, min_periods=10).std().shift(1)
