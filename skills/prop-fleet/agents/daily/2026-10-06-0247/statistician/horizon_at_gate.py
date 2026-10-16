#!/usr/bin/env python3
"""Statistician 2026-10-06: references/numbers.md:182-188 and scripts/detect.py:74-95 give the
days-with-a-trade needed for a POSITIVE LOWER BOUND using a two-sided 95% t quantile
(detect.py:86 `_tcrit(k-1)`). Gate rule 3 needs the one-sided 0.05/N bound. Same anchor
(detect.SE_MEASURED, 28 clusters), quantile replaced by z(0.05/N), N from the ledger.
Run from skills/prop-fleet/scripts."""
import sys, csv
from pathlib import Path
from statistics import NormalDist
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import detect as dt

here = Path(__file__).resolve()
N = sum(int(r["count"]) for r in csv.DictReader(open(here.parents[3] / "ledger.csv")))
z = NormalDist().inv_cdf(1 - 0.05 / N)
print(f"anchor SE {dt.SE_MEASURED:.4f}R at {dt.DAYS_MEASURED} clusters; N={N} z={z:.3f}")
for edge in (0.101, 0.200, 0.250, 0.300, 0.500):
    d95 = dt.days_to_clear(edge)
    k = 2
    while edge - z * dt.se_at(k) <= 0:
        k += 1
    print(f"  true {edge:+.3f}R: detect.py (t 95%) {d95} days -> gate z {k} days ({k / d95:.2f}x)")
