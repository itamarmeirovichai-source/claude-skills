"""Market footprints: S1 abnormal volume without news, S2 quiet accumulation."""

from __future__ import annotations

import math
from datetime import date, timedelta
from statistics import median

from ..config import NEWS_FORMS, Config
from ..context import TickerContext
from ..models import SignalHit


def abnormal_volume_no_news(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S1: dollar volume many times its normal level with no filing to explain it."""

    bar = ctx.bar(day)
    if bar is None:
        return None
    history = ctx.bars_before(day, cfg.vol_lookback)
    if len(history) < cfg.vol_min_history:
        return None
    base = median(b.dollar_volume for b in history)
    if base <= 0:
        base = 1.0
    ratio = bar.dollar_volume / base
    if ratio < cfg.vol_ratio_trigger:
        return None
    window = timedelta(days=cfg.news_window_days)
    news = [f for f in ctx.filings_between(day - window, day) if f.form.upper() in NEWS_FORMS]
    if news:
        return None
    strength = min(1.0, math.log(ratio) / math.log(cfg.vol_ratio_full))
    return SignalHit(
        "S1_abnormal_volume",
        "market",
        ctx.ticker,
        day,
        round(strength, 3),
        f"dollar volume {ratio:.1f}x its {len(history)}-day median, no news filing within "
        f"{cfg.news_window_days} day(s)",
    )


def quiet_accumulation(ctx: TickerContext, day: date, cfg: Config) -> SignalHit | None:
    """S2: steady climb on rising volume without any single big jump.

    This is what the promoters' own buying looks like before the public pitch.
    """

    window = ctx.bars_before(day, cfg.acc_window)
    today = ctx.bar(day)
    if today is None or len(window) < cfg.acc_window:
        return None
    seq = window + [today]
    first, last = seq[0].close, seq[-1].close
    if first <= 0:
        return None
    gain = last / first - 1.0
    if gain < cfg.acc_min_gain:
        return None
    rets = [seq[i].close / seq[i - 1].close - 1.0 for i in range(1, len(seq)) if seq[i - 1].close > 0]
    if not rets or max(rets) > cfg.acc_max_single_day:
        return None
    up_share = sum(r > 0 for r in rets) / len(rets)
    if up_share < cfg.acc_min_up_share:
        return None
    prior = ctx.bars_before(window[0].day, cfg.vol_lookback)
    if len(prior) < cfg.vol_min_history:
        return None
    prior_vol = median(b.volume for b in prior) or 1.0
    recent_vol = median(b.volume for b in seq)
    vol_ratio = recent_vol / prior_vol
    if vol_ratio < cfg.acc_min_volume_ratio:
        return None
    strength = min(1.0, 0.4 * min(gain / 1.0, 1.0) + 0.3 * up_share + 0.3 * min(vol_ratio / 5.0, 1.0))
    return SignalHit(
        "S2_quiet_accumulation",
        "market",
        ctx.ticker,
        day,
        round(strength, 3),
        f"+{gain:.0%} over {cfg.acc_window} sessions, {up_share:.0%} up days, largest day "
        f"{max(rets):+.0%}, volume {vol_ratio:.1f}x prior median",
    )
