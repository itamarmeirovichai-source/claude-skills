"""Unit tests for fxtrend.py on synthetic data (no network)."""
import numpy as np
import pandas as pd

import fxtrend as F


def synth(n=900, k=6, seed=1):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2000-01-03", periods=n)
    R = pd.DataFrame(rng.normal(0.0002, 0.01, (n, k)), index=idx,
                     columns=["EURUSD", "GBPUSD", "US500", "GER40", "XAUUSD", "USOIL"])
    meta = pd.DataFrame(dict(cls=["FX", "FX", "IDX", "IDX", "CMD", "CMD"],
                             cost_bps=1.0, swap=0.02, lev=10.0), index=R.columns)
    return R, meta


def test_trend_positions_ignore_the_future():
    R, meta = synth()
    P = F.trend_positions(R, meta)
    R2 = R.copy()
    R2.iloc[600:] = R2.iloc[600:] * -3 + 0.01
    P2 = F.trend_positions(R2, meta)
    assert np.allclose(P.iloc[:600].values, P2.iloc[:600].values)


def test_no_position_before_entry():
    R, meta = synth()
    P = F.trend_positions(R, meta)
    assert (P.iloc[:F.ENTRY_DAYS - 1].abs().sum().sum()) == 0


def test_buffer_holds_small_changes():
    T = pd.DataFrame({"a": [1.0, 1.05, 1.2, 0.0]})
    H = F.execute(T)
    assert list(H["a"]) == [1.0, 1.0, 1.2, 0.0]


def test_pnl_lag_and_costs():
    idx = pd.bdate_range("2020-01-01", periods=4)
    H = pd.DataFrame({"x": [1.0, 1.0, 0.0, 0.0]}, index=idx)
    R = pd.DataFrame({"x": [0.01, 0.02, 0.03, 0.04]}, index=idx)
    meta = pd.DataFrame(dict(cls=["FX"], cost_bps=10.0, swap=0.0, lev=10.0), index=["x"])
    dcal = pd.Series(1.0, index=idx)
    out = F.pnl(H, R, meta, dcal, lag=1)
    assert np.allclose(out["gross"].values, [0, 0.02, 0.03, 0])
    assert np.allclose(out["cost"].values, [0.001, 0, 0.001, 0])
    out2 = F.pnl(H, R, meta, dcal, lag=2)
    assert np.allclose(out2["gross"].values, [0, 0, 0.03, 0.04])


def test_prop_sim_rules():
    # constant +1%/day at 10% vol: passes phase 1 on day 10, phase 2 on day 5
    net = np.full(50, 0.01)
    margin = np.zeros(50)
    idx = np.tile(np.arange(50) % 50, (3, 1))[:, :40]
    out = F.prop_sim(net, margin, 1.0, idx, max_eval=504, funded_days=21)
    assert out["p_pass"] == 1.0 and out["med_days_pass"] == 15
    # one -4% day kills it
    net2 = net.copy()
    net2[2] = -0.04
    out2 = F.prop_sim(net2, margin, 1.0, idx)
    assert out2["p_pass"] == 0.0 and out2["p_blow_eval"] == 1.0


def test_boot_paths_shape_and_range():
    idx = F.boot_paths(100, 7, 300)
    assert idx.shape == (7, 300) and idx.min() >= 0 and idx.max() < 100
