#!/usr/bin/env python3
"""Q-0009 prereg_orb30 A/B/C (registered 0a46ddd). Data only through qe.gateway.load.
Stages:  --stage is   leak harness (truncation + perturbation, qe.engine.harness, IS only; planted look-ahead must fail),
                      then STAGE 1 as written: IS 2010-11-15..2018-12-31 at the written 0.6 pt cost, A/B/C tables, A's
                      day-level bootstrap p5 (10,000 draws, seed 0). The row earns its OOS read ONLY if A's p5 > 0.
         --stage oos  (exists only if Stage 1 passes) one OOS read, Gate v2 per variant.
Usage: python3 quant-edge/research/q0009/q0009.py --stage is
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
import orb30 as orb  # noqa: E402

ID = "Q-0009"
DS = "histdata_cfd_1m_SPXUSD"
IS_START, IS_END = "2010-11-15", "2018-12-31"
OOS_START, OOS_END = "2019-01-02", "2024-12-31"
SEED = 0
VARIANTS = {"A": orb.Params(), "B": orb.Params(target_r=2.0), "C": orb.Params(narrow=True)}


def stage1_table(t: pd.DataFrame, years: float, n_weekdays: int, n_elig: int, kind: str = "is") -> dict:
    if len(t) == 0:
        return {"n": 0}
    net = orb.net_R(t, kind)
    g = t["gross_R"].to_numpy(float)
    bs = stats.day_cluster_bootstrap_mean(net, t["day"].astype(str).to_numpy(), n_draws=10_000, seed=SEED)
    tt = t.assign(net=net)
    yr = tt.groupby(tt["day"].dt.year).agg(n=("net", "size"), net_mean_R=("net", "mean"), net_sum_R=("net", "sum"))
    ls = tt.groupby("side").agg(n=("net", "size"), gross_mean_R=("gross_R", "mean"), net_mean_R=("net", "mean"))
    ex = tt.groupby("exit_type").agg(n=("net", "size"), net_mean_R=("net", "mean"))
    return {"n": len(t), "trades_per_year": len(t) / years, "trades_per_weekday": len(t) / n_weekdays,
            "trades_per_eligible_session": len(t) / n_elig, "gross_mean_R": float(g.mean()), "net_mean_R": float(net.mean()),
            "net_sd_R": float(net.std(ddof=1)), "t_iid_net": stats.iid_t(net), "boot_p5": bs["p5"], "boot_p50": bs["p50"],
            "boot_draws": bs["n_draws"], "median_risk_pt": float(t["risk"].median()), "mean_cost_R": float((g - net).mean()),
            "by_year": yr, "long_short": ls, "exits": ex}


def n_eligible(p: ck.Prepared) -> int:
    n = 0
    for d, (a, b) in ck.day_slices(p).items():
        if pd.Timestamp(d).dayofweek >= 5:
            continue
        mm = p.minute[a:b]
        k0 = int(np.searchsorted(mm, orb.OR_A))
        k1 = int(np.searchsorted(mm, orb.OR_B, side="right"))
        n += int(k0 < mm.size and mm[k0] == orb.OR_A and (k1 - k0) >= 25)
    return n


def stage_is(cmd: str):
    pin = pins.verify(ID, DS)
    bars = ck.load(ID, DS, "is")
    p = ck.prepare(bars, ck.NY)
    fr = fx.tag_for_harness(bars)
    leak = {}
    for name, prm in list(VARIANTS.items()) + [("planted look-ahead (must FAIL)", orb.Params(leak="plant"))]:
        rule = orb.ORBRule(prm)
        a = harness.future_truncation_test(rule, fr, n_days=30, seed=SEED)
        b = harness.perturbation_test(rule, fr, n_days=30, seed=SEED)
        leak[name] = {"truncation_passed": a["passed"], "truncation_checked": a["n_checked"], "truncation_violations": len(a["violations"]),
                      "perturbation_passed": b["passed"], "perturbation_checked": b["n_checked"], "perturbation_violations": len(b["violations"])}
        print(name, leak[name], flush=True)
    years = (pd.Timestamp(IS_END) - pd.Timestamp(IS_START)).days / 365.25
    n_wd = len(pd.bdate_range(IS_START, IS_END))
    n_el = n_eligible(p)
    res, tabs = {}, {}
    for k, prm in VARIANTS.items():
        t = orb.trades(p, prm)
        tabs[k] = t
        res[k] = stage1_table(t, years, n_wd, n_el, "is")
        res[k]["cfd1x_net_mean_R_info"] = float(orb.net_R(t, "cfd1x").mean())
        print(k, {kk: v for kk, v in res[k].items() if not isinstance(v, pd.DataFrame)}, flush=True)
        t.to_csv(HERE / f"Q-0009_is_trades_{k}.csv", index=False)
    passed = bool(res["A"]["boot_p5"] > 0)
    out = {"pin": pin, "leak": leak, "years": years, "n_weekdays": n_wd, "n_eligible": n_el, "stage1_pass": passed,
           "res": {k: {kk: (v.reset_index().to_dict(orient="records") if isinstance(v, pd.DataFrame) else v) for kk, v in r.items()} for k, r in res.items()}}
    (HERE / "Q-0009_is.json").write_text(json.dumps(out, indent=1, default=str))
    write_stage1(out, res, cmd)
    print("STAGE 1:", "PASS -> OOS earned" if passed else "FAIL -> refuted in-sample, no OOS read", flush=True)


def write_stage1(o, res, cmd):
    L = []
    A = L.append
    pin = o["pin"]
    A("# Q-0009 — prereg_orb30 (S&P 30-minute opening-range breakout, variants A/B/C): staged result")
    A("")
    A(f"Registry row Q-0009 (registered commit 0a46ddd, count 3, sign fixed: trade WITH the first break). Script `research/q0009/q0009.py` (rule `research/q0009/orb30.py`, plumbing `research/batch1b/cfdkit.py`, `research/batch1/gatekit.py`, `fxkit.py`). Result-writing commit {gk.git_commit()} (working tree). A pre-registered hypothesis under test; nothing here is called an edge.")
    A("")
    A(f"- Command: `{cmd}`")
    A(f"- Seeds: Stage-1 day-level bootstrap {SEED} (10,000 draws, as written), harness {SEED}.")
    A(f"- Data `{pin['dataset']}` sha256: manifest {pin['manifest_sha256']} = row pin {pin['row_sha256']} = recomputed {pin['computed_sha256']} (ok={pin['ok']}).")
    A(f"- Windows: IS {IS_START}..{IS_END} (= the written D1); OOS {OOS_START}..{OOS_END}; hold-out not read.")
    A("- Stage-1 cost (as written): 0.6 pt round trip (tjr COST_PTS), deducted as cost/Risk in R. The OOS 1x CFD cost (max(0.6 pt, 2.0 bp of entry) round trip) is printed beside it as information only.")
    A("- Clock: America/New_York via zoneinfo on bar-open UTC timestamps (histdata_rule; identical to the written NY clock for 2010-2018).")
    A("")
    A("## registry_reads.log lines for this id")
    A("")
    A("```")
    for l in gk.reads_log_lines(ID):
        A(l)
    A("```")
    A("")
    A("## Leak checks (IS window only, before any OOS decision)")
    A("")
    A("| rule version | truncation passed | days | violations | perturbation passed | days | violations |")
    A("|---|---|---|---|---|---|---|")
    for k, r in o["leak"].items():
        A(f"| {k} | {gk.fmt(r['truncation_passed'])} | {r['truncation_checked']} | {r['truncation_violations']} | {gk.fmt(r['perturbation_passed'])} | {r['perturbation_checked']} | {r['perturbation_violations']} |")
    A("")
    A("`qe.engine.harness` future-truncation and perturbation tests on 30 sampled IS days per version (seed 0). The planted version trades only when the day's 15:59 close is beyond the entry (a deliberate look-ahead); the harness must catch it.")
    A("")
    A("## Stage 1 (as written, in-sample 2010-11-15..2018-12-31, 0.6 pt round trip)")
    A("")
    A(f"IS {o['years']:.2f} years, {o['n_weekdays']} weekdays, {o['n_eligible']} sessions eligible at 10:00 (rule 1).")
    A("")
    A("| variant | n | trades/yr | trades/weekday | trades/eligible session | gross mean R | net mean R | net s.d. R | t (iid) | boot p5 (10,000) | boot p50 | median Risk pt | mean cost R | net mean R at OOS 1x CFD cost (info) |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, r in res.items():
        A(f"| {k} | {r['n']} | {r['trades_per_year']:.1f} | {r['trades_per_weekday']:.3f} | {r['trades_per_eligible_session']:.3f} | {r['gross_mean_R']:+.4f} | {r['net_mean_R']:+.4f} | {r['net_sd_R']:.3f} | {r['t_iid_net']:.2f} | {r['boot_p5']:+.4f} | {r['boot_p50']:+.4f} | {r['median_risk_pt']:.2f} | {r['mean_cost_R']:.4f} | {r['cfd1x_net_mean_R_info']:+.4f} |")
    A("")
    for k, r in res.items():
        A(f"### Variant {k}: net R by year, long vs short, exits by type")
        A("")
        y = r["by_year"].reset_index().rename(columns={"day": "year"})
        A(gk.md_table(y, {"year": lambda x: str(int(x)), "n": lambda x: str(int(x)), "net_mean_R": lambda x: f"{x:+.4f}", "net_sum_R": lambda x: f"{x:+.2f}"}))
        A("")
        s = r["long_short"].reset_index()
        s["side"] = s["side"].map({1: "long", -1: "short"})
        A(gk.md_table(s, {"n": lambda x: str(int(x)), "gross_mean_R": lambda x: f"{x:+.4f}", "net_mean_R": lambda x: f"{x:+.4f}"}))
        A("")
        e = r["exits"].reset_index()
        A(gk.md_table(e, {"n": lambda x: str(int(x)), "net_mean_R": lambda x: f"{x:+.4f}"}))
        A("")
    pa = res["A"]["boot_p5"]
    A("## Stage-1 decision (the row's rule, applied mechanically)")
    A("")
    A(f"- Variant A D1 net bootstrap p5 = {pa:+.4f} R: {'> 0' if pa > 0 else '<= 0'}.")
    if o["stage1_pass"]:
        A("- **Stage 1 PASSED: the family earns the OOS read** (Stage 2 below).")
    else:
        A("- **Stage 1 FAILED. Verdict: FAIL (refuted in-sample).** As fixed in the row: no OOS read was made for Q-0009 (none of A, B, C), "
          "B and C cannot rescue it, and the family orb-30min is closed (no other range lengths, entry windows, targets or filters). "
          "No t_min, bootstrap lower bound or 2x-cost t exists for the OOS window because the OOS window was never loaded.")
        A("- Criterion-4 power that the OOS read would have had (6.0 years): bar in Sharpe units "
          f"{stats.bar_sharpe_units(6.0):.3f}; power at true Sharpe 1.5/2.0/2.4 = " + "/".join(f"{stats.power(s, 6.0):.2f}" for s in (1.5, 2.0, 2.4))
          + f"; {gk.joint_power_note(6.0)}. Not reached.")
    A("")
    A("## Disclosures and implementation notes (fixed before any IS result)")
    A("")
    A("- Session d = New York calendar date of the bar open; only bars of d are read; rules 1-7 exactly as written.")
    A("- B's target fills only when price trades through it (CONVENTIONS.md section 3 limit rule), at the target price; the stop is checked first on every bar, so a bar touching both counts as stop, as written. The entry bar is checked for stop and target from its open.")
    A("- Exit at the close of the last existing bar at or before 15:59 (bars after 15:59 ignored). Half days are not skipped (as written: the rule has no half-day clause).")
    A("- Disclosed adaptations in the row (data = histdata_cfd_1m_SPXUSD, byte-identical 2010-2018 to the inherited pins; OOS on SPXUSD instead of ES; OOS cost at FTMO CFD floors) touch no rule.")
    A("- No news skip (as written).")
    Path(ROOT / "research" / "results" / "Q-0009.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is"])
    a = ap.parse_args()
    stage_is(f"python3 quant-edge/research/q0009/q0009.py --stage {a.stage}")
