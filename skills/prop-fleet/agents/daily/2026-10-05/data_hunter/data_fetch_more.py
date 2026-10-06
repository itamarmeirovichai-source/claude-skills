#!/usr/bin/env python3
"""Fetch the intraday files found by the data hunter on 2026-10-05.

Same contract as daily/2026-10-04/data_fetch.py: every URL is pinned to a git
commit, every file is checked against the sha256 and byte size measured on
2026-10-05, and files go to a cache OUTSIDE the repository
($CLAUDE_SCRATCH/intraday or /tmp/prop-fleet-data/intraday). Never commit them.

    python3 data_fetch_more.py              # fetch all small/medium files
    python3 data_fetch_more.py es_1m_rth    # fetch one

LICENSE WARNING: es_1m_rth / es_5m / es_1m_24h_lfs are FirstRateData files
(vendor README: "copyright FirstRateData.com", license at firstratedata.com/about/license);
es_1m_databento is Databento data whose uploader's own docs say "no redistribution".
Third parties published them on GitHub. Research use only; the director decides.
"""
import hashlib
import os
import sys
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"
LFS = "https://media.githubusercontent.com/media/{repo}/{sha}/{path}"

# name: (url template, repo, commit, path, bytes, sha256 or None, what)
SOURCES = {
    "es_1m_rth": (RAW, "jimmuell/mes-orb-strategy", "48993b9c446922f00b9cee9d526007b6e2b88a5b",
                  "api/data/ES_full_1min_rth.parquet", 28349422,
                  "093596df077abd90feac0c6f18d65626c718580969a3c36e97116e01b4737b9e",
                  "ES 1m RTH 09:30-15:59 ET naive, 2008-01-02..2026-04-10, FirstRate continuous UNadjusted"),
    "es_5m": (RAW, "jimmuell/mes-orb-strategy", "48993b9c446922f00b9cee9d526007b6e2b88a5b",
              "api/data/ES_full_5min_continuous_UNadjusted.parquet", 19890248,
              "3d2c4864788a49dc2ec67fdfac18e276fd1c248393b4f76faaa4c185baf9982a",
              "ES 5m 24h ET naive, 2008-01-02..2026-04-09, FirstRate continuous UNadjusted"),
    "es_1m_24h_lfs": (LFS, "jimmuell/mes-orb-strategy", "48993b9c446922f00b9cee9d526007b6e2b88a5b",
                      "data/raw/ES_full_1min_continuous_UNadjusted.txt", 349771494,
                      "b78716f5bb7cd2f7bc07bc6ef5cb9bd5ac9a754154930538cf49633c7fd553db",
                      "ES 1m 24h ET naive, 2008-01-02 06:00..2026-04-10 16:59, no header; sha256 = LFS oid, NOT downloaded in full on 2026-10-05"),
    "es_1m_databento": (RAW, "Warrenn/ibkr-bull-call", "ff3cc44fd124781b8fe915705a1cd23f49edb054",
                        "research/data/dataset-v1/es_intraday.parquet", 27378378,
                        "c4d8b3d2d75431b71a7a4635969cf8de8cec362704aa832242f79183019f792d",
                        "ES 1m 24h UTC, 2021-04-30..2026-04-29 23:59, Databento GLBX.MDP3 ES.c.0 calendar roll"),
    "spy_1m_ibkr": (RAW, "kfhoo88/ibkr-scalper", "da900822d97db03d82ee277fbce1f96643fa2728",
                    "data/historical/SPY_IBKR_1min_1year_20251110.csv", 7341612,
                    "4effe1ed5918e5dea673f181ff6e786d3db40921469f6e0d1907eecf09d51f2c",
                    "SPY 1m RTH, NY offset, 2024-10-31..2025-11-07, IBKR TRADES, unadjusted"),
    "qqq_1m_ibkr": (RAW, "kfhoo88/ibkr-scalper", "da900822d97db03d82ee277fbce1f96643fa2728",
                    "data/historical/QQQ_IBKR_1min_1year_20251110.csv", 7311586,
                    "cc350dd0a17e7038c851d3895cf68d1a07f71ddbadce381c1d0505dbdc1cf2fd",
                    "QQQ 1m RTH, NY offset, 2024-10-31..2025-11-07, IBKR TRADES"),
}
DEFAULT = [k for k in SOURCES if k != "es_1m_24h_lfs"]  # 350 MB file only on request


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
    return tmpl.format(repo=repo, sha=commit, path=path)


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
    for n in (sys.argv[1:] or DEFAULT):
        print(n, fetch(n), SOURCES[n][-1])
