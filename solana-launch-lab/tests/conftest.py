"""Shared fixtures. Tests never touch the network: every HTTP client gets a fake transport."""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launchlab import db
from launchlab.config import PaperConfig, Settings

# A frictionless configuration so expected numbers can be worked out by hand.
FRICTIONLESS = PaperConfig(
    size_sol=1.0, latency_s=10.0, decision_delay_s=60.0, max_wait_s=60.0, fail_prob=0.0, max_attempts=3, retry_delay_s=5.0,
    base_fee_sol=0.0, priority_fee_sol=0.0, tip_sol=0.0, token_account_rent_sol=0.0, extra_slippage_bps=0.0,
    max_pool_share=1.0, min_exit_liquidity_sol=0.0, venue_fee_override=0.0, seed=1,
)


@pytest.fixture
def conn():
    connection = db.connect(":memory:")
    yield connection
    connection.close()


@pytest.fixture
def settings() -> Settings:
    return Settings(mode="demo", db_path=Path(":memory:"), paper=FRICTIONLESS)


def with_paper(settings: Settings, **changes) -> Settings:
    return dataclasses.replace(settings, paper=dataclasses.replace(settings.paper, **changes))


def market(conn, mint: str, t: float, quote: float | None, base: float | None, *, price: float | None = None,
           stale: bool = False, synthetic: bool = True, liquidity: float | None = None, venue: str = "pool") -> int:
    """Store one market observation. With reserves the price is quote/base."""
    if price is None and quote and base:
        price = quote / base
    payload = {"venue": venue, "price_sol": price, "quote_reserve_sol": quote, "base_reserve": base,
               "liquidity_sol": liquidity if liquidity is not None else quote, "sol_usd": 100.0}
    return db.add_observation(conn, mint, "market", "test", t, payload, is_synthetic=synthetic, ingested_at=t, stale=stale)


def launch(conn, mint: str, t: float, *, slot0_share: float = 0.01, creator_share: float = 0.01, groups=None, buyers=None,
           status: str = "known", prior=(0, 0), synthetic: bool = True) -> None:
    db.upsert_token(conn, mint, is_synthetic=synthetic, now=t, launch_time=t, launch_source="test", symbol="TST")
    payload = {"status": status, "creation_time": t, "creator": "creatorwallet", "creator_share_at_launch": creator_share,
               "slot0_share": slot0_share, "slot0_buyers": buyers or [], "cosigner_groups": groups or [],
               "creator_prior_launches": prior[0], "creator_prior_completed": prior[1]}
    db.add_observation(conn, mint, "launch", "test", t, payload, is_synthetic=synthetic, ingested_at=t)


class FakeTransport:
    """Scripted HTTP transport: a list of (status, headers, body) or a callable(method, url, body)."""

    def __init__(self, script):
        self.script, self.calls = script, []

    def __call__(self, method, url, headers, body, timeout):
        self.calls.append((method, url, json.loads(body) if body else None))
        step = self.script(method, url, json.loads(body) if body else None) if callable(self.script) else self.script.pop(0)
        if isinstance(step, Exception):
            raise step
        status, hdrs, payload = step
        return status, hdrs, payload if isinstance(payload, bytes) else json.dumps(payload).encode()


class FakeClock:
    def __init__(self, start: float = 1_000_000.0):
        self.now, self.sleeps = start, []

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds
