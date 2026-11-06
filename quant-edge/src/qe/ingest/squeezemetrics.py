#!/usr/bin/env python3
"""SqueezeMetrics DIX / GEX daily -> squeeze_dix_gex_daily (ts, price, dix, gex).

Source: https://squeezemetrics.com/monitor/static/DIX.csv (public CSV, 2011-05-02 onward). Published after the close
(≈ 17:52 ET per the inherited publication-time check, briefs/inherited-data-in-hand.md): a value dated d is usable from
the NEXT trading day only (look-ahead rule). ts = date 00:00 UTC.

Usage: python3 -m qe.ingest.squeezemetrics [--dry-run]
"""
from __future__ import annotations

import argparse

import pandas as pd

from qe.ingest import common

URL = "https://squeezemetrics.com/monitor/static/DIX.csv"


def parse(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"date": "ts"})
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df


def run(dry_run: bool = False, manifest=None, raw_dir=None) -> dict:
    raw = (raw_dir or common.RAW / "squeezemetrics") / "DIX.csv"
    f = common.fetch(URL, raw, dry_run=dry_run, overwrite=True)
    if dry_run and not raw.exists():
        return {}
    df = parse(raw)
    return common.land("squeeze_dix_gex_daily", df, "derived/squeeze_dix_gex_daily.parquet", source=URL, licence_status="free",
                       resolution="1d", tz_note="US trading date 00:00 UTC; published ≈17:52 ET -> usable next day", dry_run=dry_run,
                       manifest=manifest, notes=f"fetched {common.today()}; raw sha256 {f['sha256'][:16]}; public CSV, terms unstated")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run(dry_run=a.dry_run)


if __name__ == "__main__":
    main()
