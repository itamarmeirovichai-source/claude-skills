import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
def rep(tag,ev):
    out=[]
    for nm,(a,b) in (("IS",L.IS),("OOS",L.OOS)):
        s=L.stats(ev.net.loc[a:b].values,nboot=2000); out.append(f"{nm} {s['mean_bp']:6.2f} t {s['t']:5.2f}")
    print(tag," | ".join(out))
# baseline
w7=L.g_carry(d); ws,wp=L.g_cashcarry(d)
rep("D3-07 base   ",L.evaluate([(w7,d.pret,L.C_PERP,True)],data=d))
rep("D3-08 base   ",L.evaluate([(ws,d.ret,L.C_SPOT,False),(wp,d.pret,L.C_PERP,True)],data=d))
# patch A: per-8h normalisation of funding signal
def g_carry8(data):
    Uh,_=L.holding_universe(data)
    fmean=data.fund.rolling(7,min_periods=7).sum()/21.0
    fmean=fmean.where(data.fund_n.rolling(7,min_periods=7).sum().notna())
    hist=data.fund_n.notna().cumsum()>=7
    el=Uh&data.pclose.notna()&hist&fmean.notna()
    return L.weekly(data,-fmean,el,data.pret)
def g_cc8(data):
    Uh,_=L.holding_universe(data)
    m=data.fund.rolling(3,min_periods=3).sum()/9.0
    m=m.where(data.fund_n.rolling(3,min_periods=3).sum().notna())
    act=Uh&data.pclose.notna()&data.close.notna()&(m>0.0001)
    n=act.sum(axis=1); w=act.astype(float).div(np.maximum(5,n),axis=0); return w,-w
w7b=g_carry8(d); wsb,wpb=g_cc8(d)
rep("D3-07 per-8h ",L.evaluate([(w7b,d.pret,L.C_PERP,True)],data=d))
rep("D3-08 per-8h ",L.evaluate([(wsb,d.ret,L.C_SPOT,False),(wpb,d.pret,L.C_PERP,True)],data=d))
# patch B: 00:00 print charged to the position held before the rebalance (trades execute after the 00:00 print)
import glob
f00={}
for c in d.close.columns:
    try: f=pd.read_parquet(f"{S}/data/funding_{c}.parquet").iloc[:,0]
    except FileNotFoundError: continue
    h0=f[f.index.floor('h').hour==0]
    f00[c]=h0.groupby(h0.index.floor('D')).sum().reindex(d.close.index).fillna(0)
f00=pd.DataFrame(f00).reindex(columns=d.close.columns).fillna(0)
fd_alt=d.fdaily - f00 + f00.shift(-1).fillna(0)
import copy
d2=copy.copy(d); d2.fdaily=fd_alt
rep("D3-07 00UTC->old pos",L.evaluate([(w7,d.pret,L.C_PERP,True)],data=d2))
rep("D3-08 00UTC->old pos",L.evaluate([(ws,d.ret,L.C_SPOT,False),(wp,d.pret,L.C_PERP,True)],data=d2))
w2=L.g_tsmom(d,longflat=True)
rep("D3-02 base   ",L.evaluate([(w2,d.ret,L.C_PERP,True)],data=d))
rep("D3-02 00UTC->old pos",L.evaluate([(w2,d.ret,L.C_PERP,True)],data=d2))
# patch C: TSMOM on perp returns instead of spot returns (it is traded as a perp)
P=d.pret.where(d.pret.notna(), d.ret)
rep("D3-02 perp returns",L.evaluate([(w2,P,L.C_PERP,True)],data=d))
w1=L.g_tsmom(d)
rep("D3-01 base   ",L.evaluate([(w1,d.ret,L.C_PERP,True)],data=d))
rep("D3-01 perp returns",L.evaluate([(w1,P,L.C_PERP,True)],data=d))
# D3-08 gross decomposition by year and coin
ev=L.evaluate([(ws,d.ret,L.C_SPOT,False),(wp,d.pret,L.C_PERP,True)],data=d)
x=ev.loc[o0:o1]; print("D3-08 OOS gross/cost/fund bp:", (x[['gross','cost','fund']].mean()*1e4).round(2).to_dict(), "days active:", int((ws.loc[o0:o1].sum(1)>0).sum()))
W=ws.shift(1).fillna(0).loc[o0:o1]
basis=(W*(d.ret-d.pret).loc[o0:o1].fillna(0)).sum()*1e4/len(W)
print(" basis P&L by coin bp/day:", basis[basis.abs()>0.01].round(3).sort_values().to_dict())
