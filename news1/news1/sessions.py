"""Trading-day and time-window helpers, all in US Eastern Time."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from . import config

ET = ZoneInfo("America/New_York")

# Best-effort list of full-day NYSE closures. The final check is at settlement:
# a day with no daily bar is void whatever this list says.
HOLIDAYS = {
    date(2026, 11, 26), date(2026, 12, 25),
    date(2027, 1, 1), date(2027, 1, 18), date(2027, 2, 15), date(2027, 3, 26),
    date(2027, 5, 31), date(2027, 6, 18), date(2027, 7, 5), date(2027, 9, 6),
    date(2027, 11, 25), date(2027, 12, 24),
}  # fmt: skip


def is_trading_day(day: date) -> bool:
    return day.weekday() < 5 and day not in HOLIDAYS


def prev_trading_day(day: date) -> date:
    day -= timedelta(days=1)
    while not is_trading_day(day):
        day -= timedelta(days=1)
    return day


def at_et(day: date, hour_minute: tuple[int, int]) -> datetime:
    return datetime(day.year, day.month, day.day, *hour_minute, tzinfo=ET)


def window(day: date) -> tuple[datetime, datetime]:
    """News window for a signal day: previous close (16:00 ET) to 09:00 ET."""
    return at_et(prev_trading_day(day), config.WINDOW_START), at_et(day, config.WINDOW_END)
