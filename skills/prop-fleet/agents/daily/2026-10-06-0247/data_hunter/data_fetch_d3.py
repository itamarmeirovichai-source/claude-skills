#!/usr/bin/env python3
"""Fetch the intraday files found by the data hunter on 2026-10-06.

Same contract as daily/2026-10-04/data_fetch.py and daily/2026-10-05/data_hunter/
data_fetch_more.py: every URL is pinned to a full git commit, every file is
checked against the sha256 and byte size measured on 2026-10-06, and files go to
a cache OUTSIDE the repository ($CLAUDE_SCRATCH/intraday or
/tmp/prop-fleet-data/intraday). Never commit them.

    python3 data_fetch_d3.py                 # everything (~150 MB)
    python3 data_fetch_d3.py nq_1m_db_2020   # one file

LICENSE WARNING: the es_/nq_1m_db_* files are Databento GLBX.MDP3 data that a
third party committed to GitHub (the uploader's own CLAUDE.md calls it "paid
Databento data" and says the cache is "not committed" -- it is). Databento's
terms forbid redistribution. qqq_1m_2017_2026 has no stated vendor; spy_1m_poly
is Polygon data. Research cross-checks only, scratch only; the director decides
(board decision 8, open question 4).
"""
import hashlib
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"

# name: (url template, repo, commit, path, bytes, sha256, what)
SOURCES = {
    "es_1m_db_2019": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2019.parquet", 5115432, "d2a121410d1288a48f18d867fd3a6616bc55554350e6d56605ad27663c29a846", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2019"),
    "es_1m_db_2020": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2020.parquet", 5705014, "61921391b675d018ebad6fa2b4713edac3ab1e73df567e5878a41d382e43cf63", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2020"),
    "es_1m_db_2021": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2021.parquet", 5755150, "a4bbb1e8012b50211d667737a05d0bcb19b60f4bce7320f8926aef3e1adf96a0", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2021"),
    "es_1m_db_2022": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2022.parquet", 5788335, "1aa6c0c790db72e7ff01f27e72b2eedf472fa44bd607963a156cec62fd6ae520", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2022"),
    "es_1m_db_2023": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2023.parquet", 5471123, "818027df76a4272f7dae60177be7e9b671faa36a2ddafd3032f526126478b05f", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2023"),
    "es_1m_db_2024": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2024.parquet", 5771191, "b8774ae5a08cfbf4fd439714e6e08eeefa54423e27b7c47b5f80233629fb9c29", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2024"),
    "es_1m_db_2025": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2025.parquet", 5947255, "80bbbbe64b3363a47eb7bd4e3122c0cde88882930a828972f78ab228639a0577", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2025"),
    "es_1m_db_2026": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures ES/data/es_1m_2026.parquet", 4385672, "727073cf30f89a859d8d80ddc9be5b2c43f83fb48e8300abc39296eff0bb6e73", "ES 1m 23h UTC, Databento GLBX.MDP3 ES.c.0 (calendar roll), year 2026"),
    "nq_1m_db_2019": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2019.parquet", 5679942, "fa4144f49b20358d8ae1ff275ad9aff152a3b0f2205013241c2f7c6648ef456f", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2019"),
    "nq_1m_db_2020": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2020.parquet", 6119408, "0369585b762f41ac5a2a43b1d51e487b5f1fae69a68f9743b3650a834b9f1db2", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2020"),
    "nq_1m_db_2021": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2021.parquet", 5978833, "7dbc96d50c47d64b4fe04b71bcfb0b77e87e0e4ade255866e6b27cca3d27013a", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2021"),
    "nq_1m_db_2022": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2022.parquet", 6275508, "45e8bdea53e3a45f3ab273c1337379a3c73a17c7aa275397e08dc17be3433138", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2022"),
    "nq_1m_db_2023": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2023.parquet", 6209946, "8757468391bccc7a4fd6605b5917fe2ab008f025ac22af1bd6914ae15496ad82", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2023"),
    "nq_1m_db_2024": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2024.parquet", 6214208, "066a0d268a1b91c34f1b67f4f9935a0540adb8dae30983fda99c1f408ee13cc9", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2024"),
    "nq_1m_db_2025": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2025.parquet", 6467264, "ace7bfcd13ed7e5f8db89f9adea0ff238041bc582223a3737b1e24d070afb4ef", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2025"),
    "nq_1m_db_2026": (RAW, "Eric1K/Trading-Overnight-Drift", "e7d69651d4c60efa66a84e0543b4b707602aa14b", "Parent Paper Futures/data/nq_1m_2026.parquet", 4632334, "534d04918f9a0e7a294b477b612b8799a377e91a416213f0ec1e4fbd3bf8f2a2", "NQ 1m 23h UTC, Databento GLBX.MDP3 NQ.c.0 (calendar roll), year 2026"),
    "qqq_1m_2017_2026": (RAW, "soyMarioPineda/Research-QQQ", "cc71b31d168cdd549328ccf4f3d1e9d21b4147b9", "QQQ_1min.csv", 59179002, "a48cbb92cd6cfc58c94e22f0700faa4d77692c295443648027a8aa50bef4792a", "QQQ 1m RTH 2017-01-26..2026-03-06, NY offset, vendor unknown, ~unadjusted (median -0.014..-0.024 USD vs Alpaca SIP)"),
    "spy_1m_poly_2024_2026": (RAW, "trilespharm2/bactest-openclaw", "6b6b00db1c735d76679e8eb0b2085c2623f2cb9c", "data/spy_1min.parquet", 14209995, "3bc080a1259e7a7218bc8ce86d662b2be376f94ec19ae32037c74ebc1e125772", "SPY 1m 04:00-20:00 ET 2024-03-28..2026-08-07, Polygon aggs, epoch-ms UTC, unadjusted (matches IBKR to the cent on 98.2% of bars)"),
}


def cache_dir() -> Path:
    base = os.environ.get("CLAUDE_SCRATCH") or "/tmp/prop-fleet-data"
    p = Path(base) / "intraday"
    p.mkdir(parents=True, exist_ok=True)
    return p


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def url(name: str) -> str:
    tmpl, repo, commit, path, *_ = SOURCES[name]
    return tmpl.format(repo=repo, sha=commit, path=urllib.parse.quote(path))


def verify(path: Path, size: int, digest: str) -> None:
    got_size = path.stat().st_size
    got = sha256(path)
    if got_size != size or got != digest:
        raise SystemExit(f"{path.name}: sha256/size mismatch ({got}, {got_size})")


def fetch(name: str) -> Path:
    _, _, _, path, size, digest, _ = SOURCES[name]
    out = cache_dir() / f"{name}{Path(path).suffix}"
    if out.exists() and out.stat().st_size == size and sha256(out) == digest:
        return out
    urllib.request.urlretrieve(url(name), out)
    verify(out, size, digest)
    return out


if __name__ == "__main__":
    for n in (sys.argv[1:] or SOURCES):
        print(n, fetch(n), SOURCES[n][-1])
