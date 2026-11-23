"""SQLite storage and the append-only, hash-chained event log."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS tokens (
    mint TEXT PRIMARY KEY,
    name TEXT, symbol TEXT, creator TEXT,
    launch_time REAL, launch_source TEXT, token_program TEXT,
    first_seen_at REAL NOT NULL,
    is_synthetic INTEGER NOT NULL DEFAULT 0,
    meta TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mint TEXT NOT NULL,
    kind TEXT NOT NULL,
    provider TEXT NOT NULL,
    observed_at REAL NOT NULL,
    ingested_at REAL NOT NULL,
    payload TEXT NOT NULL,
    is_synthetic INTEGER NOT NULL DEFAULT 0,
    stale INTEGER NOT NULL DEFAULT 0,
    missing TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS idx_obs_mint_time ON observations (mint, kind, observed_at);
CREATE TABLE IF NOT EXISTS raw_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL, url TEXT NOT NULL, fetched_at REAL NOT NULL,
    sha256 TEXT NOT NULL, body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mint TEXT NOT NULL, field TEXT NOT NULL,
    provider_a TEXT NOT NULL, value_a REAL, provider_b TEXT NOT NULL, value_b REAL,
    rel_diff REAL NOT NULL, observed_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL, mint TEXT NOT NULL, as_of REAL NOT NULL,
    ruleset TEXT NOT NULL, config_hash TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('candidate', 'rejected')),
    reasons TEXT NOT NULL, features TEXT NOT NULL, features_hash TEXT NOT NULL,
    recorded_at REAL NOT NULL,
    UNIQUE (book, mint)
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id INTEGER NOT NULL UNIQUE REFERENCES signals (id),
    book TEXT NOT NULL, mint TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'closed', 'unsellable', 'not_filled')),
    opened_at REAL, closed_at REAL,
    tokens REAL NOT NULL DEFAULT 0,
    cost_sol REAL NOT NULL DEFAULT 0,          -- SOL that left the paper account at entry, all-in
    proceeds_sol REAL NOT NULL DEFAULT 0,      -- SOL that came back at exit, net of all costs
    gross_pnl_sol REAL NOT NULL DEFAULT 0,     -- price effect incl. market impact, before fees
    fees_sol REAL NOT NULL DEFAULT 0,          -- venue fees + network costs + rent, both sides
    net_pnl_sol REAL NOT NULL DEFAULT 0,
    mark_price_sol REAL, exit_reason TEXT,
    partial INTEGER NOT NULL DEFAULT 0,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    detail TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS fills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id INTEGER NOT NULL REFERENCES positions (id),
    side TEXT NOT NULL CHECK (side IN ('buy', 'sell')),
    filled_at REAL NOT NULL, price_sol REAL NOT NULL, tokens REAL NOT NULL,
    quote_sol REAL NOT NULL, venue_fee_sol REAL NOT NULL, network_fee_sol REAL NOT NULL,
    model TEXT NOT NULL, uncertainty TEXT NOT NULL DEFAULT '{}', observation_id INTEGER
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL, type TEXT NOT NULL, payload TEXT NOT NULL,
    prev_hash TEXT NOT NULL, hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS provider_health (
    provider TEXT PRIMARY KEY,
    last_ok REAL, last_error REAL, last_error_text TEXT,
    error_count INTEGER NOT NULL DEFAULT 0, ok_count INTEGER NOT NULL DEFAULT 0,
    rate_limited_until REAL
);
CREATE TABLE IF NOT EXISTS backfill_cursors (      -- every launch found in the window: a clock made of signatures
    signature TEXT PRIMARY KEY, block_time REAL NOT NULL, slot INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cursor_time ON backfill_cursors (block_time, slot);
CREATE TABLE IF NOT EXISTS backfill_queue (        -- the systematic sample drawn from it
    signature TEXT PRIMARY KEY, block_time REAL NOT NULL, slot INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', mint TEXT, note TEXT
);
CREATE TABLE IF NOT EXISTS study (
    book TEXT PRIMARY KEY, plan TEXT NOT NULL, registered_at REAL NOT NULL
);
"""

GENESIS_HASH = "0" * 64


def connect(path: Path | str) -> sqlite3.Connection:
    """Open (and create if needed) the database. `:memory:` is accepted for tests."""
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 60000")   # several readers/writers may share one file (parallel backfill)
    if str(path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA)
    return conn


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def log_event(conn: sqlite3.Connection, type_: str, payload: dict[str, Any], ts: float | None = None) -> str:
    """Append an event. Each hash covers the previous hash, so edits and deletions are detectable."""
    ts = time.time() if ts is None else ts
    row = conn.execute("SELECT hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
    prev = row["hash"] if row else GENESIS_HASH
    body = canonical(payload)
    digest = hashlib.sha256(f"{prev}|{ts!r}|{type_}|{body}".encode()).hexdigest()
    conn.execute(
        "INSERT INTO events (ts, type, payload, prev_hash, hash) VALUES (?, ?, ?, ?, ?)",
        (ts, type_, body, prev, digest),
    )
    return digest


def verify_event_chain(conn: sqlite3.Connection) -> dict[str, Any]:
    """Recompute the chain. Returns {'ok': bool, 'count': int, 'first_bad_id': int | None}."""
    prev = GENESIS_HASH
    count = 0
    for row in conn.execute("SELECT id, ts, type, payload, prev_hash, hash FROM events ORDER BY id"):
        count += 1
        expected = hashlib.sha256(f"{prev}|{row['ts']!r}|{row['type']}|{row['payload']}".encode()).hexdigest()
        if row["prev_hash"] != prev or row["hash"] != expected:
            return {"ok": False, "count": count, "first_bad_id": row["id"]}
        prev = row["hash"]
    return {"ok": True, "count": count, "first_bad_id": None}


def upsert_token(conn: sqlite3.Connection, mint: str, *, is_synthetic: bool, now: float | None = None, **fields: Any) -> None:
    """Insert a token or fill in fields that are still empty. Never overwrites a known value with None."""
    now = time.time() if now is None else now
    meta = fields.pop("meta", None)
    conn.execute(
        "INSERT OR IGNORE INTO tokens (mint, first_seen_at, is_synthetic) VALUES (?, ?, ?)",
        (mint, now, int(is_synthetic)),
    )
    allowed = {"name", "symbol", "creator", "launch_time", "launch_source", "token_program"}
    for key, value in fields.items():
        if key not in allowed:
            raise KeyError(key)
        if value is not None:
            conn.execute(f"UPDATE tokens SET {key} = ? WHERE mint = ? AND {key} IS NULL", (value, mint))
    if meta:
        current = json.loads(conn.execute("SELECT meta FROM tokens WHERE mint = ?", (mint,)).fetchone()["meta"])
        current.update(meta)
        conn.execute("UPDATE tokens SET meta = ? WHERE mint = ?", (canonical(current), mint))


def add_observation(
    conn: sqlite3.Connection,
    mint: str,
    kind: str,
    provider: str,
    observed_at: float,
    payload: dict[str, Any],
    *,
    is_synthetic: bool,
    ingested_at: float | None = None,
    stale: bool = False,
    missing: Iterable[str] = (),
) -> int:
    cur = conn.execute(
        "INSERT INTO observations (mint, kind, provider, observed_at, ingested_at, payload, is_synthetic, stale, missing)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (mint, kind, provider, observed_at, time.time() if ingested_at is None else ingested_at,
         canonical(payload), int(is_synthetic), int(stale), canonical(sorted(missing))),
    )
    return int(cur.lastrowid or 0)


def observations(
    conn: sqlite3.Connection, mint: str, kind: str | None = None, *, as_of: float | None = None, after: float | None = None
) -> list[dict[str, Any]]:
    """Observations for a mint in time order. `as_of` is inclusive and is the look-ahead guard."""
    sql = "SELECT * FROM observations WHERE mint = ?"
    args: list[Any] = [mint]
    if kind is not None:
        sql += " AND kind = ?"
        args.append(kind)
    if as_of is not None:
        sql += " AND observed_at <= ?"
        args.append(as_of)
    if after is not None:
        sql += " AND observed_at > ?"
        args.append(after)
    sql += " ORDER BY observed_at, id"
    return [row_to_obs(r) for r in conn.execute(sql, args)]


def row_to_obs(row: sqlite3.Row) -> dict[str, Any]:
    d = dict(row)
    d["payload"] = json.loads(d["payload"])
    d["missing"] = json.loads(d["missing"])
    d["is_synthetic"] = bool(d["is_synthetic"])
    d["stale"] = bool(d["stale"])
    return d


def record_health(conn: sqlite3.Connection, provider: str, *, ok: bool, error: str | None = None,
                  rate_limited_until: float | None = None, now: float | None = None) -> None:
    now = time.time() if now is None else now
    conn.execute("INSERT OR IGNORE INTO provider_health (provider) VALUES (?)", (provider,))
    if ok:
        conn.execute("UPDATE provider_health SET last_ok = ?, ok_count = ok_count + 1 WHERE provider = ?", (now, provider))
    else:
        conn.execute(
            "UPDATE provider_health SET last_error = ?, last_error_text = ?, error_count = error_count + 1,"
            " rate_limited_until = COALESCE(?, rate_limited_until) WHERE provider = ?",
            (now, (error or "")[:300], rate_limited_until, provider),
        )
