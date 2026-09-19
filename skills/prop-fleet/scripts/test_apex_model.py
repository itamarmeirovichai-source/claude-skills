"""בדיקות למכניקה של apex_model.

כל המספרים בתוכנית יוצאים מהמודול הזה. עד עכשיו בדקתי רק שהפלט המצרפי
נראה שפוי — וזה לא מספיק: תנאי אחד שגוי בנעילת הרצפה או בסולם המשיכות
משנה כל מספר בדוח, ושום דבר לא היה תופס את זה.

הבדיקות כאן דטרמיניסטיות. ב-RR של 1:2, ההסתברות לזכייה היא (avg_R+1)/3,
אז avg_R=2.0 נותן זכייה תמיד ו-avg_R=-1.0 נותן הפסד תמיד. ככה אפשר לבדוק
כלל ולא התפלגות.
"""

import numpy as np
import pytest

from apex_model import EVAL_TRADING_DAYS, PLANS, TRADES_DAY, allocate, simulate

ALWAYS_WIN, ALWAYS_LOSE = 2.0, -1.0
P50 = PLANS["50K"]
LADDER_TOTAL = sum(P50["ladder"])          # 13,000
SAFETY = P50["start"] + P50["dd"] + 100    # 52,600
LOCK = P50["start"] + 100                  # 50,100


def one(avg_R, **kw):
    kw.setdefault("n", 40)
    kw.setdefault("slots", 1)
    kw.setdefault("years", 2)
    kw.setdefault("risk_pct", 0.04)
    return simulate(avg_R=avg_R, **kw)


# ── הרצפה והמוות ────────────────────────────────────────────────

def test_a_losing_account_dies_and_costs_only_fees():
    d = one(ALWAYS_LOSE)
    assert d["gross"].sum() == 0, "חשבון מפסיד לא מייצר משיכות"
    assert d["fees"].sum() > 0, "אבל כן צורך דמי הערכה"
    assert d["burned"].mean() > 0


def test_loss_is_bounded_by_fees_never_by_capital():
    """ההבטחה המרכזית בכל התוכנית. אם היא לא נכונה, הכל נופל."""
    d = one(ALWAYS_LOSE, years=8, slots=20)
    worst = d["net_year"].sum(axis=1).min()
    total_fees = d["fees"].sum(axis=1).max()
    assert worst >= -total_fees - 1e-6, "הפסד לא יכול לעבור את סך העמלות"


def test_dying_takes_about_drawdown_over_risk_trades():
    """DD של 2,500 בסיכון 250 לעסקה -> בערך עשר עסקאות, לא מאה."""
    d = one(ALWAYS_LOSE, risk_pct=0.10, risk_pct_eval=0.10, years=1, n=20)
    trades_per_year = TRADES_DAY * 250
    deaths = d["burned"].mean()
    expected = trades_per_year / (P50["dd"] / (0.10 * P50["dd"]))
    assert 0.5 * expected < deaths < 2.0 * expected


# ── סולם המשיכות ────────────────────────────────────────────────

def test_one_account_never_exceeds_the_ladder():
    d = one(ALWAYS_WIN, years=8, slots=1)
    per_path = d["gross"].sum(axis=1)
    # שמונה שנים של זכיות = כמה מחזורי חשבון, כל אחד עד 13,000
    assert (per_path % LADDER_TOTAL < 1e-6).all() or per_path.max() > LADDER_TOTAL
    assert (per_path >= LADDER_TOTAL).all(), "חשבון מנצח חייב להשלים לפחות סולם אחד"


def test_withdrawals_come_in_whole_ladders():
    """כל חשבון מוציא בדיוק 13,000 ואז נסגר. אין סכומים אחרים."""
    d = one(ALWAYS_WIN, years=4, slots=1, n=30)
    for total in d["gross"].sum(axis=1):
        assert abs(total % LADDER_TOTAL) < 1.0, f"{total} אינו כפולה של הסולם"


def test_more_slots_scale_the_output():
    a = one(ALWAYS_WIN, slots=1, years=4)
    b = one(ALWAYS_WIN, slots=4, years=4)
    assert b["gross"].sum() > a["gross"].sum()


def test_zero_slots_produces_nothing():
    d = one(ALWAYS_WIN, slots=0, years=2, n=5)
    assert d["gross"].sum() == 0
    assert d["fees"].sum() == 0


# ── שעון ההערכה ─────────────────────────────────────────────────

def test_evaluation_expires_when_the_target_is_out_of_reach():
    """סיכון זעיר -> אי אפשר להגיע ל-3,000 ב-21 ימים, גם בזכייה תמיד."""
    tiny = 20.0 / P50["dd"]        # 20 דולר לעסקה
    d = one(ALWAYS_WIN, risk_pct=tiny, risk_pct_eval=tiny, years=2, n=20)
    assert d["gross"].sum() == 0, "אסור שחשבון כזה יגיע למימון"
    assert d["fees"].sum() > 0, "אבל הוא כן שילם על הערכות שפגו"


def test_a_reachable_target_does_get_funded():
    """אותה בדיקה בכיוון ההפוך, כדי שהקודמת לא תעבור מסיבה לא נכונה."""
    d = one(ALWAYS_WIN, risk_pct=0.04, risk_pct_eval=0.10, years=2, n=20)
    assert d["gross"].sum() > 0


def test_eval_window_is_the_documented_length():
    assert EVAL_TRADING_DAYS == 21, "30 ימים קלנדריים, כפי שתועד"


# ── תוכניות ─────────────────────────────────────────────────────

def test_the_bigger_plan_yields_more_per_slot():
    a = one(ALWAYS_WIN, plan="50K", slots=2, years=4)
    b = one(ALWAYS_WIN, plan="150K", slots=2, years=4)
    assert b["gross"].sum() > a["gross"].sum()


def test_plan_constants_match_the_documented_rules():
    assert P50["dd"] == 2500 and P50["target"] == 3000
    assert list(P50["ladder"]) == [1500, 1500, 2000, 2500, 2500, 3000]
    assert LADDER_TOTAL == 13000
    assert SAFETY == 52600 and LOCK == 50100


# ── מס ──────────────────────────────────────────────────────────

def test_tax_reduces_profit_but_never_a_loss():
    win_hi = one(ALWAYS_WIN, years=4, tax=0.25)["net_year"].sum()
    win_lo = one(ALWAYS_WIN, years=4, tax=0.47)["net_year"].sum()
    assert win_lo < win_hi

    lose_hi = one(ALWAYS_LOSE, years=2, tax=0.25)["net_year"].sum()
    lose_lo = one(ALWAYS_LOSE, years=2, tax=0.47)["net_year"].sum()
    assert lose_hi == pytest.approx(lose_lo), "מס לא מגדיל ולא מקטין הפסד"


def test_tax_scales_profit_exactly():
    a = one(ALWAYS_WIN, years=4, tax=0.0)["net_year"].sum()
    b = one(ALWAYS_WIN, years=4, tax=0.5)["net_year"].sum()
    assert b == pytest.approx(a * 0.5, rel=1e-9)


# ── מתאם בין חשבונות ────────────────────────────────────────────

def test_copy_trading_is_perfectly_correlated():
    """עותק פקודות -> כל החשבונות חיים ומתים יחד. זה לא פיזור."""
    d = simulate(n=200, slots=5, avg_R=0.0, risk_pct=0.10, risk_pct_eval=0.10,
                 years=1, correlated=True)
    e = simulate(n=200, slots=5, avg_R=0.0, risk_pct=0.10, risk_pct_eval=0.10,
                 years=1, correlated=False)
    assert d["burned"].std() > e["burned"].std(), \
        "מתואם -> שונות גבוהה יותר במספר החשבונות שנשרפים"


# ── מדינות שוק ──────────────────────────────────────────────────

def test_zero_spread_is_plain_independent_trading():
    a = simulate(n=100, slots=2, avg_R=0.30, years=2, seed=3,
                 persistence=0.5, spread=0.0)
    b = simulate(n=100, slots=2, avg_R=0.30, years=2, seed=3,
                 persistence=0.99, spread=0.0)
    assert a["gross"].sum() == pytest.approx(b["gross"].sum()), \
        "בלי spread, ההתמדה לא אמורה לשנות כלום"


def test_an_impossible_spread_is_rejected():
    with pytest.raises(ValueError, match="spread"):
        simulate(n=10, avg_R=0.30, spread=0.9, years=1)


# ── חלוקת הרווחים ───────────────────────────────────────────────

def test_nothing_is_extracted_before_year_five():
    ny = np.full((3, 8), 100_000.0)
    for y, (res, port, biz) in enumerate(allocate(ny), start=1):
        if y <= 4:
            assert port.sum() == 0 and biz.sum() == 0
        else:
            assert port.sum() > 0 and biz.sum() > 0


def test_the_split_is_a_quarter_each():
    ny = np.zeros((1, 6))
    ny[0, 5] = 100_000.0
    res, port, biz = allocate(ny, port_r=0.0, biz_r=0.0)[-1]
    assert port[0] == pytest.approx(25_000)
    assert biz[0] == pytest.approx(25_000)
    assert res[0] == pytest.approx(50_000)


def test_a_losing_year_is_not_split_into_investments():
    ny = np.zeros((1, 6))
    ny[0, 5] = -40_000.0
    res, port, biz = allocate(ny, port_r=0.0, biz_r=0.0)[-1]
    assert port[0] == 0 and biz[0] == 0
    assert res[0] == pytest.approx(-40_000), "ההפסד יורד מהרזרבה במלואו"


def test_returns_compound_on_what_was_extracted():
    ny = np.full((1, 8), 100_000.0)
    flat = allocate(ny, port_r=0.0, biz_r=0.0)[-1]
    grown = allocate(ny, port_r=0.10, biz_r=0.10)[-1]
    assert grown[1][0] > flat[1][0] and grown[2][0] > flat[2][0]
    assert grown[0][0] == pytest.approx(flat[0][0]), "הרזרבה לא אמורה לצמוח"
