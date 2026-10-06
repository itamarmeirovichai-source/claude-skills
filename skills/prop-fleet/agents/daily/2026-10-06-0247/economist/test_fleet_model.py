"""Tests for today's fleet_model copy (Economist, 2026-10-06).
Run: python3 -m pytest -q daily/2026-10-06-0247/economist/test_fleet_model.py
"""
import os, sys, importlib.util
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../../scripts"))
import fleet_model as fm
import apex_model as am


def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, rel))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


fm_prev = _load("fm_1005", "../../2026-10-05/economist/fleet_model.py")

SIMPLE = dict(name="t", start=50_000., dd=2_000., dd_mode="eod", target=3_000., qmin=150.,
              evalfee=100., activation=0., eval_days=None, payout="frac", frac=0.5,
              cap=2_000., min_payout=250., qual_days=5, consist=None, split=0.9, lock_off=100.)


def test_reproduces_apex_model_original():
    for plan in ("50K", "50K-2026"):
        a = am.simulate(plan, slots=4, avg_R=0.25, years=2, n=150, seed=3, risk_pct_eval=0.10)
        b = fm.simulate(plan, slots=4, avg_R=0.25, years=2, n=150, seed=3, risk_pct_eval=0.10)
        assert np.array_equal(a["net_year"], b["net_year"])


def test_reproduces_yesterdays_copy_at_integer_td():
    for td in (1, 3):
        x = fm_prev.simulate(SIMPLE, slots=3, avg_R=0.2, years=2, n=120, seed=5, trades_day=td,
                             risk_pct=0.04, risk_pct_eval=0.10)
        y = fm.simulate(SIMPLE, slots=3, avg_R=0.2, years=2, n=120, seed=5, trades_day=td,
                        risk_pct=0.04, risk_pct_eval=0.10)
        assert np.array_equal(x["net_year"], y["net_year"])


def test_cost_in_R_equals_zeroed_globals():
    a = fm.simulate(SIMPLE, slots=3, avg_R=0.2, years=2, n=120, seed=7, cost_in_R=True,
                    risk_pct=0.04, risk_pct_eval=0.10)
    c, s = fm.COMM_RT, fm.SLIP_PTS
    try:
        fm.COMM_RT, fm.SLIP_PTS = 0.0, 0.0
        b = fm.simulate(SIMPLE, slots=3, avg_R=0.2, years=2, n=120, seed=7,
                        risk_pct=0.04, risk_pct_eval=0.10)
    finally:
        fm.COMM_RT, fm.SLIP_PTS = c, s
    assert np.array_equal(a["net_year"], b["net_year"])


def test_cost_in_R_pays_more_than_charging_costs():
    kw = dict(slots=5, avg_R=0.25, years=3, n=300, seed=9, risk_pct=0.04, risk_pct_eval=0.10)
    a = fm.simulate(SIMPLE, cost_in_R=True, **kw)["net_year"].mean()
    b = fm.simulate(SIMPLE, cost_in_R=False, **kw)["net_year"].mean()
    assert a > b


def test_fractional_trades_day_between_integers():
    kw = dict(slots=5, avg_R=0.30, years=3, n=300, seed=4, risk_pct=0.04, risk_pct_eval=0.10,
              cost_in_R=True)
    g = {td: fm.simulate(SIMPLE, trades_day=td, **kw)["gross"][:, 1:].mean() for td in (0.3, 1, 2)}
    assert 0 < g[0.3] < g[1] < g[2]


def test_zero_trades_day_pays_nothing():
    d = fm.simulate(SIMPLE, slots=2, avg_R=0.3, years=1, n=50, seed=1, trades_day=0,
                    risk_pct=0.04, risk_pct_eval=0.10)
    assert d["gross"].sum() == 0


def test_dll_never_binds_when_larger_than_max_day_loss():
    P = dict(SIMPLE, dll=10_000.)
    kw = dict(slots=3, avg_R=0.2, years=2, n=120, seed=8, risk_pct=0.04, risk_pct_eval=0.10)
    a = fm.simulate(P, **kw)["net_year"]
    b = fm.simulate(SIMPLE, **kw)["net_year"]
    assert np.array_equal(a, b)


def test_dll_binding_cuts_losses_and_burns_fewer():
    # risk $200 eval / $200 funded, 3 trades/day: worst day -$600 before costs; DLL $250 binds
    kw = dict(slots=5, avg_R=0.0, years=2, n=300, seed=2, risk_pct=0.10, risk_pct_eval=0.10)
    a = fm.simulate(dict(SIMPLE, dll=250.), **kw)
    b = fm.simulate(SIMPLE, **kw)
    assert a["burned"].mean() < b["burned"].mean()


def test_firm_exit_closes_firm_for_good():
    P = dict(SIMPLE, firm_exit_payouts=1)
    kw = dict(slots=5, avg_R=0.4, years=4, n=200, seed=6, risk_pct=0.04, risk_pct_eval=0.10,
              cost_in_R=True)
    a = fm.simulate(P, **kw)
    b = fm.simulate(SIMPLE, **kw)
    # once one payout lands the firm is gone: later years pay ~nothing
    assert a["gross"][:, 3].mean() < 0.05 * b["gross"][:, 3].mean()
    assert a["gross"].sum() < b["gross"].sum()
