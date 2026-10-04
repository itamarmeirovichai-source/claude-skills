"""Small builders for hand-made test markets."""

from __future__ import annotations

from datetime import date, timedelta

from pumpwatch.models import Bar, Dataset, Filing, Post

START = date(2025, 1, 6)  # a Monday


def days(n: int, start: date = START) -> list[date]:
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def flat_bars(ticker: str, n: int, price: float = 1.0, volume: float = 100_000) -> list[Bar]:
    return [Bar(ticker, d, price, price, price, price, volume) for d in days(n)]


def with_spike(bars: list[Bar], i: int, vol_mult: float, price_mult: float = 1.0) -> list[Bar]:
    b = bars[i]
    out = list(bars)
    out[i] = Bar(b.ticker, b.day, b.open, b.high * price_mult, b.low, b.close * price_mult, b.volume * vol_mult)
    return out


def promo_posts(ticker: str, day: date, n_authors: int, text: str | None = None) -> list[Post]:
    text = text or f"${ticker} is about to explode!!! huge news coming, get in now 🚀🚀"
    return [Post("telegram", f"a{i}", day, text, (ticker,)) for i in range(n_authors)]


def dataset(bars=(), filings=(), posts=()) -> Dataset:
    return Dataset(bars=list(bars), filings=list(filings), posts=list(posts))


__all__ = ["START", "days", "flat_bars", "with_spike", "promo_posts", "dataset", "Filing"]
