#!/usr/bin/env python3
"""Q-0007 cross-index overnight-vs-intraday reversal on seven index CFDs (registered 0a46ddd). Data only through
qe.gateway.load. Stages:
  --stage is      IS days (information), IS tercile bounds (SPX trailing 20-day vol), joint leak harness on all seven
                  instruments (truncation + perturbation at the 09:32 entry instant; as_written, ex_ante, planted leak)
  --stage dryrun  the complete OOS pipeline on IS data only (2013-01-02..2014-12-31 as the pretend window)
  --stage oos     exactly ONE OOS read per dataset (seven) + IS history; every Gate-v2 number
Usage: python3 quant-edge/research/q0007/q0007.py --stage {is,dryrun,oos}
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
from qe.qa import pins  # noqa: E402
import gatekit as gk  # noqa: E402
import cfdkit as ck  # noqa: E402
import gate1b as g1  # noqa: E402
import xsrev as xs  # noqa: E402

ID = "Q-0007"
IS_START, IS_END = "2010-11-15", "2014-12-31"
OOS_START, OOS_END = "2015-01-02", "2024-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"
SUBPERIODS = [("2015-01-02", "2019-12-31", "2015-2019"), ("2020-03-01", "2022-04-30", "2020-03..2022-04"),
              ("2022-05-01", "2024-12-31", "2022-05.. (daily 0DTE)"), ("2020-06-15", "2023-12-01", "GRX hole: universe without GER40")]


def load_all(window_stage: str) -> dict:
    P = {}
    for k in xs.U:
        b = ck.load(ID, xs.DS[k], "is") if window_stage == "is" else ck.load_is_oos(ID, xs.DS[k])   # <- one OOS read each
        P[k] = xs.keep_rule_minutes(ck.prepare(b, ck.NY))
        del b
    return P


def spx_vol(panel) -> pd.Series:
    C = panel["rows"]["SPX"]["C"]
    r = np.log(C).diff()
    return r.rolling(20, min_periods=15).std().shift(1)


def leak_checks(P, panel_by_mode):
    out = {}
    rng0 = np.random.default_rng(SEED)
    for name, prm in (("as_written (registered)", xs.Params()), ("ex_ante (no post-entry coverage test)", xs.Params(coverage="ex_ante")),
                      ("planted look-ahead (must FAIL)", xs.Params(leak="plant"))):
        full = panel_by_mode.get(name) or xs.build(P, prm)
        days = full["trades"]["day"].to_numpy()
        pick = rng0.choice(days, size=min(30, len(days)), replace=False)
        bad_t = bad_p = 0
        rng = np.random.default_rng(SEED + 1)
        for d in pick:
            d = pd.Timestamp(d)
            cut = ck.local_ns(d, prm.entry_min, ck.NY)
            ref = xs.decisions(full, d)
            pt = xs.build({k: P[k].head_until(cut) for k in P}, prm)
            bad_t += int(xs.decisions(pt, d) != ref)
            pp = xs.build({k: P[k].perturbed_after(cut, rng) for k in P}, prm)
            bad_p += int(xs.decisions(pp, d) != ref)
        out[name] = {"truncation_passed": bad_t == 0, "truncation_checked": len(pick), "truncation_violations": bad_t,
                     "perturbation_passed": bad_p == 0, "perturbation_checked": len(pick), "perturbation_violations": bad_p}
        print(name, out[name], flush=True)
    return out


def evaluate(P, start, end, bounds, years, heavy=True):
    prm = xs.Params()
    panel = xs.build(P, prm, start, end)
    ev = panel["trades"]
    o = g1.core(ev, start, end, years, heavy=heavy, seed=SEED)
    if heavy:
        o["boot_stat20"] = gk.bootstrap_daily(o["d1"], 20.0, SEED)
    sess = panel["sess"]
    win = (sess >= pd.Timestamp(start)) & (sess <= pd.Timestamp(end))
    o["n_tdays"] = int((panel["tday"] & win).sum())
    o["elig_by_inst"] = {k: int(panel["elig"][win & panel["tday"], j].sum()) for j, k in enumerate(panel["names"])}
    o["n_elig_dist"] = ev["n_elig"].value_counts().sort_index().to_dict()
    legs = pd.concat([ev[["day"]].assign(net1=ev["legL"], inst=ev["L"], side="long", how=ev["howL"]),
                      ev[["day"]].assign(net1=ev["legS"], inst=ev["S"], side="short", how=ev["howS"])], ignore_index=True)
    o["legs"] = g1.ev_stats(legs, "net1")
    o["n_legs"] = len(legs)
    o["exit_how"] = legs["how"].value_counts().to_dict()
    o["by_inst"] = legs.groupby(["inst", "side"])["net1"].agg(["count", "sum", "mean"]).unstack(fill_value=0)
    pk = ev.apply(lambda r: "/".join(sorted((r["L"], r["S"]))), axis=1)
    pp = ev.assign(pair=pk).groupby("pair")["net1"].agg(["count", "sum", "mean"]).sort_values("sum", ascending=False)
    tot = float(ev["net1"].sum())
    pp["share_of_net"] = pp["sum"] / tot if tot > 0 else np.nan
    o["pairs"] = pp
    o["pair_max_share"] = float(pp["sum"].max() / tot) if tot > 0 else float("nan")
    o["pair_ok"] = bool(tot > 0 and o["pair_max_share"] <= 0.5)
    o["share_zL_neg"] = float((ev["zL"] < 0).mean())
    o["share_zS_pos"] = float((ev["zS"] > 0).mean())
    o["bp_notional"] = {"spread_signed_bp": float((ev["rL"] - ev["rS"]).mean() * 1e4), "spread_sd_bp": float((ev["rL"] - ev["rS"]).std() * 1e4)}
    vol = spx_vol(panel)
    v = vol.reindex(pd.DatetimeIndex(ev["day"])).to_numpy()
    lo, hi = bounds
    terc = np.where(np.isnan(v), -1, np.where(v <= lo, 0, np.where(v <= hi, 1, 2)))
    tt = ev.assign(tercile=terc).groupby("tercile")["net1"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    o["terciles"], o["terciles_positive"], o["terc_missing"] = tt, int((tt["sum"] > 0).sum()), int((terc < 0).sum())
    sh = round(0.25 * (prm.exit_min - prm.entry_min))
    o["shift_min"] = sh
    rows = []
    for name, q in [("(as registered)", prm), (f"entry +{sh} min ({ck.hhmm(prm.entry_min + sh)}; hold x0.75, exit fixed)", replace(prm, entry_min=prm.entry_min + sh)),
                    (f"exit -{sh} min ({ck.hhmm(prm.exit_min - sh)}; hold x0.75, entry fixed)", replace(prm, exit_min=prm.exit_min - sh)),
                    ("EWMA com 45 (x0.75; z and sigma)", replace(prm, com=45.0)), ("EWMA com 75 (x1.25; z and sigma)", replace(prm, com=75.0))]:
        e = ev if q == prm else xs.build(P, q, start, end)["trades"]
        rows.append({"variant": name, "days": len(e), "net1x_total": float(e["net1"].sum()), "net1x_bp_per_day": float(e["net1"].mean() * 1e4),
                     "t_min": g1.ev_stats(e, "net1")["t_min"], "net_positive": bool(e["net1"].sum() > 0)})
    o["neighbourhood"] = pd.DataFrame(rows)
    ex = []
    base_tot = tot
    for name, q in (("registered", prm), ("entry delayed one minute (09:33)", replace(prm, entry_min=prm.entry_min + 1)),
                    ("entry and exit delayed one minute (09:33 -> 15:56)", replace(prm, entry_min=prm.entry_min + 1, exit_min=prm.exit_min + 1)),
                    ("ex-ante (no 300-of-384 coverage test)", replace(prm, coverage="ex_ante"))):
        e = ev if q == prm else xs.build(P, q, start, end)["trades"]
        ex.append({"variant": name, "days": len(e), "net1x_total": float(e["net1"].sum()), "t_min": g1.ev_stats(e, "net1")["t_min"],
                   "share_of_base": float(e["net1"].sum() / base_tot) if base_tot > 0 else float("nan")})
    o["execution"] = pd.DataFrame(ex)
    sp = []
    for a, b, lab in SUBPERIODS:
        x = ev[(ev["day"] >= pd.Timestamp(a)) & (ev["day"] <= pd.Timestamp(b))]
        sp.append({"period": f"{a}..{b} ({lab})", "days": len(x), "net1x_total": float(x["net1"].sum()),
                   "net1x_bp_per_day": float(x["net1"].mean() * 1e4) if len(x) else np.nan, "t_min": g1.ev_stats(x, "net1")["t_min"]})
    for y0, y1 in ((2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)):
        pass
    o["subperiods"] = pd.DataFrame(sp)
    # nulls
    idx = np.searchsorted(sess, pd.DatetimeIndex(ev["day"]))
    W, R, E_ = panel["w"], panel["R"], panel["elig"]
    rng = np.random.default_rng(SEED)
    null = np.zeros(10_000)
    for i in idx:
        e = np.nonzero(E_[i])[0]
        a = rng.integers(0, e.size, 10_000)
        b = (a + rng.integers(1, e.size, 10_000)) % e.size
        g = W[i] * R[i]
        null += g[e[a]] - g[e[b]]
    null /= len(idx)
    sg = float(ev["gross"].mean())
    o["random_pair"] = {"n_paths": 10_000, "strategy_gross": sg, "null_mean": float(null.mean()), "null_p95": float(np.quantile(null, 0.95)),
                        "percentile": float((null < sg).mean()), "beats_95": bool((null < sg).mean() >= 0.95)}
    gr = ev["gross"].to_numpy(float)
    perm = np.empty(10_000)
    for i in range(0, 10_000, 1000):
        sg_ = rng.choice([-1.0, 1.0], size=(1000, gr.size))
        perm[i:i + 1000] = (sg_ * gr[None]).mean(axis=1)
    o["sign_perm"] = {"n_perm": 10_000, "observed": sg, "p": float((1 + (perm >= sg).sum()) / 10_001)}
    s_, bench = ev["net1"].to_numpy(float), ev["bench"].to_numpy(float)
    beta = float(np.cov(s_, bench)[0, 1] / bench.var()) if bench.var() > 0 else 0.0
    al = s_ - beta * bench
    o["bh_same"] = {"bh_mean_bp": float(bench.mean() * 1e4), "beta": beta, "alpha_bp": float(al.mean() * 1e4),
                    "alpha_t_min": g1.ev_stats(ev.assign(al=al), "al")["t_min"]}
    j = panel["names"].index("SPX")
    ok = win & panel["tday"] & np.isfinite(W[:, j]) & np.isfinite(R[:, j])
    expo = float((ev["wL"] + ev["wS"]).sum() / max(len(pd.bdate_range(start, end)), 1))
    spx = pd.DataFrame({"day": sess[ok], "bh": W[ok, j] * R[ok, j]})
    scale = expo / float(W[ok, j].sum() / max(len(pd.bdate_range(start, end)), 1)) if ok.any() else 0.0
    bh = g1.daily_series(spx.assign(bh=spx["bh"] * scale), "bh", start, end)
    ss, bb = o["d1"].to_numpy(), bh.to_numpy()
    bet2 = float(np.cov(ss, bb)[0, 1] / bb.var()) if bb.var() > 0 else 0.0
    o["bh_always"] = {"scale": scale, "bh_total": float(bb.sum()), "beta": bet2, "alpha_t_min": gk.t_block(ss - bet2 * bb, 10)["t_min"]}
    o["ev_tab"] = ev
    return o


def write_result(o, isj, pinres, cmd, out_path):
    years = o["years"]
    dc = g1.deciding(o)
    lb_all = min(dc["lb"], o["boot_stat20"]["lower_alpha"])
    p5_all = min(dc["p5"], o["boot_stat20"]["p5"])
    neigh_ok = bool(o["neighbourhood"]["net_positive"].all())
    delay_share = float(o["execution"].iloc[1]["share_of_base"])
    c7 = bool(o["years_summary"]["passed"] and o["terciles_positive"] >= 2 and neigh_ok and delay_share >= 0.5 and o["pair_ok"])
    v = gk.verdict(dc["t_dec"], lb_all, p5_all, dc["net2_mean"], dc["t2"], c7, "row: near-miss = t >= 2.0 with criterion 3 passed")
    L = []
    A = L.append
    A("# Q-0007 — cross-index overnight-vs-intraday reversal on seven index CFDs: Gate-v2 OOS result")
    A("")
    A(f"Registry row Q-0007 (registered commit 0a46ddd, count 1, sign fixed: LONG the most negative standardised overnight return, SHORT the most positive). Script `research/q0007/q0007.py` (rule `research/q0007/xsrev.py`, plumbing `research/batch1b/cfdkit.py`, `gate1b.py`, `research/batch1/gatekit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap {SEED} (430,000 draws each), random-pair null and sign permutation {SEED} (10,000 each), harness {SEED}.")
    for r in pinres:
        A(f"- Data `{r['dataset']}` sha256: manifest {r['manifest_sha256']} = row pin {r['row_sha256']} = recomputed {r['computed_sha256']} (ok={r['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END}; OOS {OOS_START}..{OOS_END}; hold-out not read. Usable spans per data/qa: GRX excluded 2020-06-15..2023-12-01 (Euro Stoxx 50 levels in the file), ETX ends 2018-12-14; HKX excluded by construction.")
    A("- Costs 1x per side on each leg's notional (bid-to-bid log returns): SPX 1.0, NSX 1.0, UKX 1.0, FRX 1.0, GRX 0.8, ETX 1.5, JPX 1.5 bp; 2x doubled; no swap (flat intraday). Returns in each index's own currency (FX translation ignored, as registered).")
    A("- Units: P&L as a fraction of account; w_i = (0.10/sqrt(252))/sigma_i per leg; 1 bp = 1e-4 of account. One long and one short leg per traded day.")
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
    A("Joint harness (the `qe.engine.harness` logic applied to all seven instruments at once, since the signal is cross-sectional): for 30 sampled IS trade days, every bar of every instrument after the 09:32 NY entry instant of day d is deleted (truncation) or multiplied by 1% noise (perturbation); day d's decision (traded?, long leg, short leg, both weights) must not change. The registered 300-of-384 coverage test reads bar availability after the entry, so truncation fails it by construction (a data-availability look-ahead, not a price look-ahead; perturbation passes); the ex-ante version passes both and its OOS numbers are printed (criterion 8: the worse is reported). The planted version reads the signal price at 15:55 of d and must fail.")
    A("")
    A("QA (outcome-free, data/qa/*.md): every dataset PASS or PASS with caveats; clocks histdata_rule (UKX 'conflict' on the US anchor, PASS on the London anchor); cross-source checks vs daily_assets GLSTOCK are in the QA files (GRX lag-0 corr 0.897).")
    A("")
    A(f"IS (information only; only the SPX tercile bounds are taken from IS): {isj['is_info']}")
    A("")
    A("## Headline (OOS)")
    A("")
    A(f"Trading days (full XNYS sessions, previous session full) in OOS {o['n_tdays']}; traded days {o['n']} (universe size on traded days {o['n_elig_dist']}); eligible days per instrument {o['elig_by_inst']}; legs {o['n_legs']}; share of days with z_L < 0 {o['share_zL_neg']:.2f}, z_S > 0 {o['share_zS_pos']:.2f}; leg exit types {o['exit_how']}.")
    A("")
    L.extend(g1.lines_series(o, "day"))
    lg = o["legs"]
    A(f"| leg-level net1x (2 per day, clustered by day) | {lg['n']} | {gk.bp(lg['mean'], 2)} | {gk.fmt(lg['t_iid'], 2)} | {gk.fmt(lg['t_nw10'], 2)} | {gk.fmt(lg['t_cluster'], 2)} | {gk.fmt(lg['t_min'], 2)} |")
    A("")
    L.extend(g1.lines_headline_bullets(o, "day"))
    A(f"- Stationary bootstrap of the daily net 1x (mean block 20 days, 430,000 draws, as the row names it): lower bound {gk.bp(o['boot_stat20']['lower_alpha'], 3)} bp/day, p5 {gk.bp(o['boot_stat20']['p5'], 3)}. Deciding lower bound = min of the three = {gk.bp(lb_all, 3)} bp.")
    A(f"- Long-minus-short return spread on notional (unweighted): {o['bp_notional']['spread_signed_bp']:.2f} bp per day; s.d. {o['bp_notional']['spread_sd_bp']:.1f} bp.")
    A("")
    bi = o["by_inst"]
    bi.columns = [f"{a}_{b}" for a, b in bi.columns]
    bi = bi.reset_index()
    A("Legs by instrument (count, net1x sum, mean):")
    A("")
    A(gk.md_table(bi, {c: ((lambda x: str(int(x))) if c.startswith("count") else (g1.pct if c.startswith("sum") else (lambda x: gk.bp(x, 2) + " bp"))) for c in bi.columns if c != "inst"}))
    A("")
    A("## Criterion 3 (2x cost)")
    A("")
    A(f"Net 2x per day {gk.bp(o['ev']['net2x']['mean'], 2)} bp, t_min {gk.fmt(o['ev']['net2x']['t_min'], 2)} (daily {gk.fmt(o['daily']['net2x']['t_min'], 2)}): **{'passed' if v['criterion_3'] else 'failed'}**.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    rp, sp_, bs, ba = o["random_pair"], o["sign_perm"], o["bh_same"], o["bh_always"]
    A(f"- Random-pair null (10,000 paths; on every traded day the long and the short leg are drawn at random, distinct, from that day's eligible instruments, same clocks and weights): strategy gross {gk.bp(rp['strategy_gross'], 2)} bp/day vs null mean {gk.bp(rp['null_mean'], 2)}, p95 {gk.bp(rp['null_p95'], 2)}; percentile {rp['percentile']:.3f}: {'passed' if rp['beats_95'] else 'failed'}.")
    A(f"- Shuffled signal (each day's long/short assignment flipped at random, 10,000; N_family = 1): p = {sp_['p']:.4f} (need < 0.05).")
    A(f"- Buy-and-hold (a), the equal-risk long basket of the day's eligible instruments over the same minutes: B&H {bs['bh_mean_bp']:.2f} bp/day, beta {bs['beta']:.3f}, alpha {bs['alpha_bp']:.2f} bp/day, alpha t_min {gk.fmt(bs['alpha_t_min'], 2)} (need >= 3.6807).")
    A(f"- Buy-and-hold (b), always long SPX 09:32->15:55 at its row weight, scaled by {ba['scale']:.3f} to the strategy's average gross exposure: B&H total {ba['bh_total']*100:.2f}%, beta {ba['beta']:.3f}, alpha t_min {gk.fmt(ba['alpha_t_min'], 2)}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    L.extend(g1.lines_years(o, "days"))
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["SPX vol tercile (0 = low)", "days", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"SPX vol tercile (0 = low)": lambda x: str(int(x)), "days": lambda x: str(int(x)), "net1x sum": g1.pct, "net1x mean": lambda x: gk.bp(x, 2) + " bp"}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; IS bounds of the SPX trailing 20-day s.d. of 15:55-to-15:55 log returns: {isj['bounds'][0]*100:.3f}% / {isj['bounds'][1]*100:.3f}%; days without a value {o['terc_missing']}).")
    A("")
    pp = o["pairs"].reset_index()
    A(f"Instrument-pair concentration (unordered pair; need no pair > 50% of a positive net): max share {gk.fmt(o['pair_max_share'], 2)}: **{'passed' if o['pair_ok'] else 'failed'}**.")
    A("")
    A(gk.md_table(pp, {"count": lambda x: str(int(x)), "sum": g1.pct, "mean": lambda x: gk.bp(x, 2) + " bp", "share_of_net": lambda x: gk.fmt(x, 2)}))
    b20 = o["best20"]
    A("")
    A(f"Best-20-days: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A(f"Neighbourhood (hold 383 min; +-25% = {o['shift_min']} min; EWMA centre of mass x0.75 / x1.25; run once on OOS, never changes the headline). The two x1.25-hold neighbours do not exist inside the row's own constraints: the entry cannot precede the 09:31 signal price and the exit cannot pass the flat-before-16:00 rule (FRX/ETX bars end 15:59 NY); fixed before the read:")
    A("")
    A(gk.md_table(o["neighbourhood"], {"net1x_total": g1.pct, "net1x_bp_per_day": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "days": lambda x: str(int(x)), "net_positive": gk.fmt}))
    A("")
    A("Execution variants (one-minute delay: criterion 7; as-written vs ex-ante: criterion 8):")
    A("")
    A(gk.md_table(o["execution"], {"net1x_total": g1.pct, "t_min": lambda x: gk.fmt(x, 2), "share_of_base": lambda x: gk.fmt(x, 2), "days": lambda x: str(int(x))}))
    A("")
    A(f"Criterion 7 overall: **{'passed' if c7 else 'failed'}**.")
    A("")
    A("Sub-periods (institutional change dates in the row; information only):")
    A("")
    A(gk.md_table(o["subperiods"], {"net1x_total": g1.pct, "net1x_bp_per_day": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "days": lambda x: str(int(x))}))
    A("")
    A("## Criteria 2 and 12 (process)")
    A("")
    A(f"- Criterion 2: OOS {years:.1f} years incl. 2020 and 2022; {o['n_legs']} leg round trips on {o['n']} distinct days (need >= 300 trades on >= 150 days): **{'met' if (o['n_legs'] >= 300 and o['n'] >= 150) else 'not met'}**.")
    A("- Criterion 5: single configuration; CSCV n/a. Criterion 11 (prop-fit) belongs to Department F.")
    A("- FTMO news rule: entry 09:32 and exit 15:55 ET are clear of the 08:30 and 10:00 ET releases (as registered); no calendar filter applied.")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(dc['t_dec'], 2)} vs 3.6807, bootstrap lower bound {'> 0' if lb_all > 0 else '<= 0'}: **{'passed' if v['criterion_4'] else 'failed'}**. (2) criterion 3: **{'passed' if v['criterion_3'] else 'failed'}**. (3) criterion 7: **{'passed' if c7 else 'failed'}**. (4)-(5): not reached.")
    A(f"- Near-miss by the row's definition (t >= 2.0 with criterion 3 passed): {gk.fmt(v['near_miss_row_def'])}; by the batch brief's (t within 1.0 of the bar with p5 > 0): {gk.fmt(v['near_miss_brief_def'])}.")
    A(f"- **Verdict: {v['verdict']}.** Read against the power above; a failure is not evidence of absence.")
    A("")
    A("## Disclosures and implementation notes (fixed before the OOS read)")
    A("")
    A("- EWMA histories run over each instrument's own valid trading days (s: CO exists inside the span; sigma: the 09:32 bar exists inside the span); s^2 = ewm(com 60, min_periods 40).mean() of CO^2, sigma = ewm(com 60, min_periods 40).std(), both read at the previous valid day; sigma must exist for eligibility. The row's 'eligible days' would otherwise be circular.")
    A("- Last-resort exit (no bar in 15:45..15:58): close of the last bar in [entry, 15:44], counted as 'lastbar'. Shifted clocks keep the fallback shape (exit+1..+3, else close of the last bar in exit-10..exit-1).")
    A("- Only bars with NY minute 09:31..15:58 are kept after loading (the rule reads nothing else); trading days and early closes from exchange_calendars XNYS.")
    A("- B&H (a) is the equal-risk long basket (mean of w_i r_i over the day's eligible instruments); the pair is not beta-hedged, as registered.")
    Path(out_path).write_text("\n".join(L) + "\n")
    summ = {"id": ID, "net1x_bp_per_day": o["ev"]["net1x"]["mean"] * 1e4, "t_min": dc["t_dec"], "boot_lower_bp": lb_all * 1e4, "t2x": dc["t2"], "verdict": v["verdict"]}
    print(json.dumps(summ, indent=1), flush=True)
    return summ


def main(stage, cmd):
    pinres = [pins.verify(ID, xs.DS[k]) for k in xs.U]
    if stage == "is":
        P = load_all("is")
        panel = xs.build(P, xs.Params())
        ev = panel["trades"]
        ev = ev[(ev["day"] >= pd.Timestamp(IS_START)) & (ev["day"] <= pd.Timestamp(IS_END))]
        vol = spx_vol(panel)
        sess = panel["sess"]
        isd = (sess >= pd.Timestamp(IS_START)) & (sess <= pd.Timestamp(IS_END)) & panel["tday"]
        vv = vol[isd].dropna()
        bounds = (float(vv.quantile(1 / 3)), float(vv.quantile(2 / 3)))
        st = g1.ev_stats(ev, "net1")
        info = (f"{int(isd.sum())} trading days, {len(ev)} traded (universe {ev['n_elig'].value_counts().sort_index().to_dict()}); "
                f"net 1x {ev['net1'].mean()*1e4:.2f} bp/day, t {st['t_min']:.2f}")
        print(info, bounds, flush=True)
        leak = leak_checks(P, {"as_written (registered)": panel})
        (HERE / "Q-0007_is.json").write_text(json.dumps({"leak": leak, "is_info": info, "bounds": bounds}, indent=1, default=str))
        return
    isj = json.loads((HERE / "Q-0007_is.json").read_text())
    bounds = tuple(isj["bounds"])
    if stage == "dryrun":
        P = load_all("is")
        a, b = "2013-01-02", IS_END
        yrs = (pd.Timestamp(b) - pd.Timestamp(a)).days / 365.25
        o = evaluate(P, a, b, bounds, yrs)
        write_result(o, isj, pinres, cmd, Path(SCRATCH) / "Q-0007.dry.md")
        return
    P = load_all("oos")
    yrs = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    o = evaluate(P, OOS_START, OOS_END, bounds, yrs)
    write_result(o, isj, pinres, cmd, ROOT / "research" / "results" / "Q-0007.md")
    o["ev_tab"].to_csv(HERE / "Q-0007_oos_days.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    main(a.stage, f"python3 quant-edge/research/q0007/q0007.py --stage {a.stage}")
