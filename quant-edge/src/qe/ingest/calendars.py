#!/usr/bin/env python3
"""Release calendars with exact timestamps -> DATA_ROOT/calendars/cal_*.csv, one manifest row each.

Every row carries `ts` (UTC instant of the release), `date_local`, `time_local`, `tz`, `date_source` and `time_source`
(`page`/`file` = read from the named source; `rule` = generated from the documented rule, to be verified before a
registered row leans on the exact minute). Sources and fetch dates are in each dataset's manifest notes.

  cal_fomc            FOMC statement releases 2010-01..2027-12. 2010-01..2026-06 from the inherited E2 calendar
                      (~/quant-edge-inherited/pr4/.../w2-events/events.csv, built 2026-10-11 by calendar_build.py from
                      federalreserve.gov fomchistoricalYYYY.htm / fomccalendars.htm; statement time 14:15 ET before
                      2013-03-20, 12:30 ET on the 2011–2012 press-conference meetings, 14:00 ET from 2013-03-20 on,
                      per the Fed press release of 2013-03-13); 2026-07..2027 appended from fomccalendars.htm fetched today.
  cal_bls_cpi, cal_bls_nfp   BLS release dates 2010..2026-09 from the same inherited file (ALFRED rid=10 / rid=50,
                      08:30 ET). bls.gov answers 403 and alfred.stlouisfed.org / fred.stlouisfed.org did not answer from
                      this session today (recorded in the fetch log): nothing newer than the inherited pull.
  cal_eia_wpsr        Weekly Petroleum Status Report. Release DATES 2011-08-03..today parsed from the EIA archive page
                      (eia.gov/petroleum/supply/weekly/archive/); 2010-01..2011-07 by rule (Wednesday; Thursday after a
                      Monday federal holiday). Times: Wednesday 10:30 ET; otherwise the EIA schedule page's exceptions
                      for 2025–2026 (exact) and 11:00 ET (before 2025) / 12:00 ET (2025-) by rule.
  cal_eia_ngsr        Weekly Natural Gas Storage Report: Thursday 10:30 ET by rule, with the 2025–2026 holiday
                      exceptions exact from ir.eia.gov/ngs/schedule.html; earlier holiday weeks flagged, not shifted.
  cal_wasde           USDA WASDE 12:00 ET: 2026–2027 dates from usda.gov (page), history by the ESMIS archive when
                      reachable (usda.gov data pages answered 403 today).
  cal_index_rebalance S&P 500 quarterly rebalance (third Friday of Mar/Jun/Sep/Dec, effective after the close),
                      Russell reconstitution (fourth Friday of June; 2026 also 2026-12-11), MSCI SAIR/QIR (last business
                      day of Feb/May/Aug/Nov) — rule-generated; sources in notes.
  cal_lbma_auctions   LBMA auction times (London): gold 10:30/15:00, silver 12:00, platinum 09:45/14:00, palladium
                      follows platinum; launch dates 2015-03-20 / 2014-08-14 / 2014-12-01.

Usage: python3 -m qe.ingest.calendars [--only fomc,bls,eia,wasde,index,lbma] [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import pandas as pd

from qe.ingest import common

INHERITED_EVENTS = Path(os.path.expanduser("~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w2-events/events.csv"))
INHERITED_NOTE = "inherited E2 calendar events.csv (PR#4 worktree e0f5e59; built 2026-10-11 by w2-events/calendar_build.py)"
FOMC_CAL_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FOMC_TIME_SRC = "https://www.federalreserve.gov/newsevents/pressreleases/monetary20130313a.htm"
EIA_WPSR_ARCHIVE = "https://www.eia.gov/petroleum/supply/weekly/archive/"
EIA_WPSR_SCHEDULE = "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
EIA_NGSR_SCHEDULE = "https://ir.eia.gov/ngs/schedule.html"
WASDE_URL = "https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report"
NY = "America/New_York"
LON = "Europe/London"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September",
                                      "October", "November", "December"], 1)}


def _row(date, time_s: str, tz: str, **extra) -> dict:
    local = pd.Timestamp(f"{pd.Timestamp(date).date()} {time_s}")
    ts = local.tz_localize(tz, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC")
    return {"ts": ts, "date_local": str(pd.Timestamp(date).date()), "time_local": time_s, "tz": tz, **extra}


def _frame(rows) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["ts"]).sort_values("ts").reset_index(drop=True)


def _us_federal_holidays(years) -> set:
    from pandas.tseries.holiday import USFederalHolidayCalendar
    cal = USFederalHolidayCalendar()
    hol = set(d.date() for d in cal.holidays(start=f"{min(years)}-01-01", end=f"{max(years)}-12-31"))
    for y in years:   # Juneteenth (federal holiday since 2021) is not in pandas' calendar
        if y >= 2021:
            d = pd.Timestamp(y, 6, 19)
            if d.weekday() == 5:
                d -= pd.Timedelta(days=1)
            elif d.weekday() == 6:
                d += pd.Timedelta(days=1)
            hol.add(d.date())
    return hol


# ------------------------------------------------------------------------------------------------------------ inherited
def inherited_events() -> pd.DataFrame:
    if not INHERITED_EVENTS.exists():
        raise FileNotFoundError(f"{INHERITED_EVENTS} missing: run quant-edge/tools/fetch_inherited.sh")
    ev = pd.read_csv(INHERITED_EVENTS, dtype=str)
    ev = ev[ev["date"] != "2026-10-11"]          # three placeholder rows carry the build date instead of a release date
    return ev


# ------------------------------------------------------------------------------------------------------------ FOMC
def parse_fomc_calendar_page(html: str) -> list:
    """(year, month, last_day, flags) for every meeting on fomccalendars.htm (statement day = last day of the range)."""
    text = re.sub(r"\s+", " ", html)
    out = []
    for ym in re.finditer(r"(\d{4}) FOMC Meetings(.*?)(?=\d{4} FOMC Meetings|$)", text):
        year = int(ym.group(1))
        body = ym.group(2)
        for m in re.finditer(r'fomc-meeting__month[^>]*>\s*<strong>\s*([A-Za-z]+)(?:/([A-Za-z]+))?\s*</strong>.*?fomc-meeting__date[^>]*>\s*([^<]*?)\s*<', body):
            mon1, mon2, days = m.group(1), m.group(2), m.group(3)
            flags = []
            low = days.lower()
            if "unscheduled" in low:
                flags.append("unscheduled")
            if "notation" in low:
                flags.append("notation_vote")
            if "cancel" in low:
                flags.append("cancelled")
            nums = re.findall(r"\d+", days)
            if not nums:
                continue
            last = int(nums[-1])
            mon = MONTHS.get(mon2 or mon1) if mon2 else MONTHS.get(mon1)
            if mon is None:
                continue
            out.append((year, mon, last, ",".join(flags), "*" in days))
    return out


def build_fomc(dry_run: bool = False) -> pd.DataFrame:
    ev = inherited_events()
    rows = []
    for _, r in ev[ev["event"] == "FOMC"].iterrows():
        rows.append(_row(r["date"], r["time_et"], NY, event="FOMC_statement", scheduled=r["scheduled"] == "True",
                         date_source="inherited", time_source="inherited(14:15 pre-2013-03-20; 12:30 presconf 2011-12; 14:00 after)"))
    last_inherited = max(r["date"] for _, r in ev[ev["event"] == "FOMC"].iterrows())
    try:
        html = common.fetch_text(FOMC_CAL_URL)
        for year, mon, day, flags, sep in parse_fomc_calendar_page(html):
            d = pd.Timestamp(year, mon, day)
            if str(d.date()) <= last_inherited or "notation_vote" in flags or "cancelled" in flags:
                continue
            rows.append(_row(d, "14:00", NY, event="FOMC_statement", scheduled="unscheduled" not in flags,
                             date_source=f"page:{FOMC_CAL_URL}", time_source=f"rule:14:00 ET since 2013-03-20 ({FOMC_TIME_SRC})"))
    except common.Blocked as e:
        print(f"FOMC calendar page not read: {e}", file=sys.stderr)
    return _frame(rows)


# ------------------------------------------------------------------------------------------------------------ BLS
def build_bls(event: str) -> pd.DataFrame:
    ev = inherited_events()
    rows = [_row(r["date"], r["time_et"], NY, event=event, date_source="inherited(ALFRED rid=10 CPI / rid=50 NFP, fetched 2026-10-11)",
                 time_source="BLS convention 08:30 ET") for _, r in ev[ev["event"] == event].iterrows()]
    return _frame(rows)


# ------------------------------------------------------------------------------------------------------------ EIA
WPSR_EXCEPTIONS = {   # from EIA_WPSR_SCHEDULE fetched 2026-11-04 (release date -> time ET)
    "2025-01-02": "11:00", "2025-01-23": "12:00", "2025-02-20": "12:00", "2025-05-29": "12:00", "2025-09-04": "12:00",
    "2025-10-16": "12:00", "2025-11-13": "12:00", "2025-12-29": "17:00", "2026-01-22": "12:00", "2026-02-19": "12:00",
    "2026-05-28": "12:00", "2026-09-10": "12:00", "2026-10-15": "12:00", "2026-11-12": "12:00",
}
NGSR_EXCEPTIONS = {   # from EIA_NGSR_SCHEDULE fetched 2026-11-04 (release date -> time ET); replaces that week's Thursday
    "2025-01-03": "10:30", "2025-01-08": "12:00", "2025-06-18": "12:00", "2025-11-14": "10:30", "2025-11-26": "12:00",
    "2025-12-29": "12:00", "2025-12-31": "12:00", "2026-11-13": "10:30", "2026-11-25": "12:00",
}


def parse_wpsr_archive(html: str) -> list:
    dates = sorted(set(re.findall(r"archive/\d{4}/(\d{4})_(\d{2})_(\d{2})/wpsr_", html)))
    return [pd.Timestamp(int(y), int(m), int(d)) for y, m, d in dates]


def build_eia_wpsr(start_year: int = 2010) -> pd.DataFrame:
    raw = common.RAW / "eia" / "wpsr_archive.html"
    archive_dates = []
    try:
        common.fetch(EIA_WPSR_ARCHIVE, raw, overwrite=True)
        archive_dates = parse_wpsr_archive(raw.read_text(errors="replace"))
    except common.Blocked as e:
        print(f"EIA archive not read: {e}", file=sys.stderr)
        if raw.exists():
            archive_dates = parse_wpsr_archive(raw.read_text(errors="replace"))
    first_archive = min(archive_dates) if archive_dates else pd.Timestamp("2100-01-01")
    rows = []
    hol = _us_federal_holidays(range(start_year, 2028))
    # rule-based Wednesdays before the archive starts
    for wed in pd.date_range(f"{start_year}-01-06", first_archive - pd.Timedelta(days=1), freq="W-WED"):
        d = wed
        if (wed - pd.Timedelta(days=2)).date() in hol or (wed - pd.Timedelta(days=1)).date() in hol or wed.date() in hol:
            d = wed + pd.Timedelta(days=1)
        t = "10:30" if d.weekday() == 2 else "11:00"
        rows.append(_row(d, t, NY, event="EIA_WPSR", date_source="rule:Wed, Thu after Mon-Wed federal holiday", time_source="rule"))
    for d in archive_dates:
        key = str(d.date())
        if key in WPSR_EXCEPTIONS:
            t, ts_src = WPSR_EXCEPTIONS[key], f"page:{EIA_WPSR_SCHEDULE}"
        elif d.weekday() == 2:
            t, ts_src = "10:30", "rule:Wednesday 10:30 ET"
        else:
            t, ts_src = ("11:00" if d.year < 2025 else "12:00"), "rule:non-Wednesday release 11:00 ET (<2025) / 12:00 ET"
        rows.append(_row(d, t, NY, event="EIA_WPSR", date_source=f"page:{EIA_WPSR_ARCHIVE}", time_source=ts_src))
    return _frame(rows)


def build_eia_ngsr(start_year: int = 2010, end_year: int = 2026) -> pd.DataFrame:
    hol = _us_federal_holidays(range(start_year, end_year + 2))
    exc_weeks = {pd.Timestamp(k).to_period("W-SAT") for k in NGSR_EXCEPTIONS}
    rows = []
    for thu in pd.date_range(f"{start_year}-01-07", f"{end_year}-12-31", freq="W-THU"):
        wk = thu.to_period("W-SAT")
        if wk in exc_weeks:
            continue
        hol_week = any((thu - pd.Timedelta(days=k)).date() in hol for k in range(0, 4)) or (thu + pd.Timedelta(days=1)).date() in hol
        rows.append(_row(thu, "10:30", NY, event="EIA_NGSR", date_source="rule:Thursday" + (" (holiday week: real date may differ)" if hol_week else ""),
                         time_source="rule:10:30 ET", holiday_week=hol_week))
    for k, t in NGSR_EXCEPTIONS.items():
        rows.append(_row(k, t, NY, event="EIA_NGSR", date_source=f"page:{EIA_NGSR_SCHEDULE}", time_source=f"page:{EIA_NGSR_SCHEDULE}", holiday_week=True))
    return _frame(rows)


# ------------------------------------------------------------------------------------------------------------ WASDE
WASDE_PAGE_DATES = {   # from WASDE_URL fetched 2026-11-04 (12:00 ET)
    2026: [(1, 12), (2, 10), (3, 10), (4, 9), (5, 12), (6, 11), (7, 10), (8, 12), (9, 11), (10, 9), (11, 10), (12, 10)],
    2027: [(1, 12), (2, 10), (3, 10), (4, 9), (5, 12), (6, 11), (7, 9), (8, 12), (9, 10), (10, 8), (11, 10), (12, 10)],
}


def build_wasde(history_dates=None) -> pd.DataFrame:
    rows = []
    for y, lst in WASDE_PAGE_DATES.items():
        for m, d in lst:
            rows.append(_row(pd.Timestamp(y, m, d), "12:00", NY, event="USDA_WASDE", date_source=f"page:{WASDE_URL}", time_source=f"page:{WASDE_URL}"))
    for d, src in (history_dates or []):
        rows.append(_row(d, "12:00", NY, event="USDA_WASDE", date_source=src, time_source="rule:12:00 ET (USDA)"))
    return _frame(rows)


# ------------------------------------------------------------------------------------------------------------ index rebalances
SP_SRC = "https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-us-indices.pdf (quarterly rebalance, third Friday of Mar/Jun/Sep/Dec, effective after the close)"
RUSSELL_SRC = "https://www.lseg.com/en/ftse-russell/ (annual reconstitution, fourth Friday of June; 2026: June 26 and December 11 per LSEG press release 2026-09-01)"
MSCI_SRC = "https://www.msci.com/index-review (index reviews effective at the close of the last business day of Feb/May/Aug/Nov)"


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> pd.Timestamp:
    first = pd.Timestamp(year, month, 1)
    return first + pd.Timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def build_index_rebalance(start_year: int = 2010, end_year: int = 2027) -> pd.DataFrame:
    rows = []
    for y in range(start_year, end_year + 1):
        for m in (3, 6, 9, 12):
            rows.append(_row(_nth_weekday(y, m, 4, 3), "16:00", NY, event="SPX_quarterly_rebalance", date_source=f"rule:{SP_SRC}", time_source="rule:US close"))
        rows.append(_row(_nth_weekday(y, 6, 4, 4), "16:00", NY, event="Russell_reconstitution", date_source=f"rule:{RUSSELL_SRC}", time_source="rule:US close"))
        for m in (2, 5, 8, 11):
            last = pd.Timestamp(y, m, 1) + pd.offsets.BMonthEnd(0)
            rows.append(_row(last, "16:00", NY, event="MSCI_index_review", date_source=f"rule:{MSCI_SRC}", time_source="rule:US close"))
    rows.append(_row(pd.Timestamp(2026, 12, 11), "16:00", NY, event="Russell_reconstitution", date_source="page:LSEG press release 2026-09-01 (semi-annual, rank day 2026-10-30)", time_source="rule:US close"))
    return _frame(rows)


# ------------------------------------------------------------------------------------------------------------ LBMA
LBMA_SRC = "https://www.lbma.org.uk/prices-and-data/precious-metal-prices (fetched 2026-11-04); launch dates: lbma.org.uk articles 2015-03-23 (gold), LBMA OTC guide (silver 2014-08-14, Pt/Pd 2014-12-01)"


def build_lbma() -> pd.DataFrame:
    rows = [
        _row("2015-03-20", "10:30", LON, event="LBMA_gold_AM", administrator="IBA", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2015-03-20", "15:00", LON, event="LBMA_gold_PM", administrator="IBA", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2014-08-14", "12:00", LON, event="LBMA_silver", administrator="IBA (CME/Thomson Reuters at launch)", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2014-12-01", "09:45", LON, event="LBMA_platinum_AM", administrator="IBA (LME at launch)", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2014-12-01", "14:00", LON, event="LBMA_platinum_PM", administrator="IBA (LME at launch)", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2014-12-01", "09:45", LON, event="LBMA_palladium_AM (starts when platinum concludes)", administrator="IBA", source=LBMA_SRC, date_source="launch date", time_source="page"),
        _row("2014-12-01", "14:00", LON, event="LBMA_palladium_PM (starts when platinum concludes)", administrator="IBA", source=LBMA_SRC, date_source="launch date", time_source="page"),
    ]
    df = pd.DataFrame(rows)
    return df.sort_values(["ts", "event"]).reset_index(drop=True)


# ------------------------------------------------------------------------------------------------------------ driver
def _land(ds: str, df: pd.DataFrame, source: str, notes: str, dry_run: bool, manifest=None) -> dict:
    return common.land(ds, df, f"calendars/{ds}.csv", fmt="csv", source=source, licence_status="free", resolution="event",
                       tz_note="ts = release instant in UTC; date_local/time_local/tz as published", notes=notes, dry_run=dry_run, manifest=manifest)


def run(only=None, *, dry_run: bool = False, manifest=None) -> dict:
    only = set(only or ["fomc", "bls", "eia", "wasde", "index", "lbma"])
    out = {}
    today = common.today()
    if "fomc" in only:
        out["cal_fomc"] = _land("cal_fomc", build_fomc(dry_run), f"{INHERITED_NOTE}; {FOMC_CAL_URL}",
                                f"statement releases; times per Fed release 2013-03-13; 2026-07.. appended from fomccalendars.htm fetched {today}; unscheduled meetings flagged scheduled=False", dry_run, manifest)
    if "bls" in only:
        for ev, ds in (("CPI", "cal_bls_cpi"), ("NFP", "cal_bls_nfp")):
            out[ds] = _land(ds, build_bls(ev), INHERITED_NOTE,
                            f"BLS {ev} 08:30 ET release dates via ALFRED (inherited pull 2026-10-11); bls.gov 403 and ALFRED/FRED unreachable on {today}: not refreshed", dry_run, manifest)
    if "eia" in only:
        out["cal_eia_wpsr"] = _land("cal_eia_wpsr", build_eia_wpsr(), f"{EIA_WPSR_ARCHIVE}; {EIA_WPSR_SCHEDULE}",
                                    f"dates from the EIA archive (2011-08-03..) fetched {today}, earlier by rule; times exact for 2025-2026 exceptions, else rule (Wed 10:30 ET)", dry_run, manifest)
        out["cal_eia_ngsr"] = _land("cal_eia_ngsr", build_eia_ngsr(), EIA_NGSR_SCHEDULE,
                                    f"Thursday 10:30 ET by rule; 2025-2026 holiday exceptions exact (page fetched {today}); earlier holiday weeks flagged holiday_week=True, real date unverified", dry_run, manifest)
    if "wasde" in only:
        out["cal_wasde"] = _land("cal_wasde", build_wasde(), WASDE_URL,
                                 f"2026-2027 dates from usda.gov (fetched {today}); history NOT landed: usda.gov data pages answered 403 and the ESMIS archive is pending", dry_run, manifest)
    if "index" in only:
        out["cal_index_rebalance"] = _land("cal_index_rebalance", build_index_rebalance(), f"{SP_SRC}; {RUSSELL_SRC}; {MSCI_SRC}",
                                           "rule-generated effective dates (US close); verify against the index providers' announcements before a registered row depends on a specific date", dry_run, manifest)
    if "lbma" in only:
        out["cal_lbma_auctions"] = _land("cal_lbma_auctions", build_lbma(), LBMA_SRC, "auction times in London local time (ts = launch date + auction time); times valid from launch to today", dry_run, manifest)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    run([s for s in a.only.split(",") if s] or None, dry_run=a.dry_run)


if __name__ == "__main__":
    main()
