#!/usr/bin/env python3
"""HistData.com FX 1-minute bars -> histdata_fx_1m_<PAIR> (partitioned parquet, one directory per pair).

Source: https://www.histdata.com/download-free-forex-data/?/ascii/1-minute-bar-quotes/<pair>/<year> (free for personal
use; the page's hidden form fields are POSTed to /get.php, one request at a time, Referer = the page). Raw zips are kept
under DATA_ROOT/raw/histdata/<PAIR>/ with sha256 pins in the fetch log; a zip already on disk is never re-downloaded.

Raw format: `YYYYMMDD HHMMSS;open;high;low;close;volume` with volume always 0 (bid quotes, no volume).
Clock: HistData's FAQ says "EST without daylight-saving adjustments"; the inherited team measured New York time WITH
DST on SPXUSD (briefs/inherited-method-lessons.md). This loader does not trust either statement: it runs the outcome-free
winter-vs-summer diagnostic (`qe.qa.clock.diagnose`: the minute of day with the largest mean |return| in Jan–Feb vs
Jun–Jul; the 08:30 ET US-release spike moves by 60 minutes under a fixed-EST clock and stays put under a NY-with-DST
clock) and converts with the verdict, which is recorded in the manifest notes. `--clock` overrides.

ts = bar OPEN time in UTC. Weekend rows (Fri 17:00 ET .. Sun 17:00 ET) are kept as delivered.

Usage: python3 -m qe.ingest.histdata [--pairs EURUSD,GBPUSD,USDJPY,AUDUSD] [--years 2010-2024] [--dry-run] [--clock auto|ny_dst|est_fixed]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

from qe.ingest import common

PAIRS = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD")
PAGE = "https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{pair_l}/{year}"
POST = "https://www.histdata.com/get.php"
_TK = re.compile(r'name="tk"\s+id="tk"\s+value="([0-9a-f]+)"')


def raw_zip_path(pair: str, year: int) -> Path:
    return common.RAW / "histdata" / pair / f"HISTDATA_COM_ASCII_{pair}_M1_{year}.zip"


def download_year(pair: str, year: int, *, dry_run: bool = False) -> dict:
    dest = raw_zip_path(pair, year)
    if dest.exists() and dest.stat().st_size > 0:
        return {"path": dest, "sha256": common.sha256_file(dest), "status": "cached"}
    page_url = PAGE.format(pair_l=pair.lower(), year=year)
    if dry_run:
        print(f"[dry-run] would GET {page_url} then POST {POST} -> {dest}")
        return {"path": dest, "sha256": "", "status": "dry-run"}
    html = common.fetch_text(page_url)
    m = _TK.search(html)
    if not m:
        raise common.Blocked(f"{page_url}: no download token on the page (layout changed or file missing for {pair} {year})")
    form = {"tk": m.group(1), "date": str(year), "datemonth": str(year), "platform": "ASCII", "timeframe": "M1", "fxpair": pair}
    r = common.fetch(POST, dest, post=form, headers={"Referer": page_url, "Origin": "https://www.histdata.com"})
    with open(dest, "rb") as f:
        magic = f.read(2)
    if magic != b"PK":
        dest.unlink()
        raise common.Blocked(f"{pair} {year}: response was not a zip (token rejected?)")
    return r


def parse_zip(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise ValueError(f"{path}: no csv inside")
        raw = z.read(names[0])
    df = pd.read_csv(io.BytesIO(raw), sep=";", header=None, names=["local", "open", "high", "low", "close", "volume"],
                     dtype={"local": str})
    df["local"] = pd.to_datetime(df["local"], format="%Y%m%d %H%M%S")
    return df


def to_utc(df: pd.DataFrame, clock: str) -> pd.DataFrame:
    """clock: 'ny_dst' (America/New_York wall clock) or 'est_fixed' (UTC-5 all year)."""
    out = df.copy()
    if clock == "ny_dst":
        out["ts"] = out["local"].dt.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
        out = out.dropna(subset=["ts"])
    elif clock == "est_fixed":
        out["ts"] = out["local"].dt.tz_localize("Etc/GMT+5").dt.tz_convert("UTC")
    else:
        raise ValueError(clock)
    out = out.drop(columns=["local"])[["ts", "open", "high", "low", "close", "volume"]]
    out = out.drop_duplicates(subset=["ts"], keep="first")
    return out


def run(pairs=PAIRS, years=range(2010, 2025), *, dry_run: bool = False, clock: str = "auto", manifest=None) -> dict:
    from qe.qa import clock as qclock
    out = {}
    for pair in pairs:
        frames = []
        pins = []
        for y in years:
            try:
                r = download_year(pair, y, dry_run=dry_run)
            except common.RateLimited as e:
                print(f"STOP (429): {e}", file=sys.stderr)
                break
            except common.Blocked as e:
                print(f"blocked/missing: {e}", file=sys.stderr)
                continue
            if dry_run or not Path(r["path"]).exists():
                continue
            pins.append(f"{y}:{r['sha256'][:8]}")
            frames.append(parse_zip(Path(r["path"])))
        if not frames:
            continue
        raw = pd.concat(frames, ignore_index=True)
        verdict = clock
        diag = {}
        if clock == "auto":
            diag = qclock.diagnose_local(raw["local"], raw["close"])
            verdict = diag["verdict"] if diag["verdict"] in ("ny_dst", "est_fixed") else "ny_dst"
        df = to_utc(raw, verdict)
        note = (f"HistData personal use; fetched {common.today()}; raw zips {len(pins)} pinned in fetch_log; clock={verdict}"
                + (f" (diag winter peak {diag.get('winter_peak')} summer peak {diag.get('summer_peak')} NY-minute, shift {diag.get('shift_minutes')} min)" if diag else " (forced)")
                + "; bid quotes, volume=0; weekend rows kept")
        out[pair] = common.land(f"histdata_fx_1m_{pair}", df, f"derived/histdata_fx_1m/{pair}", fmt="partitioned", source=PAGE.format(pair_l=pair.lower(), year="YYYY"),
                                licence_status="free", resolution="1m", tz_note="bar open UTC (converted from HistData local clock, see notes)",
                                notes=note, dry_run=dry_run, manifest=manifest)
    return out


def _years(s: str):
    a, b = s.split("-") if "-" in s else (s, s)
    return range(int(a), int(b) + 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pairs", default=",".join(PAIRS))
    ap.add_argument("--years", default="2010-2024")
    ap.add_argument("--clock", default="auto", choices=("auto", "ny_dst", "est_fixed"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run(tuple(p.strip().upper() for p in a.pairs.split(",") if p.strip()), _years(a.years), dry_run=a.dry_run, clock=a.clock)


if __name__ == "__main__":
    main()
