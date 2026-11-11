# Registry

Prefixes: `P-` products, `A-` ads and creatives, `C-` store and conversion, `O-` operations and automation, `L-` learning hypotheses.
An entry is frozen once its development run starts. A changed version is a new ID with a post-hoc penalty.
Bar for every P- entry (frozen in Phase 0, see `phase0/FRAME.md` §2.4): M1 = contribution margin > $0 per order over ≥ 30 orders and ≥ 14 days, reconciled between Shopify orders and processor payouts, refunds and chargebacks applied to their period. "Held direction but missed the bar" = FAIL.

| ID | Hypothesis (one sentence) | Family | Test / budget | Kill condition | Prior P(pass) | Status | Result file |
|---|---|---|---|---|---|---|---|
| P-0001 | Candle warmer lamp (timer/dimmer) at $59.90 to US buyers yields contribution > $0 per order after itemized costs over ≥ 30 orders / ≥ 14 days | F1 home | T1 $120 (6 days, $20/day, ABO, 1 ad set, 2 creatives by hook type) → continue if purchases ≥ 4; T2 $120 → M1-candidate if purchases ≥ 3 (unit_economics.py: price 59.90, landed 22.00 est., home 17%, grow; share 0.429, breakeven ROAS 2.33; VAT-18% scenario share 0.27) | fails T1/T2; no ATC by $60; CTR < 0.5% at 2,000 impr.; stockout; policy strike | 10% | REGISTERED 2026-11-11, landed cost provisional until Doba/Eprolo sign-up (edit allowed before development run) | results/P-0001.md (pending) |
| P-0002 | Personalised/design elevated pet bowl at $49.90 yields contribution > $0 per order (M1 bar) | F2 pet | same design; T1 continue if ≥ 5; T2 $180 pass if ≥ 2 (price 49.90, landed 18.00 est., pet 10%; share 0.506, breakeven ROAS 1.98; VAT-18% share 0.35) | as above; supplier cannot personalise in US → kill the personalised variant (re-register as design-led before spend); any ad or page targeting large/giant breeds → stop | 10% | REGISTERED 2026-11-11, provisional landed cost; build package `runbooks/p-0002-build.md` 2026-11-11; **targeting restricted before any spend to small/medium dogs and cats, no health claims** (S-205) | results/P-0002.md (pending) |
| P-0003 | Timer-based 6-meal automatic pet feeder (no app) at $59.90 yields contribution > $0 per order (M1 bar) | F2 pet / electronics | same design; T1 continue if ≥ 4; T2 $120 pass if ≥ 3 (price 59.90, landed 26.00 est., electronics 9%; share 0.442, breakeven ROAS 2.26; VAT-18% share 0.29) | as above; US-warehouse SKU without UL/ETL mark → kill | 10% | REGISTERED 2026-11-11, provisional landed cost | results/P-0003.md (pending) |
| P-0004 | 6-pack rechargeable motion-sensor closet lights at $49.90 yields contribution > $0 per order (M1 bar) | F1 home | same design; T1 continue if ≥ 6; T2 $120 pass if ≥ 2 (price 49.90, landed 21.00 est. for 6, home 17%; share 0.376, breakeven ROAS 2.66) | as above; cells > 20 Wh or no UN3481 handling by supplier → kill | 12% | REGISTERED 2026-11-11, provisional landed cost; build package `runbooks/p-0004-build.md` 2026-11-11 (claims restricted to mount/battery/sensor facts; no safety claims) | results/P-0004.md (pending) |

## Fee basis changed 2026-11-11 before any development run: gateway = Shopify Payments (US), 2.9% + $0.30, no third-party fee. Recomputed shares: P-0001 0.429 (BE ROAS 2.33), P-0002 0.504 (1.98), P-0003 0.442 (2.26), P-0004 0.374 (2.67); stop rules unchanged.

## Test order (serial, overlay §3.3): P-0002 (highest share, lowest saturation) → P-0004 (strongest demand) → P-0003 → P-0001. Each starts only after the previous resolves. All four wait on M0 (store live, gateway, fulfillment tested on one real order). Evidence: S-166, S-167, S-169–S-173, S-177, S-181–S-186.

## Cumulative count

| Cycle | Registered | Tested | Passed | Not tested | Contaminated |
|---|---|---|---|---|---|
| Phase 0 (2026-11-10) | 0 | 0 | 0 | 0 | 0 |
| Phase 2 (2026-11-11) | 4 | 0 | 0 | 0 | 0 |
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
