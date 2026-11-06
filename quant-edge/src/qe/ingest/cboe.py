#!/usr/bin/env python3
"""CBOE VIX daily history -> cboe_vix_daily (ts, open, high, low, close).

Source: https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv (public CSV, 1990-01-02 onward; CBOE
terms: free for personal/non-commercial research use, no redistribution). Clock: Chicago trading date; ts = date 00:00 UTC.

Usage: python3 -m qe.ingest.cboe [--dry-run]
"""
from __future__ import annotations

import argparse

import pandas as pd

from qe.ingest import common

URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"


def parse(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"date": "ts"})
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df[["ts", "open", "high", "low", "close"]]


def run(dry_run: bool = False, manifest=None, raw_dir=None) -> dict:
    raw = (raw_dir or common.RAW / "cboe") / "VIX_History.csv"
    f = common.fetch(URL, raw, dry_run=dry_run, overwrite=True)
    if dry_run and not raw.exists():
        return {}
    df = parse(raw)
    return common.land("cboe_vix_daily", df, "derived/cboe_vix_daily.parquet", source=URL, licence_status="free", resolution="1d",
                       tz_note="Chicago trading date 00:00 UTC", dry_run=dry_run, manifest=manifest,
                       notes=f"fetched {common.today()}; raw sha256 {f['sha256'][:16]}; CBOE: personal research use; no redistribution")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run(dry_run=a.dry_run)


if __name__ == "__main__":
    main()
