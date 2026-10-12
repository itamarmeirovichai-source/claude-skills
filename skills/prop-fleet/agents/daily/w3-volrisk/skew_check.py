# Does negative skew (steady small gains, rare big loss) beat symmetric returns under
# FTMO-like rules at the SAME mean and vol? Simplified FTMO Swing 2-step 100K.
import numpy as np
rng=np.random.default_rng(0)
FEE=600.; TD=250; JUMP=-0.06
def gen(kind,mu,sig,n,T):
    if kind=='sym':
        return mu+sig*rng.standard_normal((n,T))
    # jump: with prob p a loss of size J, else gain g + small noise; match mean mu, sd sig
    p=1/250; J=JUMP   # one -6% day a year on average
    # var = p*(1-p)*(J-g)^2 + s2 ; mean = p*J+(1-p)*g = mu
    g=(mu-p*J)/(1-p); jv=p*(1-p)*(J-g)**2; s=np.sqrt(max(sig**2-jv,1e-12))
    x=g+s*rng.standard_normal((n,T)); jumps=rng.random((n,T))<p
    x[jumps]=J+s*rng.standard_normal(jumps.sum()); return x
def run(kind,S,vol,n=20000,years=3):
    mu=S*vol/TD; sig=vol/np.sqrt(TD); T=years*TD
    r=gen(kind,mu,sig,n,T)
    cash=np.zeros(n)
    for i in range(n):
        t=0; 
        while t<T:
            # evaluation: phase1 +10%, phase2 +5%, max loss 10%, daily 5%
            cash[i]-=FEE; ok=True
            for tgt in (0.10,0.05):
                eq=1.0
                while t<T:
                    d=r[i,t]; t+=1
                    if d<-0.05: ok=False;break
                    eq*=1+d
                    if eq<0.90: ok=False;break
                    if eq>=1+tgt: break
                if not ok or t>=T: break
            if not ok or t>=T: continue
            # funded: payout every 10 trading days of 80% of profit, refund fee at first payout
            eq=1.0; k=0; first=True
            while t<T:
                d=r[i,t]; t+=1; k+=1
                if d<-0.05: break
                eq*=1+d
                if eq<0.90: break
                if k%10==0 and eq>1.0:
                    cash[i]+=0.8*(eq-1.0)*100_000+(FEE if first else 0); first=False; eq=1.0
    return cash.mean()/years, np.percentile(cash/years,10)
for S in ():
    for vol in (0.12,0.20):
        a=run('sym',S,vol,4000); b=run('skew',S,vol,4000)
        print(f"S={S} vol={vol:.0%}: symmetric ${a[0]:,.0f}/yr (p10 {a[1]:,.0f})  neg-skew ${b[0]:,.0f}/yr (p10 {b[1]:,.0f})",flush=True)
print("--- positive skew (one +6% day a year)")
JUMP=0.06
for S in (0.0,0.5,1.0):
    for vol in (0.12,0.20):
        b=run('skew',S,vol,4000)
        print(f"S={S} vol={vol:.0%}: pos-skew ${b[0]:,.0f}/yr (p10 {b[1]:,.0f})",flush=True)
