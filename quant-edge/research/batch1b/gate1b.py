"""Batch-1b gate arrangement shared by Q-0007/Q-0008/Q-0009 (Dept D, 2026-11-06): the batch-1 tables (research/batch1/
gatekit.py, used read-only) for a per-trade series `ev` with columns day, gross, net1, net2 (+ optional venue column).
Every statistic is computed by qe.stats via gatekit. No rule content."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "batch1"))
import gatekit as gk  # noqa: E402


def daily_series(ev: pd.DataFrame, col: str, start, end) -> pd.Series:
    idx = pd.bdate_range(start, end)
    s = pd.Series(0.0, index=idx)
    v = ev.groupby(pd.to_datetime(ev["day"]))[col].sum()
    k = v.index.intersection(idx)
    s.loc[k] = v.loc[k].to_numpy()
    return s


def ev_stats(ev: pd.DataFrame, col: str) -> dict:
    if len(ev) < 3:
        return {"n": len(ev), "mean": float(ev[col].mean()) if len(ev) else float("nan"), "t_iid": float("nan"),
                "t_nw10": float("nan"), "t_cluster": float("nan"), "t_min": float("nan")}
    return gk.event_stats(ev.assign(xx=ev[col]), "xx")


def core(ev: pd.DataFrame, start, end, years: float, cols=("gross", "net1", "net2"), venue=None, heavy=True, seed=0) -> dict:
    o = {"years": years, "n": len(ev), "n_days": int(pd.to_datetime(ev["day"]).nunique())}
    names = {"gross": "gross", "net1": "net1x", "net2": "net2x"}
    allc = list(cols) + ([venue] if venue else [])
    o["ev"] = {names.get(c, c): ev_stats(ev, c) for c in allc}
    d = {c: daily_series(ev, c, start, end) for c in ("gross", "net1", "net2")}
    o["d1"] = d["net1"]
    ppy = len(d["net1"]) / years
    o["ppy"] = ppy
    o["daily"] = {names[k]: {"mean": float(v.mean()), **gk.t_block(v.to_numpy(), 10)} for k, v in d.items()}
    o["metrics"], o["metrics_gross"] = gk.daily_metrics(d["net1"], ppy), gk.daily_metrics(d["gross"], ppy)
    yt, ys = gk.by_year(d["net1"], d["net1"].groupby(d["net1"].index.year).size(), float(d["net1"].sum()))
    o["by_year"], o["years_summary"] = yt, ys
    o["by_year_trades"] = ev.groupby(pd.to_datetime(ev["day"]).dt.year)["net1"].agg(["count", "sum"])
    o["best20"] = gk.best_days_drop(d["net1"], 20, 10)
    o["ftmo"] = {"days_below_-5pct": int((d["net1"] < -0.05).sum())}
    if heavy:
        t0 = time.time()
        o["boot_ev"] = gk.bootstrap_events(ev, "net1", seed)
        o["boot_daily"] = gk.bootstrap_daily(d["net1"], 1.0, seed)
        o["boot_seconds"] = time.time() - t0
    return o


def deciding(o: dict) -> dict:
    t_ev, t_d = o["ev"]["net1x"]["t_min"], o["daily"]["net1x"]["t_min"]
    lb = min(o["boot_ev"]["lower_alpha"], o["boot_daily"]["lower_alpha"])
    p5 = min(o["boot_ev"]["p5"], o["boot_daily"]["p5"])
    t2 = min(o["ev"]["net2x"]["t_min"], o["daily"]["net2x"]["t_min"])
    return {"t_ev": t_ev, "t_daily": t_d, "t_dec": float(min(t_ev, t_d)), "lb": lb, "p5": p5, "t2": t2,
            "net2_mean": o["ev"]["net2x"]["mean"]}


def lines_series(o: dict, unit_ev: str = "trade", venue_label=None) -> list:
    L = [f"| per-{unit_ev} series | n | mean bp of account | t_iid | t_NW(10) | t day-clustered | t_min |", "|---|---|---|---|---|---|---|"]
    for k, d in o["ev"].items():
        lab = venue_label if (venue_label and k not in ("gross", "net1x", "net2x")) else k
        L.append(f"| {lab} | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw10'], 2)} | {gk.fmt(d['t_cluster'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    L += ["", "| daily series (zeros on other weekdays) | mean bp/day | t_min | t_iid | t_NW(10) |", "|---|---|---|---|---|"]
    for k, d in o["daily"].items():
        L.append(f"| {k} | {gk.bp(d['mean'], 3)} | {gk.fmt(d['t_min'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw'], 2)} |")
    return L


def lines_headline_bullets(o: dict, unit_ev: str = "trade") -> list:
    dc = deciding(o)
    m, pw = o["metrics"], gk.power_block(o["years"])
    return [
        f"- Bootstrap (430,000 draws, alpha 0.05/430): day-cluster on {unit_ev}s: lower bound {gk.bp(o['boot_ev']['lower_alpha'], 2)} bp/{unit_ev}, p5 {gk.bp(o['boot_ev']['p5'], 2)}; daily iid-day: lower bound {gk.bp(o['boot_daily']['lower_alpha'], 3)} bp/day, p5 {gk.bp(o['boot_daily']['p5'], 3)} ({o['boot_seconds']:.0f} s).",
        f"- Deciding t = min({unit_ev}, daily) = {gk.fmt(dc['t_dec'], 2)} vs bar 3.6807.",
        f"- Sharpe (daily net 1x) {m['sharpe']:.3f}, Mertens/Opdyke s.e. {m['sharpe_se']:.3f}, 90% CI {m['ci90'][0]:.2f}..{m['ci90'][1]:.2f}, Lo-adjusted {m['sharpe_lo']:.3f}; gross {o['metrics_gross']['sharpe']:.3f}. Annual mean {m['ann_mean']*100:.3f}%, vol {m['ann_vol']*100:.3f}%.",
        f"- Max drawdown {m['max_dd']*100:.2f}% of account; worst day {m['worst_day']*100:.2f}% ({m['worst_day_date']}); days below -5%: {o['ftmo']['days_below_-5pct']}.",
        f"- OOS {o['years']:.2f} years: bar in Sharpe units {pw['bar_sharpe']:.3f}; criterion-4 power at true Sharpe 1.5/2.0/2.4 = {pw['power'][0]:.2f}/{pw['power'][1]:.2f}/{pw['power'][2]:.2f}. {gk.joint_power_note(o['years'])}.",
    ]


def lines_years(o: dict, label_trades: str = "trades") -> list:
    yt = o["by_year"].reset_index()
    yt.columns = ["year", "net1x", "weekdays", "counts", "share_of_net"]
    yt[label_trades] = yt["year"].map(o["by_year_trades"]["count"]).fillna(0).astype(int)
    ys = o["years_summary"]
    return [gk.md_table(yt, {"net1x": lambda x: f"{x*100:.3f}%", "share_of_net": lambda x: gk.fmt(x, 2), "weekdays": lambda x: str(int(x))}), "",
            f"Years counted {ys['years_counted']}, positive {ys['positive']}, need {ys['need']}; max year share {gk.fmt(ys['max_year_share'], 2)}, max month share {gk.fmt(ys['max_month_share'], 2)}: **{'passed' if ys['passed'] else 'failed'}**."]


def pct(x):
    return f"{x*100:.3f}%"
