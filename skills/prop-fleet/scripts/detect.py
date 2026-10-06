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

# נקודות העיגון, נגזרות ממה ש-replay.py מדפיס: +0.101R עם רווח
# [-0.197, +0.398] על 28 ימי-עסקה. מחצית-הרווח חלקי t(27) היא
# שגיאת התקן, 0.145R.
#
# חשוב לדעת למה זה כתוב ככה. diagnose_edge.py ו-dashboard.py מדפיסים
# 0.207R על אותן 111 עסקאות, כי הם מחשבים פיזור של ממוצעי-ימים חלקי
# שורש מספרם במקום שגיאה עמידת-אשכולות סביב ממוצע העסקאות. גרסה
# קודמת כאן עיגנה על 0.207 והכפילה כל שורה בטבלה. סימולציה מול
# שגיאת תקן ידועה נותנת 0.99 לעמידת-האשכולות ו-1.07 לממוצעי-הימים,
# ומה שכל המספרים במורד הזרם משתמשים בו הוא הממוצע לעסקה — ולכן זו
# העמידה. שלושה סקריפטים, שני אומדנים, ואי-התאמה של 1.43 בנתונים
# האמיתיים: זה פתוח ורשום כ-task, לא סגור.
#
# מי שמעדכן מדידה מעדכן את שתי השורות למטה מתוך פלט הריצה.
MEAN_MEASURED = 0.101
CI_MEASURED = (-0.197, 0.398)
DAYS_MEASURED = 28
HALF_WIDTH_MEASURED = (CI_MEASURED[1] - CI_MEASURED[0]) / 2
TRADES_PER_DAY = 4.0
GRID = (0.101, 0.15, 0.20, 0.25, 0.30, 0.40)
MAX_DAYS = 2000
SE_MEASURED = HALF_WIDTH_MEASURED / _tcrit(DAYS_MEASURED - 1)

# שני מוני-ימים חיים כאן ואסור לבלבל ביניהם. 28 הוא מספר הימים שבהם
# נסגרה עסקה — האשכולות, ובהם מתכווצת שגיאת התקן. 41 הוא מספר ימי
# המסחר שחלפו בחלון הנקי. היומן מתקדם ב-41, המידע נצבר ב-28, ולכן
# המרה של "ימים" לחודשים חייבת לעבור דרך היחס ביניהם. בדיקה: 111
# מילויים חלקי 41 הם 2.71 ליום שחלף, וחלקי 28 הם 3.96 ליום-עסקה —
# שני המספרים מופיעים בנפרד ב-numbers.md ומאשרים את ההפרדה.
ELAPSED_DAYS_MEASURED = 41
ACTIVE_FRACTION = DAYS_MEASURED / ELAPSED_DAYS_MEASURED
TRADING_DAYS_PER_MONTH = 21.0
ACTIVE_DAYS_PER_MONTH = TRADING_DAYS_PER_MONTH * ACTIVE_FRACTION


def months_for(active_days: int) -> float:
    """כמה חודשי לוח לוקח לצבור `active_days` ימים עם עסקה."""
    return active_days / ACTIVE_DAYS_PER_MONTH


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
    print(f"  עוגן: שגיאת תקן מקובצת {se0:.3f}R על {k0} ימי-עסקה, "
          f"{TRADES_PER_DAY:.1f} עסקאות ליום כזה.")
    print("  שגיאת התקן מתכווצת בימים, לא בעסקאות. יום עמוס אינו יום נוסף.")
    print(f"  'ימים' כאן = ימים שבהם נסגרה עסקה. בחלון הנקי היו {DAYS_MEASURED}")
    print(f"  כאלה מתוך {ELAPSED_DAYS_MEASURED} ימי מסחר שחלפו, כלומר "
          f"{ACTIVE_DAYS_PER_MONTH:.1f} בחודש —")
    print("  וזה מה שממיר ימים לחודשים, לא 21.")

    print(f"\n{'יתרון אמיתי':>12} {'ימים (50%)':>12} {'חודשים':>8} "
          f"{'ימים (84%)':>12} {'חודשים':>8}")
    for m in GRID:
        a = days_to_clear(m, 0.0, se0, k0)
        b = days_to_clear(m, 1.0, se0, k0)
        fa = f"{a:>12}" if a else f"{'לעולם':>12}"
        fb = f"{b:>12}" if b else f"{'לעולם':>12}"
        ma = f"{months_for(a):>8.1f}" if a else f"{'—':>8}"
        mb = f"{months_for(b):>8.1f}" if b else f"{'—':>8}"
        print(f"{m:>+12.3f} {fa} {ma} {fb} {mb}")

    print(f"\n  ומהכיוון השני — מה בכלל ניתן להכרעה אחרי X ימים:")
    print(f"{'ימים':>8} {'חודשים':>8} {'היתרון הקטן ביותר':>20}")
    for d in (25, 50, 77, 100, 150, 250):
        print(f"{d:>8} {months_for(d):>8.1f} "
              f"{smallest_detectable(d, 0.0, se0, k0):>+19.3f}R")

    print("\n  שתי מסקנות שלא תלויות בשום בחירה בטבלה:")
    k101 = days_to_clear(0.101, 0.0, se0, k0)
    print(f"  1. יתרון בגודל המדוד (+0.101R) דורש {k101} ימי-עסקה, שהם")
    print(f"     כ-{months_for(k101):.0f} חודשי לוח במקרה החציוני ופי שניים כדי")
    print("     להיות בטוחים. אם זה הגודל האמיתי, התוכנית לא תיענה בזמן.")
    print("  2. לכן ההמתנה אינה 'עד שנדע כמה היתרון', אלא 'עד שנדע אם")
    k25 = days_to_clear(0.25, 0.0, se0, k0)
    print(f"     הוא גדול מספיק'. יתרון שלא נראה תוך כ-{months_for(k25):.0f} חודשים הוא")
    print("     ממילא קטן מכדי להצדיק את הצי.")


if __name__ == "__main__":
    main()
