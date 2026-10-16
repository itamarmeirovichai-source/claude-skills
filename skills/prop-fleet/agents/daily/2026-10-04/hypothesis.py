#!/usr/bin/env python3
"""H-2026-10-04 (hypothesis builder): last-half-hour intraday momentum.

Source of the idea: Gao, Han, Li & Zhou (2018, JFE), "Market intraday
momentum": the S&P return from the previous 16:00 close to 10:00 predicts
the return of the last half hour (15:30-16:00). Not in ledger.csv (H0005 is
the Beat-the-Market noise-area breakout, a different rule).

PRE-REGISTERED RULES (written before the first run, not changed after)
---------------------------------------------------------------------
Data: SPXUSD 1-minute, 2010-2018, New York clock, loaded with
tjr_backtest.load_minutes(). Bar timestamps are bar opens.
Per weekday d:
  P0  = close of the 15:59 bar of the previous trading day that has one.
  P1  = close of the 09:59 bar of day d          (first-half-hour return r1 = P1/P0-1)
  r12 = close(15:29 bar) / close(14:59 bar) - 1   (12th half-hour return)
  Skip the day if any of the 09:59, 14:59, 15:29, 15:30, 15:59 bars is missing
  (covers half-days) or r1 == 0.
Signal: side = sign(r1).
Entry: market at the OPEN of the 15:30 bar.
Stop: entry -/+ STOP_PCT * entry. Risk = that distance (must be >= 1.0 pt,
  tjr MIN_RISK). Checked on every bar 15:30..15:59 including the entry bar.
  Stop fill = the worse of the stop price and the bar open (gap-through).
Exit: close of the 15:59 bar if not stopped. No target (so no ambiguous
  stop/target bar; stop-first rule is trivially satisfied).
Cost: 0.6 pt round trip (tjr_backtest.COST_PTS). R = net pts / risk.
Gross R = (net pts + 0.6) / risk.
Variants (all reported, three max):
  A  base: STOP_PCT = 0.20%
  B  same as A, but trade only when sign(r12) == sign(r1) (Gao's two predictors agree)
  C  same as A with STOP_PCT = 0.40%
Statistics: mean R, bootstrap 5th pct of mean (tjr_backtest.boot_mean, 5000
draws, seed 0), trades, trades/yr, gross mean R, annualised Sharpe, and the
two halves 2010-2014 / 2015-2018 (the second half is the pseudo-OOS check).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import tjr_backtest as tj  # noqa: E402

COST = tj.COST_PTS
VARIANTS = {"A_base_0.20pct": (0.0020, False),
            "B_agree12_0.20pct": (0.0020, True),
            "C_base_0.40pct": (0.0040, False)}


def build_days(m1: pd.DataFrame) -> list[dict]:
    hm = m1.index.strftime("%H:%M")
    dates = m1.index.normalize()
    need = ["09:59", "14:59", "15:29", "15:30", "15:59"]
    sub = m1[np.isin(hm, need)].copy()
    sub["d"] = dates[np.isin(hm, need)]
    sub["hm"] = hm[np.isin(hm, need)]
    piv = {k: g.set_index("d") for k, g in sub.groupby("hm")}
    last_bars = m1[(hm >= "15:30") & (hm <= "15:59")]
    lb_by_day = {d: g for d, g in last_bars.groupby(last_bars.index.normalize())}
    days = sorted(set(piv["15:59"].index))
    out, prev_close = [], None
    for d in days:
        c1559 = float(piv["15:59"].loc[d, "c"])
        if d.weekday() < 5 and prev_close is not None and all(d in piv[k].index for k in need):
            p1 = float(piv["09:59"].loc[d, "c"])
            r1 = p1 / prev_close - 1
            r12 = float(piv["15:29"].loc[d, "c"]) / float(piv["14:59"].loc[d, "c"]) - 1
            if r1 != 0 and d in lb_by_day:
                out.append(dict(day=d, r1=r1, r12=r12, bars=lb_by_day[d]))
        prev_close = c1559
    return out


def trade(day: dict, stop_pct: float) -> dict | None:
    side = 1 if day["r1"] > 0 else -1
    bars = day["bars"]
    entry = float(bars["o"].iloc[0])
    risk = stop_pct * entry
    if risk < tj.MIN_RISK:
        return None
    stop = entry - side * risk
    exit_px, why = float(bars["c"].iloc[-1]), "time"
    for o, h, l in zip(bars["o"].values, bars["h"].values, bars["l"].values):
        if (side > 0 and l <= stop) or (side < 0 and h >= stop):
            exit_px = min(stop, o) if side > 0 else max(stop, o)
            why = "stop"
            break
    pts = (exit_px - entry) * side - COST
    return dict(day=day["day"], side=side, risk=risk, why=why, pts=pts,
                R=pts / risk, gross_R=(pts + COST) / risk)


def stats(t: pd.DataFrame) -> dict:
    x = t["R"].values
    lo, _, hi = tj.boot_mean(x)
    yrs = (t["day"].max() - t["day"].min()).days / 365.25
    py = len(t) / yrs
    glo, _, _ = tj.boot_mean(t["gross_R"].values)
    return dict(n=len(t), per_year=round(py, 1), mean_R=round(x.mean(), 4),
                p5_R=round(lo, 4), p95_R=round(hi, 4),
                gross_mean_R=round(t["gross_R"].mean(), 4), gross_p5_R=round(glo, 4),
                sharpe=round(x.mean() / x.std(ddof=1) * np.sqrt(py), 2),
                stop_rate=round((t["why"] == "stop").mean(), 3),
                med_risk_pts=round(t["risk"].median(), 2))


def main() -> int:
    m1 = tj.load_minutes()
    print(f"bars {len(m1):,}  {m1.index[0]} .. {m1.index[-1]}")
    days = build_days(m1)
    print(f"eligible days {len(days)}")
    for name, (sp, agree) in VARIANTS.items():
        rows = [trade(d, sp) for d in days
                if not agree or np.sign(d["r12"]) == np.sign(d["r1"])]
        t = pd.DataFrame([r for r in rows if r])
        s = stats(t)
        h1 = t[t["day"].dt.year <= 2014]
        h2 = t[t["day"].dt.year >= 2015]
        s1, s2 = stats(h1), stats(h2)
        print(name, s)
        print("   2010-14", {k: s1[k] for k in ("n", "mean_R", "p5_R", "gross_mean_R")})
        print("   2015-18", {k: s2[k] for k in ("n", "mean_R", "p5_R", "gross_mean_R")})
        print("   by year", t.groupby(t["day"].dt.year)["R"].mean().round(3).to_dict())
    return 0


if __name__ == "__main__":
    sys.exit(main())
