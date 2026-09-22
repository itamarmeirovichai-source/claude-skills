#!/usr/bin/env python3
"""כמה זמן עד שנדע — והתשובה ארוכה ממה שאמרתי.

השאלה שקובעת אם התוכנית הזאת שווה את ההמתנה איננה "כמה היתרון",
אלא "מתי אפשר יהיה להכריע". עד היום המספר הזה נאמר בשיחה ולא חושב
בשום מקום, ולכן הוא נדד: נמסר 39 ימי מסחר ל-+0.250R, והחישוב הנכון
נותן 77. פי שניים, וההפרש הוא בין חודשיים לארבעה.

המנגנון: שגיאת התקן מקובצת לפי יום מסחר, כי עסקאות באותו יום חולקות
את אותו משטר ואינן עצמאיות. היא מתכווצת כשורש מספר הימים, לא מספר
העסקאות, ולכן הוספת עסקאות ביום קיים כמעט לא עוזרת. עם מעט אשכולות
הקוונטיל הוא t ולא נורמלי.

מה זה לא: זה אינו חישוב עוצמה פורמלי. "ימים עד שהגבול התחתון חוצה
אפס" מניח שהממוצע הנצפה יֵצא בדיוק על היתרון האמיתי — כלומר הסתברות
50%. לכן מודפס גם המקרה הזהיר, שבו הנצפה יוצא שגיאת תקן אחת מתחת
לאמת, וזה כ-84%.
"""
import sys

import numpy as np

from replay import _tcrit

# מה שנמדד בפועל על 111 מילויים ב-28 ימי מסחר. אלה נקודות העיגון,
# והן מוצהרות כאן כדי שיהיה ברור מה משתנה אם המדידה תתעדכן.
SE_MEASURED = 0.207
DAYS_MEASURED = 28
TRADES_PER_DAY = 4.0
GRID = (0.101, 0.15, 0.20, 0.25, 0.30, 0.40)
TRADING_DAYS_PER_MONTH = 21.0
MAX_DAYS = 2000


def se_at(days: int, se0: float = SE_MEASURED, k0: int = DAYS_MEASURED) -> float:
    """שגיאת התקן המקובצת אחרי `days` ימי מסחר.

    מתכווצת כשורש מספר האשכולות. פיזור-היום נשאר כפי שנמדד — זו
    ההנחה היחידה כאן, והיא נשברת אם המשטר משתנה.
    """
    return se0 * (k0 / days) ** 0.5


def days_to_clear(true_edge: float, margin_se: float = 0.0,
                  se0: float = SE_MEASURED, k0: int = DAYS_MEASURED) -> int | None:
    """ימי מסחר עד שהגבול התחתון חוצה אפס.

    margin_se=0 הוא המקרה החציוני. margin_se=1 מוריד את הנצפה שגיאת
    תקן אחת מתחת לאמת — הרבה יותר קרוב למה שצריך כדי להסתמך על זה.
    """
    if true_edge <= 0:
        return None
    for k in range(5, MAX_DAYS):
        se = se_at(k, se0, k0)
        observed = true_edge - margin_se * se
        if observed - _tcrit(k - 1) * se > 0:
            return k
    return None


def smallest_detectable(days: int, margin_se: float = 0.0,
                        se0: float = SE_MEASURED, k0: int = DAYS_MEASURED) -> float:
    """היתרון הקטן ביותר שאפשר להכריע אחריו `days` ימים."""
    se = se_at(days, se0, k0)
    return (_tcrit(days - 1) + margin_se) * se


def main() -> None:
    se0 = float(sys.argv[1]) if len(sys.argv) > 1 else SE_MEASURED
    k0 = int(sys.argv[2]) if len(sys.argv) > 2 else DAYS_MEASURED
    print(f"\n{'=' * 62}\n  מתי אפשר יהיה להכריע\n{'=' * 62}")
    print(f"  עוגן: שגיאת תקן מקובצת {se0:.3f}R על {k0} ימי מסחר, "
          f"{TRADES_PER_DAY:.1f} עסקאות ליום.")
    print("  שגיאת התקן מתכווצת בימים, לא בעסקאות. יום עמוס אינו יום נוסף.")

    print(f"\n{'יתרון אמיתי':>12} {'ימים (50%)':>12} {'חודשים':>8} "
          f"{'ימים (84%)':>12} {'חודשים':>8}")
    for m in GRID:
        a = days_to_clear(m, 0.0, se0, k0)
        b = days_to_clear(m, 1.0, se0, k0)
        fa = f"{a:>12}" if a else f"{'לעולם':>12}"
        fb = f"{b:>12}" if b else f"{'לעולם':>12}"
        ma = f"{a / TRADING_DAYS_PER_MONTH:>8.1f}" if a else f"{'—':>8}"
        mb = f"{b / TRADING_DAYS_PER_MONTH:>8.1f}" if b else f"{'—':>8}"
        print(f"{m:>+12.3f} {fa} {ma} {fb} {mb}")

    print(f"\n  ומהכיוון השני — מה בכלל ניתן להכרעה אחרי X ימים:")
    print(f"{'ימים':>8} {'חודשים':>8} {'היתרון הקטן ביותר':>20}")
    for d in (25, 50, 77, 100, 150, 250):
        print(f"{d:>8} {d / TRADING_DAYS_PER_MONTH:>8.1f} "
              f"{smallest_detectable(d, 0.0, se0, k0):>+19.3f}R")

    print("\n  שתי מסקנות שלא תלויות בשום בחירה בטבלה:")
    print("  1. יתרון בגודל המדוד (+0.101R) אינו ניתן להכרעה בטווח")
    print("     שמעניין מישהו. אם זה הגודל האמיתי, התוכנית לא תיענה.")
    print("  2. לכן ההמתנה אינה 'עד שנדע כמה היתרון', אלא 'עד שנדע אם")
    print("     הוא גדול מספיק'. יתרון שלא נראה תוך כארבעה חודשים הוא")
    print("     ממילא קטן מכדי להצדיק את הצי.")


if __name__ == "__main__":
    main()
