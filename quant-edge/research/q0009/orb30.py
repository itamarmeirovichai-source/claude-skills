"""Q-0009 prereg_orb30 as written (registered 0a46ddd): S&P 30-minute opening-range breakout, flat by 15:59 ET.

Rules (America/New_York, per day with zoneinfo; HistData SPXUSD bid bars, ts = bar open UTC, clock histdata_rule):
 (1) eligible at 10:00: weekday, the 09:30 bar exists, >= 25 of the 30 bars 09:30..09:59 exist;
 (2) ORH = max high, ORL = min low of bars 09:30..09:59; W = ORH - ORL;
 (3) trigger = first bar with time in 10:00..11:59 whose CLOSE > ORH (long) or < ORL (short); one trade per day;
 (4) entry = open of the next existing bar after the trigger bar if its time <= 12:00, else no trade;
 (5) stop = ORL (long) / ORH (short); Risk = |entry - stop|; no trade if Risk < 1.0 pt or entry at/beyond the stop;
 (6) from the entry bar inclusive: stop touched (long low <= stop, short high >= stop) -> exit at the worse of the stop
     and that bar's open; else exit at the close of the last existing bar at or before 15:59;
 (7) gross R = side*(exit-entry)/Risk; net R = gross R - cost/Risk.
 Variants: A = (1)-(7); B = A + target entry + side*2*Risk, a bar touching both stop and target counts as stop;
 C = A traded only if W < median W of the previous 20 eligible sessions (today excluded; needs 20).

Conventions the row leaves open, fixed here before any IS result was computed:
  * "session d" = New York calendar date of the bar open; bars of d only.
  * B target fill: CONVENTIONS.md section 3 limit rule - filled only when price trades THROUGH the target (long high >
    target, short low < target), at the target price (a gap through the target at the bar open also fills at the target).
    The stop check runs first on every bar (stop-first on any ambiguous bar, as written).
  * The entry bar itself is checked for stop/target after its open (from the entry bar inclusive, as written).
  * Bars after 15:59 are ignored; if no bar exists in entry..15:59 other than the entry bar, exit = entry bar close.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "batch1b"))
import cfdkit as ck  # noqa: E402

OR_A, OR_B = 9 * 60 + 30, 9 * 60 + 59          # 09:30..09:59
EXIT_LAST = 15 * 60 + 59


@dataclass(frozen=True)
class Params:
    trig_end: int = 11 * 60 + 59                 # last trigger minute (11:59)
    entry_last: int = 12 * 60                    # entry bar time <= 12:00
    min_risk: float = 1.0                        # pt
    target_r: float = 0.0                        # 0 = no target (A, C); 2.0 = B
    narrow: bool = False                         # C filter
    entry_delay: int = 0                         # extra existing bars of delay after the "next bar" (one-bar delay test)
    leak: str = ""                               # "plant" = deliberately reads the day's last close (harness sanity check)


def trades(p: ck.Prepared, prm: Params) -> pd.DataFrame:
    days = ck.day_slices(p)
    m, o, h, l, c = p.minute, p.open, p.high, p.low, p.close
    rows = []
    Ws = []                                      # W of previous eligible sessions
    for d, (a, b) in days.items():
        if pd.Timestamp(d).dayofweek >= 5:
            continue
        mm = m[a:b]
        k0 = a + int(np.searchsorted(mm, OR_A))
        k1 = a + int(np.searchsorted(mm, OR_B, side="right"))
        if not (k0 < b and m[k0] == OR_A and (k1 - k0) >= 25):
            continue
        orh, orl = float(h[k0:k1].max()), float(l[k0:k1].min())
        W = orh - orl
        hist = Ws[-20:]
        Ws.append(W)
        if prm.narrow:
            if len(hist) < 20 or not (W < float(np.median(hist))):
                continue
        t1 = a + int(np.searchsorted(mm, prm.trig_end, side="right"))
        hit = np.nonzero((c[k1:t1] > orh) | (c[k1:t1] < orl))[0]
        if hit.size == 0:
            continue
        kt = k1 + int(hit[0])
        side = 1 if c[kt] > orh else -1
        ke = kt + 1 + prm.entry_delay
        if ke >= b or m[ke] > prm.entry_last:
            continue
        entry = float(o[ke])
        stop = orl if side == 1 else orh
        risk = abs(entry - stop)
        if (side == 1 and entry <= stop) or (side == -1 and entry >= stop) or risk < prm.min_risk:
            continue
        if prm.leak == "plant":                   # look-ahead on purpose: trade only if the day closes beyond the entry
            last = a + int(np.searchsorted(mm, EXIT_LAST, side="right")) - 1
            if side * (c[last] - entry) <= 0:
                continue
        tgt = entry + side * prm.target_r * risk if prm.target_r > 0 else np.nan
        kx_end = a + int(np.searchsorted(mm, EXIT_LAST, side="right"))      # bars with time <= 15:59
        exit_px, how, kx = np.nan, "eod", -1
        sl = slice(ke, max(kx_end, ke))
        st = np.nonzero(l[sl] <= stop)[0] if side == 1 else np.nonzero(h[sl] >= stop)[0]
        js = ke + int(st[0]) if st.size else 10 ** 12
        jt = 10 ** 12
        if prm.target_r > 0:
            tg = np.nonzero(h[sl] > tgt)[0] if side == 1 else np.nonzero(l[sl] < tgt)[0]
            jt = ke + int(tg[0]) if tg.size else 10 ** 12
        if js <= jt and js < 10 ** 12:                       # stop first on any ambiguous bar
            kx, how = js, "stop"
            exit_px = min(stop, o[js]) if side == 1 else max(stop, o[js])
        elif jt < 10 ** 12:
            kx, how, exit_px = jt, "target", tgt
        if how == "eod":
            kx = max(kx_end - 1, ke)
            exit_px = float(c[kx])
        rows.append({"day": pd.Timestamp(d), "side": side, "W": W, "orh": orh, "orl": orl, "trig_min": int(m[kt]),
                     "entry_i": ke, "entry_min": int(m[ke]), "entry": entry, "stop": stop, "risk": risk, "exit_i": kx,
                     "exit_min": int(m[kx]), "exit": float(exit_px), "exit_type": how,
                     "gross_R": side * (float(exit_px) - entry) / risk})
    t = pd.DataFrame(rows)
    if len(t) == 0:
        t = pd.DataFrame(columns=["day", "side", "W", "entry", "risk", "exit", "exit_type", "gross_R", "entry_i", "exit_i"])
    return t


def cost_pts(t: pd.DataFrame, kind: str) -> np.ndarray:
    """Round-trip cost in index points. is: 0.6 pt (written COST_PTS); cfd1x: max(0.6 pt, 2.0 bp of entry);
    cfd2x: double cfd1x; es: 2 x (0.30 pt + $2.50 / $50) = 0.70 pt (venue sensitivity, no count)."""
    e = t["entry"].to_numpy(float)
    if kind == "is":
        return np.full(e.size, 0.6)
    if kind == "cfd1x":
        return np.maximum(0.6, 2.0e-4 * e)
    if kind == "cfd2x":
        return 2 * np.maximum(0.6, 2.0e-4 * e)
    if kind == "es":
        return np.full(e.size, 2 * (0.30 + 2.50 / 50.0))
    raise ValueError(kind)


def net_R(t: pd.DataFrame, kind: str) -> np.ndarray:
    return t["gross_R"].to_numpy(float) - cost_pts(t, kind) / t["risk"].to_numpy(float)


class ORBRule:
    """qe.engine.harness interface: target[i] = side held over bar i (entry bar .. exit bar)."""
    name = "orb30"
    mode = "target"

    def __init__(self, prm: Params):
        self.prm, self.params = prm, {}

    def signal(self, bars: pd.DataFrame):
        p = ck.prepare(bars, ck.NY)
        t = trades(p, self.prm)
        tgt = np.zeros(len(bars))
        for r in t.itertuples():
            tgt[int(r.entry_i):int(r.exit_i) + 1] = r.side
        return tgt
