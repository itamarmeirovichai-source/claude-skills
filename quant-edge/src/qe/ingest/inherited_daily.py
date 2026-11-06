#!/usr/bin/env python3
"""Inherited daily files (PR #4 worktree, commit e0f5e59) -> three parquet datasets.

Source: ~/quant-edge-inherited/pr4/skills/prop-fleet/data/ (provenance, clock and licence in its README.md):
  futures.csv            55 futures, daily EXCESS returns, 1984-01-03..2016-10-31 (rkohli3/TSMOM, MOP 2012 replication)
  asset_classes.csv      9 asset-class total-return levels 1970-01-02..2026-09-25 + asset_classes_observed.csv 0/1 flags
  spx_open_close.csv     ^GSPC open/close 1990-01-02..2026-09-25 (opens before 2010 are stale 64–77% of days)

Datasets: daily_futures_1984_2016 (wide, ts + 55 return columns), daily_assets_1970_2026 (wide, 9 levels + obs_* flags),
spx_oc_1990_2026 (ts, open, close). ts = trading date at 00:00 UTC (daily convention, qe.engine.bars.tag_daily).

Usage: python3 -m qe.ingest.inherited_daily [--dry-run] [--src DIR]
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

from qe.ingest import common

DEFAULT_SRC = Path(os.path.expanduser("~/quant-edge-inherited/pr4/skills/prop-fleet/data"))
PROVENANCE = "inherited PR#4 worktree commit e0f5e59 (prop-fleet/data/README.md)"


def load_futures(src: Path) -> pd.DataFrame:
    df = pd.read_csv(src / "futures.csv", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"Date": "ts"})
    df["ts"] = pd.to_datetime(df["ts"], format="%m/%d/%y", utc=True)
    sym = [c for c in df.columns if c != "ts"]
    df[sym] = df[sym].apply(pd.to_numeric, errors="coerce")
    df = df.dropna(subset=sym, how="all")
    return df.reset_index(drop=True)


def load_assets(src: Path) -> pd.DataFrame:
    lv = pd.read_csv(src / "asset_classes.csv")
    ob = pd.read_csv(src / "asset_classes_observed.csv")
    lv = lv.rename(columns={"Date": "ts"})
    ob = ob.rename(columns={"Date": "ts"})
    lv["ts"] = pd.to_datetime(lv["ts"], utc=True)
    ob["ts"] = pd.to_datetime(ob["ts"], utc=True)
    ob = ob.rename(columns={c: f"obs_{c}" for c in ob.columns if c != "ts"})
    df = lv.merge(ob, on="ts", how="left")
    for c in df.columns:
        if c.startswith("obs_"):
            df[c] = df[c].fillna(0).astype("int8")
    return df


def load_spx_oc(src: Path) -> pd.DataFrame:
    df = pd.read_csv(src / "spx_open_close.csv").rename(columns={"Date": "ts", "Open": "open", "Close": "close"})
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df


def run(src: Path = DEFAULT_SRC, dry_run: bool = False, manifest=None) -> dict:
    out = {}
    pins = {f: common.sha256_file(src / f) for f in ("futures.csv", "asset_classes.csv", "asset_classes_observed.csv", "spx_open_close.csv")}
    fut = load_futures(src)
    out["daily_futures_1984_2016"] = common.land(
        "daily_futures_1984_2016", fut, "derived/daily_futures_1984_2016.parquet", source="rkohli3/TSMOM via " + PROVENANCE,
        licence_status="free", resolution="1d", tz_note="trading date 00:00 UTC (US close-to-close excess returns)",
        notes=f"55 futures daily EXCESS returns (MOP 2012 universe); VF has no metadata; raw sha256 {pins['futures.csv'][:16]}; "
              f"ES vs SPY corr 0.98 (README); seven |r|>25% days listed by the inherited loader", dry_run=dry_run, manifest=manifest)
    ass = load_assets(src)
    out["daily_assets_1970_2026"] = common.land(
        "daily_assets_1970_2026", ass, "derived/daily_assets_1970_2026.parquet", source="mwilczynska/financial_datasets via " + PROVENANCE,
        licence_status="free", resolution="1d", tz_note="trading date 00:00 UTC",
        notes=f"9 total-return levels + obs_* flags (1=observed fund/index; 0=modelled, never evidence); observed 5-asset set from 1991-10-29; "
              f"raw sha256 {pins['asset_classes.csv'][:16]} / {pins['asset_classes_observed.csv'][:16]}; source licence MIT code, series terms unstated",
        dry_run=dry_run, manifest=manifest)
    spx = load_spx_oc(src)
    out["spx_oc_1990_2026"] = common.land(
        "spx_oc_1990_2026", spx, "derived/spx_oc_1990_2026.parquet", source="^GSPC via mwilczynska/financial_datasets via " + PROVENANCE,
        licence_status="free", resolution="1d", tz_note="trading date 00:00 UTC (NY 09:30 open / 16:00 close)",
        notes=f"index open == previous close on 77%/64% of days in the 1990s/2000s: opens usable from 2010-01-01 only; raw sha256 {pins['spx_open_close.csv'][:16]}",
        dry_run=dry_run, manifest=manifest)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    a = ap.parse_args(argv)
    run(a.src, dry_run=a.dry_run)


if __name__ == "__main__":
    main()
