"""Per-ticker view of the dataset with fast date lookups."""

from __future__ import annotations

import bisect
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from statistics import median

from .models import Bar, BrokerFlow, Dataset, Filing, Post, VictimReport


@dataclass
class TickerContext:
    ticker: str
    bars: list[Bar]
    filings: list[Filing]
    posts: list[Post]
    broker_flow: dict[date, BrokerFlow]
    reports: list[VictimReport]
    days: list[date] = field(init=False)
    _bar_index: dict[date, int] = field(init=False)
    _posts_by_day: dict[date, list[Post]] = field(init=False)

    def __post_init__(self) -> None:
        self.bars.sort(key=lambda b: b.day)
        self.filings.sort(key=lambda f: f.day)
        self.reports.sort(key=lambda r: r.day)
        self.days = [b.day for b in self.bars]
        self._bar_index = {d: i for i, d in enumerate(self.days)}
        by_day: dict[date, list[Post]] = defaultdict(list)
        for p in self.posts:
            by_day[p.day].append(p)
        self._posts_by_day = dict(by_day)

    # -- bars -----------------------------------------------------------
    def index(self, day: date) -> int | None:
        return self._bar_index.get(day)

    def bars_before(self, day: date, n: int) -> list[Bar]:
        """Up to ``n`` bars strictly before ``day`` (no look-ahead)."""

        i = bisect.bisect_left(self.days, day)
        return self.bars[max(0, i - n) : i]

    def bar(self, day: date) -> Bar | None:
        i = self.index(day)
        return None if i is None else self.bars[i]

    # -- filings --------------------------------------------------------
    def filings_between(self, start: date, end: date) -> list[Filing]:
        return [f for f in self.filings if start <= f.day <= end]

    def filings_before(self, day: date) -> list[Filing]:
        return [f for f in self.filings if f.day < day]

    # -- posts ----------------------------------------------------------
    def posts_on(self, day: date) -> list[Post]:
        return self._posts_by_day.get(day, [])

    def posts_between(self, start: date, end: date) -> list[Post]:
        out: list[Post] = []
        d = start
        while d <= end:
            out.extend(self._posts_by_day.get(d, []))
            d += timedelta(days=1)
        return out

    def daily_mentions(self, end: date, days: int) -> list[int]:
        """Mention counts for the ``days`` calendar days before ``end``."""

        return [
            len(self._posts_by_day.get(end - timedelta(days=k), []))
            for k in range(days, 0, -1)
        ]

    # -- customer data --------------------------------------------------
    def flow(self, day: date) -> BrokerFlow | None:
        return self.broker_flow.get(day)

    def flow_baseline(self, day: date, days: int = 30) -> float | None:
        vals = [
            f.new_buyers
            for d, f in self.broker_flow.items()
            if day - timedelta(days=days) <= d < day
        ]
        return median(vals) if vals else None

    def reports_between(self, start: date, end: date) -> list[VictimReport]:
        return [r for r in self.reports if start <= r.day <= end]


def build_contexts(data: Dataset) -> dict[str, TickerContext]:
    bars: dict[str, list[Bar]] = defaultdict(list)
    filings: dict[str, list[Filing]] = defaultdict(list)
    posts: dict[str, list[Post]] = defaultdict(list)
    flows: dict[str, dict[date, BrokerFlow]] = defaultdict(dict)
    reports: dict[str, list[VictimReport]] = defaultdict(list)
    for b in data.bars:
        bars[b.ticker].append(b)
    for f in data.filings:
        filings[f.ticker].append(f)
    for p in data.posts:
        for t in p.tickers:
            posts[t].append(p)
    for fl in data.broker_flow:
        flows[fl.ticker][fl.day] = fl
    for r in data.reports:
        reports[r.ticker].append(r)
    return {
        t: TickerContext(t, bars[t], filings[t], posts[t], flows[t], reports[t])
        for t in sorted(bars)
    }
