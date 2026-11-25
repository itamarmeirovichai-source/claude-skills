"""Re-check a claim of the form "alert at time T at cap C, then N× from the alert".

Uses provider candles (and optionally one on-chain pool reading) for the exact mint. The output separates
three things that are often conflated: the quoted move from the stated time, the claimed move, and what a
position could capture — the last of which this function does NOT estimate; use the paper simulator.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from . import amm
from .config import is_valid_mint
from .providers import geckoterminal, solana_rpc
from .providers.base import HttpClient, ProviderError

CAP_DEFINITION = "price × 1,000,000,000 (fixed Pump.fun supply); an FDV-style quotation, not a realizable amount"


def parse_utc(value: str) -> float:
    """Parse an ISO-8601 time. A value without an offset is taken as UTC."""
    parsed = dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.UTC)
    return parsed.timestamp()


def iso(ts: float | None) -> str | None:
    return None if ts is None else dt.datetime.fromtimestamp(ts, dt.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def analyse_candles(candles: list[dict[str, float]], alert_time: float, *, claimed_cap_usd: float | None = None,
                    claimed_multiple: float | None = None, supply: float = amm.TOTAL_SUPPLY) -> dict[str, Any]:
    """Pure analysis of USD minute candles (oldest first). No network."""
    minute = int(alert_time // 60) * 60
    by_time = {int(c["t"]): c for c in candles}
    alert = by_time.get(minute)
    after = [c for c in candles if c["t"] >= minute]
    out: dict[str, Any] = {"alert_minute": iso(minute), "cap_definition": CAP_DEFINITION, "candles_used": len(candles),
                           "first_candle": iso(candles[0]["t"]) if candles else None, "last_candle": iso(candles[-1]["t"]) if candles else None}
    if alert is None or not after:
        out["status"] = "no_data"
        out["note"] = "no candle covers the stated alert minute; the claim cannot be checked against this source"
        return out
    peak = max(after, key=lambda c: c["h"])
    cap = {k: alert[k] * supply for k in ("o", "h", "l", "c")}
    out.update(
        status="ok",
        alert_candle_cap_usd={"open": cap["o"], "high": cap["h"], "low": cap["l"], "close": cap["c"]},
        peak_after_alert={"cap_usd": peak["h"] * supply, "time": iso(peak["t"]), "minutes_after_alert": (peak["t"] - minute) / 60},
        best_case_multiple_from_alert_open=peak["h"] / alert["o"],
        best_case_multiple_from_alert_close=peak["h"] / alert["c"],
        minutes_closing_at_or_above={f"{m}x": sum(1 for c in after if c["c"] >= m * alert["c"]) for m in (2, 5, 10, 20)},
        last_cap_usd=candles[-1]["c"] * supply,
        caveats=[
            "Best case = bought at the alert-minute price and sold at the single highest later one-minute high, "
            "with no fees, slippage, delay or price impact. Nobody can trade that; it is an upper bound.",
            "One-minute candles do not show the order of trades inside a minute.",
            "A later peak is known only in hindsight and is never a valid exit rule.",
        ],
    )
    if claimed_cap_usd:
        out["claimed_cap_usd"] = claimed_cap_usd
        out["observed_over_claimed_cap"] = cap["o"] / claimed_cap_usd
        out["peak_over_claimed_cap"] = peak["h"] * supply / claimed_cap_usd
        out["claimed_cap_seen_in_alert_minute"] = cap["l"] <= claimed_cap_usd <= cap["h"]
    if claimed_multiple:
        out["claimed_multiple"] = claimed_multiple
        out["claim_reproducible_from_alert_time"] = peak["h"] / alert["o"] >= claimed_multiple
    return out


def check_claim(gecko: HttpClient, mint: str, alert_time: float, *, claimed_cap_usd: float | None = None,
                claimed_multiple: float | None = None, rpc: HttpClient | None = None, rpc_url: str | None = None) -> dict[str, Any]:
    """Fetch minute candles for the mint's pools around `alert_time` and analyse the claim."""
    if not is_valid_mint(mint):
        raise ValueError("not a valid Solana address")
    pools = geckoterminal.normalize_pools(geckoterminal.fetch_token_pools(gecko, mint).data, mint)
    result: dict[str, Any] = {"mint": mint, "alert_time": iso(alert_time), "provider": geckoterminal.NAME,
                              "pools": [{"address": p["pool_address"], "dex": p["dex_id"], "created": iso(p["pool_created_at"])} for p in pools]}
    if not pools:
        result.update(status="no_data", note="the provider lists no pool with this mint as base token")
        return result
    merged: dict[int, dict[str, float]] = {}
    before = int(alert_time // 60) * 60 + 1000 * 60
    for pool in pools[:3]:
        try:
            candles = geckoterminal.normalize_ohlcv(geckoterminal.fetch_ohlcv(gecko, pool["pool_address"], before=before, currency="usd").data)
        except ProviderError as exc:
            result.setdefault("errors", []).append({"pool": pool["pool_address"], "kind": exc.kind, "message": exc.message})
            continue
        for c in candles:
            key = int(c["t"])
            if key not in merged or c["v"] > merged[key]["v"]:  # where two pools overlap, use the busier one
                merged[key] = c
    result.update(analyse_candles([merged[k] for k in sorted(merged)], alert_time, claimed_cap_usd=claimed_cap_usd, claimed_multiple=claimed_multiple))

    # optional independent reading straight from chain: pool balances in the block at the alert second
    if rpc is not None and rpc_url:
        curve = next((p for p in pools if p["dex_id"] == geckoterminal.CURVE_DEX), None)
        amm_pool = next((p for p in pools if p["dex_id"] == "pumpswap"), None)
        try:
            if not curve or not amm_pool:
                raise ProviderError(solana_rpc.NAME, "bad_response", "need both the bonding-curve account and a PumpSwap pool")
            launch = solana_rpc.read_launch_structure(rpc, rpc_url, curve["pool_address"], mint, max_txs=1)
            if not launch.get("creation_slot") or not launch.get("creation_time"):
                raise ProviderError(solana_rpc.NAME, "bad_response", launch.get("reason") or "creation slot not readable")
            slot = solana_rpc.slot_at_time(rpc, rpc_url, int(alert_time), launch["creation_slot"], int(launch["creation_time"]))
            state = solana_rpc.pool_state_near_slot(rpc, rpc_url, amm_pool["pool_address"], mint, slot) if slot else None
            if state:
                state["cap_sol"] = state["price_sol"] * amm.TOTAL_SUPPLY
                state["block_time"] = iso(state["block_time"])
            result["onchain_at_alert"] = state or {"status": "no pool transaction found near the alert slot"}
        except ProviderError as exc:
            result["onchain_at_alert"] = {"status": "unavailable", "kind": exc.kind, "message": exc.message}
    return result
