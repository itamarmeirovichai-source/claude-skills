#!/usr/bin/env python3
"""E1 data fetch (wave 2): point-in-time S&P 500 membership (fja05680/sp500 on GitHub)
and Yahoo daily OHLC + adjusted close for every ticker that was ever a member since
1996, plus index/ETF hedges. Raw downloads are cached in $E1_CACHE (the session
scratchpad), never committed.

Usage: python3 fetch.py members|yahoo|earnings
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

CACHE = Path(os.environ.get(
    "E1_CACHE",
    "/tmp/claude-0/-home-user-claude-skills/80a7d2bf-12e0-5535-a15b-046f4782cd0b/"
    "scratchpad/data"))
RAW = CACHE / "raw"
YDIR = CACHE / "yahoo"
EDIR = CACHE / "earnings"
UA = {"User-Agent": "Mozilla/5.0"}
MEMBERS_URL = ("https://raw.githubusercontent.com/fja05680/sp500/master/"
               "S%26P%20500%20Historical%20Components%20%26%20Changes%20(Updated).csv")
EXTRA = ["SPY", "^GSPC", "QQQ", "^NDX", "RSP"]
P1, P2 = 915148800, 1791000000          # 1999-01-01 .. far future


def get(url: str, tries=4, timeout=30) -> bytes | None:
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                return None
            time.sleep(2 ** (k + 1))
        except Exception:
            time.sleep(2 ** (k + 1))
    return None


def members():
    RAW.mkdir(parents=True, exist_ok=True)
    b = get(MEMBERS_URL)
    (RAW / "sp500_hist.csv").write_bytes(b)
    print("members bytes", len(b))


def all_tickers() -> list[str]:
    import csv
    s = set()
    with open(RAW / "sp500_hist.csv") as f:
        for row in csv.DictReader(f):
            s.update(t.strip() for t in row["tickers"].split(",") if t.strip())
    return sorted(s) + EXTRA


def yahoo_one(t: str) -> tuple[str, str]:
    out = YDIR / (t.replace("^", "_") + ".json")
    if out.exists():
        return t, "cached"
    ys = t.replace(".", "-")
    url = (f"https://query2.finance.yahoo.com/v8/finance/chart/{ys}?period1={P1}"
           f"&period2={P2}&interval=1d&events=div,split&includeAdjustedClose=true")
    b = get(url)
    if b is None:
        out.write_text("null")
        return t, "missing"
    out.write_bytes(b)
    return t, "ok"


def yahoo():
    YDIR.mkdir(parents=True, exist_ok=True)
    tick = all_tickers()
    stat = {}
    with cf.ThreadPoolExecutor(6) as ex:
        for i, (t, s) in enumerate(ex.map(yahoo_one, tick)):
            stat[s] = stat.get(s, 0) + 1
            if i % 100 == 0:
                print(i, t, s, stat, flush=True)
    print("done", len(tick), stat)


def earnings_one(d: str) -> tuple[str, str]:
    # curl: urllib stalls on this host without browser-like headers
    import subprocess
    out = EDIR / f"{d}.json"
    if out.exists() and out.stat().st_size > 50:
        return d, "cached"
    url = f"https://api.nasdaq.com/api/calendar/earnings?date={d}"
    for k in range(4):
        r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", "Mozilla/5.0",
                            "-H", "Accept: application/json", "-o", str(out), url])
        if r.returncode == 0 and out.exists() and out.stat().st_size > 50:
            return d, "ok"
        time.sleep(2 ** (k + 1))
    return d, "missing"


def earnings(start="2008-01-01", end="2026-10-09"):
    import pandas as pd
    EDIR.mkdir(parents=True, exist_ok=True)
    days = [d.strftime("%Y-%m-%d") for d in pd.bdate_range(start, end)]
    stat = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for i, (d, s) in enumerate(ex.map(earnings_one, days)):
            stat[s] = stat.get(s, 0) + 1
            if i % 250 == 0:
                print(i, d, s, stat, flush=True)
    print("done", len(days), stat)


if __name__ == "__main__":
    {"members": members, "yahoo": yahoo, "earnings": earnings}[sys.argv[1]]()
