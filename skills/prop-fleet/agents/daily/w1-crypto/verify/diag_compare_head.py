import sys, runpy, numpy as np, pandas as pd
sys.argv=['x','../data']
V = runpy.run_path('verify_d3.py')
sys.path.insert(0,'/home/user/claude-skills/skills/prop-fleet/agents/daily/w1-crypto')
import d3lib as H
data=H.load('../data')
Uh,_=H.holding_universe(data)
U=V['U'].shift(-1).fillna(False)
def merge(df):  # collapse segments into base name
    out={}
    for c in df.columns:
        b=c.split('#')[0]; out[b]=out.get(b,0)+df[c].astype(float)
    return pd.DataFrame(out)
Um=merge(U)>0
d=(Um!=Uh[Um.columns]).iloc[:-1]; s=d.sum(); print('universe diff', s[s>0].to_dict())
for c in s[s>0].index: print(c, sorted(set(d.index[d[c]].strftime('%Y-%m'))))
w5=H.g_xsmom(data,28).shift(1).fillna(0); W5=merge(V['W05'])
dd=(w5[W5.columns]!=0)!=(W5!=0); x=dd.any(axis=1); print('D3-05 diff days', x.sum(), sorted(set(x[x].index.strftime('%Y-%m'))))
