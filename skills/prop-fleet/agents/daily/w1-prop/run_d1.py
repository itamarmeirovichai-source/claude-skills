"""D1 run: every firm x Sharpe under D1-01 (uncapped vol), D1-04 (vol <=12%,
decides), D1-02 (Gaussian, EOD only, capped), D1-03 (S x 0.7) and D1-05
(S = 0). Pre-registered in agents/prereg/D1.csv. Writes results.json and
results.txt next to this file.

usage: python3 run_d1.py [firm substring ...]
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from firms import FIRMS, SHARPES
from prop_model import SIGMAS, economics, min_sharpe, slot_years

N = 4000                                  # paths, D1-01
CAP = SIGMAS[SIGMAS <= 0.12]              # D1-04
HERE = Path(__file__).parent
KEYS = ("S", "sig_e", "sig_f", "p_pass", "t_eval", "attempts", "life", "pay",
        "n_pay", "survive", "net_yr", "fees_yr", "ros_pre", "ros_after")


def row(e):
    return {k: float(e[k]) for k in KEYS}


def run_firm(name):
    F = FIRMS[name]
    out = dict(firm=name, slots=F["slots"], auto=F["auto"], hold=F["hold"],
               unmodeled=F.get("unmodeled", ""))
    out["capped"] = [row(economics(F, S, n=N, sigmas=CAP)) for S in SHARPES]
    out["uncapped"] = [row(economics(F, S, n=N)) for S in SHARPES]
    out["haircut_117"] = row(economics(F, 1.17 * 0.7, n=N, sigmas=CAP))     # D1-03
    out["min_S_capped"] = min_sharpe(F, n=N, sigmas=CAP)
    out["min_S_uncapped"] = min_sharpe(F, n=N)
    out["min_S_capped_gauss_eod"] = min_sharpe(F, n=N, sigmas=CAP, tdist=False, sub=1)
    out["capped_gauss_eod_117"] = row(economics(F, 1.17, n=N, sigmas=CAP, tdist=False, sub=1))
    # fleet distribution at S = 1.17, capped optimum (years 2-3 of a 3-year run)
    e = out["capped"][SHARPES.index(1.17)]
    y = slot_years(F, 1.17, e["sig_e"], e["sig_f"], years=3, n=2000)
    per = y[:, 1:].mean(1)
    out["slot_117"] = dict(mean=float(per.mean()), p10=float(np.percentile(per, 10)),
                           p50=float(np.median(per)), y1_mean=float(y[:, 0].mean()),
                           y1_p10=float(np.percentile(y[:, 0], 10)),
                           y1_loss=float((y[:, 0] < 0).mean()))
    # D1-06: vol cap 8% and 15% at S = 0.6 and 1.17
    out["cap_sens"] = {f"{c:.2f}": {f"{S}": row(economics(F, S, n=N, sigmas=SIGMAS[SIGMAS <= c + 1e-9]))
                                    for S in (0.6, 1.17)} for c in (0.08, 0.15)}
    print("done", name, flush=True)
    return out


def fmt(res):
    L = []
    for r in res:
        L.append(f"\n## {r['firm']}  slots={r['slots']}  auto={r['auto']}  hold={r['hold']}")
        L.append(f"   not modeled: {r['unmodeled']}")
        for tag in ("capped", "uncapped"):
            L.append(f"   [{tag}]   S  sig_e sig_f  pass  evalDays  life  pay/acct  "
                     "net$/slot-yr  fees$/yr  ROS_after  fleet$/yr")
            for e in r[tag]:
                L.append(f"   {e['S']:5.2f} {e['sig_e']:5.2f} {e['sig_f']:5.2f} "
                         f"{e['p_pass']:5.2f} {e['t_eval']:8.0f} {e['life']:5.0f} "
                         f"{e['pay']:9,.0f} {e['net_yr']:13,.0f} {e['fees_yr']:9,.0f} "
                         f"{e['ros_after']:10.2f} {e['net_yr'] * r['slots']:10,.0f}")
        L.append(f"   min S for ROS_after>=20%: capped {r['min_S_capped']:.2f} | "
                 f"uncapped {r['min_S_uncapped']:.2f} | capped Gaussian-EOD "
                 f"{r['min_S_capped_gauss_eod']:.2f}")
        h = r["haircut_117"]
        L.append(f"   S=0.82 (1.17 x 0.7) capped: net/slot-yr {h['net_yr']:,.0f}  "
                 f"ROS_after {h['ros_after']:.2f}")
        for c, d in r.get("cap_sens", {}).items():
            L.append(f"   cap {c}: " + " | ".join(f"S={S} net/slot-yr {v['net_yr']:,.0f}" for S, v in d.items()))
        s = r["slot_117"]
        L.append(f"   S=1.17 capped slot-yr (sequential sim, yrs 2-3): mean {s['mean']:,.0f} "
                 f"p50 {s['p50']:,.0f} p10 {s['p10']:,.0f}; fleet x{r['slots']}: mean "
                 f"{s['mean'] * r['slots']:,.0f} p10 {s['p10'] * r['slots']:,.0f}")
    return "\n".join(L)


if __name__ == "__main__":
    names = [k for k in FIRMS if not sys.argv[1:] or any(a in k for a in sys.argv[1:])]
    with Pool(4) as p:
        res = p.map(run_firm, names, chunksize=1)
    path = HERE / "results.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.update({r["firm"]: r for r in res})
    path.write_text(json.dumps(old, indent=1))
    allres = [old[k] for k in FIRMS if k in old]
    (HERE / "results.txt").write_text(fmt(allres) + "\n")
    print(fmt(res))
