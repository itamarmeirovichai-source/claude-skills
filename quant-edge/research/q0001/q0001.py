#!/usr/bin/env python3
"""Q-0001 London-fix month-end equity-hedge legs (registered 93cb97a). Data only through qe.gateway.load.
Stages:  --stage is      IS events (information), IS tercile bounds, leak harness per pair (as-written and ex-ante),
                         signal truncation/perturbation on the daily assets, cross-source QA
         --stage dryrun  the complete OOS pipeline on IS data only (2013-2015 as the pretend window)
         --stage oos     exactly ONE OOS read per dataset (3 pairs + daily_assets) + IS history; every Gate-v2 number
Usage: python3 quant-edge/research/q0001/q0001.py --stage {is,dryrun,oos}
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
import fixflow as ff  # noqa: E402

ID = "Q-0001"
FXDS = {p: f"histdata_fx_1m_{p}" for p in ff.PAIRS}
ASDS = "daily_assets_1970_2026"
FUT = {"EURUSD": "EC", "GBPUSD": "BP", "AUDUSD": "AD"}
IS_START, IS_END = "2010-01-04", "2015-02-13"
OOS_START, OOS_END = "2015-03-02", "2024-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"
SUBPERIODS = [("2015-03-02", "2018-01-02", "before MiFID II"), ("2018-01-03", "2024-12-31", "MiFID II / FX Global Code")]


def load_bars(pair, window):
    b = gateway.load(ID, window, dataset=FXDS[pair])
    return b[["ts", "open", "high", "low", "close"]].reset_index(drop=True)


def load_assets(window):
    a = gateway.load(ID, window, dataset=ASDS).set_index("ts")
    a.index = a.index.tz_localize(None).normalize()
    return a


def run_events(bars, closes, sig, p):
    parts = [ff.pair_events(bars[k], k, sig, p, closes[k] if (closes and p.com == 60.0) else None) for k in ff.PAIRS]
    return pd.concat(parts, ignore_index=True)


def aggregate(pe: pd.DataFrame, venue=True) -> pd.DataFrame:
    ok = pe[pe["status"] == "ok"].copy()
    if venue:
        ok["cme_cost"] = ok["w"] * np.array([fx.cme_cost_frac(k, d, a) + fx.cme_cost_frac(k, d, b)
                                             for k, d, a, b in zip(ok["pair"], ok["day"], ok["entry_px"], ok["exit_px"])])
    else:
        ok["cme_cost"] = np.nan
    ok["net1"] = ok["gross"] - ok["cost1"]
    ok["net2"] = ok["gross"] - 2 * ok["cost1"]
    ok["net_cme"] = ok["gross"] - ok["cme_cost"]
    ev = ok.groupby("day").agg(gross=("gross", "sum"), cost1=("cost1", "sum"), net1=("net1", "sum"), net2=("net2", "sum"),
                               net_cme=("net_cme", "sum"), bench=("bench", "sum"), n_pairs=("pair", "size"), side=("side", "first"),
                               S=("S", "first")).reset_index()
    return ok, ev


def daily_series(ev, col, start, end):
    idx = pd.bdate_range(start, end)
    s = pd.Series(0.0, index=idx)
    v = ev.set_index(pd.to_datetime(ev["day"]))[col]
    k = v.index.intersection(idx)
    s.loc[k] = v.loc[k].to_numpy()
    return s


def leak_checks(bars_is, assets_is, days):
    sig = ff.signal_table(assets_is, days)
    out = {}
    for pair in ff.PAIRS:
        fr = fx.tag_for_harness(bars_is[pair])
        for mode in ("as_written", "ex_ante"):
            rule = ff.FixRule(pair, sig, ff.Params(filter=mode))
            a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
            b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
            out[f"{pair} {mode}"] = {"truncation_passed": a["passed"], "truncation_checked": a["n_checked"], "truncation_violations": len(a["violations"]),
                                     "perturbation_passed": b["passed"], "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])}
            print(pair, mode, out[f"{pair} {mode}"], flush=True)
    # the signal's own truncation / perturbation on the daily assets: rows dated >= D deleted or perturbed
    rng = np.random.default_rng(SEED)
    bad_t = bad_p = 0
    for D in days:
        a = ff.signal_table(assets_is[assets_is.index < D], [D]).iloc[0]
        pert = assets_is.copy()
        m = pert.index >= D
        for c in ("GLSTOCK", "USLCAP"):
            pert.loc[m, c] = pert.loc[m, c] * np.exp(rng.standard_normal(m.sum()) * 0.05)
        b = ff.signal_table(pert, [D]).iloc[0]
        f = sig[sig["day"] == D].iloc[0]
        bad_t += int(not (a["side"] == f["side"] and (np.isnan(f["S"]) and np.isnan(a["S"]) or a["S"] == f["S"])))
        bad_p += int(not (b["side"] == f["side"] and (np.isnan(f["S"]) and np.isnan(b["S"]) or b["S"] == f["S"])))
    out["signal (daily assets)"] = {"truncation_passed": bad_t == 0, "truncation_checked": len(days), "truncation_violations": bad_t,
                                    "perturbation_passed": bad_p == 0, "perturbation_checked": len(days), "perturbation_violations": bad_p}
    return out, sig


def xsource_qa(bars_is):
    res = {"daily_assets_columns": xsource.available_columns(ASDS)}
    for pair in ff.PAIRS:
        r = fx.ny_closes(bars_is[pair])["r"].dropna()
        fut = xsource.second_source_returns("daily_futures_1984_2016", FUT[pair], IS_START, IS_END)
        res[pair] = {"vs": FUT[pair], **xsource.compare(r, fut)}
    return res


def evaluate(bars, assets, start, end, bounds, years, heavy=True):
    p = ff.Params()
    days = ff.event_days(start, end)
    sig = ff.signal_table(assets, days)
    closes = {k: fx.ny_closes(bars[k]) for k in ff.PAIRS}
    pe = run_events(bars, closes, sig, p)
    ok, ev = aggregate(pe)
    o = {"years": years, "n_event_days": len(days), "sig_status": sig["sig_status"].value_counts().to_dict(),
         "pair_status": pe.groupby(["pair", "status"]).size().unstack(fill_value=0), "n_events": len(ev), "n_pair_events": len(ok),
         "share_S_pos": float((ev["S"] > 0).mean()) if len(ev) else float("nan"), "S_abs_median": float(ev["S"].abs().median())}
    cl = lambda x, c: gk.event_stats(x.assign(xx=x[c]), "xx")  # noqa: E731
    o["ev"] = {k: cl(ev, c) for k, c in (("gross", "gross"), ("net1x", "net1"), ("net2x", "net2"), ("net_cme", "net_cme"))}
    o["pair_level"] = {k: cl(ok, c) for k, c in (("gross", "gross"), ("net1x", "net1"))}
    o["by_pair"] = ok.groupby("pair").agg(n=("net1", "size"), net1_sum=("net1", "sum"), net1_mean=("net1", "mean"),
                                          ret_signed_bp=("ret", lambda s: float((s * ok.loc[s.index, "side"]).mean() * 1e4)))
    d1, d2, dg = (daily_series(ev, c, start, end) for c in ("net1", "net2", "gross"))
    ppy = len(d1) / years
    o["ppy"] = ppy
    o["daily"] = {k: {"mean": float(v.mean()), **gk.t_block(v.to_numpy(), 10)} for k, v in (("gross", dg), ("net1x", d1), ("net2x", d2))}
    o["metrics"], o["metrics_gross"] = gk.daily_metrics(d1, ppy), gk.daily_metrics(dg, ppy)
    o["bp_notional"] = {"gross_signed": float((ok["ret"] * ok["side"]).mean() * 1e4), "ret_sd": float(ok["ret"].std() * 1e4)}
    o["trades_per_year"] = len(ok) / years
    yt, ys = gk.by_year(d1, d1.groupby(d1.index.year).size(), float(d1.sum()))
    o["by_year"], o["years_summary"] = yt, ys
    o["by_year_events"] = ev.groupby(pd.to_datetime(ev["day"]).dt.year)["net1"].agg(["count", "sum"])
    o["best20"] = gk.best_days_drop(d1, 20, 10)
    terc = []
    for r in ok.itertuples():
        lo, hi = bounds[r.pair]
        terc.append(0 if r.sd20 <= lo else (1 if r.sd20 <= hi else 2))
    ok["tercile"] = terc
    tt = ok.groupby("tercile")["net1"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    o["terciles"], o["terciles_positive"] = tt, int((tt["sum"] > 0).sum())
    hold0 = 357.0
    sh = round(0.25 * hold0)
    o["shift_min"] = sh
    rows = []
    for name, q in [("(as registered)", p), (f"entry +{sh} min (hold x0.75, exit fixed)", replace(p, entry_shift_min=sh)),
                    (f"entry -{sh} min (hold x1.25, exit fixed)", replace(p, entry_shift_min=-sh)),
                    (f"exit -{sh} min (hold x0.75, entry fixed)", replace(p, exit_shift_min=-sh)),
                    (f"exit +{sh} min (hold x1.25, entry fixed; crosses the fix)", replace(p, exit_shift_min=sh)),
                    ("com=45", replace(p, com=45.0)), ("com=75", replace(p, com=75.0))]:
        _, e = aggregate(run_events(bars, closes, sig, q), venue=False)
        rows.append({"variant": name, "events": len(e), "net1x_total": float(e["net1"].sum()), "net1x_bp_per_event": float(e["net1"].mean() * 1e4),
                     "t_min": cl(e, "net1")["t_min"], "net_positive": bool(e["net1"].sum() > 0)})
    o["neighbourhood"] = pd.DataFrame(rows)
    o["threshold_note"] = "signal threshold 0: +-25% of 0 is 0, no neighbour exists"
    ex = []
    base_tot = float(ev["net1"].sum())
    for name, q in (("registered", p), ("entry delayed one minute (10:01)", replace(p, entry_shift_min=1)),
                    ("entry and exit delayed one minute", replace(p, entry_shift_min=1, exit_shift_min=1)),
                    ("ex-ante filter (pre-entry bars only; exit first bar at or after 15:57)", replace(p, filter="ex_ante"))):
        _, e = aggregate(run_events(bars, closes, sig, q), venue=False)
        ex.append({"variant": name, "events": len(e), "net1x_total": float(e["net1"].sum()), "t_min": cl(e, "net1")["t_min"],
                   "share_of_base": float(e["net1"].sum() / base_tot) if base_tot > 0 else float("nan")})
    o["execution"] = pd.DataFrame(ex)
    sp = []
    for a, b, lab in SUBPERIODS:
        x = ev[(pd.to_datetime(ev["day"]) >= a) & (pd.to_datetime(ev["day"]) <= b)]
        sp.append({"period": f"{a}..{b} ({lab})", "events": len(x), "net1x_total": float(x["net1"].sum()),
                   "net1x_bp_per_event": float(x["net1"].mean() * 1e4) if len(x) else float("nan"),
                   "t_min": cl(x, "net1")["t_min"] if len(x) > 2 else float("nan")})
    o["subperiods"] = pd.DataFrame(sp)
    # random entry: other weekdays, same clocks and filter, each event's side and pair set kept
    evd = set(pd.Timestamp(d) for d in days)
    pdays = [d for d in pd.bdate_range(start, end) if d not in evd]
    psig = pd.DataFrame({"day": pdays, "S": np.nan, "side": 1, "sig_status": "placebo"})
    G, Wp = [], []
    for k in ff.PAIRS:
        x = ff.pair_events(bars[k], k, psig, p, closes[k])
        G.append(np.where(x["status"] == "ok", x["bench"], np.nan))
        Wp.append(np.where(x["status"] == "ok", x["w"], np.nan))
    G, Wp = np.vstack(G).T, np.vstack(Wp).T              # days x pairs: w * ret (long), w
    full = np.isfinite(G).all(axis=1)
    G = G[full]
    mask = np.zeros((len(ev), 3))
    for j, d in enumerate(ev["day"]):
        mask[j] = [((ok["day"] == d) & (ok["pair"] == k)).any() for k in ff.PAIRS]
    sides = ev["side"].to_numpy(float)
    rng = np.random.default_rng(SEED)
    null = np.empty(10_000)
    for i in range(0, 10_000, 500):
        D = rng.integers(0, G.shape[0], size=(500, len(ev)))
        null[i:i + 500] = ((G[D] * mask[None]).sum(axis=2) * sides[None]).mean(axis=1)
    sg = float(ev["gross"].mean())
    o["random_entry"] = {"n_paths": 10_000, "pool_days": int(G.shape[0]), "strategy_gross": sg, "null_mean": float(null.mean()),
                         "null_p95": float(np.quantile(null, 0.95)), "percentile": float((null < sg).mean()), "beats_95": bool((null < sg).mean() >= 0.95)}
    # shuffled signal: event sides permuted across events (side mix kept), 10,000 permutations, gross
    bench = ev["bench"].to_numpy()
    perm = np.array([(rng.permutation(sides) * bench).mean() for _ in range(10_000)])
    o["sign_perm"] = {"n_perm": 10_000, "observed": float((sides * bench).mean()), "p": float((1 + (perm >= (sides * bench).mean()).sum()) / 10_001)}
    # buy-and-hold: (a) long the foreign currencies over the same minutes at the same weights (event level);
    # (b) always long the same window every weekday at the strategy's average daily exposure (daily level)
    s_, b_ = ev["net1"].to_numpy(), bench
    beta = float(np.cov(s_, b_)[0, 1] / b_.var()) if b_.var() > 0 else 0.0
    al = s_ - beta * b_
    o["bh_same"] = {"bh_mean_bp": float(b_.mean() * 1e4), "beta": beta, "alpha_bp": float(al.mean() * 1e4),
                    "alpha_t_min": cl(ev.assign(al=al), "al")["t_min"]}
    pdi = pd.DatetimeIndex(np.array(pdays)[full])
    bh = pd.Series(0.0, index=d1.index)
    k_ = pdi.intersection(bh.index)
    bh.loc[k_] = pd.Series(G.sum(axis=1), index=pdi).loc[k_].to_numpy()
    k2 = pd.DatetimeIndex(pd.to_datetime(ev["day"])).intersection(bh.index)
    bh.loc[k2] = ev.set_index(pd.to_datetime(ev["day"]))["bench"].loc[k2].to_numpy()
    Wsum_all = float(np.nansum(Wp[full])) + float(ok["w"].sum())
    scale = float(ok["w"].sum()) / Wsum_all if Wsum_all > 0 else 0.0        # same average exposure as the strategy
    bh = bh * scale
    ss, bb = d1.to_numpy(), bh.to_numpy()
    bet2 = float(np.cov(ss, bb)[0, 1] / bb.var()) if bb.var() > 0 else 0.0
    o["bh_always"] = {"scale": scale, "bh_total": float(bb.sum()), "beta": bet2, "alpha_t_min": gk.t_block(ss - bet2 * bb, 10)["t_min"]}
    o["ftmo"] = {"days_below_-5pct": int((d1 < -0.05).sum())}
    o["ok"], o["evtab"] = ok, ev
    if heavy:
        t0 = time.time()
        o["boot_ev"] = gk.bootstrap_events(ev, "net1", SEED)
        o["boot_daily"] = gk.bootstrap_daily(d1, 1.0, SEED)
        o["boot_seconds"] = time.time() - t0
    return o


def write_result(o, isj, pinres, cmd, out_path):
    years = o["years"]
    pw = gk.power_block(years)
    t_ev, t_d = o["ev"]["net1x"]["t_min"], o["daily"]["net1x"]["t_min"]
    t_pair = o["pair_level"]["net1x"]["t_min"]
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
    A("# Q-0001 — month-end London-fix equity-hedge legs (EURUSD, GBPUSD, AUDUSD): Gate-v2 OOS result")
    A("")
    A(f"Registry row Q-0001 (registered commit 93cb97a, count 1, sign fixed: S_D > 0 sells the foreign currencies). Script `research/q0001/q0001.py` (rule `research/q0001/fixflow.py`, plumbing `research/batch1/fxkit.py`, `gatekit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap {SEED} (430,000 draws each), random-entry and sign permutation {SEED} (10,000 each), harness {SEED}.")
    for r in pinres:
        A(f"- Data `{r['dataset']}` sha256: manifest {r['manifest_sha256']} = row pin {r['row_sha256']} = recomputed {r['computed_sha256']} (ok={r['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END}; OOS {OOS_START}..{OOS_END} (2015-02-14..2015-03-01 is in neither window); hold-out not read.")
    A("- Costs 1x per side on notional: EURUSD 1.0 bp, GBPUSD 1.2 bp, AUDUSD 1.5 bp (bid-to-bid returns); 2x doubled; no swap. Venue sensitivity (no count): CME 6E/6B/6A 1 tick + $2.50 per side (6E $.00005 x 125,000 EUR; 6B $.0001 x 62,500 GBP; 6A $.0001 x 100,000 AUD, $.00005 from 2020-11-22 per CME SER 8648).")
    A("- Units: P&L as a fraction of account; w_p = (0.10/sqrt(252))/sigma_p/3; 1 bp = 1e-4 of account. Per-event P&L = sum over the traded pairs.")
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
    A("The registered skip rule (as_written: more than 10 missing bars in 09:55-15:57, or the 15:57 bar missing) reads post-entry bar availability, so "
      "truncation fails it by construction (a data-availability look-ahead, not a price look-ahead; perturbation passes). The ex_ante version passes "
      "both; its OOS numbers are printed (criterion 8: the worse is reported). The signal check deletes / perturbs (5% noise) every daily-assets row "
      "dated on or after D and requires S_D and the side to be unchanged.")
    q = isj["xsource"]
    A("")
    A(f"Cross-source QA (outcome-free): `daily_assets_1970_2026` has no FX series (columns: {', '.join(q['daily_assets_columns'])}): **no matching series exists**, "
      "so the requested correlation cannot be computed. Substitute check (`qe.qa.xsource`, IS dates only): HistData 17:00 NY close-to-close log returns vs "
      "`daily_futures_1984_2016` CME currency-futures excess returns (US close-to-close):")
    A("")
    A("| pair | futures | n | corr lag -1 | corr lag 0 | corr lag +1 | s.d. ratio fut/HistData |")
    A("|---|---|---|---|---|---|---|")
    for pair in ff.PAIRS:
        z = q[pair]
        A(f"| {pair} | {z['vs']} | {z['n']} | {z['corr_lag-1']:.3f} | {z['corr_lag+0']:.3f} | {z['corr_lag+1']:.3f} | {z['sd_ratio_other_over_fx']:.3f} |")
    A("")
    A("The clock is otherwise supported only by the manifest's outcome-free diagnostic (shift 0, peak NY 08:30 winter and summer); CAL-I is still owed (accepted risk in the row).")
    A("")
    A(f"IS (information only; nothing is chosen in sample for this row): {isj['is_info']}")
    A("")
    A("## Headline (OOS)")
    A("")
    A(f"Event days {o['n_event_days']}; signal status {o['sig_status']}; traded events {o['n_events']}, pair-events {o['n_pair_events']} ({o['trades_per_year']:.1f}/yr); share of events with S_D > 0 (sell foreign) {o['share_S_pos']:.2f}; median |S_D| {o['S_abs_median']*100:.2f}%.")
    A("")
    ps = o["pair_status"].reset_index()
    A(gk.md_table(ps, {c: (lambda x: str(int(x))) for c in ps.columns if c != "pair"}))
    A("")
    A("| per-event series | n | mean bp of account | t_iid | t_NW(10) | t day-clustered | t_min |")
    A("|---|---|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x", "net_cme"):
        d = o["ev"][k]
        A(f"| {k} | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw10'], 2)} | {gk.fmt(d['t_cluster'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    for k in ("gross", "net1x"):
        d = o["pair_level"][k]
        A(f"| pair-event {k} (clustered by day) | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw10'], 2)} | {gk.fmt(d['t_cluster'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    A("")
    A("| daily series (zeros on other weekdays) | mean bp/day | t_min | t_iid | t_NW(10) |")
    A("|---|---|---|---|---|")
    for k in ("gross", "net1x", "net2x"):
        d = o["daily"][k]
        A(f"| {k} | {gk.bp(d['mean'], 3)} | {gk.fmt(d['t_min'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw'], 2)} |")
    A("")
    bpair = o["by_pair"].reset_index()
    A(gk.md_table(bpair, {"n": lambda x: str(int(x)), "net1_sum": lambda x: f"{x*100:.3f}%", "net1_mean": lambda x: gk.bp(x, 2) + " bp", "ret_signed_bp": lambda x: gk.fmt(x, 2)}))
    A("")
    A(f"- Bootstrap (430,000 draws, alpha 0.05/430): day-cluster on events: lower bound {gk.bp(lb_ev, 2)} bp/event, p5 {gk.bp(o['boot_ev']['p5'], 2)}; daily iid-day: lower bound {gk.bp(lb_d, 3)} bp/day, p5 {gk.bp(o['boot_daily']['p5'], 3)} ({o['boot_seconds']:.0f} s).")
    A(f"- Deciding t = min(event, daily) = {gk.fmt(t_dec, 2)} vs bar 3.6807 (pair-event clustered t {gk.fmt(t_pair, 2)}).")
    A(f"- Signed return per pair-event on notional: {o['bp_notional']['gross_signed']:.2f} bp gross; s.d. {o['bp_notional']['ret_sd']:.1f} bp.")
    A(f"- Sharpe (daily net 1x) {m['sharpe']:.3f}, Mertens/Opdyke s.e. {m['sharpe_se']:.3f}, 90% CI {m['ci90'][0]:.2f}..{m['ci90'][1]:.2f}, Lo-adjusted {m['sharpe_lo']:.3f}; gross {o['metrics_gross']['sharpe']:.3f}. Annual mean {m['ann_mean']*100:.3f}%, vol {m['ann_vol']*100:.3f}%.")
    A(f"- Max drawdown {m['max_dd']*100:.2f}% of account; worst day {m['worst_day']*100:.2f}% ({m['worst_day_date']}); days below -5%: {o['ftmo']['days_below_-5pct']}.")
    A(f"- OOS {years:.2f} years: bar in Sharpe units {pw['bar_sharpe']:.3f}; criterion-4 power at true Sharpe 1.5/2.0/2.4 = {pw['power'][0]:.2f}/{pw['power'][1]:.2f}/{pw['power'][2]:.2f}. {gk.joint_power_note(years)}.")
    A("")
    A("## Criterion 3 (2x cost) and venue sensitivity")
    A("")
    A(f"Net 2x per event {gk.bp(o['ev']['net2x']['mean'], 2)} bp, t_min {gk.fmt(o['ev']['net2x']['t_min'], 2)} (daily {gk.fmt(o['daily']['net2x']['t_min'], 2)}): **{'passed' if v['criterion_3'] else 'failed'}**. CME venue (no count): {gk.bp(o['ev']['net_cme']['mean'], 2)} bp/event, t_min {gk.fmt(o['ev']['net_cme']['t_min'], 2)}.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    re_, sp_, bs, ba = o["random_entry"], o["sign_perm"], o["bh_same"], o["bh_always"]
    A(f"- Random-entry null (10,000 paths; each event's side and pair set kept, its day drawn from {re_['pool_days']} other OOS weekdays with all three pairs valid, same clocks, the drawn day's weights): strategy gross {gk.bp(re_['strategy_gross'], 2)} bp/event vs null mean {gk.bp(re_['null_mean'], 2)}, p95 {gk.bp(re_['null_p95'], 2)}; percentile {re_['percentile']:.3f}: {'passed' if re_['beats_95'] else 'failed'}.")
    A(f"- Shuffled signal (event sides permuted across events, 10,000; N_family = 1): p = {sp_['p']:.4f} (need < 0.05).")
    A(f"- Buy-and-hold (a), long the three currencies over the same minutes at the same weights on the event days: B&H {bs['bh_mean_bp']:.2f} bp/event, beta {bs['beta']:.3f}, alpha {bs['alpha_bp']:.2f} bp/event, alpha t_min {gk.fmt(bs['alpha_t_min'], 2)} (need >= 3.6807).")
    A(f"- Buy-and-hold (b), always long the same window every weekday (three pairs, row weights, scaled by {ba['scale']:.4f} to the strategy's average exposure): B&H total {ba['bh_total']*100:.2f}%, beta {ba['beta']:.3f}, alpha t_min {gk.fmt(ba['alpha_t_min'], 2)}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    yt = o["by_year"].reset_index()
    yt.columns = ["year", "net1x", "weekdays", "counts", "share_of_net"]
    yt["events"] = yt["year"].map(o["by_year_events"]["count"]).fillna(0).astype(int)
    A(gk.md_table(yt, {"net1x": lambda x: f"{x*100:.3f}%", "share_of_net": lambda x: gk.fmt(x, 2), "weekdays": lambda x: str(int(x))}))
    ys = o["years_summary"]
    A("")
    A(f"Years counted {ys['years_counted']} (2015 holds {int(yt.loc[yt.year == 2015, 'weekdays'].iloc[0]) if (yt.year == 2015).any() else 0} OOS weekdays), positive {ys['positive']}, need {ys['need']}; max year share {gk.fmt(ys['max_year_share'], 2)}, max month share {gk.fmt(ys['max_month_share'], 2)}: **{'passed' if ys['passed'] else 'failed'}**.")
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["tercile (0 = low vol)", "pair-events", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"tercile (0 = low vol)": lambda x: str(int(x)), "pair-events": lambda x: str(int(x)), "net1x sum": lambda x: f"{x*100:.3f}%", "net1x mean": lambda x: gk.bp(x, 2) + " bp"}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; per-pair IS bounds of the trailing 20-day s.d.: {', '.join(f'{k} {a*100:.3f}%/{b*100:.3f}%' for k, (a, b) in o['bounds'].items())}).")
    b20 = o["best20"]
    A("")
    A(f"Best-20-days: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A(f"Neighbourhood (hold 357 min; +-25% = {o['shift_min']} min; {o['threshold_note']}; run once on OOS, never changes the headline):")
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
    A(f"- Criterion 2: OOS {years:.1f} years incl. 2020 and 2022; {o['n_pair_events']} pair-trades on {o['n_events']} distinct days (need >= 300 trades on >= 150 days): **{'met' if (o['n_pair_events'] >= 300 and o['n_events'] >= 150) else 'not met'}**.")
    A("- Criterion 5: single configuration; CSCV n/a. Criterion 11 (prop-fit) belongs to Department F.")
    A("- FTMO news rule: the row's skip of entries/exits inside +-2 min of a high-impact release needs a UK/EU calendar that is not in the manifest; not applied, logged here as the row instructs. (US 08:30/10:00 ET releases fall at 13:30/15:00 London, not at 10:00 or 15:57.)")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(t_dec, 2)} vs 3.6807, bootstrap lower bound {'> 0' if min(lb_ev, lb_d) > 0 else '<= 0'}: **{'passed' if v['criterion_4'] else 'failed'}**. (2) criterion 3: **{'passed' if v['criterion_3'] else 'failed'}**. (3) criterion 7: **{'passed' if c7 else 'failed'}**. (4)-(5): not reached.")
    A(f"- Near-miss by the row's definition (t >= 2.0 with criterion 3 passed): {gk.fmt(v['near_miss_row_def'])}; by the batch brief's (t within 1.0 of the bar with p5 > 0): {gk.fmt(v['near_miss_brief_def'])}.")
    A(f"- **Verdict: {v['verdict']}.** Read against the power above; a failure is not evidence of absence.")
    Path(out_path).write_text("\n".join(L) + "\n")
    summ = {"id": ID, "net1x_bp_per_event": o["ev"]["net1x"]["mean"] * 1e4, "t_min": t_dec, "t_event": t_ev, "t_daily": t_d, "t_pair": t_pair,
            "boot_lower_event_bp": lb_ev * 1e4, "boot_lower_daily_bp": lb_d * 1e4, "t2x": o["ev"]["net2x"]["t_min"], "verdict": v["verdict"]}
    print(json.dumps(summ, indent=1))
    return summ


def main(stage, cmd):
    pinres = [pins.verify(ID, FXDS[k]) for k in ff.PAIRS] + [pins.verify(ID, ASDS)]
    if stage == "is":
        bars = {k: load_bars(k, "is") for k in ff.PAIRS}
        assets = load_assets("is")
        days = ff.event_days(IS_START, IS_END)
        bounds = {}
        for k in ff.PAIRS:
            sd20 = fx.ny_closes(bars[k])["r"].rolling(20, min_periods=15).std().dropna()
            bounds[k] = (float(sd20.quantile(1 / 3)), float(sd20.quantile(2 / 3)))
        xs = xsource_qa(bars)
        print(xs, flush=True)
        sig = ff.signal_table(assets, days)
        pe = run_events(bars, None, sig, ff.Params())
        okk, ev = aggregate(pe, venue=False)
        info = (f"{len(days)} event days, signal status {sig['sig_status'].value_counts().to_dict()}, {len(ev)} traded events / {len(okk)} pair-events; "
                f"net 1x {ev['net1'].mean()*1e4:.2f} bp/event, t {gk.event_stats(ev, 'net1')['t_min']:.2f}")
        print(info, flush=True)
        leak, _ = leak_checks(bars, assets, days)
        (HERE / "Q-0001_is.json").write_text(json.dumps({"leak": leak, "is_info": info, "bounds": bounds, "xsource": xs}, indent=1, default=str))
        return
    isj = json.loads((HERE / "Q-0001_is.json").read_text())
    bounds = {k: tuple(v) for k, v in isj["bounds"].items()}
    if stage == "dryrun":
        bars = {k: load_bars(k, "is") for k in ff.PAIRS}
        assets = load_assets("is")
        mid = "2013-01-01"
        yrs = (pd.Timestamp(IS_END) - pd.Timestamp(mid)).days / 365.25
        o = evaluate(bars, assets, mid, IS_END, bounds, yrs)
        o["bounds"] = bounds
        write_result(o, isj, pinres, cmd, Path(SCRATCH) / "Q-0001.dry.md")
        return
    bars, assets = {}, None
    for k in ff.PAIRS:                                                   # <- one OOS read per pair
        bars[k] = pd.concat([load_bars(k, "is"), load_bars(k, "oos")], ignore_index=True).drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    assets = pd.concat([load_assets("is"), load_assets("oos")]).sort_index()   # <- one OOS read of daily_assets
    assets = assets[~assets.index.duplicated()]
    yrs = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    o = evaluate(bars, assets, OOS_START, OOS_END, bounds, yrs)
    o["bounds"] = bounds
    write_result(o, isj, pinres, cmd, ROOT / "research" / "results" / "Q-0001.md")
    o["ok"].to_csv(HERE / "Q-0001_oos_pair_events.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    main(a.stage, f"python3 quant-edge/research/q0001/q0001.py --stage {a.stage}")
