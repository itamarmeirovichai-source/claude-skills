"""Outcome-free provenance check: recompute the sha256 of a manifest dataset and compare it with the manifest and with
the registry row's `data_sha256` pin (briefs/inherited-method-lessons.md, "Pin every file by sha256 and refuse on
mismatch"). Hashes bytes only; never parses market data and never computes P&L."""
from __future__ import annotations

import csv
from typing import Optional

from .. import paths, registry
from ..ingest.common import sha256_path


def row_pins(id_: str, registry_path=None) -> dict:
    raw = registry.get(id_, registry_path).raw.get("data_sha256", "") or ""
    out = {}
    for part in raw.replace(",", ";").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def verify(id_: str, dataset_id: str, *, registry_path=None, manifest_path=None, data_root=None) -> dict:
    """Return {dataset, manifest_sha256, row_sha256, computed_sha256, ok}; raises on mismatch."""
    with open(manifest_path or paths.MANIFEST_CSV, newline="", encoding="utf-8") as f:
        man = {r["dataset_id"]: r for r in csv.DictReader(f)}
    m = man[dataset_id]
    p = (data_root or paths.DATA_ROOT)
    computed = sha256_path(p.joinpath(m["path"]) if hasattr(p, "joinpath") else p)
    pin = row_pins(id_, registry_path).get(dataset_id)
    ok = computed == m["sha256"] and (pin is None or pin == computed)
    res = {"dataset": dataset_id, "manifest_sha256": m["sha256"], "row_sha256": pin, "computed_sha256": computed, "ok": ok}
    if not ok:
        raise RuntimeError(f"sha256 mismatch for {dataset_id}: {res}")
    return res


def manifest_vs_disk(dataset_id: str, *, manifest_path=None, data_root=None) -> dict:
    """sha256 in the manifest vs the file on disk (for rows registered before their data existed, pinned at ingest)."""
    import csv as _csv
    from .. import paths as _p
    from ..ingest import common as _c
    man = {r["dataset_id"]: r for r in _csv.DictReader(open(manifest_path or _p.MANIFEST_CSV, newline="", encoding="utf-8"))}
    from pathlib import Path as _P
    rec = _c.sha256_path(_P(data_root or _p.DATA_ROOT) / man[dataset_id]["path"])
    return {"manifest": man[dataset_id]["sha256"], "recomputed": rec, "ok": man[dataset_id]["sha256"] == rec}
