#!/usr/bin/env python3
"""בדיקות ל-pipeline.py.

הערך היחיד של שלב מקשר הוא שהוא נעצר במקום הנכון. אם השליפה נכשלה
והריפליי רץ בכל זאת, הוא מדפיס מספר שנראה תקין לחלוטין ומתאר את
הנרות של אתמול — וזו בדיוק התקלה שהשלב הזה אמור למנוע.
"""

import sys
import types

import pytest

import pipeline


class Ran(Exception):
    """מסמן שהריפליי הופעל, כדי להבדיל בין רץ לא רץ."""


def wire(monkeypatch, tmp_path, fetch, bars_after, bars_before=()):
    """מרכיב סביבה מלאכותית: תיקיית בוט, קובצי נרות, ושני השלבים."""
    bot = tmp_path / "bot"
    bot.mkdir()
    monkeypatch.setattr(pipeline, "D", tmp_path)
    for sym in bars_before:
        (tmp_path / f"{sym}_5min_clean.csv").write_text("old")

    fb = types.ModuleType("futures_bars")
    fb.BOT = None

    def _fetch():
        # הנרות נכתבים לפני שהשליפה מסיימת, כמו במציאות: יציאה נקייה
        # אחרי עבודה מוצלחת היא לא כישלון.
        for sym in bars_after:
            (tmp_path / f"{sym}_5min_clean.csv").write_text("new bars")
        fetch()

    fb.main = _fetch
    monkeypatch.setitem(sys.modules, "futures_bars", fb)

    rp = types.ModuleType("replay")

    def _replay():
        raise Ran()

    rp.main = _replay
    monkeypatch.setitem(sys.modules, "replay", rp)

    monkeypatch.setattr(sys, "argv", ["pipeline.py", str(bot), "--measure-only"])
    return bot


def test_a_clean_fetch_runs_the_replay(monkeypatch, tmp_path):
    wire(monkeypatch, tmp_path, lambda: None, ("ES", "NQ"))
    with pytest.raises(Ran):
        pipeline.main()


def test_a_crashed_fetch_never_reaches_the_replay(monkeypatch, tmp_path, capsys):
    """הריפליי על נרות ישנים נראה בדיוק כמו ריפליי על נרות חדשים.

    מה שנבדק כאן הוא שהריפליי לא רץ, לא איך העצירה מיושמת. קודם
    היא הייתה sys.exit, והבדיקה נעלה את המנגנון במקום את הכלל —
    כך שגרסה שעוצרת ומדפיסה סיכום שמנקב את החוסם נחשבה לכישלון.
    """
    def boom():
        raise ConnectionError("no gateway on 4002")
    wire(monkeypatch, tmp_path, boom, (), bars_before=("ES", "NQ"))
    pipeline.main()                      # לא Ran -> הריפליי לא רץ
    out = capsys.readouterr().out
    assert "נכשלה" in out
    assert "חוסם" in out or "✗" in out


def test_a_fetch_that_exits_with_an_error_stops_the_run(monkeypatch, tmp_path, capsys):
    def quit_():
        raise SystemExit("אין חיבור ל-IB Gateway")
    wire(monkeypatch, tmp_path, quit_, (), bars_before=("ES", "NQ"))
    pipeline.main()
    assert "IB Gateway" in capsys.readouterr().out


def test_a_fetch_that_exits_cleanly_is_not_treated_as_failure(monkeypatch, tmp_path):
    def done():
        raise SystemExit(0)
    wire(monkeypatch, tmp_path, done, ("ES",))
    with pytest.raises(Ran):
        pipeline.main()


def test_no_bars_at_all_stops_before_the_replay(monkeypatch, tmp_path, capsys):
    wire(monkeypatch, tmp_path, lambda: None, ())
    pipeline.main()
    assert "אין קובצי נרות" in capsys.readouterr().out


def test_unchanged_bars_still_run_but_say_so(monkeypatch, tmp_path, capsys):
    """--keep הוא בחירה לגיטימית. שקט לגביה הוא לא."""
    bot = tmp_path / "bot"
    bot.mkdir()
    monkeypatch.setattr(pipeline, "D", tmp_path)
    for sym in ("ES", "NQ"):
        (tmp_path / f"{sym}_5min_clean.csv").write_text("unchanged")
    fb = types.ModuleType("futures_bars")
    fb.BOT = None
    fb.main = lambda: None
    monkeypatch.setitem(sys.modules, "futures_bars", fb)
    rp = types.ModuleType("replay")
    rp.main = lambda: None
    monkeypatch.setitem(sys.modules, "replay", rp)
    monkeypatch.setattr(sys, "argv",
                        ["pipeline.py", str(bot), "--measure-only"])
    pipeline.main()
    assert "לא השתנו" in capsys.readouterr().out


def test_a_missing_bot_folder_is_named_not_guessed(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["pipeline.py", str(tmp_path / "nope")])
    with pytest.raises(SystemExit) as e:
        pipeline.main()
    assert "תיקיית הבוט" in str(e.value)


def test_the_bot_path_reaches_both_stages(monkeypatch, tmp_path):
    """שכחת הנתיב בשלב השני היא בדיוק מה שהשלב הזה בא לסלק."""
    bot = wire(monkeypatch, tmp_path, lambda: None, ("ES",))
    seen = {}
    rp = sys.modules["replay"]
    rp.main = lambda: seen.update(argv=list(sys.argv))
    pipeline.main()
    assert seen["argv"][1] == str(bot)
    assert sys.modules["futures_bars"].BOT == bot


# ---------- חצי התיקון ----------
#
# הסכנה כאן הפוכה מהסכנה בחצי המדידה. שם הפחד הוא שהשלב ימשיך כשהוא
# צריך לעצור. כאן הפחד הוא שהוא יכתוב כשהוא לא בטוח. טלאי שממציא
# משתנה שלא קיים הופך באג שקט לקריסה בזמן שליחת פקודה.

BUGGY = '''\
def to_proxy(entry, stop_loss, futures_price, etf_price):
    ratio = entry / etf_price
    return round(entry / ratio, 4), round(stop_loss / ratio, 4)
'''

NO_FUTURES = '''\
def to_proxy(entry, stop_loss, etf_price):
    ratio = entry / etf_price
    return round(entry / ratio, 4), round(stop_loss / ratio, 4)
'''

FIXED = '''\
def to_proxy(entry, stop_loss, futures_price, etf_price):
    ratio = futures_price / etf_price
    return round(entry / ratio, 4), round(stop_loss / ratio, 4)
'''

DEMO_ONLY = '''\
def explain(entry, etf_price, futures_price):
    """ratio = entry / etf_price  ->  מחיר הכניסה מתבטל."""
    buggy_ratio = entry / etf_price
    ratio = futures_price / etf_price
    return buggy_ratio, ratio
'''


def _proxy(tmp_path, src):
    p = tmp_path / "proxy.py"
    p.write_text(src, encoding="utf-8")
    return p


def test_the_bug_is_found_and_the_ratio_is_rederived(tmp_path):
    p = _proxy(tmp_path, BUGGY)
    r = pipeline.patch_proxy(p, apply=True)
    assert r["status"] == "patched"
    assert "ratio = futures_price / etf_price" in p.read_text()
    assert pipeline.buggy_sites(p.read_text()) == []


def test_a_quoted_or_demonstrated_bug_is_not_a_bug(tmp_path):
    """proxy_fix.py מצטט את הבאג כדי להסביר אותו.

    סימון הקובץ המתוקן כפגום גרוע מאי-זיהוי: הוא מאמן אותך להתעלם.
    """
    p = _proxy(tmp_path, DEMO_ONLY)
    before = p.read_text()
    assert pipeline.patch_proxy(p, apply=True)["status"] == "clean"
    assert p.read_text() == before


def test_an_already_fixed_file_is_left_alone(tmp_path):
    p = _proxy(tmp_path, FIXED)
    before = p.read_text()
    assert pipeline.patch_proxy(p, apply=True)["status"] == "clean"
    assert p.read_text() == before


def test_it_refuses_rather_than_inventing_a_variable(tmp_path):
    """אין מחיר חוזה בתחום -> לא נוגעים, ואומרים למה.

    זו הבדיקה שמונעת את הנזק הגרוע ביותר שהסקריפט הזה יכול לגרום:
    להחליף באג שקט בקריסה ברגע שליחת פקודה.
    """
    p = _proxy(tmp_path, NO_FUTURES)
    before = p.read_text()
    r = pipeline.patch_proxy(p, apply=True)
    assert r["status"] == "blocked"
    assert "מחיר חוזה" in r["why"]
    assert p.read_text() == before, "קובץ חסום חייב להישאר בייט-בבייט"


def test_a_dry_run_reports_the_exact_change_and_writes_nothing(tmp_path):
    p = _proxy(tmp_path, BUGGY)
    before = p.read_text()
    r = pipeline.patch_proxy(p, apply=False)
    assert r["status"] == "would_patch"
    assert r["hits"][0]["before"] == "ratio = entry / etf_price"
    assert r["hits"][0]["after"] == "ratio = futures_price / etf_price"
    assert p.read_text() == before


def test_an_unparseable_file_is_reported_not_rewritten(tmp_path):
    p = _proxy(tmp_path, "def broken(:\n")
    before = p.read_text()
    r = pipeline.patch_proxy(p, apply=True)
    assert r["status"] == "blocked"
    assert p.read_text() == before


def test_the_backup_runs_before_anything_is_written(tmp_path):
    bot = tmp_path / "bot"
    (bot / "broker").mkdir(parents=True)
    (bot / "logs").mkdir()
    (bot / "broker" / "proxy.py").write_text(BUGGY, encoding="utf-8")
    (bot / "logs" / "trades.db").write_bytes(b"sqlite-ish")
    dest = pipeline.backup(bot)
    assert (dest / "broker_proxy.py").read_text() == BUGGY
    assert (dest / "logs_trades.db").read_bytes() == b"sqlite-ish"


def test_strategy_is_never_touched(tmp_path, monkeypatch):
    """הכלל היחיד שאין עליו שיקול דעת."""
    bot = tmp_path / "bot"
    (bot / "broker").mkdir(parents=True)
    (bot / "strategy").mkdir()
    (bot / "broker" / "proxy.py").write_text(BUGGY, encoding="utf-8")
    graded = bot / "strategy" / "grading.py"
    graded.write_text("THRESHOLD = 7\n", encoding="utf-8")
    monkeypatch.setattr(pipeline, "blocking", [])
    pipeline.step_proxy(bot, apply=True)
    assert graded.read_text() == "THRESHOLD = 7\n"
