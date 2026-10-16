#!/usr/bin/env python3
"""Statistician audit 2026-10-05: ledger N, bootstrap coverage, look-ahead.

Run:  python3 skills/prop-fleet/agents/daily/2026-10-05/statistician/audit.py
Reads the ledger, the reference run logs and the scripts; re-uses the cached
SPXUSD 1m files that tjr_backtest.load_minutes() keeps in scratch.

Part 4 re-runs ONLY the already-run IBS variant A (builder, today) with one
bug fixed (trade-day validity must not use the trade day's own bars). It adds
no new rule, threshold or filter. Whether it counts toward N is the director's
call; it is reported as a look-ahead perturbation, not as a result.
"""
from __future__ import annotations

import ast
import csv
import re
import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
PF = HERE.parents[4]                       # skills/prop-fleet
sys.path.insert(0, str(PF / "scripts"))
sys.path.insert(0, str(HERE.parents[1]))   # daily/2026-10-05 (hypothesis.py)
import tjr_backtest as tj                  # noqa: E402
import hypothesis as ibs                   # noqa: E402


def z(n):
    return NormalDist().inv_cdf(1 - 0.05 / n)


# 1. N ----------------------------------------------------------------------
print("== 1. ledger N")
rows = list(csv.DictReader(open(PF / "agents" / "ledger.csv")))
bad = [r["id"] for r in rows if not re.fullmatch(r"[1-9]\d*", r["count"] or "")]
ids = [r["id"] for r in rows]
N = sum(int(r["count"]) for r in rows)
print(f"rows {len(rows)}  N = {N}  non-integer/<1 counts: {bad}  "
      f"duplicate ids: {sorted({i for i in ids if ids.count(i) > 1})}")
print("rows with a mean but no p5:", [r["id"] for r in rows
                                     if r["result_mean_R"] and not r["result_p5_R"]])
print("rows with neither mean nor p5:", [r["id"] for r in rows
                                        if not r["result_mean_R"] and not r["result_p5_R"]
                                        and r["passed_gate"] != "pending"])

# stack-run.txt: rows printed per section vs H0009 count
txt = (PF / "references" / "stack-run.txt").read_text().splitlines()
fut_stacks = [l.split("  ")[1].strip() for l in txt
              if re.match(r"\s+(tsmom|xsmom|value|6040|trend|overnight)( \+ \w+)+\s+\d", l)]
print("multi-component stacks printed in stack-run.txt:", len(fut_stacks), fut_stacks)

# replay.py / diagnose_edge.py grids (legacy H0002 has count 1)
src = (PF / "scripts" / "replay.py").read_text()
grids = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(src).body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
         and n.targets[0].id in ("RR_GRID", "TRAIL_GRID")}
print("replay.py grids:", grids)
de = (PF / "scripts" / "diagnose_edge.py").read_text()
print("diagnose_edge.candidates drop_bucket calls:",
      de.split("def candidates")[1].split("def target_reach")[0].count("drop_bucket(")
      - 0, "(one of them inside a 3-value loop)")

# 2. z at plausible N ---------------------------------------------------------
print("\n== 2. one-sided Bonferroni z")
for n in (173, 176, 178, 193):
    a = 0.05 / n
    print(f"N={n}: alpha {a:.2e}  z {z(n):.3f}  expected bootstrap draws below "
          f"that quantile with 5000 draws: {5000 * a:.2f}")

# 3. IBS (today) — staleness and trade-day validity -------------------------
print("\n== 3. IBS builder run: session filter")
m1 = tj.load_minutes()
sess = ibs.sessions(m1)
sig = ibs.signals(sess)
pos = {s["day"]: i for i, s in enumerate(sess)}
gaps = np.array([(sess[pos[s["day"]]]["day"] - sess[pos[s["day"]] - 1]["day"]).days
                 for s in sig])
print(f"signals {len(sig)}; previous valid session > 4 calendar days back: "
      f"{(gaps > 4).sum()} ({(gaps > 4).mean():.1%}); > 30 days: {(gaps > 30).sum()}; "
      f"max {gaps.max()} days")
atr_span = np.array([(sess[pos[s['day']] - 1]['day'] - sess[pos[s['day']] - 14]['day']).days
                     for s in sig])
print(f"ATR14 window span in calendar days: median {np.median(atr_span):.0f}, "
      f"p95 {np.percentile(atr_span, 95):.0f}, max {atr_span.max()}")

# trade-day validity uses the trade day's own full-session bar count (>=370) and
# its 15:59 bar: information not available at 09:31.
hm = m1.index.strftime("%H:%M")
rth = m1[(hm >= "09:30") & (hm <= "15:59")]
cnt = rth.groupby(rth.index.normalize()).size()
valid_days = {s["day"] for s in sess}
cand = []          # (day, prev valid session) for weekdays with a 09:31 bar
vlist = [s["day"] for s in sess]
vi = 0
for d, g in rth.groupby(rth.index.normalize()):
    if d.weekday() >= 5:
        continue
    ghm = g.index.strftime("%H:%M")
    if "09:31" not in ghm:
        continue
    while vi < len(vlist) and vlist[vi] < d:
        vi += 1
    if vi < 14:
        continue
    cand.append((d, vi, g[ghm >= "09:31"]))
print(f"weekdays with a 09:31 bar and >=14 prior valid sessions: {len(cand)}; "
      f"of them 'valid' by the trade-day filter: {sum(d in valid_days for d, _, _ in cand)}")

# 4. perturbation: variant A with ex-ante trade-day eligibility ---------------
print("\n== 4. look-ahead perturbation, variant A only (k=0.5, both sides)")
alt = []
for d, vi, bars in cand:
    p = sess[vi - 1]
    if p["H"] == p["L"]:
        continue
    x = (p["C"] - p["L"]) / (p["H"] - p["L"])
    side = 1 if x <= ibs.LO else (-1 if x >= ibs.HI else 0)
    if not side:
        continue
    atr = float(np.mean([s["H"] - s["L"] for s in sess[vi - 14:vi]]))
    r = ibs.trade(dict(day=d, ibs=x, atr=atr, side=side, bars=bars), 0.5)
    if r:
        r["in_builder_set"] = d in valid_days
        alt.append(r)
t = pd.DataFrame(alt)
for lab, sub in (("ex-ante eligible (all)", t),
                 ("  of which builder-valid", t[t.in_builder_set]),
                 ("  of which dropped by trade-day filter", t[~t.in_builder_set])):
    x = sub["R"].values
    lo, _, _ = tj.boot_mean(x)
    print(f"{lab:<40} n {len(x):4d}  net mean {x.mean():+.4f}R  boot p5 {lo:+.4f}  "
          f"gross {sub['gross_R'].mean():+.4f}R  stop rate {(sub.why == 'stop').mean():.3f}")

# 5. bootstrap lower bound at alpha = 0.05/N with enough draws ----------------
print("\n== 5. builder variant A: normal vs bootstrap lower bound at 0.05/176")
b = pd.DataFrame([ibs.trade(s, 0.5) for s in sig])
b = b[b.notna().all(axis=1)]
x = b["R"].values
rng = np.random.default_rng(0)
B = 200_000
means = np.concatenate([rng.choice(x, size=(20_000, len(x))).mean(axis=1)
                        for _ in range(B // 20_000)])
a = 0.05 / 176
print(f"n {len(x)}  mean {x.mean():+.4f}  normal LB {x.mean() - z(176) * x.std(ddof=1) / np.sqrt(len(x)):+.4f}  "
      f"bootstrap LB ({B} draws) {np.quantile(means, a):+.4f}  "
      f"draws below it {int((means < np.quantile(means, a)).sum())}")

yrs = (t["day"].max() - t["day"].min()).days / 365.25
print(f"\nperturbation set span {t['day'].min().date()}..{t['day'].max().date()}  "
      f"trades/yr {len(t) / yrs:.1f}")
