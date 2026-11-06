"""The 16-year one-minute calibration run (synthetic, full Globex session, ~5.7M bars): a driftless walk with a 2R target
and a 1R stop must return mean R ~ 0 at zero cost, and the whole pipeline (generation, tagging, simulate, gate
statistics, nulls) must run in minutes. Opt-in with QE_SLOW=1 because three agents share four cores; the measured
runtime is printed and recorded in CONVENTIONS.md."""
import os
import time

import numpy as np
import pytest

from qe.engine import bars, fills, harness, pnl, rules

pytestmark = pytest.mark.skipif(not os.environ.get("QE_SLOW"), reason="set QE_SLOW=1 to run the 16-year calibration")


class EveryHour(rules.Rule):
    name = "every-hour-2R"
    params = {"stop": 8.0, "rr": 2.0}
    continuous = ("stop", "rr")

    def orders(self, b):
        t = b["tday_minute"].to_numpy()
        idx = np.nonzero((t % 60 == 0) & b["in_session"].to_numpy())[0]
        n = len(idx)
        return fills.BracketOrders(idx, np.ones(n, int), np.full(n, self.params["stop"]), np.full(n, self.params["stop"] * self.params["rr"]))


def test_sixteen_year_one_minute_calibration_runs_in_minutes():
    t0 = time.time()
    b = bars.synthetic_walk("2009-01-01", "2024-12-31", sigma_per_min=1.0, seed=16)
    t_gen = time.time() - t0
    assert len(b) > 5_000_000
    cfg = pnl.RunConfig(firm="topstep", inst_overrides={"slip_pts": 0.0, "commission": 0.0})
    t1 = time.time()
    res = pnl.simulate(b, EveryHour(), cfg)
    t_sim = time.time() - t1
    r = res.trades["r_mult"].to_numpy()
    se = r.std(ddof=1) / np.sqrt(len(r))
    assert len(r) > 20_000
    assert abs(r.mean()) < 3 * se, (r.mean(), se, len(r))
    t2 = time.time()
    g = harness.gate_statistics(res)                        # 430,000 draws
    rn = harness.random_entry_null(b, res, n_paths=10_000)
    pm = harness.shuffled_signal_permutation(b, res, n_perm=1000)
    lag = harness.execution_lag_variants(b, EveryHour(), cfg)
    t_h = time.time() - t2
    total = time.time() - t0
    print(f"\n16y calibration: bars={len(b):,} trades={len(r):,} meanR={r.mean():.4f} se={se:.4f} "
          f"gen+tag={t_gen:.1f}s simulate={t_sim:.1f}s gate+nulls+lag={t_h:.1f}s total={total:.1f}s")
    assert g["criterion_4_significance"]["n_draws"] == 430_000
    assert not g["criterion_4_significance"]["passed"]
    assert total < 15 * 60
