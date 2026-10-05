import csv
import numpy as np
import pytest
from pathlib import Path
from ledger_gate import ledger_n, alpha_z, one_sided_lb, passes_rule3

LEDGER = Path(__file__).resolve().parents[3] / "ledger.csv"


def _write(tmp_path, counts):
    p = tmp_path / "l.csv"
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "count"])
        for i, c in enumerate(counts):
            w.writerow([f"H{i:04d}", c])
    return p


def test_real_ledger_n_is_173():
    assert ledger_n(LEDGER) == 173


@pytest.mark.parametrize("bad", ["", "0", "-2", "1.5", "x"])
def test_invalid_count_rejected(tmp_path, bad):
    with pytest.raises(ValueError):
        ledger_n(_write(tmp_path, ["3", bad]))


def test_alpha_z_matches_board():
    a, z = alpha_z(173)
    assert a == pytest.approx(0.05 / 173)
    assert round(z, 2) == 3.44


def test_draws_resolve_tail():
    rng = np.random.default_rng(1)
    r = rng.normal(0, 1, 400)
    lb, draws = one_sided_lb(r, np.arange(400) // 2, 173)
    assert draws * 0.05 / 173 >= 50


def test_clear_edge_passes_noise_fails():
    rng = np.random.default_rng(2)
    days = np.repeat(np.arange(500), 2)
    assert passes_rule3(rng.normal(0.5, 1, 1000), days, 173)
    assert not passes_rule3(rng.normal(0.0, 1, 1000), days, 173)


def test_clustering_widens_interval():
    rng = np.random.default_rng(3)
    day_shock = np.repeat(rng.normal(0, 1, 100), 10)
    r = 0.1 + day_shock + rng.normal(0, 0.2, 1000)
    lb_iid, _ = one_sided_lb(r, np.arange(1000), 173)
    lb_day, _ = one_sided_lb(r, np.repeat(np.arange(100), 10), 173)
    assert lb_day < lb_iid
