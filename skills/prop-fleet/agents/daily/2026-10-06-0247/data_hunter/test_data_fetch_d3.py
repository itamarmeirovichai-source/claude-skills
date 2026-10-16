"""Offline tests for data_fetch_d3.py (no network)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import data_fetch_d3 as f  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[5]


def test_every_source_is_pinned_and_hashed():
    assert len(f.SOURCES) == 18
    for name, (tmpl, repo, commit, path, size, digest, what) in f.SOURCES.items():
        assert re.fullmatch(r"[0-9a-f]{40}", commit), name
        assert re.fullmatch(r"[0-9a-f]{64}", digest), name
        assert isinstance(size, int) and size > 100_000, name
        assert "/" in repo and what, name


def test_urls_are_raw_github_and_quoted():
    u = f.url("nq_1m_db_2020")
    assert u.startswith("https://raw.githubusercontent.com/Eric1K/Trading-Overnight-Drift/")
    assert "Parent%20Paper%20Futures/data/nq_1m_2020.parquet" in u
    assert " " not in u


def test_years_cover_2019_to_2026_for_es_and_nq():
    for sym in ("es", "nq"):
        assert {int(k[-4:]) for k in f.SOURCES if k.startswith(f"{sym}_1m_db_")} == set(range(2019, 2027))


def test_cache_dir_is_outside_repo(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_SCRATCH", str(tmp_path))
    p = f.cache_dir()
    assert p.exists() and REPO_ROOT not in p.resolve().parents


def test_verify_rejects_bad_file(tmp_path):
    p = tmp_path / "x.bin"
    p.write_bytes(b"abc")
    try:
        f.verify(p, 3, "0" * 64)
    except SystemExit as e:
        assert "mismatch" in str(e)
    else:
        raise AssertionError("verify accepted a wrong digest")
