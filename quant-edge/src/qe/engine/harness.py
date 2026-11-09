"""qe.engine.harness — leak tests, execution-lag variants, neighbourhood, nulls, benchmark, gate statistics.

* future_truncation_test: for a sample of trading days d, delete every bar after the entry minute of day d and recompute
  the rule; the decisions of day d up to and including the entry minute must be identical (targets, or bracket orders).
  A rule that reads the day's close, the day's bar count or any post-entry bar fails.
* perturbation_test: same sampling; every bar after the entry minute is multiplied by random noise (and the far
  future shuffled); decisions up to the entry minute must not move. Catches leaks that survive truncation (global
  statistics computed on the whole frame, normalisations by the sample maximum, ...).
* execution_lag_variants: next-open (lag 1, the base case), signal-at-close/fill-at-close (optimistic), lag 2, and the
  rule's own as-written / ex-ante eligibility variants when it exposes them; the WORSE net mean per day decides.
* neighbourhood: each continuous parameter x0.75 and x1.25, each discrete parameter one step each way, one run each.
* entry_delay_runs: entries delayed one and five bars; share of the base net kept.
* random_entry_null: >= 10,000 random-entry strategies with the same trade count, side mix and holding-time
  distribution, entries uniform over the bars of the same session type (RTH when every entry is in RTH, else the whole
  session) before the flat-by minute; percentile of the strategy's gross per trade.
* shuffled_signal_permutation: day-level block permutation (20-day blocks) of the position path against the returns;
  p-value of the strategy's gross.
* buy_and_hold_matched: long the instrument over the strategy's in-market minutes at its mean absolute exposure, and
  always-long at the same average exposure; alpha t of the strategy against each.
* gate_statistics: criterion 3, 4 and 7 arithmetic on the daily net series (430,000 draws by default).
"""
from __future__ import annotations

import math
from dataclasses import replace
from typing import Dict, Optional

import numpy as np
import pandas as pd
from numba import njit

from .. import stats
from . import bars as _bars
from . import fills as _fills
from . import pnl as _pnl


# --------------------------------------------------------------------------------------------------- leak tests
def _decisions(rule, bars) -> tuple:
    if rule.mode == "brackets":
        o = rule.orders(bars)
        order = np.argsort(np.asarray(o.entry_idx), kind="stable")
        return ("orders", np.asarray(o.entry_idx)[order], np.asarray(o.side)[order], np.asarray(o.stop_pts, float)[order],
                np.asarray(o.target_pts, float)[order], None if o.qty is None else np.asarray(o.qty, float)[order])
    return ("target", np.nan_to_num(np.asarray(rule.signal(bars), float), nan=0.0))


def _entry_minute_index(dec, bars, day_id: int) -> Optional[int]:
    """Bar index of day d's first decision (first non-zero target or first order); None if the day has none."""
    d = bars["day_id"].to_numpy()
    in_day = np.nonzero(d == day_id)[0]
    if in_day.size == 0:
        return None
    if dec[0] == "target":
        tgt = dec[1][in_day]
        nz = np.nonzero(tgt != 0)[0]
        return int(in_day[nz[0]]) if nz.size else None
    ei = dec[1]
    m = (ei >= in_day[0]) & (ei <= in_day[-1])
    return int(ei[m].min()) if m.any() else None


def _slice_decisions(dec, lo: int, hi: int):
    """Decisions with bar index in [lo, hi]."""
    if dec[0] == "target":
        return dec[1][lo:hi + 1]
    ei = dec[1]
    m = (ei >= lo) & (ei <= hi)
    parts = [dec[1][m], dec[2][m], dec[3][m], dec[4][m]]
    if dec[5] is not None:
        parts.append(dec[5][m])
    return parts


def _same(a, b) -> bool:
    if isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    a = np.asarray(a)
    b = np.asarray(b)
    return a.shape == b.shape and np.allclose(a, b, equal_nan=True, atol=1e-12, rtol=0)


def _sample_days(bars, n_days, seed, dec):
    rng = np.random.default_rng(seed)
    days = np.unique(bars["day_id"].to_numpy())
    # prefer days with a decision; fall back to any day
    with_dec = [d for d in days if _entry_minute_index(dec, bars, int(d)) is not None]
    pool = np.asarray(with_dec if len(with_dec) >= min(n_days, 5) else days)
    if pool.size <= n_days:
        return [int(x) for x in pool]
    return [int(x) for x in rng.choice(pool, size=n_days, replace=False)]


def future_truncation_test(rule, bars: pd.DataFrame, n_days: int = 30, seed: int = 0, days=None) -> dict:
    """Returns {"passed": bool, "n_checked": int, "violations": [(trading_day, entry_ts, detail), ...]}."""
    full = _decisions(rule, bars)
    day_ids = days if days is not None else _sample_days(bars, n_days, seed, full)
    d = bars["day_id"].to_numpy()
    violations = []
    for day in day_ids:
        in_day = np.nonzero(d == day)[0]
        e = _entry_minute_index(full, bars, day)
        cut = e if e is not None else int(in_day[-1])
        trunc = bars.iloc[: cut + 1].copy()
        trunc.attrs.update(bars.attrs)
        part = _decisions(rule, trunc)
        a = _slice_decisions(full, int(in_day[0]), cut)
        b = _slice_decisions(part, int(in_day[0]), cut)
        if not _same(a, b):
            violations.append((str(pd.Timestamp(bars["trading_day"].iloc[cut]).date()), str(bars["ts"].iloc[cut]),
                               "decisions up to the entry minute changed when later bars were deleted"))
    return {"passed": not violations, "n_checked": len(day_ids), "violations": violations, "test": "future_truncation"}


def perturbation_test(rule, bars: pd.DataFrame, n_days: int = 30, seed: int = 0, eps: float = 0.01, days=None) -> dict:
    """Bars after the entry minute get multiplicative noise (sd `eps`) and a shuffled far future; decisions must not move."""
    full = _decisions(rule, bars)
    day_ids = days if days is not None else _sample_days(bars, n_days, seed, full)
    d = bars["day_id"].to_numpy()
    rng = np.random.default_rng(seed + 1)
    violations = []
    for day in day_ids:
        in_day = np.nonzero(d == day)[0]
        e = _entry_minute_index(full, bars, day)
        cut = e if e is not None else int(in_day[-1])
        pert = bars.copy()
        pert.attrs.update(bars.attrs)
        n_after = len(bars) - cut - 1
        if n_after == 0:
            continue
        noise = np.exp(rng.standard_normal(n_after) * eps)
        for c in ("open", "high", "low", "close"):
            v = pert[c].to_numpy(float).copy()
            v[cut + 1:] *= noise
            pert[c] = v
        hi = np.maximum.reduce([pert["open"].to_numpy(), pert["high"].to_numpy(), pert["close"].to_numpy()])
        lo = np.minimum.reduce([pert["open"].to_numpy(), pert["low"].to_numpy(), pert["close"].to_numpy()])
        pert["high"] = hi
        pert["low"] = lo
        part = _decisions(rule, pert)
        a = _slice_decisions(full, int(in_day[0]), cut)
        b = _slice_decisions(part, int(in_day[0]), cut)
        if not _same(a, b):
            violations.append((str(pd.Timestamp(bars["trading_day"].iloc[cut]).date()), str(bars["ts"].iloc[cut]),
                               "decisions up to the entry minute changed when later bars were perturbed"))
    return {"passed": not violations, "n_checked": len(day_ids), "violations": violations, "test": "perturbation"}


# ------------------------------------------------------------------------------------------ execution variants
def _summary(res: _pnl.Result) -> dict:
    s = res.stats
    return {"net_1x_mean_usd_per_day": s["net_1x_mean_usd_per_day"], "net_1x_total_usd": s["net_1x_total_usd"],
            "net_2x_mean_usd_per_day": s["net_2x_mean_usd_per_day"], "t_min_1x": s["net_1x_t_min"],
            "sharpe_1x": s["net_1x_sharpe"]["sharpe"], "n_trades": s["n_trades"]}


def execution_lag_variants(bars, rule, config: _pnl.RunConfig, scale=None) -> dict:
    runs: Dict[str, dict] = {}
    base = _pnl.simulate(bars, rule, config, scale=scale)
    runs["next_open_lag1 (base)"] = _summary(base)
    if rule.mode == "target":
        runs["signal_at_close_fill_at_close (optimistic)"] = _summary(_pnl.simulate(bars, rule, replace(config, fill_at="close"), scale=scale))
    else:
        runs["signal_at_close_fill_at_close (optimistic)"] = {"note": "n/a: bracket entries are market-at-open by construction"}
    runs["lag2 (next open + 1 bar)"] = _summary(_pnl.simulate(bars, rule, replace(config, lag_bars=config.lag_bars + 1), scale=scale))
    for name, variant in rule.variants().items():
        runs[f"rule variant: {name}"] = _summary(_pnl.simulate(bars, variant, config, scale=scale))
    scored = {k: v["net_1x_mean_usd_per_day"] for k, v in runs.items() if "net_1x_mean_usd_per_day" in v and "optimistic" not in k}
    worst = min(scored, key=scored.get)
    return {"runs": runs, "worst": worst, "worst_net_1x_mean_usd_per_day": scored[worst], "rule": "the worse decides"}


def neighbourhood(bars, rule, config: _pnl.RunConfig, scale=None) -> pd.DataFrame:
    rows = []
    base = _pnl.simulate(bars, rule, config, scale=scale)
    rows.append({"parameter": "(as registered)", "value": "", **_summary(base)})
    for p in rule.continuous:
        v0 = float(rule.params[p])
        for f in (0.75, 1.25):
            r = rule.with_params(**{p: v0 * f})
            rows.append({"parameter": p, "value": v0 * f, **_summary(_pnl.simulate(bars, r, config, scale=scale))})
    for p in rule.discrete:
        v0 = rule.params[p]
        step = rule.params.get(p + "_step", 1)
        for dv in (-step, step):
            r = rule.with_params(**{p: v0 + dv})
            rows.append({"parameter": p, "value": v0 + dv, **_summary(_pnl.simulate(bars, r, config, scale=scale))})
    t = pd.DataFrame(rows)
    t["net_positive"] = t["net_1x_total_usd"] > 0
    return t


def entry_delay_runs(bars, rule, config: _pnl.RunConfig, delays=(1, 5), scale=None) -> pd.DataFrame:
    base = _pnl.simulate(bars, rule, config, scale=scale)
    b = base.stats["net_1x_total_usd"]
    rows = [{"delay_bars": 0, **_summary(base), "share_of_base_net": 1.0}]
    for k in delays:
        r = _pnl.simulate(bars, rule, replace(config, entry_delay_bars=config.entry_delay_bars + k), scale=scale)
        rows.append({"delay_bars": k, **_summary(r), "share_of_base_net": (r.stats["net_1x_total_usd"] / b) if b > 0 else float("nan")})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------------ nulls
@njit(cache=True)
def _random_entry_kernel(o, c, day_last, mkt_cost, elig, holds, sides, n_paths, seed):
    np.random.seed(seed)
    n = o.shape[0]
    k = holds.shape[0]
    ne = elig.shape[0]
    gross = np.empty(n_paths)
    net = np.empty(n_paths)
    for p in range(n_paths):
        sg = 0.0
        sn = 0.0
        for t in range(k):
            i = elig[np.random.randint(0, ne)]
            hb = holds[np.random.randint(0, k)]
            s = sides[np.random.randint(0, k)]
            j = i + hb
            if j > day_last[i]:
                j = day_last[i]
            if j >= n:
                j = n - 1
            px_exit = o[j] if j > i else c[i]
            g = s * (px_exit - o[i])
            sg += g
            sn += g - mkt_cost[i] - mkt_cost[j]
        gross[p] = sg / k
        net[p] = sn / k
    return gross, net


def random_entry_null(bars, res: _pnl.Result, n_paths: int = 10_000, seed: int = 0, eligible: Optional[np.ndarray] = None) -> dict:
    """Percentile of the strategy's gross (and net, market both sides) per trade among random-entry strategies."""
    tr = res.trades
    if len(tr) == 0:
        return {"note": "no trades"}
    holds = np.maximum(tr["hold_bars"].to_numpy(np.int64), 0)
    sides = tr["side"].to_numpy(np.int64)
    if eligible is None:
        # same session type as the strategy's entries: RTH when every entry is in RTH, else the whole session
        tm = bars["tday_minute"].to_numpy()
        fi = tr["fill_idx"].to_numpy()
        all_rth = bool(bars["is_rth"].to_numpy(bool)[fi].all())
        eligible = (bars["is_rth"] if all_rth else bars["in_session"]).to_numpy(bool).copy()
        if res.config.firm is not None:
            fb = _fills.flat_by_per_bar(bars, res.config.firm, res.config.flat_by_margin_minutes)
            eligible &= tm < fb
    elig = np.nonzero(eligible)[0].astype(np.int64)
    day_id = bars["day_id"].to_numpy()
    n = len(bars)
    last = np.r_[np.nonzero(day_id[1:] != day_id[:-1])[0], n - 1]
    day_last = last[np.searchsorted(last, np.arange(n))] if res.config.intraday_only else np.full(n, n - 1)
    mkt, _ = _fills.per_bar_costs(bars, res.config.instrument(), res.config.slip)
    g, nn = _random_entry_kernel(bars["open"].to_numpy(float), bars["close"].to_numpy(float), day_last.astype(np.int64), mkt,
                                 elig, holds, sides, int(n_paths), int(seed))
    sg = float((tr["gross_pts"] * tr["qty"]).mean() / max(tr["qty"].mean(), 1e-12))
    sn = float(((tr["gross_pts"] - tr["cost_pts_1x"]) * tr["qty"]).mean() / max(tr["qty"].mean(), 1e-12))
    return {"n_paths": int(n_paths), "n_trades": int(len(tr)), "strategy_gross_per_trade_pts": sg, "strategy_net_per_trade_pts": sn,
            "null_gross_mean": float(g.mean()), "null_gross_p95": float(np.quantile(g, 0.95)), "null_gross_sd": float(g.std()),
            "percentile_gross": float((g < sg).mean()), "percentile_net": float((nn < sn).mean()),
            "beats_95pct": bool((g < sg).mean() >= 0.95), "n_eligible_bars": int(elig.size), "seed": seed}


@njit(cache=True)
def _perm_kernel(T, R, lo, hi, perm):
    P, D = perm.shape
    out = np.empty(P)
    for p in range(P):
        s = 0.0
        for d in range(D):
            a = perm[p, d]
            for m in range(lo[a], hi[a]):
                s += T[a, m] * R[d, m]
        out[p] = s
    return out


def shuffled_signal_permutation(bars, res: _pnl.Result, n_perm: int = 1000, block_days: int = 20, seed: int = 0) -> dict:
    """Block-permute the position path across trading days against the realised bar returns (gross, close-to-close MTM).
    Returns the one-sided p-value P(perm gross >= observed gross) with the +1 correction."""
    pos = res.bar["position"].to_numpy(float)
    c = bars["close"].to_numpy(float)
    ret = np.r_[0.0, np.diff(c)]
    day_id = bars["day_id"].to_numpy(np.int64)
    D = int(day_id.max()) + 1
    if bars.attrs.get("daily"):
        M = 1
        slot = np.zeros(len(bars), np.int64)
    else:
        M = 1440
        slot = bars["tday_minute"].to_numpy(np.int64)
    T = np.zeros((D, M), np.float32)
    R = np.zeros((D, M), np.float32)
    T[day_id, slot] = pos
    R[day_id, slot] = ret
    nz = T != 0
    any_nz = nz.any(axis=1)
    lo = np.where(any_nz, nz.argmax(axis=1), 0).astype(np.int64)
    hi = np.where(any_nz, M - nz[:, ::-1].argmax(axis=1), 0).astype(np.int64)
    rng = np.random.default_rng(seed)
    n_blocks = int(math.ceil(D / block_days))
    blocks = [np.arange(b * block_days, min((b + 1) * block_days, D)) for b in range(n_blocks)]
    perm = np.empty((n_perm, D), np.int64)
    for p in range(n_perm):
        order = rng.permutation(n_blocks)
        seq = np.concatenate([blocks[i] for i in order])
        perm[p] = seq[:D]
    observed = float((T.astype(np.float64) * R.astype(np.float64)).sum())
    null = _perm_kernel(T, R, lo, hi, perm)
    p = (1 + int((null >= observed).sum())) / (n_perm + 1)
    return {"n_perm": int(n_perm), "block_days": block_days, "observed_gross_pts": observed, "null_mean": float(null.mean()),
            "null_sd": float(null.std()), "p_value": float(p), "seed": seed}


def buy_and_hold_matched(bars, res: _pnl.Result) -> dict:
    """Long the instrument (a) over the strategy's in-market bars at its mean |position|, (b) always in session at the
    same average exposure. Daily P&L in money and the alpha t (NW) of the strategy's net 1x on each benchmark."""
    pos = res.bar["position"].to_numpy(float)
    c = bars["close"].to_numpy(float)
    ret = np.r_[0.0, np.diff(c)]
    day_id = bars["day_id"].to_numpy(np.int64)
    nd = len(res.daily)
    in_mkt = pos != 0
    ins = bars["in_session"].to_numpy(bool)
    exp_same = float(np.abs(pos[in_mkt]).mean()) if in_mkt.any() else 0.0
    exp_all = float(np.abs(pos[ins]).mean()) if ins.any() else 0.0
    bh_same = np.where(in_mkt, exp_same, 0.0) * ret
    bh_all = np.where(ins, exp_all, 0.0) * ret
    pv = res.point_value
    d_same = np.bincount(day_id, weights=bh_same, minlength=nd) * pv
    d_all = np.bincount(day_id, weights=bh_all, minlength=nd) * pv
    s = res.daily["net_1x_usd"].to_numpy()
    out = {"exposure_same_minutes": exp_same, "exposure_always": exp_all}
    for name, b in (("same_minutes", d_same), ("always_long", d_all)):
        var = b.var()
        beta = float(np.cov(s, b)[0, 1] / var) if var > 0 else 0.0
        alpha = s - beta * b
        t_min, t_iid, t_nw = stats.gate_t(alpha) if nd > 2 else (float("nan"),) * 3
        out[name] = {"bh_total_usd": float(b.sum()), "bh_sharpe": stats.sharpe(b) if nd > 2 and b.std() > 0 else float("nan"),
                     "beta": beta, "alpha_mean_usd_per_day": float(alpha.mean()), "alpha_t_min": t_min,
                     "strategy_minus_bh_total_usd": float(s.sum() - b.sum())}
    return out


# ------------------------------------------------------------------------------------------------ gate statistics
def gate_statistics(res: _pnl.Result, n_draws: int = stats.MIN_DRAWS, two_count: bool = False, seed: int = 0, years_oos: Optional[float] = None) -> dict:
    """Criteria 3, 4 and 7 arithmetic on daily net P&L (money, 1x and 2x). Bootstrap: iid whole-day resampling for
    strategies flat by the session end, stationary block (mean 20 days) otherwise."""
    d = res.daily
    s = res.stats
    z = stats.Z_BAR_TWO_COUNT if two_count else stats.Z_BAR
    net1 = d["net_1x_usd"].to_numpy()
    net2 = d["net_2x_usd"].to_numpy()
    block = 1.0 if res.config.intraday_only else 20.0
    boot = stats.stationary_bootstrap_mean(net1, n_draws=n_draws, mean_block=block, seed=seed) if len(net1) > 5 else {"lower_alpha": float("nan"), "p5": float("nan"), "n_draws": 0}
    years = years_oos if years_oos else s["years"]
    c3 = bool(net2.mean() > 0 and s["net_2x_t_min"] >= 1.65)
    c4 = bool(net1.mean() > 0 and s["net_1x_t_min"] >= z and boot["lower_alpha"] > 0)
    c7 = {"years_positive": f"{s['years_positive']} of {s['years_counted']} (need {s['years_needed']})",
          "years_ok": bool(s["years_positive"] >= s["years_needed"]) if s["years_counted"] else None,
          "max_year_share": s["max_year_share"], "max_month_share": s["max_month_share"],
          "concentration_ok": bool((not (s["max_year_share"] > 0.5)) and (not (s["max_month_share"] > 0.5))),
          "vol_terciles_positive": f"{s['vol_terciles_positive']} of 3 (need 2)", "terciles_ok": bool(s["vol_terciles_positive"] >= 2),
          "tercile_bounds_source": s["vol_tercile_bounds_source"]}
    return {"z_bar": z, "two_count": two_count, "bar_sharpe_units_for_oos_length": stats.bar_sharpe_units(years, z),
            "power_at_1.5_2.0_2.4": tuple(stats.power(x, years, z) for x in (1.5, 2.0, 2.4)), "years": years,
            "criterion_3_2x_cost": {"net_2x_mean_usd_per_day": float(net2.mean()), "t_min_2x": s["net_2x_t_min"], "passed": c3},
            "criterion_4_significance": {"net_1x_mean_usd_per_day": float(net1.mean()), "t_min": s["net_1x_t_min"], "t_iid": s["net_1x_t_iid"],
                                         "t_nw": s["net_1x_t_nw"], "bootstrap_lower_alpha": boot["lower_alpha"], "bootstrap_p5": boot["p5"],
                                         "n_draws": boot["n_draws"], "mean_block_days": block, "passed": c4},
            "criterion_7_stability": c7, "bootstrap": boot}
