#!/usr/bin/env python3
"""בדיקות לחוג הסיכון.

הבדיקות כאן שומרות על שלוש טענות שקל מאוד לאבד: שהאחוז לא תלוי
במספר החשבונות, שגודל הסיכון מכפיל את הסימן ולא יוצר אותו, ושמה
שהוא קונה הוא רף נמוך יותר לאסטרטגיה ולא תשואה.
"""

import numpy as np
import pytest

from apex_model import allocate, simulate
from sizing_grid import R_GRID, RISKS, needed_R


def steady_pct(plan="50K", slots=20, nominal=None, **kw) -> float:
    s = simulate(plan=plan, slots=slots, risk_pct_eval=0.10, n=250,
                 seed=11, **kw)
    nominal = nominal or slots * (50_000 if plan == "50K" else 150_000)
    return 100 * float(s["net_year"][:, 4:].mean()) / nominal


def test_the_percentage_does_not_depend_on_the_number_of_accounts():
    """עשרה ועשרים נותנים אותו אחוז. תוספת חשבונות מכפילה דולרים.

    זו הטענה שמפילה את הרעיון ש'עוד חשבונות' הם דרך להעלות
    תשואה. הם לא. בתוחלת שלילית הם מכפילים גם את ההפסד.
    """
    ten = steady_pct(slots=10, avg_R=0.30, risk_pct=0.04)
    twenty = steady_pct(slots=20, avg_R=0.30, risk_pct=0.04)
    assert ten == pytest.approx(twenty, rel=0.06), (ten, twenty)


def test_raising_risk_cannot_turn_a_negative_edge_positive():
    """המכפיל פועל על הסימן. אין גודל סיכון שממציא קצה."""
    for p in (0.02, 0.04, 0.08, 0.12):
        pct = steady_pct(avg_R=-0.10, risk_pct=p)
        assert pct < 0, (p, pct)


def test_raising_risk_raises_both_the_return_and_the_death_rate():
    """שני הצדדים של החוג, על אותה הרצה."""
    lo = simulate(plan="50K", slots=20, avg_R=0.30, risk_pct=0.04,
                  risk_pct_eval=0.10, n=250, seed=11)
    hi = simulate(plan="50K", slots=20, avg_R=0.30, risk_pct=0.08,
                  risk_pct_eval=0.10, n=250, seed=11)
    assert hi["net_year"][:, 4:].mean() > lo["net_year"][:, 4:].mean()
    assert np.median(hi["burned"]) > np.median(lo["burned"])


def test_more_risk_lowers_the_expectancy_the_target_demands():
    """הניסוח הנכון: הסיכון קונה מרווח, לא תשואה."""
    g = {}
    for r in R_GRID:
        for p in RISKS:
            s = simulate(plan="50K", slots=20, avg_R=r, risk_pct=p,
                         risk_pct_eval=0.10, n=250, seed=11)
            g[(r, p)] = (float(s["net_year"][:, 4:].mean()), 0.0)
    needs = [needed_R(g, p, 20.0) for p in (0.04, 0.06, 0.08, 0.12)]
    assert all(x is not None for x in needs), needs
    assert needs == sorted(needs, reverse=True), needs


def test_needed_R_reports_unreachable_rather_than_extrapolating():
    """יעד שלא מושג בטווח שנבדק מוחזר כלא-מושג, לא כמספר מומצא.

    אקסטרפולציה כאן הייתה מייצרת תוחלת שנראית מוכרעת ולא נבדקה
    מעולם — בדיוק סוג המספר שמצדיק חשיפה בטעות.
    """
    g = {(r, 0.02): (-1000.0, 0.0) for r in R_GRID}
    assert needed_R(g, 0.02, 20.0) is None
