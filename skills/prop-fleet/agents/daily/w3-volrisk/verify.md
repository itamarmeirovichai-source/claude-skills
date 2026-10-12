# F2 (wave 3) verification

Verifier, 12 Oct 2026. I re-ran the numbers independently. I edited no existing files and made no commits.
The scratch scripts are in `/tmp/claude-0/f2-verify/`: `jobs.py` runs the simulations and
`tables_check.py` checks the tables. The total compute was about 5 CPU-minutes on 4 cores.

**Overall: PASS on all six checks.** The only thing to flag is in check 6: a wording point about the lottery rule, which does not change any result.

## 1. Unit tests: PASS

| Folder | Result |
|---|---|
| `agents/daily/w3-volrisk` | 21 passed |
| `agents/daily/w1-prop` | 14 passed |

## 2. Exact re-computation with the same seeds: PASS

For each cell I called `eval_sim` (seed 11), `funded_sim` (seed 12), `economics(E=, Fd=)` and `capped`.
The firm parameters and stress settings came from `scenarios.firm_params` / `scen_stress`, with n = 3000.

| Scenario | Firm | S | Cap | results.json | Recomputed | Match |
|---|---|---|---|---|---|---|
| F2-01 | FTMO | 1.5 | 12% | 12,003.772894 (σ 12/12) | 12,003.772894 (σ 12/12) | exact |
| F2-01 | FTMO | 1.5 | 20% | 21,055.445465 (σ 20/20) | 21,055.445465 (σ 20/20) | exact |
| F2-12 | FTMO | 1.5 | 20% | 20,639.011890 (σ 20/20) | 20,639.011890 (σ 20/20) | exact |
| F2-12 | CFT | 1.75 | 20% | 21,240.871395 (σ 20/20) | 21,240.871395 (σ 20/20) | exact |
| F2-07 | Blue Guardian | 1.0 | 12% | 4,016.245605 (σ 12/8) | 4,016.245605 (σ 12/8) | exact |

Every cap of these four jobs also matches bit for bit: 20 of 20 cells, including the chosen (σ_e, σ_f) pair.

## 3. Independent check with D1's own `prop_model.economics`: PASS

This check uses a different method. It runs D1's code with the σ grid itself restricted to ≤ the cap, instead of masking the full grid. A different grid shape gives different random draws, and n = 3000.

| S | Cap | D1 restricted grid | F2-01 | Difference | Synthesis (n = 1500) | Difference |
|---|---|---|---|---|---|---|
| 1.5 | 12% | 12,156 | 12,004 | +1.3% | 12.1k | +0.5% |
| 1.5 | 20% | 21,147 | 21,055 | +0.4% | 20.6k | +2.7% |
| 2.5 | 12% | 20,853 | 20,718 | +0.7% | 20.9k | −0.2% |
| 2.5 | 20% | 36,442 | 36,190 | +0.7% | 35.9k | +1.5% |

- All differences are within about 3%, which is consistent with Monte Carlo noise.
- Every run chose the σ pair at the cap.

## 4. "Sharpe needed for $20k" and monotonicity: PASS

FTMO F2-12, interpolated linearly on the S grid from `results.json`:

| Cap | Bracketing points | My crossing | tables.md |
|---|---|---|---|
| 12% | S 2.25 → $18,241; S 2.5 → $20,520 | 2.44 | 2.44 |
| 15% | S 1.75 → $17,637; S 2.0 → $20,506 | 1.96 | 1.96 |
| 20% | S 1.25 → $16,915; S 1.5 → $20,639 | 1.46 (1.457) | 1.46 |

Monotonicity: for F2-12, net $ never falls as S rises along the grid 0 to 3.5, for any of the 3 firms at any of the 5 caps. There are no non-monotone steps. F2-13 is also monotone.

## 5. Seed robustness of the headline (F2-12, FTMO, cap 20%): PASS

| S | Seed 11/12 (results.json) | Seed 101/102 |
|---|---|---|
| 1.25 | 16,915 | 17,043 |
| 1.5 | 20,639 | 20,735 |
| 1.75 | 24,372 | 24,615 |

- The $20k crossing is at S = 1.457 with seed 11 and S = 1.450 with seed 101.
- That is a shift of 0.007 Sharpe, well under the 0.1 threshold.

## 6. Decision table and lottery table: PASS (with one note)

**Decision table** (better of F2-12 / F2-13):
- All 60 cells match `results.json`, including the (12)/(13) labels.
- The "decision" rows of the Sharpe table also match for all 15 cells. All other rows of that table (F2-01, F2-09, F2-12, F2-13) match as well.
- F2-12 beats F2-13 everywhere except one point on the full S grid: CFT at S = 3.5, no cap. That point falls outside the S values shown in the table and has no effect on any crossing.

**Lottery table:** every cell reproduces exactly, and so does the "survives?" column.

| Firm | Survives? | F2-12 renewal-reward net / years-2-3 median |
|---|---|---|
| FTMO | yes | +6,956 / +4,770 |
| Blue Guardian | yes | +5,237 / +3,854 |
| CFT | no | +1,173 / −99 |

**Note on how the lottery rule is applied:** the script picks the variant with the higher renewal-reward net and then requires both its numbers to be positive. A looser reading, "either variant has both numbers positive", gives the same verdict for all three firms. So the wording does not change the result.
