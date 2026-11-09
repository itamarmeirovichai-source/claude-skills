#!/usr/bin/env python3
"""Q-0003 FOMC-day AUDUSD long (registered 93cb97a). Data only through qe.gateway.load.
Stages:  --stage is      IS events (information), IS tercile bounds, leak harness (as-written and ex-ante), cross-source QA
         --stage dryrun  the complete OOS pipeline on IS data only (2012-2013 as the pretend window)
         --stage oos     exactly ONE OOS read per dataset (AUDUSD 1m, cal_fomc) + IS history; every Gate-v2 number
Usage: python3 quant-edge/research/q0003/q0003.py --stage {is,dryrun,oos}
"""
from __future__ import annotations

import argparse
import json
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
from qe.qa import pins, xsource  # noqa: E402
import gatekit as gk  # noqa: E402
import fxkit as fx  # noqa: E402
import fomcday as fd  # noqa: E402

ID = "Q-0003"
FXDS, CALDS = "histdata_fx_1m_AUDUSD", "cal_fomc"
IS_START, IS_END = "2010-01-04", "2013-12-31"
OOS_START, OOS_END = "2014-01-01", "2024-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"
SUBPERIODS = [("2014-01-01", "2015-12-15", "ZLB to lift-off"), ("2015-12-16", "2022-02-28", "lift-off to hiking cycle"),
              ("2022-03-01", "2024-12-31", "hiking cycle and after")]


def load_bars(window):
    b = gateway.load(ID, window, dataset=FXDS)
    return b[["ts", "open", "high", "low", "close"]].reset_index(drop=True)


def load_cal(window):
    return gateway.load(ID, window, dataset=CALDS)


def daily_series(ev_ok: pd.DataFrame, col: str, start, end) -> pd.Series:
    idx = pd.bdate_range(start, end)
    s = pd.Series(0.0, index=idx)
    v = ev_ok.groupby(pd.to_datetime(ev_ok["day"]))[col].sum()
    s.loc[v.index.intersection(idx)] += v.reindex(v.index.intersection(idx)).to_numpy()
    return s


def leak_checks(bars_is, days_is):
    fr = fx.tag_for_harness(bars_is)
    out = {}
    for mode in ("exact", "ex_ante"):
        rule = fd.FomcRule(days_is, fd.Params(exit_mode=mode))
        a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
        b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
        out[mode] = {"truncation_passed": a["passed"], "truncation_checked": a["n_checked"], "truncation_violations": len(a["violations"]),
                     "perturbation_passed": b["passed"], "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])}
        print(mode, out[mode], flush=True)
    return out


def xsource_qa(bars_is):
    c = fx.ny_closes(bars_is)
    r = c["r"].dropna()
    cols = xsource.available_columns("daily_assets_1970_2026")
    fx_like = [x for x in cols if any(k in x.upper() for k in ("AUD", "USD", "FX", "CUR"))]
    fut = xsource.second_source_returns("daily_futures_1984_2016", "AD", IS_START, IS_END)
    cmp = xsource.compare(r, fut)
    return {"daily_assets_columns": cols, "daily_assets_fx_like": fx_like, "fut_AD": cmp, "n_fx_returns": int(len(r))}


def evaluate(bars, days, start, end, bounds, years, heavy=True):
    p = fd.Params()
    ev = fd.events(bars, days, p)
    ok = ev[ev["status"] == "ok"].copy()
    ok["net1"] = ok["gross"] - ok["cost1"]
    ok["net2"] = ok["gross"] - 2 * ok["cost1"]
    ok["cme_cost"] = ok["w"] * np.array([fx.cme_cost_frac("AUDUSD", d, a) + fx.cme_cost_frac("AUDUSD", d, b)
                                         for d, a, b in zip(ok["day"], ok["entry_px"], ok["exit_px"])])
    ok["net_cme"] = ok["gross"] - ok["cme_cost"]
    ok["entry_delay_min"] = (pd.DatetimeIndex(ok["entry_ts"]) - pd.DatetimeIndex(ok["entry_target"])).total_seconds() / 60
    o = {"events_total": len(ev), "status_counts": ev["status"].value_counts().to_dict(), "n": len(ok), "years": years,
         "entry_delay_max_min": float(ok["entry_delay_min"].max()), "entry_delay_gt0": int((ok["entry_delay_min"] > 0).sum())}
    o["ev"] = {k: gk.event_stats(ok.assign(x=ok[c]), "x") for k, c in (("gross", "gross"), ("net1x", "net1"), ("net2x", "net2"), ("net_cme", "net_cme"))}
    d1 = daily_series(ok, "net1", start, end)
    d2 = daily_series(ok, "net2", start, end)
    dg = daily_series(ok, "gross", start, end)
    ppy = len(d1) / years
    o["ppy"] = ppy
    o["daily"] = {k: {"mean": float(v.mean()), **gk.t_block(v.to_numpy(), 10)} for k, v in (("gross", dg), ("net1x", d1), ("net2x", d2))}
    o["metrics"] = gk.daily_metrics(d1, ppy)
    o["metrics_gross"] = gk.daily_metrics(dg, ppy)
    o["bp_notional"] = {"gross": float(ok["ret"].mean() * 1e4), "net1x": float((ok["net1"] / ok["w"]).mean() * 1e4),
                        "ret_sd": float(ok["ret"].std() * 1e4)}
    o["trades_per_year"] = len(ok) / years
    yt, ys = gk.by_year(d1, d1.groupby(d1.index.year).size(), float(d1.sum()))
    o["by_year"], o["years_summary"] = yt, ys
    o["by_year_events"] = ok.groupby(pd.to_datetime(ok["day"]).dt.year)["net1"].agg(["count", "sum", "mean"])
    o["best20"] = gk.best_days_drop(d1, 20, 10)
    lo, hi = bounds
    ok["tercile"] = np.where(ok["sd20"] <= lo, 0, np.where(ok["sd20"] <= hi, 1, 2))
    tt = ok.groupby("tercile")["net1"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    o["terciles"], o["terciles_positive"] = tt, int((tt["sum"] > 0).sum())
    hold0 = float(np.median([(fx.local_instant(D, p.exit_clock, fx.NY) - fx.local_instant(D, p.entry_clock, fx.PRG)).total_seconds() / 60 for D in days]))
    sh = round(0.25 * hold0)
    o["hold0_min"], o["shift_min"] = hold0, sh
    variants = [("(as registered)", p), (f"entry +{sh} min (hold x0.75)", replace(p, entry_shift_min=sh)),
                (f"entry -{sh} min (hold x1.25)", replace(p, entry_shift_min=-sh)), (f"exit -{sh} min (hold x0.75)", replace(p, exit_shift_min=-sh)),
                (f"exit +{sh} min (hold x1.25)", replace(p, exit_shift_min=sh)), ("com=45", replace(p, com=45.0)), ("com=75", replace(p, com=75.0))]
    rows = []
    for name, q in variants:
        e = fd.events(bars, days, q)
        e = e[e["status"] == "ok"]
        n1 = e["gross"] - e["cost1"]
        rows.append({"variant": name, "events": len(e), "net1x_total": float(n1.sum()), "net1x_bp_per_event": float(n1.mean() * 1e4),
                     "t_min": gk.event_stats(e.assign(x=n1), "x")["t_min"], "net_positive": bool(n1.sum() > 0)})
    o["neighbourhood"] = pd.DataFrame(rows)
    ex = []
    base_tot = float(ok["net1"].sum())
    for name, q in (("registered (exact 15:58 bar, skip if missing)", p), ("entry delayed one minute", replace(p, entry_shift_min=1)),
                    ("ex-ante exit (first bar at or after 15:58)", replace(p, exit_mode="ex_ante"))):
        e = fd.events(bars, days, q)
        e = e[e["status"] == "ok"]
        n1 = e["gross"] - e["cost1"]
        ex.append({"variant": name, "events": len(e), "net1x_total": float(n1.sum()), "t_min": gk.event_stats(e.assign(x=n1), "x")["t_min"],
                   "share_of_base": float(n1.sum() / base_tot) if base_tot > 0 else float("nan")})
    o["execution"] = pd.DataFrame(ex)
    sp = []
    for a, b, lab in SUBPERIODS:
        x = ok[(pd.to_datetime(ok["day"]) >= a) & (pd.to_datetime(ok["day"]) <= b)]
        sp.append({"period": f"{a}..{b} ({lab})", "events": len(x), "net1x_total": float(x["net1"].sum()),
                   "net1x_bp_per_event": float(x["net1"].mean() * 1e4) if len(x) else float("nan"),
                   "t_min": gk.event_stats(x, "net1")["t_min"] if len(x) > 2 else float("nan")})
    o["subperiods"] = pd.DataFrame(sp)
    # placebo / random-entry: every other New York weekday in the window, same clocks, long, the row's weight
    sd = set(pd.Timestamp(d) for d in days)
    pdays = [d for d in pd.bdate_range(start, end) if d not in sd]
    pe = fd.events(bars, pdays, p)
    pe = pe[pe["status"] == "ok"].copy()
    o["placebo"] = {"n": len(pe), "gross_mean": float(pe["gross"].mean()), "t": gk.event_stats(pe.assign(x=pe["gross"]), "x")["t_min"],
                    "ret_bp_mean": float(pe["ret"].mean() * 1e4)}
    rng = np.random.default_rng(SEED)
    g = pe["gross"].to_numpy()
    k = len(ok)
    null = np.empty(10_000)
    for i in range(0, 10_000, 1000):
        null[i:i + 1000] = g[rng.integers(0, g.size, size=(1000, k))].mean(axis=1)
    sg = float(ok["gross"].mean())
    o["random_entry"] = {"n_paths": 10_000, "strategy_gross": sg, "null_mean": float(null.mean()), "null_p95": float(np.quantile(null, 0.95)),
                         "percentile": float((null < sg).mean()), "beats_95": bool((null < sg).mean() >= 0.95), "seed": SEED}
    # buy-and-hold: always long the same window every weekday at the strategy's average daily exposure
    allw = pd.concat([pe[["day", "ret"]], ok[["day", "ret"]]])
    mean_exp = float(ok["w"].sum() / len(d1))
    bh = pd.Series(0.0, index=d1.index)
    v = allw.groupby(pd.to_datetime(allw["day"]))["ret"].sum() * mean_exp
    bh.loc[v.index.intersection(bh.index)] = v.reindex(v.index.intersection(bh.index)).to_numpy()
    s_, b_ = d1.to_numpy(), bh.to_numpy()
    beta = float(np.cov(s_, b_)[0, 1] / b_.var()) if b_.var() > 0 else 0.0
    a_ = s_ - beta * b_
    o["buy_hold"] = {"mean_exposure": mean_exp, "bh_total": float(b_.sum()), "beta": beta, "alpha_mean": float(a_.mean()),
                     "alpha_t_min": gk.t_block(a_, 10)["t_min"], "note": "matched-minutes B&H on the event days is the strategy itself (long-only, same minutes, same weight): alpha undefined"}
    o["ftmo"] = {"days_below_-5pct": int((d1 < -0.05).sum())}
    o["ok"] = ok
    if heavy:
        t0 = time.time()
        o["boot_ev"] = gk.bootstrap_events(ok, "net1", SEED)
        o["boot_daily"] = gk.bootstrap_daily(d1, 1.0, SEED)
        o["boot_seconds"] = time.time() - t0
    return o


def write_result(o, isj, pinres, cmd, out_path, crash_note=""):
    years = o["years"]
    pw = gk.power_block(years)
    t_ev, t_d = o["ev"]["net1x"]["t_min"], o["daily"]["net1x"]["t_min"]
    t_dec = min(t_ev, t_d)
    lb_ev, lb_d = o["boot_ev"]["lower_alpha"], o["boot_daily"]["lower_alpha"]
    neigh_ok = bool(o["neighbourhood"]["net_positive"].all())
    delay_share = float(o["execution"].iloc[1]["share_of_base"])
    c7 = bool(o["years_summary"]["passed"] and o["terciles_positive"] >= 2 and neigh_ok and delay_share >= 0.5)
    v = gk.verdict(t_dec, min(lb_ev, lb_d), min(o["boot_ev"]["p5"], o["boot_daily"]["p5"]), o["ev"]["net2x"]["mean"],
                   min(o["ev"]["net2x"]["t_min"], o["daily"]["net2x"]["t_min"]), c7, "row: near-miss = t >= 2.0 with criterion 3 passed")
    m = o["metrics"]
    L = []
    A = L.append
    A("# Q-0003 — FOMC statement-day long AUDUSD: Gate-v2 OOS result")
    A("")
    A(f"Registry row Q-0003 (registered commit 93cb97a, count 1, sign long fixed). Script `research/q0003/q0003.py` (rule `research/q0003/fomcday.py`, plumbing `research/batch1/fxkit.py`, `gatekit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap {SEED} (430,000 draws each), random-entry {SEED} (10,000 paths), harness {SEED}.")
    for r in pinres:
        A(f"- Data `{r['dataset']}` sha256: manifest {r['manifest_sha256']} = row pin {r['row_sha256']} = recomputed {r['computed_sha256']} (ok={r['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END} (vol warm-up, tercile bounds, harness, QA); OOS {OOS_START}..{OOS_END}; hold-out not read.")
    A("- Costs: 1x 1.5 bp per side on notional (bid-to-bid return, HistData bid-only); 2x 3.0 bp; no swap (entry after 00:00 CE(S)T, exit before the rollover). Venue sensitivity: CME 6A 1 tick + $2.50 per side (tick $.0001, $.00005 from 2020-11-22 per CME SER 8648, contract 100,000 AUD).")
    A("- Units: P&L as a fraction of account at weight (0.10/sqrt(252))/sigma; 1 bp = 1e-4 of account.")
    if crash_note:
        A(f"- Disclosure: {crash_note}")
    A("")
    A("## registry_reads.log lines for this id")
    A("")
    A("```")
    for l in gk.reads_log_lines(ID):
        A(l)
    A("```")
    A("")
    A("## Leak checks and QA (before the OOS read; IS window only)")
    A("")
    A("| rule version | truncation passed | days | violations | perturbation passed | days | violations |")
    A("|---|---|---|---|---|---|---|")
    for k, r in isj["leak"].items():
        A(f"| {k} | {gk.fmt(r['truncation_passed'])} | {r['truncation_checked']} | {r['truncation_violations']} | {gk.fmt(r['perturbation_passed'])} | {r['perturbation_checked']} | {r['perturbation_violations']} |")
    A("")
    A("The registered skip rule (`exact`: skip the event when the 15:58 NY bar is missing) reads whether a post-entry bar exists, so the "
      "truncation harness (which deletes every bar after the entry minute) fails it by construction on every sampled day: a data-availability "
      "look-ahead, not a price look-ahead (perturbation, which keeps the bars and moves their prices, passes). The `ex_ante` version (exit at the "
      "first bar at or after 15:58) passes both; its OOS numbers are printed beside the headline (criterion 8, the worse is reported).")
    q = isj["xsource"]
    A("")
    A(f"Cross-source QA (outcome-free): `daily_assets_1970_2026` has no FX series (columns: {', '.join(q['daily_assets_columns'])}), so the "
      f"requested comparison cannot be made: **no matching series exists**. Substitute check through `qe.qa.xsource` on IS dates only: HistData AUDUSD "
      f"17:00 NY close-to-close log returns vs `daily_futures_1984_2016` AD (CME AUD futures excess returns, US close-to-close): correlation lag -1 "
      f"{q['fut_AD']['corr_lag-1']:.3f}, lag 0 {q['fut_AD']['corr_lag+0']:.3f}, lag +1 {q['fut_AD']['corr_lag+1']:.3f}; n = {q['fut_AD']['n']}; "
      f"s.d. ratio futures/HistData {q['fut_AD']['sd_ratio_other_over_fx']:.3f}. Clock evidence for the FX pipeline otherwise rests on the outcome-free "
      "diagnostic in the manifest (shift 0, peak NY 08:30 winter and summer); CAL-I is still owed.")
    A("")
    A(f"IS (information only; nothing is chosen in sample for this row): {isj['is_info']}")
    A("")
    A("## Headline (OOS)")
    A("")
    A(f"Events: {o['events_total']} scheduled statement days; status {o['status_counts']}; traded {o['n']} ({o['trades_per_year']:.1f}/yr). Entry bar later than 00:05 Prague on {o['entry_delay_gt0']} events (max {o['entry_delay_max_min']:.0f} min).")
    A("")
    A("| per-event series | n | mean bp of account | t_iid | t_NW(10) | t day-clustered | t_min |")
    A("|---|---|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x", "net_cme"):
        d = o["ev"][k]
        A(f"| {k} | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw10'], 2)} | {gk.fmt(d['t_cluster'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    A("")
    A("| daily series (zeros on non-event weekdays) | mean bp/day | t_min | t_iid | t_NW(10) |")
    A("|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x"):
        d = o["daily"][k]
        A(f"| {k} | {gk.bp(d['mean'], 3)} | {gk.fmt(d['t_min'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw'], 2)} |")
    A("")
    A(f"- Bootstrap (430,000 draws, alpha 0.05/430): day-cluster on events: lower bound {gk.bp(lb_ev, 2)} bp/event, p5 {gk.bp(o['boot_ev']['p5'], 2)}; daily iid-day resampling: lower bound {gk.bp(lb_d, 3)} bp/day, p5 {gk.bp(o['boot_daily']['p5'], 3)} ({o['boot_seconds']:.0f} s).")
    A(f"- Deciding t = min(event, daily) = {gk.fmt(t_dec, 2)} vs bar 3.6807.")
    A(f"- bp per event on notional: gross {o['bp_notional']['gross']:.2f}, net 1x {o['bp_notional']['net1x']:.2f}; s.d. of the event return {o['bp_notional']['ret_sd']:.1f} bp.")
    A(f"- Sharpe (daily net 1x) {m['sharpe']:.3f}, Mertens/Opdyke s.e. {m['sharpe_se']:.3f}, 90% CI {m['ci90'][0]:.2f}..{m['ci90'][1]:.2f}, Lo-adjusted {m['sharpe_lo']:.3f}; gross {o['metrics_gross']['sharpe']:.3f}. Annual mean {m['ann_mean']*100:.3f}%, vol {m['ann_vol']*100:.3f}%.")
    A(f"- Max drawdown {m['max_dd']*100:.2f}% of account; worst day {m['worst_day']*100:.2f}% ({m['worst_day_date']}); days below -5%: {o['ftmo']['days_below_-5pct']}.")
    A(f"- OOS {years:.2f} years: bar in Sharpe units {pw['bar_sharpe']:.3f}; criterion-4 power at true Sharpe 1.5/2.0/2.4 = {pw['power'][0]:.2f}/{pw['power'][1]:.2f}/{pw['power'][2]:.2f}. {gk.joint_power_note(years)}.")
    A("")
    A("## Criterion 3 (2x cost) and venue sensitivity")
    A("")
    A(f"Net 2x per event {gk.bp(o['ev']['net2x']['mean'], 2)} bp, t_min {gk.fmt(o['ev']['net2x']['t_min'], 2)} (daily {gk.fmt(o['daily']['net2x']['t_min'], 2)}): **{'passed' if v['criterion_3'] else 'failed'}**. CME 6A venue (no count): {gk.bp(o['ev']['net_cme']['mean'], 2)} bp/event, t_min {gk.fmt(o['ev']['net_cme']['t_min'], 2)}.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    pl, re_, bh = o["placebo"], o["random_entry"], o["buy_hold"]
    A(f"- Placebo days (every other OOS weekday, same clocks, long, row weight): n {pl['n']}, mean gross {gk.bp(pl['gross_mean'], 2)} bp of account (return {pl['ret_bp_mean']:.2f} bp), t {gk.fmt(pl['t'], 2)}.")
    A(f"- Random-entry null (10,000 paths of {o['n']} placebo days): strategy gross {gk.bp(re_['strategy_gross'], 2)} bp vs null mean {gk.bp(re_['null_mean'], 2)}, p95 {gk.bp(re_['null_p95'], 2)}; percentile {re_['percentile']:.3f}: {'passed' if re_['beats_95'] else 'failed'}.")
    A(f"- Buy-and-hold, always long the same window every weekday at the strategy's average exposure ({bh['mean_exposure']:.4f}): B&H total {bh['bh_total']*100:.2f}%, beta {bh['beta']:.3f}, alpha t_min {gk.fmt(bh['alpha_t_min'], 2)} (need >= 3.6807). {bh['note']}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    yt = o["by_year"].reset_index()
    yt.columns = ["year", "net1x", "weekdays", "counts", "share_of_net"]
    ye = o["by_year_events"]
    yt["events"] = yt["year"].map(ye["count"]).fillna(0).astype(int)
    A(gk.md_table(yt, {"net1x": lambda x: f"{x*100:.3f}%", "share_of_net": lambda x: gk.fmt(x, 2), "weekdays": lambda x: str(int(x))}))
    ys = o["years_summary"]
    A("")
    A(f"Years counted {ys['years_counted']}, positive {ys['positive']}, need {ys['need']}; max year share {gk.fmt(ys['max_year_share'], 2)}, max month share {gk.fmt(ys['max_month_share'], 2)}: **{'passed' if ys['passed'] else 'failed'}**.")
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["tercile (0 = low vol)", "events", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"tercile (0 = low vol)": lambda x: str(int(x)), "events": lambda x: str(int(x)), "net1x sum": lambda x: f"{x*100:.3f}%", "net1x mean": lambda x: gk.bp(x, 2) + " bp"}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; IS bounds of the trailing 20-day s.d. of daily returns {o['bounds'][0]*100:.3f}% / {o['bounds'][1]*100:.3f}%).")
    b20 = o["best20"]
    A("")
    A(f"Best-20-days: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A(f"Neighbourhood (median hold {o['hold0_min']:.0f} min; +-25% = {o['shift_min']} min; run once on OOS, never changes the headline; threshold: none in this row):")
    A("")
    A(gk.md_table(o["neighbourhood"], {"net1x_total": lambda x: f"{x*100:.3f}%", "net1x_bp_per_event": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "events": lambda x: str(int(x)), "net_positive": gk.fmt}))
    A("")
    A("Execution variants (one-minute delay: criterion 7; as-written vs ex-ante: criterion 8):")
    A("")
    A(gk.md_table(o["execution"], {"net1x_total": lambda x: f"{x*100:.3f}%", "t_min": lambda x: gk.fmt(x, 2), "share_of_base": lambda x: gk.fmt(x, 2), "events": lambda x: str(int(x))}))
    A("")
    A(f"Criterion 7 overall: **{'passed' if c7 else 'failed'}**.")
    A("")
    A("Sub-periods (institutional change dates in the row; information only):")
    A("")
    A(gk.md_table(o["subperiods"], {"net1x_total": lambda x: f"{x*100:.3f}%", "net1x_bp_per_event": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "events": lambda x: str(int(x))}))
    A("")
    A("## Criteria 2 and 12 (process)")
    A("")
    A(f"- Criterion 2: OOS {years:.1f} years incl. 2020 and 2022; {o['n']} trades on {o['n']} distinct days (need >= 300 trades on >= 150 days for an event strategy): **not met** (8 events/yr cannot meet it; the row is a stack-sleeve test, as its notes say).")
    A("- Criterion 5: single configuration; CSCV n/a. Criterion 11 (prop-fit) belongs to Department F; no order falls inside 13:58-14:02 NY by construction.")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(t_dec, 2)} vs 3.6807, bootstrap lower bound {'> 0' if min(lb_ev, lb_d) > 0 else '<= 0'}: **{'passed' if v['criterion_4'] else 'failed'}**. (2) criterion 3: **{'passed' if v['criterion_3'] else 'failed'}**. (3) criterion 7: **{'passed' if c7 else 'failed'}**. (4)-(5): not reached.")
    A(f"- Near-miss by the row's definition (t >= 2.0 with criterion 3 passed): {gk.fmt(v['near_miss_row_def'])}; by the batch brief's (t within 1.0 of the bar with p5 > 0): {gk.fmt(v['near_miss_brief_def'])}.")
    A(f"- **Verdict: {v['verdict']}.** Read against the power above; a failure is not evidence of absence.")
    Path(out_path).write_text("\n".join(L) + "\n")
    summ = {"id": ID, "net1x_bp_per_event": o["ev"]["net1x"]["mean"] * 1e4, "t_min": t_dec, "t_event": t_ev, "t_daily": t_d,
            "boot_lower_event_bp": lb_ev * 1e4, "boot_lower_daily_bp": lb_d * 1e4, "t2x": o["ev"]["net2x"]["t_min"], "verdict": v["verdict"]}
    print(json.dumps(summ, indent=1))
    return summ


def main(stage, cmd):
    pinres = [pins.verify(ID, FXDS), pins.verify(ID, CALDS)]
    if stage == "is":
        bars = load_bars("is")
        days = [d for d in fd.statement_days(load_cal("is")) if pd.Timestamp(IS_START) <= d <= pd.Timestamp(IS_END)]
        c = fx.ny_closes(bars)
        sd20 = c["r"].rolling(20, min_periods=15).std().dropna()
        bounds = (float(sd20.quantile(1 / 3)), float(sd20.quantile(2 / 3)))
        ev = fd.events(bars, days, fd.Params())
        okk = ev[ev["status"] == "ok"]
        n1 = okk["gross"] - okk["cost1"]
        info = (f"{len(days)} statement days, status {ev['status'].value_counts().to_dict()}; net 1x {n1.mean()*1e4:.2f} bp/event, "
                f"t {gk.event_stats(okk.assign(x=n1), 'x')['t_min']:.2f}")
        xs = xsource_qa(bars)
        print(info, xs, flush=True)
        leak = leak_checks(bars, days)
        d = {"leak": leak, "is_info": info, "bounds": bounds, "xsource": xs}
        (HERE / "Q-0003_is.json").write_text(json.dumps(d, indent=1, default=str))
        return
    isj = json.loads((HERE / "Q-0003_is.json").read_text())
    bounds = tuple(isj["bounds"])
    if stage == "dryrun":
        bars = load_bars("is")
        mid = "2012-01-01"
        days = [d for d in fd.statement_days(load_cal("is")) if pd.Timestamp(mid) <= d <= pd.Timestamp(IS_END)]
        yrs = (pd.Timestamp(IS_END) - pd.Timestamp(mid)).days / 365.25
        o = evaluate(bars, days, mid, IS_END, bounds, yrs)
        o["bounds"] = bounds
        write_result(o, isj, pinres, cmd, Path(SCRATCH) / "Q-0003.dry.md")
        return
    bars = pd.concat([load_bars("is"), load_bars("oos")], ignore_index=True)   # <- the one OOS read of the bars
    cal = load_cal("oos")                                                       # <- the one OOS read of the calendar
    bars = bars.drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    days = [d for d in fd.statement_days(cal) if pd.Timestamp(OOS_START) <= d <= pd.Timestamp(OOS_END)]
    yrs = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    o = evaluate(bars, days, OOS_START, OOS_END, bounds, yrs)
    o["bounds"] = bounds
    write_result(o, isj, pinres, cmd, ROOT / "research" / "results" / "Q-0003.md")
    o["ok"].to_csv(HERE / "Q-0003_oos_events.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    main(a.stage, f"python3 quant-edge/research/q0003/q0003.py --stage {a.stage}")
