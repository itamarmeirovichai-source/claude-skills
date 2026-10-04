"""Corporate footprint: S3 dilutive or reshaping filings ahead of a move."""

from __future__ import annotations

from datetime import date, timedelta

from ..config import DILUTION_FORMS, RED_FLAG_TITLE_WORDS, Config
from ..context import TickerContext
from ..models import SignalHit


def suspicious_filings(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S3: new shares registered, a name or control change, or a dormant shell waking up."""

    start = day - timedelta(days=cfg.filing_lookback_days)
    recent = ctx.filings_between(start, day)
    if not recent:
        return None
    reasons: list[str] = []
    score = 0.0

    dilutive = [f for f in recent if f.form.upper() in DILUTION_FORMS]
    if dilutive:
        forms = sorted({f.form.upper() for f in dilutive})
        reasons.append(f"share registration/issuance filings: {', '.join(forms)}")
        score += min(0.5, 0.25 * len(dilutive))

    flagged = []
    for f in recent:
        title = f" {f.title.lower()} "
        hits = [w.strip() for w in RED_FLAG_TITLE_WORDS if w in title]
        if hits:
            flagged.append((f, hits))
    if flagged:
        words = sorted({w for _, hs in flagged for w in hs})
        reasons.append(f"red-flag events: {', '.join(words)}")
        score += min(0.4, 0.2 * len(flagged))

    first_recent = recent[0]
    earlier = [f for f in ctx.filings_before(first_recent.day)]
    if earlier:
        gap = (first_recent.day - earlier[-1].day).days
        if gap >= cfg.dormant_gap_days:
            reasons.append(f"filings resumed after {gap} days of silence")
            score += 0.4

    if not reasons:
        return None
    return SignalHit(
        "S3_suspicious_filings",
        "corporate",
        ctx.ticker,
        day,
        round(min(1.0, score), 3),
        "; ".join(reasons) + f" (last {cfg.filing_lookback_days} days)",
    )
