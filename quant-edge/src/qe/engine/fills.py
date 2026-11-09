"""qe.engine.fills — instruments, slippage, and the fill models (market, limit, stop, bracket, flat-by).

Fixed conventions (CONVENTIONS.md, section "Fills"):
  * Market orders fill at the NEXT bar open relative to the deciding bar (the bar whose close produced the decision);
    in array terms a target decided from bars < i fills at open[i]. Costs are charged per side as points
    (slippage floor x window multiplier + commission / point value); fill prices in the trade table are the
    reference prices (open, stop, limit) and the cost is a separate column, so the 1x and 2x cost runs share one
    trade path and only the cost column doubles.
  * Limit orders fill only when price trades THROUGH the limit: a long target at L fills when high > L (strictly), a
    short target when low < L; a gap through the limit at the open fills at the limit price (conservative). Limit fills
    pay commission but no slippage.
  * Stop orders are sampled at bar granularity: a long stop at S triggers when low <= S, filled at S; when the bar
    OPENS through the stop (open <= S) the fill is the open (gap-through fills at the open). Stops pay slippage.
  * Bar ambiguity: when one bar touches both the stop and the target, the STOP is assumed first.
  * Flat-by: the exit market order is sent at the open of the first bar whose tday_minute >= deadline - N minutes
    (`flat_by_margin_minutes`); no new entry is taken at or after that minute. On a half day the deadline is
    min(firm deadline, RTH early close) (qe.sessions.flat_by_tminute). A day without a bar at or after the flat-by minute
    closes at the last bar of its session (exit_reason = "flat_by_lastbar", counted in the diagnostics).
  * Entry delay: `entry_delay_bars` shifts every entry (and target change) that many bars later; the bracket distances
    stay relative to the ORIGINAL reference open, so a delayed entry changes the fill price, not the stop and target.
  * Extra slippage: the floor is multiplied inside the windows of `SlippageModel.windows` (default x2 for 02:00-02:05 ET,
    the RTH open 09:30-09:32 ET, the 18:00-18:02 ET reopen, the 15:59-16:01 cash close and the 16:14-16:16 ET settlement).
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from numba import njit

from .. import sessions
from .bars import ts_take

# ----------------------------------------------------------------------------------------------------- instruments
@dataclass(frozen=True)
class Instrument:
    root: str
    tick: float                 # minimum price increment in points
    point_value: float          # money per 1.0 point per contract (or per unit)
    slip_pts: float = 0.0       # per-side slippage floor in points (market orders, RTH)
    slip_bp: float = 0.0        # per-side slippage floor in basis points of price (used when slip_pts == 0)
    commission: float = 0.0     # money per side per contract
    source: str = "briefs/00-common.md cost floors (market orders, RTH)"

    def slip_points(self, price: np.ndarray) -> np.ndarray:
        if self.slip_pts > 0:
            return np.full_like(np.asarray(price, float), self.slip_pts)
        return np.asarray(price, float) * self.slip_bp / 1e4

    @property
    def commission_pts(self) -> float:
        return self.commission / self.point_value


INSTRUMENTS: Dict[str, Instrument] = {
    "ES": Instrument("ES", 0.25, 50.0, slip_pts=0.30, commission=2.50),
    "MES": Instrument("MES", 0.25, 5.0, slip_pts=0.25, commission=0.80),
    "NQ": Instrument("NQ", 0.25, 20.0, slip_pts=0.25, commission=2.50),
    "MNQ": Instrument("MNQ", 0.25, 2.0, slip_pts=0.25, commission=0.80,
                      source="assumed as MES (00-common.md gives no MNQ floor); confirm with the Rules Keeper"),
    "SPY": Instrument("SPY", 0.01, 1.0, slip_bp=0.5, commission=0.0),
    "CFD_INDEX": Instrument("CFD_INDEX", 0.01, 1.0, slip_bp=1.0, source="00-common.md: CFDs 0.5-1.5 bp FX/indices; 1.0 bp used"),
    "CFD_FX": Instrument("CFD_FX", 0.00001, 1.0, slip_bp=1.0, source="00-common.md: CFDs 0.5-1.5 bp FX/indices; 1.0 bp used"),
    "CFD_GOLD": Instrument("CFD_GOLD", 0.01, 1.0, slip_bp=1.0),
    "CFD_WTI": Instrument("CFD_WTI", 0.01, 1.0, slip_bp=2.5),
    "CFD_NATGAS": Instrument("CFD_NATGAS", 0.001, 1.0, slip_bp=8.0),
    "CRYPTO_PERP": Instrument("CRYPTO_PERP", 0.01, 1.0, slip_bp=7.0, source="00-common.md: 7 bp per side + funding (funding not modelled here)"),
}


def instrument(root: str, **overrides) -> Instrument:
    if root not in INSTRUMENTS:
        raise KeyError(f"no cost floor for {root!r}; known: {sorted(INSTRUMENTS)}. Add it with its source before use.")
    return replace(INSTRUMENTS[root], **overrides) if overrides else INSTRUMENTS[root]


# -------------------------------------------------------------------------------------------------------- slippage
def _tmin(ny_h: int, ny_m: int) -> int:
    return int(sessions.tday_minute(ny_h * 60 + ny_m))


@dataclass(frozen=True)
class SlippageModel:
    """Per-side slippage multiplier by tday_minute window (minutes since the 18:00 ET reopen, [start, end))."""
    windows: Tuple[Tuple[int, int, float], ...] = (
        (_tmin(2, 0), _tmin(2, 5), 2.0),       # 02:00-02:05 ET European open
        (_tmin(9, 30), _tmin(9, 32), 2.0),     # RTH open
        (_tmin(18, 0), _tmin(18, 2), 2.0),     # Globex reopen (tday 0-2)
        (_tmin(15, 59), _tmin(16, 1), 2.0),    # cash close
        (_tmin(16, 14), _tmin(16, 16), 2.0),   # ES/NQ settlement 15:14:30-15:15 CT
    )
    outside_rth_multiplier: float = 1.0        # applied to bars with is_rth == False (in addition to windows)

    def multiplier(self, tday_minute: np.ndarray, is_rth: Optional[np.ndarray] = None) -> np.ndarray:
        t = np.asarray(tday_minute)
        m = np.ones(t.shape, dtype=float)
        for a, b, k in self.windows:
            m = np.where((t >= a) & (t < b), np.maximum(m, k), m)
        if is_rth is not None and self.outside_rth_multiplier != 1.0:
            m = np.where(~np.asarray(is_rth, bool), np.maximum(m, self.outside_rth_multiplier), m)
        return m


def per_bar_costs(bars: pd.DataFrame, inst: Instrument, slip: SlippageModel = SlippageModel()) -> Tuple[np.ndarray, np.ndarray]:
    """(market_cost_pts, limit_cost_pts) per bar per contract per side at 1x: slippage x multiplier + commission; commission only."""
    price = bars["open"].to_numpy(float)
    mult = slip.multiplier(bars["tday_minute"].to_numpy(), bars["is_rth"].to_numpy() if "is_rth" in bars else None)
    market = inst.slip_points(price) * mult + inst.commission_pts
    limit = np.full(len(bars), inst.commission_pts)
    return market, limit


# ------------------------------------------------------------------------------------------------ bracket kernel
EXIT_REASONS = {0: "open", 1: "stop", 2: "target", 3: "flat_by", 4: "max_hold", 5: "flat_by_lastbar", 6: "end_of_data", 7: "session_end"}


@njit(cache=True)
def _bracket_kernel(o, h, l, c, day_id, tday_min, flat_by, mkt_cost, lim_cost,
                    entry_idx, side, qty, stop_pts, target_pts, max_hold, delay, one_at_a_time, intraday_only):
    """Sequential bracket simulation. Distances are relative to the reference open o[entry_idx]; the fill happens at
    o[entry_idx + delay]. Returns per-entry arrays; status 0 = taken, 1 = skipped (position open), 2 = skipped (past
    flat-by or no bar), 3 = skipped (delayed bar in another day)."""
    n = o.shape[0]
    m = entry_idx.shape[0]
    status = np.zeros(m, dtype=np.int8)
    fill_i = np.full(m, -1, dtype=np.int64)
    exit_i = np.full(m, -1, dtype=np.int64)
    fill_px = np.zeros(m)
    exit_px = np.zeros(m)
    reason = np.full(m, -1, dtype=np.int8)
    cost = np.zeros(m)      # 1x cost in points per contract (both sides)
    busy_until = -1
    for k in range(m):
        i0 = entry_idx[k]
        i = i0 + delay
        if i >= n or i0 < 0:
            status[k] = 2
            continue
        if day_id[i] != day_id[i0]:
            status[k] = 3
            continue
        if one_at_a_time and i <= busy_until:
            status[k] = 1
            continue
        if tday_min[i] >= flat_by[i]:
            status[k] = 2
            continue
        s = side[k]
        ref = o[i0]
        stop = ref - s * stop_pts[k]
        tgt = ref + s * target_pts[k]
        fp = o[i]
        fill_i[k] = i
        fill_px[k] = fp
        ck = mkt_cost[i]
        j = i
        done = False
        # a delayed fill that is already through the stop or the target exits at once at the fill price
        if delay > 0 and ((s > 0 and (fp <= stop or fp >= tgt)) or (s < 0 and (fp >= stop or fp <= tgt))):
            exit_i[k] = i
            exit_px[k] = fp
            reason[k] = 1 if ((s > 0 and fp <= stop) or (s < 0 and fp >= stop)) else 2
            ck += mkt_cost[i]
            done = True
            j = n
        while j < n:
            if j > i:
                if day_id[j] != day_id[i] and intraday_only:
                    # the session ended without a bar at/after the flat-by minute: closed at the last bar's close
                    exit_i[k] = j - 1
                    exit_px[k] = c[j - 1]
                    reason[k] = 5
                    ck += mkt_cost[j - 1]
                    done = True
                    break
                if tday_min[j] >= flat_by[j] and intraday_only:
                    exit_i[k] = j
                    exit_px[k] = o[j]
                    reason[k] = 3
                    ck += mkt_cost[j]
                    done = True
                    break
                if max_hold > 0 and j - i >= max_hold:
                    exit_i[k] = j
                    exit_px[k] = o[j]
                    reason[k] = 4
                    ck += mkt_cost[j]
                    done = True
                    break
                # gap through the stop at the open: filled at the open
                if (s > 0 and o[j] <= stop) or (s < 0 and o[j] >= stop):
                    exit_i[k] = j
                    exit_px[k] = o[j]
                    reason[k] = 1
                    ck += mkt_cost[j]
                    done = True
                    break
                # gap through the target at the open: limit fills at the limit price (conservative)
                if (s > 0 and o[j] > tgt) or (s < 0 and o[j] < tgt):
                    exit_i[k] = j
                    exit_px[k] = tgt
                    reason[k] = 2
                    ck += lim_cost[j]
                    done = True
                    break
            stop_hit = (s > 0 and l[j] <= stop) or (s < 0 and h[j] >= stop)
            tgt_hit = (s > 0 and h[j] > tgt) or (s < 0 and l[j] < tgt)
            if stop_hit:                       # ambiguity: stop first
                exit_i[k] = j
                exit_px[k] = stop
                reason[k] = 1
                ck += mkt_cost[j]
                done = True
                break
            if tgt_hit:
                exit_i[k] = j
                exit_px[k] = tgt
                reason[k] = 2
                ck += lim_cost[j]
                done = True
                break
            j += 1
        if not done:
            exit_i[k] = n - 1
            exit_px[k] = c[n - 1]
            reason[k] = 6
            ck += mkt_cost[n - 1]
        cost[k] = ck
        busy_until = exit_i[k]
    return status, fill_i, fill_px, exit_i, exit_px, reason, cost


@dataclass
class BracketOrders:
    """Entries decided at the information set of bar `entry_idx`'s open (from bars < entry_idx): reference price =
    open[entry_idx]; side +1/-1; stop and target distances in points (target <= 0 means none); qty in contracts."""
    entry_idx: np.ndarray
    side: np.ndarray
    stop_pts: np.ndarray
    target_pts: np.ndarray
    qty: Optional[np.ndarray] = None


def flat_by_per_bar(bars: pd.DataFrame, firm: Optional[str], margin_minutes: int) -> np.ndarray:
    """Deadline (tday_minute units) per bar: firm deadline - margin on that trading day; a very large number when no firm."""
    n = len(bars)
    if firm is None:
        return np.full(n, 10 ** 6, dtype=np.int64)
    days = sessions.day_table(pd.Timestamp(bars["trading_day"].min()), pd.Timestamp(bars["trading_day"].max()), bars.attrs.get("root", "ES"))
    dl = sessions.flat_by_tminute(firm, days) - margin_minutes
    m = pd.Series(dl, index=days.index).reindex(pd.DatetimeIndex(bars["trading_day"]))
    out = m.to_numpy(float)
    if np.isnan(out).any():
        out = np.where(np.isnan(out), 10 ** 6, out)
    return out.astype(np.int64)


def run_brackets(bars: pd.DataFrame, orders: BracketOrders, inst: Instrument, *, firm: Optional[str] = None,
                 flat_by_margin_minutes: int = 2, max_hold_bars: int = 0, entry_delay_bars: int = 0,
                 one_at_a_time: bool = True, intraday_only: bool = True, slip: SlippageModel = SlippageModel()) -> pd.DataFrame:
    """Simulate bracket trades. Returns the trade table (one row per taken entry) with columns
    entry_idx, fill_idx, exit_idx, side, qty, ref_px, fill_px, exit_px, stop_pts, target_pts, exit_reason, gross_pts
    (per contract), cost_pts_1x (both sides, per contract), r_mult (gross / stop_pts), hold_bars, hold_minutes, day_id,
    and the skipped counts in attrs."""
    o, h, l, c = (bars[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    day_id = bars["day_id"].to_numpy(np.int64)
    tday = bars["tday_minute"].to_numpy(np.int64)
    fb = flat_by_per_bar(bars, firm, flat_by_margin_minutes)
    mkt, lim = per_bar_costs(bars, inst, slip)
    qty = orders.qty if orders.qty is not None else np.ones(len(orders.entry_idx))
    ei = np.asarray(orders.entry_idx, np.int64)
    order = np.argsort(ei, kind="stable")
    ei = ei[order]
    side = np.asarray(orders.side, np.int64)[order]
    sp = np.asarray(orders.stop_pts, float)[order]
    tp = np.asarray(orders.target_pts, float)[order]
    q = np.asarray(qty, float)[order]
    if (sp <= 0).any():
        raise ValueError("stop_pts must be positive for every bracket order")
    tp = np.where(tp <= 0, np.inf, tp)
    status, fi, fpx, xi, xpx, reason, cost = _bracket_kernel(o, h, l, c, day_id, tday, fb, mkt, lim, ei, side, q, sp, tp,
                                                             int(max_hold_bars), int(entry_delay_bars), bool(one_at_a_time), bool(intraday_only))
    taken = status == 0
    t = pd.DataFrame({"entry_idx": ei[taken], "fill_idx": fi[taken], "exit_idx": xi[taken], "side": side[taken], "qty": q[taken],
                      "ref_px": o[ei[taken]], "fill_px": fpx[taken], "exit_px": xpx[taken], "stop_pts": sp[taken],
                      "target_pts": np.where(np.isinf(tp[taken]), 0.0, tp[taken]),
                      "exit_reason": [EXIT_REASONS[int(r)] for r in reason[taken]]})
    t["gross_pts"] = t["side"] * (t["exit_px"] - t["fill_px"])
    t["cost_pts_1x"] = cost[taken]
    t["r_mult"] = t["gross_pts"] / t["stop_pts"]
    t["hold_bars"] = t["exit_idx"] - t["fill_idx"]
    bm = int(bars["bar_minutes"].iloc[0])
    t["hold_minutes"] = t["hold_bars"] * bm
    t["day_id"] = day_id[t["fill_idx"].to_numpy()]
    t["trading_day"] = bars["trading_day"].to_numpy()[t["fill_idx"].to_numpy()]
    t["entry_ts"] = ts_take(bars["ts"], t["fill_idx"].to_numpy())
    t["exit_ts"] = ts_take(bars["ts"], t["exit_idx"].to_numpy())
    t.attrs["skipped_position_open"] = int((status == 1).sum())
    t.attrs["skipped_past_flat_by"] = int((status == 2).sum())
    t.attrs["skipped_delay_crossed_day"] = int((status == 3).sum())
    t.attrs["n_orders"] = int(len(ei))
    return t


def trades_to_fills(trades: pd.DataFrame) -> pd.DataFrame:
    """Two fills per trade: (bar_idx, qty signed, price, cost_pts per contract-side)."""
    e = pd.DataFrame({"bar_idx": trades["fill_idx"], "qty": trades["side"] * trades["qty"], "price": trades["fill_px"],
                      "cost_pts": 0.0, "trade_id": np.arange(len(trades))})
    x = pd.DataFrame({"bar_idx": trades["exit_idx"], "qty": -trades["side"] * trades["qty"], "price": trades["exit_px"],
                      "cost_pts": trades["cost_pts_1x"], "trade_id": np.arange(len(trades))})
    # the whole round-trip cost is booked on the exit bar (the day of the exit); sums are unchanged
    f = pd.concat([e, x], ignore_index=True).sort_values(["bar_idx", "trade_id"], kind="stable").reset_index(drop=True)
    return f


# ------------------------------------------------------------------------------------------- target-position mode
def execute_targets(bars: pd.DataFrame, target: np.ndarray, inst: Instrument, *, firm: Optional[str] = None,
                    flat_by_margin_minutes: int = 2, entry_delay_bars: int = 0, lag_bars: int = 0,
                    fill_at: str = "open", slip: SlippageModel = SlippageModel(), intraday_only: bool = False) -> Tuple[np.ndarray, pd.DataFrame]:
    """Turn a per-bar target position (decided from bars < i, held over bar i) into fills.

    fill_at = "open": a change of target at bar i fills at open[i] (market at next open; the base case).
    fill_at = "close": fills at close[i-1] (the optimistic 'signal at close, fill at close' variant of the lag harness).
    lag_bars = k shifts fills to open[i+k] (lag 2 = 1). entry_delay_bars shifts the whole target series later.
    Flat-by (firm) zeroes the target from the flat-by minute to the session end; intraday_only also zeroes it outside
    the session. Returns (position per bar actually held, fills table)."""
    n = len(bars)
    tgt = np.asarray(target, float).copy()
    if tgt.shape[0] != n:
        raise ValueError("target must have one value per bar")
    tgt = np.nan_to_num(tgt, nan=0.0)
    shift = int(entry_delay_bars) + int(lag_bars)
    if shift > 0:
        tgt = np.r_[np.zeros(shift), tgt[:-shift]]
    tday = bars["tday_minute"].to_numpy(np.int64)
    if firm is not None:
        fb = flat_by_per_bar(bars, firm, flat_by_margin_minutes)
        tgt = np.where(tday >= fb, 0.0, tgt)
    if intraday_only or firm is not None:
        tgt = np.where(bars["in_session"].to_numpy(bool), tgt, 0.0)
        # also force flat at the last bar of each trading day when the next bar is in a new day
        day_id = bars["day_id"].to_numpy()
        last_of_day = np.r_[day_id[1:] != day_id[:-1], True]
        if intraday_only:
            tgt = np.where(last_of_day, 0.0, tgt)
    pos = tgt
    dq = np.diff(np.r_[0.0, pos])
    idx = np.nonzero(dq)[0]
    mkt, _ = per_bar_costs(bars, inst, slip)
    if fill_at == "open":
        price = bars["open"].to_numpy(float)[idx]
        cost = mkt[idx]
    elif fill_at == "close":
        cl = bars["close"].to_numpy(float)
        price = cl[np.maximum(idx - 1, 0)]
        cost = mkt[np.maximum(idx - 1, 0)]
    else:
        raise ValueError("fill_at must be 'open' or 'close'")
    fills = pd.DataFrame({"bar_idx": idx, "qty": dq[idx], "price": price, "cost_pts": cost, "trade_id": np.arange(idx.size)})
    return pos, fills


# ------------------------------------------------------------------------------------------- fills -> bar P&L
@njit(cache=True)
def _bar_pnl_kernel(close, fill_bar, fill_qty, fill_price, fill_cost, n):
    """Exact mark-to-market per bar in points: pos_before * (close[i] - close[i-1]) + sum over fills at bar i of
    qty * (close[i] - price). cost_pts per contract-side is charged on the fill bar. Returns (gross, cost, position)."""
    gross = np.zeros(n)
    cost = np.zeros(n)
    pos = np.zeros(n)
    p = 0.0
    k = 0
    m = fill_bar.shape[0]
    prev_close = close[0]
    for i in range(n):
        g = p * (close[i] - prev_close)
        while k < m and fill_bar[k] == i:
            q = fill_qty[k]
            g += q * (close[i] - fill_price[k])
            cost[i] += abs(q) * fill_cost[k]
            p += q
            k += 1
        gross[i] = g
        pos[i] = p
        prev_close = close[i]
    return gross, cost, pos


def bar_pnl(bars: pd.DataFrame, fills: pd.DataFrame) -> pd.DataFrame:
    """Per-bar gross P&L (points per contract-weighted), 1x cost (points) and end-of-bar position from a fills table."""
    close = bars["close"].to_numpy(float)
    f = fills.sort_values(["bar_idx", "trade_id"], kind="stable") if len(fills) else fills
    gross, cost, pos = _bar_pnl_kernel(close, f["bar_idx"].to_numpy(np.int64), f["qty"].to_numpy(float),
                                       f["price"].to_numpy(float), f["cost_pts"].to_numpy(float), len(bars))
    return pd.DataFrame({"gross_pts": gross, "cost_pts_1x": cost, "position": pos})
