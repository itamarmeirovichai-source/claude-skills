#!/usr/bin/env python3
"""E2 backtest: scheduled macro events, intraday ES/NQ (SPY proxy), wave 2.

Implements agents/prereg/E2_rules.md exactly (pre-registered in commit d489ea8, before this
file existed). Variants E2-01..E2-12; IS = SPXUSD 2010-11..2018-12 (FOMC days before
2013-03-20 dropped); OOS = SPY 2019-01..2025-07 + NQ 2020-09..2025-11 pooled by event day.

    export CLAUDE_SCRATCH=...   # data from daily/2026-10-04/data_fetch.py + FutureSharks SPXUSD
    python3 events_bt.py > run.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import loaders as L

HERE = Path(__file__).resolve().parent
BAR = 3.5603
COST = {"SPX": 0.30, "SPY": 0.030, "NQ": 0.375}    # per side, price units (1 tick + $2.50)
SIX = {"FOMC", "CPI", "NFP", "PCE", "RETAIL", "ISM"}
RTH_EVENTS = {"FOMC", "FOMC_MINUTES", "ISM"}
IS_FOMC_FROM = pd.Timestamp("2013-03-20").date()
VARIANTS = [f"E2-{i:02d}" for i in range(1, 13)]


def mins(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# ── calendar ─────────────────────────────────────────────────────────────────
def calendar():
    ev = pd.read_csv(HERE / "events.csv", parse_dates=["date"])
    ev = ev[ev.scheduled.astype(str) == "True"].copy()
    ev["d"] = ev.date.dt.date
    ev["t"] = ev.time_et.map(mins)
    kinds = ev.groupby("d").event.apply(set).to_dict()
    fomc_t = {r.d: r.t for r in ev[ev.event == "FOMC"].itertuples()}
    black = {}
    for r in ev[ev.event.isin(RTH_EVENTS)].itertuples():
        if 9 * 60 + 30 <= r.t <= 16 * 60:
            black.setdefault(r.d, []).append(r.t)
    return kinds, fomc_t, black


# ── per-session arrays ───────────────────────────────────────────────────────
class Day:
    __slots__ = ("d", "mn", "o", "h", "l", "c", "pc", "adj")

    def __init__(self, d, g, pc, adj):
        self.d = d
        self.mn = (g.index.hour * 60 + g.index.minute).to_numpy()
        self.o, self.h, self.l, self.c = (g[k].to_numpy() for k in ("o", "h", "l", "c"))
        self.pc, self.adj = pc, adj

    def truncated(self, upto: int) -> "Day":
        k = int(np.searchsorted(self.mn, upto, side="right"))
        t = object.__new__(Day)
        t.d, t.pc, t.adj = self.d, self.pc, self.adj
        t.mn, t.o, t.h, t.l, t.c = self.mn[:k], self.o[:k], self.h[:k], self.l[:k], self.c[:k]
        return t

    def c_at(self, m):
        """close of the last bar at or before minute m (signal bar rule)"""
        k = int(np.searchsorted(self.mn, m, side="right")) - 1
        return None if k < 0 else self.c[k]

    def o_entry(self, m):
        """open of the first bar in [m, m+3] (entry rule) -> (minute, price) or None"""
        k = int(np.searchsorted(self.mn, m, side="left"))
        if k < len(self.mn) and self.mn[k] <= m + 3:
            return int(self.mn[k]), self.o[k]
        return None


def build_days(name: str):
    raw = {"SPX": L.load_spx, "SPY": L.load_spy, "NQ": L.load_nq}[name]()
    r = L.rth(raw)
    adj = {}
    if name == "NQ":    # 00:00-bar jump (front-month switch sits there; ~0 otherwise)
        t = raw.index
        prevc = raw.c.shift(1)
        mid = raw[(t.hour == 0) & (t.minute == 0)]
        pcm = prevc.loc[mid.index]
        for ts, o0, p0 in zip(mid.index, mid.o, pcm):
            if np.isfinite(p0):
                adj[ts.date()] = np.log(o0 / p0)
    days, pc = [], None
    for d, g in r.groupby("date", sort=True):
        if pc is not None:
            days.append(Day(d, g, pc, adj.get(d, 0.0)))
        pc = g.c.iloc[-1]
    return days


# ── decisions (use only bars up to the entry minute) ─────────────────────────
def decide(v: str, day: Day, kinds, fomc_t, delay: int = 0, rng20=None):
    """-> list of (side, entry_minute, entry_price, exit_cap_minute_or_None)"""
    k = kinds.get(day.d, set())
    out = []

    def enter(side, m, cap=None):
        if side == 0:
            return
        e = day.o_entry(m + delay)
        if e is not None:
            out.append((int(side), e[0], e[1], cap))

    if v in ("E2-01", "E2-02", "E2-03", "E2-04", "E2-05") and day.d in fomc_t:
        T = fomc_t[day.d]
        if v == "E2-05":
            enter(1, 9 * 60 + 30)
        else:
            N = {"E2-01": 15, "E2-02": 5, "E2-03": 30, "E2-04": 15}[v]
            if day.o_entry(T + N + delay) is None:
                return out
            a, b = day.c_at(T - 1), day.c_at(T + N - 1)
            if a is None or b is None:
                return out
            s = np.sign(b - a) * (-1 if v == "E2-04" else 1)
            enter(s, T + N)
    elif v in ("E2-06", "E2-07") and k & {"CPI", "NFP"}:
        e = day.o_entry(9 * 60 + 30)
        if e is None or e[0] != 9 * 60 + 30:
            return out
        g = np.log(e[1] / day.pc) - day.adj
        s = np.sign(g) * (-1 if v == "E2-07" else 1)
        enter(s, 9 * 60 + 31)
    elif v in ("E2-08", "E2-09", "E2-10", "E2-11"):
        is_ev = bool(k & SIX)
        if (v == "E2-10") == is_ev:
            return out
        c959 = day.c_at(9 * 60 + 59)
        if c959 is None:
            return out
        s = np.sign(np.log(c959 / day.pc) - day.adj)
        if v == "E2-11":
            if rng20 is None or not np.isfinite(rng20):
                return out
            w = day.mn <= 9 * 60 + 59
            e0 = day.o_entry(9 * 60 + 30)
            if e0 is None or e0[0] != 9 * 60 + 30 or not w.any():
                return out
            rg = (day.h[w].max() - day.l[w].min()) / e0[1]
            if not rg > rng20:
                return out
        enter(s, 15 * 60 + 30 if v == "E2-09" else 10 * 60 + 3)
    return out


def exit_trade(day: Day, side, em, ep, black, cost):
    """close at last bar <= 15:59, or at close of bar T-3 for a Tier-1 event inside the hold."""
    cap = 15 * 60 + 59
    for T in black.get(day.d, []):
        assert not (T - 2 <= em <= T + 2), (day.d, em, T)
        if em < T - 2:
            cap = min(cap, T - 3)
    k = int(np.searchsorted(day.mn, cap, side="right")) - 1
    if k < 0 or day.mn[k] < em:
        return None
    xp = day.c[k]
    return side * (xp - ep) / ep * 1e4 - 2 * cost / ep * 1e4


def exit_e205(day: Day, fomc_t, cost, ep, em, black):
    """E2-05 exits at c[T-3]; an earlier Tier-1 event in the hold (ISM 10:00 on the same day)
    caps it at that event's T-3 (fixed after the verifier's independent re-run disagreed)."""
    cap = fomc_t[day.d] - 3
    for t in black.get(day.d, []):
        if em < t - 2:
            cap = min(cap, t - 3)
    k = int(np.searchsorted(day.mn, cap, side="right")) - 1
    if k < 0 or day.mn[k] < em:
        return None
    return (day.c[k] - ep) / ep * 1e4 - 2 * cost / ep * 1e4


def range20(days):
    """median over the previous 20 sessions of range(09:30..09:59)/o[09:30]; NaN if < 20."""
    rg = []
    for day in days:
        w = day.mn <= 9 * 60 + 59
        if w.any() and day.mn[0] == 9 * 60 + 30:
            rg.append((day.h[w].max() - day.l[w].min()) / day.o[0])
        else:
            rg.append(np.nan)
    s = pd.Series(rg)
    return s.rolling(20, min_periods=20).median().shift(1).to_numpy()


def run_market(name, days, cal, cmult=1.0, delay=0, is_leg=False):
    kinds, fomc_t, black = cal
    cost = COST[name] * cmult
    med = range20(days)
    res = {v: {} for v in VARIANTS}
    dec_log = []
    for i, day in enumerate(days):
        ft = fomc_t
        if is_leg and day.d < IS_FOMC_FROM and day.d in fomc_t:
            continue        # IS: FOMC days before 2013-03-20 dropped (statement clock unconfirmed)
        for v in VARIANTS[:11]:
            for side, em, ep, _ in decide(v, day, kinds, ft, delay, med[i]):
                if v == "E2-05":
                    r = exit_e205(day, ft, cost, ep, em, black)
                else:
                    r = exit_trade(day, side, em, ep, black, cost)
                if r is not None:
                    res[v][day.d] = res[v].get(day.d, 0.0) + r
                    dec_log.append((v, i, side, em, ep))
        comb = [res[v][day.d] for v in ("E2-01", "E2-05", "E2-06", "E2-08") if day.d in res[v]]
        if comb:
            res["E2-12"][day.d] = float(np.sum(comb))
    return res, dec_log


# ── statistics ───────────────────────────────────────────────────────────────
def pool(legs):
    """legs: list of {day: bp}; per day mean of available legs"""
    days = sorted(set().union(*[set(x) for x in legs]))
    return pd.Series({d: np.mean([x[d] for x in legs if d in x]) for d in days}, dtype=float)


def tstat(x):
    x = np.asarray(x, float)
    return x.mean() / x.std(ddof=1) * np.sqrt(len(x)) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan


def boot_p5(x, block=1, B=10_000, seed=0):
    x = np.asarray(x, float)
    n = len(x)
    rng = np.random.default_rng(seed)
    if block == 1:
        return np.percentile(x[rng.integers(0, n, (B, n))].mean(1), 5)
    nb = int(np.ceil(n / block))
    st = rng.integers(0, n - block + 1, (B, nb))
    idx = (st[:, :, None] + np.arange(block)).reshape(B, -1)[:, :n]
    return np.percentile(x[idx].mean(1), 5)


def truncation_test(name, days, cal, dec_log):
    kinds, fomc_t, _ = cal
    med = range20(days)
    bad = 0
    for v, i, side, em, ep in dec_log:
        if v == "E2-12":
            continue
        t = days[i].truncated(em)
        got = [(s, m, p) for s, m, p, _ in decide(v, t, kinds, fomc_t, 0, med[i])]
        if (side, em, ep) not in got:
            bad += 1
    return bad, len(dec_log)


def main():
    cal = calendar()
    print("E2 scheduled macro events — pre-registered in agents/prereg/E2_rules.md (commit d489ea8)")
    print(f"bar t >= {BAR}; costs per side {COST}; 2x = double\n")
    D = {k: build_days(k) for k in ("SPX", "SPY", "NQ")}
    for k, v in D.items():
        print(f"{k}: {len(v)} sessions {v[0].d}..{v[-1].d}")
    oos_years = (pd.Timestamp("2025-11-21") - pd.Timestamp("2019-01-02")).days / 365.25
    out = {}
    for cm in (1.0, 2.0):
        R = {k: run_market(k, D[k], cal, cm, 0, is_leg=(k == "SPX")) for k in D}
        out[cm] = R
    Rd = {k: run_market(k, D[k], cal, 1.0, 1, is_leg=(k == "SPX")) for k in ("SPY", "NQ")}
    print("\nunit = bp per event day (net); pooled OOS = mean of SPY and NQ legs on each day\n")
    hdr = (f"{'id':6} {'IS n':>5} {'IS bp':>7} | {'SPY n':>5} {'SPY bp':>7} | {'NQ n':>5} {'NQ bp':>7} | "
           f"{'OOS n':>5} {'bp':>7} {'t':>6} {'p5':>7} {'tr/yr':>6} | {'t 2x':>6} | {'t +1bar':>7} | gate")
    print(hdr)
    print("-" * len(hdr))
    summary = {}
    for v in VARIANTS:
        R1 = out[1.0]
        is_ = pd.Series(R1["SPX"][0][v], dtype=float)
        spy = pd.Series(R1["SPY"][0][v], dtype=float)
        nq = pd.Series(R1["NQ"][0][v], dtype=float)
        p = pool([R1["SPY"][0][v], R1["NQ"][0][v]])
        p2 = pool([out[2.0]["SPY"][0][v], out[2.0]["NQ"][0][v]])
        pd1 = pool([Rd["SPY"][0][v], Rd["NQ"][0][v]])
        t1, t2, td = tstat(p), tstat(p2), tstat(pd1)
        p5 = boot_p5(p)
        if v == "E2-12":
            p5 = min(p5, boot_p5(p.values, block=5))
        la_ok = np.sign(pd1.mean()) == np.sign(p.mean()) and td >= 0.5 * t1
        gate = (t1 >= BAR) and (p5 > 0) and spy.mean() > 0 and nq.mean() > 0 and la_ok
        summary[v] = dict(n=len(p), mean=p.mean(), t=t1, p5=p5, t2=t2, tpy=len(p) / oos_years,
                          spy=spy.mean(), nq=nq.mean(), is_mean=is_.mean() if len(is_) else np.nan,
                          is_n=len(is_), td=td, gate=gate, la=la_ok)
        print(f"{v:6} {len(is_):5d} {is_.mean():+7.2f} | {len(spy):5d} {spy.mean():+7.2f} | {len(nq):5d} "
              f"{nq.mean():+7.2f} | {len(p):5d} {p.mean():+7.2f} {t1:+6.2f} {p5:+7.2f} {len(p) / oos_years:6.1f} | "
              f"{t2:+6.2f} | {td:+7.2f} | {'PASS' if gate else 'FAIL'}")
    print("\ngross check (0 cost) pooled OOS mean bp / t:")
    R0 = {k: run_market(k, D[k], cal, 0.0, 0, is_leg=(k == "SPX")) for k in ("SPY", "NQ", "SPX")}
    for v in VARIANTS:
        p0 = pool([R0["SPY"][0][v], R0["NQ"][0][v]])
        i0 = pd.Series(R0["SPX"][0][v], dtype=float)
        print(f"  {v}: OOS gross {p0.mean():+7.2f} bp t {tstat(p0):+5.2f} | IS gross {i0.mean():+7.2f} bp t {tstat(i0):+5.2f}")
    print("\ntruncation test (decision identical when bars after the entry minute are deleted):")
    allok = True
    for k in ("SPY", "NQ", "SPX"):
        bad, n = truncation_test(k, D[k], cal, out[1.0][k][1])
        allok &= bad == 0
        print(f"  {k}: {bad} violations / {n} trade decisions")
    print(f"  => {'PASS' if allok else 'FAIL'}")
    best = max(VARIANTS, key=lambda v: summary[v]["t"])
    npass = sum(s["gate"] and allok for s in summary.values())
    print(f"\nbest OOS t: {best} t {summary[best]['t']:+.2f} (bar {BAR}); variants passing the gate: {npass}/12")
    pd.DataFrame(summary).T.to_csv(HERE / "summary.csv", float_format="%.4f")
    # per-day pooled series for the verifier / red team
    rows = []
    for v in VARIANTS:
        for k in ("SPY", "NQ", "SPX"):
            for d, x in out[1.0][k][0][v].items():
                rows.append((v, k, d, round(x, 4)))
    pd.DataFrame(rows, columns=["variant", "market", "date", "net_bp_1x"]).to_csv(
        Path(L.SCR) / "e2_trades.csv", index=False)


if __name__ == "__main__":
    main()
