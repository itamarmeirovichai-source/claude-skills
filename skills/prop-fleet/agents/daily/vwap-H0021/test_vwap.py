"""Unit tests for H0021 (VWAP, next-open execution, flat at close, cost arithmetic).
Run: python3 -I -m pytest test_vwap.py (from this folder). No market data used."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import vwap as V  # noqa: E402

FLAT = lambda p: np.zeros(np.shape(p))            # noqa: E731
ONE = lambda p: np.full(np.shape(p), 1.0)         # noqa: E731


def arr(rows):
    o, h, l, c, v = (np.array(x, float) for x in zip(*rows))
    return o, h, l, c, v


def test_vwap_is_cumulative_typical_price_weighted():
    o, h, l, c, v = arr([(10, 12, 9, 9, 100), (9, 11, 8, 11, 300), (11, 14, 11, 14, 0)])
    vw, *_ = V.positions(h, l, c, v, np.array([0]))
    tp = (h + l + c) / 3
    assert vw[0] == pytest.approx(tp[0])
    assert vw[1] == pytest.approx((tp[0] * 100 + tp[1] * 300) / 400)
    assert vw[2] == pytest.approx(vw[1])                      # zero-volume bar leaves VWAP unchanged


def test_vwap_resets_each_session_and_undefined_without_volume():
    o, h, l, c, v = arr([(1, 1, 1, 1, 5), (1, 3, 1, 2, 5), (50, 51, 49, 50, 0), (50, 52, 50, 52, 10)])
    vw, sig, _, _ = V.positions(h, l, c, v, np.array([0, 2]))
    assert np.isnan(vw[2]) and sig[2] == 0                   # new session, no volume yet
    assert vw[3] == pytest.approx((52 + 50 + 52) / 3)         # nothing from session 1


def test_signal_acts_at_next_open_and_equal_keeps_position():
    # bar0 close above vwap -> long from bar1 open; bar1 equal -> keep; bar2 below -> short from bar3
    o, h, l, c, v = arr([(100, 102, 99, 102, 1), (102, 103, 101, 101, 0), (101, 101, 95, 95, 10),
                         (95, 96, 94, 96, 1)])
    vw, sig, desired, pos = V.positions(h, l, c, v, np.array([0]))
    assert sig[0] == 1 and sig[1] == 0 and sig[2] == -1      # bar1: close 101 == vwap 101 (tp0, no vol)
    assert list(pos) == [0, 1, 1, -1]


def test_equal_close_holds_previous_signal():
    h, l, c, v = (np.array(x, float) for x in ([3, 2, 2], [1, 2, 2], [3, 2, 2], [1, 0, 0]))
    # bar0 tp=7/3 < close 3 -> +1 ; bars1,2 no volume, vwap 7/3 > close 2 -> -1
    _, sig, desired, pos = V.positions(h, l, c, v, np.array([0]))
    assert list(sig) == [1, -1, -1] and list(pos) == [0, 1, -1]
    # a flat bar first (close == vwap) leaves the position flat
    _, sig, desired, pos = V.positions(np.array([5., 6]), np.array([5., 4]), np.array([5., 6]),
                                       np.array([1., 1]), np.array([0]))
    assert sig[0] == 0 and list(pos) == [0, 0] and desired[1] == 1


def test_flat_at_last_bar_close_and_last_signal_ignored():
    # long held into the last bar; last bar's own signal (short) is never acted on
    o, h, l, c, v = arr([(100, 101, 99, 101, 1), (101, 104, 101, 104, 1), (104, 104, 90, 90, 100)])
    _, _, _, pos = V.positions(h, l, c, v, np.array([0]))
    assert list(pos) == [0, 1, 1]
    g, cost, units, entry = V.daily_pnl(o, c, pos, np.array([0]), ONE)
    assert g[0] == pytest.approx((104 - 101) + (90 - 104))   # open-to-open then last bar open-to-close
    assert units[0] == 2 and cost[0] == 2 and entry[0] == 101


def test_cost_counts_flip_as_two_units_and_pct_cost():
    o = np.array([100., 101, 99, 98])
    c = np.array([101., 99, 98, 97])
    pos = np.array([0., 1, -1, -1])
    g, cost, units, entry = V.daily_pnl(o, c, pos, np.array([0]), ONE)
    assert units[0] == 1 + 2 + 1                              # open, flip, close
    assert g[0] == pytest.approx(1 * (99 - 101) + -1 * (98 - 99) + -1 * (97 - 98))
    _, cost_pct, _, _ = V.daily_pnl(o, c, pos, np.array([0]), lambda p: V.SPY_COST_FRAC * p)
    assert cost_pct[0] == pytest.approx(0.5e-4 * (101 + 2 * 99 + 97))


def test_multi_session_no_carry_and_matches_stream():
    rng = np.random.default_rng(1)
    n = 60
    c = 100 + np.cumsum(rng.normal(0, 1, n))
    o = np.r_[100, c[:-1]] + rng.normal(0, .2, n)
    h = np.maximum(o, c) + .3
    l = np.minimum(o, c) - .3
    v = rng.integers(0, 50, n).astype(float)
    starts = np.array([0, 20, 41])
    _, _, _, pos = V.positions(h, l, c, v, starts)
    assert all(pos[s] == 0 for s in starts)
    g, cost, units, entry = V.daily_pnl(o, c, pos, starts, ONE)
    ends = np.append(starts[1:], n)
    for j, (s, e) in enumerate(zip(starts, ends)):
        p, cash, cst, u, en = V.stream_day(o[s:e], h[s:e], l[s:e], c[s:e], v[s:e], ONE)
        assert np.array_equal(p, pos[s:e])
        assert cash == pytest.approx(g[j]) and cst == pytest.approx(cost[j]) and u == units[j]
        for k in range(1, e - s + 1):                         # truncation on synthetic data
            _, _, _, pk = V.positions(h[s:s + k], l[s:s + k], c[s:s + k], v[s:s + k], np.array([0]))
            assert np.array_equal(pk, pos[s:s + k])


def test_no_position_day_scores_zero_units():
    o = c = np.array([5., 5])
    g, cost, units, entry = V.daily_pnl(o, c, np.zeros(2), np.array([0]), ONE)
    assert g[0] == 0 and cost[0] == 0 and units[0] == 0 and np.isnan(entry[0])
