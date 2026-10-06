"""H0021 loaders. Same sha256 pins, session window and roll_excluded as orb-H0020/loaders.py,
but these KEEP the volume column (VWAP needs it). Data come from $CLAUDE_SCRATCH
(fetched by daily/2026-10-04/data_fetch.py; never committed)."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

import numpy as np
import pandas as pd

SCR = Path(os.environ["CLAUDE_SCRATCH"])

SHA = {  # identical to orb-H0020/loaders.py and data_fetch.py pins
    "intraday/spy_rth.csv": "d4671c48d18bdaab21f4b44e02992d2fc91070b01a357189f67b2305a75f9ee6",
    "intraday/nq_1m.parquet": "46f2a9a6ee921dcb8b5895120f8069e5fa3197db94180cbe2df8bba725390662",
}


def _check(rel: str) -> Path:
    p = SCR / rel
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != SHA[rel]:
        raise SystemExit(f"sha256 mismatch {rel}: {h}")
    return p


# ── loaders: o,h,l,c,v indexed by naive NY bar-open time ─────────────────────
def load_spy() -> pd.DataFrame:
    d = pd.read_csv(_check("intraday/spy_rth.csv"), parse_dates=["caldt"])
    d = d.rename(columns={"caldt": "dt", "open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c", "v"]].astype(float)


def load_nq() -> pd.DataFrame:
    d = pd.read_parquet(_check("intraday/nq_1m.parquet"))
    d = d.rename(columns={"DateTime_ET": "dt", "Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c", "v"]].astype(float)


def roll_excluded(dates) -> set:
    """Copied from orb-H0020/loaders.py (from gapfade-H0012): Mon-Fri of the week holding
    the 3rd Friday of Mar/Jun/Sep/Dec, plus the next Monday."""
    out = set()
    years = sorted({d.year for d in dates})
    for y in years:
        for m in (3, 6, 9, 12):
            first = pd.Timestamp(y, m, 1)
            fri3 = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
            mon = fri3 - pd.Timedelta(days=4)
            for i in range(5):
                out.add((mon + pd.Timedelta(days=i)).date())
            out.add((fri3 + pd.Timedelta(days=3)).date())
    return out


def rth(m: pd.DataFrame) -> pd.DataFrame:
    """RTH bars 09:30..15:59 NY on weekdays (same window as orb-H0020 sessions()), as one
    flat frame sorted by time with a `date` and `hm` column. A session = a date in here."""
    t = m.index
    hm = t.hour * 100 + t.minute
    r = m[(hm >= 930) & (hm <= 1559) & (t.dayofweek < 5)].copy()
    r["date"] = r.index.date
    r["hm"] = r.index.hour * 100 + r.index.minute
    return r
