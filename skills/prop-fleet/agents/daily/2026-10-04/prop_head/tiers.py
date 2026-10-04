"""Head of Prop Structure, 2026-10-04. Re-runs the economist's fleet_model with
5 accounts per firm, grouped into tiers by how well each firm satisfies BOTH
unchangeable rules (fully automatic + many funded accounts). Plans are imported
unchanged from economist_run.FIRM_PLANS; only slots, tiers and two sensitivities
(Bulenox at equal $80 risk; Bulenox keep_off) are new."""
import sys, os, copy
import numpy as np
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "../../../../scripts"))
import fleet_model as fm
from economist_run import FIRM_PLANS, KW, SS

TIERS = {
  "A  Bulenox5+Lucid5 (rule1 on own FAQ snippet)": ["Bulenox", "Lucid"],
  "B  A + Topstep5 Express (until Live)": ["Bulenox", "Lucid", "Topstep"],
  "C  B + Tradeify5 (only if 'not at other firms' waived)": ["Bulenox", "Lucid", "Topstep", "Tradeify"],
}
SLOTS = 5
RS = (0.10, 0.25, 0.40)

def firm_net(key, R, plan=None, risk_pct=None):
    P = plan or FIRM_PLANS[key]
    kw = dict(KW)
    if risk_pct is not None:
        kw["risk_pct"] = risk_pct
    d = fm.simulate(P, slots=SLOTS, avg_R=R, **kw)
    return d["net_year"][:, SS].mean(axis=1)

cache = {}
print("per firm, 5 accounts, net/yr after 25% tax, mean yrs 2-4 (p10/p90)")
for key in ["Bulenox", "Lucid", "Topstep", "Tradeify", "MFFU"]:
    row = []
    for R in RS:
        v = firm_net(key, R); cache[(key, R)] = v
        row.append(f"{R:+.2f}R {v.mean():>8,.0f} ({np.percentile(v,10):,.0f}/{np.percentile(v,90):,.0f})")
    print(f"{key:9}", " | ".join(row))

print("\ntiers: net/yr, % of nominal 50K*accounts")
for name, firms in TIERS.items():
    cap = 50_000. * SLOTS * len(firms)
    out = []
    for R in RS:
        t = sum(cache[(f, R)] for f in firms)
        out.append(f"{R:+.2f}R {t.mean():>9,.0f} = {100*t.mean()/cap:4.1f}% (p10 {np.percentile(t,10):,.0f})")
    print(f"{name:52} n={SLOTS*len(firms):2}", " | ".join(out))

print("\nR needed for 20% of nominal, by tier (grid 0.20..0.50 step 0.02)")
for name, firms in TIERS.items():
    cap = 50_000. * SLOTS * len(firms)
    hit = None
    for R in np.arange(0.20, 0.52, 0.02):
        R = round(float(R), 2)
        t = sum((cache.get((f, R)) if (f, R) in cache else cache.setdefault((f, R), firm_net(f, R))) for f in firms)
        pct = 100 * t.mean() / cap
        if hit is None and pct >= 20:
            hit = (R, pct)
    print(f"{name:52} first R with >=20%: {hit}")

print("\nsensitivity Bulenox (5 accts)")
for R in RS:
    eq = firm_net("Bulenox", R, risk_pct=80/2500)       # $80 risk like the $2,000-dd firms
    P = copy.deepcopy(FIRM_PLANS["Bulenox"]); P["keep_off"] = 2_500. + 500.   # bigger buffer
    kb = firm_net("Bulenox", R, plan=P)
    print(f"{R:+.2f}R base {cache[('Bulenox',R)].mean():>8,.0f} | equal $80 risk {eq.mean():>8,.0f} | keep_off 3000 {kb.mean():>8,.0f}")
