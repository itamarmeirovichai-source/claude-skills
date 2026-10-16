import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings, json; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
base=json.load(open(f"{S}/out/results.json"))
# intraday (hourly) worst equity within each day for D3-02, using held daily weights (static intraday)
w2=L.g_tsmom(d,longflat=True); W=w2.shift(1).fillna(0)
hr=d.h_ret.loc[o0:o1+pd.Timedelta(hours=23)].fillna(0)
Wh=W.reindex(hr.index.floor('D')).values
# cumulative intraday price relatives per coin from 00:00
cum=(1+hr).groupby(hr.index.floor('D')).cumprod()
intr=(Wh*(cum.values-1)).sum(1)
intr=pd.Series(intr,index=hr.index).groupby(hr.index.floor('D')).min()
def sim(x, dl, mdd, static):
    eq=1.0; peak=1.0
    for i,r in enumerate(x):
        if r<=-dl: return i
        eq*=1+r; peak=max(peak,eq)
        ref=1.0 if static else peak
        if eq<=ref*(1-mdd): return i
    return None
for k in ["D3-02","D3-11","D3-10"]:
    x=pd.read_csv(f"{S}/out/daily_{k}.csv.gz",index_col=0,parse_dates=True).net.loc[o0:o1]
    kscale=0.20/(x.mean()*365)
    print(f"\n{k}: OOS mean {x.mean()*365:.1%}/yr arithmetic, vol {x.std()*np.sqrt(365):.1%}; scale for 20%/yr = {kscale:.2f}x; IS-fixed 20%-vol scale = {base[k]['scale']:.2f}x")
    for nm,sc in (("20%/yr",kscale),("IS-scale",base[k]['scale'])):
        y=x*sc; eq=(1+y).cumprod(); dd=(eq/eq.cummax()-1)
        print(f"  [{nm} x{sc:.2f}] OOS CAGR {eq.iloc[-1]**(365/len(y))-1:.1%} maxDD {dd.min():.1%} worst day {y.min():.2%}; days < -3%: {(y<-.03).sum()}, < -4%: {(y<-.04).sum()}, < -5%: {(y<-.05).sum()}; min equity vs start {eq.min()-1:.1%}")
        # rolling 365-day account starts (every 7 days)
        for dl,mdd in ((0.05,0.10),(0.04,0.08),(0.03,0.06),(0.05,0.06)):
            out=[]
            for static in (True,False):
                starts=range(0,len(y)-365,7); br=0
                for s0 in starts:
                    if sim(y.values[s0:s0+365],dl,mdd,static) is not None: br+=1
                out.append(br/len(starts))
            print(f"    daily {dl:.0%} / maxDD {mdd:.0%}: P(breach within 1y) static {out[0]:.0%}, trailing {out[1]:.0%}")
    if k=="D3-02":
        sc=kscale; iw=(intr*sc).loc[o0:o1]
        print(f"  intraday (hourly marks) worst floating loss within a day at 20%/yr scale: {iw.min():.2%}; days with floating < -3%: {(iw<-.03).sum()}, < -5%: {(iw<-.05).sum()}")
# benchmark: BTC scaled to same vol as D3-02
btc=d.ret.BTC.loc[o0:o1]; x=pd.read_csv(f"{S}/out/daily_D3-02.csv.gz",index_col=0,parse_dates=True).net.loc[o0:o1]
b=btc*x.std()/btc.std(); eq=(1+b).cumprod()
print(f"\nBTC buy&hold scaled to D3-02 vol: mean {b.mean()*1e4:.2f} bp/d, SR {b.mean()/b.std()*np.sqrt(365):.2f}, maxDD {(eq/eq.cummax()-1).min():.1%}")
