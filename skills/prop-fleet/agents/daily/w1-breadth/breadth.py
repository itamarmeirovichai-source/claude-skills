#!/usr/bin/env python3
"""D4 (w1-breadth) — the pre-registered run of agents/prereg/D4-spec.md (D4-01..D4-05).

    CLAUDE_SCRATCH=... python3 breadth.py > run.txt

Data from fetch.py (never committed). Every number in references/w1-breadth.md comes from
this script's output.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

from common import HISTDATA, IS_END, MARKETS, OOS_END, MIN, sessions, session_bars, arrays
from strategies import DECISIONS, execute

BAR = 3.5504
SEED_H = 20261011
OUT = os.path.join(os.environ.get("CLAUDE_SCRATCH", "/tmp"), "w1-breadth")


# ── eligibility (spec §3) and held-out draw (spec §4) ───────────────────────
def eligibility():
    rows = []
    for m, (O, C, tz, cs, src) in MARKETS.items():
        s = sessions(m)
        v = s[s.valid & (s.index <= IS_END)]
        sig_bp = v.lr.std() * 1e4
        rt = 2 * cs
        ok = len(v) >= 250 and rt <= 0.10 * sig_bp
        rows.append((m, len(v), sig_bp, rt, rt / sig_bp, ok))
    e = pd.DataFrame(rows, columns=["market", "n_IS", "sigma_IS_bp", "rt_cost_bp", "cost/sigma", "eligible"])
    return e.set_index("market")


def held_out(elig):
    oanda = sorted(m for m in elig.index[elig.eligible] if m not in HISTDATA)
    draw = list(np.random.default_rng(SEED_H).choice(oanda, 4, replace=False))
    return [m for m in ("GRXEUR", "ETXEUR") if elig.loc[m, "eligible"]] + draw


# ── per-market daily series ─────────────────────────────────────────────────
def run_market(m, heldout):
    s = sessions(m)
    cs = MARKETS[m][3]
    t_all, o_all, h_all, l_all, c_all = arrays(m)
    out = {k: [] for k in DECISIONS}
    for d, r in s.iterrows():
        if not r.valid or not (r.sig > 0):
            continue
        if heldout and d <= IS_END:          # spec §4: nothing computed for H in IS
            continue
        t, o, h, l, c = session_bars(m, r)
        for k, f in DECISIONS.items():
            ev = f(t, o, h, l, c, np.int64(r.tO), np.int64(r.tC), r.Cprev)
            g, cost, sides = execute(ev, t, o, c, np.int64(r.tC), cs)
            sc = 0.01 / r.sig
            out[k].append((d, g * sc, (g - cost) * sc, (g - 2 * cost) * sc, sides))
    res = {}
    for k, rows in out.items():
        res[k] = pd.DataFrame(rows, columns=["date", "gross", "net", "net2", "sides"]).set_index("date")
    return res, s.index[s.valid]


# ── statistics ──────────────────────────────────────────────────────────────
def stats(x):
    x = np.asarray(x, float)
    n = len(x)
    mu, sd = x.mean(), x.std(ddof=1)
    t = mu / (sd / np.sqrt(n))
    xc = x - mu
    v = xc @ xc / n
    for k in range(1, 6):
        v += 2 * (1 - k / 6) * (xc[k:] @ xc[:-k]) / n
    t_nw = mu / np.sqrt(v / n)
    rng = np.random.default_rng(0)
    p5_iid = np.percentile(x[rng.integers(0, n, (10_000, n))].mean(axis=1), 5)
    rng = np.random.default_rng(0)
    B = 20
    nb = int(np.ceil(n / B))
    st = rng.integers(0, n - B + 1, (10_000, nb))
    idx = (st[:, :, None] + np.arange(B)).reshape(10_000, -1)[:, :n]
    p5_blk = np.percentile(x[idx].mean(axis=1), 5)
    sh = mu / sd * np.sqrt(252)
    cum = np.cumsum(x * (0.10 / (sd * np.sqrt(252))))
    mdd = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum)
    return dict(n=n, mean=mu, t=t, t_nw=t_nw, p5_iid=p5_iid, p5_blk=p5_blk, sharpe=sh, mdd10=mdd * 100)


def fmt(s):
    return (f"n {s['n']:5d}  mean {s['mean']*100:+.3f}  t {s['t']:+.2f}  t_NW {s['t_nw']:+.2f}  "
            f"p5 iid {s['p5_iid']*100:+.3f} blk {s['p5_blk']*100:+.3f}  Sharpe {s['sharpe']:+.2f}  "
            f"maxDD@10%vol {s['mdd10']:.1f}%")


def basket(per, mkts, lo, hi, col, dates):
    """(1/K) sum over markets of u(m,d); dates = weekdays with >=1 valid session in split."""
    K = len(mkts)
    idx = dates[(dates > lo) & (dates <= hi)]
    tot = pd.Series(0.0, index=idx)
    for m in mkts:
        x = per[m][col]
        x = x[(x.index > lo) & (x.index <= hi)]
        tot = tot.add(x.reindex(idx).fillna(0.0), fill_value=0.0)
    return tot / K


# ── truncation test (spec G5a) ──────────────────────────────────────────────
def truncation_test(mkts, n=300):
    rng = np.random.default_rng(0)
    pairs = []
    for m in mkts:
        s = sessions(m)
        v = s[s.valid & (s.sig > 0)]
        pairs += [(m, d) for d in v.index]
    pick = [pairs[i] for i in rng.choice(len(pairs), n, replace=False)]
    checks = fails = 0
    for m, d in pick:
        r = sessions(m).loc[d]
        t, o, h, l, c = session_bars(m, r)
        O, C = np.int64(r.tO), np.int64(r.tC)
        for k, f in DECISIONS.items():
            full = f(t, o, h, l, c, O, C, r.Cprev)
            for T in t[(t >= O) & (t <= C)]:
                keep = t < T
                part = f(t[keep], o[keep], h[keep], l[keep], c[keep], O, C, r.Cprev)
                a = [e for e in full if e[0] <= T]
                b = [e for e in part if e[0] <= T]
                checks += 1
                if a != b:
                    fails += 1
                    if fails <= 5:
                        print("  TRUNCATION MISMATCH", m, d.date(), k, pd.Timestamp(T), a, b)
    # sigma uses earlier sessions only: recompute sigma at the picked dates from data before d
    sig_bad = 0
    for m, d in pick:
        s = sessions(m)
        v = s[s.valid & (s.index < d)]
        ref = np.log(v.MC / v.MO).tail(60)
        exp = ref.std() if len(ref) >= 40 else np.nan
        if not np.isclose(exp, s.loc[d, "sig"], equal_nan=True):
            sig_bad += 1
    return checks, fails, sig_bad


def main():
    pd.set_option("display.width", 200)
    print("D4 w1-breadth — pre-registered run (agents/prereg/D4-spec.md). Bar z = 3.5504.\n")
    elig = eligibility()
    print("Eligibility (spec §3: >=250 IS sessions and round-trip cost <= 0.10 x sigma_IS):")
    print(elig.round(3).to_string())
    H = held_out(elig)
    basket_m = list(elig.index[elig.eligible])
    D = [m for m in basket_m if m not in H]
    print(f"\nBasket K = {len(basket_m)}: {basket_m}")
    print(f"Held-out H ({len(H)}): {H}")
    print(f"Design   D ({len(D)}): {D}\n")

    per = {k: {} for k in DECISIONS}
    vdates = set()
    for m in basket_m:
        res, vd = run_market(m, m in H)
        for k in DECISIONS:
            per[k][m] = res[k]
        vdates |= set(vd)
        print(f"  ran {m}", file=sys.stderr, flush=True)
    dates = pd.DatetimeIndex(sorted(vdates))
    dates = dates[dates.weekday < 5]
    lo0, is_end, oos_end = pd.Timestamp("2000-01-01"), IS_END, OOS_END

    # blend D4-05
    variants = list(DECISIONS) + ["D4-05"]
    series = {}
    for k in DECISIONS:
        for split, mk, lo, hi in (("OOS", basket_m, is_end, oos_end), ("OOS_H", H, is_end, oos_end),
                                  ("OOS_D", D, is_end, oos_end), ("IS_D", D, lo0, is_end)):
            for col in ("gross", "net", "net2"):
                series[(k, split, col)] = basket(per[k], mk, lo, hi, col, dates)
    for split in ("OOS", "OOS_H", "OOS_D", "IS_D"):
        for col in ("gross", "net", "net2"):
            series[("D4-05", split, col)] = sum(series[(k, split, col)] for k in DECISIONS) / 4

    os.makedirs(OUT, exist_ok=True)
    pd.DataFrame({f"{k}|{s}|{c}": v for (k, s, c), v in series.items()}).to_csv(f"{OUT}/basket_daily.csv")
    for k in DECISIONS:
        pd.concat({m: per[k][m] for m in basket_m}).to_csv(f"{OUT}/per_market_{k}.csv")

    print("Units: basket daily mean in % of a market's 1% target session vol, i.e. x100 = bp of")
    print("capital per day if every market is sized to 1% session vol and the basket averages them.\n")
    verdict = {}
    for k in variants:
        print(f"===== {k} =====")
        for split in ("OOS", "OOS_D", "OOS_H", "IS_D"):
            for col in ("gross", "net", "net2"):
                print(f"  {split:6s} {col:5s} {fmt(stats(series[(k, split, col)].values))}")
        so = stats(series[(k, "OOS", "net")].values)
        s2 = stats(series[(k, "OOS", "net2")].values)
        g1 = so["mean"] > 0 and min(so["t"], so["t_nw"]) >= BAR
        g2 = min(so["p5_iid"], so["p5_blk"]) > 0
        g3 = series[(k, "OOS_H", "net")].mean() > 0
        g4 = series[(k, "IS_D", "gross")].mean() > 0
        verdict[k] = (g1, g2, g3, g4, so, s2)
        print(f"  gate: G1 t>={BAR} {g1} (min t {min(so['t'], so['t_nw']):+.2f})  G2 p5>0 {g2} "
              f"(min p5 {min(so['p5_iid'], so['p5_blk'])*100:+.3f})  G3 H net>0 {g3}  G4 IS_D gross>0 {g4}")
        worse = so if so["mean"] < s2["mean"] else s2
        print(f"  worse of cost x1/x2 (OOS net): mean {worse['mean']*100:+.3f} t {worse['t']:+.2f} Sharpe {worse['sharpe']:+.2f}")
        # per-year
        x = series[(k, "OOS", "net")]
        xi = series[(k, "IS_D", "net")]
        yr = pd.concat([xi, x])
        g = yr.groupby(yr.index.year)
        tab = pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100,
                            "t": g.mean() / (g.std() / np.sqrt(g.size())),
                            "Sharpe": g.mean() / g.std() * np.sqrt(252)})
        print("  per year net (<=2012 = IS design markets; >=2013 = OOS all basket):")
        print("   " + tab.round(2).to_string().replace("\n", "\n   "))
        print()

    # per-market OOS net Sharpe and correlation
    print("===== per-market OOS (2013..) net Sharpe of u (equal-vol), sides/session =====")
    pm = []
    for m in basket_m:
        row = [m, "H" if m in H else "D"]
        for k in DECISIONS:
            x = per[k][m]
            x = x[x.index > is_end]
            xr = x.net.reindex(dates[(dates > is_end) & (dates <= oos_end)]).fillna(0)
            row += [xr.mean() / xr.std() * np.sqrt(252) if xr.std() > 0 else np.nan, x.sides.mean()]
        pm.append(row)
    cols = ["market", "set"] + sum([[f"{k} Sh", f"{k} sides"] for k in DECISIONS], [])
    print(pd.DataFrame(pm, columns=cols).set_index("market").round(2).to_string())
    print()
    print("===== correlation of per-market OOS net daily P&L =====")
    od = dates[(dates > is_end) & (dates <= oos_end)]
    for k in DECISIONS:
        M = pd.DataFrame({m: per[k][m].net.reindex(od).fillna(0.0) for m in basket_m})
        R = M.corr().values
        K = R.shape[0]
        rb = (R.sum() - K) / (K * (K - 1))
        print(f"  {k}: mean pairwise rho {rb:+.3f}  max {np.max(R - np.eye(K)):+.3f}  "
              f"effective N = K/(1+(K-1)rho) = {K/(1+(K-1)*rb):.1f} of {K}")
    print()
    print("===== look-ahead: truncation test (300 random market-sessions, every bar) =====")
    checks, fails, sig_bad = truncation_test(basket_m)
    print(f"  {checks:,} cut points x variants checked, mismatches {fails}; sigma-from-past mismatches {sig_bad}")
    g5 = fails == 0 and sig_bad == 0
    print()
    print("===== GATE SUMMARY (bar 3.5504) =====")
    for k in variants:
        g1, g2, g3, g4, so, s2 = verdict[k]
        ok = g1 and g2 and g3 and g4 and g5
        print(f"  {k}: OOS net mean {so['mean']*100:+.3f} t {so['t']:+.2f} t_NW {so['t_nw']:+.2f} "
              f"p5 {min(so['p5_iid'], so['p5_blk'])*100:+.3f} Sharpe {so['sharpe']:+.2f} maxDD {so['mdd10']:.1f}% | "
              f"x2: mean {s2['mean']*100:+.3f} t {s2['t']:+.2f} | G1 {g1} G2 {g2} G3 {g3} G4 {g4} G5 {g5} -> "
              f"{'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
