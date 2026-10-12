"""Diagnostics (not counted variants): per-market average gross return per trade (in % of
notional) for the long RSI(2) and 3-down rules, IS vs OOS, close fill; and the worst book days."""
import numpy as np
import pandas as pd

import meanrev as M

data = M.load()
for rule in ("rsi", "down3"):
    print(f"\n== long-only {rule}, close fill, gross per trade (% of notional), no filter ==")
    for n, _, sl, ss, cb in M.MKT:
        df = data[n]
        pos, notl = M.positions(df, rule, ls=False, trend=False)
        r = df.close.pct_change().fillna(0).values
        held = np.r_[0, pos[:-1]]
        tid = np.cumsum((pos != 0) & (np.r_[0, pos[:-1]] == 0))
        tr = pd.DataFrame(dict(r=held * r, tid=np.r_[0, tid[:-1]], h=held), index=df.index)
        tr = tr[tr.h != 0]
        g = tr.groupby("tid").agg(ret=("r", lambda x: np.prod(1 + x) - 1), d=("r", "size"),
                                  date=("r", lambda x: x.index[0]))
        for lab, m in (("IS", g.date <= M.IS_END), ("OOS", g.date > M.IS_END)):
            x = g[m]
            print(f"{n:7s} {lab:3s} trades {len(x):4d}  mean {x.ret.mean()*100:+.3f}%  "
                  f"hit {(x.ret>0).mean():.2f}  days {x.d.mean():.2f}  t {x.ret.mean()/x.ret.std()*np.sqrt(len(x)):+.2f}")
b = M.book(data, "G2-01", "close")
print("\nG2-01 worst book days:\n", b.net.nsmallest(5).round(4), "\n", b.absexpo.loc[b.net.nsmallest(5).index].round(3))
