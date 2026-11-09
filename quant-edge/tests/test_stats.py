import math
import numpy as np
import pytest
from qe import stats


def test_bar_constants():
    assert abs(stats.Z_BAR - 3.6807) < 1e-3
    assert stats.MIN_DRAWS == 430000
    assert abs(stats.bar_sharpe_units(10) - 1.164) < 1e-2
    assert abs(stats.power(1.5, 5) - 0.37) < 0.02


def test_driftless_walk_does_not_pass():
    rng = np.random.default_rng(1)
    x = rng.standard_t(4, size=2500) * 0.01
    t_min, t_iid, t_nw = stats.gate_t(x)
    assert abs(t_min) < 3.0
    bb = stats.stationary_bootstrap_mean(x, n_draws=20_000)
    assert bb["lower_alpha"] < 0 and bb["n_draws"] == 20_000


def test_strong_drift_passes_and_nw_below_iid_under_autocorrelation():
    rng = np.random.default_rng(2)
    n = 2520
    e = rng.standard_normal(n)
    ar = np.empty(n); ar[0] = e[0]
    for i in range(1, n):
        ar[i] = 0.5 * ar[i - 1] + e[i]
    x = 0.30 + ar  # positive mean (t well above the bar), positively autocorrelated
    t_min, t_iid, t_nw = stats.gate_t(x)
    assert t_nw < t_iid
    assert t_min == t_nw
    bb = stats.stationary_bootstrap_mean(x, n_draws=20_000, mean_block=20)
    assert bb["lower_alpha"] > 0


def test_day_cluster_bootstrap_and_clustered_t():
    rng = np.random.default_rng(3)
    days = np.repeat(np.arange(400), 3)
    day_effect = rng.standard_normal(400)[days]       # strong within-day correlation
    r = 0.05 + day_effect + 0.1 * rng.standard_normal(days.size)
    t_c = stats.clustered_t(r, days)
    t_i = stats.iid_t(r)
    assert t_c < t_i                                  # clustering widens the error
    bb = stats.day_cluster_bootstrap_mean(r, days, n_draws=20_000)
    assert bb["n_days"] == 400 and bb["p5"] < bb["p50"]


def test_sharpe_se_matches_normal_case():
    rng = np.random.default_rng(4)
    x = rng.standard_normal(5000) * 0.01 + 0.0005
    out = stats.sharpe_se(x)
    # normal returns: se ~ sqrt((1 + 0.5 SR^2)/n)
    sr = out["sharpe_period"]
    assert abs(out["se_period"] - math.sqrt((1 + 0.5 * sr * sr) / 5000)) < 2e-3
    assert out["ci90_annual"][0] < out["sharpe_annual"] < out["ci90_annual"][1]


def test_deflated_sharpe_null_is_low_and_skill_is_high():
    # 430 trials of noise, best one picked: DSR should not call it skill
    T = 2520
    rng = np.random.default_rng(5)
    srs = rng.standard_normal((430, T)).mean(1) / rng.standard_normal((430, T)).std(1)
    best = float(srs.max())
    d = stats.deflated_sharpe(best, 430, float(srs.var()), 0.0, 3.0, T)
    assert d["dsr"] < 0.8
    strong = stats.deflated_sharpe(3.0 / math.sqrt(252), 430, float(srs.var()), 0.0, 3.0, T)
    assert strong["dsr"] > 0.95


def test_cscv_noise_is_conservative_and_skill_is_detected():
    rng = np.random.default_rng(6)
    M = rng.standard_normal((1600, 12)) * 0.01
    out = stats.cscv(M, n_splits=8)
    assert out["n_combos"] == 70
    assert out["pbo"] >= 0.5                     # complementary halves: noise never looks robust
    assert out["p_oos_loss"] >= 0.5               # same bias: read beside a skill column, never alone
    skilled = M.copy(); skilled[:, 0] += 0.0025  # one configuration with true annual Sharpe ~ 4
    out2 = stats.cscv(skilled, n_splits=8)
    assert out2["pbo"] < 0.15 and out2["p_oos_loss"] < 0.05
    single = stats.cscv(M[:, :1])
    assert math.isnan(single["pbo"])
