#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
תיקון analysis_id — שורת הניתוח חייבת להיכתב לפני שליחת הפקודה.

הבאג
====
‏`bot/engine.py` שולח את הפקודה בשורה ~1288 (`_execute_signal`), ורק אחר כך,
בשורה ~1373, כותב את שורת הניתוח וזורק את המזהה שהיא מחזירה. לכן כשהעסקה
נכתבת ל-trades, שורת הניתוח שלה עוד לא קיימת, ‏`analysis_id` נשאר 0,
‏`integrity.validate_trade_record` פוסל אותו, והשורה מסומנת
‏`integrity_open_fail`. הוכחה מהמסד: עסקה 58 ב-09:30:50.037783,
שורת הניתוח שלה (3819) ב-09:30:50.563466 — חצי שנייה אחריה.

המשמעות: כל עסקה מכאן והלאה נפסלת, ושער חמש-העסקאות לא ייפתח לעולם.

התיקון
======
1. ‏`bot/decision.py` — שדה `analysis_id` ל-TradeSignal (‏`_record_journal_entry`
   כבר מצפה לו ב-getattr).
2. ‏`bot/engine.py` — בלוק "שלב 6" עובר מעל "שלב 5", תופס את המזהה שמחזירה
   ‏`log_analysis` ושם אותו על הסיגנל.
3. ‏`bot/engine.py` — שתי הקריאות ל-`register` מעבירות אותו הלאה.

מה נגרע: ‏`bracket_parent_id` ו-`bracket_status` יורדים מהפיילוד של הניתוח,
כי הברקט עדיין לא קיים כשהוא נכתב. הקישור לא אובד — ‏`trades.broker_order_id`
הוא בדיוק אותו `parent_id`.

מה מסתכן: כתיבה ל-SQLite נכנסת לפני שליחת הפקודה. במצב רגיל מילישניות.

הסקריפט מגבה, מוודא כל עוגן מילה במילה, מתקן, מהדר ומדפיס diff.
הוא **לא מפעיל את הבוט מחדש** ולא נוגע במסד הנתונים.
"""
from __future__ import annotations

import difflib
import py_compile
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

DEFAULT_BOT = Path.home() / "Desktop/meirox-ai/MeiroX-AI - בוט מסחר"

# ── העוגנים, מילה במילה מתוך הקוד שלו ─────────────────────────────

SIGNAL_FIELD_ANCHOR = (
    "    prices_are_etf:  bool = False      "
    "# True when ES/NQ prices came from SPY/QQQ proxies\n"
)

SIGNAL_FIELD_NEW = SIGNAL_FIELD_ANCHOR + (
    "    analysis_id:     int = 0           "
    "# 2026-09-24: analyses row id, set by the engine BEFORE\n"
    "                                       "
    "# the order is submitted. 0 = unknown (boot/replay).\n"
)

STEP5_ANCHOR = (
    "            # Step 5: Execute via broker (Day 7)\n"
    "            bracket = None\n"
    "            if signal.approved and self.broker:\n"
    "                bracket = self._execute_signal(signal)\n"
)

STEP6_BLOCK = (
    "\n"
    "            # Step 6: Log to journal\n"
    "            if self.journal:\n"
    "                try:\n"
    "                    log_payload = {**claude_result}\n"
    '                    log_payload["bias"] = result.bias\n'
    '                    log_payload["signal_approved"] = signal.approved\n'
    '                    log_payload["signal_reason"]   = signal.reason\n'
    '                    log_payload["quantity"]         = signal.quantity\n'
    "                    if bracket:\n"
    '                        log_payload["bracket_parent_id"] = bracket.parent_id\n'
    '                        log_payload["bracket_status"]    = bracket.status\n'
    '                    if pipe_result.get("checklist"):\n'
    '                        log_payload["checklist_summary"] = '
    'pipe_result["checklist"].summary()\n'
    "                    self.journal.log_analysis(\n"
    "                        market=symbol,\n"
    "                        kill_zone=result.kill_zone,\n"
    "                        analysis=log_payload,\n"
    "                    )\n"
    "                except Exception as e:\n"
    '                    logger.warning(f"[{symbol}] Journal write failed: {e}")\n'
)

STEP5A_NEW = (
    "            # Step 5a: write the analysis row BEFORE the order is submitted\n"
    "            # and carry its id on the signal.\n"
    "            #\n"
    "            # 2026-09-24: this block used to sit AFTER Step 5 (as 'Step 6'),\n"
    "            # and its return value was discarded. The trades row is written\n"
    "            # inside _execute_signal, so at that moment the analyses row did\n"
    "            # not exist yet and analysis_id was 0 — integrity.validate_trade_"
    "record\n"
    "            # rejected every such row and marked it integrity_open_fail.\n"
    "            # The id has to exist at INSERT time, so the analysis row has to\n"
    "            # exist before the order. Evidence: trade 58 at 09:30:50.037783,\n"
    "            # its analyses row 3819 at 09:30:50.563466 — half a second later.\n"
    "            #\n"
    "            # bracket_parent_id/bracket_status are gone from the payload: the\n"
    "            # bracket does not exist yet. trades.broker_order_id holds the same\n"
    "            # parent_id, so the analysis<->trade link survives from that side.\n"
    "            if self.journal:\n"
    "                try:\n"
    "                    log_payload = {**claude_result}\n"
    '                    log_payload["bias"] = result.bias\n'
    '                    log_payload["signal_approved"] = signal.approved\n'
    '                    log_payload["signal_reason"]   = signal.reason\n'
    '                    log_payload["quantity"]         = signal.quantity\n'
    '                    if pipe_result.get("checklist"):\n'
    '                        log_payload["checklist_summary"] = '
    'pipe_result["checklist"].summary()\n'
    "                    signal.analysis_id = int(\n"
    "                        self.journal.log_analysis(\n"
    "                            market=symbol,\n"
    "                            kill_zone=result.kill_zone,\n"
    "                            analysis=log_payload,\n"
    "                        ) or 0\n"
    "                    )\n"
    "                except Exception as e:\n"
    '                    logger.warning(f"[{symbol}] Journal write failed: {e}")\n'
    "\n"
) + STEP5_ANCHOR

REGISTER_OLD = (
    "trade_id = self.order_manager.register(bracket=bracket, signal=signal)"
)
# שתי הקריאות יושבות בעומקי הזחה שונים (12 ו-16 רווחים), ולכן ההחלפה
# קוראת את ההזחה מהשורה עצמה ולא מניחה אותה.
REGISTER_RE = re.compile(
    r"^([ \t]*)" + re.escape(REGISTER_OLD) + r"[ \t]*$", re.M
)
REGISTER_COUNT = 2


def _register_repl(m: "re.Match[str]") -> str:
    pad = m.group(1)
    inner = pad + "    "
    return (
        f"{pad}trade_id = self.order_manager.register(\n"
        f"{inner}bracket=bracket, signal=signal,\n"
        f'{inner}analysis_id=getattr(signal, "analysis_id", 0) or 0,\n'
        f"{pad})"
    )

# ── עזר ───────────────────────────────────────────────────────────


def die(msg: str) -> None:
    print(f"\n  ✗ {msg}")
    print("  שום קובץ לא שונה.")
    sys.exit(1)


def need(text: str, anchor: str, want: int, what: str) -> None:
    got = text.count(anchor)
    if got != want:
        die(f"{what}: ציפיתי ל-{want} מופעים, מצאתי {got}. "
            "הקוד השתנה מאז האבחון — עוצר.")


def first_assignment(text: str, name: str) -> int | None:
    """מספר התו שבו המשתנה מקבל ערך בפעם הראשונה, או None."""
    m = re.search(rf"^\s*{re.escape(name)}\s*=[^=]", text, re.M)
    return m.start() if m else None


def unified(old: str, new: str, name: str) -> str:
    return "".join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f"a/{name}", tofile=f"b/{name}", n=2,
    ))


def compiles(text: str, name: str) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8",
                                     delete=False) as fh:
        fh.write(text)
        tmp = fh.name
    try:
        py_compile.compile(tmp, doraise=True)
        return True, ""
    except py_compile.PyCompileError as exc:
        return False, str(exc).replace(tmp, name)
    finally:
        Path(tmp).unlink(missing_ok=True)


# ── הראשי ─────────────────────────────────────────────────────────


def main() -> int:
    bot = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_BOT
    engine = bot / "bot" / "engine.py"
    decision = bot / "bot" / "decision.py"

    print("=" * 62)
    print("  תיקון analysis_id — שורת הניתוח לפני הפקודה")
    print("=" * 62)
    print(f"  בוט: {bot}")

    for p in (engine, decision):
        if not p.is_file():
            die(f"לא מצאתי את {p}")

    eng_old = engine.read_text(encoding="utf-8")
    dec_old = decision.read_text(encoding="utf-8")

    # כבר מותקן?
    done_dec = "    analysis_id:     int = 0" in dec_old
    done_eng = "# Step 5a: write the analysis row BEFORE" in eng_old
    if done_dec and done_eng:
        print("\n  ✓ התיקון כבר מותקן בשני הקבצים. אין מה לעשות.")
        return 0
    if done_dec or done_eng:
        die("תיקון חלקי — קובץ אחד מתוקן והשני לא. "
            "שחזר מהגיבוי לפני שממשיכים.")

    # עוגנים
    need(dec_old, SIGNAL_FIELD_ANCHOR, 1, "decision.py: שורת prices_are_etf")
    need(eng_old, STEP5_ANCHOR, 1, "engine.py: בלוק שלב 5")
    need(eng_old, STEP6_BLOCK, 1, "engine.py: בלוק שלב 6")
    need(eng_old, REGISTER_OLD, REGISTER_COUNT, "engine.py: הקריאות ל-register")
    hits = REGISTER_RE.findall(eng_old)
    if len(hits) != REGISTER_COUNT:
        die(f"engine.py: הקריאות ל-register אינן כל אחת בשורה נפרדת "
            f"({len(hits)} מתוך {REGISTER_COUNT}) — עוצר.")

    # האם המשתנים שהפיילוד צריך מוגדרים לפני נקודת ההזזה?
    # אם לא — ההזזה תשתיק את רישום הניתוחים לגמרי, וזה גרוע מהבאג.
    step5_at = eng_old.index(STEP5_ANCHOR)
    print("\n  בדיקת מוקדמוּת — המשתנים שהפיילוד צריך:")
    for name in ("claude_result", "pipe_result", "result"):
        at = first_assignment(eng_old, name)
        if at is None:
            die(f"לא מצאתי השמה ל-{name} בכלל. עוצר.")
        line = eng_old.count("\n", 0, at) + 1
        if at >= step5_at:
            die(f"{name} מוגדר בשורה {line}, אחרי נקודת ההזזה. "
                "ההזזה תשבור את רישום הניתוחים — עוצר.")
        print(f"    ✓ {name} מוגדר בשורה {line}, לפני ההזזה")

    # הרכבה
    dec_new = dec_old.replace(SIGNAL_FIELD_ANCHOR, SIGNAL_FIELD_NEW, 1)
    eng_new = eng_old.replace(STEP6_BLOCK, "", 1)
    eng_new = eng_new.replace(STEP5_ANCHOR, STEP5A_NEW, 1)
    eng_new = REGISTER_RE.sub(_register_repl, eng_new)

    if eng_new.count("self.journal.log_analysis(") != 1:
        die("אחרי התיקון יש יותר מקריאה אחת ל-log_analysis — עוצר.")
    if eng_new.count(REGISTER_OLD) != 0:
        die("נשארה קריאה ל-register בלי analysis_id — עוצר.")
    if eng_new.count("analysis_id=getattr(signal") != REGISTER_COUNT:
        die("מספר הקריאות המתוקנות ל-register אינו 2 — עוצר.")

    # הידור לפני שנוגעים בדיסק
    print("\n  הידור:")
    for text, name in ((eng_new, "bot/engine.py"), (dec_new, "bot/decision.py")):
        ok, err = compiles(text, name)
        if not ok:
            die(f"{name} לא מתהדר אחרי התיקון:\n{err}")
        print(f"    ✓ {name}")

    # גיבוי וכתיבה
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    print("\n  גיבוי:")
    for p in (engine, decision):
        bak = p.with_suffix(f".py.bak-analysisid-{stamp}")
        shutil.copy2(p, bak)
        print(f"    ✓ {bak.name}")

    engine.write_text(eng_new, encoding="utf-8")
    decision.write_text(dec_new, encoding="utf-8")

    print("\n" + "=" * 62)
    print("  מה בדיוק השתנה")
    print("=" * 62)
    print(unified(dec_old, dec_new, "bot/decision.py"))
    print(unified(eng_old, eng_new, "bot/engine.py"))

    print("=" * 62)
    print("  הצעד הבא")
    print("=" * 62)
    print("  הסקריפט הזה לא הפעיל את הבוט מחדש בכוונה.")
    print("  קרא את ה-diff. אם הוא נראה נכון, הפעל מחדש:")
    print("    launchctl kickstart -k gui/$(id -u)/com.meiroxai.bot")
    print("  לשחזור: העתק בחזרה את קבצי ה-bak-analysisid שלמעלה.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
