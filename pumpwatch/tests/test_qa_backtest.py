"""QA: backtest metric definitions and calibration/holdout integrity."""

from __future__ import annotations

from datetime import date

import pytest

from pumpwatch.backtest import Case, calibrate_and_test, evaluate, load_cases, split_cases
from pumpwatch.engine import Engine, TickerRun
from pumpwatch.models import Alert, DayScore, SignalHit

D = date


def A(t: str, d: date) -> Alert:
    return Alert(t, d, 50.0, ("market", "social"), ())


# -- correct today ----------------------------------------------------------
def test_alert_on_or_after_collapse_is_not_a_catch():
    case = Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 10))
    m = evaluate({"PPP": [A("PPP", D(2024, 3, 10)), A("PPP", D(2024, 3, 20))]}, [case], 40)
    assert (m.caught, m.false_alerts) == (0, 2)


def test_lead_days_measured_to_collapse():
    case = Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 10))
    m = evaluate({"PPP": [A("PPP", D(2024, 3, 4)), A("PPP", D(2024, 3, 7))]}, [case], 40)
    assert (m.caught, m.lead_days, m.false_alerts) == (1, [6], 0)


def test_unlabelled_and_legit_alerts_count_as_false():
    cases = [Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 10)), Case("LLL", "legit", D(2024, 3, 1), D(2024, 3, 10))]
    alerts = {"PPP": [A("PPP", D(2024, 3, 5))], "LLL": [A("LLL", D(2024, 3, 5))], "ZZZ": [A("ZZZ", D(2024, 3, 5))]}
    m = evaluate(alerts, cases, 40)
    assert (m.caught, m.legit_flagged, m.false_alerts) == (1, 1, 2)
    assert evaluate(alerts, cases, 40, universe=set()).false_alerts == 1


def test_split_is_deterministic_stratified_and_disjoint_for_unique_tickers():
    cases = [Case(f"P{i}", "pump", D(2024, 1, 1), D(2024, 2, 1)) for i in range(7)]
    cases += [Case(f"L{i}", "legit", D(2024, 1, 1), D(2024, 2, 1)) for i in range(6)]
    c1, h1 = split_cases(cases)
    c2, h2 = split_cases(list(reversed(cases)))
    assert (c1, h1) == (c2, h2) or ({c.ticker for c in c1}, {c.ticker for c in h1}) == (
        {c.ticker for c in c2},
        {c.ticker for c in h2},
    )
    assert {c.ticker for c in c1}.isdisjoint({c.ticker for c in h1})
    assert sum(c.label == "pump" for c in c1) in (3, 4)
    assert sum(c.label == "legit" for c in c1) == 3


# -- QA-2: same ticker in both halves ---------------------------------------------
TWICE = [
    Case("AAA", "pump", D(2024, 1, 10), D(2024, 2, 1)),
    Case("AAA", "pump", D(2024, 6, 10), D(2024, 7, 1)),
    Case("BBB", "pump", D(2024, 1, 10), D(2024, 2, 1)),
    Case("CCC", "pump", D(2024, 1, 10), D(2024, 2, 1)),
]


@pytest.mark.xfail(strict=True, reason="QA-2")
def test_ticker_never_appears_in_both_halves():
    calib, hold = split_cases(TWICE)
    assert {c.ticker for c in calib}.isdisjoint({c.ticker for c in hold})


@pytest.mark.xfail(strict=True, reason="QA-2")
def test_twice_pumped_ticker_causes_no_phantom_false_alerts():
    runs = {}
    for t, days in {"AAA": [D(2024, 1, 20), D(2024, 6, 20)], "BBB": [D(2024, 1, 20)], "CCC": [D(2024, 1, 20)]}.items():
        hit = SignalHit("S1_abnormal_volume", "market", t, days[0], 1.0, "x")
        hit2 = SignalHit("S4_hype_burst", "social", t, days[0], 1.0, "x")
        runs[t] = TickerRun(t, [DayScore(t, d, 60.0, [hit, hit2]) for d in days])
    rep = calibrate_and_test(Engine(), runs, TWICE, grid=[40.0])
    assert rep.calibration.false_alerts == 0 and rep.holdout.false_alerts == 0


# -- QA-8: alerts long before the promotion ------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-8")
def test_alert_a_month_before_promotion_is_not_credited_as_early_warning():
    case = Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 5))
    m = evaluate({"PPP": [A("PPP", D(2024, 2, 1)), A("PPP", D(2024, 3, 3))]}, [case], 40)
    assert m.lead_days == [2]


# -- QA-9: one alert credited twice ------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-9")
def test_one_alert_cannot_catch_two_pumps():
    cases = [Case("AAA", "pump", D(2024, 1, 10), D(2024, 2, 1)), Case("AAA", "pump", D(2024, 2, 20), D(2024, 3, 1))]
    m = evaluate({"AAA": [A("AAA", D(2024, 1, 25))]}, cases, 40)
    assert m.caught == 1


@pytest.mark.xfail(strict=True, reason="QA-9")
def test_pump_alert_is_not_also_a_legit_flag():
    cases = [Case("BBB", "legit", D(2024, 1, 10), D(2024, 2, 10)), Case("BBB", "pump", D(2024, 3, 1), D(2024, 3, 20))]
    m = evaluate({"BBB": [A("BBB", D(2024, 3, 5))]}, cases, 40)
    assert (m.caught, m.legit_flagged) == (1, 0)


# -- QA-12: zero catches pass the false-alert gate -------------------------------
@pytest.mark.xfail(strict=True, reason="QA-12")
def test_zero_catches_never_pass_false_alert_gate():
    case = Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 10))
    m = evaluate({"ZZZ": [A("ZZZ", D(2024, 3, k)) for k in (1, 12, 23, 30)]}, [case], 40)
    assert m.caught == 0 and not (m.false_per_catch <= 5.0)


# -- QA-13: failed calibration is silent ---------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-13")
def test_report_says_when_no_threshold_met_the_constraint():
    runs = {}
    for t in ("PPP", "QQQ"):  # each pump ticker only has noise alerts, a month before its case window
        hits = [SignalHit("S1_abnormal_volume", "market", t, D(2024, 1, 1), 1.0, "x"),
                SignalHit("S4_hype_burst", "social", t, D(2024, 1, 1), 1.0, "x")]
        runs[t] = TickerRun(t, [DayScore(t, D(2024, 1, 1 + 11 * k), 90.0, hits) for k in range(3)])
    cases = [Case("PPP", "pump", D(2024, 3, 1), D(2024, 3, 10)), Case("QQQ", "pump", D(2024, 3, 1), D(2024, 3, 10))]
    rep = calibrate_and_test(Engine(), runs, cases, max_false_per_catch=0.5, grid=[40.0, 60.0])
    assert getattr(rep, "constraint_met", True) is False


@pytest.mark.xfail(strict=True, reason="QA-13")
def test_empty_grid_raises_clear_error():
    with pytest.raises(ValueError, match="grid"):
        calibrate_and_test(Engine(), {}, [Case("P", "pump", D(2024, 1, 1), D(2024, 1, 2))], grid=[])


# -- QA-19: case file parsing ----------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-19")
@pytest.mark.parametrize(
    "content",
    [
        "﻿ticker,label,start,end\nAAA,pump,2024-01-01,2024-02-01\n",  # Excel UTF-8 BOM
        "Ticker,Label,Start,End\nAAA,pump,2024-01-01,2024-02-01\n",
        "ticker, label, start, end\nAAA,pump,2024-01-01,2024-02-01\n",
    ],
)
def test_load_cases_accepts_common_header_variants(tmp_path, content):
    p = tmp_path / "cases.csv"
    p.write_text(content, encoding="utf-8")
    assert [c.ticker for c in load_cases(p)] == ["AAA"]


@pytest.mark.xfail(strict=True, reason="QA-19")
def test_load_cases_skips_indented_comments_and_strips_dollar(tmp_path):
    p = tmp_path / "cases.csv"
    p.write_text(
        "ticker,label,start,end\n  # TODO,pump,2024-01-01,2024-02-01\n$DDD,pump,2024-01-01,2024-02-01\n",
        encoding="utf-8",
    )
    assert [c.ticker for c in load_cases(p)] == ["DDD"]


# -- QA-25: recall with no pumps ------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-25")
def test_recall_is_undefined_without_pumps():
    m = evaluate({}, [Case("LLL", "legit", D(2024, 1, 1), D(2024, 2, 1))], 40)
    assert m.summary()["recall"] is None
