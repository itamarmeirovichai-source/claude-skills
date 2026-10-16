#!/usr/bin/env python3
"""Fetch the free intraday files found by the data hunter on 2026-10-04.

Every URL is pinned to a git commit, and every file is checked against the
sha256 measured on 2026-10-04, so a changed upstream file fails loudly.
Files go to a cache directory OUTSIDE the repository (default: $CLAUDE_SCRATCH
or /tmp/prop-fleet-data). Never commit them.

    python3 data_fetch.py            # fetch all
    python3 data_fetch.py spy_rth    # fetch one
"""
import hashlib
import os
import sys
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"
LFS = "https://media.githubusercontent.com/media/{repo}/{sha}/{path}"

# name: (url template, repo, commit, path, bytes, sha256, what)
SOURCES = {
    "spy_rth": (LFS, "Ascensao/Intraday-momentum-strategy",
                "5a9e956994d1ca9ef16e5e0ae6af4ce4e04e87eb", "spy_intra_data.csv",
                35376879, "d4671c48d18bdaab21f4b44e02992d2fc91070b01a357189f67b2305a75f9ee6",
                "SPY 1m RTH 2019-01-02..2025-07-18, Polygon, ET naive, appears dividend back-adjusted (ratio to noiiiise file drifts 0.941->0.997 over 2021-2024)"),
    "spy_rth_raw_2021_2024": (RAW, "noiiiise/SPY-Intraday-Momentum",
                "d5af5981fd66477b5791a445b97077bcd8d07a01", "data/spy_intra_data.csv",
                24058963, "ab9b2790a7af73a16d9776ad81eefdbd7eb4f456e4b4419a95cd1ba0f0bed8eb",
                "SPY 1m RTH 2021-01-04..2024-12-30, ET with offset, likely unadjusted; same volumes as spy_rth"),
    "qqq_sip": (RAW, "ramires666/rtharb",
                "3c95880f5b9977f84e042a4076b96669f2f8f895", "data_cache/QQQ_1m.parquet",
                14213777, "65058e81354645b79c4990f004e1d19ad586a9f28634cbfdf983135d855f8a96",
                "QQQ 1m 04:00-20:00 ET 2024-08-22..2026-08-21, Alpaca SIP, raw"),
    "nq_1m": (RAW, "hindsight-finance/Silver-Bullet-AM-Session",
                "9f00a853288db4e7cf5026491d0fcab1c0db1dc9", "nq_1m.parquet",
                39856249, "46f2a9a6ee921dcb8b5895120f8069e5fa3197db94180cbe2df8bba725390662",
                "NQ 1m 23h 2020-08-31..2025-11-21, ET+UTC columns, front month unadjusted"),
    "nq_5m": (RAW, "prashanthaitha24/nq-strategy-b-bot",
                "bc199e73d733ab41fdc9b4dbaf27a915c93a6b7e", "data/nq_databento_5min.csv",
                15144646, "748add4222ef6d663aed0884d0c77a889bd3cf0cf17af636badc83428bfc9abd",
                "NQ 5m 23h 2023-01-02..2026-05-07, Databento NQ.c.0, UTC"),
    "es_1m_2026": (RAW, "axb0306/cme-futures-ohlc",
                "60abd3fb6369c6ce0b6a4a65b0f2562fc96b1264", "ES/ES_1min_20260120_20260415.csv",
                4540566, "e24e9a02d5e69e075b48965eb83e14f0a49c5355c298362a468af067f160ccfb",
                "ES 1m 23h 2026-01-20..2026-04-15, TopstepX API, UTC"),
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


def fetch(name: str) -> Path:
    tmpl, repo, commit, path, size, digest, _ = SOURCES[name]
    out = cache_dir() / f"{name}{Path(path).suffix}"
    if out.exists() and sha256(out) == digest:
        return out
    urllib.request.urlretrieve(tmpl.format(repo=repo, sha=commit, path=path), out)
    got = sha256(out)
    if got != digest or out.stat().st_size != size:
        raise SystemExit(f"{name}: sha256/size mismatch ({got}, {out.stat().st_size})")
    return out


if __name__ == "__main__":
    for n in (sys.argv[1:] or SOURCES):
        print(n, fetch(n), SOURCES[n][-1])
