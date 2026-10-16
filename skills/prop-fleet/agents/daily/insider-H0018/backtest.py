"""H0018 stage 2: pre-registered test. Each month-end, buy equal-weight every stock with >=1
opportunistic officer/director purchase FILED that month; hold one month; 20 bp round-trip cost;
exclude raw price < $5; benchmark SPY (total return). IS = signal months 2009-2016, OOS = 2017-latest.
Fixed implementation choices (set before results):
 - Formation = last SPY trading day of the signal month; the stock must have a close that day.
 - Ticker-mismatch guard: drop if formation raw close is outside [0.5x, 2x] the median Form 4
   purchase price (catches recycled/wrong tickers on Yahoo).
 - Return = adjclose(end of next month)/adjclose(formation)-1; if the series stops mid-month the
   last available adjclose is used (delisting return otherwise unobserved).
 - Turnover = 0.5*sum|w_new - w_old_drifted|; cost = turnover * round-trip cost.
 - Sharpe = annualised mean/sd of monthly net return (no risk-free deduction).
Usage: python -I backtest.py <signals.csv> <prices.parquet> [routine]"""
import sys, numpy as np, pandas as pd
BAR = 3.48
sig = pd.read_csv(sys.argv[1], parse_dates=["first_filing"])
sig["sig_month"] = pd.PeriodIndex(sig.sig_month, freq="M")
routine = len(sys.argv) > 3 and sys.argv[3] == "routine"
sig = sig[sig.routine == routine]
px = pd.read_parquet(sys.argv[2])
spy = px[px.ticker == "SPY"].set_index("date").sort_index()
cal = spy.index
me = pd.Series(cal, index=cal.to_period("M")).groupby(level=0).max()   # month -> last trading day
adj = px.pivot(index="date", columns="ticker", values="adjclose").reindex(cal)
raw = px.pivot(index="date", columns="ticker", values="raw_close").reindex(cal)

def run(cost_rt):
    recs, w_prev, r_prev = [], None, None
    months = sorted(m for m in sig.sig_month.unique() if m + 1 in me.index and m >= pd.Period("2009-01"))
    drop_px = drop_mis = drop_nopx = 0
    for m in months:
        f, e = me[m], me[m + 1]
        s = sig[sig.sig_month == m].groupby("ticker").med_px.median()
        s = s[s.index.isin(adj.columns)]
        drop_nopx += (sig.sig_month == m).sum() - len(s)
        rc = raw.loc[f, s.index]
        ok = rc.notna(); drop_nopx += (~ok).sum(); s, rc = s[ok], rc[ok]
        mis = (rc / s).between(0.5, 2.0) | s.isna() | (s <= 0)
        drop_mis += (~mis).sum(); s, rc = s[mis], rc[mis]
        keep = rc >= 5; drop_px += (~keep).sum(); names = s.index[keep]
        if len(names) == 0:
            recs.append(dict(month=m + 1, n=0, gross=0.0, turnover=0.0)); w_prev = None; continue
        a0 = adj.loc[f, names]
        a1 = adj.loc[f:e, names].ffill().iloc[-1]
        r = a1 / a0 - 1
        w = pd.Series(1 / len(names), index=names)
        if w_prev is None:
            to = 1.0
        else:
            drift = w_prev * (1 + r_prev); drift /= drift.sum()
            to = 0.5 * w.sub(drift, fill_value=0).abs().sum()
        recs.append(dict(month=m + 1, n=len(names), gross=float((w * r).sum()), turnover=to))
        w_prev, r_prev = w, r
    d = pd.DataFrame(recs).set_index("month")
    sp = spy.adjclose.groupby(cal.to_period("M")).last().pct_change()
    d["spy"] = sp.reindex(d.index).values
    d["net"] = d.gross - cost_rt * d.turnover
    d["excess"] = d.net - d.spy
    return d, dict(dropped_no_price=int(drop_nopx), dropped_mismatch=int(drop_mis), dropped_under5=int(drop_px))

def stats(d):
    x = d.excess; n = len(x)
    eq = (1 + d.net).cumprod()
    return dict(months=n, mean_ret=d.net.mean(), mean_excess=x.mean(), t_excess=x.mean() / (x.std(ddof=1) / np.sqrt(n)),
                sharpe=d.net.mean() / d.net.std() * np.sqrt(12), max_dd=(eq / eq.cummax() - 1).min(),
                avg_stocks=d.n.mean(), avg_turnover=d.turnover.mean(), mean_spy=d.spy.mean())

if __name__ == "__main__":
    tag = "routine (placebo)" if routine else "opportunistic"
    for cost, label in [(0.002, "20bp (pre-registered)"), (0.005, "50bp (SENSITIVITY only)")]:
        d, drops = run(cost)
        if cost == 0.002:
            print("signal-level drops:", drops)
            d.to_csv(f"monthly_{'routine' if routine else 'opp'}_20bp.csv")
        print(f"\n== {tag}, cost {label} ==")
        for name, sl in [("IS 2009-2016", d[(d.index >= pd.Period('2009-02')) & (d.index <= pd.Period('2017-01'))]),
                         ("OOS 2017-latest", d[d.index >= pd.Period('2017-02')])]:
            s = stats(sl)
            print(name, f"({sl.index.min()}..{sl.index.max()} holding months)")
            for k, v in s.items():
                print(f"   {k:14s} {v: .4f}")
        if cost == 0.002:
            so = stats(d[d.index >= pd.Period('2017-02')])
            print("\nDECISION (pre-registered, OOS @20bp): mean excess > 0 and t >= %.2f ->" % BAR,
                  "PASS" if so["mean_excess"] > 0 and so["t_excess"] >= BAR else "FAIL")
