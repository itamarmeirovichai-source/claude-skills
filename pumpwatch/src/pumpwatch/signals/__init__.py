"""The seven footprints a pump-and-dump has to leave.

Each signal is a pure function ``(ctx, day, cfg) -> SignalHit | None`` that may
only look at data dated on or before ``day``. That no-look-ahead rule is what
makes the backtest honest, and ``tests/test_no_lookahead.py`` enforces it.
"""

from __future__ import annotations

from typing import Callable

from ..config import Config
from ..context import TickerContext
from ..models import SignalHit
from .client import broker_flow_surge, victim_reports
from .corporate import suspicious_filings
from .market import abnormal_volume_no_news, quiet_accumulation
from .social import coordinated_promotion, hype_burst

Signal = Callable[[TickerContext, object, Config], SignalHit | None]

ALL_SIGNALS: dict[str, Signal] = {
    "S1_abnormal_volume": abnormal_volume_no_news,
    "S2_quiet_accumulation": quiet_accumulation,
    "S3_suspicious_filings": suspicious_filings,
    "S4_hype_burst": hype_burst,
    "S5_coordinated_promotion": coordinated_promotion,
    "S6_broker_flow": broker_flow_surge,
    "S7_victim_reports": victim_reports,
}

__all__ = ["ALL_SIGNALS", "Signal"]
