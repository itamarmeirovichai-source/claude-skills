"""Tables for references/w3-volrisk.md from results.json. Writes tables.md."""
import json
from pathlib import Path

import numpy as np

from scenarios import CAPS, FIRM_NAMES, S_GRID, S_MAIN

HERE = Path(__file__).parent
R = json.loads((HERE / "results.json").read_text())
SHORT = {"FTMO Swing 2-Step 100K": "FTMO", "Blue Guardian 2-Step 100K": "Blue Guardian",
         "CFT 2-Phase 100K": "CFT"}
CAPN = {0.12: "12%", 0.15: "15%", 0.20: "20%", 0.30: "30%", 0.40: "no cap (40%)"}
# rule (a), from the clause readers' verdict tables (clauses-*.md): True = no
# hard breach and not rated high-risk at that annual vol. 12% was not rated
# by the readers; it is taken as the 15% verdict except where they named a
# lower safe level (Blue Guardian: Shield triggers stay rare only at ~8%).
RULE_A = {"FTMO Swing 2-Step 100K": {0.12: True, 0.15: True, 0.20: True, 0.30: False},
          "Blue Guardian 2-Step 100K": {0.12: False, 0.15: False, 0.20: False, 0.30: False},
          "CFT 2-Phase 100K": {0.12: True, 0.15: True, 0.20: True, 0.30: False}}
NAMES = {"F2-01": "baseline (D1)", "F2-02": "t3 tails", "F2-03": "gaps + kill switch",
         "F2-04": "kill switch only", "F2-05": "GARCH clustering",
         "F2-06": "DLL on equity, strictest ref", "F2-07": "firm-exact rules",
         "F2-08": "BG, daily close", "F2-09": "ALL combined",
         "F2-12": "ALL corrected (post-hoc)", "F2-13": "F2-12, realise daily, -0.47 S (post-hoc)"}


def best(firm, S, cap):
    """Post-hoc decision value: the better of F2-12 and F2-13."""
    a, b = net("F2-12", firm, S, cap), net("F2-13", firm, S, cap)
    return (a, "12") if a >= b else (b, "13")


def need_best(firm, cap, target=20_000.):
    xs = [S for S in S_GRID]
    ys = [best(firm, S, cap)[0] for S in xs]
    if ys[0] >= target:
        return f"<= {xs[0]:.2f}"
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if y0 < target <= y1:
            return f"{x0 + (target - y0) / (y1 - y0) * (x1 - x0):.2f}"
    return f"> {xs[-1]:.2f}"


def posthoc(L):
    if "F2-12" not in R or "F2-13" not in R:
        return
    for sid in ("F2-12", "F2-13"):
        L.append(f"\n## Net $ per slot-year, pre-tax, {sid} {NAMES[sid]}\n")
        L.append("| Firm | S | " + " | ".join(CAPN[c] for c in CAPS) + " |")
        L.append("|---|---|" + "---|" * len(CAPS))
        for f in FIRM_NAMES:
            for S in S_MAIN:
                L.append(f"| {SHORT[f]} | {S:.1f} | " +
                         " | ".join(k(net(sid, f, S, c)) for c in CAPS) + " |")
    L.append("\n## DECISION (post-hoc): better of F2-12 / F2-13, net $ per slot-year\n")
    L.append("| Firm | S | " + " | ".join(CAPN[c] for c in CAPS) + " |")
    L.append("|---|---|" + "---|" * len(CAPS))
    for f in FIRM_NAMES:
        for S in S_MAIN:
            L.append(f"| {SHORT[f]} | {S:.1f} | " + " | ".join(
                f"{k(best(f, S, c)[0])} ({best(f, S, c)[1]})" for c in CAPS) + " |")
    L.append("\n## Sharpe needed for $20k per slot-year: F2-01 vs F2-09 vs F2-12 vs F2-13 vs decision\n")
    L.append("| Firm | scenario | " + " | ".join(CAPN[c] for c in CAPS) + " |")
    L.append("|---|---|" + "---|" * len(CAPS))
    for f in FIRM_NAMES:
        for sid in ("F2-01", "F2-09", "F2-12", "F2-13"):
            L.append(f"| {SHORT[f]} | {sid} | " + " | ".join(need(sid, f, c) for c in CAPS) + " |")
        L.append(f"| {SHORT[f]} | **decision** | " + " | ".join(need_best(f, c) for c in CAPS) + " |")
    # Monte Carlo s.e. from F2-12 (seed 11) and F2-15 s1..s4, S = 1.0
    seeds = ["F2-12"] + [f"F2-15s{i}" for i in range(1, 5)]
    if all(s_ in R for s_ in seeds):
        L.append("\n## Monte Carlo noise (F2-12 at S = 1.0, 5 seed pairs) and safe-vol rule\n")
        L.append("| Firm | cap | mean net | s.e. of one run | gain vs lower cap (mean) | s.e. of gain (one run) "
                 "| rule (a) clauses | rule (b) $250 | rule (b) 2 s.e. | breach before 1st payout |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for f in FIRM_NAMES:
            prev = None
            for c in (0.12, 0.15, 0.20, 0.30):
                v = np.array([R[s_][f]["1.00"]["caps"][f"{c:.2f}"]["net"] for s_ in seeds])
                bp = R["F2-12"][f]["1.00"]["caps"][f"{c:.2f}"]["breach_pre1"]
                if prev is None:
                    g = "–"; gs = "–"; rb = rb2 = "–"
                else:
                    d = v - prev
                    se = d.std(ddof=1)
                    g = f"{d.mean():+,.0f}"; gs = f"{se:,.0f}"
                    rb = "pass" if d[0] > 250 else "fail"
                    rb2 = "pass" if d[0] > 2 * se else "fail"
                L.append(f"| {SHORT[f]} | {CAPN[c]} | {k(v.mean())} | {v.std(ddof=1):,.0f} | {g} | {gs} | "
                         f"{'pass' if RULE_A[f][c] else 'FAIL'} | {rb} | {rb2} | {bp*100:.0f}% |")
                prev = v
    for sid in ("F2-14a", "F2-14b"):
        if sid not in R:
            continue
        L.append(f"\n## {sid}: calendar chain per slot under {'F2-12' if sid.endswith('a') else 'F2-13'}\n")
        L.append("| Firm | S | cap | sigma e/f | year-1 mean | year-1 p10 | P(year-1 loss) | "
                 "yrs 2-3 mean | p50 | p10 | P(loss) |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for f in FIRM_NAMES:
            for key, r in sorted(R[sid][f].items()):
                L.append(f"| {SHORT[f]} | {r['S']:.1f} | {CAPN[r['cap']]} | "
                         f"{r['sig_e']*100:.0f}/{r['sig_f']*100:.0f}% | {k(r['y1_mean'])} | "
                         f"{k(r['y1_p10'])} | {r['y1_loss']*100:.0f}% | {k(r['ss_mean'])} | "
                         f"{k(r['ss_p50'])} | {k(r['ss_p10'])} | {r['ss_loss']*100:.0f}% |")
    L.append("\n## Lottery check (S = 0, no cap): renewal-reward net and calendar years-2-3 median\n")
    L.append("| Firm | F2-01 | F2-09 net / p50 (F2-11) | F2-12 net / p50 (F2-14a) | F2-13 net / p50 (F2-14b) | survives? |")
    L.append("|---|---|---|---|---|---|")
    for f in FIRM_NAMES:
        def cell(sid, seq):
            n_ = net(sid, f, 0.0, 0.40)
            p = R.get(seq, {}).get(f, {}).get("0.00@0.40", {}).get("ss_p50", float("nan"))
            return n_, p, f"{k(n_)} / {k(p)}"
        a, b, c = cell("F2-09", "F2-11"), cell("F2-12", "F2-14a"), cell("F2-13", "F2-14b")
        best_ = b if b[0] >= c[0] else c
        surv = "yes" if best_[0] > 0 and best_[1] > 0 else "no"
        L.append(f"| {SHORT[f]} | {k(net('F2-01', f, 0.0, 0.40))} | {a[2]} | {b[2]} | {c[2]} | {surv} |")


def net(sid, firm, S, cap):
    return R[sid][firm][f"{S:.2f}"]["caps"][f"{cap:.2f}"]["net"]


def k(x):
    return f"{x / 1000:,.1f}k"


def need(sid, firm, cap, target=20_000.):
    """Linear interpolation of S where net $/slot-yr crosses target."""
    xs = [S for S in S_GRID if f"{S:.2f}" in R[sid][firm]]
    ys = [net(sid, firm, S, cap) for S in xs]
    if ys[0] >= target:
        return f"<= {xs[0]:.2f}"
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if y0 < target <= y1:
            return f"{x0 + (target - y0) / (y1 - y0) * (x1 - x0):.2f}"
    return f"> {xs[-1]:.2f}"


def main():
    L = []
    L.append("# F2 tables (generated by make_report.py from results.json)\n")
    for sid in ("F2-01", "F2-09"):
        L.append(f"\n## Net $ per slot-year, pre-tax, {sid} {NAMES[sid]}\n")
        L.append("| Firm | S | " + " | ".join(CAPN[c] for c in CAPS) + " |")
        L.append("|---|---|" + "---|" * len(CAPS))
        for f in FIRM_NAMES:
            for S in S_MAIN:
                L.append(f"| {SHORT[f]} | {S:.1f} | " +
                         " | ".join(k(net(sid, f, S, c)) for c in CAPS) + " |")
    L.append("\n## Sharpe needed for $20k per slot-year (pre-tax)\n")
    L.append("| Firm | scenario | " + " | ".join(CAPN[c] for c in CAPS) + " |")
    L.append("|---|---|" + "---|" * len(CAPS))
    for f in FIRM_NAMES:
        for sid in ("F2-01", "F2-09"):
            L.append(f"| {SHORT[f]} | {sid} | " + " | ".join(need(sid, f, c) for c in CAPS) + " |")
    for cap in (0.12, 0.20, 0.40):
        L.append(f"\n## Each stress alone, cap {CAPN[cap]}: net $/slot-yr (change vs F2-01)\n")
        L.append("| Scenario | " + " | ".join(f"{SHORT[f]} S={S:.1f}" for f in FIRM_NAMES
                                             for S in (0.0, 1.0, 1.5)) + " |")
        L.append("|---|" + "---|" * 9)
        for sid in NAMES:
            if sid not in R:
                continue
            cells = []
            for f in FIRM_NAMES:
                for S in (0.0, 1.0, 1.5):
                    if f not in R[sid]:
                        cells.append("–"); continue
                    v, b = net(sid, f, S, cap), net("F2-01", f, S, cap)
                    cells.append(f"{k(v)} ({(v - b) / max(abs(b), 1) * 100:+.0f}%)")
            L.append(f"| {sid} {NAMES[sid]} | " + " | ".join(cells) + " |")
    L.append("\n## At a FIXED vol (sigma_e = sigma_f), S = 1.0: pass %, funded breach "
             "before 1st payout %, funded life (days), shield triggers\n")
    L.append("| Firm | scenario | " + " | ".join(f"vol {int(s*100)}%" for s in (0.12, 0.15, 0.20, 0.30)) + " |")
    L.append("|---|---|" + "---|" * 4)
    for f in FIRM_NAMES:
        for sid in ("F2-01", "F2-07", "F2-09"):
            fx = R[sid][f]["1.00"]["fixed"]
            cells = []
            for s in (0.12, 0.15, 0.20, 0.30):
                x = fx[f"{s:.2f}"]
                sh = f", sh {x['shield']:.1f}" if x["shield"] else ""
                cells.append(f"{x['p_pass']*100:.0f} / {x['breach_pre1']*100:.0f} / "
                             f"{x['life']:.0f}{sh}")
            L.append(f"| {SHORT[f]} | {sid} | " + " | ".join(cells) + " |")
    for sid in ("F2-10", "F2-11"):
        if sid not in R:
            continue
        L.append(f"\n## {sid}: calendar chain per slot (fees when paid, refund on its date)\n")
        L.append("| Firm | S | cap | sigma e/f | year-1 mean | year-1 p10 | P(year-1 loss) | "
                 "yrs 2-3 mean | p50 | p10 | P(loss) |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for f in FIRM_NAMES:
            for key, r in sorted(R[sid][f].items()):
                L.append(f"| {SHORT[f]} | {r['S']:.1f} | {CAPN[r['cap']]} | "
                         f"{r['sig_e']*100:.0f}/{r['sig_f']*100:.0f}% | {k(r['y1_mean'])} | "
                         f"{k(r['y1_p10'])} | {r['y1_loss']*100:.0f}% | {k(r['ss_mean'])} | "
                         f"{k(r['ss_p50'])} | {k(r['ss_p10'])} | {r['ss_loss']*100:.0f}% |")
    L.append("\n## Safe-vol rule (b): F2-09, S = 1.0, gain from raising the cap\n")
    L.append("| Firm | 12->15 | 15->20 | 20->30 | chosen sigma e/f at each cap |")
    L.append("|---|---|---|---|---|")
    for f in FIRM_NAMES:
        c = R["F2-09"][f]["1.00"]["caps"]
        g = [c[f"{b:.2f}"]["net"] - c[f"{a:.2f}"]["net"] for a, b in ((0.12, 0.15), (0.15, 0.20), (0.20, 0.30))]
        ch = ", ".join(f"{int(cc*100)}: {c[f'{cc:.2f}']['sig_e']*100:.0f}/{c[f'{cc:.2f}']['sig_f']*100:.0f}"
                       for cc in CAPS)
        L.append(f"| {SHORT[f]} | " + " | ".join(f"{x:+,.0f}" for x in g) + f" | {ch} |")
    posthoc(L)
    (HERE / "tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
