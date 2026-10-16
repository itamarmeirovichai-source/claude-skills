"""D4 decision rules (spec §6) and the shared executor.

A decision function sees one session's bars (t, o, h, l, c: open time ns, UTC) and returns
events (info_time, fill_time, price, new_pos):
  * info_time = the earliest time at which every input of the decision is known (all inputs
    are bars with open time < info_time). The truncation test checks exactly this.
  * price = nan -> fill at F(fill_time); otherwise a fixed price (stop orders).
The executor turns events into fills, P&L and cost. A missing fill leaves the position as is.
"""
from __future__ import annotations

import numpy as np

from common import MIN, fill, mark

NAN = float("nan")


def dec_gao(t, o, h, l, c, O, C, cprev):
    """D4-01: s = sign(log M(O+30) - log Cprev); enter at F(C-30)."""
    m30 = mark(t, c, O + 30 * MIN)
    if not (cprev > 0) or not (m30 > 0):
        return []
    s = int(np.sign(np.log(m30) - np.log(cprev)))
    return [(O + 30 * MIN, C - 30 * MIN, NAN, s)] if s else []


def dec_rest(t, o, h, l, c, O, C, cprev):
    """D4-02: same signal, enter at F(O+30)."""
    m30 = mark(t, c, O + 30 * MIN)
    if not (cprev > 0) or not (m30 > 0):
        return []
    s = int(np.sign(np.log(m30) - np.log(cprev)))
    return [(O + 30 * MIN, O + 30 * MIN, NAN, s)] if s else []


def dec_twap(t, o, h, l, c, O, C, cprev):
    """D4-03: at T = O+30, O+60, ... <= C-30: desired = sign(M(T) - TWAP[O, T))."""
    a = np.searchsorted(t, O, "left")
    tp = (h + l + c) / 3.0
    cs = np.concatenate([[0.0], np.cumsum(tp[a:])])
    ev, desired = [], 0
    T = O + 30 * MIN
    while T <= C - 30 * MIN:
        k = np.searchsorted(t, T, "left") - a          # bars with open time in [O, T)
        mt = mark(t, c, T)
        if k > 0 and mt == mt:
            tw = cs[k] / k
            if mt > tw:
                desired = 1
            elif mt < tw:
                desired = -1
            if desired:
                ev.append((T, T, NAN, desired))
        T += 30 * MIN
    return ev


def dec_orb(t, o, h, l, c, O, C, cprev):
    """D4-04: 30-min opening range breakout, first breakout only, stop = opposite side."""
    a = np.searchsorted(t, O, "left")
    b = np.searchsorted(t, O + 30 * MIN, "left")
    if b <= a:
        return []
    hi, lo = h[a:b].max(), l[a:b].min()
    e = np.searchsorted(t, C - 30 * MIN, "left")
    if e <= b:
        return []
    cc = c[b:e]
    br = np.flatnonzero((cc > hi) | (cc < lo))
    if len(br) == 0:
        return []
    j = b + br[0]                                       # breakout bar
    side = 1 if c[j] > hi else -1
    T = t[j] + MIN                                      # its close is known at t+1m
    ev = [(T, T, NAN, side)]
    # entry bar = first bar with open time in [T, T+10m]; stop can hit from that bar on
    k = np.searchsorted(t, T, "left")
    if k >= len(t) or t[k] > T + 10 * MIN:
        return ev                                       # executor will find no fill
    z = np.searchsorted(t, C, "left")                   # bars with open time < C
    stop = lo if side == 1 else hi
    hit = np.flatnonzero(l[k:z] <= stop) if side == 1 else np.flatnonzero(h[k:z] >= stop)
    if len(hit):
        q = k + hit[0]
        px = min(o[q], stop) if side == 1 else max(o[q], stop)
        ev.append((t[q] + MIN, t[q], px, 0))
    return ev


DECISIONS = {"D4-01": dec_gao, "D4-02": dec_rest, "D4-03": dec_twap, "D4-04": dec_orb}


def execute(events, t, o, c, C, cost_bp):
    """Returns (gross return, cost per 1x cost, sides traded) as fractions of notional,
    P&L referenced to the day's first fill price. Flat at M(C)."""
    pos, legs = 0, []
    for info, ft, px, new in sorted(events, key=lambda e: (e[0], e[1])):
        if new == pos:
            continue
        p = px if px == px else fill(t, o, ft)
        if not (p == p):
            continue
        legs.append((p, new - pos))
        pos = new
    if pos != 0:
        legs.append((mark(t, c, C), -pos))
    if not legs:
        return 0.0, 0.0, 0
    ref = legs[0][0]
    gross, cur, last = 0.0, 0, None
    for p, d in legs:
        if cur != 0:
            gross += cur * (p - last) / ref
        cur += d
        last = p
    sides = sum(abs(d) for _, d in legs)
    return gross, sides * cost_bp * 1e-4, sides
