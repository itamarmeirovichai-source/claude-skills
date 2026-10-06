#!/usr/bin/env python3
"""H0022 (low-turnover intraday VWAP trend: H0021 rules with decisions every 30 minutes), run
as pre-registered in agents/ledger.csv. Built from vwap-H0021/vwap.py; the ONLY rule change is
the decision cadence (positions()/stream_day() below). Nothing tuned after seeing results.

Rule (as registered):
  identical to H0021: session = weekday with RTH bars 09:30-15:59 NY; VWAP from 09:30 =
    cumsum((h+l+c)/3 * v) / cumsum(v); position changes execute at the NEXT bar's open; flat at
    the session's last bar close; no stops/targets/filters; size 1; cost per unit traded
    (flip = 2, open or close = 1): NQ 0.375 index pt, SPY 0.5 bp of price
  EXCEPT: desired position is evaluated ONLY at the closes of the 09:59, 10:29, ..., 15:29 bars
    (12 decisions): +1 if close > VWAP, -1 if close < VWAP, unchanged if equal (flat before
    the first non-equal decision). If a decision bar is missing, use the last existing bar
    before it in that half hour (09:30-09:59, 10:00-10:29, ..., 15:00-15:29), else skip that
    decision. Held until the next decision or the flat exit.
  unit = net daily return in bp = day's P&L / that day's first entry price
  DECISIVE = NQ 1m 2020-09..2025-11 ex roll weeks (seen in H0021);
  UNSEEN = SPXUSD 1m 2010-11..2018-12 (FutureSharks, no volume) with session TWAP (running mean
    of typical price, i.e. VWAP with v = 1) and cost 0.5 bp of price per unit;
  corroboration = SPY 1m RTH 2019-01..2025-07
  PASS only if NQ net daily mean > 0 with one-sided t >= z(0.05/N) at N = 200
  AND SPXUSD-TWAP net daily mean > 0 AND SPY net daily mean > 0.

Implementation choices fixed BEFORE any result was computed (also in the report). All of
H0021's choices carry over unchanged; the H0022-specific ones are:
  * half-hour slot of a bar = (minutes since 09:30) // 30 for bars 09:30..15:29 (slots 0..11);
    bars 15:30..15:59 are in no slot. The decision bar of a slot = the last bar of that slot
    that exists in the session (= the :59/:29 bar when present). A slot with no bar = skipped.
    "Last existing bar of the slot" is known in real time when the next bar arrives (its
    timestamp is outside the slot) or the session ends, and the decision is acted on at
    exactly that next bar's open, so no future price is used.
  * a decision bar that is the session's last bar (half days) is never acted on (flat exit).
  * SPXUSD: no roll exclusion (cash-index CFD); volume column is all 0 in the file, so v = 1.
H0021's choices:
  * session = weekday with >= 1 bar in 09:30..15:59 NY (same as orb-H0020). VWAP uses those
    RTH bars only, starting from the first bar of the session.
  * "next bar" = the next bar that exists in the session file (1m gaps are not filled).
  * flat at the close of the session's LAST bar (15:59 normally; earlier on half days or
    when the 15:59 bar is missing). The signal of that last bar is never acted on; the
    signal of every earlier bar is acted on at the following bar's open. Sessions whose
    last bar is not 15:59 are counted in the output.
  * if cumulative volume is 0 at a bar, VWAP is undefined and the bar's signal is treated
    as "equal" (position unchanged). Counted in the output.
  * P&L in price units per 1 unit: sum over bars of pos * (next fill price - this bar open),
    i.e. mark-to-market open-to-open, last bar open-to-close. Cost at the price of each fill
    (bar open, or last close for the final flatten). NQ cost is fixed 0.375 pt per unit.
  * a session with no position at all scores 0 bp and 0 units and stays in the sample.
  * NQ: roll-week days (roll_excluded, from gapfade-H0012) are never traded and dropped.
  * t = mean / (sd/sqrt(n)), one-sided. Bootstrap p5 = 5th percentile of the mean over
    10,000 iid resamples of days, seed 0. Sharpe = mean/sd * sqrt(252). Max drawdown =
    largest peak-to-trough fall of the running SUM of net daily bp (no compounding).
  * NQ post-publication subsample = dates >= 2023-11-01. Cost x2 = both cost rates doubled.
  * future-truncation test: (a) 250 random days per dataset (seed 0): for every bar k,
    rerun the vectorized positions on that day's bars[:k] and require the positions of
    bars [:k] to be identical; (b) full check: an independent bar-by-bar streaming loop
    (sees only past bars, cash accounting) must reproduce the vectorized position of every
    bar and the daily gross/net P&L of every session.

    CLAUDE_SCRATCH=<dir with intraday/ and spx/> python3 -I vwap30.py > run.txt
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

FLEET = HERE.parents[2]                      # skills/prop-fleet
_spec = importlib.util.spec_from_file_location(
    "ledger_gate", FLEET / "agents/daily/2026-10-05/eng_head/ledger_gate.py")
lg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lg)

NQ_COST_PTS = 0.375
SPY_COST_FRAC = 0.5e-4
SPX_COST_FRAC = 0.5e-4
DECISION_HM = (959, 1029, 1059, 1129, 1159, 1229, 1259, 1329, 1359, 1429, 1459, 1529)
POST_PUB = dt.date(2023, 11, 1)
TRUNC_DAYS = 250
BIG = np.iinfo(np.int64).max


# ── vectorized core (all sessions at once; `starts` = index of each session's first bar) ──
def seg_cumsum(x: np.ndarray, starts: np.ndarray) -> np.ndarray:
    out = np.empty_like(x)
    ends = np.append(starts[1:], x.size)
    for s, e in zip(starts, ends):          # per-session cumsum: no float carry across days
        out[s:e] = np.cumsum(x[s:e])
    return out


def slot_of(hm) -> np.ndarray:
    """Half-hour decision slot 0..11 for bars 09:30..15:29 (slot k ends at DECISION_HM[k]);
    -1 outside (15:30..15:59)."""
    hm = np.asarray(hm, int)
    mins = (hm // 100) * 60 + hm % 100 - 570
    return np.where((mins >= 0) & (mins < 360), mins // 30, -1)


def decision_bars(hm, starts) -> np.ndarray:
    """True on the last existing bar of each half-hour slot within each session."""
    n = len(hm)
    s = slot_of(hm)
    nxt_s = np.empty(n, int)
    nxt_s[:-1] = s[1:]
    nxt_s[-1] = -2
    ends = np.append(starts[1:], n)
    nxt_s[ends - 1] = -2                       # session end closes the slot
    return (s >= 0) & (nxt_s != s)


def positions(h, l, c, v, starts, hm):
    """Returns (vwap, signal, desired, pos). signal is computed at every bar (as H0021) but
    desired only changes at decision bars. pos[i] = position HELD during bar i (entered at
    bar i's open) = desired after bar i-1's close, 0 on a session's first bar."""
    n = c.size
    is_start = np.zeros(n, bool)
    is_start[starts] = True
    is_dec = decision_bars(hm, starts)
    tp = (h + l + c) / 3.0
    cpv = seg_cumsum(tp * v, starts)
    cv = seg_cumsum(v, starts)
    with np.errstate(invalid="ignore", divide="ignore"):
        vwap = np.where(cv > 0, cpv / cv, np.nan)
    sig = np.sign(c - vwap)
    sig = np.where(np.isnan(sig), 0.0, sig)
    val = np.where(is_dec, sig, 0.0)
    anchor = (is_dec & (sig != 0)) | is_start
    idx = np.maximum.accumulate(np.where(anchor, np.arange(n), 0))
    desired = val[idx]                      # forward-filled within session; 0 before first decision
    pos = np.empty(n)
    pos[0] = 0.0
    pos[1:] = desired[:-1]
    pos[is_start] = 0.0
    return vwap, sig, desired, pos


def daily_pnl(o, c, pos, starts, cost_fn):
    """Per session: gross P&L (price units), cost (price units), units traded, first entry px."""
    n = o.size
    ends = np.append(starts[1:], n)
    is_last = np.zeros(n, bool)
    is_last[ends - 1] = True
    is_start = np.zeros(n, bool)
    is_start[starts] = True
    nxt = np.empty(n)
    nxt[:-1] = o[1:]
    nxt[is_last] = c[is_last]
    gross_bar = pos * (nxt - o)
    prev = np.empty(n)
    prev[0] = 0.0
    prev[1:] = pos[:-1]
    prev[is_start] = 0.0
    u_open = np.abs(pos - prev)
    u_close = np.where(is_last, np.abs(pos), 0.0)
    cost_bar = u_open * cost_fn(o) + u_close * cost_fn(c)
    first = np.minimum.reduceat(np.where(pos != 0, np.arange(n), BIG), starts)
    entry = np.where(first < BIG, o[np.minimum(first, n - 1)], np.nan)
    return (np.add.reduceat(gross_bar, starts), np.add.reduceat(cost_bar, starts),
            np.add.reduceat(u_open + u_close, starts), entry)


# ── independent streaming reference (one bar at a time, past data only) ───────
def stream_day(o, h, l, c, v, hm, cost_fn):
    """Sees bar i's timestamp at its open and bar i's prices only at its close."""
    cpv = cv = 0.0
    desired = 0.0
    last_sig = 0.0
    prev_slot = -1
    held = 0.0
    cash = cost = units = 0.0
    entry = np.nan
    pos_out = []
    for i in range(o.size):
        k = (hm[i] // 100) * 60 + hm[i] % 100 - 570
        slot = k // 30 if 0 <= k < 360 else -1
        if i > 0 and prev_slot >= 0 and slot != prev_slot:
            if last_sig != 0:                    # previous bar closed its half hour: decide
                desired = last_sig
        new = desired if i > 0 else 0.0
        if new != held:                          # trade at this bar's open
            u = abs(new - held)
            cash -= (new - held) * o[i]
            cost += u * cost_fn(np.array(o[i]))
            units += u
            if np.isnan(entry):
                entry = o[i]
            held = new
        pos_out.append(held)
        cpv += (h[i] + l[i] + c[i]) / 3.0 * v[i]
        cv += v[i]
        last_sig = 0.0
        if cv > 0:
            vw = cpv / cv
            if c[i] > vw:
                last_sig = 1.0
            elif c[i] < vw:
                last_sig = -1.0
        prev_slot = slot
    if held != 0:                                # flat at the last bar's close
        cash += held * c[-1]
        cost += abs(held) * cost_fn(np.array(c[-1]))
        units += abs(held)
    return np.array(pos_out), cash, cost, units, entry


# ── data prep ────────────────────────────────────────────────────────────────
def prep(r: pd.DataFrame):
    r = r.sort_index()
    d = r["date"].to_numpy()
    starts = np.flatnonzero(np.r_[True, d[1:] != d[:-1]])
    arr = {k: r[k].to_numpy(float) for k in "ohlcv"}
    arr["hm"] = r["hm"].to_numpy(int)
    return r, arr, starts


def run(r: pd.DataFrame, cost_fn):
    r, a, starts = prep(r)
    vwap, sig, desired, pos = positions(a["h"], a["l"], a["c"], a["v"], starts, a["hm"])
    g, cst, units, entry = daily_pnl(a["o"], a["c"], pos, starts, cost_fn)
    dates = r["date"].to_numpy()[starts]
    with np.errstate(invalid="ignore"):
        gbp = np.where(np.isnan(entry), 0.0, g / entry * 1e4)
        nbp = np.where(np.isnan(entry), 0.0, (g - cst) / entry * 1e4)
        cbp = np.where(np.isnan(entry), 0.0, cst / entry * 1e4)
    day = pd.DataFrame(dict(date=dates, gross=gbp, net=nbp, cost=cbp, units=units,
                            gross_pts=g, cost_pts=cst, entry=entry))
    is_dec = decision_bars(a["hm"], starts)
    hm = a["hm"]
    diag = dict(nan_vwap=int(np.isnan(vwap).sum()), eq_sig=int(((sig == 0) & ~np.isnan(vwap)).sum()),
                bars=int(pos.size), decisions=int(is_dec.sum()),
                fallback=int((is_dec & ~np.isin(hm, DECISION_HM)).sum()),
                skipped=int(starts.size * len(DECISION_HM) - is_dec.sum()),
                dec_eq=int((is_dec & (sig == 0)).sum()),
                dec_last=int(is_dec[np.append(starts[1:], pos.size) - 1].sum()))
    return day, pos, r, a, starts, diag


# ── tests on the real data ───────────────────────────────────────────────────
def truncation_test(a, starts, pos, n_days, seed=0):
    rng = np.random.default_rng(seed)
    ends = np.append(starts[1:], pos.size)
    pick = rng.choice(starts.size, size=min(n_days, starts.size), replace=False)
    bars = 0
    for j in pick:
        s, e = starts[j], ends[j]
        for k in range(1, e - s + 1):
            sl = slice(s, s + k)
            _, _, _, p = positions(a["h"][sl], a["l"][sl], a["c"][sl], a["v"][sl], np.array([0]),
                                   a["hm"][sl])
            assert np.array_equal(p, pos[sl]), (j, k)
            bars += 1
    return pick.size, bars


def full_stream_check(a, starts, pos, day, cost_fn):
    ends = np.append(starts[1:], pos.size)
    worst = 0.0
    for j, (s, e) in enumerate(zip(starts, ends)):
        sl = slice(s, e)
        p, cash, cost, units, entry = stream_day(a["o"][sl], a["h"][sl], a["l"][sl], a["c"][sl],
                                                 a["v"][sl], a["hm"][sl], cost_fn)
        assert np.array_equal(p, pos[sl]), j
        assert units == day.units.iat[j], j
        assert (np.isnan(entry) and np.isnan(day.entry.iat[j])) or entry == day.entry.iat[j], j
        worst = max(worst, abs(cash - day.gross_pts.iat[j]), abs(cost - day.cost_pts.iat[j]))
    assert worst < 1e-6, worst
    return starts.size, worst


# ── statistics ───────────────────────────────────────────────────────────────
def boot_p5(x: np.ndarray, draws=10_000, seed=0) -> float:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(draws, x.size))
    return float(np.quantile(x[idx].mean(1), 0.05))


def tstat(x):
    return x.mean() / (x.std(ddof=1) / np.sqrt(x.size))


def stats(day: pd.DataFrame) -> dict:
    g, n = day.gross.to_numpy(), day.net.to_numpy()
    cum = np.cumsum(n)
    dd = float((np.maximum.accumulate(np.r_[0.0, cum]) - np.r_[0.0, cum]).max())
    return dict(n=n.size, units=day.units.mean(), gross=g.mean(), net=n.mean(), cost=day.cost.mean(),
                t_net=tstat(n), t_gross=tstat(g), p5_net=boot_p5(n), p5_gross=boot_p5(g),
                win=(n > 0).mean(), sharpe=n.mean() / n.std(ddof=1) * np.sqrt(252),
                maxdd=dd, worst=n.min(), worst_date=day.date.iat[int(n.argmin())],
                flat_days=int((day.units == 0).sum()))


def show(label: str, st: dict) -> None:
    print(f"  {label}: days {st['n']}  units/day {st['units']:.2f}  mean bp/day gross {st['gross']:+.3f}  "
          f"net {st['net']:+.3f}  (cost {st['cost']:.3f})  t net {st['t_net']:+.2f} (gross {st['t_gross']:+.2f})")
    print(f"      boot p5 net {st['p5_net']:+.3f} (gross {st['p5_gross']:+.3f})  win {st['win']:.3f}  "
          f"Sharpe net {st['sharpe']:+.2f}  max DD {st['maxdd']:.1f} bp  worst day {st['worst']:+.1f} bp "
          f"({st['worst_date']})  days with no position {st['flat_days']}")


def year_table(day: pd.DataFrame) -> None:
    y = day.assign(y=pd.to_datetime(day.date).dt.year).groupby("y")
    print("      year     n  units/day   gross bp    net bp   t net    win   Sharpe")
    for yr, d in y:
        n = d.net.to_numpy()
        print(f"      {yr}  {len(d):4d}  {d.units.mean():9.2f}  {d.gross.mean():+9.3f}  {n.mean():+8.3f}  "
              f"{tstat(n):+6.2f}  {(n > 0).mean():.3f}  {n.mean() / n.std(ddof=1) * np.sqrt(252):+6.2f}")


def main() -> int:
    import loaders as L
    N = lg.ledger_n(FLEET / "agents/ledger.csv")
    assert N == 200, N
    alpha, Z = lg.alpha_z(N)
    print(f"ledger N = {N}; one-sided alpha = 0.05/{N} = {alpha:.3e}; bar z = {Z:.4f}")
    costs = {"NQ": lambda p: np.full(np.shape(p), NQ_COST_PTS), "SPY": lambda p: SPY_COST_FRAC * p,
             "SPX": lambda p: SPX_COST_FRAC * p}
    costs2 = {"NQ": lambda p: np.full(np.shape(p), 2 * NQ_COST_PTS), "SPY": lambda p: 2 * SPY_COST_FRAC * p,
              "SPX": lambda p: 2 * SPX_COST_FRAC * p}
    summary = {}
    for key, name, loader, roll in (("NQ", "NQ 1m 2020-09..2025-11 ex roll weeks (DECISIVE)", L.load_nq, True),
                                    ("SPX", "SPXUSD 1m 2010-11..2018-12, session TWAP (UNSEEN)", L.load_spx, False),
                                    ("SPY", "SPY 1m RTH 2019-01..2025-07", L.load_spy, False)):
        raw = L.rth(loader())
        days = sorted(set(raw.date))
        excluded = L.roll_excluded(days) if roll else set()
        r = raw[~raw.date.isin(excluded)]
        years = (pd.Timestamp(days[-1]) - pd.Timestamp(days[0])).days / 365.25
        day, pos, r, a, starts, diag = run(r, costs[key])
        last_hm = r["hm"].to_numpy()[np.append(starts[1:], len(r)) - 1]
        first_hm = r["hm"].to_numpy()[starts]
        print(f"\n=== {name}: sessions {len(days)} ({days[0]}..{days[-1]}, {years:.2f} yr), "
              f"roll-excluded {len(days) - starts.size}, used {starts.size}")
        print(f"    bars {diag['bars']}  bars/session {diag['bars'] / starts.size:.1f}  sessions not starting 09:30 "
              f"{int((first_hm != 930).sum())}  sessions whose last bar is not 15:59 {int((last_hm != 1559).sum())}  "
              f"zero-volume bars {int((a['v'] == 0).sum())}  bars with undefined VWAP {diag['nan_vwap']}  "
              f"bars with close == VWAP {diag['eq_sig']}")
        print(f"    decisions {diag['decisions']} ({diag['decisions'] / starts.size:.2f}/session)  using fallback bar "
              f"(decision bar missing) {diag['fallback']}  skipped (no bar in the half hour) {diag['skipped']}  "
              f"decision with close == VWAP {diag['dec_eq']}  decision on the session's last bar (not acted) "
              f"{diag['dec_last']}")
        nd, nb = truncation_test(a, starts, pos, TRUNC_DAYS)
        print(f"    future-truncation test (a): {nd} random sessions, {nb} truncation points (every bar), "
              f"positions identical")
        ns, worst = full_stream_check(a, starts, pos, day, costs[key])
        print(f"    future-truncation test (b): streaming bar-by-bar loop reproduces every bar's position and "
              f"units in all {ns} sessions; max |P&L diff| {worst:.2e} price units")
        st = stats(day)
        summary[key] = st
        show("all", st)
        year_table(day)
        d2, *_ = run(r, costs2[key])
        s2 = stats(d2)
        show("cost x2", s2)
        summary[key + "_x2"] = s2
        if key == "NQ":
            sub = day[day.date >= POST_PUB]
            print(f"    post-publication subsample (dates >= {POST_PUB}):")
            show("2023-11+", stats(sub))
            show("2023-11+ cost x2", stats(d2[d2.date >= POST_PUB]))
            print(f"    avg first entry price {day.entry.mean():.1f} pts; cost/unit {NQ_COST_PTS} pt = "
                  f"{(NQ_COST_PTS / day.entry).mean() * 1e4:.3f} bp; avg gross {day.gross_pts.mean():+.2f} pts/day, "
                  f"avg cost {day.cost_pts.mean():.2f} pts/day")
    nq, spx, spy = summary["NQ"], summary["SPX"], summary["SPY"]
    c1 = nq["net"] > 0 and nq["t_net"] >= Z
    c2 = spx["net"] > 0
    c3 = spy["net"] > 0
    print(f"\n=== decision rule (prereg): NQ net mean > 0 with one-sided t >= {Z:.4f}: "
          f"net {nq['net']:+.3f} bp, t {nq['t_net']:+.2f} -> {c1} | SPXUSD-TWAP net mean > 0: {spx['net']:+.3f} bp "
          f"-> {c2} | SPY net mean > 0: {spy['net']:+.3f} bp -> {c3} => {'PASS' if c1 and c2 and c3 else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
