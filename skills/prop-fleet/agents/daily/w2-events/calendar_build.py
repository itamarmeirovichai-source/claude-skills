#!/usr/bin/env python3
"""E2 event calendar, built only from official / free sources (fetched 2026-10-11).

Sources (every date in events.csv traces to one of these):
  FOMC   federalreserve.gov/monetarypolicy/fomchistorical{2010..2020}.htm (meeting headings,
         "(unscheduled)" / "(cancelled)" tags, minutes "Released <date>") and
         federalreserve.gov/monetarypolicy/fomccalendars.htm (2021..2026 statement links).
         Statement TIME: 14:00 ET from 2013-03-20 on (Fed press release 2013-03-13,
         federalreserve.gov/newsevents/pressreleases/monetary20130313a.htm: "Committee policy
         statements for all regularly scheduled meetings will now be released at 2 p.m.").
         Before that: press-conference meetings (Apr 2011..Dec 2012) use the time printed on
         federalreserve.gov/monetarypolicy/fomcpresconf<date>.htm ("Released ... at 12:30 p.m.");
         all other meetings 14:15 ET (the pre-2013 convention the 2013-03-13 release replaced;
         checked against the 1m data by clock_check.py, which reads no trade outcome).
  CPI    ALFRED release dates, rid=10 (alfred.stlouisfed.org/release/downloaddates?rid=10).
         February months with two dates: the earlier one is the seasonal-factor revision, dropped.
  NFP    ALFRED rid=50 (Employment Situation). Months with two dates: keep the first (the
         second ones are benchmark / annual-revision postings).
  PCE    ALFRED rid=54 (Personal Income and Outlays). All dates kept (08:30, pre-open).
  RETAIL ALFRED rid=9 (Advance Monthly Sales for Retail and Food Services). All dates kept.
  ISM    ISM Manufacturing PMI: first business day of the month, 10:00 ET (ISM Report On
         Business calendar rule, ismworld.org rob-report-calendar). Not on FRED/ALFRED since
         2016, so built by rule: first NYSE weekday that is not a US federal holiday.
  BLS's own schedule pages (bls.gov/schedule) return "Access Denied" (HTTP 403) from this
  session: reported, not routed around; ALFRED carries the same BLS release dates.

Writes events.csv: date,event,time_et,scheduled
"""
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0"}
_M = ["January", "February", "March", "April", "May", "June", "July",
      "August", "September", "October", "November", "December"]
MON = {m: i for i, m in enumerate(_M, 1)}
MON.update({m[:3]: i for i, m in enumerate(_M, 1)})
MON.update({"Sept": 9})


def get(url: str) -> str:
    """curl (ALFRED drops urllib connections without a response; curl is served normally)."""
    import subprocess
    r = subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-m", "60", url],
                       capture_output=True, check=True)
    return r.stdout.decode("utf-8", "replace")


def text(h: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


def fomc_historical(y: int):
    t = text(get(f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm"))
    out, minutes = [], []
    # headings like "January 27-28 Meeting - 2015", "April 30-May 1 Meeting - 2013",
    # "March 2 (unscheduled) Meeting - 2020", "October 31-November 1 Meeting - 2017"
    for m in re.finditer(r"([A-Z][a-z]+) (\d+)(?:-(?:([A-Z][a-z]+) )?(\d+))?( \((?:unscheduled|cancelled)\))? Meeting - (\d{4})", t):
        mo1, d1, mo2, d2, tag, yy = m.groups()
        if int(yy) != y or mo1 not in MON:
            continue
        mo = MON[mo2] if mo2 else MON[mo1]
        dd = int(d2) if d2 else int(d1)
        out.append((date(y, mo, dd), not tag))
    for m in re.finditer(r"Released ([A-Z][a-z]+)\.? (\d+), (\d{4})", t):
        if m.group(1) not in MON:
            continue
        minutes.append(date(int(m.group(3)), MON[m.group(1)], int(m.group(2))))
    return out, minutes


def fomc_recent():
    """Scheduled meetings from the year sections of fomccalendars.htm: statement day = last day of
    the "Month dd-dd" (or "Apr/May 30-1") range. Other monetary*a.htm links on the page (e.g.
    2025-08-22 longer-run-goals statement) are not meetings and are ignored."""
    h = get("https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", h))
    parts = re.split(r"(\d{4}) FOMC Meetings", t)
    st, unsched = [], False
    for y, body in zip(parts[1::2], parts[2::2]):
        y = int(y)
        for m in re.finditer(r"\|([A-Z][a-z]+)(?:/([A-Z][a-z]+))?\|\| \|(\d+)(?:-(\d+))?\*?( \(unscheduled\))?\|", body):
            mo1, mo2, d1, d2, un = m.groups()
            if mo1 not in MON:
                continue
            if un:
                unsched = True
                continue
            mo = MON[mo2] if mo2 else MON[mo1]
            st.append(date(y, mo, int(d2 or d1)))
    mins = [date(int(m.group(3)), MON[m.group(1)], int(m.group(2)))
            for m in re.finditer(r"Released ([A-Z][a-z]+)\.? (\d+), (\d{4})", text(h)) if m.group(1) in MON]
    return sorted(set(st)), mins, unsched


def presconf_time(d: date):
    try:
        t = text(get(f"https://www.federalreserve.gov/monetarypolicy/fomcpresconf{d:%Y%m%d}.htm"))
    except Exception:
        return None
    m = re.search(r"Released [A-Z][a-z]+ \d+, \d{4} at (\d+):(\d+) (a|p)\.m\.", t)
    if not m:
        return None
    hh, mm = int(m.group(1)), int(m.group(2))
    if m.group(3) == "p" and hh != 12:
        hh += 12
    return f"{hh:02d}:{mm:02d}"


def alfred(rid: int):
    t = get(f"https://alfred.stlouisfed.org/release/downloaddates?rid={rid}&ff=txt")
    return sorted({date.fromisoformat(s) for s in re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", t)})


def fed_holidays(y0, y1):
    from pandas.tseries.holiday import USFederalHolidayCalendar
    return {d.date() for d in USFederalHolidayCalendar().holidays(f"{y0}-01-01", f"{y1}-12-31")}


def main():
    rows = []
    # FOMC
    for y in range(2010, 2021):
        meets, mins = fomc_historical(y)
        for d, sched in meets:
            rows.append((d, "FOMC", None, sched))
        for d in mins:
            rows.append((d, "FOMC_MINUTES", "14:00", True))
    st, mins, unsched = fomc_recent()
    if unsched:
        print("WARNING: fomccalendars.htm mentions an unscheduled meeting; check by hand", file=sys.stderr)
    for d in st:
        if d.year >= 2021 and d <= date(2026, 10, 11):
            rows.append((d, "FOMC", None, True))
    for d in mins:
        if d.year >= 2021 and d <= date(2026, 10, 11):
            rows.append((d, "FOMC_MINUTES", "14:00", True))
    fixed = []
    for d, ev, tm, sched in rows:
        if ev == "FOMC":
            if d >= date(2013, 3, 20):
                tm = "14:00"
            else:
                pt = presconf_time(d) if d >= date(2011, 4, 1) else None
                tm = pt if pt else "14:15"
                if pt == "12:20":      # 2012-01-25 page typo; statement went out 12:30 (clock_check.py)
                    tm = "12:30"
        fixed.append((d, ev, tm, sched))
    rows = fixed
    # ALFRED releases
    cpi = alfred(10)
    keep = []
    for d in cpi:
        same = [x for x in cpi if (x.year, x.month) == (d.year, d.month)]
        if d.month == 2 and len(same) > 1 and d != max(same):
            continue
        keep.append(d)
    rows += [(d, "CPI", "08:30", True) for d in keep]
    nfp = alfred(50)
    rows += [(d, "NFP", "08:30", True) for d in nfp
             if d == min(x for x in nfp if (x.year, x.month) == (d.year, d.month))]
    rows += [(d, "PCE", "08:30", True) for d in alfred(54)]
    rows += [(d, "RETAIL", "08:30", True) for d in alfred(9)]
    hol = fed_holidays(2010, 2026)
    for y in range(2010, 2027):
        for m in range(1, 13):
            d = date(y, m, 1)
            while d.weekday() >= 5 or d in hol:
                d += timedelta(days=1)
            rows.append((d, "ISM", "10:00", True))
    df = pd.DataFrame(rows, columns=["date", "event", "time_et", "scheduled"])
    df = df[(df.date >= date(2010, 1, 1)) & (df.date <= date(2026, 10, 11))]
    df = df.drop_duplicates().sort_values(["date", "event"])
    df.to_csv(HERE / "events.csv", index=False)
    print(df.groupby([pd.to_datetime(df.date).dt.year, "event"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
