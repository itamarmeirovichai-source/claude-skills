import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
w1=L.g_tsmom(d); w5=L.g_xsmom(d,28); w7=L.g_carry(d)
def m(D,R,t):
    g=L.evaluate([(D,R,0.0,False)],data=d).gross; sd=g.rolling(60,min_periods=60).std()*np.sqrt(365); return (t/sd).clip(upper=3).fillna(0)
m1,m5,m7=m(w1,d.ret,.1),m(w5,d.ret,.1),m(w7,d.pret,.1)
for nm,D,R in (("TSMOM part",w1.mul(m1,axis=0),d.ret),("XSMOM part",w5.mul(m5,axis=0),d.ret),("carry part",w7.mul(m7,axis=0),d.pret)):
    ev=L.evaluate([(D,R,L.C_PERP,True)],data=d).loc[o0:o1]
    s=L.stats(ev.net.values,nboot=500)
    print(f"{nm}: OOS standalone net {s['mean_bp']:.2f} bp/d t {s['t']:.2f}; gross {ev.gross.mean()*1e4:.2f} fund {ev.fund.mean()*1e4:.2f} cost {ev.cost.mean()*1e4:.2f}; years", {y:round(g.mean()*1e4,1) for y,g in ev.net.groupby(ev.index.year)})
print("mean multipliers OOS m1,m5,m7:", round(m1.loc[o0:o1].mean(),2), round(m5.loc[o0:o1].mean(),2), round(m7.loc[o0:o1].mean(),2), " share of days m at cap 3:", round((m1.loc[o0:o1]>=3).mean(),2), round((m5.loc[o0:o1]>=3).mean(),2), round((m7.loc[o0:o1]>=3).mean(),2))
# D3-11 multiplier
m11=m(w1,d.ret,.2); print("D3-11 m mean OOS", round(m11.loc[o0:o1].mean(),2), "cap share", round((m11.loc[o0:o1]>=3).mean(),2))
