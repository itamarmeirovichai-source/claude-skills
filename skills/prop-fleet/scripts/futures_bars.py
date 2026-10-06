#!/usr/bin/env python3
"""
futures_bars.py — נרות חמש דקות של ES ו-NQ לתקופה הנקייה, מ-IBKR.

למה בכלל
--------
מ-18/05 ועד 13/07 יש 131 סטאפים שנרשמו במחיר ששרר (שגיאה 0.107%,
99.2% בתוך חצי אחוז). זו כל הראיה התקפה שקיימת. אבל רק 7 מהן הפכו
לעסקאות סגורות בלי באג הפרוקסי, והתוחלת שלהן היא -0.384R עם רווח
סמך [-1.455, +0.687] — כלומר שום דבר. כדי להגיע לרווח סמך של חצי R
צריך 22 עסקאות, ולזהות יתרון של 0.3R כמובהק צריך 117. בקצב הנוכחי
של חצי עסקה ליום זה חמישה עד עשרה חודשים של המתנה.

הדרך היחידה לקצר את זה היא לשחזר את 131 הסטאפים מול נרות אמיתיים
במקום לחכות. לזה צריך נרות תוך-יומיים של מאי-יולי, ו-yfinance מגביל
אינטראדיי ל-60 יום אחורה. IBKR כן מחזיק אותם.

למה חוזים מתוארכים
------------------
`ContFuture` מסרב ל-endDateTime (שגיאה 10339), ולכן הניסיון הקודם
חזר ריק. חוזה עם חודש פקיעה מפורש לא מסרב. בתקופה הזאת רלוונטיים
חוזה יוני וחוזה ספטמבר.

איך נקבע הגלגול
---------------
לא בתאריך קשיח. הסקריפט מושך את שני החוזים על כל החלון ובוחר לכל יום
את זה שנסחר בו יותר — ההגדרה התפעולית של החוזה הקדמי. תאריך גלגול
מנוחש הוא בדיוק סוג הקירוב שמכניס קפיצת מחיר שקטה לתוך הנתונים.

הבדיקה שבלעדיה אין ערך
----------------------
הסטאפים נרשמו מול הסדרה הרציפה של yfinance, והנרות כאן הם חוזה
ספציפי. בין שני החוזים יש מרווח, אז צריך לוודא שהסדרה המורכבת תואמת
את מה שהבוט ראה. הסקריפט ממיר את נרות החמש דקות לשעתיים ומשווה
לנרות השעתיים של yfinance. חוסר התאמה, ובמיוחד קפיצה סביב הגלגול,
נאמר במפורש במקום להיבלע.

שימוש
-----
    python3 futures_bars.py            (צריך IB Gateway על 4002)
"""

import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

D = Path.home() / "Desktop"
BOT = D / "meirox-ai" / "MeiroX-AI - בוט מסחר"
ET = ZoneInfo("America/New_York")

# החלון הנקי: מהיום שבו הסטאפים עברו לקנה מידה של חוזים, ועד האחרון.
START = date(2026, 5, 18)
END = date(2026, 7, 14)
# שני החוזים הרבעוניים שמכסים את החלון. הבחירה ביניהם לפי מחזור.
MONTHS = ("202606", "202609")
SYMBOLS = ("ES", "NQ")
BAR_SIZE = "5 mins"
# חלון לכל בקשה. חמישה ימים נותנים כ-9 בקשות לכל חוזה-סימבול, 36 סך
# הכל — הרבה מתחת למגבלת הקצב של IBKR (60 בקשות לעשר דקות).
CHUNK_DAYS = 5
THROTTLE_S = 3.0
# סופי שבוע וחגים מחזירים ריק כדין. הסקריפט הקודם עצר על הריק הראשון
# ולכן לא הביא כלום. עוצרים רק אחרי כמה ריקים רצופים.
MAX_EMPTY = 4
PORT = 4002
CLIENT_ID = 77
# מעל פער כזה בין הסדרה המורכבת לסדרה שהבוט ראה, הנתונים אינם
# מתאימים לשחזור והסקריפט אומר זאת.
MAX_DRIFT_PCT = 0.25


def pick_front(frames: dict) -> tuple:
    """לכל יום, החוזה שנסחר בו יותר. מחזיר את הסדרה המורכבת ואת הגלגול.

    זו ההגדרה התפעולית של "החוזה הקדמי", וזו הסיבה שלא מנחשים תאריך:
    הגלגול נקרא מהנתונים עצמם.
    """
    if not frames:
        return pd.DataFrame(), []
    daily = {}
    for month, df in frames.items():
        if df is None or df.empty:
            continue
        v = df.groupby(df.ts.dt.date).volume.sum()
        for d, vol in v.items():
            daily.setdefault(d, {})[month] = float(vol)
    if not daily:
        return pd.DataFrame(), []
    chosen = {d: max(m, key=m.get) for d, m in daily.items()}
    parts = []
    for month, df in frames.items():
        if df is None or df.empty:
            continue
        keep = df.ts.dt.date.map(lambda d: chosen.get(d) == month)
        parts.append(df[keep])
    out = (pd.concat(parts).sort_values("ts").drop_duplicates("ts")
           .reset_index(drop=True) if parts else pd.DataFrame())
    days = sorted(chosen)
    rolls = [(d, chosen[prev], chosen[d])
             for prev, d in zip(days, days[1:]) if chosen[d] != chosen[prev]]
    return out, rolls


def hourly_close(df5: pd.DataFrame) -> pd.Series:
    """נרות חמש דקות לסגירות שעתיות, להשוואה מול הפיד של הבוט."""
    if df5 is None or df5.empty:
        return pd.Series(dtype=float)
    return df5.set_index("ts").resample("1h").close.last().dropna()


def load_reference(symbol: str):
    """הסדרה שהבוט עצמו ניתח. זו נקודת האמת כאן.

    לא "החוזה הקדמי האמיתי" — הרמות בסטאפים חושבו מהסדרה הזאת, ולכן
    היא זו שצריך לשחזר. אם yfinance גלגל מוקדם או מאוחר, זה מה שהבוט
    ראה, וזה מה שהריפליי חייב לראות.
    """
    sys.path.insert(0, str(BOT))
    try:
        from data.feed import MarketDataFeed
    except Exception as e:
        print(f"    אין סדרת ייחוס — data.feed לא נטען: {str(e)[:50]}")
        return None
    ref = MarketDataFeed().get_ohlcv(symbol, "1h")
    if ref is None or ref.empty:
        return None
    return ref["Close"]


def daily_error(frames: dict, ref) -> pd.DataFrame:
    """שגיאה חציונית יומית של כל חוזה מול סדרת הייחוס."""
    cols = {}
    for month, df in frames.items():
        h = hourly_close(df)
        if h.empty:
            continue
        j = pd.DataFrame({"mine": h}).join(pd.DataFrame({"ref": ref}), how="inner").dropna()
        if j.empty:
            continue
        err = (j.mine - j.ref).abs()
        cols[month] = err.groupby(err.index.date).median()
    return pd.DataFrame(cols).dropna(how="all")


def choose_by_error(err: pd.DataFrame, order) -> tuple:
    """לכל יום, החוזה שהכי מתאים לייחוס. מחזיר בחירה, מעברים ואזהרה.

    הגלגול הוא אירוע חד־פעמי: פעם אחת עוברים מהחוזה הקרוב לרחוק ולא
    חוזרים. אם הבחירה מקפצת הלוך ושוב, ההתאמה לא זיהתה שום דבר
    אמיתי והיא לא ראויה לאמון — זה נאמר במפורש במקום להשתיק.
    """
    if err.empty:
        return {}, [], "אין חפיפה מול סדרת הייחוס"
    rank = {m: i for i, m in enumerate(order)}
    chosen = {d: min(row.dropna().index, key=lambda m: row[m])
              for d, row in err.iterrows() if row.notna().any()}
    days = sorted(chosen)
    switches = [(d, chosen[a], chosen[d])
                for a, d in zip(days, days[1:]) if chosen[d] != chosen[a]]
    warn = ""
    if len(switches) > 1:
        warn = f"{len(switches)} מעברים — הבחירה מקפצת, לא לסמוך עליה"
    elif switches and rank.get(switches[0][2], 0) < rank.get(switches[0][1], 0):
        warn = "המעבר הוא מהחוזה הרחוק לקרוב — הפוך מגלגול"
    return chosen, switches, warn


def fill_choice(chosen: dict, all_days) -> dict:
    """משלים ימים שלא הייתה להם סדרת ייחוס, בגרירה קדימה.

    יום חג או יום שבו yfinance חסר נופל מטבלת השגיאות, ובלי זה הוא
    נופל גם מהסדרה — שקט, בלי ששום שורה תגיד שהוא נעלם. הגלגול
    מונוטוני, ולכן הבחירה של היום הקודם היא התשובה הנכונה עבורו.
    """
    if not chosen:
        return {}
    out, last = {}, None
    first = chosen[min(chosen)]
    for d in sorted(all_days):
        if d in chosen:
            last = chosen[d]
        out[d] = last if last is not None else first
    return out


def stitch(frames: dict, chosen: dict) -> pd.DataFrame:
    """מרכיב סדרה אחת לפי הבחירה היומית."""
    parts = []
    for d, month in chosen.items():
        df = frames.get(month)
        if df is None or df.empty:
            continue
        parts.append(df[df.ts.dt.date == d])
    if not parts:
        return pd.DataFrame()
    return (pd.concat(parts).sort_values("ts")
            .drop_duplicates("ts").reset_index(drop=True))


def daily_offset(df5: pd.DataFrame, ref) -> pd.DataFrame:
    """היסט יומי בנקודות בין הסדרה שנשלפה לסדרה שהבוט ניתח.

    למה בכלל. IBKR מזהה את חוזה יוני עם includeExpired אבל אין לו
    עליו נתונים היסטוריים — "HMDS query returned no data". אז החוזה
    שממנו חושבו הרמות במאי פשוט לא ניתן לשליפה, ומה שיש הוא ספטמבר,
    שגבוה ממנו ב-60 נקודות ב-ES וב-279 ב-NQ.

    ההפרש הזה הוא carry, והוא נמדד: הסדרה השעתית של הבוט למאי היא
    חוזה יוני. מחסרים אותו, ומקבלים סדרה בקנה מידה של יוני עם המסלול
    התוך-יומי של ספטמבר. שני החוזים זזים כמעט זהה, וכמה בדיוק —
    זה מה שהשארית אחרי ההתאמה מודדת.
    """
    h = hourly_close(df5)
    if h.empty or ref is None:
        return pd.DataFrame()
    j = pd.DataFrame({"mine": h}).join(pd.DataFrame({"ref": ref}),
                                       how="inner").dropna()
    if j.empty:
        return pd.DataFrame()
    d = j.mine - j.ref
    g = d.groupby(d.index.date)
    return pd.DataFrame({"offset": g.median(), "spread": g.std(), "n": g.size()})


def lagged_offset(off: pd.DataFrame) -> dict:
    """ההיסט של יום המסחר הקודם, לשימוש היום.

    להשתמש בהיסט של היום עצמו זה להסתכל על סגירות שעדיין לא קרו
    ברגע המילוי. ה-carry הוא פונקציה של הזמן לפקיעה ושל הריבית, והוא
    זז לאט — אתמול הוא אומדן טוב להיום, ובלי שום הצצה קדימה.
    """
    if off.empty:
        return {}
    days = list(off.index)
    out = {days[0]: float(off.offset.iloc[0])}
    for prev, d in zip(days, days[1:]):
        out[d] = float(off.offset.loc[prev])
    return out


def apply_offset(df5: pd.DataFrame, per_day: dict) -> pd.DataFrame:
    """מחסר את ההיסט מכל נר. יום בלי היסט נשאר כמו שהוא."""
    if df5.empty or not per_day:
        return df5
    out = df5.copy()
    shift = out.ts.dt.date.map(per_day).astype(float).fillna(0.0)
    for c in ("open", "high", "low", "close"):
        out[c] = out[c] - shift
    return out


def to_frame(bars) -> pd.DataFrame:
    """נרות של IBKR לטבלה, עם אזור זמן שנשמר."""
    if not bars:
        return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])
    rows = [{
        "ts": b.date, "open": float(b.open), "high": float(b.high),
        "low": float(b.low), "close": float(b.close),
        "volume": float(getattr(b, "volume", 0) or 0),
    } for b in bars]
    df = pd.DataFrame(rows)
    df["ts"] = pd.to_datetime(df.ts, utc=True).dt.tz_convert(ET)
    return df.sort_values("ts").drop_duplicates("ts").reset_index(drop=True)


def pull(ib, contract, start: date, end: date) -> list:
    """הולך אחורה בחלונות, בלי לעצור על ריק בודד."""
    out, empties = [], 0
    cursor = datetime.combine(end, datetime.min.time()).replace(tzinfo=ET)
    floor = datetime.combine(start, datetime.min.time()).replace(tzinfo=ET)
    while cursor > floor and empties < MAX_EMPTY:
        try:
            bars = ib.reqHistoricalData(
                contract, endDateTime=cursor,
                durationStr=f"{CHUNK_DAYS} D", barSizeSetting=BAR_SIZE,
                whatToShow="TRADES", useRTH=False, formatDate=2)
        except Exception as e:
            print(f"      {cursor:%Y-%m-%d}: {str(e)[:60]}")
            bars = []
        if bars:
            out.extend(bars)
            empties = 0
            print(f"      {cursor:%Y-%m-%d}: {len(bars):,}")
        else:
            empties += 1
        cursor -= timedelta(days=CHUNK_DAYS)
        time.sleep(THROTTLE_S)
    return out


def validate(df5: pd.DataFrame, symbol: str) -> float:
    """האם הסדרה המורכבת היא מה שהבוט ראה. מחזיר פער חציוני באחוזים."""
    if df5.empty:
        return float("nan")
    sys.path.insert(0, str(BOT))
    try:
        from data.feed import MarketDataFeed
    except Exception as e:
        print(f"    אין בקרה — data.feed לא נטען: {str(e)[:50]}")
        return float("nan")
    ref = MarketDataFeed().get_ohlcv(symbol, "1h")
    if ref is None or ref.empty:
        return float("nan")
    mine = (df5.set_index("ts").resample("1h")
            .agg({"close": "last"}).dropna())
    r = pd.DataFrame({"ref": ref["Close"]})
    j = mine.join(r, how="inner").dropna()
    if j.empty:
        return float("nan")
    return float((100 * (j.close - j.ref).abs() / j.ref).median())


def main() -> None:
    try:
        import asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())
    except Exception:
        pass
    try:
        from ib_async import IB, Future
    except ImportError:
        try:
            from ib_insync import IB, Future
        except ImportError:
            sys.exit("צריך ib_async או ib_insync בסביבה של הבוט")

    # ברירת המחדל היא לשלוף מחדש. הקובץ שנוצר לפני התיקון נראה תקין
    # לגמרי ואין בו שום סימן לכך שמאי הגיע מהחוזה הלא נכון; דילוג
    # שקט עליו היה משאיר את השגיאה בדיוק במקום.
    keep = "--keep" in sys.argv

    ib = IB()
    try:
        ib.connect("127.0.0.1", PORT, clientId=CLIENT_ID, timeout=20)
    except Exception as e:
        sys.exit(f"אין חיבור ל-IB Gateway על {PORT}: {str(e)[:80]}")
    print(f"מחובר. מושך {START} עד {END}\n")

    for sym in SYMBOLS:
        out = D / f"{sym}_5min_clean.csv"
        if out.exists() and keep:
            print(f"{sym}: קיים כבר — מדלג")
            continue
        frames = {}
        for month in MONTHS:
            # חוזה יוני 2026 כבר פג. בלי הדגל הזה IBKR מחזיר
            # "No security definition" והכל נשלף מספטמבר — וזה בדיוק
            # מה שהזיז את מאי ב-60 נקודות ב-ES וב-279 ב-NQ.
            c = Future(sym, month, "CME", includeExpired=True)
            try:
                ib.qualifyContracts(c)
            except Exception as e:
                print(f"  {sym} {month}: לא זוהה — {str(e)[:60]}")
                continue
            print(f"  {sym} {month}:")
            frames[month] = to_frame(pull(ib, c, START, END))

        # הבחירה נעשית מול הסדרה שהבוט ניתח, לא לפי מחזור. המחזור
        # אומר מי החוזה הקדמי האמיתי; אנחנו צריכים את החוזה שממנו
        # חושבו הרמות, ואלה שני דברים שונים כשהפיד מגלגל בתאריך אחר.
        ref = load_reference(sym)
        rolls, how = [], "מחזור"
        if ref is not None:
            err = daily_error(frames, ref)
            chosen, rolls, warn = choose_by_error(err, MONTHS)
            if warn:
                print(f"    התאמה מול הייחוס נכשלה: {warn} — נופל למחזור")
            else:
                days = sorted({d for f in frames.values() if f is not None
                               and not f.empty for d in f.ts.dt.date.unique()})
                filled = fill_choice(chosen, days)
                gaps = len(filled) - len(chosen)
                if gaps:
                    print(f"    {gaps} ימים בלי סדרת ייחוס — נגררו מהיום הקודם")
                df, how = stitch(frames, filled), "התאמה לייחוס"
        if how == "מחזור":
            df, rolls = pick_front(frames)
        if df.empty:
            print(f"{sym}: אין נתונים\n")
            continue
        lo = pd.Timestamp(START, tz=ET)
        hi = pd.Timestamp(END, tz=ET)
        df = df[(df.ts >= lo) & (df.ts < hi)].reset_index(drop=True)
        print(f"    הרכבה לפי {how}")
        for d, a, b in rolls:
            print(f"    גלגול {d}: {a} -> {b}")

        # תיקון קנה המידה. אם החוזה שממנו חושבו הרמות אינו זמין,
        # ההפרש נמדד מול הסדרה שהבוט ניתח ומוסר. יום שכבר תואם
        # מקבל היסט אפס, כלומר זה לא נוגע ביוני וביולי.
        if ref is not None:
            off = daily_offset(df, ref)
            if not off.empty:
                big = off[off.offset.abs() > 1.0]
                if not big.empty:
                    print(f"    תיקון carry על {len(big)} ימים: "
                          f"חציון {big.offset.median():+.2f} נקודות, "
                          f"פיזור תוך-יומי {big.spread.median():.2f}")
                    df = apply_offset(df, lagged_offset(off))
                    after = daily_offset(df, ref)
                    if not after.empty:
                        left = after.loc[big.index.intersection(after.index)]
                        if not left.empty:
                            print(f"    שארית אחרי התיקון: "
                                  f"{left.offset.abs().median():.2f} נקודות")

        drift = validate(df, sym)
        mark = "" if not np.isfinite(drift) else (
            "  ✓" if drift <= MAX_DRIFT_PCT else "  ✗ גדול מדי")
        print(f"    פער מול הסדרה שהבוט ראה: "
              f"{'לא נבדק' if not np.isfinite(drift) else f'{drift:.3f}%'}{mark}")
        if np.isfinite(drift) and drift > MAX_DRIFT_PCT:
            print("    הנרות אינם תואמים את מה שנרשם. לא לשחזר עליהם")
            print("    בלי להבין קודם למה.")

        df[["ts", "open", "high", "low", "close", "volume"]].rename(
            columns={"ts": "timestamp"}).to_csv(out, index=False)
        print(f"  {sym}: {len(df):,} נרות  "
              f"{df.ts.iloc[0]:%Y-%m-%d} עד {df.ts.iloc[-1]:%Y-%m-%d}  ->  {out}\n")

    ib.disconnect()
    print("סיימתי.")


if __name__ == "__main__":
    main()
