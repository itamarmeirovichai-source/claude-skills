#!/usr/bin/env python3
"""Q-0011 18:00 ET reopen-overshoot fade on US500/US100/XAUUSD CFDs (registered fd38c6e). Data only through qe.gateway.load.
Stages:  --stage is      IS evenings (information), IS tercile bounds of |M|/s, leak harness per instrument
                         (truncation + perturbation; a planted look-ahead must fail)
         --stage dryrun  the complete OOS pipeline on IS data only (2011-07-01..2012-12-31 as the pretend window)
         --stage oos     exactly ONE OOS read per dataset, then every Gate-v2 number
Usage: python3 quant-edge/research/q0011/q0011.py --stage {is,dryrun,oos}
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
from qe.engine import harness  # noqa: E402
from qe.qa import pins  # noqa: E402
import gatekit as gk  # noqa: E402
import fxkit as fx  # noqa: E402
import cfdkit as ck  # noqa: E402
import gate1b as g1  # noqa: E402
import reopen as ro  # noqa: E402

ID = "Q-0011"
DS = {"SPX": "histdata_cfd_1m_SPXUSD", "NSX": "histdata_cfd_1m_NSXUSD", "XAU": "histdata_cfd_1m_XAUUSD"}
SPIKE_DROP = {"SPX": True, "NSX": True, "XAU": False}       # the row names SPX/NSX spike-reversal prints
IS_START, IS_END = "2010-11-15", "2012-12-31"
OOS_START, OOS_END = "2013-01-01", "2024-12-31"
SEED = 0
SCRATCH = "/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad"
SUBPERIODS = [("2013-01-01", "2018-12-31", "SPX/NSX halt 16:59/17:15 ET"), ("2019-01-01", "2024-12-31", "SPX/NSX halt 16:14 ET")]
FUT = {"SPX": (0.25 + 0.80 / 5.0), "NSX": (0.25 + 0.80 / 2.0), "XAU": (0.10 + 0.80 / 10.0)}   # price points per side


def in_window(t, start, end, col="d"):
    d = pd.to_datetime(t[col])
    return t[(d >= pd.Timestamp(start)) & (d <= pd.Timestamp(end))]


class Book:
    def __init__(self, P):
        self.P = P
        self.spk = {i: ro.spike_flags(p) for i, p in P.items()}
        self.cache = {}

    def tables(self, prm):
        if prm not in self.cache:
            self.cache[prm] = {i: ro.evening_table(p, prm, i) for i, p in self.P.items()}
        return self.cache[prm]

    def ev(self, prm, start, end, cost_bp=ro.COST_BP):
        out = []
        for i, t in self.tables(prm).items():
            out.append(ro.trades(in_window(t, start, end), self.spk[i] if SPIKE_DROP[i] else None, cost_bp))
        e = pd.concat(out, ignore_index=True)
        return e.sort_values(["day", "inst"]).reset_index(drop=True)

    def spike_counts(self, prm, start, end):
        res = {}
        for i, t in self.tables(prm).items():
            x = in_window(t, start, end)
            x = x[x["trig"]]
            s = set(int(k) for k in self.spk[i])
            s1 = set(k + 1 for k in s)
            res[i] = {"flagged_bars_total": len(s), "legs_hit": int(sum((int(a) in s) or (int(b) in s) for a, b in zip(x["entry_i"], x["exit_i"]))),
                      "legs_hit_next_bar_info": int(sum((int(a) in s1) or (int(b) in s1) for a, b in zip(x["entry_i"], x["exit_i"]))),
                      "dropped": bool(SPIKE_DROP[i])}
        return res


def load_all(stage):
    P = {}
    for i, ds in DS.items():
        bars = ck.load(ID, ds, "is") if stage != "oos" else ck.load_is_oos(ID, ds)
        P[i] = ck.prepare(bars, ck.NY)
        if stage == "is":
            P[i + "_bars"] = bars
    return P


def leak_checks(P):
    out = {}
    for name, leak in (("as registered", ""), ("planted look-ahead (must FAIL)", "plant")):
        for i in DS:
            fr = fx.tag_for_harness(P[i + "_bars"])
            rule = ro.FadeRule(ro.Params(leak=leak), i)
            a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
            b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
            out[f"{name} [{i}]"] = {"truncation_passed": a["passed"], "truncation_checked": a["n_checked"], "truncation_violations": len(a["violations"]),
                                    "perturbation_passed": b["passed"], "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])}
            print(name, i, out[f"{name} [{i}]"], flush=True)
    return out


def tstats(x):
    x = np.asarray(x, float)
    if x.size < 3:
        return {"n": int(x.size), "mean": float(np.nanmean(x)) if x.size else np.nan, "t_iid": np.nan, "t_nw": np.nan, "t_min": np.nan}
    tb = gk.t_block(x, 10)
    return {"n": int(x.size), "mean": float(x.mean()), **tb}


def evaluate(B, start, end, bounds, years, heavy=True):
    prm = ro.Params()
    ev = B.ev(prm, start, end)
    o = g1.core(ev, start, end, years, heavy=heavy, seed=SEED)
    if heavy:
        o["boot_stat20"] = gk.bootstrap_daily(o["d1"], 20.0, SEED)
    o["pe"] = {k: tstats(ev.groupby("day")[c].sum().to_numpy()) for k, c in (("gross", "gross"), ("net1x", "net1"), ("net2x", "net2"), ("net3x (info)", "net3"))}
    o["ev3"] = g1.ev_stats(ev, "net3")
    tabs = {i: in_window(t, start, end) for i, t in B.tables(prm).items()}
    o["status"] = {i: t["status"].value_counts().to_dict() for i, t in tabs.items()}
    o["n_elig"] = {i: int((t["eligible"]).sum()) for i, t in tabs.items()}
    o["n_elig_ftmo"] = {i: int((t["eligible"] & t["ftmo_ok"]).sum()) for i, t in tabs.items()}
    o["n_trig"] = {i: int(t["trig"].sum()) for i, t in tabs.items()}
    o["spikes"] = B.spike_counts(prm, start, end)
    o["exit_how"] = ev["exit_how"].value_counts().to_dict()
    o["share_short"] = float((ev["side"] < 0).mean())
    o["bp_notional"] = {"gross_signed": float((ev["r"] * ev["side"]).mean() * 1e4), "ret_sd": float(ev["r"].std() * 1e4),
                        "median_absM_bp": float(ev["M"].abs().median() * 1e4)}
    o["legs_per_year"] = len(ev) / years
    net_tot = float(ev["net1"].sum())
    bi = ev.groupby("inst").agg(legs=("net1", "size"), gross_sum=("gross", "sum"), net1_sum=("net1", "sum"), net1_mean=("net1", "mean"))
    bi["t_min"] = [g1.ev_stats(ev[ev["inst"] == i], "net1")["t_min"] for i in bi.index]
    bi["share_of_net"] = bi["net1_sum"] / net_tot if net_tot > 0 else np.nan
    o["by_inst"] = bi.reset_index()
    bs = ev.groupby("sunday").agg(legs=("net1", "size"), gross_sum=("gross", "sum"), net1_sum=("net1", "sum"), net1_mean=("net1", "mean"))
    bs["t_min"] = [g1.ev_stats(ev[ev["sunday"] == s], "net1")["t_min"] for s in bs.index]
    bs["share_of_net"] = bs["net1_sum"] / net_tot if net_tot > 0 else np.nan
    o["by_sunday"] = bs.reset_index().assign(sunday=lambda x: x["sunday"].map({True: "Sunday (weekend reopen)", False: "Mon-Thu (daily reopen)"}))
    conc_inst = float(bi["share_of_net"].max()) if net_tot > 0 else np.nan
    conc_sun = float(bs.set_index("sunday").get("share_of_net", pd.Series(dtype=float)).get(True, np.nan)) if net_tot > 0 else np.nan
    o["conc"] = {"max_inst_share": conc_inst, "sunday_share": conc_sun,
                 "passed": bool(net_tot > 0 and conc_inst <= 0.5 and (np.isnan(conc_sun) or conc_sun <= 0.5))}
    lo, hi = bounds
    az = ev["z"].abs()
    terc = np.where(az <= lo, 0, np.where(az <= hi, 1, 2))
    tt = ev.assign(tercile=terc).groupby("tercile")["net1"].agg(["count", "sum", "mean"]).reindex([0, 1, 2]).fillna(0.0)
    o["terciles"], o["terciles_positive"] = tt, int((tt["sum"] > 0).sum())
    sh = 20
    rows = []
    for name, q in [("(as registered)", prm), ("trigger 1.125 s (x0.75)", replace(prm, k=1.125)), ("trigger 1.875 s (x1.25)", replace(prm, k=1.875)),
                    (f"entry +{sh} min (18:31; exit fixed)", replace(prm, entry_min=prm.entry_min + sh)),
                    ("entry 18:10 (the -20 min neighbour 17:51 is inside the halt; earliest bar after the signal)", replace(prm, entry_min=18 * 60 + 10)),
                    (f"exit -{sh} min (19:10)", replace(prm, exit_min=prm.exit_min - sh)), (f"exit +{sh} min (19:50)", replace(prm, exit_min=prm.exit_min + sh)),
                    ("EWMA com 45 (x0.75)", replace(prm, com=45.0)), ("EWMA com 75 (x1.25)", replace(prm, com=75.0))]:
        e = B.ev(q, start, end)
        rows.append({"variant": name, "legs": len(e), "net1x_total": float(e["net1"].sum()), "net1x_bp_per_leg": float(e["net1"].mean() * 1e4) if len(e) else np.nan,
                     "t_min": g1.ev_stats(e, "net1")["t_min"], "net_positive": bool(e["net1"].sum() > 0)})
    o["neighbourhood"] = pd.DataFrame(rows)
    ex = []
    for name, q in (("registered", prm), ("entry delayed one bar (18:12)", replace(prm, entry_min=prm.entry_min + 1)),
                    ("entry and exit delayed one bar (18:12 -> 19:31)", replace(prm, entry_min=prm.entry_min + 1, exit_min=prm.exit_min + 1))):
        e = B.ev(q, start, end)
        ex.append({"variant": name, "legs": len(e), "net1x_total": float(e["net1"].sum()), "t_min": g1.ev_stats(e, "net1")["t_min"],
                   "share_of_base": float(e["net1"].sum() / net_tot) if net_tot > 0 else float("nan")})
    o["execution"] = pd.DataFrame(ex)
    sp = []
    for a, b, lab in SUBPERIODS:
        x = in_window(ev, a, b)
        sp.append({"period": f"{a}..{b} ({lab})", "legs": len(x), "net1x_total": float(x["net1"].sum()),
                   "net1x_bp_per_leg": float(x["net1"].mean() * 1e4) if len(x) else np.nan, "t_min": g1.ev_stats(x, "net1")["t_min"]})
    o["subperiods"] = pd.DataFrame(sp)
    # futures-venue cost sensitivity (no count): MES/MNQ 0.25 pt + $0.80, MGC 1 tick + $0.80 per side, on the CFD returns
    fc = ev["inst"].map(FUT) / ev["entry"]
    fnet = ev["gross"] - ev["w"] * 2 * fc
    o["fut"] = {"cost_bp_per_side_median": {i: float((fc[ev["inst"] == i]).median() * 1e4) for i in DS},
                "net_mean_bp": float(fnet.mean() * 1e4), "t_min": g1.ev_stats(ev.assign(f=fnet), "f")["t_min"]}
    # criterion 6 nulls
    rng = np.random.default_rng(SEED)
    null = np.zeros(10_000)
    for i in DS:
        pool = tabs[i][tabs[i]["eligible"] & tabs[i]["ftmo_ok"]]
        G = (pool["w"] * pool["r"]).to_numpy(float)
        sides = ev.loc[ev["inst"] == i, "side"].to_numpy(float)
        if sides.size == 0 or G.size == 0:
            continue
        for k in range(0, 10_000, 500):
            D = rng.integers(0, G.size, size=(500, sides.size))
            null[k:k + 500] += (G[D] * sides[None]).sum(axis=1)
    null /= len(ev)
    sg = float(ev["gross"].mean())
    o["random_entry"] = {"strategy_gross": sg, "null_mean": float(null.mean()), "null_p95": float(np.quantile(null, 0.95)),
                         "percentile": float((null < sg).mean()), "beats_95": bool((null < sg).mean() >= 0.95)}
    sides, bench = ev["side"].to_numpy(float), ev["bench"].to_numpy(float)
    obs = float((sides * bench).mean())
    perm = np.array([(rng.permutation(sides) * bench).mean() for _ in range(10_000)])
    o["sign_perm"] = {"observed": obs, "p": float((1 + (perm >= obs).sum()) / 10_001)}
    s_ = ev["net1"].to_numpy(float)
    beta = float(np.cov(s_, bench)[0, 1] / bench.var()) if bench.var() > 0 else 0.0
    o["bh_same"] = {"bh_mean_bp": float(bench.mean() * 1e4), "beta": beta, "alpha_bp": float((s_ - beta * bench).mean() * 1e4),
                    "alpha_t_min": g1.ev_stats(ev.assign(al=s_ - beta * bench), "al")["t_min"]}
    allp = pd.concat([t[t["eligible"] & t["ftmo_ok"]] for t in tabs.values()], ignore_index=True)
    scale = len(ev) / max(len(allp), 1)
    bh = g1.daily_series(allp.assign(bh=allp["w"] * allp["r"] * scale), "bh", start, end)
    ss, bb = o["d1"].to_numpy(), bh.to_numpy()
    bet2 = float(np.cov(ss, bb)[0, 1] / bb.var()) if bb.var() > 0 else 0.0
    o["bh_always"] = {"scale": scale, "bh_total": float(bb.sum()), "beta": bet2, "alpha_t_min": gk.t_block(ss - bet2 * bb, 10)["t_min"]}
    o["ev_tab"] = ev
    return o


def write_result(o, isj, pinres, cmd, out_path):
    years = o["years"]
    dc = g1.deciding(o)
    t_pe = o["pe"]["net1x"]["t_min"]
    t_dec = float(min(dc["t_dec"], t_pe))
    lb = min(dc["lb"], o["boot_stat20"]["lower_alpha"])
    p5 = min(dc["p5"], o["boot_stat20"]["p5"])
    t2 = float(min(dc["t2"], o["pe"]["net2x"]["t_min"]))
    neigh_ok = bool(o["neighbourhood"]["net_positive"].all())
    delay_share = float(o["execution"].iloc[1]["share_of_base"])
    c7 = bool(o["years_summary"]["passed"] and o["terciles_positive"] >= 2 and neigh_ok and delay_share >= 0.5 and o["conc"]["passed"])
    v = gk.verdict(t_dec, lb, p5, dc["net2_mean"], t2, c7, "row: near-miss not defined; batch definitions printed")
    c3_row = bool(dc["net2_mean"] > 0)
    gate3 = bool(v["criterion_4"] and c3_row and v["criterion_3"] and c7)
    L = []
    A = L.append
    A("# Q-0011 — 18:00 ET reopen-overshoot fade on US500 / US100 / XAUUSD CFDs: Gate-v2 OOS result")
    A("")
    A(f"Registry row Q-0011 (registered commit fd38c6e, stamped 9e23dcc; count 1, sign fixed: FADE the reopen move). Script `research/q0011/q0011.py` (rule `research/q0011/reopen.py`, plumbing `research/batch1b/cfdkit.py`, `gate1b.py`, `research/batch1/gatekit.py`, `fxkit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: bootstrap {SEED} (430,000 draws each), random-entry and sign permutation {SEED} (10,000 each), harness {SEED}.")
    for pin in pinres:
        A(f"- Data `{pin['dataset']}` sha256: manifest {pin['manifest_sha256']} = row pin {pin['row_sha256']} = recomputed {pin['computed_sha256']} (ok={pin['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END}; OOS {OOS_START}..{OOS_END} (evening dates d, NY); hold-out not read.")
    A("- Costs 1x: 1.0 bp per side on notional at entry and exit (bid-to-bid log returns); 2x: 2.0 bp; 3x (information, reopen spread sensitivity): 3.0 bp; no swap (entry after the FTMO 00:00 Prague rollover, exit the same FTMO day).")
    A("- Units: P&L as a fraction of account; w_i = (0.10/sqrt(252))/sigma_i per leg; 1 bp = 1e-4 of account. 0-3 legs per evening; the series' day is the FTMO (Prague) date d+1, so Sunday evenings land on Monday.")
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
    A("| rule version [instrument] | truncation passed | days | violations | perturbation passed | days | violations |")
    A("|---|---|---|---|---|---|---|")
    for k, r in isj["leak"].items():
        A(f"| {k} | {gk.fmt(r['truncation_passed'])} | {r['truncation_checked']} | {r['truncation_violations']} | {gk.fmt(r['perturbation_passed'])} | {r['perturbation_checked']} | {r['perturbation_violations']} |")
    A("")
    A("`qe.engine.harness` future-truncation and perturbation tests on 30 sampled IS trade days per instrument (seed 0; trading day = NY date + 6 h, so the 18:00 reopen belongs to the next day). The planted version also requires the fade to win over 18:11->19:30 (a deliberate look-ahead) and must fail.")
    A("")
    A("QA (outcome-free, data/qa/*.md): SPXUSD, NSXUSD, XAUUSD clock histdata_rule (single); SPX/NSX daily halt 16:59/17:15 ET to 2018, 16:14 ET from 2019 (sub-periods below); 2017-02-17..02-26 outage absent. Spike-reversal prints (QA definition, `qe.qa.histdata_qa.outliers`, recomputed on the loaded bars):")
    A("")
    A("| instrument | flagged bars (IS+OOS file) | OOS triggered legs whose entry/exit bar is flagged | legs whose entry/exit bar is the bar after a flag (information) | dropped? |")
    A("|---|---|---|---|---|")
    for i, s in o["spikes"].items():
        A(f"| {i} | {s['flagged_bars_total']} | {s['legs_hit']} | {s['legs_hit_next_bar_info']} | {'yes (row)' if s['dropped'] else 'no (row names SPX/NSX only)'} |")
    A("")
    A(f"IS (information only; only the |M|/s tercile bounds are taken from IS): {isj['is_info']}")
    A("")
    A("## Headline (OOS)")
    A("")
    A(f"Evening status by instrument {o['status']}; eligible evenings {o['n_elig']}; eligible and FTMO-day aligned {o['n_elig_ftmo']}; triggered {o['n_trig']}; legs after spike drops {o['n']} on {o['n_days']} evenings ({o['legs_per_year']:.1f} legs/yr); share short (fading an up-move) {o['share_short']:.2f}; median |M| of legs {o['bp_notional']['median_absM_bp']:.1f} bp; exit types {o['exit_how']}.")
    A("")
    L.extend(g1.lines_series(o, "leg"))
    A("")
    A("| per-evening series (legs summed per evening, traded evenings only) | n | mean bp of account | t_iid | t_NW(10) | t_min |")
    A("|---|---|---|---|---|---|")
    for k, d in o["pe"].items():
        A(f"| {k} | {d['n']} | {gk.bp(d['mean'], 2)} | {gk.fmt(d['t_iid'], 2)} | {gk.fmt(d['t_nw'], 2)} | {gk.fmt(d['t_min'], 2)} |")
    A("")
    L.extend(g1.lines_headline_bullets(o, "leg"))
    A(f"- Stationary bootstrap of the daily net 1x (mean block 20 days, 430,000 draws): lower bound {gk.bp(o['boot_stat20']['lower_alpha'], 3)} bp/day, p5 {gk.bp(o['boot_stat20']['p5'], 3)}. Deciding lower bound = min of the three = {gk.bp(lb, 3)} bp; deciding t = min(leg clustered, per-evening, daily) = {gk.fmt(t_dec, 2)} vs 3.6807.")
    A(f"- Signed return per leg on notional: {o['bp_notional']['gross_signed']:.2f} bp gross (vs 2.0 bp round-trip 1x cost); s.d. {o['bp_notional']['ret_sd']:.1f} bp.")
    A("")
    A("By instrument and by evening type (criterion 7 concentration):")
    A("")
    fm = {"gross_sum": g1.pct, "net1_sum": g1.pct, "net1_mean": lambda x: gk.bp(x, 2) + " bp", "t_min": lambda x: gk.fmt(x, 2), "share_of_net": lambda x: gk.fmt(x, 2), "legs": lambda x: str(int(x))}
    A(gk.md_table(o["by_inst"], fm))
    A("")
    A(gk.md_table(o["by_sunday"], fm))
    A("")
    A(f"Concentration (need a positive net with no instrument and not the Sunday evenings > 50% of it): max instrument share {gk.fmt(o['conc']['max_inst_share'], 2)}, Sunday share {gk.fmt(o['conc']['sunday_share'], 2)}: **{'passed' if o['conc']['passed'] else 'failed'}**.")
    A("")
    A("## Criterion 3 (2x cost) and the reopen spread sensitivity")
    A("")
    A(f"- Net 2x per leg {gk.bp(o['ev']['net2x']['mean'], 2)} bp, t_min {gk.fmt(o['ev']['net2x']['t_min'], 2)} (per-evening {gk.fmt(o['pe']['net2x']['t_min'], 2)}, daily {gk.fmt(o['daily']['net2x']['t_min'], 2)}): row criterion (net-2x mean > 0) **{'passed' if c3_row else 'failed'}**; batch convention (mean > 0 and t >= 1.65) **{'passed' if v['criterion_3'] else 'failed'}**.")
    A(f"- 3x (information, no decision; the Red Team's 'honest read'): net 3x per leg {gk.bp(o['ev3']['mean'], 2)} bp, t_min {gk.fmt(o['ev3']['t_min'], 2)}; per-evening {gk.bp(o['pe']['net3x (info)']['mean'], 2)} bp, t_min {gk.fmt(o['pe']['net3x (info)']['t_min'], 2)}.")
    f = o["fut"]
    A(f"- Futures-venue cost sensitivity (no count; MES/MNQ 0.25 pt + $0.80, MGC 1 tick + $0.80 per side, applied to the CFD returns): median cost per side SPX {f['cost_bp_per_side_median']['SPX']:.2f} bp, NSX {f['cost_bp_per_side_median']['NSX']:.2f} bp, XAU {f['cost_bp_per_side_median']['XAU']:.2f} bp; net {f['net_mean_bp']:.2f} bp/leg, t_min {gk.fmt(f['t_min'], 2)}.")
    A("")
    A("## Criterion 6 (nulls)")
    A("")
    re_, sp_, bs, ba = o["random_entry"], o["sign_perm"], o["bh_same"], o["bh_always"]
    A(f"- Random-entry null (10,000 paths; each leg's side kept, its evening drawn from the same instrument's eligible FTMO-aligned OOS evenings, triggered or not, same clocks, the drawn evening's weight): strategy gross {gk.bp(re_['strategy_gross'], 2)} bp/leg vs null mean {gk.bp(re_['null_mean'], 2)}, p95 {gk.bp(re_['null_p95'], 2)}; percentile {re_['percentile']:.3f}: {'passed' if re_['beats_95'] else 'failed'}.")
    A(f"- Shuffled signal (leg sides permuted across legs, 10,000; N_family = 1): p = {sp_['p']:.4f} (need < 0.05).")
    A(f"- Buy-and-hold (a), long the same instrument over the same minutes at the same weights on the leg evenings: B&H {bs['bh_mean_bp']:.2f} bp/leg, beta {bs['beta']:.3f}, alpha {bs['alpha_bp']:.2f} bp/leg, alpha t_min {gk.fmt(bs['alpha_t_min'], 2)} (need >= 3.6807).")
    A(f"- Buy-and-hold (b), always long 18:11->19:30 on every eligible FTMO-aligned evening of all three (row weights, scaled by {ba['scale']:.4f} to the strategy's average exposure): B&H total {ba['bh_total']*100:.2f}%, beta {ba['beta']:.3f}, alpha t_min {gk.fmt(ba['alpha_t_min'], 2)}.")
    A("")
    A("## Criterion 7 (stability)")
    A("")
    L.extend(g1.lines_years(o, "legs"))
    A("")
    tt = o["terciles"].reset_index()
    tt.columns = ["tercile of |M|/s (0 = small)", "legs", "net1x sum", "net1x mean"]
    A(gk.md_table(tt, {"tercile of |M|/s (0 = small)": lambda x: str(int(x)), "legs": lambda x: str(int(x)), "net1x sum": g1.pct, "net1x mean": lambda x: gk.bp(x, 2) + " bp"}))
    A("")
    A(f"Terciles positive {o['terciles_positive']} of 3 (need 2; IS bounds of |M|/s over IS triggered legs: {isj['bounds'][0]:.3f} / {isj['bounds'][1]:.3f}).")
    b20 = o["best20"]
    A("")
    A(f"Best-20-days: the 20 best days hold {b20['net_of_best_k']*100:.2f}% of account; without them net {b20['net_total_after']*100:.2f}%, t_min {gk.fmt(b20['t_min'], 2)}.")
    A("")
    A("Neighbourhood (hold 79 min; +-25% = 20 min; trigger multiple x0.75 / x1.25; EWMA com x0.75 / x1.25 (both s and sigma); run once on OOS, never changes the headline):")
    A("")
    A(gk.md_table(o["neighbourhood"], {"net1x_total": g1.pct, "net1x_bp_per_leg": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "legs": lambda x: str(int(x)), "net_positive": gk.fmt}))
    A("")
    A("Execution variants (one-bar delay: criterion 7):")
    A("")
    A(gk.md_table(o["execution"], {"net1x_total": g1.pct, "t_min": lambda x: gk.fmt(x, 2), "share_of_base": lambda x: gk.fmt(x, 2), "legs": lambda x: str(int(x))}))
    A("")
    A(f"Criterion 7 overall (years, terciles, all neighbours net positive, one-bar delay keeps >= 50%, concentration): **{'passed' if c7 else 'failed'}**.")
    A("")
    A("Sub-periods (information only, not decisive):")
    A("")
    A(gk.md_table(o["subperiods"], {"net1x_total": g1.pct, "net1x_bp_per_leg": lambda x: gk.fmt(x, 2), "t_min": lambda x: gk.fmt(x, 2), "legs": lambda x: str(int(x))}))
    A("")
    A("## Criteria 2, 8 and 12 (process)")
    A("")
    A(f"- Criterion 2: OOS {years:.1f} years incl. 2020 and 2022; {o['n']} legs on {o['n_days']} distinct evenings (need >= 300 trades on >= 150 days): **{'met' if (o['n'] >= 300 and o['n_days'] >= 150) else 'not met'}**.")
    A("- Criterion 8: the worse of every reported variant of the deciding statistic is used (min over leg-clustered, per-evening and daily t; min over three bootstraps); the harness passed before the OOS read.")
    A("- Criterion 12: data only through qe.gateway.load; exactly one OOS read per dataset (log above); hold-out not read; no rule change after the read.")
    A("- Criterion 5: single configuration; CSCV n/a. Criterion 11 (prop-fit) belongs to Department F. FTMO news rule: the Red Team owes the JP release-time check at the 19:30 exit (row note); not run here.")
    A("")
    A("## Verdict (the row's decision rule, applied mechanically)")
    A("")
    A(f"- (1) criterion 4: t {gk.fmt(t_dec, 2)} vs 3.6807, bootstrap lower bound {gk.bp(lb, 3)} bp ({'> 0' if lb > 0 else '<= 0'}): **{'passed' if v['criterion_4'] else 'failed'}**. (2) criterion 3: **{'passed' if c3_row else 'failed'}**. (3) criteria 4/7 stability: **{'passed' if c7 else 'failed'}**. (4)-(5): not reached.")
    A(f"- Near-miss (the row leaves it undefined; batch definitions): t >= 2.0 with criterion 3 passed: {gk.fmt(v['near_miss_row_def'])}; t within 1.0 of the bar with p5 > 0: {gk.fmt(v['near_miss_brief_def'])}.")
    verdict = "PASS Gate 3 (criteria 1-3 of the row's rule; Red Team, re-implementation and hold-out still owed)" if gate3 else v["verdict"]
    A(f"- **Verdict: {verdict}.** Read against the power above; a failure is not evidence of absence.")
    A("")
    A("## Disclosures and implementation notes (fixed before the OOS read)")
    A("")
    A("- 'Previous trading day' = latest XNYS session <= d: Friday (or the last session before it) for Sunday evenings, d itself for Mon-Thu evenings (the pre-halt close of the same futures trading day).")
    A("- Eligible evening for the scale s = passes the evening definition (Sun-Thu, XNYS holiday filter on d and d+1, all 18:00..18:10 bars) and C exists; for sigma additionally the 18:11 bar exists. Both histories include evenings failing the FTMO-day filter. EWMA = pandas ewm(com=60, min_periods=40): mean of M^2 (s), std of r (sigma), read at the last eligible evening before d.")
    A("- Missing 18:11 bar -> no trade. Last-resort exit (no bar in 19:15..19:33): close of the last bar in [entry, 19:30), counted 'lastbar'. Shifted clocks keep the fallback shape (+1..+3 open, else close in -15..-1).")
    A("- Spike-reversal drop: flags recomputed with the data/qa definition on the loaded bars; applied to SPX and NSX as the row names them (XAU hits printed, not dropped); the drop sits outside the harnessed rule because the QA flag reads the next bar.")
    A("- The -20 min entry neighbour (17:51) lies inside the halt; 18:10 (earliest bar after the 18:09 signal) is run in its place. EWMA neighbours move both centres of mass together.")
    A("- Futures sensitivity uses the CFD bid level as the contract price and CFD returns (no futures data in the manifest for this row).")
    Path(out_path).write_text("\n".join(L) + "\n")
    summ = {"id": ID, "net1x_bp_per_leg": o["ev"]["net1x"]["mean"] * 1e4, "net1x_bp_per_evening": o["pe"]["net1x"]["mean"] * 1e4, "t_min": t_dec,
            "boot_lower_bp": lb * 1e4, "t2x": t2, "net3x_bp_leg": o["ev3"]["mean"] * 1e4, "c7": c7, "verdict": verdict}
    print(json.dumps(summ, indent=1), flush=True)
    return summ


def main(stage, cmd):
    pinres = [pins.verify(ID, ds) for ds in DS.values()]
    if stage == "is":
        P = load_all("is")
        B = Book({i: P[i] for i in DS})
        ev = B.ev(ro.Params(), IS_START, IS_END)
        bounds = (float(ev["z"].abs().quantile(1 / 3)), float(ev["z"].abs().quantile(2 / 3)))
        st = g1.ev_stats(ev, "net1")
        el = {i: int(in_window(t, IS_START, IS_END)['eligible'].sum()) for i, t in B.tables(ro.Params()).items()}
        info = (f"eligible evenings {el}, legs {len(ev)} "
                f"({ev['inst'].value_counts().to_dict()}); net 1x {ev['net1'].mean()*1e4:.2f} bp/leg, t {st['t_min']:.2f}")
        print(info, bounds, flush=True)
        leak = leak_checks(P)
        (HERE / "Q-0011_is.json").write_text(json.dumps({"leak": leak, "is_info": info, "bounds": bounds}, indent=1, default=str))
        return
    isj = json.loads((HERE / "Q-0011_is.json").read_text())
    bounds = tuple(isj["bounds"])
    if stage == "dryrun":
        B = Book(load_all("is"))
        a, b = "2011-07-01", IS_END
        yrs = (pd.Timestamp(b) - pd.Timestamp(a)).days / 365.25
        o = evaluate(B, a, b, bounds, yrs)
        write_result(o, isj, pinres, cmd, Path(SCRATCH) / "Q-0011.dry.md")
        return
    B = Book(load_all("oos"))                                     # <- the one OOS read per dataset (+ IS history)
    yrs = (pd.Timestamp(OOS_END) - pd.Timestamp(OOS_START)).days / 365.25
    o = evaluate(B, OOS_START, OOS_END, bounds, yrs)
    write_result(o, isj, pinres, cmd, ROOT / "research" / "results" / "Q-0011.md")
    o["ev_tab"].drop(columns=[]).to_csv(HERE / "Q-0011_oos_legs.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    main(a.stage, f"python3 quant-edge/research/q0011/q0011.py --stage {a.stage}")
