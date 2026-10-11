#!/usr/bin/env python3
"""D4 (w1-breadth) data fetch: free 1-minute bars for many markets.

Source: github.com/FutureSharks/financial-data pinned at commit 7ba1d404 (reachable via
raw.githubusercontent.com from this container).
  * oanda/<INSTR>/<year>/oanda-<INSTR>-<year>-<month>.csv  — Oanda v20 M1 MID candles,
    columns time,close,high,low,open,volume (volume = tick count). 2005-01..2019-12.
    The clock is checked (not assumed) in data_check.py.
  * stocks/histdata/<SYM>/DAT_ASCII_<SYM>_M1_<year>.csv — HistData M1, ';' separated,
    'YYYYMMDD HHMMSS;o;h;l;c;v'. 2010..2018. HistData documents fixed EST (UTC-5, no DST),
    but clock_xcorr.py (2026-10-11, outcome-free) shows these files follow New York local
    time WITH daylight saving: against Oanda (UTC) the best shift is 0 in US-winter months
    and -60 min in every US-summer month. So they are localized to America/New_York.

Every downloaded file's sha256 is written to manifest.csv (committed, small). Data are
stored as one parquet per market in $CLAUDE_SCRATCH/w1-breadth/ (never committed), with a
UTC naive index.

    python3 fetch.py               # all markets
    python3 fetch.py EUR_USD GRXEUR
"""
from __future__ import annotations

import hashlib
import io
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

COMMIT = "7ba1d404aa8b0e1c0f71321acebadcbfb9bcca8d"
RAW = f"https://raw.githubusercontent.com/FutureSharks/financial-data/{COMMIT}/pyfinancialdata/data/"

OANDA = ["AU200_AUD", "AUD_JPY", "AUD_USD", "CORN_USD", "DE10YB_EUR", "EUR_JPY", "EUR_USD",
         "FR40_EUR", "GBP_USD", "JP225_USD", "NAS100_USD", "NATGAS_USD", "NL25_EUR",
         "SOYBN_USD", "SPX500_USD", "SUGAR_USD", "UK100_GBP", "UK10YB_GBP", "US2000_USD",
         "USB02Y_USD", "USB10Y_USD", "USD_CAD", "WHEAT_USD", "WTICO_USD", "XAU_USD"]
HISTDATA = ["GRXEUR", "ETXEUR", "SPXUSD", "JPXJPY"]

HERE = Path(__file__).resolve().parent


def out_dir() -> Path:
    p = Path(os.environ.get("CLAUDE_SCRATCH", "/tmp/prop-fleet-data")) / "w1-breadth"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _get(url: str) -> bytes | None:
    for _ in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:
            pass
    raise SystemExit(f"failed: {url}")


def fetch_oanda(sym: str):
    jobs = [(y, m) for y in range(2005, 2021) for m in range(1, 13)]
    urls = {(y, m): f"{RAW}currencies/oanda/{sym}/{y}/oanda-{sym}-{y}-{m}.csv" for y, m in jobs}
    with ThreadPoolExecutor(8) as ex:
        blobs = dict(zip(jobs, ex.map(_get, urls.values())))
    frames, man = [], []
    for k in jobs:
        b = blobs[k]
        if b is None:
            continue
        man.append((sym, urls[k].replace(RAW, ""), len(b), hashlib.sha256(b).hexdigest()))
        d = pd.read_csv(io.BytesIO(b))
        frames.append(d)
    d = pd.concat(frames)
    d["t"] = pd.to_datetime(d["time"])
    d = d.set_index("t").sort_index()
    d = d[~d.index.duplicated()]
    d = d.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    return d[["o", "h", "l", "c", "v"]].astype("float64"), man


def fetch_histdata(sym: str):
    frames, man = [], []
    for y in range(2010, 2019):
        u = f"{RAW}stocks/histdata/{sym}/DAT_ASCII_{sym}_M1_{y}.csv"
        b = _get(u)
        if b is None:
            continue
        man.append((sym, u.replace(RAW, ""), len(b), hashlib.sha256(b).hexdigest()))
        frames.append(pd.read_csv(io.BytesIO(b), sep=";", header=None,
                                  names=["dt", "o", "h", "l", "c", "v"]))
    d = pd.concat(frames)
    # HistData clock = New York local time with DST (clock_xcorr.py) -> UTC
    loc = pd.DatetimeIndex(pd.to_datetime(d["dt"], format="%Y%m%d %H%M%S"))
    d["t"] = loc.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT").tz_convert("UTC").tz_localize(None)
    d = d.dropna(subset=["t"])
    d = d.set_index("t").sort_index()
    d = d[~d.index.duplicated()]
    return d[["o", "h", "l", "c", "v"]].astype("float64"), man


def main(names):
    od = out_dir()
    mf = HERE / "manifest.csv"
    rows = pd.read_csv(mf).values.tolist() if mf.exists() else []
    for s in names:
        d, man = (fetch_histdata if s in HISTDATA else fetch_oanda)(s)
        d.to_parquet(od / f"{s}.parquet")
        rows = [r for r in rows if r[0] != s] + man
        print(f"{s}: {len(d):,} bars {d.index[0]} .. {d.index[-1]} files {len(man)}", flush=True)
    pd.DataFrame(rows, columns=["market", "path", "bytes", "sha256"]).sort_values(
        ["market", "path"]).to_csv(mf, index=False)


if __name__ == "__main__":
    main(sys.argv[1:] or OANDA + HISTDATA)
