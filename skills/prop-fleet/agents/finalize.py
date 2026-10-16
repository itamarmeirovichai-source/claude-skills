#!/usr/bin/env python3
"""finalize.py — writes one day's output of the agent organization to the repo.

Usage:  python3 finalize.py <result.json>

<result.json> is the object the prop-fleet-daily workflow returns. This script is
the only writer of board.md and ledger.csv: agents return text, this step puts
it on disk, so parallel agents never race on the same file.

- board.md   ← director.board_md
- ledger.csv ← director.ledger_rows, each given the next H#### id; rows whose
               column count does not match the header are rejected, not fixed
- daily/<date>/record.json ← the whole result, for audit
- daily/<date>/report_he.md ← the Hebrew report
"""
from __future__ import annotations

import csv
import io
import json
import sys

from pathlib import Path

HERE = Path(__file__).resolve().parent


def next_id(rows: list) -> int:
    nums = [int(r["id"][1:]) for r in rows if r.get("id", "").startswith("H")]
    return (max(nums) if nums else 0) + 1


def main(path: str) -> int:
    res = json.loads(Path(path).read_text())
    date = res.get("date") or "unknown-date"
    d = res.get("director") or {}
    if not d:
        print("no director output — nothing written to board or ledger")
        return 1

    day = HERE / "daily" / date
    day.mkdir(parents=True, exist_ok=True)
    (day / "record.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    (day / "report_he.md").write_text(d.get("report_he", ""))

    (HERE / "board.md").write_text(d["board_md"].rstrip() + "\n")

    ledger = HERE / "ledger.csv"
    text = ledger.read_text()
    reader = csv.DictReader(io.StringIO(text))
    header = reader.fieldnames
    rows = list(reader)
    nid = next_id(rows)
    added, rejected = [], []
    for raw in d.get("ledger_rows", []):
        cells = next(csv.reader([raw]))
        if cells and cells[0].startswith("H") and len(cells) == len(header):
            cells = cells[1:]
        if len(cells) != len(header) - 1:
            rejected.append(raw)
            continue
        added.append([f"H{nid:04d}"] + cells)
        nid += 1
    if added:
        buf = io.StringIO()
        csv.writer(buf).writerows(added)
        ledger.write_text(text.rstrip("\n") + "\n" + buf.getvalue())
    n = sum(int(r["count"] or 1) for r in csv.DictReader(io.StringIO(ledger.read_text())))
    print(f"date {date}: board written, {len(added)} ledger rows added, "
          f"{len(rejected)} rejected, N = {n}, edge_found = {d.get('edge_found')}")
    for r in rejected:
        print("  rejected:", r[:120])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
