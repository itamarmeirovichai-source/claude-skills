#!/usr/bin/env python3
"""בדיקות ל-detect.py.

הן קיימות כי המספר הזה נדד פעמיים, ולשני הכיוונים. תחילה נמסר "39
ימי מסחר, כ-1.8 חודשים" ל-+0.250R — הספירה נכונה, ההמרה לחודשים לא.
אחר כך "תוקן" ל-77 על בסיס שגיאת תקן שנרשמה מהזיכרון כ-0.207 במקום
0.145 שנובע מהרווח שהודפס, וזה קלקל גם את מה שהיה נכון. לכן נבדק כאן
גם העוגן עצמו, גם שהוא משחזר את הרווח המקורי, וגם היחידות.
"""
import pytest

import detect as d
from detect import (DAYS_MEASURED, SE_MEASURED, days_to_clear, se_at,
                    smallest_detectable)
from replay import _tcrit


def test_se_shrinks_as_root_of_days_not_of_trades():
    """פי ארבעה ימים הם חצי שגיאת תקן. פי ארבעה עסקאות באותו יום — כלום.

    אם זה היה 1/K במקום 1/sqrt(K), כל לוח הזמנים היה מתקצר פי כמה
    וההמתנה הייתה נראית קצרה בהרבה ממה שהיא.
    """
    assert se_at(DAYS_MEASURED) == pytest.approx(SE_MEASURED)
    assert se_at(4 * DAYS_MEASURED) == pytest.approx(SE_MEASURED / 2)
    assert se_at(9 * DAYS_MEASURED) == pytest.approx(SE_MEASURED / 3)


def test_the_anchor_reproduces_the_printed_interval():
    """שגיאת התקן חייבת להחזיר את הרווח ש-replay.py הדפיס.

    זו הבדיקה שהייתה חסרה. גרסה קודמת קיבעה כאן SE=0.207 מהזיכרון,
    שממנו נובע רווח [-0.324, +0.526] במקום [-0.197, +0.398] שהודפס,
    והיא הכפילה כל שורה בטבלה. עיגון שאינו משחזר את המדידה שממנה
    הוא בא אינו עיגון.
    """
    half = _tcrit(d.DAYS_MEASURED - 1) * d.SE_MEASURED
    lo, hi = d.MEAN_MEASURED - half, d.MEAN_MEASURED + half
    assert lo == pytest.approx(d.CI_MEASURED[0], abs=0.002)
    assert hi == pytest.approx(d.CI_MEASURED[1], abs=0.002)


def test_the_anchor_is_thirty_nine_days():
    """+0.250R דורש כ-39 ימי-עסקה.

    המספר הזה נדד פעמיים. תחילה נמסר 39 ימים "כ-1.8 חודשים" — הספירה
    נכונה וההמרה לחודשים שגויה. אחר כך "תוקן" ל-77 על בסיס שגיאת תקן
    מנופחת, וזה קלקל גם את הספירה. הנכון הוא 39 ימי-עסקה, שהם 2.7
    חודשי לוח, ושניהם נבדקים כאן.
    """
    assert days_to_clear(0.25) == 39
    assert d.months_for(39) == pytest.approx(2.7, abs=0.1)


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
    """+0.101R דורש מעל שנה של ימי-עסקה. זו המסקנה שמכריעה."""
    assert days_to_clear(0.101) > 200
    assert d.months_for(days_to_clear(0.101)) > 12


def test_months_use_active_days_not_elapsed_trading_days():
    """המרה לחודשים חייבת לעבור דרך ימי-עסקה, לא דרך 21.

    `days_to_clear` מחזיר אשכולות — ימים שבהם נסגרה עסקה. בחלון הנקי
    היו 28 כאלה מתוך 41 ימי מסחר שחלפו, ולכן חודש לוח מספק כ-14.3
    ואלה, לא 21. חלוקה ב-21 מקצרת כל שורה בטבלה בשליש, תמיד לכיוון
    שמחמיא לתוכנית.
    """
    assert d.ELAPSED_DAYS_MEASURED > d.DAYS_MEASURED
    assert d.ACTIVE_DAYS_PER_MONTH < d.TRADING_DAYS_PER_MONTH
    assert d.months_for(39) == pytest.approx(2.7, abs=0.1)
    naive = 39 / d.TRADING_DAYS_PER_MONTH
    assert d.months_for(39) > naive * 1.3


def test_the_measured_edge_takes_over_a_year():
    """+0.101R הוא 222 ימי-עסקה, שהם מעל שנה של לוח שנה."""
    k = d.days_to_clear(0.101)
    assert k == 222
    assert d.months_for(k) > 12
