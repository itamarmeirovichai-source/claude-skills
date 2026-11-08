"""Q-0011 18:00 ET reopen-overshoot fade on US500/US100/XAUUSD CFDs (registered fd38c6e). One code path for backtest,
harness and variants. HistData bid bars, ts = bar open UTC (clock histdata_rule, D-019); local times via zoneinfo.

As registered: evening d = Sun..Thu NY date whose 18:00..18:10 ET bars all exist; skip if d is an XNYS full holiday or
d+1 is one. C = close of the last bar with open in [15:00, 17:00) ET on the previous trading day; S = close of 18:09;
M = ln(S/C); s = sqrt(EWMA com 60 of M^2 over prior eligible evenings), >= 40 obs; trigger |M| > 1.5 s; FTMO-day rule
(18:11 NY is on the next Prague date); entry open 18:11, side -sign(M); exit open 19:30, fallback first bar 19:31..19:33
(open), else close of the last bar in 19:15..19:29. w = (0.10/sqrt252)/sigma, sigma = EWMA com 60 s.d. of the
18:11->19:30 log return over prior eligible evenings, >= 40 obs. P&L = w*side*r - w*2*cost.

Conventions the row leaves open, fixed here before any read of returns (disclosed in the result file):
  * "previous trading day" = the latest XNYS session <= d (Friday for a Sunday; d itself for Mon..Thu, i.e. the
    pre-halt close of the same futures trading day).
  * eligible evening for the scale s = passes the evening definition and C exists; for sigma additionally the 18:11
    entry bar exists. Both histories include evenings that fail the FTMO-day filter (the filter is a trading filter).
  * EWMA = pandas ewm(com=60, min_periods=40) (mean of M^2 for s; std of r for sigma), read at the last eligible evening
    before d. Missing 18:11 bar -> no trade. Last-resort exit (no bar in 19:15..19:33): close of the last bar in
    [entry, exit), counted 'lastbar'. Shifted clocks keep the same fallback shape (+1..+3 open, else close in -15..-1).
  * The QA spike-reversal drop is applied at the leg level outside the rule (trades()), as a data exclusion.
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

COST_BP = 1.0
NY, PRG = "America/New_York", "Europe/Prague"


@dataclass(frozen=True)
class Params:
    k: float = 1.5
    signal_min: int = 18 * 60 + 9
    entry_min: int = 18 * 60 + 11
    exit_min: int = 19 * 60 + 30
    com: float = 60.0
    min_obs: int = 40
    leak: str = ""          # "plant" = trigger also requires the fade to win (deliberate look-ahead; harness check)


@functools.lru_cache(maxsize=2)
def xnys(start="2009-01-01", end="2025-12-31"):
    cal = xc.get_calendar("XNYS", start=start, end=end)
    sess = pd.DatetimeIndex(cal.sessions)
    sess = sess.tz_localize(None) if sess.tz is not None else sess
    wk = pd.bdate_range(start, end)
    hol = set(wk.difference(sess))
    return sess, hol


def keys_of(p: ck.Prepared) -> np.ndarray:
    return p.date.astype("int64") * 1440 + p.minute


def evening_table(p: ck.Prepared, prm: Params, inst: str) -> pd.DataFrame:
    sess, hol = xnys()
    if len(p) == 0:
        return pd.DataFrame()
    key = keys_of(p)
    sel = np.nonzero((p.minute >= 15 * 60) & (p.minute <= 20 * 60))[0]
    pos = dict(zip(key[sel].tolist(), sel.tolist()))
    o, c = p.open, p.close
    days = pd.date_range(pd.Timestamp(p.date[0]), pd.Timestamp(p.date[-1]), freq="D")
    days = days[days.dayofweek.isin([6, 0, 1, 2, 3])]
    sarr = sess.to_numpy()
    rows = []
    for d in days:
        dn = int(np.datetime64(d.date(), "D").astype("int64"))
        st = "ok"
        if d in hol or (d + pd.Timedelta(days=1)) in hol:
            st = "holiday"
        if st == "ok":
            idx = [pos.get(dn * 1440 + m) for m in range(18 * 60, 18 * 60 + 11)]
            if any(i is None for i in idx):
                st = "missing_1800_1810"
        C = S = np.nan
        if st == "ok":
            j = np.searchsorted(sarr, np.datetime64(d.date()), side="right") - 1
            pv = int(np.datetime64(pd.Timestamp(sarr[j]).date(), "D").astype("int64"))
            a, b = np.searchsorted(key, pv * 1440 + 15 * 60), np.searchsorted(key, pv * 1440 + 17 * 60)
            if b > a:
                C = float(c[b - 1])
            else:
                st = "no_reference"
        si = pos.get(dn * 1440 + prm.signal_min) if st == "ok" else None
        if st == "ok":
            if si is None:
                st = "no_signal_bar"
            else:
                S = float(c[si])
        ei = pos.get(dn * 1440 + prm.entry_min, -1) if st == "ok" else -1
        xpx, how, xi = np.nan, "", -1
        if st == "ok" and ei >= 0:
            xpx, how, xi = exit_price(p, key, pos, dn, prm.exit_min, ei)
        rows.append({"d": d, "inst": inst, "status": st, "C": C, "S": S, "entry_i": ei, "exit_i": xi,
                     "entry": float(o[ei]) if ei >= 0 else np.nan, "exit": xpx, "exit_how": how})
    t = pd.DataFrame(rows)
    t["day"] = t["d"] + pd.Timedelta(days=1)
    t["sunday"] = t["d"].dt.dayofweek == 6
    t["M"] = np.log(t["S"] / t["C"])
    t["r"] = np.log(t["exit"] / t["entry"])
    e1 = (t["status"] == "ok") & np.isfinite(t["M"])
    t["s"] = np.nan
    t.loc[e1, "s"] = np.sqrt((t.loc[e1, "M"] ** 2).ewm(com=prm.com, min_periods=prm.min_obs).mean().shift(1))
    e2 = e1 & np.isfinite(t["r"])
    t["sigma"] = np.nan
    t.loc[e2, "sigma"] = t.loc[e2, "r"].ewm(com=prm.com, min_periods=prm.min_obs).std().shift(1)
    t["w"] = ck.TARGET_DAILY / t["sigma"]
    # FTMO-day rule: 18:11 NY must fall on the next Prague calendar date (NY and Prague 6 h apart)
    ent = (t["d"] + pd.Timedelta(minutes=prm.entry_min)).dt.tz_localize(NY).dt.tz_convert(PRG)
    t["ftmo_ok"] = ent.dt.tz_localize(None).dt.normalize().to_numpy() == t["day"].to_numpy()
    t["z"] = t["M"] / t["s"]
    t["eligible"] = e2 & np.isfinite(t["w"]) & np.isfinite(t["s"])
    t["trig"] = t["eligible"] & t["ftmo_ok"] & (t["M"].abs() > prm.k * t["s"])
    if prm.leak == "plant":
        t["trig"] &= (-np.sign(t["M"]) * t["r"]) > 0
    t["side"] = np.where(t["trig"], -np.sign(t["M"]), 0.0)
    return t


def exit_price(p, key, pos, dn, xm, ei):
    o, c = p.open, p.close
    k = pos.get(dn * 1440 + xm)
    if k is not None and k > ei:
        return float(o[k]), "exact", int(k)
    for m in range(xm + 1, xm + 4):
        k = pos.get(dn * 1440 + m)
        if k is not None and k > ei:
            return float(o[k]), "fallback_after", int(k)
    a, b = np.searchsorted(key, dn * 1440 + xm - 15), np.searchsorted(key, dn * 1440 + xm)
    a = max(int(a), ei + 1)
    if b > a:
        return float(c[b - 1]), "fallback_close_before", int(b - 1)
    j = max(int(b) - 1, ei)
    return float(c[j]), "lastbar", j


def spike_flags(p: ck.Prepared) -> np.ndarray:
    """The data/qa spike-reversal definition (qe.qa.histdata_qa.outliers): index of each flagged bar."""
    t, c = p.ts, p.close
    r = np.r_[np.nan, np.diff(np.log(c))]
    near = np.r_[False, np.diff(t) <= 5 * 60_000_000_000]
    r = np.where(near, r, np.nan)
    yr = pd.DatetimeIndex(t).year.to_numpy()
    med = pd.Series(np.abs(r)).groupby(yr).transform(lambda s: s[s > 0].median()).to_numpy()
    flag = np.abs(r) > np.maximum(20.0 * med, 0.005)
    nxt = np.r_[r[1:], np.nan]
    rev = flag & (np.sign(nxt) == -np.sign(r)) & (np.abs(nxt) >= 0.8 * np.abs(r))
    return np.nonzero(rev)[0]


def trades(t: pd.DataFrame, spikes=None, cost_bp: float = COST_BP) -> pd.DataFrame:
    x = t[t["trig"]].copy()
    x["spike_drop"] = False
    if spikes is not None and len(spikes):
        s = set(int(i) for i in spikes)
        x["spike_drop"] = [(int(a) in s) or (int(b) in s) for a, b in zip(x["entry_i"], x["exit_i"])]
    x = x[~x["spike_drop"]].copy()
    x["gross"] = x["w"] * x["side"] * x["r"]
    x["cost1"] = x["w"] * 2 * cost_bp * 1e-4
    x["net1"] = x["gross"] - x["cost1"]
    x["net2"] = x["gross"] - 2 * x["cost1"]
    x["net3"] = x["gross"] - 3 * x["cost1"]
    x["bench"] = x["w"] * x["r"]
    return x


class FadeRule:
    """qe.engine.harness interface: target[i] = w*side over the entry bar .. the bar before the exit."""
    name = "reopen_fade"
    mode = "target"

    def __init__(self, prm: Params, inst: str):
        self.prm, self.inst, self.params = prm, inst, {}

    def signal(self, bars: pd.DataFrame):
        p = ck.prepare(bars, ck.NY)
        t = evening_table(p, self.prm, self.inst)
        tgt = np.zeros(len(bars))
        if len(t) == 0:
            return tgt
        for r in t[t["trig"]].itertuples():
            hi = int(r.exit_i) if r.exit_i > r.entry_i else int(r.entry_i) + 1
            tgt[int(r.entry_i):hi] = r.w * r.side
        return tgt
