#!/usr/bin/env python3
"""Independent verifier for E1 (wave 2) pre-registered backtests.

Re-implemented from agents/prereg/E1_rules.md only. Uses data.panels() solely to
load raw O/H/L/C/V/AC and point-in-time membership; coverage, eligibility,
returns, betas, signals, weights, costs and statistics are computed here.

Usage: python3 verifier/verify.py [--no-earnings]
Output: verifier/verify_run.txt
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from data import panels  # noqa: E402  (raw data loading only)
from fetch import EDIR   # noqa: E402

OUT = HERE / "verify_run.txt"
IS0, IS0_E, IS1, OOS0 = "1999-04-01", "2008-04-01", "2014-12-31", "2015-01-02"
COMM = 0.4e-4
HS = {"A": 3e-4, "B": 2e-4}
HS_IDX = 0.5e-4
SLIP_OI = 2e-4
SW_L, SW_S = -0.0840, -0.0664          # stock swap, %/yr of notional (rules §4)
SW_IL, SW_IS = -0.0837, +0.0042        # US500 swap
DIVY = 0.013
NBOOT, BLOCK = 2000, 20
RNG = np.random.default_rng(12345)

lines: list[str] = []


def log(s=""):
    print(s, flush=True)
    lines.append(str(s))


# ---------------------------------------------------------------- data
P = panels()
cal = pd.DatetimeIndex(P["cal"])
O, H, L, C, V, AC = (P[k].astype(float) for k in ("O", "H", "L", "C", "V", "AC"))
mem = P["member"].astype(bool)
tick = list(C.columns)
T, N = C.shape

# coverage (rules §1), re-derived independently
first = AC.apply(lambda s: s.first_valid_index())
pos = {d: i for i, d in enumerate(cal)}
cov = np.zeros((T, N), bool)
mv = mem.values
for j, t in enumerate(tick):
    fd = first[t]
    if fd is None or pd.isna(fd):
        continue
    fi = pos[fd]
    col = mv[:, j]
    starts = np.flatnonzero(col & ~np.r_[False, col[:-1]])
    ends = np.flatnonzero(col & ~np.r_[col[1:], False])
    for s, e in zip(starts, ends):
        if s == 0 or fi <= s + 5:
            cov[s:e + 1, j] = True
cov = pd.DataFrame(cov, index=cal, columns=tick)
agree = ((cov & C.notna()) == P["covered"]).values.mean()
log(f"coverage: re-derived vs data.py covered agreement {agree:.5f}")

# returns (rules §2)
r = (AC / AC.shift(1) - 1).replace([np.inf, -np.inf], np.nan)
f = (AC / C) / (AC.shift(1) / C.shift(1))
badO = O.isna() | (O <= 0) | (O < L) | (O > H)
on = (O * f / C.shift(1) - 1).where(~badO)
idr = (C / O - 1).where(~badO)
spy = P["x_SPY"]
mkt = spy["AC"] / spy["AC"].shift(1) - 1
nights = pd.Series(np.r_[1, np.diff(cal.values).astype("timedelta64[D]").astype(int)], index=cal)
us500 = mkt - DIVY * nights / 365.0

# eligibility A
cnt = r.notna().rolling(60, min_periods=1).sum()
eligA = cov & (C >= 5) & (cnt >= 55) & AC.notna() & (V > 0)
ftmo = pd.read_csv(HERE.parent / "ftmo_swaps_implied.csv")["sym"].tolist()
inB = pd.Series([t in ftmo for t in tick], index=tick)
eligB = eligA & inB.values[None, :]
log(f"FTMO syms matched to membership tickers: {sorted(set(ftmo) & set(tick))} ({int(inB.sum())})")
log(f"mean eligible/day A {eligA.sum(axis=1).mean():.1f}  B {eligB.sum(axis=1).mean():.1f}; "
    f"B OOS mean {eligB.loc[OOS0:].sum(axis=1).mean():.1f}")
nbad = int((badO & r.notna() & (eligA)).values.sum())
log(f"invalid-open stock-days among eligible A with valid r: {nbad} "
    f"(of {int((eligA & r.notna()).values.sum())})")

# beta: 60d OLS of r on mkt over t-59..t, pairwise valid, min 40 obs, clip [0,3], missing->1
X = np.repeat(mkt.values[:, None], N, 1)
R = r.values
ok = ~np.isnan(R) & ~np.isnan(X)
def rs(a):
    a = np.where(ok, a, 0.0)
    c = np.cumsum(a, 0)
    out = c.copy()
    out[60:] = c[60:] - c[:-60]
    return out
n_ = rs(np.ones_like(R)); sx = rs(X); sy = rs(R); sxx = rs(X * X); sxy = rs(X * R)
with np.errstate(invalid="ignore", divide="ignore"):
    beta = (n_ * sxy - sx * sy) / (n_ * sxx - sx * sx)
beta[n_ < 40] = np.nan
beta = np.clip(beta, 0, 3)
beta = np.where(np.isnan(beta), 1.0, beta)
beta = pd.DataFrame(beta, index=cal, columns=tick)
e = r - beta.mul(mkt, axis=0)       # residual, beta of the same day (literal §2)

weekend = pd.Series(cal.to_period("W-FRI"), index=cal)
is_wk = (weekend != weekend.shift(-1)).values.copy()  # last trading day of each week
is_wk[-1] = True


# ---------------------------------------------------------------- weights
def rankw(sig: pd.DataFrame, elig: pd.DataFrame) -> pd.DataFrame:
    s = sig.where(elig)
    rk = s.rank(axis=1)
    dm = rk.sub(rk.mean(axis=1), axis=0)
    w = dm.div(dm.abs().sum(axis=1), axis=0)
    return w.fillna(0.0)


def weekly(w: pd.DataFrame) -> pd.DataFrame:
    return w.where(pd.Series(is_wk, index=cal), np.nan, axis=0).ffill().fillna(0.0)


def event_book(ev_sign: pd.DataFrame, hold=20):
    """ev_sign: +1/-1 at entry close (0 otherwise). Active for 'hold' closes from
    entry (entry close .. entry+hold-1 close), earning t+1..t+hold. Equal weight per
    active event, net per stock, sum|w over events| = 1."""
    a = ev_sign.fillna(0).values
    c = np.cumsum(a, 0)
    act = c.copy(); act[hold:] = c[hold:] - c[:-hold]
    nev = np.cumsum(np.abs(a), 0)
    ne = nev.copy(); ne[hold:] = nev[hold:] - nev[:-hold]
    ne = ne.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        w = act / ne[:, None]
    w = np.nan_to_num(w)
    return pd.DataFrame(w, index=cal, columns=tick)


# ---------------------------------------------------------------- engine
def run(W, U, lag, cm=1.0, ret="cc", hedge=None):
    """W: target weights formed at close t. Position earning day s is W_{s-1-lag}.
    hedge: US500 weight series formed at close t (same lag)."""
    h = W.shift(1 + lag).fillna(0.0)
    hv = h.values
    hs = HS[U]
    if ret == "cc":
        rr = np.nan_to_num(r.values)
        gross = (hv * rr).sum(axis=1)
        trade = np.abs(np.diff(np.r_[np.zeros((1, N)), hv], axis=0)).sum(axis=1)
        tc = trade * (COMM + hs) * cm
        lg = np.clip(hv, 0, None).sum(axis=1); sh = -np.clip(hv, None, 0).sum(axis=1)
        swap = (lg * SW_L + sh * SW_S) * cm * nights.values / 365.0
    else:
        rr = np.nan_to_num((on if ret == "on" else idr).values)
        gross = (hv * rr).sum(axis=1)
        trade = 2 * np.abs(hv).sum(axis=1)
        tc = trade * (COMM + hs + SLIP_OI) * cm
        if ret == "on":
            lg = np.clip(hv, 0, None).sum(axis=1); sh = -np.clip(hv, None, 0).sum(axis=1)
            swap = (lg * SW_L + sh * SW_S) * cm * nights.values / 365.0
        else:
            swap = np.zeros(T)
    net = gross - tc + swap
    if hedge is not None:
        hh = hedge.shift(1 + lag).fillna(0.0).values
        hg = hh * np.nan_to_num(us500.values)
        htr = np.abs(np.diff(np.r_[0.0, hh]))
        hsw = np.where(hh > 0, hh * SW_IL * cm, -hh * SW_IS * (cm if SW_IS < 0 else 1.0))
        net = net + hg - htr * HS_IDX * cm + hsw * nights.values / 365.0
        gross = gross + hg
    return pd.Series(net, index=cal), pd.Series(gross, index=cal), pd.Series(trade, index=cal)


def nw_var(x, lags=10):
    x = x - x.mean(); n = len(x)
    v = x @ x / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (x[k:] @ x[:-k]) / n
    return v


def stats(x: pd.Series):
    x = x.values; n = len(x); m = x.mean(); sd = x.std(ddof=1)
    t_iid = m / (sd / np.sqrt(n)); t_nw = m / np.sqrt(nw_var(x) / n)
    return dict(sh=m / sd * np.sqrt(252), bp=m * 1e4, t=min(t_iid, t_nw), tiid=t_iid, tnw=t_nw)


def boot_p5(x: pd.Series):
    x = x.values; n = len(x); p = 1.0 / BLOCK
    means = np.empty(NBOOT)
    for b in range(NBOOT):
        st = RNG.random(n) < p; st[0] = True
        starts = RNG.integers(0, n, n)
        grp = np.cumsum(st) - 1
        s0 = starts[np.flatnonzero(st)][grp]
        off = np.arange(n) - np.flatnonzero(st)[grp]
        means[b] = x[(s0 + off) % n].mean()
    return np.percentile(means, 5) * 1e4


# ---------------------------------------------------------------- variants
def build(vid, U):
    el = eligA if U == "A" else eligB
    if vid == "E1-01":
        return dict(W=rankw(-(AC / AC.shift(5) - 1), el))
    if vid == "E1-02":
        return dict(W=weekly(rankw(-(AC / AC.shift(5) - 1), el)))
    if vid == "E1-03":
        sig = -e.rolling(5, min_periods=5).sum()
        return dict(W=weekly(rankw(sig, el)))
    if vid == "E1-04":
        s = (AC / AC.shift(5) - 1).where(el)
        rk = s.rank(axis=1); med = (s.notna().sum(axis=1) + 1) / 2
        w = (-rk).add(med, axis=0).clip(lower=0).fillna(0.0)
        w = w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        hd = -(w * beta).sum(axis=1)
        wk = pd.Series(is_wk, index=cal)
        return dict(W=weekly(w), hedge=hd.where(wk).ffill().fillna(0.0))
    if vid in ("E1-05", "E1-06"):
        ev = earn_events(vid, el)
        W = event_book(ev)
        return dict(W=W, hedge=-(W * beta).sum(axis=1))
    if vid == "E1-07":
        medv = V.shift(1).rolling(60, min_periods=60).median()
        evm = (V > 3 * medv) & (e.abs() > 0.03) & el
        ev = np.sign(e).where(evm, 0.0)
        W = event_book(ev)
        return dict(W=W, hedge=-(W * beta).sum(axis=1))
    if vid == "E1-08":
        lon = np.log1p(on.fillna(0.0)).rolling(21, min_periods=21).sum()
        lid = np.log1p(idr.fillna(0.0)).rolling(21, min_periods=21).sum()
        lon = lon.where(el); lid = lid.where(el)
        sig = lon.rank(axis=1) - lid.rank(axis=1)
        return dict(W=weekly(rankw(sig, el)))
    if vid in ("E1-09", "E1-10"):
        lon = np.log1p(on.fillna(0.0)).rolling(21, min_periods=21).sum()
        sgn = 1 if vid == "E1-09" else -1
        return dict(W=rankw(sgn * lon, el), ret="on" if vid == "E1-09" else "id")
    raise KeyError(vid)


EARN = None


def load_earn():
    global EARN
    if EARN is not None:
        return EARN
    rows = []
    files = sorted(EDIR.glob("*.json"))
    for p in files:
        try:
            j = json.loads(p.read_text())
            rr_ = (j.get("data") or {}).get("rows") or []
        except Exception:
            continue
        for x in rr_:
            rows.append((p.stem, (x.get("symbol") or "").strip().upper().replace("/", ".").replace("-", "."),
                         x.get("surprise")))
    df = pd.DataFrame(rows, columns=["d", "sym", "sur"])
    df["d"] = pd.to_datetime(df["d"])
    k = cal.searchsorted(df["d"].values)
    df = df[k < T].copy(); df["i0"] = k[k < T]
    df = df[df.sym.isin(set(tick))].drop_duplicates(["sym", "i0"])
    df["j"] = df.sym.map({t: j for j, t in enumerate(tick)})
    s = pd.to_numeric(df.sur, errors="coerce")
    s[s == -999] = np.nan  # Nasdaq sentinel for undefined surprise
    df["sur"] = s
    log(f"earnings: {len(files)} day-files {files[0].stem}..{files[-1].stem}; "
        f"{len(df)} member-ticker events; surprise valid&nonzero {int((df.sur.fillna(0) != 0).sum())}")
    EARN = df
    return df


def earn_events(vid, el):
    df = load_earn()
    ev = np.zeros((T, N))
    elv = el.values; ev_ = e.values
    for i0, j, s in zip(df.i0.values, df.j.values, df.sur.values):
        ie = i0 + 1
        if ie >= T or not elv[ie, j]:      # eligible on entry day d0+1
            continue
        if vid == "E1-05":
            if not np.isfinite(s) or s == 0:
                continue
            sg = np.sign(s)
        else:
            a = ev_[i0, j] + ev_[ie, j]
            if not np.isfinite(a) or a == 0:
                continue
            sg = np.sign(a)
        ev[ie, j] += sg
    return pd.DataFrame(ev, index=cal, columns=tick)


def report(vid, U, spec, is0):
    res = {}
    for lag in (0, 1):
        for cm in (1.0, 2.0):
            net, gross, tr = run(spec["W"], U, lag, cm, spec.get("ret", "cc"), spec.get("hedge"))
            o = net.loc[OOS0:]
            st = stats(o)
            st["turn"] = tr.loc[OOS0:].mean() * 252
            if cm == 1.0:
                st["IS"] = stats(net.loc[is0:IS1])["sh"]
                st["ISgross"] = stats(gross.loc[is0:IS1])
                st["OOSgross"] = stats(gross.loc[OOS0:])
            res[(lag, cm)] = (st, net)
    wl = 0 if res[(0, 1.0)][0]["sh"] <= res[(1, 1.0)][0]["sh"] else 1
    p5 = boot_p5(res[(wl, 1.0)][1].loc[OOS0:])
    log(f"{vid} U={U} worse lag={wl} | boot p5 (worse,1x) {p5:+.2f} bp")
    for lag in (0, 1):
        for cm in (1.0, 2.0):
            st = res[(lag, cm)][0]
            extra = (f" IS_Sh {st['IS']:+.2f} | gross OOS Sh {st['OOSgross']['sh']:+.2f} "
                     f"{st['OOSgross']['bp']:+.2f}bp, gross IS Sh {st['ISgross']['sh']:+.2f}") if cm == 1.0 else ""
            log(f"   lag{lag} {cm:.0f}x  OOS Sh {st['sh']:+.2f}  mean {st['bp']:+.2f}bp  "
                f"t {st['t']:+.2f} (iid {st['tiid']:+.2f} NW {st['tnw']:+.2f})  turn/yr {st['turn']:.1f}{extra}")
    return res, wl, p5


SUMMARY = []


def do(vid, U):
    spec = build(vid, U)
    is0 = IS0_E if vid in ("E1-05", "E1-06", "E1-11") else IS0
    res, wl, p5 = report(vid, U, spec, is0)
    a, b = res[(wl, 1.0)][0], res[(wl, 2.0)][0]
    SUMMARY.append((vid, U, wl, a["sh"], a["t"], b["sh"], b["t"], a["IS"], p5, a["turn"]))
    return spec, res


if __name__ == "__main__":
    noe = "--no-earnings" in sys.argv
    specs = {}
    vids = ["E1-01", "E1-02", "E1-03", "E1-04", "E1-07", "E1-08", "E1-09", "E1-10"]
    if not noe:
        vids += ["E1-05", "E1-06"]
    for vid in vids:
        for U in ("A", "B"):
            specs[(vid, U)], _ = do(vid, U)
    if not noe:
        for U in ("A", "B"):
            parts = {}
            for vid, is0 in (("E1-03", IS0), ("E1-06", IS0_E), ("E1-08", IS0)):
                sp = specs[(vid, U)]
                _, g, _ = run(sp["W"], U, 0, 1.0, "cc", sp.get("hedge"))
                vol = g.loc[is0:IS1].std() * np.sqrt(252)
                parts[vid] = (sp, 1.0 / vol)
                log(f"STACK {U}: {vid} IS gross vol {vol:.4f}")
            Wsum = sum(sp["W"] * k for sp, k in parts.values())
            g = Wsum.abs().sum(axis=1).replace(0, np.nan)
            sc = (1.0 / g).fillna(0.0)
            W = Wsum.mul(sc, axis=0)
            sp6, k6 = parts["E1-06"]
            hed = sp6["hedge"] * k6 * sc
            spec = dict(W=W, hedge=hed)
            res, wl, p5 = report("E1-11", U, spec, IS0_E)
            a, b = res[(wl, 1.0)][0], res[(wl, 2.0)][0]
            SUMMARY.append(("E1-11", U, wl, a["sh"], a["t"], b["sh"], b["t"], a["IS"], p5, a["turn"]))
    log("")
    log("SUMMARY (worse lag by OOS 1x Sharpe): vid U lag | OOS Sh/t 1x | OOS Sh/t 2x | IS Sh 1x | p5 bp | turn/yr")
    for s in sorted(SUMMARY):
        log(f"{s[0]} {s[1]} L{s[2]} | {s[3]:+.2f} / {s[4]:+.2f} | {s[5]:+.2f} / {s[6]:+.2f} | "
            f"{s[7]:+.2f} | {s[8]:+.2f} | {s[9]:.0f}")
    OUT.write_text("\n".join(lines) + "\n")
