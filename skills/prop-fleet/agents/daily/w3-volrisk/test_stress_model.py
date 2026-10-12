"""Tests for the F2 stress extension. As in D1's tests, S = +-1000 at
sigma = 1% makes the drift (3.97% of start a day) dwarf the noise, so rules
fire on known days."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w1-prop"))
import prop_model as D1  # noqa: E402
import stress_model as M  # noqa: E402
from firms import FIRMS  # noqa: E402

SIG = np.array([0.01])
BASE = dict(start=100_000., fee=500., targets=[0.10, 0.05], time_limit=None,
            min_days=[4, 4], dd_type="static", dd=0.10, dll=0.05,
            funded=dict(split=0.8, first_wait=10, cycle=10))
SHIELD = dict(level=0.02, cut_split=0.5, breach_on=2)


# ------------------------------------------------- D1 is reproduced exactly
def test_no_stress_reproduces_d1_eval_and_funded():
    F = FIRMS["FTMO Swing 2-Step 100K"]
    sig = np.array([0.08, 0.2, 0.3])
    a, b = D1.eval_sim(F, 1.2, sig, n=200), M.eval_sim(F, 1.2, sig, n=200)
    for k in ("p_pass", "t_pass", "t_fail", "fee_pass"):
        assert np.array_equal(a[k], b[k])
    a, b = D1.funded_sim(F, 0.5, sig, n=200), M.funded_sim(F, 0.5, sig, n=200)
    for k in ("life", "pay", "n_pay", "breach", "p_refund"):
        assert np.array_equal(a[k], b[k])


def test_no_stress_reproduces_d1_economics_grid():
    F = FIRMS["Blue Guardian 2-Step 100K"]
    sig = np.array([0.12, 0.25])
    a = D1.economics(F, 1.0, n=150, sigmas=sig)
    b = M.economics(F, 1.0, n=150, sigmas=sig, stress={})
    assert np.array_equal(a["grid"], b["grid"]) and a["net_yr"] == b["net_yr"]


def test_capped_helper_matches_uncapped_optimum():
    F = FIRMS["FTMO Swing 2-Step 100K"]
    sig = np.array([0.1, 0.2, 0.3])
    e = M.economics(F, 1.0, n=150, sigmas=sig)
    assert M.capped(e["grid"], sig, 0.3)[0] == e["net_yr"]
    v, se, sf = M.capped(e["grid"], sig, 0.2)
    assert se <= 0.2 and sf <= 0.2 and v <= e["net_yr"]


# ------------------------------------------------------------ the market
def _days(stress, days=5000, n=400, seed=3):
    C = M.cfg(stress)
    sd = np.full((1, n), 1.0, np.float32); mu = np.zeros((1, n), np.float32)
    mk = M.Market(C, mu, sd, (1, n), np.random.default_rng(seed))
    return np.array([sum(mk.day(d))[0] for d in range(days)])   # (days, n)


def test_gaps_keep_annual_variance_and_load_mondays():
    x = _days(dict(gap_frac=0.25, weekend_var=1.0, df=5))
    assert abs(x.var() - 1.0) < 0.03                       # sigma unchanged
    mon, rest = x[0::5].var(), np.delete(x, np.s_[0::5], axis=0).var()
    assert 1.8 < mon / rest < 2.2                          # Monday carries 2 days


def test_gap_arrives_before_the_first_check():
    C = M.cfg(dict(gap_frac=0.5, df=5))
    mk = M.Market(C, np.zeros((1, 20000), np.float32), np.ones((1, 20000), np.float32),
                  (1, 20000), np.random.default_rng(1))
    incs = mk.day(1)
    v = [float(i.var()) for i in incs]
    assert abs(v[0] - (0.5 + 0.5 / 4)) < 0.05 and abs(v[1] - 0.5 / 4) < 0.02


def test_t3_is_unit_variance_and_fatter_than_t5():
    rng = np.random.default_rng(0)
    z3, z5 = M._t(rng, (2_000_000,), 3), M._t(rng, (2_000_000,), 5)
    assert abs(z3.var() - 1) < 0.15                        # t3 variance converges slowly
    q3, q5 = np.quantile(np.abs(z3), 0.9999), np.quantile(np.abs(z5), 0.9999)
    assert q3 > q5                                         # fatter far tail
    assert np.median(np.abs(z3)) < np.median(np.abs(z5))   # thinner shoulders


def test_garch_mean_one_and_clusters():
    x = _days(dict(garch=(0.10, 0.88, 16.0), df=5), days=4000, n=300)
    assert abs(x.var() - 1.0) < 0.15
    s = x ** 2
    ac = np.mean([np.corrcoef(s[:-1, i], s[1:, i])[0, 1] for i in range(s.shape[1])])
    assert ac > 0.05
    y = _days(dict(df=5), days=4000, n=300) ** 2
    ac0 = np.mean([np.corrcoef(y[:-1, i], y[1:, i])[0, 1] for i in range(y.shape[1])])
    assert abs(ac0) < 0.01


# ----------------------------------------------------------- the account
def _acc(F=BASE, **st):
    return M.Account(F, (1,), 100_000., M.cfg(st))


def test_kill_switch_flattens_instead_of_breaching():
    a = _acc(kill=0.8)
    dead = a.step(np.array([-4_500.], np.float32), np.array([True]))
    assert not dead[0] and a.halted[0]
    dead = a.step(np.array([-4_500.], np.float32), np.array([True]))
    assert not dead[0] and float(a.bal[0]) == 95_500.      # flat: no more loss today


def test_gap_jumps_through_kill_switch():
    a = _acc(kill=0.8)
    assert a.step(np.array([-6_000.], np.float32), np.array([True]))[0]


def test_kill_switch_survives_where_d1_breaches():
    F = dict(BASE, dll=0.03)
    no = M.eval_sim(F, -1000, SIG, n=100)
    ks = M.eval_sim(F, -1000, SIG, n=100, stress=dict(kill=0.5))
    assert no["t_fail"][0] == 0                            # D1: dead on day 1
    assert ks["t_fail"][0] >= 4 and ks["p_pass"][0] == 0   # halts daily, dies at -10%


def test_dll_reference_conventions():
    # closed balance never realises (real_rate 0): +3% floating at midnight
    for ref, floor in (("equity", 98_000.), ("balance", 95_000.), ("max", 98_000.)):
        a = _acc(dll_ref=ref, real_rate=0.0)
        a.step(np.array([3_000.], np.float32), np.array([True])); a.end_day()
        assert float(a.day0[0]) - a.dll == floor
    # -3% floating at midnight: "equity" leaves 5% room, "max"/"balance" 2%
    for ref, dies in (("equity", False), ("balance", True), ("max", True)):
        a = _acc(dll_ref=ref, real_rate=0.0)
        a.step(np.array([-3_000.], np.float32), np.array([True])); a.end_day()
        assert bool(a.step(np.array([-2_500.], np.float32), np.array([True]))[0]) == dies


def test_real_rate_moves_closed_balance():
    a = _acc(real_rate=0.25)
    a.step(np.array([4_000.], np.float32), np.array([True])); a.end_day()
    assert float(a.closed[0]) == 101_000.
    b = _acc()                                             # D1: balance == equity
    b.step(np.array([4_000.], np.float32), np.array([True])); b.end_day()
    assert float(b.closed[0]) == 104_000.


def test_shield_cuts_then_breaches_only_on_funded():
    G = dict(BASE, _funded=True, dll=0.10)
    a = _acc(G, shield=SHIELD, real_rate=0.0)
    d = a.step(np.array([-2_500.], np.float32), np.array([True]))
    assert not d[0] and a.shield_hits[0] == 1 and a.halted[0]
    assert float(a.closed[0]) == 97_500.                   # positions closed
    a.end_day()
    assert a.step(np.array([-2_500.], np.float32), np.array([True]))[0]
    e = _acc(dict(BASE, dll=0.10), shield=SHIELD, real_rate=0.0)   # evaluation
    assert not e.step(np.array([-2_500.], np.float32), np.array([True]))[0]
    assert e.shield_hits[0] == 0


def test_shield_cut_split_applies_to_payouts():
    G = dict(BASE, funded=dict(split=0.8, first_wait=10, cycle=10, max_payouts=1, dll=0.5),
             dd=0.5)
    up = M.funded_sim(G, 1000, SIG, n=50, horizon=30, stress=dict(shield=SHIELD))
    assert up["shield"][0] == 0 and 0.8 * 39_000 < up["pay"][0] < 0.8 * 40_500
    down = M.funded_sim(G, -1000, SIG, n=50, horizon=30,
                        stress=dict(shield=SHIELD, real_rate=0.0))
    assert down["breach"][0] == 1.0 and down["n_pay"][0] == 0


def test_breach_before_first_payout_reported():
    f = M.funded_sim(BASE, -1000, SIG, n=50, horizon=30)
    assert f["breach_pre1"][0] == 1.0


def test_day_profit_cap_cuts_excess():
    a = _acc(dict(BASE, day_cap=3_000.))
    a.step(np.array([5_000.], np.float32), np.array([True])); a.end_day()
    assert float(a.bal[0]) == 103_000. and float(a.day0[0]) == 103_000.
    b = _acc(dict(BASE, day_cap=3_000.))
    b.step(np.array([-5_000.], np.float32), np.array([True])); b.end_day()
    assert float(b.bal[0]) == 95_000.                      # losses are not capped
