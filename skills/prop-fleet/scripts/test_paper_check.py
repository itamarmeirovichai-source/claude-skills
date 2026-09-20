#!/usr/bin/env python3
"""בדיקות לבדיקת נתיב הביצוע.

הטעות שהבדיקה הזאת קיימת בשבילה היא טעות שכבר קרתה: באג ההמרה עבר
חודשים בלי שאיש יראה אותו, כי כל רמה בנפרד הייתה מחיר סביר. לכן כל
בדיקה כאן בונה שורה שנראית תקינה לגמרי בעין ונופלת רק על היחס.
"""

import sqlite3

import pytest

from paper_check import REL_TOL, ratios, verdict_for

SCHEMA = """
CREATE TABLE trades (
    id INTEGER PRIMARY KEY, analysis_id INTEGER, timestamp TEXT,
    market TEXT, direction TEXT, status TEXT,
    entry_price REAL, stop_loss REAL, take_profit_1 REAL,
    exec_entry REAL, exec_stop_loss REAL, exec_take_profit REAL,
    exit_price REAL, pnl REAL, pnl_r REAL
)
"""


def row(**kw):
    """שורה אמיתית מ-sqlite, כדי ש-row['x'] יתנהג כמו בייצור."""
    base = dict(id=1, analysis_id=7, timestamp="2026-09-21", market="ES",
                direction="long", status="closed",
                entry_price=5000.0, stop_loss=4990.0, take_profit_1=5020.0,
                exec_entry=500.0, exec_stop_loss=499.0, exec_take_profit=502.0,
                exit_price=502.0, pnl=20.0, pnl_r=2.0)
    base.update(kw)
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.execute(SCHEMA)
    keys = ",".join(base)
    con.execute(f"INSERT INTO trades ({keys}) "
                f"VALUES ({','.join('?' * len(base))})", tuple(base.values()))
    return con.execute("SELECT * FROM trades").fetchone()


def test_a_clean_conversion_scales_every_level_by_one_ratio():
    ok, why = verdict_for(row())
    assert ok is True, why


def test_futures_mode_passes_with_every_ratio_at_one():
    """אין המרה — הרמות זהות, וזה יחס אחיד לגמרי תקין."""
    ok, why = verdict_for(row(exec_entry=5000.0, exec_stop_loss=4990.0,
                              exec_take_profit=5020.0))
    assert ok is True, why


def test_the_conversion_bug_is_caught_even_though_every_price_is_plausible():
    """החתימה המדויקת של הבאג.

    ratio = entry / etf_price, ואז proxy_entry מתכווץ למחיר ה-ETF
    בזמן השליחה בעוד הסטופ והיעד מומרים נכון. כאן ה-ETF נסחר ב-505
    כשהכניסה המתוכננת הייתה שקולה ל-500. כל מספר בשורה הוא מחיר
    שוק אמיתי ובטווח סביר — בדיקת טווח לא תראה כאן כלום. רק היחס
    בין שלוש הרמות מפריד ביניהן.
    """
    ok, why = verdict_for(row(exec_entry=505.0))
    assert ok is False
    assert "נחלקות" in why


def test_a_small_rounding_difference_is_not_a_bug():
    """round(..., 4) משאיר רעש. אזעקת שווא מאמנת להתעלם."""
    ok, _ = verdict_for(row(exec_stop_loss=499.0 * (1 + REL_TOL / 3)))
    assert ok is True


def test_a_real_divergence_just_above_the_tolerance_is_a_bug():
    ok, _ = verdict_for(row(exec_stop_loss=499.0 * (1 + REL_TOL * 5)))
    assert ok is False


def test_one_comparable_level_is_unknown_not_a_pass():
    """שורה שאי אפשר להשוות בה היא לא שורה שעברה.

    לספור 'לא נבדק' כ'תקין' זה בדיוק איך שהבאג המקורי שרד: כל בדיקה
    שלא רצה נראתה כמו בדיקה שעברה.
    """
    ok, why = verdict_for(row(exec_stop_loss=None, exec_take_profit=None))
    assert ok is None
    assert "אי אפשר" in why


def test_a_zero_signal_level_does_not_divide_by_zero():
    ok, _ = verdict_for(row(entry_price=0.0, stop_loss=0.0))
    assert ok is None


def test_a_negative_ratio_is_rejected(monkeypatch):
    ok, why = verdict_for(row(exec_entry=-500.0, exec_stop_loss=-499.0,
                              exec_take_profit=-502.0))
    assert ok is False
    assert "לא חיובי" in why


def test_ratios_reports_only_the_levels_that_exist():
    r = ratios(row(take_profit_1=None, exec_take_profit=None))
    assert set(r) == {"כניסה", "סטופ"}
    assert r["כניסה"] == pytest.approx(0.1)


def test_a_short_is_judged_by_the_same_rule():
    """הבאג לא יודע כיוון, ולכן גם הבדיקה לא צריכה לדעת."""
    ok, _ = verdict_for(row(direction="short", entry_price=5000.0,
                            stop_loss=5010.0, take_profit_1=4980.0,
                            exec_entry=500.0, exec_stop_loss=501.0,
                            exec_take_profit=498.0))
    assert ok is True
    bad, why = verdict_for(row(direction="short", entry_price=5000.0,
                               stop_loss=5010.0, take_profit_1=4980.0,
                               exec_entry=505.0, exec_stop_loss=501.0,
                               exec_take_profit=498.0))
    assert bad is False
