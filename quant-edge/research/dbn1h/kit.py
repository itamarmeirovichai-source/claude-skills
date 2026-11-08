"""Shared plumbing for the Databento 1h rows Q-0012..Q-0015 (written after their registration commit 4588d6c).

Bars: dict inst -> {(et_date, et_hour): (open, close, instrument_id)}, built from qe.gateway.load reads only.
Gate statistics follow research/results/Q-0007.md (bar z 3.6807, 430,000 bootstrap draws, alpha 0.05/430).
"""
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from qe import gateway, stats  # noqa: E402
import exchange_calendars as xc  # noqa: E402

NY = "America/New_York"
BAR = stats.Z_BAR
VOL_TARGET = 0.10 / math.sqrt(252)


def load_bars(rid, datasets, windows=("is",)):
    """One gateway read per dataset per window; returns {root: {(date, hour): (o, c, iid)}} and the raw frames."""
    out, frames = {}, {}
    for ds in datasets:
        parts = [gateway.load(rid, w, dataset=ds) for w in windows]
        df = pd.concat(parts, ignore_index=True).sort_values("ts").drop_duplicates("ts")
        frames[ds] = df
        et = df["ts"].dt.tz_convert(NY)
        keys = zip(et.dt.date, et.dt.hour)
        out[ds.rsplit("_", 1)[-1]] = dict(zip(keys, zip(df["open"].to_numpy(float), df["close"].to_numpy(float),
                                                         df["instrument_id"].to_numpy())))
    return out, frames


_CAL = xc.get_calendar("XNYS")


def sessions(start, end):
    s = _CAL.sessions_in_range(pd.Timestamp(start), pd.Timestamp(end))
    early = set(_CAL.early_closes.date) if hasattr(_CAL.early_closes, "date") else set(pd.DatetimeIndex(_CAL.early_closes).date)
    return [d.date() for d in s], early


def ewma_prev(values: pd.Series, com, kind, min_periods=40):
    """EWMA RMS ('rms') or s.d. ('std') through the previous observation (shifted by one)."""
    if kind == "rms":
        r = np.sqrt((values ** 2).ewm(com=com, min_periods=min_periods).mean())
    else:
        r = values.ewm(com=com, min_periods=min_periods).std()
    return r.shift(1)


def cost_frac(price, slip_pts, point_value, comm=2.50, mult=1.0):
    return mult * (slip_pts * point_value + comm) / (point_value * price)


# ------------------------------------------------------------------ gate statistics
def gate(x, dates, clusters=None, nw_lag=10, mean_block=20.0, per_year=None, seed=0):
    x = np.asarray(x, float)
    t_iid = stats.iid_t(x)
    t_nw = stats.newey_west_t(x, nw_lag)
    t_cl = stats.clustered_t(x, np.asarray(clusters)) if clusters is not None else float("nan")
    ts = [t for t in (t_iid, t_nw, t_cl) if not math.isnan(t)]
    sb = stats.stationary_bootstrap_mean(x, mean_block=mean_block, seed=seed)
    res = {"n": int(x.size), "mean": float(x.mean()), "t_iid": t_iid, "t_nw": t_nw, "t_cl": t_cl, "t_min": min(ts),
           "boot_lower": sb["lower_alpha"], "boot_p5": sb["p5"], "boot_draws": sb["n_draws"]}
    if clusters is not None:
        cb = stats.day_cluster_bootstrap_mean(x, np.asarray(clusters), seed=seed)
        res["cboot_lower"], res["cboot_p5"] = cb["lower_alpha"], cb["p5"]
        res["boot_lower_min"] = min(sb["lower_alpha"], cb["lower_alpha"])
        res["boot_p5_min"] = min(sb["p5"], cb["p5"])
    else:
        res["boot_lower_min"], res["boot_p5_min"] = sb["lower_alpha"], sb["p5"]
    d = pd.to_datetime(pd.Series(dates))
    yrs = (d.max() - d.min()).days / 365.25 if len(d) > 1 else float("nan")
    py = per_year or (x.size / yrs if yrs and yrs > 0 else 252)
    sd = x.std(ddof=1)
    res["sharpe_ann"] = float(x.mean() / sd * math.sqrt(py)) if sd > 0 else float("nan")
    res["per_year"] = py
    return res


def verdict(g1, g2_mean, crit7_ok):
    c1 = g1["t_min"] >= BAR and g1["boot_lower_min"] > 0
    c3 = g2_mean > 0
    if c1 and c3 and crit7_ok:
        return "PASS Gate 3"
    if g1["t_min"] >= BAR - 1.0 and g1["boot_p5_min"] > 0:
        return "NEAR-MISS"
    return "FAIL"


def years_table(x, dates):
    s = pd.Series(np.asarray(x, float), index=pd.to_datetime(pd.Series(dates)).values)
    y = s.groupby(s.index.year).agg(["sum", "count"])
    return y


def tercile_bounds(v):
    v = pd.Series(v).dropna()
    return float(v.quantile(1 / 3)), float(v.quantile(2 / 3))


def fmt_bp(v):
    return f"{1e4 * v:.2f}"


def power_line(years):
    p = [stats.power(s, years) for s in (1.5, 2.0, 2.4)]
    return (f"OOS {years:.2f} years: bar {stats.bar_sharpe_units(years):.3f} annual Sharpe; criterion-4 power at true Sharpe "
            f"1.5/2.0/2.4 = {p[0]:.2f}/{p[1]:.2f}/{p[2]:.2f}")


def gate_md(name, g, unit="bp per obs"):
    tcl = "" if math.isnan(g["t_cl"]) else f"{g['t_cl']:.2f}"
    return (f"| {name} | {g['n']} | {fmt_bp(g['mean'])} | {g['t_iid']:.2f} | {g['t_nw']:.2f} | {tcl} | {g['t_min']:.2f} | "
            f"{fmt_bp(g['boot_lower_min'])} | {fmt_bp(g['boot_p5_min'])} | {g['sharpe_ann']:.2f} |")


GATE_HDR = ("| series | n | mean bp of account | t_iid | t_NW | t_clustered | t_min | bootstrap lower (0.05/430) bp | bootstrap p5 bp | ann. Sharpe |\n"
            "|---|---|---|---|---|---|---|---|---|---|")


# ------------------------------------------------------------------ harness (truncation / perturbation / planted)
def harness(compute, bars, ev_key, entry_of, sample, decision_cols, seed=0):
    """compute(bars) -> DataFrame with ev_key and decision_cols; entry_of(row) -> (date, hour) entry instant.
    For each sampled event, bars at/after the entry instant (all instruments) are deleted (truncation) or noised
    by 1% (perturbation); the event's decision must not change."""
    base = compute(bars).set_index(ev_key)
    rng = np.random.default_rng(seed)
    keys = list(base.index)
    pick = [keys[i] for i in sorted(rng.choice(len(keys), size=min(sample, len(keys)), replace=False))]
    out = {"truncation": 0, "perturbation": 0, "n": len(pick)}
    for k in pick:
        ed, eh = entry_of(base.loc[k], k)
        cut = (ed, eh)
        tb = {i: {kk: v for kk, v in b.items() if kk < cut} for i, b in bars.items()}
        pb = {i: {kk: ((v[0] * (1 + 0.01 * rng.standard_normal()), v[1] * (1 + 0.01 * rng.standard_normal()), v[2])
                        if kk >= cut else v) for kk, v in b.items()} for i, b in bars.items()}
        for name, bb in (("truncation", tb), ("perturbation", pb)):
            r = compute(bb).set_index(ev_key)
            a = base.loc[k, decision_cols]
            b = r.loc[k, decision_cols] if k in r.index else None
            same = b is not None and all((pd.isna(a[c]) and pd.isna(b[c])) or (isinstance(a[c], float) and abs(a[c] - b[c]) < 1e-12) or a[c] == b[c] for c in decision_cols)
            if not same:
                out[name] += 1
    out["truncation_passed"] = out["truncation"] == 0
    out["perturbation_passed"] = out["perturbation"] == 0
    return out
