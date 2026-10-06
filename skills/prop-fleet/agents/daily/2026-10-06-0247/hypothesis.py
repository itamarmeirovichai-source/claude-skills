#!/usr/bin/env python3
"""ORB30 (hypothesis builder, run 2026-10-06-0247): S&P 30-minute opening-range breakout.

Rules: builder/prereg_orb30.txt (sha256 1e99c775..., stamped 2026-10-05T23:58:55Z in
builder/prereg_orb30.sha256), written before this file existed. Summary:
  eligible at 10:00: weekday, 09:30 bar, >= 25 of the 30 bars 09:30..09:59
  ORH/ORL = high/low of 09:30..09:59; first bar 10:00..11:59 closing beyond -> side
  entry = open of the next bar (time <= 12:00); stop = opposite OR edge; risk >= 1 pt
  stop-first, fill at worse of stop and bar open; exit = close of last bar <= 15:59
  cost 0.6 pt RT.  A: no target.  B: 2R target.  C: A if W < median W of prior 20 eligible.
Reuses tjr_backtest.load_minutes, COST_PTS, MIN_RISK.

Running on market data is REFUSED unless --ledger-id names a ledger.csv row with
rules_fixed_before_test=yes whose notes cite this prereg's sha256 prefix (ORG.md day-2
rule: only a row pre-registered the evening before may be run). --feasibility reads only
bars 09:30..09:59 (no outcome) and prints opening-range widths.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                       # skills/prop-fleet
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE.parent / "2026-10-05" / "eng_head"))
import tjr_backtest as tj  # noqa: E402

COST = tj.COST_PTS
MIN_RISK = tj.MIN_RISK
PREREG_SHA_PREFIX = "1e99c775"
LEDGER = ROOT / "agents" / "ledger.csv"
N_AFTER = 198                                 # board N 195 + these 3 variants
VARIANTS = ("A", "B", "C")


# -- per-day logic (only bars of day d) -------------------------------------
def opening_range(day_bars: pd.DataFrame):
    """Return (ORH, ORL) or None. Reads only bars 09:30..09:59."""
    hm = day_bars.index.strftime("%H:%M")
    orb = day_bars[(hm >= "09:30") & (hm <= "09:59")]
    if orb.empty or orb.index[0].strftime("%H:%M") != "09:30" or len(orb) < 25:
        return None
    return float(orb["h"].max()), float(orb["l"].min())


def trade_day(day_bars: pd.DataFrame, orh: float, orl: float, variant: str) -> dict | None:
    hm = day_bars.index.strftime("%H:%M")
    win = day_bars[(hm >= "10:00") & (hm <= "11:59")]
    side, trig_ts = 0, None
    for ts, c in zip(win.index, win["c"].values):
        if c > orh:
            side, trig_ts = 1, ts
            break
        if c < orl:
            side, trig_ts = -1, ts
            break
    if not side:
        return None
    after = day_bars[(day_bars.index > trig_ts) & (hm <= "15:59")]
    if after.empty or after.index[0].strftime("%H:%M") > "12:00":
        return None
    entry = float(after["o"].iloc[0])
    stop = orl if side > 0 else orh
    risk = (entry - stop) * side
    if not risk >= MIN_RISK:
        return None
    tgt = entry + side * 2 * risk if variant == "B" else None
    exit_px, why = float(after["c"].iloc[-1]), "time"
    for o, h, l in zip(after["o"].values, after["h"].values, after["l"].values):
        if (side > 0 and l <= stop) or (side < 0 and h >= stop):
            exit_px, why = (min(stop, o) if side > 0 else max(stop, o)), "stop"
            break
        if tgt is not None and ((side > 0 and h >= tgt) or (side < 0 and l <= tgt)):
            exit_px, why = tgt, "target"
            break
    gross_pts = (exit_px - entry) * side
    return dict(side=side, entry=entry, stop=stop, risk=risk, exit=exit_px, why=why,
                gross_R=gross_pts / risk, R=(gross_pts - COST) / risk)


def run(m1: pd.DataFrame, variant: str) -> tuple[pd.DataFrame, int]:
    """Returns (trades, eligible weekdays)."""
    out, widths, eligible = [], [], 0
    for d, g in m1.groupby(m1.index.normalize()):
        if d.weekday() >= 5:
            continue
        orr = opening_range(g)
        if orr is None:
            continue
        eligible += 1
        orh, orl = orr
        w = orh - orl
        prior = widths[-20:]
        widths.append(w)
        if variant == "C" and (len(prior) < 20 or not w < float(np.median(prior))):
            continue
        r = trade_day(g, orh, orl, variant)
        if r:
            r["day"] = d
            r["W"] = w
            out.append(r)
    return pd.DataFrame(out), eligible


# -- statistics ---------------------------------------------------------------
def summarize(t: pd.DataFrame, eligible: int, seed: int = 0) -> dict:
    from ledger_gate import one_sided_lb, alpha_z
    x = t["R"].to_numpy()
    rng = np.random.default_rng(seed)
    boots = np.array([rng.choice(x, x.size).mean() for _ in range(10_000)])
    years = (t["day"].max() - t["day"].min()).days / 365.25
    alpha, z = alpha_z(N_AFTER)
    lb_boot, draws = one_sided_lb(x, t["day"].dt.date.astype(str).to_numpy(), N_AFTER, seed=seed)
    lb_norm = x.mean() - z * x.std(ddof=1) / np.sqrt(x.size)
    return dict(n=int(x.size), per_year=x.size / years, per_day=x.size / eligible,
                gross=float(t["gross_R"].mean()), net=float(x.mean()),
                p5=float(np.percentile(boots, 5)), lb_boot=lb_boot, draws=draws,
                lb_norm=float(lb_norm), z=z, med_risk=float(t["risk"].median()),
                long=(int((t.side > 0).sum()), float(t.loc[t.side > 0, "R"].mean())),
                short=(int((t.side < 0).sum()), float(t.loc[t.side < 0, "R"].mean())),
                exits=t["why"].value_counts(normalize=True).round(3).to_dict(),
                by_year=t.groupby(t["day"].dt.year)["R"].agg(["count", "mean"]))


# -- guards and modes ---------------------------------------------------------
def ledger_row_ok(ledger_id: str, path: Path = LEDGER) -> bool:
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["id"] == ledger_id:
                return (r["rules_fixed_before_test"].strip() == "yes"
                        and PREREG_SHA_PREFIX in r.get("notes", ""))
    return False


def feasibility(m1: pd.DataFrame) -> None:
    """Ex ante only: opening-range width W from bars 09:30..09:59. No outcome is read."""
    hm = m1.index.strftime("%H:%M")
    orb = m1[(hm >= "09:30") & (hm <= "09:59")]
    rows = []
    for d, g in orb.groupby(orb.index.normalize()):
        if d.weekday() >= 5:
            continue
        orr = opening_range(g)
        if orr:
            rows.append((d, orr[0] - orr[1], float(g["o"].iloc[0])))
    f = pd.DataFrame(rows, columns=["day", "W", "px"])
    f["W_pct"] = f["W"] / f["px"] * 100
    print(f"eligible weekdays {len(f)}  ({f.day.min().date()}..{f.day.max().date()})")
    print(f"W pt: median {f.W.median():.2f}  p25 {f.W.quantile(.25):.2f}  p75 {f.W.quantile(.75):.2f}")
    print(f"W % of price: median {f.W_pct.median():.3f}")
    print(f"cost 0.6 pt as R at median W: {COST / f.W.median():.3f}")
    print(f"share of days with W >= 15 ES-equivalent pt scaled by price "
          f"(W% >= 15/4000*100 = 0.375%): {(f.W_pct >= 0.375).mean():.3f}")
    print("median W pt by year:", f.groupby(f.day.dt.year)["W"].median().round(2).to_dict())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger-id")
    ap.add_argument("--feasibility", action="store_true")
    a = ap.parse_args(argv)
    m1 = tj.load_minutes()
    if a.feasibility:
        feasibility(m1)
        return 0
    if not a.ledger_id or not ledger_row_ok(a.ledger_id):
        print("REFUSED: no ledger row with rules_fixed_before_test=yes citing prereg sha256 "
              f"{PREREG_SHA_PREFIX}. ORG.md day-2 rule. Not run.")
        return 2
    for v in VARIANTS:
        t, elig = run(m1, v)
        s = summarize(t, elig)
        print(f"{v}: n={s['n']} {s['per_year']:.1f}/yr {s['per_day']:.3f}/day  gross {s['gross']:+.4f}R  "
              f"net {s['net']:+.4f}R  p5 {s['p5']:+.4f}  LB(boot,{s['draws']}) {s['lb_boot']:+.4f}  "
              f"LB(norm,z={s['z']:.3f}) {s['lb_norm']:+.4f}  med risk {s['med_risk']:.2f} pt")
        print(f"   long {s['long']}  short {s['short']}  exits {s['exits']}")
        print("   by year:", {int(y): (int(r['count']), round(r['mean'], 4))
                              for y, r in s["by_year"].iterrows()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
