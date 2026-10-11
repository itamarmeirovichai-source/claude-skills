import pandas as pd, numpy as np, sys
S=sys.argv[1]
C=("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR AAVE ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM APE GALA CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
for c in C:
    try: p=pd.read_parquet(f"{S}/data/perp1d_{c}.parquet")
    except: print(c,"no perp"); continue
    z=p[p.volume==0]
    f=pd.read_parquet(f"{S}/data/funding_{c}.parquet").iloc[:,0]
    msg=""
    if len(z): 
        msg=f"zero-vol perp days {len(z)} {z.index[0].date()}..{z.index[-1].date()} (last traded {p[p.volume>0].index[-1].date()})"
        aft=f.loc[z.index[0]:]
        msg+=f"; funding prints after: {len(aft)} unique {np.unique(aft.round(8))[:4]}"
    # stale funding without zero-vol (eg perp file ended)
    if f.index[-1]>p.index[-1]+pd.Timedelta(days=2):
        aft=f.loc[p.index[-1]+pd.Timedelta(days=1):]
        msg+=f" | funding continues past perp file end {p.index[-1].date()} -> {f.index[-1].date()}, n={len(aft)}, unique {np.unique(aft.round(8))[:4]}"
    if msg: print(c,msg)
