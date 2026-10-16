"""Unit tests for H0022 (VWAP trend, decisions only at the 12 half-hour bar closes).
Run: python3 -I -m pytest test_vwap30.py (from this folder). No market data used."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import vwap30 as V  # noqa: E402

ONE = lambda p: np.full(np.shape(p), 1.0)         # noqa: E731


def hm_range(start, end):
    """All 1m bar labels start..end inclusive as HHMM ints."""
    out, t = [], (start // 100) * 60 + start % 100
    while t <= (end // 100) * 60 + end % 100:
        out.append((t // 60) * 100 + t % 60)
        t += 1
    return np.array(out)


def session(hm, close_fn):
    """Bars with o=h=l=c=close_fn(hm) except where given; volume 1 -> VWAP = running mean of c."""
    c = np.array([float(close_fn(x)) for x in hm])
    return c.copy(), c.copy(), c.copy(), c, np.ones(c.size)


def test_slot_mapping_and_decision_hm():
    assert list(V.slot_of([930, 959, 1000, 1029, 1529, 1530, 1559, 929])) == [0, 0, 1, 1, 11, -1, -1, -1]
    hm = hm_range(930, 1559)
    dec = V.decision_bars(hm, np.array([0]))
    assert tuple(hm[dec]) == V.DECISION_HM                   # exactly the 12 registered closes


def test_vwap_is_cumulative_typical_price_weighted():
    h, l, c, v = (np.array(x, float) for x in ([12, 11, 14], [9, 8, 11], [9, 11, 14], [100, 300, 0]))
    vw, *_ = V.positions(h, l, c, v, np.array([0]), np.array([930, 931, 932]))
    tp = (h + l + c) / 3
    assert vw[1] == pytest.approx((tp[0] * 100 + tp[1] * 300) / 400)
    assert vw[2] == pytest.approx(vw[1])                      # zero-volume bar leaves VWAP unchanged


def test_signals_between_decision_bars_are_ignored():
    hm = hm_range(930, 1100)
    # price rises until 09:45 then falls hard: per-bar H0021 would flip short well before 09:59,
    # but the only decision before 10:29 is the 09:59 close
    def close(x):
        if x <= 945:
            return 100 + (x - 930)                            # rising: per-bar signal long
        if x < 959:
            return 98                                         # below TWAP: per-bar signal short
        return 200 if x == 959 else 120
    o, h, l, c, v = session(hm, close)
    vw, sig, desired, pos = V.positions(h, l, c, v, np.array([0]), hm)
    i959, i1000 = list(hm).index(959), list(hm).index(1000)
    assert (sig[:i959] != 0).any() and np.all(pos[:i1000 + 1][:-1] == 0)   # flat until 10:00 open
    assert sig[i959] == 1 and pos[i1000] == 1                # 09:59 close > TWAP -> long at 10:00 open
    i1029, i1030 = list(hm).index(1029), list(hm).index(1030)
    assert np.all(pos[i1000:i1030 + 1] == 1)                  # held through 10:29, decided again at 10:29


def test_short_decision_and_hold_until_next_decision():
    hm = hm_range(930, 1100)
    close = lambda x: 100 - (x - 930) if x < 1000 else 200   # noqa: E731
    o, h, l, c, v = session(hm, close)
    _, sig, _, pos = V.positions(h, l, c, v, np.array([0]), hm)
    i = list(hm).index
    assert sig[i(959)] == -1 and pos[i(1000)] == -1
    assert sig[i(1000)] == 1                                  # price jumps above VWAP at 10:00 ...
    assert np.all(pos[i(1000):i(1029) + 1] == -1)             # ... but the short is held to 10:29
    assert pos[i(1030)] == 1                                  # 10:29 decision acts at 10:30 open


def test_missing_decision_bar_uses_last_bar_of_half_hour():
    hm = np.array([h for h in hm_range(930, 1040) if h not in (958, 959)])
    close = lambda x: 90 if x <= 950 else 110 if x == 957 else 50   # noqa: E731
    o, h, l, c, v = session(hm, close)
    _, sig, _, pos = V.positions(h, l, c, v, np.array([0]), hm)
    i = list(hm).index
    assert V.decision_bars(hm, np.array([0]))[i(957)]         # 09:57 stands in for 09:59
    assert sig[i(957)] == 1 and sig[i(1000)] == -1
    assert pos[i(957)] == 0 and pos[i(1000)] == 1             # decided on 09:57 close, filled 10:00 open
    p, *_ = V.stream_day(o, h, l, c, v, hm, ONE)
    assert np.array_equal(p, pos)


def test_half_hour_with_no_bars_is_skipped():
    hm = np.array([h for h in hm_range(930, 1100) if not 1000 <= h <= 1029])
    close = lambda x: 110 if x == 959 else 100 if x < 959 else 50   # noqa: E731
    o, h, l, c, v = session(hm, close)
    _, sig, _, pos = V.positions(h, l, c, v, np.array([0]), hm)
    i = list(hm).index
    dec = V.decision_bars(hm, np.array([0]))
    assert list(hm[dec]) == [959, 1059, 1100]                 # 10:29 skipped; 11:00 = last bar (not acted)
    assert pos[i(1030)] == 1 and np.all(pos[i(1030):i(1059) + 1] == 1)   # held through skipped slot
    assert pos[i(1100)] == -1


def test_equal_at_decision_keeps_position_and_flat_before_first():
    hm = hm_range(930, 1040)
    o, h, l, c, v = session(hm, lambda x: 100)                # close == TWAP at every bar
    _, sig, desired, pos = V.positions(h, l, c, v, np.array([0]), hm)
    assert np.all(sig == 0) and np.all(pos == 0)              # flat before the first non-equal decision
    # long at 09:59 (29 x 100 then 130: TWAP 101 < 130); 10:00..10:29 close 101 == TWAP exactly
    c2 = np.r_[np.full(29, 100.0), 130.0, np.full(30, 101.0), np.zeros(hm.size - 60)]
    _, sig2, _, pos2 = V.positions(c2, c2, c2, np.ones(c2.size), np.array([0]), hm)
    i = list(hm).index
    assert sig2[i(959)] == 1 and sig2[i(1029)] == 0
    assert np.all(pos2[i(1000):i(1040) + 1] == 1)             # equal at 10:29 -> unchanged; 10:59 not reached


def test_last_half_hour_no_decisions_and_flat_at_close():
    hm = hm_range(1500, 1559)
    close = lambda x: 100 + (x - 1500) if x <= 1529 else 50   # noqa: E731
    o, h, l, c, v = session(hm, close)
    _, sig, _, pos = V.positions(h, l, c, v, np.array([0]), hm)
    i = list(hm).index
    assert sig[i(1530)] == -1 and np.all(pos[i(1530):] == 1)  # 15:29 decision long, held to 15:59
    g, cost, units, entry = V.daily_pnl(o, c, pos, np.array([0]), ONE)
    assert units[0] == 2 and entry[0] == o[i(1530)]
    assert g[0] == pytest.approx(c[-1] - o[i(1530)])


def test_decision_on_session_last_bar_is_not_acted():
    hm = hm_range(1200, 1259)                                 # half day ending 12:59
    o, h, l, c, v = session(hm, lambda x: 100 + (x - 1200))
    _, sig, _, pos = V.positions(h, l, c, v, np.array([0]), hm)
    assert V.decision_bars(hm, np.array([0]))[-1] and sig[-1] == 1
    i = list(hm).index
    assert np.all(pos[:i(1230)] == 0) and np.all(pos[i(1230):] == 1)


def test_cost_counts_flip_as_two_units_and_pct_cost():
    o = np.array([100., 101, 99, 98])
    c = np.array([101., 99, 98, 97])
    pos = np.array([0., 1, -1, -1])
    g, cost, units, entry = V.daily_pnl(o, c, pos, np.array([0]), ONE)
    assert units[0] == 1 + 2 + 1
    _, cost_pct, _, _ = V.daily_pnl(o, c, pos, np.array([0]), lambda p: V.SPX_COST_FRAC * p)
    assert cost_pct[0] == pytest.approx(0.5e-4 * (101 + 2 * 99 + 97))


def test_random_sessions_match_stream_and_truncation():
    rng = np.random.default_rng(1)
    full = hm_range(930, 1559)
    hms, starts = [], []
    for _ in range(6):
        keep = rng.random(full.size) > 0.15                   # drop ~15% of bars, incl. decision bars
        keep[rng.integers(0, 12) * 30:][:30] &= rng.random() > 0.3   # sometimes drop a whole slot
        starts.append(sum(len(x) for x in hms))
        hms.append(full[keep])
    hm = np.concatenate(hms)
    starts = np.array(starts)
    n = hm.size
    c = 100 + np.cumsum(rng.normal(0, 1, n))
    o = np.r_[100, c[:-1]] + rng.normal(0, .2, n)
    h = np.maximum(o, c) + .3
    l = np.minimum(o, c) - .3
    v = rng.integers(0, 50, n).astype(float)
    _, _, _, pos = V.positions(h, l, c, v, starts, hm)
    assert all(pos[s] == 0 for s in starts)
    g, cost, units, entry = V.daily_pnl(o, c, pos, starts, ONE)
    assert units.mean() <= 13                                 # at most 12 decisions + flatten
    ends = np.append(starts[1:], n)
    for j, (s, e) in enumerate(zip(starts, ends)):
        p, cash, cst, u, en = V.stream_day(o[s:e], h[s:e], l[s:e], c[s:e], v[s:e], hm[s:e], ONE)
        assert np.array_equal(p, pos[s:e])
        assert cash == pytest.approx(g[j]) and cst == pytest.approx(cost[j]) and u == units[j]
        for k in range(1, e - s + 1):
            _, _, _, pk = V.positions(h[s:s + k], l[s:s + k], c[s:s + k], v[s:s + k], np.array([0]),
                                      hm[s:s + k])
            assert np.array_equal(pk, pos[s:s + k])


def test_no_position_day_scores_zero_units():
    o = c = np.array([5., 5])
    g, cost, units, entry = V.daily_pnl(o, c, np.zeros(2), np.array([0]), ONE)
    assert g[0] == 0 and cost[0] == 0 and units[0] == 0 and np.isnan(entry[0])
