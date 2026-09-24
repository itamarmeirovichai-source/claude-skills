#!/usr/bin/env python3
"""
drift_diagnostic.py — למה מחירי הכניסה המוקלטים סטו מהמחיר האמיתי.

הרקע
----
בתקופת ה-ETF (פברואר-מאי 2026) מחירי הכניסה שנרשמו ב-analyses סטו
מהמחיר האמיתי של SPY/QQQ ב-2%-7%. פברואר היה מדויק (סטייה חציונית
0.03%), ומשם זה התדרדר. הבאג ב-broker/proxy.py לא מסביר את זה — מסלול
ה-proxy בכלל לא היה פעיל אז.

הבדיקה
------
לכל סטאפ, מחפשים את הרגע בנתוני הנרות האמיתיים שבו המחיר היה הכי קרוב
ל-entry שנרשם, ומשווים אותו לזמן שבו הסטאפ נוצר. ההפרש בין השניים מפריד
בין ההשערות:

    ההפרש ~ 0                 -> אין סטייה. הסטאפ הזה תקין.
    ההפרש קבוע (למשל 3 ימים)  -> מטמון עם TTL. מחיר ישן שלא רוענן.
    ההפרש גדל עם הזמן,
      והרגע המתאים מתכנס
      לתאריך אחד קבוע         -> עוגן קפוא. משתנה שנקבע פעם אחת ולא עודכן.
    רועש, בלי מבנה            -> לא מחיר ישן. ללכת להשערה 3 ו-4.

בנוסף נבדקות שתי השערות זולות:
    3. סימבול מוחלף  — האם entry של ES מתאים דווקא ל-QQQ ולהיפך
    4. פקטור קבוע    — האם היחס entry/אמיתי הוא מספר אחד יציב

שימוש
-----
    python3 drift_diagnostic.py
    python3 drift_diagnostic.py /נתיב/אחר

מצפה ל-~/Desktop/setups.csv, ~/Desktop/SPY_5min.csv, ~/Desktop/QQQ_5min.csv
(אותם קבצים ש-mx.py כבר משתמש בהם).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ET = "America/New_York"


def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    ren = {}
    for c in df.columns:
        lc = c.strip().lower()
        if lc in ("timestamp", "time", "datetime", "date", "t"):
            ren[c] = "ts"
        elif lc in ("open", "o"):
            ren[c] = "open"
        elif lc in ("high", "h"):
            ren[c] = "high"
        elif lc in ("low", "l"):
            ren[c] = "low"
        elif lc in ("close", "c", "last"):
            ren[c] = "close"
    df = df.rename(columns=ren)
    if "ts" not in df:
        df = df.rename(columns={df.columns[0]: "ts"})

    raw = df.ts.astype(str)
    first = raw.iloc[0]
    aware = first.endswith("Z") or (len(first) > 6 and first[-6] in "+-" and first[-3] == ":")
    t = pd.to_datetime(raw, errors="coerce", format="mixed", utc=True)
    df["ts"] = t.dt.tz_convert(ET) if aware else t.dt.tz_localize(None).dt.tz_localize(ET)

    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["mid"] = (df.high + df.low) / 2
    return (df.dropna(subset=["ts", "open", "high", "low", "close"])
              .sort_values("ts").reset_index(drop=True))


def load_setups(path: Path) -> pd.DataFrame:
    s = pd.read_csv(path)
    s["ts"] = pd.to_datetime(s.timestamp, errors="coerce", utc=True,
                             format="mixed").dt.tz_convert(ET)
    s = s.dropna(subset=["ts", "entry"])
    s["direction"] = s.direction.str.strip().str.lower()
    s = s[s.direction.isin(["long", "short"])]
    s["_k"] = (s.ts.dt.date.astype(str) + s.market + s.direction
               + s.entry.round(2).astype(str))
    s = s.sort_values("ts").drop_duplicates("_k").reset_index(drop=True)
    s["symbol"] = np.where(s.entry < 2000,
                           np.where(s.market == "ES", "SPY", "QQQ"), s.market)
    return s[s.entry < 2000].reset_index(drop=True)


def nearest_moment(entry: float, bars: pd.DataFrame):
    """הרגע שבו המחיר האמיתי היה הכי קרוב ל-entry, וכמה קרוב."""
    i = int(np.abs(bars.mid.values - entry).argmin())
    return bars.ts.iloc[i], abs(bars.mid.iloc[i] - entry) / entry * 100


def h1_stale_price(s: pd.DataFrame, B: dict) -> pd.DataFrame:
    rows = []
    for r in s.itertuples():
        b = B.get(r.symbol)
        if b is None or b.empty:
            continue
        # רק נרות עד רגע הסטאפ: מחיר ישן, לא עתידי
        past = b[b.ts <= r.ts]
        if past.empty:
            continue
        when, err = nearest_moment(r.entry, past)
        live = past.mid.iloc[-1]
        rows.append({
            "ts": r.ts, "symbol": r.symbol, "month": f"{r.ts:%Y-%m}",
            "entry": r.entry, "live": live,
            "dev_pct": (r.entry - live) / live * 100,
            "match_ts": when,
            "lag_days": (r.ts - when).total_seconds() / 86400,
            "match_err_pct": err,
        })
    return pd.DataFrame(rows)


def h3_swapped_symbol(s: pd.DataFrame, B: dict) -> None:
    print("\n" + "=" * 62)
    print("  השערה 3 — סימבול מוחלף")
    print("=" * 62)
    other = {"SPY": "QQQ", "QQQ": "SPY"}
    rows = []
    for r in s.itertuples():
        own, alt = B.get(r.symbol), B.get(other.get(r.symbol, ""))
        if own is None or alt is None or own.empty or alt.empty:
            continue
        o = own[own.ts <= r.ts]
        a = alt[alt.ts <= r.ts]
        if o.empty or a.empty:
            continue
        rows.append({
            "own_pct": abs(r.entry - o.mid.iloc[-1]) / o.mid.iloc[-1] * 100,
            "alt_pct": abs(r.entry - a.mid.iloc[-1]) / a.mid.iloc[-1] * 100,
        })
    d = pd.DataFrame(rows)
    if d.empty:
        print("  אין מספיק נתונים")
        return
    better = (d.alt_pct < d.own_pct).mean() * 100
    print(f"  סטייה חציונית מול הסימבול שנרשם : {d.own_pct.median():6.3f}%")
    print(f"  סטייה חציונית מול הסימבול השני  : {d.alt_pct.median():6.3f}%")
    print(f"  אחוז הסטאפים שמתאימים יותר לשני : {better:5.1f}%")
    print("  -> החלפת סימבול" if better > 70 else "  -> לא החלפת סימבול")


def h4_constant_factor(d: pd.DataFrame) -> None:
    print("\n" + "=" * 62)
    print("  השערה 4 — פקטור קבוע")
    print("=" * 62)
    ratio = d.entry / d.live
    print(f"  יחס entry/אמיתי: חציון {ratio.median():.5f}  "
          f"סטיית תקן {ratio.std():.5f}")
    print(f"  טווח: {ratio.min():.5f} עד {ratio.max():.5f}")
    if ratio.std() < 0.002:
        print(f"  -> פקטור קבוע של {ratio.median():.5f}. לחפש מספר קשיח בקוד.")
    else:
        print("  -> לא פקטור קבוע. היחס נודד.")


# ── הכרעה ────────────────────────────────────────────────────────

FROZEN, CACHE, WRONG_BAR, COMPUTED = "frozen", "cache", "wrong_bar", "computed"

# שגיאת התאמה מתחת לזה = המחיר התקיים בשוק באיזשהו רגע.
#
# אזהרה: עם סדרת נרות צפופה המבחן הזה חלש. 4,680 נרות על טווח של 75
# דולר נותנים מרחק ממוצע של כ-0.002% בין נרות סמוכים, אז כמעט כל מחיר
# בטווח ימצא התאמה "מושלמת" במקרה. שגיאה נמוכה כאן שוללת "מחושב"
# בביטחון נמוך בלבד. המבחן החזק הוא lag_scan.py, שמשווה מול היסט זמן
# אמיתי במקום לחפש חופשי.
REAL_PRICE_TOL = 0.10

# פיזור הפיגור מתחת לזה, כחלק מהחציון, נחשב קבוע. 0.5 היה צר מדי:
# על נתונים אמיתיים פיגור נעול על 15 יום נתן פיזור של 0.503 ונפל לתשובה
# הכללית בשוליים של 0.4%.
CACHE_SPREAD_MAX = 0.65


def classify(match_err_pct, span_days, corr, med_lag, lag_iqr):
    """איזו תקלה מסבירה את הסטייה.

    פיגור קבוע = מטמון עם TTL. פיגור שגדל והרגעים המתאימים מתכנסים
    לתאריך אחד = עוגן קפוא. ההבחנה היא בפיזור הפיגור, לא במתאם שלו:
    מטמון מחזיר בדיוק אותה יישנות כל פעם, והעוגן הוא זה שנופל מאחור.
    """
    if match_err_pct >= REAL_PRICE_TOL:
        return COMPUTED
    if span_days < 10 and corr > 0.7:
        return FROZEN
    if med_lag > 0.5 and lag_iqr < CACHE_SPREAD_MAX * med_lag:
        return CACHE
    return WRONG_BAR


def explain(cause, med_lag, anchor_median):
    if cause == FROZEN:
        return ["\n  -> עוגן קפוא. מחיר ייחוס נקבע פעם אחת ולא עודכן.",
                f"     לחפש בקוד ערך שנקבע סביב {anchor_median:%Y-%m-%d}."]
    if cause == CACHE:
        return [f"\n  -> מטמון עם TTL. המחיר מפגר בקביעות ב-{med_lag:.1f} ימים.",
                "     ה-TTL לא פוקע, או שהרענון נכשל בשקט ונשאר הערך הישן."]
    if cause == WRONG_BAR:
        return ["\n  -> המחירים אמיתיים אבל מזמן אחר, בלי תבנית ברורה.",
                "     באג בבחירת הנר או בחותמת הזמן.",
                "     הרץ את lag_scan.py לפני שמקבלים את זה — המבחן כאן",
                "     חלש כשסדרת הנרות צפופה."]
    return ["\n  -> המחירים האלה לא הופיעו בשוק באף רגע. לא מחיר ישן —",
            "     משהו מחשב אותם. לבדוק את השערות 3 ו-4."]


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
        sys.exit("אין נרות. הרץ קודם את ibbars.py")

    print(f"\nסטאפים בתקופת ה-ETF: {len(s):,}")
    print(f"נרות: {', '.join(f'{k} {len(v):,}' for k, v in B.items())}")

    d = h1_stale_price(s, B)
    if d.empty:
        sys.exit("אין חפיפה בין הסטאפים לנרות")

    print("\n" + "=" * 62)
    print("  השערה 1 — מחיר ישן")
    print("=" * 62)
    print(f"{'חודש':>9} {'n':>5} {'סטייה%':>9} {'פיגור (ימים)':>14} "
          f"{'שגיאת התאמה%':>14}")
    for m, g in d.groupby("month"):
        print(f"{m:>9} {len(g):>5} {g.dev_pct.median():>8.3f}% "
              f"{g.lag_days.median():>14.2f} {g.match_err_pct.median():>13.3f}%")

    lag = d.lag_days
    err = d.match_err_pct
    print(f"\n  פיגור חציוני כולל : {lag.median():.2f} ימים "
          f"(רבעונים {lag.quantile(.25):.2f} / {lag.quantile(.75):.2f})")
    print(f"  שגיאת התאמה חציונית: {err.median():.3f}%")

    drifting = d[d.dev_pct.abs() > 1.0]
    if len(drifting) >= 10:
        anchor = drifting.match_ts
        span_days = (anchor.max() - anchor.min()).total_seconds() / 86400
        corr = float(np.corrcoef(drifting.ts.astype("int64"),
                                 drifting.lag_days)[0, 1])
        q1, q3 = drifting.lag_days.quantile(.25), drifting.lag_days.quantile(.75)
        med_lag = float(drifting.lag_days.median())

        print(f"\n  מבין {len(drifting)} הסטאפים הסוטים (מעל 1%):")
        print(f"    הרגע המתאים נע בין {anchor.min():%Y-%m-%d} ל-{anchor.max():%Y-%m-%d} "
              f"({span_days:.0f} ימים)")
        print(f"    מתאם בין זמן הסטאפ לפיגור: {corr:+.3f}")
        print(f"    פיזור הפיגור: {q1:.2f} עד {q3:.2f} ימים (חציון {med_lag:.2f})")

        cause = classify(float(err.median()), span_days, corr, med_lag,
                         float(q3 - q1))
        for line in explain(cause, med_lag, anchor.median()):
            print(line)

    h3_swapped_symbol(s, B)
    h4_constant_factor(d)

    out = D / "drift_diagnostic.csv"
    d.to_csv(out, index=False)
    print(f"\nנשמר: {out}")


if __name__ == "__main__":
    main()
