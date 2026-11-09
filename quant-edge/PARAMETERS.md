# Parameters (fixed on Day 0, 2026-11-03)

| parameter | value | note |
|---|---|---|
| TARGET_NET_USD_PER_100K_PER_YEAR | 20000 | net to Itamar after split, fees, resets, failed accounts, fleet-averaged |
| STRETCH_NET_USD_PER_100K_PER_YEAR | 30000 | |
| MAX_ANNUAL_VOL_ALLOWED | 20% | |
| DEADLINE_DATE | 2026-12-19 | |
| VARIANT_BUDGET | 150 | N_total = 280 + 150 = 430 |
| Bar | z(0.05/430) = 3.6807 one-sided; z(0.025/430) = 3.8538 for unfixed sign; ≥ 430,000 bootstrap draws | never lowered |
| DATABENTO_PLAN_CEILING_USD | min(94, confirmed remaining credit − 20) | set after Itamar confirms the credit |
| DATABENTO_HARD_CAP_USD | min(105, 85% of confirmed remaining credit) | the portal monthly limit Itamar sets |
| OTHER_SPENDING_ALLOWED_USD | 0 | |
| MAX_CONCURRENT_AGENTS | 4 read/write (Agent tool), 2 compute (Workflow tool) | lower on the first killed run |
| PROGRAM_ROOT | quant-edge/ | |
| DATA_ROOT | ~/quant-edge-data/ (= /root/quant-edge-data) | outside the repository |
| RESEARCH_BRANCH | **claude/keen-cori-fvtxcl** (changed from `quant-edge`) | see change record |
| REPORT_LANGUAGE | Hebrew to Itamar; English elsewhere | |
| WORKING_HOURS | continuous | |
| HOLDOUT | 2025-01-01 → plan purchase date; unlock 2026-12-05 via `quant-edge/HOLDOUT_UNLOCK` | |

## Derived numbers

| OOS length | bar in Sharpe units | power at true Sharpe 1.5 / 2.0 / 2.4 |
|---|---|---|
| 22 months (hold-out) | 2.72 | 0.05 / 0.16 / 0.33 |
| 3 years | 2.13 | 0.14 / 0.41 / 0.68 |
| 5 years | 1.65 | 0.37 / 0.79 / 0.95 |
| 8 years | 1.30 | 0.71 / 0.98 / 1.00 |
| 10 years | 1.16 | 0.86 / 1.00 / 1.00 |

Source: `tools/registry_n.py` (normal approximation, annualised Sharpe × √T).

## Change record

- 2026-11-03 RESEARCH_BRANCH `quant-edge` → `claude/keen-cori-fvtxcl`. Reason: the platform assigned this
  branch to the session and forbids pushing elsewhere without explicit permission. No derived number changes.

## Standards fixed on Day 0 after the Red Team pre-mortem (2026-11-03)

### Hold-out pass criterion (replaces "hold-out mean inside the OOS 90% confidence interval of the mean")

The criterion as written compares a 22-month mean against a 10-year interval that is 2.5× tighter than the hold-out's own
sampling error: a true edge with **no decay** passes it only 48% of the time, and an edge decayed to half passes 11%
(normal approximation, `scratchpad/holdout_power.py` by the Red Team, re-derived by the Director on Day 0). A criterion that
closes half of all true edges cannot be the deciding test. Restated, in the Phase-6 (one-sided tolerance) form:

A candidate passes the hold-out read if all three hold:
1. hold-out net mean > 0;
2. m_holdout ≥ h · m_oos − 1.28 · √(SE²_oos + SE²_holdout), where h is the decay haircut written in the row before the OOS read,
   and both standard errors use the Mertens/Opdyke formula with skew and kurtosis (day-clustered for trade-level series);
3. worst day and maximum drawdown inside the firm's rules, path-wise.

Pass probabilities (normal approximation, OOS 10 years, hold-out 2025-01-01..2026-10-31 ≈ 458 days):

| OOS Sharpe | haircut h | true edge, no decay | true edge decayed to h | dead edge (zero) |
|---|---|---|---|---|
| 2.4 | 0.5 | 0.998 | 0.91 | 0.41 |
| 2.4 | 0.7 | 0.99 | 0.91 | 0.20 |
| 3.0 | 0.5 | 1.00 | 0.91 | 0.27 |
| 3.0 | 0.7 | 0.99 | 0.91 | 0.08 |

A dead edge still passes 8–41% of the time: 22 months cannot do better, which is why forward paper trading (Phase 6) remains the
second confirmation and why S1 needs Gate 5 and the hold-out read together, never the hold-out alone.

### "Derivative" rule extended to published evidence

A row whose motivating evidence (paper, blog, forum curve) displays a window that overlaps the registered OOS is marked
"derivative" and is decided on markets or dates the evidence did not touch; the candidate brief carries an **evidence window**
field (markets × dates displayed). The published-mechanism haircut of 0.5 stays in any case.

### Joint power of the simulable criteria (`tools/joint_power.py`, 2,000 paths per cell, Student-t(4) daily P&L)

The Day-0 line "a real edge passes about 37% with five years and 86% with ten" is criterion 4 alone. Running criteria 3 (2× cost),
4 and 7 (years, concentration, terciles, ±25% neighbours, one-minute delay) together on a synthetic strategy whose costs are one
third of its gross edge:

| true net Sharpe | 5 years | 8 years | 10 years |
|---|---|---|---|
| 1.5 | 0.32 | 0.63 | 0.72 |
| 2.0 | 0.67 | 0.82 | 0.85 |
| 2.4 | 0.78 | 0.89 | 0.91 |
| 3.0 | 0.88 | 0.94 | 0.96 |

When costs are **half** of gross, the 2× cost criterion alone passes about 5% at every Sharpe, by construction: the program can only
certify strategies whose gross edge is at least about three times their round-trip cost. Criteria 6 (null models) are implied by 4 for a
benchmark-uncorrelated strategy; criteria 1, 2, 5, 8–12 are process criteria and were taken as passed. Every result file prints the
criterion-4 power and this joint figure for its own OOS length.

### Critical path (deadline 2026-12-19)

| date | what must be true |
|---|---|
| 2026-11-06 | 72-hour Databento trigger: if (a)+(b)+(c) are not confirmed, batch 1 is re-ordered toward free-data rows and the Hebrew report names the blocked rows |
| 2026-11-07 | sweep, pre-screen and batch-1 registrations done (Gate 1) |
| 2026-11-10 | Gate 2 for every batch-1 dataset |
| 2026-11-23 | batch testing (Gate 3) and verification (Gate 4) of batch 1–2 done |
| 2026-11-28 | Gate 5 PASS for any S1 candidate; paper trading (≥ 3 weeks or ≥ 60 trades, whichever is later) starts |
| 2026-12-05 | hold-out unlock: one run, every Gate-4 pass listed in `HOLDOUT_UNLOCK` |
| 2026-12-19 | decision memo |

P1 is available only to a variant with dated Gate-4 and Gate-5 PASS files older than its first paper fill and with its hold-out read done.
