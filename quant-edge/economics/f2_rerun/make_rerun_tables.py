"""Markdown tables for economics/required-sharpe-2026-11.md from
results_rerun.json (F2-12 / F2-13 re-run) and futures_frame.json.
usage: python3 make_rerun_tables.py > tables_rerun.md"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "results_rerun.json").read_text())
FF = json.loads((HERE / "futures_frame.json").read_text()) if (HERE / "futures_frame.json").exists() else None
CAPS = ["0.12", "0.15", "0.20"]
CAPN = {"0.12": "12%", "0.15": "15%", "0.20": "20%", "0.30": "30%", "0.40": "no cap (40%)"}
# inherited, agents/daily/w3-volrisk/tables.md (commit e0f5e59), FTMO Swing 2-Step 100K
INH_NEED = {"F2-01 (D1 baseline)": {"0.12": 2.42, "0.15": 1.88, "0.20": 1.42},
            "F2-09 (ALL combined)": {"0.12": 2.42, "0.15": 1.92, "0.20": 1.46}}
INH_F209_S1 = {"0.12": 7500., "0.15": 9900., "0.20": 13600., "0.30": 21200., "0.40": 26600.}
TARGETS = [(20_000., "$20k pre-tax"), (30_000., "$30k pre-tax"),
           (20_000. / 0.75, "$20k after 25% tax (= $26.7k pre-tax)"),
           (30_000. / 0.75, "$30k after 25% tax (= $40.0k pre-tax)"),
           (20_000. / 0.53, "$20k after 47% tax (= $37.7k pre-tax)"),
           (30_000. / 0.53, "$30k after 47% tax (= $56.6k pre-tax)")]


def k(x):
    return f"{x / 1000:,.1f}k"


def cells(sid):
    out = {}
    for Sk, seeds in R[sid].items():
        S = float(Sk)
        out[S] = {}
        for c in CAPS:
            if c not in seeds[next(iter(seeds))]["caps"]:
                continue
            order = sorted(seeds, key=int)
            vals = np.array([seeds[sd]["caps"][c]["net"] for sd in order])
            base = seeds["11"]["caps"][c]["net"] if "11" in seeds else float(vals[0])
            se = float(vals.std(ddof=1) / np.sqrt(len(vals))) if len(vals) > 1 else float("nan")
            out[S][c] = dict(base=float(base), mean=float(vals.mean()), se=se, k=len(vals),
                             sd=float(vals.std(ddof=1)) if len(vals) > 1 else float("nan"))
    return dict(sorted(out.items()))


def need(xs, ys, target, ses=None):
    """First upward crossing by linear interpolation; delta-method s.e. of the
    crossing from the bracketing cells' s.e. (nan where only one seed ran)."""
    if ys[0] >= target:
        return f"<= {xs[0]:.2f}", None
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(zip(xs, ys), zip(xs[1:], ys[1:]))):
        if y0 < target <= y1:
            x = x0 + (target - y0) / (y1 - y0) * (x1 - x0)
            if ses is not None:
                s = [v for v in (ses[i], ses[i + 1]) if v == v]
                se_net = float(np.mean(s)) if s else float("nan")
                slope = (y1 - y0) / (x1 - x0)
                return f"{x:.2f}", se_net / slope
            return f"{x:.2f}", None
    return f"> {xs[-1]:.2f}", None


def fmt_need(txt, se):
    if se is None or se != se:
        return txt
    return f"{txt} ± {se:.3f}"


L = []
C12, C13 = cells("F2-12"), cells("F2-13")
S_ALL = sorted(set(C12) | set(C13))

L.append("### T1. Net $ per slot-year, pre-tax, FTMO Swing 2-Step 100K (renewal reward; seed-mean ± Monte Carlo s.e. over seed pairs; base-seed value in brackets; n = 3000 paths per sigma)\n")
L.append("| Scenario | S | " + " | ".join(f"cap {CAPN[c]}" for c in CAPS) + " | seed pairs |")
L.append("|---|---|" + "---|" * len(CAPS) + "---|")
for sid, C in (("F2-12", C12), ("F2-13", C13)):
    for S in sorted(C):
        row = []
        for c in CAPS:
            d = C[S][c]
            row.append(f"{k(d['mean'])} ± {d['se']:,.0f} ({k(d['base'])})" if d["k"] > 1 else f"{k(d['base'])} (1 seed)")
        L.append(f"| {sid} | {S:.1f} | " + " | ".join(row) + f" | {C[S][CAPS[0]]['k']} |")

L.append("\n### T2. Better of F2-12 and F2-13 per cell (seed means), and which book wins\n")
L.append("| S | " + " | ".join(f"cap {CAPN[c]}" for c in CAPS) + " |")
L.append("|---|" + "---|" * len(CAPS))
BEST = {}
for S in S_ALL:
    row = []
    BEST[S] = {}
    for c in CAPS:
        a, b = C12.get(S, {}).get(c), C13.get(S, {}).get(c)
        if a and b:
            w = "F2-12" if a["mean"] >= b["mean"] else "F2-13"
            v = max(a["mean"], b["mean"]); se = a["se"] if w == "F2-12" else b["se"]
        else:
            d = a or b; w = "F2-12" if a else "F2-13"; v, se = d["mean"], d["se"]
        BEST[S][c] = dict(mean=v, se=se, who=w)
        row.append(f"{k(v)} ({w})")
    L.append(f"| {S:.1f} | " + " | ".join(row) + " |")

L.append("\n### T3. Required net Sharpe (linear interpolation on the S grid; ± = delta-method s.e. from the bracketing cells' Monte Carlo s.e.)\n")
L.append("| Target | Book | " + " | ".join(f"vol {CAPN[c]}" for c in CAPS) + " |")
L.append("|---|---|" + "---|" * len(CAPS))
for tgt, name in TARGETS:
    for lab, C in (("F2-12 re-run 2026-11-03", C12), ("F2-13 re-run 2026-11-03", C13), ("better-of re-run 2026-11-03", BEST)):
        row = []
        for c in CAPS:
            xs = [S for S in sorted(C) if c in C[S]]
            ys = [C[S][c]["mean"] for S in xs]
            ses = [C[S][c]["se"] for S in xs]
            row.append(fmt_need(*need(xs, ys, tgt, ses)))
        L.append(f"| {name} | {lab} | " + " | ".join(row) + " |")
    if tgt == 20_000.:
        for lab, d in INH_NEED.items():
            L.append(f"| {name} | {lab} inherited | " + " | ".join(f"{d[c]:.2f}" for c in CAPS) + " |")

L.append("\n### T4. Diagnostics at the base seed (eval 11 / funded 12), per cap: pass probability per attempt, expected evaluation days until the first pass (geometric re-buys), funded life (days), payouts per funded account ($, trader share), payouts count, P(any payout), breach before 1st payout, time to first payout (trading days from the first purchase), evaluations bought and funded accounts lost per slot-year, fees per slot-year\n")
L.append("| Scenario | S | cap | sig e/f | pass | eval days | life | pay/acct | n_pay | P(any) | breach pre-1st | days to 1st payout | evals/slot-yr | funded lost/slot-yr | fees/slot-yr |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for sid in ("F2-12", "F2-13"):
    for Sk in sorted(R[sid], key=float):
        b = R[sid][Sk].get("11")
        if not b:
            continue
        for c in CAPS:
            r = b["caps"][c]
            L.append(f"| {sid} | {float(Sk):.1f} | {CAPN[c]} | {r['sig_e']*100:.0f}/{r['sig_f']*100:.0f} | "
                     f"{r['p_pass']*100:.0f}% | {r['t_eval']:.0f} | {r['life']:.0f} | {r['pay']:,.0f} | "
                     f"{r['n_pay']:.1f} | {r['p_any']*100:.0f}% | {r['breach_pre1']*100:.0f}% | "
                     f"{r['t_first_payout_total']:.0f} | {r['evals_per_slot_yr']:.2f} | "
                     f"{r['funded_breached_per_slot_yr']:.2f} | {r['fees_yr']:,.0f} |")

if "seq" in R:
    L.append("\n### T5. Calendar chain per slot (inherited slot_years: fees paid when bought, refund with the first payout; 2000 slots x 3 years, seed 21; sigma pair from the base-seed grid). Year 1 and the mean of years 2-3, pre-tax $\n")
    L.append("| Scenario | S | cap | sig e/f | yr-1 mean | p10 | p50 | p90 | P(loss) | yrs 2-3 mean | p10 | p50 | p90 | P(loss) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sid in ("F2-12", "F2-13"):
        for key in sorted(R["seq"].get(sid, {}), key=lambda s: (float(s.split("@")[0]), float(s.split("@")[1]))):
            r = R["seq"][sid][key]
            a, b = r["year1"], r["years23"]
            L.append(f"| {sid} | {r['S']:.1f} | {CAPN[f'{r['cap']:.2f}']} | {r['sig_e']*100:.0f}/{r['sig_f']*100:.0f} | "
                     f"{k(a['mean'])} | {k(a['p10'])} | {k(a['p50'])} | {k(a['p90'])} | {a['p_loss']*100:.0f}% | "
                     f"{k(b['mean'])} | {k(b['p10'])} | {k(b['p50'])} | {k(b['p90'])} | {b['p_loss']*100:.0f}% |")

if "F2-09" in R:
    L.append("\n### T6. Replication check: F2-09 at S = 1.0, base seed, full D1 sigma grid, against the inherited tables.md\n")
    L.append("| cap | re-run net $/slot-yr | inherited (tables.md, rounded to $0.1k) | sig e/f re-run |")
    L.append("|---|---|---|---|")
    b = R["F2-09"]["1.00"]["11"]["caps"]
    for c in ("0.12", "0.15", "0.20", "0.30", "0.40"):
        if c in b:
            L.append(f"| {CAPN[c]} | {b[c]['net']:,.0f} | {INH_F209_S1[c]:,.0f} | {b[c]['sig_e']*100:.0f}/{b[c]['sig_f']*100:.0f} |")

# runtime
cpu = 0.0; nj = 0
for sid in R:
    if sid == "seq":
        for s2 in R[sid]:
            for key in R[sid][s2]:
                cpu += R[sid][s2][key]["cpu_s"]; nj += 1
        continue
    for Sk in R[sid]:
        for sd in R[sid][Sk]:
            cpu += R[sid][Sk][sd]["meta"]["cpu_s"]; nj += 1
L.append(f"\nRuntime: {nj} jobs, {cpu/60:.1f} CPU-minutes in total (per-job wall/CPU seconds are in results_rerun.json).")

if FF:
    L.append("\n### T7. Futures-firm frame A (trade level, Apex-era plans, inherited parameters fetched 2026-10-11): R per trade needed for 20% of nominal per year in steady state, by trades per day and tax reading\n")
    L.append("| Plan | trades/day | pre-tax | 25% tax (capital gains) | 47% (business income) | 53% (business + NI) | implied annual Sharpe at the 25%-tax threshold (net of modelled costs) | implied vol, % of nominal |")
    L.append("|---|---|---|---|---|---|---|---|")
    for key, th in FF["thresholds"].items():
        plan, tpd = key.split("|")
        rows = FF["trade"][key]
        # Sharpe implied at the 25% threshold: interpolate S_eq over R
        xs = [r["avg_R"] for r in rows]; se_ = [r["equiv"]["S_net"] for r in rows]; vv = [r["equiv"]["vol_pct_nominal"] for r in rows]
        try:
            rt = float(th["tax25"])
            s_eq = float(np.interp(rt, xs, se_)); vol = float(np.interp(rt, xs, vv))
            tail = f"{s_eq:.1f} | {vol*100:.0f}%"
        except ValueError:
            tail = "– | –"
        L.append(f"| {plan} | {tpd} | {th['tax0']} | {th['tax25']} | {th['tax47']} | {th['tax53']} | {tail} |")
    F1 = json.loads((HERE / "futures_frame_1tpd.json").read_text()) if (HERE / "futures_frame_1tpd.json").exists() else None
    if F1:
        L.append("\n### T7b. Same frame with the funded account at 8% of drawdown (two wins a day clear the plan's $200 qualifying-day minimum; at 4% a single win does not, so 1 trade/day never pays out at 4%)\n")
        L.append("| Plan | trades/day | funded risk | pre-tax | 25% tax | 47% tax | 53% tax | implied annual Sharpe at the 25%-tax threshold | implied vol, % of nominal |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for key, th in F1["thresholds"].items():
            plan, tpd, risk = key.split("|")
            rows = F1["trade"][key]
            xs = [r["avg_R"] for r in rows]; se_ = [r["equiv"]["S_net"] for r in rows]; vv = [r["equiv"]["vol_pct_nominal"] for r in rows]
            try:
                rt = float(th["tax25"])
                tail = f"{float(np.interp(rt, xs, se_)):.1f} | {float(np.interp(rt, xs, vv))*100:.0f}%"
            except ValueError:
                tail = "– | –"
            L.append(f"| {plan} | {tpd} | {risk.replace('risk', '')}% of DD | {th['tax0']} | {th['tax25']} | {th['tax47']} | {th['tax53']} | {tail} |")
        if "meta" in F1:
            L.append(f"\nSupplement runtime: {F1['meta']['cpu_s']/60:.1f} CPU-minutes.")
    L.append("\n### T8. Futures-firm frame A, 50K-2026 plan, 3 trades/day: the grid behind the thresholds (steady-state net as % of nominal; p10 across fleet paths; accounts lost and evaluations bought per slot-year)\n")
    L.append("| R/trade | pre-tax | 25% tax | 47% tax | p10 at 25% | lost/slot-yr | evals/slot-yr | implied Sharpe (net) | implied vol % nominal |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in FF["trade"].get("50K-2026|3", []):
        L.append(f"| {r['avg_R']:+.2f} | {r['pct_nominal_tax0']*100:.1f}% | {r['pct_nominal_tax25']*100:.1f}% | "
                 f"{r['pct_nominal_tax47']*100:.1f}% | {r['p10_pct_nominal_tax25']*100:.1f}% | {r['burned_per_slot_yr']:.1f} | "
                 f"{r['evals_per_slot_yr']:.1f} | {r['equiv']['S_net']:.2f} | {r['equiv']['vol_pct_nominal']*100:.0f}% |")
    L.append("\n### T9. Futures-firm frame B (daily Sharpe/vol D1 model, inherited firms.py parameters fetched 2026-10-11, t5 shocks, 4 checks a day): net $/slot-year at vol caps 12% and 20%, and the Sharpe at which it reaches 20% of nominal ($10k per 50K slot-year)\n")
    L.append("| Program | " + " | ".join(f"S={S:g}: cap12 / cap20" for S in [r["S"] for r in next(iter(FF["daily"].values()))]) + " | S for 20% of nominal, cap 12% / cap 20% |")
    L.append("|---|" + "---|" * (len(next(iter(FF["daily"].values()))) + 1))
    for name, rows in FF["daily"].items():
        nd = FF["daily_need"][name]
        L.append(f"| {name} | " + " | ".join(f"{r['caps']['0.12']['net']:,.0f} / {r['caps']['0.20']['net']:,.0f}" for r in rows)
                 + f" | {nd['0.12']} / {nd['0.20']} |")
    if "meta" in FF:
        L.append(f"\nFutures frame runtime: {FF['meta']['cpu_s']/60:.1f} CPU-minutes.")

txt = "\n".join(L) + "\n"
(HERE / "tables_rerun.md").write_text(txt)
print(txt)
