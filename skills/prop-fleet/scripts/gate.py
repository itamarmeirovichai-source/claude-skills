#!/usr/bin/env python3
"""
gate.py — כמה חשבונות מותר להריץ עכשיו, לפי הראיות בלבד.

מה זה עושה
----------
קורא את רשומת העסקאות, מחשב את התוחלת ואת רווח הסמך סביבה, ואומר באיזה
שלב בסולם אתה נמצא. זה כל התפקיד. הוא לא מנתח אסטרטגיה, לא מציע שיפורים,
ולא מפרש רצף הפסדים — הוא רק אומר כמה חשיפה הראיות מצדיקות.

למה זה סקריפט ולא שיקול דעת
---------------------------
כי בדיוק כאן אנשים טועים, ואני טעיתי כאן בעצמי. אחרי רצף הפסדים מתחשק
להקטין; אחרי רצף רווחים מתחשק להגדיל. שתי התחושות לא קשורות לראיות. מספר
שמחושב באותה נוסחה בכל שבוע לא מושפע מזה.

הכלל היחיד: **הגבול התחתון של רווח הסמך** קובע. לא הממוצע. ממוצע של
+0.40R מתוך 20 עסקאות הוא רעש; ממוצע של +0.25R מתוך 400 הוא עסק.

שימוש
-----
    python3 gate.py                        קורא את trades.db בנתיב הרגיל
    python3 gate.py /path/to/trades.db
    python3 gate.py /path/to/trades.csv    עמודות: pnl_r  (ואופציונלי ts)
    python3 gate.py ... --stage 3          מה מותר לעומת איפה אתה עכשיו
"""

import sqlite3
import sys
from pathlib import Path

import numpy as np

# שלב, חשבונות מותרים, מינימום עסקאות, הגבול התחתון הנדרש
LADDER = [
    (0, 0,  0,   None),
    (1, 1,  100, 0.00),
    (2, 3,  250, 0.10),
    (3, 10, 500, 0.20),
    (4, 20, 900, 0.20),
]
BOOTSTRAP = 20_000
CONF = 95.0


def load(path: Path) -> np.ndarray:
    if path.suffix.lower() == ".csv":
        import csv
        vals = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                v = (row.get("pnl_r") or "").strip()
                if v not in ("", "None", "NULL"):
                    try:
                        vals.append(float(v))
                    except ValueError:
                        pass
        return np.array(vals, dtype=float)

    con = sqlite3.connect(str(path))
    try:
        rows = con.execute(
            "SELECT pnl_r FROM trades WHERE status='closed' AND pnl_r IS NOT NULL"
        ).fetchall()
    finally:
        con.close()
    return np.array([r[0] for r in rows if r[0] is not None], dtype=float)


def integrity_warnings(path: Path) -> list:
    """רשומות שלא יכולות להיות נכונות. אם יש כאלה, המספר למטה לא אמין."""
    if path.suffix.lower() == ".csv":
        return []
    con = sqlite3.connect(str(path))
    out = []
    def q(sql):
        try:
            return con.execute(sql).fetchone()[0]
        except sqlite3.Error:
            return None
    checks = [
        ("עסקאות סגורות עם pnl_r ריק",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r IS NULL"),
        ("pnl_r בדיוק 0.0 עם רווח שאינו אפס",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r=0 "
         "AND pnl IS NOT NULL AND pnl<>0"),
        ("|pnl_r| מעל 10",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND ABS(pnl_r)>10"),
        ("כניסה ויציאה זהות",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND entry=exit_price"),
        ("ללא analysis_id",
         "SELECT COUNT(*) FROM trades WHERE analysis_id IS NULL OR analysis_id=0"),
    ]
    for label, sql in checks:
        n = q(sql)
        if n:
            out.append(f"{label}: {n}")
    con.close()
    return out


def bootstrap_ci(r: np.ndarray, conf=CONF, n_boot=BOOTSTRAP, seed=17):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(r), size=(n_boot, len(r)))
    means = r[idx].mean(axis=1)
    lo = np.percentile(means, (100 - conf) / 2)
    hi = np.percentile(means, 100 - (100 - conf) / 2)
    return float(lo), float(hi)


def permitted(n: int, lower: float):
    """השלב הגבוה ביותר שגם מספר העסקאות וגם הגבול התחתון מצדיקים."""
    best = LADDER[0]
    for stage in LADDER[1:]:
        _, _, need_n, need_lo = stage
        if n >= need_n and lower > need_lo:
            best = stage
    return best


def longest_losing_run(r: np.ndarray) -> int:
    run = best = 0
    for x in r:
        if x < 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cur_stage = None
    for a in sys.argv[1:]:
        if a.startswith("--stage"):
            try:
                cur_stage = int(a.split("=", 1)[1] if "=" in a
                                else sys.argv[sys.argv.index(a) + 1])
            except (ValueError, IndexError):
                pass

    default = (Path.home() / "Desktop" / "meirox-ai" /
               "MeiroX-AI - בוט מסחר" / "logs" / "trades.db")
    path = Path(args[0]).expanduser() if args else default
    if not path.exists():
        sys.exit(f"לא נמצא {path}")

    warns = integrity_warnings(path)
    r = load(path)

    print()
    print("=" * 60)
    print("  שער ההרחבה")
    print("=" * 60)

    if warns:
        print("\n  ⚠ רשומות פגומות — המספרים למטה לא אמינים:")
        for w in warns:
            print(f"      {w}")
        print("      תקן קודם (bot/integrity.py), ואז הרץ שוב.")

    n = len(r)
    if n == 0:
        print("\n  אין עסקאות סגורות עם pnl_r. אין מה למדוד.")
        print("  שלב מותר: 0 — אפס חשבונות.\n")
        return

    mean = float(r.mean())
    lo, hi = bootstrap_ci(r) if n >= 10 else (float("nan"), float("nan"))
    wins = float((r > 0).mean())

    print(f"\n  עסקאות סגורות : {n:,}")
    print(f"  אחוז הצלחה    : {100*wins:.1f}%")
    print(f"  תוחלת         : {mean:+.3f}R")
    if n >= 10:
        print(f"  רווח סמך {CONF:.0f}%  : [{lo:+.3f}R , {hi:+.3f}R]")
    else:
        print(f"  רווח סמך {CONF:.0f}%  : לא מחושב מתחת ל-10 עסקאות")
    print(f"  רצף ההפסדים הארוך: {longest_losing_run(r)}")

    if n < 10 or not np.isfinite(lo):
        print("\n  מדגם קטן מדי לכל מסקנה.")
        print("  שלב מותר: 0 — אפס חשבונות.\n")
        return

    stage, accounts, _, _ = permitted(n, lo)
    print(f"\n  {'-'*56}")
    print(f"  שלב מותר: {stage} — עד {accounts} חשבונות")
    print(f"  {'-'*56}")

    if cur_stage is not None:
        if stage > cur_stage:
            print(f"\n  אתה בשלב {cur_stage}. הראיות מצדיקות {stage}. -> להרחיב.")
        elif stage < cur_stage:
            print(f"\n  אתה בשלב {cur_stage}. הראיות מצדיקות רק {stage}. "
                  f"-> **להקטין חשיפה**.")
            print("     לא לשנות אסטרטגיה. להוריד מספר חשבונות.")
        else:
            print(f"\n  אתה בשלב {cur_stage}, וזה מה שהראיות מצדיקות. -> להמשיך כרגיל.")

    nxt = next((s for s in LADDER if s[0] == stage + 1), None)
    if nxt:
        _, acc2, need_n, need_lo = nxt
        if n < need_n:
            print(f"\n  לשלב {stage+1} ({acc2} חשבונות) חסרות {need_n - n:,} עסקאות")
            print(f"  ואז הגבול התחתון צריך להיות מעל {need_lo:+.2f}R "
                  f"(עכשיו {lo:+.3f}R)")
        elif lo <= need_lo:
            print(f"\n  מספר העסקאות מספיק לשלב {stage+1}, "
                  f"אבל הגבול התחתון {lo:+.3f}R עדיין לא מעל {need_lo:+.2f}R.")
    print()


if __name__ == "__main__":
    main()
