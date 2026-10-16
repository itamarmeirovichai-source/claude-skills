"""Unit tests for stocks.py (synthetic data, no network)."""
import numpy as np
import pandas as pd

import stocks as S


def test_rank_weights_dollar_neutral():
    rng = np.random.default_rng(0)
    sig = pd.DataFrame(rng.normal(size=(5, 8)))
    E = pd.DataFrame(True, index=sig.index, columns=sig.columns)
    E.iloc[0, :3] = False
    W = S.rank_w(sig, E)
    assert np.allclose(W.sum(axis=1), 0)
    assert np.allclose(W.abs().sum(axis=1), 1)
    assert (W.iloc[0, :3] == 0).all()


def test_weekly_holds_last_day_of_week():
    cal = pd.bdate_range("2024-01-01", periods=10)
    W = pd.DataFrame({"a": np.arange(10.0)}, index=cal)
    out = S.weekly(W)
    assert out.loc["2024-01-05", "a"] == 4 and out.loc["2024-01-08", "a"] == 4
    assert out.loc["2024-01-12", "a"] == 9


def test_cc_pnl_lag_and_costs():
    cal = pd.bdate_range("2024-01-01", periods=4)
    r = pd.DataFrame({"x": [0, 0.01, 0.02, -0.01], "y": [0, -0.01, 0.0, 0.01]},
                     index=cal)
    D = dict(r=r, nights=pd.Series(1.0, index=cal), on=r * 0, idr=r * 0)
    W = pd.DataFrame({"x": [0.5, 0.5, 0.5, 0.5], "y": [-0.5] * 4}, index=cal)
    net = S.pnl("E1-01", W, None, D, "B", lag=0, cost_mult=0.0)
    # weights at close t earn t+1
    assert np.isclose(net.iloc[1], 0.5 * 0.01 + 0.5 * 0.01)
    assert np.isclose(net.iloc[0], 0)
    n1 = S.pnl("E1-01", W, None, D, "B", lag=0, cost_mult=1.0)
    trade_cost = 1.0 * (S.COMM + S.HALF["B"])
    swap = (0.5 * S.SW_LONG + 0.5 * S.SW_SHORT) / 365
    assert np.isclose(n1.iloc[1], net.iloc[1] - trade_cost - swap)
    assert np.isclose(n1.iloc[2], net.iloc[2] - swap)


def test_overnight_intraday_identity():
    rng = np.random.default_rng(1)
    C = pd.DataFrame(100 * np.exp(np.cumsum(rng.normal(0, 0.01, (50, 3)), 0)))
    O = C.shift(1) * np.exp(rng.normal(0, 0.005, (50, 3)))
    AC = C * 0.9
    r = AC / AC.shift(1) - 1
    f = (AC / C) / (AC / C).shift(1)
    on = O * f / C.shift(1) - 1
    idr = C / O - 1
    assert np.allclose(((1 + on) * (1 + idr)).iloc[2:], (1 + r).iloc[2:])
