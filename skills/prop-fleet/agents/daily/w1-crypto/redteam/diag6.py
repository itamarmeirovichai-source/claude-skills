import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
ws,wp=L.g_cashcarry(d)
W=ws.shift(1).fillna(0)
for c in ["FTM","MATIC"]:
    contr=(W[c]*(d.ret[c].fillna(0)-d.pret[c].fillna(0)))
    big=contr.loc[o0:o1].abs().sort_values().tail(4).index.sort_values()
    for t in big:
        lo,hi=t-pd.Timedelta(days=3),t+pd.Timedelta(days=2)
        print(c); print(pd.DataFrame({"w_spot":W[c],"spot":d.close[c],"perp":d.pclose[c],"r":d.ret[c],"pr":d.pret[c],"pnl_bp":contr*1e4,"fund":d.fdaily[c]}).loc[lo:hi].to_string())
