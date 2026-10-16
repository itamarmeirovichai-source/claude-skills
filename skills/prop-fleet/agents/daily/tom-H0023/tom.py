"""H0023 turn-of-the-month on S&P 500 closes, exactly as pre-registered in ledger.csv.
Long from the close of trading day -2 (second-to-last trading day of the month) to the
close of trading day +3 of the next month. Returns are close-to-close; the position held
over day t's return is decided from the calendar only (no prices), so no look-ahead."""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parents[3] / "data" / "spx_open_close.csv"
Z = 3.5632
SPREAD, SWAP_YR = 1.0e-4, 0.025


def positions(idx):
    """1.0 on the days whose close-to-close return is held: trading days -1, +1, +2, +3
    (entering at the close of day -2 means holding the returns of days -1..+3)."""
    s = pd.Series(idx, index=idx)
    ym = idx.to_period("M")
    pos_in_month = s.groupby(ym).cumcount()            # 0 = first trading day
    from_end = s.groupby(ym).cumcount(ascending=False)  # 0 = last trading day
    hold = (from_end == 0) | (pos_in_month <= 2)        # day -1 (last) and +1..+3
    return hold.astype(float).values


def run(cost_mult=1.0):
    px = pd.read_csv(D, parse_dates=["Date"]).set_index("Date")["Close"]
    r = px.pct_change().dropna()
    pos = pd.Series(positions(r.index), index=r.index)
    # first day of the dataset's first month cannot have been entered: fine, tiny effect
    entry = (pos.diff().fillna(pos) > 0)               # day the held block starts
    gross = pos * r
    cost = cost_mult * (entry * SPREAD + pos * SWAP_YR / 252)
    return gross, gross - cost, pos


def stats(x, label):
    x = x.dropna()
    m, sd = x.mean(), x.std(ddof=1)
    t = m / (sd / np.sqrt(len(x)))
    rng = np.random.default_rng(0)
    bs = np.array([x.values[rng.integers(0, len(x), len(x))].mean() for _ in range(10000)])
    eq = x.cumsum()
    dd = (eq - eq.cummax()).min()
    print(f"{label}: days {len(x)} mean {m*1e4:+.3f} bp/day  t {t:+.2f}  p5 {np.percentile(bs,5)*1e4:+.3f} bp  "
          f"Sharpe {m/sd*np.sqrt(252):+.2f}  ret/yr {m*252:+.2%}  maxDD {dd:+.2%}  worst {x.min():+.2%}")
    return t, np.percentile(bs, 5)


if __name__ == "__main__":
    g, n, pos = run()
    _, n2, _ = run(2.0)
    print("exposure (share of days held):", round(pos.mean(), 3))
    stats(g.loc[:"2009"], "IS 1990-2009 gross")
    stats(n.loc[:"2009"], "IS 1990-2009 net")
    stats(g.loc["2010":], "OOS 2010-2026 gross")
    t, p5 = stats(n.loc["2010":], "OOS 2010-2026 net (DECISIVE)")
    stats(n2.loc["2010":], "OOS 2010-2026 net cost x2")
    # same-exposure benchmark: buy and hold S&P scaled to the same exposure
    px = pd.read_csv(D, parse_dates=["Date"]).set_index("Date")["Close"]
    bh = px.pct_change().dropna().loc["2010":] * pos.mean()
    stats(bh, "OOS buy&hold x exposure (benchmark)")
    print("per year net bp/day:", (n.loc["2010":].groupby(n.loc['2010':].index.year).mean() * 1e4).round(2).to_dict())
    print("VERDICT:", "PASS" if (t >= Z and p5 > 0) else "FAIL", f"(t {t:.2f} vs {Z}, p5 {p5*1e4:.3f} bp)")
