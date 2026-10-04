"""Social footprints: S4 hype burst, S5 coordinated copy-paste promotion."""

from __future__ import annotations

from datetime import date, timedelta
from statistics import mean

from ..config import Config
from ..context import TickerContext
from ..models import SignalHit
from ..text import hype_score, near_duplicate_clusters


def hype_burst(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S4: mentions jump far above normal and the messages read like promotion."""

    today = ctx.posts_on(day)
    n = len(today)
    if n < cfg.mention_min_count:
        return None
    history = ctx.daily_mentions(day, cfg.mention_baseline_days)
    base = mean(history) if history else 0.0
    ratio = n / base if base > 0 else float("inf")
    if ratio < cfg.mention_ratio_trigger:
        return None
    hype = mean(hype_score(p.text) for p in today)
    if hype < cfg.hype_min_avg:
        return None
    ratio_part = 1.0 if ratio == float("inf") else min(1.0, ratio / (cfg.mention_ratio_trigger * 4))
    strength = min(1.0, 0.5 * ratio_part + 0.5 * hype)
    ratio_txt = "from ~0" if ratio == float("inf") else f"{ratio:.1f}x the {cfg.mention_baseline_days}-day average"
    return SignalHit(
        "S4_hype_burst",
        "social",
        ctx.ticker,
        day,
        round(strength, 3),
        f"{n} mentions today ({ratio_txt}), average hype score {hype:.2f}",
    )


def coordinated_promotion(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S5: near-identical messages pushed by several different accounts."""

    start = day - timedelta(days=cfg.coord_window_days - 1)
    posts = ctx.posts_between(start, day)
    if len(posts) < cfg.coord_min_authors:
        return None
    items = [(p.author, p.text) for p in posts]
    clusters = near_duplicate_clusters(items, threshold=cfg.coord_similarity)
    best = None
    for c in clusters:
        authors = {posts[i].author for i in c}
        sources = {posts[i].source for i in c}
        if len(authors) >= cfg.coord_min_authors and (best is None or len(authors) > best[0]):
            best = (len(authors), len(c), sources)
    if best is None:
        return None
    n_authors, n_msgs, sources = best
    strength = min(1.0, 0.3 + 0.1 * n_authors + (0.1 if len(sources) > 1 else 0.0))
    return SignalHit(
        "S5_coordinated_promotion",
        "social",
        ctx.ticker,
        day,
        round(strength, 3),
        f"{n_msgs} near-identical messages from {n_authors} different accounts across "
        f"{', '.join(sorted(sources))} in {cfg.coord_window_days} day(s)",
    )
