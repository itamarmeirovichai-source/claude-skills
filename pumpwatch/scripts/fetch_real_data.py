#!/usr/bin/env python3
"""Download real daily bars (Yahoo) and filings (SEC EDGAR) for the labelled cases.

Run from the ``pumpwatch/`` directory::

    python scripts/fetch_real_data.py                       # all tickers in data/cases.csv
    python scripts/fetch_real_data.py --only AREB GME       # refresh a few tickers

For each ticker in the cases file the window is the union of its cases,
``[min(start) - pre_days, max(end) + post_days]``. Outputs (in ``--out``):

* ``bars.csv``     ticker,day,open,high,low,close,volume (Yahoo, split-adjusted)
* ``filings.csv``  ticker,day,form,title (EDGAR filingDate = public day). Filings
  are kept from ``window_start - 400`` days so the dormant-shell check in
  ``signals/corporate.py`` (a 365-day gap) can see the history before the window.
* ``coverage.csv`` one row per ticker: what was found, status and warnings.

Ticker reuse: Yahoo serves the *current* holder of a symbol and SEC's
``company_tickers.json`` maps only current tickers. Delisted pump symbols may
return nothing or another company's data. The script warns when Yahoo's first
trade date is after a case start, when the Yahoo and EDGAR names share no
significant word, or when the CIK only started filing after the case; bars that
do not overlap any case window at all are dropped (status ``no_bars``). Use
``--cik-overrides`` (ticker,cik,company) to pin the historical CIK for delisted
tickers.

Raw responses are cached in ``--cache-dir`` so re-runs do not hit the network
(delete the cache to refresh). SEC calls are throttled to <= 5/s with a
declared User-Agent, as SEC requires. With ``--only`` the existing output
files are kept and only the selected tickers' rows are replaced.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pumpwatch.adapters import edgar, market_csv  # noqa: E402
from pumpwatch.models import Bar, Filing  # noqa: E402

SEC_UA = "PumpWatch research contact@example.com"
# Yahoo answers a short browser-like UA; a full Chrome UA string (without the
# cookies a real browser sends) gets HTTP 429, as do non-browser UAs.
YAHOO_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SEC_MIN_INTERVAL = 0.2  # seconds between SEC requests (<= 5/s; SEC allows 10/s)
FILING_HISTORY_DAYS = 400  # history before the window for the dormant-shell check
COVERAGE_FIELDS = (
    "ticker,label,cik,cik_source,edgar_name,yahoo_name,yahoo_exchange,window_start,window_end,"
    "bars,first_bar,last_bar,filings,status,warning"
).split(",")
NAME_STOPWORDS = {
    "inc", "corp", "corporation", "co", "company", "ltd", "limited", "plc", "llc", "lp", "sa", "nv", "ag",
    "holdings", "holding", "group", "the", "of", "and", "international", "intl", "global", "class", "common",
    "stock", "shares", "ordinary", "new", "de", "com",
}


class FetchError(Exception):
    """A request that failed after retries (or with a non-retryable status)."""


# ---------------------------------------------------------------------------
# HTTP with cache, throttle and retries
# ---------------------------------------------------------------------------
class Http:
    def __init__(self, cache_dir: Path, yahoo_sleep: float, retries: int = 4) -> None:
        self.cache_dir = cache_dir
        self.yahoo_sleep = yahoo_sleep
        self.retries = retries
        self._last: dict[str, float] = {}
        cache_dir.mkdir(parents=True, exist_ok=True)

    def _wait(self, kind: str, interval: float) -> None:
        gap = time.monotonic() - self._last.get(kind, 0.0)
        if gap < interval:
            time.sleep(interval - gap)
        self._last[kind] = time.monotonic()

    def get_json(self, url: str, cache_name: str, kind: str, keep_status: tuple[int, ...] = ()) -> dict:
        """GET JSON, caching the body. ``keep_status`` lists HTTP errors whose JSON body is a valid answer."""

        path = self.cache_dir / re.sub(r"[^A-Za-z0-9._-]", "_", cache_name)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        ua, interval = (SEC_UA, SEC_MIN_INTERVAL) if kind == "sec" else (YAHOO_UA, self.yahoo_sleep)
        last_err = ""
        for attempt in range(self.retries):
            self._wait(kind, interval)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = resp.read()
            except urllib.error.HTTPError as e:
                body = e.read()
                if e.code in keep_status:
                    pass  # e.g. Yahoo 404 "symbol may be delisted": a real, cacheable answer
                elif e.code == 429 or e.code >= 500:
                    last_err = f"HTTP {e.code}"
                    time.sleep(2 ** (attempt + 1))
                    continue
                else:
                    raise FetchError(f"HTTP {e.code} for {url}") from None
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                last_err = str(e)
                time.sleep(2 ** (attempt + 1))
                continue
            data = json.loads(body)
            path.write_text(json.dumps(data), encoding="utf-8")
            return data
        raise FetchError(f"{last_err} after {self.retries} attempts: {url}")


# ---------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------
@dataclass
class TickerJob:
    ticker: str
    labels: set[str] = field(default_factory=set)
    cases: list[tuple[date, date]] = field(default_factory=list)

    def window(self, pre: int, post: int) -> tuple[date, date]:
        return min(s for s, _ in self.cases) - timedelta(days=pre), max(e for _, e in self.cases) + timedelta(days=post)


def read_cases(path: Path) -> dict[str, TickerJob]:
    jobs: dict[str, TickerJob] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            t = (row.get("ticker") or "").strip().upper()
            if not t or t.startswith("#"):
                continue
            try:
                start, end = date.fromisoformat(row["start"].strip()), date.fromisoformat(row["end"].strip())
            except (KeyError, ValueError, AttributeError):
                print(f"  ! skipping case row with bad dates: {row}", file=sys.stderr)
                continue
            job = jobs.setdefault(t, TickerJob(t))
            job.labels.add((row.get("label") or "").strip().lower())
            job.cases.append((start, end))
    return jobs


def read_overrides(path: Path | None) -> dict[str, tuple[str, str]]:
    if not path or not path.exists():
        return {}
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            t = (row.get("ticker") or "").strip().upper()
            if t and not t.startswith("#") and (row.get("cik") or "").strip():
                out[t] = (edgar.cik10(row["cik"]), (row.get("company") or "").strip())
    return out


# ---------------------------------------------------------------------------
# per-ticker work
# ---------------------------------------------------------------------------
def _unix(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())


def _words(name: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (name or "").lower()) if w not in NAME_STOPWORDS and len(w) > 1}


def fetch_ticker(job: TickerJob, http: Http, ticker_ciks: dict[str, str], overrides: dict, pre: int, post: int):
    t = job.ticker
    w_start, w_end = job.window(pre, post)
    cases_lo, cases_hi = min(s for s, _ in job.cases), max(e for _, e in job.cases)
    row = {k: "" for k in COVERAGE_FIELDS}
    row.update(ticker=t, label="/".join(sorted(job.labels)), window_start=w_start, window_end=w_end)
    warnings: list[str] = []
    bars: list[Bar] = []
    filings: list[Filing] = []
    errors: list[str] = []

    # --- bars (Yahoo) -------------------------------------------------------
    p1, p2 = _unix(w_start), _unix(w_end + timedelta(days=1))
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1={p1}&period2={p2}&interval=1d&events=split"
    yahoo_names: set[str] = set()
    try:
        chart = http.get_json(url, f"yahoo_{t}_{p1}_{p2}.json", "yahoo", keep_status=(400, 404))
        meta = market_csv.yahoo_meta(chart)
        bars = market_csv.parse_yahoo_chart(chart, t)
        row["yahoo_name"] = meta.get("long_name") or meta.get("short_name") or ""
        row["yahoo_exchange"] = meta.get("full_exchange_name") or meta.get("exchange_name") or ""
        yahoo_names = _words(meta.get("long_name") or "") | _words(meta.get("short_name") or "")
        if not bars and market_csv.yahoo_error(chart):
            warnings.append(f"yahoo: {market_csv.yahoo_error(chart)}")
        ftd = meta.get("first_trade_date")
        if ftd and ftd > cases_lo:
            warnings.append(f"yahoo first trade date {ftd} after case start {cases_lo} (ticker reuse or relisting?)")
    except FetchError as e:
        errors.append(f"yahoo: {e}")

    if bars and not any(cases_lo <= b.day <= cases_hi for b in bars):
        warnings.append(f"{len(bars)} bars outside every case window dropped (likely another company)")
        bars = []
    if bars:
        if bars[0].day > cases_lo + timedelta(days=4) or bars[-1].day < min(cases_hi, date.today()) - timedelta(days=4):
            warnings.append("bars do not cover the full case window")
        zero = sum(b.volume == 0 for b in bars)
        if zero > len(bars) // 5:
            warnings.append(f"{zero}/{len(bars)} bars have zero volume (split-adjusted volume rounded away?)")

    # --- filings (EDGAR) ----------------------------------------------------
    cik, source = None, ""
    if t in overrides:
        cik, source = overrides[t][0], "override"
    elif t in ticker_ciks:
        cik, source = ticker_ciks[t], "sec_tickers"
    row.update(cik=cik or "", cik_source=source)
    f_start = w_start - timedelta(days=FILING_HISTORY_DAYS)
    edgar_names: set[str] = set()
    if cik:
        try:
            sub = http.get_json(f"https://data.sec.gov/submissions/CIK{cik}.json", f"sec_CIK{cik}.json", "sec")
            row["edgar_name"] = sub.get("name") or ""
            edgar_names = _words(sub.get("name") or "")
            for fn in sub.get("formerNames") or []:
                edgar_names |= _words(fn.get("name") or "")
            if t in overrides and overrides[t][1]:
                edgar_names |= _words(overrides[t][1])
            filings = edgar.parse_submissions(sub, t, f_start, w_end)
            covered = edgar.recent_coverage_start(sub)
            if covered is None or covered > f_start:
                for name in edgar.extra_page_names(sub, f_start, w_end):
                    page = http.get_json(f"https://data.sec.gov/submissions/{name}", f"sec_{name}", "sec")
                    filings = edgar.merge_filings(filings, edgar.parse_submissions_page(page, t, f_start, w_end))
            first = edgar.earliest_filing_date(sub)
            if first and first > cases_hi:
                warnings.append(f"CIK {cik} first filed {first}, after the cases (ticker reuse?)")
        except FetchError as e:
            errors.append(f"edgar: {e}")

    if yahoo_names and edgar_names and not (yahoo_names & edgar_names):
        warnings.append(f"name mismatch yahoo={row['yahoo_name']!r} edgar={row['edgar_name']!r} (possible ticker reuse)")

    row.update(
        bars=len(bars),
        first_bar=bars[0].day if bars else "",
        last_bar=bars[-1].day if bars else "",
        filings=len(filings),
    )
    if errors and not bars and not filings:
        status = "error"
    elif not bars:
        status = "no_bars"
    elif not cik:
        status = "no_cik"
    elif "bars do not cover the full case window" in warnings:
        status = "partial_bars"
    else:
        status = "ok"
    row["status"] = status
    row["warning"] = "; ".join(errors + warnings)
    return bars, filings, row


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cases", type=Path, default=Path("data/cases.csv"))
    ap.add_argument("--cik-overrides", type=Path, default=Path("data/cik_overrides.csv"))
    ap.add_argument("--out", type=Path, default=Path("data/real"))
    ap.add_argument("--cache-dir", type=Path, default=None, help="raw JSON cache (default: <out>/.cache)")
    ap.add_argument("--pre-days", type=int, default=120)
    ap.add_argument("--post-days", type=int, default=30)
    ap.add_argument("--only", nargs="+", metavar="TICKER", help="fetch only these tickers")
    ap.add_argument("--sleep", type=float, default=1.0, help="seconds between Yahoo requests")
    args = ap.parse_args(argv)

    jobs = read_cases(args.cases)
    if args.only:
        wanted = {t.strip().upper() for x in args.only for t in x.split(",") if t.strip()}
        missing = wanted - set(jobs)
        if missing:
            print(f"not in {args.cases}: {', '.join(sorted(missing))}", file=sys.stderr)
        jobs = {t: j for t, j in jobs.items() if t in wanted}
    if not jobs:
        print("no tickers to fetch", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    http = Http(args.cache_dir or args.out / ".cache", args.sleep)
    overrides = read_overrides(args.cik_overrides)
    try:
        ticker_ciks = edgar.parse_company_tickers(
            http.get_json("https://www.sec.gov/files/company_tickers.json", "sec_company_tickers.json", "sec")
        )
    except FetchError as e:
        print(f"! could not load SEC ticker map ({e}); only --cik-overrides will be used", file=sys.stderr)
        ticker_ciks = {}

    all_bars: list[Bar] = []
    all_filings: list[Filing] = []
    coverage: list[dict] = []
    for i, t in enumerate(sorted(jobs), 1):
        try:
            bars, filings, row = fetch_ticker(jobs[t], http, ticker_ciks, overrides, args.pre_days, args.post_days)
        except Exception as e:  # one bad ticker must never abort the run
            bars, filings = [], []
            row = {k: "" for k in COVERAGE_FIELDS} | {"ticker": t, "status": "error", "warning": f"{type(e).__name__}: {e}"}
        all_bars += bars
        all_filings += filings
        coverage.append(row)
        print(f"[{i}/{len(jobs)}] {t:<8} {row['status']:<12} bars={row['bars'] or 0:<5} filings={row['filings'] or 0:<5} {row['warning']}")

    bars_path, filings_path, cov_path = args.out / "bars.csv", args.out / "filings.csv", args.out / "coverage.csv"
    if args.only:  # keep other tickers' rows from a previous full run
        done = set(jobs)
        if bars_path.exists():
            all_bars += [b for b in market_csv.read_bars_csv(bars_path) if b.ticker not in done]
        if filings_path.exists():
            all_filings += [f for f in market_csv.read_filings_csv(filings_path) if f.ticker not in done]
        if cov_path.exists():
            with open(cov_path, newline="", encoding="utf-8") as fh:
                coverage += [r for r in csv.DictReader(fh) if r.get("ticker") not in done]
    market_csv.write_bars_csv(all_bars, bars_path)
    market_csv.write_filings_csv(all_filings, filings_path)
    with open(cov_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, COVERAGE_FIELDS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(coverage, key=lambda r: r["ticker"]))

    counts: dict[str, int] = {}
    for r in coverage:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(
        f"\n{len(coverage)} tickers: "
        + ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        + f" | {len(all_bars)} bars, {len(all_filings)} filings -> {args.out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
