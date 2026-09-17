#!/usr/bin/env python3
"""
doctor.py — פקודה אחת שאומרת איפה הכל עומד ומה הצעד הבא.

יש כאן תשעה סקריפטים. אתה לא אמור לזכור איזה להריץ ומתי. תריץ את זה,
והוא יריץ את מה שרלוונטי ויגיד לך מה חסר.

    python3 doctor.py
    python3 doctor.py /נתיב/אחר/לבית      אם המבנה אצלך שונה

הוא לא משנה כלום. רק קורא ומדווח.
"""

import importlib.util
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOME = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home()
DESK = HOME / "Desktop"
BOT = DESK / "meirox-ai" / "MeiroX-AI - בוט מסחר"
DB = BOT / "logs" / "trades.db"
PROXY = BOT / "broker" / "proxy.py"
INTEGRITY = BOT / "bot" / "integrity.py"

OK, WARN, BAD, INFO = "  ✓", "  !", "  ✗", "  ·"
issues, nexts = [], []


def say(mark, text):
    print(f"{mark}  {text}")


def section(title):
    print(f"\n{'─' * 62}\n  {title}\n{'─' * 62}")


def have(name):
    return importlib.util.find_spec(name) is not None


# ── 1. סביבה ────────────────────────────────────────────────────

def check_env():
    section("סביבה")
    for mod, why in (("numpy", "המודלים והשער"), ("pandas", "אבחון הסטייה")):
        if have(mod):
            say(OK, f"{mod} מותקן ({why})")
        else:
            say(BAD, f"{mod} חסר — {why} לא ירוצו")
            issues.append(f"pip3 install {mod}")
    say(INFO, f"פייתון {sys.version.split()[0]}")


# ── 2. הבאג בשכבת הביצוע ────────────────────────────────────────

def _proxy_verdict(src: str):
    """מנתח את הקוד עצמו, לא את הטקסט.

    סריקת מחרוזות נתנה אזעקת שווא: ה-docstring של proxy_fix.py מצטט את
    הבאג כדי להסביר אותו, אז חיפוש טקסט מסמן את הקובץ המתוקן כפגום.
    ast מסתכל רק על מה שרץ.
    """
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None

    # הדגמה מכוונת של הבאג אינה הבאג. proxy_fix.py מחשב אותו תחת שם
    # כזה כדי להראות את ההפרש, וסימון שלו כתקלה הוא אזעקת שווא.
    DEMO = ("buggy", "demo", "old", "before", "wrong")

    buggy = fixed = False
    for node in ast.walk(tree):
        # ratio = entry / etf_price   ->  מחיר הכניסה מתבטל
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp) \
                and isinstance(node.value.op, ast.Div) \
                and isinstance(node.value.left, ast.Name) \
                and isinstance(node.value.right, ast.Name) \
                and node.value.left.id == "entry":
            names = [t.id.lower() for t in node.targets if isinstance(t, ast.Name)]
            if not any(n.startswith(DEMO) for n in names):
                buggy = True
        # ratio = futures_price / etf_price  ->  זוג ייחוס חי
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp) \
                and isinstance(node.value.op, ast.Div) \
                and isinstance(node.value.left, ast.Name) \
                and node.value.left.id in ("futures_price", "contract_price", "fut_price"):
            fixed = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "assert_levels_preserved":
            fixed = True
    return buggy, fixed


def check_proxy():
    section("שכבת הביצוע")
    if not PROXY.exists():
        say(WARN, f"לא מצאתי את {PROXY.name} בנתיב הרגיל — דלג אם עברת מקום")
        return
    try:
        src = PROXY.read_text(errors="ignore")
    except OSError as e:
        say(WARN, f"לא הצלחתי לקרוא: {e}")
        return

    verdict = _proxy_verdict(src)
    if verdict is None:
        say(WARN, "הקובץ לא נפרס כפייתון תקין — תבדוק ידנית")
        return
    buggy, fixed = verdict

    if buggy and fixed:
        say(WARN, "יש גם את התיקון וגם השמה פגומה שנשארה — תבדוק איזה מסלול באמת רץ")
        issues.append("להסיר את ההשמה הישנה מ-broker/proxy.py")
    elif buggy:
        say(BAD, "הבאג עדיין שם: ratio נגזר מ-entry, אז מחיר הכניסה מתבטל")
        issues.append("להחליף את ההמרה ב-broker/proxy.py לפי proxy_fix.py")
        nexts.append("זה חוסם הכל. עד שזה לא מתוקן, כל עסקה נכנסת במחיר השוק.")
    elif fixed:
        say(OK, "ההמרה מתוקנת (יחס מזוג ייחוס חי, עם אינווריאנטה)")
    else:
        say(WARN, "לא מצאתי לא את הבאג ולא את התיקון — תבדוק ידנית מול proxy_fix.py")


def check_integrity_installed():
    if INTEGRITY.exists():
        say(OK, "bot/integrity.py מותקן")
    else:
        say(BAD, "bot/integrity.py לא מותקן")
        issues.append(f"cp {HERE/'integrity.py'} '{INTEGRITY}'")


# ── 3. הרשומה ───────────────────────────────────────────────────

def check_db():
    section("רשומת העסקאות")
    if not DB.exists():
        say(WARN, f"אין {DB.name} עדיין — נורמלי לפני שהבוט רץ")
        nexts.append("אחרי שהבוט ירוץ, תריץ את doctor שוב.")
        return None
    con = sqlite3.connect(str(DB))
    def q(sql, d=0):
        try:
            return con.execute(sql).fetchone()[0]
        except sqlite3.Error:
            return d
    total = q("SELECT COUNT(*) FROM trades")
    closed = q("SELECT COUNT(*) FROM trades WHERE status='closed'")
    openn = q("SELECT COUNT(*) FROM trades WHERE status='open'")
    say(INFO, f"{total:,} עסקאות, {closed:,} סגורות, {openn:,} פתוחות")

    bad = 0
    for label, sql in (
        ("pnl_r ריק", "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r IS NULL"),
        ("0.0R עם רווח שאינו אפס",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r=0 AND pnl IS NOT NULL AND pnl<>0"),
        ("|pnl_r| מעל 10", "SELECT COUNT(*) FROM trades WHERE status='closed' AND ABS(pnl_r)>10"),
        ("כניסה=יציאה", "SELECT COUNT(*) FROM trades WHERE status='closed' AND entry=exit_price"),
        ("בלי analysis_id", "SELECT COUNT(*) FROM trades WHERE analysis_id IS NULL OR analysis_id=0"),
    ):
        n = q(sql)
        if n:
            say(BAD, f"{label}: {n}")
            bad += n
    con.close()
    if bad:
        issues.append("לתקן את הרשומות הפגומות לפני שסומכים על מספר כלשהו")
    elif closed:
        say(OK, "כל הרשומות הסגורות עוברות את בדיקות השלמות")
    return closed


# ── 4. השער ─────────────────────────────────────────────────────

def check_gate(closed):
    section("כמה חשבונות מותר")
    if not closed:
        say(INFO, "אין עסקאות סגורות. שלב מותר: 0 — אפס חשבונות.")
        nexts.append("שלב 1 נפתח אחרי 100 עסקאות נקיות עם גבול תחתון חיובי.")
        return
    if not have("numpy"):
        say(WARN, "numpy חסר, אי אפשר לחשב")
        return
    sys.path.insert(0, str(HERE))
    from gate import bootstrap_ci, load, permitted
    r = load(DB)
    if len(r) < 10:
        say(INFO, f"{len(r)} עסקאות — מעט מדי. שלב מותר: 0.")
        return
    lo, hi = bootstrap_ci(r)
    stage, acc, _, _ = permitted(len(r), lo)
    say(INFO, f"תוחלת {r.mean():+.3f}R, רווח סמך [{lo:+.3f}R, {hi:+.3f}R]")
    mark = OK if acc else WARN
    say(mark, f"שלב מותר: {stage} — עד {acc} חשבונות")
    if acc == 0:
        nexts.append("הראיות עדיין לא מצדיקות חשבון. להמשיך לאסוף.")


# ── 5. נתוני מחיר ───────────────────────────────────────────────

def check_bars():
    section("נתוני מחיר לאבחון הסטייה")
    setups = DESK / "setups.csv"
    bars = [DESK / f"{s}_5min.csv" for s in ("SPY", "QQQ")]
    if not setups.exists():
        say(WARN, "אין setups.csv — אי אפשר להריץ את אבחון הסטייה")
        return
    say(OK, "setups.csv קיים")
    missing = [b.name for b in bars if not b.exists()]
    if missing:
        say(WARN, f"חסרים נרות: {', '.join(missing)} — הרץ קודם את ibbars.py")
        return
    say(OK, "נרות SPY ו-QQQ קיימים")
    nexts.append(f"python3 {HERE/'drift_diagnostic.py'}   ← סוגר את השאלה הפתוחה האחרונה")


# ── 6. מה שדורש בני אדם ─────────────────────────────────────────

def check_external():
    section("מה שתלוי באחרים")
    say(INFO, "אישור בכתב מ-Apex על עותק פקודות אוטומטי — הסיכון היחיד שלא חסום בדמי הערכה")
    say(INFO, "רואה חשבון: סיווג ההכנסה. שווה $507,154 על פני שמונה שנים")
    say(INFO, f"שני המכתבים מוכנים ב-{HERE.parent/'references'/'verification-letters.md'}")


def main():
    print("\n" + "=" * 62)
    print("  prop-fleet — בדיקת מצב")
    print("=" * 62)
    check_env()
    check_proxy()
    check_integrity_installed()
    closed = check_db()
    check_gate(closed)
    check_bars()
    check_external()

    print("\n" + "=" * 62)
    if issues:
        print("  חוסם:")
        for i in issues:
            print(f"    ✗ {i}")
    else:
        print("  אין חוסמים.")
    if nexts:
        print("\n  הצעד הבא:")
        for n in nexts:
            print(f"    → {n}")
    print("=" * 62 + "\n")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
