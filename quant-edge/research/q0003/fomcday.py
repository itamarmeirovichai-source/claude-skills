"""Q-0003 FOMC-day AUDUSD long (registered 93cb97a). One code path for the backtest, the harness and the variants.

As registered: event set = cal_fomc rows with scheduled=True (statement day = New York date `date_local`).
ENTRY at the open of the first 1m bar at or after 00:05 Europe/Prague on the statement day (= 18:05 NY the evening
before outside the DST-mismatch weeks). EXIT at the open of the 15:58 America/New_York bar of the statement day.
LONG AUDUSD, every scheduled statement day. Missing entry/exit bar -> event skipped (no forward fill).
weight = (0.10/sqrt(252)) / sigma, sigma = EWMA (com 60) s.d. of daily 17:00 NY close-to-close log returns through
the close before entry. Cost 1.5 bp per side (2x: 3 bp).

Conventions fixed before the OOS read: the entry bar must open before the exit instant (else "missing"); sigma needs
60 returns (no trade before); `exit_mode="exact"` is the registered skip rule, which reads whether the 15:58 bar
exists, i.e. post-entry data; `exit_mode="ex_ante"` instead exits at the first bar at or after 15:58 NY and is the
variant the truncation harness can certify (criterion 8: as-written vs ex-ante, the worse is reported).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "batch1"))
import fxkit as fx  # noqa: E402

COST_BP = 1.5


@dataclass(frozen=True)
class Params:
    entry_clock: str = "00:05"        # Europe/Prague, on the statement day
    exit_clock: str = "15:58"         # America/New_York, on the statement day
    com: float = 60.0
    exit_mode: str = "exact"          # "exact" (registered) or "ex_ante"
    entry_shift_min: float = 0.0      # neighbourhood: move the entry instant by this many minutes (+ = later)
    exit_shift_min: float = 0.0       # neighbourhood: move the exit instant by this many minutes


def statement_days(cal: pd.DataFrame) -> list:
    c = cal[cal["scheduled"].astype(str).str.lower() == "true"]
    return sorted(pd.to_datetime(c["date_local"]).dt.normalize().unique())


def events(bars: pd.DataFrame, days, p: Params) -> pd.DataFrame:
    tsn = fx.ts_ns(bars)
    closes = fx.ny_closes(bars)
    sig = fx.ewm_sd(closes, p.com)
    sd20 = closes["r"].rolling(20, min_periods=15).std()
    o = bars["open"].to_numpy(float)
    rows = []
    for D in days:
        e_inst = fx.local_instant(D, p.entry_clock, fx.PRG) + pd.Timedelta(minutes=p.entry_shift_min)
        x_inst = fx.local_instant(D, p.exit_clock, fx.NY) + pd.Timedelta(minutes=p.exit_shift_min)
        status = "ok"
        ei = fx.bar_at_or_after(tsn, e_inst, before=x_inst)
        if ei < 0:
            status = "missing_entry"
        s = fx.value_before(closes, sig, bars["ts"].iloc[ei]) if ei >= 0 else np.nan
        if status == "ok" and not (np.isfinite(s) and s > 0):
            status = "no_sigma"
        w = fx.TARGET_DAILY / s if status == "ok" else np.nan
        xi = fx.bar_at(tsn, x_inst) if p.exit_mode == "exact" else fx.bar_at_or_after(tsn, x_inst)
        if status == "ok" and xi < 0:
            status = "missing_exit"
        rows.append({"day": pd.Timestamp(D).date(), "entry_i": ei, "exit_i": xi if status == "ok" else -1, "w": w if status in ("ok", "missing_exit") else np.nan, "sigma": s,
                     "sd20": fx.value_before(closes, sd20, bars["ts"].iloc[ei]) if ei >= 0 else np.nan,
                     "entry_ts": bars["ts"].iloc[ei] if ei >= 0 else pd.NaT, "entry_target": e_inst,
                     "entry_px": o[ei] if ei >= 0 else np.nan, "exit_px": o[xi] if (status == "ok") else np.nan, "status": status})
    ev = pd.DataFrame(rows)
    ok = ev["status"] == "ok"
    ev["ret"] = np.where(ok, ev["exit_px"] / ev["entry_px"] - 1.0, np.nan)
    ev["gross"] = ev["w"] * ev["ret"]
    ev["cost1"] = ev["w"] * 2 * COST_BP * 1e-4
    return ev


class FomcRule:
    """qe.engine harness interface: target[i] = weight held over bar i (open i -> open i+1)."""
    name = "fomc_day_audusd"
    mode = "target"

    def __init__(self, days, p: Params):
        self.days, self.p, self.params = days, p, {}

    def signal(self, bars):
        ev = events(bars, self.days, self.p)
        t = np.zeros(len(bars))
        for r in ev.itertuples():
            if r.status == "ok":
                t[int(r.entry_i):int(r.exit_i)] = r.w
            elif r.status == "missing_exit" and self.p.exit_mode == "ex_ante":
                t[int(r.entry_i):] = r.w          # exit not yet in the data: the position is held (decided ex ante)
        return t
