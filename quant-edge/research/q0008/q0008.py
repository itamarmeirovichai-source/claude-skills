#!/usr/bin/env python3
"""Q-0008 HSI after-hours fade on HK50 (registered 0a46ddd). Data only through qe.gateway.load.
Stages:  --stage is      IS sessions (information), Gate-2 precondition on IS (information), IS tercile bounds of |m|,
                         leak harness (truncation + perturbation; a planted look-ahead must fail)
         --stage dryrun  the complete OOS pipeline on IS data only (2015-01-02..2016-11-11 as the pretend window)
         --stage oos     exactly ONE OOS read: Gate-2 precondition on the OOS sessions FIRST (outcome-free; if it fails the
                         row is reported 'data not fit' and no P&L is computed), then every Gate-v2 number
Usage: python3 quant-edge/research/q0008/q0008.py --stage {is,dryrun,oos}
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research" / "batch1"))
sys.path.insert(0, str(ROOT / "research" / "batch1b"))
sys.path.insert(0, str(HERE))
from qe import stats  # noqa: E402
from qe.engine import harness  # noqa: E402
from qe.qa import pins  # noqa: E402
import gatekit as gk  # noqa: E402
import fxkit as fx  # noqa: E402
import cfdkit as ck  # noqa: E402
import gate1b as g1  # noqa: E402
import ahtfade as af  # noqa: E402

ID = "Q-0008"
DS = "histdata_cfd_1m_HKXHKD"
IS_START, IS_END = "2013-04-08", "2016-11-11"
OOS_START, OOS_END = "2016-11-14", "2024-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"
SUBPERIODS = [("2016-11-14", "2019-06-14", "AHT to 01:00"), ("2019-06-17", "2024-12-31", "AHT to 03:00; vendor file ends near 01:00"),
              ("2023-01-01", "2023-12-31", "2023, Stock Connect holiday trading")]


def precondition(p: ck.Prepared, start, end) -> dict:
    """Outcome-free Gate-2 precondition: first bar of the day session at 09:15 HKT +-2 min in >= 90% of sessions, and the
    16:30-17:15 HKT gap visible (no bar opening 16:31..17:14) in >= 90% of full-day sessions with a bar in 16:00..16:30."""
    sess, half = af.xhkg("2010-01-01", "2025-12-31")
    sess = sess[(sess >= pd.Timestamp(start)) & (sess <= pd.Timestamp(end))]
    ts = p.ts
    first, gap_ok, gap_n = [], 0, 0
    for d in sess:
        a, b = np.searchsorted(ts, af._ns(d, 6 * 60)), np.searchsorted(ts, af._ns(d, 12 * 60))
        if b > a:
            first.append(int(p.minute[a]))
        if d in half:
            continue
        x0, x1 = np.searchsorted(ts, af._ns(d, 16 * 60)), np.searchsorted(ts, af._ns(d, 16 * 60 + 30), side="right")
        if x1 > x0:
            gap_n += 1
            g0, g1_ = np.searchsorted(ts, af._ns(d, 16 * 60 + 31)), np.searchsorted(ts, af._ns(d, 17 * 60 + 14), side="right")
            gap_ok += int(g1_ == g0)
    f = np.array(first)
    vals, cnt = np.unique(f, return_counts=True) if f.size else (np.array([-1]), np.array([0]))
    modal = int(vals[np.argmax(cnt)])
    share = float(((f >= 553) & (f <= 557)).mean()) if f.size else 0.0
    gshare = gap_ok / gap_n if gap_n else 0.0
    return {"sessions": int(len(sess)), "sessions_with_day_bar": int(f.size), "modal_first_bar": ck.hhmm(modal),
            "share_first_bar_0913_0917": share, "gap_sessions": gap_n, "share_gap_visible": gshare,
            "passed": bool(share >= 0.90 and abs(modal - 555) <= 2 and gshare >= 0.90)}


def in_window(t, start, end):
    d = pd.to_datetime(t["day"])
    return t[(d >= pd.Timestamp(start)) & (d <= pd.Timestamp(end))]


def leak_checks(bars_is):
    fr = fx.tag_for_harness(bars_is)
    out = {}
    for name, prm in (("as registered", af.Params()), ("planted look-ahead (must FAIL)", af.Params(leak="plant"))):
        rule = af.FadeRule(prm)
        a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
        b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
        out[name] = {"truncation_passed": a["passed"], "truncation_checked": a["n_checked"], "truncation_violations": len(a["violations"]),
                     "perturbation_passed": b["passed"], "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])}
        print(name, out[name], flush=True)
    return out


def ev_of(p, prm, start, end):
    t = af.session_table(p, prm)
    return t, in_window(af.trades(t), start, end)


def evaluate(p, start, end, bounds, years, heavy=True):
    prm = af.Params()
    t_all, ev = ev_of(p, prm, start, end)
    tw = in_window(t_all, start, end)
    o = g1.core(ev, start, end, years, heavy=heavy, seed=SEED)
    o["status"] = tw["status"].value_counts().to_dict()
    o["n_eligible"] = int(tw["eligible"].sum())
    o["n_sessions"] = len(tw)
    o["exit_how"] = ev["exit_how"].value_counts().to_dict()
    o["share_short"] = float((ev["side"] < 0).mean()) if len(ev) else float("nan")
    o["m_abs_median"] = float(ev["m"].abs().median()) if len(ev) else float("nan")
    o["bp_notional"] = {"gross_signed": float((ev["r"] * ev["side"]).mean() * 1e4), "ret_sd": float(ev["r"].std() * 1e4)}
    o["trades_per_year"] = len(ev) / years
    lo, hi = bounds
    terc = np.where(ev["m"].abs() <= lo, 0, np.where(ev["m"].abs() <= hi, 1, 2))
    tt = ev.assign(tercile=terc).groupby("tercile")["net1"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    o["terciles"], o["terciles_positive"] = tt, int((tt["sum"] > 0).sum())
    sh = round(0.25 * 37)
    o["shift_min"] = sh
    rows = []
    for name, q in [("(as registered)", prm), ("threshold 0.525% (x0.75)", replace(prm, threshold=0.00525)),
                    ("threshold 0.875% (x1.25)", replace(prm, threshold=0.00875)),
                    (f"entry +{sh} min (09:29; hold x0.76, exit fixed)", replace(prm, entry_min=prm.entry_min + sh)),
                    ("entry 09:15 (the -9 min neighbour 09:11 is before the open; earliest feasible, hold x1.14)", replace(prm, entry_min=9 * 60 + 15)),
                    (f"exit -{sh} min (09:48; hold x0.76, entry fixed)", replace(prm, exit_min=prm.exit_min - sh)),
                    (f"exit +{sh} min (10:06; hold x1.24, entry fixed)", replace(prm, exit_min=prm.exit_min + sh))]:
        _, e = ev_of(p, q, start, end)
        rows.append({"variant": name, "trades": len(e), "net1x_total": float(e["net1"].sum()), "net1x_bp_per_trade": float(e["net1"].mean() * 1e4) if len(e) else np.nan,
                     "t_min": g1.ev_stats(e, "net1")["t_min"], "net_positive": bool(e["net1"].sum() > 0)})
    o["neighbourhood"] = pd.DataFrame(rows)
    ex = []
    base_tot = float(ev["net1"].sum())
    for name, q in (("registered", prm), ("entry delayed one minute (09:21)", replace(prm, entry_min=prm.entry_min + 1)),
                    ("entry and exit delayed one minute (09:21 -> 09:58)", replace(prm, entry_min=prm.entry_min + 1, exit_min=prm.exit_min + 1))):
        _, e = ev_of(p, q, start, end)
        ex.append({"variant": name, "trades": len(e), "net1x_total": float(e["net1"].sum()), "t_min": g1.ev_stats(e, "net1")["t_min"],
                   "share_of_base": float(e["net1"].sum() / base_tot) if base_tot > 0 else float("nan")})
    o["execution"] = pd.DataFrame(ex)
    sp = []
    for a, b, lab in SUBPERIODS:
        x = in_window(ev, a, b)
        sp.append({"period": f"{a}..{b} ({lab})", "trades": len(x), "net1x_total": float(x["net1"].sum()),
                   "net1x_bp_per_trade": float(x["net1"].mean() * 1e4) if len(x) else np.nan, "t_min": g1.ev_stats(x, "net1")["t_min"]})
    o["subperiods"] = pd.DataFrame(sp)
    # random entry: each trade keeps its side; its day is drawn from all eligible OOS sessions (same clocks, that day's w)
    pool = tw[tw["eligible"]]
    G = (pool["w"] * pool["r"]).to_numpy(float)
    sides = ev["side"].to_numpy(float)
    rng = np.random.default_rng(SEED)
    null = np.empty(10_000)
    for i in range(0, 10_000, 500):
        D = rng.integers(0, G.size, size=(500, len(ev)))
        null[i:i + 500] = (G[D] * sides[None]).mean(axis=1)
    sg = float(ev["gross"].mean())
    o["random_entry"] = {"n_paths": 10_000, "pool_days": int(G.size), "strategy_gross": sg, "null_mean": float(null.mean()),
                         "null_p95": float(np.quantile(null, 0.95)), "percentile": float((null < sg).mean()), "beats_95": bool((null < sg).mean() >= 0.95)}
    bench = ev["bench"].to_numpy(float)
    obs = float((sides * bench).mean())
    perm = np.array([(rng.permutation(sides) * bench).mean() for _ in range(10_000)])
    o["sign_perm"] = {"n_perm": 10_000, "observed": obs, "p": float((1 + (perm >= obs).sum()) / 10_001)}
    s_ = ev["net1"].to_numpy(float)
    beta = float(np.cov(s_, bench)[0, 1] / bench.var()) if bench.var() > 0 else 0.0
    al = s_ - beta * bench
    o["bh_same"] = {"bh_mean_bp": float(bench.mean() * 1e4), "beta": beta, "alpha_bp": float(al.mean() * 1e4),
                    "alpha_t_min": g1.ev_stats(ev.assign(al=al), "al")["t_min"]}
    scale = len(ev) / max(len(pool), 1)
    bh = g1.daily_series(pool.assign(bh=pool["w"] * pool["r"] * scale), "bh", start, end)
    ss, bb = o["d1"].to_numpy(), bh.to_numpy()
    bet2 = float(np.cov(ss, bb)[0, 1] / bb.var()) if bb.var() > 0 else 0.0
    o["bh_always"] = {"scale": scale, "bh_total": float(bb.sum()), "beta": bet2, "alpha_t_min": gk.t_block(ss - bet2 * bb, 10)["t_min"]}
    o["ev_tab"] = ev
    return o


def write_result(o, isj, pin, pre, cmd, out_path):
    years = o["years"]
    dc = g1.deciding(o)
    neigh_ok = bool(o["neighbourhood"]["net_positive"].all())
    delay_share = float(o["execution"].iloc[1]["share_of_base"])
    c7 = bool(o["years_summary"]["passed"] and o["terciles_positive"] >= 2 and neigh_ok and delay_share >= 0.5)
    v = gk.verdict(dc["t_dec"], dc["lb"], dc["p5"], dc["net2_mean"], dc["t2"], c7, "row: near-miss = t >= 2.0 with criterion 3 passed")
    L = []
    A = L.append
    A("# Q-0008 — HSI after-hours fade on HK50 (FTMO intraday CFD): Gate-v2 OOS result")
    A("")
    A(f"Registry row Q-0008 (registered commit 0a46ddd, count 1, sign fixed: FADE the after-hours move). Script `research/q0008/q0008.py` (rule `research/q0008/ahtfade.py`, plumbing `research/batch1b/cfdkit.py`, `gate1b.py`, `research/batch1/gatekit.py`, `fxkit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap {SEED} (430,000 draws each), random-entry and sign permutation {SEED} (10,000 each), harness {SEED}.")
    A(f"- Data `{pin['dataset']}` sha256: manifest {pin['manifest_sha256']} = row pin {pin['row_sha256']} = recomputed {pin['computed_sha256']} (ok={pin['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END}; OOS {OOS_START}..{OOS_END}; hold-out not read.")
    A("- Costs 1x: 1.5 bp per side on notional (bid-to-bid log returns); 2x: 3.0 bp per side; no swap (flat intraday).")
    A("- Units: P&L as a fraction of account; w = (0.10/sqrt(252))/sigma; 1 bp = 1e-4 of account. One trade per session at most.")
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
    A("`qe.engine.harness` future-truncation and perturbation tests on 30 sampled IS days (seed 0). The planted version also requires the fade to win over 09:20->09:57 (a deliberate look-ahead) and must fail.")
    A("")
    A("Gate-2 precondition (outcome-free; first bar of the day session at 09:15 HKT +-2 min in >= 90% of sessions, modal at 09:15 +-2; 16:30-17:15 HKT gap visible, i.e. no bar opening 16:31..17:14, in >= 90% of full-day sessions with a bar in 16:00..16:30):")
    A("")
    A("| window | sessions | with a day-session bar | modal first bar | share 09:13-09:17 | gap sessions | share gap visible | passed |")
    A("|---|---|---|---|---|---|---|---|")
    for lab, q in (("IS (information)", isj["pre_is"]), ("OOS (deciding)", pre)):
        A(f"| {lab} | {q['sessions']} | {q['sessions_with_day_bar']} | {q['modal_first_bar']} | {q['share_first_bar_0913_0917']:.3f} | {q['gap_sessions']} | {q['share_gap_visible']:.3f} | {gk.fmt(q['passed'])} |")
    A("")
    A("The IS share of visible gaps is low by construction of the exchange schedule, not of the clock: outcome-free IS bar profiles show the vendor's day session ending 16:14 HKT and the after-hours bars starting 17:00 HKT until 2016-07-22 (HKEX's old T-session close 16:15 and AHT open 17:00), and the 16:30-17:15 gap from 2016-07-25 (closing-auction reform): IS 2013-04-08..2016-07-22 share visible 0.004 (793 sessions); 2016-07-25..2016-11-11 share 0.987 (76 sessions), modal first bar 09:15 in both. The precondition is fixed on the OOS sessions (all after the change), as registered.")
    A("")
    A(f"IS (information only; only the |m| tercile bounds are taken from IS): {isj['is_info']}")
    A("")
    A("## Headline (OOS)")
    A("")
    A(f"XHKG sessions in OOS {o['n_sessions']}; status {o['status']}; eligible {o['n_eligible']}; trades {o['n']} on {o['n_days']} days ({o['trades_per_year']:.1f}/yr); share short (fading an up-move) {o['share_short']:.2f}; median |m| of trades {o['m_abs_median']*100:.2f}%; exit types {o['exit_how']}.")
    A("")
    L.extend(g1.lines_series(o, "trade"))
    A("")
    L.extend(g1.lines_headline_bullets(o, "trade"))
    A(f"- Signed return per trade on notional: {o['bp_notional']['gross_signed']:.2f} bp gross; s.d. {o['bp_notional']['ret_sd']:.1f} bp.")
    A("")
    A("## Criterion 3 (2x cost)")
    A("")
    A(f"Net 2x per trade {gk.bp(o['ev']['net2x']['mean'], 2)} bp, t_min {gk.fmt(o['ev']['net2x']['t_min'], 2)} (daily {gk.fmt(o['daily']['net2x']['t_min'], 2)}): **{'passed' if v['criterion_3'] else 'failed'}**.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    re_, sp_, bs, ba = o["random_entry"], o["sign_perm"], o["bh_same"], o["bh_always"]
    A(f"- Random-entry null (10,000 paths; each trade's side kept, its day drawn from the {re_['pool_days']} eligible OOS sessions, triggered or not, same clocks, the drawn day's weight): strategy gross {gk.bp(re_['strategy_gross'], 2)} bp/trade vs null mean {gk.bp(re_['null_mean'], 2)}, p95 {gk.bp(re_['null_p95'], 2)}; percentile {re_['percentile']:.3f}: {'passed' if re_['beats_95'] else 'failed'}.")
    A(f"- Shuffled signal (trade sides permuted across trades, 10,000; N_family = 1): p = {sp_['p']:.4f} (need < 0.05).")
    A(f"- Buy-and-hold (a), long HK50 over the same minutes at the same weights on the trade days: B&H {bs['bh_mean_bp']:.2f} bp/trade, beta {bs['beta']:.3f}, alpha {bs['alpha_bp']:.2f} bp/trade, alpha t_min {gk.fmt(bs['alpha_t_min'], 2)} (need >= 3.6807).")
    A(f"- Buy-and-hold (b), always long 09:20->09:57 every eligible session (row weights, scaled by {ba['scale']:.4f} to the strategy's average exposure): B&H total {ba['bh_total']*100:.2f}%, beta {ba['beta']:.3f}, alpha t_min {gk.fmt(ba['alpha_t_min'], 2)}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    L.extend(g1.lines_years(o))
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["tercile of |m| (0 = small)", "trades", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"tercile of |m| (0 = small)": lambda x: str(int(x)), "trades": lambda x: str(int(x)), "net1x sum": g1.pct, "net1x mean": lambda x: gk.bp(x, 2) + " bp"}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; IS bounds of |m| over IS trades: {isj['bounds'][0]*100:.3f}% / {isj['bounds'][1]*100:.3f}%).")
    b20 = o["best20"]
    A("")
    A(f"Best-20-days: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A(f"Neighbourhood (hold 37 min; +-25% = {o['shift_min']} min; threshold x0.75 / x1.25; run once on OOS, never changes the headline):")
    A("")
    A(gk.md_table(o["neighbourhood"], {"net1x_total": g1.pct, "net1x_bp_per_trade": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "trades": lambda x: str(int(x)), "net_positive": gk.fmt}))
    A("")
    A("Execution variants (one-minute delay: criterion 7):")
    A("")
    A(gk.md_table(o["execution"], {"net1x_total": g1.pct, "t_min": lambda x: gk.fmt(x, 2), "share_of_base": lambda x: gk.fmt(x, 2), "trades": lambda x: str(int(x))}))
    A("")
    A(f"Criterion 7 overall: **{'passed' if c7 else 'failed'}**.")
    A("")
    A("Sub-periods (institutional change dates in the row; information only):")
    A("")
    A(gk.md_table(o["subperiods"], {"net1x_total": g1.pct, "net1x_bp_per_trade": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "trades": lambda x: str(int(x))}))
    A("")
    A("## Criteria 2 and 12 (process)")
    A("")
    A(f"- Criterion 2: OOS {years:.1f} years incl. 2020 and 2022; {o['n']} trades on {o['n_days']} distinct days (need >= 300 trades on >= 150 days): **{'met' if (o['n'] >= 300 and o['n_days'] >= 150) else 'not met'}**.")
    A("- Criterion 5: single configuration; CSCV n/a. Criterion 11 (prop-fit) belongs to Department F.")
    A("- FTMO funded +-2 min news rule: entry 09:20 and exit 09:57 HKT are outside +-2 min of 09:30 NBS PMI, 09:45 Caixin PMI and 10:00 NBS releases by construction (as registered); no calendar filter needed.")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(dc['t_dec'], 2)} vs 3.6807, bootstrap lower bound {'> 0' if dc['lb'] > 0 else '<= 0'}: **{'passed' if v['criterion_4'] else 'failed'}**. (2) criterion 3: **{'passed' if v['criterion_3'] else 'failed'}**. (3) criterion 7: **{'passed' if c7 else 'failed'}**. (4)-(5): not reached.")
    A(f"- Near-miss by the row's definition (t >= 2.0 with criterion 3 passed): {gk.fmt(v['near_miss_row_def'])}; by the batch brief's (t within 1.0 of the bar with p5 > 0): {gk.fmt(v['near_miss_brief_def'])}.")
    A(f"- **Verdict: {v['verdict']}.** Read against the power above; a failure is not evidence of absence.")
    A("")
    A("## Disclosures and implementation notes (fixed before the OOS read)")
    A("")
    A("- Eligible session (sigma history and null pool) = d passes the day definition, C(p) exists, A(d) exists with >= 60 bars and the 09:20 bar exists; sigma = pandas ewm(com 60, min_periods 40).std() of those sessions' 09:20->09:57 log returns, read at the last eligible session before d (the row's 'eligible' would otherwise be circular).")
    A("- Half days from exchange_calendars XHKG early_closes; the previous session p is the previous XHKG session (gap <= 5 calendar days).")
    A("- Last-resort exit (no bar at all in 09:50..09:59): close of the last bar in [entry, 09:56], counted as 'lastbar'. Shifted clocks keep the same fallback shape.")
    A("- The -9 min entry neighbour (09:11) lies before the 09:15 day-session open; the earliest feasible entry (09:15) is run in its place, fixed before the read.")
    A("- The vendor file carries no AHT volume; the Red-Team objection (stale / indicative after-hours quotes) is answered here only by the Gate-2 precondition; Dept C's cross-check against HKEX daily AHT summaries is not part of this run.")
    Path(out_path).write_text("\n".join(L) + "\n")
    summ = {"id": ID, "net1x_bp_per_trade": o["ev"]["net1x"]["mean"] * 1e4, "t_min": dc["t_dec"], "boot_lower_trade_bp": o["boot_ev"]["lower_alpha"] * 1e4,
            "boot_lower_daily_bp": o["boot_daily"]["lower_alpha"] * 1e4, "t2x": dc["t2"], "verdict": v["verdict"]}
    print(json.dumps(summ, indent=1), flush=True)
    return summ


def write_not_fit(isj, pin, pre, cmd, out_path):
    L = ["# Q-0008 — HSI after-hours fade on HK50: data not fit (Gate-2 precondition failed)", "",
         f"Registry row Q-0008 (registered 0a46ddd). Script `research/q0008/q0008.py`. Command `{cmd}`. Data `{pin['dataset']}` sha256 recomputed {pin['computed_sha256']} (ok={pin['ok']}).", "",
         "The row fixes an outcome-free precondition on the OOS sessions; it failed, so as registered the row is NOT run and is reported 'data not fit', not 'refuted'. No P&L was computed on the OOS window.", "",
         "| window | sessions | with a day-session bar | modal first bar | share 09:13-09:17 | gap sessions | share gap visible | passed |", "|---|---|---|---|---|---|---|---|"]
    for lab, q in (("IS (information)", isj["pre_is"]), ("OOS (deciding)", pre)):
        L.append(f"| {lab} | {q['sessions']} | {q['sessions_with_day_bar']} | {q['modal_first_bar']} | {q['share_first_bar_0913_0917']:.3f} | {q['gap_sessions']} | {q['share_gap_visible']:.3f} | {gk.fmt(q['passed'])} |")
    L += ["", "## registry_reads.log lines for this id", "", "```"] + gk.reads_log_lines(ID) + ["```"]
    Path(out_path).write_text("\n".join(L) + "\n")


def main(stage, cmd):
    pin = pins.verify(ID, DS)
    if stage == "is":
        bars = ck.load(ID, DS, "is")
        p = ck.prepare(bars, ck.HK)
        pre_is = precondition(p, IS_START, IS_END)
        print("precondition IS", pre_is, flush=True)
        t = af.session_table(p, af.Params())
        tw = in_window(t, IS_START, IS_END)
        ev = af.trades(tw)
        bounds = (float(ev["m"].abs().quantile(1 / 3)), float(ev["m"].abs().quantile(2 / 3)))
        st = g1.ev_stats(ev, "net1")
        info = (f"{len(tw)} sessions, status {tw['status'].value_counts().to_dict()}, eligible {int(tw['eligible'].sum())}, trades {len(ev)}; "
                f"net 1x {ev['net1'].mean()*1e4:.2f} bp/trade, t {st['t_min']:.2f}")
        print(info, flush=True)
        leak = leak_checks(bars)
        (HERE / "Q-0008_is.json").write_text(json.dumps({"leak": leak, "is_info": info, "bounds": bounds, "pre_is": pre_is}, indent=1, default=str))
        return
    isj = json.loads((HERE / "Q-0008_is.json").read_text())
    bounds = tuple(isj["bounds"])
    if stage == "dryrun":
        bars = ck.load(ID, DS, "is")
        p = ck.prepare(bars, ck.HK)
        a, b = "2015-01-02", IS_END
        pre = precondition(p, a, b)
        yrs = (pd.Timestamp(b) - pd.Timestamp(a)).days / 365.25
        o = evaluate(p, a, b, bounds, yrs)
        write_result(o, isj, pin, pre, cmd, Path(SCRATCH) / "Q-0008.dry.md")
        write_not_fit(isj, pin, pre, cmd, Path(SCRATCH) / "Q-0008.dry-notfit.md")
        return
    bars = ck.load_is_oos(ID, DS)                                    # <- the one OOS read (+ IS history)
    p = ck.prepare(bars, ck.HK)
    pre = precondition(p, OOS_START, OOS_END)
    print("precondition OOS", pre, flush=True)
    out = ROOT / "research" / "results" / "Q-0008.md"
    if not pre["passed"]:
        write_not_fit(isj, pin, pre, cmd, out)
        print("DATA NOT FIT: no P&L computed", flush=True)
        return
    yrs = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    o = evaluate(p, OOS_START, OOS_END, bounds, yrs)
    write_result(o, isj, pin, pre, cmd, out)
    o["ev_tab"].to_csv(HERE / "Q-0008_oos_trades.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    main(a.stage, f"python3 quant-edge/research/q0008/q0008.py --stage {a.stage}")
