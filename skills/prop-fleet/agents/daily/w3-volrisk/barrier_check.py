# Does barrier-aware sizing (risk scaled to the cushion above the max-loss floor) lower the
# Sharpe needed for $20k per $100K slot, vs the best constant volatility? Simplified FTMO Swing
# 2-step: +10% then +5%, 10% static max loss, 5% daily loss, payout every 10 trading days of
# 80% of profit above start, fee $600 refunded at first payout. t(4) daily shocks.
import numpy as np, itertools
TD=250; FEE=600.
def sim(S, policy, n=3000, years=3, seed=0):
    rng=np.random.default_rng(seed); T=years*TD
    z=rng.standard_t(4,(n,T))/np.sqrt(2)          # unit-variance t4
    cash=np.zeros(n)
    for i in range(n):
        t=0
        while t<T:
            cash[i]-=FEE; ok=True
            for tgt in (0.10,0.05):
                eq=1.0
                while t<T:
                    s=policy('eval',eq,tgt)/np.sqrt(TD)
                    d=S*s/np.sqrt(TD)*np.sqrt(TD)/np.sqrt(TD)*0+ (S*policy('eval',eq,tgt)/TD) + s*z[i,t]; t+=1
                    if d<-0.05: ok=False;break
                    eq*=1+d
                    if eq<0.90: ok=False;break
                    if eq>=1+tgt: break
                if not ok or t>=T: break
            if not ok or t>=T: continue
            eq=1.0;k=0;first=True
            while t<T:
                vol=policy('fund',eq,None); d=S*vol/TD+vol/np.sqrt(TD)*z[i,t]; t+=1;k+=1
                if d<-0.05: break
                eq*=1+d
                if eq<0.90: break
                if k%10==0 and eq>1.0:
                    cash[i]+=0.8*(eq-1.0)*1e5+(FEE if first else 0); first=False; eq=1.0
    return cash.mean()/years
def const(v): return lambda ph,eq,tgt: v
def cppi(vmax,m):   # vol proportional to cushion above the 0.90 floor, capped
    return lambda ph,eq,tgt: min(vmax, m*max(eq-0.90,0.0))
for S in (0.75,1.0,1.5):
    best=max(((sim(S,const(v),1500),f"const {v:.0%}") for v in (0.12,0.15,0.20)),key=lambda x:x[0])
    bc=max(((sim(S,cppi(vm,m),1500),f"cppi vmax {vm:.0%} m {m}") for vm in (0.20,0.30) for m in (2.0,3.0)),key=lambda x:x[0])
    print(f"S={S}: best constant ${best[0]:,.0f}/yr ({best[1]})  |  best barrier-aware ${bc[0]:,.0f}/yr ({bc[1]})",flush=True)
