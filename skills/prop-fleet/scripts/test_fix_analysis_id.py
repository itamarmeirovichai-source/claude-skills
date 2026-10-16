#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקות ל-fix_analysis_id.py.

הבדיקה המרכזית היא התנהגותית ולא טקסטואלית: בונים מנוע מדומה שמשחזר
את סדר הפעולות של הבוט (פקודה ואז ניתוח), מריצים את הסקריפט על הקוד
הזה ממש, ומריצים אותו שוב — ובודקים שסדר הקריאות התהפך ושהמזהה עבר.

לפני:  register(analysis_id=0)  ואז  log_analysis -> 3819
אחרי:  log_analysis -> 3819     ואז  register(analysis_id=3819)

זה בדיוק מה שהמסד שלו הראה: עסקה 58 עם analysis_id=0, ושורת הניתוח
3819 שנכתבה חצי שנייה אחריה.
"""
from __future__ import annotations

import subprocess
import sys

from pathlib import Path

HERE = Path(__file__).resolve().parent
PATCH = HERE / "fix_analysis_id.py"

DECISION = '''\
from dataclasses import dataclass, field
from typing import Optional

TRADEABLE_GRADES = {"A++", "A+", "A", "B"}   # B added (4/5 conditions) — traded at 0.5x size


@dataclass
class TradeSignal:
    """Final output of the Decision Engine."""
    approved:        bool
    symbol:          str
    quantity:        float
    grade:           str
    kill_zone:       Optional[str]
    timestamp:       str = ""
    reason:          str = ""
    warnings:        list[str] = field(default_factory=list)
    risk_check:      Optional[object] = None
    prices_are_etf:  bool = False      # True when ES/NQ prices came from SPY/QQQ proxies

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = "now"
'''

ENGINE = '''\
import logging
logger = logging.getLogger("meirox_bot")

CALLS = []


class Engine:
    def __init__(self, journal, order_manager, broker):
        self.journal = journal
        self.order_manager = order_manager
        self.broker = broker
        self._results = []

    def run_once(self, symbol):
        if True:
            pipe_result = {"checklist": None}
            claude_result = {"grade": "B"}
            result = type("R", (), {"bias": "bullish", "kill_zone": "am"})()
            from bot.decision import TradeSignal
            signal = TradeSignal(approved=True, symbol=symbol, quantity=1.0,
                                 grade="B", kill_zone="am")

            if signal.approved:
                logger.info(f"[{symbol}] APPROVED")

            # Step 5: Execute via broker (Day 7)
            bracket = None
            if signal.approved and self.broker:
                bracket = self._execute_signal(signal)
                _bad_statuses = {"error", "skipped"}

            # Step 6: Log to journal
            if self.journal:
                try:
                    log_payload = {**claude_result}
                    log_payload["bias"] = result.bias
                    log_payload["signal_approved"] = signal.approved
                    log_payload["signal_reason"]   = signal.reason
                    log_payload["quantity"]         = signal.quantity
                    if bracket:
                        log_payload["bracket_parent_id"] = bracket.parent_id
                        log_payload["bracket_status"]    = bracket.status
                    if pipe_result.get("checklist"):
                        log_payload["checklist_summary"] = pipe_result["checklist"].summary()
                    self.journal.log_analysis(
                        market=symbol,
                        kill_zone=result.kill_zone,
                        analysis=log_payload,
                    )
                except Exception as e:
                    logger.warning(f"[{symbol}] Journal write failed: {e}")

            self._results.append(result)
            return signal

    def _execute_signal(self, signal):
        bracket = type("B", (), {"parent_id": "98", "status": "pending"})()
        try:
            if bracket.parent_id.startswith("dry_"):
                trade_id = self.order_manager.register(bracket=bracket, signal=signal)
                self._record_journal_entry(signal, bracket, trade_id=trade_id)
                return bracket

            # Register with OrderManager for tracking (Day 8)
            trade_id = self.order_manager.register(bracket=bracket, signal=signal)
            self._record_journal_entry(signal, bracket, trade_id=trade_id)
            return bracket
        except Exception as e:
            logger.error("failed", exc_info=True)
            return None

    def _record_journal_entry(self, signal, bracket, trade_id=None):
        pass
'''

HARNESS = '''\
import json
import bot.engine as E


class Journal:
    def __init__(self):
        self.rows = 0

    def log_analysis(self, market, kill_zone, analysis):
        self.rows += 1
        aid = 3818 + self.rows
        E.CALLS.append(["log_analysis", aid])
        return aid


class OM:
    def register(self, bracket, signal=None, analysis_id: int = 0):
        E.CALLS.append(["register", analysis_id])
        return 59


sig = E.Engine(Journal(), OM(), broker=object()).run_once("ES")
print(json.dumps({"calls": E.CALLS,
                  "analysis_id": getattr(sig, "analysis_id", None)}))
'''


def _plant(root: Path) -> None:
    (root / "bot").mkdir(parents=True, exist_ok=True)
    (root / "bot" / "__init__.py").write_text("", encoding="utf-8")
    (root / "bot" / "decision.py").write_text(DECISION, encoding="utf-8")
    (root / "bot" / "engine.py").write_text(ENGINE, encoding="utf-8")
    (root / "harness.py").write_text(HARNESS, encoding="utf-8")


def _run(root: Path) -> dict:
    import json
    import shutil
    shutil.rmtree(root / "bot" / "__pycache__", ignore_errors=True)
    out = subprocess.run([sys.executable, "harness.py"], cwd=root,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def _patch(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(PATCH), str(root)],
                          capture_output=True, text=True)


def test_before_the_patch_the_bug_reproduces(tmp_path):
    _plant(tmp_path)
    got = _run(tmp_path)
    # זה בדיוק מה שקרה בשורה 58: הפקודה נרשמת עם 0, הניתוח נולד אחריה.
    assert got["calls"] == [["register", 0], ["log_analysis", 3819]]
    assert got["analysis_id"] is None


def test_after_the_patch_the_id_exists_before_the_order(tmp_path):
    _plant(tmp_path)
    assert _patch(tmp_path).returncode == 0
    got = _run(tmp_path)
    assert got["calls"] == [["log_analysis", 3819], ["register", 3819]]
    assert got["analysis_id"] == 3819


def test_the_id_passes_the_real_validator(tmp_path):
    """אין טעם בתיקון אם הוולידטור עדיין פוסל. מריצים את המאמת האמיתי."""
    sys.path.insert(0, str(HERE))
    import integrity

    try:
        integrity.validate_trade_record(
            symbol="SPYM", direction="short", analysis_id=0,
            entry=90.98, stop_loss=91.07, quantity=107.0, closing=False)
        raise AssertionError("analysis_id=0 היה אמור להיפסל")
    except integrity.IntegrityError:
        pass

    integrity.validate_trade_record(
        symbol="SPYM", direction="short", analysis_id=3819,
        entry=90.98, stop_loss=91.07, quantity=107.0, closing=False)


def test_running_twice_changes_nothing(tmp_path):
    _plant(tmp_path)
    assert _patch(tmp_path).returncode == 0
    first = (tmp_path / "bot" / "engine.py").read_text(encoding="utf-8")
    second = _patch(tmp_path)
    assert second.returncode == 0
    assert "כבר מותקן" in second.stdout
    assert (tmp_path / "bot" / "engine.py").read_text(encoding="utf-8") == first


def test_a_changed_anchor_aborts_without_touching_anything(tmp_path):
    _plant(tmp_path)
    eng = tmp_path / "bot" / "engine.py"
    eng.write_text(eng.read_text(encoding="utf-8").replace(
        "# Step 5: Execute via broker (Day 7)", "# Step 5: Execute via broker"),
        encoding="utf-8")
    before = eng.read_text(encoding="utf-8")
    res = _patch(tmp_path)
    assert res.returncode == 1
    assert "שום קובץ לא שונה" in res.stdout
    assert eng.read_text(encoding="utf-8") == before
    assert not list((tmp_path / "bot").glob("*.bak-analysisid-*"))


def test_aborts_if_the_payload_variables_come_too_late(tmp_path):
    """אם claude_result מוגדר רק אחרי נקודת ההזזה, ההזזה תשתיק את רישום
    הניתוחים לגמרי — וזה גרוע מהבאג עצמו. חייב לעצור."""
    _plant(tmp_path)
    eng = tmp_path / "bot" / "engine.py"
    t = eng.read_text(encoding="utf-8")
    t = t.replace('            claude_result = {"grade": "B"}\n', "")
    t = t.replace("            # Step 6: Log to journal\n",
                  '            claude_result = {"grade": "B"}\n'
                  "            # Step 6: Log to journal\n")
    eng.write_text(t, encoding="utf-8")
    before = eng.read_text(encoding="utf-8")
    res = _patch(tmp_path)
    assert res.returncode == 1
    assert "אחרי נקודת ההזזה" in res.stdout
    assert eng.read_text(encoding="utf-8") == before


def test_both_register_sites_keep_their_own_indentation(tmp_path):
    _plant(tmp_path)
    assert _patch(tmp_path).returncode == 0
    t = (tmp_path / "bot" / "engine.py").read_text(encoding="utf-8")
    assert t.count('analysis_id=getattr(signal, "analysis_id", 0) or 0,') == 2
    assert "register(bracket=bracket, signal=signal)" not in t
    # הקריאה העמוקה יותר (בתוך ה-dry_) מוזחת ב-16, הרדודה ב-12, ושורות
    # ההמשך של כל אחת חייבות ללכת אחרי ההזחה שלה ולא אחרי קבוע.
    deep = ("                trade_id = self.order_manager.register(\n"
            "                    bracket=bracket, signal=signal,\n"
            '                    analysis_id=getattr(signal, "analysis_id", 0) or 0,\n'
            "                )\n")
    shallow = ("            trade_id = self.order_manager.register(\n"
               "                bracket=bracket, signal=signal,\n"
               '                analysis_id=getattr(signal, "analysis_id", 0) or 0,\n'
               "            )\n")
    assert deep in t, "הקריאה בעומק 16 לא נבנתה לפי ההזחה שלה"
    assert shallow in t, "הקריאה בעומק 12 לא נבנתה לפי ההזחה שלה"


if __name__ == "__main__":
    import shutil
    import tempfile

    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        tmp = Path(tempfile.mkdtemp())
        try:
            fn(tmp)
            print(f"  ✓ {name}")
        except Exception as exc:                       # noqa: BLE001
            failures += 1
            print(f"  ✗ {name}: {exc}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n  {'הכול עבר' if not failures else str(failures) + ' נכשלו'}")
    sys.exit(1 if failures else 0)
