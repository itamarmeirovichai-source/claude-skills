# Curriculum (iron law 14)

One row per source studied. The "what we now do differently" column is honest: "no change" is a valid entry.

| date | area | source | quality | what we now do differently | expected effect (size, where) | cost to apply | status |
|---|---|---|---|---|---|---|---|
| 2026-11-10 | finance | PayPal IL merchant fees (S-10) | primary | Unit economics use 3.4% + ₪1.20 + 1–2% cross-border + 2.5% FX, not the US 2.9% figure | correct breakeven ROAS by ~+0.05; avoids a false "profitable" | $0 | applied (in goal_math.py) |
| 2026-11-10 | finance | PayPal holds and reserves (S-11, S-12) | primary | Cash model assumes 21-day hold on first sales and a possible rolling reserve; scaling cap tied to cash on hand | prevents over-scaling into a hold | $0 | applied (in goal_math.py) |
| 2026-11-10 | ops | Shopify Payments country list (S-02) | primary | Israel path is a third-party gateway + 2% Shopify fee on Basic; M0 includes a gateway-selection unit | M0 blocker identified before spend | $0 | applied (frame) |
| 2026-11-10 | ads | Meta learning phase, practitioner consensus (S-29) | secondary | Product tests are sized so an ad set can plausibly reach ~50 events/7 days or are read as learning-limited data; budget steps ≤ 20–30% | fewer learning resets per test | $0 | queued (primary page pending) |
| 2026-11-10 | policy | Meta Advertising Standards (S-08) | primary | Health/weight-loss, before/after and personal-attribute products are excluded from the candidate list; AI creative is labeled where Meta labels it, no evasion | avoids strikes counted as losses under law 17 | $0 | applied (frame) |
| 2026-11-10 | tax | Exempt-dealer ceiling 2026 ₪122,833 (S-21, secondary) | secondary | Registration decision waits for accountant; revenue crossing the ceiling in-year is a planned event, not a surprise | no retroactive VAT exposure | accountant fee TBD | queued |
| 2026-11-10 | outside view | Failure-rate search (S-20) | secondary | The "90% fail" number is not used; the frame uses a sensitivity table instead | honest base-rate line | $0 | applied (frame) |
| 2026-11-10 | tax | Exempt-dealer ceiling vs. revenue path (S-21, S-22, S-33) | secondary | Unit economics carry a VAT scenario (0% vs 18% on US sales) until the accountant answers; breakeven ROAS shown both ways (1.80 / ~2.45) | prevents calling a product "passing" that fails under VAT | $0 | applied (sweep 1) |
| 2026-11-10 | ops | CBP postal duty rule: duties remitted by carriers/qualified parties, not collected from addressees (S-50) | primary | Supplier shortlist restricted to US-warehouse or DDP so the landed cost is known at order time; express routes that bill the consignee excluded | avoids refund spiral under FTC 30-day rule and PayPal disputes | $0 | applied (sweep 1) |
| 2026-11-10 | finance | Israeli gateway fee stacks (S-37, S-38) | practitioner | Fee line per gateway in the model: Grow 3.35% + ₪59/mo; PayPal ~8.9% + ₪1.20 | correct breakeven by up to +0.15 ROAS for PayPal-heavy mixes | $0 | applied (sweep 1) |
| 2026-11-10 | ops | Owner/staff split on Shopify (S-01, S-52) | practitioner | Every onboarding instruction names the mother as owner and the operator as staff | removes a law-7 violation path | $0 | applied |
| 2026-11-10 | tax | US economic nexus (S-42, S-43, S-44) | primary+secondary | Annual January review of per-state sales; no registration below $100k/state | no change until scale | $0 | no change now |
