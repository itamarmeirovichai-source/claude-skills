"""Append-only, hash-chained alert log (the Sentinel flight-recorder idea).

Every record carries the SHA-256 of the previous one, so editing, deleting or
reordering any past alert breaks the chain and ``verify`` reports where.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .models import Alert

GENESIS = "0" * 64


def _digest(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@dataclass
class VerifyResult:
    ok: bool
    records: int
    broken_at: int | None = None
    reason: str = ""


class AuditLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _last_hash(self) -> str:
        if not self.path.exists():
            return GENESIS
        last = GENESIS
        with self.path.open(encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    last = json.loads(line)["hash"]
        return last

    def append(self, alert: Alert, engine_version: str, config_hash: str) -> dict:
        body = {
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "engine_version": engine_version,
            "config_hash": config_hash,
            "alert": alert.to_dict(),
            "prev": self._last_hash(),
        }
        record = {**body, "hash": _digest(body)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def verify(self) -> VerifyResult:
        if not self.path.exists():
            return VerifyResult(True, 0)
        prev = GENESIS
        n = 0
        with self.path.open(encoding="utf-8") as fh:
            for i, line in enumerate(fh, start=1):
                if not line.strip():
                    continue
                n += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    return VerifyResult(False, n, i, "line is not valid JSON")
                claimed = rec.pop("hash", None)
                if rec.get("prev") != prev:
                    return VerifyResult(False, n, i, "chain broken: prev hash does not match")
                if _digest(rec) != claimed:
                    return VerifyResult(False, n, i, "record content was modified")
                prev = claimed
        return VerifyResult(True, n)


def config_fingerprint(cfg) -> str:
    from dataclasses import asdict

    return _digest(asdict(cfg))[:16]
