"""Independent re-implementation of G2 (prereg/G2_rules.md) from the written rules only.
Usage: python3 -I verify.py <yahoo_dir>   (writes verify_run.txt next to this file)"""
import sys, json, os
import numpy as np, pandas as pd

YDIR = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify_run.txt')
# symbol: (cost bp per side, swap long %/yr, swap short %/yr)
MK = {'GSPC': (1.0, -8.28, .42), 'NDX': (1.0, -8.29, .42), 'DJI': (1.0, -8.25, .42),
      'GDAXI': (1.0, -6.50, -.07), 'FTSE': (1.0, -8.22, .38), 'N225': (1.5, -4.88, -1.63),
      'FCHI': (2.0, -6.50, -.07), 'AXJO': (2.5, -7.74, -.84), 'STOXX50E': (3.0, -6.50, -.07),
      'HSI': (4.0, -6.70, .07)}
VARS = {'G2-01': ('rsi', False, False), 'G2-02': ('d3', False, False), 'G2-03': ('rsi', True, False),
        'G2-04': ('d3', True, False), 'G2-05': ('rsi', False, True), 'G2-06': ('d3', False, True),
        'G2-07': ('rsi', True, True)}
SPLIT = pd.Timestamp('2013-01-01'); FIRST = pd.Timestamp('1990-01-02')
BAR = 3.5914

def load(sym):
    r = json.load(open(os.path.join(YDIR, sym + '.json')))['chart']['result'][0]
    off = r['meta']['gmtoffset']; q = r['indicators']['quote'][0]
    ts = pd.to_datetime(np.array(r['timestamp'], dtype='int64') + off, unit='s').normalize()
    df = pd.DataFrame({'o': pd.to_numeric(pd.Series(q['open']), errors='coerce').values,
                       'c': pd.to_numeric(pd.Series(q['close']), errors='coerce').values}, index=ts)
    df = df[~df.index.duplicated(keep='last')].sort_index()
    df = df[(df.index >= '1989-01-01') & df.c.notna() & (df.c > 0)]
    return df

def rsi2(c):
    d = np.diff(c, prepend=np.nan); g = np.where(d > 0, d, 0.); l = np.where(d < 0, -d, 0.)
    out = np.full(len(c), np.nan)
    if len(c) < 3: return out
    ag, al = g[1:3].mean(), l[1:3].mean()
    for i in range(2, len(c)):
        if i > 2: ag = ag / 2 + g[i] / 2; al = al / 2 + l[i] / 2
        out[i] = 100. if al == 0 else 100 - 100 / (1 + ag / al)
    return out

def decisions(c, dates, rule, ls, filt):
    """Signed notional decided at each close (held after the close of t in the close version)."""
    n = len(c); r = np.full(n, np.nan); r[1:] = c[1:] / c[:-1] - 1
    sig = pd.Series(r).rolling(60).std().values  # ddof=1, last 60 returns up to t
    w = (0.10 / np.sqrt(252)) / sig / 10
    s5 = pd.Series(c).rolling(5).mean().values; s200 = pd.Series(c).rolling(200).mean().values
    rs = rsi2(c)
    dn = np.zeros(n, bool); up = np.zeros(n, bool); dn[1:] = c[1:] < c[:-1]; up[1:] = c[1:] > c[:-1]
    d3 = np.zeros(n, bool); u3 = np.zeros(n, bool)
    d3[3:] = dn[3:] & dn[2:-1] & dn[1:-2]; u3[3:] = up[3:] & up[2:-1] & up[1:-2]
    if rule == 'rsi': L, S = rs < 10, rs > 90
    else: L, S = d3, u3
    D = np.zeros(n); entry = np.zeros(n, bool)
    pos = 0.; side = 0; age = 0
    ok = (np.arange(n) >= 199) & (dates >= FIRST)
    for t in range(n):
        exited = False
        if side != 0:
            age += 1
            if (side > 0 and c[t] > s5[t]) or (side < 0 and c[t] < s5[t]) or age >= 5:
                pos = 0.; side = 0; exited = True
        if side == 0 and not exited and ok[t] and np.isfinite(w[t]):
            if L[t] and (not filt or c[t] > s200[t]): side = 1
            elif ls and S[t] and (not filt or c[t] < s200[t]): side = -1
            if side: pos = side * w[t]; age = 0; entry[t] = True
        D[t] = pos
    return D, entry, w, r

def market_streams(df, sym, D, cm=1.0, swm=1.0, lag=0):
    """Per-market daily net-return contributions indexed by the market's dates."""
    c = df.c.values; o = df.o.values; dates = df.index; n = len(c)
    bp, sl, ss = MK[sym]; cost = bp * 1e-4 * cm
    nights = np.zeros(n); nights[:-1] = (dates[1:] - dates[:-1]).days
    def swap(P):  # charged on positions held through close s, booked on day s+1
        rate = np.where(P > 0, sl, np.where(P < 0, ss, 0.)) / 100 / 365 * swm
        sw = np.abs(P) * rate * nights; out = np.zeros(n); out[1:] = sw[:-1]; return out
    gross = np.zeros(n); cst = np.zeros(n)
    Dp = np.concatenate([[0.], D[:-1]])
    if lag == 0:
        gross[1:] = D[:-1] * (c[1:] / c[:-1] - 1)
        cst = cost * np.abs(D - Dp); held = D
    else:
        valid = np.zeros(n, bool)
        valid[1:] = np.isfinite(o[1:]) & (o[1:] > 0) & (o[1:] != c[:-1]) & (o[1:] != c[1:])
        Dpp = np.concatenate([[0., 0.], D[:-2]])  # position before the fill on day s
        a = Dpp; b = Dp  # before / after fill on day s
        g = np.zeros(n)
        cc = np.zeros(n); cc[1:] = c[1:] / c[:-1] - 1
        on = np.zeros(n); idy = np.zeros(n)
        on[1:] = np.where(valid[1:], o[1:] / c[:-1] - 1, 0.); idy[1:] = np.where(valid[1:], c[1:] / o[1:] - 1, 0.)
        gross = np.where(valid, a * on + b * idy, a * cc)
        cst = cost * np.abs(b - a); held = b
    sw = swap(held)
    return gross, cst, sw, held

def nw_se(x, L=10):
    x = x - x.mean(); n = len(x); s = x @ x / n
    for k in range(1, L + 1): s += 2 * (1 - k / (L + 1)) * (x[k:] @ x[:-k]) / n
    return np.sqrt(s / n)

def tstat(x):
    ti = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))); tn = x.mean() / nw_se(x)
    return min(ti, tn), ti, tn

def boot_p5(x, B=10000, bl=10, seed=0):
    rng = np.random.default_rng(seed); n = len(x); k = int(np.ceil(n / bl)); cs = np.concatenate([[0.], np.cumsum(x)])
    means = np.empty(B)
    for i in range(0, B, 1000):
        st = rng.integers(0, n - bl + 1, size=(min(1000, B - i), k))
        sums = cs[st + bl] - cs[st]  # full blocks; last block truncated below
        tot = sums[:, :-1].sum(1)
        rem = n - (k - 1) * bl; tot += cs[st[:, -1] + rem] - cs[st[:, -1]]
        means[i:i + len(st)] = tot / n
    return np.percentile(means, 5)

def ols_nw(y, x, L=10):
    X = np.column_stack([np.ones(len(x)), x]); b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    n = len(y); XtXi = np.linalg.inv(X.T @ X); u = X * e[:, None]; S = u.T @ u
    for k in range(1, L + 1):
        G = u[k:].T @ u[:-k]; S += (1 - k / (L + 1)) * (G + G.T)
    V = XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V))

def sharpe(x): return x.mean() / x.std(ddof=1) * np.sqrt(252) if x.std() > 0 else np.nan

def mdd(x):
    eq = np.cumprod(1 + x); return (eq / np.maximum.accumulate(eq) - 1).min()

# ---------------- load ----------------
data = {s: load(s) for s in MK}
allidx = sorted(set().union(*[d.index for d in data.values()]))
U = pd.DatetimeIndex(allidx)
# basket (gross, rebalanced daily, weights from sigma_t, earns t->t+1, booked on t+1)
bask = pd.Series(0., index=U); bnot = pd.Series(0., index=U)
pre = {}
for s, df in data.items():
    c = df.c.values; r = np.full(len(c), np.nan); r[1:] = c[1:] / c[:-1] - 1
    w = (0.10 / np.sqrt(252)) / pd.Series(r).rolling(60).std().values / 10
    w = np.where(np.isfinite(w) & (df.index >= FIRST), w, 0.)
    br = np.zeros(len(c)); br[1:] = w[:-1] * r[1:]
    bask = bask.add(pd.Series(br, index=df.index), fill_value=0)
    bnot = bnot.add(pd.Series(w, index=df.index), fill_value=0)

lines = []; P = lines.append
res = {}
for v, (rule, ls, filt) in VARS.items():
    decs = {s: decisions(df.c.values, df.index, rule, ls, filt) for s, df in data.items()}
    first_sig = min(df.index[199] for df in data.values()); start = max(FIRST, first_sig)
    for lag in (0, 1):
        for cm in (1.0, 2.0):
            book = pd.Series(0., index=U); hnot = pd.Series(0., index=U); ent = pd.Series(0., index=U)
            for s, df in data.items():
                D, entry, w, r = decs[s]
                g, cst, sw, held = market_streams(df, s, D, cm, cm, lag)
                book = book.add(pd.Series(g - cst + sw, index=df.index), fill_value=0)
                hnot = hnot.add(pd.Series(held, index=df.index), fill_value=0)
                ent = ent.add(pd.Series(entry.astype(float), index=df.index), fill_value=0)
            res[(v, lag, cm)] = (book, hnot, ent, start)

def stats(book, hnot, ent, lo, hi):
    m = (book.index >= lo) & (book.index < hi)
    x = book[m].values; b = bask[m].values
    expo = (hnot[m] / bnot[m].replace(0, np.nan)).dropna().mean()
    t, ti, tn = tstat(x); bt, at = ols_nw(x, b)
    yrs = (book.index[m][-1] - book.index[m][0]).days / 365.25
    return dict(S=sharpe(x), t=t, ti=ti, tn=tn, p5=boot_p5(x), at=at[0], beta=bt[1],
                mbS=np.sign(expo) * sharpe(b), resS=sharpe(x - bt[1] * b), mdd=mdd(x), worst=x.min(),
                tpy=ent[m].sum() / yrs, expo=expo, n=len(x), mean=x.mean(), vol=x.std(ddof=1) * np.sqrt(252))

END = pd.Timestamp('2100-01-01')
P('G2 independent verifier (verify.py) -- rules: prereg/G2_rules.md only')
P('Data: %s ; last date %s' % (YDIR, U[-1].date()))
P('OOS = 2013-01-01..end; IS = first signal date..2012-12-31. lag0 = close fill, lag1 = next-open fill.')
P('t = min(iid, NW10); p5 = moving-block bootstrap (10, 10000, seed 0) 5th pct of daily mean (bp/day);')
P('alpha t: OLS on equal-risk B&H basket, NW10; MDD/worst on the raw (unscaled) book and at the 15%%-vol scale k fixed on IS close book.')
P('')
out = {}
hdr = '%-6s %-4s %-3s %7s %6s %6s %6s %8s %7s %6s %6s %7s %8s %8s %7s %6s %6s' % (
    'var', 'fill', 'cx', 'S', 't', 't_iid', 't_nw', 'p5bp', 'alpha_t', 'beta', 'mbS', 'resS', 'MDDraw', 'MDD15', 'worst15', 'tr/yr', 'expo')
P(hdr)
for v in VARS:
    kIS = None
    for lag in (0, 1):
        for cm in (1.0, 2.0):
            book, hnot, ent, start = res[(v, lag, cm)]
            st_o = stats(book, hnot, ent, SPLIT, END); st_i = stats(book, hnot, ent, start, SPLIT)
            out[(v, lag, cm)] = (st_i, st_o)
    kIS = 0.15 / out[(v, 0, 1.0)][0]['vol']
    for lag in (0, 1):
        for cm in (1.0, 2.0):
            o = out[(v, lag, cm)][1]; book = res[(v, lag, cm)][0]; x = book[book.index >= SPLIT].values * kIS
            P('%-6s %-4s %-3s %7.3f %6.2f %6.2f %6.2f %8.3f %7.2f %6.3f %6.2f %7.3f %8.2f%% %7.2f%% %6.2f%% %6.1f %6.3f' % (
                v, ['cls', 'opn'][lag], '%dx' % cm, o['S'], o['t'], o['ti'], o['tn'], o['p5'] * 1e4, o['at'], o['beta'],
                o['mbS'], o['resS'], o['mdd'] * 100, mdd(x) * 100, x.min() * 100, o['tpy'], o['expo']))
P('')
P('In-sample net Sharpe (1x cost):')
best = None
for v in VARS:
    si0, si1 = out[(v, 0, 1.0)][0]['S'], out[(v, 1, 1.0)][0]['S']
    t0, t1 = out[(v, 0, 1.0)][1]['t'], out[(v, 1, 1.0)][1]['t']
    worse_oos = 0 if t0 < t1 else 1
    is_worse_by_oos = [si0, si1][worse_oos]
    P('  %s  IS S close %.3f  open %.3f | worse-by-OOS-t fill = %s -> IS S %.3f | min IS S %.3f' % (
        v, si0, si1, ['close', 'open'][worse_oos], is_worse_by_oos, min(si0, si1)))
    if best is None or min(si0, si1) > best[1]: best = (v, min(si0, si1))
P('Headline (highest IS net Sharpe of the worse fill, worse = lower IS Sharpe): %s (IS S %.3f)' % best)
P('')
P('Gate (decisive = fill with lower OOS net t at 1x cost; bar %.4f; look-ahead see below):' % BAR)
for v in VARS:
    o0, o1 = out[(v, 0, 1.0)][1], out[(v, 1, 1.0)][1]
    o, f = (o0, 'close') if o0['t'] <= o1['t'] else (o1, 'open')
    ok = o['t'] >= BAR and o['p5'] > 0 and o['at'] >= BAR
    P('  %s  fill=%-5s t=%.2f S=%.3f p5=%.3fbp alpha_t=%.2f -> %s' % (v, f, o['t'], o['S'], o['p5'] * 1e4, o['at'], 'PASS' if ok else 'FAIL'))

# ---------------- look-ahead: truncation & perturbation on decision series ----------------
rng = np.random.default_rng(1)
lo, hi = U.searchsorted(pd.Timestamp('1992-01-01')), len(U) - 5
cuts = U[np.sort(rng.integers(lo, hi, 20))]
P('')
P('Look-ahead (decision series, 20 cut dates seed 1, every market; fills only use the fill-day bar):')
for v, (rule, ls, filt) in VARS.items():
    passT = passP = 0
    for d in cuts:
        okT = okP = True
        for s, df in data.items():
            full = decisions(df.c.values, df.index, rule, ls, filt)[0]
            k = df.index.searchsorted(d, side='right')
            tr = decisions(df.c.values[:k], df.index[:k], rule, ls, filt)[0]
            okT &= np.array_equal(full[:k], tr)
            cp = df.c.values.copy(); cp[k:] = cp[k - 1] * np.exp(np.cumsum(rng.normal(0, .02, len(cp) - k))) if k < len(cp) else cp[k:]
            pr = decisions(cp, df.index, rule, ls, filt)[0]
            okP &= np.array_equal(full[:k], pr[:k])
        passT += okT; passP += okP
    P('  %s truncation %d/20 perturbation %d/20' % (v, passT, passP))

P('')
P('''Ambiguities and choices:
 1. Notional "fixed at entry": held as a constant fraction of equity w (daily P&L = w * market return), not fixed units.
 2. sigma = sample std (ddof=1) of the last 60 close-to-close returns incl. day t; warm-up: decisions from index 199 (200 closes) and not before 1990-01-02.
 3. RSI(2): seed avg gain/loss = mean of first two changes, then Wilder alpha 1/2; RSI=100 when avg loss is 0.
 4. Exit: day counter starts at the entry close; exit at the close of the first later day with C>SMA5 (short: C<SMA5) or at the 5th trading day after entry. No entry on an exit close. If both long and short rules fire (impossible here) long wins.
 5. Next-open fill: decision at close t filled at open t+1 if valid (open != C_t and != C_{t+1}, finite), else at close t+1; overnight leg earns old position, intraday leg the new one; same lag for exits. Cost charged on |change| at the fill.
 6. Swap: rate/365 per calendar night between a held close and the market's next trading date; booked on the next trading date with that night's return. Positive short swap credited.
 7. Book is the sum over markets on the union of dates; all union dates in the period count (zero-return days included). IS starts at max(1990-01-02, first market's 200th close).
 8. Basket weights from sigma_t (60 returns) from 1990-01-02, no 200-day warm-up; gross; earns t->t+1.
 9. Exposure E = mean over days of (sum signed held notional)/(sum basket notional); next-open uses the post-fill position. Matched-benchmark Sharpe = sign(E) x basket Sharpe (scaling does not change Sharpe).
10. "Worse version" for the IS headline is ambiguous (the worse version is defined by OOS t): headline uses the lower IS Sharpe of the two fills; the line above also shows the IS Sharpe of the OOS-worse fill.
11. Bootstrap: ceil(n/10) blocks with uniform starts in [0, n-10], last block truncated to n; numpy default_rng(0).
12. Look-ahead tests run on the decision series (positions decided at closes); the perturbation replaces closes after d with a random walk. Cut dates drawn on the union calendar from 1992 on.
13. Gate decisive fill chosen at 1x cost (cost x2 reported, not gated).''')
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
