"""G2 red team: information-only checks (NOT counted variants).
1) US-only (US500/US100/US30) book, every variant, both fills, at zero cost / spread-only / 1x.
2) Swap actually charged OOS by year (is today's swap what kills it?).
3) Daily-rebalanced (vs fixed-at-entry) notional for the best rule, zero cost.
usage: G2_CACHE=... python3 redteam/rt.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import meanrev as M

data = M.load()
US = ["US500", "US100", "US30"]


def sub_book(names, var, mode, **kw):
    keep = [m for m in M.MKT if m[0] in names]
    old_mkt, old_names = M.MKT, M.NAMES
    M.MKT, M.NAMES = keep, [m[0] for m in keep]
    try:
        return M.book(data, var, mode, **kw)
    finally:
        M.MKT, M.NAMES = old_mkt, old_names


print("== 1) US-only book (US500, US100, US30), OOS 2013-2026 ==")
print(f"{'id':6} {'fill':5} {'cost':6} {'sharpe':>7} {'t':>6} {'alpha_t':>8} {'ret_yr':>7}")
best = -9
for v in M.VARIANTS:
    for mode in ("close", "open"):
        for lab, kw in (("zero", dict(swap_on=False, cost_on=False)), ("noswap", dict(swap_on=False)), ("1x", {})):
            b = sub_book(US, v, mode, **kw).loc[M.OOS_START:]
            s = M.summarize(b)
            best = max(best, s["t"])
            print(f"{v:6} {mode:5} {lab:6} {s['sharpe']:7.3f} {s['t']:6.2f} {s['alpha_t']:8.2f} {s['ret_yr']:7.4f}")
print(f"best US-only OOS t across all variants/fills/cost levels: {best:.2f} (bar {M.BAR})")

print("\n== 1b) US-only, IS (to 2012), zero cost, close fill ==")
for v in M.VARIANTS:
    s = M.summarize(sub_book(US, v, "close", swap_on=False, cost_on=False).loc[:M.IS_END])
    print(f"{v} sharpe {s['sharpe']:.3f} t {s['t']:.2f}")

print("\n== 2) Full book G2-06 open: OOS gross / swap / spread by year (fraction of book) ==")
b = M.book(data, "G2-06", "open").loc[M.OOS_START:]
y = b[["gross", "swap", "cost"]].groupby(b.index.year).sum()
y["net"] = y.gross + y.swap - y.cost
print(y.round(4).to_string())
print("totals:", y.sum().round(4).to_dict())

print("\n== 3) Daily-rebalanced notional (RISK/sigma_t each day) vs fixed at entry, G2-06/G2-02 close, zero cost, OOS ==")
for v in ("G2-06", "G2-02"):
    rows = []
    for name, *_ in M.MKT:
        df = data[name]
        pos, notl = M.positions(df, **M.VARIANTS[v])
        sig = df.close.pct_change().rolling(60).std().values
        nl2 = np.where(pos != 0, M.RISK / sig, 0.0)
        r = df.close.pct_change().fillna(0).values
        rows.append(pd.Series(np.r_[0.0, (pos * nl2)[:-1]] * r, index=df.index))
    cal = sorted(set().union(*[s.index for s in rows]))
    x = sum(s.reindex(cal).fillna(0) for s in rows)
    x = pd.Series(x, index=pd.DatetimeIndex(cal)).loc[M.OOS_START:]
    print(v, f"rebalanced: sharpe {M.sharpe(x):.3f} t {M.tstat(x.values)[0]:.2f}")
