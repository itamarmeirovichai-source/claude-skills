#!/usr/bin/env python3
"""בדיקות ל-detect.py.

הן קיימות כי המספר הזה כבר נדד פעם אחת: נמסר 39 ימי מסחר ל-+0.250R
במקום 77. מספר שנאמר מהזיכרון ולא מחושב הוא מספר שיטעה שוב, ולכן
העוגן עצמו נבדק כאן ולא רק המנגנון סביבו.
"""
import pytest

from detect import (DAYS_MEASURED, SE_MEASURED, days_to_clear, se_at,
                    smallest_detectable)


def test_se_shrinks_as_root_of_days_not_of_trades():
    """פי ארבעה ימים הם חצי שגיאת תקן. פי ארבעה עסקאות באותו יום — כלום.

    אם זה היה 1/K במקום 1/sqrt(K), כל לוח הזמנים היה מתקצר פי כמה
    וההמתנה הייתה נראית קצרה בהרבה ממה שהיא.
    """
    assert se_at(DAYS_MEASURED) == pytest.approx(SE_MEASURED)
    assert se_at(4 * DAYS_MEASURED) == pytest.approx(SE_MEASURED / 2)
    assert se_at(9 * DAYS_MEASURED) == pytest.approx(SE_MEASURED / 3)


def test_the_anchor_is_seventy_seven_not_thirty_nine():
    """+0.250R דורש כ-77 ימי מסחר, לא 39. זה הערך שנמסר שגוי."""
    assert days_to_clear(0.25) == 77


def test_bigger_edges_resolve_sooner():
    seq = [days_to_clear(m) for m in (0.15, 0.20, 0.25, 0.30, 0.40)]
    assert all(a > b for a, b in zip(seq, seq[1:])), seq


def test_the_conservative_case_is_always_slower():
    """הנצפה שגיאת תקן מתחת לאמת — תמיד לוקח יותר, לכל גודל יתרון."""
    for m in (0.15, 0.25, 0.40):
        assert days_to_clear(m, margin_se=1.0) > days_to_clear(m, margin_se=0.0)


def test_the_two_directions_agree():
    """round-trip: היתרון הקטן ביותר אחרי k ימים הוא בדיוק זה שדורש k.

    זו הבדיקה החזקה כאן — היא מפילה כל אי-התאמה בין שתי הנוסחאות,
    כולל קוונטיל שונה או כיווץ שונה באחת מהן.
    """
    for k in (40, 77, 120, 200):
        m = smallest_detectable(k)
        assert days_to_clear(m + 1e-9) <= k
        assert days_to_clear(m - 1e-3) > k


def test_a_non_positive_edge_never_resolves():
    assert days_to_clear(0.0) is None
    assert days_to_clear(-0.1) is None


def test_the_measured_edge_is_out_of_reach():
    """+0.101R דורש יותר משנה של ימי מסחר. זו המסקנה שמכריעה."""
    assert days_to_clear(0.101) > 250
