"""Deterministic checks of the D1 extension. With S = +-1000 and sigma = 1%
the drift (3.97% of start per day) dwarfs the noise (0.063%), so every rule
fires on a known day."""
import numpy as np
import pytest

from prop_model import PLANS, economics, eval_sim, funded_sim, simulate

SIG = np.array([0.01])
BASE = dict(start=100_000., fee=500., targets=[0.10, 0.05], time_limit=None,
            min_days=[4, 4], dd_type="static", dd=0.10, dll=0.05,
            funded=dict(split=0.8, first_wait=10, cycle=10))


def test_two_phase_pass_waits_for_min_days():
    e = eval_sim(BASE, 1000, SIG, n=200)
    assert e["p_pass"][0] == 1.0
    assert e["t_pass"][0] == 8          # 4 days per phase, target hit on day 3 / 2


def test_static_drawdown_breaches_on_day_three():
    e = eval_sim(dict(BASE, dll=0), -1000, SIG, n=200)
    assert e["p_pass"][0] == 0.0
    assert e["t_fail"][0] == 2          # day 3 breaches; days counted while alive


def test_hard_daily_loss_limit_breaches_day_one():
    e = eval_sim(dict(BASE, dll=0.03), -1000, SIG, n=200)
    assert e["t_fail"][0] == 0


def test_soft_daily_loss_only_halts():
    F = dict(BASE, dll=0.02, dll_hard=False, dd=0.30, time_limit=[10, 10])
    e = eval_sim(F, -1000, SIG, n=200)
    assert e["p_pass"][0] == 0.0
    assert e["t_fail"][0] == 10         # loses 2%/day, never breaches 30%, expires


def test_time_limit_expires():
    e = eval_sim(dict(BASE, time_limit=[5, 5], dll=0, dd=0.5), 0.0,
                 np.array([0.0001]), n=50)
    assert e["p_pass"][0] == 0.0 and e["t_fail"][0] == 5


def test_trailing_eod_locks():
    F = dict(BASE, dd_type="trail_eod", dd=0.02, dd_lock=0.0, dll=0)
    acc_floor_after_gain = None
    from prop_model import _Account
    a = _Account(F, (1,), 100_000.)
    a.bal[:] = 103_000.; a.end_day()
    assert float(a.floor()[0]) == 100_000.          # locked at start
    a.bal[:] = 101_000.; a.end_day()
    assert float(a.floor()[0]) == 100_000.


def test_trailing_intraday_moves_with_equity():
    from prop_model import _Account
    F = dict(BASE, dd_type="trail_intraday", dd=0.02, dll=0)
    a = _Account(F, (1,), 100_000.)
    a.step(np.array([500.], np.float32), np.array([True]))
    assert float(a.floor()[0]) == 98_500.


def test_funded_payout_and_split():
    G = dict(BASE, funded=dict(split=0.8, first_wait=10, cycle=10, max_payouts=1))
    f = funded_sim(G, 1000, SIG, n=100, horizon=30)
    # day 10 balance about +39.7% -> withdraw all of it, keep 80%
    assert f["n_pay"][0] == 1 and f["life"][0] == 10
    assert 0.8 * 39_000 < f["pay"][0] < 0.8 * 40_500


def test_payout_cap_and_fraction():
    G = dict(BASE, funded=dict(split=1.0, first_wait=5, cycle=5, payout_frac=0.5,
                               payout_cap=0.02, max_payouts=1))
    f = funded_sim(G, 1000, SIG, n=50, horizon=20)
    assert abs(f["pay"][0] - 2_000) < 1


def test_economics_zero_pass_costs_fees():
    e = economics(dict(BASE, dll=0), -1000, n=100, sigmas=SIG)
    assert e["net_yr"] < 0 and e["p_pass"] == 0


def test_original_apex_model_still_runs():
    d = simulate(plan="50K", slots=1, avg_R=0.3, years=1, n=20)
    assert d["net_year"].shape == (20, 1)
    assert "50K-2026" in PLANS


def test_lock_on_payout_raises_static_floor():
    from prop_model import _Account
    F = dict(BASE, lock_on_payout=0.0)
    a = _Account(F, (1,), 100_000.)
    assert float(np.asarray(a.floor()).ravel()[0]) == 90_000.
    a.paylock[:] = True
    assert float(np.asarray(a.floor()).ravel()[0]) == 100_000.


def test_refund_after_nth_payout():
    G = dict(BASE, refund_after=4, funded=dict(split=0.8, first_wait=1, cycle=1, max_payouts=3))
    f = funded_sim(G, 1000, SIG, n=50, horizon=20)
    assert f["p_refund"][0] == 0.0 and f["p_any"][0] == 1.0
