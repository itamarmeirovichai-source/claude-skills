"""AMM arithmetic on examples small enough to check by hand."""

import pytest

from launchlab import amm
from launchlab.costs import BONDING_CURVE_FEE, venue_fee_rate


def test_buy_without_fee_matches_hand_calculation():
    # 100 SOL / 1,000,000 tokens. Spending 10 SOL: out = 1e6 * 10 / 110 = 90,909.0909...
    tokens, fee, after = amm.buy(amm.Reserves(100.0, 1_000_000.0), 10.0)
    assert tokens == pytest.approx(90_909.090909, rel=1e-9)
    assert fee == 0
    assert after.quote == pytest.approx(110.0) and after.base == pytest.approx(909_090.909091)
    assert after.quote * after.base == pytest.approx(100.0 * 1_000_000.0)  # k is preserved


def test_buy_then_sell_round_trip_returns_the_stake_when_free():
    start = amm.Reserves(100.0, 1_000_000.0)
    tokens, _, mid = amm.buy(start, 10.0)
    out, _, end = amm.sell(mid, tokens)
    assert out == pytest.approx(10.0)
    assert end.quote == pytest.approx(start.quote)


def test_fee_is_taken_from_input_on_buy_and_output_on_sell():
    tokens, fee, _ = amm.buy(amm.Reserves(100.0, 1_000_000.0), 10.0, 0.01)
    assert fee == pytest.approx(0.1)
    assert tokens == pytest.approx(1_000_000.0 * 9.9 / 109.9)
    out, fee, _ = amm.sell(amm.Reserves(100.0, 1_000_000.0), 100_000.0, 0.01)
    gross = 100.0 * 100_000.0 / 1_100_000.0  # 9.0909...
    assert fee == pytest.approx(gross * 0.01) and out == pytest.approx(gross * 0.99)


def test_price_ratio_after_sale_is_the_square_law():
    # selling an amount equal to the pool's token reserve halves x and doubles y: price falls to 1/4
    assert amm.price_ratio_after_sale(1_000_000.0, 1_000_000.0) == pytest.approx(0.25)
    assert amm.price_ratio_after_sale(1_000_000.0, 0.0) == 1.0
    _, _, after = amm.sell(amm.Reserves(100.0, 1_000_000.0), 250_000.0)
    assert after.price / 1e-4 == pytest.approx(amm.price_ratio_after_sale(1_000_000.0, 250_000.0))


def test_bonding_curve_constants_reproduce_documented_figures():
    start = amm.initial_curve()
    assert start.market_cap() == pytest.approx(27.9590, abs=1e-3)           # 30 / 1.073e9 * 1e9 SOL
    raised = amm.curve_cost_for_tokens(start, amm.CURVE_TOKENS_FOR_SALE)
    assert raised == pytest.approx(85.005, abs=1e-3)                          # SOL raised at completion
    end = amm.curve_state_after_sold(amm.CURVE_TOKENS_FOR_SALE)
    assert end.market_cap() == pytest.approx(410.9, abs=0.1)                  # market cap at completion
    assert amm.graduation_pool().base == amm.MIGRATED_TOKENS


def test_observed_pool_pricing_matches_the_audited_reading():
    # BartCoin pool, last transaction read on 2026-11-22: 2.3441 SOL real, 971,816,856 tokens; DexScreener quoted 2.062e-8
    res = amm.effective_pool_reserves(2.3441, 971_816_856.0)
    assert res.price == pytest.approx(2.05e-8, rel=0.01)


def test_invalid_inputs_are_rejected_not_guessed():
    with pytest.raises(ValueError):
        amm.Reserves(0.0, 1.0)
    with pytest.raises(ValueError):
        amm.buy(amm.Reserves(1.0, 1.0), -1.0)
    with pytest.raises(ValueError):
        amm.sell(amm.Reserves(1.0, 1.0), 1.0, 1.0)
    with pytest.raises(ValueError):
        amm.curve_cost_for_tokens(amm.initial_curve(), 2e9)


def test_fee_tiers_follow_the_documented_table():
    assert venue_fee_rate("curve", None) == BONDING_CURVE_FEE == 0.0125
    assert venue_fee_rate("pool", 0) == 0.0125
    assert venue_fee_rate("pool", 419.9) == 0.0125
    assert venue_fee_rate("pool", 420) == 0.0120
    assert venue_fee_rate("pool", 7359) == 0.0100      # BartCoin at its claimed alert time
    assert venue_fee_rate("pool", 11637) == 0.0095     # MAYA at its claimed alert time
    assert venue_fee_rate("pool", 1e6) == 0.0030
    assert venue_fee_rate("pool", None) == 0.0125      # unknown cap -> most expensive tier
    with pytest.raises(ValueError):
        venue_fee_rate("somewhere", 1.0)
