"""Time one F2-12 job (FTMO Swing 2-Step 100K, S = 1.0) on the sigma grid
restricted to <= 20% and on the full D1 grid, to size the re-run budget.
run_f2.log in the inherited record carries no timings."""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "w3-volrisk"))

import numpy as np  # noqa: E402

import stress_model as M  # noqa: E402
from scenarios import SCEN, firm_params, scen_stress  # noqa: E402

firm = "FTMO Swing 2-Step 100K"
sc = SCEN["F2-12"]
F = firm_params(firm, sc)
st = scen_stress(firm, sc)
print("stress:", st, flush=True)
print("firm:", F, flush=True)
print("SIGMAS:", M.SIGMAS, "HORIZON:", M.HORIZON, "SUB:", M.SUB, "TAX:", M.TAX, flush=True)
grids = [("le20", M.SIGMAS[M.SIGMAS <= 0.20 + 1e-9]), ("full", M.SIGMAS)]
for label, sig in grids:
    for S in (1.0,):
        w0, c0 = time.time(), time.process_time()
        E = M.eval_sim(F, S, sig, 3000, 11, stress=st)
        w1, c1 = time.time(), time.process_time()
        Fd = M.funded_sim(F, S, sig, 3000, 12, stress=st)
        w2, c2 = time.time(), time.process_time()
        e = M.economics(F, S, sigmas=sig, E=E, Fd=Fd)
        print(f"{label} k={len(sig)} S={S}: eval wall {w1-w0:.1f}s cpu {c1-c0:.1f}s | "
              f"funded wall {w2-w1:.1f}s cpu {c2-c1:.1f}s | net_yr {e['net_yr']:.0f} "
              f"sig_e {e['sig_e']:.2f} sig_f {e['sig_f']:.2f}", flush=True)
        for cap in (0.12, 0.15, 0.20):
            v, se, sf = M.capped(e["grid"], sig, cap)
            print(f"   cap {cap:.2f}: net {v:.0f} sig_e {se:.2f} sig_f {sf:.2f}", flush=True)
