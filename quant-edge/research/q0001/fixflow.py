"""Q-0001 London-fix month-end equity-hedge legs (registered 93cb97a). One code path for backtest, harness, variants.

As registered: event day D = last Monday-Friday of each calendar month (no UK holiday adjustment).
S_D = [GLSTOCK(T1)/GLSTOCK(M0) - 1] - [USLCAP(T1)/USLCAP(M0) - 1], M0 = last row dated in the previous calendar month,
T1 = last row dated strictly before D; both rows need obs flag 1 (GLSTOCK and USLCAP), else no trade.
S_D > 0 -> SELL EURUSD, GBPUSD, AUDUSD; S_D < 0 -> BUY; S_D = 0 or missing -> no trade.
ENTRY open of the 10:00 London 1m bar; EXIT open of the 15:57 London 1m bar. A pair-event is skipped if the
09:55-15:57 London span has more than 10 missing 1m bars or the entry/exit bar is missing (no forward fill).
w_p = (0.10/sqrt(252)) / sigma_p / 3, sigma_p = EWMA (com 60) s.d. of daily 17:00 NY close-to-close log returns
through the close before D. Costs per side: EURUSD 1.0 bp, GBPUSD 1.2 bp, AUDUSD 1.5 bp.

Conventions fixed before the OOS read:
  * M0 must be served data from the END of the previous month: the gateway serves IS to 2015-02-13 and OOS from
    2015-03-02, so for an event whose previous month is cut by an unserved gap, the last served row of that month is
    not M0. Rule: M0 must be dated no earlier than the previous month's last weekday minus 4 calendar days, else no
    trade (affects March 2015 and the first IS month). T1 must be dated after M0.
  * "09:55-15:57 span" = bar opens in [entry-5 min, exit] inclusive (363 minutes as registered).
  * filter="as_written" is the registered skip rule (reads post-entry bar availability); filter="ex_ante" counts
    missing bars only in [entry-5 min, entry] and exits at the first bar at or after the exit instant.
  * sigma as in Q-0003 (pandas ewm(com, min_periods=com).std(), read at the last 17:00 NY close before the entry bar).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "batch1"))
import fxkit as fx  # noqa: E402

PAIRS = ("EURUSD", "GBPUSD", "AUDUSD")
COST_BP = {"EURUSD": 1.0, "GBPUSD": 1.2, "AUDUSD": 1.5}


@dataclass(frozen=True)
class Params:
    entry_clock: str = "10:00"       # Europe/London
    exit_clock: str = "15:57"        # Europe/London
    pre_minutes: int = 5             # span starts 5 min before entry (09:55)
    max_missing: int = 10
    threshold: float = 0.0
    com: float = 60.0
    filter: str = "as_written"       # or "ex_ante"
    entry_shift_min: float = 0.0
    exit_shift_min: float = 0.0


def event_days(start, end) -> list:
    """Last Monday-Friday of each calendar month with the day inside [start, end]."""
    months = pd.period_range(pd.Timestamp(start).to_period("M"), pd.Timestamp(end).to_period("M"), freq="M")
    out = []
    for m in months:
        last = m.end_time.normalize()
        while last.dayofweek >= 5:
            last -= pd.Timedelta(days=1)
        if pd.Timestamp(start) <= last <= pd.Timestamp(end):
            out.append(last)
    return out


def signal_table(assets: pd.DataFrame, days, threshold: float = 0.0) -> pd.DataFrame:
    """S_D per event day from the daily_assets frame (date-indexed, naive dates). Only rows dated < D are read."""
    idx = assets.index
    rows = []
    for D in days:
        D = pd.Timestamp(D)
        prev_end = (D.to_period("M") - 1).end_time.normalize()
        while prev_end.dayofweek >= 5:
            prev_end -= pd.Timedelta(days=1)
        m0c = idx[(idx < D.replace(day=1)) & (idx >= (D.to_period("M") - 1).start_time)]
        t1c = idx[idx < D]
        status, S = "ok", np.nan
        if len(m0c) == 0 or len(t1c) == 0:
            status = "no_rows"
        else:
            M0, T1 = m0c[-1], t1c[-1]
            if M0 < prev_end - pd.Timedelta(days=4):
                status = "m0_unserved"
            elif T1 <= M0:
                status = "t1_not_after_m0"
            else:
                a0, a1 = assets.loc[M0], assets.loc[T1]
                if not (a0["obs_GLSTOCK"] == 1 and a0["obs_USLCAP"] == 1 and a1["obs_GLSTOCK"] == 1 and a1["obs_USLCAP"] == 1):
                    status = "obs_flag"
                else:
                    S = (a1["GLSTOCK"] / a0["GLSTOCK"] - 1) - (a1["USLCAP"] / a0["USLCAP"] - 1)
                    if not np.isfinite(S) or S == threshold:
                        status = "zero_or_missing"
        side = 0 if status != "ok" else (-1 if S > threshold else (1 if S < threshold else 0))
        rows.append({"day": D, "S": S, "side": side, "sig_status": status})
    return pd.DataFrame(rows)


def pair_events(bars: pd.DataFrame, pair: str, sig: pd.DataFrame, p: Params, closes=None) -> pd.DataFrame:
    tsn = fx.ts_ns(bars)
    closes = closes if closes is not None else fx.ny_closes(bars)
    sd = fx.ewm_sd(closes, p.com)
    sd20 = closes["r"].rolling(20, min_periods=15).std()
    o = bars["open"].to_numpy(float)
    rows = []
    for r in sig.itertuples():
        D = r.day
        e_inst = fx.local_instant(D, p.entry_clock, fx.LON) + pd.Timedelta(minutes=p.entry_shift_min)
        x_inst = fx.local_instant(D, p.exit_clock, fx.LON) + pd.Timedelta(minutes=p.exit_shift_min)
        status = "ok" if r.side != 0 else "no_signal"
        ei = fx.bar_at(tsn, e_inst)
        if status == "ok" and ei < 0:
            status = "missing_entry"
        a = e_inst - pd.Timedelta(minutes=p.pre_minutes)
        if p.filter == "as_written":
            exp = int((x_inst - a).total_seconds() // 60) + 1
            miss = exp - fx.count_bars(tsn, a, x_inst)
            xi = fx.bar_at(tsn, x_inst)
        else:
            exp = p.pre_minutes + 1
            miss = exp - fx.count_bars(tsn, a, e_inst)
            xi = fx.bar_at_or_after(tsn, x_inst)
        s = fx.value_before(closes, sd, bars["ts"].iloc[ei]) if ei >= 0 else np.nan
        if status == "ok" and not (np.isfinite(s) and s > 0):
            status = "no_sigma"
        if status == "ok" and miss > p.max_missing:
            status = "too_many_missing"
        if status == "ok" and xi < 0:
            status = "missing_exit"
        w = fx.TARGET_DAILY / s / 3.0 if status in ("ok", "missing_exit") else np.nan
        rows.append({"day": D, "pair": pair, "side": r.side, "S": r.S, "entry_i": ei, "exit_i": xi if status == "ok" else -1,
                     "w": w, "sigma": s, "sd20": fx.value_before(closes, sd20, bars["ts"].iloc[ei]) if ei >= 0 else np.nan,
                     "missing": miss, "entry_px": o[ei] if ei >= 0 else np.nan, "exit_px": o[xi] if status == "ok" else np.nan,
                     "status": status})
    ev = pd.DataFrame(rows)
    ok = ev["status"] == "ok"
    ev["ret"] = np.where(ok, ev["exit_px"] / ev["entry_px"] - 1.0, np.nan)
    ev["gross"] = ev["w"] * ev["side"] * ev["ret"]
    ev["bench"] = ev["w"] * ev["ret"]                       # long the foreign currency, same minutes, same weight
    ev["cost1"] = ev["w"] * 2 * COST_BP[pair] * 1e-4
    return ev


class FixRule:
    """qe.engine harness interface for one pair: target[i] = signed weight held over bar i."""
    name = "fix_month_end"
    mode = "target"

    def __init__(self, pair, sig, p: Params):
        self.pair, self.sig, self.p, self.params = pair, sig, p, {}

    def signal(self, bars):
        ev = pair_events(bars, self.pair, self.sig, self.p)
        t = np.zeros(len(bars))
        for r in ev.itertuples():
            if r.status == "ok":
                t[int(r.entry_i):int(r.exit_i)] = r.w * r.side
            elif r.status == "missing_exit" and self.p.filter == "ex_ante":
                t[int(r.entry_i):] = r.w * r.side          # exit not yet in the data: held, decided ex ante
        return t
