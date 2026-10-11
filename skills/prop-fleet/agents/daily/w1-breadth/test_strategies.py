"""Unit tests on synthetic bars (spec G5b).  python3 -m pytest -q test_strategies.py"""
import numpy as np
import pytest

from common import MIN, fill, mark
from strategies import dec_gao, dec_orb, dec_rest, dec_twap, execute

O = np.int64(1_000_000) * MIN
C = O + 120 * MIN


def bars(prices, start=O - 10 * MIN, drop=()):
    n = len(prices)
    t = start + np.arange(n) * MIN
    p = np.asarray(prices, float)
    o, c = p.copy(), p.copy()
    h, l = p + 0.0, p - 0.0
    keep = np.array([i not in drop for i in range(n)])
    return t[keep], o[keep], h[keep], l[keep], c[keep]


def test_mark_and_fill_windows():
    t, o, h, l, c = bars(np.arange(200) + 100.0)
    T = O + 30 * MIN
    i = int((T - t[0]) // MIN)
    assert mark(t, c, T) == c[i - 1]          # bar that ends at T
    assert fill(t, o, T) == o[i]              # bar that opens at T
    t2, o2, *_ , c2 = bars(np.arange(200) + 100.0, drop=set(range(i - 11, i + 11)))
    assert np.isnan(mark(t2, c2, T)) and np.isnan(fill(t2, o2, T))


def test_gao_and_rest_signal_and_fills():
    p = np.r_[np.full(40, 100.0), np.linspace(101, 105, 160)]
    t, o, h, l, c = bars(p)
    ev = dec_rest(t, o, h, l, c, O, C, 99.0)
    assert ev == [(O + 30 * MIN, O + 30 * MIN, ev[0][2], 1)]
    g, cost, sides = execute(ev, t, o, c, C, 1.0)
    entry, exitp = fill(t, o, O + 30 * MIN), mark(t, c, C)
    assert sides == 2 and cost == pytest.approx(2e-4)
    assert g == pytest.approx((exitp - entry) / entry)
    ev = dec_gao(t, o, h, l, c, O, C, 200.0)          # down from prior close -> short
    assert ev[0][3] == -1 and ev[0][1] == C - 30 * MIN
    g, _, _ = execute(ev, t, o, c, C, 1.0)
    e2 = fill(t, o, C - 30 * MIN)
    assert g == pytest.approx(-(mark(t, c, C) - e2) / e2)
    assert dec_gao(t, o, h, l, c, O, C, np.nan) == []


def test_twap_flip_costs_two_sides_and_flat_at_close():
    p = np.r_[np.full(10, 100.0), np.linspace(100, 110, 50), np.linspace(110, 90, 80), np.full(10, 90.0)]
    t, o, h, l, c = bars(p)
    ev = dec_twap(t, o, h, l, c, O, C, np.nan)
    pos = [e[3] for e in ev]
    assert pos[0] == 1 and -1 in pos
    g, cost, sides = execute(ev, t, o, c, C, 1.0)
    assert sides == 1 + 2 + 1                     # open, one flip, close
    assert cost == pytest.approx(4e-4)


def test_twap_equal_keeps_flat():
    t, o, h, l, c = bars(np.full(200, 100.0))
    assert dec_twap(t, o, h, l, c, O, C, np.nan) == []


def test_orb_breakout_stop_and_gap_fill():
    p = np.r_[np.full(10, 100.0), np.full(30, 100.0), np.full(10, 100.0), [102.0], np.full(20, 103.0),
              [98.0], np.full(80, 98.0)]
    t, o, h, l, c = bars(p)
    h[10:40] = 101.0; l[10:40] = 99.0                # OR 99..101
    ev = dec_orb(t, o, h, l, c, O, C, np.nan)
    assert ev[0][3] == 1 and len(ev) == 2
    assert ev[1][2] == 98.0                          # gapped through the stop -> its open
    g, cost, sides = execute(ev, t, o, c, C, 1.0)
    entry = fill(t, o, ev[0][1])
    assert g == pytest.approx((98.0 - entry) / entry) and sides == 2


def test_orb_no_breakout():
    t, o, h, l, c = bars(np.full(200, 100.0))
    h[:] = 100.5; l[:] = 99.5
    assert dec_orb(t, o, h, l, c, O, C, np.nan) == []


def test_missing_fill_no_position():
    p = np.r_[np.full(40, 100.0), np.linspace(101, 105, 160)]
    i = 40
    t, o, h, l, c = bars(p, drop=set(range(i, i + 12)))
    ev = dec_rest(t, o, h, l, c, O, C, 99.0)
    assert execute(ev, t, o, c, C, 1.0) == (0.0, 0.0, 0)
