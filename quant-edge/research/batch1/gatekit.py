"""Batch-1 gate arithmetic shared by Q-0001, Q-0003, Q-0005, Q-0006 (Dept D, 2026-11-06). No rule content lives here.

Units: P&L is a fraction of account equity (the row's vol-scaled notional times the return), so 1e-4 = 1 bp of account.
Every statistic is computed by qe.stats; this module only arranges series and tables.
"""
from __future__ import annotations

import hashlib
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from qe import stats  # noqa: E402


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def reads_log_lines(id_: str) -> list:
    p = ROOT / "registry_reads.log"
    return [l for l in p.read_text().splitlines() if f",{id_}," in l] if p.exists() else []


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def t_block(x: np.ndarray, hold_days: int = 1) -> dict:
    tmin, ti, tn = stats.gate_t(np.asarray(x, float), longest_hold_days=hold_days)
    return {"t_min": tmin, "t_iid": ti, "t_nw": tn}


def event_stats(ev: pd.DataFrame, col: str) -> dict:
    """Per-event series (one value per event day; clusters = event day)."""
    x = ev[col].to_numpy(float)
    cl = ev["day"].astype(str).to_numpy()
    tmin, ti, tn = stats.gate_t(x, 1)
    tc = stats.clustered_t(x, cl) if len(x) > 2 else float("nan")
    return {"n": len(x), "mean": float(x.mean()) if len(x) else float("nan"), "t_iid": ti, "t_nw10": tn,
            "t_cluster": tc, "t_min": float(np.nanmin([ti, tn, tc])) if len(x) > 2 else float("nan")}


def daily_metrics(daily: pd.Series, ppy: float) -> dict:
    x = daily.to_numpy(float)
    se = stats.sharpe_se(x, int(round(ppy)))
    cum = np.cumsum(x)
    dd = float((cum - np.maximum.accumulate(np.r_[0.0, cum])[1:]).min())
    return {"sharpe": se["sharpe_annual"], "sharpe_se": se["se_annual"], "ci90": se["ci90_annual"],
            "sharpe_lo": se["sharpe_annual_lo"], "skew": se["skew"], "kurt": se["kurtosis"],
            "max_dd": dd, "worst_day": float(x.min()), "worst_day_date": str(daily.idxmin().date()),
            "ann_mean": float(x.mean() * ppy), "ann_vol": float(x.std(ddof=1) * math.sqrt(ppy))}


def by_year(daily: pd.Series, n_days_per_year: pd.Series, net_total: float) -> tuple:
    """Gate v2 criterion 7: a year counts with >= 200 OOS trading days; need round-half-up(0.7 x years) positive."""
    g = daily.groupby(daily.index.year)
    t = pd.DataFrame({"net": g.sum(), "days": n_days_per_year})
    t["counts"] = t["days"] >= 200
    t["share_of_net"] = t["net"] / net_total if net_total > 0 else np.nan
    counted = t[t["counts"]]
    need = round_half_up(0.7 * len(counted))
    pos = int((counted["net"] > 0).sum())
    m = daily.groupby([daily.index.year, daily.index.month]).sum()
    max_month = float(m.max() / net_total) if net_total > 0 else float("nan")
    max_year = float(t["net"].max() / net_total) if net_total > 0 else float("nan")
    ok = pos >= need and (net_total > 0) and max_year <= 0.5 and max_month <= 0.5
    return t, {"years_counted": len(counted), "positive": pos, "need": need, "max_year_share": max_year,
               "max_month_share": max_month, "passed": bool(ok)}


def best_days_drop(daily: pd.Series, k: int = 20, hold_days: int = 1) -> dict:
    x = daily.sort_values(ascending=False)
    rest = x.iloc[k:].sort_index()
    tb = t_block(rest.to_numpy(), hold_days)
    return {"k": k, "net_total_after": float(rest.sum()), "mean_after": float(rest.mean()), **tb,
            "net_of_best_k": float(x.iloc[:k].sum())}


def bootstrap_events(ev: pd.DataFrame, col: str, seed: int = 0) -> dict:
    return stats.day_cluster_bootstrap_mean(ev[col].to_numpy(float), ev["day"].astype(str).to_numpy(),
                                            n_draws=stats.MIN_DRAWS, seed=seed)


def bootstrap_daily(daily: pd.Series, block: float = 20.0, seed: int = 0) -> dict:
    return stats.stationary_bootstrap_mean(daily.to_numpy(float), n_draws=stats.MIN_DRAWS, mean_block=block, seed=seed)


def power_block(years: float) -> dict:
    return {"years": years, "bar_sharpe": stats.bar_sharpe_units(years),
            "power": tuple(stats.power(s, years) for s in (1.5, 2.0, 2.4))}


def joint_power_note(years: float) -> str:
    tab = {5: (0.32, 0.67, 0.78), 8: (0.63, 0.82, 0.89), 10: (0.72, 0.85, 0.91)}
    if years >= 10:
        return (f"{years:.1f} years >= 10: joint (criteria 3+4+7, costs 1/3 of gross) at least the 10-year figure "
                f"0.72 / 0.85 / 0.91 at true Sharpe 1.5 / 2.0 / 2.4 (PARAMETERS.md; not re-simulated for this length)")
    if years < 5:
        return (f"{years:.1f} years < 5: joint below the 5-year figure 0.32 / 0.67 / 0.78 at true Sharpe 1.5 / 2.0 / 2.4 "
                "(PARAMETERS.md; not simulated for this length)")
    lo, hi = (8, 10) if years >= 8 else (5, 8)
    f = (years - lo) / (hi - lo)
    v = tuple(a + f * (b - a) for a, b in zip(tab[lo], tab[hi]))
    return (f"{years:.1f} years: joint (criteria 3+4+7) about {v[0]:.2f} / {v[1]:.2f} / {v[2]:.2f} at true Sharpe "
            f"1.5 / 2.0 / 2.4 (linear interpolation of the PARAMETERS.md {lo}- and {hi}-year rows)")


def fmt(x, nd=3):
    if x is None:
        return "n/a"
    if isinstance(x, (bool, np.bool_)):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return f"{int(x):,}"
    try:
        if not np.isfinite(x):
            return "nan"
    except TypeError:
        return str(x)
    return f"{x:.{nd}f}"


def bp(x, nd=2):
    return fmt(x * 1e4, nd)


def md_table(df: pd.DataFrame, floatfmt=None) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            f = (floatfmt or {}).get(c)
            cells.append(f(v) if f else (fmt(v) if isinstance(v, (float, np.floating)) else str(v)))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def verdict(t_min: float, boot_lower: float, p5: float, net2_mean: float, net2_t: float, c7_ok: bool,
            near_miss_rule: str) -> dict:
    """Mechanical application of the batch-1 decision rule items (1)-(3); (4)-(5) (Red Team, re-implementation,
    hold-out) are later gates and cannot be passed here."""
    z = stats.Z_BAR
    c1 = bool(t_min >= z and boot_lower > 0)
    c3 = bool(net2_mean > 0 and net2_t >= 1.65)
    gate3 = c1 and c3 and c7_ok
    row_near = bool(t_min >= 2.0 and c3)                     # the row's definition
    brief_near = bool(t_min >= z - 1.0 and p5 > 0)            # the caller's definition (t within 1.0 of the bar, p5 > 0)
    if gate3:
        v = "PASS Gate 3 (criteria 1-3 of the row's rule; Red Team, re-implementation and hold-out still owed)"
    elif row_near or brief_near:
        v = "NEAR-MISS"
    else:
        v = "FAIL (refuted under the row's rule)"
    return {"criterion_4": c1, "criterion_3": c3, "criterion_7": c7_ok, "gate3": gate3,
            "near_miss_row_def": row_near, "near_miss_brief_def": brief_near, "verdict": v, "rule": near_miss_rule}
