#!/usr/bin/env python3
"""H0012 (S&P overnight-gap fade) and H0017 (ex-ante eligibility companion), run as
pre-registered in agents/ledger.csv and agents/daily/2026-10-04/prereg_gapfade_draft.txt.

Nothing here is tuned. Rules (one variant, both hypotheses):
  P0 = close of the prior session's 15:59 bar; O = open of today's 09:30 bar
  g  = O/P0 - 1; s = stdev of g over the previous 20 sessions (today excluded)
  trade if |g| > 1.0 * s; side = -sign(g); entry = open of 09:31 bar; target = P0
  1R = max(|entry - P0|, 0.15% of entry); stop = entry -/+ 1R
  skip if the target is already at/beyond entry (gap filled by 09:31)
  bars 09:31..15:59: stop first if both touched in one bar; stop fills at the worse
  of stop and bar open; target fills at P0; else exit at the 15:59 close
  cost = 2 bp of entry round trip; R = P&L / 1R
H0012: today's 09:30, 09:31 AND 15:59 bars must exist (as written; reads the future).
H0017: only today's 09:30 and 09:31 bars must exist; exit at the last bar at or
       before 15:59; prior session = most recent earlier weekday with RTH bars, and if
       its 15:59 bar is missing, skip (do not reach further back).

Implementation choices fixed BEFORE any result was computed (written into the report):
  * "session" = weekday with at least one bar in 09:30..15:59 NY. H0012 uses the same
    prior-session rule as H0017 (the prereg does not say otherwise).
  * s = sample stdev (ddof=1) of the last 20 defined gaps strictly before today; a day
    with fewer than 20 earlier defined gaps is not traded.
  * D3 roll weeks (Mon-Fri of the week holding the 3rd Friday of Mar/Jun/Sep/Dec, plus
    the following Monday) are never traded and their gaps are left out of s; their bars
    still serve as the prior session for the next day's P0.
  * "target already beyond entry" includes entry == P0.
  * A bar that opens through the target fills at P0 (no price improvement).

    CLAUDE_SCRATCH=... python3 -I gapfade.py > run.txt
Data are read from $CLAUDE_SCRATCH (never committed); see fetch notes in the report.
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

_spec = importlib.util.spec_from_file_location(
    "ledger_gate", FLEET / "agents/daily/2026-10-05/eng_head/ledger_gate.py")
lg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lg)

N = lg.ledger_n(FLEET / "agents/ledger.csv")
assert N == 196, N
ALPHA, Z = lg.alpha_z(N)
COST = 0.0002
MIN_R = 0.0015
K = 1.0
LOOKBACK = 20

SHA = {  # measured at fetch time (2026-10-06); D2/D3 also match data_fetch.py pins
    "spx/SPX_2010.csv": "1166316b0547be9610b3027f312894a582424917e7905d0ffca1bee194e8d10f",
    "spx/SPX_2011.csv": "5c93bd8779d19d127a79184a4edd70735ff79a03e9c2970794a0670cb90bc90c",
    "spx/SPX_2012.csv": "9fa9e760fab82b4fb53e4a88e8eaf2ea258f3ad578b21765b4d6376539624efb",
    "spx/SPX_2013.csv": "28b162825090927c5c9f47a6571a7b5d8a257dc40363cc9f7aa60a7919c82ff0",
    "spx/SPX_2014.csv": "f2fd077d58b2a9b5125456d8f7c8893b0ded3a3dd229792bf9afa231201daa72",
    "spx/SPX_2015.csv": "0f344ee1ecc0e34f707a340a482314159dc1f414950cc083deae8436b55b9493",
    "spx/SPX_2016.csv": "8be247ca5008d6a91c6287c52f1b9df133e4b5ebad29141e9de4686a79c327d2",
    "spx/SPX_2017.csv": "01236a4178eb7802cd32fb569b7bed13670813ffddb69c95f47eee48d6552e3e",
    "spx/SPX_2018.csv": "7f20d258d549893be83c4416a115861eae8d54ae530dcfd1c3a0dd6e5cc11a43",
    "intraday/spy_rth.csv": "d4671c48d18bdaab21f4b44e02992d2fc91070b01a357189f67b2305a75f9ee6",
    "intraday/nq_1m.parquet": "46f2a9a6ee921dcb8b5895120f8069e5fa3197db94180cbe2df8bba725390662",
}


def _check(rel: str) -> Path:
    p = SCR / rel
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != SHA[rel]:
        raise SystemExit(f"sha256 mismatch {rel}: {h}")
    return p


# ── loaders: all return o,h,l,c indexed by naive NY bar-open time ────────────
def load_d1() -> pd.DataFrame:
    fr = []
    for y in range(2010, 2019):
        f = _check(f"spx/SPX_{y}.csv")
        fr.append(pd.read_csv(f, sep=";", header=None, names=["dt", "o", "h", "l", "c", "v"]))
    d = pd.concat(fr)
    d["dt"] = pd.to_datetime(d["dt"], format="%Y%m%d %H%M%S")   # same as tjr_backtest.load_minutes
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def load_d2() -> pd.DataFrame:
    d = pd.read_csv(_check("intraday/spy_rth.csv"), parse_dates=["caldt"])
    d = d.rename(columns={"caldt": "dt", "open": "o", "high": "h", "low": "l", "close": "c"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def load_d3() -> pd.DataFrame:
    d = pd.read_parquet(_check("intraday/nq_1m.parquet"))
    d = d.rename(columns={"DateTime_ET": "dt", "Open": "o", "High": "h", "Low": "l", "Close": "c"})
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def roll_excluded(dates) -> set:
    """Mon-Fri of the week holding the 3rd Friday of Mar/Jun/Sep/Dec, plus the next Monday."""
    out = set()
    years = sorted({d.year for d in dates})
    for y in years:
        for m in (3, 6, 9, 12):
            first = pd.Timestamp(y, m, 1)
            fri3 = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
            mon = fri3 - pd.Timedelta(days=4)
            for i in range(5):
                out.add((mon + pd.Timedelta(days=i)).date())
            out.add((fri3 + pd.Timedelta(days=3)).date())
    return out


# ── per-session table (ex-ante pieces only) ──────────────────────────────────
def sessions(m: pd.DataFrame) -> dict:
    t = m.index
    hm = t.hour * 100 + t.minute
    rth = m[(hm >= 930) & (hm <= 1559) & (t.dayofweek < 5)].copy()
    rth["date"] = rth.index.date
    rth["hm"] = rth.index.hour * 100 + rth.index.minute
    return {d: g for d, g in rth.groupby("date", sort=True)}


def _bar(g: pd.DataFrame, hm: int):
    r = g[g.hm == hm]
    return None if r.empty else r.iloc[0]


def gap_table(S: dict, excluded: set) -> pd.DataFrame:
    """One row per session: P0, O, g, s (from earlier gaps only)."""
    days = list(S)
    rows = []
    for i, d in enumerate(days):
        p0 = o = np.nan
        if i > 0:
            b = _bar(S[days[i - 1]], 1559)            # prior session's 15:59 bar, no reaching back
            if b is not None:
                p0 = b.c
        b = _bar(S[d], 930)
        if b is not None:
            o = b.o
        rows.append((d, p0, o))
    gt = pd.DataFrame(rows, columns=["date", "p0", "o"]).set_index("date")
    gt["g"] = gt.o / gt.p0 - 1
    hist = gt.g[~gt.index.isin(excluded)].dropna()
    hd, hv = list(hist.index), hist.to_numpy()
    # s for day d = stdev of the last 20 defined gaps on dates strictly before d
    pos = np.searchsorted(np.array(hd, dtype="datetime64[D]"),
                          np.array(list(gt.index), dtype="datetime64[D]"), side="left")
    gt["s"] = [hv[p - LOOKBACK:p].std(ddof=1) if p >= LOOKBACK else np.nan for p in pos]
    return gt


def trade_day(g: pd.DataFrame, p0: float, gap: float, s: float, mode: str):
    """Returns (side, entry, R1, exit, why) or None. mode in {'H0012','H0017'}."""
    if not (np.isfinite(gap) and np.isfinite(s)) or abs(gap) <= K * s:
        return None
    b930, b931 = _bar(g, 930), _bar(g, 931)
    if b930 is None or b931 is None:
        return None
    if mode == "H0012" and _bar(g, 1559) is None:
        return None                                   # as registered (look-ahead)
    side = -1 if gap > 0 else 1
    entry = b931.o
    if side * (p0 - entry) <= 0:
        return None                                   # gap filled by 09:31
    r1 = max(abs(entry - p0), MIN_R * entry)
    stop = entry - side * r1
    path = g[(g.hm >= 931) & (g.hm <= 1559)]
    for o, h, l, c in path[["o", "h", "l", "c"]].itertuples(index=False):
        hit_stop = l <= stop if side > 0 else h >= stop
        hit_tgt = h >= p0 if side > 0 else l <= p0
        if hit_stop:
            px = min(stop, o) if side > 0 else max(stop, o)
            return side, entry, r1, px, "stop"
        if hit_tgt:
            return side, entry, r1, p0, "target"
    return side, entry, r1, path.c.iloc[-1], "close"


def run(S: dict, gt: pd.DataFrame, excluded: set, mode: str) -> pd.DataFrame:
    out = []
    for d, g in S.items():
        if d in excluded:
            continue
        row = gt.loc[d]
        res = trade_day(g, row.p0, row.g, row.s, mode)
        if res is None:
            continue
        side, entry, r1, px, why = res
        gross = side * (px - entry)
        out.append(dict(date=d, side=side, entry=entry, r1=r1, exit=px, why=why,
                        gross_R=gross / r1, net_R=(gross - COST * entry) / r1))
    return pd.DataFrame(out)


# ── stats ────────────────────────────────────────────────────────────────────
def boot_p5(x: np.ndarray, draws=10_000, seed=0) -> float:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(draws, x.size))
    return float(np.quantile(x[idx].mean(1), 0.05))


def stats(t: pd.DataFrame, years: float) -> dict:
    g, n_ = t.gross_R.to_numpy(), t.net_R.to_numpy()
    n = n_.size
    se = n_.std(ddof=1) / np.sqrt(n)
    lb_boot, draws = lg.one_sided_lb(n_, t.date.astype(str).to_numpy(), N)
    return dict(n=n, per_yr=n / years, gross=g.mean(), net=n_.mean(),
                p5_net=boot_p5(n_), p5_gross=boot_p5(g),
                t_net=n_.mean() / se, t_gross=g.mean() / (g.std(ddof=1) / np.sqrt(n)),
                win=(n_ > 0).mean(), lb_normal=n_.mean() - Z * se, lb_boot=lb_boot,
                draws=draws, why=t.why.value_counts().to_dict())


def truncation_test(S: dict, gt: pd.DataFrame, excluded: set, k=60) -> int:
    """H0017 future-truncation check: deleting day d's bars after 09:31 must not change
    whether d trades, its side or entry. Returns the number of days checked."""
    rng = np.random.default_rng(1)
    days = [d for d in S if d not in excluded]
    checked = 0
    for d in rng.choice(np.array(days, dtype=object), size=min(k, len(days)), replace=False):
        g = S[d]
        row = gt.loc[d]
        a = trade_day(g, row.p0, row.g, row.s, "H0017")
        b = trade_day(g[g.hm <= 931], row.p0, row.g, row.s, "H0017")
        assert (a is None) == (b is None), d
        if a is not None:
            assert a[:3] == b[:3], d
        checked += 1
    return checked


def main() -> int:
    print(f"ledger N = {N}; one-sided alpha = 0.05/{N} = {ALPHA:.3e}; z = {Z:.4f}")
    summary = {}
    for name, loader, roll in (("D1 SPXUSD 2010-2018 (in-sample)", load_d1, False),
                               ("D2 SPY RTH 2019-2025 (primary OOS)", load_d2, False),
                               ("D3 NQ 2020-2025 ex roll weeks (second OOS)", load_d3, True)):
        m = loader()
        S = sessions(m)
        days = list(S)
        excluded = roll_excluded(days) if roll else set()
        gt = gap_table(S, excluded)
        years = (pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25
        n_ex = sum(d in excluded for d in days)
        print(f"\n=== {name}: sessions {len(days)} ({days[0]}..{days[-1]}, {years:.2f} yr), "
              f"roll-excluded {n_ex}, days with 15:59 bar missing {sum(_bar(S[d], 1559) is None for d in days)}")
        print(f"    future-truncation test (H0017, random days): {truncation_test(S, gt, excluded)} days OK")
        for mode in ("H0012", "H0017"):
            t = run(S, gt, excluded, mode)
            st = stats(t, years)
            summary[(name[:2], mode)] = st
            print(f"  {mode}: n {st['n']}  trades/yr {st['per_yr']:.1f}  "
                  f"mean R gross {st['gross']:+.4f}  net {st['net']:+.4f}  "
                  f"boot p5 net {st['p5_net']:+.4f} (gross {st['p5_gross']:+.4f})  "
                  f"t net {st['t_net']:+.2f} (gross {st['t_gross']:+.2f})  win {st['win']:.3f}")
            print(f"         rule-3 lower bounds at 0.05/{N}: normal {st['lb_normal']:+.4f}  "
                  f"day-bootstrap {st['lb_boot']:+.4f} ({st['draws']} draws)  exits {st['why']}")
            by = t.assign(y=pd.to_datetime(t.date).dt.year).groupby("y").net_R.agg(["size", "mean"])
            print("         net R by year: " + "  ".join(f"{y}:{r['mean']:+.3f}({int(r['size'])})"
                                                      for y, r in by.iterrows()))
            t.to_csv(SCR / f"trades_{name[:2]}_{mode}.csv", index=False)
    print("\n=== decision rule (prereg): D2 net lower bound at 0.05/N > 0 AND D3 net mean same sign "
          "AND D1 gross mean > 0; the WORSE of H0012/H0017 governs")
    verdicts = {}
    for mode in ("H0012", "H0017"):
        d1, d2, d3 = (summary[(k, mode)] for k in ("D1", "D2", "D3"))
        lb = min(d2["lb_normal"], d2["lb_boot"])
        c1, c2, c3 = lb > 0, np.sign(d3["net"]) == np.sign(d2["net"]) and d3["net"] != 0, d1["gross"] > 0
        verdicts[mode] = c1 and c2 and c3
        print(f"  {mode}: D2 net LB {lb:+.4f} > 0? {c1} | D3 net {d3['net']:+.4f} same sign as D2 net "
              f"{d2['net']:+.4f}? {c2} | D1 gross {d1['gross']:+.4f} > 0? {c3} -> {'PASS' if verdicts[mode] else 'FAIL'}")
    print(f"  governing (worse of the two): {'PASS' if all(verdicts.values()) else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
