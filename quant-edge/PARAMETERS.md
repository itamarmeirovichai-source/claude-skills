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
