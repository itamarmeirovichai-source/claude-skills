"""Outcome-free Data QA for HistData 1-minute datasets (batch 1b): bar counts against the instrument's cash session,
gaps, stale prints, outliers, OHLC sanity, the post-conversion clock check, inherited-pin provenance and daily
cross-source agreement. Writes quant-edge/data/qa/<dataset_id>.md.

Nothing about any strategy is computed. For a HOLD-OUT dataset (`*_holdout`, ts >= paths.HOLDOUT_START) the report is
structural only: counts, coverage, gaps, flat-bar shares, outlier COUNTS and the clock peak minutes; no price level,
no return value and no cross-source correlation is computed or printed.
"""
from __future__ import annotations

import csv
import zipfile
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from .. import paths
from . import clock as qclock

NY = "America/New_York"
# cash session per symbol: exchange_calendars name, or "CMES23" = the 23-hour futures-style day 18:00 -> 17:00 ET
SESSION = {"SPXUSD": "XNYS", "NSXUSD": "XNYS", "HKXHKD": "XHKG", "JPXJPY": "XTKS", "ETXEUR": "XETR", "GRXEUR": "XETR",
           "FRXEUR": "XPAR", "UKXGBP": "XLON", "XAUUSD": "CMES23", "BCOUSD": "CMES23", "WTIUSD": "CMES23",
           "EURUSD": "CMES23", "GBPUSD": "CMES23", "USDJPY": "CMES23", "AUDUSD": "CMES23"}
# post-conversion clock anchors: (zone, minute) whose spike must sit at the same wall-clock minute in winter and summer
ANCHOR_UTC = {"HKXHKD": ("Asia/Hong_Kong", 9 * 60 + 15), "JPXJPY": ("Asia/Tokyo", 9 * 60), "ETXEUR": ("Europe/Berlin", 8 * 60),
              "GRXEUR": ("Europe/Berlin", 9 * 60), "FRXEUR": ("Europe/Paris", 8 * 60), "UKXGBP": ("Europe/London", 8 * 60)}
# daily cross-source: (manifest dataset, column, sampling zone, sampling minute = the bar CLOSE time, label)
XSOURCE = {
    "SPXUSD": [("spx_oc_1990_2026", "close", NY, 16 * 60, "S&P 500 cash close (^GSPC)"),
               ("daily_assets_1970_2026", "USLCAP", NY, 16 * 60, "US large-cap index level")],
    "NSXUSD": [("daily_assets_1970_2026", "USLCAP", NY, 16 * 60, "US large-cap index level (Nasdaq-100 vs broad US)"),
               ("spx_oc_1990_2026", "close", NY, 16 * 60, "S&P 500 cash close")],
    "XAUUSD": [("daily_assets_1970_2026", "GOLDPM", "Europe/London", 15 * 60, "LBMA gold PM price")],
    "BCOUSD": [("daily_assets_1970_2026", "CMDTY", NY, 16 * 60, "broad commodity index (loose)")],
    "WTIUSD": [("daily_assets_1970_2026", "CMDTY", NY, 16 * 60, "broad commodity index (loose)")],
    "ETXEUR": [("daily_assets_1970_2026", "GLSTOCK", NY, 16 * 60, "global equity index (loose; EUR vs USD)")],
    "GRXEUR": [("daily_assets_1970_2026", "GLSTOCK", NY, 16 * 60, "global equity index (loose; EUR vs USD)")],
    "FRXEUR": [("daily_assets_1970_2026", "GLSTOCK", NY, 16 * 60, "global equity index (loose; EUR vs USD)")],
    "UKXGBP": [("daily_assets_1970_2026", "GLSTOCK", NY, 16 * 60, "global equity index (loose; GBP vs USD)")],
    "HKXHKD": [("daily_assets_1970_2026", "GLSTOCK", "Asia/Hong_Kong", 16 * 60, "global equity index (loose; Asia close precedes US)")],
    "JPXJPY": [("daily_assets_1970_2026", "GLSTOCK", "Asia/Tokyo", 15 * 60, "global equity index (loose; Asia close precedes US)")],
}
# inherited per-CSV pins (FutureSharks/financial-data copy of HistData; ~/quant-edge-inherited/pr4/skills/prop-fleet/
# agents/daily/w1-breadth/manifest.csv and orb-H0020/loaders.py, measured 2026-10-06)
INHERITED_PINS_FILE = Path.home() / "quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-breadth/manifest.csv"


# hand-written auditor notes (2026-11-06), printed in the report
COMMON_NOTE = ("2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD "
               "also appear on the FX files (WORK-LOG 3.1).")
AUDITOR_NOTES = {
    "GRXEUR": "Bars 2020-06-15 06:00 .. 2023-12-01 20:59 UTC (637,707) are EXCLUDED: the HistData GRXEUR files carry Euro Stoxx 50 "
              "levels (2,908-4,490) there, while DAX sits at 12,011 before and 16,429 after. Hence the months without bars and the "
              "one level break across the hole. The excluded span is NOT landed as an ETXEUR substitute (provenance is a guess).",
    "ETXEUR": "HistData offers no ETXEUR file from 2020 (the year pages serve an empty download token) and the 2019 file stops "
              "2019-02-01; from 2018-12-17 07:00 UTC the file jumps to 8,880-9,222 (not Euro Stoxx 50; IBEX-like), so those "
              "22,163 bars are EXCLUDED. Usable span 2010-11-15 .. 2018-12-14; no hold-out part.",
    "WTIUSD": "HistData offers no WTIUSD file for 2024 and 2025 or for 2026-01..05 (empty tokens); IS ends 2023-12-01 and the hold-out "
              "part is 2026-06-28 .. 2026-10-30 only. The two level breaks are real: the 2020-03-09 OPEC+ gap and the 2020-04-19 "
              "CFD roll after the negative-price May contract.",
    "XAUUSD": "GOLDPM in daily_assets_1970_2026 correlates 0.63 at lag 0 and 0.38 at lag +1, stable in every year 2010-2024: the "
              "second source mixes same-day and next-day dating. XAUUSD's clock checks pass, so the shortfall is attributed to GOLDPM.",
    "HKXHKD": "GLSTOCK is a loose, US-timed check: an Asian close precedes the US close, so lag +1 carries as much as lag 0. "
              "The 2010-2018 winter profile has bad prints near the open (robust anchor still shifts 12 min); the US anchor and "
              "the mismatch-week releases place the clock correctly.",
    "JPXJPY": "GLSTOCK is a loose, US-timed check: the Tokyo close precedes the US close (lag +1 0.43 > lag 0).",
    "UKXGBP": "From 2019 the daily halt sits at 16:14 NY in aligned weeks and ~16:59 in mismatch weeks: the CFD's halt follows the "
              "London clock (capped by the 17:00 NY close), not a clock error; the release votes put the clock right (16 vs 0). "
              "The Jan-Feb vs Jun-Jul US-anchor peaks compete (09:31 vs 08:30); the London 08:00 open anchor is stable.",
    "BCOUSD": "Coverage is measured against the 18:00->17:00 ET template; the Brent CFD keeps ICE-like hours, so ~85% is its own "
              "session length, not missing data.",
    "SPXUSD": "This dataset also supersedes the inherited SPXUSD 2010-18 (FutureSharks copy): the yearly CSVs are byte-identical.",
}


# ----------------------------------------------------------------------------------------------------------- helpers
def manifest_row(dataset_id: str) -> dict:
    with open(paths.MANIFEST_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["dataset_id"] == dataset_id:
                return r
    raise KeyError(dataset_id)


def load(dataset_id: str) -> pd.DataFrame:
    df = pd.read_parquet(paths.DATA_ROOT / manifest_row(dataset_id)["path"])
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df.sort_values("ts").reset_index(drop=True)


def _ns(ts) -> np.ndarray:
    return pd.DatetimeIndex(pd.to_datetime(ts, utc=True)).as_unit("ns").asi8


def trading_minutes(ts) -> np.ndarray:
    """Minutes on a clock that skips the FX/CFD weekend (Fri 17:00 -> Sun 17:00 New York)."""
    ny = pd.DatetimeIndex(pd.to_datetime(ts, utc=True)).tz_convert(NY).tz_localize(None) + pd.Timedelta(hours=7)
    days = (ny - pd.Timestamp("2000-01-03")).total_seconds().to_numpy() / 60.0      # 2000-01-03 is a Monday
    week = np.floor(days / 10080.0)
    inweek = np.clip(days - week * 10080.0, 0, 7200)
    return week * 7200 + inweek


def gaps(ts, min_trading_minutes: int = 1440) -> pd.DataFrame:
    """Gaps between consecutive bars longer than `min_trading_minutes` of weekday market time."""
    ts = pd.DatetimeIndex(pd.to_datetime(ts, utc=True))
    if len(ts) < 2:
        return pd.DataFrame(columns=["after", "before", "trading_days"])
    tm = trading_minutes(ts)
    d = np.diff(tm)
    idx = np.where(d > min_trading_minutes)[0]
    return pd.DataFrame({"after": ts[idx], "before": ts[idx + 1], "trading_days": d[idx] / 1440.0}).sort_values(
        "trading_days", ascending=False).reset_index(drop=True)


def missing_months(ts) -> list:
    ts = pd.DatetimeIndex(pd.to_datetime(ts, utc=True))
    if not len(ts):
        return []
    have = set(ts.tz_convert(NY).strftime("%Y-%m"))
    allm = pd.period_range(ts.min().tz_convert(NY).strftime("%Y-%m"), ts.max().tz_convert(NY).strftime("%Y-%m"), freq="M")
    return [str(m) for m in allm if str(m) not in have]


def gap_note(df: pd.DataFrame) -> str:
    """One-line gap summary for the manifest notes."""
    g = gaps(df["ts"])
    mm = missing_months(df["ts"])
    top = "; ".join(f"{r.after:%Y-%m-%d}..{r.before:%Y-%m-%d} {r.trading_days:.1f}d" for r in g.head(3).itertuples())
    return (f"{len(g)} gaps > 1 weekday-trading-day (longest: {top or 'none'}); "
            f"months without bars: {','.join(mm) if mm else 'none'}")


# ----------------------------------------------------------------------------------------------------------- sessions
def session_table(cal: str, start, end) -> pd.DataFrame:
    """One row per cash session: open/close UTC and the break (NaT if none)."""
    start = pd.Timestamp(start).tz_localize(None).normalize()
    end = pd.Timestamp(end).tz_localize(None).normalize()
    if cal == "CMES23":
        import exchange_calendars as xc
        s = xc.get_calendar("CMES", start=max(start, pd.Timestamp("2010-01-04")).strftime("%Y-%m-%d"),
                            end=end.strftime("%Y-%m-%d")).schedule
        s = s.loc[(s.index >= start) & (s.index <= end)].copy()
        s["close"] = s["open"] + pd.Timedelta(hours=23)        # 18:00 ET -> 17:00 ET; short days keep the library close
        out = s[["open", "close"]].copy()
        lib = xc.get_calendar("CMES", start=max(start, pd.Timestamp("2010-01-04")).strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d")).schedule
        lib = lib.loc[out.index]
        out["close"] = np.minimum(out["close"].to_numpy(), lib["close"].to_numpy())
        out["close"] = pd.to_datetime(out["close"], utc=True)
        out["break_start"] = pd.NaT
        out["break_end"] = pd.NaT
        return out
    import exchange_calendars as xc
    s = xc.get_calendar(cal, start=max(start, pd.Timestamp("2010-01-04")).strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d")).schedule
    return s.loc[(s.index >= start) & (s.index <= end), ["open", "close", "break_start", "break_end"]]


def session_coverage(df: pd.DataFrame, cal: str) -> pd.DataFrame:
    """Per session: expected minutes, bars present, coverage, missing-run stats, flat-bar share, stale runs, close."""
    if df.empty:
        return pd.DataFrame()
    st = session_table(cal, df["ts"].iloc[0].tz_convert(NY).normalize().tz_localize(None),
                       df["ts"].iloc[-1].tz_convert(NY).normalize().tz_localize(None))
    t = _ns(df["ts"])
    o, h, l, c = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    rows = []
    one = 60_000_000_000
    for day, r in st.iterrows():
        segs = []
        if pd.notna(r["break_start"]) and pd.notna(r["break_end"]):
            segs = [(r["open"], r["break_start"]), (r["break_end"], r["close"])]
        else:
            segs = [(r["open"], r["close"])]
        exp = np.concatenate([np.arange(pd.Timestamp(a).value, pd.Timestamp(b).value, one) for a, b in segs])
        i0, i1 = np.searchsorted(t, exp[0]), np.searchsorted(t, exp[-1], side="right")
        tt = t[i0:i1]
        present = np.isin(exp, tt)
        n = int(present.sum())
        # missing runs
        miss = ~present
        runs = []
        if miss.any():
            edges = np.diff(np.r_[0, miss.astype(int), 0])
            starts, ends = np.where(edges == 1)[0], np.where(edges == -1)[0]
            runs = (ends - starts).tolist()
        sel = np.isin(tt, exp)
        oo, hh, ll, cc = o[i0:i1][sel], h[i0:i1][sel], l[i0:i1][sel], c[i0:i1][sel]
        flat = int(((oo == hh) & (hh == ll) & (ll == cc)).sum())
        opc = int((oo[1:] == cc[:-1]).sum()) if len(cc) > 1 else 0
        # stale runs: >= 15 consecutive bars with an unchanged close
        stale15 = 0
        if len(cc) > 15:
            same = np.r_[False, cc[1:] == cc[:-1]].astype(int)
            e2 = np.diff(np.r_[0, same, 0])
            s2, e2_ = np.where(e2 == 1)[0], np.where(e2 == -1)[0]
            stale15 = int(((e2_ - s2) >= 14).sum())
        rows.append({"session": day, "expected": len(exp), "bars": n, "coverage": n / len(exp),
                     "runs_ge5": sum(1 for x in runs if x >= 5), "runs_ge30": sum(1 for x in runs if x >= 30),
                     "longest_run": max(runs) if runs else 0, "flat": flat, "open_eq_prev_close": opc,
                     "stale_runs_15": stale15, "last_close": float(cc[-1]) if len(cc) else np.nan})
    return pd.DataFrame(rows)


def hour_profile(df: pd.DataFrame, year: Optional[int] = None) -> str:
    """Share of NY weekdays that carry at least one bar in each NY hour (0..23), as a compact string."""
    ny = pd.DatetimeIndex(df["ts"]).tz_convert(NY)
    m = ny.dayofweek < 5
    if year is not None:
        m &= ny.year == year
    if not m.any():
        return "n/a"
    d = pd.DataFrame({"day": ny[m].normalize(), "hour": ny[m].hour}).drop_duplicates()
    ndays = d["day"].nunique()
    share = d.groupby("hour")["day"].count().reindex(range(24), fill_value=0) / ndays
    return " ".join(f"{h:02d}:{int(round(100 * v)):d}" for h, v in share.items())


# ----------------------------------------------------------------------------------------------------------- returns-level checks
def ohlc_sanity(df: pd.DataFrame) -> dict:
    o, h, l, c = (df[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
    return {"nan": int(np.isnan(np.c_[o, h, l, c]).any(axis=1).sum()), "nonpositive": int(((np.c_[o, h, l, c]) <= 0).any(axis=1).sum()),
            "high_below_oc": int((h < np.maximum(o, c) - 1e-12).sum()), "low_above_oc": int((l > np.minimum(o, c) + 1e-12).sum()),
            "dup_ts": int(df["ts"].duplicated().sum()), "nonzero_volume": int((df["volume"] != 0).sum()) if "volume" in df else 0}


def outliers(df: pd.DataFrame, k: float = 20.0, floor: float = 0.005) -> dict:
    """1-minute close-to-close log moves between bars <= 5 min apart: |r| > max(k * that year's median |r|, floor).
    spike_reversal = an outlier followed by a move back of >= 80% of it (an isolated bad print)."""
    t = _ns(df["ts"])
    c = df["close"].to_numpy(dtype=float)
    r = np.r_[np.nan, np.diff(np.log(c))]
    near = np.r_[False, np.diff(t) <= 5 * 60_000_000_000]
    r = np.where(near, r, np.nan)
    yr = pd.DatetimeIndex(df["ts"]).year.to_numpy()
    med = pd.Series(np.abs(r)).groupby(yr).transform(lambda s: s[s > 0].median()).to_numpy()
    thr = np.maximum(k * med, floor)
    flag = np.abs(r) > thr
    nxt = np.r_[r[1:], np.nan]
    rev = flag & (np.sign(nxt) == -np.sign(r)) & (np.abs(nxt) >= 0.8 * np.abs(r))
    idx = np.where(flag)[0]
    top = sorted(idx, key=lambda i: -abs(r[i]))[:10]
    return {"n": int(flag.sum()), "spike_reversals": int(rev.sum()),
            "top": [(df["ts"].iloc[i], float(r[i]) * 1e4, bool(rev[i])) for i in top],
            "max_range_bp": float(np.nanmax((df["high"] - df["low"]) / df["close"]) * 1e4) if len(df) else float("nan")}


def level_breaks(df: pd.DataFrame, thr: float = 0.25) -> list:
    """Bar-to-bar |log move| > thr (25%): a mislabelled file segment or a real crash/roll; listed for review."""
    c = df["close"].to_numpy(dtype=float)
    lr = np.r_[np.nan, np.diff(np.log(c))]
    idx = np.where(np.abs(lr) > thr)[0]
    return [(df["ts"].iloc[i - 1], df["ts"].iloc[i], float(lr[i])) for i in idx]


def daily_closes(df: pd.DataFrame, tz: str, minute: int) -> pd.Series:
    """Close of the last bar whose CLOSE time (open + 1 min) is <= `minute` wall-clock in `tz`, per local date, taken
    only when that bar closes within 15 minutes of `minute` (otherwise the date is skipped)."""
    loc = pd.DatetimeIndex(df["ts"]).tz_convert(tz).tz_localize(None) + pd.Timedelta(minutes=1)
    mod = loc.hour * 60 + loc.minute
    m = (mod <= minute) & (mod > minute - 15) & (loc.dayofweek < 5)
    s = pd.Series(df["close"].to_numpy()[m], index=loc[m].normalize())
    return s.groupby(level=0).last()


def cross_source(df: pd.DataFrame, sym: str) -> list:
    from . import xsource
    out = []
    for ds, col, tz, minute, label in XSOURCE.get(sym, []):
        try:
            hd = daily_closes(df, tz, minute)
            if len(hd) < 50:
                continue
            start, end = hd.index.min().strftime("%Y-%m-%d"), hd.index.max().strftime("%Y-%m-%d")
            other = xsource.second_source_returns(ds, col, start, end)
            if ds == "daily_assets_1970_2026":
                obs = xsource.second_source_returns(ds, f"obs_{col}", start, end)
                other = other[obs.reindex(other.index).fillna(0) > 0]
            j = pd.concat([hd.rename("hd"), other.rename("o")], axis=1, join="inner").dropna()
            j = j[(j > 0).all(axis=1)]
            rh, ro = np.log(j["hd"]).diff(), np.log(j["o"]).diff()
            res = xsource.compare(rh.dropna(), ro.dropna())
            res.update({"dataset": ds, "column": col, "label": label, "sample": f"{tz} {qclock.fmt_minute(minute)}",
                        "start": start, "end": end})
            if ds == "spx_oc_1990_2026":
                ratio = (j["hd"] / j["o"])
                res["level_ratio_median"] = float(ratio.median())
                res["level_ratio_p01_p99"] = (float(ratio.quantile(0.01)), float(ratio.quantile(0.99)))
                d = (rh - ro).abs().dropna()
                res["abs_ret_diff_bp_median"] = float(d.median() * 1e4)
                res["abs_ret_diff_bp_p99"] = float(d.quantile(0.99) * 1e4)
            out.append(res)
        except Exception as e:  # noqa: BLE001
            out.append({"dataset": ds, "column": col, "label": label, "error": str(e)[:200]})
    return out


def clock_check_utc(df: pd.DataFrame, sym: str) -> dict:
    """After conversion: the US 08:30/09:30 ET spike and the home-market open must sit at the same wall-clock minute in
    winter and in summer (|shift| <= 5)."""
    res = {"us": qclock.diagnose_utc(df["ts"], df["close"])}
    if sym in ANCHOR_UTC:
        tz, minute = ANCHOR_UTC[sym]
        loc = pd.Series(pd.DatetimeIndex(df["ts"]).tz_convert(tz).tz_localize(None))
        w = qclock.minute_profile(loc, df["close"], qclock.WINTER, clip_q=0.999)
        s = qclock.minute_profile(loc, df["close"], qclock.SUMMER, clip_q=0.999)
        lo, hi = max(0, minute - 25), min(1440, minute + 26)
        wp, sp = qclock._peak(w, lo, hi), qclock._peak(s, lo, hi)
        shift = sp - wp if wp >= 0 and sp >= 0 else None
        res["anchor"] = {"anchor": f"{tz} {qclock.fmt_minute(minute)}", "winter_peak": wp, "summer_peak": sp,
                         "shift_minutes": shift, "ok": shift is not None and abs(shift) <= 5}
    return res


def mismatch_check_utc(df: pd.DataFrame) -> dict:
    """After conversion: 08:30 ET CPI/NFP spikes in US/EU DST-mismatch weeks must sit at offset 0 (NY wall clock), and
    the modal start of the daily halt (intraday gap 20-600 min, Mon-Thu, NY) must be the same in aligned and mismatch
    weeks. Outcome-free (locations only)."""
    from ..ingest import histdata
    ny_local = pd.Series(pd.DatetimeIndex(df["ts"]).tz_convert(NY).tz_localize(None))
    ev = histdata.us_release_events()
    mm = qclock.diagnose_mismatch_events(ny_local, df["close"], ev) if len(ev) else {"events": pd.DataFrame(), "years": {}}
    votes = mm["events"]["vote"].value_counts().to_dict() if len(mm["events"]) else {}
    t = pd.DatetimeIndex(df["ts"])
    ny = t.tz_convert(NY)
    gap = np.r_[np.diff(_ns(t)) / 60e9, 0]
    mis = qclock.is_mismatch(t)
    mod = (ny.hour * 60 + ny.minute).to_numpy()
    base = (ny.dayofweek.to_numpy() < 4) & (gap >= 20) & (gap < 600)
    per_year = {}
    for y in sorted(set(ny.year)):
        ym = ny.year.to_numpy() == y
        a_ = pd.Series(mod[base & ym & ~mis]).value_counts()
        m_ = pd.Series(mod[base & ym & mis]).value_counts()
        if a_.sum() >= 5 and m_.sum() >= 3:
            d = int(m_.index[0]) - int(a_.index[0])
            per_year[int(y)] = (qclock.fmt_minute(int(a_.index[0])), qclock.fmt_minute(int(m_.index[0])),
                                "same" if abs(d) <= 2 else ("hour" if 55 <= abs(d) <= 65 else "other"))
    halts = {}
    for era, em in (("2010-2018", ny.year.to_numpy() < qclock.HISTDATA_EU_RULE_FROM), (f"{qclock.HISTDATA_EU_RULE_FROM}+", ny.year.to_numpy() >= qclock.HISTDATA_EU_RULE_FROM)):
        for nm, mk in (("aligned", ~mis), ("mismatch", mis)):
            m = base & em & mk
            if m.sum():
                vc = pd.Series(mod[m]).value_counts()
                halts[(era, nm)] = (qclock.fmt_minute(int(vc.index[0])), int(vc.iloc[0]), int(m.sum()))
    return {"votes": votes, "n_events": int(len(mm["events"])), "offsets": mm["events"], "halts": halts, "halts_by_year": per_year}


def inherited_pin_check(sym: str) -> list:
    """Compare sha256 of the CSV inside our raw HistData zips with the inherited per-CSV pins (same vendor files)."""
    from ..ingest import histdata
    if not INHERITED_PINS_FILE.exists():
        return []
    pins = {}
    with open(INHERITED_PINS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0] == sym and "DAT_ASCII" in row[1]:
                y = int(row[1].rsplit("_", 1)[1][:4])
                pins[y] = row[3]
    out = []
    for y, pin in sorted(pins.items()):
        z = histdata.raw_zip_path(sym, y)
        if not z.exists():
            out.append((y, pin[:12], "no raw zip", False))
            continue
        try:
            sha = histdata.inner_csv_sha256(z)
        except zipfile.BadZipFile:
            sha = "bad zip"
        out.append((y, pin[:12], sha[:12], sha == pin))
    return out


# ----------------------------------------------------------------------------------------------------------- report
def _pct(x) -> str:
    return f"{100 * x:.1f}%"


def report(dataset_id: str, sym: str, *, out_dir: Optional[Path] = None) -> dict:
    holdout = dataset_id.endswith("_holdout")
    man = manifest_row(dataset_id)
    df = load(dataset_id)
    cal = SESSION.get(sym, "CMES23")
    cov = session_coverage(df, cal)
    g = gaps(df["ts"])
    mm = missing_months(df["ts"])
    san = ohlc_sanity(df)
    lb = level_breaks(df)
    outl = outliers(df)
    clk = clock_check_utc(df, sym)
    mmc = mismatch_check_utc(df)
    xs = [] if holdout else cross_source(df, sym)
    pinchk = [] if holdout else inherited_pin_check(sym)
    ny = pd.DatetimeIndex(df["ts"]).tz_convert(NY)
    weekend = int(((ny.dayofweek == 5) | ((ny.dayofweek == 4) & (ny.hour >= 17)) | ((ny.dayofweek == 6) & (ny.hour < 17))).sum())

    L = [f"# QA — {dataset_id}", "",
         f"Data QA Auditor, Department C, {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC. Outcome-free: no strategy, signal or P&L is computed."
         + (" **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation)." if holdout else ""),
         "", f"- path `DATA_ROOT/{man['path']}`; rows {int(man['rows']):,}; {man['start']} .. {man['end']} (UTC); sha256 `{man['sha256'][:16]}…`",
         f"- source {man['source']}; licence {man['licence_status']}",
         f"- manifest notes: {man['notes']}", ""]

    # verdict items computed first, written at the top
    issues = []
    if not cov.empty:
        full = cov[cov["bars"] > 0]
        zero = int((cov["bars"] == 0).sum())
        med_cov = float(full["coverage"].median()) if len(full) else 0.0
        share95 = float((full["coverage"] >= 0.95).mean()) if len(full) else 0.0
    else:
        full, zero, med_cov, share95 = cov, 0, 0.0, 0.0
    us_ok = clk["us"]["ok"]
    anc_ok = clk.get("anchor", {}).get("ok")
    hy = mmc["halts_by_year"]
    n_same = sum(1 for v in hy.values() if v[2] == "same")
    hour_years = [y for y, v in hy.items() if v[2] == "hour"]
    halts_ok = None if not hy else (n_same > len(hour_years) or len(hour_years) < 2)
    votes_ok = mmc["votes"].get("ny_dst", 0) > mmc["votes"].get("eu_dst", 0)
    untestable = clk["us"]["shift_minutes"] is None and "anchor" not in clk
    if untestable:
        issues.append("clock not testable on this span (no Jan–Feb or no Jun–Jul bars); conversion follows the measured HistData rule")
    elif not us_ok and not anc_ok:
        if halts_ok or votes_ok:
            issues.append("Jan–Feb vs Jun–Jul peaks differ (competing 08:30/09:30 spikes), but the mismatch-week "
                          + ("halt and " if halts_ok else "") + "release checks place the clock correctly")
        else:
            issues.append("clock check failed on every anchor")
    if halts_ok is False:
        issues.append(f"daily halt one hour off in mismatch weeks in {len(hour_years)} years ({' '.join(map(str, hour_years))})")
    if mmc["votes"].get("eu_dst", 0) > mmc["votes"].get("ny_dst", 0):
        issues.append("mismatch-week releases sit one hour early (clock rule wrong for this dataset)")
    if med_cov < 0.9:
        issues.append(f"median cash-session coverage {_pct(med_cov)}")
    if mm:
        issues.append(f"{len(mm)} months without bars")
    if san["high_below_oc"] or san["low_above_oc"] or san["nonpositive"] or san["nan"]:
        issues.append("OHLC inconsistencies")
    if lb:
        issues.append(f"{len(lb)} bar-to-bar level breaks > 25% (review: crash/roll or mislabelled segment)")
    if outl["spike_reversals"] > 20:
        issues.append(f"{outl['spike_reversals']} spike-reversal prints")
    clock_fail = any(x.startswith("clock check failed") or x.startswith("mismatch-week releases") or x.startswith("daily halt one hour") for x in issues)
    verdict = "PASS" if not issues else ("CAVEATS" if clock_fail or med_cov < 0.8 or len(issues) > 3 else "PASS with caveats")
    L += [f"## Verdict: {verdict}", ""]
    L += [f"- {x}" for x in issues] or ["- no blocking issue found"]
    L += [""]

    L += ["## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)", ""]
    u = clk["us"]
    L.append(f"- After conversion, US anchor (08:15–09:45 New York): winter peak {qclock.fmt_minute(u['winter_peak_ny_minute'])}, "
             f"summer peak {qclock.fmt_minute(u['summer_peak_ny_minute'])} NY, shift {u['shift_minutes']} min -> {'OK' if u['ok'] else 'NOT OK'}.")
    if "anchor" in clk:
        a = clk["anchor"]
        L.append(f"- After conversion, home-market anchor {a['anchor']} (±25 min): winter peak {qclock.fmt_minute(a['winter_peak'])}, "
                 f"summer peak {qclock.fmt_minute(a['summer_peak'])} local, shift {a['shift_minutes']} min -> {'OK' if a['ok'] else 'NOT OK'}.")
    v = mmc["votes"]
    L.append(f"- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): {mmc['n_events']} CPI/NFP releases; "
             f"spike at offset 0 (correct) {v.get('ny_dst', 0)}, at −60 min (one hour early) {v.get('eu_dst', 0)}, undecided {v.get('none', 0)}.")
    if len(mmc["offsets"]):
        L.append("  - offsets (min): " + " ".join(f"{r.event:%Y-%m-%d}:{r.offset}" for r in mmc["offsets"].itertuples()))
    if hy:
        L.append(f"- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): {n_same} same, "
                 f"{len(hour_years)} one hour off{(' (' + ' '.join(map(str, hour_years)) + ')') if hour_years else ''}, "
                 f"{len(hy) - n_same - len(hour_years)} other: " + " ".join(f"{y} {a}→{m}" for y, (a, m, _) in hy.items()))
    if mmc["halts"]:
        L.append("- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: "
                 + "; ".join(f"{era} {nm} {hm} ({k}/{n})" for (era, nm), (hm, k, n) in mmc["halts"].items()))
    L.append("- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, "
             "EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).")
    L.append("")

    L += [f"## Bar counts vs the cash session ({cal}{' = 18:00→17:00 ET futures-style day' if cal == 'CMES23' else ', exchange_calendars, breaks excluded'})", ""]
    if not cov.empty:
        L.append(f"- sessions in span {len(cov):,}; with ≥1 bar {len(full):,}; with no bar {zero:,}; median coverage of sessions with bars {_pct(med_cov)}; "
                 f"sessions ≥95% covered {_pct(share95)}")
        cov["year"] = pd.DatetimeIndex(cov["session"]).year
        yt = cov.groupby("year").agg(sessions=("bars", "size"), no_bar=("bars", lambda s: int((s == 0).sum())),
                                     median_cov=("coverage", lambda s: float(s[s > 0].median()) if (s > 0).any() else 0.0),
                                     ge95=("coverage", lambda s: float((s[s > 0] >= 0.95).mean()) if (s > 0).any() else 0.0),
                                     runs_ge5=("runs_ge5", "sum"), runs_ge30=("runs_ge30", "sum"))
        bars_wd = pd.Series(1, index=ny[ny.dayofweek < 5]).groupby(ny[ny.dayofweek < 5].normalize()).count()
        bpd = bars_wd.groupby(bars_wd.index.year).median()
        L += ["", "| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |",
              "|---|---|---|---|---|---|---|---|"]
        for y, r in yt.iterrows():
            L.append(f"| {y} | {int(r.sessions)} | {int(r.no_bar)} | {_pct(r.median_cov)} | {_pct(r.ge95)} | {int(r.runs_ge5)} | {int(r.runs_ge30)} | {int(bpd.get(y, 0))} |")
        worst = cov[cov["bars"] > 0].nsmallest(5, "coverage")
        L += ["", "- lowest-coverage sessions (with bars): " + "; ".join(f"{pd.Timestamp(r.session):%Y-%m-%d} {_pct(r.coverage)} (longest hole {r.longest_run} min)" for r in worst.itertuples())]
        nob = cov[cov["bars"] == 0]["session"]
        if len(nob):
            L.append(f"- sessions with no bar (first 15 of {len(nob)}): " + ", ".join(f"{pd.Timestamp(d):%Y-%m-%d}" for d in nob.head(15)))
    yrs = sorted(set(ny.year))
    prof_year = max([y for y in yrs if y < int(paths.HOLDOUT_START[:4])] or yrs)
    L += [f"- delivered hours ({prof_year}, share of NY weekdays with ≥1 bar in each NY hour, %): {hour_profile(df, prof_year)}",
          f"- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: {weekend:,}", ""]

    L += ["## Gaps (weekday market time, weekend removed)", "",
          f"- gaps > 1 trading day: {len(g)}; months without any bar: {', '.join(mm) if mm else 'none'}"]
    for r in g.head(10).itertuples():
        L.append(f"  - {r.after:%Y-%m-%d %H:%M} → {r.before:%Y-%m-%d %H:%M} UTC: {r.trading_days:.1f} trading days")
    L.append("")

    L += ["## Stale prints (inside the cash session)", ""]
    if not cov.empty and len(full):
        nb = full["bars"].sum()
        L.append(f"- flat bars (O=H=L=C): {_pct(full['flat'].sum() / nb)}; open == previous close: {_pct(full['open_eq_prev_close'].sum() / max(1, nb - len(full)))} "
                 "(HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)")
        L.append(f"- runs of ≥15 consecutive unchanged closes: {int(full['stale_runs_15'].sum())} in {int((full['stale_runs_15'] > 0).sum())} sessions")
        if not holdout:
            lc = full["last_close"].to_numpy()
            same = int((lc[1:] == lc[:-1]).sum())
            L.append(f"- sessions whose last cash-session close equals the previous session's: {same}")
    L.append("")

    L += ["## Outliers and OHLC sanity", "",
          f"- OHLC: NaN rows {san['nan']}, non-positive {san['nonpositive']}, high < max(O,C) {san['high_below_oc']}, low > min(O,C) {san['low_above_oc']}, "
          f"duplicate ts {san['dup_ts']}, non-zero volume {san['nonzero_volume']}",
          f"- 1m moves above max(20 × the year's median |move|, 50 bp): {outl['n']}; of which spike-reversals (≥80% retraced next bar): {outl['spike_reversals']}"]
    L.append(f"- bar-to-bar level breaks > 25%: {len(lb)}" + ("" if not lb else ": " + "; ".join(
        f"{a:%Y-%m-%d %H:%M} → {b:%Y-%m-%d %H:%M} UTC" + ("" if holdout else f" ({100 * x:+.0f}%)") for a, b, x in lb)))
    if not holdout:
        L.append(f"- widest single bar high–low: {outl['max_range_bp']:.0f} bp")
        for ts, bp, rev in outl["top"]:
            L.append(f"  - {ts:%Y-%m-%d %H:%M} UTC {bp:+.0f} bp{' (reversed next bar)' if rev else ''}")
    L.append("")

    if not holdout:
        L += ["## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)", ""]
        if not xs:
            L.append("- no free daily series in the manifest matches this instrument")
        for x in xs:
            if "error" in x:
                L.append(f"- {x['dataset']}.{x['column']}: error {x['error']}")
                continue
            L.append(f"- vs {x['dataset']}.{x['column']} ({x['label']}), HistData sampled at {x['sample']} bar close, {x['start']}..{x['end']}: "
                     f"n={x['n']}, corr lag−1 {x['corr_lag-1']:.3f}, lag0 {x['corr_lag+0']:.3f}, lag+1 {x['corr_lag+1']:.3f}; sd ratio other/HistData {x['sd_ratio_other_over_fx']:.2f}")
            if "level_ratio_median" in x:
                L.append(f"  - level ratio HistData/^GSPC median {x['level_ratio_median']:.4f} (p1–p99 {x['level_ratio_p01_p99'][0]:.4f}–{x['level_ratio_p01_p99'][1]:.4f}); "
                         f"|daily return difference| median {x['abs_ret_diff_bp_median']:.1f} bp, p99 {x['abs_ret_diff_bp_p99']:.1f} bp")
        L.append("")
        if pinchk:
            ok = sum(1 for p in pinchk if p[3])
            L += ["## Provenance vs inherited pins (FutureSharks/financial-data copy of the same HistData CSVs)", "",
                  f"- {ok} of {len(pinchk)} yearly CSVs byte-identical to the inherited pins: "
                  + ", ".join(f"{y} {'=' if m else '≠'}" for y, _, _, m in pinchk), ""]
    else:
        L += ["## Cross-source", "", "- not computed on hold-out data (outcome-free rule for the hold-out).", ""]

    L += ["## Auditor notes", "", f"- {COMMON_NOTE}"] + ([f"- {AUDITOR_NOTES[sym]}"] if sym in AUDITOR_NOTES else []) + [""]
    out_dir = out_dir or (paths.PROGRAM_ROOT / "data" / "qa")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{dataset_id}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return {"dataset_id": dataset_id, "verdict": verdict, "issues": issues, "us_clock_ok": us_ok, "anchor_ok": anc_ok,
            "median_cov": med_cov, "missing_months": mm, "xsource": [(x.get("dataset"), x.get("column"), x.get("corr_lag+0")) for x in xs]}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dataset_ids", nargs="+", help="e.g. histdata_cfd_1m_SPXUSD (symbol = the token after the prefix)")
    a = ap.parse_args(argv)
    for ds in a.dataset_ids:
        sym = ds.replace("_holdout", "").rsplit("_", 1)[1]
        r = report(ds, sym)
        print(f"{ds}: {r['verdict']} {r['issues']} clock_us={r['us_clock_ok']} anchor={r['anchor_ok']} cov={r['median_cov']:.3f} xs={r['xsource']}")


if __name__ == "__main__":
    main()
