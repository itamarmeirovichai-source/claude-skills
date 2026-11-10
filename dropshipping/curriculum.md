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
