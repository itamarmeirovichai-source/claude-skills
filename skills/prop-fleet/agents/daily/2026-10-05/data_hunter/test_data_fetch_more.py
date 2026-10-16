"""Offline tests for data_fetch_more.py (no network)."""
import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import data_fetch_more as m  # noqa: E402


def test_sources_are_pinned_to_full_commits():
    for name, (tmpl, repo, commit, path, size, digest, what) in m.SOURCES.items():
        assert len(commit) == 40 and all(c in "0123456789abcdef" for c in commit), name
        assert len(digest) == 64, name
        assert size > 1_000_000, name
        assert commit in m.url(name) and path in m.url(name)


def test_big_lfs_file_not_in_default():
    assert "es_1m_24h_lfs" not in m.DEFAULT
    assert m.SOURCES["es_1m_24h_lfs"][0] == m.LFS


def test_cache_dir_outside_repo(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_SCRATCH", str(tmp_path))
    assert m.cache_dir() == tmp_path / "intraday"


def test_verify_rejects_mismatch(tmp_path):
    p = tmp_path / "x.bin"
    p.write_bytes(b"abc")
    good = hashlib.sha256(b"abc").hexdigest()
    m.verify(p, 3, good)
    with pytest.raises(SystemExit):
        m.verify(p, 4, good)
    with pytest.raises(SystemExit):
        m.verify(p, 3, "0" * 64)
