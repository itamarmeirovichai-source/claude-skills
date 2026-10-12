import numpy as np
import pandas as pd

import meanrev as M


def _df(closes):
    idx = pd.bdate_range("2000-01-03", periods=len(closes))
    c = np.asarray(closes, float)
    return pd.DataFrame(dict(open=c * 0.999, close=c), index=idx)


def test_rsi2_hand():
    c = pd.Series([100, 101, 99, 98, 100.0])
    r = M.rsi2(c)
    # changes +1,-2,-1,+2 ; seed at i=2: au=.5 ad=1 ; i=3: au=.25 ad=1 ; i=4: au=1.125 ad=.5
    assert np.isclose(r.iloc[2], 100 - 100 / 1.5)
    assert np.isclose(r.iloc[3], 100 - 100 / 1.25)
    assert np.isclose(r.iloc[4], 100 - 100 / (1 + 2.25))


def test_exit_after_5_days_and_sma5():
    rng = np.random.default_rng(0)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, 400)))
    df = _df(c)
    pos, notl = M.positions(df, "rsi", ls=True, trend=False)
    runs, cur, k = [], 0, 0
    for p in pos:
        if p != 0 and p == cur:
            k += 1
        else:
            if cur != 0:
                runs.append(k)
            cur, k = p, (1 if p != 0 else 0)
    assert max(runs) <= 5
    # notional is constant inside a run
    for t in range(1, len(pos)):
        if pos[t] != 0 and pos[t] == pos[t - 1]:
            assert notl[t] == notl[t - 1]


def test_close_mode_pnl_sign_and_swap():
    df = _df([100, 101, 102])
    pos = np.array([1.0, 1.0, 0.0])
    notl = np.array([0.5, 0.5, 0.0])
    p = M.pnl(df, pos, notl, -3.65, 0.0, 1.0, "close")
    assert np.isclose(p.gross.iloc[1], 0.5 * 0.01)
    assert np.isclose(p.gross.iloc[2], 0.5 * (102 / 101 - 1))
    assert np.isclose(p.cost.sum(), 2 * 0.5 * 1e-4)
    assert p.swap.iloc[0] < 0 and p.swap.iloc[2] == 0


def test_no_lookahead_truncation_synthetic():
    rng = np.random.default_rng(3)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.012, 600)))
    df = _df(c)
    p_full, _ = M.positions(df, "down3", ls=True, trend=True)
    p_cut, _ = M.positions(df.iloc[:450], "down3", ls=True, trend=True)
    assert np.array_equal(p_full[:450], p_cut)
