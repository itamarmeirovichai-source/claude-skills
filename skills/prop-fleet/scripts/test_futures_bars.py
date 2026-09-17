#!/usr/bin/env python3
"""
בדיקות ל-futures_bars.

הליבה שאפשר לבדוק בלי IBKR היא בחירת החוזה הקדמי. היא זו שקובעת אם
הסדרה המורכבת נאמנה למה שהבוט ראה, ושגיאה בה מכניסה קפיצת מחיר שקטה
בדיוק במקום שבו אי אפשר לראות אותה — באמצע התקופה.
"""

from datetime import date
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

from futures_bars import pick_front, to_frame

ET = ZoneInfo("America/New_York")


def frame(days, price, volume):
    """נרות שעתיים ליום, במחיר ובמחזור נתונים."""
    rows = []
    for d in days:
        for h in range(9, 16):
            rows.append({"ts": pd.Timestamp(f"{d} {h:02d}:00", tz=ET),
                         "open": price, "high": price, "low": price,
                         "close": price, "volume": volume})
    return pd.DataFrame(rows)


DAYS_A = ["2026-05-18", "2026-05-19", "2026-05-20"]
DAYS_B = ["2026-05-21", "2026-05-22"]
ALL = DAYS_A + DAYS_B


def test_the_busier_contract_wins_each_day():
    front = frame(DAYS_A, 7500, 1000)
    back = frame(DAYS_A, 7530, 10)
    df, rolls = pick_front({"202606": front, "202609": back})
    assert (df.close == 7500).all()
    assert rolls == []


def test_the_roll_is_read_from_volume_not_guessed():
    a = pd.concat([frame(DAYS_A, 7500, 1000), frame(DAYS_B, 7500, 10)])
    b = pd.concat([frame(DAYS_A, 7530, 10), frame(DAYS_B, 7530, 1000)])
    df, rolls = pick_front({"202606": a, "202609": b})
    assert len(rolls) == 1
    d, old, new = rolls[0]
    assert d == date(2026, 5, 21)
    assert (old, new) == ("202606", "202609")
    before = df[df.ts.dt.date < date(2026, 5, 21)]
    after = df[df.ts.dt.date >= date(2026, 5, 21)]
    assert (before.close == 7500).all()
    assert (after.close == 7530).all()


def test_every_day_appears_exactly_once():
    a = pd.concat([frame(DAYS_A, 7500, 1000), frame(DAYS_B, 7500, 10)])
    b = pd.concat([frame(DAYS_A, 7530, 10), frame(DAYS_B, 7530, 1000)])
    df, _ = pick_front({"202606": a, "202609": b})
    assert df.ts.is_unique
    assert sorted({str(d) for d in df.ts.dt.date}) == sorted(ALL)
    assert len(df) == len(ALL) * 7


def test_a_single_contract_is_used_whole():
    only = frame(ALL, 7500, 500)
    df, rolls = pick_front({"202606": only})
    assert len(df) == len(only)
    assert rolls == []


def test_an_empty_contract_is_ignored():
    df, rolls = pick_front({"202606": frame(ALL, 7500, 100),
                            "202609": pd.DataFrame()})
    assert len(df) == len(ALL) * 7
    assert rolls == []


def test_nothing_at_all_is_not_a_crash():
    df, rolls = pick_front({})
    assert df.empty and rolls == []
    df, rolls = pick_front({"202606": pd.DataFrame()})
    assert df.empty and rolls == []


def test_a_days_worth_of_volume_decides_not_a_single_bar():
    """נר בודד עם מחזור חריג לא אמור להעביר את כל היום לחוזה האחורי."""
    a = frame(["2026-05-18"], 7500, 100)
    b = frame(["2026-05-18"], 7530, 10)
    b.loc[b.index[0], "volume"] = 500        # ספייק אחד, עדיין פחות מ-700
    df, _ = pick_front({"202606": a, "202609": b})
    assert (df.close == 7500).all()


def test_two_rolls_are_both_reported():
    x = ["2026-05-18"]
    y = ["2026-05-19"]
    z = ["2026-05-20"]
    a = pd.concat([frame(x, 1, 100), frame(y, 1, 1), frame(z, 1, 100)])
    b = pd.concat([frame(x, 2, 1), frame(y, 2, 100), frame(z, 2, 1)])
    _, rolls = pick_front({"202606": a, "202609": b})
    assert len(rolls) == 2


# ── המרה מ-IBKR ───────────────────────────────────────────────

class Bar:
    def __init__(self, d, o, h, l, c, v):
        self.date, self.open, self.high = d, o, h
        self.low, self.close, self.volume = l, c, v


def test_bars_keep_their_timezone():
    b = [Bar(pd.Timestamp("2026-05-18 14:30", tz="UTC"), 1, 2, 0.5, 1.5, 10)]
    df = to_frame(b)
    assert str(df.ts.dt.tz) == "America/New_York"
    assert df.ts.iloc[0].hour == 10


def test_duplicate_timestamps_collapse():
    t = pd.Timestamp("2026-05-18 14:30", tz="UTC")
    df = to_frame([Bar(t, 1, 2, 0.5, 1.5, 10), Bar(t, 1, 2, 0.5, 1.5, 10)])
    assert len(df) == 1


def test_no_bars_gives_an_empty_frame_with_the_right_columns():
    df = to_frame([])
    assert df.empty
    assert list(df.columns) == ["ts", "open", "high", "low", "close", "volume"]
