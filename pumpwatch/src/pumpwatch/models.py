"""Plain data records shared by every part of the engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Bar:
    """One trading day for one ticker."""

    ticker: str
    day: date
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def dollar_volume(self) -> float:
        return self.close * self.volume


@dataclass(frozen=True)
class Filing:
    """A public company filing or corporate event (EDGAR, OTC Markets, press)."""

    ticker: str
    day: date
    form: str
    title: str = ""


@dataclass(frozen=True)
class Post:
    """A public social-media message. Authors are stored as opaque ids only."""

    source: str
    author: str
    day: date
    text: str
    tickers: tuple[str, ...] = ()


@dataclass(frozen=True)
class BrokerFlow:
    """Customer-owned aggregate buying data a broker can share under contract."""

    ticker: str
    day: date
    new_buyers: int
    first_time_microcap_buyers: int = 0


@dataclass(frozen=True)
class VictimReport:
    """A consent-based report (for example a screenshot submitted by a user)."""

    ticker: str
    day: date
    note: str = ""


@dataclass(frozen=True)
class SignalHit:
    """One signal firing for one ticker on one day, with its evidence."""

    signal: str
    family: str
    ticker: str
    day: date
    strength: float
    evidence: str


@dataclass
class DayScore:
    ticker: str
    day: date
    score: float
    hits: list[SignalHit] = field(default_factory=list)

    @property
    def families(self) -> set[str]:
        return {h.family for h in self.hits}


@dataclass(frozen=True)
class Alert:
    ticker: str
    day: date
    score: float
    families: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "day": self.day.isoformat(),
            "score": round(self.score, 1),
            "families": list(self.families),
            "reasons": list(self.reasons),
        }


@dataclass
class Dataset:
    """Everything the engine knows, grouped by ticker on demand."""

    bars: list[Bar] = field(default_factory=list)
    filings: list[Filing] = field(default_factory=list)
    posts: list[Post] = field(default_factory=list)
    broker_flow: list[BrokerFlow] = field(default_factory=list)
    reports: list[VictimReport] = field(default_factory=list)

    def tickers(self) -> list[str]:
        return sorted({b.ticker for b in self.bars})

    def extend(self, other: "Dataset") -> None:
        self.bars.extend(other.bars)
        self.filings.extend(other.filings)
        self.posts.extend(other.posts)
        self.broker_flow.extend(other.broker_flow)
        self.reports.extend(other.reports)
