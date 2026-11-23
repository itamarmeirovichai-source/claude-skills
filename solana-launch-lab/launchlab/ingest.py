"""Combine read-only providers into stored observations with provenance, quality flags and conflicts.

A failing provider never blocks the others and never produces a made-up value: its error is recorded in
`provider_health` and returned to the caller, and whatever it would have supplied stays unknown.
"""

from __future__ import annotations

import hashlib
import math
import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from . import amm, db
from .config import Settings, is_valid_mint, redact_url
from .providers import dexscreener, geckoterminal, solana_rpc
from .providers.base import FetchResult, HttpClient, ProviderError

# Signatures are returned newest first, 1,000 per page. A busy new curve can pass 2,000 within a minute, so read deeper;
# beyond this the creation slot is reported as unknown rather than guessed.
LAUNCH_HISTORY_PAGES = 6


@dataclass
class Clients:
    dex: HttpClient = field(default_factory=dexscreener.make_client)
    gecko: HttpClient = field(default_factory=geckoterminal.make_client)
    rpc: HttpClient = field(default_factory=solana_rpc.make_client)

    @classmethod
    def for_settings(cls, settings: Settings) -> Clients:
        clients = cls()
        for client in (clients.dex, clients.gecko, clients.rpc):
            client.enabled = settings.live_enabled
        return clients


def _snapshot(conn: sqlite3.Connection, settings: Settings, provider: str, res: FetchResult, request: Any = None) -> None:
    """Keep the raw reply when that provider's switch is on. URLs are redacted: a custom RPC URL may embed a token."""
    if settings.store_raw.get(provider):
        label = redact_url(res.url) if provider == solana_rpc.NAME else res.url.split("?")[0]
        if isinstance(request, dict) and request.get("method"):
            label += "#" + str(request["method"])
        conn.execute("INSERT INTO raw_snapshots (provider, url, fetched_at, sha256, body) VALUES (?, ?, ?, ?, ?)",
                     (provider, label, res.fetched_at, hashlib.sha256(res.body).hexdigest(), res.body.decode("utf-8", "replace")))


def _guard(conn: sqlite3.Connection, provider: str, errors: list[dict[str, Any]], fn: Callable[[], Any]) -> Any:
    """Run one provider step; record health; convert failure into an entry in `errors`."""
    try:
        out = fn()
    except ProviderError as exc:
        db.record_health(conn, provider, ok=False, error=f"{exc.kind}: {exc.message}", rate_limited_until=exc.retry_at)
        errors.append({"provider": provider, "kind": exc.kind, "message": exc.message})
        return None
    db.record_health(conn, provider, ok=True)
    return out


def attach_reserves(payload: dict[str, Any], tolerance: float = 0.05) -> None:
    """Add pricing reserves to a market payload when they can be derived AND cross-checked against the
    quoted price. If the check fails the reserves are left out and the reason is noted."""
    price = payload.get("price_sol")
    if not price:
        return
    if payload.get("venue") == "curve":
        k = amm.INITIAL_VIRTUAL_SOL * amm.INITIAL_VIRTUAL_TOKENS
        quote = math.sqrt(k * price)
        payload.update(quote_reserve_sol=quote, base_reserve=math.sqrt(k / price), liquidity_sol=max(quote - amm.INITIAL_VIRTUAL_SOL, 0.0),
                       curve_real_sol=max(quote - amm.INITIAL_VIRTUAL_SOL, 0.0),
                       reserve_model="derived from price assuming standard bonding-curve constants (not read from the account)")
        return
    base, quote_real = payload.get("pool_base_balance"), payload.get("pool_quote_balance")
    if payload.get("dex_id") == "pumpswap" and base and quote_real is not None and payload.get("quote_symbol") == "SOL":
        effective = quote_real + amm.OBSERVED_POOL_BOOST_SOL
        implied = effective / base
        if abs(implied / price - 1) <= tolerance:
            payload.update(quote_reserve_sol=effective, base_reserve=base, liquidity_sol=quote_real,
                           reserve_model="pool balances + observed InitBoost constant; cross-checked against quoted price")
        else:
            payload["reserve_note"] = f"reserves omitted: balances imply {implied:.3e} SOL but quoted price is {price:.3e} SOL"


def flag_negligible(payload: dict[str, Any], threshold_usd: float = 1.0) -> bool:
    """Mark a pool whose reported depth is effectively zero (a drained curve, a dust pool). Its last price is kept
    for the record but is not used to describe or trade the token."""
    liquidity = payload.get("liquidity_usd")
    if liquidity is not None and liquidity < threshold_usd:
        payload["negligible_liquidity"] = True
        return True
    return False


def _conflicts(conn: sqlite3.Connection, mint: str, a: dict[str, Any], b: dict[str, Any], when: float, tolerance: float) -> int:
    found = 0
    for name in ("price_usd", "fdv_usd", "liquidity_usd"):
        va, vb = a.get(name), b.get(name)
        if va and vb:
            diff = abs(va - vb) / max(abs(va), abs(vb))
            if diff > tolerance:
                conn.execute("INSERT INTO conflicts (mint, field, provider_a, value_a, provider_b, value_b, rel_diff, observed_at)"
                             " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (mint, name, dexscreener.NAME, va, geckoterminal.NAME, vb, diff, when))
                found += 1
    return found


def ingest_mint(conn: sqlite3.Connection, settings: Settings, mint: str, clients: Clients, *, now: float | None = None) -> dict[str, Any]:
    """Fetch public data for one exact mint and store it. Read-only."""
    if not is_valid_mint(mint):
        raise ValueError("not a valid Solana address; search uses exact mint addresses, never tickers")
    if not settings.live_enabled:
        raise ProviderError("launchlab", "disabled", "live connectors are off (LAUNCHLAB_MODE=demo)")
    now = time.time() if now is None else now
    errors: list[dict[str, Any]] = []
    stored = {"market": 0, "launch": 0, "holders": 0, "conflicts": 0}
    db.upsert_token(conn, mint, is_synthetic=False, now=now)

    # --- DEX Screener ---------------------------------------------------------------------------
    dex_pairs: list[dict[str, Any]] = []
    res = _guard(conn, dexscreener.NAME, errors, lambda: dexscreener.fetch_token_pairs(clients.dex, mint))
    if res is not None:
        _snapshot(conn, settings, dexscreener.NAME, res)
        dex_pairs = dexscreener.normalize_response(res.data, mint)
        for payload in dex_pairs:
            missing = payload.pop("missing")
            if flag_negligible(payload):
                missing.append("usable price (pool depth under $1)")
            else:
                attach_reserves(payload, settings.conflict_tolerance)
            db.add_observation(conn, mint, "market", dexscreener.NAME, res.fetched_at, payload, is_synthetic=False, ingested_at=now, missing=missing)
            stored["market"] += 1
            db.upsert_token(conn, mint, is_synthetic=False, name=payload.get("name"), symbol=payload.get("symbol"))
        if not dex_pairs:
            errors.append({"provider": dexscreener.NAME, "kind": "empty", "message": "no pair lists this mint as its base token"})

    # --- GeckoTerminal ---------------------------------------------------------------------------
    curve_address: str | None = None
    pool_addresses: set[str] = set()
    res = _guard(conn, geckoterminal.NAME, errors, lambda: geckoterminal.fetch_token_pools(clients.gecko, mint))
    if res is not None:
        _snapshot(conn, settings, geckoterminal.NAME, res)
        pools = geckoterminal.normalize_pools(res.data, mint)
        created = [p["pool_created_at"] for p in pools if p["pool_created_at"]]
        for payload in pools:
            pool_addresses.add(payload["pool_address"])
            if payload["dex_id"] == geckoterminal.CURVE_DEX:
                curve_address = payload["pool_address"]
            if payload.get("price_usd") is None and not payload.get("liquidity_usd"):
                continue  # an emptied pool record carries no market information
            missing = [k for k in ("price_usd", "liquidity_usd") if payload.get(k) is None]
            if flag_negligible(payload):
                missing.append("usable price (pool depth under $1)")
            else:
                attach_reserves(payload, settings.conflict_tolerance)
            db.add_observation(conn, mint, "market", geckoterminal.NAME, res.fetched_at, payload, is_synthetic=False, ingested_at=now, missing=missing)
            stored["market"] += 1
            match = next((d for d in dex_pairs if d.get("pool_address") == payload["pool_address"]), None)
            if match:
                stored["conflicts"] += _conflicts(conn, mint, match, payload, res.fetched_at, settings.conflict_tolerance)
        if created:
            db.upsert_token(conn, mint, is_synthetic=False, launch_time=min(created), launch_source="geckoterminal pool_created_at (earliest pool)")
        db.upsert_token(conn, mint, is_synthetic=False, meta={"curve_address": curve_address, "pool_addresses": sorted(pool_addresses)})

    # --- Solana RPC: creation slot -------------------------------------------------------------
    url = settings.solana_rpc_url
    clients.rpc.on_fetch = lambda res, request: _snapshot(conn, settings, solana_rpc.NAME, res, request)
    if curve_address:
        launch = _guard(conn, solana_rpc.NAME, errors,
                        lambda: solana_rpc.read_launch_structure(clients.rpc, url, curve_address, mint, max_pages=LAUNCH_HISTORY_PAGES))
        if launch is not None:
            buyers = [b["wallet"] for b in reversed(launch.get("slot0_buyers") or [])]   # smallest first: shortest histories
            if len(buyers) >= 2:
                funders = _guard(conn, solana_rpc.NAME, errors, lambda: solana_rpc.read_first_funders(clients.rpc, url, buyers))
                if funders:
                    launch.update(funders)
            when = launch.get("creation_time") or now
            db.add_observation(conn, mint, "launch", solana_rpc.NAME, when, launch, is_synthetic=False, ingested_at=now,
                               missing=[] if launch.get("status") == "known" else ["slot0_buyers"])
            stored["launch"] += 1
            if launch.get("creation_time"):
                # on-chain block time beats a provider's pool timestamp
                conn.execute("UPDATE tokens SET launch_time = ?, launch_source = ?, creator = COALESCE(?, creator) WHERE mint = ?",
                             (launch["creation_time"], "on-chain block time of the creation transaction", launch.get("creator"), mint))
    else:
        errors.append({"provider": solana_rpc.NAME, "kind": "skipped", "message": "bonding-curve account address unknown, creation slot not read"})

    # --- Solana RPC: largest accounts (often refused by the public endpoint) -------------------
    def holders() -> dict[str, Any] | None:
        largest = solana_rpc.call(clients.rpc, url, "getTokenLargestAccounts", [mint]).data.get("result", {}).get("value") or []
        accounts = [a["address"] for a in largest if isinstance(a, dict) and a.get("address")]
        if not accounts:
            return None
        info = solana_rpc.call(clients.rpc, url, "getMultipleAccounts", [accounts, {"encoding": "jsonParsed"}]).data.get("result", {}).get("value") or []
        rows = []
        for acct, parsed in zip(largest, info, strict=False):
            owner = ((((parsed or {}).get("data") or {}).get("parsed") or {}).get("info") or {}).get("owner")
            tokens = float(acct.get("uiAmountString") or 0)
            if owner and owner not in pool_addresses and owner != curve_address:
                rows.append({"wallet": owner, "tokens": tokens, "share": tokens / amm.TOTAL_SUPPLY})
        return {"complete": False, "scope": "20 largest token accounts, pool and curve accounts removed", "holders": rows}

    holder_payload = _guard(conn, solana_rpc.NAME, errors, holders)
    if holder_payload:
        db.add_observation(conn, mint, "holders", solana_rpc.NAME, now, holder_payload, is_synthetic=False, ingested_at=now)
        stored["holders"] += 1

    clients.rpc.on_fetch = None
    db.log_event(conn, "ingest", {"mint": mint, "stored": stored, "errors": errors})
    return {"mint": mint, "stored": stored, "errors": errors}


def discover(conn: sqlite3.Connection, settings: Settings, clients: Clients, *, now: float | None = None) -> dict[str, Any]:
    """Import the newest Pump.fun bonding-curve pools from GeckoTerminal's documented `new_pools` list.
    This is a sample of recent launches, not a complete stream; the gap is stated in the result."""
    if not settings.live_enabled:
        raise ProviderError("launchlab", "disabled", "live connectors are off (LAUNCHLAB_MODE=demo)")
    now = time.time() if now is None else now
    errors: list[dict[str, Any]] = []
    res = _guard(conn, geckoterminal.NAME, errors, lambda: geckoterminal.fetch_new_pools(clients.gecko))
    added = 0
    new_mints: list[str] = []
    if res is not None:
        _snapshot(conn, settings, geckoterminal.NAME, res)
        for payload in geckoterminal.normalize_pools(res.data):
            mint = payload.get("base_mint")
            if payload["dex_id"] != geckoterminal.CURVE_DEX or not mint or not is_valid_mint(mint):
                continue
            known = conn.execute("SELECT 1 FROM tokens WHERE mint = ?", (mint,)).fetchone()
            name = (payload.get("pool_name") or "").split(" / ")[0] or None
            db.upsert_token(conn, mint, is_synthetic=False, now=now, symbol=name, launch_time=payload.get("pool_created_at"),
                            launch_source="geckoterminal pool_created_at (bonding-curve pool)", meta={"curve_address": payload["pool_address"]})
            attach_reserves(payload, settings.conflict_tolerance)
            db.add_observation(conn, mint, "market", geckoterminal.NAME, res.fetched_at, payload, is_synthetic=False, ingested_at=now,
                               missing=[k for k in ("price_sol",) if payload.get(k) is None])
            if not known:
                added += 1
                new_mints.append(mint)
    db.log_event(conn, "discover", {"added": added, "errors": errors})
    return {"added": added, "new_mints": new_mints, "errors": errors,
            "coverage_note": "one page of the provider's newest pools; launches between polls are missed"}


def watch_cycle(conn: sqlite3.Connection, settings: Settings, clients: Clients, *, max_new: int = 2, now: float | None = None) -> dict[str, Any]:
    """One collection cycle for the live paper study: discover new launches, read the newest few in
    detail, then let the paper book decide. Bounded so the providers' rate limits are respected."""
    from . import paper  # local import: paper depends on risk, which depends on this module's siblings only

    found = discover(conn, settings, clients, now=now)
    ingested = [ingest_mint(conn, settings, mint, clients, now=now) for mint in found["new_mints"][:max_new]]
    book = paper.run_book(conn, settings, "live", synthetic=False, now=now)
    return {"discovered": found["added"], "ingested": [r["mint"] for r in ingested],
            "errors": found["errors"] + [e for r in ingested for e in r["errors"]], "paper": book}
