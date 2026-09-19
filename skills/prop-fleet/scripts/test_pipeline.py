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

    monkeypatch.setattr(sys, "argv", ["pipeline.py", str(bot)])
    return bot


def test_a_clean_fetch_runs_the_replay(monkeypatch, tmp_path):
    wire(monkeypatch, tmp_path, lambda: None, ("ES", "NQ"))
    with pytest.raises(Ran):
        pipeline.main()


def test_a_crashed_fetch_never_reaches_the_replay(monkeypatch, tmp_path):
    """הריפליי על נרות ישנים נראה בדיוק כמו ריפליי על נרות חדשים."""
    def boom():
        raise ConnectionError("no gateway on 4002")
    wire(monkeypatch, tmp_path, boom, (), bars_before=("ES", "NQ"))
    with pytest.raises(SystemExit) as e:
        pipeline.main()
    assert "נכשלה" in str(e.value)


def test_a_fetch_that_exits_with_an_error_stops_the_run(monkeypatch, tmp_path):
    def quit_():
        raise SystemExit("אין חיבור ל-IB Gateway")
    wire(monkeypatch, tmp_path, quit_, (), bars_before=("ES", "NQ"))
    with pytest.raises(SystemExit) as e:
        pipeline.main()
    assert "לא ממשיך לריפליי" in str(e.value)


def test_a_fetch_that_exits_cleanly_is_not_treated_as_failure(monkeypatch, tmp_path):
    def done():
        raise SystemExit(0)
    wire(monkeypatch, tmp_path, done, ("ES",))
    with pytest.raises(Ran):
        pipeline.main()


def test_no_bars_at_all_stops_before_the_replay(monkeypatch, tmp_path):
    wire(monkeypatch, tmp_path, lambda: None, ())
    with pytest.raises(SystemExit) as e:
        pipeline.main()
    assert "אין קובצי נרות" in str(e.value)


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
    monkeypatch.setattr(sys, "argv", ["pipeline.py", str(bot), "--keep"])
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
