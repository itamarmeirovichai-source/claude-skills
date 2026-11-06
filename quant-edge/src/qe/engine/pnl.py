"""qe.engine.pnl — simulate() and the daily mark-to-market P&L with every standard table.

Units: points per contract (qty-weighted), ticks, money (point_value x points), R (points / r_points, where r_points is
config.r_points, else the median stop distance of the run's bracket trades, else the ex-ante daily vol in points).
Costs: 1x and 2x in the same run (net_1x = gross - cost, net_2x = gross - 2 cost); every table carries both.
Daily P&L is the exact mark-to-market by bar closes aggregated to the trading day (18:00 ET boundary), so the sum of daily
P&L equals the sum of trade P&L plus the open mark at the end of the sample.

Provenance: simulate() refuses a bar frame that is neither gateway-marked (attrs["registered_id"], set by
qe.engine.run.run_registered after qe.gateway.load) nor synthetic (attrs["synthetic"], set by bars.synthetic_walk).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np
import pandas as pd

from .. import stats
from . import bars as _bars
from . import fills as _fills


class UnregisteredRunError(RuntimeError):
    """P&L was requested on a bar frame that did not come through qe.gateway.load (or the synthetic generator)."""


@dataclass
class RunConfig:
    root: str = "ES"
    firm: Optional[str] = None                  # None = no flat-by enforcement (FTMO Swing / daily strategies)
    flat_by_margin_minutes: int = 2             # exit order sent at deadline - N minutes
    entry_delay_bars: int = 0                   # 1 and 5 for the alpha-decay runs
    lag_bars: int = 0                           # 0 = next open (lag 1 from the deciding bar), 1 = lag 2
    fill_at: str = "open"                       # "close" = the optimistic signal-at-close/fill-at-close variant
    max_hold_bars: int = 0
    one_at_a_time: bool = True
    intraday_only: bool = True                  # force flat at the session end (futures-firm structures)
    account_usd: float = 100_000.0
    contracts: float = 1.0                      # base position size multiplier for money and breach tables
    r_points: Optional[float] = None
    guard_fraction: float = 0.7
    ftmo_daily_loss: float = 0.05
    ftmo_max_loss: float = 0.10
    trailing_dd_usd: float = 3_000.0            # preliminary trailing-drawdown plan limit per account (row sets the real one)
    vol_tercile_bounds: Optional[tuple] = None  # (b1, b2) fixed in sample; None = computed on the run (flagged)
    vol_window: int = 20
    slip: _fills.SlippageModel = field(default_factory=_fills.SlippageModel)
    inst_overrides: dict = field(default_factory=dict)
    seed: int = 0

    def instrument(self) -> _fills.Instrument:
        return _fills.instrument(self.root, **self.inst_overrides)


@dataclass
class Result:
    config: RunConfig
    mode: str
    trades: pd.DataFrame
    fills: pd.DataFrame
    bar: pd.DataFrame            # gross_pts, cost_pts_1x, position per bar
    daily: pd.DataFrame          # indexed by trading_day
    stats: dict
    tables: Dict[str, pd.DataFrame]
    provenance: dict
    r_points: float
    point_value: float


def require_provenance(bars: pd.DataFrame) -> dict:
    a = bars.attrs
    if a.get("registered_id"):
        return {"registered_id": a["registered_id"], "window": a.get("window"), "dataset": a.get("dataset"), "synthetic": False}
    if a.get("synthetic"):
        return {"registered_id": None, "window": None, "dataset": "synthetic", "synthetic": True, "synthetic_params": a.get("synthetic_params")}
    raise UnregisteredRunError("simulate(): the bar frame carries no registered_id (use qe.engine.run.run_registered, which calls "
                               "qe.gateway.load) and is not a synthetic frame; no P&L is computed on data that did not pass the door")


# ------------------------------------------------------------------------------------------------------- simulate
def simulate(bars: pd.DataFrame, rule=None, config: Optional[RunConfig] = None, *, target: Optional[np.ndarray] = None,
             orders: Optional[_fills.BracketOrders] = None, scale: Optional[np.ndarray] = None) -> Result:
    """Run one configuration. Give a rule (signal() or orders()) or a precomputed target / orders.
    `scale` (per bar) multiplies a target position (vol scaler); a bracket order's qty is left to the rule."""
    config = config or RunConfig()
    prov = require_provenance(bars)
    if "day_id" not in bars.columns:
        bars = _bars.tag(bars, config.root)
    inst = config.instrument()
    if rule is not None:
        if rule.mode == "brackets":
            orders = rule.orders(bars)
        else:
            target = rule.signal(bars)
    if orders is not None:
        mode = "brackets"
        trades = _fills.run_brackets(bars, orders, inst, firm=config.firm, flat_by_margin_minutes=config.flat_by_margin_minutes,
                                     max_hold_bars=config.max_hold_bars, entry_delay_bars=config.entry_delay_bars + config.lag_bars,
                                     one_at_a_time=config.one_at_a_time, intraday_only=config.intraday_only, slip=config.slip)
        if config.contracts != 1.0:
            trades["qty"] = trades["qty"] * config.contracts
        fills = _fills.trades_to_fills(trades)
    elif target is not None:
        mode = "target"
        tgt = np.asarray(target, float) * config.contracts
        if scale is not None:
            tgt = np.round(tgt * np.asarray(scale, float))
        pos, fills = _fills.execute_targets(bars, tgt, inst, firm=config.firm, flat_by_margin_minutes=config.flat_by_margin_minutes,
                                            entry_delay_bars=config.entry_delay_bars, lag_bars=config.lag_bars, fill_at=config.fill_at,
                                            slip=config.slip, intraday_only=config.intraday_only)
        trades = _trades_from_position(bars, pos, fills, inst)
    else:
        raise ValueError("simulate needs a rule, a target array or bracket orders")
    bar = _fills.bar_pnl(bars, fills)
    r_points = _r_unit(config, trades, bars)
    daily = aggregate_daily(bars, bar, fills, trades, inst.point_value, r_points, inst.tick)
    st, tables = standard_tables(bars, bar, daily, trades, fills, config, inst, r_points)
    st["n_bars"] = int(len(bars))
    st["mode"] = mode
    st["instrument"] = inst.root
    st["cost_model"] = (f"{inst.root}: {inst.slip_pts} pt" if inst.slip_pts else f"{inst.root}: {inst.slip_bp} bp") + \
                       f" + ${inst.commission:.2f} per side (x{config.slip.windows[0][2]:.0f} in the extra-slippage windows); 2x run in the same tables"
    return Result(config, mode, trades, fills, bar, daily, st, tables, prov, r_points, inst.point_value)


def _r_unit(config: RunConfig, trades: pd.DataFrame, bars: pd.DataFrame) -> float:
    if config.r_points:
        return float(config.r_points)
    if len(trades) and "stop_pts" in trades and trades["stop_pts"].notna().any():
        return float(np.median(trades["stop_pts"].to_numpy(float) * trades["qty"].to_numpy(float)))
    # target mode without a stop: R = one ex-ante daily standard deviation in points of one base unit
    c = bars["close"].to_numpy(float)
    d = _bars.daily_from_bars(bars) if not bars.attrs.get("daily") else None
    if d is not None and len(d) > 2:
        sd = float(np.nanstd(d["close"].diff().to_numpy(float)))
    else:
        sd = float(np.nanstd(np.diff(c)))
    return max(sd * max(config.contracts, 1.0), 1e-9)


def _trades_from_position(bars: pd.DataFrame, pos: np.ndarray, fills: pd.DataFrame, inst) -> pd.DataFrame:
    """Round trips from a position path: a trade starts when the position leaves zero and ends when it returns (or flips)."""
    n = len(pos)
    if n == 0 or not (pos != 0).any():
        return pd.DataFrame(columns=["fill_idx", "exit_idx", "side", "qty", "fill_px", "exit_px", "gross_pts", "cost_pts_1x",
                                     "stop_pts", "r_mult", "hold_bars", "hold_minutes", "day_id", "trading_day", "exit_reason"])
    o = bars["open"].to_numpy(float)
    c = bars["close"].to_numpy(float)
    sgn = np.sign(pos)
    change = np.nonzero(np.r_[True, sgn[1:] != sgn[:-1]])[0]          # first bar of every run of equal sign
    starts = change[sgn[change] != 0]
    nxt = np.searchsorted(change, starts, side="right")                 # index of the next run start
    ends = np.where(nxt < len(change), change[np.minimum(nxt, len(change) - 1)] - 1, n - 1)
    exit_idx = np.minimum(ends + 1, n - 1)
    exit_px = np.where(ends + 1 < n, o[np.minimum(ends + 1, n - 1)], c[ends])
    qty = np.abs(pos[starts])
    side = sgn[starts].astype(int)
    fill_px = o[starts]
    # cost of the fills inside [start, exit]
    fb = fills["bar_idx"].to_numpy()
    fc = (np.abs(fills["qty"].to_numpy()) * fills["cost_pts"].to_numpy())
    csum = np.r_[0.0, np.cumsum(fc)]
    lo = np.searchsorted(fb, starts, side="left")
    hi = np.searchsorted(fb, exit_idx, side="right")
    cost = csum[hi] - csum[lo]
    # gross: mark-to-market of the position over the holding bars (handles size changes inside the trip)
    bar_g = _fills.bar_pnl(bars, fills)["gross_pts"].to_numpy()
    gsum = np.r_[0.0, np.cumsum(bar_g)]
    gross = gsum[exit_idx + 1] - gsum[starts]
    bm = int(bars["bar_minutes"].iloc[0])
    t = pd.DataFrame({"fill_idx": starts, "exit_idx": exit_idx, "side": side, "qty": qty, "fill_px": fill_px, "exit_px": exit_px,
                      "gross_pts": gross, "cost_pts_1x": cost, "stop_pts": np.nan, "r_mult": np.nan,
                      "hold_bars": exit_idx - starts, "hold_minutes": (exit_idx - starts) * bm,
                      "day_id": bars["day_id"].to_numpy()[starts], "trading_day": bars["trading_day"].to_numpy()[starts],
                      "exit_reason": np.where(exit_idx > ends, "target_change", "end_of_data")})
    t["entry_ts"] = _bars.ts_take(bars["ts"], starts)
    t["exit_ts"] = _bars.ts_take(bars["ts"], exit_idx)
    return t


# ------------------------------------------------------------------------------------------------ daily aggregation
def aggregate_daily(bars: pd.DataFrame, bar: pd.DataFrame, fills: pd.DataFrame, trades: pd.DataFrame, point_value: float,
                    r_points: float, tick: float) -> pd.DataFrame:
    day_id = bars["day_id"].to_numpy(np.int64)
    days = _bars.day_index(bars) if not bars.attrs.get("daily") else pd.DatetimeIndex(bars["trading_day"])
    nd = len(days)
    g = np.bincount(day_id, weights=bar["gross_pts"].to_numpy(), minlength=nd)
    cst = np.bincount(day_id, weights=bar["cost_pts_1x"].to_numpy(), minlength=nd)
    d = pd.DataFrame(index=days)
    d.index.name = "trading_day"
    d["gross_pts"] = g
    d["cost_pts_1x"] = cst
    d["net_pts_1x"] = g - cst
    d["net_pts_2x"] = g - 2 * cst
    for k in ("gross", "net_1x", "net_2x"):
        src = {"gross": "gross_pts", "net_1x": "net_pts_1x", "net_2x": "net_pts_2x"}[k]
        d[f"{k}_ticks"] = d[src] / tick
        d[f"{k}_usd"] = d[src] * point_value
        d[f"{k}_R"] = d[src] / r_points
    if len(fills):
        fday = day_id[fills["bar_idx"].to_numpy(np.int64)]
        d["contracts_traded"] = np.bincount(fday, weights=np.abs(fills["qty"].to_numpy(float)), minlength=nd)
    else:
        d["contracts_traded"] = 0.0
    if len(trades):
        d["n_trades"] = np.bincount(trades["day_id"].to_numpy(np.int64), minlength=nd)
    else:
        d["n_trades"] = 0
    pos = bar["position"].to_numpy()
    d["bars_in_market"] = np.bincount(day_id, weights=(pos != 0).astype(float), minlength=nd)
    d["mean_abs_position"] = np.bincount(day_id, weights=np.abs(pos), minlength=nd) / np.maximum(np.bincount(day_id, minlength=nd), 1)
    d["is_roll_week"] = pd.Series(bars["is_roll_week"].to_numpy(bool)).groupby(day_id).first().reindex(range(nd)).fillna(False).to_numpy(bool)
    d["is_half_day"] = pd.Series(bars["is_half_day"].to_numpy(bool)).groupby(day_id).first().reindex(range(nd)).fillna(False).to_numpy(bool)
    d["close"] = pd.Series(bars["close"].to_numpy(float)).groupby(day_id).last().reindex(range(nd)).to_numpy(float)
    return d


# -------------------------------------------------------------------------------------------------- standard tables
def _max_drawdown(x: np.ndarray) -> float:
    eq = np.cumsum(x)
    return float(np.max(np.maximum.accumulate(np.r_[0.0, eq]) - np.r_[0.0, eq]))


def _sharpe_block(x: np.ndarray) -> dict:
    x = np.asarray(x, float)
    if x.size < 3 or x.std(ddof=1) == 0:
        return {"sharpe": float("nan"), "se": float("nan"), "ci90": (float("nan"), float("nan")), "lower90": float("nan"), "lo_factor": float("nan")}
    s = stats.sharpe_se(x)
    return {"sharpe": s["sharpe_annual"], "se": s["se_annual"], "ci90": s["ci90_annual"], "lower90": s["lower90_one_sided_annual"],
            "lo_factor": s["lo_factor"], "sharpe_lo": s["sharpe_annual_lo"], "skew": s["skew"], "kurtosis": s["kurtosis"]}


def standard_tables(bars, bar, daily, trades, fills, config: RunConfig, inst, r_points) -> (dict, Dict[str, pd.DataFrame]):
    d = daily
    nd = len(d)
    years = max(nd / 252.0, 1e-9)
    st: dict = {}
    tables: Dict[str, pd.DataFrame] = {}
    net1 = d["net_1x_usd"].to_numpy()
    net2 = d["net_2x_usd"].to_numpy()
    gross = d["gross_usd"].to_numpy()
    st["days"] = nd
    st["years"] = years
    st["n_trades"] = int(len(trades))
    st["trades_per_year"] = len(trades) / years
    st["trades_per_day"] = len(trades) / max(nd, 1)
    st["days_with_trade"] = int((d["n_trades"] > 0).sum())
    st["distinct_trading_days_with_trade"] = st["days_with_trade"]
    st["turnover_contracts_per_day"] = float(d["contracts_traded"].mean())
    if len(trades):
        hm = trades["hold_minutes"].to_numpy(float)
        st["hold_minutes_median"] = float(np.median(hm))
        st["hold_minutes_mean"] = float(hm.mean())
        st["hold_minutes_max"] = float(hm.max())
        st["share_profit_held_le_10s"] = 0.0   # bars are >= 1 minute: no sub-10-second holds are representable
        st["win_rate"] = float((trades["gross_pts"] - trades["cost_pts_1x"] > 0).mean())
        st["gross_per_trade_pts"] = float((trades["gross_pts"] * trades["qty"]).mean())
        st["net_per_trade_pts_1x"] = float(((trades["gross_pts"] - trades["cost_pts_1x"]) * trades["qty"]).mean())
        st["net_per_trade_pts_2x"] = float(((trades["gross_pts"] - 2 * trades["cost_pts_1x"]) * trades["qty"]).mean())
        st["net_per_trade_ticks_1x"] = st["net_per_trade_pts_1x"] / inst.tick
        st["net_per_trade_usd_1x"] = st["net_per_trade_pts_1x"] * inst.point_value
        st["net_per_trade_usd_2x"] = st["net_per_trade_pts_2x"] * inst.point_value
        if trades["r_mult"].notna().any():
            r = trades["r_mult"].to_numpy(float)
            rc = (trades["gross_pts"] - trades["cost_pts_1x"]).to_numpy(float) / trades["stop_pts"].to_numpy(float)
            rc2 = (trades["gross_pts"] - 2 * trades["cost_pts_1x"]).to_numpy(float) / trades["stop_pts"].to_numpy(float)
            st["mean_R_gross"] = float(np.nanmean(r))
            st["mean_R_net_1x"] = float(np.nanmean(rc))
            st["mean_R_net_2x"] = float(np.nanmean(rc2))
            st["se_R_net_1x"] = float(np.nanstd(rc, ddof=1) / math.sqrt(len(rc))) if len(rc) > 1 else float("nan")
            st["t_R_net_1x_dayclustered"] = stats.clustered_t(rc, trades["day_id"].to_numpy()) if len(rc) > 2 else float("nan")
        tables["exit_reasons"] = trades["exit_reason"].value_counts().rename_axis("exit_reason").to_frame("n")
    for k, x in (("gross", gross), ("net_1x", net1), ("net_2x", net2)):
        st[f"{k}_total_usd"] = float(x.sum())
        st[f"{k}_mean_usd_per_day"] = float(x.mean()) if nd else float("nan")
        st[f"{k}_total_pts"] = float(d[{"gross": "gross_pts", "net_1x": "net_pts_1x", "net_2x": "net_pts_2x"}[k]].sum())
        st[f"{k}_max_drawdown_usd"] = _max_drawdown(x)
        st[f"{k}_worst_day_usd"] = float(x.min()) if nd else float("nan")
        st[f"{k}_t_min"], st[f"{k}_t_iid"], st[f"{k}_t_nw"] = stats.gate_t(x, _longest_hold_days(trades, bars)) if nd > 2 else (float("nan"),) * 3
        st[f"{k}_sharpe"] = _sharpe_block(x)
        st[f"{k}_mean_R_per_day"] = float(d[{"gross": "gross_R", "net_1x": "net_1x_R", "net_2x": "net_2x_R"}[k]].mean()) if nd else float("nan")
    st["r_points"] = r_points
    st["annual_vol_usd"] = float(net1.std(ddof=1) * math.sqrt(252)) if nd > 1 else float("nan")
    st["annual_vol_frac_of_account"] = st["annual_vol_usd"] / config.account_usd
    st["cost_share_of_gross"] = float(d["cost_pts_1x"].sum() / d["gross_pts"].sum()) if d["gross_pts"].sum() > 0 else float("nan")
    # best-20-days fragility
    k20 = min(20, nd)
    top = np.sort(net1)[::-1][:k20]
    st["best20_sum_usd"] = float(top.sum())
    st["best20_share_of_net"] = float(top.sum() / net1.sum()) if net1.sum() > 0 else float("nan")
    st["net_1x_without_best20_usd"] = float(net1.sum() - top.sum())
    # by year
    yr = d.index.year
    by = pd.DataFrame({"year": yr, "net_1x_usd": net1, "net_2x_usd": net2, "gross_usd": gross, "n_trades": d["n_trades"].to_numpy()})
    t = by.groupby("year").agg(days=("net_1x_usd", "size"), net_1x_usd=("net_1x_usd", "sum"), net_2x_usd=("net_2x_usd", "sum"),
                               gross_usd=("gross_usd", "sum"), n_trades=("n_trades", "sum"),
                               sharpe_1x=("net_1x_usd", lambda x: stats.sharpe(x) if len(x) > 2 and x.std() > 0 else float("nan")))
    t["counts"] = t["days"] >= 200
    t["share_of_net"] = t["net_1x_usd"] / net1.sum() if net1.sum() > 0 else float("nan")
    tables["by_year"] = t
    full = t[t["counts"]]
    st["years_counted"] = int(len(full))
    st["years_positive"] = int((full["net_1x_usd"] > 0).sum())
    st["years_needed"] = int(math.floor(0.7 * len(full) + 0.5))
    st["max_year_share"] = float(full["share_of_net"].max()) if len(full) and net1.sum() > 0 else float("nan")
    # by month
    mo = pd.DataFrame({"ym": d.index.to_period("M"), "net_1x_usd": net1}).groupby("ym")["net_1x_usd"].sum()
    st["max_month_share"] = float(mo.max() / net1.sum()) if net1.sum() > 0 else float("nan")
    tables["by_month"] = mo.to_frame()
    # vol terciles (trailing 20-day realized vol of the instrument, ex ante)
    ret = np.log(d["close"]).diff().to_numpy()
    vol = _bars.ex_ante_daily_vol(ret, config.vol_window)
    ok = np.isfinite(vol)
    if config.vol_tercile_bounds is not None:
        b1, b2 = config.vol_tercile_bounds
        st["vol_tercile_bounds_source"] = "fixed in sample (config)"
    elif ok.sum() > 10:
        b1, b2 = np.quantile(vol[ok], [1 / 3, 2 / 3])
        st["vol_tercile_bounds_source"] = "computed on this run (NOT fixed in sample; fix before the OOS read)"
    else:
        b1 = b2 = float("nan")
        st["vol_tercile_bounds_source"] = "n/a"
    terc = np.where(~ok, -1, np.where(vol <= b1, 0, np.where(vol <= b2, 1, 2)))
    vt = pd.DataFrame({"tercile": terc, "net_1x_usd": net1, "net_2x_usd": net2}).groupby("tercile").agg(days=("net_1x_usd", "size"), net_1x_usd=("net_1x_usd", "sum"), net_2x_usd=("net_2x_usd", "sum"))
    vt.index = vt.index.map({-1: "warmup", 0: "low", 1: "mid", 2: "high"})
    tables["by_vol_tercile"] = vt
    st["vol_tercile_bounds"] = (float(b1), float(b2))
    st["vol_terciles_positive"] = int((vt.loc[[i for i in ("low", "mid", "high") if i in vt.index], "net_1x_usd"] > 0).sum())
    # session-edge and roll-week share of P&L (bar level, MTM)
    tm = bars["tday_minute"].to_numpy()
    rth_open, rth_close = 930, bars["rth_close_minute"].to_numpy()
    rc_t = (rth_close.astype(np.int64) - 1080) % 1440
    edge = ((tm >= rth_open) & (tm < rth_open + 5)) | ((tm >= rc_t - 5) & (tm < rc_t + 1)) | (tm < 5) | ((tm >= 1334) & (tm < 1336))
    bnet = bar["gross_pts"].to_numpy() - bar["cost_pts_1x"].to_numpy()
    tot = bnet.sum()
    st["session_edge_share_of_net"] = float(bnet[edge].sum() / tot) if tot > 0 else float("nan")
    st["session_edge_net_usd"] = float(bnet[edge].sum() * inst.point_value)
    rw = d["is_roll_week"].to_numpy(bool)
    st["roll_week_share_of_net"] = float(net1[rw].sum() / net1.sum()) if net1.sum() > 0 else float("nan")
    st["roll_week_net_usd"] = float(net1[rw].sum())
    tables["session_roll"] = pd.DataFrame({"segment": ["session edges (first/last 5 min RTH, reopen, settlement)", "roll weeks", "all"],
                                           "net_1x_usd": [st["session_edge_net_usd"], st["roll_week_net_usd"], float(net1.sum())],
                                           "share": [st["session_edge_share_of_net"], st["roll_week_share_of_net"], 1.0]})
    # preliminary path-wise breach counts
    st["breaches"] = breach_counts(bars, bar, inst.point_value, config)
    st["longest_gap_between_trades_days"] = _longest_gap(d["n_trades"].to_numpy())
    return st, tables


def _longest_hold_days(trades, bars) -> int:
    if len(trades) == 0:
        return 1
    bm = int(bars["bar_minutes"].iloc[0])
    if bm >= 1440:
        return int(max(1, trades["hold_bars"].max()))
    return int(max(1, math.ceil(trades["hold_minutes"].max() / 1440)))


def _longest_gap(n_trades: np.ndarray) -> int:
    idx = np.nonzero(n_trades > 0)[0]
    if idx.size < 2:
        return int(len(n_trades))
    return int(max(np.diff(idx).max() - 1, 0))


def breach_counts(bars: pd.DataFrame, bar: pd.DataFrame, point_value: float, config: RunConfig) -> dict:
    """Path-wise (bar-level) breach counts at the run's size: FTMO 5% daily loss from the 00:00 Prague balance incl.
    floating P&L, FTMO 10% static max loss, and an EOD-trailing drawdown plan (limit `trailing_dd_usd`) with the guard
    at `guard_fraction` of the limit. Preliminary: Department F's prop-fit simulation is the authority (criterion 11)."""
    net = (bar["gross_pts"].to_numpy() - bar["cost_pts_1x"].to_numpy()) * point_value
    eq = np.cumsum(net)
    acct = config.account_usd
    # FTMO day = calendar day in Europe/Prague
    local_ns = pd.DatetimeIndex(bars["ts"]).tz_convert("Europe/Prague").tz_localize(None).asi8
    pday = local_ns // 86_400_000_000_000
    pid = np.cumsum(np.r_[0, (pday[1:] != pday[:-1]).astype(np.int64)])
    start_eq = np.r_[0.0, eq[:-1]]
    first = np.r_[True, pid[1:] != pid[:-1]]
    day_start_eq = np.where(first, start_eq, np.nan)
    day_start_eq = pd.Series(day_start_eq).ffill().to_numpy()
    daily_dd = eq - day_start_eq
    ftmo_daily = daily_dd < -config.ftmo_daily_loss * acct
    ftmo_max = eq < -config.ftmo_max_loss * acct
    # EOD trailing drawdown: high-water mark of end-of-trading-day equity (starts at 0), lock when HWM >= limit
    day_id = bars["day_id"].to_numpy()
    last = np.r_[day_id[1:] != day_id[:-1], True]
    eod = np.where(last, eq, -np.inf)
    hwm_eod = np.maximum.accumulate(np.r_[0.0, eod[:-1]])
    hwm_eod = np.maximum(hwm_eod, 0.0)
    lim = config.trailing_dd_usd
    floor = np.minimum(hwm_eod - lim, 0.0)      # the floor locks at the starting balance once HWM >= limit
    trail_breach = eq < floor
    guard_floor = np.minimum(hwm_eod - config.guard_fraction * lim, 0.0)
    guard_hit = eq < guard_floor
    worst_bar_dd = float((eq - np.maximum.accumulate(np.r_[0.0, eq])[1:]).min()) if len(eq) else 0.0
    return {"ftmo_daily_loss_breach_days": int(np.unique(pid[ftmo_daily]).size),
            "ftmo_max_loss_breached": bool(ftmo_max.any()),
            "ftmo_max_loss_first_bar": int(np.argmax(ftmo_max)) if ftmo_max.any() else None,
            "ftmo_worst_intraday_day_loss_usd": float(daily_dd.min()) if len(daily_dd) else 0.0,
            "trailing_dd_breach_days": int(np.unique(day_id[trail_breach]).size),
            "trailing_guard_hit_days": int(np.unique(day_id[guard_hit]).size),
            "trailing_limit_usd": lim, "guard_fraction": config.guard_fraction,
            "max_drawdown_bar_level_usd": -worst_bar_dd, "account_usd": acct}
