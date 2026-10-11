#!/usr/bin/env python3
"""E1 engine: the 11 pre-registered stock-CFD variants (agents/prereg/E1_rules.md).

Signals -> weight frames W (date x ticker, set at the close of each date) plus a US500
hedge notional h. pnl() turns them into daily net returns of a gross-1 book under
FTMO costs (commission + half-spread per side, swap per calendar night).
Run: python3 stocks.py  (writes run.txt-style output to stdout)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from data import panels
from fetch import EDIR

HERE = Path(__file__).parent
IS_START, IS_END, OOS_START = "1999-04-01", "2014-12-31", "2015-01-02"
PEAD_IS_START = "2008-04-01"
BAR = 3.5603

FTMO_US = pd.read_csv(HERE / "ftmo_swaps_implied.csv")["sym"].tolist()
# costs (E1_rules.md section 4), fractions
COMM = 0.4e-4
HALF = {"A": 3e-4, "B": 2e-4}
HEDGE_HALF = 0.5e-4
OI_EXTRA = 2e-4                     # extra slippage, open/close legs of E1-09/E1-10
SW_LONG, SW_SHORT = 0.0840, 0.0664  # paid, % of notional per year
H_SW_LONG, H_SW_SHORT = 0.0837, -0.0042   # US500: long pays, short receives
IDX_DIV = 0.013


# ── inputs ────────────────────────────────────────────────────────────
def prepare(P: dict) -> dict:
    cal = P["cal"]
    C, O, H, L, AC, V = (P[k] for k in ("C", "O", "H", "L", "AC", "V"))
    r = AC / AC.shift(1) - 1
    f = (AC / C) / (AC / C).shift(1)
    on = O * f / C.shift(1) - 1
    idr = C / O - 1
    bad = O.isna() | (O <= 0) | (O > H * 1.0000001) | (O < L * 0.9999999)
    on = on.mask(bad)
    idr = idr.mask(bad)
    spy = P["x_SPY"]["AC"]
    mkt = spy / spy.shift(1) - 1
    nights = pd.Series((cal[1:] - cal[:-1]).days, index=cal[1:]).reindex(cal).fillna(1)
    nvalid = r.notna().rolling(60, min_periods=1).sum()
    elig = (P["member"] & P["covered"] & (C >= 5) & (nvalid >= 55) & AC.notna()
            & (V > 0))
    # 60-day beta to SPY, data t-59..t
    m = mkt.values[:, None]
    rr = r.values
    msk = ~np.isnan(rr) & ~np.isnan(m)
    x = np.where(msk, m, 0.0)
    y = np.where(msk, rr, 0.0)
    def roll(a):
        cs = np.cumsum(np.nan_to_num(a), axis=0)
        out = cs.copy()
        out[60:] = cs[60:] - cs[:-60]
        return out
    n = roll(msk.astype(float))
    sx, sy, sxx, sxy = roll(x), roll(y), roll(x * x), roll(x * y)
    with np.errstate(invalid="ignore", divide="ignore"):
        beta = (sxy - sx * sy / n) / (sxx - sx * sx / n)
    beta = np.where(n >= 40, beta, np.nan)
    beta = pd.DataFrame(np.clip(beta, 0, 3), index=cal, columns=C.columns).fillna(1.0)
    ftmo = pd.Series(C.columns.isin(FTMO_US), index=C.columns)
    return dict(cal=cal, r=r, on=on, idr=idr, bad=bad, mkt=mkt, nights=nights,
                elig=elig, beta=beta, V=V, ftmo=ftmo,
                hedge_r=mkt - IDX_DIV * nights / 365)


def universe(D: dict, u: str) -> pd.DataFrame:
    return D["elig"] & D["ftmo"] if u == "B" else D["elig"]


# ── weights ───────────────────────────────────────────────────────────
def rank_w(sig: pd.DataFrame, E: pd.DataFrame) -> pd.DataFrame:
    s = sig.where(E)
    rk = s.rank(axis=1)
    d = rk.sub(rk.mean(axis=1), axis=0)
    g = d.abs().sum(axis=1)
    return d.div(g.where(g > 0), axis=0).fillna(0.0)


def weekly(W: pd.DataFrame) -> pd.DataFrame:
    cal = W.index
    wk = pd.Series(cal.to_period("W-FRI"), index=cal)
    last = wk != wk.shift(-1)
    last.iloc[-1] = True
    return W.where(last, np.nan).ffill().fillna(0.0)


def sum_k(df: pd.DataFrame, k: int, log=False) -> pd.DataFrame:
    x = np.log1p(df) if log else df
    return x.rolling(k, min_periods=k).sum()


def resid(D):
    return D["r"].sub(D["beta"].shift(0).mul(1).mul(D["mkt"], axis=0))


def w_rev5(D, u, wk=False, residual=False):
    ret = resid(D) if residual else D["r"]
    sig = -sum_k(ret, 5)
    W = rank_w(sig, universe(D, u))
    return (weekly(W) if wk else W), None


def w_rev5_lh(D, u):
    E = universe(D, u)
    sig = -sum_k(D["r"], 5).where(E)
    # weight ∝ (median rank - rank) on the lower half, ranked by 5-day return
    rk_ret = (-sig).rank(axis=1)
    med = rk_ret.median(axis=1)
    w = (-(rk_ret.sub(med, axis=0))).clip(lower=0)
    w = w.div(w.sum(axis=1).where(lambda s: s > 0), axis=0).fillna(0.0)
    W = weekly(w)
    h = -(W * D["beta"]).sum(axis=1)
    h = weekly(h.to_frame()).iloc[:, 0]
    return W, h


def events_to_w(D, u, ev: pd.DataFrame, hold=20):
    """ev: DataFrame entry_date, ticker, sign. Active on closes entry..entry+hold-1."""
    cal, cols = D["cal"], D["r"].columns
    pos = pd.Series(np.arange(len(cal)), index=cal)
    S = np.zeros((len(cal), len(cols)))
    ci = pd.Series(np.arange(len(cols)), index=cols)
    E = universe(D, u)
    ev = ev[ev.ticker.isin(cols)]
    ev = ev[ev.entry.isin(cal)]
    ok = [bool(E.at[e, t]) for e, t in zip(ev.entry, ev.ticker)]
    ev = ev[ok]
    for e, t, s in zip(ev.entry, ev.ticker, ev.sign):
        i = pos[e]
        S[i:i + hold, ci[t]] += s
    W = pd.DataFrame(S, index=cal, columns=cols)
    g = W.abs().sum(axis=1)
    W = W.div(g.where(g > 0), axis=0).fillna(0.0)
    h = -(W * D["beta"]).sum(axis=1)
    return W, h


def load_earnings() -> pd.DataFrame:
    cache = EDIR.parent / "earnings.pkl"
    if cache.exists():
        return pd.read_pickle(cache)
    rows = []
    for p in sorted(EDIR.glob("*.json")):
        try:
            j = json.loads(p.read_text())
            rr = (j.get("data") or {}).get("rows") or []
        except Exception:
            continue
        for x in rr:
            rows.append((pd.Timestamp(p.stem), x.get("symbol"), x.get("surprise")))
    df = pd.DataFrame(rows, columns=["d", "ticker", "surprise"])
    df["surprise"] = pd.to_numeric(df["surprise"].astype(str).str.replace(",", ""),
                                   errors="coerce")
    df = df.drop_duplicates(["d", "ticker"])
    df.to_pickle(cache)
    return df


def pead_events(D, kind: str) -> pd.DataFrame:
    er = load_earnings()
    cal = D["cal"]
    i0 = cal.searchsorted(er["d"].values)          # first trading day >= d
    keep = i0 + 1 < len(cal)
    er = er[keep].copy()
    i0 = i0[keep]
    er["d0"] = cal[i0]
    er["entry"] = cal[i0 + 1]
    if kind == "sue":
        er["sign"] = np.sign(er["surprise"])
    else:
        ar = resid(D)
        cols = set(ar.columns)
        er = er[er.ticker.isin(cols)]
        a0 = [ar.at[d, t] for d, t in zip(er.d0, er.ticker)]
        a1 = [ar.at[e, t] for e, t in zip(er.entry, er.ticker)]
        er["sign"] = np.sign(np.array(a0) + np.array(a1))
    er = er[er["sign"].notna() & (er["sign"] != 0)]
    return er[["entry", "ticker", "sign"]]


def gapvol_events(D) -> pd.DataFrame:
    V = D["V"]
    medv = V.shift(1).rolling(60, min_periods=40).median()
    ar = resid(D)
    ev = (V > 3 * medv) & (ar.abs() > 0.03)
    st = ar.where(ev).stack().dropna()
    idx = st.index
    return pd.DataFrame(dict(entry=idx.get_level_values(0), ticker=idx.get_level_values(1),
                             sign=np.sign(st.values)))


def w_tow(D, u):
    E = universe(D, u)
    so = sum_k(D["on"].fillna(0), 21, log=True)
    si = sum_k(D["idr"].fillna(0), 21, log=True)
    sig = so.where(E).rank(axis=1) - si.where(E).rank(axis=1)
    return weekly(rank_w(sig, E)), None


def w_ovn(D, u, sign=1):
    E = universe(D, u)
    so = sum_k(D["on"].fillna(0), 21, log=True)
    return rank_w(sign * so, E), None


IS_VOL = {}


def build(vid: str, D: dict, u: str):
    if vid == "E1-01":
        return w_rev5(D, u)
    if vid == "E1-02":
        return w_rev5(D, u, wk=True)
    if vid == "E1-03":
        return w_rev5(D, u, wk=True, residual=True)
    if vid == "E1-04":
        return w_rev5_lh(D, u)
    if vid == "E1-05":
        return events_to_w(D, u, pead_events(D, "sue"))
    if vid == "E1-06":
        return events_to_w(D, u, pead_events(D, "ear"))
    if vid == "E1-07":
        return events_to_w(D, u, gapvol_events(D))
    if vid == "E1-08":
        return w_tow(D, u)
    if vid == "E1-09":
        return w_ovn(D, u, +1)
    if vid == "E1-10":
        return w_ovn(D, u, -1)
    if vid == "E1-11":
        parts = [("E1-03", 1.0), ("E1-06", 1.0), ("E1-08", 1.0)]
        W = None
        h = pd.Series(0.0, index=D["cal"])
        for p, _ in parts:
            Wp, hp = build(p, D, u)
            key = (p, u)
            if key not in IS_VOL:
                g = pnl(p, Wp, hp, D, u, lag=0, cost_mult=0.0)
                st = PEAD_IS_START
                IS_VOL[key] = float(g.loc[st:IS_END].std())
            s = 1.0 / IS_VOL[key]
            W = Wp * s if W is None else W.add(Wp * s, fill_value=0.0)
            if hp is not None:
                h = h + hp * s
        g = W.abs().sum(axis=1)
        k = 1.0 / g.where(g > 0)
        return W.mul(k, axis=0).fillna(0.0), (h * k).fillna(0.0)
    raise KeyError(vid)


# ── P&L ───────────────────────────────────────────────────────────────
MODE = {"E1-09": "on", "E1-10": "id"}


def pnl(vid, W, h, D, u, lag=0, cost_mult=1.0, detail=False):
    mode = MODE.get(vid, "cc")
    Wf = W.shift(1 + lag).fillna(0.0)                 # weights in force on day t
    half = (COMM + HALF[u]) * cost_mult
    nt = D["nights"]
    if mode == "cc":
        R = D["r"].fillna(0.0)
        gross = (Wf * R).sum(axis=1)
        trade = (Wf - Wf.shift(1).fillna(0.0)).abs().sum(axis=1)
        tc = trade * half
        lng = Wf.clip(lower=0).sum(axis=1)
        sht = (-Wf.clip(upper=0)).sum(axis=1)
        sw = (lng * SW_LONG + sht * SW_SHORT) * cost_mult * nt / 365
    else:
        R = (D["on"] if mode == "on" else D["idr"]).fillna(0.0)
        gross = (Wf * R).sum(axis=1)
        trade = 2 * Wf.abs().sum(axis=1)
        tc = trade * (half + OI_EXTRA * cost_mult)
        if mode == "on":
            lng = Wf.clip(lower=0).sum(axis=1)
            sht = (-Wf.clip(upper=0)).sum(axis=1)
            sw = (lng * SW_LONG + sht * SW_SHORT) * cost_mult * nt / 365
        else:
            sw = 0.0 * gross
    net = gross - tc - sw
    htrade = pd.Series(0.0, index=net.index)
    if h is not None:
        hf = h.shift(1 + lag).fillna(0.0)
        hg = hf * D["hedge_r"].fillna(0.0)
        htrade = (hf - hf.shift(1).fillna(0.0)).abs()
        htc = htrade * (COMM * 0 + HEDGE_HALF) * cost_mult
        hsw = (hf.clip(lower=0) * H_SW_LONG + (-hf.clip(upper=0)) * H_SW_SHORT) \
            * cost_mult * nt / 365
        net = net + hg - htc - hsw
        gross = gross + hg
    if detail:
        npos = (Wf != 0).sum(axis=1)
        orders = ((Wf - Wf.shift(1).fillna(0.0)).abs() > 1e-12).sum(axis=1)
        if mode != "cc":
            orders = 2 * npos
        return pd.DataFrame(dict(net=net, gross=gross, trade=trade + htrade,
                                 npos=npos, orders=orders,
                                 grossexp=Wf.abs().sum(axis=1) + (0 if h is None else
                                                                  h.shift(1 + lag).abs().fillna(0))))
    return net


# ── statistics ────────────────────────────────────────────────────────
def t_stats(x: np.ndarray, lags=10):
    n = len(x)
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    xc = x - m
    s = xc @ xc / n
    for l in range(1, lags + 1):
        s += 2 * (1 - l / (lags + 1)) * (xc[l:] @ xc[:-l] / n)
    return m / se, m / np.sqrt(s / n)


def boot_p5(x: np.ndarray, n=10_000, block=20, seed=0) -> float:
    T = len(x)
    rng = np.random.default_rng(seed)
    means = np.empty(n)
    for i0 in range(0, n, 250):
        m = min(250, n - i0)
        starts = rng.integers(0, T, size=(m, T))
        newb = rng.random((m, T)) < 1.0 / block
        newb[:, 0] = True
        blk = np.cumsum(newb, axis=1) - 1
        pos = np.where(newb, np.arange(T)[None, :], 0)
        off = np.arange(T)[None, :] - np.maximum.accumulate(pos, axis=1)
        st = np.take_along_axis(starts, blk, axis=1)
        means[i0:i0 + m] = x[(st + off) % T].mean(axis=1)
    return float(np.percentile(means, 5))


def summ(net: pd.Series, boot=0) -> dict:
    x = net.values
    eq = np.cumprod(1 + x)
    dd = eq / np.maximum.accumulate(eq) - 1
    ti, tn = t_stats(x)
    yrs = len(x) / 252
    return dict(sharpe=x.mean() / x.std() * np.sqrt(252), ann=x.mean() * 252,
                cagr=eq[-1] ** (1 / yrs) - 1, vol=x.std() * np.sqrt(252),
                mdd=dd.min(), worst=x.min(), t=min(ti, tn), t_iid=ti, t_nw=tn,
                mean_bp=x.mean() * 1e4,
                p5_bp=boot_p5(x, n=boot) * 1e4 if boot else np.nan)


def window(s: pd.Series, vid: str, part: str) -> pd.Series:
    if part == "IS":
        st = PEAD_IS_START if vid in ("E1-05", "E1-06", "E1-11") else IS_START
        return s.loc[st:IS_END]
    return s.loc[OOS_START:]


# ── look-ahead tests ──────────────────────────────────────────────────
def cut_D(D: dict, end) -> dict:
    out = {}
    for k, v in D.items():
        if isinstance(v, (pd.DataFrame, pd.Series)) and k != "ftmo":
            out[k] = v.loc[:end]
        elif k == "cal":
            out[k] = v[v <= end]
        else:
            out[k] = v
    return out


def lookahead(vid, D, u, n=20, seed=0):
    rng = np.random.default_rng(seed)
    W, h = build(vid, D, u)
    cal = D["cal"]
    st = cal.searchsorted(pd.Timestamp("2009-01-01" if vid in ("E1-05", "E1-06", "E1-11")
                                       else "2001-01-01"))
    days = sorted(rng.choice(cal[st:-30], n, replace=False))
    ok_t = ok_p = 0
    for d in days:
        # truncation: weights computed on data ending at d must match
        # (event variants: events entered after d are unknown at d, compare up to d)
        Dt = cut_D(D, d)
        Wt, ht = build(vid, Dt, u)
        a, b = W.loc[:d].values, Wt.values
        ok_t += bool(np.allclose(a, b, atol=1e-10))
        # perturbation: scramble every return after d
        Dp = dict(D)
        m = cal > d
        for k in ("r", "on", "idr"):
            x = D[k].copy()
            x.loc[m] = x.loc[m].values + rng.normal(0, 0.02, x.loc[m].shape)
            Dp[k] = x
        Dp["mkt"] = D["mkt"].copy()
        Dp["mkt"].loc[m] += rng.normal(0, 0.01, m.sum())
        Wp, hp = build(vid, Dp, u)
        ok_p += bool(np.allclose(Wp.loc[:d].values, W.loc[:d].values, atol=1e-10))
    return ok_t, ok_p, n


def main(argv):
    P = panels()
    D = prepare(P)
    vids = argv[1:] or [f"E1-{i:02d}" for i in range(1, 12)]
    rows = []
    for vid in vids:
        for u in ("A", "B"):
            W, h = build(vid, D, u)
            res = {}
            for lag in (0, 1):
                for cm in (0.0, 1.0, 2.0):
                    net = pnl(vid, W, h, D, u, lag, cm)
                    res[(lag, cm)] = net
            # worse lag decided on OOS mean at 1x
            oos1 = {lag: window(res[(lag, 1.0)], vid, "OOS").mean() for lag in (0, 1)}
            wl = min(oos1, key=oos1.get)
            det = pnl(vid, W, h, D, u, wl, 1.0, detail=True)
            do = window(det["npos"], vid, "OOS")
            row = dict(vid=vid, u=u, worse_lag=wl)
            for part in ("IS", "OOS"):
                for cm in (0.0, 1.0, 2.0):
                    s = summ(window(res[(wl, cm)], vid, part),
                             boot=10_000 if (part == "OOS" and cm == 1.0) else 0)
                    for k, v in s.items():
                        row[f"{part}_{cm:g}x_{k}"] = v
            for lag in (0, 1):
                s = summ(window(res[(lag, 1.0)], vid, "OOS"))
                row[f"OOS_1x_lag{lag}_sharpe"] = s["sharpe"]
                row[f"OOS_1x_lag{lag}_t"] = s["t"]
            row["turnover_yr"] = float(window(det["trade"], vid, "OOS").mean() * 252 / 2)
            row["pos_avg"] = float(do.mean())
            row["pos_max"] = int(do.max())
            row["orders_avg"] = float(window(det["orders"], vid, "OOS").mean())
            row["orders_max"] = int(window(det["orders"], vid, "OOS").max())
            row["names_avg"] = float(window(universe(D, u).sum(axis=1), vid, "OOS").mean())
            rows.append(row)
            print(fmt(row), flush=True)
            res_store[(vid, u)] = res[(wl, 1.0)]
            res_store[(vid, u, 2)] = res[(wl, 2.0)]
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "results.csv", index=False)
    return df, D


res_store: dict = {}


def fmt(r):
    def g(p, c):
        return (f"Sh {r[f'{p}_{c}_sharpe']:5.2f} t {r[f'{p}_{c}_t']:6.2f} "
                f"ann {r[f'{p}_{c}_ann']*100:6.2f}%")
    return (f"{r['vid']} {r['u']} lag*={r['worse_lag']} | IS 1x {g('IS','1x')} | "
            f"OOS 0x {g('OOS','0x')} | OOS 1x {g('OOS','1x')} p5 {r['OOS_1x_p5_bp']:6.2f}bp "
            f"mdd {r['OOS_1x_mdd']*100:6.1f}% worst {r['OOS_1x_worst']*100:5.2f}% | "
            f"OOS 2x {g('OOS','2x')} | lag0 t {r['OOS_1x_lag0_t']:5.2f} lag1 t "
            f"{r['OOS_1x_lag1_t']:5.2f} | turn {r['turnover_yr']:6.1f}x/yr pos "
            f"{r['pos_avg']:5.1f}/{r['pos_max']} orders/day {r['orders_avg']:5.1f}/"
            f"{r['orders_max']} names {r['names_avg']:5.1f}")


if __name__ == "__main__":
    main(sys.argv)
