"""Frozen universe: a deterministic sample of liquid US common stocks."""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from . import config, sources
from .http import FetchError, Http

NAME_OK = re.compile(r"\bCommon (Stock|Shares)\b")
NAME_BAD = re.compile(r"\b(Warrants?|Units?|Rights?|Preferred|Depositary|Notes|Debentures?)\b")
SYMBOL_OK = re.compile(r"^[A-Z]{1,5}$")


def eligible(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Cheap first pass on the stock list. The 20-day check on price bars follows."""
    out = []
    for row in rows:
        price, volume = row.get("price"), row.get("volume")
        if (
            SYMBOL_OK.match(row["symbol"])
            and row["country"] == "United States"
            and NAME_OK.search(row["name"])
            and not NAME_BAD.search(row["name"])
            and price is not None
            and volume is not None
            and price >= config.MIN_PRICE
            and price * volume >= config.MIN_ADV_USD
        ):
            out.append(row)
    return out


def ordered(symbols: list[str], seed: str = config.SEED) -> list[str]:
    """Pseudo-random order fixed by the seed: no property of a stock decides its place."""
    return sorted(symbols, key=lambda s: hashlib.sha256(f"{seed}:{s}".encode()).hexdigest())


def liquidity(bars: list[dict[str, Any]]) -> tuple[float, float] | None:
    """(20-day average dollar volume, last close), or None when history is too short."""
    full = [b for b in bars if b["close"] and b["volume"] is not None]
    if len(full) < config.ADV_DAYS:
        return None
    last = full[-config.ADV_DAYS :]
    return sum(b["close"] * b["volume"] for b in last) / len(last), last[-1]["close"]


def build(http: Http, now: datetime | None = None) -> dict[str, Any]:
    rows = eligible(sources.screener(http))
    by_symbol = {r["symbol"]: r for r in rows}
    chosen: list[dict[str, Any]] = []
    checked = 0
    for symbol in ordered(list(by_symbol)):
        if len(chosen) >= config.UNIVERSE_SIZE:
            break
        checked += 1
        try:
            liq = liquidity(sources.bars(http, symbol, "3mo"))
        except FetchError:
            continue
        if liq and liq[0] >= config.MIN_ADV_USD and liq[1] >= config.MIN_PRICE:
            chosen.append(
                {
                    "symbol": symbol,
                    "name": by_symbol[symbol]["name"],
                    "adv_usd": round(liq[0]),
                    "last_close": round(liq[1], 2),
                }
            )
    return {
        "built_at": (now or datetime.now(UTC)).isoformat(timespec="seconds"),
        "seed": config.SEED,
        "first_pass": len(rows),
        "checked": checked,
        "tickers": chosen,
    }
