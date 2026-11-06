#!/usr/bin/env python3
"""Rewrite quant-edge/data/MANIFEST.md (human table) from quant-edge/data/manifest.csv (machine source of truth)."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(ROOT / "data" / "manifest.csv", newline="", encoding="utf-8")))
cols = ["path", "dataset_id", "source", "licence_status", "rows", "start", "end", "sha256", "resolution", "tz", "notes"]
out = ["# Data manifest", "", "One row per dataset file under DATA_ROOT (`~/quant-edge-data/`). Generated from `manifest.csv` by `tools/render_manifest.py`;",
       "a path listed here is refused by the pre-commit hook. licence_status: ok | free | licensed | hold (crosscheck-only).", "",
       "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
for r in rows:
    out.append("| " + " | ".join((r.get(c) or "").replace("|", "/") for c in cols) + " |")
(ROOT / "data" / "MANIFEST.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"rendered {len(rows)} rows")
