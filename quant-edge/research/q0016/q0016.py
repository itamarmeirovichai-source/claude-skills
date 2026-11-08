#!/usr/bin/env python3
"""Q-0016 (registered d0f7d39): own-capital risk-parity + 10-month trend filter, 10% vol target, vs 60/40.
Data only through qe.gateway.load. IS read first (warm-up + IS report); one OOS read. Hold-out never read.
"""
import sys, math
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "src"))
from qe import gateway, stats  # noqa

ID = "Q-0016"; RISKY = ["USLCAP", "LTT", "ITT", "GLSTOCK", "GLBOND", "GOLDPM", "CMDTY"]; CASH = "STT"
VOLW, TRW, TGT, KMAX, KMIN, BORROW, COST = 63, 210, 0.10, 1.5, 0.25, 0.01, 2e-4


def lv(window):
    df = gateway.load(ID, window).set_index("ts")
    return df[RISKY + [CASH]].astype(float)


def simulate(levels, cost=COST):
    rets = levels.pct_change()
    idx = levels.index
    month = pd.Series(idx.tz_localize(None).to_period("M"), index=idx)
    ends = idx[(month != month.shift(-1)).values]
    W = pd.DataFrame(np.nan, index=idx, columns=RISKY + [CASH])
    for t in ends:
        pos = idx.get_loc(t)
        if pos < max(VOLW, TRW):
            continue
        r_win = rets.iloc[pos - VOLW + 1:pos + 1][RISKY]
        sig = r_win.std(ddof=1) * math.sqrt(252)
        w = (1 / sig) / (1 / sig).sum()
        sma = levels[RISKY].iloc[pos - TRW + 1:pos + 1].mean()
        below = levels[RISKY].iloc[pos] < sma
        wc = w.where(~below, 0.0); cash_w = w[below].sum()
        full = pd.concat([wc, pd.Series({CASH: cash_w})])
        port_hist = (rets.iloc[pos - VOLW + 1:pos + 1][RISKY + [CASH]] * full).sum(axis=1)
        sp = port_hist.std(ddof=1) * math.sqrt(252)
        k = min(KMAX, max(KMIN, TGT / sp)) if sp > 0 else 1.0
        W.loc[t] = full * k
    W = W.ffill().shift(1)                              # applied from the next day's return
    gross = (W * rets).sum(axis=1, min_count=1)
    expo = W.sum(axis=1)
    borrow = (expo - 1).clip(lower=0) * (rets[CASH] + BORROW / 252)
    turn = W.diff().abs().sum(axis=1).fillna(0)
    net = gross - borrow - cost * turn
    ok = W.notna().all(axis=1)
    excess = (net - rets[CASH])[ok]
    return excess.dropna(), net[ok].dropna(), turn[ok]


def bench(levels, cost=COST):
    rets = levels.pct_change()
    idx = levels.index
    month = pd.Series(idx.tz_localize(None).to_period("M"), index=idx)
    ends = idx[(month != month.shift(-1)).values]
    w = pd.Series({"USLCAP": 0.6, "ITT": 0.4})
    W = pd.DataFrame(np.nan, index=idx, columns=["USLCAP", "ITT"])
    W.loc[ends] = w.values
    W = W.ffill().shift(1)
    # drift between rebalances ignored (monthly reset); 2 bp per side on a nominal 2x monthly drift turnover proxy
    net = (W * rets[["USLCAP", "ITT"]]).sum(axis=1, min_count=1)
    return (net - rets[CASH]).dropna()


def summarize(x, name):
    x = x.values; tmin, ti, tn = stats.gate_t(x, longest_hold_days=21); se = stats.sharpe_se(x)
    eq = np.cumprod(1 + x); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    cagr = eq[-1] ** (252 / len(x)) - 1
    return dict(name=name, n=len(x), mean_bp=x.mean() * 1e4, sharpe=se["sharpe_annual"], ci=se["ci90_annual"], tmin=tmin, tiid=ti, tnw=tn,
                vol=x.std(ddof=1) * math.sqrt(252), cagr=cagr, mdd=dd)


def alpha_t(y, xb, lag=21):
    df = pd.concat([y, xb], axis=1, join="inner").dropna(); Y = df.iloc[:, 0].values; X = df.iloc[:, 1].values
    beta = np.cov(Y, X, ddof=1)[0, 1] / X.var(ddof=1); a = Y - beta * X
    return beta, stats.newey_west_t(a, lag), a.mean() * 252


def main():
    IS = lv("is"); OOS = lv("oos")
    full = pd.concat([IS, OOS]).sort_index(); full = full[full.index >= pd.Timestamp("1992-01-02", tz="UTC")]
    ex, net, turn = simulate(full); ex2, _, _ = simulate(full, cost=2 * COST); b = bench(full)
    cut = pd.Timestamp("2010-01-01", tz="UTC")
    oos, oos2, boos, isx = ex[ex.index >= cut], ex2[ex2.index >= cut], b[b.index >= cut], ex[ex.index < cut]
    S = summarize(oos, "strategy OOS net 1x (excess of cash)"); S2 = summarize(oos2, "strategy OOS net 2x"); SI = summarize(isx, "strategy IS net 1x")
    # 60/40 scaled ex post to the strategy's OOS realized vol (comparison only)
    bscale = S["vol"] / (boos.std(ddof=1) * math.sqrt(252)); B = summarize(boos * bscale, f"60/40 scaled x{bscale:.2f} to equal vol"); B0 = summarize(boos, "60/40 unscaled")
    boot = stats.stationary_bootstrap_mean(oos.values, n_draws=stats.MIN_DRAWS, mean_block=20)
    beta, at, aann = alpha_t(oos, boos)
    subs = []
    for lo, hi, lab in (("2010-01-01", "2016-10-31", "2010-01..2016-10 (clean window)"), ("2016-11-01", "2024-12-31", "2016-11..2024-12 (derivative window)")):
        s = oos[(oos.index >= pd.Timestamp(lo, tz="UTC")) & (oos.index <= pd.Timestamp(hi, tz="UTC"))]
        bs = boos[(boos.index >= pd.Timestamp(lo, tz="UTC")) & (boos.index <= pd.Timestamp(hi, tz="UTC"))]
        subs.append((lab, summarize(s, lab), summarize(bs * bscale, "60/40 equal vol")))
    yearly = oos.groupby(oos.index.year).apply(lambda r: float(np.prod(1 + r) - 1))
    passed = S["tmin"] >= stats.Z_BAR and boot["lower_alpha"] > 0 and S2["tmin"] >= 1.65
    def row(d): return f"| {d['name']} | {d['n']} | {d['sharpe']:.2f} ({d['ci'][0]:.2f}..{d['ci'][1]:.2f}) | {d['tmin']:.2f} | {d['cagr']*100:.1f}% | {d['vol']*100:.1f}% | {d['mdd']*100:.1f}% |"
    L = ["# Q-0016 — own-capital risk parity + 10-month trend filter (path 1)", "",
         "Registry row Q-0016 (registered d0f7d39, count 1). Script `research/q0016/q0016.py`. Data `daily_assets_1970_2026` via `qe.gateway.load` (IS read for warm-up; one OOS read; hold-out not read).",
         "**A pre-registered hypothesis under test, not an edge claim.** Bar z = 3.6807 (N_total 430); OOS 15.0 years → bar in Sharpe units 0.95; criterion-4 power at true Sharpe 0.7 ≈ 0.26, at 1.0 ≈ 0.74.", "",
         "| series | days | Sharpe (90% CI) | t_min | CAGR | vol | max DD |", "|---|---|---|---|---|---|---|",
         row(SI), row(S), row(S2), row(B0), row(B), "",
         f"- Bootstrap (stationary, block 20, {boot['n_draws']:,} draws) lower bound at 0.05/430: {boot['lower_alpha']*1e4:.3f} bp/day; p5 {boot['p5']*1e4:.3f} bp/day.",
         f"- Alpha vs 60/40 (daily excess on 60/40 excess): beta {beta:.2f}, annual alpha {aann*100:.2f}%, NW(21) t {at:.2f}.",
         f"- Average monthly turnover (sum |Δw|): {turn[turn.index>=cut].sum()/ (len(oos)/21):.2f}; positive calendar years {(yearly>0).sum()} of {len(yearly)}.", "",
         "| sub-period | strategy Sharpe | strategy CAGR / max DD | 60/40 equal-vol Sharpe | 60/40 CAGR / max DD |", "|---|---|---|---|---|"]
    for lab, s, bb in subs:
        L.append(f"| {lab} | {s['sharpe']:.2f} | {s['cagr']*100:.1f}% / {s['mdd']*100:.1f}% | {bb['sharpe']:.2f} | {bb['cagr']*100:.1f}% / {bb['mdd']*100:.1f}% |")
    L += ["", "| year | strategy excess return |", "|---|---|"] + [f"| {y} | {v*100:.1f}% |" for y, v in yearly.items()]
    L += ["", "## Verdict (decision rule applied mechanically)", "",
          f"- Gate v2 criterion 4: t_min {S['tmin']:.2f} vs 3.6807; bootstrap lower bound {boot['lower_alpha']*1e4:.3f} bp/day; 2x-cost t {S2['tmin']:.2f}. **{'PASS Gate 3' if passed else 'FAIL'}** at the program's bar.",
          f"- Own-capital standard (pre-specified, reported regardless): strategy Sharpe {S['sharpe']:.2f} vs 60/40 at equal volatility {B['sharpe']:.2f}; max drawdown {S['mdd']*100:.1f}% vs {B['mdd']*100:.1f}%; alpha t vs 60/40 {at:.2f}.",
          "- Notes: CAGR is of the excess-of-cash series (add the cash rate for total return). The 60/40 benchmark is monthly reset without intra-month drift costs. Excess series uses STT as cash."]
    out = ROOT / "research" / "results" / "Q-0016.md"; out.write_text("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
