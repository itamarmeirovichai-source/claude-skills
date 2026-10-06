#!/usr/bin/env python3
"""
בדיקות ל-futures_era_check.

מה שנבדק כאן הוא לא "האם הקוד רץ" אלא האם הוא מסוגל להבדיל בין סדרה
נקייה לסדרה מפוגרת ברזולוציה שעתית — כי על ההבדל הזה נשענת ההחלטה
אם 131 הסטאפים של עידן החוזים הם ראיה או אשפה.

יש כאן גם בדיקה שמתעדת את נקודת העיוורון: בשוק רגוע, פיגור אמיתי
מייצר שגיאה קטנה בפיגור אפס, והמסווג נופל ל"תבנית שלישית" במקום
לזהות אותו. עדיף לתעד מגבלה מאשר לגלות אותה בשדה.
"""

import numpy as np
import pandas as pd
import pytest

from futures_era_check import (CLEAN_AT_ZERO, CORROBORATING_AT_ZERO,
                               FLANK_DAYS, PER_DAY, SCAN_HI_DAYS, SHARP_RATIO,
                               STEP_HOURS, classify, lock_time)
from lag_refine import scan_time, summarize

ET = "America/New_York"


def make_bars(days: int = 120, hourly_sigma: float = 0.0022, seed: int = 0):
    """נרות שעתיים רציפים, הילוך מקרי גיאומטרי. חוזים נסחרים כמעט 24/7."""
    rng = np.random.default_rng(seed)
    n = days * 24
    ts = pd.date_range("2026-04-01", periods=n, freq="h", tz=ET)
    mid = 7000 * np.exp(np.cumsum(rng.normal(0, hourly_sigma, n)))
    return pd.DataFrame({"ts": ts, "mid": mid})


def make_setups(bars: pd.DataFrame, n: int = 120, lag_days: float = 0.0,
                fvg_noise: float = 0.002, seed: int = 1, last_days: int = 25):
    """סטאפים ש-entry שלהם הוא המחיר לפני lag_days, ועוד רעש FVG."""
    rng = np.random.default_rng(seed)
    end = bars.ts.iloc[-1]
    start = end - pd.Timedelta(days=last_days)
    pool = bars[bars.ts >= start].reset_index(drop=True)
    pick = np.sort(rng.choice(len(pool), size=n, replace=False))
    # דקות אקראיות בתוך השעה: כך שהסטאפ לא נופל בדיוק על גבול נר.
    # הסדרה נשארת מודעת לאזור זמן לכל אורך הדרך — .values על סדרה
    # כזאת מפיל את האזור ושובר את החיסור שבא אחריו.
    base = pool.ts.iloc[pick].reset_index(drop=True)
    ts = base + pd.to_timedelta(rng.integers(0, 60, n), unit="m")
    j = np.searchsorted(bars.ts.values,
                        (ts - pd.Timedelta(days=lag_days)).values,
                        side="right") - 1
    entry = bars.mid.values[j] * (1 + rng.normal(0, fvg_noise, n))
    return pd.DataFrame({"symbol": "ES", "ts": ts, "entry": entry})


def verdict(setups, bars):
    """מריץ את אותה סריקה שהסקריפט מריץ, ומחזיר את אותם שני המספרים."""
    B = {"ES": bars}
    c = lock_time(setups, B, SCAN_HI_DAYS)
    d = scan_time(c, B, 0.0, SCAN_HI_DAYS, STEP_HOURS)
    v = summarize(d, flank_days=FLANK_DAYS, per_day=PER_DAY)
    v["at_zero"] = float(d.median_err_pct.iloc[0])
    return v


# ── הבחנה בין נקי למפוגר ──────────────────────────────────────

def test_a_clean_series_has_no_trough():
    b = make_bars(seed=2)
    v = verdict(make_setups(b, lag_days=0.0, seed=3), b)
    assert v["at_zero"] < CLEAN_AT_ZERO, v
    assert v["two_sided"] < SHARP_RATIO, v


def test_a_planted_lag_is_found_at_the_right_place():
    b = make_bars(seed=4)
    v = verdict(make_setups(b, lag_days=15.0, seed=5), b)
    assert abs(v["at"] - 15.0) < 0.6, v
    assert v["two_sided"] >= SHARP_RATIO, v
    assert classify(v) == "lagged", v


def test_the_two_cases_are_far_apart_not_adjacent():
    """הפרדה שנשענת על סף אחד היא שברירית. כאן הפער עצמו נמדד."""
    b = make_bars(seed=6)
    clean = verdict(make_setups(b, lag_days=0.0, seed=7), b)
    dirty = verdict(make_setups(b, lag_days=15.0, seed=7), b)
    assert dirty["at_zero"] > clean["at_zero"] * 8, (clean, dirty)


@pytest.mark.parametrize("seed", range(5))
def test_clean_stays_clean_across_seeds(seed):
    b = make_bars(seed=100 + seed)
    v = verdict(make_setups(b, lag_days=0.0, seed=200 + seed), b)
    assert v["two_sided"] < SHARP_RATIO, (seed, v)


@pytest.mark.parametrize("seed", range(5))
def test_lag_is_found_across_seeds(seed):
    b = make_bars(seed=300 + seed)
    v = verdict(make_setups(b, lag_days=15.0, seed=400 + seed), b)
    assert v["two_sided"] >= SHARP_RATIO, (seed, v)
    assert abs(v["at"] - 15.0) < 1.0, (seed, v)


# ── מה שהרזולוציה השעתית לא הורסת ─────────────────────────────

def test_hourly_resolution_does_not_fabricate_error():
    """גס יותר מחמש דקות, אבל לא מספיק גס כדי לזייף פיגור."""
    b = make_bars(seed=8)
    v = verdict(make_setups(b, lag_days=0.0, fvg_noise=0.0, seed=9), b)
    assert v["at_zero"] < 0.30, v


def test_a_short_lag_is_not_mistaken_for_the_long_one():
    b = make_bars(seed=10)
    v = verdict(make_setups(b, lag_days=1.0, seed=11), b)
    assert v["at"] < 3.0, v


# ── הקבוצה הנעולה ─────────────────────────────────────────────

def test_lock_time_drops_setups_without_deep_enough_history():
    b = make_bars(days=40, seed=12)
    s = make_setups(b, n=60, seed=13, last_days=35)
    kept = lock_time(s, {"ES": b}, 30.0)
    assert len(kept) < len(s)
    earliest = b.ts.iloc[0] + pd.Timedelta(days=30)
    assert (kept.ts >= earliest).all()


def test_lock_time_keeps_everything_when_history_is_deep():
    b = make_bars(days=200, seed=14)
    s = make_setups(b, n=60, seed=15)
    assert len(lock_time(s, {"ES": b}, 30.0)) == len(s)


def test_an_unknown_symbol_is_dropped_not_crashed():
    b = make_bars(seed=16)
    s = make_setups(b, n=40, seed=17)
    s.loc[s.index[:10], "symbol"] = "RTY"
    kept = lock_time(s, {"ES": b}, 30.0)
    assert set(kept.symbol) == {"ES"}
    assert len(kept) == 30


# ── נקודת העיוורון, מתועדת ולא מוסתרת ─────────────────────────

def test_a_quiet_market_does_not_hide_a_real_lag():
    """שוק רגוע פי ארבעה. השגיאה בפיגור אפס קטנה — הפיגור עדיין נמצא.

    זה בדיוק המקרה שהפיל את הגרסה הראשונה של הסקריפט, שדרשה גם שוקת
    וגם שגיאה גדולה בפיגור אפס. השגיאה בפיגור אפס מודדת כמה השוק זז,
    לא כמה חמור הבאג, ולכן היא אינה תנאי.
    """
    b = make_bars(hourly_sigma=0.00055, seed=18)
    v = verdict(make_setups(b, lag_days=15.0, seed=19), b)
    assert v["at_zero"] < CORROBORATING_AT_ZERO, v
    assert classify(v) == "lagged", v


@pytest.mark.parametrize("sigma", [0.0005, 0.001, 0.002, 0.004])
def test_the_call_survives_every_volatility_regime(sigma):
    """אותו פיגור, ארבע רמות תנודתיות. ההכרעה לא תלויה בשוק."""
    b = make_bars(hourly_sigma=sigma, seed=20)
    lag = verdict(make_setups(b, lag_days=15.0, seed=21), b)
    clean = verdict(make_setups(b, lag_days=0.0, seed=21), b)
    assert classify(lag) == "lagged", (sigma, lag)
    assert classify(clean) == "clean", (sigma, clean)


def test_no_trough_but_a_big_error_is_left_undecided():
    """היעדר שוקת לבדו אינו רישיון לקרוא לנתונים תקינים."""
    assert classify({"two_sided": 1.1, "at_zero": 3.0, "at": 0.0}) == "unknown"
    assert classify({"two_sided": 1.1, "at_zero": 0.2, "at": 0.0}) == "clean"
    assert classify({"two_sided": 2.6, "at_zero": 0.2, "at": 15.0}) == "lagged"
