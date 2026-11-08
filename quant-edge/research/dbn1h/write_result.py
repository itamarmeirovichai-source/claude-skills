"""Render research/results/Q-00nn.md from the run JSONs (numbers only; prose passed in)."""
import json, math, sys, subprocess, csv
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); import kit


def bp(v): return f"{1e4*v:.2f}"


def gate_rows(r, keys):
    out = [kit.GATE_HDR]
    for name, k in keys:
        g = r[k]
        out.append(kit.gate_md(name, g))
    return "\n".join(out)


def manifest_lines(datasets):
    man = {row["dataset_id"]: row for row in csv.DictReader(open(ROOT / "data/manifest.csv"))}
    lines = []
    for ds in datasets:
        p = Path.home() / "quant-edge-data" / man[ds]["path"]
        rec = subprocess.check_output(["sha256sum", str(p)], text=True).split()[0]
        lines.append(f"- Data `{ds}` sha256: manifest {man[ds]['sha256']} = recomputed {rec} (ok={man[ds]['sha256'] == rec}).")
    return "\n".join(lines)


def reads(rid):
    return "\n".join(l.strip() for l in open(ROOT / "registry_reads.log") if f",{rid}," in l)


def years_md(r):
    y = r["years"]; ks = sorted(y["sum"].keys())
    rows = ["| year | obs | net1x (% of account) |", "|---|---|---|"]
    rows += [f"| {k} | {y['count'][k]} | {100*y['sum'][k]:.3f}% |" for k in ks]
    pos = sum(1 for k in ks if y["sum"][k] > 0)
    return "\n".join(rows), pos, len(ks)
