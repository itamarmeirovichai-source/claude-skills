"""Generic CSV of public posts -> ``Post``.

Required header: ``source,author,day,text``. An optional ``tickers`` column
(separated by ``;``, ``,`` or spaces) overrides cashtag extraction, for
sources that tag stocks by name or numeric code instead of ``$TICKER``.

``author`` is the raw platform id and is hashed with the salt on load, so
handles never reach the dataset. ``day`` is ``YYYY-MM-DD``; a full ISO
timestamp is accepted and cut to its date (convert to UTC before export).
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path
from typing import Iterable, TextIO

from ..models import Post
from ..text import extract_cashtags
from . import hash_author

REQUIRED = ("source", "author", "day", "text")
_SPLIT = re.compile(r"[;,\s]+")


def _parse_day(raw: str, line: int) -> date:
    raw = (raw or "").strip()
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        raise ValueError(f"line {line}: bad day {raw!r}, expected YYYY-MM-DD") from None


def _tickers(row: dict, text: str, known: list[str] | None) -> tuple[str, ...]:
    explicit = (row.get("tickers") or "").strip()
    if not explicit:
        return extract_cashtags(text, known)
    found = [t.lstrip("$").upper() for t in _SPLIT.split(explicit) if t.strip("$ ")]
    if known is not None:
        allowed = {k.upper() for k in known}
        found = [t for t in found if t in allowed]
    return tuple(dict.fromkeys(found))


def read_posts_csv(
    fh: TextIO,
    salt: str | bytes,
    known: Iterable[str] | None = None,
    keep_untagged: bool = False,
) -> list[Post]:
    """Parse posts from an open CSV file. Raises ``ValueError`` on bad rows."""

    reader = csv.DictReader(fh)
    header = [h.strip().lower() for h in (reader.fieldnames or [])]
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        raise ValueError(f"CSV is missing column(s): {', '.join(missing)}")
    reader.fieldnames = header
    known = list(known) if known is not None else None
    out: list[Post] = []
    for row in reader:
        line = reader.line_num
        source = (row.get("source") or "").strip().lower()
        author = (row.get("author") or "").strip()
        text = row.get("text") or ""
        if not source or not author:
            raise ValueError(f"line {line}: source and author are required")
        day = _parse_day(row.get("day") or "", line)
        if not text.strip():
            continue
        tickers = _tickers(row, text, known)
        if not tickers and not keep_untagged:
            continue
        out.append(Post(source, hash_author(author, salt, source), day, text, tickers))
    return out


def load_posts_csv(
    path: str | Path,
    salt: str | bytes,
    known: Iterable[str] | None = None,
    keep_untagged: bool = False,
) -> list[Post]:
    """Read a UTF-8 CSV file (a BOM from Excel is tolerated)."""

    with open(path, encoding="utf-8-sig", newline="") as fh:
        return read_posts_csv(fh, salt, known, keep_untagged)
