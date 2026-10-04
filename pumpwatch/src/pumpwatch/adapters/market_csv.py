"""Daily bars from Yahoo chart JSON, plus the project's CSV formats (pure, no network).

Yahoo chart API (``/v8/finance/chart/{T}?interval=1d``)
    ``chart.result[0].timestamp`` holds one Unix timestamp per day (usually the
    market *open*, e.g. 14:30 UTC for New York in winter) and
    ``indicators.quote[0]`` holds parallel ``open/high/low/close/volume``
    arrays. Rows with any ``None`` (days Yahoo has no complete quote for) are
    skipped. Timestamps are converted to the **exchange-local** calendar date
    with ``meta.exchangeTimezoneName`` (falling back to ``meta.gmtoffset``):
    a plain UTC conversion lands on the wrong day whenever the timestamp sits
    near midnight UTC (e.g. 00:00 New York = 04:00/05:00 UTC is fine, but a
    20:00 New York close stamp is 00:00/01:00 UTC *the next day*).

    Yahoo prices are back-adjusted for later splits (volume inversely), so
    absolute price levels of serially reverse-split pump tickers can look
    huge; returns and dollar volume are unaffected.

CSV formats (header row required, extra columns ignored)
    bars.csv    ``ticker,day,open,high,low,close,volume``
    filings.csv ``ticker,day,form,title``

Validation
    :func:`validate_bars` drops bars with non-positive prices, ``high < low``
    or negative volume, and duplicate ``(ticker, day)`` rows (first kept),
    returning the reasons so callers can report them.
"""

from __future__ import annotations

import csv
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import IO, Any, Iterable, Iterator

from ..models import Bar, Dataset, Filing

try:  # zoneinfo needs the OS tz database (or the tzdata package); degrade to gmtoffset.
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]

BAR_FIELDS = ("ticker", "day", "open", "high", "low", "close", "volume")
FILING_FIELDS = ("ticker", "day", "form", "title")

PathOrFile = str | Path | IO[str]


# ---------------------------------------------------------------------------
# Yahoo chart JSON
# ---------------------------------------------------------------------------
def _result(json_obj: Any) -> dict | None:
    results = ((json_obj or {}).get("chart") or {}).get("result") or []
    return results[0] if results else None


def yahoo_error(json_obj: Any) -> str | None:
    """Yahoo's error description (e.g. "No data found, symbol may be delisted"), if any."""

    err = ((json_obj or {}).get("chart") or {}).get("error")
    if not err:
        return None if _result(json_obj) else "empty chart response"
    return str(err.get("description") or err.get("code") or err)


def local_date(ts: int | float, tz_name: str | None = None, gmtoffset: int | None = None) -> date:
    """Exchange-local calendar date of a Unix timestamp."""

    if tz_name and ZoneInfo is not None:
        try:
            return datetime.fromtimestamp(ts, ZoneInfo(tz_name)).date()
        except Exception:  # unknown zone or no tz database: fall through
            pass
    offset = timedelta(seconds=gmtoffset or 0)
    return datetime.fromtimestamp(ts, timezone(offset)).date()


def yahoo_meta(json_obj: Any) -> dict:
    """Instrument metadata from a chart response (empty dict when there is no result)."""

    res = _result(json_obj)
    if not res:
        return {}
    m = res.get("meta") or {}
    tz, off = m.get("exchangeTimezoneName"), m.get("gmtoffset")
    first = m.get("firstTradeDate")
    return {
        "symbol": m.get("symbol"),
        "currency": m.get("currency"),
        "exchange_name": m.get("exchangeName"),
        "full_exchange_name": m.get("fullExchangeName"),
        "long_name": m.get("longName"),
        "short_name": m.get("shortName"),
        "instrument_type": m.get("instrumentType"),
        "timezone": tz,
        "gmtoffset": off,
        "first_trade_date": local_date(first, tz, off) if isinstance(first, (int, float)) else None,
    }


def parse_yahoo_chart(json_obj: Any, ticker: str) -> list[Bar]:
    """Daily bars from a Yahoo chart response, validated and sorted by day."""

    res = _result(json_obj)
    if not res:
        return []
    m = res.get("meta") or {}
    tz, off = m.get("exchangeTimezoneName"), m.get("gmtoffset")
    stamps = res.get("timestamp") or []
    quotes = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    cols = [quotes.get(k) or [] for k in ("open", "high", "low", "close", "volume")]
    ticker = ticker.strip().upper()
    bars: list[Bar] = []
    for i, ts in enumerate(stamps):
        row = [c[i] if i < len(c) else None for c in cols]
        if ts is None or any(v is None for v in row):
            continue
        # Yahoo stores prices as float32; 7 significant digits drops the noise
        # (130.27999877929688 -> 130.28). Volume is kept exact.
        o, h, lo, c = (float(f"{float(x):.7g}") for x in row[:4])
        v = float(row[4])
        bars.append(Bar(ticker, local_date(ts, tz, off), o, h, lo, c, v))
    good, _ = validate_bars(bars)
    return good


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------
def validate_bars(bars: Iterable[Bar]) -> tuple[list[Bar], list[str]]:
    """Drop impossible bars and duplicate (ticker, day) rows; return (kept sorted, problems)."""

    kept: dict[tuple[str, date], Bar] = {}
    problems: list[str] = []
    for b in bars:
        key = (b.ticker, b.day)
        why = None
        if min(b.open, b.high, b.low, b.close) <= 0:
            why = "non-positive price"
        elif b.high < b.low:
            why = "high < low"
        elif b.volume < 0:
            why = "negative volume"
        elif key in kept:
            why = "duplicate day"
        if why:
            problems.append(f"{b.ticker} {b.day}: {why}")
        else:
            kept[key] = b
    return sorted(kept.values(), key=lambda b: (b.ticker, b.day)), problems


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------
@contextmanager
def _open(path_or_file: PathOrFile, mode: str) -> Iterator[IO[str]]:
    if isinstance(path_or_file, (str, Path)):
        with open(path_or_file, mode, newline="", encoding="utf-8") as fh:
            yield fh
    else:
        yield path_or_file


def _rows(fh: IO[str]) -> Iterator[dict]:
    for row in csv.DictReader(fh):
        t = (row.get("ticker") or "").strip()
        if t and not t.startswith("#"):
            yield row


def _num(x: float) -> str:
    """Shortest exact text for a float (integers without a trailing .0)."""

    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else repr(x)


def read_bars_csv(path_or_file: PathOrFile) -> list[Bar]:
    """Read ``ticker,day,open,high,low,close,volume``; invalid rows are dropped (see validate_bars)."""

    with _open(path_or_file, "r") as fh:
        bars = [
            Bar(
                r["ticker"].strip().upper(),
                date.fromisoformat(r["day"].strip()),
                *(float(r[k]) for k in ("open", "high", "low", "close", "volume")),
            )
            for r in _rows(fh)
        ]
    return validate_bars(bars)[0]


def write_bars_csv(bars: Iterable[Bar], path_or_file: PathOrFile) -> None:
    with _open(path_or_file, "w") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(BAR_FIELDS)
        for b in sorted(bars, key=lambda b: (b.ticker, b.day)):
            w.writerow([b.ticker, b.day.isoformat(), *(_num(x) for x in (b.open, b.high, b.low, b.close, b.volume))])


def read_filings_csv(path_or_file: PathOrFile) -> list[Filing]:
    with _open(path_or_file, "r") as fh:
        return [
            Filing(r["ticker"].strip().upper(), date.fromisoformat(r["day"].strip()), r["form"].strip(), (r.get("title") or "").strip())
            for r in _rows(fh)
        ]


def write_filings_csv(filings: Iterable[Filing], path_or_file: PathOrFile) -> None:
    with _open(path_or_file, "w") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(FILING_FIELDS)
        for f in sorted(set(filings), key=lambda f: (f.ticker, f.day, f.form, f.title)):
            w.writerow([f.ticker, f.day.isoformat(), f.form, f.title])


def load_dataset(bars_csv: PathOrFile, filings_csv: PathOrFile | None = None) -> Dataset:
    """Build an engine-ready :class:`~pumpwatch.models.Dataset` from the two CSVs."""

    filings = read_filings_csv(filings_csv) if filings_csv is not None else []
    return Dataset(bars=read_bars_csv(bars_csv), filings=filings)
