"""Independent verifier for E2 (prereg/E2_rules.md), written from the spec only.
Does not read events.py / events_bt*.py. Uses loaders.py (sha256-pinned) and events.csv.
Run: CLAUDE_SCRATCH=... python3 verify.py > verify_run.txt"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import loaders as L  # noqa: E402

GATE = 3.5603
COST = {"SPX": 0.30, "SPY": 0.030, "NQ": 0.375}
SIX = {"FOMC", "CPI", "NFP", "PCE", "RETAIL", "ISM"}
BLACKOUT_EV = {"FOMC", "FOMC_MINUTES", "ISM"}
RTH0, RTH1 = 9 * 60 + 30, 15 * 60 + 59


def hm2m(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


# ── calendar ────────────────────────────────────────────────────────────────
ev = pd.read_csv(HERE.parent / "events.csv")
ev["scheduled"] = ev["scheduled"].astype(str).str.lower() == "true"
ev = ev[ev.scheduled].copy()                      # unscheduled rows are never event days
ev["d"] = pd.to_datetime(ev["date"]).dt.date
ev["T"] = ev["time_et"].map(hm2m)
EV_BY_DAY: dict = {}
for r in ev.itertuples():
    EV_BY_DAY.setdefault(r.d, []).append((r.event, r.T))


# ── per-session arrays ──────────────────────────────────────────────────────
class Sess:
    __slots__ = ("t", "o", "h", "l", "c")

    def __init__(self, g):
        self.t = (g.index.hour * 60 + g.index.minute).to_numpy()
        self.o, self.h, self.l, self.c = (g[k].to_numpy() for k in "ohlc")

    def sig_close(self, x):  # c of last bar at or before x
        i = np.searchsorted(self.t, x, side="right") - 1
        return None if i < 0 else self.c[i]

    def sig_open(self, x):   # o of last bar at or before x
        i = np.searchsorted(self.t, x, side="right") - 1
        return None if i < 0 else self.o[i]

    def entry_idx(self, x):  # next bar within 3 minutes
        i = np.searchsorted(self.t, x, side="left")
        return i if i < len(self.t) and self.t[i] <= x + 3 else None

    def idx_at_or_before(self, x):
        i = np.searchsorted(self.t, x, side="right") - 1
        return None if i < 0 else i


def build(m: pd.DataFrame, full_nq: pd.DataFrame | None = None):
    r = L.rth(m)
    days = {}
    for d, g in r.groupby("date", sort=True):
        days[d] = Sess(g)
    dates = sorted(days)
    pc = {dates[i]: days[dates[i - 1]].c[-1] for i in range(1, len(dates))}
    adj = {}
    if full_nq is not None:
        idx = full_nq.index
        tt = idx.values
        for d in dates:
            t0 = np.datetime64(pd.Timestamp(d))
            j = np.searchsorted(tt, t0, side="left")      # first bar at/after 00:00
            if j <= 0 or j >= len(tt) or pd.Timestamp(tt[j]).date() != d or \
                    pd.Timestamp(tt[j]).hour * 60 + pd.Timestamp(tt[j]).minute >= RTH0:
                adj[d] = 0.0
                continue
            adj[d] = math.log(full_nq["o"].iat[j] / full_nq["c"].iat[j - 1])
    return days, dates, pc, adj


# ── trade engine ────────────────────────────────────────────────────────────
def trade(s: Sess, d, entry_min, side, exit_min=None, delay=0):
    """Return (entry_price, exit_price, side) or None. Applies tier-1 blackout."""
    if side == 0:
        return None
    ei = s.entry_idx(entry_min + delay)
    if ei is None:
        return None
    et = s.t[ei]
    # natural exit
    if exit_min is None:
        xi = s.idx_at_or_before(RTH1)
    else:
        xi = s.idx_at_or_before(exit_min)
    if xi is None or xi < ei:
        return None
    xt = s.t[xi]
    # blackout: any in-RTH tier-1 event with entry <= T-3 and natural exit bar beyond T-3
    for e, T in EV_BY_DAY.get(d, []):
        if e in BLACKOUT_EV and RTH0 <= T <= RTH1:
            b = T - 3
            if et <= b and xt > b:
                bi = s.idx_at_or_before(b)
                if bi is not None and bi >= ei and s.t[bi] < xt:
                    xi, xt = bi, s.t[bi]
    return s.o[ei], s.c[xi], side


def ret_bp(tr, cost):
    eo, xc, side = tr
    return side * (xc - eo) / eo * 1e4 - 2 * cost / eo * 1e4


def sgn(x):
    return 0 if x == 0 else (1 if x > 0 else -1)


def gap(s, d, pc, adj):
    o930 = s.sig_open(RTH0)
    if o930 is None or d not in pc:
        return None
    return math.log(o930 / pc[d]) - adj.get(d, 0.0)


def first30(s, d, pc, adj):
    c959 = s.sig_close(9 * 60 + 59)
    if c959 is None or d not in pc:
        return None
    return math.log(c959 / pc[d]) - adj.get(d, 0.0)


def fomc_T(d):
    for e, T in EV_BY_DAY.get(d, []):
        if e == "FOMC":
            return T
    return None


def has(d, names):
    return any(e in names for e, _ in EV_BY_DAY.get(d, []))


def variant_trades(vid, days, dates, pc, adj, drop_days, delay=0):
    """dict date -> trade tuple for simple variants."""
    out = {}
    rng20 = {}
    if vid == "E2-11":
        rv = {}
        for d in dates:
            s = days[d]
            o930 = s.sig_open(RTH0)
            k = s.t <= 9 * 60 + 59
            if o930 is None or not k.any():
                rv[d] = None
            else:
                rv[d] = (s.h[k].max() - s.l[k].min()) / o930
        for i, d in enumerate(dates):
            prev = [rv[x] for x in dates[max(0, i - 20):i]]
            if len(prev) == 20 and all(p is not None for p in prev) and rv[d] is not None:
                rng20[d] = rv[d] > float(np.median(prev))
            else:
                rng20[d] = False
    for d in dates:
        if d in drop_days:
            continue
        s = days[d]
        T = fomc_T(d)
        tr = None
        if vid in ("E2-01", "E2-02", "E2-03", "E2-04") and T is not None:
            k = {"E2-01": 15, "E2-02": 5, "E2-03": 30, "E2-04": 15}[vid]
            a, b = s.sig_close(T + k - 1), s.sig_close(T - 1)
            if a is not None and b is not None:
                side = sgn(a - b) * (-1 if vid == "E2-04" else 1)
                tr = trade(s, d, T + k, side, delay=delay)
        elif vid == "E2-05" and T is not None:
            tr = trade(s, d, RTH0, 1, exit_min=T - 3, delay=delay)
        elif vid in ("E2-06", "E2-07") and has(d, {"CPI", "NFP"}):
            g = gap(s, d, pc, adj)
            if g is not None:
                tr = trade(s, d, 9 * 60 + 31, sgn(g) * (-1 if vid == "E2-07" else 1), delay=delay)
        elif vid in ("E2-08", "E2-09", "E2-10", "E2-11"):
            ok = has(d, SIX) if vid != "E2-10" else not has(d, SIX)
            if vid == "E2-11":
                ok = ok and rng20.get(d, False)
            if ok:
                x = first30(s, d, pc, adj)
                if x is not None:
                    if vid == "E2-09":
                        tr = trade(s, d, 15 * 60 + 30, sgn(x), exit_min=RTH1, delay=delay)
                    else:
                        tr = trade(s, d, 10 * 60 + 3, sgn(x), delay=delay)
        if tr is not None:
            out[d] = tr
    return out


VIDS = [f"E2-{i:02d}" for i in range(1, 13)]


def leg_returns(days, dates, pc, adj, drop_days, cost, delay=0):
    """vid -> pd.Series(date -> bp)."""
    res = {}
    tr = {v: variant_trades(v, days, dates, pc, adj, drop_days, delay) for v in VIDS[:11]}
    for v in VIDS[:11]:
        res[v] = pd.Series({d: ret_bp(t, cost) for d, t in tr[v].items()}, dtype=float).sort_index()
    comb = pd.concat([res[v] for v in ("E2-01", "E2-05", "E2-06", "E2-08")], axis=1)
    res["E2-12"] = comb.sum(axis=1, min_count=1).dropna().sort_index()
    return res


def tstat(x):
    x = np.asarray(x, float)
    n = len(x)
    if n < 2 or x.std(ddof=1) == 0:
        return float("nan")
    return x.mean() / x.std(ddof=1) * math.sqrt(n)


def boot_p5(x, B=10000):
    x = np.asarray(x, float)
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    return float(np.percentile(x[idx].mean(axis=1), 5))


def block_p5(x, b=5, B=10000):
    x = np.asarray(x, float)
    n = len(x)
    rng = np.random.default_rng(0)
    nb = math.ceil(n / b)
    st = rng.integers(0, n, size=(B, nb))              # circular moving blocks
    idx = (st[:, :, None] + np.arange(b)[None, None, :]) % n
    idx = idx.reshape(B, -1)[:, :n]
    return float(np.percentile(x[idx].mean(axis=1), 5))


def main():
    print("loading ...", flush=True)
    spx = L.load_spx()
    spy = L.load_spy()
    nq = L.load_nq()
    D = {"SPX": build(spx), "SPY": build(spy), "NQ": build(nq, full_nq=nq)}
    cut = pd.Timestamp("2013-03-20").date()
    drop_is = {d for d in D["SPX"][1] if d < cut and fomc_T(d) is not None}
    nadj = sum(abs(v) > 1e-4 for v in D["NQ"][3].values())
    print(f"IS sessions {len(D['SPX'][1])}  dropped pre-2013-03-20 FOMC days {len(drop_is)}")
    print(f"SPY sessions {len(D['SPY'][1])} {D['SPY'][1][0]}..{D['SPY'][1][-1]}")
    print(f"NQ  sessions {len(D['NQ'][1])} {D['NQ'][1][0]}..{D['NQ'][1][-1]}  |00:00 adj|>1bp on {nadj} days")
    miss930 = {k: sum(1 for d in D[k][1] if D[k][0][d].t[0] != RTH0) for k in D}
    print("sessions without a 09:30 bar:", miss930)

    R = {}
    for k in D:
        days, dates, pc, adj = D[k]
        dd = drop_is if k == "SPX" else set()
        for mult in (1, 2):
            R[(k, mult, 0)] = leg_returns(days, dates, pc, adj, dd, COST[k] * mult)
        R[(k, 1, 1)] = leg_returns(days, dates, pc, adj, dd, COST[k], delay=1)

    def pooled(mult, delay, v):
        a, b = R[("SPY", mult, delay)][v], R[("NQ", mult, delay)][v]
        return pd.concat([a, b], axis=1).mean(axis=1).dropna().sort_index()

    oos_start = min(D["SPY"][1][0], D["NQ"][1][0])
    oos_end = max(D["SPY"][1][-1], D["NQ"][1][-1])
    oos_yrs = (pd.Timestamp(oos_end) - pd.Timestamp(oos_start)).days / 365.25
    is_yrs = (pd.Timestamp(D["SPX"][1][-1]) - pd.Timestamp(D["SPX"][1][0])).days / 365.25

    hdr = (f"{'id':6} {'IS n':>5} {'IS mean':>8} | {'SPY n':>5} {'SPY mn':>7} | {'NQ n':>5} {'NQ mn':>7} |"
           f" {'OOS n':>5} {'mean':>7} {'t':>6} {'p5':>7} {'blk p5':>7} | {'t 2x':>6} {'mean2x':>7} |"
           f" {'t dly':>6} {'mn dly':>7} | {'tr/yr':>5} | gate")
    print()
    print(f"OOS span {oos_start}..{oos_end} ({oos_yrs:.2f} y); IS span {is_yrs:.2f} y. bp net of costs.")
    print(hdr)
    print("-" * len(hdr))
    for v in VIDS:
        is_ = R[("SPX", 1, 0)][v]
        sp, nqv = R[("SPY", 1, 0)][v], R[("NQ", 1, 0)][v]
        p1 = pooled(1, 0, v)
        p2 = pooled(2, 0, v)
        pd1 = pooled(1, 1, v)
        t1 = tstat(p1)
        bp5 = boot_p5(p1)
        blk = block_p5(p1) if v == "E2-12" else float("nan")
        p5use = min(bp5, blk) if v == "E2-12" else bp5
        t2 = tstat(p2)
        td = tstat(pd1)
        la = (np.sign(pd1.mean()) == np.sign(p1.mean())) and td >= 0.5 * t1
        gate = (t1 >= GATE) and (p5use > 0) and (sp.mean() > 0) and (nqv.mean() > 0) and la
        verdict = "PASS" if gate and t2 >= GATE else ("PASS@1x only" if gate else "fail")
        print(f"{v:6} {len(is_):5d} {is_.mean():8.2f} | {len(sp):5d} {sp.mean():7.2f} | {len(nqv):5d} {nqv.mean():7.2f} |"
              f" {len(p1):5d} {p1.mean():7.2f} {t1:6.2f} {bp5:7.2f} {blk:7.2f} | {t2:6.2f} {p2.mean():7.2f} |"
              f" {td:6.2f} {pd1.mean():7.2f} | {len(p1) / oos_yrs:5.1f} | {verdict}")
    print()
    print("Columns: p5 = iid bootstrap p5 of pooled mean (10k, default_rng(0)); blk p5 = 5-day circular block")
    print("bootstrap (E2-12 only; lower of the two used in gate). t dly / mn dly = entry delayed one bar (look-ahead a).")
    print("Gate here = t>=3.5603, p5>0, SPY mean>0, NQ mean>0, look-ahead (a); truncation test not re-run (by construction).")
    print()
    print("Per-leg t at 1x (SPY / NQ) and IS t:")
    for v in VIDS:
        print(f"  {v}: IS t {tstat(R[('SPX',1,0)][v]):6.2f}  SPY t {tstat(R[('SPY',1,0)][v]):6.2f}"
              f"  NQ t {tstat(R[('NQ',1,0)][v]):6.2f}  IS tr/yr {len(R[('SPX',1,0)][v]) / is_yrs:5.1f}")


if __name__ == "__main__":
    main()
