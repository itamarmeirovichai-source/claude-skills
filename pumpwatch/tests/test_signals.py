from datetime import timedelta

from helpers import dataset, days, flat_bars, promo_posts, with_spike

from pumpwatch.config import Config
from pumpwatch.context import build_contexts
from pumpwatch.models import Bar, BrokerFlow, Dataset, Filing, Post, VictimReport
from pumpwatch.signals import ALL_SIGNALS
from pumpwatch.signals.client import broker_flow_surge, victim_reports
from pumpwatch.signals.corporate import suspicious_filings
from pumpwatch.signals.market import abnormal_volume_no_news, quiet_accumulation
from pumpwatch.signals.social import coordinated_promotion, hype_burst

CFG = Config()


def ctx_of(data: Dataset, ticker: str = "ABC"):
    return build_contexts(data)[ticker]


# S1 ---------------------------------------------------------------------
def test_s1_fires_on_unexplained_volume():
    bars = with_spike(flat_bars("ABC", 80), 70, vol_mult=20)
    hit = abnormal_volume_no_news(ctx_of(dataset(bars)), bars[70].day, CFG)
    assert hit is not None and hit.family == "market" and 0 < hit.strength <= 1


def test_s1_silent_when_news_explains_volume():
    bars = with_spike(flat_bars("ABC", 80), 70, vol_mult=20)
    news = Filing("ABC", bars[70].day, "8-K", "FDA approval")
    assert abnormal_volume_no_news(ctx_of(dataset(bars, [news])), bars[70].day, CFG) is None


def test_s1_needs_history():
    bars = with_spike(flat_bars("ABC", 10), 9, vol_mult=50)
    assert abnormal_volume_no_news(ctx_of(dataset(bars)), bars[9].day, CFG) is None


def test_s1_zero_volume_history_does_not_crash():
    bars = [Bar("ABC", d, 1, 1, 1, 1, 0) for d in days(40)]
    bars[-1] = Bar("ABC", bars[-1].day, 1, 1, 1, 1, 1_000_000)
    hit = abnormal_volume_no_news(ctx_of(dataset(bars)), bars[-1].day, CFG)
    assert hit is not None and hit.strength == 1.0


# S2 ---------------------------------------------------------------------
def test_s2_detects_steady_climb_on_rising_volume():
    ds = days(110)
    bars, p = [], 1.0
    for i, d in enumerate(ds):
        if i >= 85:
            p *= 1.02
        v = 300_000 if i >= 85 else 100_000
        bars.append(Bar("ABC", d, p, p, p, p, v))
    hit = quiet_accumulation(ctx_of(dataset(bars)), ds[105], CFG)
    assert hit is not None


def test_s2_ignores_single_jump():
    bars = with_spike(flat_bars("ABC", 110), 105, vol_mult=5, price_mult=1.6)
    assert quiet_accumulation(ctx_of(dataset(bars)), bars[105].day, CFG) is None


# S3 ---------------------------------------------------------------------
def test_s3_flags_dilution_and_red_flags():
    bars = flat_bars("ABC", 120)
    d = bars[100].day
    filings = [
        Filing("ABC", d - timedelta(days=30), "S-1", "registration"),
        Filing("ABC", d - timedelta(days=10), "8-K", "Name change to AI Robotics Corp"),
    ]
    hit = suspicious_filings(ctx_of(dataset(bars, filings)), d, CFG)
    assert hit is not None and "S-1" in hit.evidence and "name change" in hit.evidence


def test_s3_flags_dormant_shell_waking_up():
    bars = flat_bars("ABC", 120)
    d = bars[110].day
    filings = [Filing("ABC", d - timedelta(days=900), "10-K", "annual"), Filing("ABC", d - timedelta(days=5), "10-Q", "quarterly")]
    hit = suspicious_filings(ctx_of(dataset(bars, filings)), d, CFG)
    assert hit is not None and "silence" in hit.evidence


def test_s3_quiet_for_routine_reports():
    bars = flat_bars("ABC", 120)
    d = bars[110].day
    filings = [Filing("ABC", d - timedelta(days=d_), "10-Q", "quarterly report") for d_ in (5, 95)]
    assert suspicious_filings(ctx_of(dataset(bars, filings)), d, CFG) is None


def test_s3_ai_word_needs_whole_word():
    bars = flat_bars("ABC", 120)
    d = bars[110].day
    f = [Filing("ABC", d - timedelta(days=5), "8-K", "Chairman retires")]
    assert suspicious_filings(ctx_of(dataset(bars, f)), d, CFG) is None


# S4 / S5 ----------------------------------------------------------------
def test_s4_fires_on_hype_burst_from_quiet_baseline():
    bars = flat_bars("ABC", 60)
    d = bars[50].day
    hit = hype_burst(ctx_of(dataset(bars, posts=promo_posts("ABC", d, 8))), d, CFG)
    assert hit is not None and hit.family == "social"


def test_s4_silent_for_calm_chatter():
    bars = flat_bars("ABC", 60)
    d = bars[50].day
    posts = [Post("reddit", f"u{i}", d, f"$ABC results were ok, nothing special, note {i}", ("ABC",)) for i in range(10)]
    assert hype_burst(ctx_of(dataset(bars, posts=posts)), d, CFG) is None


def test_s5_needs_several_distinct_authors():
    bars = flat_bars("ABC", 60)
    d = bars[50].day
    same_author = [Post("telegram", "a1", d, "$ABC is about to explode, huge news coming, get in now", ("ABC",)) for _ in range(6)]
    assert coordinated_promotion(ctx_of(dataset(bars, posts=same_author)), d, CFG) is None
    assert coordinated_promotion(ctx_of(dataset(bars, posts=promo_posts("ABC", d, 5))), d, CFG) is not None


# S6 / S7 ----------------------------------------------------------------
def test_s6_and_s7_customer_signals():
    bars = flat_bars("ABC", 60)
    d = bars[50].day
    flows = [BrokerFlow("ABC", bars[i].day, 3, 0) for i in range(20, 50)] + [BrokerFlow("ABC", d, 120, 80)]
    data = Dataset(bars=bars, broker_flow=flows, reports=[VictimReport("ABC", d, "screenshot")])
    ctx = ctx_of(data)
    assert broker_flow_surge(ctx, d, CFG) is not None
    assert victim_reports(ctx, d, CFG) is not None


def test_all_signals_registered_with_families():
    assert len(ALL_SIGNALS) == 7
