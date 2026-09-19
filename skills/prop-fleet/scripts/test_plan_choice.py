#!/usr/bin/env python3
"""בדיקות לבחירת התוכנית.

הבדיקה המרכזית כאן היא על המסקנה ולא על החשבון: שהתשובה נשארת
מותנית. "הקטן עדיף" בלי תנאי הוא בדיוק מה שהדוח הזה אמר עד
שהוספתי בקרה של מספר חשבונות זהה, והבקרה הפילה את זה.
"""

import numpy as np
import pytest

from apex_model import MES_PT, PLANS, STOP_PTS, allocate, simulate
from plan_choice import compare, effective_risk, ladder_value


def test_the_small_plan_underrisks_and_the_large_one_overrisks():
    """עיגול לחוזה שלם מזיז את שתי התוכניות לכיוונים הפוכים.

    זה לא פרט חשבונאי. 4% הוא מה שנכתב בכלל, ושתי התוכניות
    לוקחות בפועל משהו אחר — אחת פחות ואחת יותר.
    """
    small = effective_risk("50K", 0.04)
    big = effective_risk("150K", 0.04)
    assert small["err_pct"] < 0, small
    assert big["err_pct"] > 0, big
    assert small["k"] == 2 and big["k"] == 5


def test_effective_risk_never_rounds_to_zero_contracts():
    """חשבון עם סיכון קטן מחוזה אחד עדיין סוחר חוזה אחד."""
    e = effective_risk("50K", 0.001)
    assert e["k"] == 1
    assert e["got"] == pytest.approx(STOP_PTS * MES_PT)


def test_the_small_ladder_is_richer_per_dollar_of_drawdown():
    assert ladder_value("50K")["per_dd"] > ladder_value("150K")["per_dd"]


def test_the_large_ladder_is_still_bigger_in_absolute_terms():
    """היחס והסכום מצביעים לכיוונים הפוכים, וזה כל העניין."""
    assert ladder_value("150K")["ladder"] > ladder_value("50K")["ladder"]


def test_the_evaluation_target_is_out_of_reach_at_funded_sizing():
    """למה ההערכה נמדדת ב-10% ולא ב-4%.

    63 עסקאות בהערכה. יעד של 35R או 42R מהן הוא לא יעד קשה,
    הוא יעד שלא קורה. ההשוואה שלי רצה קודם ב-4% בשתי התוכניות,
    וזה חנק דווקא את הגדול — כלומר מדד את הטעות שלי.
    """
    for plan, floor in (("50K", 30.0), ("150K", 35.0)):
        e = effective_risk(plan, 0.04)
        assert PLANS[plan]["target"] / e["got"] > floor
    for plan in ("50K", "150K"):
        e = effective_risk(plan, 0.10)
        assert PLANS[plan]["target"] / e["got"] < 20.0


def test_compare_sizes_the_evaluation_separately():
    """רגרסיה על הבאג שלי: ההערכה חייבת לקבל מידה משלה."""
    rows = compare(a=("50K", 2), b=("150K", 2), n=60, years=2)
    assert len(rows) == 2 * 5
    # אותה הרצה עם מידה אחידה חייבת לתת תוצאה אחרת, אחרת
    # הפרמטר לא באמת עובר הלאה.
    same = compare(a=("50K", 2), b=("150K", 2), risk_pct_eval=0.04,
                   n=60, years=2)
    assert [r["median"] for r in rows] != [r["median"] for r in same]


@pytest.mark.parametrize("avg_R,expect", [(0.00, "50K"), (0.30, "150K")])
def test_the_answer_flips_with_expectancy_at_equal_slot_count(avg_R, expect):
    """הבדיקה ששומרת על המסקנה מלהפוך לסיסמה.

    במספר חשבונות זהה אין תשובה אחת. בלי קצה הקטן מפסיד פחות;
    עם קצה מבוסס הגדול מרוויח יותר. מי שיפשט את זה ל"הקטן
    תמיד" יפיל את הבדיקה הזאת.
    """
    out = {}
    for plan in ("50K", "150K"):
        s = simulate(plan=plan, slots=10, avg_R=avg_R, risk_pct_eval=0.10,
                     n=400, seed=11)
        res, port, biz = allocate(s["net_year"])[-1]
        out[plan] = float(np.median(res + port + biz))
    win = "50K" if out["50K"] > out["150K"] else "150K"
    assert win == expect, (avg_R, out)


def test_twenty_small_beats_ten_large_as_the_question_was_asked():
    """השאלה כפי שנשאלה, בשתי תוחלות מנוגדות."""
    for avg_R in (0.00, 0.30):
        res = {}
        for plan, slots in (("50K", 20), ("150K", 10)):
            s = simulate(plan=plan, slots=slots, avg_R=avg_R,
                         risk_pct_eval=0.10, n=400, seed=11)
            r, p, b = allocate(s["net_year"])[-1]
            res[plan] = float(np.median(r + p + b))
        assert res["50K"] > res["150K"], (avg_R, res)
