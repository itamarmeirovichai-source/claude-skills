"""D3 crypto backtests: rules exactly as pre-registered in agents/prereg/D3.csv (commit 53539f1).

Conventions
- Daily index = UTC calendar days. A *decision* matrix D[t] holds the weights chosen with data
  through the end of day t; they are held during day t+1 (held W[t] = D[t-1]).
- Every generator takes a Data object and returns decision weights; the truncation test reruns the
  generators on Data cut at a date and checks that every decision up to the cut is unchanged.
"""
import numpy as np, pandas as pd
from dataclasses import dataclass, field

CANDS = ("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR AAVE "
         "ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM APE GALA "
         "CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
START, END = pd.Timestamp("2018-07-01"), pd.Timestamp("2026-09-30")
IS = (pd.Timestamp("2019-01-01"), pd.Timestamp("2022-12-31"))
OOS = (pd.Timestamp("2023-01-01"), pd.Timestamp("2026-09-30"))
C_PERP, C_SPOT = 0.0007, 0.00095          # per side per unit notional (fee + spread)
F_DEFAULT = 0.0003                          # 0.0001 per 8h, before a symbol has funding history
GAP_H = 72                                  # hourly gap that starts a new data segment (e.g. LUNA -> LUNA 2.0)


@dataclass
class Data:
    close: pd.DataFrame      # daily spot close (last 1h bar of the UTC day)
    qvol: pd.DataFrame       # daily quote volume
    ret: pd.DataFrame        # daily spot return, NaN across segment gaps
    age: pd.DataFrame        # days since segment start (NaN where no data)
    pclose: pd.DataFrame     # daily perp close
    pret: pd.DataFrame       # daily perp return
    fund: pd.DataFrame       # sum of funding prints in the day (NaN = no print)
    fund_n: pd.DataFrame     # number of prints in the day
    fdaily: pd.DataFrame     # funding charged per day (actual, or F_DEFAULT before history)
    h_close: pd.DataFrame    # hourly spot close
    h_ret: pd.DataFrame      # hourly spot return (NaN across gaps)
    end: pd.Timestamp = END

    def cut(self, day):
        day = pd.Timestamp(day)
        hend = day + pd.Timedelta(hours=23)
        f = lambda df: df.loc[:day]
        return Data(*(f(getattr(self, k)) for k in ("close", "qvol", "ret", "age", "pclose", "pret", "fund",
                                                      "fund_n", "fdaily")),
                    self.h_close.loc[:hend], self.h_ret.loc[:hend], day)


def load(datadir):
    days = pd.date_range(START, END, freq="D")
    hours = pd.date_range(START, END + pd.Timedelta(hours=23), freq="h")
    cl, qv, rt, ag, pc, pr, fu, fn, fd, hc, hr = ({} for _ in range(11))
    for c in CANDS:
        try:
            h = pd.read_parquet(f"{datadir}/spot1h_{c}.parquet")
        except FileNotFoundError:
            continue
        h = h.loc[START:END + pd.Timedelta(hours=23)]
        seg = (h.index.to_series().diff() > pd.Timedelta(hours=GAP_H)).cumsum()
        hcl = h.close.reindex(hours)
        hseg = seg.reindex(hours)
        hret = hcl.pct_change(fill_method=None)
        hret[hseg.ne(hseg.shift())] = np.nan
        hc[c], hr[c] = hcl, hret
        d = h.groupby(h.index.floor("D")).agg(close=("close", "last"), qvol=("qvol", "sum"))
        dseg = seg.groupby(h.index.floor("D")).last()
        d = d.reindex(days); dseg = dseg.reindex(days)
        cl[c], qv[c] = d.close, d.qvol
        r = d.close.pct_change(fill_method=None)
        r[dseg.ne(dseg.shift()) & dseg.shift().notna()] = np.nan
        rt[c] = r
        segstart = pd.Series(days, index=days).where(dseg.notna()).groupby(dseg).transform("min")
        ag[c] = (pd.Series(days, index=days) - segstart).dt.days.astype(float)
        try:
            p = pd.read_parquet(f"{datadir}/perp1d_{c}.parquet").loc[START:END]
            p = p[~p.index.duplicated()].close.reindex(days)
            pc[c], pr[c] = p, p.pct_change(fill_method=None)
        except FileNotFoundError:
            pc[c] = pr[c] = pd.Series(np.nan, index=days)
        try:
            f = pd.read_parquet(f"{datadir}/funding_{c}.parquet").iloc[:, 0]
            g = f.groupby(f.index.floor("D"))
            fs, fcount = g.sum().reindex(days), g.size().reindex(days)
            first = f.index.min().floor("D")
        except FileNotFoundError:
            fs = fcount = pd.Series(np.nan, index=days); first = END + pd.Timedelta(days=1)
        fu[c], fn[c] = fs, fcount
        fd[c] = fs.where(days >= first, F_DEFAULT).fillna(0.0)
    D = lambda x: pd.DataFrame(x)
    return Data(D(cl), D(qv), D(rt), D(ag), D(pc), D(pr), D(fu), D(fn), D(fd), D(hc), D(hr))


# ---------------------------------------------------------------- universe
def universe(data, n=25):
    """Boolean daily matrix: coin in U_m on that day (ranked once per month from data before the month)."""
    days = data.close.index
    U = pd.DataFrame(False, index=days, columns=data.close.columns)
    rank = pd.DataFrame(np.nan, index=days, columns=data.close.columns)
    qv30 = data.qvol.rolling(30, min_periods=1).sum()
    for m0 in days[days.day == 1]:
        prev = m0 - pd.Timedelta(days=1)
        if prev < days[0]:
            continue
        ok = (data.age.loc[prev] >= 180) & data.close.loc[prev].notna()
        v = qv30.loc[prev][ok].sort_values(ascending=False).head(n)
        m1 = min(m0 + pd.offsets.MonthEnd(0), days[-1])
        U.loc[m0:m1, v.index] = True
        rank.loc[m0:m1, v.index] = np.arange(1, len(v) + 1)
    return U, rank


def sigma(data):
    return data.ret.rolling(60, min_periods=60).std() * np.sqrt(365)


def drift(w, r):
    r = np.nan_to_num(r)
    g = 1 + r
    port = 1 + np.sum(w * r)
    return w * g / port if port > 0 else w * 0


# ---------------------------------------------------------------- generators (decision weights)
def tsmom_signal(data):
    c = data.close
    s = sum(np.sign(c / c.shift(L) - 1) for L in (20, 60, 120)) / 3
    valid = c.notna() & c.shift(120).notna()
    return s.where(valid)


def g_tsmom(data, longflat=False, coins=None):
    s = tsmom_signal(data)
    if longflat:
        s = s.clip(lower=0)
    lev = (0.5 / sigma(data)).clip(upper=1.5)
    if coins is None:
        Uh, _ = holding_universe(data)      # universe in force on the holding day t+1
        mask = Uh & s.notna() & lev.notna()
    else:
        mask = pd.DataFrame(False, index=s.index, columns=s.columns)
        mask[coins] = s[coins].notna() & lev[coins].notna()
    n = mask.sum(axis=1).replace(0, np.nan)
    w = (s * lev).where(mask, 0.0).div(n, axis=0).fillna(0.0)
    return w


def _next_universe_row(data, U):
    """Universe in force on day end+1, computed from data through `end` (only differs at a month end)."""
    last = data.close.index[-1]
    if (last + pd.Timedelta(days=1)).day != 1:
        return U.iloc[-1]
    qv30 = data.qvol.rolling(30, min_periods=1).sum().loc[last]
    ok = (data.age.loc[last] >= 180) & data.close.loc[last].notna()
    v = qv30[ok].sort_values(ascending=False).head(25)
    row = pd.Series(False, index=U.columns); row[v.index] = True
    return row


def holding_universe(data):
    U, rank = universe(data)
    Uh = U.shift(-1).fillna(False).astype(bool)
    Uh.iloc[-1] = _next_universe_row(data, U)
    Rh = rank.shift(-1)
    if (data.close.index[-1] + pd.Timedelta(days=1)).day == 1:
        last = data.close.index[-1]
        qv30 = data.qvol.rolling(30, min_periods=1).sum().loc[last]
        ok = (data.age.loc[last] >= 180) & data.close.loc[last].notna()
        v = qv30[ok].sort_values(ascending=False).head(25)
        r = pd.Series(np.nan, index=U.columns); r[v.index] = np.arange(1, len(v) + 1); Rh.iloc[-1] = r
    else:
        Rh.iloc[-1] = rank.iloc[-1]
    return Uh, Rh


def weekly(data, score, eligible, ret, k=5, w0=0.1, ascending=False):
    """Every Sunday decision (held from Monday): long top-k score, short bottom-k; drift between."""
    days = data.close.index
    cols = data.close.columns
    D = np.zeros((len(days), len(cols)))
    w = np.zeros(len(cols))
    R = ret.values
    sc, el = score.values, eligible.values
    for i, d in enumerate(days):
        if i > 0:
            w = drift(w, R[i])
            # a position whose market has no price today is closed (weight 0 from next day)
            w[np.isnan(R[i]) & (w != 0)] = 0.0
        if d.dayofweek == 6:
            ok = el[i] & ~np.isnan(sc[i])
            idx = np.where(ok)[0]
            w = np.zeros(len(cols))
            if len(idx) >= 2 * k:
                order = idx[np.argsort(-sc[i][idx] if not ascending else sc[i][idx], kind="stable")]
                w[order[:k]] = w0
                w[order[-k:]] = -w0
        D[i] = w
    return pd.DataFrame(D, index=days, columns=cols)


def g_xsmom(data, L):
    Uh, _ = holding_universe(data)
    c = data.close
    score = c / c.shift(L) - 1
    return weekly(data, score, Uh & c.notna(), data.ret)


def g_carry(data):
    Uh, _ = holding_universe(data)
    fsum = data.fund.rolling(7, min_periods=7).sum()
    fcnt = data.fund_n.rolling(7, min_periods=7).sum()
    fmean = fsum / fcnt
    # require >= 7 full days of funding history
    hist = data.fund_n.notna().cumsum() >= 7
    el = Uh & data.pclose.notna() & hist & fmean.notna()
    # long = lowest funding, short = highest: score = -funding, long top-k
    return weekly(data, -fmean, el, data.pret)


def g_cashcarry(data):
    """Returns (spot decision weights, perp decision weights)."""
    Uh, _ = holding_universe(data)
    f = data.fund
    # mean of the last 9 prints, approximated by the last 3 days when each day has 3 prints
    s3 = f.rolling(3, min_periods=3).sum(); n3 = data.fund_n.rolling(3, min_periods=3).sum()
    m = s3 / n3
    act = Uh & data.pclose.notna() & data.close.notna() & (m > 0.0001)
    n = act.sum(axis=1)
    w = act.astype(float).div(np.maximum(5, n), axis=0)
    return w, -w


def hour_select(data, coin="BTC"):
    r = np.log1p(data.h_ret[coin].loc[IS[0]:IS[1] + pd.Timedelta(hours=23)])
    mu = r.groupby(r.index.hour).mean()
    o = mu.sort_values()
    return list(o.index[-2:]), list(o.index[:2]), mu


def g_hour(data, coin="BTC", hours=None):
    """Hourly decision weights: weight to hold during hour h+1 (index = decision hour h)."""
    longh, shorth = hours if hours is not None else hour_select(data, "BTC")[:2]
    idx = data.h_close.index
    nxt = (idx + pd.Timedelta(hours=1)).hour
    w = np.where(np.isin(nxt, longh), 1.0, np.where(np.isin(nxt, shorth), -1.0, 0.0))
    W = pd.DataFrame(0.0, index=idx, columns=data.h_close.columns)
    W[coin] = np.where(data.h_close[coin].notna(), w, 0.0)
    return W


def g_intraday(data):
    """Hourly decision weights for D3-04."""
    _, Rh = holding_universe(data)            # rank in force on day t+1, from data through t
    top = (Rh <= 10)
    sig = sigma(data)
    lev = (0.5 / sig).clip(upper=1.5)          # as of day t (end of day), used for hours of day t+1
    hc = data.h_close
    e24 = hc.ewm(span=24, adjust=False).mean()
    e168 = hc.ewm(span=168, adjust=False).mean()
    s = np.sign(e24 - e168).where(hc.notna())
    # map daily quantities (decided at end of day t, for day t+1) onto hours of day t+1.
    # a decision at hour h is held during h+1; h+1 belongs to day floor(h+1).
    hold_day = (hc.index + pd.Timedelta(hours=1)).floor("D")
    dec_day = hold_day - pd.Timedelta(days=1)
    top_h = top.reindex(dec_day).fillna(False).astype(bool).values
    lev_h = lev.reindex(dec_day).values
    w = s.values * lev_h / 10.0
    w = np.where(top_h & ~np.isnan(w), w, 0.0)
    return pd.DataFrame(w, index=hc.index, columns=hc.columns)


# ---------------------------------------------------------------- evaluation
def evaluate(legs, fund_daily=None, hourly=False, data=None):
    """legs: list of (decision weights D, returns R, cost per side, perp: bool).
    Returns daily DataFrame with gross, cost, funding, net, turnover."""
    out = []
    for D, R, c, perp in legs:
        W = D.shift(1).fillna(0.0).values                 # held weights
        Rv = R.reindex(D.index).values
        Rz = np.nan_to_num(Rv)
        gross = np.sum(W * Rz, axis=1)
        Wd = W * (1 + Rz) / (1 + gross)[:, None]          # end-of-period drifted weights
        prev = np.vstack([np.zeros(W.shape[1]), Wd[:-1]])
        to = np.sum(np.abs(W - prev), axis=1)
        df = pd.DataFrame({"gross": gross, "to": to, "cost": c * to}, index=D.index)
        if perp:
            Wdf = pd.DataFrame(W, index=D.index, columns=D.columns)
            if hourly:
                Wday = Wdf.groupby(Wdf.index.floor("D")).mean()
                fu = (Wday * data.fdaily.reindex(Wday.index)[Wday.columns].fillna(0)).sum(axis=1)
            else:
                fu = (Wdf * data.fdaily.reindex(Wdf.index)[Wdf.columns].fillna(0)).sum(axis=1)
        else:
            fu = None
        if hourly:
            df = df.groupby(df.index.floor("D")).sum()
        df["fund"] = 0.0 if fu is None else fu.reindex(df.index).fillna(0)
        out.append(df)
    tot = sum(out)
    tot["net"] = tot.gross - tot.cost - tot.fund
    tot["net2"] = tot.gross - 2 * tot.cost - tot.fund
    return tot


def stats(x, seed=0, nboot=10000, block=20):
    x = np.asarray(x, float)
    n = len(x)
    m, s = x.mean(), x.std(ddof=1)
    t = m / (s / np.sqrt(n))
    # Newey-West lag 10
    e = x - m
    lrv = e @ e / n
    for L in range(1, 11):
        lrv += 2 * (1 - L / 11) * (e[L:] @ e[:-L]) / n
    tnw = m / np.sqrt(lrv / n)
    rng = np.random.default_rng(seed)
    bi = x[rng.integers(0, n, (nboot, n))].mean(axis=1)
    p5_iid = np.percentile(bi, 5)
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, (nboot, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    bb = x[idx.reshape(nboot, -1)[:, :n]].mean(axis=1)
    p5_blk = np.percentile(bb, 5)
    eq = np.cumprod(1 + x)
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    cagr = eq[-1] ** (365 / n) - 1 if eq[-1] > 0 else -1.0
    return dict(n=n, mean_bp=m * 1e4, t_iid=t, t_nw=tnw, t=min(t, tnw), p5_iid_bp=p5_iid * 1e4,
                p5_blk_bp=p5_blk * 1e4, p5_bp=min(p5_iid, p5_blk) * 1e4,
                sharpe=m / s * np.sqrt(365), cagr=cagr, maxdd=dd, worst=x.min(), vol=s * np.sqrt(365))
