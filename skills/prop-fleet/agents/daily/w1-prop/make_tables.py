"""Markdown tables for references/w1-prop.md, straight from results.json.
usage: python3 make_tables.py > tables.md"""
import json
from pathlib import Path

R = json.loads((Path(__file__).parent / "results.json").read_text())
from firms import FIRMS  # noqa: E402  (order)


def at(r, S, tag="capped"):
    return [e for e in r[tag] if abs(e["S"] - S) < 1e-6][0]


def ms(r, key):
    v = r[key]
    if v != v:
        return ">3.0"
    return "<=0.30" if v <= 0.30 + 1e-9 else f"{v:.2f}"


def s0(r):
    z = at(r, 0.0)
    return "yes" if z["ros_after"] >= 0.20 else "no"


print("### A. Per firm at Sharpe 1.17, vol capped at 12%/yr (D1-04, decides)\n")
print("| Firm / program | Bot on funded | Overnight | Slots | Pass % | Eval days | Funded life (days) "
      "| Payouts per funded acct $ | Net $/slot-yr | Fees $/slot-yr | ROS after tax | Fleet $/yr (mean) | Fleet $/yr p10 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in FIRMS:
    r = R[k]; e = at(r, 1.17)
    print(f"| {k} | {r['auto']} | {'yes' if r['hold'] else 'no'} | {r['slots']} | {100*e['p_pass']:.0f} "
          f"| {e['t_eval']:.0f} | {e['life']:.0f} | {e['pay']:,.0f} | {e['net_yr']:,.0f} | {e['fees_yr']:,.0f} "
          f"| {100*e['ros_after']:,.0f}% | {e['net_yr']*r['slots']:,.0f} | {r['slot_117']['p10']*r['slots']:,.0f} |")

print("\n### B. Net $ per slot-year by Sharpe, vol capped at 12% (D1-04) — fleet $ = x slots\n")
Ss = [0.0, 0.8, 1.0, 1.17, 1.2, 1.5, 2.0]
print("| Firm | " + " | ".join(f"S={s}" for s in Ss) + " | S=0.82 (1.17x0.7) |")
print("|---|" + "---|" * (len(Ss) + 1))
for k in FIRMS:
    r = R[k]
    print(f"| {k} | " + " | ".join(f"{at(r, s)['net_yr']:,.0f}" for s in Ss)
          + f" | {r['haircut_117']['net_yr']:,.0f} |")

print("\n### C. Pass probability per attempt and funded lifetime, capped (pass % / life days)\n")
print("| Firm | " + " | ".join(f"S={s}" for s in Ss) + " |")
print("|---|" + "---|" * len(Ss))
for k in FIRMS:
    r = R[k]
    print(f"| {k} | " + " | ".join(f"{100*at(r, s)['p_pass']:.0f}% / {at(r, s)['life']:.0f}" for s in Ss) + " |")

print("\n### D. Uncapped vol (D1-01, upper bound — the optimizer always picks 25-40%/yr: a lottery on the fee)\n")
print("| Firm | sig eval/funded at S=1.17 | Net $/slot-yr S=0 | S=1.17 | S=2.0 | ROS after tax S=1.17 |")
print("|---|---|---|---|---|---|")
for k in FIRMS:
    r = R[k]; e = at(r, 1.17, "uncapped")
    print(f"| {k} | {e['sig_e']:.2f}/{e['sig_f']:.2f} | {at(r, 0.0, 'uncapped')['net_yr']:,.0f} "
          f"| {e['net_yr']:,.0f} | {at(r, 2.0, 'uncapped')['net_yr']:,.0f} | {100*e['ros_after']:,.0f}% |")

print("\n### E. Minimum Sharpe for >= 20%/yr after tax on money spent\n")
print("| Firm | ROS>=20% already at S=0 (D1-05)? | ROS after tax at S=0, capped | min S capped (D1-04) "
      "| min S uncapped (D1-01) | min S capped, Gaussian, EOD-only (D1-02) |")
print("|---|---|---|---|---|---|")
for k in FIRMS:
    r = R[k]
    print(f"| {k} | {s0(r)} | {100*at(r, 0.0)['ros_after']:,.0f}% | {ms(r, 'min_S_capped')} "
          f"| {ms(r, 'min_S_uncapped')} | {ms(r, 'min_S_capped_gauss_eod')} |")
