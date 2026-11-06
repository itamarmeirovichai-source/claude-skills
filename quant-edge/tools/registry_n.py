#!/usr/bin/env python3
"""Print the running N, N_total and the fixed bar from quant-edge/registry.csv.

N_running = sum of the count column over every row (inherited + program).
N_total   = 280 (inherited) + VARIANT_BUDGET (150) = 430, fixed on Day 0; the bar never moves.
"""
import csv, math, sys
from statistics import NormalDist

INHERITED_N = 280
VARIANT_BUDGET = 150
N_TOTAL = INHERITED_N + VARIANT_BUDGET
ALPHA = 0.05 / N_TOTAL
Z_BAR = NormalDist().inv_cdf(1 - ALPHA)            # one-sided, sign fixed
Z_BAR_TWO_COUNT = NormalDist().inv_cdf(1 - 0.025 / N_TOTAL)  # sign not fixed (occupies two counts)
MIN_BOOT_DRAWS = int(math.ceil(50 / ALPHA))

def running_n(path):
    n = 0
    for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
        c = (r.get("count") or "").strip()
        if c == "":
            continue
        if not c.isdigit():
            raise ValueError(f"row {r.get('id')}: count {c!r} is not a non-negative integer")
        n += int(c)
    return n

def bar_sharpe_units(years):
    return Z_BAR / math.sqrt(years)

def power(true_sharpe, years):
    return 1 - NormalDist().cdf(Z_BAR - true_sharpe * math.sqrt(years))

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "quant-edge/registry.csv"
    n = running_n(path)
    print(f"N_running={n}  N_inherited={INHERITED_N}  program_variants_counted={n - INHERITED_N}  budget_left={N_TOTAL - n}")
    print(f"N_total={N_TOTAL}  alpha={ALPHA:.6g}  z_bar={Z_BAR:.4f}  z_bar_two_count={Z_BAR_TWO_COUNT:.4f}  min_bootstrap_draws={MIN_BOOT_DRAWS}")
    for T in (1.83, 3, 5, 8, 10):
        print(f"  OOS {T:>4} years: bar {bar_sharpe_units(T):.3f} Sharpe; power at S=1.5/2.0/2.4: "
              f"{power(1.5, T):.2f}/{power(2.0, T):.2f}/{power(2.4, T):.2f}")
    if n > N_TOTAL:
        print("ERROR: running N exceeds N_total; the program has exhausted its variant budget", file=sys.stderr)
        sys.exit(2)
