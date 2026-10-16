"""Independent verifier re-implementation of D3 pre-registration (D3-00 common rules).
Written from prereg/D3.csv only. Usage: python3 -I verify_d3.py <data_dir>
"""
import sys, os
import numpy as np, pandas as pd

DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'data')
COINS = ("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR "
         "AAVE ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM "
         "APE GALA CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
C_PERP, C_SPOT = 0.0007, 0.00095
DEF_F = 0.0001
IS0, IS1 = '2019-01-01', '2022-12-31'
OS0, OS1 = '2023-01-01', '2026-09-30'
DAYS = pd.date_range('2018-07-01', '2026-09-30', freq='D')

def p(name):
    return os.path.join(DATA, name + '.parquet')

# ---------------- load: spot daily (segments split on >72h gaps) ----------------
close, qvol, seg_base, seg_first = {}, {}, {}, {}
hourly = {}
for c in COINS:
    if not os.path.exists(p('spot1h_' + c)):
        print('skip (absent):', c); continue
    h = pd.read_parquet(p('spot1h_' + c)).sort_index()
    h = h[~h.index.duplicated()]
    hourly[c] = h
    gap = h.index.to_series().diff() > pd.Timedelta('72h')
    segid = gap.cumsum().values
    for k in np.unique(segid):
        hs = h[segid == k]
        name = c if k == 0 else f'{c}#{k}'
        d = hs.groupby(hs.index.floor('D')).agg(close=('close', 'last'), qvol=('qvol', 'sum'))
        close[name] = d['close'].reindex(DAYS)
        qvol[name] = d['qvol'].reindex(DAYS)
        seg_base[name] = c
        seg_first[name] = d.index[0]
        if k > 0: print('segment split:', name, 'starts', d.index[0].date())
CL = pd.DataFrame(close); QV = pd.DataFrame(qvol)
NAMES = list(CL.columns)
R = CL / CL.shift(1) - 1          # NaN if either day missing (also across segments: other segment col is NaN)

# perp daily and funding (per base symbol; segments only get prints within their life)
PCL = {}; FUND_D = {}; FUND_FIRST = {}; FUND_PRINTS = {}
for n in NAMES:
    b = seg_base[n]
    first, last = seg_first[n], CL[n].last_valid_index()
    if os.path.exists(p('perp1d_' + b)):
        pc = pd.read_parquet(p('perp1d_' + b))['close']
        pc = pc[(pc.index >= first) & (pc.index <= last + pd.Timedelta('1D'))]
        PCL[n] = pc.reindex(DAYS)
    else:
        PCL[n] = pd.Series(np.nan, DAYS)
    if os.path.exists(p('funding_' + b)):
        f = pd.read_parquet(p('funding_' + b)).iloc[:, 0]
        f = f[(f.index >= first) & (f.index < last + pd.Timedelta('1D'))]
    else:
        f = pd.Series(dtype=float)
    FUND_PRINTS[n] = f
    FUND_D[n] = f.groupby(f.index.floor('D')).sum().reindex(DAYS).fillna(0.0)
    FUND_FIRST[n] = f.index.min().floor('D') if len(f) else pd.NaT
PCL = pd.DataFrame(PCL); RP = PCL / PCL.shift(1) - 1
FD = pd.DataFrame(FUND_D)
# funding used for a held perp: actual prints; before first print -> default 3*1bp/day
FDEF = FD.copy()
for n in NAMES:
    ff = FUND_FIRST[n]
    mask = DAYS < ff if pd.notna(ff) else np.ones(len(DAYS), bool)
    FDEF.loc[mask, n] = 3 * DEF_F

# ---------------- universe U_m ----------------
first_days = pd.date_range('2018-08-01', '2026-09-01', freq='MS')
U = pd.DataFrame(False, index=DAYS, columns=NAMES)
ULIST = {}
for m0 in first_days:
    prev = m0 - pd.Timedelta('1D')
    elig = [n for n in NAMES if seg_first[n] <= m0 - pd.Timedelta('180D') and pd.notna(CL.at[prev, n])]
    vol = QV.loc[m0 - pd.Timedelta('30D'):prev, elig].sum()
    top = list(vol.sort_values(ascending=False).index[:25])
    ULIST[m0] = top
    m1 = m0 + pd.offsets.MonthBegin(1)
    U.loc[m0:m1 - pd.Timedelta('1D'), top] = True

SIG = R.rolling(60, min_periods=60).std() * np.sqrt(365)

# ---------------- generic daily P&L engine ----------------
def run_perp(W, ret=R, fund=FDEF, cost=C_PERP):
    """W.loc[t] = weights held during day t (decided with data through t-1). Returns dict of net series."""
    W = W.reindex(index=DAYS, columns=NAMES).fillna(0.0)
    r = ret.reindex(columns=NAMES).fillna(0.0)
    gross = (W * r).sum(1)
    drift = W * (1 + r)
    drift = drift.div(1 + gross, axis=0).shift(1).fillna(0.0)
    turn = (W - drift).abs().sum(1)
    fpay = (W * fund.reindex(columns=NAMES).fillna(0.0)).sum(1)
    return dict(gross=gross, turn=turn, fund=fpay,
                net=gross - cost * turn - fpay, net2=gross - 2 * cost * turn - fpay)

def shift_next(Wsig):
    """weights computed at close of t -> held on t+1"""
    return Wsig.shift(1)

# ---------------- stats ----------------
def nw_t(x, L=10):
    x = np.asarray(x, float); n = len(x); e = x - x.mean()
    s = e @ e / n
    for l in range(1, L + 1):
        s += 2 * (1 - l / (L + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / np.sqrt(s / n)

def stats(res, a, b):
    x = res['net'].loc[a:b]; x2 = res['net2'].loc[a:b]
    m = x.mean(); sd = x.std(ddof=1)
    return dict(mean=1e4 * m, t=m / (sd / np.sqrt(len(x))), nw=nw_t(x), sh=m / sd * np.sqrt(365),
                c2=1e4 * x2.mean(), turn=res['turn'].loc[a:b].mean(), n=len(x))

RESULTS = {}
def report(name, res, extra=''):
    o = stats(res, OS0, OS1); i = stats(res, IS0, IS1)
    RESULTS[name] = (o, i)
    print(f"{name}: OOS mean {o['mean']:.2f} bp t {o['t']:.2f} NW {o['nw']:.2f} Sh {o['sh']:.2f} "
          f"c2 {o['c2']:.2f} turn {o['turn']:.3f} | IS mean {i['mean']:.2f} t {i['t']:.2f} NW {i['nw']:.2f} {extra}")

# ---------------- D3-01 / 02 / 11 / 03 ----------------
def tsmom_sig(cols=None):
    s = sum(np.sign(CL / CL.shift(L) - 1) for L in (20, 60, 120)) / 3
    valid = (CL / CL.shift(120)).notna() & SIG.notna()
    return s.where(valid), valid

S, VALID = tsmom_sig()
SIZE = np.minimum(0.5 / SIG, 1.5)
Unext = U.shift(-1).fillna(False).astype(bool)   # universe of day t+1, known at t (fixed at month start)
mem = VALID & Unext
N = mem.sum(1).replace(0, np.nan)
W01 = (S * SIZE).where(mem).div(N, axis=0)
res01 = run_perp(shift_next(W01)); report('D3-01', res01)
W02 = (S.clip(lower=0) * SIZE).where(mem).div(N, axis=0)
res02 = run_perp(shift_next(W02)); report('D3-02', res02)

# D3-11 vol-managed D3-01
sg = res01['gross'].rolling(60, min_periods=60).std() * np.sqrt(365)
mult = np.minimum(0.20 / sg, 3.0)   # known at close of t, applies to weights for t+1
W11 = W01.mul(mult, axis=0)
res11 = run_perp(shift_next(W11)); report('D3-11', res11)

# D3-03 BTC/ETH only
memb = VALID[['BTC', 'ETH']]
W03 = (S * SIZE)[['BTC', 'ETH']].where(memb) / 2
res03 = run_perp(shift_next(W03)); report('D3-03', res03)

# ---------------- weekly helpers ----------------
def weekly(target_fn, ret, fund):
    """target_fn(sunday) -> Series of target weights for Monday..Sunday; drift in between."""
    W = pd.DataFrame(0.0, index=DAYS, columns=NAMES)
    r = ret.reindex(columns=NAMES).fillna(0.0)
    cur = pd.Series(0.0, index=NAMES)
    for i, d in enumerate(DAYS):
        if d.dayofweek == 0 and i > 0:
            tgt = target_fn(DAYS[i - 1], d)
            if tgt is not None:
                cur = pd.Series(0.0, index=NAMES); cur[tgt.index] = tgt.values
        W.iloc[i] = cur.values
        g = (cur * r.iloc[i]).sum()
        cur = cur * (1 + r.iloc[i]) / (1 + g)
    return W

def xs_target(L):
    mom = CL / CL.shift(L) - 1
    def f(sun, mon):
        u = U.loc[mon]; m = mom.loc[sun][u[u].index].dropna()
        if len(m) < 10: return None
        m = m.sort_values()
        return pd.concat([pd.Series(-0.1, m.index[:5]), pd.Series(0.1, m.index[-5:])])
    return f

W05 = weekly(xs_target(28), R, FDEF); res05 = run_perp(W05); report('D3-05', res05)
W06 = weekly(xs_target(7), R, FDEF); res06 = run_perp(W06); report('D3-06', res06)

# D3-07 funding carry on perp klines
def fc_target(sun, mon):
    u = U.loc[mon]; cand = []
    for n in u[u].index:
        ff = FUND_FIRST[n]
        if pd.isna(ff) or pd.isna(PCL.at[sun, n]) or ff > sun - pd.Timedelta('6D'): continue
        pr = FUND_PRINTS[n]; pr = pr[(pr.index >= sun - pd.Timedelta('6D')) & (pr.index < sun + pd.Timedelta('1D'))]
        if len(pr): cand.append((n, pr.mean()))
    if len(cand) < 10: return None
    s = pd.Series(dict(cand)).sort_values()
    return pd.concat([pd.Series(0.1, s.index[:5]), pd.Series(-0.1, s.index[-5:])])
W07 = weekly(fc_target, RP, FD); res07 = run_perp(W07, ret=RP, fund=FD); report('D3-07', res07)

# ---------------- D3-08 cash and carry ----------------
mean9 = {}
for n in NAMES:
    pr = FUND_PRINTS[n]
    if len(pr) == 0: mean9[n] = pd.Series(np.nan, DAYS); continue
    rm = pr.rolling(9, min_periods=9).mean()
    mean9[n] = rm.groupby(rm.index.floor('D')).last().reindex(DAYS)
M9 = pd.DataFrame(mean9)
act = (M9 > DEF_F) & Unext & PCL.notna() & CL.notna()
na = act.sum(1)
w8 = act.astype(float).div(np.maximum(5, na), axis=0)
W8 = w8.shift(1).fillna(0.0)
rs = R.fillna(0.0); rp = RP.fillna(0.0)
g8 = (W8 * (rs - rp)).sum(1) + (W8 * FD).sum(1)   # short perp receives funding
# drift per leg: spot leg drifts with spot, perp leg with perp (in capital terms, ignore tiny denominator)
ds = (W8 * (1 + rs)).shift(1).fillna(0.0); dp = (W8 * (1 + rp)).shift(1).fillna(0.0)
ts = (W8 - ds).abs().sum(1); tp = (W8 - dp).abs().sum(1)
c8 = C_SPOT * ts + C_PERP * tp
res08 = dict(gross=g8, turn=ts + tp, fund=-(W8 * FD).sum(1), net=g8 - c8, net2=g8 - 2 * c8)
report('D3-08', res08, f"avg|A| OOS {na.loc[OS0:OS1].mean():.2f}")

# ---------------- D3-09 hour of day ----------------
def hod(coin, hours=None):
    h = hourly[coin]['close']
    full = pd.date_range(h.index[0], h.index[-1], freq='h')
    h = h.reindex(full)
    lr = np.log(h / h.shift(1))      # return of bar opened at t (close_t / close_{t-1})
    if hours is None:
        isr = lr.loc[IS0:'2022-12-31 23:00']
        mh = isr.groupby(isr.index.hour).mean().sort_values()
        hours = (list(mh.index[-2:][::-1]), list(mh.index[:2]))
    longs, shorts = hours
    pos = pd.Series(0.0, index=full)
    pos[np.isin(full.hour, longs)] = 1.0; pos[np.isin(full.hour, shorts)] = -1.0
    sr = (h / h.shift(1) - 1).fillna(0.0)
    turn = (pos - pos.shift(1).fillna(0)).abs()
    day = full.floor('D')
    gross = (pos * sr).groupby(day).sum(); tn = turn.groupby(day).sum()
    avgw = pos.groupby(day).mean()
    fd = FDEF[coin].reindex(gross.index).fillna(0)
    fp = avgw * fd
    res = dict(gross=gross, turn=tn, fund=fp, net=gross - C_PERP * tn - fp, net2=gross - 2 * C_PERP * tn - fp)
    return res, hours
res09, H = hod('BTC'); report('D3-09', res09, f"hours long {H[0]} short {H[1]}")
res09e, _ = hod('ETH', H); report('D3-09 ETH', res09e)

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify_results.csv')
    rows = []
    for k, (o, i) in RESULTS.items():
        rows.append(dict(variant=k, oos_mean=o['mean'], oos_t=o['t'], oos_nw=o['nw'], oos_sharpe=o['sh'],
                         oos_cost2=o['c2'], oos_turn=o['turn'], is_mean=i['mean'], is_t=i['t']))
    pd.DataFrame(rows).round(3).to_csv(out, index=False)
    print('passes gate (t=min(iid,NW)>=3.5504):', [k for k, (o, i) in RESULTS.items() if min(o['t'], o['nw']) >= 3.5504 and o['mean'] > 0])
