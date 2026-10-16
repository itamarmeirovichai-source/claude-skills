"""F1 (wave 3): the pre-registered equal-risk stack, exactly as agents/prereg/F1.csv (F1-00..03,
pushed in d2a5938 before this file existed).

Sleeves are rebuilt with the departments' own code, unchanged:
  S1 crypto vol-managed TSMOM  = daily/w1-crypto/d3lib.py (D3-11), universe restricted to FTMO crypto CFDs
  S2 US100 30-minute VWAP trend = daily/vwap30-H0022/vwap30.py (H0022 positions and per-day P&L)

usage: CLAUDE_SCRATCH=<data dir> python3 ensemble.py <binance parquet dir> [--trunc]
Data are never committed (Binance from w1-crypto/download.py, NQ from 2026-10-04/data_fetch.py).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DAILY = HERE.parent
sys.path.insert(0, str(DAILY / "w1-crypto"))
sys.path.insert(0, str(DAILY / "vwap30-H0022"))
import d3lib as D3                      # noqa: E402
import loaders as L                     # noqa: E402  (vwap30-H0022/loaders.py)
import vwap30 as V                      # noqa: E402

BAR = 3.5745                             # z(0.05/285), wave-3 bar
W0, W1 = pd.Timestamp("2023-01-01"), pd.Timestamp("2026-05-07")
SPLICE_1M_END = pd.Timestamp("2025-11-21")   # last nq_1m session; 5m used from the next session on
FTMO = ("BTC ETH LTC XRP XMR NEO ADA DOT DOGE SOL AVAX BCH ETC BNB SAND LINK NEAR ALGO ICP AAVE HBAR "
        "GALA MANA VET XLM UNI XTZ DASH").split()
# FTMO costs (symbol table 2026-10-12): crypto 0.065% commission + 5 bp half spread per side,
# swap -30%/yr both sides per calendar day; US100.cash 0.75 pt per unit (1.5 pt round-trip spread)
C1_FTMO, SWAP_FTMO = 0.00065 + 0.0005, 0.30 / 365
C2_FTMO, C2_FUT = 0.75, 0.375
TARGET, LOOK, K1_CAP, K2_CAP, LEV_US100 = 0.10, 120, 3.0, 5.0, 15.0


# ───────────────────────────── S1: crypto ─────────────────────────────
def g_tsmom_ftmo(data):
    """D3-01 weights with N_t and the mask restricted to FTMO-listed coins in U_m."""
    s = D3.tsmom_signal(data)
    lev = (0.5 / D3.sigma(data)).clip(upper=1.5)
    Uh, _ = D3.holding_universe(data)
    listed = pd.Series([c in FTMO for c in s.columns], index=s.columns)
    mask = Uh & s.notna() & lev.notna() & listed
    n = mask.sum(axis=1).replace(0, np.nan)
    return (s * lev).where(mask, 0.0).div(n, axis=0).fillna(0.0)


def vol_managed(data, w):
    """D3-11 multiplier: min(0.20 / sd60(gross) * sqrt365, 3) -- copied from w1-crypto/run.py m()."""
    g = D3.evaluate([(w, data.ret, 0.0, False)], data=data).gross
    sd = g.rolling(60, min_periods=60).std() * np.sqrt(365)
    return w.mul((0.20 / sd).clip(upper=3).fillna(0.0), axis=0)


def s1_decisions(data, which):
    w = g_tsmom_ftmo(data) if which == "ftmo" else D3.g_tsmom(data, coins=["BTC", "ETH"])
    return vol_managed(data, w)


def s1_ftmo_eval(D, data, mult=1.0):
    """Net daily return at FTMO CFD costs: commission+spread on turnover, swap on gross held notional."""
    base = D3.evaluate([(D, data.ret, 0.0, False)], data=data)
    Wh = D.shift(1).fillna(0.0).abs().sum(axis=1)
    cost = mult * C1_FTMO * base.to
    swap = mult * SWAP_FTMO * Wh
    return pd.DataFrame(dict(gross=base.gross, cost=cost, swap=swap, net=base.gross - cost - swap,
                             gross_notional=Wh, to=base.to))


def s1_venue_eval(D, data):
    """D3's own Binance-perp costs (7 bp/side + actual funding), as in D3-11."""
    e = D3.evaluate([(D, data.ret, D3.C_PERP, True)], data=data)
    return pd.DataFrame(dict(net=e.net, net2=e.net2, gross_notional=D.shift(1).fillna(0).abs().sum(axis=1)))


# ───────────────────────────── S2: US100 ─────────────────────────────
def load_nq5() -> pd.DataFrame:
    p = L.SCR / "intraday/nq_5m.csv"
    import hashlib
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert h == "748add4222ef6d663aed0884d0c77a889bd3cf0cf17af636badc83428bfc9abd", h
    d = pd.read_csv(p)
    t = pd.to_datetime(d["datetime"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    d = d.assign(dt=t).set_index("dt").sort_index()
    d = d.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    return d[~d.index.duplicated()][["o", "h", "l", "c", "v"]].astype(float)


def s2_days(raw: pd.DataFrame, cost_pts: float, end=None) -> pd.DataFrame:
    """H0022 per-session net return per unit notional (fraction), roll weeks excluded."""
    if end is not None:
        raw = raw[raw.date <= end.date()]
    days = sorted(set(raw.date))
    excl = L.roll_excluded(days)
    r = raw[~raw.date.isin(excl)]
    day, *_ = V.run(r, lambda p: np.full(np.shape(p), cost_pts))
    out = pd.DataFrame(dict(net=day.net.values / 1e4, gross=day.gross.values / 1e4,
                            units=day.units.values), index=pd.to_datetime(day.date))
    return out


def nq_raw():
    m1 = L.rth(L.load_nq())
    m5 = L.rth(load_nq5())
    return m1, m5


def s2_series(m1, m5, cost_pts, end=None, which="splice"):
    a = s2_days(m1, cost_pts, end)
    if which == "1m":
        return a
    b = s2_days(m5, cost_pts, end)
    if which == "5m":
        return b
    return pd.concat([a.loc[:SPLICE_1M_END], b.loc[SPLICE_1M_END + pd.Timedelta(days=1):]])


# ───────────────────────────── stack ─────────────────────────────
def risk_weights(r1: pd.Series, r2obs: pd.Series, cal: pd.DatetimeIndex) -> pd.DataFrame:
    """k_i fixed on the 1st of each month from the last 120 obs through the previous month end."""
    rows = {}
    for m0 in cal[cal.day == 1]:
        prev = m0 - pd.Timedelta(days=1)
        a = r1.loc[:prev].dropna().iloc[-LOOK:]
        b = r2obs.loc[:prev].iloc[-LOOK:]
        k1 = min(TARGET / (a.std() * np.sqrt(365)), K1_CAP) if len(a) == LOOK else np.nan
        k2 = min(TARGET / (b.std() * np.sqrt(252)), K2_CAP) if len(b) == LOOK else np.nan
        rows[m0] = (k1, k2)
    k = pd.DataFrame.from_dict(rows, orient="index", columns=["k1", "k2"]).reindex(cal).ffill()
    return k


def stack(s1: pd.DataFrame, s2: pd.DataFrame, s1col="net", s2col="net", k=None):
    cal = pd.date_range(min(s1.index[0], s2.index[0]), min(s1.index[-1], W1), freq="D")
    r1 = s1[s1col].reindex(cal)
    r2 = s2[s2col].reindex(cal).fillna(0.0)
    if k is None:
        k = risk_weights(s1["net"].reindex(cal), s2["net"], cal)
    g1 = s1.gross_notional.reindex(cal).fillna(0.0)
    u2 = (s2.units.reindex(cal).fillna(0.0) > 0).astype(float)
    margin = k.k1 * g1 + k.k2 * u2 / LEV_US100
    f = (1.0 / margin).clip(upper=1.0).where(margin > 0, 1.0)
    r = f * (k.k1 * r1 + k.k2 * r2)
    return pd.DataFrame(dict(r=r, r1=r1, r2=r2, k1=k.k1, k2=k.k2, f=f, margin=margin, n1=k.k1 * g1,
                             n2=k.k2 * u2))


def summarize(x: pd.Series):
    x = x.loc[W0:W1].dropna()
    s = D3.stats(x.values)
    s["years"] = {str(y): float(g.mean() * 1e4) for y, g in x.groupby(x.index.year)}
    return s


def main():
    data = D3.load(sys.argv[1])
    m1, m5 = nq_raw()
    out = {}
    S2 = {c: s2_series(m1, m5, c) for c in (C2_FTMO, 2 * C2_FTMO, C2_FUT)}
    S2_2fut = s2_series(m1, m5, 2 * C2_FUT)
    # data check: 1m vs 5m S2 on their overlap
    a, b = s2_days(m1, C2_FTMO), s2_days(m5, C2_FTMO)
    j = a.net.to_frame("m1").join(b.net.to_frame("m5"), how="inner").loc[W0:SPLICE_1M_END]
    out["check_1m_vs_5m"] = dict(n=len(j), corr=float(j.m1.corr(j.m5)), mean_m1_bp=float(j.m1.mean() * 1e4),
                                 mean_m5_bp=float(j.m5.mean() * 1e4))
    res = {}
    for vid, which in (("F1-01", "ftmo"), ("F1-02", "btceth")):
        D = s1_decisions(data, which)
        s1 = s1_ftmo_eval(D, data)
        s1x2 = s1_ftmo_eval(D, data, 2.0)
        st = stack(s1, S2[C2_FTMO])
        k = st[["k1", "k2"]]
        st2 = stack(s1.assign(net=s1x2.net), S2[2 * C2_FTMO], k=k)   # same weights, doubled costs
        res[vid] = dict(st=st, st2=st2, s1=s1, s1x2=s1x2, D=D, s2=S2[C2_FTMO])
        if vid == "F1-01":
            v = s1_venue_eval(D, data)
            sv = stack(v, S2[C2_FUT], k=k)
            sv2 = stack(v.assign(net=v.net2), S2_2fut, k=k)
            res["F1-03"] = dict(st=sv, st2=sv2, s1=v, s2=S2[C2_FUT])
    for vid, R in res.items():
        st, st2 = R["st"], R["st2"]
        w = st.loc[W0:W1]
        o = dict(stack=summarize(st.r), stack_x2=summarize(st2.r),
                 s1=summarize(st.r1), s2=summarize(R["s2"].net),
                 s1_scaled=summarize(st.k1 * st.r1), s2_scaled=summarize(st.k2 * st.r2),
                 corr_r1_r2_all=float(w.r1.corr(w.r2)),
                 corr_r1_r2_sessions=float(w.r1[w.r2 != 0].corr(w.r2[w.r2 != 0])),
                 k1_mean=float(w.k1.mean()), k2_mean=float(w.k2.mean()),
                 margin_cap_days=int((w.f < 1).sum()), margin_max=float(w.margin.max()),
                 n1_mean=float(w.n1.mean()), n1_max=float(w.n1.max()))
        if "s1x2" in R:
            s1 = R["s1"].loc[W0:W1]
            o["s1_cost_bp"] = float(s1.cost.mean() * 1e4)
            o["s1_swap_bp"] = float(s1.swap.mean() * 1e4)
            o["s1_gross_bp"] = float(s1.gross.mean() * 1e4)
            o["s1_gross_notional"] = float(s1.gross_notional.mean())
            o["s1_turnover"] = float(s1.to.mean())
        o["gate"] = bool(o["stack"]["mean_bp"] > 0 and o["stack"]["t"] >= BAR and o["stack"]["p5_bp"] > 0)
        out[vid] = o
        st.to_csv(HERE / f"daily_{vid}.csv.gz", float_format="%.7g")
    # context correlations (headline window): BTC and NQ buy-and-hold
    w = res["F1-01"]["st"].loc[W0:W1]
    btc = data.ret["BTC"].reindex(w.index)
    nqd = m1.groupby("date").agg(o=("o", "first"), c=("c", "last"))
    nq5 = m5.groupby("date").agg(o=("o", "first"), c=("c", "last"))
    nqd = pd.concat([nqd.loc[:SPLICE_1M_END.date()], nq5.loc[(SPLICE_1M_END + pd.Timedelta(days=1)).date():]])
    nqr = (nqd.c / nqd.o - 1)
    nqr.index = pd.to_datetime(nqr.index)
    C = pd.DataFrame(dict(S1=w.r1, S2=w.r2.where(w.r2 != 0), stack=w.r, BTC=btc, NQ_rth=nqr.reindex(w.index)))
    out["corr_sessions"] = C.dropna().corr().round(3).to_dict()
    out["corr_all_days"] = C.assign(S2=C.S2.fillna(0), NQ_rth=C.NQ_rth.fillna(0)).corr().round(3).to_dict()
    json.dump(out, open(HERE / "results.json", "w"), indent=1, default=float)
    return out, res


def fmt(out):
    L_ = []
    L_.append(f"1m vs 5m S2 check: {out['check_1m_vs_5m']}")
    for vid in ("F1-01", "F1-02", "F1-03"):
        o = out[vid]
        L_.append(f"\n=== {vid}  gate={'PASS' if o['gate'] else 'FAIL'}  (bar t {BAR})")
        for key in ("stack", "stack_x2", "s1", "s2", "s1_scaled", "s2_scaled"):
            s = o[key]
            L_.append(f"  {key:10s} n {s['n']:5d} mean {s['mean_bp']:+7.2f} bp/d  t iid {s['t_iid']:+5.2f} "
                      f"NW {s['t_nw']:+5.2f} t {s['t']:+5.2f}  p5 {s['p5_bp']:+7.2f} (iid {s['p5_iid_bp']:+.2f} "
                      f"blk {s['p5_blk_bp']:+.2f})  Sharpe(365) {s['sharpe']:+5.2f}  vol {s['vol']:.3f}  "
                      f"maxDD {s['maxdd']:+.3f}  worst {s['worst']:+.4f}  CAGR {s['cagr']:+.3f}")
            L_.append("             years: " + "  ".join(f"{y} {v:+.2f}" for y, v in s["years"].items()))
        L_.append(f"  corr r1,r2 all days {o['corr_r1_r2_all']:+.3f}  on sessions {o['corr_r1_r2_sessions']:+.3f}; "
                  f"k1 {o['k1_mean']:.2f} k2 {o['k2_mean']:.2f}; margin-cap days {o['margin_cap_days']}, "
                  f"max margin {o['margin_max']:.2f}; crypto notional mean {o['n1_mean']:.2f} max {o['n1_max']:.2f}")
        if "s1_swap_bp" in o:
            L_.append(f"  S1 unit book: gross {o['s1_gross_bp']:+.2f} bp/d, trading cost {o['s1_cost_bp']:.2f}, "
                      f"swap {o['s1_swap_bp']:.2f}, mean gross notional {o['s1_gross_notional']:.3f}, "
                      f"turnover {o['s1_turnover']:.3f}/d")
    L_.append("\ncorrelation (NQ session days, W):")
    L_.append(pd.DataFrame(out["corr_sessions"]).to_string())
    L_.append("\ncorrelation (all calendar days, W; S2/NQ = 0 off-session):")
    L_.append(pd.DataFrame(out["corr_all_days"]).to_string())
    return "\n".join(L_)


if __name__ == "__main__":
    out, res = main()
    txt = fmt(out)
    print(txt)
    (HERE / "run.txt").write_text(txt + "\n")
