"""Backtest data collection: an UNSELECTED sample of past Pump.fun launches, read from the chain.

Why this is not a cherry-picked list
  Every `create` transaction is signed by Pump.fun's mint-authority address, so that address's signature
  history is a complete list of launches. The sample is every k-th launch in a time window fixed before any
  outcome is read.

How the past is read without looking ahead
  `getSignaturesForAddress(curve, before=<signature of some later transaction>)` returns the curve's history
  up to that moment. The list of all launches doubles as a clock of signatures, so "the curve state at
  launch + T" is the state after the curve's last successful transaction at or before that time.

Price needs one number
  The creation event states the curve's starting virtual reserves and its quote currency. From then on,
  virtual tokens = starting virtual tokens − tokens that have left the curve account, and virtual SOL =
  k ÷ virtual tokens. "Mayhem" launches use the same curve (an automated agent holds a second billion tokens
  and trades for 24 hours), so they are read the same way. Curves quoted in something other than SOL are
  recorded as unreadable, not approximated.

Read-only. Uses only the allow-listed RPC methods.
"""

from __future__ import annotations

import base64
import bisect
import dataclasses
import json
import sqlite3
import struct
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from . import amm, db, paper, policy
from .config import Settings
from .providers import solana_rpc
from .providers.base import HttpClient, ProviderError
from .providers.solana_rpc import NATIVE_SOL, b58decode, b58encode

MINT_AUTHORITY = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"   # Pump.fun mint authority (official docs)
OUTCOME_WINDOW_S = 100 + 1800 + 180          # entry offset + longest hold + room for the exit to fill
STRUCTURE_WINDOW_S = 3                        # the creation slot lies well inside the first 3 seconds
def parse_create_event(raw: bytes, mint: str) -> dict[str, Any] | None:
    """Decode a Pump.fun CreateEvent (layout from the official IDL) if `raw` is one for `mint`."""
    if raw[:8] != CREATE_EVENT:
        return None
    try:
        offset = 8                                   # event discriminator
        for _ in range(3):                           # name, symbol, uri
            (length,) = struct.unpack_from("<I", raw, offset)
            offset += 4 + length
        if raw[offset:offset + 32] != b58decode(mint):
            return None
        curve, creator = raw[offset + 32:offset + 64], raw[offset + 96:offset + 128]
        offset += 128
        _ts, virtual_tokens, _vs, real_tokens, supply = struct.unpack_from("<qQQQQ", raw, offset)
        offset += 40 + 32                            # the five numbers, then the token program
        mayhem = bool(raw[offset])
        quote = raw[offset + 2:offset + 34]
        (virtual_quote,) = struct.unpack_from("<Q", raw, offset + 34)
    except (struct.error, IndexError, ValueError):
        return None
    return {"curve": b58encode(curve), "creator": b58encode(creator), "virtual_tokens": virtual_tokens / 1e6, "real_tokens": real_tokens / 1e6,
            "supply": supply / 1e6, "is_mayhem": mayhem, "quote_mint": b58encode(quote), "virtual_quote_units": virtual_quote}


def observation_grid(decision_delay_s: float) -> list[float]:
    """Offsets from launch at which the curve state is recorded: just before the decision, then every 30 s
    for five minutes and every 60 s to the end of the outcome window."""
    first = decision_delay_s - 5
    return [first, first + 15, *range(130, 430, 30), *range(460, OUTCOME_WINDOW_S + 1, 60)]


TRADE_EVENT = bytes.fromhex("bddb7fd34ee661ee")    # first 8 bytes of sha256("event:TradeEvent"), as seen on-chain
CREATE_EVENT = bytes.fromhex("1b72a94ddeeb6376")   # first 8 bytes of sha256("event:CreateEvent")


def event_payloads(tx: dict[str, Any]) -> list[bytes]:
    out = []
    for line in (tx.get("meta") or {}).get("logMessages") or []:
        if isinstance(line, str) and line.startswith("Program data: "):
            try:
                out.append(base64.b64decode(line[14:]))
            except ValueError:
                continue
    return out


def last_trade_state(tx: dict[str, Any], mint: str) -> dict[str, float] | None:
    """Curve reserves after the last trade of `mint` in this transaction, from its TradeEvent (official IDL
    layout: mint, sol_amount, token_amount, is_buy, user, timestamp, then the four reserves)."""
    key = b58decode(mint)
    state = None
    for raw in event_payloads(tx):
        if raw[:8] == TRADE_EVENT and len(raw) >= 129 and raw[8:40] == key:
            virtual_sol, virtual_tokens, real_sol, real_tokens = struct.unpack_from("<QQQQ", raw, 97)
            state = {"virtual_sol": virtual_sol / 1e9, "virtual_tokens": virtual_tokens / 1e6, "real_sol": real_sol / 1e9, "real_tokens": real_tokens / 1e6}
    return state


def curve_payload(state: dict[str, float], state_time: float, signature: str, source: str) -> dict[str, Any]:
    """A market observation from exact curve reserves. `liquidity_sol` is the real SOL a seller can take out."""
    res = amm.Reserves(state["virtual_sol"], state["virtual_tokens"])
    return {"venue": "curve", "price_sol": res.price, "quote_reserve_sol": res.quote, "base_reserve": res.base,
            "liquidity_sol": state["real_sol"], "curve_real_sol": state["real_sol"], "curve_real_tokens": state["real_tokens"],
            "fdv_sol": res.market_cap(), "fdv_definition": "price × 1e9 curve supply, in SOL",
            "market_cap_usd": None, "market_cap_definition": "not computed in the backtest",
            "reserve_model": f"exact curve reserves from the {source} (on-chain)", "state_time": state_time, "state_signature": signature}


# --------------------------------------------------------------------------------------------
# the population and the sample
# --------------------------------------------------------------------------------------------

def list_launches(client: HttpClient, url: str, since: float, *, max_pages: int = 120) -> tuple[list[dict[str, Any]], bool]:
    """Successful mint-authority transactions newer than `since`, oldest first. Returns (rows, reached_since)."""
    rows: list[dict[str, Any]] = []
    before: str | None = None
    for _ in range(max_pages):
        opts: dict[str, Any] = {"limit": 1000}
        if before:
            opts["before"] = before
        page = solana_rpc.call(client, url, "getSignaturesForAddress", [MINT_AUTHORITY, opts]).data.get("result") or []
        rows.extend(r for r in page if not r.get("err") and r.get("blockTime"))
        if len(page) < 1000 or (page[-1].get("blockTime") or 0) < since:
            return sorted((r for r in rows if r["blockTime"] >= since), key=lambda r: (r["slot"], r["signature"])), True
        before = page[-1]["signature"]
    return sorted(rows, key=lambda r: (r["slot"], r["signature"])), False


def systematic_sample(rows: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    """Every k-th row, k chosen so about n rows are taken. No information about outcomes is used."""
    if n <= 0 or not rows:
        return []
    step = max(1, len(rows) // n)
    return rows[step // 2::step][:n]


def plan_backfill(conn: sqlite3.Connection, client: HttpClient, url: str, *, hours: float, sample: int, now: float) -> dict[str, Any]:
    """Fix the window and the sample, and store them. Called once; later runs resume the stored plan."""
    since = now - hours * 3600 - OUTCOME_WINDOW_S
    rows, complete = list_launches(client, url, since)
    eligible = [r for r in rows if r["blockTime"] <= now - OUTCOME_WINDOW_S - 60]   # outcome window fully in the past
    chosen = systematic_sample(eligible, sample)
    conn.execute("BEGIN")
    conn.executemany("INSERT OR IGNORE INTO backfill_cursors (signature, block_time, slot) VALUES (?, ?, ?)",
                     [(r["signature"], r["blockTime"], r["slot"]) for r in rows])
    conn.executemany("INSERT OR IGNORE INTO backfill_queue (signature, block_time, slot) VALUES (?, ?, ?)",
                     [(r["signature"], r["blockTime"], r["slot"]) for r in chosen])
    conn.execute("COMMIT")
    plan = {"planned_at": now, "window_start": since, "window_end": now - OUTCOME_WINDOW_S - 60, "hours": hours,
            "launches_in_window": len(eligible), "sample_size": len(chosen), "sampling": "systematic, every k-th launch",
            "window_fully_listed": complete, "ruleset": policy.RULESET}
    db.log_event(conn, "backfill_planned", plan)
    return plan


class Clock:
    """Signatures of all launches in the window, used as cursors into other accounts' histories."""

    def __init__(self, conn: sqlite3.Connection):
        rows = conn.execute("SELECT block_time, signature FROM backfill_cursors ORDER BY block_time, slot, signature").fetchall()
        self.times = [r["block_time"] for r in rows]
        self.sigs = [r["signature"] for r in rows]

    def cursor_at(self, t: float) -> str | None:
        """A signature whose block time is at or just after `t`; history 'before' it ends at about `t`."""
        i = bisect.bisect_left(self.times, t)
        return self.sigs[i] if i < len(self.sigs) else None


# --------------------------------------------------------------------------------------------
# one launch
# --------------------------------------------------------------------------------------------

def parse_creation(tx: dict[str, Any]) -> dict[str, Any]:
    """Mint, curve account and curve parameters from a creation transaction. Raises ValueError if it is not one."""
    meta = tx.get("meta") or {}
    names = solana_rpc._instruction_names(meta)
    if not any(n.startswith("CreateV") or n == "Create" for n in names):
        raise ValueError("not a creation transaction")
    keys = ((tx.get("transaction") or {}).get("message") or {}).get("accountKeys") or []
    signers = [k["pubkey"] for k in keys if isinstance(k, dict) and k.get("signer")]
    post = [b for b in meta.get("postTokenBalances") or [] if isinstance(b, dict)]
    mint = next((s for s in signers if any(b.get("mint") == s for b in post)), None)
    if mint is None:
        raise ValueError("mint not found among the signers")
    event = next((e for e in (parse_create_event(raw, mint) for raw in event_payloads(tx)) if e), None)
    out: dict[str, Any] = {"mint": mint, "creation_time": tx.get("blockTime"), "slot": tx.get("slot"), "creator": signers[0] if signers else None,
                           "curve": None, "standard": False, "is_mayhem": None, "why_not_standard": None, "start": None}
    if event is None:
        out["why_not_standard"] = "creation event not readable in the transaction logs"
        return out

    def held(owner: str) -> float:
        return sum(solana_rpc.num((b.get("uiTokenAmount") or {}).get("uiAmountString")) or 0.0
                   for b in post if b.get("mint") == mint and b.get("owner") == owner)

    curve = event["curve"]
    bought = sum(held(s) for s in signers if s != mint)
    out.update(curve=curve, creator=event["creator"], is_mayhem=event["is_mayhem"], curve_tokens=held(curve))
    if event["quote_mint"] not in NATIVE_SOL:
        out["why_not_standard"] = f"quoted in token {event['quote_mint'][:8]}…, not SOL"
    elif abs(held(curve) + bought - amm.TOTAL_SUPPLY) > 1.0:
        out["why_not_standard"] = f"curve started with {held(curve) + bought:,.0f} tokens, not 1,000,000,000"
    else:
        out["standard"] = True
        out["start"] = {"virtual_sol": event["virtual_quote_units"] / 1e9, "virtual_tokens": event["virtual_tokens"],
                        "real_sol": 0.0, "real_tokens": event["real_tokens"]}
    return out


def curve_tokens_in(tx: dict[str, Any], curve: str, mint: str) -> float | None:
    """Tokens of `mint` held by the curve account after this transaction, if the transaction shows it."""
    for b in (tx.get("meta") or {}).get("postTokenBalances") or []:
        if b.get("owner") == curve and b.get("mint") == mint:
            return solana_rpc.num((b.get("uiTokenAmount") or {}).get("uiAmountString"))
    return None


def state_from_balance(curve_tokens: float, start: dict[str, float]) -> dict[str, float]:
    """Reserves of a NON-Mayhem curve from its token balance: tokens that left the account were bought and the
    product of virtual reserves is constant. Checked against trade events on mainnet (exact). Not valid for
    Mayhem launches, where the agent moves virtual reserves independently."""
    sold = amm.TOTAL_SUPPLY - curve_tokens
    virtual_tokens = start["virtual_tokens"] - sold
    virtual_sol = start["virtual_sol"] * start["virtual_tokens"] / virtual_tokens
    return {"virtual_sol": virtual_sol, "virtual_tokens": virtual_tokens, "real_sol": virtual_sol - start["virtual_sol"],
            "real_tokens": start["real_tokens"] - sold}


def _pool_of(tx: dict[str, Any], curve: str, mint: str, signers: set[str]) -> str | None:
    """The AMM pool created in a migration transaction: the non-signer account that holds both the token and wrapped SOL."""
    post = (tx.get("meta") or {}).get("postTokenBalances") or []
    holds_sol = {b.get("owner") for b in post if b.get("mint") == solana_rpc.WSOL_MINT}
    best: tuple[float, str] | None = None
    for b in post:
        owner, amount = b.get("owner"), solana_rpc.num((b.get("uiTokenAmount") or {}).get("uiAmountString")) or 0.0
        if b.get("mint") == mint and owner in holds_sol and owner != curve and owner not in signers and (best is None or amount > best[0]):
            best = (amount, owner)
    return best[1] if best else None


def _pool_payload(tx: dict[str, Any], pool: str, mint: str, state_time: float, signature: str) -> dict[str, Any] | None:
    base = quote = None
    for b in (tx.get("meta") or {}).get("postTokenBalances") or []:
        if b.get("owner") != pool:
            continue
        amount = solana_rpc.num((b.get("uiTokenAmount") or {}).get("uiAmountString"))
        if b.get("mint") == mint:
            base = amount
        elif b.get("mint") == solana_rpc.WSOL_MINT:
            quote = amount
    if not base or quote is None:
        return None
    res = amm.effective_pool_reserves(quote, base)
    return {"venue": "pool", "price_sol": res.price, "quote_reserve_sol": res.quote, "base_reserve": res.base, "liquidity_sol": quote,
            "pool_address": pool, "fdv_sol": res.market_cap(), "fdv_definition": "price × 1e9 supply, in SOL",
            "market_cap_usd": None, "market_cap_definition": "not computed in the backtest",
            "reserve_model": "pool balances read on-chain + observed InitBoost constant", "state_time": state_time, "state_signature": signature}


def backfill_launch(conn: sqlite3.Connection, settings: Settings, client: HttpClient, url: str, row: sqlite3.Row | dict[str, Any],
                    clock: Clock, *, now: float | None = None) -> tuple[str, str | None, str]:
    """Read one sampled launch and store what a reader would have known at each grid time. Returns (status, mint, note).

    Nothing is decided here: every readable launch gets its whole outcome window, and each paper book applies
    its own rule afterwards."""
    now = time.time() if now is None else now
    cfg = settings.paper
    tx = solana_rpc.call(client, url, "getTransaction", [row["signature"], solana_rpc.TX_OPTS]).data.get("result")
    if not isinstance(tx, dict):
        return "skipped", None, "creation transaction not available from this endpoint"
    try:
        info = parse_creation(tx)
    except ValueError as exc:
        return "skipped", None, str(exc)
    mint, curve, t0, start = info["mint"], info["curve"], float(info["creation_time"]), info["start"]
    conn.execute("DELETE FROM observations WHERE mint = ?", (mint,))   # a re-read after an interruption starts clean
    db.upsert_token(conn, mint, is_synthetic=False, now=now, creator=info["creator"], launch_time=t0,
                    launch_source="on-chain block time of the creation transaction (backtest sample)",
                    meta={"backfill": True, "curve_address": curve, "creation_signature": row["signature"], "is_mayhem": info["is_mayhem"]})
    if not info["standard"]:
        reason = f"curve type not supported by the backtest: {info['why_not_standard']}"
        db.add_observation(conn, mint, "launch", solana_rpc.NAME, t0, {"status": "unknown", "reason": reason},
                           is_synthetic=False, ingested_at=now, missing=["slot0_buyers"])
        return "unsupported", mint, str(info["why_not_standard"])

    tx_cache: dict[str, dict[str, Any]] = {row["signature"]: tx}

    def fetch(sig: str) -> dict[str, Any] | None:
        if sig not in tx_cache:
            got = solana_rpc.call(client, url, "getTransaction", [sig, solana_rpc.TX_OPTS]).data.get("result")
            if not isinstance(got, dict):
                return None
            tx_cache[sig] = got
        return tx_cache[sig]

    # the curve's history over the outcome window, newest first; when it reaches back to creation it also
    # contains the creation slot, so the structure needs no second read
    end_cursor = clock.cursor_at(t0 + OUTCOME_WINDOW_S)
    structure_cursor = clock.cursor_at(t0 + STRUCTURE_WINDOW_S)
    if end_cursor is None or structure_cursor is None:
        return "skipped", mint, "outcome window not covered by the cursor list"
    history, complete = solana_rpc.signatures(client, url, curve, max_pages=3, before=end_cursor)
    ok_history = [h for h in history if not h.get("err") and h.get("blockTime")]   # complete=False -> a very busy curve: read point by point
    if complete:
        launch = solana_rpc.read_launch_structure(client, url, curve, mint, history=(history, True), fetch=fetch)
    else:
        launch = solana_rpc.read_launch_structure(client, url, curve, mint, max_pages=3, before=structure_cursor, fetch=fetch)
    launch["is_mayhem"] = info["is_mayhem"]   # an automated agent holds a second billion tokens and trades for 24 hours
    db.add_observation(conn, mint, "launch", solana_rpc.NAME, t0, launch, is_synthetic=False, ingested_at=now,
                       missing=[] if launch.get("status") == "known" else ["slot0_buyers"])

    def ok_before(address: str, t: float, local: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """Successful transactions of `address` at or before time t, newest first."""
        if local is not None:
            return [h for h in local if h["blockTime"] <= t]
        cursor = clock.cursor_at(t)
        if cursor is None:
            return []
        rows = solana_rpc.call(client, url, "getSignaturesForAddress", [address, {"limit": 50, "before": cursor}]).data.get("result") or []
        return [r for r in rows if not r.get("err") and (r.get("blockTime") or float("inf")) <= t]

    def read_row(hit: dict[str, Any]) -> dict[str, Any] | None:
        """What one curve transaction tells us: exact reserves if it traded this token, otherwise (non-Mayhem
        only) reserves from the curve's token balance. `kind` says which, or that it is a migration."""
        state_tx = fetch(hit["signature"])
        if state_tx is None:
            return None
        names = solana_rpc._instruction_names(state_tx.get("meta") or {})
        tokens = curve_tokens_in(state_tx, curve, mint)
        base = {"signature": hit["signature"], "time": float(hit["blockTime"]), "curve_tokens": tokens, "tx": state_tx}
        if "CreatePool" in names:
            return {**base, "kind": "migration"}
        state = last_trade_state(state_tx, mint)
        if state is not None:
            return {**base, "kind": "trade event", "state": state}
        if hit["signature"] == row["signature"]:
            return {**base, "kind": "creation event", "state": start}
        if not info["is_mayhem"] and tokens is not None and tokens > 1.0:
            return {**base, "kind": "curve token balance and curve constants", "state": state_from_balance(tokens, start)}
        return {**base, "kind": "other"}

    pool: str | None = None
    migration: dict[str, Any] | None = None

    def reading_at(t: float) -> dict[str, Any] | None:
        """The newest informative curve transaction at or before t. Transactions that touch the curve without
        trading are stepped over a few times, then the moment is recorded as unreadable."""
        nonlocal migration
        for hit in ok_before(curve, t, ok_history if complete else None)[:5]:
            got = read_row(hit)
            if got is None:
                return None
            if got["kind"] == "migration":
                migration = got
                continue
            if got["kind"] != "other":
                return got
        return None

    def payload_at(t: float, reading: dict[str, Any] | None) -> dict[str, Any] | None:
        nonlocal pool
        if reading is None:
            return None
        if reading["state"]["real_tokens"] > 0 and (migration is None or migration["time"] > t):
            return curve_payload(reading["state"], reading["time"], reading["signature"], reading["kind"])
        if migration is None or migration["time"] > t:
            return None            # curve complete but not yet migrated: no venue to quote
        mtx = migration["tx"]
        signers = {k["pubkey"] for k in ((mtx.get("transaction") or {}).get("message") or {}).get("accountKeys") or [] if k.get("signer")}
        pool = pool or _pool_of(mtx, curve, mint, signers)
        if pool is None:
            return None
        hits = ok_before(pool, t)
        pool_tx = fetch(hits[0]["signature"]) if hits else None
        if not hits or pool_tx is None:
            return _pool_payload(mtx, pool, mint, migration["time"], migration["signature"])
        return _pool_payload(pool_tx, pool, mint, float(hits[0]["blockTime"]), hits[0]["signature"])

    grid = observation_grid(cfg.decision_delay_s)
    readings: dict[int, dict[str, Any] | None] = {}

    def fill(lo: int, hi: int) -> None:
        """Read grid points lo..hi, skipping the stretch between two points whose curve balance is identical:
        no tokens moved, so nothing traded and the state is the same."""
        for i in (lo, hi):
            if i not in readings:
                readings[i] = reading_at(t0 + grid[i])
        a, b = readings[lo], readings[hi]
        if hi - lo <= 1:
            return
        same = a is not None and b is not None and (a["signature"] == b["signature"] or (
            a["curve_tokens"] is not None and a["curve_tokens"] == b["curve_tokens"] and a["kind"] != "migration"))
        if same:
            for i in range(lo + 1, hi):
                readings[i] = a
            return
        mid = (lo + hi) // 2
        fill(lo, mid)
        fill(mid, hi)

    fill(0, len(grid) - 1)
    stored = 0
    for i, offset in enumerate(grid):
        payload = payload_at(t0 + offset, readings.get(i))
        if payload is not None:
            payload["history_complete"] = complete
            db.add_observation(conn, mint, "market", solana_rpc.NAME, t0 + offset, payload, is_synthetic=False, ingested_at=now)
            stored += 1
    return ("read" if stored else "unreadable"), mint, f"{stored}/{len(grid)} grid points, {len(tx_cache)} transactions read"


# --------------------------------------------------------------------------------------------
# the whole run
# --------------------------------------------------------------------------------------------

BOOKS: dict[str, tuple[str, policy.DecisionRule | None]] = {
    # the filter fixed in policy.py before any data was read
    "backtest": (policy.RULESET, None),
    # the baseline: enter every launch that has a price, with the same timing, costs and exit rule
    "backtest-all": ("enter-all-v1", policy.DecisionRule(max_slot0_share=2.0, max_creator_share=2.0, max_cosigned_share=2.0, serial_min_launches=10**9,
                                                         min_liquidity_sol=0.0, max_data_age_s=1e12, require_launch_structure=False)),
}


def _read_one(conn: sqlite3.Connection, settings: Settings, client: HttpClient, url: str, row: sqlite3.Row, clock: Clock, now: float,
              say: Callable[[str], None], sleep: Callable[[float], None]) -> str:
    """Read one queued launch, with patience for rate limits, and record what happened to it."""
    status, mint, note = "error", None, ""
    for attempt in range(5):
        try:
            status, mint, note = backfill_launch(conn, settings, client, url, row, clock, now=now)
            break
        except ProviderError as exc:
            status, mint, note = "error", None, f"{exc.kind}: {exc.message}"
            if exc.kind not in ("rate_limited", "timeout") or attempt == 4:
                break
            wait = min(max((exc.retry_at or 0) - client.clock(), 5.0 * (attempt + 1)), 90.0)
            say(f"{exc.kind}; waiting {wait:.0f}s")
            sleep(wait)
            client._cooldown_until = 0.0
    retry_later = status == "error" and note.split(":")[0] in ("rate_limited", "timeout")
    conn.execute("UPDATE backfill_queue SET status = ?, mint = ?, note = ? WHERE signature = ?",
                 ("pending" if retry_later else status, mint, note[:300], row["signature"]))
    return status


def run_books(conn: sqlite3.Connection, settings: Settings, now: float) -> dict[str, Any]:
    """Apply each ruleset to the stored history and return its metrics."""
    out: dict[str, Any] = {}
    for book, (ruleset, rule) in BOOKS.items():
        run = paper.run_book(conn, settings, book, synthetic=False, final=True, now=now, decision_rule=rule, ruleset=ruleset)
        out[book] = {"run": run, "metrics": paper.book_metrics(conn, book, settings)}
    return out


def run_backfill(conn: sqlite3.Connection, settings: Settings, client: HttpClient, url: str, *, hours: float = 24.0, sample: int = 500,
                 now: float | None = None, progress: Callable[[str], None] | None = None, max_launches: int | None = None,
                 sleep: Callable[[float], None] = time.sleep, workers: int = 1,
                 worker_setup: Callable[[], tuple[sqlite3.Connection, HttpClient]] | None = None) -> dict[str, Any]:
    """Plan (once), read every pending sampled launch, then run the paper books on the complete history.

    With `workers` > 1 the launches are read in parallel; `worker_setup` must then return a separate database
    connection and HTTP client for each worker thread. Reads are independent, so the order does not matter."""
    if not settings.live_enabled:
        raise ProviderError("launchlab", "disabled", "the backtest reads public chain data: add --live or set LAUNCHLAB_MODE=live")
    now = time.time() if now is None else now
    say = progress or (lambda _msg: None)
    if conn.execute("SELECT COUNT(*) FROM backfill_queue").fetchone()[0] == 0:
        plan = plan_backfill(conn, client, url, hours=hours, sample=sample, now=now)
        say(f"planned: {plan['launches_in_window']} launches in the window, {plan['sample_size']} sampled")
    clock = Clock(conn)
    pending = conn.execute("SELECT * FROM backfill_queue WHERE status = 'pending' ORDER BY block_time").fetchall()[:max_launches]

    def counts() -> dict[str, int]:
        return {r["status"]: r["n"] for r in conn.execute("SELECT status, COUNT(*) AS n FROM backfill_queue GROUP BY status")}

    if workers > 1 and worker_setup is not None:
        local = threading.local()

        def work(row: sqlite3.Row) -> str:
            if not hasattr(local, "ctx"):
                local.ctx = worker_setup()
            return _read_one(local.ctx[0], settings, local.ctx[1], url, row, clock, now, say, sleep)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            for done, _status in enumerate(pool.map(work, pending), start=1):
                if done % 50 == 0:
                    say(f"{done}/{len(pending)} read; queue: {counts()}")
    else:
        for done, row in enumerate(pending, start=1):
            _read_one(conn, settings, client, url, row, clock, now, say, sleep)
            if done % 25 == 0:
                say(f"{done}/{len(pending)} read; queue: {counts()}")
    books = run_books(conn, settings, now)
    db.log_event(conn, "backfill_run", {"queue": counts(), "books": {name: b["run"] for name, b in books.items()}})
    return {"queue": counts(), "books": books}


# --------------------------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------------------------

SUMMARY_KEYS = ("ruleset", "signals", "candidates", "rejected", "resolved", "filled", "unsellable", "failed_attempts", "gross_pnl_sol", "fees_sol",
                "net_pnl_sol", "expectancy", "expectancy_ci", "ci_confidence", "median_return", "win_rate", "avg_win", "avg_loss", "max_drawdown_sol",
                "rejection_reasons", "positions_by_status", "distribution", "verdict", "verdict_note")
SENSITIVITY: dict[str, dict[str, Any]] = {
    "conservative_exit": {"own_liquidity": False},      # exit priced as if the position's own SOL were not in the pool
    "no_random_failures": {"fail_prob": 0.0},           # every transaction lands first time
}


def _summary(metrics: dict[str, Any]) -> dict[str, Any]:
    return {k: metrics[k] for k in SUMMARY_KEYS}


def _group_stats(returns: list[float], seed: int) -> dict[str, Any]:
    if not returns:
        return {"n": 0}
    ordered = sorted(returns)
    ci = paper.bootstrap_mean_ci(returns, seed=seed)
    return {"n": len(returns), "mean_return": sum(returns) / len(returns), "median_return": ordered[len(ordered) // 2],
            "interval_95": list(ci) if ci else None, "win_rate": sum(r > 0 for r in returns) / len(returns),
            "share_losing_90pct_or_more": sum(r <= -0.9 for r in returns) / len(returns),
            "share_gaining_100pct_or_more": sum(r >= 1.0 for r in returns) / len(returns)}


def report(conn: sqlite3.Connection, settings: Settings, *, now: float | None = None) -> dict[str, Any]:
    """Everything needed to read a finished backtest: the plan, what could be read, both books, a split of
    the baseline by launch type, and sensitivity runs. No network. The stored books are not modified."""
    now = time.time() if now is None else now
    size = settings.paper.size_sol
    plan_row = conn.execute("SELECT payload FROM events WHERE type = 'backfill_planned' ORDER BY id DESC LIMIT 1").fetchone()
    queue = {r["status"]: r["n"] for r in conn.execute("SELECT status, COUNT(*) AS n FROM backfill_queue GROUP BY status")}
    unsupported: dict[str, int] = {}
    for r in conn.execute("SELECT note FROM backfill_queue WHERE status = 'unsupported'"):
        key = "quoted in another token, not SOL" if "not SOL" in r["note"] else r["note"]
        unsupported[key] = unsupported.get(key, 0) + 1
    readable = conn.execute("SELECT COUNT(DISTINCT mint) FROM observations WHERE kind = 'market'").fetchone()[0]
    mayhem = {str(r["flag"]): r["n"] for r in conn.execute(
        "SELECT json_extract(meta, '$.is_mayhem') AS flag, COUNT(*) AS n FROM tokens WHERE is_synthetic = 0 GROUP BY flag")}
    books: dict[str, Any] = {}
    for book in BOOKS:
        metrics = paper.book_metrics(conn, book, settings)
        exits = {r["exit_reason"]: r["n"] for r in conn.execute(
            "SELECT exit_reason, COUNT(*) AS n FROM positions WHERE book = ? GROUP BY exit_reason ORDER BY n DESC", (book,))}
        books[book] = {**_summary(metrics), "exit_reasons": exits}
    split: dict[str, Any] = {}
    for label, flag in (("mayhem", 1), ("standard", 0)):
        rows = conn.execute("SELECT p.net_pnl_sol FROM positions p JOIN tokens t ON t.mint = p.mint WHERE p.book = 'backtest-all'"
                            " AND json_extract(t.meta, '$.is_mayhem') = ?", (flag,)).fetchall()
        split[label] = _group_stats([r["net_pnl_sol"] / size for r in rows], settings.paper.seed)
    sensitivity: dict[str, Any] = {}
    for name, change in SENSITIVITY.items():
        mem = sqlite3.connect(":memory:", isolation_level=None)
        conn.backup(mem)
        mem.row_factory = sqlite3.Row
        for book in BOOKS:
            paper.reset_book(mem, book)
        variant = dataclasses.replace(settings, paper=dataclasses.replace(settings.paper, **change))
        result = run_books(mem, variant, now)
        keys = ("candidates", "resolved", "expectancy", "expectancy_ci", "net_pnl_sol", "win_rate", "unsellable")
        sensitivity[name] = {"change": change, **{book: {k: result[book]["metrics"][k] for k in keys} for book in BOOKS}}
        mem.close()
    return {"plan": json.loads(plan_row["payload"]) if plan_row else None, "queue": queue, "unsupported": unsupported,
            "launches_with_a_price": readable, "mayhem_flag_counts": mayhem, "books": books, "baseline_by_launch_type": split,
            "sensitivity": sensitivity, "position_size_sol": size,
            "note": "Descriptive results for one past window with modelled fills. Not evidence of an edge, not a forecast."}
