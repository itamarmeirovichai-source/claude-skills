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

Batch 1b (2026-11-06) adds index/commodity CFDs (`histdata_cfd_1m_<SYM>`) and the hold-out split (D-004): HistData lists
every completed year as one zip and the current year month by month (`.../<pair>/<year>/<month>`, form field
datemonth=YYYYMM); `list_periods` reads the symbol's index page so a symbol HistData does not carry is reported, not
guessed. Every bar with ts >= paths.HOLDOUT_START (UTC) is written to DATA_ROOT/holdout/<prefix>/<SYM> as the separate
dataset `<prefix>_<SYM>_holdout`, and raw zips for years >= the hold-out year are kept under DATA_ROOT/holdout/raw/; the
derived IS/OOS dataset never holds a hold-out bar. The clock verdict combines the US-anchor diagnostic with a
home-market-open anchor (`qe.qa.clock.diagnose_anchor`) where one is defined (ANCHORS), then the US/EU DST-mismatch-week
release test (`qe.qa.clock.diagnose_mismatch_events`): HistData stamps follow the New York DST dates through 2018 and the
EUROPEAN DST dates from 2019 (clock 'histdata_rule'). NOTE: `run()` (the FX 2010-2024 path that landed histdata_fx_1m_*
on 2026-11-04) still converts with plain ny_dst, so those datasets are one hour early in the 2019-2024 mismatch weeks
(about 3 weeks a year); re-landing them changes their sha256 pins and is a Director decision.

Usage: python3 -m qe.ingest.histdata [--pairs EURUSD,GBPUSD,USDJPY,AUDUSD] [--years 2010-2024] [--dry-run] [--clock auto|ny_dst|est_fixed]
       python3 -m qe.ingest.histdata --symbols SPXUSD,GRXEUR [--start-year 2010] [--prefix histdata_cfd_1m] [--holdout-only]
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd

from qe import paths
from qe.ingest import common

PAIRS = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD")
CFD_SYMBOLS = ("HKXHKD", "ETXEUR", "GRXEUR", "SPXUSD", "NSXUSD", "JPXJPY", "XAUUSD", "BCOUSD", "UKXGBP", "FRXEUR", "WTIUSD")
# home-market open used as a second, non-US clock anchor: (zone, wall-clock minute of the open)
ANCHORS = {"HKXHKD": ("Asia/Hong_Kong", 9 * 60 + 15), "JPXJPY": ("Asia/Tokyo", 9 * 60), "ETXEUR": ("Europe/Berlin", 8 * 60),
           "GRXEUR": ("Europe/Berlin", 9 * 60), "FRXEUR": ("Europe/Paris", 8 * 60), "UKXGBP": ("Europe/London", 8 * 60)}
# Spans whose bars are another instrument's (Data QA 2026-11-06: a 1-minute level break of >25% that never reverts,
# levels matching a different index). Removed before landing; [start, end] inclusive, UTC bar-open times.
EXCLUDE = {
    "GRXEUR": [("2020-06-15 06:00", "2023-12-01 20:59", "GRXEUR file carries Euro Stoxx 50 levels (2,908-4,490) instead of DAX (12,000 -> 16,429 either side)")],
    "ETXEUR": [("2018-12-17 07:00", "2019-12-31 23:59", "ETXEUR file jumps from 3,072 to 8,880-9,222 (not Euro Stoxx 50; IBEX-like levels) until the data end 2019-02-01")],
}
INDEX = "https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{pair_l}"
PAGE = INDEX + "/{year}"
POST = "https://www.histdata.com/get.php"
HOLDOUT_YEAR = int(paths.HOLDOUT_START[:4])
_TK = re.compile(r'name="tk"\s+id="tk"\s+value="([0-9a-f]+)"')
_HIDDEN = re.compile(r'<input type="hidden" name="(\w+)" id="\w+" value="([^"]*)"')


class NotCarried(common.Blocked):
    """HistData's index page for the symbol lists no 1-minute files (the symbol is not carried)."""


def raw_zip_path(pair: str, year: int, month: Optional[int] = None) -> Path:
    base = (common.DATA_ROOT / "holdout" / "raw") if year >= HOLDOUT_YEAR else common.RAW
    tag = f"{year}" if month is None else f"{year}{month:02d}"
    return base / "histdata" / pair / f"HISTDATA_COM_ASCII_{pair}_M1_{tag}.zip"


def page_url(pair: str, year: int, month: Optional[int] = None) -> str:
    return PAGE.format(pair_l=pair.lower(), year=year) + ("" if month is None else f"/{month}")


def parse_periods(html: str, pair: str) -> list:
    """(year, month|None) for every 1-minute file linked from the symbol's index page, sorted."""
    pat = re.compile(r"1-minute-bar-quotes/" + re.escape(pair.lower()) + r"/(\d{4})(?:/(\d{1,2}))?\"")
    out = {(int(y), int(m) if m else None) for y, m in pat.findall(html)}
    return sorted(out, key=lambda t: (t[0], t[1] or 0))


def list_periods(pair: str) -> list:
    url = INDEX.format(pair_l=pair.lower())
    periods = parse_periods(common.fetch_text(url), pair)
    if not periods:
        raise NotCarried(f"{url}: no 1-minute files listed for {pair}")
    return periods


def parse_form(html: str) -> dict:
    form = {}
    for k, v in _HIDDEN.findall(html):
        form.setdefault(k, v)
    return form


def download_period(pair: str, year: int, month: Optional[int] = None, *, dry_run: bool = False) -> dict:
    dest = raw_zip_path(pair, year, month)
    if dest.exists() and dest.stat().st_size > 0:
        return {"path": dest, "sha256": common.sha256_file(dest), "status": "cached"}
    url = page_url(pair, year, month)
    if dry_run:
        print(f"[dry-run] would GET {url} then POST {POST} -> {dest}")
        return {"path": dest, "sha256": "", "status": "dry-run"}
    html = common.fetch_text(url)
    m = _TK.search(html)
    if not m:
        raise common.Blocked(f"{url}: no download token on the page (layout changed or file missing for {pair} {year} {month or ''})")
    form = {"tk": m.group(1), "date": str(year), "datemonth": str(year) if month is None else f"{year}{month:02d}",
            "platform": "ASCII", "timeframe": "M1", "fxpair": pair}
    form.update({k: v for k, v in parse_form(html).items() if k in form})
    r = common.fetch(POST, dest, post=form, headers={"Referer": url, "Origin": "https://www.histdata.com"})
    with open(dest, "rb") as f:
        magic = f.read(2)
    if magic != b"PK":
        dest.unlink()
        raise common.Blocked(f"{pair} {year} {month or ''}: response was not a zip (token rejected?)")
    return r


def download_year(pair: str, year: int, *, dry_run: bool = False) -> dict:
    return download_period(pair, year, None, dry_run=dry_run)


def inner_csv_sha256(path: Path) -> str:
    """sha256 of the CSV inside a HistData zip (comparable with inherited per-CSV pins)."""
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        return common.sha256_bytes(z.read(names[0])) if names else ""


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
    """clock: 'ny_dst' (America/New_York wall clock), 'est_fixed' (UTC-5 all year), 'eu_dst' (EST/EDT on the EU switch
    dates = Europe/Berlin wall clock - 6 h) or 'histdata_rule' (ny_dst for local years < qclock.HISTDATA_EU_RULE_FROM,
    eu_dst from that year: the measured HistData clock, see qe.qa.clock)."""
    from qe.qa import clock as qclock
    out = df.copy()
    if clock == "histdata_rule":
        late = out["local"] >= pd.Timestamp(f"{qclock.HISTDATA_EU_RULE_FROM}-01-01")
        ts = qclock.clock_to_utc(out["local"], "ny_dst")
        ts[late] = qclock.clock_to_utc(out.loc[late, "local"], "eu_dst")
        out["ts"] = ts
    elif clock in ("ny_dst", "est_fixed", "eu_dst"):
        out["ts"] = qclock.clock_to_utc(out["local"], clock)
    else:
        raise ValueError(clock)
    out = out.dropna(subset=["ts"])
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


def clock_verdict(sym: str, local: pd.Series, close: pd.Series) -> dict:
    """US-anchor diagnostic + home-market anchor (if any) -> {'verdict', 'status', 'us', 'anchor', 'text'}."""
    from qe.qa import clock as qclock
    us = qclock.diagnose_local(local, close)
    anc = qclock.diagnose_anchor(local, close, *ANCHORS[sym]) if sym in ANCHORS else None
    verdict, status = qclock.combine(us, anc)
    f = qclock.fmt_minute
    mm_text = ""
    if verdict == "ny_dst":
        # Jan-Feb vs Jun-Jul cannot separate the NY and EU DST rules; the mismatch-week release test can
        ev = us_release_events()
        if len(ev):
            mm = qclock.diagnose_mismatch_events(local, close, ev)
            rc = qclock.rule_check(mm)
            verdict = "histdata_rule"
            if rc["disagree"] > rc["agree"]:
                status = "conflict"
            mm_text = (f" | US/EU DST-mismatch weeks, 08:30 ET CPI/NFP spike vs rule (NY DST <{qclock.HISTDATA_EU_RULE_FROM}, EU DST from it): "
                       f"{rc['agree']} agree, {rc['disagree']} disagree{(' (years ' + ' '.join(map(str, rc['years_disagreeing'])) + ')') if rc['years_disagreeing'] else ''}, "
                       f"{rc['undecided']} undecided")
    text = (f"US anchor: winter peak {f(us['winter_peak'])} summer peak {f(us['summer_peak'])} clock; shift {us['shift_minutes']} min -> {us['verdict']}")
    if anc:
        pr = anc["predicted"]
        text += (f" | {anc['anchor']} open: winter {f(anc['winter_peak'])} summer {f(anc['summer_peak'])} clock; shift {anc['shift_minutes']} min"
                 f" (ny_dst predicts {pr['ny_dst']['summer'] - pr['ny_dst']['winter']:+d}; est_fixed {pr['est_fixed']['summer'] - pr['est_fixed']['winter']:+d}) -> {anc['verdict']}")
    text += mm_text + f" | verdict {verdict} ({status})"
    return {"verdict": verdict, "status": status, "us": us, "anchor": anc, "text": text}


def us_release_events() -> pd.Series:
    """08:30 ET CPI and NFP release instants (UTC) from the program calendars, for the mismatch-week clock test."""
    out = []
    for name in ("cal_bls_cpi", "cal_bls_nfp"):
        f = common.CALENDARS / f"{name}.csv"
        if f.exists():
            out.append(pd.read_csv(f, usecols=["ts"])["ts"])
    return pd.to_datetime(pd.concat(out), utc=True).sort_values().reset_index(drop=True) if out else pd.Series(dtype="datetime64[ns, UTC]")


def split_holdout(df: pd.DataFrame) -> tuple:
    cut = pd.Timestamp(paths.HOLDOUT_START, tz="UTC")
    return df[df["ts"] < cut].reset_index(drop=True), df[df["ts"] >= cut].reset_index(drop=True)


def ingest_symbol(sym: str, *, prefix: str = "histdata_cfd_1m", start_year: int = 2010, holdout_only: bool = False,
                  clock: str = "auto", dry_run: bool = False, manifest=None, log=print) -> dict:
    """Download every listed period of `sym` from start_year, convert to UTC with the diagnosed clock, land the IS/OOS
    part (< HOLDOUT_START) under derived/<prefix>/<sym> and the hold-out part under holdout/<prefix>/<sym>.
    Raises common.RateLimited (caller stops everything) and NotCarried. Returns a summary dict."""
    from qe.qa import histdata_qa
    periods = [p for p in list_periods(sym) if p[0] >= start_year and (not holdout_only or p[0] >= HOLDOUT_YEAR)]
    frames, pins, missing = [], [], []
    for (y, m) in periods:
        try:
            r = download_period(sym, y, m, dry_run=dry_run)
        except common.RateLimited:
            raise
        except common.Blocked as e:
            log(f"blocked/missing: {e}")
            missing.append(f"{y}{'' if m is None else f'-{m:02d}'}")
            continue
        if dry_run or not Path(r["path"]).exists():
            continue
        pins.append(f"{y}{'' if m is None else f'{m:02d}'}:{r['sha256'][:8]}")
        frames.append(parse_zip(Path(r["path"])))
    out = {"symbol": sym, "periods": periods, "missing_periods": missing, "pins": pins}
    if not frames:
        return out
    raw = pd.concat(frames, ignore_index=True).sort_values("local", kind="mergesort")
    n_dup_local = int(raw.duplicated(subset=["local"]).sum())
    raw = raw.drop_duplicates(subset=["local"], keep="first").reset_index(drop=True)
    ho_cut_local = pd.Timestamp(paths.HOLDOUT_START)
    # the verdict is taken on the pre-hold-out part when it exists (it is the larger sample); the hold-out part is
    # diagnosed separately for the record (outcome-free: minute-of-day |return| profile only)
    pre = raw[raw["local"] < ho_cut_local]
    basis = pre if len(pre) > 100_000 else raw
    cv = clock_verdict(sym, basis["local"], basis["close"]) if clock == "auto" else {"verdict": clock, "status": "forced", "text": f"forced {clock}"}
    post = raw[raw["local"] >= ho_cut_local]
    cv_ho = clock_verdict(sym, post["local"], post["close"]) if (clock == "auto" and len(post) > 50_000 and basis is pre) else None
    ho_self = cv_ho is not None or basis is not pre     # the hold-out part was diagnosed on its own bars
    df = to_utc(raw, cv["verdict"])
    n_dropped = int(len(raw) - len(df))
    excl_notes = []
    for a, b, why in EXCLUDE.get(sym, []):
        m = (df["ts"] >= pd.Timestamp(a, tz="UTC")) & (df["ts"] <= pd.Timestamp(b, tz="UTC"))
        if m.any():
            excl_notes.append((pd.Timestamp(a, tz="UTC"), f"EXCLUDED {int(m.sum())} bars {a}..{b} UTC: {why}"))
            df = df.loc[~m]
    is_df, ho_df = split_holdout(df)
    out.update({"clock": cv, "clock_holdout": cv_ho, "dropped_dst": n_dropped, "dup_local": n_dup_local})
    src = PAGE.format(pair_l=sym.lower(), year="YYYY") + " (+ /YYYY/M for current-year months)"
    base_note = (f"HistData personal use; fetched {common.today()}; {{n}} raw zips pinned in fetch_log; clock={cv['verdict']} ({cv['status']}): "
                 f"{{clock}}; bid quotes; volume=0; weekend rows kept; {n_dropped} bars dropped at DST fall-back/spring-forward; "
                 f"{n_dup_local} duplicate local stamps dropped")
    for part, dsid, rel, cvx, ho in ((is_df, f"{prefix}_{sym}", f"derived/{prefix}/{sym}", cv, False),
                                      (ho_df, f"{prefix}_{sym}_holdout", f"holdout/{prefix}/{sym}", cv_ho or cv, True)):
        if part.empty or (holdout_only and not ho):
            continue
        gaps = histdata_qa.gap_note(part)
        n = sum(1 for p in pins if (int(p[:4]) >= HOLDOUT_YEAR) == ho)
        note = base_note.format(n=n, clock=cvx["text"]) + f"; gaps: {gaps}" + "".join(f"; {x}" for t0, x in excl_notes if (t0 >= pd.Timestamp(paths.HOLDOUT_START, tz="UTC")) == ho)
        if ho:
            note = ("HOLD-OUT (ts >= " + paths.HOLDOUT_START + "; gateway window 'holdout' only; QA outcome-free); "
                    + note + ("; clock diag on hold-out part itself" if ho_self else "; clock verdict from the IS part"))
        if missing:
            note += f"; periods listed but not downloaded: {','.join(missing)}"
        out[dsid] = common.land(dsid, part, rel, fmt="partitioned", source=src, licence_status="free", resolution="1m",
                                tz_note="bar open UTC (converted from HistData local clock, see notes)", notes=note,
                                dry_run=dry_run, manifest=manifest)
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
    ap.add_argument("--symbols", default="", help="batch 1b path: comma list (e.g. SPXUSD,GRXEUR); uses ingest_symbol")
    ap.add_argument("--start-year", type=int, default=2010)
    ap.add_argument("--prefix", default="histdata_cfd_1m")
    ap.add_argument("--holdout-only", action="store_true", help="only periods >= the hold-out year (FX 2025-2026)")
    a = ap.parse_args(argv)
    if a.symbols:
        for sym in (x.strip().upper() for x in a.symbols.split(",") if x.strip()):
            try:
                r = ingest_symbol(sym, prefix=a.prefix, start_year=a.start_year, holdout_only=a.holdout_only, clock=a.clock, dry_run=a.dry_run)
                print(f"{sym}: {r.get('clock', {}).get('text', 'no data')}")
            except NotCarried as e:
                print(f"NOT CARRIED: {e}", file=sys.stderr)
            except common.RateLimited as e:
                print(f"STOP (429): {e}", file=sys.stderr)
                return 2
        return 0
    run(tuple(p.strip().upper() for p in a.pairs.split(",") if p.strip()), _years(a.years), dry_run=a.dry_run, clock=a.clock)


if __name__ == "__main__":
    main()
