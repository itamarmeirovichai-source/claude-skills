"""Synthetic-data tests for hypothesis.py (no market data is read)."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location("orb30", Path(__file__).with_name("hypothesis.py"))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def day(date="2015-03-04", n_or=30, path=None):
    """One RTH session 09:30..15:59. OR bars oscillate in [99, 101]."""
    idx = pd.date_range(f"{date} 09:30", f"{date} 15:59", freq="1min")
    c = np.full(len(idx), 100.0)
    c[:30] = np.where(np.arange(30) % 2, 100.5, 99.5)
    if path:
        for hm, px in path.items():
            c[idx.get_loc(pd.Timestamp(f"{date} {hm}")):] = px
    o = np.r_[c[0], c[:-1]]
    hi = np.maximum(o, c) + 0.5
    lo = np.minimum(o, c) - 0.5
    d = pd.DataFrame(dict(o=o, h=hi, l=lo, c=c), index=idx)
    if n_or < 30:
        d = d.drop(idx[30 - (30 - n_or):30])
    return d


def test_opening_range_and_eligibility():
    assert h.opening_range(day()) == (101.0, 99.0)
    assert h.opening_range(day(n_or=24)) is None
    assert h.opening_range(day().iloc[1:]) is None          # 09:30 missing


def test_long_time_exit_with_cost():
    d = day(path={"10:05": 102.0, "13:00": 106.0})
    r = h.trade_day(d, 101.0, 99.0, "A")
    assert r["side"] == 1 and r["entry"] == 102.0 and r["stop"] == 99.0
    assert r["why"] == "time" and r["exit"] == 106.0
    assert r["gross_R"] == pytest.approx(4 / 3)
    assert r["R"] == pytest.approx((4 - 0.6) / 3)


def test_stop_first_and_gap_through_fill():
    d = day(path={"10:05": 102.0, "11:00": 96.0})
    d.loc[pd.Timestamp("2015-03-04 11:00"), "o"] = 96.5      # opens through stop 99
    r = h.trade_day(d, 101.0, 99.0, "A")
    assert r["why"] == "stop" and r["exit"] == 96.5          # worse of stop and open
    d2 = day(path={"10:05": 102.0})
    ts = pd.Timestamp("2015-03-04 11:00")
    d2.loc[ts, ["h", "l"]] = [120.0, 98.0]                   # ambiguous bar for B
    r2 = h.trade_day(d2, 101.0, 99.0, "B")
    assert r2["why"] == "stop"


def test_short_target_B():
    d = day(path={"10:05": 98.0, "12:00": 90.0})
    r = h.trade_day(d, 101.0, 99.0, "B")
    assert r["side"] == -1 and r["why"] == "target"
    assert r["exit"] == pytest.approx(r["entry"] - 2 * r["risk"])


def test_no_trigger_after_noon():
    d = day(path={"12:05": 103.0})
    assert h.trade_day(d, 101.0, 99.0, "A") is None


def test_future_truncation_does_not_change_signal():
    """Deleting bars after the entry minute must not change side, entry or stop."""
    d = day(path={"10:05": 102.0, "14:00": 90.0})
    full = h.trade_day(d, *h.opening_range(d), "A")
    cut = d[d.index <= pd.Timestamp("2015-03-04 10:06")]
    part = h.trade_day(cut, *h.opening_range(cut), "A")
    for k in ("side", "entry", "stop", "risk"):
        assert full[k] == part[k]


def test_variant_C_uses_only_prior_widths():
    days = [day(date=str(d.date())) for d in pd.bdate_range("2015-01-05", periods=22)]
    m1 = pd.concat(days)
    t, elig = h.run(m1, "C")
    assert elig == 22 and t.empty                            # equal widths: not strictly narrower


def test_guard_refuses_unregistered(tmp_path):
    p = tmp_path / "l.csv"
    p.write_text("id,rules_fixed_before_test,notes\nH0018,yes,prereg 1e99c775\nH0019,no,1e99c775\n")
    assert h.ledger_row_ok("H0018", p)
    assert not h.ledger_row_ok("H0019", p)
    assert not h.ledger_row_ok("H9999", p)


def test_summarize_runs_on_synthetic_trades():
    rng = np.random.default_rng(1)
    days = pd.bdate_range("2012-01-02", periods=300)
    t = pd.DataFrame(dict(day=days, R=rng.normal(0, 1, 300), gross_R=rng.normal(0.1, 1, 300),
                          risk=5.0, side=np.where(np.arange(300) % 2, 1, -1), why="time"))
    s = h.summarize(t, eligible=600)
    assert s["n"] == 300 and s["per_day"] == 0.5 and s["draws"] >= 198_000
    assert s["lb_boot"] < s["p5"] < s["net"]
