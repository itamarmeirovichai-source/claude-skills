#!/usr/bin/env python3
"""H0019 (gamma-conditioned last-half-hour momentum), run as pre-registered in
agents/ledger.csv. Nothing here is tuned after seeing results.

Rule (as registered):
  eligible day = previous trading day's SqueezeMetrics GEX < 0 (control: >= 0)
  signal       = sign( close of today's 15:29 bar / close of prior session's 15:59 bar - 1 )
  entry        = open of the 15:30 bar, in the signal direction
  exit         = close of the 15:59 bar; one trade a day, no stop, no target
  cost         = 2 bp round trip; unit = net return in bp per trade
  D1 in-sample = SPXUSD 1m 2011-05..2018-12 (FutureSharks); D2 OOS = SPY 1m RTH 2019-01..2025-07
  pass only if D2 net mean > 0 with one-sided t >= z(0.05/N) AND D1 gross mean > 0

Implementation choices fixed BEFORE any result was computed (also in the report):
  * "session" = weekday with at least one bar in 09:30..15:59 NY (same as gapfade.py).
  * prior session = the previous session in the price file; if its 15:59 bar is
    missing, the day is skipped (no reaching further back), as in H0017.
  * previous trading day's GEX = the latest DIX.csv row dated strictly before the
    trade date (as-of lookup; DIX rows are end-of-day values).
  * today's 15:29 bar must exist; a zero return gives no trade.
  * eligibility and signal use only: DIX rows dated < today, the prior session's
    bars, today's bars up to 15:29. Proven by the future-truncation test below.
  * fill: entry = open of the first bar in 15:30..15:59 (normally 15:30);
    exit = close of the last bar at or before 15:59 (normally 15:59). A day with no
    bar in 15:30..15:59 cannot be filled and is counted, not traded.
  * t = mean / (sd/sqrt(n)), one-sided; bar z = Phi^-1(1 - 0.05/N), N from the ledger.
    Bootstrap p5 = 5th percentile of the mean over 10,000 iid resamples (seed 0).
  * trades/yr = trades / (calendar span of the dataset window in years).
Stage 2 (run ONLY if the decision rule passes; all fixed here in advance):
  (a) same rule at 5 bp cost;
  (b) threshold = 20th percentile of the 252 GEX rows ending with the previous
      trading day's row (inclusive) instead of 0; needs 252 rows of history;
  (c) NQ 1m (hindsight-finance) 2020-09..2025-11, GEX < 0, 2 bp, roll weeks excluded
      (Mon-Fri of the 3rd-Friday week of Mar/Jun/Sep/Dec plus the next Monday).

    CLAUDE_SCRATCH=<dir with spx/, intraday/, gex/> python3 -I gamma.py > run.txt
Data are read from $CLAUDE_SCRATCH (never committed).
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FLEET = HERE.parents[2]                      # skills/prop-fleet
SCR = Path(os.environ["CLAUDE_SCRATCH"])


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lg = _load("ledger_gate", FLEET / "agents/daily/2026-10-05/eng_head/ledger_gate.py")
gf = _load("loaders", HERE / "loaders.py")      # gapfade-H0012 loaders + sha pins

N = lg.ledger_n(FLEET / "agents/ledger.csv")
assert N == 197, N
ALPHA, Z = lg.alpha_z(N)
COST_BP = 2.0
GEX_SHA = "51bef9ea5ee13af2f72b14f4198de57eeb865a36c1d3e244a3f64b3603e9ce62"

WINDOWS = {"D1": ("2011-05-01", "2018-12-31"), "D2": ("2019-01-01", "2025-07-31"),
           "D3": ("2020-09-01", "2025-11-30")}


def load_gex() -> pd.Series:
    p = SCR / "gex/DIX.csv"
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != GEX_SHA:
        raise SystemExit(f"sha256 mismatch DIX.csv: {h}")
    d = pd.read_csv(p, parse_dates=["date"])
    assert list(d.columns) == ["date", "price", "dix", "gex"], d.columns
    d = d.dropna(subset=["gex"]).drop_duplicates("date").sort_values("date")
    return pd.Series(d.gex.to_numpy(), index=d.date.dt.date)


class Gex:
    """As-of lookups that can only see DIX rows dated strictly before the trade date."""

    def __init__(self, s: pd.Series):
        self.d = np.array(list(s.index), dtype="datetime64[D]")
        self.v = s.to_numpy(float)
        self.n = len(self.v)

    def _pos(self, day) -> int:                     # number of rows dated < day
        return int(np.searchsorted(self.d, np.datetime64(day, "D"), side="left"))

    def prev(self, day):
        p = self._pos(day)
        return (self.v[p - 1], self.d[p - 1]) if p > 0 else (np.nan, None)

    def prev_threshold(self, day, win=252, q=0.20):
        p = self._pos(day)
        return np.quantile(self.v[p - win:p], q) if p >= win else np.nan


# ── per-day signal (ex-ante only) and fill ───────────────────────────────────
def signal(g_today: pd.DataFrame, g_prior, gex: Gex, day, regime: str, thr: str = "zero"):
    """Returns (side, gex_value) or None. Uses only bars <= 15:29 of today."""
    if g_prior is None:
        return None
    gv, _ = gex.prev(day)
    if not np.isfinite(gv):
        return None
    cut = 0.0 if thr == "zero" else gex.prev_threshold(day)
    if not np.isfinite(cut):
        return None
    neg = gv < cut
    if (regime == "neg") != neg:
        return None
    b0 = gf._bar(g_prior, 1559)
    b1 = gf._bar(g_today, 1529)
    if b0 is None or b1 is None:
        return None
    r = b1.c / b0.c - 1
    if r == 0 or not np.isfinite(r):
        return None
    return (1 if r > 0 else -1), gv


def fill(g_today: pd.DataFrame):
    w = g_today[(g_today.hm >= 1530) & (g_today.hm <= 1559)]
    if w.empty:
        return None
    return w.o.iloc[0], w.c.iloc[-1], int(w.hm.iloc[0]), int(w.hm.iloc[-1])


def run(S: dict, gex: Gex, regime: str, lo, hi, excluded=frozenset(), cost=COST_BP, thr="zero"):
    days = list(S)
    out, unfilled = [], 0
    for i, d in enumerate(days):
        if i == 0 or d in excluded or not (lo <= d <= hi):
            continue
        sg = signal(S[d], S[days[i - 1]], gex, d, regime, thr)
        if sg is None:
            continue
        f = fill(S[d])
        if f is None:
            unfilled += 1
            continue
        side, gv = sg
        entry, ex, ehm, xhm = f
        gross = side * (ex / entry - 1) * 1e4
        out.append(dict(date=d, side=side, gex=gv, entry=entry, exit=ex, entry_hm=ehm,
                        exit_hm=xhm, gross_bp=gross, net_bp=gross - cost))
    return pd.DataFrame(out), unfilled


def truncation_test(S: dict, gex_series: pd.Series, lo, hi) -> int:
    """For EVERY day in the window and both regimes and both thresholds: the signal
    (eligibility + side + GEX value) computed from (a) today's bars truncated at 15:29
    and (b) a GEX table truncated to rows dated < today must equal the full-data one."""
    full = Gex(gex_series)
    days = list(S)
    checked = 0
    for i, d in enumerate(days):
        if i == 0 or not (lo <= d <= hi):
            continue
        g = S[d]
        g_cut = g[g.hm <= 1529]
        gser_cut = gex_series[[x < d for x in gex_series.index]]
        cut = Gex(gser_cut) if len(gser_cut) else None
        for regime in ("neg", "pos"):
            for thr in ("zero", "p20"):
                a = signal(g, S[days[i - 1]], full, d, regime, thr)
                b = signal(g_cut, S[days[i - 1]], cut, d, regime, thr) if cut else None
                assert a == b, (d, regime, thr, a, b)
        checked += 1
    return checked


# ── stats ────────────────────────────────────────────────────────────────────
def boot_p5(x: np.ndarray, draws=10_000, seed=0) -> float:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(draws, x.size))
    return float(np.quantile(x[idx].mean(1), 0.05))


def tstat(x):
    return x.mean() / (x.std(ddof=1) / np.sqrt(x.size)) if x.size > 1 else np.nan


def report(label: str, t: pd.DataFrame, years: float, unfilled: int) -> dict:
    if t.empty:
        print(f"  {label}: no trades")
        return dict(n=0, gross=np.nan, net=np.nan, t_net=np.nan)
    g, n_ = t.gross_bp.to_numpy(), t.net_bp.to_numpy()
    st = dict(n=n_.size, per_yr=n_.size / years, gross=g.mean(), net=n_.mean(),
              t_net=tstat(n_), t_gross=tstat(g), p5_net=boot_p5(n_), p5_gross=boot_p5(g),
              win=(n_ > 0).mean())
    odd = int(((t.entry_hm != 1530) | (t.exit_hm != 1559)).sum())
    print(f"  {label}: n {st['n']}  trades/yr {st['per_yr']:.1f}  mean bp gross {st['gross']:+.2f}  "
          f"net {st['net']:+.2f}  t net {st['t_net']:+.2f} (gross {st['t_gross']:+.2f})  "
          f"boot p5 net {st['p5_net']:+.2f} (gross {st['p5_gross']:+.2f})  win {st['win']:.3f}  "
          f"long share {(t.side > 0).mean():.2f}  [fills not at 15:30/15:59: {odd}; unfillable: {unfilled}]")
    by = t.assign(y=pd.to_datetime(t.date).dt.year).groupby("y").agg(
        n=("net_bp", "size"), gross=("gross_bp", "mean"), net=("net_bp", "mean"))
    print("     by year (n, gross bp, net bp): " + "  ".join(
        f"{y}:{int(r.n)}/{r.gross:+.1f}/{r.net:+.1f}" for y, r in by.iterrows()))
    return st


def years_of(S, lo, hi):
    ds = [d for d in S if lo <= d <= hi]
    return ds, (pd.Timestamp(ds[-1]) - pd.Timestamp(ds[0])).days / 365.25


def main() -> int:
    print(f"ledger N = {N}; one-sided alpha = 0.05/{N} = {ALPHA:.3e}; bar z = {Z:.4f}")
    gser = load_gex()
    gex = Gex(gser)
    print(f"GEX rows {len(gser)} ({gser.index[0]}..{gser.index[-1]}); share < 0: {(gser < 0).mean():.3f}")
    res, data = {}, {}
    for key, loader in (("D1", gf.load_d1), ("D2", gf.load_d2)):
        S = gf.sessions(loader())
        lo, hi = (pd.Timestamp(x).date() for x in WINDOWS[key])
        ds, yrs = years_of(S, lo, hi)
        data[key] = (S, lo, hi, yrs)
        print(f"\n=== {key}: sessions in window {len(ds)} ({ds[0]}..{ds[-1]}, {yrs:.2f} yr); "
              f"missing 15:29 bar {sum(gf._bar(S[d], 1529) is None for d in ds)}, "
              f"missing 15:59 bar {sum(gf._bar(S[d], 1559) is None for d in ds)}")
        print(f"    future-truncation test (all days, both regimes, both thresholds): "
              f"{truncation_test(S, gser, lo, hi)} days OK")
        for regime, name in (("neg", "GEX<0 (test)"), ("pos", "GEX>=0 (control)")):
            t, unf = run(S, gex, regime, lo, hi)
            res[(key, regime)] = report(f"{name}", t, yrs, unf)
            t.to_csv(SCR / f"h0019_trades_{key}_{regime}.csv", index=False)

    d1, d2 = res[("D1", "neg")], res[("D2", "neg")]
    c1 = d2["net"] > 0 and d2["t_net"] >= Z
    c2 = d1["gross"] > 0
    ok = bool(c1 and c2)
    print(f"\n=== decision rule: D2 net mean > 0 with one-sided t >= {Z:.4f}: net {d2['net']:+.2f} bp, "
          f"t {d2['t_net']:+.2f} -> {c1} | D1 gross mean > 0: {d1['gross']:+.2f} bp -> {c2} "
          f"=> {'PASS' if ok else 'FAIL'}")

    if not ok:
        print("\nstage 2 not run (pre-registered: only if stage 1 passes)")
        return 0
    print("\n=== STAGE 2 (fixed in advance)")
    for key in ("D1", "D2"):
        S, lo, hi, yrs = data[key]
        t, unf = run(S, gex, "neg", lo, hi, cost=5.0)
        report(f"{key} (a) cost 5 bp, GEX<0", t, yrs, unf)
        t, unf = run(S, gex, "neg", lo, hi, thr="p20")
        report(f"{key} (b) GEX < trailing-252 p20, 2 bp", t, yrs, unf)
    S = gf.sessions(gf.load_d3())
    lo, hi = (pd.Timestamp(x).date() for x in WINDOWS["D3"])
    ex = frozenset(gf.roll_excluded(list(S)))
    ds, yrs = years_of(S, lo, hi)
    print(f"  D3 NQ sessions {len(ds)} ({ds[0]}..{ds[-1]}), roll-excluded {sum(d in ex for d in ds)}; "
          f"truncation test {truncation_test(S, gser, lo, hi)} days OK")
    for regime in ("neg", "pos"):
        t, unf = run(S, gex, regime, lo, hi, excluded=ex)
        report(f"D3 (c) NQ ex roll, GEX {'<0' if regime == 'neg' else '>=0 control'}, 2 bp", t, yrs, unf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
