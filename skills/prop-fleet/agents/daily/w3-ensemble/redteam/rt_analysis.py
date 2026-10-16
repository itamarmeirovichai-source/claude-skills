"""Red team F1: timing, cost sensitivity, ex-post weight diagnostic and stats checks, all built from the
cached sleeve pieces of rt_rebuild.py (head's own functions). No new strategy variants; every row below
is a diagnostic of F1-01's fixed positions.

usage: CLAUDE_SCRATCH=<data dir> python3 rt_analysis.py <cache dir>
"""
import sys
from pathlib import Path

import warnings
import numpy as np
warnings.filterwarnings("ignore")
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ensemble as E  # noqa: E402

D3 = E.D3
C = Path(sys.argv[1])
W0, W1 = E.W0, E.W1
SPL = E.SPLICE_1M_END
out = []
P = lambda *a: (print(*a), out.append(" ".join(str(x) for x in a)))


def s1(which="ftmo", comm=0.00065, half=0.0005, swap_yr=0.30, swap_days=365.0, swap_mult=1.0,
       half_alt=None):
    b = pd.read_pickle(C / f"s1_{which}.pkl")
    if half_alt is None:
        cost = (comm + half) * b.to
    else:
        cost = (comm + half) * b.to_btceth + (comm + half_alt) * b.to_alts
    sw = swap_mult * swap_yr / swap_days * b.gross_notional
    return pd.DataFrame(dict(net=b.gross - cost - sw, gross_notional=b.gross_notional, gross=b.gross,
                             cost=cost, swap=sw))


def s1_triple(which="ftmo", weekday=2, weekend_charged=True):
    """swap 30%/yr: charged x3 on one weekday (MT5 'rollover3days'); weekend nights charged or not."""
    b = pd.read_pickle(C / f"s1_{which}.pkl")
    dow = b.index.dayofweek
    mult = np.where(dow == weekday, 3.0, 1.0)
    if not weekend_charged:
        mult = np.where(dow >= 5, 0.0, mult)
    cost = 0.00115 * b.to
    sw = 0.30 / 360 * b.gross_notional * mult      # MT5 interest mode uses a 360-day year
    return pd.DataFrame(dict(net=b.gross - cost - sw, gross_notional=b.gross_notional, gross=b.gross))


def s2(cost_pts=0.75, roll=True, which="splice"):
    sfx = "" if roll else "_noroll"
    parts = []
    for nm in ("m1", "m5"):
        d = pd.read_pickle(C / f"s2_{nm}{sfx}.pkl")
        net = np.where(d.entry.isna(), 0.0, (d.gross_pts - cost_pts * d.units) / d.entry)
        gross = np.where(d.entry.isna(), 0.0, d.gross_pts / d.entry)
        parts.append(pd.DataFrame(dict(net=net, gross=gross, units=d.units), index=d.index))
    a, b = parts
    if which == "1m":
        return a
    return pd.concat([a.loc[:SPL], b.loc[SPL + pd.Timedelta(days=1):]])


def st(x):
    return D3.stats(x.loc[W0:W1].dropna().values)


def line(name, x):
    s = st(x)
    return (f"{name:58s} mean {s['mean_bp']:+6.2f} bp/d  t {s['t']:+5.2f} (iid {s['t_iid']:+5.2f} NW {s['t_nw']:+5.2f})"
            f"  p5 {s['p5_bp']:+6.2f}  Sh {s['sharpe']:+5.2f}")


# ---------------------------------------------------------------- 0. reproduce the headline
S1, S2 = s1(), s2()
base = E.stack(S1, S2)
K = base[["k1", "k2"]]
P("=== 0. reproduction of F1-01 from cached pieces")
P(line("F1-01 stack (head: +1.65, t 0.74)", base.r))
ref = pd.read_csv(E.HERE / "daily_F1-01.csv.gz", index_col=0, parse_dates=True)
P("   max |r - head daily_F1-01.r| =", float((base.r - ref.r.reindex(base.index)).abs().max()))

# ---------------------------------------------------------------- 1. timing
P("\n=== 1. timing / look-ahead diagnostics")
# 1a: k uses only data through the previous month end -- shift test: k from one month EARLIER (staler) and
#     a deliberately look-ahead k (through the current month end) bracket the effect of the k timing.
cal = base.index
r1 = S1.net.reindex(cal)


def kfrom(lag_months):
    rows = {}
    for m0 in cal[cal.day == 1]:
        prev = (m0 - pd.DateOffset(months=lag_months)) - pd.Timedelta(days=1) if lag_months >= 0 else \
            m0 + pd.offsets.MonthEnd(0)
        a = r1.loc[:prev].dropna().iloc[-E.LOOK:]
        b = S2.net.loc[:prev].iloc[-E.LOOK:]
        rows[m0] = (min(E.TARGET / (a.std() * np.sqrt(365)), E.K1_CAP) if len(a) == E.LOOK else np.nan,
                    min(E.TARGET / (b.std() * np.sqrt(252)), E.K2_CAP) if len(b) == E.LOOK else np.nan)
    return pd.DataFrame.from_dict(rows, orient="index", columns=["k1", "k2"]).reindex(cal).ffill()


k0 = kfrom(0)
P("   k recomputed independently == head k:", bool(np.allclose(k0.loc[W0:W1].values, K.loc[W0:W1].values)))
P(line("   k one month staler", E.stack(S1, S2, k=kfrom(1)).r))
P(line("   k LOOK-AHEAD (through current month end, invalid)", E.stack(S1, S2, k=kfrom(-1)).r))
# 1b: margin cap uses ex-post u2 (units>0 that day); show it never binds, and what the margin would be
#     with a 1-unit US100 position assumed every session regardless
m = base.loc[W0:W1]
u_all = (S2.units.reindex(cal).fillna(0) >= 0).astype(float).loc[W0:W1]
P(f"   margin max {m.margin.max():.3f}; with US100 assumed on every calendar day: "
  f"{(m.k1 * m.n1 / m.k1 + m.k2 / E.LEV_US100).max():.3f}; cap days {int((m.f < 1).sum())}")
# 1c: UTC-day vs NY-session alignment. NY RTH 09:30-16:00 = 13:30/14:30-20:00/21:00 UTC, inside the same UTC
#     day as the S1 return, so same-date stacking is right. Lead/lag correlations as a check of mis-dating:
w = base.loc[W0:W1]
s2d = w.r2.where(w.r2 != 0)
for lag in (-1, 0, 1):
    P(f"   corr(S1 day t+{lag}, S2 session t) = {w.r1.shift(-lag).corr(s2d):+.3f}")
# 1d: splice -- 1m vs 5m S2 at FTMO cost on the overlap, and the stack using 1m only through 2025-11-21
a1, a5 = s2(which="1m"), None
b5 = pd.read_pickle(C / "s2_m5.pkl")
P(f"   splice: 1m sessions end {a1.index[-1].date()}, 5m sessions start {b5.index[0].date()}; "
  f"stack S2 days after splice {int((S2.index > SPL).sum())}")
P(line("   stack on 2023-01-01..2025-11-21 (1m only)", E.stack(S1, a1, k=K).r.loc[:SPL]))
P(line("   stack on 2023-01-01..2025-11-21 (spliced; same)", base.r.loc[:SPL]))
P(line("   stack on 2025-11-22..2026-05-07 (5m part only)", base.r.loc[SPL + pd.Timedelta(days=1):]))
s2_5all = s2(which="splice")  # noqa
x5 = pd.read_pickle(C / "s2_m5.pkl")
net5 = pd.Series(np.where(x5.entry.isna(), 0, (x5.gross_pts - 0.75 * x5.units) / x5.entry), index=x5.index)
S2_5 = pd.DataFrame(dict(net=net5, units=x5.units))
P(line("   stack with S2 from 5m for all of W (data check, headline k)", E.stack(S1, S2_5, k=K).r))
# 1e: weekday/weekend split of the stack (S2 is 0 on weekends)
wk = base.r.loc[W0:W1]
P(f"   stack mean weekdays {wk[wk.index.dayofweek < 5].mean() * 1e4:+.2f} bp, weekends "
  f"{wk[wk.index.dayofweek >= 5].mean() * 1e4:+.2f} bp")

# ---------------------------------------------------------------- 2. costs
P("\n=== 2. cost sensitivity (F1-01 positions and the headline k held fixed)")
b1 = pd.read_pickle(C / "s1_ftmo.pkl").loc[W0:W1]
P(f"   S1 unit book in W: gross {b1.gross.mean() * 1e4:+.2f} bp/d, turnover {b1.to.mean():.3f}/d "
  f"(BTC/ETH {b1.to_btceth.mean():.3f}, alts {b1.to_alts.mean():.3f}), gross notional {b1.gross_notional.mean():.3f}, "
  f"BTC/ETH notional {b1.gn_btceth.mean():.3f}; mean k1 {K.loc[W0:W1].k1.mean():.2f}")
x2 = pd.read_pickle(C / "s2_m1.pkl")
P(f"   S2 units/session (1m, W) {x2.loc[W0:SPL].units.mean():.2f}; 0.75 pt/unit = "
  f"{(0.75 * x2.loc[W0:SPL].units / x2.loc[W0:SPL].entry).mean() * 1e4:.2f} bp/session; mean k2 {K.loc[W0:W1].k2.mean():.2f}")
rows = [
    ("headline FTMO (11.5 bp/side, swap 30%/365, US100 0.75)", dict(), 0.75),
    ("swap 30%/360 (MT5 interest-mode year)", dict(swap_days=360.0), 0.75),
    ("swap 15%/yr (half)", dict(swap_yr=0.15), 0.75),
    ("swap 0", dict(swap_yr=0.0), 0.75),
    ("half-spread 0 (commission only, 6.5 bp/side)", dict(half=0.0), 0.75),
    ("half-spread 2.5 bp", dict(half=0.00025), 0.75),
    ("half-spread 10 bp", dict(half=0.0010), 0.75),
    ("half-spread BTC/ETH 3 bp, alts 15 bp", dict(half=0.0003, half_alt=0.0015), 0.75),
    ("half-spread BTC/ETH 3 bp, alts 25 bp", dict(half=0.0003, half_alt=0.0025), 0.75),
    ("US100 0.25 pt/side (0.5 pt round trip)", dict(), 0.25),
    ("US100 0.375 pt/side (H0022 futures)", dict(), 0.375),
    ("US100 0.5 pt/side", dict(), 0.5),
    ("US100 1.0 pt/side", dict(), 1.0),
    ("most favourable plausible: swap 0, 6.5 bp/side, US100 0.25", dict(swap_yr=0.0, half=0.0), 0.25),
    ("ZERO cost everywhere (gross)", dict(swap_yr=0.0, half=0.0, comm=0.0), 0.0),
]
for name, kw, c2 in rows:
    P(line("   " + name, E.stack(s1(**kw), s2(c2), k=K).r))
P("   swap timing (30%/360 per night, 11.5 bp/side, US100 0.75):")
for nm, kw in (("x3 on Wed, weekends charged (9 nights/wk)", dict(weekday=2, weekend_charged=True)),
               ("x3 on Fri, weekends NOT charged (FX-style, 7/wk)", dict(weekday=4, weekend_charged=False))):
    P(line("     " + nm, E.stack(s1_triple(**kw), S2, k=K).r))
# re-estimated k (prereg says k from the sleeve's own net series) for the zero-cost case
P(line("   ZERO cost with k re-estimated on gross series", E.stack(s1(swap_yr=0, half=0, comm=0), s2(0.0)).r))

# ---------------------------------------------------------------- 3. weights
P("\n=== 4. ex-post fixed weight diagnostic (NOT a variant): stack = a*k1*r1 + (1-a)*k2*r2 rescaled x2")
best = None
for a in np.linspace(0, 1, 101):
    x = 2 * (a * base.k1 * base.r1 + (1 - a) * base.k2 * base.r2)
    s = st(x)
    if best is None or s["t"] > best[1]["t"]:
        best = (a, s)
P(f"   best a = {best[0]:.2f}: t {best[1]['t']:+.2f}, mean {best[1]['mean_bp']:+.2f}, Sharpe {best[1]['sharpe']:+.2f}")
for a in (0.0, 0.5, 1.0):
    P(line(f"   a = {a:.1f}", 2 * (a * base.k1 * base.r1 + (1 - a) * base.k2 * base.r2)))
# also with raw (unscaled) sleeve returns, constant weights
best = None
for a in np.linspace(0, 1, 101):
    x = a * base.r1 + (1 - a) * base.r2
    s = st(x)
    if best is None or s["t"] > best[1]["t"]:
        best = (a, s)
P(f"   raw sleeves, best constant mix a*r1+(1-a)*r2: a={best[0]:.2f} t {best[1]['t']:+.2f}")
# same at zero cost / F1-03 costs, to show the ceiling
for nm, x1, x2_ in (("F1-03 costs (venue)", None, 0.375), ("zero cost", dict(swap_yr=0, half=0, comm=0), 0.0)):
    if x1 is None:
        v = pd.read_pickle(C / "s1_ftmo.pkl")
        S1v = pd.DataFrame(dict(net=v.venue_net, gross_notional=v.gross_notional))
    else:
        S1v = s1(**x1)
    bb = E.stack(S1v, s2(x2_), k=K)
    tb = max((st(a * bb.k1 * bb.r1 + (1 - a) * bb.k2 * bb.r2)["t"], a) for a in np.linspace(0, 1, 101))
    P(f"   ex-post best weight at {nm}: t {tb[0]:+.2f} at a={tb[1]:.2f}")

# ---------------------------------------------------------------- 5. stats checks
P("\n=== 5. statistics checks")
x = base.r.loc[W0:W1].values
n = len(x)
mu, sd = x.mean(), x.std(ddof=1)
# independent NW (Bartlett, lag 10) via explicit autocovariances
g = [np.sum((x[L:] - mu) * (x[:n - L] - mu)) / n for L in range(11)]
lrv = g[0] + 2 * sum((1 - L / 11) * g[L] for L in range(1, 11))
P(f"   iid t {mu / (sd / np.sqrt(n)):+.4f}; NW10 t (independent) {mu / np.sqrt(lrv / n):+.4f}; "
  f"head {st(base.r)['t_iid']:+.4f}/{st(base.r)['t_nw']:+.4f}")
try:
    import statsmodels.api as sm
    r = sm.OLS(x, np.ones(n)).fit(cov_type="HAC", cov_kwds=dict(maxlags=10, use_correction=False))
    P(f"   statsmodels HAC(10) t {r.tvalues[0]:+.4f}")
except Exception as ex:  # noqa
    P(f"   statsmodels not available ({type(ex).__name__})")
# analytic p5 vs bootstrap
P(f"   analytic iid p5 = mean - 1.645 se = {(mu - 1.645 * sd / np.sqrt(n)) * 1e4:+.2f} bp (head iid boot "
  f"{st(base.r)['p5_iid_bp']:+.2f})")
# annualisation: stack Sharpe sqrt365 on calendar days with weekend zeros is internally consistent; the
# standalone s2 line uses sqrt365 on SESSION-ONLY data (should be sqrt252 / session-count)
s2w = S2.net.loc[W0:W1].values
P(f"   s2 standalone Sharpe: head sqrt365 {s2w.mean() / s2w.std(ddof=1) * np.sqrt(365):+.3f} vs sqrt(sessions/yr "
  f"{len(s2w) / ((W1 - W0).days / 365.25):.0f}) {s2w.mean() / s2w.std(ddof=1) * np.sqrt(len(s2w) / ((W1 - W0).days / 365.25)):+.3f}")
# vol actually delivered by each scaled sleeve on the calendar index
P(f"   realised vol on calendar days: k1*r1 {(base.k1 * base.r1).loc[W0:W1].std() * np.sqrt(365):.3f}, "
  f"k2*r2 {(base.k2 * base.r2).loc[W0:W1].std() * np.sqrt(365):.3f} (target 0.10 each)")
# t needed vs achievable: mean needed at the observed vol for t = 3.5745
P(f"   mean needed for t=3.5745 at the stack's sd: {3.5745 * sd / np.sqrt(n) * 1e4:+.2f} bp/d "
  f"(= Sharpe {3.5745 / np.sqrt(n / 365):.2f}); observed {mu * 1e4:+.2f}")

(Path(__file__).parent / "rt_analysis.txt").write_text("\n".join(out) + "\n")
