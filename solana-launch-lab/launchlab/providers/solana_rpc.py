"""Solana JSON-RPC adapter — READ-ONLY.

Only the methods in READ_METHODS can be called. There is no code here (or anywhere in this package) that
builds, signs, simulates or submits a transaction, and no parameter that accepts a key.

Docs: https://solana.com/docs/rpc/http (read 2026-11-23). Public endpoint limits: 100 requests / 10 s per
IP and 40 / 10 s per method. Version-1 transactions are live, so `maxSupportedTransactionVersion` is 1.
"""

from __future__ import annotations

from typing import Any

from ..amm import OBSERVED_POOL_BOOST_SOL, TOTAL_SUPPLY
from .base import FetchResult, HttpClient, ProviderError, num

NAME = "solana_rpc"
WSOL_MINT = "So11111111111111111111111111111111111111112"

READ_METHODS = frozenset({
    "getAccountInfo", "getBlock", "getBlockTime", "getHealth", "getMinimumBalanceForRentExemption",
    "getMultipleAccounts", "getSignaturesForAddress", "getSlot", "getTokenAccountsByOwner",
    "getTokenLargestAccounts", "getTokenSupply", "getTransaction",
})
TX_OPTS = {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}
SLOT_SECONDS = 0.218  # measured 2026-11-20/21; only used as a first guess when locating a slot by time


def make_client(**overrides: Any) -> HttpClient:
    return HttpClient(provider=NAME, min_interval_s=0.35, **overrides)


def call(client: HttpClient, url: str, method: str, params: list[Any]) -> FetchResult:
    """Call one allow-listed read method. Anything else is refused before a request is built."""
    if method not in READ_METHODS:
        raise ProviderError(NAME, "forbidden_method", f"{method} is not an allowed read-only method")
    res = client.request_json(url, method="POST", body={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    data = res.data
    if not isinstance(data, dict):
        raise ProviderError(NAME, "bad_response", "JSON-RPC reply was not an object")
    if data.get("error"):
        err = data["error"] if isinstance(data["error"], dict) else {"message": str(data["error"])}
        kind = "rate_limited" if err.get("code") in (429, -32005) else "http"
        raise ProviderError(NAME, kind, str(err.get("message", "rpc error"))[:200])
    return res


def signatures(client: HttpClient, url: str, address: str, *, max_pages: int = 2) -> tuple[list[dict[str, Any]], bool]:
    """Signatures for an address, newest first. Returns (rows, reached_beginning)."""
    rows: list[dict[str, Any]] = []
    before: str | None = None
    for _ in range(max_pages):
        opts: dict[str, Any] = {"limit": 1000}
        if before:
            opts["before"] = before
        page = call(client, url, "getSignaturesForAddress", [address, opts]).data.get("result") or []
        rows.extend(r for r in page if isinstance(r, dict))
        if len(page) < 1000:
            return rows, True
        before = page[-1].get("signature")
    return rows, False


def _instruction_names(meta: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for line in meta.get("logMessages") or []:
        if isinstance(line, str) and "Instruction:" in line:
            name = line.split("Instruction:", 1)[1].strip()
            if name and name not in names:
                names.append(name)
    return names


def _token_deltas(meta: dict[str, Any], mint: str) -> dict[str, float]:
    """Change in whole tokens of `mint` per owner within one transaction."""
    def amount(entry: dict[str, Any]) -> float:
        return num((entry.get("uiTokenAmount") or {}).get("uiAmountString")) or 0.0

    deltas: dict[str, float] = {}
    for sign, key in ((-1.0, "preTokenBalances"), (1.0, "postTokenBalances")):
        for entry in meta.get(key) or []:
            if isinstance(entry, dict) and entry.get("mint") == mint and entry.get("owner"):
                deltas[entry["owner"]] = deltas.get(entry["owner"], 0.0) + sign * amount(entry)
    return deltas


def _lp_burned(tx: dict[str, Any]) -> bool | None:
    """True if the same amount that was minted (LP tokens) is burned in this transaction."""
    minted: set[str] = set()
    burned: set[str] = set()
    for group in (tx.get("meta") or {}).get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            parsed = ix.get("parsed") if isinstance(ix, dict) else None
            if isinstance(parsed, dict):
                amount = str((parsed.get("info") or {}).get("amount"))
                if parsed.get("type") == "mintTo":
                    minted.add(amount)
                elif parsed.get("type") == "burn":
                    burned.add(amount)
    if not minted:
        return None
    return bool(minted & burned)


def read_launch_structure(client: HttpClient, url: str, curve_address: str, mint: str, *,
                          max_pages: int = 2, max_txs: int = 10, supply: float = TOTAL_SUPPLY) -> dict[str, Any]:
    """Who bought in the creation slot? Reads the bonding-curve account's earliest transactions.

    Returns a launch-observation payload. `status` is 'known', 'partial' or 'unknown'; nothing is guessed.
    """
    rows, complete = signatures(client, url, curve_address, max_pages=max_pages)
    if not rows:
        return {"status": "unknown", "reason": "no transactions found for the bonding-curve account (pruned history or wrong address)"}
    if not complete:
        return {"status": "unknown", "reason": f"curve history exceeds {max_pages * 1000} signatures; creation slot not reached on this endpoint",
                "signatures_read": len(rows)}
    slot0 = min(r["slot"] for r in rows if isinstance(r.get("slot"), int))
    in_slot0 = [r for r in reversed(rows) if r.get("slot") == slot0]  # oldest first
    ok_rows = [r for r in in_slot0 if not r.get("err")]
    partial = len(ok_rows) > max_txs
    buyers: dict[str, float] = {}
    cosigner_groups: list[list[str]] = []
    creator: str | None = None
    creation_time: float | None = None
    migrated = False
    lp_burned: bool | None = None
    creator_tokens = 0.0
    for row in ok_rows[:max_txs]:
        tx = call(client, url, "getTransaction", [row["signature"], TX_OPTS]).data.get("result")
        if not isinstance(tx, dict):
            partial = True
            continue
        meta = tx.get("meta") or {}
        keys = ((tx.get("transaction") or {}).get("message") or {}).get("accountKeys") or []
        signers: list[str] = [k["pubkey"] for k in keys if isinstance(k, dict) and k.get("signer") and isinstance(k.get("pubkey"), str)]
        names = _instruction_names(meta)
        creation_time = creation_time or tx.get("blockTime")
        is_create = any(n.startswith("Create") and n != "CreatePool" and not n.startswith("CreateIdempotent") for n in names)
        if is_create and creator is None and signers:
            creator = signers[0]
        if any(n.startswith("Migrate") for n in names) and "CreatePool" in names:
            migrated = True
            lp_burned = _lp_burned(tx)
        deltas = _token_deltas(meta, mint)
        tx_buyers = [w for w in signers if w != mint and deltas.get(w, 0.0) > 1.0]
        for wallet in tx_buyers:
            buyers[wallet] = buyers.get(wallet, 0.0) + deltas[wallet]
        if len(tx_buyers) > 1:
            cosigner_groups.append(tx_buyers)
        if is_create and creator:
            creator_tokens += max(deltas.get(creator, 0.0), 0.0)
    bought = sum(buyers.values())
    return {
        "status": "partial" if partial else "known",
        "reason": "more creation-slot transactions than were read" if partial else None,
        "creation_slot": slot0,
        "creation_time": creation_time,
        "creator": creator,
        "creator_tokens_at_launch": creator_tokens,
        "creator_share_at_launch": creator_tokens / supply,
        "slot0_buyers": [{"wallet": w, "tokens": t, "share": t / supply} for w, t in sorted(buyers.items(), key=lambda kv: -kv[1])],
        "slot0_tokens_bought": bought,
        "slot0_share": bought / supply,
        "slot0_tx_count": len(in_slot0),
        "slot0_failed_tx_count": len(in_slot0) - len(ok_rows),
        "cosigner_groups": cosigner_groups,
        "migrated_in_creation_slot": migrated,
        "lp_burned_at_migration": lp_burned,
        "supply_assumed": supply,
        "curve_address": curve_address,
        "curve_signatures_total": len(rows),
    }


def read_first_funders(client: HttpClient, url: str, wallets: list[str], *, max_wallets: int = 8) -> dict[str, Any]:
    """Who paid for each wallet's first transaction? One hop only.

    A shared first funder is a PROBABILISTIC link: exchanges, bridges and launch services fund many
    unrelated wallets. Wallets with more than 1,000 transactions cannot be traced this cheaply and are skipped.
    """
    funders: dict[str, list[str]] = {}
    checked = skipped = 0
    for wallet in wallets[:max_wallets]:
        rows, complete = signatures(client, url, wallet, max_pages=1)
        if not rows or not complete:
            skipped += 1
            continue
        tx = call(client, url, "getTransaction", [rows[-1]["signature"], TX_OPTS]).data.get("result")
        keys = (((tx or {}).get("transaction") or {}).get("message") or {}).get("accountKeys") or []
        payer = keys[0].get("pubkey") if keys and isinstance(keys[0], dict) else None
        checked += 1
        if isinstance(payer, str) and payer != wallet:
            funders.setdefault(payer, []).append(wallet)
    shared = [{"funder": f, "count": len(ws), "wallets": ws} for f, ws in funders.items() if len(ws) >= 2]
    return {"first_funders_checked": checked, "first_funders_skipped": skipped,
            "shared_first_funders": sorted(shared, key=lambda x: -x["count"])}


def slot_at_time(client: HttpClient, url: str, target: int, hint_slot: int, hint_time: int, *, max_steps: int = 16) -> int | None:
    """Find a slot whose block time is `target` (seconds), starting from a known (slot, time) pair."""
    slot = hint_slot + int((target - hint_time) / SLOT_SECONDS)
    for _ in range(max_steps):
        block_time = None
        probe = slot
        for probe in range(slot, slot + 6):  # skipped slots have no block time
            block_time = call(client, url, "getBlockTime", [probe]).data.get("result")
            if block_time is not None:
                break
        if block_time is None:
            slot += 6
            continue
        if block_time == target:
            return probe
        step = int((target - block_time) / SLOT_SECONDS)
        slot = probe + (step if step else (1 if target > block_time else -1))
    return None


def pool_state_near_slot(client: HttpClient, url: str, pool: str, mint: str, slot: int, *,
                         max_blocks: int = 30, boost: float = OBSERVED_POOL_BOOST_SOL) -> dict[str, Any] | None:
    """Pool balances after the last successful transaction touching `pool` in the first block that has one."""
    opts = {"encoding": "json", "transactionDetails": "accounts", "rewards": False,
            "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}
    for candidate in range(slot, slot + max_blocks):
        try:
            block = call(client, url, "getBlock", [candidate, opts]).data.get("result")
        except ProviderError as exc:
            if exc.kind == "rate_limited":
                raise
            continue  # skipped slot
        if not isinstance(block, dict):
            continue
        found: tuple[float, float] | None = None
        for tx in block.get("transactions") or []:
            meta = tx.get("meta") or {}
            if meta.get("err"):
                continue
            base = quote = None
            for entry in meta.get("postTokenBalances") or []:
                if entry.get("owner") != pool:
                    continue
                amount = num((entry.get("uiTokenAmount") or {}).get("uiAmountString"))
                if amount is None:
                    continue
                if entry.get("mint") == mint:
                    base = amount
                elif entry.get("mint") == WSOL_MINT:
                    quote = amount
            if base and quote:
                found = (base, quote)
        if found:
            base, quote = found
            return {"slot": candidate, "block_time": block.get("blockTime"), "pool_base_balance": base,
                    "pool_quote_balance": quote, "quote_reserve_effective": quote + boost, "boost_assumed_sol": boost,
                    "price_sol": (quote + boost) / base,
                    "reserve_model": "real WSOL balance + observed InitBoost constant (see DATA_SOURCES.md)"}
    return None
