import sys; sys.path.insert(0, '.')
import numpy as np, pandas as pd, loaders as L
SCR = L.SCR
tr = pd.read_csv(SCR / "e2_trades.csv", parse_dates=["date"])
spy = L.load_spy(); nq = L.load_nq()
def bar(df, ts): return df.loc[pd.Timestamp(ts)]
def prevclose(df, d):
    r = L.rth(df); dates = sorted(set(r.date)); i = dates.index(pd.Timestamp(d).date())
    return r[r.date == dates[i-1]].c.iloc[-1]
def got(v, mk, d):
    x = tr[(tr.variant==v)&(tr.market==mk)&(tr.date==d)].net_bp_1x
    return None if x.empty else float(x.iloc[0])
# E2-01 SPY 2022-11-02 (T=14:00)
d = "2022-11-02"
a = bar(spy, f"{d} 13:59").c; b = bar(spy, f"{d} 14:14").c; s = np.sign(b-a)
ep = bar(spy, f"{d} 14:15").o; xp = bar(spy, f"{d} 15:59").c
print("E2-01 SPY", d, "s", s, "mine", round(s*(xp-ep)/ep*1e4 - 2*0.03/ep*1e4, 4), "bt", got("E2-01","SPY",d))
a = bar(nq, f"{d} 13:59").c; b = bar(nq, f"{d} 14:14").c; s = np.sign(b-a)
ep = bar(nq, f"{d} 14:15").o; xp = bar(nq, f"{d} 15:59").c
print("E2-01 NQ ", d, "s", s, "mine", round(s*(xp-ep)/ep*1e4 - 2*0.375/ep*1e4, 4), "bt", got("E2-01","NQ",d))
# E2-06 NQ on roll+CPI day 2022-12-13
for d in ["2022-12-13", "2023-03-14", "2023-06-13", "2023-12-12", "2024-09-17"]:
    pc = prevclose(nq, d); o930 = bar(nq, f"{d} 09:30").o
    o0 = bar(nq, f"{d} 00:00").o; c_prev = nq[nq.index < pd.Timestamp(f"{d} 00:00")].c.iloc[-1]
    g_raw = np.log(o930/pc); adj = np.log(o0/c_prev); g = g_raw - adj
    ep = bar(nq, f"{d} 09:31").o; xp = bar(nq, f"{d} 15:59").c
    print(d, "gap raw bp", round(g_raw*1e4,1), "adj bp", round(adj*1e4,1), "g bp", round(g*1e4,1),
          "E2-06 mine", round(np.sign(g)*(xp-ep)/ep*1e4 - 0.75/ep*1e4, 4), "bt", got("E2-06","NQ",d))
