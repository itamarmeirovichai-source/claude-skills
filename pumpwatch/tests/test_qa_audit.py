"""QA: tamper evidence of the hash-chained audit log."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest

from pumpwatch.audit import AuditLog, _digest, config_fingerprint
from pumpwatch.config import Config
from pumpwatch.models import Alert

from qa_helpers import D0


def _log(tmp_path, n=4) -> AuditLog:
    log = AuditLog(tmp_path / "alerts.jsonl")
    for i in range(n):
        log.append(Alert(f"T{i}", D0, 40.0 + i, ("market", "social"), ("r",)), "0.1.0", "cfg")
    return log


def _lines(log):
    return log.path.read_text(encoding="utf-8").splitlines()


def _write(log, lines):
    log.path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# -- correct today -------------------------------------------------------------
def test_clean_log_verifies(tmp_path):
    assert _log(tmp_path).verify().ok


def test_detects_edit_reorder_and_middle_delete(tmp_path):
    log = _log(tmp_path)
    orig = _lines(log)

    rec = json.loads(orig[1])
    rec["alert"]["score"] = 1.0
    _write(log, [orig[0], json.dumps(rec), *orig[2:]])
    assert log.verify().broken_at == 2

    _write(log, [orig[1], orig[0], *orig[2:]])
    assert not log.verify().ok

    _write(log, [orig[0], *orig[2:]])
    assert log.verify().broken_at == 2

    _write(log, orig[1:])
    assert log.verify().broken_at == 1


# -- QA-5: truncation and full rewrite --------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-5")
def test_detects_deleted_tail(tmp_path):
    log = _log(tmp_path)
    _write(log, _lines(log)[:2])
    assert not log.verify().ok


@pytest.mark.xfail(strict=True, reason="QA-5")
def test_detects_rechained_rewrite(tmp_path):
    """Someone with file access drops a record and recomputes every hash."""

    log = _log(tmp_path)
    prev, out = "0" * 64, []
    for line in _lines(log)[1:]:
        rec = json.loads(line)
        rec.pop("hash")
        rec["prev"] = prev
        rec["alert"]["score"] = 0.0
        prev = _digest(rec)
        out.append(json.dumps({**rec, "hash": prev}))
    _write(log, out)
    assert not log.verify().ok


# -- QA-11: malformed lines ----------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="QA-11")
@pytest.mark.parametrize("junk", ["[]", "5", '"x"', "null"])
def test_verify_reports_non_object_line_instead_of_crashing(tmp_path, junk):
    log = _log(tmp_path, 1)
    _write(log, [*_lines(log), junk])
    res = log.verify()
    assert not res.ok and res.broken_at == 2


@pytest.mark.xfail(strict=True, reason="QA-11")
def test_verify_rejects_duplicate_keys(tmp_path):
    """A forged first 'alert' key is what grep and first-key-wins parsers show."""

    log = _log(tmp_path, 1)
    line = _lines(log)[0]
    forged = '{"alert": {"ticker": "FAKE", "score": 99.9}, ' + line[1:]
    _write(log, [forged])
    assert not log.verify().ok


@pytest.mark.xfail(strict=True, reason="QA-11")
def test_append_refuses_to_chain_onto_corrupt_log(tmp_path):
    log = _log(tmp_path, 1)
    _write(log, [*_lines(log), '{"hash": 1}'])
    with pytest.raises(Exception):
        log.append(Alert("X", D0, 50.0, ("market",), ()), "0.1.0", "cfg")


# -- QA-24: fingerprint coverage ------------------------------------------------------------
def test_fingerprint_changes_with_config():
    assert config_fingerprint(Config()) != config_fingerprint(Config().with_(alert_threshold=40.0))


@pytest.mark.xfail(strict=True, reason="QA-24")
def test_fingerprint_covers_rule_tables(monkeypatch):
    import pumpwatch.config as config_mod

    before = config_fingerprint(Config())
    monkeypatch.setattr(config_mod, "NEWS_FORMS", config_mod.NEWS_FORMS | {"FAKE"})
    assert config_fingerprint(Config()) != before
