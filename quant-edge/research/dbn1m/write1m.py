"""Render research/results/Q-00nn.md for the 1m rows from <ID>_is.json and <ID>_oos.json (numbers only)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(HERE.parent / "dbn1h")); sys.path.insert(0, str(HERE))
import kit
from run1m import DATASETS
def bp(v): return "nan" if v is None or v != v else f"{1e4*v:.2f}"
def main(rid, title, units="bp of notional per event"):
    I = json.load(open(HERE / f"{rid}_is.json")); O = json.load(open(HERE / f"{rid}_oos.json"))
    pre = json.load(open(ROOT / "research" / "prereg" / f"{rid}.json"))
    g, gi = O["gate_net1"], I["gate_net1"]; c = O["crit7"]
    L = [f"# {rid} — {title}: {O['verdict']}", "",
         f"Registered at commit 56c0f6f (research/prereg/{rid}.json) before the data purchase and before any code; code at 19f1fba and later. Split {pre['split']}. Series: {units}.", "",
         "## OOS decision (one read per dataset)", "", kit.GATE_HDR.replace("mean bp of account", "mean bp"),
         kit.gate_md("net 1x", g).replace(" bp per obs", ""), "",
         f"- Mean gross {bp(O['mean_gross'])} bp; net 1x {bp(g['mean'])} bp; net 2x {bp(O['mean_net2'])} bp.",
         f"- Deciding t_min {g['t_min']:.2f} vs bar {kit.BAR:.4f}; bootstrap lower (0.05/430) {bp(g['boot_lower_min'])} bp; bootstrap p5 {bp(g['boot_p5_min'])} bp; {g['boot_draws']} draws.",
         f"- Criterion 7: share of positive years {c['years_positive_share']:.2f}; tercile sums {[round(1e4*x,1) for x in c['tercile_sums']]} (bp, summed); neighbours net-1x means (bp) {{{', '.join(f'{k}: {bp(v)}' for k,v in c['neighbours'].items())}}}; one-bar delay {bp(c['delay_mean'])} bp.",
         f"- {O['power']}.", ""]
    extra = {k: v for k, v in O.items() if k.startswith(("leg_", "control", "mes_"))}
    if extra: L += [f"- Information only (no decision): {json.dumps(extra)}", ""]
    L += ["| year | net 1x sum (bp) | events |", "|---|---|---|"] + [f"| {y} | {1e4*v[0]:.1f} | {v[1]} |" for y, v in sorted(O["years"].items(), key=lambda kv: int(kv[0]))]
    L += ["", "## IS (information; read before the OOS run)", "",
          f"- n {gi['n']}; gross {bp(I['mean_gross'])} bp; net 1x {bp(gi['mean'])} bp; t_min {gi['t_min']:.2f}.",
          f"- Harness on {I['harness']['n']} sampled IS events: truncation changes {I['harness']['truncation']}, perturbation changes {I['harness']['perturbation']} (must be 0). Planted look-ahead: truncation changes {I['planted']['truncation']} of {I['planted']['n']} (must be > 0 — caught).", ""]
    ie = {k: v for k, v in I.items() if k.startswith(("leg_", "control", "mes_"))}
    if ie: L += [f"- IS information: {json.dumps(ie)}", ""]
    reads = [l.strip() for l in open(ROOT / "registry_reads.log") if f",{rid}," in l]
    L += ["## Reads (registry_reads.log)", "", "```"] + reads + ["```", "",
          f"Datasets: {', '.join(DATASETS[rid])} (sha256 pinned in data/manifest.csv at ingest, before the first read). Hold-out never read.", ""]
    (ROOT / "research" / "results" / f"{rid}.md").write_text("\n".join(L))
    print("wrote", rid, O["verdict"])
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
