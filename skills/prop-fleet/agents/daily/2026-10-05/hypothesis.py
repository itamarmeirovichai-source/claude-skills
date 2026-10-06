#!/usr/bin/env python3
"""H-2026-10-05 (hypothesis builder): intraday IBS reversal on the S&P.

Rules: builder/prereg_ibs_intraday.txt (sha256 + UTC time in
builder/prereg_ibs_intraday.sha256), written before this file ran. Summary:
  prev-session IBS = (C-L)/(H-L) on RTH 09:30..15:59 (NY clock; clock checked by
  builder/diag_clock.py -> same peak minute Jan/Jul -> no conversion).
  long if IBS <= 0.20, short if >= 0.80; entry 09:31 open; stop k * ATR14 (mean RTH
  range of the 14 previous valid sessions); stop checked from the entry bar, fills
  at the worse of stop and bar open; no target; exit 15:59 close; 0.6 pt round trip.
  A: k=0.5 both sides   B: k=0.5 long-only   C: k=1.0 both sides
Reuses tjr_backtest.load_minutes, COST_PTS, MIN_RISK, boot_mean.
"""
from __future__ import annotations

import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import tjr_backtest as tj  # noqa: E402

COST = tj.COST_PTS
LO, HI = 0.20, 0.80
N_LEDGER = 176                     # board N 173 + these 3 variants
VARIANTS = {"A_both_0.5atr": (0.5, True),
            "B_long_0.5atr": (0.5, False),
            "C_both_1.0atr": (1.0, True)}


def sessions(m1: pd.DataFrame) -> list[dict]:
    """Valid RTH sessions in date order: weekday, >=370 RTH bars, 09:31 and 15:59 present."""
    hm = m1.index.strftime("%H:%M")
    rth = m1[(hm >= "09:30") & (hm <= "15:59")]
    out = []
    for d, g in rth.groupby(rth.index.normalize()):
        if d.weekday() >= 5 or len(g) < 370:
            continue
        ghm = g.index.strftime("%H:%M")
        if "09:31" not in ghm or "15:59" not in ghm:
            continue
        out.append(dict(day=d, H=float(g["h"].max()), L=float(g["l"].min()),
                        C=float(g["c"].iloc[np.where(ghm == "15:59")[0][0]]),
                        bars=g[ghm >= "09:31"]))
    return out


def signals(sess: list[dict]) -> list[dict]:
    """Uses only sessions before d for IBS and ATR14."""
    out = []
    for i in range(14, len(sess)):
        p = sess[i - 1]
        if p["H"] == p["L"]:
            continue
        ibs = (p["C"] - p["L"]) / (p["H"] - p["L"])
        atr = float(np.mean([s["H"] - s["L"] for s in sess[i - 14:i]]))
        side = 1 if ibs <= LO else (-1 if ibs >= HI else 0)
        if side:
            out.append(dict(day=sess[i]["day"], ibs=ibs, atr=atr, side=side,
                            bars=sess[i]["bars"]))
    return out


def trade(sig: dict, k: float) -> dict | None:
    side, bars = sig["side"], sig["bars"]
    entry = float(bars["o"].iloc[0])           # 09:31 open
    risk = k * sig["atr"]
    if risk < tj.MIN_RISK:
        return None
    stop = entry - side * risk
    exit_px, why = float(bars["c"].iloc[-1]), "time"   # 15:59 close
    for o, h, l in zip(bars["o"].values, bars["h"].values, bars["l"].values):
        if (side > 0 and l <= stop) or (side < 0 and h >= stop):
            exit_px = min(stop, o) if side > 0 else max(stop, o)
            why = "stop"
            break
    gross = (exit_px - entry) * side
    return dict(day=sig["day"], side=side, ibs=sig["ibs"], risk=risk, why=why,
                pts=gross - COST, R=(gross - COST) / risk, gross_R=gross / risk)


def stats(t: pd.DataFrame) -> dict:
    x, g = t["R"].values, t["gross_R"].values
    lo, _, hi = tj.boot_mean(x)
    glo, _, _ = tj.boot_mean(g)
    yrs = (t["day"].max() - t["day"].min()).days / 365.25
    py = len(t) / yrs
    z = NormalDist().inv_cdf(1 - 0.05 / N_LEDGER)
    return dict(n=len(t), per_year=round(py, 1), mean_R=round(x.mean(), 4),
                p5_R=round(lo, 4), p95_R=round(hi, 4),
                gross_mean_R=round(g.mean(), 4), gross_p5_R=round(glo, 4),
                lb_bonf=round(x.mean() - z * x.std(ddof=1) / np.sqrt(len(x)), 4),
                z=round(z, 3),
                sharpe=round(x.mean() / x.std(ddof=1) * np.sqrt(py), 2),
                stop_rate=round((t["why"] == "stop").mean(), 3),
                med_risk_pts=round(t["risk"].median(), 2),
                cost_R_median=round(COST / t["risk"].median(), 4))


def main() -> int:
    m1 = tj.load_minutes()
    print(f"bars {len(m1):,}  {m1.index[0]} .. {m1.index[-1]}")
    sess = sessions(m1)
    sig = signals(sess)
    print(f"valid sessions {len(sess)}  signal days (IBS<=0.2 or >=0.8) {len(sig)}")
    for name, (k, both) in VARIANTS.items():
        rows = [trade(s, k) for s in sig if both or s["side"] > 0]
        t = pd.DataFrame([r for r in rows if r])
        print(name, stats(t))
        for lab, sub in (("2010-14", t[t["day"].dt.year <= 2014]),
                         ("2015-18", t[t["day"].dt.year >= 2015])):
            s = stats(sub)
            print(f"   {lab}", {kk: s[kk] for kk in ("n", "mean_R", "p5_R", "gross_mean_R")})
        for sd, lab in ((1, "long"), (-1, "short")):
            sub = t[t["side"] == sd]
            if len(sub):
                print(f"   {lab}: n={len(sub)} net {sub['R'].mean():+.4f} "
                      f"gross {sub['gross_R'].mean():+.4f}")
        print("   by year net", t.groupby(t["day"].dt.year)["R"].mean().round(3).to_dict())
    return 0


if __name__ == "__main__":
    sys.exit(main())
