import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
w1=L.g_tsmom(d); w2=L.g_tsmom(d,longflat=True)
g1=L.evaluate([(w1,d.ret,0.0,False)],data=d).gross
sd=g1.rolling(60,min_periods=60).std()*np.sqrt(365); m11=(0.20/sd).clip(upper=3).fillna(0)
w11=w1.mul(m11,axis=0)
for k,w in (("D3-02",w2),("D3-11",w11),("D3-01",w1)):
    ev=L.evaluate([(w,d.ret,L.C_PERP,True)],data=d)
    ref=pd.read_csv(f"{S}/out/daily_{k}.csv.gz",index_col=0,parse_dates=True)
    print(k,"reproduces csv:",np.allclose(ev.net.values,ref.net.values,atol=1e-6))
    W=w.shift(1).fillna(0).loc[o0:o1]; R=d.ret.loc[o0:o1].fillna(0)
    contrib=(W*R).sum()*1e4/len(W)   # bp/day gross contribution
    fund=(W*d.fdaily.loc[o0:o1]).sum()*1e4/len(W)
    c=(contrib-fund).sort_values()
    print(" gross-minus-funding contribution bp/day, top 8:", c.tail(8).round(2).to_dict())
    print(" bottom 5:", c.head(5).round(2).to_dict())
    tot=c.sum(); print(f" total {tot:.2f}; ex-top1 {tot-c.iloc[-1]:.2f}; ex-top3 {tot-c.iloc[-3:].sum():.2f}; BTC+ETH only {c[['BTC','ETH']].sum():.2f}")
    hind=["PEPE","WIF","SUI","TON","INJ","APT","ARB","OP"]
    print(f" contribution of hindsight-famous post-2022 listings {hind}: {c[hind].sum():.2f}")
    # exposure stats
    gexp=W.abs().sum(1); nexp=W.sum(1)
    print(f" gross exposure mean {gexp.mean():.3f} max {gexp.max():.3f}; net exposure mean {nexp.mean():.3f} max {nexp.max():.3f} min {nexp.min():.3f}")
    # weight held where no perp exists that day (untradeable as a perp) and where funding is defaulted / zero-filled
    noperp=(W.abs()*d.pclose.loc[o0:o1].isna()).sum(1)
    nof=(W.abs()*(d.fund_n.loc[o0:o1].isna())).sum(1)
    print(f" avg |w| held in coin-days with NO perp kline: {noperp.mean():.4f} ({noperp.mean()/gexp.mean():.1%} of gross); with no funding print that day: {nof.mean():.4f}")
    bad=(W.abs()*d.pclose.loc[o0:o1].isna()).sum()
    print("   by coin:", bad[bad>0].div(len(W)).round(4).sort_values(ascending=False).head(8).to_dict())
