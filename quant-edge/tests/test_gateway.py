"""Tests for the single data door load(id, window): registration, slicing, logging, hold-out lock, planted leak."""
import csv
from pathlib import Path
import pandas as pd
import pytest

from qe import gateway, registry

REG_COLS = ["id", "date", "owner", "source", "family", "lane", "status", "hypothesis", "rules", "parameters", "grid",
            "sign", "instruments", "holding", "firm_structure", "data", "data_sha256", "split", "vol_scaler",
            "guard_fraction", "decay_haircut", "cost_model", "decision_rule", "count", "rules_fixed_before_test",
            "result_mean_R", "result_p5_R", "result_units", "passed_gate", "registered_commit", "notes"]


def _env(tmp_path: Path):
    reg = tmp_path / "registry.csv"
    with open(reg, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REG_COLS); w.writeheader()
        w.writerow({c: "" for c in REG_COLS} | {"id": "H0012", "source": "inherited", "status": "inherited-closed", "count": "1", "data": "spy"})
        w.writerow({c: "" for c in REG_COLS} | {
            "id": "Q-0001", "source": "program", "status": "registered", "count": "1", "sign": "long",
            "data": "es_1m_rth", "split": "IS=2010-06-06..2014-12-31;OOS=2015-01-01..2024-12-31;HOLDOUT=2025-01-01.."})
        w.writerow({c: "" for c in REG_COLS} | {
            "id": "Q-0002", "source": "program", "status": "registered", "count": "1", "sign": "long",
            "data": "es_1m_rth,es_1m_firstrate[xcheck]", "split": "IS=2010-06-06..2014-12-31;OOS=2015-01-01..2024-12-31;HOLDOUT=2025-01-01.."})
        w.writerow({c: "" for c in REG_COLS} | {
            "id": "Q-0003", "source": "program", "status": "registered", "count": "1", "sign": "long",
            "data": "es_1m_firstrate", "split": "IS=2010-06-06..2014-12-31;OOS=2015-01-01..2024-12-31;HOLDOUT=2025-01-01.."})
    man = tmp_path / "manifest.csv"
    with open(man, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["dataset_id", "path", "source", "licence_status", "resolution", "tz", "start", "end", "sha256", "rows", "notes"])
        w.writerow(["es_1m_rth", "es.csv", "test", "ok", "1m", "UTC", "2010-01-01", "2026-01-01", "x", "5", ""])
        w.writerow(["es_1m_firstrate", "es.csv", "third-party copy", "hold", "1m", "UTC", "2010-01-01", "2026-01-01", "x", "5", ""])
    data_root = tmp_path / "data"; data_root.mkdir()
    # planted rows: one before IS, inside IS, inside OOS, inside hold-out (the leak), far future
    pd.DataFrame({"ts": ["2010-01-04T14:30:00Z", "2012-06-01T14:30:00Z", "2014-12-31T20:59:00Z", "2015-01-02T14:30:00Z",
                         "2020-03-16T14:30:00Z", "2024-12-31T20:59:00Z", "2025-01-02T14:30:00Z", "2026-10-01T14:30:00Z"],
                  "close": [1, 2, 3, 4, 5, 6, 7, 8]}).to_csv(data_root / "es.csv", index=False)
    log = tmp_path / "registry_reads.log"
    unlock = tmp_path / "HOLDOUT_UNLOCK"
    return dict(registry_path=reg, manifest_path=man, data_root=data_root, log_path=log, unlock_path=unlock)


def test_unregistered_id_is_refused(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(registry.UnregisteredHypothesisError):
        gateway.load("Q-9999", "is", **env)


def test_inherited_id_is_refused(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(registry.UnregisteredHypothesisError):
        gateway.load("H0012", "is", **env)


def test_is_slice_and_planted_leak(tmp_path):
    env = _env(tmp_path)
    df = gateway.load("Q-0001", "is", **env)
    assert df["close"].tolist() == [2, 3]
    oos = gateway.load("Q-0001", "oos", **env)
    assert oos["close"].tolist() == [4, 5, 6]          # the 2025 row (7) never appears in OOS
    assert 7 not in df["close"].tolist() and 7 not in oos["close"].tolist()


def test_every_read_is_logged(tmp_path):
    env = _env(tmp_path)
    gateway.load("Q-0001", "is", **env)
    gateway.load("Q-0001", "oos", **env)
    lines = env["log_path"].read_text().splitlines()
    assert lines[0] == "ts_utc,registered_id,window,script,commit"
    assert [l.split(",")[2] for l in lines[1:]] == ["is", "oos"]
    assert all(l.split(",")[1] == "Q-0001" for l in lines[1:])


def test_holdout_locked_without_unlock_file(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(gateway.HoldoutLockedError):
        gateway.load("Q-0001", "holdout", **env)
    assert "holdout-REFUSED" in env["log_path"].read_text()


def test_holdout_locked_when_id_not_listed(tmp_path):
    env = _env(tmp_path)
    env["unlock_path"].write_text("# unlocked 2026-12-05\nQ-0002 some other variant\n")
    with pytest.raises(gateway.HoldoutLockedError):
        gateway.load("Q-0001", "holdout", **env)


def test_holdout_opens_only_for_listed_id(tmp_path):
    env = _env(tmp_path)
    env["unlock_path"].write_text("# unlocked 2026-12-05\nQ-0001 passed Gate 4 on 2026-11-30\n")
    df = gateway.load("Q-0001", "holdout", **env)
    assert df["close"].tolist() == [7, 8]
    assert "Q-0001,holdout," in env["log_path"].read_text()


def test_dataset_must_be_named_in_row_and_manifest(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(ValueError):
        gateway.load("Q-0001", "is", dataset="nq_1m", **env)


def test_bad_window_name(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(ValueError):
        gateway.load("Q-0001", "insample", **env)


def test_licence_held_dataset_is_crosscheck_only(tmp_path):
    env = _env(tmp_path)
    with pytest.raises(gateway.LicenceHoldError):          # listed without [xcheck]: refused in every window
        gateway.load("Q-0003", "is", **env)
    with pytest.raises(gateway.LicenceHoldError):          # OOS read of a held dataset: refused and logged
        gateway.load("Q-0002", "oos", dataset="es_1m_firstrate", **env)
    assert "oos-REFUSED-licence" in env["log_path"].read_text()
    df = gateway.load("Q-0002", "crosscheck", dataset="es_1m_firstrate", **env)
    assert df["close"].tolist() == [4, 5, 6]               # OOS dates, logged as crosscheck
    assert "Q-0002,crosscheck," in env["log_path"].read_text()
    ok = gateway.load("Q-0002", "oos", **env)              # the default dataset (ok licence) still works
    assert ok["close"].tolist() == [4, 5, 6]
