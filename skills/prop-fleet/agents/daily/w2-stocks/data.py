#!/usr/bin/env python3
"""E1 data: build daily panels from the cached raw downloads (see fetch.py).

panels() returns a dict of wide DataFrames indexed by NYSE trading day (the SPY
calendar), columns = ticker:
  O, H, L, C   split-adjusted raw prices (Yahoo 'quote')
  AC           adjusted close (splits + dividends)
  V            share volume
  member       bool, point-in-time S&P 500 member that day (fja05680)
  covered      bool, Yahoo history is trusted for that member interval
plus 'mkt' (SPY total return close-to-close) and 'spx_on'/'spx_id'.
Total, overnight and intraday returns follow agents/prereg/E1_rules.md section 2.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from fetch import CACHE, RAW, YDIR, EDIR

PANEL = CACHE / "panel.pkl"


def load_yahoo(t: str) -> pd.DataFrame | None:
    p = YDIR / (t.replace("^", "_") + ".json")
    if not p.exists():
        return None
    j = json.loads(p.read_text())
    if not j:
        return None
    try:
        r = j["chart"]["result"][0]
        ts = r["timestamp"]
        q = r["indicators"]["quote"][0]
        ac = r["indicators"]["adjclose"][0]["adjclose"]
    except (KeyError, TypeError, IndexError):
        return None
    off = r["meta"].get("gmtoffset", 0)
    idx = pd.to_datetime(np.array(ts) + off, unit="s").normalize()
    df = pd.DataFrame(dict(O=q["open"], H=q["high"], L=q["low"], C=q["close"],
                           V=q["volume"], AC=ac), index=idx, dtype=float)
    df = df[~df.index.duplicated(keep="last")]
    return df


def membership() -> pd.DataFrame:
    rows = []
    with open(RAW / "sp500_hist.csv") as f:
        for row in csv.DictReader(f):
            rows.append((pd.Timestamp(row["date"]),
                         [t.strip() for t in row["tickers"].split(",") if t.strip()]))
    return rows


def build() -> dict:
    spy = load_yahoo("SPY")
    cal = spy.index[(spy.index >= "1999-01-04")]
    rows = membership()
    tick = sorted({t for _, ts in rows for t in ts})
    # point-in-time member matrix: row on date d holds from d until the next row
    mem = pd.DataFrame(False, index=cal, columns=tick)
    dates = [d for d, _ in rows] + [pd.Timestamp("2100-01-01")]
    for i, (d, ts) in enumerate(rows):
        m = (cal >= d) & (cal < dates[i + 1])
        if m.any():
            mem.loc[m, ts] = True
    fields = {k: {} for k in ("O", "H", "L", "C", "V", "AC")}
    first = {}
    for t in tick:
        df = load_yahoo(t)
        if df is None or df["C"].notna().sum() < 30:
            continue
        df = df.reindex(cal)
        first[t] = df["C"].first_valid_index()
        for k in fields:
            fields[k][t] = df[k]
    P = {k: pd.DataFrame(v).reindex(columns=tick) for k, v in fields.items()}
    # coverage rule (E1_rules.md section 1): a member interval is trusted only if
    # Yahoo history exists from (at most 5 trading days after) the interval start,
    # or the interval started before Yahoo's window (1999-01-04).
    cov = pd.DataFrame(False, index=cal, columns=tick)
    memv = mem.values
    pos = {d: i for i, d in enumerate(cal)}
    for j, t in enumerate(tick):
        if t not in first or first[t] is None:
            continue
        fi = pos[first[t]]
        col = memv[:, j]
        starts = np.flatnonzero(col & ~np.r_[False, col[:-1]])
        ends = np.flatnonzero(col & ~np.r_[col[1:], False])
        for s, e in zip(starts, ends):
            if s == 0 or fi <= s + 5:
                cov.iloc[max(s, fi):e + 1, j] = True
    P["member"] = mem
    P["covered"] = cov & P["C"].notna()
    for k in ("SPY", "^GSPC", "QQQ", "RSP"):
        df = load_yahoo(k)
        P["x_" + k] = None if df is None else df.reindex(cal)
    P["cal"] = cal
    return P


def panels(rebuild=False) -> dict:
    if PANEL.exists() and not rebuild:
        return pd.read_pickle(PANEL)
    P = build()
    pd.to_pickle(P, PANEL)
    return P


def coverage_report(P) -> pd.DataFrame:
    mem, cov = P["member"], P["covered"]
    y = mem.index.year
    out = pd.DataFrame({
        "members_per_day": mem.sum(1).groupby(y).mean(),
        "covered_per_day": cov.sum(1).groupby(y).mean(),
    })
    out["share"] = out["covered_per_day"] / out["members_per_day"]
    return out.round(3)


if __name__ == "__main__":
    P = panels(rebuild=True)
    print(coverage_report(P).to_string())
