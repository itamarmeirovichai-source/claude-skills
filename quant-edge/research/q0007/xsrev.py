"""Q-0007 cross-index overnight-vs-intraday reversal on seven index CFDs (registered 0a46ddd). One code path for the
backtest, the harness and every variant.

As registered (America/New_York per day with zoneinfo; HistData 1m bid CFD quotes, ts = bar open UTC, clock histdata_rule):
  trading days d = full XNYS sessions; skip d if d or the previous XNYS session d-1 is an early close.
  U = SPX, NSX, JPX, UKX, FRX, GRX, ETX (HKX excluded by construction: no US-hours bars).
  C_i(d-1) = open of the 15:55 bar on d-1 (fallback: open of the first existing bar in 15:56..15:58; else ineligible).
  S_i(d) = open of the 09:31 bar on d (no fallback).  CO = ln(S/C).  z = CO / s, s = sqrt(EWMA(com 60) of CO^2 over the
  instrument's days through d-1), >= 40 prior days.
  eligible: C, S exist, s defined, the 09:32 entry bar exists, >= 300 of the 384 bars 09:31..15:54 exist, inside the
  usable span (GRX excluded 2020-06-15..2023-12-01, ETX after 2018-12-14; no bar of an excluded span used).
  trade iff >= 4 eligible; LONG argmin z, SHORT argmax z (ties: earlier in U order); every eligible day, no threshold.
  ENTRY open 09:32; EXIT open 15:55 (fallback first existing bar in 15:56..15:58; else close of the last bar in
  15:45..15:54, counted).  P&L = w_L ln(X_L/E_L) - w_S ln(X_S/E_S) - w_L (c_L+c_L) - w_S (c_S+c_S).
  w_i = (0.10/sqrt(252))/sigma_i, sigma_i = EWMA(com 60) s.d. of the instrument's own 09:32->15:55 log return through
  d-1 (>= 40 observations); no cap/floor; pair not beta-hedged.

Conventions the row leaves open, fixed here before any read of returns:
  * EWMA histories (s and sigma) run over the instrument's own valid days: for s, trading days on which CO_i exists inside
    the usable span; for sigma, trading days on which the 09:32 bar exists inside the span (the row's 'eligible days'
    would be circular, since eligibility needs s and sigma). s^2 = pandas ewm(com, min_periods=40).mean() of CO^2,
    sigma = pandas ewm(com, min_periods=40).std(); both read at the previous valid day.
  * sigma must exist for an instrument to be eligible (no weight otherwise).
  * last-resort exit (no bar at all in 15:45..15:58): close of the last bar in [entry, 15:44] (counted as 'lastbar').
  * coverage="ex_ante" drops the 300-of-384 test, which reads bar availability after the entry (criterion 8 variant).
  * shifted clocks (neighbours, delay) keep the fallback shape: first existing bar in exit+1..exit+3, else close of the
    last bar in exit-10..exit-1. The signal clocks (15:55 on d-1, 09:31 on d) never move.
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

U = ("SPX", "NSX", "JPX", "UKX", "FRX", "GRX", "ETX")
DS = {"SPX": "histdata_cfd_1m_SPXUSD", "NSX": "histdata_cfd_1m_NSXUSD", "JPX": "histdata_cfd_1m_JPXJPY", "UKX": "histdata_cfd_1m_UKXGBP",
      "FRX": "histdata_cfd_1m_FRXEUR", "GRX": "histdata_cfd_1m_GRXEUR", "ETX": "histdata_cfd_1m_ETXEUR"}
COST_BP = {"SPX": 1.0, "NSX": 1.0, "UKX": 1.0, "FRX": 1.0, "GRX": 0.8, "ETX": 1.5, "JPX": 1.5}
EXCL = {"GRX": [("2020-06-15", "2023-12-01")], "ETX": [("2018-12-15", "2099-12-31")]}
KEEP_LO, KEEP_HI = 9 * 60 + 31, 15 * 60 + 58        # the rule reads no bar outside 09:31..15:58 NY
COV_LO, COV_HI = 9 * 60 + 31, 15 * 60 + 54


@dataclass(frozen=True)
class Params:
    ref_min: int = 15 * 60 + 55
    sig_min: int = 9 * 60 + 31
    entry_min: int = 9 * 60 + 32
    exit_min: int = 15 * 60 + 55
    com: float = 60.0
    min_obs: int = 40
    min_elig: int = 4
    min_cov: int = 300
    coverage: str = "as_written"     # or "ex_ante"
    leak: str = ""                   # "plant": signal price read at 15:55 of d (deliberate look-ahead; harness check)


def keep_rule_minutes(p: ck.Prepared) -> ck.Prepared:
    k = (p.minute >= KEEP_LO) & (p.minute <= KEEP_HI)
    return ck.Prepared(p.ts[k], p.date[k], p.minute[k], p.open[k], p.high[k], p.low[k], p.close[k], p.tz)


@functools.lru_cache(maxsize=2)
def xnys(start="2010-01-01", end="2025-12-31"):
    cal = xc.get_calendar("XNYS", start=start, end=end)
    s = pd.DatetimeIndex(cal.schedule.index)
    s = s.tz_localize(None) if s.tz is not None else s
    ec = pd.DatetimeIndex(cal.early_closes)
    ec = ec.tz_localize(None) if ec.tz is not None else ec
    return s, set(ec.normalize())


def in_span(name: str, d: pd.Timestamp) -> bool:
    for a, b in EXCL.get(name, []):
        if pd.Timestamp(a) <= d <= pd.Timestamp(b):
            return False
    return True


def inst_rows(p: ck.Prepared, name: str, sess: pd.DatetimeIndex, prm: Params) -> pd.DataFrame:
    """Per XNYS session: C (ref close), S (signal), E (entry), X (exit) with exit type, coverage, span flag."""
    sl = ck.day_slices(p)
    m, o, c = p.minute, p.open, p.close
    n = len(sess)
    C, S, E, X, cov = (np.full(n, np.nan) for _ in range(5))
    how = np.empty(n, dtype=object)
    span = np.array([in_span(name, d) for d in sess])
    for j, d in enumerate(sess):
        r = sl.get(np.datetime64(d.date(), "D"))
        if r is None or not span[j]:
            continue
        a, b = r
        mm = m[a:b]

        def exact(t):
            k = int(np.searchsorted(mm, t))
            return a + k if (k < mm.size and mm[k] == t) else -1

        def first_in(t0, t1):
            k = int(np.searchsorted(mm, t0))
            return a + k if (k < mm.size and mm[k] <= t1) else -1

        k = exact(prm.ref_min)
        k = k if k >= 0 else first_in(prm.ref_min + 1, prm.ref_min + 3)
        if k >= 0:
            C[j] = o[k]
        ks = exact(prm.ref_min if prm.leak == "plant" else prm.sig_min)
        if ks >= 0:
            S[j] = o[ks]
        ke = exact(prm.entry_min)
        if ke >= 0:
            E[j] = o[ke]
            kx = exact(prm.exit_min)
            if kx >= 0:
                X[j], how[j] = o[kx], "exact"
            else:
                kx = first_in(prm.exit_min + 1, prm.exit_min + 3)
                if kx >= 0:
                    X[j], how[j] = o[kx], "fallback_after"
                else:
                    k0 = int(np.searchsorted(mm, prm.exit_min - 10))
                    k1 = int(np.searchsorted(mm, prm.exit_min))
                    if k1 > k0 and a + k1 - 1 >= ke:
                        X[j], how[j] = c[a + k1 - 1], "fallback_close_before"
                    else:
                        k2 = max(a + int(np.searchsorted(mm, prm.exit_min - 10)) - 1, ke)
                        X[j], how[j] = c[k2], "lastbar"
        cov[j] = int(np.searchsorted(mm, COV_HI, side="right") - np.searchsorted(mm, COV_LO))
    return pd.DataFrame({"C": C, "S": S, "E": E, "X": X, "how": how, "cov": cov, "span": span}, index=sess)


def build(P: dict, prm: Params, start=None, end=None) -> dict:
    """P: name -> Prepared (rule minutes only). Returns the day panel and the trades of every trading day."""
    sess, early = xnys()
    lo = min(pd.Timestamp(P[k].date[0]) for k in P if len(P[k]))
    hi = max(pd.Timestamp(P[k].date[-1]) for k in P if len(P[k]))
    sess = sess[(sess >= lo - pd.Timedelta(days=7)) & (sess <= hi)]
    prev = pd.Series(sess).shift(1).to_numpy()
    tday = np.array([(d not in early) and (pd.notna(pv) and pd.Timestamp(pv) not in early) for d, pv in zip(sess, prev)])
    tday[0] = False
    rows = {k: inst_rows(P[k], k, sess, prm) for k in U if k in P}
    names = list(rows)
    Cp = np.column_stack([np.r_[np.nan, rows[k]["C"].to_numpy()[:-1]] for k in names])
    spanp = np.column_stack([np.r_[False, rows[k]["span"].to_numpy()[:-1]] for k in names])
    S = np.column_stack([rows[k]["S"].to_numpy() for k in names])
    E = np.column_stack([rows[k]["E"].to_numpy() for k in names])
    X = np.column_stack([rows[k]["X"].to_numpy() for k in names])
    cov = np.column_stack([rows[k]["cov"].to_numpy() for k in names])
    span = np.column_stack([rows[k]["span"].to_numpy() for k in names]) & spanp
    CO = np.log(S / Cp)
    R = np.log(X / E)
    n, K = CO.shape
    s = np.full((n, K), np.nan)
    sig = np.full((n, K), np.nan)
    for j in range(K):
        v = tday & span[:, j] & np.isfinite(CO[:, j])
        x = pd.Series(CO[v, j] ** 2)
        s[v, j] = np.sqrt(x.ewm(com=prm.com, min_periods=prm.min_obs).mean().shift(1).to_numpy())
        v2 = tday & span[:, j] & np.isfinite(E[:, j])
        y = pd.Series(R[v2, j])
        sig[v2, j] = y.ewm(com=prm.com, min_periods=prm.min_obs).std().shift(1).to_numpy()
    elig = (tday[:, None] & span & np.isfinite(CO) & np.isfinite(s) & (s > 0) & np.isfinite(E) & np.isfinite(sig) & (sig > 0))
    if prm.coverage == "as_written":
        elig &= cov >= prm.min_cov
    z = np.where(elig, CO / s, np.nan)
    w = np.where(elig, ck.TARGET_DAILY / sig, np.nan)
    ne = elig.sum(axis=1)
    trade = ne >= prm.min_elig
    cst = np.array([COST_BP[k] for k in names]) * 1e-4
    rec = []
    for i in np.nonzero(trade)[0]:
        zi = z[i]
        L = int(np.nanargmin(zi))
        Sx = int(np.nanargmax(zi))
        g = w[i, L] * R[i, L] - w[i, Sx] * R[i, Sx]
        c1 = w[i, L] * 2 * cst[L] + w[i, Sx] * 2 * cst[Sx]
        rec.append({"day": sess[i], "n_elig": int(ne[i]), "L": names[L], "S": names[Sx], "zL": zi[L], "zS": zi[Sx],
                    "wL": w[i, L], "wS": w[i, Sx], "rL": R[i, L], "rS": R[i, Sx], "gross": g, "cost1": c1,
                    "net1": g - c1, "net2": g - 2 * c1, "howL": rows[names[L]]["how"].iloc[i], "howS": rows[names[Sx]]["how"].iloc[i],
                    "legL": w[i, L] * R[i, L] - w[i, L] * 2 * cst[L], "legS": -w[i, Sx] * R[i, Sx] - w[i, Sx] * 2 * cst[Sx],
                    "bench": float(np.nanmean(w[i, elig[i]] * R[i, elig[i]]))})
    tr = pd.DataFrame(rec)
    if start is not None and len(tr):
        tr = tr[(tr["day"] >= pd.Timestamp(start)) & (tr["day"] <= pd.Timestamp(end))].reset_index(drop=True)
    return {"sess": sess, "tday": tday, "names": names, "elig": elig, "z": z, "w": w, "R": R, "CO": CO, "trades": tr, "rows": rows}


def decisions(panel: dict, day) -> tuple:
    t = panel["trades"]
    x = t[t["day"] == pd.Timestamp(day)]
    if len(x) == 0:
        return ("no trade",)
    r = x.iloc[0]
    return ("trade", r["L"], r["S"], round(float(r["wL"]), 12), round(float(r["wS"]), 12))
