#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקות לבקטסט המומנטום.

הטעות שהבדיקות האלה קיימות בשבילה היא הצצה קדימה: פוזיציה שנגזרת
ממחיר שעוד לא ידוע. היא לא נראית בקוד, היא נראית רק בתוצאה — שארפ
שגבוה מדי — ולכן יש כאן בדיקה שמזיזה מחירים עתידיים ודורשת שהעבר
לא יזוז.
"""
from __future__ import annotations

import sys

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from trend_backtest import (COST_BPS, LOOKBACK_DAYS, TDAYS,  # noqa: E402
                            VOL_WINDOW, portfolio, prop_survival,
                            stationary_bootstrap_sharpe, stats,
                            tsmom_positions)


def _px(n=1000, drift=0.0005, vol=0.01, seed=0, start="2010-01-01"):
    rng = np.random.default_rng(seed)
    r = rng.normal(drift, vol, n)
    idx = pd.bdate_range(start, periods=n)
    return pd.Series(100.0 * np.cumprod(1 + r), index=idx)


def _frame(**cols):
    return pd.DataFrame(cols)


# ── כיוון האות ────────────────────────────────────────────────────────

def test_a_rising_series_goes_long():
    px = _frame(A=_px(drift=0.002, vol=0.002))
    pos = tsmom_positions(px)
    tail = pos["A"].dropna().iloc[-100:]
    assert (tail > 0).all()


def test_a_falling_series_goes_short():
    px = _frame(A=_px(drift=-0.002, vol=0.002))
    pos = tsmom_positions(px)
    tail = pos["A"].dropna().iloc[-100:]
    assert (tail < 0).all()


def test_long_only_never_shorts():
    px = _frame(A=_px(drift=-0.002, vol=0.002))
    pos = tsmom_positions(px, long_only=True)
    assert (pos["A"].dropna() >= 0).all()
    assert (pos["A"].dropna().iloc[-100:] == 0).all()


# ── אין הצצה קדימה ────────────────────────────────────────────────────

def test_no_lookahead():
    """מזיזים את כל המחירים מיום מסוים והלאה. הפוזיציות לפני היום
    הזה חייבות להישאר זהות עד הביט האחרון."""
    px = _frame(A=_px(seed=1), B=_px(seed=2, drift=-0.0003))
    cut = px.index[700]
    base = tsmom_positions(px)
    bent = px.copy()
    bent.loc[cut:] *= 3.0
    alt = tsmom_positions(bent)
    before = px.index < cut
    pd.testing.assert_frame_equal(base.loc[before], alt.loc[before])


def test_the_signal_uses_last_month_close_not_today():
    """הפוזיציה ביום הראשון של חודש נגזרת מסגירת החודש הקודם. אם
    משנים רק את סגירת אותו יום ראשון, הפוזיציה שלו לא זזה."""
    px = _frame(A=_px(seed=3))
    pos = tsmom_positions(px)
    firsts = px.index.to_series().groupby(px.index.to_period("M")).first()
    day = firsts.iloc[20]
    bent = px.copy()
    bent.loc[day, "A"] *= 0.5
    alt = tsmom_positions(bent)
    assert pos.loc[day, "A"] == alt.loc[day, "A"]


# ── החזקה חודשית ──────────────────────────────────────────────────────

def test_position_is_constant_within_a_month():
    px = _frame(A=_px(seed=4))
    pos = tsmom_positions(px)["A"].dropna()
    # הערך הראשון בכל חודש שווה לערך האחרון בו — בתוך החודש אין שינוי
    by_month = pos.groupby(pos.index.to_period("M"))
    assert (by_month.nunique() <= 1).all()


# ── נרמול לתנודתיות ───────────────────────────────────────────────────

def test_doubling_vol_halves_the_position():
    calm = _frame(A=_px(seed=5, drift=0.001, vol=0.005))
    wild = _frame(A=_px(seed=5, drift=0.001, vol=0.010))
    p1 = tsmom_positions(calm)["A"].dropna().abs().iloc[-60:].mean()
    p2 = tsmom_positions(wild)["A"].dropna().abs().iloc[-60:].mean()
    assert 1.6 < p1 / p2 < 2.4, (p1, p2)


# ── עלויות ────────────────────────────────────────────────────────────

def test_costs_equal_turnover_times_bps():
    px = _frame(A=_px(seed=6), B=_px(seed=7))
    pos = tsmom_positions(px)
    pf = portfolio(px, pos)
    expected = pf["turnover"] * COST_BPS / 1e4
    pd.testing.assert_series_equal(pf["gross"] - pf["net"], expected,
                                   check_names=False)


def test_zero_cost_means_gross_equals_net():
    px = _frame(A=_px(seed=8))
    pf = portfolio(px, tsmom_positions(px), cost_bps=0.0)
    pd.testing.assert_series_equal(pf["gross"], pf["net"], check_names=False)


# ── סטטיסטיקה ─────────────────────────────────────────────────────────

def test_stats_on_a_constant_return():
    idx = pd.bdate_range("2015-01-01", periods=TDAYS * 4)
    d = pd.Series(0.0004, index=idx)
    s = stats(d)
    assert abs(s["ann_ret"] - 0.0004 * TDAYS) < 1e-12
    assert s["max_dd"] == 0.0
    assert s["pct_pos_months"] == 1.0


def test_bootstrap_centres_on_the_sample_sharpe():
    rng = np.random.default_rng(0)
    m = pd.Series(rng.normal(0.01, 0.03, 240),
                  index=pd.date_range("2000-01-31", periods=240, freq="ME"))
    sample = m.mean() / m.std(ddof=1) * np.sqrt(12)
    boot = stationary_bootstrap_sharpe(m, n=2000)
    assert boot.shape == (2000,)
    assert abs(np.median(boot) - sample) < 0.25, (np.median(boot), sample)


def test_bootstrap_interval_contains_the_sample_and_is_wide_for_noise():
    """על רעש טהור ה-bootstrap מרוכז סביב שארפ המדגם (לא סביב אפס —
    זה לא מה ש-bootstrap מבטיח), והרוחב שלו הוא בערך 2×1.645×√(12/T)."""
    rng = np.random.default_rng(1)
    m = pd.Series(rng.normal(0.0, 0.03, 240),
                  index=pd.date_range("2000-01-31", periods=240, freq="ME"))
    sample = m.mean() / m.std(ddof=1) * np.sqrt(12)
    boot = stationary_bootstrap_sharpe(m, n=2000)
    lo, hi = np.percentile(boot, [5, 95])
    assert lo < sample < hi
    width = hi - lo
    expect = 2 * 1.645 * np.sqrt(12 / 240)
    assert 0.6 * expect < width < 1.6 * expect, (width, expect)


# ── מבנה הפרופ ────────────────────────────────────────────────────────

def test_pure_drift_passes_and_never_blows():
    idx = pd.bdate_range("2015-01-01", periods=500)
    d = pd.Series(0.001, index=idx)                # +0.1% כל יום
    r = prop_survival(d, notional=50_000, n=200)
    assert r["pass_rate"] == 1.0 and r["blowup_rate"] == 0.0
    # 3000 / (50000 × 0.001) = 60 ימים
    assert r["median_days_to_pass"] == 60


def test_pure_loss_blows_and_never_passes():
    idx = pd.bdate_range("2015-01-01", periods=500)
    d = pd.Series(-0.001, index=idx)
    r = prop_survival(d, notional=50_000, n=200)
    assert r["blowup_rate"] == 1.0 and r["pass_rate"] == 0.0


def test_the_floor_locks_after_the_safety_net():
    """עולים 2,600$, ואז יורדים 2,400$. לפני הנעילה הרצפה הייתה
    עוקבת והנתיב היה נשרף; אחרי הנעילה היא ב-+100$ והוא שורד."""
    idx = pd.bdate_range("2015-01-01", periods=300)
    up = [0.001] * 52          # 52 × 50$ = 2,600$
    down = [-0.001] * 48       # 48 × 50$ = -2,400$ → שווי +200$, מעל +100$
    flat = [0.0] * 200
    d = pd.Series(up + down + flat, index=idx)
    # bootstrap מערבב, אז בודקים את המנגנון ישירות עם בלוק ענק אחד
    r = prop_survival(d, notional=50_000, n=50, mean_block=10_000,
                      horizon_days=300)
    # עם בלוק שמכסה את כל הסדרה, רוב הנתיבים הם הסדרה עצמה מנקודת
    # התחלה אקראית; הנקודות שמתחילות ב-0 עוברות בלי להישרף.
    assert r["blowup_rate"] < 1.0


# ── נתוני החוזים ──────────────────────────────────────────────────────
# הניקוי הוא החלטות, ולכן כל אחת מהן נבדקת: מה שהוסר הוסר, מה שאופס
# אופס, ומה שנשמר — האירועים האמיתיים — לא נגעו בו.

def _have_data():
    from trend_backtest import DATA_DIR
    return (DATA_DIR / "futures.csv").exists()


def test_futures_loader_applies_exactly_the_documented_cleaning():
    if not _have_data():
        return
    from trend_backtest import load_futures
    px, labels = load_futures()
    assert "VF" not in px.columns
    assert px.shape[1] == 54
    r = px.pct_change()
    # האירוע המזויף אופס
    assert abs(r.loc["1999-01-04", "EO"]) < 1e-9
    # האירועים האמיתיים נשארו
    assert r.loc["1991-01-17", "CL"] < -0.30
    assert r.loc["1994-06-27", "KC"] > 0.25
    assert r.loc["2003-02-24", "NG"] > 0.35
    assert px.index[0].year == 1984 and px.index[-1].year == 2016
    assert all(t in labels for t in px.columns)


def test_futures_price_index_reproduces_the_returns():
    """cumprod ואז pct_change חייב להחזיר את התשואות המקוריות."""
    if not _have_data():
        return
    from trend_backtest import DATA_DIR, load_futures
    px, _ = load_futures()
    raw = pd.read_csv(DATA_DIR / "futures.csv", encoding="utf-8-sig")
    raw["Date"] = pd.to_datetime(raw["Date"], format="%m/%d/%y")
    raw = raw.set_index("Date").sort_index()
    raw.columns = [c.strip() for c in raw.columns]
    got = px["TY"].pct_change().loc["2005-01-03":"2005-12-30"]
    want = raw["TY"].loc["2005-01-03":"2005-12-30"]
    both = pd.concat([got, want], axis=1).dropna()
    assert np.allclose(both.iloc[:, 0], both.iloc[:, 1], atol=1e-12)


# ── אות על תשואה עודפת ────────────────────────────────────────────────

def test_flat_cash_makes_the_excess_signal_equal_the_plain_one():
    """כשהמזומן לא זז, תשואה עודפת = תשואה כוללת, והפוזיציות זהות.
    המזומן עצמו יוצא מהתיק."""
    px = _frame(A=_px(seed=13), B=_px(seed=14, drift=-0.0004))
    px["CASH"] = 100.0
    plain = tsmom_positions(px.drop(columns="CASH"))
    ex = tsmom_positions(px, cash="CASH")
    assert ex["CASH"].isna().all()
    pd.testing.assert_frame_equal(plain, ex.drop(columns="CASH"))


def test_rising_cash_can_flip_a_slow_climber_to_short():
    """נכס שעולה 3% בשנה כשהמזומן נותן 8%: לפי תשואה כוללת — לונג;
    לפי תשואה עודפת — שורט."""
    n = 1000
    idx = pd.bdate_range("2010-01-01", periods=n)
    slow = pd.Series(100.0 * (1.03 ** (np.arange(n) / 252)), index=idx)
    cash = pd.Series(100.0 * (1.08 ** (np.arange(n) / 252)), index=idx)
    # רעש קטן כדי שהנרמול לא יתפוצץ על תנודתיות אפס — קטן מספיק
    # (0.5% בשנה) כדי שלא יהפוך את סימן התשואה השנתית
    rng = np.random.default_rng(0)
    slow = slow * (1 + rng.normal(0, 0.0003, n)).cumprod()
    px = _frame(A=slow, CASH=cash)
    total = tsmom_positions(px.drop(columns="CASH"))["A"].dropna().iloc[-50:]
    excess = tsmom_positions(px, cash="CASH")["A"].dropna().iloc[-50:]
    assert (total > 0).all()
    assert (excess < 0).all()


# ── תקרת חשיפה ────────────────────────────────────────────────────────

def test_max_gross_caps_exposure_every_day():
    px = _frame(A=_px(seed=9, vol=0.002), B=_px(seed=10, vol=0.002),
                C=_px(seed=11, vol=0.002))              # תנודתיות נמוכה → נרמול מבקש מינוף
    pos = tsmom_positions(px)
    free = portfolio(px, pos)["weights"].abs().sum(axis=1)
    assert free.max() > 1.0, free.max()               # בלי תקרה יש מינוף
    capped = portfolio(px, pos, max_gross=1.0)["weights"].abs().sum(axis=1)
    assert (capped <= 1.0 + 1e-9).all(), capped.max()


def test_max_gross_leaves_low_exposure_days_alone():
    px = _frame(A=_px(seed=12, vol=0.03))               # תנודתיות גבוהה → חשיפה קטנה
    pos = tsmom_positions(px)
    free = portfolio(px, pos)["weights"]
    capped = portfolio(px, pos, max_gross=1.0)["weights"]
    assert free.abs().sum(axis=1).max() < 1.0
    pd.testing.assert_frame_equal(free, capped)


# ── נתוני הנכסים הסחירים ──────────────────────────────────────────────

def _have_assets():
    from trend_backtest import DATA_DIR
    return (DATA_DIR / "asset_classes.csv").exists()


def test_asset_loader_masks_the_modelled_history():
    """GLD נולד ב-18/11/2004. לפניו הסדרה היא מודל, ובמצב observed_only
    היא חייבת להיות NaN. עם observed_only=False היא קיימת."""
    if not _have_assets():
        return
    from trend_backtest import load_asset_classes
    px, labels = load_asset_classes()
    assert px.shape[1] == 9 and set(px.columns) == set(labels)
    assert px["GOLDPM"].loc[:"2004-11-17"].isna().all()
    assert px["GOLDPM"].loc["2004-11-18":].notna().all()
    assert px["CMDTY"].loc[:"2006-02-06"].isna().all()
    assert px["USLCAP"].notna().all()                   # לוח NYSE
    # מתחיל ביום הראשון עם תיק נצפה של חמישה, לא ב-S&P לבדו מ-1970
    assert str(px.index[0].date()) == "1991-10-29"
    assert px.iloc[0].notna().sum() == 5
    full, _ = load_asset_classes(observed_only=False)
    assert full["GOLDPM"].loc["1980-01-02":"1980-12-31"].notna().all()
    assert full.index[0].year == 1970
    assert full.index.is_unique and px.index.is_unique


def test_asset_annual_returns_match_the_known_years():
    if not _have_assets():
        return
    from trend_backtest import load_asset_classes
    px, _ = load_asset_classes()
    yr = px.resample("YE").last().pct_change()
    assert abs(yr.loc["2008-12-31", "USLCAP"] - (-0.37)) < 0.01
    assert abs(yr.loc["2022-12-31", "LTT"] - (-0.31)) < 0.01
    assert abs(yr.loc["2013-12-31", "GOLDPM"] - (-0.28)) < 0.01
    assert abs(yr.loc["2008-12-31", "CMDTY"] - (-0.32)) < 0.01


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"  ✓ {name}")
        except Exception as exc:                             # noqa: BLE001
            fails += 1
            print(f"  ✗ {name}: {exc}")
    print(f"\n  {'הכול עבר' if not fails else str(fails) + ' נכשלו'}")
    sys.exit(1 if fails else 0)
