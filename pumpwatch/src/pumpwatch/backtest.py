"""Honest scoring of the engine against labelled historical cases.

Same discipline as a trading-bot backtest:

* The alert threshold is chosen on a **calibration** half of the cases and
  then scored on a **holdout** half it never saw (no overfitting by eye).
* A pump only counts as caught if the first alert lands **before** the
  collapse. Alerts after the crash are worth nothing to a customer.
* Every alert that is not an early catch counts against the engine: alerts on
  legitimate movers, on unlabelled tickers, and stray alerts on pump tickers
  outside their window.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from statistics import median
from typing import Iterable

from .engine import Engine, TickerRun
from .models import Alert


@dataclass(frozen=True)
class Case:
    ticker: str
    label: str  # "pump" or "legit"
    start: date  # first public promotion / news day
    end: date  # collapse day for pumps, end of the move for legit cases
    note: str = ""

    def __post_init__(self) -> None:
        if self.label not in ("pump", "legit"):
            raise ValueError(f"{self.ticker}: label must be 'pump' or 'legit', got {self.label!r}")
        if self.end < self.start:
            raise ValueError(f"{self.ticker}: end {self.end} is before start {self.start}")


def load_cases(path: str | Path) -> list[Case]:
    out: list[Case] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row.get("ticker") or row["ticker"].startswith("#"):
                continue
            out.append(
                Case(
                    row["ticker"].strip().upper(),
                    row["label"].strip().lower(),
                    date.fromisoformat(row["start"].strip()),
                    date.fromisoformat(row["end"].strip()),
                    (row.get("note") or "").strip(),
                )
            )
    return out


def split_cases(cases: Iterable[Case]) -> tuple[list[Case], list[Case]]:
    """Deterministic 50/50 split by ticker hash, stratified by label."""

    calib: list[Case] = []
    hold: list[Case] = []
    for label in ("pump", "legit"):
        group = sorted((c for c in cases if c.label == label), key=lambda c: hashlib.sha1(c.ticker.encode()).hexdigest())
        for i, c in enumerate(group):
            (calib if i % 2 == 0 else hold).append(c)
    return calib, hold


@dataclass
class CaseResult:
    case: Case
    first_alert: date | None
    lead_days: int | None

    @property
    def caught(self) -> bool:
        return self.lead_days is not None and self.lead_days > 0


@dataclass
class Metrics:
    threshold: float
    pumps: int = 0
    caught: int = 0
    legit: int = 0
    legit_flagged: int = 0
    false_alerts: int = 0
    lead_days: list[int] = field(default_factory=list)
    results: list[CaseResult] = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.caught / self.pumps if self.pumps else 0.0

    @property
    def false_per_catch(self) -> float:
        return self.false_alerts / self.caught if self.caught else float(self.false_alerts or 0)

    @property
    def median_lead(self) -> float | None:
        return median(self.lead_days) if self.lead_days else None

    def summary(self) -> dict:
        return {
            "threshold": self.threshold,
            "pumps": self.pumps,
            "caught_before_collapse": self.caught,
            "recall": round(self.recall, 3),
            "median_lead_days": self.median_lead,
            "legit_cases": self.legit,
            "legit_flagged": self.legit_flagged,
            "false_alerts": self.false_alerts,
            "false_alerts_per_catch": round(self.false_per_catch, 2),
        }


def evaluate(
    alerts: dict[str, list[Alert]],
    cases: list[Case],
    threshold: float,
    lookback_days: int = 30,
    universe: Iterable[str] | None = None,
) -> Metrics:
    """Score alerts against cases.

    ``universe`` limits which unlabelled tickers count toward false alerts;
    by default every ticker without a case counts.
    """

    m = Metrics(threshold)
    case_tickers = {c.ticker for c in cases}
    used: set[tuple[str, date]] = set()
    for c in cases:
        ticker_alerts = sorted(alerts.get(c.ticker, []), key=lambda a: a.day)
        lo = c.start - timedelta(days=lookback_days)
        if c.label == "pump":
            m.pumps += 1
            early = [a for a in ticker_alerts if lo <= a.day < c.end]
            first = early[0].day if early else None
            lead = (c.end - first).days if first else None
            m.results.append(CaseResult(c, first, lead))
            if first:
                m.caught += 1
                m.lead_days.append(lead)
                used.update((c.ticker, a.day) for a in early)
        else:
            m.legit += 1
            flagged = [a for a in ticker_alerts if lo <= a.day <= c.end + timedelta(days=lookback_days)]
            m.results.append(CaseResult(c, flagged[0].day if flagged else None, None))
            if flagged:
                m.legit_flagged += 1
    pool = set(universe) if universe is not None else set(alerts)
    pool |= case_tickers
    for t in pool:
        m.false_alerts += sum((t, a.day) not in used for a in alerts.get(t, []))
    return m


@dataclass
class BacktestReport:
    chosen_threshold: float
    calibration: Metrics
    holdout: Metrics
    overall: Metrics
    grid: list[dict]


def calibrate_and_test(
    engine: Engine,
    runs: dict[str, TickerRun],
    cases: list[Case],
    max_false_per_catch: float = 5.0,
    grid: Iterable[float] | None = None,
) -> BacktestReport:
    calib, hold = split_cases(cases)
    calib_t = {c.ticker for c in calib}
    hold_t = {c.ticker for c in hold}
    unlabelled = set(runs) - {c.ticker for c in cases}
    # Unlabelled tickers are split the same deterministic way so neither half
    # sees the other's background noise.
    ul_sorted = sorted(unlabelled, key=lambda t: hashlib.sha1(t.encode()).hexdigest())
    calib_bg = set(ul_sorted[0::2])
    hold_bg = set(ul_sorted[1::2])

    thresholds = list(grid) if grid is not None else [20 + 2.5 * i for i in range(25)]
    table: list[dict] = []
    best: tuple[float, float, float] | None = None  # (recall, -false, threshold)
    for th in thresholds:
        alerts = engine.rescore(runs, th)
        m = evaluate(alerts, calib, th, universe=calib_t | calib_bg)
        table.append(m.summary())
        if m.false_per_catch <= max_false_per_catch:
            key = (m.recall, -m.false_per_catch, th)
            if best is None or key > best:
                best = key
    chosen = best[2] if best else max(thresholds)

    alerts = engine.rescore(runs, chosen)
    return BacktestReport(
        chosen,
        evaluate(alerts, calib, chosen, universe=calib_t | calib_bg),
        evaluate(alerts, hold, chosen, universe=hold_t | hold_bg),
        evaluate(alerts, cases, chosen),
        table,
    )


def render_markdown(report: BacktestReport, data_note: str) -> str:
    def block(title: str, m: Metrics) -> str:
        s = m.summary()
        lead = "n/a" if s["median_lead_days"] is None else f"{s['median_lead_days']:.0f}"
        return (
            f"### {title}\n\n"
            f"| metric | value |\n|---|---|\n"
            f"| pumps caught before collapse | {s['caught_before_collapse']} / {s['pumps']} ({s['recall']:.0%}) |\n"
            f"| median warning (days before collapse) | {lead} |\n"
            f"| legit movers wrongly flagged | {s['legit_flagged']} / {s['legit_cases']} |\n"
            f"| false alerts | {s['false_alerts']} ({s['false_alerts_per_catch']} per catch) |\n"
        )

    rows = "\n".join(
        f"| {r.case.ticker} | {r.case.label} | {r.case.start} | {r.case.end} | "
        f"{r.first_alert or '-'} | {r.lead_days if r.lead_days is not None else '-'} |"
        for r in sorted(report.holdout.results, key=lambda r: (r.case.label, r.case.ticker))
    )
    return (
        "# PumpWatch backtest report\n\n"
        f"> **Data:** {data_note}\n"
        "> Threshold chosen on the calibration half, then frozen and scored on the holdout half.\n"
        "> Judge the engine by the **holdout** numbers only.\n\n"
        f"**Chosen alert threshold:** {report.chosen_threshold}\n\n"
        + block("Holdout (never seen during calibration)", report.holdout)
        + "\n"
        + block("Calibration", report.calibration)
        + "\n"
        + "### Holdout cases\n\n| ticker | label | start | end | first alert | lead days |\n|---|---|---|---|---|---|\n"
        + rows
        + "\n"
    )
