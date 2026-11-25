"""The daily cycle: fetch headlines, record verdicts before the open, settle after the close, report."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from datetime import date, datetime
from pathlib import Path
from typing import Any

from . import config, ledger, sessions, sources
from .http import FetchError, Http


class Refused(Exception):
    """A rule of the pre-registration would be broken."""


def today_et(now: datetime) -> date:
    return now.astimezone(sessions.ET).date()


def _iso(moment: datetime) -> str:
    return moment.astimezone(sessions.ET).isoformat(timespec="seconds")


def prompt_sha(path: Path | None = None) -> str:
    return hashlib.sha256((path or config.PROMPT).read_bytes()).hexdigest()


def load_universe(path: Path | None = None) -> list[str]:
    data = json.loads((path or config.UNIVERSE).read_text(encoding="utf-8"))
    return [t["symbol"] for t in data["tickers"]]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def open_fetch(http: Http, tickers: list[str], now: datetime) -> dict[str, Any]:
    """Headlines per ticker from the news window. Nothing is recorded here."""
    day = today_et(now)
    if not sessions.is_trading_day(day):
        raise Refused(f"{day} is not a trading day")
    start, end = sessions.window(day)
    cutoff = min(end, now)
    found: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []
    for ticker in tickers:
        try:
            items = sources.news(http, ticker)
        except FetchError:
            errors.append(ticker)
            continue
        keep = [i for i in items if ticker in i["related"] and start.timestamp() <= i["ts"] <= cutoff.timestamp()]
        keep.sort(key=lambda i: i["ts"], reverse=True)
        if keep:
            found[ticker] = keep[: config.MAX_HEADLINES]
    return {
        "date": day.isoformat(),
        "fetched_at": _iso(now),
        "window": [_iso(start), _iso(cutoff)],
        "universe_size": len(tickers),
        "errors": errors,
        "tickers": found,
    }


def record(
    pending: dict[str, Any],
    verdicts: dict[str, Any],
    model: str,
    now: datetime,
    ledger_path: Path,
    prompt_hash: str,
) -> list[dict[str, Any]]:
    """Write one day's verdicts to the log. Refuses anything that could let the future in."""
    day = today_et(now)
    if pending.get("date") != day.isoformat():
        raise Refused("the headline file is for another day")
    if not sessions.is_trading_day(day):
        raise Refused(f"{day} is not a trading day")
    if now >= sessions.at_et(day, config.RECORD_DEADLINE):
        raise Refused("too late: signals must be recorded before 09:25 ET")
    if datetime.fromisoformat(pending["fetched_at"]) > now:
        raise Refused("the headline file is dated in the future")
    if any(e.get("date") == pending["date"] for e in ledger.read(ledger_path)):
        raise Refused("this day is already recorded")
    tickers = pending["tickers"]
    missing, extra = sorted(set(tickers) - set(verdicts)), sorted(set(verdicts) - set(tickers))
    if missing or extra:
        raise Refused(f"verdicts do not match the headline file (missing {missing}, extra {extra})")
    for ticker, verdict in verdicts.items():
        if isinstance(verdict, bool) or verdict not in (-1, 0, 1):
            raise Refused(f"verdict for {ticker} must be 1, -1 or 0")
    stamp = _iso(now)
    bodies: list[dict[str, Any]] = [
        {
            "type": "batch",
            "date": pending["date"],
            "fetched_at": pending["fetched_at"],
            "recorded_at": stamp,
            "universe_size": pending["universe_size"],
            "tickers_with_news": len(tickers),
            "fetch_errors": len(pending["errors"]),
            "model": model,
            "prompt_sha": prompt_hash,
        }
    ]
    for ticker in sorted(tickers):
        bodies.append(
            {
                "type": "signal",
                "date": pending["date"],
                "ticker": ticker,
                "verdict": int(verdicts[ticker]),
                "headline_ids": [i["id"] for i in tickers[ticker]],
                "links": [i["link"] for i in tickers[ticker]],
                "recorded_at": stamp,
            }
        )
    return ledger.append(ledger_path, bodies)


def settle(http: Http, ledger_path: Path, results_path: Path, now: datetime) -> list[dict[str, Any]]:
    """Open-to-close return of every traded signal whose day is over."""
    day = today_et(now)
    done = {(r["date"], r["ticker"]) for r in read_jsonl(results_path)}
    rows: list[dict[str, Any]] = []
    for entry in ledger.read(ledger_path):
        if entry["type"] != "signal" or entry["verdict"] == 0 or (entry["date"], entry["ticker"]) in done:
            continue
        signal_day = date.fromisoformat(entry["date"])
        over = signal_day < day or (signal_day == day and now >= sessions.at_et(day, config.SETTLE_AFTER))
        if not over:
            continue
        try:
            history = sources.bars(http, entry["ticker"], "1mo")
        except FetchError:
            continue  # try again on the next run
        bar = next((b for b in history if b["date"] == entry["date"]), None)
        row = {"date": entry["date"], "ticker": entry["ticker"], "verdict": entry["verdict"]}
        if bar and bar["open"] and bar["close"]:
            row.update(status="ok", open=bar["open"], close=bar["close"], ret=bar["close"] / bar["open"] - 1)
        elif any(b["date"] > entry["date"] for b in history):
            row.update(status="no_bar")  # later days exist, this one does not: no session or no trade
        else:
            continue  # prices not published yet
        rows.append(row)
    if rows:
        results_path.parent.mkdir(parents=True, exist_ok=True)
        with results_path.open("a", encoding="utf-8") as handle:
            for row in rows:
                handle.write(ledger.canonical(row) + "\n")
    return rows


def _series_stats(series: list[float]) -> dict[str, Any]:
    n = len(series)
    mean = statistics.fmean(series) if n else None
    sd = statistics.stdev(series) if n > 1 else None
    t = mean / (sd / math.sqrt(n)) if mean is not None and sd else None
    return {"days": n, "mean": mean, "sd": sd, "t": t}


def stats(ledger_path: Path, results_path: Path) -> dict[str, Any]:
    entries = ledger.read(ledger_path)
    signals = [e for e in entries if e["type"] == "signal"]
    by_day: dict[str, list[float]] = {}
    no_bar = 0
    for row in read_jsonl(results_path):
        if row["status"] == "ok":
            by_day.setdefault(row["date"], []).append(row["verdict"] * row["ret"])
        else:
            no_bar += 1
    days = sorted(by_day)
    gross = [statistics.fmean(by_day[d]) for d in days]

    def net(cost: float, upto: int | None = None) -> dict[str, Any]:
        return _series_stats([g - 2 * cost for g in gross[:upto]])

    n = len(days)
    if n < config.STAGE1_DAYS:
        decision = f"stage 1 running: {n} of {config.STAGE1_DAYS} trading days"
    elif (net(config.COST_PER_SIDE, config.STAGE1_DAYS)["mean"] or 0) <= 0:
        decision = "CLOSED: stage 1 mean net return is not positive"
    elif n < config.STAGE2_DAYS:
        decision = f"stage 2 running: {n} of {config.STAGE2_DAYS} trading days"
    elif (net(config.COST_PER_SIDE, config.STAGE2_DAYS)["t"] or 0) >= config.STAGE2_T:
        decision = f"PASSED the bar: t >= {config.STAGE2_T} over {config.STAGE2_DAYS} days"
    else:
        decision = f"CLOSED: t below {config.STAGE2_T} after {config.STAGE2_DAYS} days"
    chain_ok, lines, message = ledger.verify(ledger_path)
    return {
        "decision": decision,
        "recorded_days": len({e["date"] for e in entries if e["type"] == "batch"}),
        "signals": len(signals),
        "long": sum(1 for s in signals if s["verdict"] == 1),
        "short": sum(1 for s in signals if s["verdict"] == -1),
        "unclear": sum(1 for s in signals if s["verdict"] == 0),
        "settled_trades": sum(len(v) for v in by_day.values()),
        "no_bar": no_bar,
        "gross": _series_stats(gross),
        "net": net(config.COST_PER_SIDE),
        "net_low_cost": net(config.COST_SENSITIVITY[0]),
        "net_high_cost": net(config.COST_SENSITIVITY[1]),
        "log": {"ok": chain_ok, "lines": lines, "message": message},
    }
