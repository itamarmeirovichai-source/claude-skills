"""Red-team independent checks (does not modify the engine)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
import stocks as S
from data import panels
D = S.prepare(panels())
cal = D["cal"]; E = S.universe(D, "A")
def sh(x): x = x.dropna(); return x.mean()/x.std()*np.sqrt(252), S.t_stats(x.values)[0]
def per(s):
    return {p: tuple(round(v,2) for v in sh(S.window(s,'x',p))) for p in ("IS","OOS")}

# 1. overnight data quality: share of eligible stock-days with on==0 exactly or bad open, by year
on = D["on"].where(E); bad = D["bad"] & E
y = cal.year
z = ((on == 0).sum(1) / E.sum(1)).groupby(y).mean()
b = (bad.sum(1) / E.sum(1)).groupby(y).mean()
print("on==0 share / bad-open share by year"); print(pd.DataFrame(dict(zero=z, bad=b)).round(3).T.to_string())

# 2. independent E1-01 recomputation (equal-weight quintile L/S, lag 0, gross)
r = D["r"]; s5 = r.rolling(5, min_periods=5).sum().where(E)
q = s5.rank(axis=1, pct=True)
W = ((q <= .2).astype(float).div((q <= .2).sum(1), axis=0) - (q > .8).astype(float).div((q > .8).sum(1), axis=0)) / 2
g = (W.shift(1).fillna(0) * r.fillna(0)).sum(1)
print("REV5 quintile LS gross (Sharpe,t):", per(g))
# year-by-year gross of engine E1-01 lag0
W1, _ = S.build("E1-01", D, "A"); g1 = S.pnl("E1-01", W1, None, D, "A", 0, 0.0)
print("E1-01 A gross by year (ann %):"); print((g1.groupby(y).mean()*252*100).round(1).to_string())

# 3. overnight persistence decile LS (LPS-style), overnight leg only, gross
so = S.sum_k(D["on"].fillna(0), 21, log=True).where(E)
q = so.rank(axis=1, pct=True)
Wd = ((q > .9).astype(float).div((q > .9).sum(1), axis=0) - (q <= .1).astype(float).div((q <= .1).sum(1), axis=0)) / 2
gon = (Wd.shift(1).fillna(0) * D["on"].fillna(0)).sum(1)
gid = (Wd.shift(1).fillna(0) * D["idr"].fillna(0)).sum(1)
print("OVN decile LS overnight leg:", per(gon), " intraday leg:", per(gid))
print("OVN decile LS overnight ann% by year:"); print((gon.groupby(y).mean()*252*100).round(1).to_string())

# 4. weekly variants: constant weights within week imply daily rebalancing. Drift-adjusted E1-02 A gross.
W2, _ = S.build("E1-02", D, "A")
wk = pd.Series(cal.to_period("W-FRI"), index=cal); last = (wk != wk.shift(-1)).values
Wt = W2.values.copy(); R = r.fillna(0).values; held = np.zeros(Wt.shape[1]); out = np.zeros(len(cal))
for i in range(1, len(cal)):
    out[i] = held @ R[i]
    held = held * (1 + R[i])
    if last[i]: held = Wt[i].copy()
gd = pd.Series(out, index=cal)
gc = S.pnl("E1-02", W2, None, D, "A", 0, 0.0)
print("E1-02 A gross const-wt:", per(gc), " buy-and-hold drift:", per(gd))

# 5. swap breakeven: what OOS t would best variants have with swap = 0 but spread/commission kept
for vid, u in [("E1-02","A"),("E1-03","A"),("E1-04","B"),("E1-07","B"),("E1-01","A")]:
    Wv, h = S.build(vid, D, u)
    sv = (S.SW_LONG, S.SW_SHORT, S.H_SW_LONG, S.H_SW_SHORT)
    S.SW_LONG = S.SW_SHORT = S.H_SW_LONG = S.H_SW_SHORT = 0.0
    res = [S.summ(S.window(S.pnl(vid, Wv, h, D, u, lag, 1.0), vid, "OOS"))["t"] for lag in (0, 1)]
    S.SW_LONG, S.SW_SHORT, S.H_SW_LONG, S.H_SW_SHORT = sv
    print(vid, u, "OOS t, no swap, 1x spread+comm, lag0/lag1:", [round(v,2) for v in res])

# 6. holiday nights charged: share of extra nights vs pure weekday+weekend
nt = D["nights"]; print("mean nights/day OOS:", round(S.window(nt,'x','OOS').mean(),4), "(365/252=", round(365/252,4), ")")
