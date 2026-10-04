"""QA: engine memory, renormalisation, convergence and cooldown."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from pumpwatch.config import Config
from pumpwatch.engine import Engine
from pumpwatch.models import Bar, Dataset, DayScore, Filing, Post, SignalHit

from qa_helpers import D0, flat_bars, pump_dataset, weekdays


def _spike_dataset(spike_idx: int, n: int = 40) -> tuple[Dataset, list[date]]:
    days = weekdays(D0, n)
    bars = flat_bars("AAA", days)
    bars[spike_idx] = Bar("AAA", days[spike_idx], 1, 1, 1, 1, 500_000)
    return Dataset(bars), days


# -- correct today ------------------------------------------------------------------
def test_one_family_never_alerts_however_loud():
    data, _ = _spike_dataset(30)
    run = Engine(Config().with_(alert_threshold=1.0)).run(data)["AAA"]
    assert max(s.score for s in run.scores) > 50
    assert run.alerts == []


def test_missing_family_is_left_out_of_the_denominator():
    data, days = _spike_dataset(30)
    s = {x.day: x.score for x in Engine().run(data)["AAA"].scores}
    # only S1 (0.20) and S2 (0.10) are available: 100 * 0.20 * 1.0 / 0.30
    assert s[days[30]] == pytest.approx(66.67, abs=0.01)


def test_full_pump_alerts_once_with_cooldown():
    run = Engine().run(pump_dataset())["PUMP"]
    assert len(run.alerts) == 1
    assert {"market", "social", "corporate", "client"} <= set(run.alerts[0].families)


def test_cooldown_counts_from_last_emitted_alert():
    eng = Engine(Config().with_(cooldown_days=10, alert_threshold=10, min_families=1))
    hit = SignalHit("S1_abnormal_volume", "market", "AAA", D0, 1.0, "x")
    scores = [DayScore("AAA", D0 + timedelta(days=k), 50.0, [hit]) for k in (0, 5, 9, 10, 15, 20)]
    assert [a.day - D0 for a in eng.alerts_from_scores(scores)] == [timedelta(0), timedelta(10), timedelta(20)]


def test_memory_lets_spike_and_next_day_hype_meet():
    days = weekdays(D0, 40)
    bars = flat_bars("AAA", days)
    bars[30] = Bar("AAA", days[30], 1, 1, 1, 1, 500_000)
    hype = "$AAA huge news coming, get in now before it explodes 🚀🚀"
    posts = [Post("tg", f"a{k}", days[31], hype, ("AAA",)) for k in range(8)]
    run = Engine().run(Dataset(bars, posts=posts))["AAA"]
    assert [a.day for a in run.alerts] == [days[31]]


# -- QA-21: memory measured in calendar days ---------------------------------
@pytest.mark.xfail(strict=True, reason="QA-21")
def test_memory_lasts_the_same_number_of_sessions_whatever_the_weekday():
    lengths = []
    for idx in (30, 34):  # a Monday and a Friday
        data, days = _spike_dataset(idx)
        assert days[idx].weekday() in (0, 4)
        scores = {s.day: s.score for s in Engine().run(data)["AAA"].scores}
        lengths.append(sum(scores[d] > 0 for d in days[idx:]))
    assert lengths[0] == lengths[1]


# -- QA-22: duplicate bar dates --------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-22")
def test_duplicate_bar_dates_score_each_day_once():
    data, days = _spike_dataset(30)
    data.bars.append(data.bars[30])
    run = Engine().run(data)["AAA"]
    assert len(run.scores) == len({s.day for s in run.scores})


# -- QA-23: invalid memory setting --------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-23")
def test_zero_signal_memory_is_rejected():
    with pytest.raises(ValueError):
        Config().with_(signal_memory_days=0)


# -- red-team guard: news veto (documents current behaviour, see RED_TEAM.md S1-1) -----
def test_news_filing_on_spike_day_vetoes_s1_today():
    """Pinned so a fix to the PR-cover evasion is a deliberate, visible change."""

    data, days = _spike_dataset(30)
    data.filings.append(Filing("AAA", days[30], "PR", "corporate update"))
    hits = [h.signal for s in Engine().run(data)["AAA"].scores for h in s.hits]
    assert "S1_abnormal_volume" not in hits
