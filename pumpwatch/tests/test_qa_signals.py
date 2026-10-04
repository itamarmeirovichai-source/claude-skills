"""QA: signal-level defects (numeric edge cases, weekends, cold starts) and guards."""

from __future__ import annotations

import math
from datetime import timedelta

import pytest

from pumpwatch.config import Config
from pumpwatch.context import build_contexts
from pumpwatch.models import Bar, BrokerFlow, Dataset, Post
from pumpwatch.signals.client import broker_flow_surge
from pumpwatch.signals.market import abnormal_volume_no_news, quiet_accumulation
from pumpwatch.signals.social import coordinated_promotion, hype_burst

from qa_helpers import D0, flat_bars, weekdays

CFG = Config()
HYPE = "$AAA get in now before it explodes, next tesla 🚀🚀"


def _ctx(data: Dataset, t: str = "AAA"):
    return build_contexts(data)[t]


# -- QA-3: NaN / inf bars --------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-3")
@pytest.mark.parametrize("field", ["volume", "close"])
@pytest.mark.parametrize("bad", [math.nan, math.inf])
def test_s1_ignores_non_finite_bar(field, bad):
    days = weekdays(D0, 30)
    last = {"volume": 10_000.0, "close": 1.0, field: bad}
    bars = flat_bars("AAA", days[:-1]) + [
        Bar("AAA", days[-1], 1, 1, 1, last["close"], last["volume"])
    ]
    assert abnormal_volume_no_news(_ctx(Dataset(bars)), days[-1], CFG) is None


@pytest.mark.xfail(strict=True, reason="QA-3")
def test_s2_ignores_nan_close_on_scored_day():
    days = weekdays(D0, 61)
    bars = flat_bars("AAA", days[:40])
    bars += [Bar("AAA", d, 1, 1, 1, 1.02 ** (i + 1), 30_000) for i, d in enumerate(days[40:60])]
    bars.append(Bar("AAA", days[60], 1, 1, 1, math.nan, 30_000))
    assert quiet_accumulation(_ctx(Dataset(bars)), days[-1], CFG) is None


def test_s1_nan_in_history_does_not_fire_on_normal_day():
    days = weekdays(D0, 30)
    bars = flat_bars("AAA", days)
    bars[5] = Bar("AAA", days[5], 1, 1, 1, 1, math.nan)
    assert abnormal_volume_no_news(_ctx(Dataset(bars)), days[-1], CFG) is None


# -- QA-4: weekend posts ---------------------------------------------------
def _weekend_case(sat_posts: int, mon_posts: int):
    days = weekdays(D0, 60)
    mon = next(d for d in days[40:] if d.weekday() == 0)
    sat = mon - timedelta(days=2)
    posts = [Post("tg", f"s{k}", sat, HYPE, ("AAA",)) for k in range(sat_posts)]
    posts += [Post("tg", f"m{k}", mon, HYPE, ("AAA",)) for k in range(mon_posts)]
    return _ctx(Dataset(flat_bars("AAA", days), posts=posts)), days, mon


def test_s4_detects_weekday_burst():
    ctx, _, mon = _weekend_case(0, 10)
    assert hype_burst(ctx, mon, CFG) is not None


@pytest.mark.xfail(strict=True, reason="QA-4")
def test_s4_detects_saturday_burst_on_next_session():
    ctx, days, _ = _weekend_case(100, 0)
    assert any(hype_burst(ctx, d, CFG) for d in days)


@pytest.mark.xfail(strict=True, reason="QA-4")
def test_s4_weekend_burst_does_not_hide_monday_burst():
    ctx, _, mon = _weekend_case(100, 10)
    assert hype_burst(ctx, mon, CFG) is not None


# -- QA-7: zero-volume baseline -------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-7")
def test_s1_tiny_trade_after_zero_volume_history_is_not_abnormal():
    days = weekdays(D0, 30)
    bars = flat_bars("AAA", days[:-1], close=6.0, volume=0) + [Bar("AAA", days[-1], 6, 6, 6, 6, 1)]
    assert abnormal_volume_no_news(_ctx(Dataset(bars)), days[-1], CFG) is None


def test_s1_fires_on_real_spike_and_respects_news():
    from pumpwatch.models import Filing

    days = weekdays(D0, 30)
    bars = flat_bars("AAA", days[:-1]) + [Bar("AAA", days[-1], 1, 1, 1, 1, 500_000)]
    assert abnormal_volume_no_news(_ctx(Dataset(bars)), days[-1], CFG).strength == 1.0
    news = Dataset(bars, filings=[Filing("AAA", days[-1], "8-K", "results")])
    assert abnormal_volume_no_news(_ctx(news), days[-1], CFG) is None


# -- QA-10: S6 cold start ----------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-10")
def test_s6_needs_a_baseline_before_firing():
    days = weekdays(D0, 10)
    data = Dataset(flat_bars("AAA", days), broker_flow=[BrokerFlow("AAA", days[5], 20, 0)])
    assert broker_flow_surge(_ctx(data), days[5], CFG) is None


def test_s6_fires_on_surge_over_established_baseline():
    days = weekdays(D0, 40)
    flows = [BrokerFlow("AAA", d, 3, 0) for d in days[:30]] + [BrokerFlow("AAA", days[30], 60, 30)]
    hit = broker_flow_surge(_ctx(Dataset(flat_bars("AAA", days), broker_flow=flows)), days[30], CFG)
    assert hit is not None and hit.strength > 0.6


# -- QA-16: short generic replies --------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-16")
def test_s5_ignores_short_generic_replies():
    days = weekdays(D0, 5)
    posts = [Post("reddit", f"u{k}", days[-1], "What happened?", ("AAA",)) for k in range(3)]
    data = Dataset(flat_bars("AAA", days), posts=posts)
    assert coordinated_promotion(_ctx(data), days[-1], CFG) is None


def test_s5_fires_on_copy_paste_campaign_and_counts_authors_not_messages():
    days = weekdays(D0, 5)
    msg = "Huge news coming for $AAA this week, get in now before it explodes, target 5 dollars"
    many = [Post("tg", f"u{k}", days[-1], msg, ("AAA",)) for k in range(4)]
    one_author = [Post("tg", "u0", days[-1], msg, ("AAA",)) for _ in range(4)]
    assert coordinated_promotion(_ctx(Dataset(flat_bars("AAA", days), posts=many)), days[-1], CFG)
    assert coordinated_promotion(_ctx(Dataset(flat_bars("AAA", days), posts=one_author)), days[-1], CFG) is None


# -- QA-18: duplicate tickers in one post -----------------------------------
@pytest.mark.xfail(strict=True, reason="QA-18")
def test_post_listing_a_ticker_twice_counts_once():
    days = weekdays(D0, 3)
    posts = [Post("x", f"u{k}", days[-1], HYPE, ("AAA", "AAA")) for k in range(3)]
    assert len(_ctx(Dataset(flat_bars("AAA", days), posts=posts)).posts_on(days[-1])) == 3


# -- numeric guards that are correct today ------------------------------------
def test_single_bar_and_zero_price_produce_no_hits():
    days = weekdays(D0, 45)
    one = _ctx(Dataset(flat_bars("AAA", days[:1])))
    assert abnormal_volume_no_news(one, days[0], CFG) is None
    assert quiet_accumulation(one, days[0], CFG) is None
    zero = _ctx(Dataset(flat_bars("AAA", days, close=0.0)))
    for d in days:
        assert abnormal_volume_no_news(zero, d, CFG) is None
        assert quiet_accumulation(zero, d, CFG) is None
