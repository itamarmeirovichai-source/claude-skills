"""F1: yearly net $ per $100K FTMO Swing slot at the stack's OOS Sharpe, via daily/w1-prop/prop_model.py
(economics(), firm 'FTMO Swing 2-Step 100K', n = 1500 as in references/w1-synthesis.md), vol caps 12% and 20%.
A negative Sharpe is floored at 0 for the model (it is not built for negative drift) and flagged.

usage: python3 prop_dollars.py   (reads results.json written by ensemble.py)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "w1-prop"))
from firms import FIRMS              # noqa: E402
from prop_model import SIGMAS, economics   # noqa: E402

F = FIRMS["FTMO Swing 2-Step 100K"]
R = json.load(open(HERE / "results.json"))
rows = []
for vid in ("F1-01", "F1-02"):
    for tag in ("stack", "stack_x2"):
        S = R[vid][tag]["sharpe"]
        for cap in (0.12, 0.20):
            e = economics(F, max(S, 0.0), n=1500, sigmas=SIGMAS[SIGMAS <= cap + 1e-9])
            rows.append(dict(id=vid, cost=tag, sharpe=S, sharpe_used=max(S, 0.0), cap=cap,
                             net_yr=float(e["net_yr"]), sig_e=float(e["sig_e"]), sig_f=float(e["sig_f"]),
                             p_pass=float(e["p_pass"]), fees_yr=float(e["fees_yr"])))
            print(f"{vid} {tag:8s} Sharpe {S:+.2f} (model {max(S, 0):.2f}) cap {cap:.0%}: net ${e['net_yr']:,.0f}"
                  f"/slot-yr  sig_e {e['sig_e']:.2f} sig_f {e['sig_f']:.2f}  pass {e['p_pass']:.2f}  "
                  f"fees ${e['fees_yr']:,.0f}/yr", flush=True)
json.dump(rows, open(HERE / "prop_dollars.json", "w"), indent=1)
