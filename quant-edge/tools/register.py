#!/usr/bin/env python3
"""Pre-registration Officer's tool: validate and append a program row to quant-edge/registry.csv.

Usage: python3 quant-edge/tools/register.py <row.json> [--registry quant-edge/registry.csv] [--dry-run]

Gate 1 fields are mandatory. The row is appended with source=program, status=registered and registered_commit=PENDING;
the Director commits, then `python3 quant-edge/tools/register.py --stamp <id> <commit>` writes the commit hash. Commit order
is the proof: the row's commit must be older than any code specific to the variant. The count column is never lowered.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE.parent / "registry.csv"
COLUMNS = ["id", "date", "owner", "source", "family", "lane", "status", "hypothesis", "rules", "parameters", "grid",
           "sign", "instruments", "holding", "firm_structure", "data", "data_sha256", "split", "vol_scaler",
           "guard_fraction", "decay_haircut", "cost_model", "decision_rule", "count", "rules_fixed_before_test",
           "result_mean_R", "result_p5_R", "result_units", "passed_gate", "registered_commit", "notes"]
REQUIRED = ["id", "date", "owner", "family", "lane", "hypothesis", "rules", "parameters", "grid", "sign", "instruments",
            "holding", "firm_structure", "data", "data_sha256", "split", "vol_scaler", "guard_fraction", "decay_haircut",
            "cost_model", "decision_rule", "count"]
ID_RE = re.compile(r"^(Q-\d{4}|CAL(-[A-Z0-9]+)?|PF-\d{4})$")
SIGNS = {"long", "short", "long-short-fixed", "unfixed(2 counts)"}
FIRM = {"intraday-futures", "overnight-session-futures", "ftmo-swing", "ftmo-intraday-cfd", "portfolio"}
MAX_FAMILY_VARIANTS = 5


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(row: dict, existing: list) -> list:
    errs = []
    for k in REQUIRED:
        if not str(row.get(k, "")).strip():
            errs.append(f"missing {k}")
    if not ID_RE.match(row.get("id", "")):
        errs.append("id must be Q-nnnn, CAL or PF-nnnn")
    if any(r["id"] == row.get("id") for r in existing):
        errs.append(f"id {row.get('id')} already exists (rows are never rewritten)")
    if row.get("sign") not in SIGNS:
        errs.append(f"sign must be one of {sorted(SIGNS)}")
    c = str(row.get("count", "")).strip()
    if not c.isdigit() or int(c) < 1:
        errs.append("count must be a positive integer (an unfixed sign is 2)")
    if row.get("sign") == "unfixed(2 counts)" and c != "2":
        errs.append("unfixed sign must carry count 2")
    if row.get("firm_structure") not in FIRM:
        errs.append(f"firm_structure must be one of {sorted(FIRM)}")
    split = row.get("split", "")
    if not re.search(r"IS=\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2};OOS=\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2};HOLDOUT=2025-01-01\.\.", split):
        errs.append("split must read IS=a..b;OOS=c..d;HOLDOUT=2025-01-01.. (ISO dates)")
    else:
        m = re.search(r"OOS=(\d{4})-(\d{2})-\d{2}\.\.(\d{4})-(\d{2})-\d{2}", split)
        yrs = (int(m.group(3)) + int(m.group(4)) / 12) - (int(m.group(1)) + int(m.group(2)) / 12)
        if yrs < 5 - 1e-9 and "post-change" not in row.get("notes", "").lower():
            errs.append(f"OOS is {yrs:.1f} years; under 5 is allowed only after an institutional change date, stated in notes as 'post-change'")
    try:
        g = float(row.get("guard_fraction", ""))
        if not (0.5 <= g <= 0.9):
            errs.append("guard_fraction must be in [0.5, 0.9] (default 0.7)")
    except ValueError:
        errs.append("guard_fraction must be a number")
    try:
        h = float(row.get("decay_haircut", ""))
        if not (0.3 <= h <= 0.8):
            errs.append("decay_haircut must be in [0.3, 0.8] (0.5 published, 0.7 original)")
    except ValueError:
        errs.append("decay_haircut must be a number")
    fam = row.get("family", "")
    n_fam = sum(int(r["count"] or 0) for r in existing if r.get("family") == fam and r.get("source") == "program")
    if n_fam + int(c or 0) > MAX_FAMILY_VARIANTS:
        errs.append(f"family {fam} would hold {n_fam + int(c or 0)} counted variants; the cap is {MAX_FAMILY_VARIANTS}")
    if "2x" not in row.get("cost_model", "").lower() and "2×" not in row.get("cost_model", ""):
        errs.append("cost_model must state the 1x floors and that the 2x run is attached")
    for k in ("result_mean_R", "result_p5_R", "passed_gate"):
        if str(row.get(k, "")).strip():
            errs.append(f"{k} must be empty at registration")
    return errs


def append(row: dict, registry: Path) -> None:
    out = {k: "" for k in COLUMNS}
    out.update({k: str(v) for k, v in row.items() if k in COLUMNS})
    out["source"] = "program"
    out["status"] = "registered"
    out["rules_fixed_before_test"] = "yes"
    out["registered_commit"] = out.get("registered_commit") or "PENDING"
    with open(registry, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNS).writerow(out)


def stamp(id_: str, commit: str, registry: Path) -> None:
    rows = load(registry)
    hit = False
    for r in rows:
        if r["id"] == id_:
            if r["registered_commit"] not in ("", "PENDING"):
                raise SystemExit(f"{id_} already stamped with {r['registered_commit']}")
            r["registered_commit"] = commit
            hit = True
    if not hit:
        raise SystemExit(f"{id_} not found")
    with open(registry, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader(); w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("row", nargs="?")
    ap.add_argument("--registry", default=str(REGISTRY))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stamp", nargs=2, metavar=("ID", "COMMIT"))
    a = ap.parse_args(argv)
    reg = Path(a.registry)
    if a.stamp:
        stamp(a.stamp[0], a.stamp[1], reg); print(f"stamped {a.stamp[0]} {a.stamp[1]}"); return 0
    row = json.loads(Path(a.row).read_text(encoding="utf-8"))
    errs = validate(row, load(reg))
    if errs:
        print("REFUSED:\n  - " + "\n  - ".join(errs)); return 2
    if a.dry_run:
        print(f"ok: {row['id']} would be appended (count {row['count']})"); return 0
    append(row, reg)
    print(f"registered {row['id']} count {row['count']}; now COMMIT the registry before any code specific to it, then --stamp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
