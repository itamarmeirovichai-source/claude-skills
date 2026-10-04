"""Turns signal hits into an explainable 0-100 risk score and alerts.

Design choices, each one tested:

* **No look-ahead.** Each day is scored only from data dated that day or earlier.
* **Convergence.** An alert needs evidence from at least ``min_families``
  independent families (market, corporate, social, client). One loud signal
  on its own is how real news looks, so it never alerts by itself.
* **Renormalisation.** Families with no data (for example no broker feed)
  are left out of the denominator instead of silently counting as zero.
* **Memory.** A hit keeps counting for ``signal_memory_days`` so that a
  volume spike and the hype that follows a day later still meet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable

from .config import Config
from .context import TickerContext, build_contexts
from .models import Alert, Dataset, DayScore, SignalHit
from .signals import ALL_SIGNALS

FAMILY_OF = {
    "S1_abnormal_volume": "market",
    "S2_quiet_accumulation": "market",
    "S3_suspicious_filings": "corporate",
    "S4_hype_burst": "social",
    "S5_coordinated_promotion": "social",
    "S6_broker_flow": "client",
    "S7_victim_reports": "client",
}


def available_signals(data: Dataset) -> set[str]:
    """Signals whose underlying data source is present at all."""

    out = {"S1_abnormal_volume", "S2_quiet_accumulation"}
    if data.filings:
        out.add("S3_suspicious_filings")
    if data.posts:
        out |= {"S4_hype_burst", "S5_coordinated_promotion"}
    if data.broker_flow:
        out.add("S6_broker_flow")
    if data.reports:
        out.add("S7_victim_reports")
    return out


@dataclass
class TickerRun:
    ticker: str
    scores: list[DayScore] = field(default_factory=list)
    alerts: list[Alert] = field(default_factory=list)


class Engine:
    def __init__(self, config: Config | None = None) -> None:
        self.cfg = config or Config()

    # ------------------------------------------------------------------
    def score_ticker(
        self, ctx: TickerContext, available: set[str], days: Iterable[date] | None = None
    ) -> list[DayScore]:
        cfg = self.cfg
        active = [name for name in ALL_SIGNALS if name in available]
        denom = sum(cfg.weights.get(n, 0.0) for n in active) or 1.0
        recent: list[SignalHit] = []
        out: list[DayScore] = []
        for day in days if days is not None else ctx.days:
            for name in active:
                hit = ALL_SIGNALS[name](ctx, day, cfg)
                if hit is not None:
                    recent.append(hit)
            horizon = day - timedelta(days=cfg.signal_memory_days - 1)
            recent = [h for h in recent if h.day >= horizon]
            best: dict[str, SignalHit] = {}
            for h in recent:
                if h.signal not in best or h.strength > best[h.signal].strength:
                    best[h.signal] = h
            score = 100.0 * sum(cfg.weights.get(n, 0.0) * h.strength for n, h in best.items()) / denom
            out.append(DayScore(ctx.ticker, day, round(score, 2), sorted(best.values(), key=lambda h: h.signal)))
        return out

    def alerts_from_scores(self, scores: list[DayScore]) -> list[Alert]:
        cfg = self.cfg
        alerts: list[Alert] = []
        last: date | None = None
        for s in scores:
            if s.score < cfg.alert_threshold or len(s.families) < cfg.min_families:
                continue
            if last is not None and (s.day - last).days < cfg.cooldown_days:
                continue
            last = s.day
            alerts.append(
                Alert(
                    s.ticker,
                    s.day,
                    s.score,
                    tuple(sorted(s.families)),
                    tuple(f"[{h.signal}] {h.evidence}" for h in s.hits),
                )
            )
        return alerts

    # ------------------------------------------------------------------
    def run(self, data: Dataset, tickers: Iterable[str] | None = None) -> dict[str, TickerRun]:
        contexts = build_contexts(data)
        available = available_signals(data)
        wanted = set(tickers) if tickers is not None else None
        results: dict[str, TickerRun] = {}
        for t, ctx in contexts.items():
            if wanted is not None and t not in wanted:
                continue
            scores = self.score_ticker(ctx, available)
            results[t] = TickerRun(t, scores, self.alerts_from_scores(scores))
        return results

    def rescore(self, runs: dict[str, TickerRun], threshold: float) -> dict[str, list[Alert]]:
        """Re-derive alerts at a different threshold without recomputing signals."""

        saved = self.cfg
        self.cfg = saved.with_(alert_threshold=threshold)
        try:
            return {t: self.alerts_from_scores(r.scores) for t, r in runs.items()}
        finally:
            self.cfg = saved
