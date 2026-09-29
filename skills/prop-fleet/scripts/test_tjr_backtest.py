#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקות למנגנון של tjr_backtest: פיבוטים בלי עתיד, וכללי ביצוע שתמיד
לחובת האסטרטגיה. בלי נתונים חיצוניים."""
from __future__ import annotations

import sys

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import tjr_backtest as T  # noqa: E402


def test_pivots_do_not_use_the_future():
    rng = np.random.default_rng(0)
    h = 100 + np.cumsum(rng.normal(0, 1, 300))
    l = h - 1
    sh, sl = T.confirmed_pivots(h, l, 2)
    h2, l2 = h.copy(), l.copy()
    h2[200:] += 50
    l2[200:] -= 50
    sh2, sl2 = T.confirmed_pivots(h2, l2, 2)
    # פיבוט בנר p מאושר בנר p+2; נר 200 משפיע מנר 200 ואילך בלבד
    assert np.array_equal(sh[:200], sh2[:200], equal_nan=True)
    assert np.array_equal(sl[:200], sl2[:200], equal_nan=True)


def _m1(rows, day="2015-06-10", start="11:00"):
    idx = pd.date_range(f"{day} {start}", periods=len(rows), freq="1min")
    return pd.DataFrame(rows, columns=["o", "h", "l", "c"], index=idx)


def _setup(side=-1, entry=100.0, stop=104.0, t="2015-06-10 10:00"):
    return dict(side=side, entry=entry, stop=stop, t=pd.Timestamp(t),
                asia_other=0.0)


def test_fill_bar_touching_the_stop_counts_as_a_stop():
    m1 = _m1([(99, 105, 98, 99)] + [(99, 99, 80, 80)] * 5, start="10:05")
    r = T.simulate(m1, _setup(), T.Spec("x"), pd.Timestamp("2015-06-10").date())
    assert r["why"] == "stop" and r["R"] < -1.0


def test_a_bar_touching_both_stop_and_target_is_a_stop():
    m1 = _m1([(99, 100.5, 99, 100), (100, 104.5, 91, 95)], start="10:05")
    r = T.simulate(m1, _setup(), T.Spec("x"), pd.Timestamp("2015-06-10").date())
    assert r["why"] == "stop"


def test_target_reached_before_fill_cancels_the_setup():
    m1 = _m1([(97, 98, 91, 92), (92, 101, 92, 100)], start="10:05")
    r = T.simulate(m1, _setup(), T.Spec("x"), pd.Timestamp("2015-06-10").date())
    assert r is None


def test_a_clean_short_reaches_2R_net_of_cost():
    m1 = _m1([(99, 100.2, 99, 100)] + [(100, 100, 91.5, 91.9)], start="10:05")
    r = T.simulate(m1, _setup(), T.Spec("x"), pd.Timestamp("2015-06-10").date())
    assert r["why"] == "target"
    assert abs(r["R"] - (8.0 - T.COST_PTS) / 4.0) < 1e-9


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
