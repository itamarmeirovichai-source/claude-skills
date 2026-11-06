#!/usr/bin/env python3
"""CFTC Commitments of Traders history -> cftc_cot_fin_weekly (Traders in Financial Futures) and cftc_cot_disagg_weekly
(Disaggregated, physical commodities), futures-only, one row per market per report week.

Source: https://www.cftc.gov/files/dea/history/fut_fin_txt_<YYYY>.zip and fut_disagg_txt_<YYYY>.zip (public domain,
US government work; a browser User-Agent is required, D-007). Raw zips kept under DATA_ROOT/raw/cftc/.

Clock: the report is "as of" Tuesday's close and RELEASED Friday 15:30 ET (Monday when Friday is a holiday; the exact
shifted days are not in the files). Columns: ts = report (as-of) date 00:00 UTC; released_ts = the nominal Friday 15:30 ET
in UTC (3 days after the as-of date) — anything that uses COT before released_ts looks ahead; holiday shifts make the
nominal time EARLY by up to 3 days on a few weeks a year, so a user should lag one extra day or check the CFTC release
schedule for the year.

Usage: python3 -m qe.ingest.cftc [--years 2010-2026] [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile

import pandas as pd

from qe.ingest import common

URL = "https://www.cftc.gov/files/dea/history/{kind}_txt_{year}.zip"
KINDS = {"fin": "fut_fin", "disagg": "fut_disagg"}


def parse_zip(path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".txt")]
        raw = z.read(names[0])
    df = pd.read_csv(io.BytesIO(raw), low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    # the CFTC files pad numbers with spaces and mix '.' for missing: strip, then coerce columns that are numeric throughout
    for c in df.columns:
        if df[c].dtype == object:
            s = df[c].astype(str).str.strip()
            num = pd.to_numeric(s.replace({"": None, ".": None, "nan": None}), errors="coerce")
            nonblank = s.ne("") & s.ne(".") & s.ne("nan")
            if nonblank.any() and num[nonblank].notna().all():
                df[c] = num
            else:
                df[c] = s
    date_col = "Report_Date_as_YYYY-MM-DD" if "Report_Date_as_YYYY-MM-DD" in df.columns else "Report_Date_as_MM_DD_YYYY"
    df["ts"] = pd.to_datetime(df[date_col], utc=True)
    rel = (df["ts"].dt.tz_convert(None) + pd.Timedelta(days=3, hours=15, minutes=30)).dt.tz_localize("America/New_York", ambiguous=True)
    df["released_ts"] = rel.dt.tz_convert("UTC")
    cols = ["ts", "released_ts"] + [c for c in df.columns if c not in ("ts", "released_ts")]
    return df[cols]


def run(years=range(2010, 2027), *, dry_run: bool = False, manifest=None) -> dict:
    out = {}
    for kind, prefix in KINDS.items():
        frames, pins = [], []
        for y in years:
            url = URL.format(kind=prefix, year=y)
            dest = common.RAW / "cftc" / f"{prefix}_txt_{y}.zip"
            try:
                r = common.fetch(url, dest, dry_run=dry_run, overwrite=(y >= 2026))   # the current year grows weekly
            except common.RateLimited as e:
                print(f"STOP (429): {e}", file=sys.stderr)
                break
            except common.Blocked as e:
                print(f"blocked/missing: {e}", file=sys.stderr)
                continue
            if dry_run or not dest.exists():
                continue
            pins.append(f"{y}:{r['sha256'][:8]}")
            frames.append(parse_zip(dest))
        if not frames:
            continue
        df = pd.concat(frames, ignore_index=True)
        df = df.drop_duplicates()
        out[kind] = common.land(f"cftc_cot_{kind}_weekly", df, f"derived/cftc_cot_{kind}_weekly.parquet", source=URL.format(kind=prefix, year="YYYY"),
                                licence_status="free", resolution="1w", tz_note="ts = as-of Tuesday 00:00 UTC; released_ts = nominal Friday 15:30 ET in UTC",
                                notes=f"US government public domain; fetched {common.today()}; {len(pins)} yearly zips pinned in fetch_log; futures only; "
                                      f"holiday-shifted releases not encoded (lag one extra day)", dry_run=dry_run, manifest=manifest)
    return out


def _years(s: str):
    a, b = s.split("-") if "-" in s else (s, s)
    return range(int(a), int(b) + 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--years", default="2010-2026")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run(_years(a.years), dry_run=a.dry_run)


if __name__ == "__main__":
    main()
