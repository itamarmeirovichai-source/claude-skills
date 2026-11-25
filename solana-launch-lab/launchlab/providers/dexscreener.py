"""DEX Screener adapter: current market state for an exact mint.

Docs: https://docs.dexscreener.com/api/reference (read 2026-11-23). No key. 300 requests/min on the token
endpoints. No historical candles. The docs do not define `marketCap`, `fdv` or `liquidity.usd`, so each
value is stored with the provider's own field name as its definition.
"""

from __future__ import annotations

from typing import Any

from .base import FetchResult, HttpClient, missing_fields, num

NAME = "dexscreener"
BASE = "https://api.dexscreener.com"
REQUIRED = ("price_usd", "price_sol", "fdv_usd", "liquidity_usd")


def make_client(**overrides: Any) -> HttpClient:
    return HttpClient(provider=NAME, min_interval_s=0.25, **overrides)


def fetch_token_pairs(client: HttpClient, mint: str) -> FetchResult:
    return client.request_json(f"{BASE}/tokens/v1/solana/{mint}")


def venue_for(dex_id: str | None) -> str | None:
    if dex_id == "pumpfun":
        return "curve"
    return "pool" if dex_id else None


def normalize_pair(pair: dict[str, Any], mint: str) -> dict[str, Any] | None:
    """Turn one pair record into a market-observation payload. Returns None if it is not for `mint`."""
    base = pair.get("baseToken") or {}
    if base.get("address") != mint:
        return None  # the mint is the quote side or a different token: never mix identities
    price_usd = num(pair.get("priceUsd"))
    price_native = num(pair.get("priceNative"))
    quote = pair.get("quoteToken") or {}
    quote_is_sol = quote.get("symbol") == "SOL"
    liquidity = pair.get("liquidity") or {}
    volume = pair.get("volume") or {}
    payload: dict[str, Any] = {
        "name": base.get("name"),
        "symbol": base.get("symbol"),
        "dex_id": pair.get("dexId"),
        "venue": venue_for(pair.get("dexId")),
        "pool_address": pair.get("pairAddress"),
        "quote_symbol": quote.get("symbol"),
        "price_usd": price_usd,
        "price_sol": price_native if quote_is_sol else None,
        "sol_usd": (price_usd / price_native) if (quote_is_sol and price_usd and price_native) else None,
        "fdv_usd": num(pair.get("fdv")),
        "fdv_definition": "dexscreener `fdv` (undefined in provider docs)",
        "market_cap_usd": num(pair.get("marketCap")),
        "market_cap_definition": "dexscreener `marketCap` (undefined in provider docs)",
        "liquidity_usd": num(liquidity.get("usd")),
        "liquidity_definition": "dexscreener `liquidity.usd` (observed: USD value of both pool token balances)",
        "pool_base_balance": num(liquidity.get("base")),
        "pool_quote_balance": num(liquidity.get("quote")),
        "volume_24h_usd": num(volume.get("h24")),
        "pair_created_at": (num(pair.get("pairCreatedAt")) or 0) / 1000 or None,
        "source_url": pair.get("url"),
    }
    payload["missing"] = missing_fields(payload, REQUIRED)
    return payload


def normalize_response(data: Any, mint: str) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        return []
    out = []
    for pair in data:
        if isinstance(pair, dict):
            norm = normalize_pair(pair, mint)
            if norm is not None:
                out.append(norm)
    return out
