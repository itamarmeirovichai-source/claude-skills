# Registry

Prefixes: `P-` products, `A-` ads and creatives, `C-` store and conversion, `O-` operations and automation, `L-` learning hypotheses.
An entry is frozen once its development run starts. A changed version is a new ID with a post-hoc penalty.
Bar for every P- entry (frozen in Phase 0, see `phase0/FRAME.md` §2.4): M1 = contribution margin > $0 per order over ≥ 30 orders and ≥ 14 days, reconciled between Shopify orders and processor payouts, refunds and chargebacks applied to their period. "Held direction but missed the bar" = FAIL.

| ID | Hypothesis (one sentence) | Family | Test / budget | Kill condition | Prior P(pass) | Status | Result file |
|---|---|---|---|---|---|---|---|
| (none yet) | Phase 2 opens after the Phase 1 sweeps | | | | | | |

## Cumulative count

| Cycle | Registered | Tested | Passed | Not tested | Contaminated |
|---|---|---|---|---|---|
| Phase 0 (2026-11-10) | 0 | 0 | 0 | 0 | 0 |
| Prior program (trading edge, operator-reported) | ~300 | ~300 | 0 | | |

## P- entry template (frozen rules from sweeps 1–4; copy verbatim into each product entry)

```
ID:                  P-00NN
Hypothesis:          <product> at $<price> to US buyers yields contribution margin > $0 per order after itemized costs, over ≥ 30 orders and ≥ 14 days (M1), within a $240 two-tranche test.
Family:              F1 home | F2 pet | F3 car/garage | F4 POD | F5 US-retailer (sweep 2 §E)
Mechanism:           one sentence a skeptic could test
Evidence of demand:  Ad Library: ≥ 2 advertisers ≥ 21 days, ≤ 5 US advertisers (runbook ad-library-scan); link + dates
Supplier:            US-warehouse or DDP only (sweep 1 §D); SKU link; landed cost $; stated delivery days; sample order date
Test design:         1 campaign, ABO, 1 ad set, US, broad, 2 creatives differing by hook type (rules C1, CR2), $20/day, 6 days = tranche 1 $120; tracking rule T1 passed before launch
Frictions included:  landed cost; gateway fee stack (Grow 3.35% + ₪59/mo or PayPal ~8.9% + ₪1.20); category refund allowance (home 15–20%, pet ~10%, electronics 8–10%, apparel 24–40%); Shopify $39 + platform plan share; VAT scenario 0% and 18% both shown
Control arm:         same creatives, $0 spend, 6 days: organic/noise baseline = 0 orders expected
Integrity checks:    planted fake order inserted into the reconciliation sheet and removed; Meta purchases vs Shopify orders vs payout reconciled; test/staff orders excluded
Bar:                 M1 as in FRAME §2.6, reconciled, both VAT scenarios reported
Stop rule:           computed per product with phase1/test_stop_rule.py (price, contribution); default T1 $120 continue only if purchases ≥ 5; T2 $120 M1-candidate only if purchases ≥ 3; early kill only: no add-to-cart by $60 or CTR < 0.5% at 2,000 impressions; hook < 20% at 1,000 impressions → replace hook, not product (ST1–ST4, CR1)
Kill condition:      fails T1 or T2; or supplier delivery > stated; or policy strike (law 17)
Maximum reads:       1 per tranche, logged in reads.log
Budget allotted:     $240 ads + sample ≤ $40; ledger entry before launch
Prior P(pass):       family prior from sweep 2 §E
```
Rules referenced: sweep 1 §A–D; sweep 2 §C–E; sweep 3 T1–T2, C1, L1–L2, S1, H1–H4, A1; sweep 4 ST1–ST4, CR1–CR3, D1–D3, TL1–TL2.
