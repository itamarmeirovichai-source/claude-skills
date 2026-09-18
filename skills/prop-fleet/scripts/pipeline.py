#!/usr/bin/env python3
"""
pipeline.py — פקודה אחת במקום שלוש.

למה זה קיים
-----------
כל מחזור עד כה דרש ממנו להריץ ידנית שליפה ואז ריפליי, ולזכור להעביר
את נתיב הבוט לשני, ולהסתכל בעצמו אם השליפה בכלל הצליחה לפני שהוא
מסתכל על התוצאה. כל אחד מהשלבים האלה הוא מקום להישמט.

כאן זה שלב אחד שנעצר בעצמו. אם השליפה לא ייצרה נרות, אין ריפליי —
כי ריפליי על נרות ישנים מדווח מספר שנראה בסדר גמור ואין בו שום סימן
לכך שהוא מתאר את השליפה של אתמול.

שימוש
-----
    python3 pipeline.py                      # נתיב ברירת מחדל לבוט
    python3 pipeline.py '/נתיב/לבוט'
    python3 pipeline.py '/נתיב/לבוט' --keep  # לא לשלוף מחדש

דורש IB Gateway פתוח על 4002 לשלב השליפה.
"""

import sys
from pathlib import Path

D = Path.home() / "Desktop"
BOT_DEFAULT = D / "meirox-ai" / "MeiroX-AI - בוט מסחר"
BARS = ("ES", "NQ")


def stamp(sym: str):
    """גודל וזמן שינוי של קובץ הנרות, כדי לדעת אם הוא באמת התחדש."""
    p = D / f"{sym}_5min_clean.csv"
    if not p.exists():
        return None
    st = p.stat()
    return (st.st_size, int(st.st_mtime))


def banner(text: str) -> None:
    print(f"\n{'=' * 62}\n  {text}\n{'=' * 62}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bot = Path(args[0]) if args else BOT_DEFAULT
    if not bot.exists():
        sys.exit(f"לא מצאתי את תיקיית הבוט:\n  {bot}")

    before = {s: stamp(s) for s in BARS}

    banner("שלב 1 מתוך 2 — נרות חמש דקות מ-IBKR")
    import futures_bars
    futures_bars.BOT = bot
    try:
        futures_bars.main()
    except SystemExit as e:
        if e.code:
            print(f"\nהשליפה נעצרה: {e}")
            sys.exit("לא ממשיך לריפליי — אין נרות חדשים לבנות עליהם.")
    except Exception as e:
        sys.exit(f"\nהשליפה נכשלה: {type(e).__name__}: {str(e)[:120]}")

    after = {s: stamp(s) for s in BARS}
    fresh = [s for s in BARS if after[s] and after[s] != before[s]]
    kept = [s for s in BARS if after[s] and after[s] == before[s]]
    if not any(after.values()):
        sys.exit("\nאין קובצי נרות בכלל. לא ממשיך.")
    if fresh:
        print(f"\nהתחדשו: {', '.join(fresh)}")
    if kept:
        # לא שגיאה — אבל צריך להיאמר, כי ריפליי על נרות מאתמול נראה
        # בדיוק כמו ריפליי על נרות מהיום.
        print(f"לא השתנו: {', '.join(kept)} — הריפליי ירוץ עליהם כמו שהם")

    banner("שלב 2 מתוך 2 — ריפליי הסטאפים")
    sys.argv = [sys.argv[0], str(bot)]
    import replay
    replay.main()


if __name__ == "__main__":
    main()
