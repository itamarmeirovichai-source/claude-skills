import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data()
o0,o1=L.OOS
res={k:pd.read_csv(f"{S}/out/daily_{k}.csv.gz",index_col=0,parse_dates=True) for k in ["D3-01","D3-02","D3-10","D3-11"]}
# benchmarks
U,_=L.universe(d)
btc=d.ret.BTC
ew=d.ret.where(U).mean(axis=1)
def st(x): 
    s=L.stats(np.asarray(x),nboot=2000); return f"mean {s['mean_bp']:6.2f} t {s['t_iid']:5.2f} tNW {s['t_nw']:5.2f} SR {s['sharpe']:5.2f} MDD {s['maxdd']:6.3f} worst {s['worst']:7.4f}"
print("BTC buy&hold OOS:", st(btc.loc[o0:o1].fillna(0)))
print("EW universe OOS:", st(ew.loc[o0:o1].fillna(0)))
for k,df in res.items():
    x=df.loc[o0:o1]
    print(f"\n=== {k} OOS net:", st(x.net), " x2:", st(x.net2))
    for y,g in x.groupby(x.index.year):
        s=L.stats(g.net.values,nboot=500); s2=L.stats(g.net2.values,nboot=500)
        print(f"  {y}: n {s['n']} net {s['mean_bp']:6.2f} t {s['t_iid']:5.2f} SR {s['sharpe']:5.2f} | x2 {s2['mean_bp']:6.2f} t {s2['t_iid']:5.2f} | MDD {s['maxdd']:.3f}")
    n=x.net.sort_values(ascending=False)
    for K in (5,10,20,50):
        r=x.net.drop(n.index[:K]); print(f"  drop best {K} days: mean {r.mean()*1e4:6.2f} t {r.mean()/r.std()*np.sqrt(len(r)):5.2f}")
    # share of total from top 1% days
    print(f"  top 1% days ({int(len(n)*.01)}) sum = {n.iloc[:int(len(n)*.01)].sum()/n.sum():.2f} of total net")
    # beta regression
    Y=x.net.values
    for name,Xs in (("BTC",[btc]),("EW",[ew]),("BTC+EW",[btc,ew])):
        X=np.column_stack([np.ones(len(Y))]+[s.loc[o0:o1].fillna(0).values for s in Xs])
        b,res_,_,_=np.linalg.lstsq(X,Y,rcond=None); e=Y-X@b
        # NW se lag10
        n_=len(Y); XtXi=np.linalg.inv(X.T@X); S0=(X*e[:,None]).T@(X*e[:,None])
        for Lg in range(1,11):
            G=(X[Lg:]*e[Lg:,None]).T@(X[:-Lg]*e[:-Lg,None]); S0+= (1-Lg/11)*(G+G.T)
        V=XtXi@S0@XtXi; se=np.sqrt(np.diag(V))
        r2=1-e.var()/Y.var()
        print(f"  reg on {name}: alpha {b[0]*1e4:6.2f} bp/d tNW {b[0]/se[0]:5.2f}; betas {np.round(b[1:],3)} R2 {r2:.2f}")
    # up/down capture
    up=btc.loc[o0:o1]>0
    print(f"  mean net on BTC-up days {x.net[up.values].mean()*1e4:.1f}, BTC-down days {x.net[~up.values].mean()*1e4:.1f}")
