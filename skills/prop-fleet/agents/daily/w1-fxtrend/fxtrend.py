#!/usr/bin/env python3
"""D2 — forex/CFD multi-asset trend and carry, as pre-registered in
agents/prereg/D2_rules.md (commit 77a78e7, pushed before this file existed).

Run:  python3 fxtrend.py            # every counted variant, gate, prop sim, checks
      python3 fxtrend.py --quick    # fewer bootstrap draws (smoke test only)

Reuses `stats` and the Politis-Romano idea from scripts/trend_backtest.py; the
bootstrap here resamples *daily* returns (mean block 20 days) as section 6 says.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
import data as D                                              # noqa: E402
from trend_backtest import stats                              # noqa: E402

TD = 252
Z_BAR = 3.5504
IS_END, OOS_START = "2012-12-31", "2013-01-01"
VOL_WIN, VOL_MIN, ENTRY_DAYS = 60, 40, 260
SLEEVE_VOL, SLEEVE_WIN, SLEEVE_MIN, K_CAP = 0.10, 126, 60, 4.0
BUFFER = 0.10
HORIZONS = (21, 63, 126, 252)
EWMAC = ((8, 32), (16, 64), (32, 128), (64, 256))
MARGIN_CAP = 0.80
CCY_PAIR = {"EUR": ("EURUSD", 1), "GBP": ("GBPUSD", 1), "AUD": ("AUDUSD", 1),
            "NZD": ("NZDUSD", 1), "JPY": ("USDJPY", -1), "CHF": ("USDCHF", -1),
            "CAD": ("USDCAD", -1), "SEK": ("USDSEK", -1), "NOK": ("USDNOK", -1)}


# ── building blocks ───────────────────────────────────────────────────
def eligible(R: pd.DataFrame) -> pd.DataFrame:
    return R.notna().cumsum() >= ENTRY_DAYS


def asset_vol(R: pd.DataFrame) -> pd.DataFrame:
    return R.rolling(VOL_WIN, min_periods=VOL_MIN).std() * np.sqrt(TD)


def class_weights(ok: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    """1/N_class inside a class, 1/N_classes across available classes."""
    w = pd.DataFrame(0.0, index=ok.index, columns=ok.columns)
    cls = meta["cls"].reindex(ok.columns)
    n_cls = pd.Series(0, index=ok.index, dtype=float)
    per = {}
    for c in cls.unique():
        cols = cls.index[cls == c]
        n = ok[cols].sum(axis=1)
        per[c] = (cols, n)
        n_cls += (n > 0).astype(float)
    for c, (cols, n) in per.items():
        w[cols] = ok[cols].astype(float).div(n.replace(0, np.nan), axis=0).div(
            n_cls.replace(0, np.nan), axis=0).fillna(0.0)
    return w


def tsmom_signal(R: pd.DataFrame, horizons=HORIZONS) -> pd.DataFrame:
    lr = np.log1p(R)
    s = sum(np.sign(lr.rolling(h, min_periods=h).sum()) for h in horizons)
    return s / len(horizons)


def ewmac_raw(R: pd.DataFrame) -> list:
    """Per crossover: (fast - slow EWMA of the financed price index) / price vol."""
    P = np.exp(np.log1p(R.fillna(0)).cumsum()).where(R.notna() | R.notna().cummax())
    pv = P * R.rolling(VOL_WIN, min_periods=VOL_MIN).std()
    out = []
    for f, s in EWMAC:
        out.append((P.ewm(span=f, adjust=False).mean()
                    - P.ewm(span=s, adjust=False).mean()) / pv)
    return out


def ewmac_scalars(raws: list, ok: pd.DataFrame) -> list:
    """Fixed in-sample (<= IS_END) scalars: 10 / mean |raw|, pooled over assets."""
    out = []
    for r in raws:
        x = r.where(ok).loc[:IS_END].abs().stack()
        out.append(10.0 / float(x.mean()))
    return out


def ewmac_signal(R: pd.DataFrame, scalars: list) -> pd.DataFrame:
    fs = [(r * k).clip(-20, 20) for r, k in zip(ewmac_raw(R), scalars)]
    return (sum(fs) / len(fs) / 10.0).clip(-2, 2)


def sleeve_scale(pos: pd.DataFrame, R: pd.DataFrame) -> pd.DataFrame:
    """Scale raw positions to SLEEVE_VOL using the realized vol of the raw sleeve's
    own past daily returns (positions at t-1 times returns at t, through t)."""
    raw = (pos.shift(1) * R.fillna(0)).sum(axis=1)
    vol = raw.rolling(SLEEVE_WIN, min_periods=SLEEVE_MIN).std() * np.sqrt(TD)
    k = (SLEEVE_VOL / vol).clip(upper=K_CAP)
    return pos.mul(k, axis=0).fillna(0.0)


# ── sleeves ───────────────────────────────────────────────────────────
def trend_positions(R, meta, kind="multi", scalars=None) -> pd.DataFrame:
    ok = eligible(R)
    sig = {"multi": lambda: tsmom_signal(R),
           "12m": lambda: tsmom_signal(R, (252,)),
           "fast": lambda: tsmom_signal(R, (21, 63)),
           "ewmac": lambda: ewmac_signal(R, scalars)}[kind]()
    vol = asset_vol(R)
    ok = ok & vol.notna() & sig.notna()
    w = class_weights(ok, meta)
    pos = (sig * SLEEVE_VOL / vol).where(ok, 0.0).fillna(0.0) * w
    return sleeve_scale(pos, R)


def carry_positions(R, rates, kind="xs") -> pd.DataFrame:
    fx = list(CCY_PAIR.values())
    pairs = [p for p, _ in fx]
    ok = eligible(R[pairs])
    vol = asset_vol(R[pairs])
    ok = ok & vol.notna()
    pos = pd.DataFrame(0.0, index=R.index, columns=R.columns)
    if kind == "xs":
        ccys = ["USD"] + list(CCY_PAIR)
        avail = pd.DataFrame({c: (ok[CCY_PAIR[c][0]] if c != "USD"
                                  else pd.Series(True, index=R.index)) for c in ccys})
        rt = rates[ccys].where(avail)
        rk = rt.rank(axis=1)
        dm = rk.sub(rk.mean(axis=1), axis=0)
        w = dm.div(dm.abs().sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        med = vol.where(ok).median(axis=1)
        for c, (p, sgn) in CCY_PAIR.items():
            pos[p] = (sgn * w[c] * med / vol[p]).where(ok[p], 0.0).fillna(0.0)
    else:
        n = ok.sum(axis=1).replace(0, np.nan)
        for c, (p, sgn) in CCY_PAIR.items():
            d = np.sign(rates[c] - rates["USD"])
            pos[p] = (sgn * d * SLEEVE_VOL / vol[p] / n).where(ok[p], 0.0).fillna(0.0)
    return sleeve_scale(pos, R)


# ── execution, costs ──────────────────────────────────────────────────
def execute(target: pd.DataFrame, buffer=BUFFER) -> pd.DataFrame:
    T = target.fillna(0.0).values
    H = np.zeros_like(T)
    h = np.zeros(T.shape[1])
    for t in range(T.shape[0]):
        tt = T[t]
        move = np.abs(tt - h) >= buffer * np.abs(tt)
        move |= (tt == 0) & (h != 0)
        h = np.where(move, tt, h)
        H[t] = h
    return pd.DataFrame(H, index=target.index, columns=target.columns)


def pnl(H, R, meta, dcal, lag=1, cost_mult=1.0) -> pd.DataFrame:
    """Daily gross, cost, swap, net (fractions of equity) and margin use."""
    held = H.shift(lag).fillna(0.0)
    gross = (held * R.fillna(0.0)).sum(axis=1)
    trade = H.diff().abs().fillna(H.abs()).shift(lag - 1).fillna(0.0)
    cost = (trade * meta["cost_bps"] / 1e4).sum(axis=1) * cost_mult
    swap = (held.abs() * meta["swap"]).sum(axis=1) * dcal / 365.0 * cost_mult
    margin = (held.abs() / meta["lev"]).sum(axis=1)
    return pd.DataFrame(dict(gross=gross, cost=cost, swap=swap,
                             net=gross - cost - swap, margin=margin,
                             gross_lev=held.abs().sum(axis=1)))


# ── variants ──────────────────────────────────────────────────────────
VARIANTS = {
    "D2-01": "TREND multi-horizon", "D2-02": "TREND 12m", "D2-03": "TREND fast",
    "D2-04": "CARRY XS", "D2-05": "CARRY TS", "D2-06": "STACK",
    "D2-07": "STACK+BONDS", "D2-08": "STACK trend-filtered carry",
    "D2-09": "TREND EWMAC",
}


def stack_targets(a: pd.DataFrame, b: pd.DataFrame, R) -> pd.DataFrame:
    return sleeve_scale(0.5 * a + 0.5 * b, R)


def build_targets(vid: str, d: dict, scalars=None) -> pd.DataFrame:
    R, rates, meta = d["R"], d["rates"], d["meta"]
    core = [c for c in R if meta.loc[c, "cls"] != "BOND"]
    Rc = R[core]
    if vid == "D2-01":
        return trend_positions(Rc, meta, "multi")
    if vid == "D2-02":
        return trend_positions(Rc, meta, "12m")
    if vid == "D2-03":
        return trend_positions(Rc, meta, "fast")
    if vid == "D2-09":
        return trend_positions(Rc, meta, "ewmac", scalars)
    if vid == "D2-04":
        return carry_positions(Rc, rates, "xs")
    if vid == "D2-05":
        return carry_positions(Rc, rates, "ts")
    if vid == "D2-06":
        return stack_targets(trend_positions(Rc, meta), carry_positions(Rc, rates), Rc)
    if vid == "D2-07":
        t = trend_positions(R, meta)
        c = carry_positions(R, rates)
        return stack_targets(t, c, R)
    if vid == "D2-08":
        c = carry_positions(Rc, rates)
        tr = tsmom_signal(Rc, (63, 252))
        agree = np.sign(c) == np.sign(tr.reindex(columns=c.columns).fillna(0))
        c = c.where(agree, 0.0)
        return stack_targets(trend_positions(Rc, meta), c, Rc)
    if vid.startswith("CLS-"):                      # diagnostic: one trend class
        cls = vid[4:]
        cols = [c for c in R if meta.loc[c, "cls"] == cls]
        return trend_positions(R[cols], meta)
    raise KeyError(vid)


def run(vid, d, scalars=None, lag=1, cost_mult=1.0) -> tuple:
    T = build_targets(vid, d, scalars)
    T = T.reindex(columns=d["R"].columns).fillna(0.0)
    H = execute(T)
    return pnl(H, d["R"], d["meta"], d["dcal"], lag, cost_mult), H


# ── statistics ────────────────────────────────────────────────────────
def t_stats(r: pd.Series, lags=10) -> tuple:
    x = r.dropna().values
    n = len(x)
    m = x.mean()
    se_iid = x.std(ddof=1) / np.sqrt(n)
    xc = x - m
    s = xc @ xc / n
    for l in range(1, lags + 1):
        s += 2 * (1 - l / (lags + 1)) * (xc[l:] @ xc[:-l] / n)
    se_nw = np.sqrt(s / n)
    return m / se_iid, m / se_nw


def boot_mean_p5(r: pd.Series, n=10_000, block=20, seed=0) -> float:
    x = r.dropna().values
    T = len(x)
    rng = np.random.default_rng(seed)
    means = np.empty(n)
    p = 1.0 / block
    for i0 in range(0, n, 500):
        m = min(500, n - i0)
        starts = rng.integers(0, T, size=(m, T))
        newb = rng.random((m, T)) < p
        newb[:, 0] = True
        # index = start of current block + offset within block
        blk_id = np.cumsum(newb, axis=1) - 1
        off = np.arange(T)[None, :] - np.maximum.accumulate(
            np.where(newb, np.arange(T)[None, :], 0), axis=1)
        st = np.take_along_axis(starts, blk_id, axis=1)
        idx = (st + off) % T
        means[i0:i0 + m] = x[idx].mean(axis=1)
    return float(np.percentile(means, 5))


def summary(net: pd.Series, n_boot=10_000) -> dict:
    s = stats(net)
    ti, tn = t_stats(net)
    return dict(sharpe=s["sharpe"], cagr=(s["cum"].iloc[-1]) ** (1 / s["years"]) - 1,
                vol=s["ann_vol"], max_dd=s["max_dd"], worst_day=float(net.min()),
                mean_bp=float(net.mean() * 1e4), t_iid=ti, t_nw=tn, t=min(ti, tn),
                p5_bp=boot_mean_p5(net, n=n_boot) * 1e4 if n_boot else np.nan,
                years=s["years"], worst_year=s["worst_year"],
                pct_pos_months=s["pct_pos_months"])


# ── look-ahead and truncation tests ───────────────────────────────────
def _cut(d: dict, end) -> dict:
    return dict(R=d["R"].loc[:end], rates=d["rates"].loc[:end], meta=d["meta"],
                dcal=d["dcal"].loc[:end], cal=d["cal"][d["cal"] <= end])


def _perturb(d: dict, end, rng) -> dict:
    R = d["R"].copy()
    m = R.index > end
    noise = rng.normal(0, 0.02, size=R.loc[m].shape)
    R.loc[m] = R.loc[m].values + noise
    rates = d["rates"].copy()
    rates.loc[rates.index > end] = rates.loc[rates.index > end].values + \
        rng.normal(0, 0.03, size=rates.loc[rates.index > end].shape)
    return dict(R=R, rates=rates, meta=d["meta"], dcal=d["dcal"], cal=d["cal"])


def future_tests(vid, d, scalars, n=20, seed=0) -> tuple:
    rng = np.random.default_rng(seed)
    _, H = run(vid, d, scalars)
    idx = d["R"].index
    days = rng.choice(idx[(idx > "1995-01-01") & (idx < idx[-30])], n, replace=False)
    ok_trunc = ok_pert = 0
    for dd in sorted(days):
        _, Ht = run(vid, _cut(d, dd), scalars)
        ok_trunc += np.allclose(Ht.values, H.loc[:dd].values, atol=1e-12, equal_nan=True)
        _, Hp = run(vid, _perturb(d, dd, rng), scalars)
        ok_pert += np.allclose(Hp.loc[:dd].values, H.loc[:dd].values, atol=1e-12,
                               equal_nan=True)
    return ok_trunc, ok_pert, n


# ── prop simulation (D2_rules.md §7) ──────────────────────────────────
VOL_GRID = np.arange(0.04, 0.301, 0.02)
FEE, ACCOUNT = 600.0, 100_000.0


def boot_paths(n_rows: int, n_paths: int, length: int, block=20, seed=0):
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n_rows, size=(n_paths, length))
    newb = rng.random((n_paths, length)) < 1.0 / block
    newb[:, 0] = True
    blk_id = np.cumsum(newb, axis=1) - 1
    pos = np.where(newb, np.arange(length)[None, :], 0)
    off = np.arange(length)[None, :] - np.maximum.accumulate(pos, axis=1)
    st = np.take_along_axis(starts, blk_id, axis=1)
    return (st + off) % n_rows


def prop_sim(net: np.ndarray, margin: np.ndarray, vol_mult: float, idx: np.ndarray,
             daily_stop=0.04, floor=0.91, p1=0.10, p2=0.05, min_days=4,
             max_eval=504, funded_days=504, payout_every=21, split=0.80) -> dict:
    """Vectorized over paths. net/margin at 10% vol; idx = bootstrap row indices."""
    n_paths, L = idx.shape
    r = net[idx] * vol_mult
    mg = margin[idx] * vol_mult
    r = r * np.minimum(1.0, MARGIN_CAP / np.maximum(mg, 1e-12))
    phase = np.ones(n_paths, dtype=int)         # 1, 2, 3=funded, 0=dead, 4=done
    eq = np.ones(n_paths)
    days = np.zeros(n_paths, dtype=int)
    pass_day = np.full(n_paths, -1)
    blown_eval = np.zeros(n_paths, bool)
    abandoned = np.zeros(n_paths, bool)
    paid = np.zeros(n_paths)
    funded_breach = np.zeros(n_paths, bool)
    funded_len = np.zeros(n_paths, dtype=int)
    t_total = 0
    for t in range(L):
        live = (phase >= 1) & (phase <= 3)
        if not live.any():
            break
        rt = r[:, t]
        eq_new = eq * (1 + rt)
        days = days + live
        breach = live & ((rt <= -daily_stop) | (eq_new <= floor))
        ev = live & (phase <= 2)
        blown_eval |= breach & ev
        funded_breach |= breach & (phase == 3)
        eq = np.where(live, eq_new, eq)
        # targets
        hit1 = live & ~breach & (phase == 1) & (eq >= 1 + p1) & (days >= min_days)
        hit2 = live & ~breach & (phase == 2) & (eq >= 1 + p2) & (days >= min_days)
        ab = live & ~breach & ev & (days >= max_eval) & ~hit1 & ~hit2
        abandoned |= ab
        phase = np.where(breach | ab, 0, phase)
        phase = np.where(hit1, 2, phase)
        pass_day = np.where(hit2, t + 1, pass_day)
        phase = np.where(hit2, 3, phase)
        reset = hit1 | hit2
        eq = np.where(reset, 1.0, eq)
        days = np.where(reset, 0, days)
        # funded: payouts
        f = (phase == 3) & ~reset
        due = f & (days > 0) & (days % payout_every == 0) & (eq > 1)
        paid += np.where(due, split * (eq - 1), 0.0)
        eq = np.where(due, 1.0, eq)
        funded_len = np.where(f, days, funded_len)
        done = f & (days >= funded_days)
        phase = np.where(done, 4, phase)
        t_total = t
    passed = pass_day > 0
    refund = passed & (paid > 0)
    value = paid * ACCOUNT + refund * FEE
    net_val = value - FEE
    pf = passed.mean()
    return dict(
        vol=vol_mult * 0.10, p_pass=pf, p_blow_eval=blown_eval.mean(),
        p_abandon=abandoned.mean(),
        med_days_pass=float(np.median(pass_day[passed])) if passed.any() else np.nan,
        funded_survival=float((~funded_breach[passed]).mean()) if passed.any() else np.nan,
        exp_payout_if_funded=float(value[passed].mean()) if passed.any() else 0.0,
        exp_net=float(net_val.mean()), exp_net_per_fee=float(net_val.mean() / FEE),
    )


def prop_grid(df: pd.DataFrame, n_paths=10_000, seed=0) -> pd.DataFrame:
    net = df["net"].values
    margin = df["margin"].values
    L = 504 * 2 + 504 + 10
    idx = boot_paths(len(net), n_paths, L, seed=seed)
    rows = [prop_sim(net, margin, v / 0.10, idx) for v in VOL_GRID]
    return pd.DataFrame(rows)


# ── report ────────────────────────────────────────────────────────────
def fmt(s: dict) -> str:
    return (f"Sharpe {s['sharpe']:5.2f}  CAGR {s['cagr']*100:6.2f}%  vol {s['vol']*100:5.2f}%  "
            f"maxDD {s['max_dd']*100:6.1f}%  worst day {s['worst_day']*100:5.2f}%  "
            f"mean {s['mean_bp']:5.2f}bp/d  t {s['t']:5.2f} (iid {s['t_iid']:.2f}, NW {s['t_nw']:.2f})  "
            f"p5 {s['p5_bp']:6.2f}bp  yrs {s['years']:.1f}")


def active(df: pd.DataFrame) -> pd.DataFrame:
    on = df["gross_lev"] > 0
    return df.loc[on.idxmax():] if on.any() else df


def main() -> int:
    quick = "--quick" in sys.argv
    nb = 1000 if quick else 10_000
    npaths = 2000 if quick else 10_000
    d = D.panel(include_bonds=True)
    R = d["R"]
    print(f"D2 run. calendar {R.index[0].date()} -> {R.index[-1].date()}, "
          f"{R.shape[1]} instruments; IS <= {IS_END}, OOS >= {OOS_START}")
    core = [c for c in R if d["meta"].loc[c, "cls"] != "BOND"]
    raws = ewmac_raw(R[core])
    scalars = ewmac_scalars(raws, eligible(R[core]))
    print("EWMAC in-sample forecast scalars:", [round(x, 3) for x in scalars])
    print("data sha256[:12]:", D.sources_sha())

    res, runs = {}, {}
    for vid, name in VARIANTS.items():
        out = {}
        for lag in (1, 2):
            for cm in (1.0, 2.0):
                df, H = run(vid, d, scalars, lag, cm)
                df = active(df)
                runs[(vid, lag, cm)] = df
                is_ = df.loc[:IS_END]
                oos = df.loc[OOS_START:]
                out[(lag, cm)] = dict(IS=summary(is_["net"], 0),
                                      OOS=summary(oos["net"], nb if cm == 1.0 or lag == 1 else 0))
        res[vid] = out
        print(f"\n=== {vid} {name}")
        for (lag, cm), o in out.items():
            print(f"  lag{lag} cost{cm:.0f}x IS : {fmt(o['IS'])}")
            print(f"  lag{lag} cost{cm:.0f}x OOS: {fmt(o['OOS'])}")
        base = runs[(vid, 1, 1.0)].loc[OOS_START:]
        print(f"  OOS lag1 1x: gross {base['gross'].mean()*TD*100:.2f}%/yr, "
              f"trading cost {base['cost'].mean()*TD*100:.2f}%/yr, swap markup "
              f"{base['swap'].mean()*TD*100:.2f}%/yr, mean gross leverage "
              f"{base['gross_lev'].mean():.2f}x, max margin use at 10% vol "
              f"{base['margin'].max()*100:.1f}%")

    # gate
    print("\n=== GATE (OOS, worse of lag1/lag2, 1x cost; 2x shown)")
    gate = {}
    for vid in VARIANTS:
        o = res[vid]
        worst = min((o[(1, 1.0)]["OOS"], o[(2, 1.0)]["OOS"]), key=lambda s: s["t"])
        worst2 = min((o[(1, 2.0)]["OOS"], o[(2, 2.0)]["OOS"]), key=lambda s: s["t"])
        p5 = min(o[(1, 1.0)]["OOS"]["p5_bp"], o[(2, 1.0)]["OOS"]["p5_bp"])
        ok = worst["t"] >= Z_BAR and p5 > 0
        gate[vid] = dict(t=worst["t"], p5=p5, t2x=worst2["t"], ok=ok,
                         sharpe=worst["sharpe"], sharpe2x=worst2["sharpe"],
                         is_sharpe=o[(1, 1.0)]["IS"]["sharpe"])
        print(f"  {vid} {VARIANTS[vid]:28s} IS Sharpe {gate[vid]['is_sharpe']:5.2f} | OOS Sharpe "
              f"{worst['sharpe']:5.2f} t {worst['t']:5.2f} p5 {p5:6.2f}bp | 2x: Sharpe "
              f"{worst2['sharpe']:5.2f} t {worst2['t']:5.2f} | t>=3.5504 & p5>0: "
              f"{'PASS' if ok else 'fail'}")
    head = max(VARIANTS, key=lambda v: gate[v]["is_sharpe"])
    print(f"\nHEADLINE (highest IS net Sharpe, lag1 1x): {head} {VARIANTS[head]}")

    # look-ahead / truncation on every variant
    print("\n=== future-truncation and future-perturbation tests (20 random cut days each)")
    for vid in VARIANTS:
        tr, pe, n = future_tests(vid, d, scalars)
        print(f"  {vid}: truncation identical {tr}/{n}, perturbation identical {pe}/{n}")

    # per-period and per-class diagnostics for the headline
    print(f"\n=== {head} by period (lag1, 1x)")
    df = runs[(head, 1, 1.0)]
    for a, b in (("1990", "1999"), ("2000", "2007"), ("2008", "2012"),
                 ("2013", "2017"), ("2018", "2021"), ("2022", "2026")):
        x = df.loc[a:b, "net"]
        if len(x) > 200:
            s = summary(x, 0)
            print(f"  {a}-{b}: Sharpe {s['sharpe']:5.2f} CAGR {s['cagr']*100:6.2f}% maxDD {s['max_dd']*100:6.1f}%")
    yrs = df.loc[OOS_START:, "net"].groupby(df.loc[OOS_START:].index.year).apply(
        lambda s: (1 + s).prod() - 1)
    print("  OOS calendar years:", ", ".join(f"{y}: {v*100:+.1f}%" for y, v in yrs.items()))
    print("\n=== trend by class (diagnostic, not counted, lag1 1x)")
    for cls in ("FX", "IDX", "CMD", "BOND"):
        dfc, _ = run("CLS-" + cls, d, scalars)
        dfc = active(dfc)
        for lab, x in (("IS", dfc.loc[:IS_END, "net"]), ("OOS", dfc.loc[OOS_START:, "net"])):
            if len(x) > 200:
                s = summary(x, 0)
                print(f"  {cls:4s} {lab:3s}: Sharpe {s['sharpe']:5.2f} t {s['t']:5.2f} CAGR {s['cagr']*100:6.2f}%")
    print("\n=== correlations of sleeves, OOS daily net (lag1 1x)")
    C = pd.DataFrame({v: runs[(v, 1, 1.0)].loc[OOS_START:, "net"] for v in
                      ("D2-01", "D2-04", "D2-05", "D2-09")}).corr()
    print(C.round(2).to_string())
    us = d["R"]["US500"].loc[OOS_START:]
    print("  corr(headline, US500 financed return) OOS:",
          round(runs[(head, 1, 1.0)].loc[OOS_START:, "net"].corr(us), 2))

    # prop simulation
    print(f"\n=== prop simulation, {head}: FTMO-type swing 10% static max loss / 5% daily,"
          f" 4% and 91% breach buffers; {npaths} bootstrap paths per vol")
    is_df = runs[(head, 1, 1.0)].loc[:IS_END]
    g_is = prop_grid(is_df, npaths)
    vstar = float(g_is.loc[g_is["exp_net"].idxmax(), "vol"])
    print("  IS grid (chooses the vol):")
    print(g_is.round(3).to_string(index=False))
    print(f"  vol chosen on IS: {vstar:.2f}")
    for lag in (1, 2):
        for cm in (1.0, 2.0):
            o_df = runs[(head, lag, cm)].loc[OOS_START:]
            g = prop_grid(o_df, npaths)
            row = g.loc[np.isclose(g["vol"], vstar)].iloc[0]
            best = g.loc[g["exp_net"].idxmax()]
            print(f"  OOS lag{lag} cost{cm:.0f}x at IS-chosen vol {vstar:.2f}: pass {row.p_pass:.3f} "
                  f"blow {row.p_blow_eval:.3f} abandon {row.p_abandon:.3f} median days {row.med_days_pass:.0f} "
                  f"funded 2y survival {row.funded_survival:.3f} E[payout|funded] ${row.exp_payout_if_funded:,.0f} "
                  f"E[net/attempt] ${row.exp_net:,.0f} ({row.exp_net_per_fee:+.2f}x fee)"
                  f" | OOS-optimal (reference only) vol {best.vol:.2f} E[net] ${best.exp_net:,.0f}")
            if lag == 1 and cm == 1.0:
                print("  OOS grid lag1 1x:")
                print(g.round(3).to_string(index=False))
                full = o_df["net"] * (vstar / 0.10)
                s = summary(full, 0)
                print(f"  OOS at vol {vstar:.2f} (no prop rules): {fmt(s)}")
                print(f"  margin use at vol {vstar:.2f}: median {o_df['margin'].median()*vstar/0.10*100:.1f}% "
                      f"max {o_df['margin'].max()*vstar/0.10*100:.1f}% of equity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
