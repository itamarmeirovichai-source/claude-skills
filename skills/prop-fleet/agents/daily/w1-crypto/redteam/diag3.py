import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings, pickle; warnings.filterwarnings("ignore")
X="WLD ORDI FET RNDR RENDER TIA SEI BONK FLOKI JUP ENA STX LDO RUNE GMT BLUR CFX TAO NOT PEOPLE TRUMP ONDO PENGU BOME ETHFI W ZRO EIGEN S BERA LAYER KAITO VIRTUAL NEIRO MKR IMX GRT JASMY DYDX MAGIC ID ARKM PYTH STRK PNUT LUNC USTC WOO KAVA KSM 1INCH SNX OCEAN AGIX GMX MASK ACH HOOK CYBER TRB BAKE MEME ACT MOVE USUAL HYPE XPL ASTER WLFI".split()
L.CANDS=tuple(L.CANDS)+tuple(X)
p=f"{S}/redteam/cdata.pkl"
if os.path.exists(p): d=pickle.load(open(p,"rb"))
else: d=L.load(f"{S}/cdata"); pickle.dump(d,open(p,"wb"))
o0,o1=L.OOS
U,_=L.universe(d)
ou=U.loc[o0:o1]
newin=ou[[c for c in X if c in ou]].sum().sort_values(ascending=False)
print("extra coins: days in U_m OOS:", newin[newin>0].to_dict())
print("share of OOS universe slots taken by extra coins: %.1f%%"%(100*ou[[c for c in X if c in ou]].sum().sum()/ou.sum().sum()))
w1=L.g_tsmom(d); w2=L.g_tsmom(d,longflat=True)
g1=L.evaluate([(w1,d.ret,0.0,False)],data=d).gross
sd=g1.rolling(60,min_periods=60).std()*np.sqrt(365); w11=w1.mul((0.20/sd).clip(upper=3).fillna(0),axis=0)
w5=L.g_xsmom(d,28)
for k,w in (("D3-01",w1),("D3-02",w2),("D3-11",w11),("D3-05",w5)):
    ev=L.evaluate([(w,d.ret,L.C_PERP,True)],data=d)
    for nm,(a,b) in (("IS",L.IS),("OOS",L.OOS)):
        s=L.stats(ev.net.loc[a:b].values,nboot=2000)
        print(f"{k} expanded-cands {nm}: mean {s['mean_bp']:6.2f} t {s['t']:5.2f} (iid {s['t_iid']:.2f}) SR {s['sharpe']:.2f} MDD {s['maxdd']:.3f} p5 {s['p5_bp']:.2f}")
    print("   years:", {y:round(g.mean()*1e4,2) for y,g in ev.net.loc[o0:o1].groupby(ev.net.loc[o0:o1].index.year)})
