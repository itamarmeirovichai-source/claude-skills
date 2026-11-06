"""qe.calendars — the heavy calendar logic behind qe.sessions (Department C, Calendar and Clock Keeper, 2026-11-04).

Contents
  * SessionTemplate per CME root (37 Databento roots in 8 groups): Globex open/close in New York minutes, the daily
    halt/pause, the RTH window (XNYS for the equity-index family, the legacy pit hours otherwise), settlement minute,
    roll months, expiry rule key, listing date (metadata), tick size and point value.
  * exchange_calendars wrappers (CMES = trading days, XNYS = RTH days), early closes, CME-only sessions.
  * day_table(start, end, root): one row per trading day with every window in UTC and in New York minutes.
  * ny_index(start, end, root): the UTC index of every in-session minute — "one New York index for everything".
  * DST transition tables for America/New_York and Europe/Prague; the FTMO day boundary (00:00 Europe/Prague).
  * roll scaffold per root: contract months, rule-based expiry / first notice / estimated roll, and the `.v.0`
    flip-back rule (`front_by_volume`).

Conventions (unchanged from the Department D stub; also in src/qe/engine/CONVENTIONS.md):
  * bars are stamped by OPEN time in UTC; `ny_minute` is the New York wall-clock minute (DST-aware); `tday_minute`
    counts minutes since the 18:00 ET reopen (18:00 ET = 0, 09:30 ET = 930, 17:00 ET = 1380);
  * the trading day is the CMES session of exchange_calendars (label = calendar date of the close) and starts at the
    18:00 ET reopen for every root (the firm's trading day); grains open inside it at 20:00 ET, livestock at 09:30 ET;
  * `in_session` is the open..close window minus any PAUSE longer than 30 minutes (grains 08:45–09:30 ET); the 15-minute
    equity-index halt (16:15–16:30 ET) is flagged `in_halt` but stays `in_session` (23 h = 1,380 minutes per full day);
  * early-close days: the library's CMES early close (13:00 ET = 12:00 CT) is used for every group. CME's published
    early closes differ by group (12:15 CT equity/rates/FX, 12:45 CT energy/metals, 12:05 CT grains/livestock, from
    memory; cmegroup.com answers 403 from this session, so they are NOT verified) — recorded as a TODO, conservative
    side: the engine closes earlier than the exchange would.

Everything here is outcome-free: no price is read.
"""
from __future__ import annotations

import functools
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import exchange_calendars as xc

TZ_NY = "America/New_York"
TZ_CT = "America/Chicago"
TZ_PRAGUE = "Europe/Prague"
TZ_LONDON = "Europe/London"
REOPEN_NY_MINUTE = 18 * 60            # 1080: the futures trading day starts at the 18:00 ET Globex reopen
SESSION_CLOSE_NY_MINUTE = 17 * 60     # 1020: 17:00 ET (16:00 CT) Globex close of the 23-hour products
MINUTES_PER_DAY = 1440
HALF_DAY_CLOSE_NY_MINUTE = 13 * 60    # 780: library CMES early close (12:00 CT); CME group-specific minutes unverified

M = lambda h, m=0: h * 60 + m  # noqa: E731


@dataclass(frozen=True)
class SessionTemplate:
    root: str
    group: str
    exchange: str
    name: str
    globex_open_minute: int = REOPEN_NY_MINUTE          # NY minute on the PREVIOUS calendar day (day_only=False)
    globex_close_minute: int = SESSION_CLOSE_NY_MINUTE  # NY minute on the trading-day date
    day_only: bool = False                               # True: the session opens on the trading-day date (livestock)
    pauses: Tuple[Tuple[int, int], ...] = ()             # NY-minute windows that are OUT of session (grains 08:45–09:30)
    halts: Tuple[Tuple[int, int], ...] = ()              # short halts flagged in_halt (equity 16:15–16:30 ET)
    rth_source: str = "template"                         # "XNYS" (cash equity hours, exact early closes) or "template"
    rth_open_minute: int = M(9, 30)
    rth_close_minute: int = M(16)
    settlement_minute: int = M(16, 15)                   # NY minute of the daily settlement window end
    roll_months: Tuple[int, ...] = (3, 6, 9, 12)
    expiry_rule: str = "third_friday"
    listing_date: str = ""                               # metadata only; see listing_note
    listing_note: str = "from memory, verify against Databento definition on Day 1"
    tick_size: float = 0.25
    point_value: float = 50.0
    calendar: str = "CMES"
    rth_calendar: str = "XNYS"

    @property
    def session_minutes(self) -> int:
        span = (self.globex_close_minute - self.globex_open_minute) % MINUTES_PER_DAY if not self.day_only else self.globex_close_minute - self.globex_open_minute
        return span - sum(b - a for a, b in self.pauses)


def _eq(root, name, tick, pv, listing, **kw):
    return SessionTemplate(root, "equity_index", "CME", name, halts=((M(16, 15), M(16, 30)),), rth_source="XNYS",
                           settlement_minute=M(16, 15), tick_size=tick, point_value=pv, listing_date=listing, **kw)


def _energy(root, name, tick, pv, listing, months, rule, settle=M(14, 30)):
    return SessionTemplate(root, "energy", "NYMEX", name, rth_open_minute=M(9), rth_close_minute=M(14, 30), settlement_minute=settle,
                           roll_months=months, expiry_rule=rule, tick_size=tick, point_value=pv, listing_date=listing)


def _metal(root, name, tick, pv, listing, months, settle):
    return SessionTemplate(root, "metals", "COMEX" if root != "PL" else "NYMEX", name, rth_open_minute=M(8, 20), rth_close_minute=M(13, 30),
                           settlement_minute=settle, roll_months=months, expiry_rule="metals_third_last_bday", tick_size=tick, point_value=pv, listing_date=listing)


def _rate(root, name, tick, pv, listing, rule):
    return SessionTemplate(root, "rates", "CBOT", name, rth_open_minute=M(8, 20), rth_close_minute=M(15), settlement_minute=M(15),
                           expiry_rule=rule, tick_size=tick, point_value=pv, listing_date=listing)


def _fx(root, name, tick, pv, listing):
    return SessionTemplate(root, "fx", "CME", name, rth_open_minute=M(8, 20), rth_close_minute=M(15), settlement_minute=M(15),
                           expiry_rule="fx_two_bdays_before_third_wed", tick_size=tick, point_value=pv, listing_date=listing)


def _grain(root, name, tick, pv, listing, months):
    return SessionTemplate(root, "grains", "CBOT", name, globex_open_minute=M(20), globex_close_minute=M(14, 20), pauses=((M(8, 45), M(9, 30)),),
                           rth_open_minute=M(9, 30), rth_close_minute=M(14, 20), settlement_minute=M(14, 15), roll_months=months,
                           expiry_rule="grains_bday_before_15th", tick_size=tick, point_value=pv, listing_date=listing)


def _live(root, name, tick, pv, listing, months, rule):
    return SessionTemplate(root, "livestock", "CME", name, globex_open_minute=M(9, 30), globex_close_minute=M(14, 5), day_only=True,
                           rth_open_minute=M(9, 30), rth_close_minute=M(14, 5), settlement_minute=M(14, 5), roll_months=months,
                           expiry_rule=rule, tick_size=tick, point_value=pv, listing_date=listing)


def _crypto(root, name, tick, pv, listing):
    return SessionTemplate(root, "crypto", "CME", name, rth_source="XNYS", settlement_minute=M(16), roll_months=tuple(range(1, 13)),
                           expiry_rule="crypto_last_friday", tick_size=tick, point_value=pv, listing_date=listing)


TEMPLATES: Dict[str, SessionTemplate] = {t.root: t for t in [
    _eq("ES", "E-mini S&P 500", 0.25, 50, "1997-09-09"), _eq("MES", "Micro E-mini S&P 500", 0.25, 5, "2019-05-06"),
    _eq("NQ", "E-mini Nasdaq-100", 0.25, 20, "1999-06-21"), _eq("MNQ", "Micro E-mini Nasdaq-100", 0.25, 2, "2019-05-06"),
    _eq("RTY", "E-mini Russell 2000 (CME since 2017-07-10)", 0.10, 50, "2017-07-10"), _eq("M2K", "Micro E-mini Russell 2000", 0.10, 5, "2019-05-06"),
    _eq("YM", "E-mini Dow", 1.0, 5, "2002-04-05", exchange="CBOT"), _eq("MYM", "Micro E-mini Dow", 1.0, 0.5, "2019-05-06", exchange="CBOT"),
    _energy("CL", "WTI crude", 0.01, 1000, "1983-03-30", tuple(range(1, 13)), "cl_three_bdays_before_25th"),
    _energy("MCL", "Micro WTI", 0.01, 100, "2021-07-12", tuple(range(1, 13)), "cl_three_bdays_before_25th"),
    _energy("NG", "Henry Hub natural gas", 0.001, 10000, "1990-04-03", tuple(range(1, 13)), "ng_three_bdays_before_month"),
    _energy("RB", "RBOB gasoline", 0.0001, 42000, "2005-10-03", tuple(range(1, 13)), "last_bday_prior_month"),
    _energy("HO", "NY Harbor ULSD", 0.0001, 42000, "1978-11-14", tuple(range(1, 13)), "last_bday_prior_month"),
    _metal("GC", "Gold", 0.10, 100, "1974-12-31", (2, 4, 6, 8, 12), M(13, 30)), _metal("MGC", "Micro gold", 0.10, 10, "2010-10-03", (2, 4, 6, 8, 12), M(13, 30)),
    _metal("SI", "Silver", 0.005, 5000, "1933-07-05", (3, 5, 7, 9, 12), M(13, 25)), _metal("HG", "Copper", 0.0005, 25000, "1988-07-29", (3, 5, 7, 9, 12), M(13)),
    _metal("PL", "Platinum", 0.10, 50, "1956-01-01", (1, 4, 7, 10), M(13, 5)),
    _rate("ZN", "10-year T-note", 1 / 64, 1000, "1982-05-03", "rates_zn_last_bday"), _rate("ZF", "5-year T-note", 1 / 128, 1000, "1988-05-20", "rates_zn_last_bday"),
    _rate("ZT", "2-year T-note", 1 / 128, 2000, "1990-06-25", "rates_zn_last_bday"), _rate("ZB", "30-year T-bond", 1 / 32, 1000, "1977-08-22", "rates_zb_seventh_bday"),
    _rate("UB", "Ultra T-bond", 1 / 32, 1000, "2010-01-11", "rates_zb_seventh_bday"),
    _fx("6E", "Euro FX", 0.00005, 125000, "1999-01-04"), _fx("6B", "British pound", 0.0001, 62500, "1972-05-16"), _fx("6J", "Japanese yen", 0.0000005, 12500000, "1972-05-16"),
    _fx("6A", "Australian dollar", 0.0001, 100000, "1987-01-13"), _fx("6C", "Canadian dollar", 0.00005, 100000, "1972-05-16"), _fx("6S", "Swiss franc", 0.0001, 125000, "1972-05-16"),
    _grain("ZC", "Corn", 0.25, 50, "1877-01-02", (3, 5, 7, 9, 12)), _grain("ZS", "Soybeans", 0.25, 50, "1936-10-05", (1, 3, 5, 7, 8, 9, 11)),
    _grain("ZW", "Chicago wheat", 0.25, 50, "1877-01-02", (3, 5, 7, 9, 12)), _grain("ZL", "Soybean oil", 0.01, 600, "1950-07-17", (1, 3, 5, 7, 8, 9, 10, 12)),
    _grain("ZM", "Soybean meal", 0.10, 100, "1951-08-20", (1, 3, 5, 7, 8, 9, 10, 12)),
    _live("LE", "Live cattle", 0.025, 400, "1964-11-30", (2, 4, 6, 8, 10, 12), "livestock_le_last_bday"),
    _live("HE", "Lean hogs", 0.025, 400, "1966-02-28", (2, 4, 5, 6, 7, 8, 10, 12), "livestock_he_tenth_bday"),
    _crypto("BTC", "Bitcoin (5 BTC)", 5.0, 5, "2017-12-18"), _crypto("MBT", "Micro Bitcoin", 5.0, 0.1, "2021-05-03"),
]}
GROUPS = tuple(sorted({t.group for t in TEMPLATES.values()}))


def template(root: str) -> SessionTemplate:
    if root not in TEMPLATES:
        raise KeyError(f"qe.calendars: no session template for root {root!r}; known roots: {sorted(TEMPLATES)}")
    return TEMPLATES[root]


# ------------------------------------------------------------------------------------------------------------ library wrappers
@functools.lru_cache(maxsize=16)
def _calendar(name: str, start: str, end: str):
    return xc.get_calendar(name, start=start, end=end)


def _pad(start, end, days=10) -> Tuple[str, str]:
    return ((pd.Timestamp(start).normalize() - pd.Timedelta(days=days)).strftime("%Y-%m-%d"),
            (pd.Timestamp(end).normalize() + pd.Timedelta(days=days)).strftime("%Y-%m-%d"))


def cme_schedule(start, end) -> pd.DataFrame:
    a, b = _pad(start, end)
    s = _calendar("CMES", a, b).schedule
    return s.loc[(s.index >= pd.Timestamp(start).normalize()) & (s.index <= pd.Timestamp(end).normalize())]


def xnys_schedule(start, end) -> pd.DataFrame:
    a, b = _pad(start, end)
    s = _calendar("XNYS", a, b).schedule
    return s.loc[(s.index >= pd.Timestamp(start).normalize()) & (s.index <= pd.Timestamp(end).normalize())]


def cme_early_closes(start, end) -> pd.DatetimeIndex:
    a, b = _pad(start, end)
    ec = _calendar("CMES", a, b).early_closes
    return ec[(ec >= pd.Timestamp(start).normalize()) & (ec <= pd.Timestamp(end).normalize())]


def cme_only_sessions(start, end) -> pd.DatetimeIndex:
    """Trading days with a CMES session but no XNYS session (US holidays on which Globex trades until 12:00 CT)."""
    return cme_schedule(start, end).index.difference(xnys_schedule(start, end).index)


def ny_minute(ts_utc) -> np.ndarray:
    idx = pd.DatetimeIndex(ts_utc)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    ny = idx.tz_convert(TZ_NY)
    return (ny.hour * 60 + ny.minute).to_numpy(dtype=np.int64)


def tday_minute(ny_min) -> np.ndarray:
    return (np.asarray(ny_min, dtype=np.int64) - REOPEN_NY_MINUTE) % MINUTES_PER_DAY


def _ny_instant(dates: pd.DatetimeIndex, minute: int, day_offset: int = 0) -> pd.DatetimeIndex:
    """UTC instants of `minute` (NY wall clock) on each date (+ day_offset), DST-exact."""
    naive = pd.DatetimeIndex(dates).normalize().tz_localize(None) + pd.Timedelta(days=day_offset) + pd.Timedelta(minutes=minute)
    return naive.tz_localize(TZ_NY, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC")


# ------------------------------------------------------------------------------------------------------------ day table
def day_table(start, end, root: str = "ES") -> pd.DataFrame:
    """One row per trading day (CMES session label) for `root` between `start` and `end` (dates, inclusive).

    Columns: session_open_utc, session_close_utc, has_rth, rth_open_utc, rth_close_utc, is_half_day, is_cme_early_close,
    is_cme_only, is_roll_week, rth_open_minute, rth_close_minute, session_open_minute, session_close_minute (NY minutes),
    tday_close_minute (minutes since the reopen), settlement_minute.
    """
    tpl = template(root)
    cme = cme_schedule(start, end)
    nyse = xnys_schedule(start, end)
    idx = cme.index.rename("trading_day")
    out = pd.DataFrame(index=idx)
    early = idx.isin(cme_early_closes(start, end))
    has_rth = idx.isin(nyse.index)
    out["has_rth"] = has_rth
    out["is_cme_early_close"] = early
    out["is_cme_only"] = ~has_rth
    # session open/close
    if tpl.day_only:
        out["session_open_utc"] = _ny_instant(idx, tpl.globex_open_minute, 0)
    else:
        out["session_open_utc"] = cme["open"].dt.tz_convert("UTC").to_numpy() if tpl.globex_open_minute == REOPEN_NY_MINUTE \
            else _ny_instant(idx, tpl.globex_open_minute, -1)
    close_min = np.where(early, np.minimum(tpl.globex_close_minute, HALF_DAY_CLOSE_NY_MINUTE), tpl.globex_close_minute)
    out["session_close_utc"] = pd.DatetimeIndex([_ny_instant(pd.DatetimeIndex([d]), int(m), 0)[0] for d, m in zip(idx, close_min)])
    out["session_open_minute"] = tpl.globex_open_minute
    out["session_close_minute"] = close_min.astype(int)
    out["tday_close_minute"] = tday_minute(out["session_close_minute"].to_numpy())
    # RTH window
    if tpl.rth_source == "XNYS":
        ro = nyse["open"].reindex(idx)
        rc = nyse["close"].reindex(idx)
        out["rth_open_utc"] = pd.to_datetime(ro.dt.tz_convert("UTC"), utc=True)
        out["rth_close_utc"] = pd.to_datetime(rc.dt.tz_convert("UTC"), utc=True)
        ny_close = rc.dt.tz_convert(TZ_NY)
        rth_close_min = (ny_close.dt.hour * 60 + ny_close.dt.minute).fillna(tpl.rth_close_minute).astype(int).to_numpy()
        rth_open_min = np.full(len(idx), tpl.rth_open_minute)
    else:
        rth_close_min = np.where(early, np.minimum(tpl.rth_close_minute, HALF_DAY_CLOSE_NY_MINUTE), tpl.rth_close_minute).astype(int)
        rth_open_min = np.full(len(idx), tpl.rth_open_minute)
        ro_utc = _ny_instant(idx, tpl.rth_open_minute, 0)
        rc_utc = pd.DatetimeIndex([_ny_instant(pd.DatetimeIndex([d]), int(m), 0)[0] for d, m in zip(idx, rth_close_min)])
        out["rth_open_utc"] = pd.DatetimeIndex(np.where(has_rth, ro_utc, pd.NaT)).tz_localize("UTC") if ro_utc.tz is None else pd.DatetimeIndex(ro_utc).where(has_rth, pd.NaT)
        out["rth_close_utc"] = pd.DatetimeIndex(rc_utc).where(has_rth, pd.NaT)
    out["rth_open_minute"] = rth_open_min
    out["rth_close_minute"] = rth_close_min
    rth_early = has_rth & (rth_close_min < tpl.rth_close_minute)
    out["is_half_day"] = rth_early | early
    out["settlement_minute"] = np.where(early, np.minimum(tpl.settlement_minute, HALF_DAY_CLOSE_NY_MINUTE), tpl.settlement_minute)
    out["is_roll_week"] = is_roll_week(idx, tpl.roll_months)
    cols = ["session_open_utc", "session_close_utc", "has_rth", "rth_open_utc", "rth_close_utc", "is_half_day", "is_cme_early_close",
            "is_cme_only", "is_roll_week", "rth_open_minute", "rth_close_minute", "session_open_minute", "session_close_minute",
            "tday_close_minute", "settlement_minute"]
    return out[cols]


def _ns(x) -> np.ndarray:
    idx = pd.DatetimeIndex(x)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    return idx.tz_convert("UTC").tz_localize(None).as_unit("ns").asi8


def tag_minutes(ts_utc, root: str = "ES") -> pd.DataFrame:
    """Per-bar session tags for UTC bar-open timestamps (any order; output aligned to the input order)."""
    tpl = template(root)
    idx = pd.DatetimeIndex(ts_utc)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    n = len(idx)
    if n == 0:
        raise ValueError("tag_minutes: empty timestamp index")
    lo = idx.min().tz_convert(TZ_NY).normalize().tz_localize(None) - pd.Timedelta(days=3)
    hi = idx.max().tz_convert(TZ_NY).normalize().tz_localize(None) + pd.Timedelta(days=3)
    days = day_table(lo, hi, root)
    ts = _ns(idx)
    # the trading day of a bar: the CMES session whose 18:00 ET reopen is the last one at or before the bar (all roots)
    reopen = _ns(_ny_instant(days.index, REOPEN_NY_MINUTE, -1)) if not tpl.day_only else _ns(_ny_instant(days.index, REOPEN_NY_MINUTE, -1))
    k = np.searchsorted(reopen, ts, side="right") - 1
    valid = k >= 0
    k_safe = np.clip(k, 0, len(days) - 1)
    opens = _ns(days["session_open_utc"])[k_safe]
    closes = _ns(days["session_close_utc"])[k_safe]
    in_session = valid & (ts >= opens) & (ts < closes)
    nym = ny_minute(idx)
    for a, b in tpl.pauses:
        in_session &= ~((nym >= a) & (nym < b))
    in_halt = np.zeros(n, dtype=bool)
    for a, b in tpl.halts:
        in_halt |= in_session & (nym >= a) & (nym < b)
    out = pd.DataFrame(index=np.arange(n))
    out["ny_minute"] = nym
    out["tday_minute"] = tday_minute(nym)
    out["trading_day"] = pd.DatetimeIndex(days.index.to_numpy()[k_safe])
    out["in_session"] = in_session
    out["in_halt"] = in_halt
    has_rth = days["has_rth"].to_numpy()[k_safe] & valid
    ro = days["rth_open_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)[k_safe]
    rc = days["rth_close_utc"].to_numpy(dtype="datetime64[ns]").astype(np.int64)[k_safe]
    with np.errstate(invalid="ignore"):
        out["is_rth"] = has_rth & (ts >= ro) & (ts < rc)
    out["has_rth"] = has_rth
    for c in ("is_half_day", "is_roll_week", "is_cme_only"):
        out[c] = days[c].to_numpy()[k_safe] & valid
    for c in ("rth_close_minute", "session_close_minute", "tday_close_minute", "settlement_minute"):
        out[c] = days[c].to_numpy()[k_safe]
    return out


def ny_index(start, end, root: str = "ES", *, rth_only: bool = False, freq_minutes: int = 1) -> pd.DatetimeIndex:
    """The UTC index of every in-session bar-open minute of `root` between `start` and `end` (dates, inclusive):
    the template every dataset is counted against (QA rule: never against 1,380 or 1,440)."""
    days = day_table(start, end, root)
    tpl = template(root)
    parts: List[pd.DatetimeIndex] = []
    for d, r in days.iterrows():
        if rth_only:
            if not r["has_rth"]:
                continue
            a, b = r["rth_open_utc"], r["rth_close_utc"]
        else:
            a, b = r["session_open_utc"], r["session_close_utc"]
        rng = pd.date_range(a, b, freq=f"{freq_minutes}min", inclusive="left", tz="UTC")
        if tpl.pauses and not rth_only:
            nym = ny_minute(rng)
            keep = np.ones(len(rng), dtype=bool)
            for pa, pb in tpl.pauses:
                keep &= ~((nym >= pa) & (nym < pb))
            rng = rng[keep]
        parts.append(rng)
    if not parts:
        return pd.DatetimeIndex([], tz="UTC")
    return parts[0].append(parts[1:]) if len(parts) > 1 else parts[0]


# ------------------------------------------------------------------------------------------------------------ DST and FTMO
def dst_transitions(tz: str, start_year: int = 2010, end_year: int = 2027) -> pd.DataFrame:
    """Instants (UTC) at which the UTC offset of `tz` changes, with the offsets before and after (minutes)."""
    z = ZoneInfo(tz)
    rows = []
    t = datetime(start_year, 1, 1, tzinfo=z)
    prev = t.utcoffset()
    while t.year <= end_year:
        nxt = t + timedelta(hours=1)
        off = nxt.utcoffset()
        if off != prev:
            # refine to the minute
            lo, hi = t, nxt
            while (hi - lo) > timedelta(minutes=1):
                mid = lo + (hi - lo) / 2
                if mid.utcoffset() == prev:
                    lo = mid
                else:
                    hi = mid
            rows.append({"ts": pd.Timestamp(hi).tz_convert("UTC"), "tz": tz, "offset_before_min": int(prev.total_seconds() // 60),
                         "offset_after_min": int(off.total_seconds() // 60), "local_date": hi.date().isoformat()})
            prev = off
        t = nxt
    return pd.DataFrame(rows)


def is_dst_transition_day(dates, tz: str = TZ_NY) -> np.ndarray:
    d = pd.DatetimeIndex(pd.to_datetime(dates)).normalize()
    if len(d) == 0:
        return np.zeros(0, dtype=bool)
    tr = dst_transitions(tz, d.min().year, d.max().year)
    days = set(tr["local_date"])
    return np.fromiter((x.date().isoformat() in days for x in d), dtype=bool, count=len(d))


def ftmo_day_start_utc(dates) -> pd.DatetimeIndex:
    """00:00 Europe/Prague of each calendar date, in UTC: the FTMO daily-loss reference instant (CE(S)T, DST-exact)."""
    d = pd.DatetimeIndex(pd.to_datetime(dates)).normalize().tz_localize(None)
    return d.tz_localize(TZ_PRAGUE, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC")


def ftmo_trading_day(ts_utc) -> pd.DatetimeIndex:
    """The FTMO day (Prague calendar date) of each UTC instant."""
    idx = pd.DatetimeIndex(ts_utc)
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    return idx.tz_convert(TZ_PRAGUE).normalize().tz_localize(None)


def eu_us_dst_mismatch_days(start_year: int = 2010, end_year: int = 2027) -> pd.DatetimeIndex:
    """Calendar dates on which New York is on DST and Prague is not, or vice versa (two to three weeks a year)."""
    days = pd.date_range(f"{start_year}-01-01", f"{end_year}-12-31", freq="D")
    ny = days.tz_localize(TZ_NY, ambiguous=True, nonexistent="shift_forward") + pd.Timedelta(hours=12)
    pr = days.tz_localize(TZ_PRAGUE, ambiguous=True, nonexistent="shift_forward") + pd.Timedelta(hours=12)
    ny_dst = np.array([bool(t.dst()) for t in ny])
    pr_dst = np.array([bool(t.dst()) for t in pr])
    return days[ny_dst != pr_dst]


# ------------------------------------------------------------------------------------------------------------ rolls
def is_roll_week(dates, roll_months: Iterable[int] = (3, 6, 9, 12)) -> np.ndarray:
    """True for Mon–Fri of the week holding the third Friday of a roll month and for the following Monday
    (the inherited `roll_excluded` approximation; the per-root scaffold below is the refinement)."""
    d = pd.DatetimeIndex(pd.to_datetime(dates)).normalize().as_unit("ns")
    if len(d) == 0:
        return np.zeros(0, dtype=bool)
    excluded = set()
    for y in range(d.min().year, d.max().year + 1):
        for m in roll_months:
            fri3 = _nth_weekday(y, m, 4, 3)
            mon = fri3 - pd.Timedelta(days=4)
            for i in range(5):
                excluded.add((mon + pd.Timedelta(days=i)).value)
            excluded.add((fri3 + pd.Timedelta(days=3)).value)
    return np.fromiter((v in excluded for v in d.asi8), dtype=bool, count=len(d))


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> pd.Timestamp:
    first = pd.Timestamp(year, month, 1)
    return first + pd.Timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def _bdays(start_year: int, end_year: int) -> pd.DatetimeIndex:
    return cme_schedule(f"{start_year - 1}-12-01", f"{end_year + 1}-01-31").index


def _shift_bdays(bd: pd.DatetimeIndex, date: pd.Timestamp, k: int) -> pd.Timestamp:
    """k business days before (k<0) or after (k>0) `date`; a non-business `date` counts from the previous business day."""
    i = bd.searchsorted(date, side="right") - 1
    j = max(0, min(len(bd) - 1, i + k))
    return bd[j]


def _last_bday_of_month(bd: pd.DatetimeIndex, year: int, month: int) -> pd.Timestamp:
    end = pd.Timestamp(year, month, 1) + pd.offsets.MonthEnd(0)
    return _shift_bdays(bd, end, 0)


def _nth_bday_of_month(bd: pd.DatetimeIndex, year: int, month: int, n: int) -> pd.Timestamp:
    first = pd.Timestamp(year, month, 1)
    i = bd.searchsorted(first, side="left")
    return bd[i + n - 1]


EXPIRY_RULES = {
    "third_friday": "last trade 09:30 ET on the third Friday of the contract month (cash-settled); estimated roll = the Thursday 8 days before",
    "cl_three_bdays_before_25th": "last trade 3 business days before the 25th calendar day of the month preceding the contract month (previous business day if the 25th is not one); estimated roll = last trade - 3 business days",
    "ng_three_bdays_before_month": "last trade 3 business days before the first calendar day of the delivery month; estimated roll = last trade - 3 business days",
    "last_bday_prior_month": "last trade = last business day of the month preceding the delivery month; estimated roll = last trade - 3 business days",
    "metals_third_last_bday": "last trade = third-to-last business day of the delivery month; first notice = last business day of the preceding month; estimated roll = first notice - 2 business days",
    "rates_zn_last_bday": "last trade = last business day of the delivery month (ZT/ZF/ZN: 7th business day preceding for ZN per CBOT; scaffold uses last business day); first notice = last business day of the preceding month; estimated roll = first notice - 2 business days",
    "rates_zb_seventh_bday": "last trade = 7th business day preceding the last business day of the delivery month; first notice = last business day of the preceding month; estimated roll = first notice - 2 business days",
    "fx_two_bdays_before_third_wed": "last trade 09:16 CT on the second business day before the third Wednesday of the contract month; estimated roll = last trade - 5 business days",
    "grains_bday_before_15th": "last trade = business day preceding the 15th calendar day of the contract month; first notice = last business day of the preceding month; estimated roll = first notice - 2 business days",
    "livestock_le_last_bday": "last trade = last business day of the contract month (12:00 CT); physically delivered; estimated roll = last trade - 5 business days",
    "livestock_he_tenth_bday": "last trade = 10th business day of the contract month (12:00 CT); cash-settled; estimated roll = last trade - 5 business days",
    "crypto_last_friday": "last trade 16:00 London on the last Friday of the contract month; estimated roll = last trade - 3 business days",
}


def roll_scaffold(root: str, start_year: int = 2010, end_year: int = 2027) -> pd.DataFrame:
    """Rule-based contract calendar: one row per contract month with expiry (last trade), first notice (NaT when the
    contract is cash-settled or the rule has none), the estimated roll date, and the rule text. A SCAFFOLD: the Day-1
    Databento `definition` schema (expiration, first notice) replaces these dates; until then every row says rule=...
    """
    tpl = template(root)
    bd = _bdays(start_year, end_year)
    rows = []
    for y in range(start_year, end_year + 1):
        for m in tpl.roll_months:
            fnd = pd.NaT
            r = tpl.expiry_rule
            py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
            if r == "third_friday":
                exp = _nth_weekday(y, m, 4, 3)
                exp = _shift_bdays(bd, exp, 0)
                roll = _shift_bdays(bd, exp - pd.Timedelta(days=8), 0)
            elif r == "cl_three_bdays_before_25th":
                d25 = pd.Timestamp(py, pm, 25)
                exp = _shift_bdays(bd, d25, -3)
                roll = _shift_bdays(bd, exp, -3)
            elif r == "ng_three_bdays_before_month":
                exp = _shift_bdays(bd, pd.Timestamp(y, m, 1) - pd.Timedelta(days=1), -2)
                roll = _shift_bdays(bd, exp, -3)
            elif r == "last_bday_prior_month":
                exp = _last_bday_of_month(bd, py, pm)
                roll = _shift_bdays(bd, exp, -3)
            elif r == "metals_third_last_bday":
                exp = _shift_bdays(bd, _last_bday_of_month(bd, y, m), -2)
                fnd = _last_bday_of_month(bd, py, pm)
                roll = _shift_bdays(bd, fnd, -2)
            elif r == "rates_zn_last_bday":
                exp = _last_bday_of_month(bd, y, m)
                fnd = _last_bday_of_month(bd, py, pm)
                roll = _shift_bdays(bd, fnd, -2)
            elif r == "rates_zb_seventh_bday":
                exp = _shift_bdays(bd, _last_bday_of_month(bd, y, m), -7)
                fnd = _last_bday_of_month(bd, py, pm)
                roll = _shift_bdays(bd, fnd, -2)
            elif r == "fx_two_bdays_before_third_wed":
                exp = _shift_bdays(bd, _nth_weekday(y, m, 2, 3), -2)
                roll = _shift_bdays(bd, exp, -5)
            elif r == "grains_bday_before_15th":
                exp = _shift_bdays(bd, pd.Timestamp(y, m, 15) - pd.Timedelta(days=1), 0)
                fnd = _last_bday_of_month(bd, py, pm)
                roll = _shift_bdays(bd, fnd, -2)
            elif r == "livestock_le_last_bday":
                exp = _last_bday_of_month(bd, y, m)
                roll = _shift_bdays(bd, exp, -5)
            elif r == "livestock_he_tenth_bday":
                exp = _nth_bday_of_month(bd, y, m, 10)
                roll = _shift_bdays(bd, exp, -5)
            elif r == "crypto_last_friday":
                last = pd.Timestamp(y, m, 1) + pd.offsets.MonthEnd(0)
                exp = last - pd.Timedelta(days=(last.weekday() - 4) % 7)
                roll = _shift_bdays(bd, exp, -3)
            else:
                raise KeyError(r)
            rows.append({"root": root, "contract_month": f"{y}-{m:02d}", "expiry": exp, "first_notice": fnd, "roll_est": roll,
                         "rule": r, "source": "rule (scaffold); replace with Databento definition"})
    return pd.DataFrame(rows)


def front_by_volume(volume: pd.DataFrame, *, persist: bool = True, lag: int = 1) -> pd.Series:
    """The `.v.0` rule made explicit. `volume` is indexed by trading day with one column per contract in EXPIRY ORDER.
    Databento's `.v.0` points at the contract with the highest volume on the previous session (lag=1) and may flip
    BACK to the old contract when its volume briefly exceeds the new one's again around the roll. With `persist=True`
    (the program's flip-back rule) a flip to a later contract is never undone: the front moves monotonically forward,
    so a continuous series built from it has exactly one roll per contract."""
    v = volume.shift(lag).fillna(0.0)
    cols = list(volume.columns)
    front = []
    cur = 0
    for _, row in v.iterrows():
        best = int(np.argmax(row.to_numpy()))
        if persist:
            if best > cur:
                cur = best
        else:
            cur = best
        front.append(cols[cur])
    return pd.Series(front, index=volume.index, name="front")
