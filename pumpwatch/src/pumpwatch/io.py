"""Load and save the engine's data directory.

A data directory holds plain CSV files (any of them may be missing, except
bars):

    bars.csv          ticker,day,open,high,low,close,volume
    filings.csv       ticker,day,form,title
    posts.csv         source,author,day,text[,tickers]   (tickers: space separated)
    broker_flow.csv   ticker,day,new_buyers,first_time_microcap_buyers
    reports.csv       ticker,day,note

When posts.csv has no tickers column, cashtags are extracted from the text and
kept only if the ticker exists in bars.csv.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from .models import Bar, BrokerFlow, Dataset, Filing, Post, VictimReport
from .text import extract_cashtags


class DataError(ValueError):
    pass


def _rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if any((v or "").strip() for v in r.values())]


def _day(value: str, where: str) -> date:
    try:
        return date.fromisoformat(value.strip()[:10])
    except (AttributeError, ValueError) as exc:
        raise DataError(f"{where}: bad date {value!r} (expected YYYY-MM-DD)") from exc


def _num(value: str, where: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise DataError(f"{where}: bad number {value!r}") from exc


def load_dir(path: str | Path) -> Dataset:
    root = Path(path)
    if not (root / "bars.csv").exists():
        raise DataError(f"{root}: bars.csv is required")
    data = Dataset()
    for i, r in enumerate(_rows(root / "bars.csv"), start=2):
        w = f"bars.csv line {i}"
        data.bars.append(
            Bar(
                r["ticker"].strip().upper(),
                _day(r["day"], w),
                _num(r["open"], w),
                _num(r["high"], w),
                _num(r["low"], w),
                _num(r["close"], w),
                _num(r["volume"], w),
            )
        )
    universe = {b.ticker for b in data.bars}
    for i, r in enumerate(_rows(root / "filings.csv"), start=2):
        data.filings.append(
            Filing(r["ticker"].strip().upper(), _day(r["day"], f"filings.csv line {i}"), r["form"].strip(), (r.get("title") or "").strip())
        )
    for i, r in enumerate(_rows(root / "posts.csv"), start=2):
        text = r.get("text") or ""
        if r.get("tickers"):
            tickers = tuple(t.upper() for t in r["tickers"].split() if t.upper() in universe)
        else:
            tickers = extract_cashtags(text, universe)
        if tickers:
            data.posts.append(Post(r["source"].strip(), r["author"].strip(), _day(r["day"], f"posts.csv line {i}"), text, tickers))
    for i, r in enumerate(_rows(root / "broker_flow.csv"), start=2):
        w = f"broker_flow.csv line {i}"
        data.broker_flow.append(
            BrokerFlow(r["ticker"].strip().upper(), _day(r["day"], w), int(_num(r["new_buyers"], w)), int(_num(r.get("first_time_microcap_buyers") or 0, w)))
        )
    for i, r in enumerate(_rows(root / "reports.csv"), start=2):
        data.reports.append(VictimReport(r["ticker"].strip().upper(), _day(r["day"], f"reports.csv line {i}"), (r.get("note") or "").strip()))
    return data


def save_dir(data: Dataset, path: str | Path) -> None:
    root = Path(path)
    root.mkdir(parents=True, exist_ok=True)

    def write(name: str, header: list[str], rows: list[list]) -> None:
        if not rows and name != "bars.csv":
            return
        with (root / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)

    write("bars.csv", ["ticker", "day", "open", "high", "low", "close", "volume"],
          [[b.ticker, b.day.isoformat(), b.open, b.high, b.low, b.close, b.volume] for b in data.bars])
    write("filings.csv", ["ticker", "day", "form", "title"],
          [[f.ticker, f.day.isoformat(), f.form, f.title] for f in data.filings])
    write("posts.csv", ["source", "author", "day", "text", "tickers"],
          [[p.source, p.author, p.day.isoformat(), p.text, " ".join(p.tickers)] for p in data.posts])
    write("broker_flow.csv", ["ticker", "day", "new_buyers", "first_time_microcap_buyers"],
          [[f.ticker, f.day.isoformat(), f.new_buyers, f.first_time_microcap_buyers] for f in data.broker_flow])
    write("reports.csv", ["ticker", "day", "note"], [[r.ticker, r.day.isoformat(), r.note] for r in data.reports])


def save_cases(cases, path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ticker", "label", "start", "end", "note"])
        for c in cases:
            w.writerow([c.ticker, c.label, c.start.isoformat(), c.end.isoformat(), c.note])
