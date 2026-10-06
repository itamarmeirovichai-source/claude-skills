#!/usr/bin/env python3
"""
futures_era_check.py — האם הפיגור קיים גם בעידן החוזים, או רק בעידן ה-ETF.

למה זה השאלה שנשארה
-------------------
כל האבחון עד כה כיסה 304 סטאפים מ-27/02 עד 15/05 — התקופה שבה הבוט
עבד על SPY ו-QQQ. שם הוכח פיגור של כ-15 ימי לוח: שוקת 2.69, שגיאה
0.404% לעומת 4.49% בפיגור אפס.

ב-18/05 הסטאפים קפצו מקנה מידה של ETF לקנה מידה של חוזים, וב-17/09
הפיד מחזיר נרות של אותו יום. כלומר משהו השתנה. מה שמעולם לא נבדק
הוא 131 הסטאפים שבין שני התאריכים האלה. הם קובעים מתי מתחיל שעון
איסוף הראיות: אם הם נקיים, יש כבר בסיס. אם לא, הכל מתחיל מאפס.

למה נרות שעתיים
---------------
IBKR סירב להחזיר חוזים היסטוריים, אבל TF_CONFIG מגדיר ל-1h חלון של
730 יום — שנתיים אחורה, הרבה מעבר למאי. רזולוציה שעתית גסה מ-5 דקות,
אבל הפיגור שמחפשים הוא 15 יום. שעה אחת של תנועה ב-ES שווה כ-0.15%,
והאות שמחפשים הוא 4%. הרעש לא מסתיר כלום בסדר הגודל הזה.

הבקרה, ולמה בלעדיה זה חסר ערך
------------------------------
כאן משווים מול yfinance, בעוד שהממצא המקורי נשען על נרות של IBKR.
אם ההיסטוריה של yfinance עצמה מוסטת, הייתי משווה דבר מוסט לעצמו
ומקבל "נקי" בלי שיהיה נקי. לכן הסקריפט מריץ קודם בקרה: אותם סטאפים
של עידן ה-ETF, הפעם מול SPY/QQQ שעתיים של yfinance. אם הבקרה
משחזרת את השוקת שנמצאה מול IBKR, מקור הנתונים כשר והמבחן תקף.
אם הבקרה נופלת — המבחן לא אומר כלום, והסקריפט אומר את זה במפורש
במקום להסיק.

מה נרשם מראש, לפני שראיתי את המספרים
-------------------------------------
  בקרה נקייה  = שוקת מעל 2.0 סביב 13–17 יום.
  אם החוזים נקיים : שגיאה בפיגור אפס מתחת ל-0.6%, ואין שוקת בשום מקום.
  אם הבאג נמשך   : שגיאה בפיגור אפס מעל 2%, ושוקת סביב 15 יום.
  כל דבר אחר     = תבנית שלישית שלא חזיתי, ואז לא מסיקים אלא בודקים.

שימוש
-----
    python3 futures_era_check.py
    python3 futures_era_check.py '/נתיב/לתיקיית/הבוט'
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from drift_diagnostic import load_bars, load_setups
from lag_refine import scan_time, summarize

D = Path.home() / "Desktop"
BOT_DEFAULT = D / "meirox-ai" / "MeiroX-AI - בוט מסחר"
ET = "America/New_York"

# טווח הסריקה. 30 יום נותן מקום לשוקת ב-15 עם צדדים משני הכיוונים.
SCAN_HI_DAYS = 30.0
STEP_HOURS = 1.0
PER_DAY = 24.0 / STEP_HOURS
# מרחק בדיקת הצדדים, בימים. אותו ערך כמו בסריקות הקודמות.
FLANK_DAYS = 4.0
# שוקת נחשבת אמיתית מעל זה. אותו סף כמו ב-lag_refine.
SHARP_RATIO = 2.0
# מתחת לזה בפיגור אפס, ההפרש מוסבר ברזולוציה השעתית ובחישוב ה-FVG.
CLEAN_AT_ZERO = 0.6
# שגיאה בפיגור אפס שמחזקת את המסקנה שהבאג נמשך — אבל אינה תנאי לה.
# היא מודדת כמה השוק זז ב-15 יום, לא כמה חמור הבאג: אותו פיגור בדיוק
# נותן 4.5% בשוק תנודתי ו-1.5% ברגוע. השוקת היא הקובעת, כי בכיול
# שב-lag_refine היא 2.5–2.7 כשיש פיגור ו-1.00 בדיוק כשאין, בכל רמות
# הרעש. בדיקה שדרשה גם וגם פסלה פיגור אמיתי באחד מחמישה זרעים.
CORROBORATING_AT_ZERO = 2.0
MIN_SETUPS = 30


def fetch_1h(bot: Path, symbols) -> dict:
    """נרות שעתיים דרך הפיד של הבוט עצמו, עם שמירה למטמון על הדיסק."""
    B = {}
    need = [s for s in symbols if not (D / f"{s}_1h.csv").exists()]
    if need:
        sys.path.insert(0, str(bot))
        try:
            from data.feed import MarketDataFeed
        except Exception as e:
            sys.exit(f"\nלא הצלחתי לטעון את data.feed מתוך {bot}\n  {e}")
        feed = MarketDataFeed()
        for sym in need:
            df = feed.get_ohlcv(sym, "1h")
            if df is None or df.empty:
                print(f"  {sym}: הפיד החזיר ריק")
                continue
            df = df.reset_index()
            t = df.columns[0]
            pd.DataFrame({
                "timestamp": df[t].astype(str),
                "open": df["Open"], "high": df["High"],
                "low": df["Low"], "close": df["Close"],
            }).to_csv(D / f"{sym}_1h.csv", index=False)
    for sym in symbols:
        p = D / f"{sym}_1h.csv"
        if p.exists():
            b = load_bars(p)
            if not b.empty:
                B[sym] = b
                print(f"  {sym}: {len(b):,} נרות שעתיים  "
                      f"{b.ts.iloc[0]:%Y-%m-%d} עד {b.ts.iloc[-1]:%Y-%m-%d}")
    return B


def load_futures_setups(path: Path) -> pd.DataFrame:
    """הסטאפים בקנה מידה של חוזים — אלה שמעולם לא נבדקו."""
    s = pd.read_csv(path)
    s["ts"] = pd.to_datetime(s.timestamp, errors="coerce", utc=True,
                             format="mixed").dt.tz_convert(ET)
    s = s.dropna(subset=["ts", "entry"])
    s["direction"] = s.direction.str.strip().str.lower()
    s = s[s.direction.isin(["long", "short"])]
    s["_k"] = (s.ts.dt.date.astype(str) + s.market + s.direction
               + s.entry.round(2).astype(str))
    s = s.sort_values("ts").drop_duplicates("_k").reset_index(drop=True)
    s["symbol"] = s.market
    return s[s.entry >= 2000].reset_index(drop=True)


def lock_time(s: pd.DataFrame, B: dict, hi_days: float) -> pd.DataFrame:
    """רק סטאפים שיש להם נר גם בהיסט המקסימלי.

    בלי זה, חציון על אוכלוסייה מתכווצת מודד נשירה ולא התאמה — הטעות
    שהפילה את lag_scan.
    """
    keep = []
    for sym, g in s.groupby("symbol"):
        b = B.get(sym)
        if b is None or b.empty:
            continue
        far = np.searchsorted(
            b.ts.values, (g.ts - pd.Timedelta(days=hi_days)).values,
            side="right") - 1
        keep.append(g[far >= 0])
    if not keep:
        return s.iloc[:0]
    return pd.concat(keep).sort_values("ts").reset_index(drop=True)


def classify(v: dict) -> str:
    """שלוש אפשרויות, והאסימטריה ביניהן מכוונת.

    "מפוגר" נקבע לפי השוקת לבדה, כי היא המדד שנשאר יציב בכל רמות
    הרעש ובכל רמות התנודתיות. "נקי" דורש גם היעדר שוקת וגם שגיאה
    קטנה בפיגור אפס — כי כדי להכריז שהמחיר שנרשם הוא המחיר ששרר,
    לא מספיק שלא מצאתי פיגור: צריך גם שההתאמה בפועל תהיה טובה.
    כל השאר נשאר לא מוכרע במפורש.
    """
    if v["two_sided"] >= SHARP_RATIO:
        return "lagged"
    if v["at_zero"] <= CLEAN_AT_ZERO:
        return "clean"
    return "unknown"


def run_scan(s: pd.DataFrame, B: dict, label: str):
    """סריקת פיגור בזמן לוח על קבוצה נעולה. מחזיר את הסיכום."""
    c = lock_time(s, B, SCAN_HI_DAYS)
    print(f"\n{'=' * 58}\n  {label}\n{'=' * 58}")
    print(f"  סטאפים: {len(s)}  ->  קבוצה קבועה {len(c)}")
    if len(c) < MIN_SETUPS:
        print(f"  פחות מ-{MIN_SETUPS} — אין מספיק כדי להסיק.")
        return None, c
    d = scan_time(c, B, 0.0, SCAN_HI_DAYS, STEP_HOURS)
    if d.empty:
        print("  הסריקה חזרה ריקה.")
        return None, c
    print(f"\n{'ימים':>10} {'n':>6} {'שגיאה חציונית':>15} {'עד 0.5%':>10}")
    best = float(d.offset.iloc[int(d.median_err_pct.values.argmin())])
    for r in d.itertuples():
        show = (abs(r.offset * 24 % 24) < 1e-9) or np.isclose(r.offset, best)
        if not show:
            continue
        mark = "  <<<" if np.isclose(r.offset, best) else ""
        print(f"{r.offset:>10.2f} {r.n:>6} {r.median_err_pct:>14.3f}% "
              f"{r.within_0_5pct:>9.1f}%{mark}")
    v = summarize(d, flank_days=FLANK_DAYS, per_day=PER_DAY)
    at_zero = float(d.median_err_pct.iloc[0])
    v["at_zero"] = at_zero
    print(f"\n  בפיגור אפס : {at_zero:.3f}%")
    print(f"  מינימום    : {v['at']:.2f} ימים  ->  {v['err']:.3f}%")
    print(f"  שוקת       : {v['two_sided']:.2f} "
          f"(מעל {SHARP_RATIO} = ירידה אמיתית משני הצדדים)")
    d.to_csv(D / f"futures_era_{label.split()[0]}.csv", index=False)
    return v, c


def main() -> None:
    bot = Path(sys.argv[1]) if len(sys.argv) > 1 else BOT_DEFAULT
    setups = D / "setups.csv"
    if not setups.exists():
        sys.exit(f"חסר {setups}")

    print("\nמושך נרות שעתיים:")
    B = fetch_1h(bot, ("SPY", "QQQ", "ES", "NQ"))
    if not B:
        sys.exit("\nאין נרות. בלי נתוני מחיר אין מה לבדוק.")

    etf = load_setups(setups)
    fut = load_futures_setups(setups)
    print(f"\nסטאפים: {len(etf)} בעידן ה-ETF, {len(fut)} בעידן החוזים")

    ctrl, _ = run_scan(etf, B, "בקרה — עידן ה-ETF מול yfinance")
    test, fut_c = run_scan(fut, B, "המבחן — עידן החוזים")

    print(f"\n{'=' * 58}\n  הכרעה\n{'=' * 58}")

    if ctrl is None:
        print("  הבקרה לא רצה. בלי בקרה אין תוקף למבחן.")
        return
    if ctrl["two_sided"] < SHARP_RATIO:
        print(f"  הבקרה נפלה: שוקת {ctrl['two_sided']:.2f} בעידן ה-ETF,")
        print("  למרות שמול נרות IBKR היא הייתה 2.69.")
        print("  כלומר ההיסטוריה של yfinance אינה עד כשר כאן,")
        print("  ותוצאת המבחן על החוזים לא אומרת כלום. לא מסיקים.")
        return
    print(f"  הבקרה עברה: שוקת {ctrl['two_sided']:.2f} ב-{ctrl['at']:.1f} ימים.")
    print("  yfinance משחזר את הממצא של IBKR, אז הוא עד כשר.")

    if test is None:
        print("\n  המבחן לא רץ — אין מספיק סטאפים בעידן החוזים.")
        return

    print()
    call = classify(test)
    if call == "lagged":
        print(f"  הבאג נמשך. שוקת {test['two_sided']:.2f} "
              f"ב-{test['at']:.1f} ימים, שגיאה {test['at_zero']:.3f}% בפיגור אפס.")
        if test["at_zero"] < CORROBORATING_AT_ZERO:
            print("  השגיאה בפיגור אפס צנועה כי השוק זז מעט בחלון הזה,")
            print("  לא כי הפיגור קטן. השוקת היא הראיה.")
        print("  גם עידן החוזים מורעל. אין אף ראיה תקפה,")
        print("  ואיסוף אמיתי מתחיל רק אחרי שהבאג ייסגר.")
    elif call == "clean":
        print(f"  עידן החוזים נקי. שגיאה {test['at_zero']:.3f}% בפיגור אפס,")
        print(f"  ואין שוקת בשום מקום (הגבוה ביותר {test['two_sided']:.2f}).")
        print(f"  כלומר {len(fut_c)} הסטאפים האלה נרשמו במחיר ששרר,")
        print("  והם ראיה תקפה. שעון איסוף הראיות מתחיל ב-18/05.")
    else:
        print(f"  לא מוכרע: בפיגור אפס {test['at_zero']:.3f}%, "
              f"שוקת {test['two_sided']:.2f} ב-{test['at']:.1f} ימים.")
        print("  אין שוקת, אבל גם השגיאה בפיגור אפס גדולה מדי")
        print("  מכדי לקרוא לזה נקי. משהו שלישי קורה כאן, ולא מסיקים")
        print("  ממנו — זה דורש בדיקה נפרדת לפני שנשענים על הסטאפים.")

    print(f"\nנשמר: {D}/futures_era_*.csv")


if __name__ == "__main__":
    main()
