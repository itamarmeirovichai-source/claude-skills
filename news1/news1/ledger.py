"""Append-only JSON-lines log. Every line carries the hash of the line before it."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

GENESIS = "0" * 64


def canonical(body: dict[str, Any]) -> str:
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def line_hash(prev: str, body: dict[str, Any]) -> str:
    return hashlib.sha256((prev + canonical(body)).encode()).hexdigest()


def read(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append(path: Path, bodies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries = read(path)
    prev = entries[-1]["hash"] if entries else GENESIS
    written = []
    for body in bodies:
        if "hash" in body or "prev" in body:
            raise ValueError("reserved field in entry")
        entry = {**body, "prev": prev, "hash": line_hash(prev, body)}
        prev = entry["hash"]
        written.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for entry in written:
            handle.write(canonical(entry) + "\n")
    return written


def verify(path: Path) -> tuple[bool, int, str]:
    prev = GENESIS
    count = 0
    for count, entry in enumerate(read(path), start=1):
        body = {k: v for k, v in entry.items() if k not in ("prev", "hash")}
        if entry.get("prev") != prev:
            return False, count, f"line {count}: broken link to the previous line"
        if entry.get("hash") != line_hash(prev, body):
            return False, count, f"line {count}: content does not match its hash"
        prev = entry["hash"]
    return True, count, "ok"
