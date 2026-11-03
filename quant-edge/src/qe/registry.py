"""Registry access: every hypothesis ever counted lives in quant-edge/registry.csv.

Program rows write `split` as `IS=YYYY-MM-DD..YYYY-MM-DD;OOS=YYYY-MM-DD..YYYY-MM-DD;HOLDOUT=YYYY-MM-DD..`
and `data` as a comma-separated list of dataset_ids from quant-edge/data/manifest.csv.
"""
import csv
from dataclasses import dataclass
from typing import Dict, Optional
from . import paths


class UnregisteredHypothesisError(RuntimeError):
    """Raised when a script asks for market data under an id that has no registry row."""


@dataclass(frozen=True)
class Window:
    start: str          # inclusive, ISO date
    end: Optional[str]  # inclusive, ISO date; None = open-ended


@dataclass(frozen=True)
class Row:
    id: str
    status: str
    source: str
    datasets: tuple
    windows: Dict[str, Window]
    count: int
    sign: str
    raw: dict


def parse_split(split: str) -> Dict[str, Window]:
    out: Dict[str, Window] = {}
    for part in (split or "").split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        name, rng = part.split("=", 1)
        if ".." not in rng:
            raise ValueError(f"bad window {part!r}: expected START..END")
        a, b = rng.split("..", 1)
        out[name.strip().lower()] = Window(a.strip(), b.strip() or None)
    return out


def load_rows(path=None) -> Dict[str, Row]:
    path = path or paths.REGISTRY_CSV
    rows: Dict[str, Row] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = (r.get("count") or "").strip()
            rows[r["id"]] = Row(
                id=r["id"], status=r.get("status", ""), source=r.get("source", ""),
                datasets=tuple(x.strip() for x in (r.get("data") or "").split(",") if x.strip()),
                windows=parse_split(r.get("split", "")) if r.get("source") == "program" else {},
                count=int(c) if c.isdigit() else 0, sign=r.get("sign", ""), raw=r,
            )
    return rows


def get(id_: str, path=None) -> Row:
    rows = load_rows(path)
    if id_ not in rows:
        raise UnregisteredHypothesisError(
            f"{id_!r} has no row in {path or paths.REGISTRY_CSV}; register it (commit first) before touching market data")
    return rows[id_]
