"""Customer-owned footprints: S6 broker flow surge, S7 victim reports.

These only fire when a customer (broker, app) supplies the data. Without it
the scoring renormalises over the signals that are available, so the engine
still works on public data alone.
"""

from __future__ import annotations

from datetime import date, timedelta

from ..config import Config
from ..context import TickerContext
from ..models import SignalHit


def broker_flow_surge(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S6: many new, small buyers piling into the same micro-cap."""

    flow = ctx.flow(day)
    if flow is None or flow.new_buyers < cfg.flow_min_new_buyers:
        return None
    base = ctx.flow_baseline(day)
    ratio = flow.new_buyers / base if base else float("inf")
    if ratio < cfg.flow_ratio_trigger:
        return None
    first_timers = flow.first_time_microcap_buyers / flow.new_buyers if flow.new_buyers else 0.0
    ratio_part = 1.0 if ratio == float("inf") else min(1.0, ratio / (cfg.flow_ratio_trigger * 4))
    strength = min(1.0, 0.6 * ratio_part + 0.4 * first_timers)
    ratio_txt = "from ~0" if ratio == float("inf") else f"{ratio:.1f}x baseline"
    return SignalHit(
        "S6_broker_flow",
        "client",
        ctx.ticker,
        day,
        round(strength, 3),
        f"{flow.new_buyers} new buyers ({ratio_txt}), {first_timers:.0%} never bought a micro-cap before",
    )


def victim_reports(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S7: consent-based user reports naming this ticker."""

    reports = ctx.reports_between(day - timedelta(days=cfg.report_window_days - 1), day)
    if not reports:
        return None
    strength = min(1.0, 0.5 + 0.1 * (len(reports) - 1))
    return SignalHit(
        "S7_victim_reports",
        "client",
        ctx.ticker,
        day,
        round(strength, 3),
        f"{len(reports)} user report(s) in the last {cfg.report_window_days} days",
    )
