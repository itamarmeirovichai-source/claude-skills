"""$ per $100K FTMO Swing slot per year at each G2 variant's decisive OOS net Sharpe,
with the wave-3 F2-09 stress settings (agents/daily/w3-volrisk), vol caps 15% and 20%.
usage: python3 prop.py S1 [S2 ...]"""
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w3-volrisk"))
import stress_model as SM  # noqa: E402
from scenarios import SCEN, firm_params, scen_stress  # noqa: E402

FIRM = "FTMO Swing 2-Step 100K"


def one(S):
    sc = SCEN["F2-09"]
    F, st = firm_params(FIRM, sc), scen_stress(FIRM, sc)
    E = SM.eval_sim(F, S, SM.SIGMAS, 3000, 11, stress=st)
    Fd = SM.funded_sim(F, S, SM.SIGMAS, 3000, 12, stress=st)
    e = SM.economics(F, S, sigmas=SM.SIGMAS, E=E, Fd=Fd)
    out = {}
    for c in (0.15, 0.20):
        v, se, sf = SM.capped(e["grid"], SM.SIGMAS, c)
        out[c] = (v, se, sf)
    return S, out


if __name__ == "__main__":
    Ss = [float(x) for x in sys.argv[1:]]
    with Pool(4) as p:
        for S, out in p.map(one, Ss):
            print(f"S={S:+.3f}  " + "  ".join(
                f"cap {c:.0%}: ${v:,.0f}/slot-yr (sig_e {se:.0%}, sig_f {sf:.0%})"
                for c, (v, se, sf) in out.items()), flush=True)
