"""Unit tests for the H0020 fill rules. Run: python3 -I -m pytest test_orb.py (from this folder)."""
import os
import sys
from pathlib import Path

os.environ.setdefault("CLAUDE_SCRATCH", "/nonexistent")   # loaders reads it at import; no data used
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd  # noqa: E402
import pytest  # noqa: E402

import orb  # noqa: E402


def day(bars):
    """bars: list of (hm, o, h, l, c) -> session frame like loaders.sessions() returns."""
    idx = pd.to_datetime([f"2024-01-03 {hm // 100:02d}:{hm % 100:02d}" for hm, *_ in bars])
    g = pd.DataFrame([b[1:] for b in bars], columns=["o", "h", "l", "c"], index=idx)
    g["hm"] = [b[0] for b in bars]
    return g


UP5 = [(930, 100, 101, 99, 100.5), (931, 100.5, 101, 100, 100.8), (932, 100.8, 101, 100.5, 100.9),
       (933, 100.9, 101.2, 100.6, 101), (934, 101, 101.3, 100.8, 101.1)]   # long, low 99


def test_signal_long_and_R():
    g = day(UP5 + [(935, 101, 101.2, 100.9, 101.1)])
    assert orb.signal(g) == (1, 101.0, 99.0, 2.0)


def test_signal_short_mirror():
    dn = [(hm, 200 - o, 200 - l, 200 - h, 200 - c) for hm, o, h, l, c in UP5]
    g = day(dn + [(935, 99, 99.1, 98.8, 98.9)])
    assert orb.signal(g) == (-1, 99.0, 101.0, 2.0)


def test_no_trade_when_doji_or_missing_bar():
    flat = UP5[:-1] + [(934, 101, 101.3, 100.8, 100)]          # close == 09:30 open
    assert orb.signal(day(flat + [(935, 100, 100, 100, 100)])) is None
    assert orb.signal(day(UP5[:2] + UP5[3:] + [(935, 101, 101, 101, 101)])) is None
    assert orb.signal(day(UP5)) is None                            # no 09:35 bar


def test_stop_first_when_bar_touches_both():
    g = day(UP5 + [(935, 101, 130, 98, 120)])                      # target 121 and stop 99 both touched
    side, entry, stop, r, px, why = orb.trade_day(g)
    assert (px, why) == (99.0, "stop")


def test_gap_through_stop_fills_at_open():
    g = day(UP5 + [(935, 101, 101.5, 100.5, 101), (936, 97, 97.5, 96, 97)])
    assert orb.trade_day(g)[4:] == (97, "stop")
    dn = [(hm, 200 - o, 200 - l, 200 - h, 200 - c) for hm, o, h, l, c in UP5]
    g = day(dn + [(935, 99, 99.5, 98.5, 99), (936, 103, 104, 102.5, 103)])
    assert orb.trade_day(g)[4:] == (103, "stop")


def test_target_fill_and_close_exit():
    g = day(UP5 + [(935, 101, 101.5, 100.5, 101), (936, 101, 125, 100.5, 124)])
    assert orb.trade_day(g)[4:] == (121.0, "target")
    g = day(UP5 + [(935, 101, 101.5, 100.5, 101), (1559, 102, 102.5, 101.5, 102.2), (1600, 1, 1, 1, 1)])
    assert orb.trade_day(g)[4:] == (102.2, "close")


def test_entry_open_already_beyond_stop_exits_at_entry():
    g = day(UP5 + [(935, 98, 98.5, 97.5, 98)])                     # long, stop 99, opens at 98
    side, entry, stop, r, px, why = orb.trade_day(g)
    assert (r, px, why) == (1.0, 98.0, "stop")


def test_run_net_R_and_roll_exclusion():
    g = day(UP5 + [(935, 101, 101.5, 100.5, 101), (1559, 102, 102.5, 101.5, 103)])
    d = g.index[0].date()
    t = orb.run({d: g}, set())
    assert t.gross_R.iloc[0] == pytest.approx(1.0)
    assert t.net_R.iloc[0] == pytest.approx((2 - 0.0002 * 101) / 2)
    assert orb.run({d: g}, {d}).empty
