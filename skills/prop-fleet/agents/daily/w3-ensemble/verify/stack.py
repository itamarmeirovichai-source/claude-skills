"""Verifier for F1-01..F1-03 (equal-risk stack S1 crypto D3-11 on FTMO coins + S2 H0022 on NQ).
Written from agents/prereg/F1.csv (F1-00), D3.csv (D3-00/01/11), ledger H0022 only.
Needs s2_nq.py to have been run first (writes <scratch>/verify_s2.parquet).

usage: python3 -I stack.py <scratch_dir>  > run.txt
"""
import json
import sys
import numpy as np
import pandas as pd

SCR = sys.argv[1]
BIN = f"{SCR}/data/bin"
W0, W1 = pd.Timestamp("2023-01-01"), pd.Timestamp("2026-05-07")

CANDS = ("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR AAVE "
         "ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM APE GALA "
         "CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
FTMO = set(("BTC ETH LTC XRP XMR NEO ADA DOT DOGE SOL AVAX BCH ETC BNB SAND LINK NEAR ALGO ICP AAVE HBAR GALA "
            "MANA VET XLM UNI XTZ DASH").split())


# ---------------------------------------------------------------- crypto data
def load_crypto():
    close, qv, fund, first = {}, {}, {}, {}
    for c in CANDS:
        try:
            h = pd.read_parquet(f"{BIN}/spot1h_{c}.parquet")
        except FileNotFoundError:
            print("missing spot", c)
            continue
        day = h.index.floor("D")
        g = h.groupby(day)
        close[c] = g["close"].last()          # close of the 23:00 bar (last bar of the UTC day if 23:00 missing)
        qv[c] = g["qvol"].sum()
        try:
            f = pd.read_parquet(f"{BIN}/funding_{c}.parquet")["f"]
            fund[c] = f.groupby(f.index.floor("D")).sum()
            first[c] = f.index.min().floor("D")
        except FileNotFoundError:
            pass
    idx = pd.date_range("2018-07-01", "2026-09-30", freq="D")
    C = pd.DataFrame(close).reindex(idx)
    Q = pd.DataFrame(qv).reindex(idx)
    F = pd.DataFrame(fund).reindex(idx).reindex(columns=C.columns)
    # funding: actual daily sum of prints; before a symbol's first print assume 0.0001 per 8h
    for c in C.columns:
        fp = first.get(c)
        pre = idx < fp if fp is not None else np.ones(len(idx), bool)
        F.loc[pre, c] = 0.0003
        F.loc[~pre, c] = F.loc[~pre, c].fillna(0.0)
    return C, Q, F


def universe(C, Q):
    """U_m for each month start: top 25 by prior-30d quote volume among coins with >=180d prior
    data and a bar on the last day of the previous month. Returns dict month_start -> set."""
    firstday = C.apply(lambda s: s.first_valid_index())
    U = {}
    for ms in pd.date_range("2019-01-01", "2026-09-01", freq="MS"):
        prev = ms - pd.Timedelta(days=1)
        ok = [c for c in C.columns if firstday[c] is not None and (ms - firstday[c]).days >= 180
              and pd.notna(C.at[prev, c])]
        vol = Q.loc[ms - pd.Timedelta(days=30): prev, ok].sum()
        U[ms] = set(vol.sort_values(ascending=False).index[:25])
    return U


def s1_book(C, F, members):
    """members(day) -> allowed coin set for weights held on that day. Returns daily frame with
    gross, turnover, gross notional, funding, and weights matrix."""
    r = C / C.shift(1) - 1
    sig = sum(np.sign(C / C.shift(L) - 1) for L in (20, 60, 120)) / 3.0
    vol = r.rolling(60, min_periods=60).std() * np.sqrt(365)
    raw = sig * np.minimum(0.5 / vol, 1.5)            # known at close of day t, held on t+1
    raw = raw.shift(1)                                 # row t+1 = weights held during day t+1
    valid = raw.notna() & r.notna()                    # coin needs a bar on t+1 (else closed at last close)
    idx = C.index
    allowed = pd.DataFrame(False, index=idx, columns=C.columns)
    for d in idx:
        m = members(d)
        allowed.loc[d, [c for c in C.columns if c in m]] = True
    ok = valid & allowed
    N = ok.sum(axis=1)
    w = raw.where(ok, 0.0).div(N.where(N > 0), axis=0).fillna(0.0)   # D3-01 weights (row = held day)
    rr = r.fillna(0.0)
    gross01 = (w * rr).sum(axis=1)                     # D3-01 gross on held day
    sd = gross01.rolling(60, min_periods=60).std() * np.sqrt(365)
    m = np.minimum(0.20 / sd, 3.0).shift(1)            # multiplier through day t, applied on t+1
    Wt = w.mul(m, axis=0).fillna(0.0)
    gross = (Wt * rr).sum(axis=1)
    drift = Wt.mul(1 + rr).div(1 + gross, axis=0)      # end-of-day drifted weights
    turn = (Wt - drift.shift(1).fillna(0.0)).abs().sum(axis=1)
    gn = Wt.abs().sum(axis=1)
    fundpay = (Wt * F.reindex(columns=Wt.columns)).sum(axis=1)
    return pd.DataFrame({"gross": gross, "turn": turn, "gn": gn, "fund": fundpay, "N": N, "m": m}), Wt


def s1_net(b, venue, cx):
    if venue == "ftmo":
        return b.gross - cx * 0.00115 * b.turn - cx * 0.30 / 365 * b.gn
    return b.gross - cx * 0.0007 * b.turn - b.fund       # Binance perp: 7 bp/side + actual funding


# ---------------------------------------------------------------- stats
def nw_t(x, L=10):
    x = np.asarray(x, float); n = len(x); e = x - x.mean()
    s = e @ e / n
    for l in range(1, L + 1):
        s += 2 * (1 - l / (L + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / np.sqrt(s / n)


def boot_p5(x, B=10000, blk=20):
    x = np.asarray(x, float); n = len(x)
    rng = np.random.default_rng(0)
    iid = np.array([x[rng.integers(0, n, n)].mean() for _ in range(B)])
    rng = np.random.default_rng(0)
    nb = int(np.ceil(n / blk))
    xx = np.concatenate([x, x[:blk]])
    bm = np.empty(B)
    for b in range(B):
        st = rng.integers(0, n, nb)
        ii = (st[:, None] + np.arange(blk)[None, :]).ravel()[:n]
        bm[b] = xx[ii].mean()
    return np.percentile(iid, 5), np.percentile(bm, 5)


def stats(r):
    x = r.to_numpy(); n = len(x)
    m = x.mean(); ti = m / (x.std(ddof=1) / np.sqrt(n)); tn = nw_t(x)
    pi, pb = boot_p5(x)
    eq = np.cumprod(1 + x); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    yr = r.groupby(r.index.year).mean() * 1e4
    return {"n": n, "mean_bp": m * 1e4, "t_iid": ti, "t_nw": tn, "t_min": min(ti, tn),
            "p5_iid_bp": pi * 1e4, "p5_block_bp": pb * 1e4, "p5_bp": min(pi, pb) * 1e4,
            "sharpe365": x.mean() / x.std(ddof=1) * np.sqrt(365), "maxdd_pct": dd * 100,
            "worst_day_pct": x.min() * 100, "worst_day": str(r.idxmin().date()),
            "per_year_bp": {int(k): round(v, 3) for k, v in yr.items()}}


# ---------------------------------------------------------------- k weights
def k_series(r1_all, r2_sess, days):
    """monthly k1,k2 from the last 120 obs through end of previous month."""
    out = []
    for ms in pd.date_range(days[0], days[-1], freq="MS"):
        prev = ms - pd.Timedelta(days=1)
        a = r1_all.loc[:prev].iloc[-120:]
        b = r2_sess.loc[:prev].iloc[-120:]
        s1 = a.std() * np.sqrt(365); s2 = b.std() * np.sqrt(252)
        out.append((ms, min(0.10 / s1, 3.0), min(0.10 / s2, 5.0), s1, s2))
    k = pd.DataFrame(out, columns=["ms", "k1", "k2", "sig1", "sig2"]).set_index("ms")
    return k.reindex(days, method="ffill")


def main():
    C, Q, F = load_crypto()
    U = universe(C, Q)
    print("universe sizes (FTMO-restricted) per month in W:",
          sorted({len(U[ms] & FTMO) for ms in U if ms >= W0}))
    mem_main = lambda d: U.get(d.to_period("M").to_timestamp(), set()) & FTMO
    mem_be = lambda d: {"BTC", "ETH"}
    s2 = pd.read_parquet(f"{SCR}/verify_s2.parquet")
    s2.index = pd.to_datetime(s2.index)
    s2ok = s2[~s2.roll]
    days = pd.date_range(W0, W1, freq="D")

    def r2_of(cost_pt, frame=s2ok):
        return ((frame.gross_pts - cost_pt * frame.units) / frame.px).fillna(0.0)

    btc = (C["BTC"] / C["BTC"].shift(1) - 1)
    nqc = s2["close"]; nqbh = (nqc / nqc.shift(1) - 1)

    results = {}
    books = {"F1-01": mem_main, "F1-02": mem_be}
    for name, mem in books.items():
        b, Wt = s1_book(C, F, mem)
        r1x1 = s1_net(b, "ftmo", 1)
        r2x1 = r2_of(0.75)
        k = k_series(r1x1, r2x1, days)
        L1 = b.gn.reindex(days)
        p2 = s2ok.anypos.reindex(days).fillna(0.0)
        lev = k.k1 * L1 + k.k2 * p2 / 15
        sc = np.where(lev > 1, 1 / lev, 1.0)
        k1, k2 = k.k1 * sc, k.k2 * sc
        capdays = int((lev > 1).sum())
        variants = [(name, "ftmo", 0.75)]
        if name == "F1-01":
            variants.append(("F1-03", "binance", 0.375))
        for vname, venue, pt in variants:
            for cx in (1, 2):
                r1 = s1_net(b, venue, cx).reindex(days)
                r2 = r2_of(pt * cx).reindex(days).fillna(0.0)
                st = (k1 * r1 + k2 * r2)
                res = stats(st)
                res.update({
                    "corr_r1_r2_calendar": r1.corr(r2),
                    "corr_r1_r2_sessiondays": r1[r2.index.isin(s2ok.index)].corr(r2[r2.index.isin(s2ok.index)]),
                    "r1_mean_bp": r1.mean() * 1e4, "r1_sharpe365": r1.mean() / r1.std() * np.sqrt(365),
                    "r2_mean_bp_cal": r2.mean() * 1e4,
                    "r2_mean_bp_session": r2[r2.index.isin(s2ok.index)].mean() * 1e4,
                    "r2_n_sessions": int(r2.index.isin(s2ok.index).sum()),
                    "k1_mean": k1.mean(), "k2_mean": k2.mean(),
                    "k1_raw_range": [k.k1.min(), k.k1.max()], "k2_raw_range": [k.k2.min(), k.k2.max()],
                    "k2_cap_months": int((k.k2.resample("MS").first() >= 5.0).sum()),
                    "k1_cap_months": int((k.k1.resample("MS").first() >= 3.0).sum()),
                    "margin_cap_days": capdays, "max_lev_raw": float(lev.max()),
                    "s1_gross_notional_mean": float(L1.mean()),
                    "s1_turnover_mean": float(b.turn.reindex(days).mean()),
                })
                if cx == 2 and venue == "ftmo":   # sensitivity: k recomputed from the 2x series
                    ka = k_series(s1_net(b, venue, 2), r2_of(pt * 2), days)
                    lv = ka.k1 * L1 + ka.k2 * p2 / 15
                    s_ = np.where(lv > 1, 1 / lv, 1.0)
                    sa = ka.k1 * s_ * r1 + ka.k2 * s_ * r2
                    res["alt_k_from_2x"] = {"mean_bp": sa.mean() * 1e4,
                                            "t_iid": sa.mean() / sa.std() * np.sqrt(len(sa)), "t_nw": nw_t(sa)}
                results[f"{vname} x{cx}"] = res
        if name == "F1-01":
            r1 = s1_net(b, "ftmo", 1).reindex(days); r2 = r2_of(0.75).reindex(days).fillna(0.0)
            cm = pd.DataFrame({"r1": r1, "r2": r2, "BTC": btc.reindex(days),
                               "NQ": nqbh.reindex(days).fillna(0.0)}).corr()
            results["corr_matrix_F1-01_x1"] = cm.round(3).to_dict()
            results["k_monthly_F1-01"] = k.resample("MS").first()[["k1", "k2", "sig1", "sig2"]].round(4).reset_index().astype(str).values.tolist()
            results["S1_alone_x1"] = {kk: v for kk, v in stats(r1).items() if kk != "per_year_bp"}
            results["S2_alone_x1_sessions"] = {kk: v for kk, v in stats(r2[r2.index.isin(s2ok.index)]).items()
                                               if kk != "per_year_bp"}
    # reproduction check: D3-11 as registered (full U_m, Binance perp costs), OOS 2023-01..2026-09
    bd, _ = s1_book(C, F, lambda d: U.get(d.to_period("M").to_timestamp(), set()))
    oos = pd.date_range("2023-01-01", "2026-09-30", freq="D")
    rd = s1_net(bd, "binance", 1).reindex(oos)
    results["check_D3-11_repro_OOS"] = {kk: v for kk, v in stats(rd).items()}
    results["check_D3-11_repro_OOS"]["gross_bp"] = bd.gross.reindex(oos).mean() * 1e4
    # data check: S2 daily from 1m vs 5m over 2023-01..2025-11 (non-roll, FTMO 1x)
    chk = pd.read_parquet(f"{SCR}/verify_s2_5mcheck.parquet"); chk.index = pd.to_datetime(chk.index)
    a = r2_of(0.75, s2ok[(s2ok.index >= "2023-01-01") & (s2ok.src == "1m")])
    bb = r2_of(0.75, chk[~chk.roll])
    j = a.to_frame("m1").join(bb.to_frame("m5"), how="inner")
    results["data_check_1m_vs_5m"] = {"n": len(j), "corr": j.m1.corr(j.m5),
                                      "mean_1m_bp": j.m1.mean() * 1e4, "mean_5m_bp": j.m5.mean() * 1e4}
    print(json.dumps(results, indent=1, default=float))
    json.dump(results, open(f"{SCR}/verify_results.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
