#!/usr/bin/env python3
"""
replay.py — התוחלת האמיתית של האסטרטגיה, מתוך 131 הסטאפים התקפים.

למה בכלל
--------
יש שבע עסקאות סגורות תקפות. הממוצע שלהן -0.384R, ורווח הסמך
[-1.455, +0.687]. זה לא אומר כלום: גם אסטרטגיה מצוינת וגם אסטרטגיה
הרסנית יושבות בתוך הקטע הזה. כדי לצמצם אותו לחצי R צריך 22 עסקאות,
וכדי לקבוע שיתרון של +0.3R אמיתי צריך 117. בקצב של חצי עסקה ביום זה
חמישה עד עשרה חודשים של המתנה.

הסטאפים הם מקור ראיות רחב הרבה יותר. מ-18/05 ואילך 131 מהם נקיים —
0.107% שגיאה בפיגור אפס, 99.2% בתוך חצי אחוז, בלי שום שוקת. מה שחסר
הוא לא עוד זמן אלא ביצוע: מה היה קורה לכל סטאפ אילו נשלחה עליו פקודה.

מה הסקריפט לא עושה
------------------
הוא לא נוגע באסטרטגיה. הוא לא מדרג, לא מסנן לפי ציון, לא בוחר
kill zones ולא משנה סף. הוא לוקח את הסטאפים כפי שהם נרשמו ומריץ
עליהם ביצוע. אם התוחלת יוצאת שלילית, המסקנה היא פחות חשיפה — לא
אסטרטגיה מכוילת מחדש.

סמנטיקת הביצוע, ואיפה קבורים הבאגים
-----------------------------------
כל שורה כאן היא החלטה שאפשר לטעות בה לטובת עצמך:

  כניסה   לימיט ברמה. מתמלא כשטווח הנר מכיל את הרמה. מחיר המילוי
          הוא min(open, level) בלונג — אם הנר נפתח מתחת ללימיט,
          מקבלים את הפתיחה, שהיא טובה יותר. זו התנהגות אמיתית של
          לימיט, לא מתנה.
  סטופ    אם הנר נפתח מעבר לסטופ, היציאה בפתיחה ולא בסטופ. בקטסט
          שמניח יציאה בסטופ תמיד מדווח הפסדים קטנים מדי.
  שני     נר שמכיל גם סטופ וגם יעד — אין דרך לדעת מה קדם ברזולוציה
  הצדדים  של חמש דקות. ברירת המחדל היא הסטופ, והסקריפט סופר כמה
          פעמים זה קרה ומדווח גם את התוצאה ההפוכה. אם שתי ההכרעות
          נותנות תשובות שונות מהותית — הבקטסט לא הכריע, וזה מה
          שייכתב.
  סיכון   |רמת הכניסה - סטופ|, לא |מילוי בפועל - סטופ|. ככה הבוט
          מחשב גודל, ולכן החלקה בכניסה מופיעה מעצמה בתוך ה-R.
  סוף יום סגירה בנר האחרון של המושב. סטאפ שלא התמלא עד הסגירה
          נספר כ"לא התמלא" ולא כאפס — ממוצע שמערבב את השניים משקר.

עלויות
------
עמלה 1.30$ הלוך-חזור לחוזה ורבע נקודה החלקה, אותם מספרים כמו
ב-apex_model.py. שתיהן לחוזה, והסיכון גם הוא לחוזה — לכן הגודל
מצטמצם והעלות ב-R אינה תלויה בכמות. על MES רבע נקודה ועוד 0.26
נקודה עמלה הן 0.51 נקודה; מול סטופ טיפוסי של 8.5 נקודות זה 6%
מכל R. ההחלקה מוחלת על כל עסקה, כולל יציאה ביעד שהיא לימיט ולא
באמת מחליקה — כלומר ההערכה שמרנית.

שימוש
-----
    python3 replay.py
    python3 replay.py '/נתיב/לתיקיית/הבוט'

מצפה ל-~/Desktop/setups.csv ול-~/Desktop/ES_5min_clean.csv,
~/Desktop/NQ_5min_clean.csv — הפלט של futures_bars.py.
"""

import sys
from datetime import time as dtime
from pathlib import Path

import numpy as np
import pandas as pd

D = Path.home() / "Desktop"
ET = "America/New_York"

# החלון הנקי, כפי ש-futures_era_check.py קבע אותו.
BOT_DEFAULT = D / "meirox-ai" / "MeiroX-AI - בוט מסחר"

CLEAN_START = pd.Timestamp("2026-05-18", tz=ET)
CLEAN_END = pd.Timestamp("2026-07-14", tz=ET)

# מיקרו-חוזים, כי זה מה שחשבון 50K יכול לשאת. ערך נקודה בדולרים.
POINT_VALUE = {"ES": 5.0, "NQ": 2.0}
COMM_RT = 1.30          # דולר, הלוך-חזור, לחוזה
SLIP_PTS = 0.25         # נקודה, הלוך-חזור

# חלון המסחר. הבוט שולח פקודות בשעות המסחר הרגילות, ו-eod_force_close
# רץ אצלו ב-15:58. בלי החלון הזה הריפליי משאיר לימיט פתוח עד 23:55,
# ממלא אותו במסחר הערב שבו הסטאפ כבר חסר משמעות, וסוגר בסוף היום
# הקלנדרי במקום בסגירה. שתי הטעויות נוטות לכיוון אחד: יותר מילויים
# ויציאה במחיר שאיש לא היה מקבל.
SESSION_OPEN = dtime(9, 30)
SESSION_FLAT = dtime(15, 58)
BAR_MINUTES = 5

# ורק שהחלון עצמו היה שגוי. נר מתויג בתחילתו, ולכן `ts < 15:58`
# מכניס את הנר של 15:55 — שנסגר ב-16:00. משם נבעו שתי טעויות
# שוב באותו כיוון:
#
#   היציאה בסוף היום נלקחה מהסגירה של אותו נר, כלומר ממחיר של
#   16:00. הבוט כבר שטוח ב-15:58. אלה שתי דקות מסחר שהריפליי
#   זוכה או נחסך בהן במחיר שהחשבון האמיתי לא יכול היה לקבל.
#
#   וגרוע מזה, לימיט יכול היה להתמלא בתוך אותו נר, כלומר להיכנס
#   לפוזיציה אחרי שהבוט כבר סגר הכול. פוזיציה שלא הייתה קיימת.
#
# ברזולוציה של חמש דקות אי אפשר לראות את המחיר ב-15:58. הנר האחרון
# שנסגר לפני ההשטחה הוא זה שמתחיל ב-15:50 ונסגר ב-15:55, והמחיר
# ההוא הוא הדבר האחרון שנצפה בוודאות לפני שהבוט יוצא. זה מקצר כל
# פוזיציה בחמש דקות ומוחק מילויים מאוחרים — כלומר זה מוריד עסקאות
# ולא מוסיף. זה הכיוון הנכון לטעות בו.
_flat_min = SESSION_FLAT.hour * 60 + SESSION_FLAT.minute
_last_start = (_flat_min - BAR_MINUTES) // BAR_MINUTES * BAR_MINUTES
LAST_BAR_START = dtime(_last_start // 60, _last_start % 60)

# סטופ קטן מזה הוא כנראה שגיאת רישום ולא רמה אמיתית.
MIN_RISK_PTS = 0.5
# מתחת לזה אין מה לדבר על רווח סמך.
MIN_TRADES = 10
# רשת ה-RR לבדיקת רגישות ליעד.
RR_GRID = (1.0, 1.5, 2.0, 2.5, 3.0)

# גרירת הסטופ. שני המספרים האלה הם פרמטרים של הבוט ולא של הריפליי,
# והם לא אומתו מול broker/ibkr.py. כל מה שמודפס בסעיף הגרירה תלוי
# בהם: טריגר שגוי מזיז את כל התוצאה. לכן הם מוצהרים כאן בשמם, נבדקים
# ברשת רגישות, ולא מוזרמים לחישוב הדולרים.
TRAIL_TRIGGER_R = 1.0       # ברווח כזה הסטופ זז
TRAIL_TO_R = 0.0            # לאן הוא זז. 0.0 = נקודת האיזון
TRAIL_GRID = (0.5, 0.75, 1.0, 1.5, 2.0)

STOP_NAMES = ("stop_loss", "stop", "sl", "stoploss", "stop_price")
TP_NAMES = ("take_profit", "tp", "target", "tp1", "take_profit_1", "tp_price")


def pick_column(df: pd.DataFrame, names) -> str | None:
    """השם הראשון שקיים בפועל, בהתעלם מרישיות ורווחים."""
    low = {c.strip().lower(): c for c in df.columns}
    for n in names:
        if n in low:
            return low[n]
    return None


def load_bars_5m(symbol: str) -> pd.DataFrame:
    p = D / f"{symbol}_5min_clean.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    df["ts"] = pd.to_datetime(df.timestamp, errors="coerce", utc=True,
                              format="mixed").dt.tz_convert(ET)
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["ts", "open", "high", "low", "close"])
    df = df.sort_values("ts").drop_duplicates("ts").reset_index(drop=True)
    df["session"] = df.ts.dt.date
    return df


def load_clean_setups(path: Path) -> pd.DataFrame:
    """רק העידן שהוכח נקי, ורק בקנה מידה של חוזים."""
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
    return s[(s.entry >= 2000) & (s.ts >= CLEAN_START)
             & (s.ts < CLEAN_END)].reset_index(drop=True)


def walk(bars: pd.DataFrame, direction: str, entry: float, stop: float,
         tp: float | None, t0: pd.Timestamp, pessimistic: bool = True,
         trail_trigger: float | None = None, trail_to: float = 0.0) -> dict:
    """מה קרה לסטאפ אחד. bars הם כל נרות המושב, t0 רגע היצירה.

    נר מתויג בתחילתו, ולכן נר שזמנו לפני t0 מכסה גם רגעים שקדמו
    לסטאפ. הוא נזרק. רק נר שמתחיל ב-t0 או אחריו הוא עתיד מלא.
    """
    long = direction == "long"
    fut = bars[bars.ts >= t0]
    if fut.empty:
        return {"status": "no_bars"}

    o = fut.open.values
    h = fut.high.values
    lo = fut.low.values
    c = fut.close.values
    # לא .values. על סדרה מודעת לאזור זמן זה ממיר ל-UTC ומפיל את
    # הסימון, והחותמות היו נכתבות ל-CSV כאילו הן מקומיות. אותה
    # מלכודת שהפילה קודם את בניית הסטאפים, הפעם בצד הפלט.
    ts = fut.ts.reset_index(drop=True)

    fill_i, fill_px = -1, np.nan
    for i in range(len(fut)):
        touched = lo[i] <= entry if long else h[i] >= entry
        if touched:
            # לימיט לא מחליק לרעה. אם הנר נפתח מעבר לרמה, מקבלים
            # את הפתיחה הטובה יותר.
            fill_px = min(o[i], entry) if long else max(o[i], entry)
            fill_i = i
            break
    if fill_i < 0:
        return {"status": "no_fill"}

    risk = abs(entry - stop)
    ambiguous = False
    exit_px, exit_i, reason = float(c[-1]), len(fut) - 1, "eod"
    # הסטופ הפעיל. הוא זז רק בגרירה, והמכנה של R נשאר תמיד הסיכון
    # המתוכנן המקורי — אחרת ברגע שהסטופ מגיע לנקודת האיזון המכנה
    # מתאפס ו-R מפסיק להיות מוגדר. זה בדיוק ה-zero_risk שהבוט עצמו
    # נתקל בו אחרי גרירה, והסיבה שבפועל הוא גורר פעם אחת ולא יותר.
    cur_stop, trailed = stop, False

    # פער שעבר גם את הרמה וגם את הסטופ באותו רגע. הלימיט והסטופ שניהם
    # חיים, ולכן בפועל נכנסים ויוצאים כמעט באותו מחיר — כמעט אפס. זה
    # נכון, אבל זה גם הדרך השקטה שבה בקטסט מוחק הפסדים: כל פער כזה
    # מחליף הפסד מלא בשריטה. לכן הוא מסומן ונספר בנפרד, ולא נבלע
    # בתוך הממוצע בלי שיראו אותו.
    gapped = (o[fill_i] <= stop) if long else (o[fill_i] >= stop)

    for i in range(fill_i, len(fut)):
        hit_stop = lo[i] <= cur_stop if long else h[i] >= cur_stop
        hit_tp = False
        if tp is not None:
            hit_tp = h[i] >= tp if long else lo[i] <= tp
        if i == fill_i and hit_tp and fill_px != o[i]:
            # נר המילוי, והמילוי היה באמצעו. הגבוה של הנר יכול היה
            # להיווצר לפני הכניסה, ואז זו פסגה שלא הייתי בתוכה.
            # היא נספרת רק אם הסגירה עצמה מעבר ליעד — אז המחיר בוודאות
            # היה שם אחרי המילוי, והלימיט היה מתמלא. אחרת ממשיכים.
            # הסטופ, לעומת זאת, נספר תמיד: להניח שהשפל קדם לכניסה זה
            # להניח לטובתי.
            sure = (c[i] >= tp) if long else (c[i] <= tp)
            hit_tp = bool(sure)
        if hit_stop and hit_tp:
            ambiguous = True
            hit_tp = not pessimistic
            hit_stop = pessimistic
        if hit_stop:
            # סטופ הוא פקודת שוק ברגע ההפעלה. פער פתיחה מעבר לרמה
            # מבוצע בפתיחה, גרוע יותר.
            exit_px = min(o[i], cur_stop) if long else max(o[i], cur_stop)
            exit_i = i
            if gapped and i == fill_i:
                reason = "gap_scratch"
            else:
                reason = "trail" if trailed else "stop"
            break
        if hit_tp:
            exit_px = max(o[i], tp) if long else min(o[i], tp)
            exit_i, reason = i, "tp"
            break

        # נקודת דגימה, בסגירת הנר.
        #
        # זה הפרט שמחליט אם המספר הזה אומר משהו. הבוט לא רואה את
        # הנר. הוא מתעורר כל 300 שניות, קורא את המחיר האחרון החי,
        # ומחשב ממנו pnl_r. תנועה שנגעה בטריגר בין סריקה לסריקה
        # וחזרה — לא קיימת מבחינתו, והגרירה לא נורתה. ריפליי שבודק
        # את ה-high של החלון היה גורר בכל אחת מהתנועות האלה, מעביר
        # הפסדים לנקודת איזון בחינם, ומחזיר תוחלת שהחשבון האמיתי
        # לעולם לא יראה. זו אותה משפחה של טעות כמו ה-look-ahead בנר
        # המילוי, רק שכאן היא נכנסת דרך הצד שאמור להגן.
        #
        # נר של חמש דקות הוא בדיוק מרווח הסריקה, וסגירתו היא המחיר
        # באותו רגע. רשת הסריקה של הבוט לא בהכרח מיושרת לגבולות
        # הנרות ויכולה ליפול גם באמצעם, כלומר ייתכנו עוד הזדמנויות
        # גרירה שלא נספרות כאן. ההטיה היא לכיוון הזהיר.
        if trail_trigger is not None:
            px = c[i]
            r_now = (px - entry) / risk if long else (entry - px) / risk
            if r_now >= trail_trigger:
                nxt = (entry + trail_to * risk if long
                       else entry - trail_to * risk)
                if (nxt > cur_stop) if long else (nxt < cur_stop):
                    # נכנס לתוקף מהנר הבא. ההחלטה נופלת בסגירה, ולכן
                    # היא לא יכולה לסגור את הנר שיצר אותה.
                    cur_stop, trailed = nxt, True

    move = (exit_px - fill_px) if long else (fill_px - exit_px)
    seg = slice(fill_i, exit_i + 1)
    if long:
        mfe = (float(h[seg].max()) - fill_px) / risk
        mae = (float(lo[seg].min()) - fill_px) / risk
    else:
        mfe = (fill_px - float(lo[seg].min())) / risk
        mae = (fill_px - float(h[seg].max())) / risk

    return {
        "status": "filled", "reason": reason, "risk_pts": risk,
        "fill_px": fill_px, "exit_px": exit_px, "raw_R": move / risk,
        "mfe_R": mfe, "mae_R": mae, "ambiguous": ambiguous,
        "gapped": bool(gapped), "trailed": bool(trailed),
        "final_stop": float(cur_stop),
        "fill_ts": ts.iloc[fill_i], "exit_ts": ts.iloc[exit_i],
        "bars_held": exit_i - fill_i + 1,
    }


def contract_drift(bars: dict, bot: Path) -> pd.DataFrame:
    """פער חודשי בין הנרות שנשלפו לבין הסדרה שהבוט ראה.

    למה זה חשוב דווקא כאן. IBKR לא החזיר את חוזה יוני 2026 — הוא כבר
    פג ונמחק — ולכן כל החלון נשלף מחוזה ספטמבר. אבל עד הגלגול באמצע
    יוני, הבוט ניתח את חוזה יוני. שני החוזים אינם מחיר אחד: מפריד
    ביניהם ה-carry, כמה נקודות ב-ES.

    כמה נקודות נשמע כלום עד שמחלקים בסטופ. שתי נקודות מול סטופ של 8.5
    הן רבע R של הזזה שיטתית בכיוון אחד, והתוחלת שנמדדת כאן היא בסדר
    גודל של 0.2R. לכן הפער נמדד לפי חודש ולא כחציון אחד על כל החלון:
    חציון כולל מדלל את התקופה שלפני הגלגול בתקופה שאחריה, שבה שני
    המקורות מדברים על אותו חוזה בדיוק ונותנים אפס.
    """
    sys.path.insert(0, str(bot))
    try:
        from data.feed import MarketDataFeed
    except Exception as e:
        print(f"  אין בקרת חוזה — data.feed לא נטען: {str(e)[:50]}")
        return pd.DataFrame()
    feed = MarketDataFeed()
    rows = []
    for sym, b in bars.items():
        ref = feed.get_ohlcv(sym, "1h")
        if ref is None or ref.empty:
            continue
        mine = b.set_index("ts").resample("1h").agg({"close": "last"}).dropna()
        j = mine.join(pd.DataFrame({"ref": ref["Close"]}), how="inner").dropna()
        if j.empty:
            continue
        j["signed"] = j.close - j.ref
        # to_period מפיל אזור זמן ומרעיש אזהרה. חודש כמחרוזת נאמן
        # לאותו דבר בלי לגעת באינדקס.
        for month, g in j.groupby(j.index.strftime("%Y-%m")):
            rows.append({
                "symbol": sym, "month": str(month), "n": len(g),
                "drift_pct": float((100 * g.signed.abs() / g.ref).median()),
                "signed_pts": float(g.signed.median()),
            })
    return pd.DataFrame(rows)


def report_drift(d: pd.DataFrame, res: pd.DataFrame) -> None:
    """מדפיס את הפער ומתרגם אותו ליחידות R, שזו היחידה שמחליטה."""
    if d.empty:
        return
    risk = res[res.status == "filled"].risk_pts
    typical = float(risk.median()) if len(risk) else float("nan")
    print(f"\n{'=' * 58}\n  בקרת חוזה — מול הסדרה שהבוט ניתח\n{'=' * 58}")
    print(f"{'סימבול':>8} {'חודש':>9} {'n':>6} {'פער':>9} {'נקודות':>9} {'ב-R':>8}")
    worst = 0.0
    for r in d.itertuples():
        in_r = abs(r.signed_pts) / typical if typical == typical and typical else float("nan")
        worst = max(worst, 0.0 if in_r != in_r else in_r)
        print(f"{r.symbol:>8} {r.month:>9} {r.n:>6} {r.drift_pct:>8.3f}% "
              f"{r.signed_pts:>+9.2f} {in_r:>8.2f}")
    print(f"\n  סטופ טיפוסי: {typical:.2f} נקודות.")
    if worst >= 1.0:
        print(f"  הזזה שיטתית של {worst:.2f}R בכיוון אחד לכל אורך החודש.")
        print("  זה לא רעש — זה מזיז כל רמה באותו כיוון, ותוחלת בסדר")
        print("  גודל של 0.2R לא שורדת דבר כזה. המספר לא תקף.")
    elif worst >= 0.05:
        # כאן לא ניתן לדעת מהקובץ אם זה פער חוזה שלא תוקן או השארית
        # שנשארה אחרי תיקון, ולכן זה לא נטען. המספר עצמו הוא מה
        # שחשוב: הזזה בכיוון אחד שקובעת כמה אפשר לסמוך על התוצאה.
        print(f"  נותרה הזזה של {worst:.2f}R בכיוון אחד. זו רצפת")
        print("  אי-הוודאות על החודשים האלה — בין אם זה פער חוזה שלא")
        print("  תוקן ובין אם זו השארית של תיקון, היא מזיזה כל רמה.")
    else:
        print(f"  ההזזה הגרועה ביותר {worst:.2f}R — קטנה מספיק כדי להתעלם.")


def cost_R(symbol: str, risk_pts: float) -> float:
    """עלות עסקה ביחידות R. הכמות מצטמצמת — שתיהן לחוזה."""
    pt = POINT_VALUE.get(symbol, 5.0)
    return (SLIP_PTS + COMM_RT / pt) / risk_pts


def interval(x: np.ndarray) -> tuple:
    """ממוצע ורווח סמך 95%. אותה אריתמטיקה כמו ב-gate.py."""
    n = len(x)
    if n < 2:
        return float(x.mean()) if n else float("nan"), float("nan"), float("nan")
    m, sd = float(x.mean()), float(x.std(ddof=1))
    half = 1.96 * sd / np.sqrt(n)
    return m, m - half, m + half


def clustered_interval(r: np.ndarray, day) -> tuple:
    """רווח סמך שמקבץ לפי יום מסחר, סביב ממוצע העסקאות.

    ארבע עסקאות באותו יום על אותו מכשיר אינן ארבע תצפיות. הן חופפות
    בזמן ורוכבות על אותה תנועה, ולכן רווח סמך שמניח n עצמאיים יוצא
    צר מדי — אותה משפחת טעות כמו חציון על אוכלוסייה מתכווצת.

    הגרסה הראשונה כאן מיצעה קודם בתוך היום ולקחה את הרווח סביב ממוצע
    הימים, אבל הדפיסה את ממוצע העסקאות כנקודת האומדן. כשלימים יש
    מספר עסקאות שונה השניים אינם שווים, ואז יצא רווח סמך שלא מכיל
    את האומדן שלו עצמו במרכזו: +0.172R עם רווח [-0.061, +0.830].
    זה לא חוסר דיוק אלא חוסר עקביות — שני גדלים שונים באותה שורה.

    כאן במקום זה נעשה חישוב שגיאה עמיד-לאשכולות סביב ממוצע העסקאות
    עצמו: סוכמים את השאריות בתוך כל יום, ומרובעי הסכומים האלה בונים
    את השונות. כשבכל יום יש עסקה אחת זה מצטמצם בדיוק ל-sd/sqrt(n)
    הרגיל, וככל שהעסקאות בתוך יום נעות יחד הרווח נפתח.
    """
    d = pd.Series(day).values
    df = pd.DataFrame({"r": np.asarray(r, dtype=float), "d": d})
    n = len(df)
    g = df.groupby("d").r
    k = g.ngroups
    if n < 2 or k < 2:
        return float(df.r.mean()) if n else float("nan"), float("nan"), float("nan"), k
    m = float(df.r.mean())
    sums = g.apply(lambda x: float((x - m).sum())).values
    var = (k / (k - 1.0)) * float(np.sum(sums ** 2)) / (n ** 2)
    half = 1.96 * np.sqrt(var)
    return m, m - half, m + half, k


def regime_of(day: pd.DataFrame) -> dict:
    """מאפייני המושב שבו העסקה קרתה. משטר, לא תוצאה.

    שניהם מחושבים על כל נרות המושב — כולל אלה שאחרי העסקה. זו לא
    דליפה מהעתיד לצורך החלטה, כי אף אחד לא מציע לסחור לפי זה בזמן
    אמת; זו תווית משטר למחקר בדיעבד. מי שירצה להפוך את זה לכלל
    חייב לחשב אותו מנתוני בוקר בלבד, ואז זו השערה אחרת.

    יחס היעילות: כמה מהתנועה הגולמית הפכה לתנועה נטו. קרוב ל-1
    זו מגמה נקייה, קרוב ל-0 זה דשדוש. זה מדד סטנדרטי ולא פרמטר
    שכוונן על הנתונים האלה.
    """
    c = day.close.values
    if len(c) < 5:
        return {}
    steps = np.abs(np.diff(c)).sum()
    net = abs(c[-1] - c[0])
    rng = float((day.high - day.low).mean())
    return {"day_atr_pts": round(rng, 3),
            "day_atr_pct": round(100 * rng / float(np.mean(c)), 4),
            "day_efficiency": round(float(net / steps) if steps else 0.0, 4),
            "day_range_pts": round(float(day.high.max() - day.low.min()), 3)}


def replay(setups: pd.DataFrame, bars: dict, stop_col: str,
           tp_col: str | None, tp_rr: float | None = None,
           pessimistic: bool = True, trail_trigger: float | None = None,
           trail_to: float = 0.0) -> pd.DataFrame:
    """מריץ את כל הסטאפים. tp_rr גובר על עמודת היעד, לסריקת רשת."""
    rows = []
    for r in setups.itertuples():
        b = bars.get(r.symbol)
        if b is None or b.empty:
            continue
        t = r.ts.time()
        # סטאפ שנוצר אחרי תחילת הנר האחרון אין לו בכלל נר עתידי
        # בתוך החלון. הוא נספר כמחוץ למושב במקום להיעלם בשקט.
        if not (SESSION_OPEN <= t <= LAST_BAR_START):
            rows.append({"status": "outside_session", "ts": r.ts,
                         "symbol": r.symbol, "direction": r.direction,
                         "entry": float(r.entry)})
            continue
        day = b[(b.session == r.ts.date())
                & (b.ts.dt.time >= SESSION_OPEN)
                & (b.ts.dt.time <= LAST_BAR_START)]
        if day.empty:
            continue
        stop = getattr(r, stop_col, None)
        if stop is None or not np.isfinite(stop):
            continue
        risk = abs(float(r.entry) - float(stop))
        if risk < MIN_RISK_PTS:
            continue
        if tp_rr is not None:
            tp = (r.entry + tp_rr * risk if r.direction == "long"
                  else r.entry - tp_rr * risk)
        elif tp_col is not None:
            v = getattr(r, tp_col, None)
            tp = float(v) if v is not None and np.isfinite(v) else None
        else:
            tp = None
        out = walk(day, r.direction, float(r.entry), float(stop), tp,
                   r.ts, pessimistic=pessimistic,
                   trail_trigger=trail_trigger, trail_to=trail_to)
        out.update(ts=r.ts, symbol=r.symbol, direction=r.direction,
                   entry=float(r.entry), stop=float(stop), tp=tp)
        # עמודות מהסטאפ שנוסעות הלאה לקובץ התוצאות.
        #
        # בלי זה אי אפשר לבדוק אם הדירוג בכלל מנבא תוצאה — וזו
        # ההשערה הראשונה בתור לפי ערך מידע. נתון שלא נאסף במהלך
        # ההרצה לא ניתן לשחזור אחריה, ולכן זה חייב להיות כאן לפני
        # שהמדידה מתחילה ולא אחריה.
        for col in ("grade", "analysis_id", "session", "setup_type"):
            v = getattr(r, col, None)
            if v is not None:
                out[col] = v
        # מדדי משטר יומיים, מאותם נרות שכבר נטענו. שניהם מחושבים
        # מהמושב כולו ולא מהעתיד של העסקה עצמה.
        out.update(regime_of(day))
        if out["status"] == "filled":
            out["net_R"] = out["raw_R"] - cost_R(r.symbol, out["risk_pts"])
        rows.append(out)
    return pd.DataFrame(rows)


def describe(res: pd.DataFrame, label: str) -> dict | None:
    f = res[res.status == "filled"]
    n_all = len(res)
    print(f"\n{'=' * 58}\n  {label}\n{'=' * 58}")
    out_s = int((res.status == "outside_session").sum())
    inside = n_all - out_s
    print(f"  סטאפים: {n_all}   מחוץ לשעות המסחר: {out_s}   "
          f"בתוכן: {inside}")
    print(f"  התמלאו: {len(f)} "
          f"({0 if not inside else len(f) / inside * 100:.0f}% מאלה שבתוך "
          f"החלון)   לא התמלאו: {int((res.status == 'no_fill').sum())}")
    if len(f) < MIN_TRADES:
        print(f"  פחות מ-{MIN_TRADES} מילויים — אין מה לחשב.")
        return None

    net = f.net_R.values
    m, lo_, hi = interval(net)
    cm, clo, chi, k = clustered_interval(net, f.ts.dt.date)
    wins = int((net > 0).sum())
    print(f"  תוחלת נטו : {m:+.3f}R")
    print(f"  רווח סמך  : [{clo:+.3f}, {chi:+.3f}] מקובץ לפי {k} ימי מסחר")
    print(f"              [{lo_:+.3f}, {hi:+.3f}] אילו {len(f)} העסקאות "
          f"היו עצמאיות — צר מדי")
    print(f"  סטיית תקן : {f.net_R.std(ddof=1):.3f}R   "
          f"מנצחות: {wins}/{len(f)} ({wins / len(f) * 100:.0f}%)")
    print(f"  ברוטו     : {f.raw_R.mean():+.3f}R   "
          f"עלות: {f.raw_R.mean() - m:.3f}R לעסקה")
    by = f.reason.value_counts().to_dict()
    print(f"  יציאות    : " + "  ".join(f"{k}={v}" for k, v in by.items()))
    print(f"  MFE חציוני: {f.mfe_R.median():+.2f}R   "
          f"MAE חציוני: {f.mae_R.median():+.2f}R")
    amb = int(f.ambiguous.sum())
    if amb:
        print(f"  נרות דו-משמעיים: {amb} מתוך {len(f)} "
              f"({amb / len(f) * 100:.0f}%)")

    # פילוח לפי חודש. מאי הוא החודש שתוקן, יוני ויולי הגיעו כמו
    # שהם. אם המסקנה מתהפכת ביניהם, התיקון הוא שנושא את התוצאה
    # ולא האסטרטגיה — וזה בדיוק מה שצריך לראות לפני שסומכים עליה.
    by_month = f.groupby(f.ts.dt.strftime("%Y-%m")).net_R.agg(["size", "mean"])
    if len(by_month) > 1:
        print("  לפי חודש  : " + "   ".join(
            f"{m} n={int(r['size'])} {r['mean']:+.3f}R"
            for m, r in by_month.iterrows()))

    gaps = int((f.reason == "gap_scratch").sum())
    if gaps:
        # כל שריטה כזאת היא הפסד שנמחק. השורה הזאת מראה מה קורה אם
        # מניחים שבפועל היו אוכלים את הפער במלואו.
        harsh = np.where(f.reason.values == "gap_scratch", -1.0, net)
        hm, hlo, _ = interval(harsh)
        print(f"  שריטות על פער: {gaps} מתוך {len(f)} "
              f"({gaps / len(f) * 100:.0f}%)")
        print(f"    אם כל אחת מהן הייתה -1R: {hm:+.3f}R "
              f"(גבול תחתון {hlo:+.3f})")
    return {"n": len(f), "mean": m, "lo": clo, "hi": chi,
            "naive_lo": lo_, "days": k, "amb": amb, "gaps": gaps}


def main() -> None:
    bot = Path(sys.argv[1]) if len(sys.argv) > 1 else BOT_DEFAULT
    setups_path = D / "setups.csv"
    if not setups_path.exists():
        sys.exit(f"חסר {setups_path}")

    bars = {}
    for sym in ("ES", "NQ"):
        b = load_bars_5m(sym)
        if b.empty:
            print(f"  {sym}: אין נרות ב-{D / f'{sym}_5min_clean.csv'}")
        else:
            bars[sym] = b
            print(f"  {sym}: {len(b):,} נרות  {b.ts.iloc[0]:%Y-%m-%d} "
                  f"עד {b.ts.iloc[-1]:%Y-%m-%d}")
    if not bars:
        sys.exit("\nאין נרות בכלל. להריץ קודם futures_bars.py.")

    s = load_clean_setups(setups_path)
    print(f"  סטאפים בחלון הנקי: {len(s)}")
    if s.empty:
        sys.exit("אין סטאפים בחלון.")

    stop_col = pick_column(s, STOP_NAMES)
    tp_col = pick_column(s, TP_NAMES)
    if stop_col is None:
        print("\nאין עמודת סטופ ב-setups.csv. העמודות שקיימות:")
        print("  " + ", ".join(map(str, s.columns)))
        sys.exit("בלי סטופ אין סיכון מוגדר, ובלי סיכון מוגדר אין R. עוצר.")
    print(f"  סטופ מעמודה '{stop_col}'" +
          (f", יעד מעמודה '{tp_col}'" if tp_col else ", אין עמודת יעד"))

    base = replay(s, bars, stop_col, tp_col)
    main_label = ("כפי שנרשם — סטופ ויעד מהסטאפ" if tp_col
                  else "כפי שנרשם — סטופ בלבד, סגירה בסוף יום")
    summary = describe(base, main_label)

    if summary and summary["amb"]:
        opt = replay(s, bars, stop_col, tp_col, pessimistic=False)
        o = opt[opt.status == "filled"]
        om, olo, ohi = interval(o.net_R.values)
        print(f"\n  אותה הרצה עם ההכרעה ההפוכה בנר הדו-משמעי: "
              f"{om:+.3f}R [{olo:+.3f}, {ohi:+.3f}]")
        if (om > 0) != (summary["mean"] > 0):
            print("  שתי ההכרעות נותנות סימן הפוך. הבקטסט לא הכריע —")
            print("  צריך נרות בדקה אחת כדי לפרק את הנרות האלה.")
        else:
            print("  אותו סימן בשתי ההכרעות. הדו-משמעיות לא משנה את המסקנה.")

    trail_summary(s, bars, stop_col, tp_col, summary)

    print(f"\n{'=' * 58}\n  רשת יעדים — איזה RR האסטרטגיה בכלל תומכת בו"
          f"\n{'=' * 58}")
    print(f"{'RR':>6} {'n':>5} {'תוחלת':>9} {'גבול תחתון':>12} "
          f"{'מנצחות':>9}")
    best = None
    for rr in RR_GRID:
        g = replay(s, bars, stop_col, None, tp_rr=rr)
        gf = g[g.status == "filled"]
        if len(gf) < MIN_TRADES:
            continue
        # אותו קיבוץ לפי יום כמו בכותרת. גבול תחתון צר יותר כאן
        # היה גורם לרשת להיראות בטוחה יותר מהמדידה הראשית.
        m, lo_, _, _ = clustered_interval(gf.net_R.values, gf.ts.dt.date)
        w = (gf.net_R > 0).mean() * 100
        print(f"{rr:>6.1f} {len(gf):>5} {m:>+8.3f}R {lo_:>+11.3f}R {w:>8.0f}%")
        if best is None or m > best[1]:
            best = (rr, m, lo_)

    if best:
        print(f"\n  הטוב ביותר ברשת: RR {best[0]:.1f} בתוחלת {best[1]:+.3f}R.")
        print("  זה נבחר בדיעבד מתוך חמש אפשרויות על אותם נתונים, ולכן")
        print("  הוא מוטה כלפי מעלה. הוא מראה מה האסטרטגיה תומכת בו,")
        print("  לא מה היא תיתן קדימה.")

    report_drift(contract_drift(bars, bot), base)

    out = D / "replay_results.csv"
    base.to_csv(out, index=False)
    print(f"\nפירוט מלא -> {out}")

    if summary:
        project(summary, base)


def trail_summary(s: pd.DataFrame, bars: dict, stop_col: str,
                  tp_col: str | None, base_summary: dict | None) -> None:
    """מה הגרירה עושה למספר — ובאיזה תנאי מותר להאמין לזה.

    החשבון הממומן רץ עם גרירה חיה. כלומר המדידה בלי גרירה כבר לא
    מתארת אותו, ולהמשיך לצטט אותה זה לדווח על מכשיר אחר. מצד שני
    הטריגר והיעד הם פרמטרים של הבוט שלא אומתו כאן, ומספר שנשען על
    קבוע לא מאומת לא נכנס לחישוב הדולרים. לכן שניהם מודפסים זה לצד
    זה, ורק זה בלי הגרירה ממשיך הלאה.
    """
    print(f"\n{'=' * 58}\n  גרירת הסטופ — מה שהחשבון הממומן באמת מריץ"
          f"\n{'=' * 58}")
    print(f"  טריגר {TRAIL_TRIGGER_R:.2f}R, הסטופ זז ל-{TRAIL_TO_R:+.2f}R.")
    print("  שני הקבועים האלה לא אומתו מול broker/ibkr.py. הסעיף הזה")
    print("  תקף רק אם הם נכונים, ולכן הוא לא נכנס לחישוב הדולרים.")
    print("  הדגימה היא בסגירת נר של חמש דקות — בדיוק מרווח הסריקה של")
    print("  הבוט. נגיעה בטריגר בתוך החלון שלא שרדה עד הסגירה איננה")
    print("  אירוע, כי הבוט קורא מחיר אחד ברגע אחד ולא את השיא.")

    t = replay(s, bars, stop_col, tp_col,
               trail_trigger=TRAIL_TRIGGER_R, trail_to=TRAIL_TO_R)
    tf = t[t.status == "filled"]
    if len(tf) < MIN_TRADES:
        print(f"\n  {len(tf)} עסקאות בלבד. מעט מדי מכדי לומר משהו.")
        return
    m, lo_, hi_, k = clustered_interval(tf.net_R.values, tf.ts.dt.date)
    fired = int(tf.trailed.sum())
    print(f"\n  {fired} מתוך {len(tf)} פוזיציות גררו "
          f"({fired / len(tf) * 100:.0f}%).")
    print(f"  תוחלת עם גרירה: {m:+.3f}R  [{lo_:+.3f}, {hi_:+.3f}] "
          f"על {k} ימים.")
    if base_summary:
        d = m - base_summary["mean"]
        print(f"  בלי גרירה: {base_summary['mean']:+.3f}R "
              f"[{base_summary['lo']:+.3f}, {base_summary['hi']:+.3f}].")
        print(f"  ההפרש: {d:+.3f}R. זה מה שהמעבר לחשבון הממומן עשה")
        print("  למספר, וזו הסיבה שהמדידה הישנה כבר לא מתארת אותו.")
        if (lo_ > 0) != (base_summary["lo"] > 0):
            print("  שימו לב: הגרירה מזיזה את הגבול התחתון מעבר לאפס.")
            print("  כלומר ההחלטה כמה חשבונות מותר תלויה בקבוע שלא אומת.")
            print("  לאמת אותו מול broker/ibkr.py לפני כל החלטת חשיפה.")

    print(f"\n  רגישות לטריגר — אם הקבוע אינו {TRAIL_TRIGGER_R:.2f}:")
    print(f"{'טריגר':>8} {'גררו':>7} {'תוחלת':>9} {'גבול תחתון':>12}")
    for trig in TRAIL_GRID:
        g = replay(s, bars, stop_col, tp_col,
                   trail_trigger=trig, trail_to=TRAIL_TO_R)
        gf = g[g.status == "filled"]
        if len(gf) < MIN_TRADES:
            continue
        gm, glo, _, _ = clustered_interval(gf.net_R.values, gf.ts.dt.date)
        print(f"{trig:>8.2f} {int(gf.trailed.sum()):>7} "
              f"{gm:>+8.3f}R {glo:>+11.3f}R")
    print("\n  אם השורות האלה חולקות על הסימן זו מזו, הקבוע אינו פרט")
    print("  טכני אלא ההחלטה עצמה, ואין להחליט על חשיפה לפני שהוא ידוע.")


def project(summary: dict, base: pd.DataFrame) -> None:
    """מה התוחלת הזאת שווה בדולרים, דרך המודל שכבר בודק דרודאון.

    הפיתוי כאן הוא להכפיל R בעסקאות ליום ב-250 וב-4% ולקרוא לזה
    תשואה שנתית. זה מחזיר מספרים כמו 900% לשנה, והם שקר: החשבון
    נשרף הרבה לפני, סולם המשיכות חסום, והדרודאון הנגרר חותך. המודל
    ב-apex_model.py כבר מכיל את כל אלה. לכן התוחלת הנמדדת נכנסת
    אליו כקלט, במקום להיות מוכפלת בראש.
    """
    print(f"\n{'=' * 58}\n  מה זה אומר על התיק\n{'=' * 58}")
    per_day = summary["n"] / max(1, summary["days"])
    print(f"  {per_day:.1f} עסקאות ביום מתוך הסטאפים, "
          f"{summary['n']} על פני {summary['days']} ימי מסחר.")
    try:
        from apex_model import simulate
    except Exception as e:
        print(f"  לא הצלחתי לטעון את apex_model: {str(e)[:60]}")
        return
    print(f"\n{'תרחיש':<14}{'avg_R':>8}{'חציון שנה 8':>16}{'אחוזון 10':>14}")
    for name, val in (("תוחלת", summary["mean"]),
                      ("גבול תחתון", summary["lo"])):
        if not np.isfinite(val):
            continue
        # risk_pct_eval הוא לא פרט. בלעדיו ההערכה נמדדת ב-4% כמו
        # החשבון הממומן, בניגוד לכלל הדו-מהירותי של המיומנות, והיעד
        # של ההערכה הופך ל-35.3R מתוך 63 עסקאות — כלומר בלתי אפשרי.
        # המודל אז שורף דמי הערכה לנצח ולא עובר אף פעם, והשורה הזאת
        # מדפיסה מינוס על תוחלת חיובית. על +0.101R זה היה ההפרש בין
        # 7,372$- ל-200,677$+.
        r = simulate(plan="50K", slots=10, avg_R=float(val), risk_pct=0.04,
                     risk_pct_eval=0.10, n=800, seed=11)
        tot = r["net_year"].sum(axis=1)
        print(f"  {name:<12}{val:>+8.3f}{np.median(tot):>15,.0f}$"
              f"{np.percentile(tot, 10):>13,.0f}$")
    print("\n  הגבול התחתון הוא מה שקובע החלטות, לא התוחלת. אם הוא")
    print("  שלילי, המסקנה היא פחות חשיפה — לא אסטרטגיה מכוילת מחדש.")


if __name__ == "__main__":
    main()
