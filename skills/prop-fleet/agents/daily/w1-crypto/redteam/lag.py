import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
w2=L.g_tsmom(d,longflat=True); w1=L.g_tsmom(d); w4=L.g_intraday(d)
for nm,D,R,h in (("D3-02",w2,d.ret,False),("D3-01",w1,d.ret,False),("D3-04",w4,d.h_ret,True)):
    for lag in (0,1,2):
        ev=L.evaluate([(D.shift(lag).fillna(0),R,L.C_PERP,True)],hourly=h,data=d)
        a=ev.loc[o0:o1]; b=ev.loc[L.IS[0]:L.IS[1]]
        print(f"{nm} extra lag {lag} {'h' if h else 'd'}: OOS gross {a.gross.mean()*1e4:6.2f} net {a.net.mean()*1e4:6.2f} | IS gross {b.gross.mean()*1e4:6.2f}")
