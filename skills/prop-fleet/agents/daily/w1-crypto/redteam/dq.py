import sys, pandas as pd, numpy as np
D=sys.argv[1]
from glob import glob
C=("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR AAVE ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM APE GALA CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
for c in C:
    try: h=pd.read_parquet(f"{D}/spot1h_{c}.parquet")
    except Exception as e: print(c,"NO SPOT"); continue
    idx=h.index
    dup=idx.duplicated().sum(); mono=idx.is_monotonic_increasing
    offgrid=(idx!=idx.floor('h')).sum()
    gaps=idx.to_series().diff(); big=gaps[gaps>pd.Timedelta(hours=72)]
    mid=gaps[(gaps>pd.Timedelta(hours=3))&(gaps<=pd.Timedelta(hours=72))]
    zero=(h.close<=0).sum()
    # extreme hourly moves
    r=h.close.pct_change(); ext=r[(r.abs()>0.5)]
    print(c, len(h), idx[0], idx[-1], "dup",dup,"mono",mono,"offgrid",offgrid,"gaps>72h",[(str(i),str(g)) for i,g in big.items()],"gaps3-72h",len(mid),"ext",[(str(i)[:13],round(v,2)) for i,v in ext.items()][:6])
    # missing months
    m=pd.period_range(idx[0].to_period('M'), idx[-1].to_period('M'),freq='M'); have=set(idx.to_period('M'))
    miss=[str(x) for x in m if x not in have]
    if miss: print("   MISSING MONTHS", miss)
