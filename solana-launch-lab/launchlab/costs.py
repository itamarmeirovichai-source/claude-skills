"""Venue fee schedule and transaction-cost model.

Fee tiers are transcribed from Pump.fun's official fee page as read on 2026-11-23 (page dated
16 Nov 2026; "may change … by updating this page"). They are data, not code from any third party, and can
be replaced by passing a different schedule. See DATA_SOURCES.md section 2.
"""

from __future__ import annotations

from dataclasses import dataclass

BONDING_CURVE_FEE = 0.0125  # 0.95% protocol + 0.30% creator, per side

# (lower bound of market cap in SOL, total fee per side) for canonical PumpSwap pools.
PUMPSWAP_TIERS: tuple[tuple[float, float], ...] = (
    (0, 0.01250), (420, 0.01200), (1470, 0.01150), (2460, 0.01100), (3440, 0.01050),
    (4420, 0.01000), (9820, 0.00950), (14740, 0.00900), (19650, 0.00850), (24560, 0.00800),
    (29470, 0.00750), (34380, 0.00700), (39300, 0.00650), (44210, 0.00600), (49120, 0.00550),
    (54030, 0.00525), (58940, 0.00500), (63860, 0.00475), (68770, 0.00450), (73681, 0.00425),
    (78590, 0.00400), (83500, 0.00375), (88400, 0.00350), (93330, 0.00325), (98240, 0.00300),
)
FEE_SCHEDULE_VERSION = "pumpfun-fees-2026-11-16"


def venue_fee_rate(venue: str, market_cap_sol: float | None, tiers: tuple[tuple[float, float], ...] = PUMPSWAP_TIERS) -> float:
    """Total fee per side for a trade on `venue` ("curve" or "pool") at the given market cap."""
    if venue == "curve":
        return BONDING_CURVE_FEE
    if venue != "pool":
        raise ValueError(f"unknown venue {venue!r}")
    if market_cap_sol is None or market_cap_sol < 0:
        return tiers[0][1]  # unknown cap: assume the most expensive tier
    rate = tiers[0][1]
    for lower, tier_rate in tiers:
        if market_cap_sol >= lower:
            rate = tier_rate
        else:
            break
    return rate


@dataclass(frozen=True)
class NetworkCosts:
    """Per-transaction costs in SOL that are paid whether or not the transaction succeeds."""

    base_fee_sol: float = 0.000005
    priority_fee_sol: float = 0.0005
    tip_sol: float = 0.0

    @property
    def per_attempt(self) -> float:
        return self.base_fee_sol + self.priority_fee_sol + self.tip_sol
