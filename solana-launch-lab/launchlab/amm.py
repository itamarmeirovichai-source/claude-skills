"""Bonding-curve and constant-product arithmetic.

Independent implementation of textbook x*y=k mathematics and of the formulas in Pump.fun's public
documentation (see DATA_SOURCES.md section 2). Pure functions, no I/O.

Units: quote amounts in SOL (float), token amounts in whole tokens (float). Floats are adequate for a
simulator whose inputs are already uncertain by far more than float error; the functions are monotone and
never return a negative amount.
"""

from __future__ import annotations

from dataclasses import dataclass

# Pump.fun launch constants (DOC + CHAIN, 2026-11-23).
TOTAL_SUPPLY = 1_000_000_000.0
INITIAL_VIRTUAL_TOKENS = 1_073_000_000.0
INITIAL_VIRTUAL_SOL = 30.0
CURVE_TOKENS_FOR_SALE = 793_100_000.0
MIGRATED_TOKENS = 206_900_000.0
# Amount the migration's InitBoost instruction moves out of the pool's quote account while pricing still
# counts it (CHAIN observation on three pools; not found in official docs).
OBSERVED_POOL_BOOST_SOL = 17.584505288


@dataclass(frozen=True)
class Reserves:
    """Effective reserves used for pricing: quote in SOL, base in tokens."""

    quote: float
    base: float

    def __post_init__(self) -> None:
        if self.quote <= 0 or self.base <= 0:
            raise ValueError("reserves must be positive")

    @property
    def price(self) -> float:
        """Marginal price in SOL per token."""
        return self.quote / self.base

    def market_cap(self, supply: float = TOTAL_SUPPLY) -> float:
        """Price times supply, in SOL. This is an FDV-style quotation, not a realizable amount."""
        return self.price * supply


def buy(reserves: Reserves, quote_in: float, fee_rate: float = 0.0) -> tuple[float, float, Reserves]:
    """Spend `quote_in` SOL (fee taken from the input). Returns (tokens_out, fee_paid, reserves_after)."""
    if quote_in < 0 or not 0 <= fee_rate < 1:
        raise ValueError("quote_in must be >= 0 and fee_rate in [0, 1)")
    if quote_in == 0:
        return 0.0, 0.0, reserves
    fee = quote_in * fee_rate
    net = quote_in - fee
    tokens_out = reserves.base * net / (reserves.quote + net)
    return tokens_out, fee, Reserves(reserves.quote + net, reserves.base - tokens_out)


def sell(reserves: Reserves, tokens_in: float, fee_rate: float = 0.0) -> tuple[float, float, Reserves]:
    """Sell `tokens_in` tokens (fee taken from the output). Returns (quote_out_net, fee_paid, reserves_after)."""
    if tokens_in < 0 or not 0 <= fee_rate < 1:
        raise ValueError("tokens_in must be >= 0 and fee_rate in [0, 1)")
    if tokens_in == 0:
        return 0.0, 0.0, reserves
    gross = reserves.quote * tokens_in / (reserves.base + tokens_in)
    fee = gross * fee_rate
    return gross - fee, fee, Reserves(reserves.quote - gross, reserves.base + tokens_in)


def price_ratio_after_sale(base_reserve: float, tokens_sold: float) -> float:
    """P_after / P_before when `tokens_sold` tokens hit a constant-product pool holding `base_reserve`.

    Derivation: k = x*y. After the sale y' = y + q, x' = k / y'. Price = x/y, so
    P'/P = (x'/y') / (x/y) = (y / (y + q))**2.
    """
    if base_reserve <= 0 or tokens_sold < 0:
        raise ValueError("base_reserve must be > 0 and tokens_sold >= 0")
    return (base_reserve / (base_reserve + tokens_sold)) ** 2


def buy_price_impact(quote_reserve: float, quote_in: float) -> float:
    """Average execution price over spot price, minus one, for a fee-free buy: equals quote_in / reserve."""
    if quote_reserve <= 0 or quote_in < 0:
        raise ValueError("quote_reserve must be > 0 and quote_in >= 0")
    return quote_in / quote_reserve


def initial_curve() -> Reserves:
    """Virtual reserves of a fresh Pump.fun bonding curve."""
    return Reserves(INITIAL_VIRTUAL_SOL, INITIAL_VIRTUAL_TOKENS)


def curve_cost_for_tokens(reserves: Reserves, tokens_out: float) -> float:
    """SOL needed (before fees) to take `tokens_out` tokens from a curve in state `reserves`."""
    if tokens_out < 0 or tokens_out >= reserves.base:
        raise ValueError("tokens_out must be in [0, base reserve)")
    return tokens_out * reserves.quote / (reserves.base - tokens_out)


def curve_state_after_sold(tokens_sold: float) -> Reserves:
    """Virtual reserves after `tokens_sold` of the 793.1M curve tokens have been bought from launch."""
    if not 0 <= tokens_sold <= CURVE_TOKENS_FOR_SALE:
        raise ValueError("tokens_sold out of range")
    start = initial_curve()
    cost = curve_cost_for_tokens(start, tokens_sold)
    return Reserves(start.quote + cost, start.base - tokens_sold)


def graduation_pool() -> Reserves:
    """Effective reserves of the PumpSwap pool right after migration (before any pool trade)."""
    raised = curve_cost_for_tokens(initial_curve(), CURVE_TOKENS_FOR_SALE)
    return Reserves(raised, MIGRATED_TOKENS)


def effective_pool_reserves(real_quote: float, base: float, boost: float = OBSERVED_POOL_BOOST_SOL) -> Reserves:
    """Pricing reserves of a migrated PumpSwap pool from its on-chain balances (observed behaviour)."""
    return Reserves(real_quote + boost, base)
