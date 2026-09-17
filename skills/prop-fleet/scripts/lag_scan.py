#!/usr/bin/env python3
"""
lag_scan.py — בכמה זמן המחיר המוקלט מפגר אחרי השוק.

למה זה ולא drift_diagnostic
---------------------------
drift_diagnostic מחפש את הרגע שבו המחיר האמיתי היה הכי קרוב ל-entry. עם
4,680 נרות על טווח של כ-75 דולר, המרחק בין נרות סמוכים הוא כ-0.002%, אז
כמעט כל מחיר בטווח ימצא התאמה "מושלמת" במקרה. שגיאת התאמה של 0.001% לא
מוכיחה שהמחיר אמיתי — היא רק מוכיחה שהנרות צפופים.

כאן אין חיפוש חופשי. לכל סטאפ משווים את ה-entry למחיר בדיוק N ימים
קודם, ומחפשים איזה N ממזער את השגיאה על פני כל הסטאפים. אם יש מינימום
חד בפיגור מסוים — זה הפיגור. אם העקומה שטוחה — המחיר לא ישן.

מה מצפים לראות
--------------
ה-entry הוא רמת FVG שהאסטרטגיה חישבה, לא ציטוט שוק, אז גם בפיגור הנכון
הוא לא יתלכד בדיוק. הסטופ הוא 0.1%-0.3% מהמחיר, אז התאמה טובה היא
שגיאה חציונית באותו סדר גודל. אם בפיגור 0 השגיאה 4% ובפיגור כלשהו היא
צונחת ל-0.3% — זו התשובה.

שימוש
-----
    python3 lag_scan.py
    python3 lag_scan.py /נתיב/אחר
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from drift_diagnostic import load_bars, load_setups

MAX_LAG_DAYS = 45


def price_at(bars: pd.DataFrame, when) -> float:
    """המחיר האחרון שנסגר עד לרגע הזה. NaN אם אין נתונים."""
    past = bars[bars.ts <= when]
    return float(past.mid.iloc[-1]) if len(past) else float("nan")


def scan(s: pd.DataFrame, B: dict, max_lag=MAX_LAG_DAYS) -> pd.DataFrame:
    rows = []
    for lag in range(max_lag + 1):
        errs = []
        for r in s.itertuples():
            b = B.get(r.symbol)
            if b is None or b.empty:
                continue
            p = price_at(b, r.ts - pd.Timedelta(days=lag))
            if not np.isfinite(p) or p <= 0:
                continue
            errs.append(abs(r.entry - p) / p * 100)
        if len(errs) >= 20:
            e = np.array(errs)
            rows.append({"lag_days": lag, "n": len(e),
                         "median_err_pct": float(np.median(e)),
                         "mean_err_pct": float(e.mean()),
                         "within_0_5pct": float((e < 0.5).mean() * 100)})
    return pd.DataFrame(rows)


def main() -> None:
    D = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Desktop"
    sp = D / "setups.csv"
    if not sp.exists():
        sys.exit(f"לא נמצא {sp}")
    s = load_setups(sp)

    B = {}
    for sym in ("SPY", "QQQ"):
        p = D / f"{sym}_5min.csv"
        if p.exists():
            B[sym] = load_bars(p)
    if not B:
        sys.exit("אין נרות.")

    print(f"\nסטאפים: {len(s):,}   נרות: "
          f"{', '.join(f'{k} {len(v):,}' for k, v in B.items())}")

    d = scan(s, B)
    if d.empty:
        sys.exit("אין מספיק חפיפה בין הסטאפים לנרות.")

    best = d.loc[d.median_err_pct.idxmin()]
    at0 = d[d.lag_days == 0].median_err_pct.iloc[0]

    print("\n" + "=" * 58)
    print("  שגיאה חציונית לפי פיגור")
    print("=" * 58)
    print(f"{'פיגור':>7} {'n':>6} {'שגיאה חציונית':>15} {'עד 0.5%':>10}")
    for r in d.itertuples():
        mark = "  <<<" if r.lag_days == int(best.lag_days) else ""
        if r.lag_days % 2 == 0 or r.lag_days == int(best.lag_days):
            print(f"{r.lag_days:>7} {r.n:>6} {r.median_err_pct:>14.3f}% "
                  f"{r.within_0_5pct:>9.1f}%{mark}")

    print("\n" + "=" * 58)
    print(f"  בפיגור 0:          {at0:.3f}%")
    print(f"  הפיגור הטוב ביותר: {int(best.lag_days)} ימים  ->  "
          f"{best.median_err_pct:.3f}%")
    print(f"  שיפור:             פי {at0 / best.median_err_pct:.1f}")
    print("=" * 58)

    if best.lag_days == 0:
        print("\n  -> המחיר לא ישן. הסטייה מגיעה ממקור אחר.")
    elif best.median_err_pct < 0.5 and at0 / best.median_err_pct > 3:
        print(f"\n  -> המחיר מפגר ב-{int(best.lag_days)} ימים, חד-משמעית.")
        print(f"     בפיגור הזה {best.within_0_5pct:.0f}% מהסטאפים נופלים")
        print("     בתוך חצי אחוז מהמחיר האמיתי.")
        print("     לחפש בקוד מטמון, קובץ נתונים שלא מתרענן, או")
        print("     קריאה שמחזירה את הנר האחרון של חלון ישן.")
    elif at0 / best.median_err_pct > 1.5:
        print(f"\n  -> יש רמז לפיגור של {int(best.lag_days)} ימים, אבל חלש.")
        print(f"     השגיאה עדיין {best.median_err_pct:.2f}% — גדולה מדי")
        print("     מכדי שזה יהיה מחיר ישן ותו לא.")
    else:
        print("\n  -> העקומה שטוחה. הפיגור לא מסביר את הסטייה.")
        print("     המחירים לא נקראו מסדרה היסטורית — הם חושבו.")

    out = D / "lag_scan.csv"
    d.to_csv(out, index=False)
    print(f"\nנשמר: {out}\n")


if __name__ == "__main__":
    main()
