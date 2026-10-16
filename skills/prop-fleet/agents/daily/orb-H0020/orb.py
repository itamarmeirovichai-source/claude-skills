#!/usr/bin/env python3
"""H0020 (5-minute opening range breakout, Zarattini & Aziz 2023), run as pre-registered
in agents/ledger.csv. Nothing here is tuned after seeing results; no filters added.

Rule (as registered):
  first 5-min bar = 1m bars 09:30..09:34 NY, all five must exist (else skip the day)
  direction = long if its close > its open, short if close < open, none if equal
  entry = open of the 09:35 1m bar
  stop  = low of the first 5-min bar (long) / high (short); R = |entry - stop|; skip if R <= 0
  target = entry +/- 10R
  exit at stop, target, or the close of the last bar at or before 15:59, whichever first;
  stop first if one bar touches both; a bar that gaps past the stop fills at its open
  one trade a day, no filters, no sizing; cost = 2 bp of entry round trip, in R
  DECISIVE = NQ 1m 2020-2025 ex roll weeks; SPY 1m RTH 2019-01..2025-07; SPXUSD 1m 2010-2018
  PASS only if NQ net mean R > 0 with one-sided t >= z(0.05/N) at N = 198,
  AND SPY net mean R > 0, AND SPXUSD gross mean R > 0.

Implementation choices fixed BEFORE any result was computed (also in the report):
  * "session" = weekday with at least one bar in 09:30..15:59 NY (as gapfade.py / gamma.py).
  * the 09:35 bar must exist (entry = its open); if missing, no trade.
  * the path that can exit the trade = bars 09:35..15:59 of the day, starting with the
    entry bar itself (its high/low come after its open).
  * stop fill: long = min(stop, bar open), short = max(stop, bar open). So if the 09:35
    open is already beyond the stop (R > 0 but on the wrong side) the trade is taken and
    exits at that open (gross 0R, net = -cost). These days are counted in the output.
  * target fill = the target price (no price improvement on a gap through the target).
  * cost in R = 0.0002 * entry / R.
  * NQ: roll-week days (roll_excluded, from gapfade-H0012) are never traded.
  * t = mean / (sd/sqrt(n)), one-sided. Bootstrap p5 = 5th percentile of the mean over
    10,000 iid resamples, seed 0. trades/yr = trades / calendar span of the sessions.
  * NQ post-publication subsample = trade dates >= 2023-05-01.

    CLAUDE_SCRATCH=<dir with spx/, intraday/> python3 -I orb.py > run.txt
Data are read from $CLAUDE_SCRATCH (never committed).
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import loaders as L  # noqa: E402

FLEET = HERE.parents[2]                      # skills/prop-fleet
_spec = importlib.util.spec_from_file_location(
    "ledger_gate", FLEET / "agents/daily/2026-10-05/eng_head/ledger_gate.py")
lg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lg)

COST = 0.0002
TARGET_R = 10.0
POST_PUB = dt.date(2023, 5, 1)


def signal(g: pd.DataFrame):
    """Ex-ante part, from bars <= 09:35 only. Returns (side, entry, stop, R) or None."""
    first = [L._bar(g, hm) for hm in (930, 931, 932, 933, 934)]
    if any(b is None for b in first):
        return None
    o5, c5 = first[0].o, first[-1].c
    hi5 = max(b.h for b in first)
    lo5 = min(b.l for b in first)
    if c5 > o5:
        side, stop = 1, lo5
    elif c5 < o5:
        side, stop = -1, hi5
    else:
        return None
    b935 = L._bar(g, 935)
    if b935 is None:
        return None
    entry = float(b935.o)
    r = abs(entry - stop)
    if not r > 0:
        return None
    return side, entry, float(stop), float(r)


def simulate(path: pd.DataFrame, side: int, entry: float, stop: float, r: float):
    """path = o,h,l,c bars from the entry bar on. Returns (exit price, why)."""
    tgt = entry + side * TARGET_R * r
    for o, h, l, c in path[["o", "h", "l", "c"]].itertuples(index=False):
        hit_stop = l <= stop if side > 0 else h >= stop
        hit_tgt = h >= tgt if side > 0 else l <= tgt
        if hit_stop:
            return (min(stop, o) if side > 0 else max(stop, o)), "stop"
        if hit_tgt:
            return tgt, "target"
    return float(path.c.iloc[-1]), "close"


def trade_day(g: pd.DataFrame):
    s = signal(g)
    if s is None:
        return None
    side, entry, stop, r = s
    path = g[(g.hm >= 935) & (g.hm <= 1559)]
    px, why = simulate(path, side, entry, stop, r)
    return side, entry, stop, r, px, why


def run(S: dict, excluded: set) -> pd.DataFrame:
    out = []
    for d, g in S.items():
        if d in excluded:
            continue
        res = trade_day(g)
        if res is None:
            continue
        side, entry, stop, r, px, why = res
        gross = side * (px - entry)
        out.append(dict(date=d, side=side, entry=entry, stop=stop, r=r, exit=px, why=why,
                        wrong_side=side * (entry - stop) < 0,
                        gross_R=gross / r, net_R=(gross - COST * entry) / r))
    return pd.DataFrame(out)


def truncation_test(S: dict, excluded: set) -> int:
    """For every tradeable day: deleting the bars after 09:35 must not change
    whether the day trades, its direction, entry or stop."""
    n = 0
    for d, g in S.items():
        if d in excluded:
            continue
        a, b = signal(g), signal(g[g.hm <= 935].copy())
        assert a == b, (d, a, b)
        n += 1
    return n


def boot_p5(x: np.ndarray, draws=10_000, seed=0) -> float:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(draws, x.size))
    return float(np.quantile(x[idx].mean(1), 0.05))


def stats(t: pd.DataFrame, years: float) -> dict:
    g, n_ = t.gross_R.to_numpy(), t.net_R.to_numpy()
    n = n_.size
    return dict(n=n, per_yr=n / years, gross=g.mean(), net=n_.mean(),
                t_net=n_.mean() / (n_.std(ddof=1) / np.sqrt(n)),
                t_gross=g.mean() / (g.std(ddof=1) / np.sqrt(n)),
                p5_net=boot_p5(n_), p5_gross=boot_p5(g),
                win=(n_ > 0).mean(), r_pts=t.r.mean(), r_bp=(t.r / t.entry).mean() * 1e4,
                cost_R=(COST * t.entry / t.r).mean(), long=(t.side > 0).mean(),
                why=t.why.value_counts().to_dict(), wrong=int(t.wrong_side.sum()))


def show(label: str, st: dict) -> None:
    print(f"  {label}: trades {st['n']}  trades/yr {st['per_yr']:.1f}  mean R gross {st['gross']:+.4f}  "
          f"net {st['net']:+.4f}  t net {st['t_net']:+.2f} (gross {st['t_gross']:+.2f})  "
          f"boot p5 net {st['p5_net']:+.4f} (gross {st['p5_gross']:+.4f})  win {st['win']:.3f}")
    print(f"      avg R size {st['r_pts']:.3f} pts ({st['r_bp']:.1f} bp of entry)  avg cost {st['cost_R']:.4f} R  "
          f"long share {st['long']:.3f}  exits {st['why']}  entry already beyond stop: {st['wrong']}")


def year_table(t: pd.DataFrame) -> None:
    y = t.assign(y=pd.to_datetime(t.date).dt.year).groupby("y")
    tab = pd.DataFrame({"n": y.size(), "gross": y.gross_R.mean(), "net": y.net_R.mean(),
                        "win": y.net_R.apply(lambda s: (s > 0).mean()),
                        "R_pts": y.r.mean()})
    print("      year     n    gross R    net R    win   avg R pts")
    for yr, r in tab.iterrows():
        print(f"      {yr}  {int(r.n):4d}  {r.gross:+8.4f}  {r.net:+8.4f}  {r.win:.3f}  {r.R_pts:9.3f}")


def main() -> int:
    N = lg.ledger_n(FLEET / "agents/ledger.csv")
    assert N == 198, N
    alpha, Z = lg.alpha_z(N)
    print(f"ledger N = {N}; one-sided alpha = 0.05/{N} = {alpha:.3e}; bar z = {Z:.4f}")
    summary = {}
    for key, name, loader, roll in (("NQ", "NQ 1m 2020-2025 ex roll weeks (DECISIVE)", L.load_d3, True),
                                    ("SPY", "SPY 1m RTH 2019-01..2025-07", L.load_d2, False),
                                    ("SPX", "SPXUSD 1m 2010-2018", L.load_d1, False)):
        S = L.sessions(loader())
        days = list(S)
        excluded = L.roll_excluded(days) if roll else set()
        years = (pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25
        live = [d for d in days if d not in excluded]
        miss5 = sum(any(L._bar(S[d], hm) is None for hm in range(930, 935)) for d in live)
        miss935 = sum(L._bar(S[d], 935) is None for d in live)
        print(f"\n=== {name}: sessions {len(days)} ({days[0]}..{days[-1]}, {years:.2f} yr), "
              f"roll-excluded {len(days) - len(live)}, missing a 09:30-09:34 bar {miss5}, missing 09:35 bar {miss935}")
        print(f"    future-truncation test (every non-excluded day, bars after 09:35 removed): "
              f"{truncation_test(S, excluded)} days identical")
        t = run(S, excluded)
        st = stats(t, years)
        summary[key] = st
        show("all", st)
        year_table(t)
        if key == "NQ":
            sub = t[t.date >= POST_PUB]
            sy = (pd.Timestamp(days[-1]) - pd.Timestamp(POST_PUB)).days / 365.25
            print(f"    post-publication subsample (trade dates >= {POST_PUB}, {sy:.2f} yr):")
            show("2023-05+", stats(sub, sy))
    nq, spy, spx = summary["NQ"], summary["SPY"], summary["SPX"]
    c1 = nq["net"] > 0 and nq["t_net"] >= Z
    c2 = spy["net"] > 0
    c3 = spx["gross"] > 0
    print(f"\n=== decision rule (prereg): NQ net mean R > 0 with one-sided t >= {Z:.4f}: "
          f"net {nq['net']:+.4f}, t {nq['t_net']:+.2f} -> {c1} | SPY net mean R > 0: {spy['net']:+.4f} -> {c2} | "
          f"SPXUSD gross mean R > 0: {spx['gross']:+.4f} -> {c3} => {'PASS' if c1 and c2 and c3 else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
