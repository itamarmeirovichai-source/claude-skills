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
    # הבאג הוא יחס המרה שהמכנה שלו הוא מחיר המכשיר הנסחר. חלוקה של entry
    # במשהו אחר (כמות, מספר חוזים) היא חשבון לגיטימי ולא התבנית הזאת.
    PRICEY = ("etf_price", "price", "market_price", "current_price",
              "last_price", "etf", "proxy_price", "spot")

    buggy = fixed = False
    for node in ast.walk(tree):
        # ratio = entry / etf_price   ->  מחיר הכניסה מתבטל
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp) \
                and isinstance(node.value.op, ast.Div) \
                and isinstance(node.value.left, ast.Name) \
                and isinstance(node.value.right, ast.Name) \
                and node.value.left.id == "entry" \
                and node.value.right.id.lower() in PRICEY:
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
    broken = []
    def q(sql, label=None):
        """המספר, או None אם השאילתה עצמה נפלה.

        קודם זה החזיר 0 על שגיאת SQL, וזה הפך כל בדיקה שבורה
        לבדיקה עוברת. בדיוק זה קרה כאן: הבדיקה חיפשה עמודה בשם
        entry בטבלה שבה העמודה נקראת entry_price, נפלה בשקט,
        החזירה 0, והדוח הכריז שהרשומות תקינות. בדיקה שלא רצה
        חייבת להיראות אחרת מבדיקה שעברה.
        """
        try:
            return con.execute(sql).fetchone()[0]
        except sqlite3.Error as e:
            if label:
                broken.append(f"{label}: {str(e)[:60]}")
            return None
    total = q("SELECT COUNT(*) FROM trades", "ספירה") or 0
    closed = q("SELECT COUNT(*) FROM trades WHERE status='closed'", "סגורות") or 0
    openn = q("SELECT COUNT(*) FROM trades WHERE status='open'", "פתוחות") or 0
    # סטטוס שנכתב כשהסגירה לא אומתה: הפוזיציה כבר לא קיימת, אבל מחיר
    # היציאה האמיתי לא ידוע. זו לא חשיפה חיה, וזו גם לא ראיה. היא
    # נספרת בנפרד כי היא לא 'closed' ולא 'open', ובלי השורה הזאת היא
    # פשוט נעלמת מהדוח.
    unver = q("SELECT COUNT(*) FROM trades WHERE status='unverified'",
              "לא מאומתות") or 0
    say(INFO, f"{total:,} עסקאות, {closed:,} סגורות, {openn:,} פתוחות")
    if unver:
        say(WARN, f"{unver:,} לא מאומתות — לא נכנסות לסטטיסטיקה ולא חשיפה חיה")

    # מחיר הכניסה בקנה המידה שבו נמדד מחיר היציאה. exec_entry הוא
    # מחיר הביצוע; entry_price הוא הרמה מהאסטרטגיה. ברשומות ישנות
    # exec_entry ריק, ושם entry_price הוא הדבר היחיד שיש. להשוות
    # entry_price ל-exit_price כששניהם בקני מידה שונים זה להשוות
    # מחיר חוזה למחיר ETF ולקבל תשובה חסרת משמעות.
    try:
        cols = {r[1] for r in con.execute("PRAGMA table_info(trades)")}
    except sqlite3.Error:
        cols = set()
    if "exec_entry" in cols:
        EXEC_ENTRY = "COALESCE(exec_entry, entry_price)"
    else:
        # העמודה טרם נוספה. אפשר עדיין להשוות, אבל רק בקנה מידה של
        # האסטרטגיה, ובמצב מניות זה משווה מחיר ETF לרמת חוזה. זה
        # נאמר בקול במקום להיחשב לבדיקה שעברה.
        EXEC_ENTRY = "entry_price"
        say(WARN, "אין exec_entry — בדיקת כניסה=יציאה חלשה יותר, "
                  "והיא לא תופסת ערבוב קני מידה")

    bad = 0
    checks = (
        ("pnl_r ריק",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r IS NULL"),
        ("0.0R עם רווח שאינו אפס",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND pnl_r=0 "
         "AND pnl IS NOT NULL AND pnl<>0"),
        ("|pnl_r| מעל 10",
         "SELECT COUNT(*) FROM trades WHERE status='closed' AND ABS(pnl_r)>10"),
        # סתירה: אותו מחיר בשני הקצוות, ובכל זאת נרשם רווח או הפסד.
        ("כניסה=יציאה עם רווח שאינו אפס",
         f"SELECT COUNT(*) FROM trades WHERE status='closed' "
         f"AND {EXEC_ENTRY}=exit_price AND pnl IS NOT NULL AND pnl<>0"),
        # לא סתירה אלא טביעת אצבע: סגירה שנכתבה כ'איפוס' — יציאה
        # שהועתקה מהכניסה ורווח אפס — כלומר מחיר היציאה לא נמדד.
        ("כניסה=יציאה עם אפס — סגירה לא מאומתת שנרשמה כסגורה",
         f"SELECT COUNT(*) FROM trades WHERE status='closed' "
         f"AND {EXEC_ENTRY}=exit_price AND (pnl IS NULL OR pnl=0)"),
        *((("מסומנות ככשל שלמות",
            "SELECT COUNT(*) FROM trades WHERE exit_reason LIKE 'integrity_%'"),)
          if "exit_reason" in cols else ()),
        ("בלי analysis_id",
         "SELECT COUNT(*) FROM trades WHERE analysis_id IS NULL OR analysis_id=0"),
    )
    for label, sql in checks:
        n = q(sql, label)
        if n:
            say(BAD, f"{label}: {n}")
            bad += n
    con.close()

    # בדיקה שנפלה היא לא בדיקה שעברה. כל עוד היא לא רצה, אי אפשר
    # לטעון שהרשומות נקיות — וזה בדיוק מה שהדוח הזה טען קודם.
    if broken:
        for b in broken:
            say(BAD, f"הבדיקה עצמה נפלה — {b}")
        issues.append("בדיקת שלמות לא רצה בכלל. לתקן אותה לפני שסומכים על הדוח.")
    if bad:
        issues.append("לתקן את הרשומות הפגומות לפני שסומכים על מספר כלשהו")
    elif closed and not broken:
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
    say(INFO, "עידן ה-ETF (27/02–15/05) אובחן: פיגור של כ-15 ימי לוח, שוקת 2.69")
    if not (DESK / "futures_era_ETF.csv").exists():
        say(WARN, "עידן החוזים (18/05 ואילך, 131 סטאפים) עדיין לא נבדק")
        nexts.append(f"python3 {HERE/'futures_era_check.py'}   ← קובע מאיזה תאריך הנתונים תקפים")
        return
    say(OK, "עידן החוזים נבדק — 131 סטאפים תקפים מ-18/05")

    # הנתיב מהסטאפים התקפים לתשובה: נרות חמש דקות, ואז ריפליי.
    clean = [DESK / f"{s}_5min_clean.csv" for s in ("ES", "NQ")]
    if not any(c.exists() for c in clean):
        say(WARN, "אין נרות חמש דקות לחלון הנקי — בלעדיהם אין בקטסט")
        nexts.append(f"python3 {HERE/'futures_bars.py'}   ← דורש IB Gateway על 4002")
        return
    say(OK, f"נרות חמש דקות: {', '.join(c.name for c in clean if c.exists())}")
    if (DESK / "replay_results.csv").exists():
        say(OK, "הריפליי רץ — ראה replay_results.csv")
    else:
        say(WARN, "הסטאפים התקפים עדיין לא שוחזרו")
        nexts.append(f"python3 {HERE/'replay.py'}   ← התוחלת האמיתית, 131 סטאפים במקום 7 עסקאות")


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
