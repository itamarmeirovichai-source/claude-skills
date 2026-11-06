"""Outcome-free clock diagnostic (inherited loader_spec TESTS; briefs/inherited-method-lessons.md "Clock and DST").

Idea: intraday |returns| have a stable spike at scheduled New York events (the 08:30 ET US releases, the 09:30 ET
cash open). Under a clock that follows New York DST the spike sits at the same NY wall-clock minute in winter and in
summer; under a fixed-offset clock (EST all year, or UTC) it moves by 60 minutes between the two. Nothing about any
strategy is used, only mean |1-minute return| by minute of day.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

WINTER = (1, 2)      # months in which New York is on standard time
SUMMER = (6, 7)      # months in which New York is on daylight time
US_OPEN_WINDOW_NY = (8 * 60 + 15, 9 * 60 + 45)   # 08:15–09:45 NY wall clock: 08:30 releases and the 09:30 cash open


def minute_profile(local_ts: pd.Series, close: pd.Series, months, clip_q: float = None) -> pd.Series:
    """Mean |1m log return| by local minute of day over the given months (NaN-safe, same-day returns only).
    clip_q: cap |r| at that quantile first (robust to a few bad prints; None = plain mean, the original behaviour)."""
    t = pd.DatetimeIndex(local_ts)
    r = np.log(pd.Series(close.to_numpy(dtype=float))).diff().to_numpy()
    same_day = np.r_[False, (t.normalize()[1:] == t.normalize()[:-1])]
    m = t.month.isin(months) & same_day & np.isfinite(r)
    mod = (t.hour * 60 + t.minute).to_numpy()
    a = np.abs(r[m])
    if clip_q is not None and len(a):
        a = np.minimum(a, np.quantile(a, clip_q))
    s = pd.Series(a).groupby(mod[m]).mean()
    return s.reindex(range(1440))


def _peak(profile: pd.Series, lo: int, hi: int) -> int:
    seg = profile.iloc[lo:hi]
    return int(seg.idxmax()) if seg.notna().any() else -1


def diagnose_local(local_ts: pd.Series, close: pd.Series) -> dict:
    """For a NAIVE local-time stamp whose zone is unknown. Searches the 07:15–09:45 window so a fixed-EST clock (spike
    at 07:30 clock time in summer) is caught. verdict: 'ny_dst' when the winter and summer peaks coincide (|shift| <= 5),
    'est_fixed' when the summer peak is ~60 min EARLIER on the clock, 'utc_fixed' when ~60 min earlier and the winter
    peak sits 5 h later than 08:30, else 'unclear'."""
    lo, hi = 7 * 60 + 15, 9 * 60 + 45
    w = minute_profile(local_ts, close, WINTER)
    s = minute_profile(local_ts, close, SUMMER)
    wp, sp = _peak(w, lo, hi), _peak(s, lo, hi)
    shift = sp - wp if wp >= 0 and sp >= 0 else None
    if shift is None:
        verdict = "unclear"
    elif abs(shift) <= 5:
        verdict = "ny_dst"
    elif -70 <= shift <= -50:
        verdict = "est_fixed"
    else:
        verdict = "unclear"
    return {"winter_peak": wp, "summer_peak": sp, "shift_minutes": shift, "verdict": verdict,
            "winter_peak_value": float(w.iloc[wp]) if wp >= 0 else float("nan"),
            "summer_peak_value": float(s.iloc[sp]) if sp >= 0 else float("nan")}


def diagnose_utc(ts_utc: pd.Series, close: pd.Series) -> dict:
    """For a dataset already in UTC: convert to New York wall clock and require the 08:15–09:45 peak to coincide in winter
    and summer (|shift| <= 5 min). A failure means the conversion was wrong (e.g. a fixed offset was applied)."""
    ny = pd.DatetimeIndex(pd.to_datetime(ts_utc, utc=True)).tz_convert("America/New_York").tz_localize(None)
    lo, hi = US_OPEN_WINDOW_NY
    w = minute_profile(pd.Series(ny), close, WINTER)
    s = minute_profile(pd.Series(ny), close, SUMMER)
    wp, sp = _peak(w, lo, hi), _peak(s, lo, hi)
    shift = sp - wp if wp >= 0 and sp >= 0 else None
    ok = shift is not None and abs(shift) <= 5
    return {"winter_peak_ny_minute": wp, "summer_peak_ny_minute": sp, "shift_minutes": shift, "ok": ok}


def fmt_minute(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}" if m is not None and m >= 0 else "n/a"


# ------------------------------------------------------------------------------------------------ non-US anchors (batch 1b)
CLOCKS = {"ny_dst": "America/New_York", "est_fixed": "Etc/GMT+5"}


def predicted_clock_minute(anchor_tz: str, anchor_minute: int, clock: str, season: str) -> int:
    """Clock minute of day at which an event fixed at `anchor_minute` wall-clock in `anchor_tz` appears in a file
    stamped with `clock` ('ny_dst' or 'est_fixed'), on a mid-January ('winter') or mid-July ('summer') weekday."""
    day = "2019-01-16" if season == "winter" else "2019-07-17"
    t = (pd.Timestamp(day) + pd.Timedelta(minutes=anchor_minute)).tz_localize(anchor_tz).tz_convert(CLOCKS[clock])
    return int(t.hour * 60 + t.minute)


def diagnose_anchor(local_ts: pd.Series, close: pd.Series, anchor_tz: str, anchor_minute: int,
                    half_window: int = 25, tol: int = 5) -> dict:
    """Second outcome-free clock test for an instrument whose home market opens at a fixed local time (Hong Kong 09:15,
    Tokyo 09:00, Frankfurt/Paris 09:00, London 08:00). The open's |return| spike is located in winter (Jan–Feb) and in
    summer (Jun–Jul) inside a window spanning both hypotheses' predicted clock minutes; the hypothesis whose predicted
    winter->summer shift matches the observed shift (within `tol` minutes) wins. Asian opens (no DST) move +60 min on a
    NY-with-DST clock and stay put on a fixed-EST clock; European opens (DST aligned with the US in Jan and Jul) stay
    put on a NY-with-DST clock and move -60 min on a fixed-EST clock. Uses mean |1m return| by minute only, with |r|
    capped at its 99.9th percentile (HKXHKD 2010-2018 carries bad prints that otherwise own the winter peak)."""
    preds = {h: (predicted_clock_minute(anchor_tz, anchor_minute, h, "winter"),
                 predicted_clock_minute(anchor_tz, anchor_minute, h, "summer")) for h in CLOCKS}
    allp = [m for p in preds.values() for m in p]
    lo, hi = max(0, min(allp) - half_window), min(1440, max(allp) + half_window + 1)
    w = minute_profile(local_ts, close, WINTER, clip_q=0.999)
    s = minute_profile(local_ts, close, SUMMER, clip_q=0.999)
    wp, sp = _peak(w, lo, hi), _peak(s, lo, hi)
    shift = sp - wp if wp >= 0 and sp >= 0 else None
    verdict = "unclear"
    if shift is not None:
        hits = [h for h, (pw, ps) in preds.items() if abs(shift - (ps - pw)) <= tol and abs(wp - pw) <= half_window]
        if len(hits) == 1:
            verdict = hits[0]
    return {"anchor": f"{anchor_tz} {fmt_minute(anchor_minute)}", "winter_peak": wp, "summer_peak": sp,
            "shift_minutes": shift, "predicted": {h: {"winter": p[0], "summer": p[1]} for h, p in preds.items()},
            "verdict": verdict}


def combine(us: dict, anchor: dict = None) -> tuple:
    """(verdict, status): both agree / one unclear -> the clear one; both unclear -> ny_dst default ('default');
    disagreement -> ny_dst with status 'conflict' (the inherited measurement), to be resolved by hand."""
    vs = [d["verdict"] for d in (us, anchor) if d]
    known = {v for v in vs if v in CLOCKS}
    if len(known) == 1:
        v = known.pop()
        return v, ("agree" if all(x == v for x in vs) and len(vs) > 1 else "single")
    if not known:
        return "ny_dst", "default"
    return "ny_dst", "conflict"


# ------------------------------------------------------------------------------------------------ US/EU DST-mismatch weeks
# Jan–Feb vs Jun–Jul cannot tell a New-York-DST clock from a clock that follows the EUROPEAN DST rule (EST/EDT switched
# on the EU dates, i.e. Europe/Berlin wall clock minus 6 h): both are UTC-5 in winter and UTC-4 in summer. They differ
# only in the 2-3 weeks a year when the US is on DST and the EU is not (2nd Sunday of March -> last Sunday of March;
# last Sunday of October -> 1st Sunday of November). Measured 2026-11-06 (batch 1b QA): HistData files follow the NY
# rule through 2018 and the EU rule from 2019 (SPXUSD daily halt 16:14 vs 15:14 NY in every mismatch window 2019-2024;
# 08:30 ET CPI/NFP spikes at -60 min on EURUSD/USDJPY in every decisive mismatch event 2019-2024, 0 min before).
# third clock hypothesis, "eu_dst" = Europe/Berlin wall clock - 6 h (see clock_to_utc)
HISTDATA_EU_RULE_FROM = 2019         # first local calendar year stamped on the EU-DST rule


def clock_to_utc(local: pd.Series, clock: str) -> pd.Series:
    """Naive clock stamps -> tz-aware UTC under one hypothesis (NaT where the stamp does not exist / is ambiguous)."""
    loc = pd.to_datetime(local)
    if clock == "ny_dst":
        return loc.dt.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
    if clock == "est_fixed":
        return loc.dt.tz_localize("Etc/GMT+5").dt.tz_convert("UTC")
    if clock == "eu_dst":
        return (loc + pd.Timedelta(hours=6)).dt.tz_localize("Europe/Berlin", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
    raise ValueError(clock)


def is_mismatch(ts_utc) -> np.ndarray:
    """True where New York's UTC offset minus Berlin's is not -6 h (the US/EU DST-mismatch weeks)."""
    t = pd.DatetimeIndex(pd.to_datetime(ts_utc, utc=True))
    ny = t.tz_convert("America/New_York").tz_localize(None)
    be = t.tz_convert("Europe/Berlin").tz_localize(None)
    return np.asarray((ny - be) != pd.Timedelta(hours=-6))


def diagnose_mismatch_events(local_ts: pd.Series, close: pd.Series, events_utc, window: int = 90, tol: int = 2) -> dict:
    """For each scheduled New York release (e.g. 08:30 ET CPI/NFP) that falls in a mismatch week, compare the largest
    |1m return| at -60, 0 and +60 min from where a NY-DST clock would stamp it: the release at 0 -> 'ny_dst', at -60 ->
    'eu_dst' (rules in the body; `offset` = argmax within ±window, for the record).
    Outcome-free (location of the spike only). Returns per-event offsets and per-year votes."""
    loc = pd.DatetimeIndex(pd.to_datetime(local_ts)).as_unit("ns")
    c = pd.Series(close).to_numpy(dtype=float)
    r = np.abs(np.r_[np.nan, np.diff(np.log(c))])
    r[np.r_[True, np.diff(loc.asi8) > 5 * 60_000_000_000]] = np.nan
    s = pd.Series(r, index=loc)
    ev = pd.DatetimeIndex(pd.to_datetime(pd.Series(events_utc), utc=True))
    ev = ev[is_mismatch(ev)]
    rows = []
    for e in ev:
        pred = e.tz_convert("America/New_York").tz_localize(None)      # where a NY-DST clock stamps the release
        w = s[pred - pd.Timedelta(minutes=window): pred + pd.Timedelta(minutes=window)]
        if w.notna().sum() < window:
            continue
        off = int((w.idxmax() - pred).total_seconds() // 60)

        def v(k):   # largest |r| within ±tol minutes of pred + k
            x = w[pred + pd.Timedelta(minutes=k - tol): pred + pd.Timedelta(minutes=k + tol)]
            return float(x.max()) if x.notna().any() else 0.0
        a, b, c2 = v(-60), v(0), v(60)
        # a = where a one-hour-early file puts the release; b = where a correct file puts it; c2 = one hour later
        # (the 09:30 cash open for equity CFDs: on a correct file it is at +60, on an early file at 0, so the open
        # cannot fake a vote: an early file needs a >= 1.5 c2, a correct one b >= 1.5 a with c2 not dead)
        if b >= 1.5 * a and c2 >= 0.5 * a:
            vote = "ny_dst"
        elif a >= 1.5 * c2 and a >= b / 1.5:
            vote = "eu_dst"
        else:
            vote = "none"
        rows.append({"event": e, "offset": off, "vote": vote})
    df = pd.DataFrame(rows, columns=["event", "offset", "vote"])
    years = {}
    for y, g in df.groupby(df["event"].dt.year) if len(df) else []:
        years[int(y)] = {"ny_dst": int((g["vote"] == "ny_dst").sum()), "eu_dst": int((g["vote"] == "eu_dst").sum()),
                         "none": int((g["vote"] == "none").sum())}
    return {"events": df, "years": years}


def rule_check(mm: dict, switch_year: int = HISTDATA_EU_RULE_FROM) -> dict:
    """Agreement of decisive mismatch-event votes with the rule 'ny_dst before switch_year, eu_dst from it'."""
    agree = disagree = 0
    bad = []
    for y, v in mm["years"].items():
        exp = "eu_dst" if y >= switch_year else "ny_dst"
        oth = "ny_dst" if exp == "eu_dst" else "eu_dst"
        agree += v[exp]
        disagree += v[oth]
        if v[oth]:
            bad.append(y)
    return {"agree": agree, "disagree": disagree, "undecided": sum(v["none"] for v in mm["years"].values()), "years_disagreeing": bad}
