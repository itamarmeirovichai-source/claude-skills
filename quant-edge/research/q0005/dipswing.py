"""Commodity dip swing (registry rows Q-0005 energy CL/CO/HO and Q-0006 gold GC; registered 93cb97a).

Rule exactly as registered (one code path for the backtest, the leak harness and the neighbourhood):
  r_t daily excess return of a root; days with |r| > 25% set to missing before the signal.
  P_t = cumprod(1 + r_t) (a missing day is a zero-return day for the index).
  Signal at close t: R2_t = r_{t-1} + r_t; sigma2_t = sqrt(2) * sd(r_{t-59..t}) (60 obs, >= 50 non-missing).
  If R2_t < -k * sigma2_t and no position is open in the root -> BUY at the close of t+1.
  EXIT at the close of the first u >= t+2 with P_u > mean(P_{u-4..u}), else at the close of t+4.
  Weight = 0.10/sqrt(252) / EWMA(com 60) s.d. of r through the signal day t, divided by the number of roots.
Implementation conventions fixed before any OOS read (stated in the result file):
  * "no position open": a root is busy from its signal day through its exit day; a new signal on the exit day itself
    is not taken (the position is still open at that close).
  * EWMA s.d. = pandas ewm(com, min_periods=com).std() on r with missing days skipped; no weight before 60 returns.
  * a position still open on the last row of the served window is closed at that close (flag `truncated`).
  * a missing r on a held day earns 0 that day; financing is charged per calendar day held.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd

BAD_ABS_RET = 0.25


@dataclass(frozen=True)
class Params:
    k: float = 2.0              # trigger in sigma2 units
    sd_window: int = 60         # observations in the sigma window
    sd_min: int = 50            # minimum non-missing observations
    mean_len: int = 5           # length of the P mean in the exit test (u-4..u)
    max_hold: int = 3           # sessions after entry (exit at t+4 at the latest)
    com: float = 60.0           # EWMA centre of mass of the weight's s.d.
    entry_lag: int = 1          # entry at close t + entry_lag (registered: 1)
    exit_lag: int = 0           # exit at close u + exit_lag (registered: 0; 1 = execution-lag variant)
    target_daily: float = 0.10 / math.sqrt(252)


def clean(r_raw: pd.Series) -> pd.Series:
    r = r_raw.astype(float).copy()
    r[r.abs() > BAD_ABS_RET] = np.nan
    return r


def trades_one_root(r_raw: pd.Series, p: Params, n_roots: int = 1) -> pd.DataFrame:
    """Trades of one root on the dates of r_raw (a date-indexed series). exit_i = None when still open at the end."""
    r = clean(r_raw)
    vals = r.to_numpy(float)
    n = len(vals)
    P = np.cumprod(1.0 + np.nan_to_num(vals, nan=0.0))
    sd = r.rolling(p.sd_window, min_periods=p.sd_min).std().to_numpy(float)
    sigma2 = math.sqrt(2.0) * sd
    R2 = vals + np.r_[np.nan, vals[:-1]]
    ew = r.ewm(com=p.com, min_periods=int(p.com)).std().to_numpy(float)
    pm = pd.Series(P).rolling(p.mean_len, min_periods=p.mean_len).mean().to_numpy(float)
    rows = []
    busy_until = -1          # index of the last day on which the root holds (or awaits) a position
    i = 0
    while i < n:
        if i > busy_until and np.isfinite(R2[i]) and np.isfinite(sigma2[i]) and R2[i] < -p.k * sigma2[i]:
            e = i + p.entry_lag
            w = p.target_daily / ew[i] / n_roots if (np.isfinite(ew[i]) and ew[i] > 0) else np.nan
            if not np.isfinite(w):
                i += 1
                continue
            if e >= n:                                       # entry day not in the served data
                busy_until = n
                break
            last = i + p.entry_lag + p.max_hold              # t+4 in the registered case
            u_sig = None
            for u in range(i + p.entry_lag + 1, min(last, n - 1) + 1):
                if np.isfinite(pm[u]) and P[u] > pm[u]:
                    u_sig = u
                    break
            if u_sig is None and last <= n - 1:
                u_sig = last
            x = None if u_sig is None else u_sig + p.exit_lag
            if x is not None and x > n - 1:
                x = None
            rows.append({"signal_i": i, "entry_i": e, "exit_i": x, "w": w, "sigma2": sigma2[i], "R2": R2[i]})
            busy_until = (x if x is not None else n)
        i += 1
    return pd.DataFrame(rows, columns=["signal_i", "entry_i", "exit_i", "w", "sigma2", "R2"])


def pnl_one_root(r_raw: pd.Series, tr: pd.DataFrame, cost_bp: float, markup: float, mult: float = 1.0):
    """Daily MTM gross / cost series and trade table (positions open at the end closed at the last close)."""
    r = clean(r_raw)
    vals = np.nan_to_num(r.to_numpy(float), nan=0.0)
    dates = pd.DatetimeIndex(r.index)
    n = len(vals)
    gross = np.zeros(n)
    cost = np.zeros(n)
    out = []
    cal = np.r_[0, np.diff(dates.values).astype("timedelta64[D]").astype(int)]
    for t in tr.itertuples():
        e = int(t.entry_i)
        x = int(t.exit_i) if t.exit_i is not None and not (isinstance(t.exit_i, float) and np.isnan(t.exit_i)) else n - 1
        trunc = t.exit_i is None or (isinstance(t.exit_i, float) and np.isnan(t.exit_i))
        held = np.arange(e + 1, x + 1)
        g = t.w * vals[held]
        fin = t.w * markup * mult / 365.0 * cal[held]
        gross[held] += g
        cost[held] += fin
        c_side = t.w * cost_bp * 1e-4 * mult
        cost[e] += c_side
        cost[x] += c_side
        out.append({"signal_date": dates[int(t.signal_i)], "entry_date": dates[e], "exit_date": dates[x],
                    "sessions": int(x - e), "cal_days": int((dates[x] - dates[e]).days), "w": t.w,
                    "gross": float(g.sum()), "cost": float(fin.sum() + 2 * c_side), "truncated": bool(trunc),
                    "ret_notional": float(vals[held].sum()), "signal_i": int(t.signal_i), "entry_i": e})
    return pd.Series(gross, index=dates), pd.Series(cost, index=dates), pd.DataFrame(out)


def run(R: pd.DataFrame, roots, p: Params, cost_bp: float, markup: float, mult: float = 1.0,
        eval_start=None, eval_end=None) -> dict:
    """R: date-indexed frame of raw excess returns. Positions are evaluated when their ENTRY date lies in
    [eval_start, eval_end]; the daily series covers the dates in that window."""
    n_roots = len(roots)
    es = pd.Timestamp(eval_start) if eval_start is not None else R.index[0]
    ee = pd.Timestamp(eval_end) if eval_end is not None else R.index[-1]
    idx = R.index[(R.index >= es) & (R.index <= ee)]
    gross = pd.Series(0.0, index=idx)
    cost = pd.Series(0.0, index=idx)
    trades = []
    for root in roots:
        s = R[root]
        first = s.first_valid_index()
        s = s.loc[first:] if first is not None else s
        tr = trades_one_root(s, p, n_roots)
        g, c, tt = pnl_one_root(s, tr, cost_bp, markup, mult)
        if len(tt):
            keep = (tt["entry_date"] >= es) & (tt["entry_date"] <= ee)
            tt = tt[keep].copy()
            tt["root"] = root
            # daily series only from the kept trades: recompute on the kept subset
            tr_k = tr.iloc[np.nonzero(keep.to_numpy())[0]]
            g, c, _ = pnl_one_root(s, tr_k, cost_bp, markup, mult)
            trades.append(tt)
        gross = gross.add(g.reindex(idx).fillna(0.0), fill_value=0.0)
        cost = cost.add(c.reindex(idx).fillna(0.0), fill_value=0.0)
    T = pd.concat(trades, ignore_index=True) if trades else pd.DataFrame()
    if len(T):
        T["net"] = T["gross"] - T["cost"]
        T["day"] = T["entry_date"].dt.date
    return {"gross": gross, "cost": cost, "net": gross - cost, "trades": T}


# ------------------------------------------------------------------------------------- rule object for the harness
class DipRuleHarness:
    """qe.engine harness interface on a single-root frame (ts, open=high=low=close = the raw index, valid, day_id,
    trading_day). target[i] = weight held over bar i (close i -> close i+1)."""
    name = "dipswing"
    mode = "target"

    def __init__(self, p: Params, n_roots: int = 1):
        self.p = p
        self.n_roots = n_roots
        self.params = {}

    def signal(self, bars: pd.DataFrame) -> np.ndarray:
        c = bars["close"].to_numpy(float)
        r = np.r_[np.nan, c[1:] / c[:-1] - 1.0]
        r[~bars["valid"].to_numpy(bool)] = np.nan
        s = pd.Series(r, index=pd.DatetimeIndex(bars["ts"]))
        tr = trades_one_root(s, self.p, self.n_roots)
        tgt = np.zeros(len(bars))
        for t in tr.itertuples():
            x = len(bars) if (t.exit_i is None or (isinstance(t.exit_i, float) and np.isnan(t.exit_i))) else int(t.exit_i)
            tgt[int(t.entry_i):x] = t.w
        return tgt


def harness_frame(r_raw: pd.Series) -> pd.DataFrame:
    first = r_raw.first_valid_index()
    s = r_raw.loc[first:]
    valid = s.notna().to_numpy()
    px = np.cumprod(1.0 + np.nan_to_num(s.to_numpy(float), nan=0.0))
    ts = pd.DatetimeIndex(s.index)
    return pd.DataFrame({"ts": ts, "open": px, "high": px, "low": px, "close": px, "valid": valid,
                         "day_id": np.arange(len(s)), "trading_day": ts.tz_localize(None) if ts.tz is not None else ts})
