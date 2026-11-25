"""Seeded synthetic launch generator for the offline demo.

EVERYTHING produced here is fake. Mints start with "SYNTH" and contain characters that cannot occur in a
real Solana address. Outcomes are not scripted: each token's path comes from random order flow against the
same bonding-curve / constant-product arithmetic the simulator uses. The archetype mix is illustrative and
is NOT calibrated to any market, so results on this data say nothing about real trading.
"""

from __future__ import annotations

import random
import sqlite3
from dataclasses import dataclass
from typing import Any

from .. import amm, db
from ..config import SYNTHETIC_PREFIX

NAME = "synthetic"
EPOCH = 1767225600.0  # 2026-01-01T00:00:00Z — a fixed, obviously artificial clock
ARCHETYPES = (("dud", 0.50), ("bundled", 0.17), ("organic", 0.24), ("runner", 0.06), ("data_gap", 0.03))


@dataclass(frozen=True)
class SyntheticConfig:
    n_tokens: int = 300
    seed: int = 7
    sol_usd: float = 70.0
    spacing_s: float = 900.0
    horizon_s: float = 4 * 3600.0


class _Market:
    """Curve until the 793.1M curve tokens are sold, then a constant-product pool."""

    def __init__(self) -> None:
        self.venue = "curve"
        self.res = amm.initial_curve()
        self.curve_sold = 0.0
        self.volume_sol = 0.0

    def buy(self, sol: float) -> float:
        if self.venue == "curve":
            remaining = amm.CURVE_TOKENS_FOR_SALE - self.curve_sold
            max_cost = amm.curve_cost_for_tokens(self.res, remaining * 0.999999)
            sol = min(sol, max_cost)
        tokens, _, self.res = amm.buy(self.res, sol)
        self.volume_sol += sol
        if self.venue == "curve":
            self.curve_sold += tokens
            if self.curve_sold >= amm.CURVE_TOKENS_FOR_SALE * 0.99999:
                self.venue, self.res = "pool", amm.graduation_pool()
        return tokens

    def sell(self, tokens: float) -> float:
        if self.venue == "curve":
            tokens = min(tokens, self.curve_sold)
            if tokens <= 0:
                return 0.0
        out, _, self.res = amm.sell(self.res, tokens)
        if self.venue == "curve":
            self.curve_sold -= tokens
        self.volume_sol += out
        return out

    def real_quote(self) -> float:
        return self.res.quote - amm.INITIAL_VIRTUAL_SOL if self.venue == "curve" else self.res.quote


def _pick(rng: random.Random) -> str:
    x, acc = rng.random(), 0.0
    for name, p in ARCHETYPES:
        acc += p
        if x < acc:
            return name
    return ARCHETYPES[0][0]


def _wallet(idx: int, n: int) -> str:
    return f"{SYNTHETIC_PREFIX}wallet{idx:04d}x{n:02d}"


def generate_token(idx: int, rng: random.Random, cfg: SyntheticConfig, creators: list[dict[str, Any]]) -> dict[str, Any]:
    """Return {'token': {...}, 'observations': [(kind, observed_at, payload, missing, stale), ...]}."""
    kind = _pick(rng)
    mint = f"{SYNTHETIC_PREFIX}{idx:04d}0demo0token0not0real"
    launch = EPOCH + idx * cfg.spacing_s + rng.uniform(0, cfg.spacing_s * 0.8)
    # a few 'factory' creators launch repeatedly; everyone else launches rarely
    creator = creators[rng.randrange(5)] if rng.random() < 0.3 else creators[rng.randrange(5, len(creators))]
    market = _Market()
    obs: list[tuple[str, float, dict[str, Any], list[str], bool]] = []

    # --- creation slot ------------------------------------------------------------------------
    insiders: dict[str, float] = {}
    cosigner_groups: list[list[str]] = []
    if kind == "bundled":
        n_wallets = rng.randint(6, 20)
        target = rng.uniform(0.35, 0.78) * amm.TOTAL_SUPPLY
        weights = [rng.random() + 0.2 for _ in range(n_wallets)]
        for n, w in enumerate(weights):
            want = target * w / sum(weights)
            cost = amm.curve_cost_for_tokens(market.res, min(want, (amm.CURVE_TOKENS_FOR_SALE - market.curve_sold) * 0.98)) if market.venue == "curve" else 0.5
            insiders[_wallet(idx, n)] = market.buy(cost)
        names = list(insiders)
        cosigner_groups = [names[i:i + 7] for i in range(0, len(names), 7) if len(names[i:i + 7]) > 1]
    dev_tokens = 0.0
    if kind != "bundled" and rng.random() < 0.7:
        dev_tokens = market.buy(rng.uniform(0.05, 2.5))
    creator_wallet = creator["wallet"]
    slot0_tokens = sum(insiders.values()) + dev_tokens
    buyers = [{"wallet": w, "tokens": t, "share": t / amm.TOTAL_SUPPLY} for w, t in insiders.items()]
    if dev_tokens:
        buyers.append({"wallet": creator_wallet, "tokens": dev_tokens, "share": dev_tokens / amm.TOTAL_SUPPLY})
    obs.append(("launch", launch, {
        "status": "known", "creation_time": launch, "creator": creator_wallet,
        "creator_tokens_at_launch": dev_tokens, "creator_share_at_launch": dev_tokens / amm.TOTAL_SUPPLY,
        "slot0_buyers": sorted(buyers, key=lambda b: -b["tokens"]), "slot0_tokens_bought": slot0_tokens,
        "slot0_share": slot0_tokens / amm.TOTAL_SUPPLY, "cosigner_groups": cosigner_groups,
        "migrated_in_creation_slot": market.venue == "pool", "lp_burned_at_migration": True if market.venue == "pool" else None,
        "creator_prior_launches": creator["launches"], "creator_prior_completed": creator["completed"],
        "supply_assumed": amm.TOTAL_SUPPLY,
    }, [], False))
    creator["launches"] += 1

    # --- order flow -----------------------------------------------------------------------------
    params = {
        "dud": {"rate": 0.02, "half_life": 120.0, "buy_bias": 0.45, "size": 0.08},
        "bundled": {"rate": 0.5, "half_life": rng.uniform(600, 3600), "buy_bias": 0.62, "size": 0.6},
        "organic": {"rate": 0.3, "half_life": rng.uniform(1200, 3600), "buy_bias": 0.5, "size": 0.5},
        "runner": {"rate": 0.5, "half_life": rng.uniform(2400, 7200), "buy_bias": 0.6, "size": 0.9},
        "data_gap": {"rate": 0.3, "half_life": 1800.0, "buy_bias": 0.52, "size": 0.5},
    }[kind]
    public: float = 0.0  # tokens held by non-insider buyers
    insider_left = dict(insiders)
    dump_start = rng.uniform(20, 240)
    dump_span = rng.uniform(300, 5400)
    gap_at = rng.uniform(150, 1500) if kind == "data_gap" else None
    t, next_obs, window_vol = 0.0, 5.0, 0.0
    while t < cfg.horizon_s:
        intensity = params["rate"] * 0.5 ** (t / params["half_life"])
        dt = rng.expovariate(max(intensity, 1e-4)) if intensity > 1e-4 else cfg.horizon_s
        # emit observations that fall before the next trade (heartbeats keep a quiet token observable)
        while next_obs <= min(t + dt, cfg.horizon_s):
            if gap_at is None or next_obs < gap_at:
                price = market.res.price
                payload: dict[str, Any] = {
                    "venue": market.venue, "price_sol": price, "sol_usd": cfg.sol_usd, "price_usd": price * cfg.sol_usd,
                    "fdv_usd": price * amm.TOTAL_SUPPLY * cfg.sol_usd, "fdv_definition": "synthetic: price × 1e9",
                    "market_cap_usd": None, "market_cap_definition": "synthetic generator does not define a market cap",
                    "quote_reserve_sol": market.res.quote, "base_reserve": market.res.base,
                    "reserve_model": "synthetic exact reserves",
                    "liquidity_sol": market.real_quote(), "liquidity_usd": market.real_quote() * cfg.sol_usd,
                    "volume_window_sol": window_vol, "curve_real_sol": market.real_quote() if market.venue == "curve" else None,
                }
                missing: list[str] = []
                if rng.random() < 0.02:  # exercise missing-field handling
                    payload["quote_reserve_sol"] = payload["base_reserve"] = None
                    missing = ["quote_reserve_sol", "base_reserve"]
                obs.append(("market", launch + next_obs, payload, missing, rng.random() < 0.01))
                window_vol = 0.0
            next_obs += 15.0 if next_obs < 600 else 60.0
        t += dt
        if t >= cfg.horizon_s:
            break
        before = market.volume_sol
        # insiders work their inventory out over the dump window
        if insider_left and t > dump_start:
            wallet = max(insider_left, key=lambda w: insider_left[w])
            chunk = min(insider_left[wallet], sum(insiders.values()) * rng.uniform(0.2, 1.0) * dt / dump_span + 1.0)
            market.sell(chunk)
            insider_left[wallet] -= chunk
            if insider_left[wallet] < 1.0:
                del insider_left[wallet]
        if rng.random() < params["buy_bias"] * (0.5 ** (t / (params["half_life"] * 2))) + 0.15:
            public += market.buy(rng.lognormvariate(0, 0.9) * params["size"])
        elif public > 0:
            amount = public * rng.uniform(0.05, 0.6)
            market.sell(amount)
            public -= amount
        window_vol += market.volume_sol - before

    # --- holders snapshots (top accounts outside the pool/curve) ------------------------------
    for when in (60.0, 600.0):
        frac = 1.0 if when == 60.0 else 0.6
        top: list[dict[str, Any]] = [{"wallet": w, "tokens": t * frac, "share": t * frac / amm.TOTAL_SUPPLY} for w, t in insiders.items()]
        if dev_tokens:
            top.append({"wallet": creator_wallet, "tokens": dev_tokens, "share": dev_tokens / amm.TOTAL_SUPPLY})
        for n in range(rng.randint(3, 12)):
            amt = rng.uniform(0.0005, 0.02) * amm.TOTAL_SUPPLY
            top.append({"wallet": _wallet(idx, 50 + n), "tokens": amt, "share": amt / amm.TOTAL_SUPPLY})
        obs.append(("holders", launch + when, {"complete": True, "scope": "all non-pool accounts (synthetic)",
                                               "holders": sorted(top, key=lambda h: -h["tokens"])[:20]}, [], False))
    if market.venue == "pool":
        creator["completed"] += 1
    return {
        "token": {"mint": mint, "name": f"Synthetic #{idx:04d}", "symbol": f"SYN{idx:04d}", "creator": creator_wallet,
                  "launch_time": launch, "launch_source": "synthetic generator", "token_program": "synthetic",
                  "meta": {"synthetic_archetype": kind, "seed": cfg.seed}},
        "observations": obs,
    }


def seed_database(conn: sqlite3.Connection, cfg: SyntheticConfig | None = None) -> dict[str, Any]:
    """Write a fresh synthetic universe. Existing synthetic rows are replaced; live rows are untouched."""
    cfg = cfg or SyntheticConfig()
    rng = random.Random(cfg.seed)
    creators = [{"wallet": f"{SYNTHETIC_PREFIX}creator{n:03d}", "launches": 0, "completed": 0} for n in range(max(12, cfg.n_tokens // 2))]
    conn.execute("BEGIN")
    try:
        conn.execute("DELETE FROM observations WHERE is_synthetic = 1")
        conn.execute("DELETE FROM tokens WHERE is_synthetic = 1")
        counts: dict[str, int] = {}
        for idx in range(cfg.n_tokens):
            gen = generate_token(idx, rng, cfg, creators)
            tok = gen["token"]
            db.upsert_token(conn, tok["mint"], is_synthetic=True, now=tok["launch_time"], name=tok["name"], symbol=tok["symbol"],
                            creator=tok["creator"], launch_time=tok["launch_time"], launch_source=tok["launch_source"],
                            token_program=tok["token_program"], meta=tok["meta"])
            for kind, when, payload, missing, stale in gen["observations"]:
                db.add_observation(conn, tok["mint"], kind, NAME, when, payload, is_synthetic=True,
                                   ingested_at=when, stale=stale, missing=missing)
            counts[tok["meta"]["synthetic_archetype"]] = counts.get(tok["meta"]["synthetic_archetype"], 0) + 1
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")  # keep the write-ahead log from doubling the disk footprint
    db.log_event(conn, "synthetic_seeded", {"n_tokens": cfg.n_tokens, "seed": cfg.seed, "archetypes": counts})
    return {"n_tokens": cfg.n_tokens, "seed": cfg.seed, "archetypes": counts}
