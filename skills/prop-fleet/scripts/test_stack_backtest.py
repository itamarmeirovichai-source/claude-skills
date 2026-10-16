#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקות לערימה.

שתי הטעויות שהבדיקות האלה קיימות בשבילן: נרמול תנודתיות שמשתמש בעתיד
(הערימה הראשונה ב-what-the-giants-do.md נורמלה לפי כל המדגם — זה בדיוק
זה), ואות חתך-רוחבי שמציץ קדימה. שתיהן לא נראות בקוד ומנפחות שארפ.
"""
from __future__ import annotations

import sys

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import stack_backtest as S  # noqa: E402


def _px(n=2500, seed=0, drift=0.0003, vol=0.01, cols=("A", "B", "C", "D")):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2000-01-03", periods=n)
    return pd.DataFrame({c: 100 * np.cumprod(1 + rng.normal(drift, vol, n))
                         for c in cols}, index=idx)


# ── משקלי דירוג ───────────────────────────────────────────────────────

def test_rank_weights_are_dollar_neutral_and_unit_gross():
    w = S.rank_weights(pd.Series([3.0, 1.0, 2.0, np.nan, 5.0]))
    assert abs(w.sum()) < 1e-12
    assert abs(w.abs().sum() - 1.0) < 1e-12
    assert np.isnan(w.iloc[3])
    assert w.iloc[4] > w.iloc[0] > w.iloc[2] > w.iloc[1]


def test_rank_weights_need_two_assets():
    assert S.rank_weights(pd.Series([1.0, np.nan])).isna().all()


# ── נרמול תנודתיות בלי עתיד ────────────────────────────────────────────

def test_vol_scale_does_not_use_the_future():
    r = _px(cols=("A",))["A"].pct_change().dropna()
    base = S.vol_scale(r)
    cut = r.index[1500]
    bent = r.copy()
    bent.loc[cut:] *= 5.0                     # עתיד תנודתי בהרבה
    alt = S.vol_scale(bent)
    before = base.index < cut
    pd.testing.assert_series_equal(base.loc[before], alt.loc[alt.index < cut])


def test_vol_scale_hits_the_target_on_stationary_noise():
    rng = np.random.default_rng(1)
    idx = pd.bdate_range("2000-01-03", periods=3000)
    r = pd.Series(rng.normal(0, 0.02, len(idx)), index=idx)
    v = S.vol_scale(r).std() * np.sqrt(252)
    assert 0.09 < v < 0.11, v


def test_vol_scale_multiplier_is_constant_within_a_month():
    r = _px(cols=("A",), seed=2)["A"].pct_change().dropna()
    k = (S.vol_scale(r) / r.reindex(S.vol_scale(r).index)).dropna()
    by_m = k.round(10).groupby(k.index.to_period("M")).nunique()
    assert (by_m <= 1).all()


# ── אות חתך-רוחבי בלי עתיד ─────────────────────────────────────────────

def test_xs_component_does_not_use_the_future():
    px = _px(seed=3)
    cls = {c: "X" for c in px.columns}
    base = S.xs_component(px, cls, S.xsmom_signal(px))
    cut = px.index[2000]
    bent = px.copy()
    bent.loc[cut:, "A"] *= 3.0
    alt = S.xs_component(bent, cls, S.xsmom_signal(bent))
    b = base.loc[base.index < cut]
    pd.testing.assert_series_equal(b, alt.loc[b.index])


def test_xsmom_skips_the_last_month():
    px = _px(seed=4)
    sig = S.xsmom_signal(px)
    day = px.index[600]
    bent = px.copy()
    # שינוי בתוך 21 הימים האחרונים לא נוגע באות
    bent.iloc[590:601] *= 1.5
    assert np.allclose(S.xsmom_signal(bent).loc[day], sig.loc[day])


def test_value_is_positive_when_price_fell_over_five_years():
    idx = pd.bdate_range("2000-01-03", periods=1600)
    down = pd.Series(np.linspace(200, 100, len(idx)), index=idx)
    up = pd.Series(np.linspace(100, 200, len(idx)), index=idx)
    v = S.value_signal(pd.DataFrame({"D": down, "U": up})).iloc[-1]
    assert v["D"] > 0 > v["U"]


def test_a_persistent_winner_is_long_in_xsmom():
    idx = pd.bdate_range("2000-01-03", periods=1500)
    rng = np.random.default_rng(5)
    cols = {}
    for c, d in (("W", 0.002), ("L", -0.002), ("M1", 0.0), ("M2", 0.0)):
        cols[c] = 100 * np.cumprod(1 + rng.normal(d, 0.003, len(idx)))
    px = pd.DataFrame(cols, index=idx)
    r = S.xs_component(px, {c: "X" for c in px}, S.xsmom_signal(px))
    assert S.stats(r)["sharpe"] > 1.0


# ── לילה ──────────────────────────────────────────────────────────────

def test_overnight_is_close_to_open_minus_cost():
    idx = pd.bdate_range("2012-01-02", periods=3)
    spx = pd.DataFrame({"Open": [100.0, 102.0, 99.0],
                        "Close": [101.0, 100.0, 100.0]}, index=idx)
    r = S.overnight_returns(spx, start="2012-01-01", cost_bps=1.0)
    assert np.allclose(r.values, [102 / 101 - 1 - 1e-4, 99 / 100 - 1 - 1e-4])


def test_overnight_starts_where_opens_become_real():
    if not (S.DATA_DIR / "spx_open_close.csv").exists():
        return
    spx = S.load_spx()
    stale = (spx["Open"] - spx["Close"].shift(1)).abs() < 1e-6
    assert stale.loc["2000":"2009"].mean() > 0.5       # לפני: מזויף
    assert stale.loc["2011":].mean() < 0.05            # אחרי: אמיתי
    r = S.overnight_returns(spx)
    assert r.index[0] >= pd.Timestamp(S.ON_START)


# ── הערימה ────────────────────────────────────────────────────────────

def test_stacking_two_independent_edges_raises_sharpe():
    rng = np.random.default_rng(6)
    idx = pd.bdate_range("2000-01-03", periods=252 * 20)
    mk = lambda: pd.Series(rng.normal(0.8 * 0.1 / 252, 0.1 / np.sqrt(252),  # noqa: E731
                                      len(idx)), index=idx)
    c = pd.DataFrame({"a": S.vol_scale(mk()), "b": S.vol_scale(mk())})
    # ההשוואה היא לממוצע של שני הרכיבים, לא לאחד מהם: רכיב בודד יכול
    # לצאת בר-מזל במדגם. הטענה היא שארפ ערימה ≈ שארפ ממוצע × √2.
    avg = np.mean([S.stats(c[k].dropna())["sharpe"] for k in c])
    two = S.stats(S.stack(c))["sharpe"]
    assert two > avg * 1.25, (avg, two)


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
