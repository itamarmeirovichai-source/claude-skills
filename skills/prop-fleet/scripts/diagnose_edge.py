#!/usr/bin/env python3
"""
diagnose_edge.py — לאן הכסף הולך, ומה מזה אפשר לשנות.

הכלל שקודם לכל מה שכאן
-----------------------
131 סטאפים הם מדגם אחד. כל כלל שיימצא על ידי חיפוש מה משפר אותו
ישפר אותו — זו תכונה של החיפוש, לא של הכלל. רשת ה-RR כבר הדגימה
את זה: הטוב ביותר בדיעבד נתן 0.106R+ מול 0.101R+ של הרישום
המקורי, כלומר שיפור בגודל הרעש.

לכן הסקריפט הזה לא מחפש פרמטרים. הוא עושה שני דברים אחרים:

  מפרק את התוצאה לפי **סיבת יציאה**, כדי לראות איפה הכסף באמת
  נמצא. זו לא בחירה מתוך מרחב — זו חלוקה של אותה תוצאה.

  ולכל מועמד לשינוי הוא מדפיס את השיפור **לצד רף הרעש**. שיפור
  קטן משגיאת התקן אינו ממצא, גם אם הוא חיובי, וגם אם הוא מפתה.

מה מותר להסיק מכאן
-------------------
רק מועמד ששלושת אלה מתקיימים בו:

  יש לו מנגנון. "עסקאות אחרי 14:30 לא מספיקות להגיע ליעד לפני
  הסגירה הכפויה" הוא מנגנון. "עסקאות בימי שלישי מפסידות" הוא לא.

  השיפור גדול משגיאת התקן, לא רק חיובי.

  והוא נבדק **קדימה** — על הרצת הנייר או על חשבון אמיתי — ולא
  מאומץ בגלל שהוא משפר את הטבלה הזאת.

שימוש
-----
    python3 diagnose_edge.py
    python3 diagnose_edge.py ~/Desktop/replay_results.csv
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CSV_DEFAULT = Path.home() / "Desktop" / "replay_results.csv"


def banner(t):
    print(f"\n{'=' * 64}\n  {t}\n{'=' * 64}")


def se_of(x: np.ndarray, day=None) -> float:
    """שגיאת תקן, מקובצת לפי יום כשאפשר.

    עסקאות באותו אחר צהריים אינן תצפיות נפרדות, ושגיאת תקן
    שמניחה עצמאות צרה מדי — כלומר הופכת רעש לממצא.
    """
    if day is None or len(set(day)) < 2:
        return float(np.std(x, ddof=1) / np.sqrt(max(len(x), 1)))
    means = np.array([x[np.array(day) == d].mean() for d in sorted(set(day))])
    return float(np.std(means, ddof=1) / np.sqrt(len(means)))


def verdict(delta: float, se: float) -> str:
    if se <= 0 or not np.isfinite(se):
        return "אין רף להשוות אליו"
    r = delta / se
    if abs(r) < 1.0:
        return f"בתוך הרעש ({r:+.1f} שגיאות תקן) — לא ממצא"
    if abs(r) < 2.0:
        return f"{r:+.1f} שגיאות תקן — רמז, לא הוכחה"
    return f"{r:+.1f} שגיאות תקן — שווה בדיקה קדימה"


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df.status == "filled"].copy()
    for c in ("net_R", "raw_R", "mfe_R", "mae_R", "risk_pts", "bars_held"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fill_ts"] = pd.to_datetime(df.fill_ts, errors="coerce", utc=True,
                                   format="mixed")
    df["day"] = df.fill_ts.dt.date
    df["hour"] = df.fill_ts.dt.tz_convert("America/New_York").dt.hour
    return df.dropna(subset=["net_R"])


def by_reason(df: pd.DataFrame) -> None:
    banner("לאן הכסף הולך — פירוק לפי סיבת יציאה")
    print(f"{'סיבה':>14} {'n':>5} {'%':>6} {'תוחלת':>10} {'תרומה':>10}")
    total = df.net_R.sum()
    for reason, g in df.groupby("reason"):
        share = g.net_R.sum()
        print(f"{reason:>14} {len(g):>5} {100*len(g)/len(df):>5.0f}% "
              f"{g.net_R.mean():>+9.3f}R {share:>+9.1f}R")
    print(f"{'סך הכל':>14} {len(df):>5} {100:>5.0f}% "
          f"{df.net_R.mean():>+9.3f}R {total:>+9.1f}R")
    print("\n  זו חלוקה של אותה תוצאה, לא בחירה מתוך מרחב אפשרויות,")
    print("  ולכן היא לא סובלת מהטיית בחירה. מה שנעשה איתה — כן.")


def drop_bucket(df: pd.DataFrame, mask, label: str) -> None:
    """מה קורה אם קבוצה שלמה לא נלקחת. לא נטענת כ-1R-, פשוט לא נלקחת."""
    if isinstance(mask, pd.Series) and not mask.index.equals(df.index):
        # מסכה שנבנתה על מסגרת ממוינת. יישור מפורש, כי pandas עושה
        # אותו בשקט ומדפיס אזהרה — ותיקון שקט מחזיר תשובה על
        # השורות הלא נכונות.
        mask = mask.reindex(df.index)
    kept = df[~mask.astype(bool)]
    if len(kept) < 10 or mask.sum() == 0:
        return
    base, new = df.net_R.mean(), kept.net_R.mean()
    se = se_of(df.net_R.values, df.day.tolist())
    print(f"\n  {label}")
    print(f"    מסיר {int(mask.sum())} עסקאות מתוך {len(df)}")
    print(f"    {base:+.3f}R -> {new:+.3f}R   ({new-base:+.3f}R)")
    print(f"    {verdict(new - base, se)}")


def candidates(df: pd.DataFrame) -> None:
    banner("מועמדים לשינוי — כל אחד מול רף הרעש")
    if "reason" in df:
        drop_bucket(df, df.reason == "gap_scratch",
                    "לא להיכנס כשהנר פער דרך הרמה והסטופ יחד")
        drop_bucket(df, df.reason == "eod",
                    "לא לקחת סטאפ שלא הספיק להיסגר לפני ההשטחה")
    if "hour" in df and df.hour.notna().any():
        for cutoff in (14, 13, 12):
            drop_bucket(df, df.hour >= cutoff,
                        f"לא להיכנס אחרי {cutoff}:00 שעון ניו יורק")
    if "risk_pts" in df:
        med = df.risk_pts.median()
        drop_bucket(df, df.risk_pts < med,
                    f"רק סטאפים עם סטופ רחב מ-{med:.1f} נקודות "
                    "(עלות ב-R יורדת ככל שהסטופ רחב)")


def target_reach(df: pd.DataFrame) -> None:
    """כמה רחוק המחיר באמת הולך לטובתך. זה קובע יעד, לא רשת."""
    banner("עד כמה המחיר הולך לטובה — מה יעד אפשרי בכלל")
    if "mfe_R" not in df:
        print("  אין mfe_R בקובץ.")
        return
    m = df.mfe_R.dropna()
    print(f"  חציון ה-MFE: {m.median():+.2f}R   ממוצע: {m.mean():+.2f}R")
    print(f"\n{'יעד':>8} {'הגיעו':>8} {'%':>7}")
    for t in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        n = int((m >= t).sum())
        print(f"{t:>7.1f}R {n:>8} {100*n/len(m):>6.0f}%")
    print("\n  זו מדידה ישירה של כמה רחוק המחיר הולך, ולא בחירה של")
    print("  היעד הרווחי ביותר בדיעבד. אם רוב העסקאות לא מגיעות ליעד")
    print("  הרשום, היעד רחוק מדי — וזה מנגנון, לא התאמה.")


def holding(df: pd.DataFrame) -> None:
    banner("כמה זמן לוקח להכריע — האם כניסות מאוחרות נידונות מראש")
    if "bars_held" not in df:
        return
    wins = df[df.net_R > 0].bars_held.dropna()
    if len(wins) < 5:
        return
    print(f"  נרות עד הכרעה, מנצחות: חציון {wins.median():.0f} "
          f"(={5*wins.median():.0f} דקות), אחוזון 75 {wins.quantile(.75):.0f}")
    need = 5 * wins.median()
    print(f"\n  כלומר עסקה שנכנסת פחות מ-{need:.0f} דקות לפני ההשטחה")
    print("  ב-15:58 לא סבירה להגיע ליעד. זה מנגנון שאפשר לבדוק")
    print("  קדימה, ולא כלל שנמצא בחיפוש.")
    if "hour" in df:
        late = df[df.hour >= 15]
        if len(late) >= 5:
            print(f"\n  בפועל, {len(late)} עסקאות נכנסו אחרי 15:00: "
                  f"תוחלת {late.net_R.mean():+.3f}R")


def concentration(df: pd.DataFrame) -> None:
    """כמה מהתוחלת תלויה בפרק זמן בודד.

    תוחלת חיובית יכולה להיות שני דברים שונים לגמרי: יתרון קטן
    שחוזר על עצמו, או חודש אחד טוב ושניים שטוחים. שניהם מדפיסים
    את אותו ממוצע, ורק הראשון מצדיק חשבון. ההפרדה היא להשמיט
    תקופה אחת ולראות מה נשאר — לא בחירה מתוך מרחב אפשרויות אלא
    אותה תוצאה בדיוק, מפורקת.

    זה לא מבחן מובהקות. חודש שמחזיק את כל התוצאה הוא מדגם של
    אחד, ואין דרך להכריז ממנו על יתרון ולא לשלול אותו.
    """
    banner("כמה מזה תלוי בתקופה אחת")
    tot = float(df.net_R.sum())
    ts = pd.to_datetime(df.ts) if "ts" in df.columns else None
    for unit, key in (("חודש", ts.dt.to_period("M").astype(str) if ts is not None else None),
                      ("יום", df.day)):
        if key is None:
            continue
        g = df.groupby(key).net_R.agg(["size", "sum", "mean"])
        if len(g) < 2:
            continue
        worst = g["sum"].idxmax()          # התקופה שתורמת הכי הרבה
        rest = df[key != worst]
        share = 100 * g.loc[worst, "sum"] / tot if tot else float("nan")
        print(f"\n  לפי {unit}: {len(g)} תקופות, סך הכל {tot:+.1f}R")
        print(f"  ה{unit} התורם ביותר ({worst}): {g.loc[worst, 'sum']:+.1f}R "
              f"= {share:.0f}% מהסך")
        print(f"  בלעדיו: {len(rest)} עסקאות, תוחלת "
              f"{rest.net_R.mean():+.3f}R (במקום {df.net_R.mean():+.3f}R)")
        if share >= 70:
            print(f"  מעל 70% מתוך תקופה אחת. זה לא יתרון שחוזר על")
            print(f"  עצמו — זו תקופה אחת, ומדגם של אחת לא מכריע דבר.")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_DEFAULT
    if not path.exists():
        sys.exit(f"אין {path}. להריץ קודם את pipeline.py.")
    df = load(path)
    if df.empty:
        sys.exit("אין עסקאות שהתמלאו בקובץ.")
    se = se_of(df.net_R.values, df.day.tolist())
    banner("הבסיס")
    print(f"  {len(df)} עסקאות, {df.day.nunique()} ימי מסחר")
    # אילו עמודות רשות הגיעו מהסטאפים. בלי השורה הזאת "אין grade"
    # נראה כמו תקלה בבודק במקום כמו נתון שלא יוצא, וההשערה הראשונה
    # בתור נשארת חסומה בלי שאיש יֵדע למה.
    opt = {"grade": "דירוג הסטאפ", "day_efficiency": "מגמה מול דשדוש",
           "day_atr_pct": "תנודתיות יומית", "setup_type": "סוג הסטאפ"}
    have = [n for c, n in opt.items() if c in df.columns]
    miss = [n for c, n in opt.items() if c not in df.columns]
    if have:
        print(f"  עמודות רשות שהגיעו: {', '.join(have)}")
    if miss:
        print(f"  חסרות: {', '.join(miss)} — הבודקים שלהן לא ירוצו")
    print(f"  תוחלת {df.net_R.mean():+.3f}R, שגיאת תקן מקובצת {se:.3f}R")
    print(f"\n  רף הרעש: שיפור קטן מ-{se:.3f}R אינו ממצא.")
    by_reason(df)
    concentration(df)
    target_reach(df)
    holding(df)
    candidates(df)
    banner("מה מותר לעשות עם זה")
    print("  מועמד מאומץ רק אם שלושת אלה מתקיימים:")
    print("    1. יש לו מנגנון שאפשר להסביר בלי להסתכל בטבלה.")
    print("    2. השיפור גדול משגיאת התקן, לא רק חיובי.")
    print("    3. הוא נבדק קדימה — נייר או חשבון אמיתי — ולא אומץ")
    print("       בגלל שהוא משפר את המדגם שבו נמצא.")
    print("\n  מועמד שעובר רק את 2 הוא הדרך היקרה ביותר להפסיד כסף")
    print("  כאן, כי הוא נראה בדיוק כמו ממצא.")


if __name__ == "__main__":
    main()
