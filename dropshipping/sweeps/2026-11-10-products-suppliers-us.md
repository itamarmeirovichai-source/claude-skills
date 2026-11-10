# Sweep 2 (2026-11-10): products and suppliers for US delivery

Constraint carried in from sweep 1: only suppliers with US-warehouse stock or a landed cost known at order time (DDP). Fee stack from sweep 1. Operator: 15, 10–15 h/week, mother holds accounts.

## תקציר בעברית
1. **ספקים.** AutoDS לבדו אינו מחסן: הוא שכבת אוטומציה מעל 30 ספקים, ו"מחסן AutoDS" שלו בסין. ספקים עם מחסן בארה"ב שנגישים דרכו: Walmart, Target, Wayfair, Home Depot, Lowe's, Costco, Costway ועוד (קמעונאים אמריקאים), ו-CJdropshipping (מחסן בארה"ב, 4–8 ימים לפי מקורות משניים). Zendrop מצהיר רשמית 3–5 ימי עסקים ממחסן בארה"ב ו-10–15 מסין, אך רק חלק מהקטלוג במחסן האמריקאי ומחיריו גבוהים (ביקורת). Spocket: $39.99–$99.99 לחודש, 80% ספקים בארה"ב/אירופה לפי הספק עצמו. הדפסה-לפי-דרישה (Printful): ייצור 2–5 ימי עסקים + משלוח 3–4, חולצה ≈ $10.5–13.5 + $4.95 משלוח.
2. **קמעונאים אמריקאים כספק (Amazon/Walmart).** Amazon אוסר לקנות ממנו ולשלוח ללקוח של חנות אחרת ("retail arbitrage"); המקור הרשמי דורש התחברות, והכלל מצוטט מפורומים של Amazon. **Amazon יוצא מרשימת הספקים.** Walmart/Target: תנאי שימוש לא נבדקו; נבדקים לפני שימוש.
3. **איך מוצאים מוצר.** השיטה היחידה שחינמית, ציבורית ולא תלויה בכלי: ספריית המודעות של Meta, חיפוש מודעות פעילות ותאריך התחלה; מודעה שרצה שבועות היא סימן (לא הוכחה) שהיא רווחית. אין מחקר עצמאי שמאמת את זה, ומוכרי הכלים מודים שהכלים שלהם מזינים את אותם "מוצרים מנצחים" לכולם, כלומר הכלי עצמו יוצר רוויה. לכן: ספרייה ביד, לא כלי בתשלום, ומוצרים עם זווית משלנו.
4. **מה לא מוכרים.** בריאות/הרזיה/תוספים (Meta 18+ וטענות), מוצרים לילדים עד 12 (CPSC דורש תעודה ובדיקת מעבדה), סוללות ליתיום (מגבלות דואר), מותגים ודמויות (זכויות), ביגוד במידות (החזרות 24–40%). ממוצע החזרות אונליין בארה"ב 2025: 19.3% (NRF), כלומר ה-8% שבמודל נדיב מדי לביגוד ושמרני למוצרי בית.
5. **הצעד למפעיל.** סריקת ספריית מודעות ידנית לפי ה-runbook, 10 מועמדים עם ראיות. $0.

## Searched
AutoDS suppliers and help center; Zendrop and Spocket and Printful/Printify pricing and delivery; CJdropshipping (site behind a validation page); Amazon drop-shipping policy (login wall; forums); Meta Ad Library pages; product-discovery methods and their critics; CPSC children's products; USPS Publication 52 lithium rules; NRF 2025 returns; return rates by category.
Refused or empty: AutoDS supplier-regions article (404 at both URLs; regions quoted from search snippet), CJdropshipping (bot validation), Amazon Seller Central policy (login), Ad Library UI (403), voc.ai dissent piece (500).

## Sources in this area (27; primary 12; dissenting 3)
Carried: S-05, S-08, S-34, S-35, S-46, S-47, S-50. New: S-54..S-73 in `../sources.md`.
Primary: S-54 (AutoDS suppliers page), S-55 (AutoDS sourcing article), S-56 (Zendrop support), S-57 (Printful shipping), S-58 (Printify pricing), S-59 (Spocket pricing), S-60 (CPSC), S-61 (USPS PI 9D), S-62 (NRF), S-63/S-64 (Meta Ad Library pages), S-65 (Shopify AUP). Dissenting: S-67 (Zendrop prices "way too high"), S-70 (research tools feed everyone the same winners), S-45 (carried).

## Findings

### A. Supplier routes that satisfy the sweep-1 constraint
| Route | Ships from | Stated delivery to US | Cost structure | Evidence | Verdict |
|---|---|---|---|---|---|
| AutoDS → US retailers (Walmart, Target, Wayfair, Home Depot, Lowe's, Costco, Costway, Sam's Club, Macy's, Kohl's) | US | retailer's own (not stated by AutoDS) | retail price + AutoDS plan; thin margin; account/ToS risk per retailer | S-54, S-66 | eligible only after each retailer's resale terms are read (Phase 2 unit); Amazon excluded (S-71) |
| AutoDS → CJdropshipping | China + US warehouses | 4–8 days from US warehouse (secondary) | product + shipping, no plan fee claimed | S-54, S-66 | eligible for SKUs stocked in the US; verify per SKU on CJ (site behind bot check for the program; operator reads) |
| AutoDS Private Suppliers / "AutoDS Warehouse" / sourcing service | China | not stated; "longer than regional suppliers"; processing 3–5 business days | prepaid Managed Balance; 1 AO credit per sourcing request | S-55 | **excluded** (China-direct, duties and 10–15+ days) |
| Zendrop | China + US 3PL | 3–5 business days US-warehouse; 10–15 China; displayed 8.5-day figure is a blend | Flex $29–79/mo by linked products, Pro $49, Plus $79 (review, Oct 2026); product prices criticised as high | S-56, S-67 | eligible for US-stocked SKUs; cost check per SKU |
| Spocket | ~80% US/EU suppliers (vendor claim) | 2–5 days (vendor/affiliate claims, unmeasured) | Starter $39.99, Professional $59.99 ($24 annual), Empire $99.99, 7-day trial | S-59, S-68 | eligible; plan fee is a fixed cost the ledger must carry; rating 3.7–3.9/5 |
| Print-on-demand (Printful / Printify) | US print partners | Printful: 2–5 business days production + 3–4 days flat-rate shipping; first shirt $4.95 shipping +$2.20 each | tee base ≈ $10.5–13.5 (Printful) / $8.8–9.95 (Printify); Printify Premium $39/mo for up to 20–33% product discount | S-57, S-58 | eligible as the "expansionist" family from the council: no duties, no stock, but a design is the product |

### B. Supplier exclusions
- Amazon as supplier: Amazon's drop-shipping policy (login-walled; quoted via its seller forums) prohibits "purchasing products from another online retailer and having that retailer ship directly to customers" and requires the seller of record to be visible; violations hit account health (S-71). Excluded.
- Any China-direct route without prepaid, itemised duty (S-35, S-50): excluded.
- Routes whose delivery estimate is a blend (Zendrop's 8.5-day figure): use the per-SKU "ships from" field, never the blended number (S-56).

### C. How products are found, and what the evidence is worth
- Meta Ad Library: "People can search for all active ads running across products from Meta" (S-64); commercial ads show active status and start date; detailed spend/reach only for political ads (S-63). It is free and public.
- The longevity heuristic ("an ad running ≥ 3–8 weeks is probably profitable") is universal in vendor guides and has no independent validation (S-69). A long run can also be a big brand's budget or an unpaused loser. It is a screening signal, not evidence.
- Tool vendors concede that their tools feed the same "winners" to all users and that this "often leads to saturation" (S-70). Dissent accepted: the program does not buy a product-research tool at this stage; the research line stays at $0.
- Consequence for the registry: a P- hypothesis needs (1) ≥ 2 advertisers running the product ≥ 21 days in the Ad Library (demand exists), (2) ≤ 5 advertisers running it in the US (not saturated), (3) a US-warehouse or DDP supplier with a per-SKU landed cost, (4) a price at which contribution before ads ≥ 55% of price, (5) none of the exclusions in D.

### D. Category exclusions (law 17)
| Category | Rule | Source |
|---|---|---|
| Health, weight loss, supplements, "before/after", personal-attribute targeting | Meta requires 18+ targeting and bans implied personal attributes and misleading health claims | S-08 |
| Products for children ≤ 12 | CPSC: Children's Product Certificate and third-party testing required; an importer/seller without it is exposed | S-60 |
| Lithium-ion battery products | USPS: ≤ 20 Wh/cell, ≤ 100 Wh/battery, ≤ 8 cells or 2 batteries per mailpiece with equipment; batteries alone surface-only; UN3481 marking | S-61 |
| Branded, character, "dupe" or lookalike goods | Shopify AUP: nothing illegal where you do business; IP rights holders can dispute; account-level action | S-65 |
| Apparel with sizing | return rates 24–40%, fit drives up to 70% of returns | S-72 |
| Anything requiring delivery promises the supplier cannot meet | FTC 30-day rule, 7-working-day refunds | S-34 |
Return-rate inputs for the model: US online return rate 19.3% of online sales (NRF 2025, S-62); the Phase 0 8% allowance is replaced by category-specific allowances: home/garden 15–20%, electronics 8–10%, apparel 24–40% (S-72, secondary).

### E. Candidate families (overlay §3.3; SKUs come from the operator's Ad Library scan)
| Family | Mechanism (one sentence a skeptic could test) | Who exploits it | Cost to test | Prior P(pass M1) | Negative looks like |
|---|---|---|---|---|---|
| F1 Home / kitchen problem-solvers, US-stocked (CJ/Zendrop/Spocket US SKUs) | a demonstrable before-and-use video stops the scroll and the buyer pays a convenience premium for 3–5-day delivery | most Meta dropshippers (S-69) | $120 ad test + $20–40 sample | 10–15% | no add-to-cart by $60; CPA above $30 |
| F2 Pet accessories, US-stocked | pet owners buy on emotion, low return rates, no sizing | Spocket pet reviewers (S-68) | same | 10–15% | same |
| F3 Car / garage gadgets, US-stocked | male 25–55 US audience, utility demo video | common | same | 8–12% | same |
| F4 Print-on-demand niche apparel/mugs (Printful/Printify) | identity-driven design sells to a tight community at 2–3x base cost with no duties | POD sellers | $0 sample optional, $120 ad test | 5–10% (apparel returns, design risk) | CTR < 1%, no purchases by $80 |
| F5 Seasonal US retail items via AutoDS US retailers | fast delivery from Walmart/Target; margin only if retailer price < 50% of a plausible ad-driven price | AutoDS users | needs retailer-terms check first | Unknown until terms read | retailer cancels orders or bans account |
Excluded families: anything China-direct; electronics with lithium cells; children's; health; branded.
Portfolio note: 5 serial tests of $120 fit the $900 M1 cap only if M0 costs ≤ $300; P(at least one passes) at 10–15% each ≈ 41–56%.

## Runbook draft: `runbooks/ad-library-scan.md` (manual, operator, $0)
Written alongside this sweep. Output: a table of 10 candidates with advertiser, start date, days running, number of US advertisers, supplier found (US-warehouse SKU link), landed cost, proposed price, contribution share.

## Research synthesis block
```
Searched: supplier routes with US stock; delivery times; plan fees; discovery methods and their critics; exclusions by platform policy, safety and shipping rules; return rates.
Strongest sources: Zendrop support article (S-56, primary, defines the 3–5 vs 10–15 day split); Printful shipping page (S-57, primary, exact fees and lead times); AutoDS sourcing article (S-55, primary, confirms AutoDS's own stock ships from China); NRF 2025 returns (S-62, primary survey); CPSC and USPS pages (S-60, S-61, primary rules).
Candidates found: 5 families; 0 previously failed; SKUs pending the operator's scan.
Patterns: every "fast US delivery" route costs either a plan fee ($29–100/mo) or a retailer-margin squeeze; the free discovery method is the Ad Library; tool vendors admit tools create saturation.
Failure modes specific to this field: blended delivery estimates; retail-arbitrage account bans; return rates 2–5x the Phase 0 allowance in apparel; AutoDS add-ons that auto-renew without refund (S-05).
Cumulative P(any passes): 41–56% for 5 serial tests at 10–15% each; floor 5% not breached.
Assumptions and gaps: per-SKU landed costs (operator reads CJ/Zendrop/Spocket catalogs, which block the program); Walmart/Target resale terms; CJ US-warehouse delivery measured by a sample order at M0.
```

## Right-For-You check for the instruction that follows
```
Instruction:         Operator runs the Ad Library scan runbook (runbooks/ad-library-scan.md) for 3–5 hours this week and fills the 10-row candidate table
Who acts:            operator (program drafted the runbook and reviews the table)
Legal and policy:    Ad Library is public (S-64); no account needed to search; no purchase; no data scraping tools
Cost:                $0 external; 3–5 operator hours; ledger unchanged
Expected value:      turns 5 families into concrete P- candidates with evidence; without it Phase 2 cannot open
Reversible?          yes
Evidence:            Observed (S-63, S-64) that the library shows active commercial ads and start dates
What makes it wrong: if the library requires login or hides start dates in the operator's region, the runbook falls back to the operator's mother's account, logged
Cheaper alternative: none (already $0)
Verdict:             advise
```
