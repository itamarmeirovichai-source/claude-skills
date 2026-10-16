"""G2 (wave 4): short-term mean reversion across 10 FTMO index CFDs.

Implements agents/prereg/G2_rules.md exactly (pre-registered in 6107458).
Data: Yahoo chart API daily open/close, cached in $G2_CACHE (default ./cache, not committed).

usage: python3 meanrev.py            -> prints the full report (run.txt)
"""
import json
import os
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("G2_CACHE", HERE / "cache"))
BAR = 3.5914
IS_END, OOS_START = "2012-12-31", "2013-01-01"

# CFD, yahoo, long swap %/yr, short swap %/yr (FTMO JSON 2026-10-12, G2_rules §0), cost per side (bp)
MKT = [
    ("US500", "^GSPC", -8.28, +0.42, 1.0),
    ("US100", "^NDX", -8.29, +0.42, 1.0),
    ("US30", "^DJI", -8.25, +0.42, 1.0),
    ("GER40", "^GDAXI", -6.50, -0.07, 1.0),
    ("UK100", "^FTSE", -8.22, +0.38, 1.0),
    ("JP225", "^N225", -4.88, -1.63, 1.5),
    ("FRA40", "^FCHI", -6.50, -0.07, 2.0),
    ("AUS200", "^AXJO", -7.74, -0.84, 2.5),
    ("EU50", "^STOXX50E", -6.50, -0.07, 3.0),
    ("HK50", "^HSI", -6.70, +0.07, 4.0),
]
NAMES = [m[0] for m in MKT]

VARIANTS = {
    "G2-01": dict(rule="rsi", ls=False, trend=False),
    "G2-02": dict(rule="down3", ls=False, trend=False),
    "G2-03": dict(rule="rsi", ls=True, trend=False),
    "G2-04": dict(rule="down3", ls=True, trend=False),
    "G2-05": dict(rule="rsi", ls=False, trend=True),
    "G2-06": dict(rule="down3", ls=False, trend=True),
    "G2-07": dict(rule="rsi", ls=True, trend=True),
}
RISK = 0.10 / np.sqrt(252) / 10          # per-position daily risk budget (fraction of book)


# ── data ───────────────────────────────────────────────────────────────
def yahoo(ticker):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{ticker.strip('^')}.json"
    if not p.exists():
        url = (f"https://query2.finance.yahoo.com/v8/finance/chart/%5E{ticker.strip('^')}"
               "?period1=0&period2=1800000000&interval=1d")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        for i in range(4):
            try:
                p.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                break
            except Exception:                                   # noqa: BLE001
                time.sleep(2 ** (i + 1))
    d = json.loads(p.read_bytes())["chart"]["result"][0]
    off = d["meta"].get("gmtoffset", 0)
    ts = pd.to_datetime(np.array(d["timestamp"]) + off, unit="s").normalize()
    q = d["indicators"]["quote"][0]
    df = pd.DataFrame({"open": np.array(q["open"], float), "close": np.array(q["close"], float)},
                      index=ts)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df[(df.close > 0)].dropna(subset=["close"])
    return df[df.index >= "1989-01-01"]


def load():
    return {n: yahoo(t) for n, t, *_ in MKT}


# ── signals (one market) ───────────────────────────────────────────────
def rsi2(c):
    d = c.diff()
    up, dn = d.clip(lower=0), (-d).clip(lower=0)
    au = _wilder(up, 2)          # Wilder smoothing alpha = 1/2, seeded with the first 2 changes
    ad = _wilder(dn, 2)
    rs = au / ad
    r = 100 - 100 / (1 + rs)
    r[(ad == 0) & (au > 0)] = 100.0
    r[(ad == 0) & (au == 0)] = 50.0
    return r


def _wilder(x, n):
    v = x.values.astype(float)
    out = np.full(len(v), np.nan)
    if len(v) <= n:
        return pd.Series(out, index=x.index)
    out[n] = np.nanmean(v[1:n + 1])
    for i in range(n + 1, len(v)):
        out[i] = out[i - 1] + (v[i] - out[i - 1]) / n
    return pd.Series(out, index=x.index)


def positions(df, rule, ls, trend):
    """Signed position (+1/-1/0) held from the close of t, decided with closes <= t,
    and the notional fixed at entry. Returns (pos, notional) as arrays on df.index."""
    c = df.close
    n = len(c)
    r = c.pct_change()
    sig = r.rolling(60).std().values
    sma5 = c.rolling(5).mean().values
    sma200 = c.rolling(200).mean().values
    cv = c.values
    if rule == "rsi":
        x = rsi2(c).values
        long_e, short_e = x < 10, x > 90
    else:
        dn = (c.diff() < 0).values
        up = (c.diff() > 0).values
        long_e = dn & np.roll(dn, 1) & np.roll(dn, 2)
        short_e = up & np.roll(up, 1) & np.roll(up, 2)
        long_e[:3] = short_e[:3] = False
    pos = np.zeros(n)
    notl = np.zeros(n)
    cur, held, w = 0, 0, 0.0
    for t in range(n):
        if t < 199 or not np.isfinite(sig[t]) or sig[t] <= 0:
            cur, held, w = 0, 0, 0.0
            continue
        if cur != 0:
            held += 1
            ex = (cv[t] > sma5[t]) if cur > 0 else (cv[t] < sma5[t])
            if ex or held >= 5:
                cur, held, w = 0, 0, 0.0
                pos[t], notl[t] = 0, 0.0
                continue                      # no re-entry on the exit day
        if cur == 0:
            if long_e[t] and (not trend or cv[t] > sma200[t]):
                cur, held, w = 1, 0, RISK / sig[t]
            elif ls and short_e[t] and (not trend or cv[t] < sma200[t]):
                cur, held, w = -1, 0, RISK / sig[t]
        pos[t], notl[t] = cur, w
    return pos, notl


# ── P&L (one market) ───────────────────────────────────────────────────
def pnl(df, pos, notl, swap_l, swap_s, cost_bp, mode, cmult=1.0, swap_on=True, cost_on=True):
    """Daily P&L (fraction of book) of one market, indexed by df.index.
    mode 'close': exposure decided at close t is filled at close t.
    mode 'open' : filled at the open of t+1 (its close if that open is invalid)."""
    c, o = df.close.values, df.open.values
    n = len(c)
    e = pos * notl                               # target signed notional after the close of t
    pc = np.r_[np.nan, c[:-1]]
    ovalid = np.isfinite(o) & (o > 0) & (np.abs(o - pc) > 1e-9 * c) & (np.abs(o - c) > 1e-9 * c)
    r_cc = np.r_[0.0, c[1:] / c[:-1] - 1]
    r_on = np.where(ovalid, o / pc - 1, 0.0)
    r_id = np.where(ovalid, c / np.where(ovalid, o, 1.0) - 1, 0.0)
    gross = np.zeros(n)
    if mode == "close":
        held = np.r_[0.0, e[:-1]]                # exposure over (t-1 close, t close]
        gross = held * r_cc
        trade = np.abs(np.diff(np.r_[0.0, e]))  # traded at close t
        night = np.abs(e) > 0                     # held through close t
        night_e = e
    else:
        # exposure carried into day t from close t-1 is the PREVIOUS executed exposure;
        # at day t's fill point it switches to e[t-1].
        prev_exec = np.zeros(n)                   # executed exposure after day t
        ex = 0.0
        trade = np.zeros(n)
        for t in range(n):
            tgt = e[t - 1] if t >= 1 else 0.0
            if t == 0:
                prev_exec[t] = 0.0
                continue
            if ovalid[t]:
                gross[t] = ex * r_on[t] + tgt * r_id[t]
            else:
                gross[t] = ex * r_cc[t]           # fill at today's close instead
            trade[t] = abs(tgt - ex)
            ex = tgt
            prev_exec[t] = ex
        night_e = prev_exec
        night = np.abs(night_e) > 0
    idx = df.index
    nights = np.r_[np.diff(idx.values).astype("timedelta64[D]").astype(float), 1.0]
    sw = np.where(night_e > 0, swap_l, np.where(night_e < 0, swap_s, 0.0)) / 100 / 365
    swap = np.abs(night_e) * sw * nights * night  # negative rate = cost (sign kept)
    cost = trade * cost_bp * 1e-4
    net = gross + (swap * cmult if swap_on else 0.0) - (cost * cmult if cost_on else 0.0)
    return pd.DataFrame(dict(gross=gross, net=net, swap=swap, cost=cost, trade=trade,
                             expo=night_e, absexpo=np.abs(night_e),
                             entry=(np.abs(np.diff(np.r_[0.0, pos])) > 0) & (pos != 0)),
                        index=idx)


def book(data, var, mode, cmult=1.0, swap_on=True, cost_on=True, cut=None):
    """Pooled daily book. Returns DataFrame on the union calendar (missing = 0)."""
    parts, bench, full = {}, {}, {}
    for name, _, sl, ss, cb in MKT:
        df = data[name] if cut is None else data[name].loc[:cut]
        pos, notl = positions(df, **VARIANTS[var])
        p = pnl(df, pos, notl, sl, ss, cb, mode, cmult, swap_on, cost_on)
        parts[name] = p
        sig = df.close.pct_change().rolling(60).std()
        w = (RISK / sig).where(np.arange(len(df)) >= 199)
        bench[name] = (w.shift(1) * df.close.pct_change()).fillna(0.0)
        full[name] = w.fillna(0.0)
    cal = sorted(set().union(*[p.index for p in parts.values()]))
    out = pd.DataFrame(index=pd.DatetimeIndex(cal))
    for k in ("gross", "net", "swap", "cost", "trade", "expo", "absexpo", "entry"):
        out[k] = sum(parts[n][k].reindex(out.index).fillna(0).astype(float) for n in NAMES)
    out["bench"] = sum(bench[n].reindex(out.index).fillna(0) for n in NAMES)
    out["fullw"] = sum(full[n].reindex(out.index).ffill().fillna(0) for n in NAMES)
    first = max(min(p.index[200] for p in parts.values() if len(p) > 200), pd.Timestamp("1990-01-02"))
    return out.loc[first:]


# ── statistics ─────────────────────────────────────────────────────────
def nw_t(x, lags=10):
    x = np.asarray(x, float)
    n = len(x)
    u = x - x.mean()
    s = u @ u / n
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (u[L:] @ u[:-L]) / n
    return x.mean() / np.sqrt(s / n)


def tstat(x):
    x = np.asarray(x, float)
    ti = x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    return min(ti, nw_t(x)), ti, nw_t(x)


def block_p5(x, block=10, reps=10000, seed=0):
    x = np.asarray(x, float)
    n = len(x)
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(reps, nb))
    cs = np.r_[0.0, np.cumsum(x)]
    sums = (cs[starts + block] - cs[starts]).sum(1)
    return np.percentile(sums / (nb * block), 5)


def ols_alpha(y, x, lags=10):
    y, x = np.asarray(y, float), np.asarray(x, float)
    X = np.c_[np.ones_like(x), x]
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    n = len(y)
    Xe = X * e[:, None]
    S = Xe.T @ Xe / n
    for L in range(1, lags + 1):
        G = Xe[L:].T @ Xe[:-L] / n
        S += (1 - L / (lags + 1)) * (G + G.T)
    Q = np.linalg.inv(X.T @ X / n)
    V = Q @ S @ Q / n
    return b[0], b[1], b[0] / np.sqrt(V[0, 0])


def sharpe(x):
    x = np.asarray(x, float)
    return x.mean() / x.std(ddof=1) * np.sqrt(252) if x.std() > 0 else 0.0


def maxdd(x):
    eq = np.cumprod(1 + np.asarray(x, float))
    return (eq / np.maximum.accumulate(eq) - 1).min()


def summarize(b):
    x = b.net.values
    t, ti, tn = tstat(x)
    ex = (b.expo / b.fullw.replace(0, np.nan)).fillna(0).mean()
    a, beta, at = ols_alpha(x, b.bench.values)
    resid = x - beta * b.bench.values
    yrs = len(x) / 252
    return dict(days=len(x), mean_bp=x.mean() * 1e4, t=t, t_iid=ti, t_nw=tn, sharpe=sharpe(x),
                ret_yr=x.mean() * 252, vol=x.std(ddof=1) * np.sqrt(252), p5_bp=block_p5(x) * 1e4,
                mdd=maxdd(x), worst=x.min(), alpha_bp=a * 1e4, beta=beta, alpha_t=at,
                resid_sharpe=sharpe(resid), expo=ex, bench_sharpe=sharpe(b.bench.values),
                bench_t=tstat(b.bench.values * ex)[0],
                matched_ret_yr=(b.bench.values * ex).mean() * 252,
                trades_yr=b.entry.sum() / yrs, gross_sharpe=sharpe(b.gross.values),
                swap_yr=b.swap.mean() * 252, cost_yr=b.cost.mean() * 252)


def per_year(b):
    g = b.net.groupby(b.index.year)
    return pd.DataFrame(dict(ret=g.sum(), sharpe=g.apply(sharpe), days=g.size()))


# ── look-ahead tests ───────────────────────────────────────────────────
def lookahead(data, var, mode, n=20, seed=1):
    rng = np.random.default_rng(seed)
    ref = book(data, var, mode)
    dates = ref.index[(ref.index > "1995-01-01") & (ref.index < ref.index[-10])]
    cuts = rng.choice(dates, n, replace=False)
    ok_t = ok_p = 0
    for d in cuts:
        d = pd.Timestamp(d)
        tr = book(data, var, mode, cut=d)
        a, b_ = ref.expo.loc[:d].iloc[:-1], tr.expo.loc[:d].iloc[:-1]
        ok_t += np.allclose(a.values, b_.reindex(a.index).fillna(0).values)
        pert = {}
        for k, df in data.items():
            df2 = df.copy()
            m = df2.index > d
            noise = np.exp(np.cumsum(rng.normal(0, 0.02, m.sum())))
            last = df2.close[~m].iloc[-1] if (~m).any() else 1.0
            df2.loc[m, "close"] = last * noise
            df2.loc[m, "open"] = last * noise * np.exp(rng.normal(0, 0.005, m.sum()))
            pert[k] = df2
        pb = book(pert, var, mode)
        ok_p += np.allclose(a.values, pb.expo.reindex(a.index).fillna(0).values)
    return ok_t, ok_p


def run_all(data):
    res = {}
    for v in VARIANTS:
        for mode in ("close", "open"):
            b = book(data, v, mode)
            b2 = book(data, v, mode, cmult=2.0)
            b0 = book(data, v, mode, swap_on=False, cost_on=False)
            bs = book(data, v, mode, swap_on=False)
            res[(v, mode)] = dict(
                IS=summarize(b.loc[:IS_END]), OOS=summarize(b.loc[OOS_START:]),
                OOS2=summarize(b2.loc[OOS_START:]), OOS0=summarize(b0.loc[OOS_START:]),
                OOSns=summarize(bs.loc[OOS_START:]), book=b, book2=b2)
    return res
