"""GeckoTerminal adapter: pools of a mint, OHLCV history, newest pools.

Docs: https://api.geckoterminal.com/docs/v2/swagger.json (read 2026-11-23). No key. "Approximately 10
calls/minute"; responses cached about a minute. OHLCV: minute/hour/day, limit <= 1000, `before_timestamp`.
`market_cap_usd` is null unless verified; `fdv_usd` is price times total supply. Terms were not readable
(bot challenge), so raw storage is off by default.
"""

from __future__ import annotations

from typing import Any

from .base import FetchResult, HttpClient, num

NAME = "geckoterminal"
BASE = "https://api.geckoterminal.com/api/v2/networks/solana"
CURVE_DEX = "pump-fun"
TIMEFRAMES = {"minute": (1, 5, 15), "hour": (1, 4, 12), "day": (1,)}


def make_client(**overrides: Any) -> HttpClient:
    return HttpClient(provider=NAME, min_interval_s=6.5, backoff_s=8.0, max_backoff_s=45.0, **overrides)


def fetch_token_pools(client: HttpClient, mint: str) -> FetchResult:
    return client.request_json(f"{BASE}/tokens/{mint}/pools?page=1")


def fetch_new_pools(client: HttpClient, page: int = 1) -> FetchResult:
    return client.request_json(f"{BASE}/new_pools?page={int(page)}")


def fetch_ohlcv(client: HttpClient, pool: str, *, timeframe: str = "minute", aggregate: int = 1,
                before: int | None = None, limit: int = 1000, currency: str = "token") -> FetchResult:
    if timeframe not in TIMEFRAMES or aggregate not in TIMEFRAMES[timeframe]:
        raise ValueError("unsupported timeframe/aggregate")
    if currency not in {"token", "usd"}:
        raise ValueError("currency must be 'token' or 'usd'")
    url = f"{BASE}/pools/{pool}/ohlcv/{timeframe}?aggregate={aggregate}&limit={max(1, min(int(limit), 1000))}&currency={currency}&token=base"
    if before is not None:
        url += f"&before_timestamp={int(before)}"
    return client.request_json(url)


def _dex_id(item: dict[str, Any]) -> str | None:
    return (((item.get("relationships") or {}).get("dex") or {}).get("data") or {}).get("id")


def _rel_address(item: dict[str, Any], key: str) -> str | None:
    rel = (((item.get("relationships") or {}).get(key) or {}).get("data") or {}).get("id")
    return rel.split("_", 1)[1] if isinstance(rel, str) and "_" in rel else None


def parse_time(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    import datetime as dt

    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def normalize_pools(data: Any, mint: str | None = None) -> list[dict[str, Any]]:
    """Pool records. With `mint`, keeps only pools whose base token is that mint."""
    items = data.get("data") if isinstance(data, dict) else None
    out: list[dict[str, Any]] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        attrs = item.get("attributes") or {}
        base_mint = _rel_address(item, "base_token")
        if mint is not None and base_mint != mint:
            continue
        dex = _dex_id(item)
        out.append({
            "pool_address": attrs.get("address"),
            "pool_name": attrs.get("name"),
            "base_mint": base_mint,
            "quote_mint": _rel_address(item, "quote_token"),
            "dex_id": dex,
            "venue": "curve" if dex == CURVE_DEX else "pool",
            "pool_created_at": parse_time(attrs.get("pool_created_at")),
            "price_usd": num(attrs.get("base_token_price_usd")),
            "price_sol": num(attrs.get("base_token_price_native_currency")),
            "fdv_usd": num(attrs.get("fdv_usd")),
            "fdv_definition": "geckoterminal `fdv_usd` (price × total supply)",
            "market_cap_usd": num(attrs.get("market_cap_usd")),
            "market_cap_definition": "geckoterminal `market_cap_usd` (null unless verified)",
            "liquidity_usd": num(attrs.get("reserve_in_usd")),
            "liquidity_definition": "geckoterminal `reserve_in_usd`",
            "volume_24h_usd": num((attrs.get("volume_usd") or {}).get("h24")),
        })
    return out


def normalize_ohlcv(data: Any) -> list[dict[str, float]]:
    """Candles oldest first: {t, o, h, l, c, v}. Malformed rows are dropped, never repaired."""
    rows = (((data or {}).get("data") or {}).get("attributes") or {}).get("ohlcv_list") if isinstance(data, dict) else None
    out: list[dict[str, float]] = []
    for row in rows or []:
        if not isinstance(row, list) or len(row) < 6:
            continue
        vals = [num(x) for x in row[:6]]
        if any(v is None for v in vals):
            continue
        t, o, h, low, c, v = (float(x) for x in vals if x is not None)
        if min(o, h, low, c) <= 0:
            continue
        out.append({"t": t, "o": o, "h": h, "l": low, "c": c, "v": v})
    out.sort(key=lambda r: r["t"])
    return out
