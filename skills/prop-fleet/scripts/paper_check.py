#!/usr/bin/env python3
"""
paper_check.py — האם נתיב הביצוע נקי, לפי הרשומות שהוא עצמו כתב.

למה זה קיים
-----------
השער דורש דבר אחד לפני החשבון הראשון: "ביצוע מאומת נקי בהרצה
מסומלצת". זה לא מספר עסקאות ולא תוחלת — זו טענה על הצנרת, ועד
עכשיו שום דבר לא בדק אותה. הרצה על נייר היא בדיוק ההרצה הזאת.

מה זה בודק, וזה החלק שמעניין
-----------------------------
באג ההמרה היה בלתי נראה כי כל רמה בפני עצמה נראתה סבירה. הכניסה
יצאה במחיר השוק — מחיר אמיתי, בטווח אמיתי — והסטופ והיעד הומרו
נכון. בדיקת טווח לא תופסת דבר כזה.

אבל יש אינווריאנטה שכן תופסת אותה, וכל מה שהיא צריכה נמצא בשורה
עצמה. המרה נכונה מכפילה את **כל שלוש** הרמות באותו יחס:

    exec_entry / entry_price
      == exec_stop_loss / stop_loss
      == exec_take_profit / take_profit_1

תחת הבאג, הכניסה נקבעת למחיר ה-ETF בזמן השליחה בזמן שהסטופ והיעד
מחולקים ביחס — ולכן שלושת המנות **נחלקות**. במצב חוזים שלושתן שוות
בדיוק 1.0. בשני המצבים זו בדיקה אחת, והיא לא דורשת לדעת מה היה
מחיר השוק באותו רגע.

מה הרצת נייר לא מוכיחה
----------------------
לא את הקצה. מילוי על נייר הוא אופטימי — לימיט מתמלא בנגיעה, בלי
תור, בלי מילוי חלקי, ובלי ההחלקה שפקודת שוק אמיתית סופגת. תוחלת
שנמדדת על נייר מוטה כלפי מעלה, ולכן הסקריפט הזה מסרב להדפיס
תוחלת בכלל. הוא אומר רק אם הצנרת נקייה.

שימוש
-----
    python3 paper_check.py
    python3 paper_check.py '/נתיב/לבוט'
    python3 paper_check.py '/נתיב/לבוט' --since 2026-09-21
"""

import sqlite3
import sys
from pathlib import Path

HOME = Path.home()
BOT_DEFAULT = HOME / "Desktop" / "meirox-ai" / "MeiroX-AI - בוט מסחר"

OK, BAD, WARN, INFO = "  ✓", "  ✗", "  !", "  ·"

# סטייה יחסית מותרת בין שלוש המנות. round(..., 4) על מחירים תלת-ספרתיים
# משאיר רעש בסדר גודל של 1e-6; 1e-4 הוא רחב פי מאה מזה וצר בהרבה
# מכל באג אמיתי.
REL_TOL = 1e-4
# מתחת לזה אין מה לומר על הצנרת.
MIN_TRADES = 5
# שני מחירים שהיחס ביניהם מחוץ לתחום הזה אינם באותו קנה מידה.
# עסקה בודדת לא מזיזה מחיר פי שניים; מה שכן נותן פי עשרה הוא
# רמת חוזה מול מחיר ETF.
SAME_SCALE = (0.5, 2.0)


def say(mark, text):
    print(f"{mark} {text}")


def banner(t):
    print(f"\n{'=' * 62}\n  {t}\n{'=' * 62}")


def ratios(row) -> dict:
    """שלוש המנות, לכל רמה שקיימת בשורה."""
    out = {}
    for name, sig, ex in (("כניסה", "entry_price", "exec_entry"),
                          ("סטופ", "stop_loss", "exec_stop_loss"),
                          ("יעד", "take_profit_1", "exec_take_profit")):
        a, b = row[sig], row[ex]
        if a in (None, 0) or b is None:
            continue
        out[name] = float(b) / float(a)
    return out


def verdict_for(row) -> tuple:
    """(תקין, הסבר). None כשאי אפשר להכריע מהשורה הזאת."""
    r = ratios(row)
    if "כניסה" not in r:
        # בלי exec_entry אין מה לבדוק, ומי שסופר שורה כזאת כעבר
        # מפספס בדיוק את הבאג שהסקריפט הזה קיים בשבילו.
        #
        # ‏exec_stop_loss ו-exec_take_profit נכתבים שניהם **בשליחת
        # הפקודה**, מאותה המרה ובאותו רגע, ולכן היחס ביניהם אחיד
        # תמיד — גם כשההמרה שגויה לגמרי. הבאג המקורי התבטא בכך
        # שהכניסה נחלקה מהשניים האחרים; הזוג סטופ-יעד לבדו הוא
        # בדיוק הזוג שלא יכול לגלות אותו.
        #
        # ‏exec_entry נכתב רק במילוי אמיתי. פקודה שבוטלה בלי שהתמלאה
        # משאירה אותו ריק, ואת שתי הרמות האחרות מלאות ומסכימות —
        # 23/09/2026 הפיקה בדיוק שורה כזאת, עם פיזור של 7e-6 מול
        # סף של 1e-4, והיא הייתה נספרת כראיה נקייה.
        return None, ("אין exec_entry — הפקודה לא התמלאה. הזוג "
                      "סטופ-יעד נכתב בשליחה ולכן הוא אחיד מעצם בנייתו")
    if len(r) < 2:
        # רמה אחת לבדה לא ניתנת להשוואה. זה לא 'עבר' — זה 'לא נבדק',
        # ומי שסופר את זה כעבר חוזר בדיוק על הבאג המקורי.
        return None, "פחות משתי רמות — אי אפשר להשוות"
    lo, hi = min(r.values()), max(r.values())
    if lo <= 0:
        return False, f"יחס לא חיובי: {r}"
    if (hi - lo) / hi > REL_TOL:
        detail = ", ".join(f"{k}={v:.5f}" for k, v in r.items())
        return False, f"המנות נחלקות: {detail}"
    return True, f"יחס אחיד {lo:.5f}"


def sign_verdict(row) -> tuple:
    """האם הרווח מסכים עם הכיוון והמחירים. None כשאי אפשר לבדוק.

    הנקודה כאן היא באיזה מחיר כניסה משתמשים, והיא הפילה אותי פעם
    אחת. ‏exit_price נרשם בקנה מידה של **ביצוע**. ‏exec_entry הוא
    באותו קנה מידה, ולכן הוא היחיד שמותר להשוות אליו. ‏entry_price
    הוא הרמה מהאסטרטגיה, ובמצב מניות היא רמת חוזה — כלומר 5000 מול
    505, והחיסור בין השניים תמיד שלילי ותמיד ענק.

    הגרסה הראשונה נפלה חזרה ל-entry_price כשחסר exec_entry, וסימנה
    בדיוק כל לונג רווחי וכל שורט מפסיד כ"סתירה". זו לא הייתה תקלה
    ברשומה — זה היה ערבוב קני מידה בתוך הבודק עצמו, בדיוק הסוג
    שהבודק הזה נבנה כדי לתפוס.

    לכן: exec_entry קודם; ובלעדיו נבדק היחס בין שני המחירים, ואם
    הוא מחוץ לתחום סביר — לא בודקים, ואומרים למה.
    """
    exit_px = row["exit_price"]
    pnl = row["pnl"]
    if exit_px is None or pnl is None:
        return None, "חסר מחיר יציאה או רווח"
    entry = row["exec_entry"]
    src = "exec_entry"
    if entry is None:
        entry = row["entry_price"]
        src = "entry_price"
    if entry in (None, 0):
        return None, "אין מחיר כניסה"
    ratio = float(exit_px) / float(entry)
    if src == "entry_price" and not (SAME_SCALE[0] <= ratio <= SAME_SCALE[1]):
        return None, (f"exec_entry ריק ו-entry_price בקנה מידה אחר "
                      f"(יציאה/כניסה = {ratio:.4f}) — אי אפשר להשוות")
    if float(pnl) == 0:
        return None, "רווח אפס — הסימן לא מוגדר"
    move = float(exit_px) - float(entry)
    want = move if (row["direction"] or "").lower() == "long" else -move
    if (want > 0) != (float(pnl) > 0):
        return False, (f"{row['direction']} מ-{float(entry):.2f} "
                       f"ל-{float(exit_px):.2f} אבל pnl={float(pnl):+.2f}")
    return True, "עקבי"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    since = None
    for a in sys.argv[1:]:
        if a.startswith("--since"):
            since = a.split("=", 1)[1] if "=" in a else None
    if "--since" in sys.argv:
        i = sys.argv.index("--since")
        if i + 1 < len(sys.argv):
            since = sys.argv[i + 1]
            args = [x for x in args if x != since]

    bot = Path(args[0]) if args else BOT_DEFAULT
    db = bot / "logs" / "trades.db"
    banner("בדיקת נתיב הביצוע — הרצת נייר")
    if not db.exists():
        sys.exit(f"אין {db}")

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    cols = {r[1] for r in con.execute("PRAGMA table_info(trades)")}
    need = {"entry_price", "stop_loss", "exec_entry", "exec_stop_loss"}
    missing = need - cols
    if missing:
        con.close()
        sys.exit(f"חסרות עמודות: {', '.join(sorted(missing))}. "
                 "להריץ קודם את המיגרציה של exec_*.")

    sql = "SELECT * FROM trades"
    params = ()
    if since:
        sql += " WHERE timestamp >= ?"
        params = (since,)
    sql += " ORDER BY id"
    rows = list(con.execute(sql, params))
    con.close()

    if not rows:
        sys.exit("אין עסקאות בטווח שנבחר.")

    good, bad, unknown = [], [], []
    for row in rows:
        ok, why = verdict_for(row)
        (good if ok else unknown if ok is None else bad).append((row, why))

    say(INFO, f"{len(rows)} עסקאות נבדקו" + (f" מאז {since}" if since else ""))
    say(OK if good else INFO, f"{len(good)} עם יחס המרה אחיד")
    if unknown:
        say(WARN, f"{len(unknown)} לא ניתנות להשוואה — לא נספרות כעבר")
    if bad:
        say(BAD, f"{len(bad)} עם מנות שנחלקות — זו חתימת באג ההמרה")
        for row, why in bad[:5]:
            say(BAD, f"  id={row['id']} {row['market']} {row['direction']}: {why}")

    # ── סימן הרווח מול הכיוון ─────────────────────────────────────
    closed = [r for r in rows if r["status"] == "closed"
              and r["pnl"] is not None and r["exit_price"] is not None]
    sign_bad, sign_skip = [], []
    for r in closed:
        ok, why = sign_verdict(r)
        if ok is False:
            sign_bad.append((r, why))
        elif ok is None:
            sign_skip.append((r, why))
    if closed:
        good_n = len(closed) - len(sign_bad) - len(sign_skip)
        if sign_bad:
            say(BAD, f"{len(sign_bad)} מתוך {len(closed)} סגורות: הרווח סותר "
                     "את הכיוון והמחירים")
            for r, why in sign_bad[:5]:
                say(BAD, f"  id={r['id']} {r['market']} {r['direction']}: {why}")
        if sign_skip:
            say(WARN, f"{len(sign_skip)} מתוך {len(closed)} לא ניתנות לבדיקת "
                      "סימן — לא נספרות כעבר")
            say(INFO, f"  {sign_skip[0][1]}")
        if good_n:
            say(OK, f"{good_n} סגורות, הרווח עקבי עם הכיוון והמחירים")

    # ── קישור לסטאפ ───────────────────────────────────────────────
    orphan = [r for r in rows
              if not r["analysis_id"] or r["analysis_id"] == 0]
    if orphan:
        say(BAD, f"{len(orphan)} בלי analysis_id — אי אפשר לקשר לסטאפ")
    else:
        say(OK, "כל העסקאות מקושרות לסטאפ שיצר אותן")

    # ── הפסק דין ──────────────────────────────────────────────────
    banner("מה זה מכריע")
    clean = not bad and not sign_bad and not orphan
    enough = len(good) >= MIN_TRADES
    if clean and enough:
        say(OK, "נתיב הביצוע נקי. תנאי השער למעבר לשלב 1 מתקיים.")
    elif clean and not good:
        # אפס עסקאות בנות-בדיקה. אף בדיקה לא רצה, ולכן אין ממצא —
        # לא ממצא חיובי ולא שלילי. "נקי" כאן היה הופך היעדר בדיקה
        # לתעודת כשרות, וזו בדיוק הדרך שבה רשומה לא-מאומתת עוברת
        # הלאה כאילו נבדקה.
        say(WARN, "לא ניתן לאמת. אפס עסקאות בנות-בדיקה, כלומר אף")
        say(WARN, "בדיקה לא רצה — זה לא 'נקי', זה 'לא ידוע'.")
        say(WARN, f"צריך {MIN_TRADES} עסקאות בנות-השוואה לפני שהשער נפתח.")
    elif clean and not enough:
        say(WARN, f"{len(good)} עסקאות נבדקו ועברו, אבל צריך "
                  f"{MIN_TRADES} לפחות. עדיין לא מספיק כדי להכריע.")
    else:
        say(BAD, "נתיב הביצוע לא נקי. אין לקנות חשבון על המצב הזה —")
        say(BAD, "הוא לא ייצר ראיות, הוא ייצר עוד רשומות פגומות.")

    print()
    say(INFO, "ומה שזה לא מכריע: הקצה. מילוי על נייר מתמלא בנגיעה,")
    say(INFO, "בלי תור, בלי מילוי חלקי ובלי החלקה אמיתית, ולכן תוחלת")
    say(INFO, "שנמדדת עליו מוטה כלפי מעלה. הסקריפט הזה לא מדפיס תוחלת")
    say(INFO, "בכוונה. את הקצה מודדים בריפליי ובחשבון אמיתי בלבד.")


if __name__ == "__main__":
    main()
