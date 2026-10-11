import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings, copy, json; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/claude-skills/skills/prop-fleet/agents/daily/w1-crypto")
import run as R
d=data()
dead=pd.DataFrame(False,index=d.close.index,columns=d.close.columns)
for c in d.close.columns:
    try: p=pd.read_parquet(f"{S}/data/perp1d_{c}.parquet")
    except FileNotFoundError: continue
    p=p[~p.index.duplicated()].reindex(d.close.index)
    dead[c]=(p.volume==0)
    last=p[p.volume>0].index.max()
    dead.loc[last+pd.Timedelta(days=1):,c]=True   # funding prints after the perp file ends are stale too
print("dead perp coin-days 2019+:", int(dead.loc['2019':].sum().sum()))
d2=copy.copy(d)
d2.pclose=d.pclose.mask(dead); d2.pret=d.pret.mask(dead|dead.shift(1,fill_value=False))
d2.fund=d.fund.mask(dead); d2.fund_n=d.fund_n.mask(dead)
d2.fdaily=d.fdaily.mask(dead, L.F_DEFAULT)   # holding a coin whose perp is gone: keep the pre-history default charge
base=json.load(open(f"{S}/out/results.json"))
res=R.run(d2)
for k,df in res.items():
    o=L.stats(df.net.loc[L.OOS[0]:L.OOS[1]].values,nboot=2000); i=L.stats(df.net.loc[L.IS[0]:L.IS[1]].values,nboot=2000)
    b=base[k]
    print(f"{k}: OOS {b['OOS']['mean_bp']:6.2f} (t {b['OOS']['t']:5.2f}) -> {o['mean_bp']:6.2f} (t {o['t']:5.2f}, p5 {o['p5_bp']:.2f}) | IS {b['IS']['mean_bp']:6.2f} (t {b['IS']['t']:5.2f}) -> {i['mean_bp']:6.2f} (t {i['t']:5.2f})")
