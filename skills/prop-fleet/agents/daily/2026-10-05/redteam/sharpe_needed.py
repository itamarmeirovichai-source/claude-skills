"""Red team 2026-10-05: attack 'required Sharpe ~3' (gate rule 4).
Re-uses today's economist plans and simulator UNCHANGED (economist/economist_run.py,
economist/fleet_model.py). Only the firm subset and the R grid are new.
Question: what R per trade, and what annual Sharpe at 2:1, does the 20%-of-nominal
goal need for the firms that survive the rule-1 attack (Bulenox; Bulenox+Lucid;
Bulenox+Topstep), at 1 and 3 trades/day? Also prints net / cash fees spent.
Sharpe at 2:1: p=(R+1)/3, sd=sqrt(4p+(1-p)-R^2), SR=R/sd*sqrt(250*td) (same formula
as economist_run.py)."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "economist"))
import economist_run as er

def sr(R, td):
    p = (R + 1) / 3; sd = np.sqrt(p * 4 + (1 - p) - R * R)
    return R / sd * np.sqrt(250 * td)

print("annual Sharpe at 2:1 for R per trade x trades/day (250 days)")
for R in (0.10, 0.25, 0.32, 0.36, 0.50, 0.90):
    print(f"  {R:+.2f}R  1/day {sr(R,1):5.2f}  3/day {sr(R,3):5.2f}")

SUBSETS = {"Bulenox5": ["Bulenox"], "Bulenox5+Lucid5 (Tier A)": ["Bulenox", "Lucid"],
           "Bulenox5+Topstep5": ["Bulenox", "Topstep"]}
grid = [round(x, 2) for x in np.arange(0.10, 1.52, 0.02)]
cache = {}
def fr(k, R, td):
    if (k, R, td) not in cache:
        d = er.firm(k, R, trades_day=td)
        cache[(k, R, td)] = (d["net_year"][:, er.SS].mean(axis=1), d["fees"][:, er.SS].mean())
    return cache[(k, R, td)]

print("\nfirst R (grid 0.02) at which subset net/yr >= 20% of 50K x accounts; economist plans of 2026-10-05")
for name, ks in SUBSETS.items():
    cap = 50_000. * 5 * len(ks)
    for td in (3, 1):
        hit = None
        for R in grid:
            net = sum(fr(k, R, td)[0] for k in ks)
            if net.mean() >= 0.20 * cap:
                fees = sum(fr(k, R, td)[1] for k in ks)
                hit = (R, net.mean(), np.percentile(net, 10), fees); break
        if hit:
            R, m, p10, fees = hit
            print(f"  {name:26} {td}/day: R {R:+.2f}  SR {sr(R,td):5.2f}  net {m:,.0f} (p10 {p10:,.0f}) "
                  f"= {100*m/cap:.1f}% of ${cap/1e3:.0f}K nominal; fees/yr {fees:,.0f}")
        else:
            print(f"  {name:26} {td}/day: none up to +1.50R")
