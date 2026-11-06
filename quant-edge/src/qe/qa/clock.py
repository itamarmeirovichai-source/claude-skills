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


def minute_profile(local_ts: pd.Series, close: pd.Series, months) -> pd.Series:
    """Mean |1m log return| by local minute of day over the given months (NaN-safe, same-day returns only)."""
    t = pd.DatetimeIndex(local_ts)
    r = np.log(pd.Series(close.to_numpy(dtype=float))).diff().to_numpy()
    same_day = np.r_[False, (t.normalize()[1:] == t.normalize()[:-1])]
    m = t.month.isin(months) & same_day & np.isfinite(r)
    mod = (t.hour * 60 + t.minute).to_numpy()
    s = pd.Series(np.abs(r[m])).groupby(mod[m]).mean()
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
