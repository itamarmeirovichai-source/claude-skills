"""Telegram Desktop JSON export of a PUBLIC channel or group -> ``Post``.

Telegram Desktop ("Export chat history", format "Machine-readable JSON")
writes a ``result.json``. Two shapes exist:

* single chat: ``{"name", "type", "id", "messages": [...]}``
* whole account: ``{"chats": {"list": [chat, ...]}, ...}``

Only chats whose ``type`` is ``public_channel`` or ``public_supergroup`` are
read. A single-chat export of any other type is refused with ``ValueError``;
in a whole-account export the private chats are skipped without reading a
single message. This enforces the red line that PumpWatch only processes
data that is public at the source.

Message text is either a string or a list mixing strings and entity objects
(``{"type": "cashtag", "text": "$ABC"}``); both are flattened to plain text.
The day is taken from ``date_unixtime`` (UTC) when present, because ``date``
is in the exporting computer's local time zone.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ..models import Post
from ..text import extract_cashtags
from . import hash_author

PUBLIC_TYPES = frozenset({"public_channel", "public_supergroup"})
SOURCE = "telegram"


@dataclass
class ExportStats:
    """What happened during a parse, for the audit trail."""

    chats_read: int = 0
    chats_skipped_private: list[str] = field(default_factory=list)
    messages_seen: int = 0
    posts_kept: int = 0
    skipped_service: int = 0
    skipped_empty: int = 0
    skipped_untagged: int = 0
    skipped_bad_date: int = 0


def flatten_text(value: Any) -> str:
    """Join Telegram's string-or-entity-list text into one string."""

    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for part in value:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                parts.append(str(part.get("text", "")))
        return "".join(parts)
    return str(value)


def message_day(msg: dict) -> date | None:
    unix = msg.get("date_unixtime")
    if unix not in (None, ""):
        try:
            return datetime.fromtimestamp(int(unix), tz=timezone.utc).date()
        except (TypeError, ValueError, OverflowError, OSError):
            pass
    raw = msg.get("date")
    if isinstance(raw, str) and len(raw) >= 10:
        try:
            return date.fromisoformat(raw[:10])
        except ValueError:
            return None
    return None


def _author_raw(msg: dict, chat: dict) -> str:
    for key in ("from_id", "actor_id"):
        if msg.get(key):
            return str(msg[key])
    # Channel posts without a from_id are written by the channel itself.
    return f"chat{chat.get('id', chat.get('name', 'unknown'))}"


def _chat_posts(
    chat: dict,
    salt: str | bytes,
    known: Iterable[str] | None,
    keep_untagged: bool,
    stats: ExportStats,
) -> list[Post]:
    out: list[Post] = []
    stats.chats_read += 1
    for msg in chat.get("messages") or []:
        if not isinstance(msg, dict):
            continue
        stats.messages_seen += 1
        if msg.get("type", "message") != "message":
            stats.skipped_service += 1
            continue
        text = flatten_text(msg.get("text"))
        if not text.strip() and msg.get("text_entities"):
            text = flatten_text(msg["text_entities"])
        if not text.strip():
            stats.skipped_empty += 1
            continue
        day = message_day(msg)
        if day is None:
            stats.skipped_bad_date += 1
            continue
        tickers = extract_cashtags(text, known)
        if not tickers and not keep_untagged:
            stats.skipped_untagged += 1
            continue
        author = hash_author(_author_raw(msg, chat), salt, SOURCE)
        out.append(Post(SOURCE, author, day, text, tickers))
        stats.posts_kept += 1
    return out


def parse_telegram_export(
    data: dict,
    salt: str | bytes,
    known: Iterable[str] | None = None,
    keep_untagged: bool = False,
    stats: ExportStats | None = None,
) -> list[Post]:
    """Convert a parsed ``result.json`` into posts.

    ``known`` limits cashtags to a ticker universe. Posts that mention no
    ticker are dropped unless ``keep_untagged`` is set, because the engine
    files posts under their tickers and would ignore them anyway.
    """

    if not isinstance(data, dict):
        raise ValueError("Telegram export must be a JSON object")
    stats = stats if stats is not None else ExportStats()
    known = list(known) if known is not None else None

    if "messages" in data:
        kind = data.get("type")
        if kind not in PUBLIC_TYPES:
            raise ValueError(
                f"refusing Telegram chat of type {kind!r}: only public channels "
                f"and public supergroups may be processed"
            )
        return _chat_posts(data, salt, known, keep_untagged, stats)

    chats = (data.get("chats") or {}).get("list")
    if not isinstance(chats, list):
        raise ValueError("not a Telegram Desktop JSON export (no 'messages' or 'chats.list')")
    out: list[Post] = []
    for chat in chats:
        if not isinstance(chat, dict):
            continue
        if chat.get("type") not in PUBLIC_TYPES:
            stats.chats_skipped_private.append(str(chat.get("type")))
            continue
        out.extend(_chat_posts(chat, salt, known, keep_untagged, stats))
    return out


def load_telegram_export(
    path: str | Path,
    salt: str | bytes,
    known: Iterable[str] | None = None,
    keep_untagged: bool = False,
    stats: ExportStats | None = None,
) -> list[Post]:
    """Read ``result.json`` from disk and convert it into posts."""

    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return parse_telegram_export(data, salt, known, keep_untagged, stats)
