"""F2-12 / F2-13 re-run, 2026-11-03 (quant-edge Economist, Department F).

FTMO Swing 2-Step 100K only. Every (scenario, S, seed) job simulates the
inherited D1 sigma grid restricted to sigma <= --sigmax (default 0.20: the
capped optimum at caps 12/15/20% only uses cells <= cap, so the restriction
changes nothing but the random stream) with the UNMODIFIED inherited code in
./w3-volrisk (stress_model.py, scenarios.py) and ./w1-prop (prop_model.py,
firms.py). Nothing here reads market data.

Per job it stores, for each cap c in {12, 15, 20}%: the best (sigma_e,
sigma_f) pair with both <= c, pre-tax net $/slot-year (renewal reward, as
D1/F2), pass probability, expected evaluation days (geometric re-buys),
funded life, payouts per funded account, breach shares, time to the first
payout, evaluations bought and funded accounts lost per slot-year, and the
job's wall / CPU seconds. Seeds: F2's base pair (eval 11, funded 12) and
F2-15's four extra pairs (101/102, 202/203, 303/304, 404/405).

A second stage (--seq) runs the inherited calendar chain (slot_years, n=2000
slots x 3 years, seed 21) at the base seed's (sigma_e, sigma_f) for each
(scenario, S, cap) and stores the year-1 and years-2-3 per-slot distribution
(mean, p10, p50, p90, P(loss)).

usage:
  python3 run_f2_rerun.py --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 \
      --seeds 11 101 202 303 404 --n 3000 --sigmax 0.20 --procs 4 \
      --out results_rerun.json
  python3 run_f2_rerun.py --seq --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 \
      --out results_rerun.json
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "w3-volrisk"))

import stress_model as M  # noqa: E402
from scenarios import SCEN, firm_params, scen_stress  # noqa: E402

FIRM = "FTMO Swing 2-Step 100K"
CAPS_DEFAULT = [0.12, 0.15, 0.20]
TD = M.TD


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def job(args):
    sid, S, seed, n, sigmax, caps = args
    sc = SCEN[sid]
    F = firm_params(FIRM, sc)
    st = scen_stress(FIRM, sc)
    sig = M.SIGMAS[M.SIGMAS <= sigmax + 1e-9]
    w0, c0 = time.time(), time.process_time()
    E = M.eval_sim(F, S, sig, n, seed, stress=st)
    Fd = M.funded_sim(F, S, sig, n, seed + 1, stress=st, keep_paths=True)
    e = M.economics(F, S, sigmas=sig, E=E, Fd=Fd)
    yearly = Fd["paths"]["yearly"]                      # (k, n, horizon) trader $ per day
    got = yearly > 0
    first = np.where(got.any(2), got.argmax(2), -1)     # first payout day per path
    p = np.clip(E["p_pass"], 1e-6, 1)
    t_eval = E["t_fail"] * (1 - E["p_pass"]) / p + E["t_pass"]
    f_eval = E["fee_fail"] * (1 - E["p_pass"]) / p + E["fee_pass"]
    out_caps = {}
    for c in caps:
        v, se, sf = M.capped(e["grid"], sig, c)
        i, j = int(np.argmin(abs(sig - se))), int(np.argmin(abs(sig - sf)))
        L = float(t_eval[i] + Fd["life"][j])            # one renewal cycle, trading days
        fj = first[j]
        anyp = fj >= 0
        t_first_f = float(fj[anyp].mean()) if anyp.any() else float("nan")
        fees = float(f_eval[i]) + (F.get("activation", 0.0) + F.get("funded_fixed", 0.0)) \
            + F.get("fixed_year", 0.0) * L / TD
        refund = F.get("refund", 0.0) * float(Fd["p_refund"][j])
        out_caps[f"{c:.2f}"] = dict(
            net=float(v), sig_e=float(se), sig_f=float(sf),
            p_pass=float(E["p_pass"][i]), t_pass=float(E["t_pass"][i]),
            t_fail=float(E["t_fail"][i]), t_eval=float(t_eval[i]),
            attempts=float(1 / p[i]), fee_eval=float(f_eval[i]),
            life=float(Fd["life"][j]), pay=float(Fd["pay"][j]),
            n_pay=float(Fd["n_pay"][j]), p_any=float(Fd["p_any"][j]),
            p_refund=float(Fd["p_refund"][j]), breach=float(Fd["breach"][j]),
            breach_pre1=float(Fd["breach_pre1"][j]), survive=float(Fd["survive"][j]),
            cycle_days=L, fees_cycle=fees, refund_cycle=refund,
            pay_cycle=float(Fd["pay"][j]),
            fees_yr=fees / L * TD,
            evals_per_slot_yr=float(1 / p[i]) * TD / L,
            failed_evals_per_slot_yr=float(1 / p[i] - 1) * TD / L,
            funded_per_slot_yr=TD / L,
            funded_breached_per_slot_yr=float(Fd["breach"][j]) * TD / L,
            t_first_payout_funded=t_first_f,
            t_first_payout_total=float(t_eval[i]) + t_first_f,
            p_first_payout_given_funded=float(anyp.mean()),
        )
    fixed = {f"{s:.2f}": dict(p_pass=float(E["p_pass"][k]), life=float(Fd["life"][k]),
                              breach_pre1=float(Fd["breach_pre1"][k]), p_any=float(Fd["p_any"][k]),
                              diag=float(e["grid"][k, k]))
             for k, s in enumerate(sig)}
    w1, c1 = time.time(), time.process_time()
    meta = dict(n=n, k=int(len(sig)), sigmas=[float(s) for s in sig], seed_eval=seed,
                seed_funded=seed + 1, wall_s=w1 - w0, cpu_s=c1 - c0, stress=st,
                firm=F, finished=_now())
    print(f"done {sid} S={S} seed={seed} wall {w1-w0:.0f}s cpu {c1-c0:.0f}s "
          f"net12 {out_caps['0.12']['net']:.0f} net15 {out_caps['0.15']['net']:.0f} "
          f"net20 {out_caps['0.20']['net']:.0f}", flush=True)
    return dict(sid=sid, S=S, seed=seed, caps=out_caps, fixed=fixed, meta=meta)


def seq_job(args):
    sid, S, cap, se, sf, n = args
    sc = SCEN[sid]
    F = firm_params(FIRM, sc)
    st = scen_stress(FIRM, sc)
    w0, c0 = time.time(), time.process_time()
    y = M.slot_years(F, S, se, sf, years=3, n=n, seed=21, stress=st)
    w1, c1 = time.time(), time.process_time()
    y1, ss = y[:, 0], y[:, 1:].mean(1)
    def dist(x):
        return dict(mean=float(x.mean()), p10=float(np.percentile(x, 10)),
                    p50=float(np.median(x)), p90=float(np.percentile(x, 90)),
                    p_loss=float((x < 0).mean()), se_mean=float(x.std(ddof=1) / np.sqrt(len(x))))
    print(f"seq {sid} S={S} cap={cap} wall {w1-w0:.0f}s cpu {c1-c0:.0f}s "
          f"y1 mean {y1.mean():.0f} ss mean {ss.mean():.0f}", flush=True)
    return dict(sid=sid, S=S, cap=cap, sig_e=se, sig_f=sf, n=n, seed=21,
                year1=dist(y1), years23=dist(ss), year2=dist(y[:, 1]), year3=dist(y[:, 2]),
                wall_s=w1 - w0, cpu_s=c1 - c0, finished=_now())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scen", nargs="+", default=["F2-12", "F2-13"])
    ap.add_argument("--S", nargs="+", type=float, default=[1.0, 1.5, 2.0, 2.4, 3.0])
    ap.add_argument("--seeds", nargs="+", type=int, default=[11])
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--sigmax", type=float, default=0.20)
    ap.add_argument("--caps", nargs="+", type=float, default=CAPS_DEFAULT)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--out", default="results_rerun.json")
    ap.add_argument("--seq", action="store_true", help="calendar-chain stage")
    ap.add_argument("--seq_n", type=int, default=2000)
    a = ap.parse_args()
    out = HERE / a.out
    old = json.loads(out.read_text()) if out.exists() else {}
    t0 = time.time()
    print(f"start {_now()} args {vars(a)}", flush=True)
    if not a.seq:
        jobs = [(sid, S, sd, a.n, a.sigmax, a.caps) for sid in a.scen for S in a.S for sd in a.seeds]
        # most expensive first: low S keeps evaluation paths alive longest
        jobs.sort(key=lambda j: j[1])
        with Pool(a.procs) as p:
            res = p.map(job, jobs, chunksize=1)
        cpu = 0.0
        for r in res:
            old.setdefault(r["sid"], {}).setdefault(f"{r['S']:.2f}", {})[str(r["seed"])] = r
            cpu += r["meta"]["cpu_s"]
        out.write_text(json.dumps(old, indent=1))
        print(f"grid stage: {len(res)} jobs, cpu {cpu/60:.1f} min, wall {(time.time()-t0)/60:.1f} min",
              flush=True)
    else:
        sj = []
        for sid in a.scen:
            for S in a.S:
                base = old[sid][f"{S:.2f}"]["11"]["caps"]
                for c in a.caps:
                    r = base[f"{c:.2f}"]
                    sj.append((sid, S, c, r["sig_e"], r["sig_f"], a.seq_n))
        with Pool(a.procs) as p:
            res = p.map(seq_job, sj, chunksize=1)
        cpu = 0.0
        for r in res:
            old.setdefault("seq", {}).setdefault(r["sid"], {})[f"{r['S']:.2f}@{r['cap']:.2f}"] = r
            cpu += r["cpu_s"]
        out.write_text(json.dumps(old, indent=1))
        print(f"seq stage: {len(res)} jobs, cpu {cpu/60:.1f} min, wall {(time.time()-t0)/60:.1f} min",
              flush=True)
    print(f"end {_now()}", flush=True)


if __name__ == "__main__":
    main()
