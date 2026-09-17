"""בדיקות להכרעה של אבחון הסטייה.

הכלי הזה עונה על השאלה הפתוחה האחרונה, והוא כבר טעה פעם: הפרדתי בין
מטמון לעוגן קפוא לפי מתאם, בהנחה שמטמון נותן פיגור שגדל. הוא לא —
מטמון עם TTL קבוע מחזיר אותה יישנות כל פעם, והעוגן הוא זה שנופל
מאחור. הבדיקות כאן נועלות את ההבחנה הנכונה כדי שאפשר יהיה לכוונן
ספים בלי לשבור אותה בשקט.

הארגומנטים: (שגיאת התאמה %, טווח הרגעים בימים, מתאם, פיגור חציוני,
פיזור בין-רבעוני של הפיגור).
"""

import pytest

from drift_diagnostic import (
    CACHE,
    COMPUTED,
    FROZEN,
    REAL_PRICE_TOL,
    WRONG_BAR,
    classify,
    explain,
)


# ── ארבעת המקרים, במספרים שנמדדו בפועל על נתונים מושתלים ──────────

def test_frozen_anchor_as_measured():
    """עוגן שהושתל ב-27/02: פיגור גדל, רגעים מתכנסים לשבוע אחד."""
    assert classify(0.003, 7.0, 0.992, 34.34, 42.09) == FROZEN


def test_cache_as_measured():
    """מטמון עם TTL של חמישה ימים: פיגור קבוע, טווח רחב."""
    assert classify(0.003, 81.0, -0.044, 5.00, 1.79) == CACHE


def test_computed_as_measured():
    """מחירים מפוברקים: שגיאת ההתאמה גבוהה, כי הם לא היו בשוק."""
    assert classify(1.181, 81.0, -0.053, 0.88, 6.83) == COMPUTED


# ── ההבחנה שכבר נשברה פעם ────────────────────────────────────────

def test_a_constant_lag_is_a_cache_not_an_anchor():
    """הבאג המקורי: פיגור קבוע נפל לתשובה הכללית."""
    assert classify(0.01, 90.0, 0.0, 5.0, 0.5) == CACHE


def test_a_growing_lag_is_an_anchor_not_a_cache():
    assert classify(0.01, 3.0, 0.95, 30.0, 40.0) == FROZEN


def test_a_wide_spread_is_never_a_cache():
    """מטמון מחזיר אותה יישנות. פיזור רחב שולל אותו."""
    assert classify(0.01, 90.0, 0.0, 5.0, 4.0) != CACHE


def test_a_near_zero_lag_is_not_a_cache():
    """פיגור אפסי אינו מטמון, גם אם הוא יציב מאוד."""
    assert classify(0.01, 90.0, 0.0, 0.1, 0.01) == WRONG_BAR


# ── עדיפות: מחיר שלא התקיים גובר על כל תבנית ─────────────────────

@pytest.mark.parametrize("span,corr,lag,iqr", [
    (7.0, 0.99, 34.0, 42.0),     # נראה כמו עוגן
    (81.0, 0.0, 5.0, 0.5),       # נראה כמו מטמון
    (90.0, 0.0, 0.1, 0.01),      # נראה כמו נר שגוי
])
def test_high_match_error_always_wins(span, corr, lag, iqr):
    """אם המחיר לא התקיים בשוק, אין טעם לדבר על פיגור."""
    assert classify(5.0, span, corr, lag, iqr) == COMPUTED


def test_the_real_price_threshold_is_where_it_is_documented():
    assert REAL_PRICE_TOL == 0.10
    assert classify(REAL_PRICE_TOL - 1e-9, 90.0, 0.0, 0.1, 0.01) != COMPUTED
    assert classify(REAL_PRICE_TOL, 90.0, 0.0, 0.1, 0.01) == COMPUTED


# ── כל פסק דין מקבל הסבר משלו ────────────────────────────────────

@pytest.mark.parametrize("cause", [FROZEN, CACHE, WRONG_BAR, COMPUTED])
def test_every_cause_explains_itself(cause):
    import datetime as dt
    lines = explain(cause, 5.0, dt.datetime(2026, 2, 27))
    assert lines and all(isinstance(x, str) for x in lines)
    assert any(x.strip() for x in lines)


def test_the_cache_explanation_names_the_lag():
    lines = explain(CACHE, 5.0, None)
    assert "5.0" in " ".join(lines), "המשתמש צריך את המספר, לא רק את הסיווג"


def test_the_anchor_explanation_names_the_date():
    import datetime as dt
    lines = explain(FROZEN, 30.0, dt.datetime(2026, 2, 27))
    assert "2026-02-27" in " ".join(lines)


def test_the_four_causes_are_distinct():
    assert len({FROZEN, CACHE, WRONG_BAR, COMPUTED}) == 4
