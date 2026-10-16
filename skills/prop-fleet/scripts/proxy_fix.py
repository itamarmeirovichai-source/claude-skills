"""
broker/proxy.py — המרת רמות מחיר מחוזה ל-ETF, מתוקנת.

הבאג המקורי
-----------
    ratio       = entry / etf_price
    proxy_entry = round(entry / ratio, 4)

    ->  entry / (entry / etf_price)  ==  etf_price

מחיר הכניסה שהאסטרטגיה חישבה מתבטל אלגברית. מה שנשלח לברוקר הוא תמיד
ובדיוק מחיר השוק הנוכחי. הסטופ וה-TP דווקא הומרו נכון, ולכן המרחקים
נראו סבירים ואף אחד לא שם לב שהכניסה לא מחכה לכלום.

התיקון
------
היחס חייב להיגזר מ**זוג ייחוס חי** — הציטוט הנוכחי של החוזה מול הציטוט
הנוכחי של ה-ETF — ולא מתוך entry. כשהאסטרטגיה נכנסה בשוק שני אלה זהים,
ולכן הבאג היה בלתי נראה בדיוק בתרחיש שבו הוא לא הזיק.

    ratio = futures_price / etf_price        (למשל 7500 / 700 = 10.714)

האינווריאנטה
------------
המרת רמות נכונה שומרת על המיקום היחסי של כל רמה מול מחיר השוק שלה:

    proxy_entry / etf_price  ==  entry / futures_price

הבאג מכריח את האגף השמאלי להיות 1.0 תמיד. הבדיקה הזאת הייתה תופסת אותו
ביום הראשון. היא רצה על כל המרה, לא רק בבדיקות.
"""

from typing import Optional

__all__ = [
    "ProxyConversionError",
    "convert_levels",
    "assert_levels_preserved",
    "MIN_SANE_ETF_PRICE",
    "MAX_SANE_ETF_PRICE",
]

MIN_SANE_ETF_PRICE = 1.0
MAX_SANE_ETF_PRICE = 10_000.0

# סטייה יחסית מותרת בין שני האגפים של האינווריאנטה.
# חמש ספרות משמעותיות — מה שנשאר אחרי round(..., 4).
_REL_TOL = 1e-5


class ProxyConversionError(ValueError):
    """המרה שלא שומרת על הגיאומטריה. הפקודה לא נשלחת."""


def convert_levels(
    entry: float,
    stop_loss: float,
    take_profit: Optional[float],
    futures_price: float,
    etf_price: float,
):
    """ממיר רמות מחיר של חוזה לרמות מחיר של ה-ETF המקביל.

    futures_price ו-etf_price הם הציטוטים החיים של שני המכשירים באותו
    רגע. הם מגדירים את היחס. entry/stop_loss/take_profit הם הרמות
    שהאסטרטגיה ביקשה — הן מומרות, לא נמחקות.

    מחזיר (proxy_entry, proxy_sl, proxy_tp).
    """
    for name, v in (("futures_price", futures_price), ("etf_price", etf_price)):
        if v is None or v <= 0:
            raise ProxyConversionError(f"{name} חייב להיות חיובי, התקבל {v!r}")
    if entry is None or entry <= 0:
        raise ProxyConversionError(f"entry חייב להיות חיובי, התקבל {entry!r}")
    if stop_loss is None or stop_loss <= 0:
        raise ProxyConversionError(f"stop_loss חייב להיות חיובי, התקבל {stop_loss!r}")

    ratio = futures_price / etf_price

    proxy_entry = round(entry / ratio, 4)
    proxy_sl = round(stop_loss / ratio, 4)
    proxy_tp = round(take_profit / ratio, 4) if take_profit is not None else None

    if not (MIN_SANE_ETF_PRICE <= proxy_entry <= MAX_SANE_ETF_PRICE):
        raise ProxyConversionError(
            f"proxy_entry={proxy_entry} מחוץ לטווח השפוי "
            f"[{MIN_SANE_ETF_PRICE}, {MAX_SANE_ETF_PRICE}]"
        )

    assert_levels_preserved(
        entry, stop_loss, take_profit,
        proxy_entry, proxy_sl, proxy_tp,
        futures_price, etf_price,
    )
    return proxy_entry, proxy_sl, proxy_tp


def assert_levels_preserved(
    entry, stop_loss, take_profit,
    proxy_entry, proxy_sl, proxy_tp,
    futures_price, etf_price,
) -> None:
    """כל רמה שומרת על מיקומה היחסי מול מחיר השוק שלה.

    proxy_level / etf_price  ==  level / futures_price

    זו הבדיקה שהבאג המקורי נכשל בה: הוא מכריח
    proxy_entry / etf_price == 1.0 בכל מקרה.
    """
    pairs = [("entry", entry, proxy_entry), ("stop_loss", stop_loss, proxy_sl)]
    if take_profit is not None and proxy_tp is not None:
        pairs.append(("take_profit", take_profit, proxy_tp))

    for name, level, proxy in pairs:
        want = level / futures_price
        got = proxy / etf_price
        if abs(got - want) > _REL_TOL * max(abs(want), 1.0):
            raise ProxyConversionError(
                f"ההמרה של {name} לא שמרה על המיקום היחסי: "
                f"{name}/futures={want:.8f} אבל proxy/etf={got:.8f}. "
                f"({name}={level}, proxy={proxy}, "
                f"futures_price={futures_price}, etf_price={etf_price})"
            )

    # אין כאן בדיקת כיוון נפרדת: היחס חיובי, ולכן שמירה על המיקום היחסי
    # של entry ושל stop_loss כבר מחייבת שהכיוון ישרוד. בדיקה נוספת הייתה
    # קוד שלא יכול לרוץ.


if __name__ == "__main__":
    # הדגמה מספרית של הבאג מול התיקון, על מספרים אמיתיים.
    entry, stop, tp = 7492.50, 7484.00, 7509.50
    futures_price, etf_price = 7500.00, 700.00

    buggy_ratio = entry / etf_price
    buggy_entry = round(entry / buggy_ratio, 4)

    fixed = convert_levels(entry, stop, tp, futures_price, etf_price)

    print(f"מחיר שוק: חוזה {futures_price}, ETF {etf_price}")
    print(f"האסטרטגיה ביקשה כניסה ב-{entry} — {futures_price - entry:.2f} נק' מתחת לשוק\n")
    print(f"הבאג   -> proxy_entry = {buggy_entry}  (בדיוק מחיר השוק. אין המתנה.)")
    print(f"התיקון -> proxy_entry = {fixed[0]}  "
          f"({etf_price - fixed[0]:.4f} דולר מתחת לשוק, כמו שהתבקש)")
    print(f"          proxy_sl    = {fixed[1]}")
    print(f"          proxy_tp    = {fixed[2]}")
