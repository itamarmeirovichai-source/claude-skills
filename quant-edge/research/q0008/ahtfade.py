"""Q-0008 HSI after-hours fade on HK50 (registered 0a46ddd). One code path for backtest, harness, variants.

As registered (Asia/Hong_Kong, UTC+8, HistData HKXHKD bid bars, ts = bar open UTC, clock histdata_rule):
  d = XHKG session with a previous XHKG session p within 5 calendar days; skip d if p was a half-day session.
  C(p) = close of the last bar with open in [16:00, 16:29] HKT on p (none -> no trade).
  A(d) = close of the last bar with open >= 17:15 HKT on p and < 03:00 HKT on the calendar day after p; >= 60 bars in
         that window, else no trade.  m = ln(A/C); trigger |m| > 0.70%; side = -sign(m).
  ENTRY open of the 09:20 HKT bar on d (missing -> no trade). EXIT open of the 09:57 bar; fallback first existing bar in
  09:58..09:59; else close of the last bar in 09:50..09:56 (counted).
  w = (0.10/sqrt(252))/sigma, sigma = EWMA (com 60 sessions) s.d. of the 09:20->09:57 log return over ALL prior eligible
  sessions (triggered or not) through p, >= 40 observations.  P&L = w*side*ln(exit/entry) - w*2*1.5 bp (2x: 3.0 bp).

Conventions the row leaves open, fixed here before any read of returns:
  * "eligible session" (for sigma and for the null pools) = d passes the day definition, C(p) exists, A(d) exists with
    >= 60 bars and the entry bar exists (everything except the trigger); its 09:20->09:57 return uses the exit rule above.
    (Requiring sigma itself would make the definition circular.)
  * sigma = pandas ewm(com=60, min_periods=40).std() over those returns, read at the last eligible session before d.
  * last-resort exit (no bar at all in 09:50..09:59): close of the last bar in [entry, 09:56] (counted as 'lastbar').
  * shifted clocks (neighbours / delay) keep the same fallback shape: first existing bar in exit+1..exit+2, else close of
    the last bar in exit-7..exit-1.
"""
from __future__ import annotations

import functools
import sys
from dataclasses import dataclass
from pathlib import Path

import exchange_calendars as xc
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "batch1b"))
import cfdkit as ck  # noqa: E402

COST_BP = 1.5
MIN = 60_000_000_000          # one minute in ns


@dataclass(frozen=True)
class Params:
    threshold: float = 0.0070
    entry_min: int = 9 * 60 + 20
    exit_min: int = 9 * 60 + 57
    com: float = 60.0
    min_obs: int = 40
    min_aht_bars: int = 60
    leak: str = ""                # "plant" = trigger also requires the fade to win (deliberate look-ahead; harness check)


@functools.lru_cache(maxsize=4)
def xhkg(start: str, end: str):
    cal = xc.get_calendar("XHKG", start=start, end=end)
    s = cal.schedule
    half = set(pd.DatetimeIndex(cal.early_closes).normalize().tz_localize(None) if pd.DatetimeIndex(cal.early_closes).tz is not None
               else pd.DatetimeIndex(cal.early_closes).normalize())
    return pd.DatetimeIndex(s.index).tz_localize(None) if pd.DatetimeIndex(s.index).tz is not None else pd.DatetimeIndex(s.index), half


def _ns(date, minute):
    # HK has no DST: local = UTC + 8 h
    return int((pd.Timestamp(date).normalize() + pd.Timedelta(minutes=int(minute) - 8 * 60)).value)


def session_table(p: ck.Prepared, prm: Params, cal_start="2010-01-01", cal_end="2025-12-31") -> pd.DataFrame:
    sess, half = xhkg(cal_start, cal_end)
    if len(p) == 0:
        return pd.DataFrame()
    lo_d, hi_d = pd.Timestamp(p.date[0]), pd.Timestamp(p.date[-1])
    ts, c, o = p.ts, p.close, p.open
    rows = []
    for i in range(1, len(sess)):
        d, pv = sess[i], sess[i - 1]
        if d < lo_d or d > hi_d + pd.Timedelta(days=1):
            continue
        st = "ok"
        if (d - pv).days > 5:
            st = "prev_too_far"
        elif pv in half:
            st = "prev_half_day"
        C = A = np.nan
        n_aht = 0
        if st == "ok":
            a = np.searchsorted(ts, _ns(pv, 16 * 60)); b = np.searchsorted(ts, _ns(pv, 16 * 60 + 29), side="right")
            if b > a:
                C = float(c[b - 1])
            else:
                st = "no_day_close"
        if st == "ok":
            a = np.searchsorted(ts, _ns(pv, 17 * 60 + 15)); b = np.searchsorted(ts, _ns(pv + pd.Timedelta(days=1), 3 * 60))
            n_aht = int(b - a)
            if n_aht >= prm.min_aht_bars:
                A = float(c[b - 1])
            else:
                st = "aht_short"
        ei = -1
        if st == "ok":
            v = _ns(d, prm.entry_min)
            k = np.searchsorted(ts, v)
            if k < ts.size and ts[k] == v:
                ei = int(k)
            else:
                st = "no_entry_bar"
        xi, xpx, how = -1, np.nan, ""
        if st == "ok":
            xpx, how, xi = exit_price(p, d, prm.exit_min, ei)
        rows.append({"day": d, "prev": pv, "status": st, "C": C, "A": A, "n_aht": n_aht, "entry_i": ei, "exit_i": xi,
                     "entry": float(o[ei]) if ei >= 0 else np.nan, "exit": xpx, "exit_how": how})
    t = pd.DataFrame(rows)
    t["m"] = np.log(t["A"] / t["C"])
    t["r"] = np.log(t["exit"] / t["entry"])
    elig = t["status"] == "ok"
    sd = t.loc[elig, "r"].ewm(com=prm.com, min_periods=prm.min_obs).std().shift(1)
    t["sigma"] = np.nan
    t.loc[elig, "sigma"] = sd
    t["w"] = ck.TARGET_DAILY / t["sigma"]
    t["eligible"] = elig & np.isfinite(t["w"])
    t["trig"] = t["eligible"] & (t["m"].abs() > prm.threshold)
    if prm.leak == "plant":
        t["trig"] &= (-np.sign(t["m"]) * t["r"]) > 0
    t["side"] = np.where(t["trig"], -np.sign(t["m"]), 0.0)
    return t


def exit_price(p: ck.Prepared, d, xm: int, ei: int):
    ts, o, c = p.ts, p.open, p.close
    v = _ns(d, xm)
    k = np.searchsorted(ts, v)
    if k < ts.size and ts[k] == v and k > ei:
        return float(o[k]), "exact", int(k)
    k2 = np.searchsorted(ts, v + 2 * MIN, side="right")
    if k2 > k and k > ei:
        return float(o[k]), "fallback_after", int(k)
    a = max(np.searchsorted(ts, v - 7 * MIN), ei)
    if k > a:
        return float(c[k - 1]), "fallback_close_before", int(k - 1)
    j = max(int(k) - 1, ei)
    return float(c[j]), "lastbar", j


def trades(t: pd.DataFrame, cost_mult: float = 1.0) -> pd.DataFrame:
    x = t[t["trig"]].copy()
    x["gross"] = x["w"] * x["side"] * x["r"]
    x["cost1"] = x["w"] * 2 * COST_BP * 1e-4
    x["net1"] = x["gross"] - x["cost1"]
    x["net2"] = x["gross"] - 2 * x["cost1"]
    x["bench"] = x["w"] * x["r"]
    return x


class FadeRule:
    """qe.engine.harness interface: target[i] = w*side held over the entry bar .. the bar before the exit."""
    name = "hk_aht_fade"
    mode = "target"

    def __init__(self, prm: Params):
        self.prm, self.params = prm, {}

    def signal(self, bars: pd.DataFrame):
        p = ck.prepare(bars, ck.HK)
        t = session_table(p, self.prm)
        tgt = np.zeros(len(bars))
        for r in t[t["trig"]].itertuples():
            hi = int(r.exit_i) if r.exit_i > r.entry_i else int(r.entry_i) + 1
            tgt[int(r.entry_i):hi] = r.w * r.side
        return tgt
