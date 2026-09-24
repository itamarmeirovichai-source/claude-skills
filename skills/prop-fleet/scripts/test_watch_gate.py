#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקות לדוח היומי.

שתי הטעויות שהדוח הזה יכול לעשות חמורות בכיוונים הפוכים: לשתוק
כשהבוט מת, או להדליף את טוקן הטלגרם אל תוך קובץ שיושב על שולחן
העבודה. שתיהן מכוסות כאן.
"""
from __future__ import annotations

import sqlite3
import subprocess
import sys

from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from watch_gate import (STALE_HOURS, build_report,  # noqa: E402
                        find_telegram, todays_decisions)

SCHEMA = """
CREATE TABLE trades (
    id INTEGER PRIMARY KEY, analysis_id INTEGER, timestamp TEXT,
    market TEXT, direction TEXT, status TEXT,
    entry_price REAL, stop_loss REAL, take_profit_1 REAL,
    exec_entry REAL, exec_stop_loss REAL, exec_take_profit REAL,
    exit_price REAL, pnl REAL, pnl_r REAL
)
"""
NO_DEC = {"scans": 0, "approved": 0, "placed": 0, "cap": False, "alive": False}


def rows(*specs):
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.execute(SCHEMA)
    for i, spec in enumerate(specs, 1):
        base = dict(id=i, analysis_id=3820 + i, timestamp="2026-09-25",
                    market="ES", direction="short", status="closed",
                    entry_price=100.0, stop_loss=101.0, take_profit_1=98.0,
                    exec_entry=1.0, exec_stop_loss=1.01, exec_take_profit=0.98,
                    exit_price=0.98, pnl=2.0, pnl_r=1.7)
        base.update(spec)
        keys = ",".join(base)
        con.execute(f"INSERT INTO trades ({keys}) "
                    f"VALUES ({','.join('?' * len(base))})",
                    tuple(base.values()))
    return list(con.execute("SELECT * FROM trades ORDER BY id"))


# ── האם המכונה חיה ────────────────────────────────────────────────

def test_a_stale_log_is_reported_as_a_dead_bot():
    r = build_report([], NO_DEC, STALE_HOURS + 1, "25/09 16:20")
    assert "הבוט כנראה מת" in r
    assert "kickstart" in r, "חייב לומר מה לעשות, לא רק שנפל"


def test_a_sleeping_bot_between_sessions_is_not_an_alarm():
    """הבוט ישן 17 שעות בין מושבים. זה תקין ואסור שייראה ככשל."""
    r = build_report([], NO_DEC, 17.0, "25/09 16:20")
    assert "הבוט חי" in r and "מת" not in r


def test_no_log_at_all_is_the_loudest_case():
    r = build_report([], NO_DEC, None, "25/09 16:20")
    assert "הוא לא רץ" in r


# ── המונה ─────────────────────────────────────────────────────────

def test_the_counter_only_counts_comparable_trades():
    r = build_report(rows({}, {}, {"exec_entry": None}), NO_DEC, 1.0, "x")
    assert "מונה הראיות: 2/5" in r, r


def test_nothing_since_the_cutoff_says_the_counter_did_not_move():
    r = build_report(rows({"timestamp": "2026-09-23"}), NO_DEC, 1.0, "x")
    assert "המונה לא זז" in r
    assert "מחוץ לפסק הדין" in r


def test_five_clean_trades_open_the_gate():
    r = build_report(rows({}, {}, {}, {}, {}), NO_DEC, 1.0, "x")
    assert "תנאי השער מתקיים" in r


# ── כשלים ─────────────────────────────────────────────────────────

def test_a_new_orphan_is_named_and_blocks():
    r = build_report(rows({"analysis_id": 0}), NO_DEC, 1.0, "x")
    assert "תיקון סדר הרישום לא עבד" in r
    assert "אין לקנות חשבון" in r


def test_a_split_conversion_ratio_blocks():
    r = build_report(rows({"exec_entry": 100.0}), NO_DEC, 1.0, "x")
    assert "חתימת באג ההמרה" in r
    assert "אין לקנות חשבון" in r


def test_five_trades_with_one_broken_do_not_open_the_gate():
    """המונה מלא אבל יש כשל. השער חייב להישאר סגור."""
    r = build_report(rows({}, {}, {}, {}, {}, {"analysis_id": 0}),
                     NO_DEC, 1.0, "x")
    assert "תנאי השער מתקיים" not in r
    assert "אין לקנות חשבון" in r


# ── הסוד ──────────────────────────────────────────────────────────

def test_the_token_never_reaches_the_report(tmp_path):
    """הדוח נכתב לשולחן העבודה ונשלח בהודעה. אסור שהטוקן יהיה בו."""
    secret = "7654321:AAHfakefaketokenvaluenotreal"
    env = tmp_path / ".env"
    env.write_text(f"TELEGRAM_BOT_TOKEN={secret}\nTELEGRAM_CHAT_ID=12345\n",
                   encoding="utf-8")
    token, chat = find_telegram([env])
    assert token == secret and chat == "12345"
    r = build_report(rows({}), NO_DEC, 1.0, "x")
    assert secret not in r and "TOKEN" not in r


def test_the_variable_names_are_matched_by_pattern_not_guessed(tmp_path):
    """אני לא יודע איך הוא קרא להם אצלו, ולכן זה תבנית ולא ניחוש."""
    env = tmp_path / ".env"
    env.write_text('export MEIROX_TELEGRAM_API_TOKEN="abc:123"  # הבוט\n'
                   "MEIROX_TELEGRAM_CHAT='999'\n", encoding="utf-8")
    assert find_telegram([env]) == ("abc:123", "999")


def test_missing_credentials_are_not_an_error(tmp_path):
    env = tmp_path / ".env"
    env.write_text("SOMETHING_ELSE=1\n", encoding="utf-8")
    assert find_telegram([env, tmp_path / "nope"]) == (None, None)


# ── קצה לקצה ──────────────────────────────────────────────────────

def test_it_runs_against_a_real_directory_and_writes_the_file(tmp_path):
    bot = tmp_path / "bot"
    (bot / "logs").mkdir(parents=True)
    con = sqlite3.connect(str(bot / "logs" / "trades.db"))
    con.execute(SCHEMA)
    con.execute("INSERT INTO trades (id,analysis_id,timestamp,market,"
                "direction,status,entry_price,stop_loss,take_profit_1,"
                "exec_entry,exec_stop_loss,exec_take_profit,exit_price,pnl) "
                "VALUES (1,0,'2026-09-25','ES','short','cancelled',"
                "100.0,101.0,98.0,NULL,1.01,0.98,0.98,0.0)")
    con.commit()
    con.close()
    (bot / "logs" / "bot.log").write_text("hello\n", encoding="utf-8")
    out = tmp_path / "status.txt"
    res = subprocess.run([sys.executable, str(HERE / "watch_gate.py"),
                          str(bot)],
                         capture_output=True, text=True,
                         env={**__import__("os").environ,
                              "PF_STATUS_OUT": str(out)})
    assert res.returncode == 0, res.stderr
    assert out.exists()
    body = out.read_text(encoding="utf-8")
    assert "prop-fleet" in body
    assert "תיקון סדר הרישום לא עבד" in body, body


def test_the_log_scan_counts_only_todays_lines(tmp_path):
    log = tmp_path / "bot.log"
    log.write_text(
        "2026-09-24 09:25 | [Engine] run_once — x\n"
        "2026-09-25 09:25 | [Engine] run_once — x\n"
        "2026-09-25 09:30 | [Decision] ✅ APPROVED ES short\n"
        "2026-09-25 09:30 | [ES] 📤 Order submitted (LIVE): x\n"
        "2026-09-25 09:36 | [Engine] Daily trade cap hit — 1/1\n",
        encoding="utf-8")
    d = todays_decisions(log, "2026-09-25")
    assert d == {"scans": 1, "approved": 1, "placed": 1,
                 "cap": True, "alive": True}


if __name__ == "__main__":
    import shutil
    import tempfile
    fails = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        tmp = Path(tempfile.mkdtemp())
        try:
            fn(tmp) if fn.__code__.co_argcount else fn()
            print(f"  ✓ {name}")
        except Exception as exc:                             # noqa: BLE001
            fails += 1
            print(f"  ✗ {name}: {exc}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n  {'הכול עבר' if not fails else str(fails) + ' נכשלו'}")
    sys.exit(1 if fails else 0)
