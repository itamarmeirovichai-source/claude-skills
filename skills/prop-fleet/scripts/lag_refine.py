#!/usr/bin/env python3
"""
lag_refine.py — האם המחיר הישן נעול על משך זמן, או על מספר נרות.

למה צריך את זה אחרי lag_scan
----------------------------
lag_scan סרק בקפיצות של יום שלם ומצא מינימום ב-15 יום, שגיאה 0.500%,
שיפור פי 8.1. הוא הדפיס "רמז חלש" כי דרשתי שגיאה מתחת ל-0.5% — סף
מוחלט שלא היה מוצדק. שגיאה של חצי אחוז היא בדיוק מה שמצפים ממינימום
אמיתי בסריקה גסה:

  · ה-entry הוא רמת FVG שחושבה מנר, לא ציטוט שוק. גם בהתאמה מושלמת
    בזמן נשאר הפרש.
  · הפיגור החציוני שנמדד הוא 15.16 ימים. קפיצות של יום שלם מחטיאות
    את השארית, ורבע יום של תנועה תוך-יומית שווה בקלות 0.3%.

ושתי בעיות מתודיות אמיתיות ב-lag_scan:

  1. האוכלוסייה השתנתה תוך כדי. בפיגור 0 נמדדו 304 סטאפים, בפיגור 15
     רק 285 — הסטאפים המוקדמים נופלים מחוץ לסדרת הנרות. חציון על קבוצה
     מתכווצת אינו בר-השוואה לחציון על הקבוצה המלאה, ובמקרה הגרוע
     הנשירה לבדה יוצרת מינימום מדומה. כאן הקבוצה ננעלת מראש.
  2. יחידת המדידה לא נבדקה. פיגור קבוע בזמן ופיגור קבוע במספר נרות הם
     שני באגים שונים עם שני תיקונים שונים, והם נבדלים בדיוק בסופי
     שבוע: היסט נרות מדלג על הפער, משך זמן נופל לתוכו.

מה זה מכריע
-----------
    מינימום חד ביחידת זמן    -> מטמון או TTL. מחיר שנשמר ולא רוענן.
    מינימום חד ביחידת נרות   -> אינדקס שגוי. קריאה שמחזירה bar[-N].
    שתיהן שטוחות             -> המחיר לא נקרא מסדרה היסטורית.

שימוש
-----
    python3 lag_refine.py
    python3 lag_refine.py /נתיב/אחר
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from drift_diagnostic import load_bars, load_setups

# שתי הסריקות חייבות לכסות את אותו טווח פיזי, אחרת ההשוואה ביניהן
# מוטה: מי שנסרק רחוק יותר מקבל יותר הזדמנויות למצוא נקודה נמוכה.
# 20 ימי לוח הם כ-14.3 ימי מסחר, כלומר כ-1,114 נרות של חמש דקות.
SESSION_BARS = 78
TIME_LO_DAYS, TIME_HI_DAYS, TIME_STEP_HOURS = 0.0, 20.0, 1.0
BAR_LO, BAR_HI = 0, 1114
# שוקת נחשבת אמיתית אם השגיאה גדלה פי כך משני צידי המינימום.
SHARP_RATIO = 2.0
# באיזה מרחק בודקים את צידי השוקת. מרחק פיזי אחיד לכל הסריקות.
FLANK_DAYS = 4.0
# מרווח מעבר לטווח המועמדים, כדי שלמינימום יהיו שני צדדים להשוות אליהם.
PAD_DAYS = 5.0


def _index_at(bars: pd.DataFrame, when) -> np.ndarray:
    """מיקום הנר האחרון שנסגר עד לכל רגע. -1 אם אין נר קודם."""
    return np.searchsorted(bars.ts.values, np.asarray(when), side="right") - 1


def _by_symbol(s: pd.DataFrame, B: dict):
    """לכל סימבול: המחירים, הרגעים, ומיקום הנר של כל סטאפ."""
    for sym, g in s.groupby("symbol"):
        b = B.get(sym)
        if b is None or b.empty:
            continue
        yield sym, g, b, _index_at(b, g.ts.values)


def scan_bars(s: pd.DataFrame, B: dict, lo=BAR_LO, hi=BAR_HI) -> pd.DataFrame:
    """שגיאה לפי היסט במספר נרות, על קבוצה קבועה."""
    parts = [(g, b, idx) for _, g, b, idx in _by_symbol(s, B)]
    rows = []
    for k in range(lo, hi + 1):
        errs = []
        for g, b, idx in parts:
            j = idx - k
            ok = j >= 0                      # אותה קבוצה בכל היסט: ראה cohort()
            if not ok.any():
                continue
            p = b.mid.values[j[ok]]
            e = g.entry.values[ok]
            good = np.isfinite(p) & (p > 0)
            errs.append(np.abs(e[good] - p[good]) / p[good] * 100)
        if errs:
            e = np.concatenate(errs)
            if len(e) >= 20:
                rows.append({"offset": k, "n": len(e),
                             "median_err_pct": float(np.median(e)),
                             "within_0_5pct": float((e < 0.5).mean() * 100)})
    return pd.DataFrame(rows)


def scan_time(s: pd.DataFrame, B: dict, lo=TIME_LO_DAYS, hi=TIME_HI_DAYS,
              step_h=TIME_STEP_HOURS) -> pd.DataFrame:
    """שגיאה לפי היסט בזמן לוח, על קבוצה קבועה."""
    parts = [(g, b) for _, g, b, _ in _by_symbol(s, B)]
    rows = []
    for hours in np.arange(lo * 24, hi * 24 + 1e-9, step_h):
        delta = pd.Timedelta(hours=float(hours))
        errs = []
        for g, b in parts:
            j = _index_at(b, (g.ts - delta).values)
            ok = j >= 0
            if not ok.any():
                continue
            p = b.mid.values[j[ok]]
            e = g.entry.values[ok]
            good = np.isfinite(p) & (p > 0)
            errs.append(np.abs(e[good] - p[good]) / p[good] * 100)
        if errs:
            e = np.concatenate(errs)
            if len(e) >= 20:
                rows.append({"offset": hours / 24, "n": len(e),
                             "median_err_pct": float(np.median(e)),
                             "within_0_5pct": float((e < 0.5).mean() * 100)})
    return pd.DataFrame(rows)


def cohort(s: pd.DataFrame, B: dict, max_days: float, max_bars: int) -> pd.DataFrame:
    """רק סטאפים שאפשר למדוד בכל היסט בטווח.

    זו ההגנה מפני המינימום המדומה: אם סטאפים נושרים ככל שההיסט גדל,
    ירידה בחציון יכולה לשקף את מי שנשר ולא את איכות ההתאמה.
    """
    keep = []
    for _, g, b, idx in _by_symbol(s, B):
        far = _index_at(b, (g.ts - pd.Timedelta(days=max_days)).values)
        keep.append(g[(far >= 0) & (idx - max_bars >= 0)])
    return (pd.concat(keep).sort_values("ts").reset_index(drop=True)
            if keep else s.iloc[:0])


def lock_cohort(s: pd.DataFrame, B: dict, hi_days: float, hi_bars: int,
                floor: int = 60, min_days: float = 6.0):
    """נועל קבוצה, ומקצר את הסריקה אם הקבוצה מתרוקנת.

    נעילה עמוקה עולה בסטאפים מוקדמים. עדיף לסרוק פחות עמוק על קבוצה
    שפויה מאשר להשוות חציונים של אוכלוסיות שונות.
    """
    c = cohort(s, B, hi_days, hi_bars)
    while len(c) < floor and hi_days > min_days:
        hi_days -= 2.0
        hi_bars = int(round(hi_days * SESSION_BARS * 5 / 7))
        c = cohort(s, B, hi_days, hi_bars)
    return c, hi_days, hi_bars


def summarize(d: pd.DataFrame, flank_days: float = FLANK_DAYS,
              limit: float | None = None, per_day: float = 1.0) -> dict:
    """המינימום, וכמה הוא באמת שוקת.

    "חדות" לבדה לא מספיקה: עקומה שרק עולה נותנת יחס גבוה בין הטיפוסי
    למינימום, והמינימום שלה יושב על שפת החלון בלי משמעות. שוקת אמיתית
    יורדת משני הצדדים, וזה מה ש-two_sided מודד.

    המרחק שבו בודקים את הצדדים חייב להיות פיזי ולא מדוד בנקודות רשת.
    בסריקה גסה של יום שלם, השכן הקרוב רחוק יום אחד בלבד, שם העקומה
    עוד שטוחה — ואז שוקת אמיתית נפסלת. flank_days קובע מרחק אחיד
    בימים, וכל סריקה ממירה אותו ליחידות שלה דרך per_day.
    """
    if d.empty:
        return {}
    cand = d[d.offset <= limit] if limit is not None else d
    if cand.empty:
        cand = d
    i = int(np.where(d.offset.values == cand.offset.values[
        int(cand.median_err_pct.values.argmin())])[0][0])
    best = d.iloc[i]
    lo = float(best.median_err_pct)
    w = max(1, int(round(flank_days * per_day)))
    if lo > 0 and i - w >= 0 and i + w < len(d):
        two_sided = min(float(d.median_err_pct.iloc[i - w]),
                        float(d.median_err_pct.iloc[i + w])) / lo
    else:
        two_sided = 1.0          # בלי שני צדדים אין שוקת להוכיח
    return {"at": float(best.offset), "err": lo, "n": int(best.n),
            "within": float(best.within_0_5pct),
            "typical": float(d.median_err_pct.median()),
            "sharpness": float(d.median_err_pct.median()) / lo if lo > 0 else float("inf"),
            "two_sided": two_sided,
            "width": int((d.median_err_pct <= lo * 1.5).sum()),
            "points": len(d)}


def _table(d: pd.DataFrame, unit: str, every: int, best_at: float) -> None:
    print(f"{unit:>12} {'n':>6} {'שגיאה חציונית':>15} {'עד 0.5%':>10}")
    for i, r in enumerate(d.itertuples()):
        if i % every and not np.isclose(r.offset, best_at):
            continue
        mark = "  <<<" if np.isclose(r.offset, best_at) else ""
        print(f"{r.offset:>12.2f} {r.n:>6} {r.median_err_pct:>14.3f}% "
              f"{r.within_0_5pct:>9.1f}%{mark}")


def main() -> None:
    D = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Desktop"
    sp = D / "setups.csv"
    if not sp.exists():
        sys.exit(f"לא נמצא {sp}")
    s_all = load_setups(sp)

    B = {}
    for sym in ("SPY", "QQQ"):
        p = D / f"{sym}_5min.csv"
        if p.exists():
            B[sym] = load_bars(p)
    if not B:
        sys.exit("אין נרות.")

    # נעילת הקבוצה עולה בסטאפים: ככל שהסריקה עמוקה יותר, יותר סטאפים
    # מוקדמים נושרים. אם הקבוצה מתרוקנת, מקצרים במקום להיכשל.
    # סורקים עמוק יותר מטווח המועמדים, כדי שלמינימום יהיו שני צדדים.
    deep_days = TIME_HI_DAYS + PAD_DAYS
    s, deep_days, deep_bars = lock_cohort(
        s_all, B, deep_days, int(round(deep_days * SESSION_BARS * 5 / 7)))
    hi_days = max(6.0, deep_days - PAD_DAYS)
    hi_bars = int(round(hi_days * SESSION_BARS * 5 / 7))

    print(f"\nסטאפים: {len(s_all):,}  ->  קבוצה קבועה {len(s):,} "
          f"(נשרו {len(s_all) - len(s):,} שאין להם נרות לכל עומק הסריקה)")
    if hi_days < TIME_HI_DAYS:
        print(f"  הסריקה קוצרה ל-{hi_days:.0f} ימים כדי לשמור על קבוצה שפויה")
    if len(s) < 20:
        sys.exit("הקבוצה הקבועה קטנה מדי. צריך סדרת נרות ארוכה יותר.")

    t = scan_time(s, B, TIME_LO_DAYS, deep_days, TIME_STEP_HOURS)
    bmap = scan_bars(s, B, BAR_LO, deep_bars)
    st = summarize(t, limit=hi_days, per_day=24 / TIME_STEP_HOURS)
    sb = summarize(bmap, limit=hi_bars, per_day=SESSION_BARS * 5 / 7)
    if not st or not sb:
        sys.exit("הסריקה לא החזירה מספיק נקודות.")

    print("\n" + "=" * 58)
    print("  לפי זמן לוח")
    print("=" * 58)
    _table(t, "ימים", 12, st["at"])
    print(f"\n  מינימום: {st['at']:.2f} ימים  ->  {st['err']:.3f}%   "
          f"(אופייני בחלון {st['typical']:.3f}%, חדות פי {st['sharpness']:.1f})")

    print("\n" + "=" * 58)
    print("  לפי מספר נרות")
    print("=" * 58)
    _table(bmap, "נרות", 50, sb["at"])
    print(f"\n  מינימום: {int(sb['at'])} נרות  ->  {sb['err']:.3f}%   "
          f"(אופייני בחלון {sb['typical']:.3f}%, חדות פי {sb['sharpness']:.1f})")

    print("\n" + "=" * 58)
    print("  הכרעה")
    print("=" * 58)
    time_wins = st["err"] < sb["err"]
    win, lose = (st, sb) if time_wins else (sb, st)
    unit = "ימים" if time_wins else "נרות"
    print(f"  זמן : {st['err']:.3f}% ב-{st['at']:.2f} ימים")
    print(f"  נרות: {sb['err']:.3f}% ב-{int(sb['at'])} נרות")
    print(f"  יחס : {lose['err'] / win['err']:.2f} לטובת {unit}")
    print(f"  שוקת: ירידה פי {win['two_sided']:.2f} משני צידי המינימום")

    if st["at"] < 0.5 and sb["at"] < SESSION_BARS / 2:
        print("\n  -> המחיר עדכני. אין פיגור בכלל, והסטייה מגיעה ממקור")
        print("     אחר לגמרי — לא מנתוני השוק. לבדוק את השערות 3 ו-4.")
    elif win["two_sided"] < SHARP_RATIO:
        print("\n  -> אין שוקת באף יחידה. המינימום יושב על שפת החלון או")
        print("     שהעקומה רק עולה — זה לא פיגור. המחיר לא נקרא מסדרה")
        print("     היסטורית, הוא חושב. לחזור להשערות 3 ו-4.")
    elif time_wins:
        print(f"\n  -> המחיר נעול על משך זמן: {st['at']:.2f} ימים.")
        print(f"     בהיסט הזה {st['within']:.0f}% מהסטאפים בתוך חצי אחוז.")
        print("     זה מטמון או קובץ שנשמר ולא רוענן. לחפש TTL, קובץ")
        print("     נתונים שנכתב פעם אחת, או רענון שנכשל בשקט.")
    else:
        sess = sb["at"] / 78
        print(f"\n  -> המחיר נעול על מספר נרות: {int(sb['at'])}, כלומר")
        print(f"     כ-{sess:.1f} ימי מסחר של נרות חמש דקות.")
        print(f"     בהיסט הזה {sb['within']:.0f}% מהסטאפים בתוך חצי אחוז.")
        print("     זה אינדקס: קריאה שמחזירה נר ישן מתוך החלון, לא האחרון.")

    out = D / "lag_refine.csv"
    pd.concat([t.assign(unit="days"), bmap.assign(unit="bars")]).to_csv(out, index=False)
    print(f"\nנשמר: {out}\n")


if __name__ == "__main__":
    main()
