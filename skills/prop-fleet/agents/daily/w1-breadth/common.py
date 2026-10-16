"""D4 shared definitions: markets, sessions, marks and fills (agents/prereg/D4-spec.md §2, §5)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

MIN = np.int64(60_000_000_000)  # one minute in ns

# market: (open, close, tz, cost per side bp, source)   — spec §2, fixed 2026-10-11
MARKETS = {
    "EUR_USD": ("08:00", "16:00", "Europe/London", 0.5, "oanda"),
    "GBP_USD": ("08:00", "16:00", "Europe/London", 0.7, "oanda"),
    "USD_CAD": ("08:00", "16:00", "Europe/London", 0.8, "oanda"),
    "AUD_USD": ("08:00", "16:00", "Europe/London", 0.7, "oanda"),
    "EUR_JPY": ("08:00", "16:00", "Europe/London", 0.8, "oanda"),
    "AUD_JPY": ("08:00", "16:00", "Europe/London", 0.9, "oanda"),
    "SPX500_USD": ("09:30", "16:00", "America/New_York", 1.0, "oanda"),
    "NAS100_USD": ("09:30", "16:00", "America/New_York", 1.0, "oanda"),
    "US2000_USD": ("09:30", "16:00", "America/New_York", 1.5, "oanda"),
    "UK100_GBP": ("08:00", "16:30", "Europe/London", 1.0, "oanda"),
    "FR40_EUR": ("09:00", "17:30", "Europe/Paris", 1.0, "oanda"),
    "NL25_EUR": ("09:00", "17:30", "Europe/Amsterdam", 1.5, "oanda"),
    "JP225_USD": ("09:00", "15:00", "Asia/Tokyo", 1.5, "oanda"),
    "AU200_AUD": ("10:00", "16:00", "Australia/Sydney", 1.2, "oanda"),
    "GRXEUR": ("09:00", "17:30", "Europe/Berlin", 0.8, "histdata"),
    "ETXEUR": ("09:00", "17:30", "Europe/Berlin", 1.5, "histdata"),
    "XAU_USD": ("08:20", "13:30", "America/New_York", 1.0, "oanda"),
    "WTICO_USD": ("09:00", "14:30", "America/New_York", 2.5, "oanda"),
    "NATGAS_USD": ("09:00", "14:30", "America/New_York", 8.0, "oanda"),
    "CORN_USD": ("08:30", "13:15", "America/Chicago", 10.0, "oanda"),
    "SOYBN_USD": ("08:30", "13:15", "America/Chicago", 6.0, "oanda"),
    "WHEAT_USD": ("08:30", "13:15", "America/Chicago", 10.0, "oanda"),
    "SUGAR_USD": ("03:30", "13:00", "America/New_York", 10.0, "oanda"),
}
HISTDATA = {"GRXEUR", "ETXEUR"}
IS_END = pd.Timestamp("2012-12-31")
OOS_END = pd.Timestamp("2020-05-13")


def data_dir() -> Path:
    return Path(os.environ.get("CLAUDE_SCRATCH", "/tmp/prop-fleet-data")) / "w1-breadth"


@lru_cache(maxsize=None)
def load(m: str) -> pd.DataFrame:
    """o,h,l,c,v indexed by bar open time, UTC naive (fetch.py)."""
    return pd.read_parquet(data_dir() / f"{m}.parquet")


@lru_cache(maxsize=None)
def arrays(m: str):
    d = load(m)
    return (d.index.values.astype("datetime64[ns]").astype(np.int64), d.o.values, d.h.values,
            d.l.values, d.c.values)


def mark(t, c, T):
    """M(T): close of the last bar with open time in [T-10m, T-1m]; nan if none."""
    j = np.searchsorted(t, T, "left") - 1
    if j >= 0 and t[j] >= T - 10 * MIN:
        return c[j]
    return np.nan


def fill(t, o, T):
    """F(T): open of the first bar with open time in [T, T+10m]; nan if none."""
    j = np.searchsorted(t, T, "left")
    if j < len(t) and t[j] <= T + 10 * MIN:
        return o[j]
    return np.nan


@lru_cache(maxsize=None)
def sessions(m: str) -> pd.DataFrame:
    """One row per local weekday in the data range: UTC open/close (ns), bar slice of the
    window [O-10m, C+10m), marks, validity (spec §5)."""
    O, C, tz = MARKETS[m][:3]
    t, o, h, l, c = arrays(m)
    first, last = pd.Timestamp(t[0]).normalize(), pd.Timestamp(t[-1]).normalize()
    days = pd.bdate_range(first - pd.Timedelta(days=1), last + pd.Timedelta(days=1))
    loc_o = pd.DatetimeIndex([f"{d.date()} {O}" for d in days]).tz_localize(tz)
    loc_c = pd.DatetimeIndex([f"{d.date()} {C}" for d in days]).tz_localize(tz)
    tO = loc_o.tz_convert("UTC").tz_localize(None).as_unit("ns").asi8
    tC = loc_c.tz_convert("UTC").tz_localize(None).as_unit("ns").asi8
    i0 = np.searchsorted(t, tO - 10 * MIN, "left")
    i1 = np.searchsorted(t, tC + 10 * MIN, "left")
    nb = np.searchsorted(t, tC, "left") - np.searchsorted(t, tO, "left")
    rows = []
    for k in range(len(days)):
        a, b = i0[k], i1[k]
        tt, oo, cc = t[a:b], o[a:b], c[a:b]
        rows.append((mark(tt, cc, tO[k]), mark(tt, cc, tO[k] + 30 * MIN),
                     fill(tt, oo, tO[k] + 30 * MIN), mark(tt, cc, tC[k])))
    s = pd.DataFrame(rows, index=days, columns=["MO", "MO30", "FO30", "MC"])
    s["tO"], s["tC"], s["i0"], s["i1"], s["nbars"] = tO, tC, i0, i1, nb
    s["nmin"] = (tC - tO) // MIN
    s["valid"] = s[["MO30", "FO30", "MC"]].notna().all(axis=1)
    if m in HISTDATA:
        s = s[(s.index >= "2010-11-15") & (s.index <= "2018-12-31")]
    s = s[s.index <= OOS_END]
    # previous valid close within 5 calendar days (spec §5)
    v = s[s.valid]
    prev_c = v.MC.shift(1)
    gap = (v.index.to_series() - v.index.to_series().shift(1)).dt.days
    s["Cprev"] = prev_c.where(gap <= 5)
    # equal-vol sizing: sd of log(M(C)/M(O)) over previous 60 valid sessions, >= 40 needed
    lr = np.log(v.MC / v.MO)
    sig = lr.rolling(60, min_periods=40).std().shift(1)
    s["sig"] = sig
    s["lr"] = lr
    return s


def session_bars(m: str, row):
    t, o, h, l, c = arrays(m)
    a, b = int(row.i0), int(row.i1)
    return t[a:b], o[a:b], h[a:b], l[a:b], c[a:b]
