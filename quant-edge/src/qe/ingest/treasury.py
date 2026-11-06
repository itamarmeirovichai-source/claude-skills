#!/usr/bin/env python3
"""US Treasury auction schedule 2010– -> calendars/cal_treasury_auctions.csv (dataset cal_treasury_auctions).

Source: Fiscal Data API (US Treasury, public domain)
  https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query
Fields kept: auction_date, announcemt_date, issue_date, maturity_date, security_type, security_term, cusip,
closing_time_comp, closing_time_noncomp, offering_amt, auction_format, cash_management_bill_cmb, reopening,
bid_to_cover_ratio (known only AFTER the auction: never an input before ts_result).
Clock: competitive bids close at closing_time_comp Eastern (13:00 ET coupons, 11:30 ET bills); results are released a
few minutes later. ts = auction date + closing_time_comp (America/New_York) in UTC; ts_announce = announcement date
00:00 UTC (the offering amount is public from the announcement, usually 11:00 ET on the announcement day).

Usage: python3 -m qe.ingest.treasury [--start 2010-01-01] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from qe.ingest import common

API = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query"
FIELDS = ["record_date", "cusip", "security_type", "security_term", "auction_date", "announcemt_date", "issue_date", "maturity_date",
          "closing_time_comp", "closing_time_noncomp", "offering_amt", "auction_format", "cash_management_bill_cmb", "reopening",
          "bid_to_cover_ratio", "high_yield", "high_discnt_rate", "total_accepted", "total_tendered"]
PAGE_SIZE = 10000


def fetch_all(start: str, *, dry_run: bool = False) -> pd.DataFrame:
    frames = []
    page = 1
    while True:
        url = (f"{API}?fields={','.join(FIELDS)}&filter=auction_date:gte:{start}&sort=auction_date,cusip"
               f"&page%5Bsize%5D={PAGE_SIZE}&page%5Bnumber%5D={page}")
        dest = common.RAW / "treasury" / f"auctions_query_{start}_p{page}.json"
        r = common.fetch(url, dest, dry_run=dry_run, overwrite=True)
        if dry_run:
            return pd.DataFrame()
        d = json.loads(dest.read_text())
        rows = d.get("data", [])
        if not rows:
            break
        frames.append(pd.DataFrame(rows))
        meta = d.get("meta", {})
        if page >= int(meta.get("total-pages", page)):
            break
        page += 1
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace({"null": None})
    close = df["closing_time_comp"].fillna("01:00 PM")
    local = pd.to_datetime(df["auction_date"] + " " + close, format="%Y-%m-%d %I:%M %p", errors="coerce")
    df["ts"] = local.dt.tz_localize("America/New_York", ambiguous=True, nonexistent="shift_forward").dt.tz_convert("UTC")
    df["ts_announce"] = pd.to_datetime(df["announcemt_date"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts"])
    cols = ["ts", "ts_announce"] + [c for c in df.columns if c not in ("ts", "ts_announce")]
    return df[cols]


def run(start: str = "2010-01-01", *, dry_run: bool = False, manifest=None) -> dict:
    try:
        raw = fetch_all(start, dry_run=dry_run)
    except common.RateLimited as e:
        print(f"STOP (429): {e}", file=sys.stderr)
        return {}
    if dry_run or raw.empty:
        return {}
    df = tidy(raw)
    return common.land("cal_treasury_auctions", df, "calendars/cal_treasury_auctions.csv", fmt="csv", source=API, licence_status="free",
                       resolution="event", tz_note="ts = auction date + competitive close (ET) in UTC; ts_announce = announcement date 00:00 UTC",
                       notes=f"US Treasury Fiscal Data, public domain; fetched {common.today()}; bid_to_cover/high_yield known only after ts",
                       dry_run=dry_run, manifest=manifest)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default="2010-01-01")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run(a.start, dry_run=a.dry_run)


if __name__ == "__main__":
    main()
