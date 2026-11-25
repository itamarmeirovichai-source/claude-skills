"""The pre-registered rules: which launches become paper candidates, and when a paper position exits.

Change a rule => change RULESET, because results from different rules must never be pooled. Every signal
stores the ruleset name and the number of rulesets tried is part of the evaluation plan
(PROJECT_SPEC.md section 10).

These rules are a *baseline to be tested*, not a recommendation. Nothing here is a buy signal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

RULESET = "baseline-v1"


@dataclass(frozen=True)
class DecisionRule:
    """A launch is rejected if any structural check fails or cannot be read."""

    max_slot0_share: float = 0.25        # share of supply bought in the creation slot
    max_creator_share: float = 0.10      # creator's own buy in the creation transaction
    max_cosigned_share: float = 0.10     # supply bought by wallets that co-signed one transaction
    serial_min_launches: int = 5         # creator with this many earlier launches ...
    serial_max_completed_rate: float = 0.10  # ... of which fewer than this share completed the curve
    min_liquidity_sol: float = 3.0       # real SOL in the curve or pool at decision time
    max_data_age_s: float = 60.0         # newest market observation must be this fresh at decision time
    require_launch_structure: bool = True


@dataclass(frozen=True)
class ExitRule:
    take_profit: float = 2.0   # exit when price >= take_profit x entry price
    stop_loss: float = 0.5     # exit when price <= stop_loss x entry price
    max_hold_s: float = 1800.0  # exit after this long regardless of price


def decide(features: dict[str, Any], rule: DecisionRule | None = None) -> tuple[str, list[str]]:
    """Return ('candidate' | 'rejected', reasons). Each reason is "code: explanation". `features` must contain
    only information available at the decision time; paper.build_features guarantees that."""
    rule = rule or DecisionRule()
    reasons: list[str] = []
    status = features.get("launch_status")
    if status not in ("known", "partial"):
        if rule.require_launch_structure:
            reasons.append("launch_unknown: creation-slot buyers could not be read")
    else:
        share = features.get("slot0_share")
        if share is not None and share >= rule.max_slot0_share:
            reasons.append(f"slot0_concentration: creation-slot buyers took {share:.1%} of supply (limit {rule.max_slot0_share:.0%})")
        creator_share = features.get("creator_share")
        if creator_share is not None and creator_share >= rule.max_creator_share:
            reasons.append(f"creator_share: creator bought {creator_share:.1%} at launch (limit {rule.max_creator_share:.0%})")
        cosigned = features.get("cosigned_share")
        if cosigned is not None and cosigned >= rule.max_cosigned_share:
            reasons.append(f"cosigned_supply: co-signing wallets bought {cosigned:.1%} of supply (limit {rule.max_cosigned_share:.0%})")
    launches, completed = features.get("creator_prior_launches"), features.get("creator_prior_completed")
    if (launches is not None and completed is not None and launches >= rule.serial_min_launches
            and completed / launches < rule.serial_max_completed_rate):
        reasons.append(f"serial_creator: {launches} earlier launches, {completed} completed the curve")
    if features.get("price_sol") is None:
        reasons.append("no_price: no market price at decision time")
    else:
        age = features.get("market_age_s")
        if age is not None and age > rule.max_data_age_s:
            reasons.append(f"stale_market_data: newest market data is {age:.0f}s old at decision time (limit {rule.max_data_age_s:.0f}s)")
        liquidity = features.get("liquidity_sol")
        if liquidity is None:
            reasons.append("liquidity_unknown: depth not available at decision time")
        elif liquidity < rule.min_liquidity_sol:
            reasons.append(f"low_liquidity: {liquidity:.2f} SOL of depth, below {rule.min_liquidity_sol:.1f} SOL")
    return ("rejected" if reasons else "candidate"), reasons


def exit_trigger(entry_price: float, entry_time: float, obs_time: float, obs_price: float | None,
                 rule: ExitRule | None = None) -> str | None:
    """Should a position entered at (entry_time, entry_price) exit on seeing this observation?

    Returns a reason string or None. This function only ever sees the *current* observation, never a
    later one, so it cannot use a future high. The simulator then executes the exit one latency later,
    at whatever price exists then.

    DESIGN NOTE — this is the most consequential choice in the study and it is yours to change:
    a tight stop cuts losses but is hit by ordinary noise on thin pools; a wide take-profit keeps the
    rare large mover but gives back gains on the common round trip; a short time stop limits exposure
    to insider dumping but exits before slow movers move. Whatever you choose, fix it BEFORE looking at
    outcomes and bump RULESET when you change it.
    """
    rule = rule or ExitRule()
    if obs_time - entry_time >= rule.max_hold_s:
        return "time_stop"
    if obs_price is None or entry_price <= 0:
        return None
    ratio = obs_price / entry_price
    if ratio <= rule.stop_loss:
        return "stop_loss"
    if ratio >= rule.take_profit:
        return "take_profit"
    return None
