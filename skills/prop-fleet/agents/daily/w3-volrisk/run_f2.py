"""F2 run: stress scenarios F2-01..F2-11 (agents/prereg/F2.csv) for FTMO
Swing 2-Step, Blue Guardian 2-Step and Crypto Fund Trader 2-Phase, $100K.

Every (scenario, firm, S) job simulates the FULL sigma grid once
(common random numbers) and reads each vol cap off the same rate matrix.
Writes results.json next to this file; make_report.py turns it into tables.

usage: python3 run_f2.py [scenario-id ...]     (default: all)
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import stress_model as M
from scenarios import CAPS, FIRM_NAMES, S_GRID, S_MAIN, SCEN, firm_params, scen_stress

N = 3000
HERE = Path(__file__).parent
OUT = HERE / "results.json"


def job(args):
    sid, firm, S = args
    sc = SCEN[sid]
    F = firm_params(firm, sc)
    st = scen_stress(firm, sc)
    sd = sc.get("seed", 11)
    E = M.eval_sim(F, S, M.SIGMAS, N, sd, stress=st)
    Fd = M.funded_sim(F, S, M.SIGMAS, N, sd + 1, stress=st)
    e = M.economics(F, S, sigmas=M.SIGMAS, E=E, Fd=Fd)
    sig = M.SIGMAS
    caps = {}
    for c in CAPS:
        v, se, sf = M.capped(e["grid"], sig, c)
        i, j = int(np.argmin(abs(sig - se))), int(np.argmin(abs(sig - sf)))
        caps[f"{c:.2f}"] = dict(net=v, sig_e=se, sig_f=sf, p_pass=float(E["p_pass"][i]),
                                life=float(Fd["life"][j]), pay=float(Fd["pay"][j]),
                                breach_pre1=float(Fd["breach_pre1"][j]),
                                shield=float(Fd["shield"][j]), p_any=float(Fd["p_any"][j]))
    # the same-sigma rows let the report show pass/breach at a FIXED vol
    fixed = {f"{s:.2f}": dict(p_pass=float(E["p_pass"][k]), life=float(Fd["life"][k]),
                              breach_pre1=float(Fd["breach_pre1"][k]),
                              p_any=float(Fd["p_any"][k]), shield=float(Fd["shield"][k]),
                              diag=float(e["grid"][k, k]))
             for k, s in enumerate(sig)}
    print("done", sid, firm, S, flush=True)
    return dict(sid=sid, firm=firm, S=S, caps=caps, fixed=fixed)


def seq_job(args):
    """F2-07 / F2-11: calendar-order chain, refund paid on its real date."""
    sid, firm, S, cap, se, sf = args
    sc = SCEN[sid]
    src = SCEN[sc["seq_of"]]
    F = firm_params(firm, src)
    y = M.slot_years(F, S, se, sf, years=3, n=2000, stress=scen_stress(firm, src))
    st = y[:, 1:].mean(1)
    print("seq", sid, firm, S, cap, flush=True)
    return dict(sid=sid, firm=firm, S=S, cap=cap, sig_e=se, sig_f=sf,
                y1_mean=float(y[:, 0].mean()), y1_p10=float(np.percentile(y[:, 0], 10)),
                y1_loss=float((y[:, 0] < 0).mean()), ss_mean=float(st.mean()),
                ss_p10=float(np.percentile(st, 10)), ss_p50=float(np.median(st)),
                ss_loss=float((st < 0).mean()))


def main(ids):
    jobs = []
    for sid in ids:
        sc = SCEN[sid]
        if sc.get("seq_of"):
            continue
        for firm in FIRM_NAMES:
            if sc.get("only") and sc["only"] not in firm:
                continue
            for S in sc.get("S_list") or (S_GRID if sc.get("sgrid") else S_MAIN):
                jobs.append((sid, firm, S))
    # heavy jobs first
    jobs.sort(key=lambda j: -scen_stress(j[1], SCEN[j[0]]).get("sub", 4))
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    with Pool(4) as p:
        res = p.map(job, jobs, chunksize=1)
    for r in res:
        old.setdefault(r["sid"], {}).setdefault(r["firm"], {})[f"{r['S']:.2f}"] = r
    OUT.write_text(json.dumps(old, indent=1))
    # sequential runs reuse the sigma pair picked by their source scenario
    sj = []
    for sid in ids:
        src = SCEN[sid].get("seq_of")
        if not src:
            continue
        for firm in FIRM_NAMES:
            for S in SCEN[sid]["seq_S"]:
                for c in SCEN[sid]["seq_caps"]:
                    r = old[src][firm][f"{S:.2f}"]["caps"][f"{c:.2f}"]
                    sj.append((sid, firm, S, c, r["sig_e"], r["sig_f"]))
    if sj:
        with Pool(4) as p:
            res = p.map(seq_job, sj, chunksize=1)
        for r in res:
            old.setdefault(r["sid"], {}).setdefault(r["firm"], {})[
                f"{r['S']:.2f}@{r['cap']:.2f}"] = r
        OUT.write_text(json.dumps(old, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or list(SCEN))
