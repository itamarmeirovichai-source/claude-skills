"""QA: scoring day D must not depend on anything dated after D.

The per-signal and same-sources engine tests guard behaviour that is correct
today. The cross-source engine test pins defect QA-1 (renormalisation reads the
whole dataset).
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from pumpwatch.context import build_contexts
from pumpwatch.config import Config
from pumpwatch.engine import Engine
from pumpwatch.models import Bar, BrokerFlow, Filing, Post, VictimReport
from pumpwatch.signals import ALL_SIGNALS

from qa_helpers import pump_dataset, truncate, weekdays, D0

DATA = pump_dataset()
DAYS = sorted({b.day for b in DATA.bars})
CFG = Config()


@pytest.mark.parametrize("name", sorted(ALL_SIGNALS))
def test_every_signal_ignores_data_after_scored_day(name):
    full = build_contexts(DATA)["PUMP"]
    fired = 0
    for d in DAYS:
        cut = build_contexts(truncate(DATA, d))["PUMP"]
        a = ALL_SIGNALS[name](full, d, CFG)
        b = ALL_SIGNALS[name](cut, d, CFG)
        assert a == b, f"{name} on {d}: {a} != {b}"
        fired += a is not None
    assert fired, f"fixture never exercises {name}"


@pytest.mark.parametrize("name", sorted(ALL_SIGNALS))
def test_every_signal_ignores_poisoned_future(name):
    """Extreme records dated after D (huge volume, hype, filings, flows) change nothing on D."""

    d = DAYS[60]
    future = d + timedelta(days=1)
    poisoned = truncate(DATA, d)
    poisoned.bars.append(Bar("PUMP", future, 9.0, 9.0, 9.0, 9.0, 1e9))
    poisoned.filings.append(Filing("PUMP", future, "8-K", "name change"))
    poisoned.posts.extend(
        Post("x", f"bot{k}", future, "$PUMP to the moon 100x 🚀🚀🚀", ("PUMP",)) for k in range(20)
    )
    poisoned.broker_flow.append(BrokerFlow("PUMP", future, 10_000, 9_000))
    poisoned.reports.append(VictimReport("PUMP", future))
    clean = build_contexts(truncate(DATA, d))["PUMP"]
    dirty = build_contexts(poisoned)["PUMP"]
    for day in DAYS[:61]:
        assert ALL_SIGNALS[name](clean, day, CFG) == ALL_SIGNALS[name](dirty, day, CFG)


def _scores(data):
    return {s.day: (s.score, [h.signal for h in s.hits]) for s in Engine().run(data)["PUMP"].scores}


def test_engine_score_identical_when_all_sources_already_present():
    """Once every data source has appeared by D, truncating after D changes nothing."""

    d = DAYS[80]  # the victim report (last source to appear) is on DAYS[78]
    full, cut = _scores(DATA), _scores(truncate(DATA, d))
    for day in DAYS:
        if day > d:
            break
        assert full[day] == cut[day], day


@pytest.mark.xfail(strict=True, reason="QA-1")
def test_engine_score_identical_whatever_lies_after_scored_day():
    """Generic no-look-ahead rule at engine level, for every day D."""

    full = _scores(DATA)
    for d in DAYS[::5]:
        assert _scores(truncate(DATA, d))[d] == full[d], d


@pytest.mark.xfail(strict=True, reason="QA-1")
def test_engine_score_ignores_future_rows_of_other_tickers():
    """A victim report about another ticker, a year after D, must not change PUMP on D."""

    spike = DAYS[75]
    alone = truncate(DATA, spike)
    with_other = truncate(DATA, spike)
    with_other.reports.append(VictimReport("OTHER", spike + timedelta(days=365)))
    with_other.bars.extend(Bar("OTHER", d, 1, 1, 1, 1, 1) for d in weekdays(D0, 5))
    assert _scores(alone)[spike] == _scores(with_other)[spike]
