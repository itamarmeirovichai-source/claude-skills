"""Three public, keyless sources: a stock list, per-ticker headlines and daily price bars."""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .http import FetchError, Http

SCREENER_URL = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
NEWS_URL = "https://query2.finance.yahoo.com/v1/finance/search?q={ticker}&quotesCount=0&newsCount=10"
BARS_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?range={span}&interval=1d"
ET = ZoneInfo("America/New_York")


def _number(text: object) -> float | None:
    try:
        return float(str(text).replace("$", "").replace(",", ""))
    except ValueError:
        return None


def screener(http: Http) -> list[dict[str, Any]]:
    payload = http.get_json(SCREENER_URL)
    try:
        rows = payload["data"]["rows"]  # type: ignore[index,call-overload]
    except (KeyError, TypeError) as error:
        raise FetchError("unexpected stock-list format") from error
    out = []
    for row in rows:
        out.append(
            {
                "symbol": str(row.get("symbol", "")).strip(),
                "name": str(row.get("name", "")).strip(),
                "country": str(row.get("country", "")).strip(),
                "price": _number(row.get("lastsale")),
                "volume": _number(row.get("volume")),
            }
        )
    return out


def news(http: Http, ticker: str) -> list[dict[str, Any]]:
    payload = http.get_json(NEWS_URL.format(ticker=ticker))
    items = payload.get("news") if isinstance(payload, dict) else None
    out = []
    for item in items or []:
        title, ts = item.get("title"), item.get("providerPublishTime")
        if not title or not isinstance(ts, (int, float)):
            continue
        ident = item.get("uuid") or hashlib.sha256(f"{title}|{ts}".encode()).hexdigest()[:32]
        out.append(
            {
                "id": str(ident),
                "ts": int(ts),
                "title": str(title),
                "publisher": str(item.get("publisher") or ""),
                "link": str(item.get("link") or ""),
                "related": [str(t) for t in item.get("relatedTickers") or []],
            }
        )
    return out


def bars(http: Http, ticker: str, span: str = "3mo") -> list[dict[str, Any]]:
    payload = http.get_json(BARS_URL.format(ticker=ticker, span=span))
    try:
        result = payload["chart"]["result"][0]  # type: ignore[index,call-overload]
        stamps = result.get("timestamp") or []
        quote = result["indicators"]["quote"][0]
    except (KeyError, TypeError, IndexError) as error:
        raise FetchError(f"unexpected price format for {ticker}") from error
    out = []
    for i, stamp in enumerate(stamps):
        out.append(
            {
                "date": datetime.fromtimestamp(stamp, ET).date().isoformat(),
                "open": quote["open"][i],
                "close": quote["close"][i],
                "volume": quote["volume"][i],
            }
        )
    return out
