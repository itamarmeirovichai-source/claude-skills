import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings, copy; warnings.filterwarnings("ignore")
exec(open(f"{S}/redteam/diag5.py").read().split("w7b=g_carry8")[0].split("# patch A")[1].split("\n",1)[1])  # defines g_carry8, g_cc8
d=data()
dead=pd.DataFrame(False,index=d.close.index,columns=d.close.columns)
for c in d.close.columns:
    try: p=pd.read_parquet(f"{S}/data/perp1d_{c}.parquet")
    except FileNotFoundError: continue
    p=p[~p.index.duplicated()].reindex(d.close.index); dead[c]=(p.volume==0)
    dead.loc[p[p.volume>0].index.max()+pd.Timedelta(days=1):,c]=True
d2=copy.copy(d); d2.pclose=d.pclose.mask(dead); d2.pret=d.pret.mask(dead|dead.shift(1,fill_value=False))
d2.fund=d.fund.mask(dead); d2.fund_n=d.fund_n.mask(dead); d2.fdaily=d.fdaily.mask(dead,L.F_DEFAULT)
for tag,dd in (("per-8h only",d),("per-8h + stale fix",d2)):
    w1=L.g_tsmom(dd); w5=L.g_xsmom(dd,28); w7=g_carry8(dd); ws,wp=g_cc8(dd)
    def m(D,R,t):
        g=L.evaluate([(D,R,0.0,False)],data=dd).gross; sd=g.rolling(60,min_periods=60).std()*np.sqrt(365); return (t/sd).clip(upper=3).fillna(0)
    out={"D3-07":[(w7,dd.pret,L.C_PERP,True)],"D3-08":[(ws,dd.ret,L.C_SPOT,False),(wp,dd.pret,L.C_PERP,True)],
         "D3-10":[(w1.mul(m(w1,dd.ret,.1),axis=0)+w5.mul(m(w5,dd.ret,.1),axis=0),dd.ret,L.C_PERP,True),(w7.mul(m(w7,dd.pret,.1),axis=0),dd.pret,L.C_PERP,True)]}
    for k,legs in out.items():
        ev=L.evaluate(legs,data=dd); s=L.stats(ev.net.loc[L.OOS[0]:L.OOS[1]].values,nboot=2000); s2=L.stats(ev.net2.loc[L.OOS[0]:L.OOS[1]].values,nboot=500); i=L.stats(ev.net.loc[L.IS[0]:L.IS[1]].values,nboot=500)
        print(f"{tag:20s} {k}: OOS {s['mean_bp']:6.2f} t {s['t']:5.2f} p5 {s['p5_bp']:6.2f} | x2 {s2['mean_bp']:6.2f} | IS {i['mean_bp']:6.2f} t {i['t']:5.2f}")
