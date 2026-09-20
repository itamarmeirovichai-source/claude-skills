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
    sign_bad = []
    for r in closed:
        entry = r["exec_entry"] if r["exec_entry"] is not None else r["entry_price"]
        if entry is None:
            continue
        move = float(r["exit_price"]) - float(entry)
        want = move if (r["direction"] or "").lower() == "long" else -move
        if float(r["pnl"]) != 0 and (want > 0) != (float(r["pnl"]) > 0):
            sign_bad.append(r)
    if closed:
        if sign_bad:
            say(BAD, f"{len(sign_bad)} מתוך {len(closed)} סגורות: הרווח סותר "
                     "את הכיוון והמחירים")
        else:
            say(OK, f"{len(closed)} סגורות, הרווח עקבי עם הכיוון והמחירים")

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
    elif clean and not enough:
        say(WARN, f"נקי עד כה, אבל רק {len(good)} עסקאות בנות-השוואה. "
                  f"צריך {MIN_TRADES} לפחות.")
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
