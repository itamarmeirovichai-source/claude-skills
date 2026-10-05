"""Gate rule 3 draft (head of engineering, 2026-10-05). Staged here because only
scripts/ owners may edit scripts/gate.py; port it there with these tests.

- ledger_n(path): N = sum of the ledger `count` column; every cell must match
  ^[1-9]\\d*$ (finalize.py:68 currently turns '' into 1 and lets 0/neg through).
- one_sided_lb(r, days, n): day-clustered bootstrap lower bound of mean R at
  alpha = 0.05/N, one-sided, with >= 50/alpha draws (boot_mean's 5000 iid draws
  cannot resolve that quantile), drawn in chunks to bound memory.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from statistics import NormalDist

import numpy as np

COUNT_RE = re.compile(r"^[1-9]\d*$")


def ledger_n(path: str | Path) -> int:
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    bad = [r.get("id", "?") for r in rows if not COUNT_RE.match((r.get("count") or "").strip())]
    if bad:
        raise ValueError(f"ledger rows with invalid count: {bad}")
    return sum(int(r["count"]) for r in rows)


def alpha_z(n: int, family_alpha: float = 0.05) -> tuple[float, float]:
    a = family_alpha / n
    return a, NormalDist().inv_cdf(1 - a)


def one_sided_lb(r, days, n: int, seed: int = 0, chunk: int = 20_000,
                 min_per_tail: int = 50) -> tuple[float, int]:
    """Day-clustered bootstrap: resample whole days, mean R per trade."""
    r = np.asarray(r, float)
    days = np.asarray(days)
    if r.size == 0 or r.size != days.size:
        raise ValueError("r and days must be the same non-zero length")
    alpha, _ = alpha_z(n)
    draws = int(np.ceil(min_per_tail / alpha))
    uniq, inv = np.unique(days, return_inverse=True)
    sums = np.bincount(inv, weights=r)
    cnts = np.bincount(inv).astype(float)
    k = uniq.size
    rng = np.random.default_rng(seed)
    out = np.empty(draws)
    for s in range(0, draws, chunk):
        m = min(chunk, draws - s)
        idx = rng.integers(0, k, size=(m, k))
        out[s:s + m] = sums[idx].sum(1) / cnts[idx].sum(1)
    return float(np.quantile(out, alpha)), draws


def passes_rule3(r, days, n: int, seed: int = 0) -> bool:
    lb, _ = one_sided_lb(r, days, n, seed=seed)
    return lb > 0
