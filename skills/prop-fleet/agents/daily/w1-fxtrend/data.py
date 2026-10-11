#!/usr/bin/env python3
"""D2 data: free daily FX (FRED H.10), OECD short rates (FRED), index CFDs and
commodity ETFs (Yahoo chart API), bond proxies built from FRED yields.

Everything is cached as raw downloads in $D2_CACHE (default: the session scratchpad),
never committed. `panel()` returns the financed daily return of every instrument,
exactly as agents/prereg/D2_rules.md sections 1-2 define it, plus the metadata the
backtest needs (class, cost per side, swap markup, margin leverage).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

CACHE = Path(os.environ.get(
    "D2_CACHE",
    "/tmp/claude-0/-home-user-claude-skills/"
    "52422590-ac2e-5d6a-916a-7bf484bde29a/scratchpad/d2data"))
START = "1987-01-01"            # warm-up: assets need 260 days before they trade
UA = {"User-Agent": "Mozilla/5.0"}

# ── currencies: USD value of one unit, from FRED H.10 ─────────────────
# (series, True if quoted as USD per unit of the currency)
FX_FRED = {
    "EUR": ("DEXUSEU", True), "GBP": ("DEXUSUK", True), "AUD": ("DEXUSAL", True),
    "NZD": ("DEXUSNZ", True), "JPY": ("DEXJPUS", False), "CHF": ("DEXSZUS", False),
    "CAD": ("DEXCAUS", False), "SEK": ("DEXSDUS", False), "NOK": ("DEXNOUS", False),
}
# short rates: primary 3m interbank, then fallbacks in order (D2_rules.md §1)
RATES = {
    "USD": ["IR3TIB01USM156N"],
    "EUR": ["IR3TIB01DEM156N"],
    "GBP": ["IR3TIB01GBM156N", "IRSTCI01GBM156N"],
    "JPY": ["IR3TIB01JPM156N", "IRSTCI01JPM156N"],
    "CHF": ["IR3TIB01CHM156N", "IRSTCI01CHM156N"],
    "CAD": ["IR3TIB01CAM156N"], "AUD": ["IR3TIB01AUM156N"],
    "NZD": ["IR3TIB01NZM156N"], "SEK": ["IR3TIB01SEM156N"],
    "NOK": ["IR3TIB01NOM156N"],
}
MAJORS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
          "USDSEK", "USDNOK"]
CROSSES = ["EURGBP", "EURJPY", "EURCHF", "GBPJPY", "AUDJPY", "EURAUD", "AUDNZD",
           "CADJPY"]
# index CFD: (yahoo, local currency for financing, fixed dividend yield)
INDICES = {
    "US500": ("^GSPC", "USD", 0.019), "US100": ("^NDX", "USD", 0.009),
    "US30": ("^DJI", "USD", 0.022), "GER40": ("^GDAXI", "EUR", 0.0),
    "UK100": ("^FTSE", "GBP", 0.036), "JP225": ("^N225", "JPY", 0.018),
    "FRA40": ("^FCHI", "EUR", 0.029), "AUS200": ("^AXJO", "AUD", 0.040),
    "EU50": ("^STOXX50E", "EUR", 0.032), "HK50": ("^HSI", "USD", 0.033),
}
COMMODS = {"XAUUSD": "GLD", "XAGUSD": "SLV", "USOIL": "USO"}
BONDS = {"US10Y": ("DGS10", 10), "US30Y": ("DGS30", 30)}

# per side bp, swap markup %/yr, margin leverage (D2_rules.md §3-4)
def _meta(cls, cost, swap, lev):
    return dict(cls=cls, cost_bps=cost, swap=swap, lev=lev)


def instrument_meta() -> pd.DataFrame:
    m = {}
    for p in MAJORS:
        m[p] = _meta("FX", 3.0 if p in ("USDSEK", "USDNOK") else 0.75, 0.010, 30)
    for p in CROSSES:
        m[p] = _meta("FX", 1.5, 0.010, 30)
    for k in INDICES:
        m[k] = _meta("IDX", 1.5, 0.025, 15)
    m["XAUUSD"] = _meta("CMD", 2.0, 0.025, 9)
    m["XAGUSD"] = _meta("CMD", 5.0, 0.025, 9)
    m["USOIL"] = _meta("CMD", 4.0, 0.025, 5)
    for k in BONDS:
        m[k] = _meta("BOND", 2.0, 0.010, 10)
    return pd.DataFrame(m).T.astype({"cost_bps": float, "swap": float, "lev": float})


# ── download with cache ───────────────────────────────────────────────
def _get(url: str, path: Path, tries=4) -> bytes:
    if path.exists() and path.stat().st_size > 0:
        return path.read_bytes()
    path.parent.mkdir(parents=True, exist_ok=True)
    err = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
            path.write_bytes(b)
            return b
        except Exception as e:                      # noqa: BLE001
            err = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"download failed {url}: {err}")


def fred(series: str) -> pd.Series:
    b = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
             CACHE / "fred" / f"{series}.csv")
    df = pd.read_csv(io.BytesIO(b))
    s = pd.to_numeric(df.iloc[:, 1], errors="coerce")
    s.index = pd.to_datetime(df.iloc[:, 0])
    return s.dropna().rename(series)


def yahoo(ticker: str) -> pd.Series:
    q = urllib.parse.quote(ticker)
    url = (f"https://query2.finance.yahoo.com/v8/finance/chart/{q}"
           "?period1=0&period2=1800000000&interval=1d&events=div,split")
    b = _get(url, CACHE / "yahoo" / f"{ticker.strip('^').replace('=', '')}.json")
    d = json.loads(b)["chart"]["result"][0]
    off = d["meta"].get("gmtoffset", 0)
    ts = pd.to_datetime(np.array(d["timestamp"]) + off, unit="s").normalize()
    ind = d["indicators"]
    if "adjclose" in ind:
        px = np.array(ind["adjclose"][0]["adjclose"], dtype=float)
    else:
        px = np.array(ind["quote"][0]["close"], dtype=float)
    s = pd.Series(px, index=ts).dropna()
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s[s > 0].rename(ticker)


def sources_sha() -> dict:
    out = {}
    for p in sorted(CACHE.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(CACHE))] = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    return out


# ── building blocks ───────────────────────────────────────────────────
def usd_value() -> pd.DataFrame:
    """USD value of one unit of each currency, FRED dates."""
    cols = {}
    for c, (sid, usd_per) in FX_FRED.items():
        s = fred(sid)
        cols[c] = s if usd_per else 1.0 / s
    return pd.DataFrame(cols).sort_index()


def calendar(v: pd.DataFrame) -> pd.DatetimeIndex:
    """Weekdays with a FRED EURUSD or GBPUSD fix (EUR only exists from 1999)."""
    ok = v["GBP"].notna() | v["EUR"].notna()
    cal = v.index[ok]
    return cal[(cal >= START) & (cal.dayofweek < 5)]


def monthly_rates(cal: pd.DatetimeIndex) -> pd.DataFrame:
    """Lagged short rates (decimal) on the calendar: the month-m value is usable from
    the first day of month m+2; spliced per RATES; last value carried forward."""
    out = {}
    for c, ids in RATES.items():
        s = None
        for sid in ids:
            x = fred(sid)
            s = x if s is None else s.combine_first(x)
        s = s.sort_index() / 100.0
        s.index = s.index.to_period("M").to_timestamp() + pd.DateOffset(months=2)
        out[c] = s.reindex(cal.union(s.index)).ffill().reindex(cal)
    return pd.DataFrame(out)


def on_cal(s: pd.Series, cal: pd.DatetimeIndex) -> pd.Series:
    """Carry a price series onto the calendar; NaN before its first real price,
    and not carried past its own last real price."""
    s = s.sort_index()
    x = s.reindex(cal.union(s.index)).ffill().reindex(cal)
    x[cal < s.index[0]] = np.nan
    return x


def pair_price(v: pd.DataFrame, pair: str) -> pd.Series:
    b, q = pair[:3], pair[3:]
    vb = v[b] if b != "USD" else 1.0
    vq = v[q] if q != "USD" else 1.0
    return vb / vq


def panel(include_bonds=True) -> dict:
    """Financed daily returns R (calendar x instruments), lagged rates, meta."""
    v = usd_value()
    cal = calendar(v)
    v = v.reindex(v.index.union(cal)).ffill().reindex(cal)
    # a currency is NaN until its first fix (EUR 1999)
    first = {c: fred(FX_FRED[c][0]).index[0] for c in FX_FRED}
    for c, d0 in first.items():
        v.loc[v.index < d0, c] = np.nan
    rates = monthly_rates(cal)
    rates["USD"] = rates["USD"]
    dcal = pd.Series(cal, index=cal).diff().dt.days.fillna(1).astype(float)
    acc = dcal / 365.0
    R, P = {}, {}
    for pair in MAJORS + CROSSES:
        px = pair_price(v, pair)
        b, q = pair[:3], pair[3:]
        R[pair] = px.pct_change(fill_method=None) + (rates[b].shift(1) - rates[q].shift(1)) * acc
        P[pair] = px
    for k, (tk, ccy, dy) in INDICES.items():
        px = on_cal(yahoo(tk), cal)
        R[k] = px.pct_change(fill_method=None) + (dy - rates[ccy].shift(1)) * acc
        P[k] = px
    for k, tk in COMMODS.items():
        px = on_cal(yahoo(tk), cal)
        R[k] = px.pct_change(fill_method=None) - rates["USD"].shift(1) * acc
        P[k] = px
    if include_bonds:
        for k, (sid, n) in BONDS.items():
            y = on_cal(fred(sid), cal) / 100.0
            y0 = y.shift(1)
            dmod = (1.0 / y0) * (1.0 - (1.0 + y0 / 2.0) ** (-2 * n))
            R[k] = y0 * acc - dmod * (y - y0) - rates["USD"].shift(1) * acc
            P[k] = y
    R = pd.DataFrame(R)
    # the very first return after an instrument appears is not a return
    for k in R:
        fv = P[k].first_valid_index()
        if fv is not None:
            R.loc[R.index <= fv, k] = np.nan
    meta = instrument_meta().loc[R.columns]
    return dict(R=R, rates=rates, meta=meta, dcal=dcal, cal=cal, P=pd.DataFrame(P))


if __name__ == "__main__":
    d = panel()
    R = d["R"]
    print("calendar", R.index[0].date(), "->", R.index[-1].date(), len(R))
    for k in R:
        s = R[k].dropna()
        big = s[s.abs() > 0.12]
        print(f"{k:8s} {s.index[0].date()} n={len(s):5d} vol={s.std()*np.sqrt(252):.3f} "
              f"max|r|={s.abs().max():.3f}" + (f"  >12%: {[(str(i.date()), round(x,3)) for i, x in big.items()][:6]}" if len(big) else ""))
    print(d["rates"].iloc[[0, 3000, 6000, -1]])
