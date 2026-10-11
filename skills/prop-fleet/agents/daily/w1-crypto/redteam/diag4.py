import sys; sys.path.insert(0, sys.argv[1])
from common import *
import warnings; warnings.filterwarnings("ignore")
d=data(); o0,o1=L.OOS
fn=d.fund_n.loc[o0:o1]
print("coin-days by #prints OOS:", fn.stack().value_counts().sort_index().to_dict())
print("coins with any day >3 prints OOS:", sorted([c for c in fn if (fn[c]>3).any()]))
print("IS:", d.fund_n.loc[L.IS[0]:L.IS[1]].stack().value_counts().sort_index().to_dict())
# weight in D3-07 / D3-08 on >3-print coin-days
w7=L.g_carry(d); ws,wp=L.g_cashcarry(d)
for k,w in (("D3-07",w7),("D3-08 perp",wp)):
    W=w.shift(1).fillna(0).loc[o0:o1]
    print(k, "share of gross |w| on coin-days with >3 prints:", float((W.abs()*(fn>3)).sum().sum()/W.abs().sum().sum()))
# max abs funding print
f=d.fund.loc[o0:o1]/d.fund_n.loc[o0:o1]
print("max per-print mean day:", f.max().sort_values().tail(5).to_dict())
