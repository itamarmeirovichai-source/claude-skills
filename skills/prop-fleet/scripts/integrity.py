"""
bot/integrity.py — מקור אמת יחיד למדידת סיכון ותוצאה.

המודול הזה לא נוגע באסטרטגיה. הוא לא מחליט מה לסחור, מתי, או באיזה דירוג.
הוא עונה על שלוש שאלות בלבד לגבי עסקה שכבר נשלחה:

    1. כמה דולרים עמדו בסיכון        -> compute_dollar_risk
    2. האם ה-PnL הרשום עקבי בכלל     -> assert_pnl_sign
    3. מה זה ב-R                     -> calc_pnl_r

כל נוסחה אחרת בקוד לחישוב dollar_risk או pnl_r אמורה להיעלם.
"""

from typing import Optional

__all__ = [
    "IntegrityError",
    "point_value",
    "compute_dollar_risk",
    "assert_pnl_sign",
    "calc_pnl_r",
    "validate_trade_record",
    "VALID_EXIT_REASONS",
]


class IntegrityError(ValueError):
    """רשומת עסקה שסותרת את עצמה. לא נכתבת ל-DB. לעולם."""


# ── ערך נקודה ────────────────────────────────────────────────────
# חוזים בלבד. מניות ו-ETF הם 1.0 (דולר לנקודה למניה).
POINT_VALUES = {
    "ES": 50.0,  "MES": 5.0,
    "NQ": 20.0,  "MNQ": 2.0,
    "YM": 5.0,   "MYM": 0.5,
    "RTY": 50.0, "M2K": 5.0,
    "CL": 1000.0, "MCL": 100.0,
    "GC": 100.0, "MGC": 10.0,
}
DEFAULT_POINT_VALUE = 1.0


def point_value(symbol: str) -> float:
    return POINT_VALUES.get((symbol or "").strip().upper(), DEFAULT_POINT_VALUE)


# ── 1. סיכון בדולרים ─────────────────────────────────────────────

def compute_dollar_risk(symbol: str, entry, stop_loss, quantity) -> float:
    """הדרך היחידה בקוד הזה לחשב סיכון בדולרים.

    נגזר מהגיאומטריה של הפקודה שנשלחה בפועל — לעולם לא מ-
    account_size × risk_pct. אלה שתי שאלות שונות:

        account × risk%  -> כמה לפתוח        (סייזינג, לפני)
        הפונקציה הזאת    -> כמה באמת הסתכן   (מדידה, אחרי)

    ערבוב בין השתיים הוא מה שייצר חמישה ערכי dollar_risk שונים
    לאותה עסקה, ומה שהפך כל ממוצע pnl_r לחסר משמעות.
    """
    if entry is None or stop_loss is None or quantity is None:
        raise IntegrityError(
            f"{symbol}: חסר entry/stop/quantity "
            f"(entry={entry}, stop={stop_loss}, qty={quantity})"
        )
    risk_per_unit = abs(float(entry) - float(stop_loss))
    if risk_per_unit <= 0:
        raise IntegrityError(f"{symbol}: entry == stop_loss ({entry}) — אין סיכון מוגדר")
    qty = abs(float(quantity))
    if qty <= 0:
        raise IntegrityError(f"{symbol}: quantity={quantity}")
    return round(risk_per_unit * qty * point_value(symbol), 2)


# ── 2. שומר הסימן ────────────────────────────────────────────────

def assert_pnl_sign(symbol: str, direction: str, entry, exit_price, pnl,
                    tol: float = 1e-9) -> None:
    """לונג שנסגר גבוה יותר חייב PnL חיובי. שורט — הפוך.

    בארכיון נמצאו שתי עסקאות שסותרות את זה (id 18, id 27).
    מכאן זו חריגה, לא שורה בדאטהבייס.
    """
    d = (direction or "").strip().lower()
    if d not in ("long", "short"):
        raise IntegrityError(f"{symbol}: direction='{direction}' לא חוקי")
    if entry is None or exit_price is None or pnl is None:
        raise IntegrityError(
            f"{symbol}: חסר entry/exit/pnl "
            f"(entry={entry}, exit={exit_price}, pnl={pnl})"
        )
    move = float(exit_price) - float(entry)
    if abs(move) < tol or abs(float(pnl)) < tol:
        return  # שטוח — אין מה לבדוק
    expected = move if d == "long" else -move
    if expected * float(pnl) < 0:
        raise IntegrityError(
            f"{symbol} {d}: entry={entry} exit={exit_price} "
            f"(תנועה {move:+.4f}) אבל pnl={float(pnl):+.2f} — הסימן סותר את הכיוון"
        )


# ── 3. R ─────────────────────────────────────────────────────────

def calc_pnl_r(pnl, dollar_risk) -> Optional[float]:
    """PnL ביחידות R. מחזיר None כשאי אפשר לחשב — אף פעם לא 0.0.

    0.0 הוא ערך אמיתי שמשמעותו breakeven. להשתמש בו בשביל "לא ידוע"
    הכניס breakeven-ים מזויפים לכל ממוצע. עסקה של +$115.20 נרשמה כ-0R
    בגלל זה בדיוק.
    """
    if pnl is None or dollar_risk is None:
        return None
    dr = float(dollar_risk)
    if dr <= 0:
        return None
    return round(float(pnl) / dr, 4)


# ── 4. שער הכתיבה ────────────────────────────────────────────────

VALID_EXIT_REASONS = {
    "tp1", "tp2", "stop", "trail_stop", "eod",
    "manual", "cancelled", "expired", "broker_close",
}


def validate_trade_record(symbol: str, direction: str, analysis_id,
                          entry, stop_loss, quantity,
                          exit_price=None, pnl=None, exit_reason=None,
                          closing: bool = False) -> float:
    """בודק רשומת עסקה לפני כתיבה. מחזיר את dollar_risk.

    closing=False  — פתיחה: חייב analysis_id וגיאומטריה תקינה.
    closing=True   — סגירה: חייב גם exit_price, pnl, exit_reason וסימן עקבי.
    """
    if analysis_id is None or int(analysis_id) <= 0:
        raise IntegrityError(
            f"{symbol}: analysis_id={analysis_id} — עסקה חייבת להיות מקושרת לסיגנל. "
            f"בלי זה אי אפשר למדוד שום דירוג או kill zone."
        )
    dollar_risk = compute_dollar_risk(symbol, entry, stop_loss, quantity)

    if closing:
        if exit_reason not in VALID_EXIT_REASONS:
            raise IntegrityError(
                f"{symbol}: exit_reason='{exit_reason}' — חייב להיות אחד מ-"
                f"{sorted(VALID_EXIT_REASONS)}"
            )
        assert_pnl_sign(symbol, direction, entry, exit_price, pnl)

    return dollar_risk
