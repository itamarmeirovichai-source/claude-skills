"""Small builders shared by the QA test files (test_qa_*.py).

Kept separate from any conftest so the QA suite never collides with the
core test fixtures.
"""

from __future__ import annotations

from datetime import date, timedelta

from pumpwatch.models import Bar, BrokerFlow, Dataset, Filing, Post, VictimReport

D0 = date(2026, 1, 5)  # a Monday


def weekdays(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def flat_bars(ticker: str, days: list[date], close: float = 1.0, volume: float = 10_000) -> list[Bar]:
    return [Bar(ticker, d, close, close, close, close, volume) for d in days]


def pump_dataset(ticker: str = "PUMP", n_days: int = 90) -> Dataset:
    """A synthetic pump that touches every signal family.

    * 60 quiet days, then a 20-session steady climb (S2), a volume spike
      with no news (S1), a dilutive filing (S3), a hype burst of
      copy-paste posts (S4, S5), new-buyer surge (S6) and a victim report (S7),
      then a collapse.
    """

    days = weekdays(D0, n_days)
    bars: list[Bar] = []
    price = 1.0
    for i, d in enumerate(days):
        vol = 10_000.0
        if 55 <= i < 75:
            price *= 1.03 if i % 4 else 0.995
            vol = 30_000.0
        if i == 75:
            vol = 1_000_000.0
            price *= 1.2
        if i >= 80:
            price *= 0.6
        bars.append(Bar(ticker, d, price, price, price, price, vol))
    spike = days[75]
    template = "Huge news coming for {t} get in now before it explodes, this is the next tesla 🚀🚀"
    posts = [
        Post("telegram", f"acct{k}", spike, template.format(t=f"${ticker}"), (ticker,)) for k in range(8)
    ] + [Post("reddit", "calm", days[10], f"anyone looked at ${ticker}?", (ticker,))]
    filings = [
        Filing(ticker, days[2], "10-Q", "quarterly report"),
        Filing(ticker, days[70], "S-1", "registration of shares"),
    ]
    flows = [BrokerFlow(ticker, d, 2, 0) for d in days[40:75]] + [BrokerFlow(ticker, spike, 80, 50)]
    reports = [VictimReport(ticker, days[78], "lost money")]
    return Dataset(bars, filings, posts, flows, reports)


def truncate(data: Dataset, last_day: date) -> Dataset:
    """Drop every record dated after ``last_day``."""

    return Dataset(
        [b for b in data.bars if b.day <= last_day],
        [f for f in data.filings if f.day <= last_day],
        [p for p in data.posts if p.day <= last_day],
        [fl for fl in data.broker_flow if fl.day <= last_day],
        [r for r in data.reports if r.day <= last_day],
    )
