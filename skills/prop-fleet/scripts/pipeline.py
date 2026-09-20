#!/usr/bin/env python3
"""
pipeline.py — פקודה אחת: לתקן, למדוד, ולהגיד מה יצא.

למה זה קיים
-----------
כל מחזור עד כה דרש ממנו לתקן ידנית, להעתיק ידנית, לשלוף ידנית, ואז
להריץ ריפליי ולזכור להעביר את נתיב הבוט לשניים מהשלבים. כל אחד
מהשלבים האלה הוא מקום להישמט, וההישמטות לא צועקות — הן פשוט מחזירות
מספר שנראה בסדר גמור.

כאן זה שלב אחד שנעצר בעצמו. ריפליי על נרות ישנים מדווח תוצאה שנראית
תקינה ואין בה שום סימן לכך שהיא מתארת את השליפה של אתמול, ולכן אם
השליפה לא ייצרה נרות — אין ריפליי.

מה זה כן נוגע בו
----------------
שני דברים בלבד:

  broker/proxy.py  — שורה אחת לכל אתר שבו היחס נגזר ממחיר הכניסה.
  bot/integrity.py — העתקה. קובץ חדש, לא נגיעה בקיים.

מה זה לעולם לא נוגע בו
----------------------
strategy/ על כל תוכנו, פרמטרי סיכון, גודל פוזיציה, bot/logger.py,
broker/ibkr.py. הוא לא מריץ את הבוט ולא שולח שום פקודה לברוקר.
logger.py ו-ibkr.py נמצאים באמצע עבודה של הסוכן המקומי, וטלאי עיוור
עליהם היה מתנגש איתה.

שימוש
-----
    python3 pipeline.py                      # מתקן, מודד, מסכם
    python3 pipeline.py '/נתיב/לבוט'
    python3 pipeline.py --dry-run            # מראה מה היה משתנה, לא נוגע
    python3 pipeline.py --measure-only       # רק מודד, בלי לתקן

גיבוי נלקח לפני כל כתיבה, תמיד, גם ב---dry-run אין כתיבה בכלל.
שלב השליפה דורש IB Gateway פתוח על 4002.
"""

import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path

D = Path.home() / "Desktop"
BOT_DEFAULT = D / "meirox-ai" / "MeiroX-AI - בוט מסחר"
HERE = Path(__file__).resolve().parent
BARS = ("ES", "NQ")

OK, BAD, WARN, INFO = "  ✓", "  ✗", "  !", "  ·"
blocking: list = []


def say(mark, text):
    print(f"{mark} {text}")


def banner(text: str) -> None:
    print(f"\n{'=' * 62}\n  {text}\n{'=' * 62}")


# ── גיבוי ────────────────────────────────────────────────────────

def backup(bot: Path) -> Path:
    """עותק מתוארך של כל מה שעלול להשתנות, לפני שמשהו משתנה.

    הגיבוי נלקח גם כשבסוף לא נכתב כלום. עותק מיותר עולה מגה־בייט;
    כתיבה בלי עותק עולה את הרשומה.
    """
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = bot / f"_pipeline_backup-{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    for rel in ("broker/proxy.py", "logs/trades.db", "bot/integrity.py"):
        src = bot / rel
        if src.exists():
            out = dest / rel.replace("/", "_")
            shutil.copy2(src, out)
            say(OK, f"גובה: {rel}  ->  {out.name}")
    return dest


# ── באג ההמרה ────────────────────────────────────────────────────

_DEMO = ("buggy", "demo", "old", "before", "wrong")
_PRICEY = ("etf_price", "price", "market_price", "current_price",
           "last_price", "etf", "proxy_price", "spot")
_FUT = ("futures_price", "contract_price", "fut_price", "future_price",
        "underlying_price", "ref_price")


def buggy_sites(src: str) -> list:
    """אתרים שבהם היחס נגזר ממחיר הכניסה, עם ההקשר הדרוש לתיקון.

    ast ולא חיפוש טקסט: ה-docstring של proxy_fix.py מצטט את הבאג כדי
    להסביר אותו, וחיפוש מחרוזות מסמן את הקובץ המתוקן כפגום.

    לכל אתר נבדק גם אילו שמות זמינים בתוך אותה פונקציה, כי בלי מחיר
    חוזה חי בתחום אין ממה לגזור את היחס הנכון — ואז אסור לגעת.
    """
    tree = ast.parse(src)
    owner, scope = {}, {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        names = {a.arg for a in fn.args.args} | {a.arg for a in fn.args.kwonlyargs}
        for sub in ast.walk(fn):
            if isinstance(sub, ast.Assign):
                names |= {t.id for t in sub.targets if isinstance(t, ast.Name)}
            if hasattr(sub, "lineno"):
                owner[sub.lineno] = fn.name
        scope[fn.name] = names

    hits = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.BinOp)
                and isinstance(node.value.op, ast.Div)
                and isinstance(node.value.left, ast.Name)
                and isinstance(node.value.right, ast.Name)
                and node.value.left.id == "entry"
                and node.value.right.id.lower() in _PRICEY):
            continue
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if any(t.lower().startswith(_DEMO) for t in targets):
            continue
        fn = owner.get(node.lineno)
        avail = scope.get(fn, set())
        hits.append({
            "line": node.lineno,
            "target": targets[0] if targets else "?",
            "denom": node.value.right.id,
            "func": fn,
            "futures_name": next((f for f in _FUT if f in avail), None),
        })
    return hits


def patch_proxy(path: Path, apply: bool) -> dict:
    """מחליף את מקור היחס ממחיר הכניסה למחיר חוזה חי.

    זה השינוי היחיד שנעשה בקוד שלו, והוא שורה אחת לכל אתר.

    אם אין מחיר חוזה בתחום — עוצר ומדווח. תיקון שממציא משתנה שלא
    קיים הופך באג שקט לקריסה בזמן שליחת פקודה, וזה גרוע יותר מהבאג.
    """
    src = path.read_text(encoding="utf-8")
    try:
        hits = buggy_sites(src)
    except SyntaxError as e:
        return {"status": "blocked", "hits": [], "why": f"הקובץ לא מתפרסר: {e}"}
    if not hits:
        return {"status": "clean", "hits": []}

    if any(not h["futures_name"] for h in hits):
        return {"status": "blocked", "hits": hits,
                "why": "אין מחיר חוזה חי בתחום הפונקציה — התיקון דורש אותו"}

    lines = src.splitlines(keepends=True)
    for h in hits:
        i, old = h["line"] - 1, lines[h["line"] - 1]
        new = old
        for a, b in ((f"entry / {h['denom']}", f"{h['futures_name']} / {h['denom']}"),
                     (f"entry/{h['denom']}", f"{h['futures_name']}/{h['denom']}")):
            if a in old:
                new = old.replace(a, b, 1)
                break
        if new == old:
            return {"status": "blocked", "hits": hits,
                    "why": f"שורה {h['line']} לא תואמת את התבנית המילולית"}
        h["before"], h["after"] = old.strip(), new.strip()
        lines[i] = new

    patched = "".join(lines)
    # אימות אחרי: אם נשאר אתר פגום, לא כותבים כלום.
    if buggy_sites(patched):
        return {"status": "blocked", "hits": hits,
                "why": "אחרי התיקון נשאר אתר פגום — לא כותב"}
    if apply:
        path.write_text(patched, encoding="utf-8")
    return {"status": "patched" if apply else "would_patch", "hits": hits}


def step_proxy(bot: Path, apply: bool) -> None:
    banner("שלב 1 — באג המרת הרמות")
    path = bot / "broker" / "proxy.py"
    if not path.exists():
        say(WARN, f"אין {path.relative_to(bot)} — מדלג")
        return
    r = patch_proxy(path, apply)
    if r["status"] == "clean":
        say(OK, "היחס כבר לא נגזר ממחיר הכניסה")
        return
    for h in r["hits"]:
        say(INFO, f"שורה {h['line']} ב-{h['func']}(): "
                  f"{h['target']} = entry / {h['denom']}")
        if h.get("before"):
            print(f"        לפני:  {h['before']}")
            print(f"        אחרי:  {h['after']}")
    if r["status"] == "blocked":
        say(BAD, f"לא נגעתי: {r.get('why', 'תבנית לא מוכרת')}")
        say(INFO, f"התיקון הנכון מיושם ב-{HERE / 'proxy_fix.py'}")
        blocking.append("באג ההמרה עדיין חי — כל פקודה יוצאת בשוק")
    elif r["status"] == "would_patch":
        say(WARN, "זו הרצת יובש. להריץ בלי --dry-run כדי לכתוב.")
        blocking.append("באג ההמרה עדיין חי (הרצת יובש)")
    else:
        say(OK, f"תוקן {len(r['hits'])} אתר. היחס נגזר עכשיו מזוג ייחוס חי.")


# ── התקנת המאמת ──────────────────────────────────────────────────

def step_integrity(bot: Path, apply: bool) -> None:
    banner("שלב 2 — מאמת נתיב הכתיבה")
    dest = bot / "bot" / "integrity.py"
    src = HERE / "integrity.py"
    if dest.exists() and dest.read_bytes() == src.read_bytes():
        say(OK, "bot/integrity.py מותקן ומעודכן")
    elif not apply:
        say(WARN, f"היה מעתיק {src.name} -> {dest.relative_to(bot)}")
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        say(OK, f"הועתק -> {dest.relative_to(bot)}")

    # החיווט עצמו לא נעשה כאן. logger.py נמצא באמצע עבודה של הסוכן
    # המקומי, וטלאי עיוור עליו היה מתנגש. נאמר בקול במקום להיעשות
    # בשקט או להישכח.
    logger = bot / "bot" / "logger.py"
    wired = logger.exists() and "integrity" in logger.read_text(
        encoding="utf-8", errors="replace")
    if wired:
        say(OK, "logger.py כבר מייבא את המאמת")
    else:
        say(WARN, "logger.py עוד לא קורא לו — זו עבודה של הסוכן המקומי, "
                  "לא של הסקריפט הזה")


# ── מדידה ────────────────────────────────────────────────────────

def stamp(sym: str):
    """גודל וזמן שינוי של קובץ הנרות, כדי לדעת אם הוא באמת התחדש."""
    p = D / f"{sym}_5min_clean.csv"
    if not p.exists():
        return None
    st = p.stat()
    return (st.st_size, int(st.st_mtime))


def step_measure(bot: Path) -> bool:
    banner("שלב 3 — נרות חמש דקות מ-IBKR")
    before = {s: stamp(s) for s in BARS}
    sys.path.insert(0, str(HERE))
    import futures_bars
    futures_bars.BOT = bot
    try:
        futures_bars.main()
    except SystemExit as e:
        if e.code:
            say(BAD, f"השליפה נעצרה: {e}")
            blocking.append("אין נרות — IB Gateway על 4002?")
            return False
    except Exception as e:
        say(BAD, f"השליפה נכשלה: {type(e).__name__}: {str(e)[:120]}")
        blocking.append("שליפת הנרות נכשלה")
        return False

    after = {s: stamp(s) for s in BARS}
    if not any(after.values()):
        say(BAD, "אין קובצי נרות בכלל")
        blocking.append("אין נרות בכלל")
        return False
    fresh = [s for s in BARS if after[s] and after[s] != before[s]]
    kept = [s for s in BARS if after[s] and after[s] == before[s]]
    if fresh:
        say(OK, f"התחדשו: {', '.join(fresh)}")
    if kept:
        # לא שגיאה — אבל צריך להיאמר, כי ריפליי על נרות מאתמול נראה
        # בדיוק כמו ריפליי על נרות מהיום.
        say(WARN, f"לא השתנו: {', '.join(kept)} — הריפליי ירוץ עליהם כמו שהם")

    banner("שלב 4 — ריפליי הסטאפים הנקיים")
    sys.argv = [sys.argv[0], str(bot)]
    import replay
    replay.main()
    return True


def step_verdict(bot: Path) -> None:
    banner("שלב 5 — מה מותר עכשיו")
    sys.path.insert(0, str(HERE))
    import doctor
    doctor.HOME = bot
    try:
        doctor.main()
    except SystemExit:
        pass
    except Exception as e:
        say(WARN, f"doctor לא רץ: {type(e).__name__}: {str(e)[:80]}")


def main() -> None:
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bot = Path(args[0]) if args else BOT_DEFAULT
    if not bot.exists():
        sys.exit(f"לא מצאתי את תיקיית הבוט:\n  {bot}")
    dry = "--dry-run" in flags
    apply = not dry
    print(f"בוט: {bot}")
    if dry:
        print("הרצת יובש — שום קובץ לא ייכתב.")

    if "--measure-only" not in flags:
        banner("שלב 0 — גיבוי")
        if apply:
            backup(bot)
        else:
            say(INFO, "הרצת יובש, אין מה לגבות")
        step_proxy(bot, apply)
        step_integrity(bot, apply)

    measured = step_measure(bot)
    if measured:
        step_verdict(bot)

    banner("סיכום")
    if blocking:
        for b in blocking:
            say(BAD, b)
        print("\n  כל עוד אחד מאלה פתוח, המספר למעלה לא מתאר את הבוט.")
    else:
        say(OK, "אין חוסם. המספר שלמעלה הוא המדידה.")
    print("\n  להעתיק את כל הפלט הזה ולשלוח אותו חזרה.")


if __name__ == "__main__":
    main()
