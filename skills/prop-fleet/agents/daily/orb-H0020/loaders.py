"""Data loaders copied verbatim from gapfade-H0012/gapfade.py (same sha256 pins), because
that module asserts the ledger N it ran at (196) on import. Data come from $CLAUDE_SCRATCH."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

import numpy as np
import pandas as pd

SCR = Path(os.environ["CLAUDE_SCRATCH"])

SHA = {  # measured at fetch time (2026-10-06); D2/D3 also match data_fetch.py pins
    "spx/SPX_2010.csv": "1166316b0547be9610b3027f312894a582424917e7905d0ffca1bee194e8d10f",
    "spx/SPX_2011.csv": "5c93bd8779d19d127a79184a4edd70735ff79a03e9c2970794a0670cb90bc90c",
    "spx/SPX_2012.csv": "9fa9e760fab82b4fb53e4a88e8eaf2ea258f3ad578b21765b4d6376539624efb",
    "spx/SPX_2013.csv": "28b162825090927c5c9f47a6571a7b5d8a257dc40363cc9f7aa60a7919c82ff0",
    "spx/SPX_2014.csv": "f2fd077d58b2a9b5125456d8f7c8893b0ded3a3dd229792bf9afa231201daa72",
    "spx/SPX_2015.csv": "0f344ee1ecc0e34f707a340a482314159dc1f414950cc083deae8436b55b9493",
    "spx/SPX_2016.csv": "8be247ca5008d6a91c6287c52f1b9df133e4b5ebad29141e9de4686a79c327d2",
    "spx/SPX_2017.csv": "01236a4178eb7802cd32fb569b7bed13670813ffddb69c95f47eee48d6552e3e",
    "spx/SPX_2018.csv": "7f20d258d549893be83c4416a115861eae8d54ae530dcfd1c3a0dd6e5cc11a43",
    "intraday/spy_rth.csv": "d4671c48d18bdaab21f4b44e02992d2fc91070b01a357189f67b2305a75f9ee6",
    "intraday/nq_1m.parquet": "46f2a9a6ee921dcb8b5895120f8069e5fa3197db94180cbe2df8bba725390662",
}


def _check(rel: str) -> Path:
    p = SCR / rel
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != SHA[rel]:
        raise SystemExit(f"sha256 mismatch {rel}: {h}")
    return p


# ── loaders: all return o,h,l,c indexed by naive NY bar-open time ────────────
def load_d1() -> pd.DataFrame:
    fr = []
    for y in range(2010, 2019):
        f = _check(f"spx/SPX_{y}.csv")
        fr.append(pd.read_csv(f, sep=";", header=None, names=["dt", "o", "h", "l", "c", "v"]))
    d = pd.concat(fr)
    d["dt"] = pd.to_datetime(d["dt"], format="%Y%m%d %H%M%S")   # same as tjr_backtest.load_minutes
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def load_d2() -> pd.DataFrame:
    d = pd.read_csv(_check("intraday/spy_rth.csv"), parse_dates=["caldt"])
    d = d.rename(columns={"caldt": "dt", "open": "o", "high": "h", "low": "l", "close": "c"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def load_d3() -> pd.DataFrame:
    d = pd.read_parquet(_check("intraday/nq_1m.parquet"))
    d = d.rename(columns={"DateTime_ET": "dt", "Open": "o", "High": "h", "Low": "l", "Close": "c"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def roll_excluded(dates) -> set:
    """Mon-Fri of the week holding the 3rd Friday of Mar/Jun/Sep/Dec, plus the next Monday."""
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


# ── per-session table (ex-ante pieces only) ──────────────────────────────────
def sessions(m: pd.DataFrame) -> dict:
    t = m.index
    hm = t.hour * 100 + t.minute
    rth = m[(hm >= 930) & (hm <= 1559) & (t.dayofweek < 5)].copy()
    rth["date"] = rth.index.date
    rth["hm"] = rth.index.hour * 100 + rth.index.minute
    return {d: g for d, g in rth.groupby("date", sort=True)}


def _bar(g: pd.DataFrame, hm: int):
    r = g[g.hm == hm]
    return None if r.empty else r.iloc[0]
