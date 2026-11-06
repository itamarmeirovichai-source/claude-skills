#!/usr/bin/env python3
"""Q-0005 (energy CL/CO/HO) and, via research/q0006/q0006.py, Q-0006 (gold GC): commodity dip swing.

Registered 93cb97a. Data only through qe.gateway.load. Stages:
  --stage is      IS run (1984-01-03..1989-12-29), IS vol-tercile bounds, leak harness (truncation + perturbation)
  --stage dryrun  the complete OOS pipeline run on IS data only (crash-proofing before the single OOS read)
  --stage oos     exactly ONE gateway.load(id, "oos") (+ the IS read for warm-up), every Gate-v2 number, result file
Usage: python3 quant-edge/research/q0005/q0005.py --stage {is,dryrun,oos}
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research" / "batch1"))
sys.path.insert(0, str(HERE))
from qe import gateway, stats  # noqa: E402
from qe.engine import harness  # noqa: E402
from qe.qa import pins  # noqa: E402
import gatekit as gk  # noqa: E402
import dipswing as ds  # noqa: E402

CONFIGS = {
    "Q-0005": dict(roots=["CL", "CO", "HO"], cost_bp=2.5, markup=0.03, label="energy dip swing (CL, CO, HO)",
                   subperiods=[("1990-01-02", "2003-12-31"), ("2004-01-01", "2007-12-31")]),
    "Q-0006": dict(roots=["GC"], cost_bp=1.0, markup=0.03, label="gold dip swing (GC)",
                   subperiods=[("1990-01-02", "2001-12-31"), ("2002-01-01", "2007-12-31")]),
}
DATASET = "daily_futures_1984_2016"
IS_START, IS_END = "1984-01-03", "1989-12-29"
OOS_START, OOS_END = "1990-01-02", "2007-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"


def frame(id_, window):
    df = gateway.load(id_, window, dataset=DATASET)
    df = df.set_index("ts")
    df.index = df.index.tz_localize(None)
    return df


def tercile_bounds(R_is: pd.DataFrame, roots):
    out = {}
    for r in roots:
        v = ds.clean(R_is[r]).rolling(20, min_periods=15).std().dropna()
        out[r] = (float(v.quantile(1 / 3)), float(v.quantile(2 / 3)))
    return out


def leak_checks(R_is: pd.DataFrame, roots, p: ds.Params) -> list:
    res = []
    for r in roots:
        fr = ds.harness_frame(R_is[r])
        rule = ds.DipRuleHarness(p, len(roots))
        a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
        b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
        res.append({"root": r, "truncation_passed": a["passed"], "truncation_checked": a["n_checked"],
                    "truncation_violations": len(a["violations"]), "perturbation_passed": b["passed"],
                    "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])})
    return res


def random_entry_null(R: pd.DataFrame, T: pd.DataFrame, roots, p: ds.Params, es, ee, n_paths=10_000, seed=SEED):
    rng = np.random.default_rng(seed)
    pools = {}
    for r in roots:
        s = R[r]
        s = s.loc[s.first_valid_index():]
        c = ds.clean(s)
        v = np.nan_to_num(c.to_numpy(float), nan=0.0)
        ew = c.ewm(com=p.com, min_periods=int(p.com)).std().to_numpy(float)
        cs = np.r_[0.0, np.cumsum(v)]
        d = s.index
        n = len(v)
        e = np.arange(1, n)
        ok = (d[e] >= pd.Timestamp(es)) & (d[e] <= pd.Timestamp(ee)) & np.isfinite(ew[e - 1]) & (ew[e - 1] > 0) & c.notna().to_numpy()[e]
        pools[r] = (e[ok], ew, cs, n)
    holds = np.maximum(T["sessions"].to_numpy(int), 1)
    roots_t = T["root"].to_numpy()
    k = len(T)
    sums = np.zeros(n_paths)
    for j in range(k):
        e_pool, ew, cs, n = pools[roots_t[j]]
        e = e_pool[rng.integers(0, e_pool.size, n_paths)]
        h = holds[rng.integers(0, k, n_paths)]
        x = np.minimum(e + h, n - 1)
        w = p.target_daily / ew[e - 1] / len(roots)
        sums += w * (cs[x + 1] - cs[e + 1])
    g = sums / k
    sg = float(T["gross"].mean())
    return {"n_paths": n_paths, "strategy_gross_per_trade": sg, "null_mean": float(g.mean()), "null_p95": float(np.quantile(g, 0.95)),
            "percentile": float((g < sg).mean()), "beats_95": bool((g < sg).mean() >= 0.95), "seed": seed}


def held_weights(R, T, roots, idx):
    W = pd.DataFrame(0.0, index=idx, columns=roots)
    for t in T.itertuples():
        m = (idx > t.entry_date) & (idx <= t.exit_date)
        W.loc[m, t.root] += t.w
    return W


def buy_hold(R, T, roots, net: pd.Series):
    idx = net.index
    W = held_weights(R, T, roots, idx)
    rr = pd.DataFrame({r: ds.clean(R[r]).reindex(idx).fillna(0.0) for r in roots})
    out = {}
    exp_all = W.mean()
    bh_all = (rr * exp_all).sum(axis=1)
    held = W > 0
    exp_same = W[held].mean().fillna(0.0)
    bh_same = (rr * held * exp_same).sum(axis=1)
    s = net.to_numpy()
    for name, b in (("always_long_same_avg_exposure", bh_all), ("long_on_held_days_mean_weight", bh_same)):
        b = b.to_numpy()
        beta = float(np.cov(s, b)[0, 1] / b.var()) if b.var() > 0 else 0.0
        a = s - beta * b
        tb = gk.t_block(a, 10)
        out[name] = {"bh_total": float(b.sum()), "bh_sharpe": stats.sharpe(b, 252) if b.std() > 0 else float("nan"), "beta": beta,
                     "alpha_mean_per_day": float(a.mean()), "alpha_t_min": tb["t_min"], "strategy_minus_bh_total": float(s.sum() - b.sum())}
    return out


def evaluate(id_, R: pd.DataFrame, es, ee, bounds, years, heavy=True):
    cfg = CONFIGS[id_]
    roots = cfg["roots"]
    p = ds.Params()
    base = ds.run(R, roots, p, cfg["cost_bp"], cfg["markup"], 1.0, es, ee)
    two = ds.run(R, roots, p, cfg["cost_bp"], cfg["markup"], 2.0, es, ee)
    T = base["trades"]
    net1, net2, gross = base["net"], two["net"], base["gross"]
    days_per_year = net1.groupby(net1.index.year).size()
    ppy = len(net1) / years
    out = {"n_trades": len(T), "n_days": len(net1), "ppy": ppy}
    out["trades_per_year"] = len(T) / years
    out["distinct_entry_days"] = int(T["day"].nunique()) if len(T) else 0
    out["truncated_trades"] = int(T["truncated"].sum()) if len(T) else 0
    out["daily"] = {k: {"mean": float(v.mean()), **gk.t_block(v.to_numpy(), 10)} for k, v in (("gross", gross), ("net1x", net1), ("net2x", net2))}
    T2 = two["trades"]
    out["trade"] = {"gross": gk.event_stats(T.assign(x=T["gross"]), "x"), "net1x": gk.event_stats(T, "net"),
                    "net2x": gk.event_stats(T2, "net")}
    out["bp_per_trade_notional_gross"] = float(T["ret_notional"].mean() * 1e4)
    out["bp_per_trade_notional_net1x"] = float(((T["gross"] - T["cost"]) / T["w"]).mean() * 1e4)
    out["metrics"] = gk.daily_metrics(net1, ppy)
    out["metrics_gross"] = gk.daily_metrics(gross, ppy)
    yt, ys = gk.by_year(net1, days_per_year, float(net1.sum()))
    out["by_year"], out["years_summary"] = yt, ys
    out["best20"] = gk.best_days_drop(net1, 20, 10)
    # terciles (trailing 20-day realized vol at the signal day; IS bounds per root)
    terc = []
    for t in T.itertuples():
        s = ds.clean(R[t.root])
        v = s.rolling(20, min_periods=15).std().loc[:t.signal_date].iloc[-1]
        lo, hi = bounds[t.root]
        terc.append(0 if v <= lo else (1 if v <= hi else 2))
    T = T.assign(tercile=terc)
    tt = T.groupby("tercile")["net"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    out["terciles"] = tt
    out["terciles_positive"] = int((tt["sum"] > 0).sum())
    # neighbourhood and execution variants
    neigh = [("(as registered)", p)]
    for f in (0.75, 1.25):
        neigh.append((f"k={p.k*f:g}", replace(p, k=p.k * f)))
    for wv in (45, 75):
        neigh.append((f"sd_window={wv} (min {gk.round_half_up(50*wv/60)})", replace(p, sd_window=wv, sd_min=gk.round_half_up(50 * wv / 60))))
    for cv in (45.0, 75.0):
        neigh.append((f"com={cv:g}", replace(p, com=cv)))
    for mh in (2, 4):
        neigh.append((f"max_hold={mh}", replace(p, max_hold=mh)))
    for ml in (4, 6):
        neigh.append((f"mean_len={ml}", replace(p, mean_len=ml)))
    rows = []
    for name, q in neigh:
        rr = ds.run(R, roots, q, cfg["cost_bp"], cfg["markup"], 1.0, es, ee)
        n = rr["net"]
        rows.append({"variant": name, "trades": len(rr["trades"]), "net1x_total": float(n.sum()),
                     "net1x_mean_bp_per_day": float(n.mean() * 1e4), "t_min": gk.t_block(n.to_numpy(), 10)["t_min"],
                     "net_positive": bool(n.sum() > 0)})
    out["neighbourhood"] = pd.DataFrame(rows)
    ex = []
    for name, q in (("registered (entry close t+1, exit close u)", p), ("entry delayed one bar (close t+2)", replace(p, entry_lag=2)),
                    ("exit lagged one bar (close u+1)", replace(p, exit_lag=1))):
        rr = ds.run(R, roots, q, cfg["cost_bp"], cfg["markup"], 1.0, es, ee)
        n = rr["net"]
        ex.append({"variant": name, "trades": len(rr["trades"]), "net1x_total": float(n.sum()), "t_min": gk.t_block(n.to_numpy(), 10)["t_min"],
                   "share_of_base": float(n.sum() / net1.sum()) if net1.sum() > 0 else float("nan")})
    out["execution"] = pd.DataFrame(ex)
    # sub-periods
    sp = []
    for a, b in cfg["subperiods"]:
        x = net1[(net1.index >= a) & (net1.index <= b)]
        sp.append({"period": f"{a}..{b}", "days": len(x), "net1x_total": float(x.sum()), "t_min": gk.t_block(x.to_numpy(), 10)["t_min"],
                   "sharpe": stats.sharpe(x.to_numpy(), int(round(ppy)))})
    out["subperiods"] = pd.DataFrame(sp)
    out["by_root"] = T.groupby("root")["net"].agg(["count", "sum", "mean"])
    out["buy_hold"] = buy_hold(R, T, roots, net1)
    # gold drift diagnostic (Red Team): trade gross minus the unconditional mean daily r over its held days
    unc = {r: float(ds.clean(R[r]).loc[es:ee].mean()) for r in roots}
    exc = T["gross"] - T["w"] * T["sessions"] * T["root"].map(unc)
    out["excess_over_unconditional"] = {"mean_per_trade": float(exc.mean()), **gk.t_block(exc.to_numpy(), 1),
                                        "unconditional_mean_daily_r": unc}
    out["ftmo"] = {"days_below_-5pct": int((net1 < -0.05).sum()), "max_dd": out["metrics"]["max_dd"],
                   "dd_beyond_10pct": bool(out["metrics"]["max_dd"] < -0.10)}
    out["trades"] = T
    out["hold_dist"] = T["sessions"].value_counts().sort_index().to_dict()
    if heavy:
        t0 = time.time()
        out["boot_daily"] = gk.bootstrap_daily(net1, 20.0, SEED)
        out["boot_trade"] = gk.bootstrap_events(T, "net", SEED)
        out["random_entry"] = random_entry_null(R, T, roots, p, es, ee)
        out["boot_seconds"] = time.time() - t0
    return out


def write_result(id_, o, is_info, leak, pinres, cmd, crash_note="", dry_dir=None):
    cfg = CONFIGS[id_]
    years = o["years"]
    pw = gk.power_block(years)
    tmin_daily = o["daily"]["net1x"]["t_min"]
    tmin_trade = o["trade"]["net1x"]["t_min"]
    t_dec = min(tmin_daily, tmin_trade)
    lb = min(o["boot_daily"]["lower_alpha"], o["boot_trade"]["lower_alpha"])
    p5_daily, p5_trade = o["boot_daily"]["p5"], o["boot_trade"]["p5"]
    neigh_ok = bool(o["neighbourhood"]["net_positive"].all())
    delay_share = float(o["execution"].iloc[1]["share_of_base"])
    c7 = bool(o["years_summary"]["passed"] and o["terciles_positive"] >= 2 and neigh_ok and (delay_share >= 0.5))
    v = gk.verdict(t_dec, lb, min(p5_daily, p5_trade), o["daily"]["net2x"]["mean"], o["daily"]["net2x"]["t_min"], c7,
                   "row: near-miss = t >= 2.0 with criterion 3 passed")
    m = o["metrics"]
    L = []
    A = L.append
    A(f"# {id_} — {cfg['label']}: Gate-v2 OOS result")
    A("")
    A(f"Registry row {id_} (registered commit 93cb97a, count 1, sign long fixed). Script `research/q0005/q0005.py`"
      + (" via `research/q0006/q0006.py`" if id_ == "Q-0006" else "") + f". Result-writing commit {gk.git_commit()} (working tree; nothing committed by Dept D). "
      "A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap seed {SEED} (430,000 draws), random-entry seed {SEED} (10,000 paths), harness seed {SEED}.")
    A(f"- Data: `{DATASET}` sha256 manifest {pinres['manifest_sha256']} = row pin {pinres['row_sha256']} = recomputed {pinres['computed_sha256']} (ok={pinres['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END} (warm-up, tercile bounds, harness); decision window OOS {OOS_START}..{OOS_END} (derivative rule D-009: 2008-2016 rows never read: the gateway serves OOS only to {OOS_END}). Hold-out not read.")
    A(f"- Costs 1x: {cfg['cost_bp']} bp per side on notional + financing markup {cfg['markup']*100:.0f}%/yr per calendar day held; 2x: {2*cfg['cost_bp']} bp and {2*cfg['markup']*100:.0f}%/yr.")
    A("- Units: P&L as a fraction of account equity at the row's sizing (0.10/sqrt(252) per unit EWMA daily s.d."
      + (", divided by 3 roots" if len(cfg["roots"]) > 1 else "") + "); 1 bp = 1e-4 of account.")
    if crash_note:
        A(f"- Disclosure: {crash_note}")
    A("")
    A("## registry_reads.log lines for this id")
    A("")
    A("```")
    for l in gk.reads_log_lines(id_):
        A(l)
    A("```")
    A("")
    A("## Leak checks (before the OOS read, IS window only)")
    A("")
    A("| root | truncation passed | days checked | violations | perturbation passed | days checked | violations |")
    A("|---|---|---|---|---|---|---|")
    for r in leak:
        A(f"| {r['root']} | {gk.fmt(r['truncation_passed'])} | {r['truncation_checked']} | {r['truncation_violations']} | {gk.fmt(r['perturbation_passed'])} | {r['perturbation_checked']} | {r['perturbation_violations']} |")
    A("")
    A("Harness = `qe.engine.harness.future_truncation_test` / `perturbation_test` on a single-root daily frame (close = the "
      "raw excess-return index); the rule object calls the same `dipswing.trades_one_root` as the backtest. The registered exit "
      "fills at the close whose P_u triggers it (signal-at-close); the harness cannot see that (it keeps bar i), so the "
      "one-bar-later exit is run below as the execution-lag variant (criterion 8).")
    A("")
    A(f"IS (information only, chosen nothing): {is_info}")
    A("")
    A("## Headline (OOS, net 1x)")
    A("")
    A("| series | mean bp/day | t_min | t_iid | t_NW(10) |")
    A("|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x"):
        d = o["daily"][k]
        A(f"| daily MTM {k} | {gk.bp(d['mean'], 3)} | {gk.fmt(d['t_min'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw'], 2)} |")
    A("")
    A("| trade-level series | n | mean bp of account per trade | t_iid | t_NW(10) | t day-clustered | t_min |")
    A("|---|---|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x"):
        d = o["trade"][k]
        A(f"| {k} | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw10'], 2)} | {gk.fmt(d['t_cluster'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    A("")
    A(f"- Bootstrap (430,000 draws, alpha 0.05/430): daily stationary blocks (mean 20 days): lower bound {gk.bp(o['boot_daily']['lower_alpha'], 3)} bp/day, p5 {gk.bp(p5_daily, 3)} bp/day; "
      f"trade-level day-cluster: lower bound {gk.bp(o['boot_trade']['lower_alpha'], 2)} bp/trade, p5 {gk.bp(p5_trade, 2)} bp/trade. ({o['boot_seconds']:.0f} s)")
    A(f"- Deciding t = min(daily t_min, trade t_min) = {gk.fmt(t_dec, 2)} vs bar {stats.Z_BAR:.4f}; deciding lower bound = {gk.bp(lb, 3)} (the smaller of the two, in its own unit).")
    A(f"- Trades {o['n_trades']} on {o['distinct_entry_days']} distinct entry days; {o['trades_per_year']:.1f} trades/yr; holds (sessions: count) {o['hold_dist']}; truncated at the window end {o['truncated_trades']}.")
    A(f"- bp per trade on notional: gross {o['bp_per_trade_notional_gross']:.1f}, net 1x {o['bp_per_trade_notional_net1x']:.1f}.")
    A(f"- Sharpe net 1x {m['sharpe']:.3f} (Mertens/Opdyke s.e. {m['sharpe_se']:.3f}; 90% CI {m['ci90'][0]:.2f}..{m['ci90'][1]:.2f}; Lo-adjusted {m['sharpe_lo']:.3f}; skew {m['skew']:.2f}, kurtosis {m['kurt']:.1f}); gross Sharpe {o['metrics_gross']['sharpe']:.3f}. Annual mean {m['ann_mean']*100:.2f}%, vol {m['ann_vol']*100:.2f}% (periods/yr {o['ppy']:.1f}).")
    A(f"- Max drawdown {m['max_dd']*100:.2f}% of account (sum of daily net); worst day {m['worst_day']*100:.2f}% on {m['worst_day_date']}; days below -5%: {o['ftmo']['days_below_-5pct']} (close-to-close only: intraday path not in the data).")
    A(f"- OOS {years:.2f} years: bar in Sharpe units 3.6807/sqrt(T) = {pw['bar_sharpe']:.3f}; criterion-4 power at true Sharpe 1.5/2.0/2.4 = {pw['power'][0]:.2f}/{pw['power'][1]:.2f}/{pw['power'][2]:.2f}. {gk.joint_power_note(years)}.")
    A("")
    A("## Criterion 3 (2x cost)")
    A("")
    A(f"Net 2x mean {gk.bp(o['daily']['net2x']['mean'], 3)} bp/day, t_min {gk.fmt(o['daily']['net2x']['t_min'], 2)} (need > 0 and t >= 1.65): **{'passed' if v['criterion_3'] else 'failed'}**.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    re_ = o["random_entry"]
    A(f"- Random-entry null ({re_['n_paths']:,} paths, same trade count, root mix and holding-time distribution, entries uniform over eligible OOS days, the row's weight on the drawn day): strategy gross per trade {gk.bp(re_['strategy_gross_per_trade'], 2)} bp vs null mean {gk.bp(re_['null_mean'], 2)} bp, null p95 {gk.bp(re_['null_p95'], 2)} bp; percentile {re_['percentile']:.3f} (need >= 0.95): {'passed' if re_['beats_95'] else 'failed'}.")
    for k, b in o["buy_hold"].items():
        A(f"- Buy-and-hold `{k}`: B&H total {b['bh_total']*100:.2f}%, B&H Sharpe {gk.fmt(b['bh_sharpe'], 2)}, beta {b['beta']:.3f}, alpha {gk.bp(b['alpha_mean_per_day'], 3)} bp/day, alpha t_min {gk.fmt(b['alpha_t_min'], 2)} (need >= 3.6807); strategy minus B&H total {b['strategy_minus_bh_total']*100:.2f}%.")
    e = o["excess_over_unconditional"]
    A(f"- Excess over the unconditional long mean (Red Team diagnostic; gate stays on raw net): {gk.bp(e['mean_per_trade'], 2)} bp/trade, t_min {gk.fmt(e['t_min'], 2)}; unconditional mean daily r {', '.join(f'{k} {v*1e4:.2f} bp' for k, v in e['unconditional_mean_daily_r'].items())}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    yt = o["by_year"].reset_index().rename(columns={"index": "year", "ts": "year"})
    yt.columns = ["year", "net1x", "days", "counts", "share_of_net"]
    A(gk.md_table(yt, {"net1x": lambda x: f"{x*100:.2f}%", "share_of_net": lambda x: gk.fmt(x, 2), "days": lambda x: str(int(x))}))
    ys = o["years_summary"]
    A("")
    A(f"Years counted {ys['years_counted']}, positive {ys['positive']}, need {ys['need']}; max year share {gk.fmt(ys['max_year_share'], 2)}, max month share {gk.fmt(ys['max_month_share'], 2)}: **{'passed' if ys['passed'] else 'failed'}**.")
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["tercile (0 = low vol)", "trades", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"tercile (0 = low vol)": lambda x: str(int(x)), "net1x sum": lambda x: f"{x*100:.3f}%", "net1x mean": lambda x: gk.bp(x, 2) + " bp", "trades": lambda x: str(int(x))}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; bounds = IS 1/3 and 2/3 quantiles of the trailing 20-day s.d. per root: {', '.join(f'{k} {a*100:.2f}%/{b*100:.2f}%' for k, (a, b) in o['bounds'].items())}).")
    A("")
    b20 = o["best20"]
    A(f"Best-20-days fragility: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A("Neighbourhood (run once on OOS; never changes the headline):")
    A("")
    A(gk.md_table(o["neighbourhood"], {"net1x_total": lambda x: f"{x*100:.2f}%", "net1x_mean_bp_per_day": lambda x: gk.fmt(x, 3), "t_min": lambda x: gk.fmt(x, 2), "trades": lambda x: str(int(x)), "net_positive": gk.fmt}))
    A("")
    A(f"All neighbours net positive: {gk.fmt(neigh_ok)}.")
    A("")
    A("Execution variants (criterion 7 one-bar delay; criterion 8 worse-of):")
    A("")
    A(gk.md_table(o["execution"], {"net1x_total": lambda x: f"{x*100:.2f}%", "t_min": lambda x: gk.fmt(x, 2), "share_of_base": lambda x: gk.fmt(x, 2), "trades": lambda x: str(int(x))}))
    A("")
    A(f"Criterion 7 overall: **{'passed' if c7 else 'failed'}**.")
    A("")
    A("Sub-periods (institutional change dates; information only):")
    A("")
    A(gk.md_table(o["subperiods"], {"net1x_total": lambda x: f"{x*100:.2f}%", "t_min": lambda x: gk.fmt(x, 2), "sharpe": lambda x: gk.fmt(x, 2), "days": lambda x: str(int(x))}))
    A("")
    br = o["by_root"].reset_index()
    br.columns = ["root", "trades", "net1x sum", "net1x mean"]
    A(gk.md_table(br, {"net1x sum": lambda x: f"{x*100:.3f}%", "net1x mean": lambda x: gk.bp(x, 2) + " bp", "trades": lambda x: str(int(x))}))
    A("")
    A("## Criteria 2 and 12 (process)")
    A("")
    A(f"- Criterion 2: OOS {years:.1f} years ({'>=' if years >= 8 else '<'} 8); position changes {2*o['n_trades']} (need >= 100 for a daily strategy): {'met' if 2*o['n_trades'] >= 100 else 'NOT met'}. OOS excludes 2020 and 2022 (the decision window ends 2007 by the derivative rule; disclosed in the row).")
    A("- Criterion 5: single pre-registered configuration, CSCV n/a; DSR not computed (criterion 4 decides).")
    A("- Prop-fit (criterion 11) belongs to Department F; FTMO 5%/10% counts above are close-to-close only.")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(t_dec, 2)} vs 3.6807 and bootstrap lower bound {'> 0' if lb > 0 else '<= 0'}: **{'passed' if v['criterion_4'] else 'failed'}**.")
    A(f"- (2) criterion 3: **{'passed' if v['criterion_3'] else 'failed'}**. (3) criterion 7: **{'passed' if c7 else 'failed'}**. (4)-(5) Red Team, re-implementation, hold-out: not reached.")
    A(f"- Near-miss by the row's definition (t >= 2.0 with criterion 3 passed): {gk.fmt(v['near_miss_row_def'])}; by the batch brief's (t within 1.0 of the bar with p5 > 0): {gk.fmt(v['near_miss_brief_def'])}.")
    A(f"- **Verdict: {v['verdict']}.** Read against the power above: a failure is not evidence that no effect exists.")
    out = (Path(dry_dir) / f"{id_}.dry.md") if dry_dir else ROOT / "research" / "results" / f"{id_}.md"
    out.write_text("\n".join(L) + "\n")
    if dry_dir:
        print("dry result written", out)
        return out
    summ = {"id": id_, "oos_net1x_mean_bp_per_day": o["daily"]["net1x"]["mean"] * 1e4, "net1x_bp_per_trade": o["trade"]["net1x"]["mean"] * 1e4,
            "t_min_daily": tmin_daily, "t_min_trade": tmin_trade, "boot_lower_daily_bp": o["boot_daily"]["lower_alpha"] * 1e4,
            "boot_lower_trade_bp": o["boot_trade"]["lower_alpha"] * 1e4, "t2x": o["daily"]["net2x"]["t_min"], "verdict": v["verdict"]}
    (HERE.parent / ("q0006" if id_ == "Q-0006" else "q0005") / f"{id_}_summary.json").write_text(json.dumps(summ, indent=1, default=str))
    o["trades"].to_csv(HERE.parent / ("q0006" if id_ == "Q-0006" else "q0005") / f"{id_}_oos_trades.csv", index=False)
    print(json.dumps(summ, indent=1, default=str))
    return out


def main(id_, stage, cmd):
    cfg = CONFIGS[id_]
    roots = cfg["roots"]
    pinres = pins.verify(id_, DATASET)
    if stage in ("is", "dryrun"):
        R_is = frame(id_, "is")[roots]
        bounds = tercile_bounds(R_is, roots)
        if stage == "is":
            leak = leak_checks(R_is, roots, ds.Params())
            yrs = (pd.Timestamp(IS_END) - pd.Timestamp(IS_START)).days / 365.25
            r = ds.run(R_is, roots, ds.Params(), cfg["cost_bp"], cfg["markup"])
            n = r["net"]
            info = {"trades": len(r["trades"]), "net1x_total": float(n.sum()), "t_min": gk.t_block(n.to_numpy(), 10)["t_min"],
                    "sharpe": stats.sharpe(n.to_numpy(), int(round(len(n) / yrs)))}
            d = {"leak": leak, "is_info": info, "bounds": bounds}
            (HERE.parent / ("q0006" if id_ == "Q-0006" else "q0005") / f"{id_}_is.json").write_text(json.dumps(d, indent=1, default=str))
            print(json.dumps(d, indent=1, default=str))
        else:
            mid = "1987-01-02"            # dry run: IS 1984-1986 as history, 1987-1989 as the pretend window (IS data only)
            yrs = (pd.Timestamp(IS_END) - pd.Timestamp(mid)).days / 365.25
            o = evaluate(id_, R_is, mid, IS_END, bounds, yrs, heavy=True)
            o["years"], o["bounds"] = yrs, bounds
            isj = json.loads((HERE.parent / ("q0006" if id_ == "Q-0006" else "q0005") / f"{id_}_is.json").read_text())
            write_result(id_, o, "dry run", isj["leak"], pinres, cmd, dry_dir=SCRATCH)
        return
    # ---- OOS: the single read
    isj = json.loads((HERE.parent / ("q0006" if id_ == "Q-0006" else "q0005") / f"{id_}_is.json").read_text())
    R_is = frame(id_, "is")[roots]
    R_oos = frame(id_, "oos")[roots]                      # <- the one OOS read for this id
    R = pd.concat([R_is, R_oos]).sort_index()
    years = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    bounds = {k: tuple(v) for k, v in isj["bounds"].items()}
    o = evaluate(id_, R, OOS_START, OOS_END, bounds, years, heavy=True)
    o["years"], o["bounds"] = years, bounds
    is_info = (f"{isj['is_info']['trades']} trades, net 1x total {isj['is_info']['net1x_total']*100:.2f}% of account, "
               f"t_min {isj['is_info']['t_min']:.2f}, Sharpe {isj['is_info']['sharpe']:.2f}")
    write_result(id_, o, is_info, isj["leak"], pinres, cmd)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    ap.add_argument("--id", default="Q-0005", choices=list(CONFIGS))
    a = ap.parse_args()
    main(a.id, a.stage, f"python3 quant-edge/research/q0005/q0005.py --stage {a.stage}" if a.id == "Q-0005" else f"python3 quant-edge/research/q0006/q0006.py --stage {a.stage}")
