"""Leak harness, registered-id gate, nulls, lag variants and the result writer, all on synthetic bars."""
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from qe import registry
from qe.engine import bars, fills, harness, pnl, report, rules, run


class PastOnlyBracket(rules.Rule):
    """Long 2R/1R bracket at 09:35 ET when yesterday's RTH close was above yesterday's RTH open."""
    name = "past-only"
    params = {"stop": 8.0, "rr": 2.0}
    continuous = ("stop", "rr")

    def orders(self, b):
        d = bars.daily_from_bars(b)
        f = bars.prior_day_features(b, d, cols=("rth_open", "rth_close"))
        idx = rules.first_bar_of_day_at_or_after(b, 935)
        idx = idx[b["is_rth"].to_numpy()[idx]]
        up = f["prev_rth_close"].to_numpy()[idx] > f["prev_rth_open"].to_numpy()[idx]
        idx = idx[up]
        n = len(idx)
        return fills.BracketOrders(idx, np.ones(n, int), np.full(n, self.params["stop"]), np.full(n, self.params["stop"] * self.params["rr"]))


class LookAheadBracket(PastOnlyBracket):
    """The planted leak: the same entry conditioned on TODAY's RTH close above today's RTH open."""
    name = "look-ahead"

    def orders(self, b):
        d = bars.daily_from_bars(b)
        idx = rules.first_bar_of_day_at_or_after(b, 935)
        idx = idx[b["is_rth"].to_numpy()[idx]]
        did = b["day_id"].to_numpy()[idx]
        up = d["rth_close"].reindex(did).to_numpy() > d["rth_open"].reindex(did).to_numpy()
        idx = idx[up]
        n = len(idx)
        return fills.BracketOrders(idx, np.ones(n, int), np.full(n, self.params["stop"]), np.full(n, self.params["stop"] * self.params["rr"]))


class PastOnlyTarget(rules.Rule):
    """Long from 09:35 to 11:00 ET when the previous day's close was above its open (prior-day feature)."""
    name = "past-only-target"
    params = {"end": 1020}
    discrete = ("end",)

    def signal(self, b):
        d = bars.daily_from_bars(b)
        f = bars.prior_day_features(b, d, cols=("open", "close"))
        up = (f["prev_close"] > f["prev_open"]).to_numpy()
        return (rules.minute_mask(b, 935, self.params["end"]) & up).astype(float)


class LeakyTarget(PastOnlyTarget):
    """Planted leak: today's close vs today's open."""
    name = "leaky-target"

    def signal(self, b):
        d = bars.daily_from_bars(b)
        up = (d["close"] > d["open"]).reindex(b["day_id"].to_numpy()).to_numpy()
        return (rules.minute_mask(b, 935, self.params["end"]) & up).astype(float)


@pytest.fixture(scope="module")
def walk():
    return bars.synthetic_walk("2014-01-01", "2014-12-31", sigma_per_min=1.0, seed=7)


def test_truncation_harness_catches_the_planted_look_ahead_and_passes_past_only(walk):
    bad = harness.future_truncation_test(LookAheadBracket(), walk, n_days=20, seed=1)
    assert not bad["passed"] and len(bad["violations"]) >= 3
    good = harness.future_truncation_test(PastOnlyBracket(), walk, n_days=20, seed=1)
    assert good["passed"] and good["n_checked"] == 20
    bad_t = harness.future_truncation_test(LeakyTarget(), walk, n_days=20, seed=1)
    assert not bad_t["passed"]
    good_t = harness.future_truncation_test(PastOnlyTarget(), walk, n_days=20, seed=1)
    assert good_t["passed"]


def test_perturbation_harness(walk):
    assert not harness.perturbation_test(LookAheadBracket(), walk, n_days=10, seed=2)["passed"]
    assert harness.perturbation_test(PastOnlyBracket(), walk, n_days=10, seed=2)["passed"]


def test_engine_refuses_an_unmarked_frame(walk):
    plain = pd.DataFrame(walk).reset_index(drop=True)     # a copy without attrs
    assert not plain.attrs
    with pytest.raises(pnl.UnregisteredRunError):
        pnl.simulate(plain, PastOnlyTarget(), pnl.RunConfig(firm="topstep"))


REG_COLS = ["id", "date", "owner", "source", "family", "lane", "status", "hypothesis", "rules", "parameters", "grid",
            "sign", "instruments", "holding", "firm_structure", "data", "data_sha256", "split", "vol_scaler",
            "guard_fraction", "decay_haircut", "cost_model", "decision_rule", "count", "rules_fixed_before_test",
            "result_mean_R", "result_p5_R", "result_units", "passed_gate", "registered_commit", "notes"]


def _env(tmp_path: Path, walk: pd.DataFrame):
    reg = tmp_path / "registry.csv"
    with open(reg, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REG_COLS)
        w.writeheader()
        w.writerow({c: "" for c in REG_COLS} | {"id": "Q-0001", "source": "program", "status": "registered", "count": "1", "sign": "long",
                                                 "instruments": "ES", "firm_structure": "intraday-futures", "guard_fraction": "0.7",
                                                 "vol_scaler": "none", "data": "syn_es_1m",
                                                 "split": "IS=2014-01-01..2014-06-30;OOS=2014-07-01..2024-12-31;HOLDOUT=2025-01-01.."})
    man = tmp_path / "manifest.csv"
    with open(man, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset_id", "path", "source", "licence_status", "resolution", "tz", "start", "end", "sha256", "rows", "notes"])
        w.writerow(["syn_es_1m", "syn.csv", "test", "ok", "1m", "UTC", "2014-01-01", "2014-12-31", "x", str(len(walk)), "synthetic"])
    data_root = tmp_path / "data"
    data_root.mkdir()
    walk[["ts", "open", "high", "low", "close", "volume"]].to_csv(data_root / "syn.csv", index=False)
    return dict(registry_path=reg, manifest_path=man, data_root=data_root, log_path=tmp_path / "registry_reads.log", unlock_path=tmp_path / "HOLDOUT_UNLOCK")


def test_run_registered_refuses_unregistered_id_and_runs_registered_one(tmp_path, walk):
    env = _env(tmp_path, walk)
    with pytest.raises(registry.UnregisteredHypothesisError):
        run.run_registered("Q-9999", "is", PastOnlyTarget(), **env)
    assert not env["log_path"].exists()
    res = run.run_registered("Q-0001", "is", PastOnlyTarget(), **env)
    assert res.provenance["registered_id"] == "Q-0001" and res.provenance["window"] == "is"
    assert res.config.firm == "topstep" and res.config.root == "ES"
    assert res.daily.index.max() == pd.Timestamp("2014-06-30")      # the straddling trading day 2014-07-01 is dropped
    assert res.daily.index.min() == pd.Timestamp("2014-01-02")      # its session opened 2014-01-01 23:00 UTC, inside the window
    oos = run.run_registered("Q-0001", "oos", PastOnlyTarget(), **env)
    assert oos.daily.index.min() == pd.Timestamp("2014-07-02") and oos.daily.index.max() == pd.Timestamp("2014-12-31")
    lines = env["log_path"].read_text().splitlines()
    assert len(lines) == 3 and [l.split(",")[1:3] for l in lines[1:]] == [["Q-0001", "is"], ["Q-0001", "oos"]]
    # the result writer lists the read
    p = report.write_result("Q-0001", res, out_dir=tmp_path / "results", log_path=env["log_path"], rule_text=PastOnlyTarget().describe(),
                            gate=harness.gate_statistics(res, n_draws=20_000), leaks=[harness.future_truncation_test(PastOnlyTarget(), res_bars(res, walk), n_days=3)],
                            window="is", oos_period="2014-07-01..2024-12-31")
    txt = p.read_text()
    for needle in ("N_total", "3.68", "bar in Sharpe units", "joint power", "By year", "Best-20-days", "registry_reads.log", "Q-0001,is,", "breach"):
        assert needle in txt, needle


def res_bars(res, walk):
    return walk


def test_lag_variants_neighbourhood_delay_nulls_and_benchmark(walk):
    cfg = pnl.RunConfig(firm="topstep")
    res = pnl.simulate(walk, PastOnlyBracket(), cfg)
    lag = harness.execution_lag_variants(walk, PastOnlyBracket(), cfg)
    assert "lag2 (next open + 1 bar)" in lag["runs"] and lag["worst"] in lag["runs"]
    nb = harness.neighbourhood(walk, PastOnlyBracket(), cfg)
    assert len(nb) == 5 and set(nb["parameter"]) == {"(as registered)", "stop", "rr"}
    nbt = harness.neighbourhood(walk, PastOnlyTarget(), cfg)
    assert list(nbt["value"])[1:] == [1019, 1021]
    dl = harness.entry_delay_runs(walk, PastOnlyBracket(), cfg)
    assert list(dl["delay_bars"]) == [0, 1, 5]
    rn = harness.random_entry_null(walk, res, n_paths=2000, seed=0)
    assert rn["n_paths"] == 2000 and 0 <= rn["percentile_gross"] <= 1
    pm = harness.shuffled_signal_permutation(walk, res, n_perm=200)
    assert 0 < pm["p_value"] <= 1 and pm["n_perm"] == 200
    bh = harness.buy_and_hold_matched(walk, res)
    assert bh["exposure_same_minutes"] == pytest.approx(1.0) and "alpha_t_min" in bh["always_long"]
    g = harness.gate_statistics(res, n_draws=20_000)
    assert g["criterion_4_significance"]["n_draws"] == 20_000 and g["z_bar"] == pytest.approx(3.6807, abs=1e-3)
    assert not g["criterion_4_significance"]["passed"]      # a driftless walk never passes


def test_random_entry_null_and_permutation_detect_a_planted_edge():
    b = bars.synthetic_walk("2014-01-01", "2014-12-31", sigma_per_min=1.0, seed=8)
    # plant a drift of +0.2 pt per minute between 09:35 and 11:00 ET on every day (a huge, obvious edge)
    o, h, l, c = (b[k].to_numpy(float).copy() for k in ("open", "high", "low", "close"))
    m = rules.minute_mask(b, 935, 1020)
    bump = np.cumsum(np.where(m, 0.2, 0.0))
    for arr, k in ((o, "open"), (h, "high"), (l, "low"), (c, "close")):
        arr += np.r_[0.0, bump[:-1]] if k == "open" else bump
        b[k] = arr
    b["high"] = np.maximum(b["high"], np.maximum(b["open"], b["close"]))
    b["low"] = np.minimum(b["low"], np.minimum(b["open"], b["close"]))
    class Edge(rules.Rule):
        name = "edge"
        params = {}
        def signal(self, bb):
            return rules.minute_mask(bb, 935, 1020).astype(float)
    res = pnl.simulate(b, Edge(), pnl.RunConfig(firm="topstep"))
    assert res.stats["net_1x_t_min"] > 3.68
    rn = harness.random_entry_null(b, res, n_paths=2000, seed=0)
    assert rn["beats_95pct"]
    pm = harness.shuffled_signal_permutation(b, res, n_perm=200)
    assert pm["p_value"] < 0.05
    dl = harness.entry_delay_runs(b, Edge(), pnl.RunConfig(firm="topstep"))
    assert dl["share_of_base_net"].iloc[1] > 0.5
