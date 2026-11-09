import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
rid = sys.argv[1]; O = json.load(open(ROOT / "research" / "dbn1m" / f"{rid}_oos.json")); g = O["gate_net1"]
p = ROOT / "registry.csv"; rows = list(csv.DictReader(open(p, newline="", encoding="utf-8"))); cols = list(rows[0].keys())
for r in rows:
    if r["id"] == rid:
        r.update(result_mean_R=f"{1e4*g['mean']:.2f}", result_p5_R=f"{1e4*g['boot_p5_min']:.2f}",
                 result_units="bp of notional per event (Q-0021: bp of account per event-date), OOS net 1x; p5 = bootstrap 5th percentile",
                 passed_gate="no" if O["verdict"] != "PASS Gate 3" else "gate3", status="tested-fail" if O["verdict"] == "FAIL" else ("near-miss" if O["verdict"] == "NEAR-MISS" else "gate3-pass"))
        r["notes"] += f" | VERDICT 2026-11-09: {O['verdict']} (t_min {g['t_min']:.2f} vs 3.68; gross {1e4*O['mean_gross']:.2f} bp, net1 {1e4*g['mean']:.2f}, net2 {1e4*O['mean_net2']:.2f}; n {g['n']})"
w = csv.DictWriter(open(p, "w", newline="", encoding="utf-8"), fieldnames=cols); w.writeheader(); w.writerows(rows); print(rid, O["verdict"])
