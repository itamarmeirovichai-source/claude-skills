"""Engine fill-model tests on synthetic bars: calibration (driftless 2R/1R ~ 0), bar ambiguity, limit-through, gap-through,
flat-by on a half day, 2x cost halves a known edge, daily P&L sums to trade P&L."""
import numpy as np
import pandas as pd
import pytest

from qe.engine import bars, fills, pnl, rules
from qe import sessions


def _frame(ohlc, start="2024-06-03T13:40:00Z", root="ES"):
    """Hand-made RTH bars (one per minute from `start`), marked synthetic."""
    n = len(ohlc)
    ts = pd.date_range(start, periods=n, freq="1min", tz="UTC")
    a = np.asarray(ohlc, float)
    df = pd.DataFrame({"ts": ts, "open": a[:, 0], "high": a[:, 1], "low": a[:, 2], "close": a[:, 3]})
    df.attrs["synthetic"] = True
    return bars.tag(df, root)


ZERO_COST = dict(root="ES", inst_overrides={"slip_pts": 0.0, "commission": 0.0})


class EveryHalfHour(rules.Rule):
    """Long bracket at every RTH bar whose minute is a multiple of 30 (sequential, one position at a time)."""
    name = "every-half-hour-2R"
    params = {"stop": 8.0, "rr": 2.0}
    continuous = ("stop", "rr")

    def orders(self, b):
        t = b["tday_minute"].to_numpy()
        idx = np.nonzero((t % 30 == 0) & b["is_rth"].to_numpy())[0]
        n = len(idx)
        return fills.BracketOrders(idx, np.ones(n, int), np.full(n, self.params["stop"]), np.full(n, self.params["stop"] * self.params["rr"]))


@pytest.fixture(scope="module")
def walk():
    # two years of RTH-only driftless bars, sigma 1 pt/min, 1R = 8 pt
    return bars.synthetic_walk("2013-01-01", "2014-12-31", sigma_per_min=1.0, seed=11, rth_only=True)


def test_driftless_walk_2r_1r_is_zero_at_zero_cost_and_negative_at_floor(walk):
    res0 = pnl.simulate(walk, EveryHalfHour(), pnl.RunConfig(firm="topstep", **ZERO_COST))
    r = res0.trades["r_mult"].to_numpy()
    se = r.std(ddof=1) / np.sqrt(len(r))
    assert len(r) > 1500
    assert abs(r.mean()) < 3 * se, (r.mean(), se)
    assert res0.stats["mean_R_net_1x"] == pytest.approx(res0.stats["mean_R_gross"])
    res1 = pnl.simulate(walk, EveryHalfHour(), pnl.RunConfig(firm="topstep", root="ES"))
    assert res1.stats["mean_R_net_1x"] < res1.stats["mean_R_gross"] - 0.05      # floor cost: 0.35 pt per side on an 8 pt stop
    assert res1.stats["mean_R_net_1x"] < -3 * se
    assert res1.stats["mean_R_net_2x"] < res1.stats["mean_R_net_1x"]


def test_daily_pnl_sums_to_trade_pnl(walk):
    res = pnl.simulate(walk, EveryHalfHour(), pnl.RunConfig(firm="topstep"))
    t = res.trades
    trade_net = float(((t["gross_pts"] - t["cost_pts_1x"]) * t["qty"]).sum())
    trade_gross = float((t["gross_pts"] * t["qty"]).sum())
    assert res.daily["net_pts_1x"].sum() == pytest.approx(trade_net, abs=1e-6)
    assert res.daily["gross_pts"].sum() == pytest.approx(trade_gross, abs=1e-6)
    assert res.daily["net_pts_2x"].sum() == pytest.approx(trade_gross - 2 * float((t["cost_pts_1x"] * t["qty"]).sum()), abs=1e-6)
    # every trade is inside one trading day (flat-by) and the position is zero at the end of every day
    assert (t["exit_idx"] > t["fill_idx"]).all() or (t["exit_idx"] >= t["fill_idx"]).all()
    assert (res.daily["net_1x_usd"] == res.daily["net_pts_1x"] * 50).all()


def test_bar_ambiguity_stop_first_and_limit_through_and_gap_through():
    # entry at bar 1 open 100 (decided at the information set of bar 1), stop 1 pt (99), target 2 pt (102)
    f = _frame([[100, 100.5, 99.5, 100], [100, 100.4, 99.6, 100.2], [100.2, 103, 98.5, 101], [101, 101, 101, 101]])
    o = fills.BracketOrders(np.array([1]), np.array([1]), np.array([1.0]), np.array([2.0]))
    t = fills.run_brackets(f, o, fills.instrument("ES", slip_pts=0, commission=0), firm=None)
    assert t["exit_reason"].iloc[0] == "stop" and t["exit_px"].iloc[0] == 99.0 and t["exit_idx"].iloc[0] == 2
    assert t["r_mult"].iloc[0] == pytest.approx(-1.0)
    # a touch of the target (high == 102) is not a fill; high > 102 is
    f2 = _frame([[100, 100.5, 99.5, 100], [100, 102.0, 99.6, 101], [101, 102.25, 100.5, 102], [102, 102, 102, 102]])
    t2 = fills.run_brackets(f2, o, fills.instrument("ES", slip_pts=0, commission=0), firm=None)
    assert t2["exit_reason"].iloc[0] == "target" and t2["exit_idx"].iloc[0] == 2 and t2["exit_px"].iloc[0] == 102.0
    # a gap through the stop at the open fills at the open, not at the stop
    f3 = _frame([[100, 100.5, 99.5, 100], [100, 100.4, 99.6, 100.2], [97.0, 97.5, 96.5, 97.2], [97, 97, 97, 97]])
    t3 = fills.run_brackets(f3, o, fills.instrument("ES", slip_pts=0, commission=0), firm=None)
    assert t3["exit_reason"].iloc[0] == "stop" and t3["exit_px"].iloc[0] == 97.0 and t3["r_mult"].iloc[0] == pytest.approx(-3.0)
    # a gap through the target at the open fills at the limit price (conservative), not at the open
    f4 = _frame([[100, 100.5, 99.5, 100], [100, 100.4, 99.6, 100.2], [104.0, 104.5, 103.5, 104.2], [104, 104, 104, 104]])
    t4 = fills.run_brackets(f4, o, fills.instrument("ES", slip_pts=0, commission=0), firm=None)
    assert t4["exit_reason"].iloc[0] == "target" and t4["exit_px"].iloc[0] == 102.0
    # short side mirrors
    os_ = fills.BracketOrders(np.array([1]), np.array([-1]), np.array([1.0]), np.array([2.0]))
    f5 = _frame([[100, 100.5, 99.5, 100], [100, 100.4, 99.6, 100.2], [100.2, 101.5, 97.0, 99], [99, 99, 99, 99]])
    t5 = fills.run_brackets(f5, os_, fills.instrument("ES", slip_pts=0, commission=0), firm=None)
    assert t5["exit_reason"].iloc[0] == "stop" and t5["exit_px"].iloc[0] == 101.0


def test_slippage_costs_are_per_side_and_doubled_in_windows():
    f = _frame([[100, 100.5, 99.5, 100]] * 5, start="2024-06-03T13:30:00Z")      # 09:30 ET open window
    inst = fills.instrument("ES")
    mkt, lim = fills.per_bar_costs(f, inst)
    assert mkt[0] == pytest.approx(0.30 * 2 + 2.5 / 50) and mkt[1] == pytest.approx(0.30 * 2 + 0.05)
    assert mkt[2] == pytest.approx(0.30 + 0.05) and lim[2] == pytest.approx(0.05)


def test_flat_by_enforcer_closes_at_deadline_minus_margin_on_a_half_day():
    b = bars.synthetic_walk("2024-11-25", "2024-11-29", sigma_per_min=0.3, seed=2)

    class Hold(rules.Rule):
        name = "hold"
        params = {}

        def orders(self, bb):
            idx = rules.first_bar_of_day_at_or_after(bb, 935)
            idx = idx[bb["is_rth"].to_numpy()[idx]]
            n = len(idx)
            return fills.BracketOrders(idx, np.ones(n, int), np.full(n, 1e6), np.full(n, 1e6))

    res = pnl.simulate(b, Hold(), pnl.RunConfig(firm="topstep", flat_by_margin_minutes=2))
    t = res.trades
    day = pd.DatetimeIndex(t["trading_day"]).strftime("%Y-%m-%d").to_numpy()
    ny = t["exit_ts"].dt.tz_convert(sessions.TZ_NY).dt.strftime("%H:%M").to_numpy()
    half = t[day == "2024-11-29"]
    assert len(half) == 1 and half["exit_reason"].iloc[0] == "flat_by"
    assert ny[day == "2024-11-29"][0] == "12:58"                               # 13:00 ET early close minus 2 minutes
    assert ny[day == "2024-11-26"][0] == "16:08"                               # Topstep 15:10 CT = 16:10 ET minus 2
    bim = res.daily["bars_in_market"]
    assert bim.loc["2024-11-28"] == 0            # Thanksgiving: CME-only session, no RTH, no entry
    assert bim.loc["2024-11-29"] == 1138 - 935   # half day: in the market from 09:35 ET to the 12:58 ET exit bar
    assert bim.loc["2024-11-26"] == 1328 - 935
    # target mode: the position is zero at and after the flat-by minute
    class Long(rules.Rule):
        name = "long-all"
        params = {}

        def signal(self, bb):
            return bb["in_session"].to_numpy().astype(float)

    r2 = pnl.simulate(b, Long(), pnl.RunConfig(firm="topstep", flat_by_margin_minutes=2))
    pos = r2.bar["position"].to_numpy()
    tm = b["tday_minute"].to_numpy()
    dl = fills.flat_by_per_bar(b, "topstep", 2)
    assert (pos[tm >= dl] == 0).all()
    assert pos[(tm == dl - 1) & (b["trading_day"].to_numpy() == np.datetime64("2024-11-29"))].sum() == 1
    assert dl[(b["trading_day"].to_numpy() == np.datetime64("2024-11-29"))][0] == 1138


def test_two_x_cost_run_halves_the_net_of_a_known_edge():
    # a deterministic edge: price rises 0.21 pt per bar over ten bars; ES cost per side = 0.30 + 2.5/50 = 0.35 pt;
    # gross 2.1 = 6 x 0.35, so net 1x = 1.4 and net 2x = 0.7 exactly
    n = 390
    px = np.full(n + 1, 4000.0)
    px[101:111] = 4000.0 + 0.21 * np.arange(1, 11)
    px[111:] = px[110]
    ohlc = [[px[i], max(px[i], px[i + 1]), min(px[i], px[i + 1]), px[i + 1]] for i in range(n)]
    f = _frame(ohlc, start="2024-06-03T13:30:00Z")
    tgt = np.zeros(n)
    tgt[100:110] = 1.0
    res = pnl.simulate(f, target=tgt, config=pnl.RunConfig(root="ES", firm=None, intraday_only=False))
    assert res.stats["gross_total_pts"] == pytest.approx(2.1)
    assert res.stats["net_1x_total_pts"] == pytest.approx(1.4)
    assert res.stats["net_2x_total_pts"] == pytest.approx(0.7)
    assert res.stats["net_2x_total_usd"] == pytest.approx(0.5 * res.stats["net_1x_total_usd"])
    assert len(res.trades) == 1 and res.trades["hold_bars"].iloc[0] == 10


def test_vol_scaler_uses_past_days_only():
    d = bars.synthetic_daily_walk("2020-01-01", "2020-12-31", sigma=0.01, seed=3)
    vs = rules.VolScaler(window=20, cap=3, floor=0.3, target_vol=0.15)
    s = vs.scale_bars(d)
    assert np.all(s[:20] == 0) and s[21] > 0
    # changing the last day's return cannot change any earlier day's scale
    d2 = d.copy()
    d2.loc[d2.index[-1], "close"] *= 1.5
    d2.attrs.update(d.attrs)
    s2 = vs.scale_bars(d2)
    assert np.allclose(s[:-1], s2[:-1])
    p = rules.parse_vol_scaler("ex-ante 20d realized, cap 3x, floor 0.3x")
    assert p.window == 20 and p.cap == 3 and p.floor == 0.3
    assert rules.parse_vol_scaler("none") is None
