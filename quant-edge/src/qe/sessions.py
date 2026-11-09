"""qe.sessions — session templates, trading-day ids, half days, roll weeks and firm flat-by times.

STUB written by Department D (engine) on 2026-11-03 so that `qe.engine` can tag bars. Department C (Calendar and
Clock Keeper, brief `briefs/C-data-run.md` §2) OWNS this module and replaces the internals; the public names below
are the interface the engine calls, keep them stable:

    TZ_NY, REOPEN_NY_MINUTE, FLAT_BY, TEMPLATES
    day_table(start, end, root)      -> one row per trading day (CMES session) with RTH window, half-day, roll-week flags
    tag_minutes(ts_utc, root)        -> per-bar tags: ny_minute, tday_minute, trading_day, in_session, is_rth, is_half_day,
                                        is_roll_week, has_rth, rth_close_minute, session_close_minute
    tag_days(dates, root)            -> per-day tags for daily bars
    flat_by_tminute(firm, days)      -> firm deadline per trading day in minutes since the 18:00 ET reopen
    is_roll_week(dates, roll_months) -> Mon–Fri of the week holding the third Friday of a roll month, plus the next Monday
    ny_minute(ts_utc), tday_minute(ny_minute)

Conventions fixed here (also in `src/qe/engine/CONVENTIONS.md`):
  * Bars are stamped by OPEN time in UTC. `ny_minute` is the New York wall-clock minute of the bar open (09:30 ET = 570
    whatever the DST state), `tday_minute` counts minutes since the 18:00 ET reopen (18:00 ET = 0, 09:30 ET = 930,
    16:10 ET = 1330, 17:00 ET = 1380), so a comparison against a deadline is monotone inside one trading day.
  * The trading day is the CMES session of `exchange_calendars` (label = the calendar date of the close): it opens at
    18:00 ET the evening before (17:00 CT) — an overnight-session hold is inside ONE trading day, a hold across the
    17:00 ET close is not (briefs/00-common.md, firm structure 1).
  * The library's CMES session runs 17:00 CT to 17:00 CT (24 h, no maintenance break); this stub overrides the close
    to 17:00 ET (16:00 CT) on normal days, so bars at 17:00–17:59 ET are `in_session=False`. Short sessions keep the
    library's close (13:00 ET on the day after Thanksgiving, etc.).
  * RTH = the XNYS session of the same calendar date: 09:30 ET ≤ open < close (16:00 ET, 13:00 ET on early closes), so
    a full RTH day has 390 one-minute bars and a half day 210 (inherited loader_spec rule 2). A trading day whose
    calendar date has no XNYS session (the "CME-only sessions") has `has_rth=False` and `is_rth=False` everywhere.
  * is_half_day = XNYS early close on the trading-day date OR a CMES session shorter than 23 h.
  * Roll week (equity index): Mon–Fri of the week holding the third Friday of Mar/Jun/Sep/Dec plus the following Monday
    (re-implementation of the inherited `roll_excluded`, briefs/inherited-code-reusable.md), keyed by trading-day date.
  * Flat-by times (FLAT_BY) are the clauses quoted in briefs/00-common.md / inherited-firms.md dated 2026-10-11:
    Topstep 15:10 CT, Bulenox 15:59 CT, MFFU 16:10 ET, Tradeify and Lucid 16:45 ET; FTMO intraday = the CE(S)T day end
    (23:55 Europe/Prague used here). On a half day the deadline is min(firm deadline, RTH early close) — conservative
    until the Rules Keeper verifies each firm's early-close clause.

TODO for Department C (in priority order):
  1. Per-root templates beyond the equity-index family (CL, GC, 6E, ZN, ...: Globex hours, maintenance breaks,
     settlement minutes, listing dates, roll months); currently every root falls back to the ES template with a warning.
  2. The real CME equity-index halts (15:15–15:30 CT on the legacy schedule; 16:00–17:00 CT maintenance) and the
     exact early-close times per holiday (12:15 CT equity index vs the library's 12:00 CT) — verify against the CME
     holiday calendar pages with fetch dates; replace `half_day_session_close_minute`.
  3. The list of CME-only sessions (44 in the inherited count) and the rule for them (drop for RTH strategies).
  4. A roll-calendar scaffold per root from Databento `definition` (expiry, first notice) and the `.v.0` flip-back rule;
     `is_roll_week` is the inherited third-Friday approximation only.
  5. FTMO: the trading day ends at 00:00 CE(S)T (Prague); the daily-loss reference balance is taken there; make the
     flat-by and the day boundary for the FTMO structures tz-exact including the two weeks a year when EU and US DST differ.
  6. Verify each FLAT_BY entry against the firm page (Rules Keeper matrix, `economics/firms-matrix-2026-11.md`) and
     each firm's early-close deadline; add Lucid/Tradeify minimum hold (5 s / 10 s) metadata here if the engine needs it.
  7. The required tests: 2024-07-03 and 2024-11-29 have 210 RTH bars; 2024-03-10 DST day; the 17:59 vs 18:01 ET
     trading-day boundary (tests/test_engine_sessions.py covers these on the stub; keep them green).
  8. One New York index for everything; the outcome-free clock check per dataset (QA, not here).
"""
from __future__ import annotations

import functools
import warnings
from dataclasses import dataclass
from datetime import time
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

import exchange_calendars as xc

TZ_NY = "America/New_York"
TZ_CT = "America/Chicago"
REOPEN_NY_MINUTE = 18 * 60            # 1080: the futures trading day starts at the 18:00 ET Globex reopen
SESSION_CLOSE_NY_MINUTE = 17 * 60     # 1020: 17:00 ET (16:00 CT) close of the equity-index Globex session
MINUTES_PER_DAY = 1440


@dataclass(frozen=True)
class SessionTemplate:
    root: str
    calendar: str = "CMES"                 # trading-day calendar (sessions start at the 18:00 ET reopen)
    rth_calendar: str = "XNYS"             # RTH window source (09:30–16:00 ET; early closes 13:00 ET)
    roll_months: Tuple[int, ...] = (3, 6, 9, 12)
    rth_open_minute: int = 9 * 60 + 30
    rth_close_minute: int = 16 * 60
    half_day_session_close_minute: int = 13 * 60 + 15   # TODO(C) 12:15 CT equity-index early close, verify per holiday
    session_close_minute: int = SESSION_CLOSE_NY_MINUTE


EQUITY_INDEX_ROOTS = ("ES", "MES", "NQ", "MNQ", "RTY", "M2K", "YM", "MYM")
TEMPLATES: Dict[str, SessionTemplate] = {r: SessionTemplate(r) for r in EQUITY_INDEX_ROOTS}

# firm -> (local wall-clock deadline, tz). Sources: briefs/00-common.md and briefs/inherited-firms.md (clauses dated 2026-10-11).
FLAT_BY: Dict[str, Tuple[time, str]] = {
    "topstep": (time(15, 10), TZ_CT),
    "bulenox": (time(15, 59), TZ_CT),
    "mffu": (time(16, 10), TZ_NY),
    "tradeify": (time(16, 45), TZ_NY),
    "lucid": (time(16, 45), TZ_NY),
    "ftmo_intraday": (time(23, 55), "Europe/Prague"),   # TODO(C) exact CE(S)T day-end clause
}


def template(root: str) -> SessionTemplate:
    if root in TEMPLATES:
        return TEMPLATES[root]
    warnings.warn(f"qe.sessions: no session template for root {root!r}; using the ES equity-index template (TODO Department C)")
    return SessionTemplate(root)


@functools.lru_cache(maxsize=16)
def _calendar(name: str, start: str, end: str):
    return xc.get_calendar(name, start=start, end=end)


def _ns(x) -> np.ndarray:
    """UTC epoch nanoseconds (int64) of a tz-aware DatetimeIndex/Series or naive-UTC datetimes."""
    idx = pd.DatetimeIndex(x)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    # pandas >= 3 parses strings to datetime64[us]; every comparison here is in nanoseconds
    return idx.tz_convert("UTC").tz_localize(None).as_unit("ns").asi8


def ny_minute(ts_utc) -> np.ndarray:
    """New York wall-clock minute of day (0..1439) of each UTC timestamp; DST-aware."""
    idx = pd.DatetimeIndex(ts_utc)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    ny = idx.tz_convert(TZ_NY)
    return (ny.hour * 60 + ny.minute).to_numpy(dtype=np.int64)


def tday_minute(ny_min) -> np.ndarray:
    """Minutes since the 18:00 ET reopen (0..1439)."""
    return (np.asarray(ny_min, dtype=np.int64) - REOPEN_NY_MINUTE) % MINUTES_PER_DAY


def is_roll_week(dates, roll_months: Iterable[int] = (3, 6, 9, 12)) -> np.ndarray:
    """True for Mon–Fri of the week holding the third Friday of a roll month and for the following Monday."""
    d = pd.DatetimeIndex(pd.to_datetime(dates)).normalize().as_unit("ns")
    if len(d) == 0:
        return np.zeros(0, dtype=bool)
    excluded = set()
    for y in range(d.min().year, d.max().year + 1):
        for m in roll_months:
            first = pd.Timestamp(y, m, 1)
            fri3 = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
            mon = fri3 - pd.Timedelta(days=4)
            for i in range(5):
                excluded.add((mon + pd.Timedelta(days=i)).value)
            excluded.add((fri3 + pd.Timedelta(days=3)).value)
    return np.fromiter((v in excluded for v in d.asi8), dtype=bool, count=len(d))


def day_table(start, end, root: str = "ES") -> pd.DataFrame:
    """One row per trading day (CMES session label) between `start` and `end` (dates, inclusive).

    Columns: session_open_utc, session_close_utc, has_rth, rth_open_utc, rth_close_utc, is_half_day, is_roll_week,
    rth_open_minute, rth_close_minute, session_close_minute (NY minutes), tday_close_minute (minutes since the reopen).
    """
    tpl = template(root)
    start = pd.Timestamp(start).normalize()
    end = pd.Timestamp(end).normalize()
    pad_start = (start - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    pad_end = (end + pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    cme = _calendar(tpl.calendar, pad_start, pad_end).schedule
    nyse = _calendar(tpl.rth_calendar, pad_start, pad_end).schedule
    cme = cme.loc[(cme.index >= start) & (cme.index <= end)]
    out = pd.DataFrame(index=cme.index.rename("trading_day"))
    out["session_open_utc"] = cme["open"].dt.tz_convert("UTC")
    lib_close = cme["close"].dt.tz_convert("UTC")
    short = (lib_close - out["session_open_utc"]) < pd.Timedelta(hours=23)
    # normal days: override the library's 17:00 CT close with the real 16:00 CT (17:00 ET) close
    normal_close = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(TZ_NY) + pd.Timedelta(minutes=tpl.session_close_minute)
                                     for d in out.index]).tz_convert("UTC")
    out["session_close_utc"] = np.where(short, lib_close, normal_close)
    out["session_close_utc"] = pd.to_datetime(out["session_close_utc"], utc=True)
    has_rth = out.index.isin(nyse.index)
    out["has_rth"] = has_rth
    ro = nyse["open"].reindex(out.index)
    rc = nyse["close"].reindex(out.index)
    out["rth_open_utc"] = ro.dt.tz_convert("UTC")
    out["rth_close_utc"] = rc.dt.tz_convert("UTC")
    ny_close = rc.dt.tz_convert(TZ_NY)
    rth_close_minute = (ny_close.dt.hour * 60 + ny_close.dt.minute).fillna(tpl.rth_close_minute).astype(int)
    early = has_rth & (rth_close_minute.to_numpy() < tpl.rth_close_minute)
    out["is_half_day"] = early | short.to_numpy()
    out["rth_open_minute"] = tpl.rth_open_minute
    out["rth_close_minute"] = rth_close_minute.to_numpy()
    close_ny = out["session_close_utc"].dt.tz_convert(TZ_NY)
    sess_close_min = (close_ny.dt.hour * 60 + close_ny.dt.minute).to_numpy()
    # an XNYS early close with a library-normal CMES session: close the futures session at the template's half-day minute
    sess_close_min = np.where(early & ~short.to_numpy(), tpl.half_day_session_close_minute, sess_close_min)
    out["session_close_minute"] = sess_close_min.astype(int)
    out["tday_close_minute"] = tday_minute(out["session_close_minute"].to_numpy())
    out["is_roll_week"] = is_roll_week(out.index, tpl.roll_months)
    return out


def tag_minutes(ts_utc, root: str = "ES") -> pd.DataFrame:
    """Per-bar session tags for UTC bar-open timestamps (any order; output aligned to the input order)."""
    idx = pd.DatetimeIndex(ts_utc)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    n = len(idx)
    if n == 0:
        raise ValueError("tag_minutes: empty timestamp index")
    days = day_table(idx.min().tz_convert(TZ_NY).normalize().tz_localize(None) - pd.Timedelta(days=3),
                     idx.max().tz_convert(TZ_NY).normalize().tz_localize(None) + pd.Timedelta(days=3), root)
    ts = _ns(idx)
    opens = days["session_open_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
    closes = days["session_close_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)
    k = np.searchsorted(opens, ts, side="right") - 1
    valid = k >= 0
    k_safe = np.clip(k, 0, len(days) - 1)
    in_session = valid & (ts < closes[k_safe])
    trading_day = days.index.to_numpy()[k_safe]
    # bars before the first session open in the table belong to no trading day
    out = pd.DataFrame(index=np.arange(n))
    out["ny_minute"] = ny_minute(idx)
    out["tday_minute"] = tday_minute(out["ny_minute"].to_numpy())
    out["trading_day"] = pd.DatetimeIndex(trading_day)
    out["in_session"] = in_session
    has_rth = days["has_rth"].to_numpy()[k_safe] & valid
    ro = days["rth_open_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)[k_safe]
    rc = days["rth_close_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)[k_safe]
    with np.errstate(invalid="ignore"):
        out["is_rth"] = has_rth & (ts >= ro) & (ts < rc)
    out["has_rth"] = has_rth
    out["is_half_day"] = days["is_half_day"].to_numpy()[k_safe] & valid
    out["is_roll_week"] = days["is_roll_week"].to_numpy()[k_safe] & valid
    out["rth_close_minute"] = days["rth_close_minute"].to_numpy()[k_safe]
    out["session_close_minute"] = days["session_close_minute"].to_numpy()[k_safe]
    out["tday_close_minute"] = days["tday_close_minute"].to_numpy()[k_safe]
    return out


def tag_days(dates, root: str = "ES") -> pd.DataFrame:
    """Per-day tags for daily bars (dates = trading-day labels)."""
    d = pd.DatetimeIndex(pd.to_datetime(dates)).normalize().as_unit("ns")
    tpl = template(root)
    days = day_table(d.min() - pd.Timedelta(days=3), d.max() + pd.Timedelta(days=3), root)
    out = pd.DataFrame({"trading_day": d})
    out["is_half_day"] = days["is_half_day"].reindex(d).fillna(False).to_numpy(dtype=bool)
    out["has_rth"] = days["has_rth"].reindex(d).fillna(False).to_numpy(dtype=bool)
    out["is_roll_week"] = is_roll_week(d, tpl.roll_months)
    out["is_calendar_session"] = d.isin(days.index)
    return out


def flat_by_tminute(firm: str, days: pd.DataFrame) -> np.ndarray:
    """The firm's flat-by deadline per trading day, in minutes since the 18:00 ET reopen (same units as tday_minute).

    `days` is a day_table (or any frame indexed by trading day with is_half_day and rth_close_minute). On a half day the
    deadline is min(firm deadline, RTH early close). FLAT_BY entries in a non-US tz are converted per date (DST-exact).
    """
    if firm not in FLAT_BY:
        raise KeyError(f"unknown firm {firm!r}; known: {sorted(FLAT_BY)}")
    t, tz = FLAT_BY[firm]
    idx = pd.DatetimeIndex(days.index)
    local = pd.DatetimeIndex([pd.Timestamp.combine(d, t) for d in idx]).tz_localize(tz, ambiguous=True, nonexistent="shift_forward")
    ny = local.tz_convert(TZ_NY)
    ny_min = (ny.hour * 60 + ny.minute).to_numpy(dtype=np.int64)
    dl = tday_minute(ny_min)
    half = days["is_half_day"].to_numpy(dtype=bool)
    rth_close = tday_minute(days["rth_close_minute"].to_numpy())
    return np.where(half, np.minimum(dl, rth_close), dl).astype(np.int64)
