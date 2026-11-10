# Sweep 1 (2026-11-10): finance, payments and registration from Israel for a US-facing store

Operator facts recorded before this sweep: operator is 15; mother will most likely hold every account and the business registration; an adult credit card and PayPal account exist; 10–15 operator hours/week. Destination market: United States.

## תקציר בעברית
1. **שערי סליקה.** Shopify Payments לא קיים בישראל. לפי שתי השוואות מתרגלים מסתיו 2026, ברשימת Shopify לישראל מופיעים Grow (לשעבר Meshulam), Hyp, Cardcom, Tranzila PayTech, PayPlus, iCount, ולצידם PayPal ואפליקציית Allpay. כולם, חוץ מ-PayPal, דורשים בפועל עסק רשום ואדם בגיר שחותם על חוזה סליקה. על כל עסקה נוספת עמלת Shopify של 2% בתכנית Basic. Grow מפרסם 0.75% + ₪59–69 לחודש + 0.6% תוספת Shopify; השאר "לפי הצעה".
2. **רישום.** קטין נרשם כעוסק רק דרך הורה שחותם על הכול (כל זכות). הדרך הפשוטה: העסק על שם אימא. פתיחת תיקים: מע"מ (טופס 821) → מס הכנסה (5329) → ביטוח לאומי (6101), ולא אונליין אלא דרך מייצג. תקרת עוסק פטור 2026: ₪122,833 לשנה ≈ $3,200 בחודש. **מוצר שעובר M1 ומתרחב חוצה את התקרה בשנה הראשונה**, ואז מע"מ על מכירות לחו"ל בדרופשיפינג הוא שאלה פתוחה ששווה עד 18% מההכנסות. זו השאלה החשובה ביותר לרו"ח.
3. **מכס בארה"ב.** מאז 29.8.2025 כל חבילה ממוסה. לפי כלל CBP מ-2026, בחבילות דואר שלא שולם עליהן מראש, הנמען משלם בסניף הדואר לפני שהוא מקבל את החבילה. לחנות שלנו זה אומר: רק ספקים עם מחסן בארה"ב או משלוח DDP (מכס משולם מראש). לקוח שמופתע במכס = החזר + מחלוקת PayPal.
4. **מס מכירה בארה"ב.** ספים של $100k למדינה ברוב המדינות, $500k בקליפורניה, טקסס וניו-יורק; חל גם על מוכרים זרים. בקנה המידה של התכנית אין חובת רישום; בודקים פעם בשנה.
5. **בעלות על חשבונות.** Shopify: אימא בעלת החשבון, לך חשבון צוות עם גישה מלאה. AutoDS: 18+, חשבון על שם אימא. Meta: תיק עסקי על שם אימא; האם מותר להוסיף משתמש בן 15, לא ידוע.

## Searched
Queries (WebSearch) and pages (WebFetch) on 2026-11-10: Shopify Israel gateway list; Tranzila, Allpay, PayPlus app listings; Payoneer Checkout Israel; PayPal Israel business account documents; economic nexus thresholds 2026 and foreign sellers; Federal Register postal de minimis rule 2026; US-warehouse DDP suppliers; China-to-US dropshipping after de minimis (counterpoint); minor-owned business in Israel; exempt-dealer registration steps; Shopify owner age and staff accounts.
Refused or empty: Shopify's own country gateway page (filter needs JS), kolzchut page (403; quoted via search snippet), PayPal IL user agreement (empty body), Federal Register HTML (redirect to an unblock page; PDF read with pdftotext instead).

## Sources read in this area (≥ 15 required: 27 here; primary ≥ 3: 11; dissenting ≥ 2: 3)
Phase 0 rows: S-02, S-10, S-11, S-12, S-21, S-22, S-23, S-26, S-27, S-28, S-35. New rows S-37 to S-52 in `../sources.md`.
Primary: S-02, S-10, S-11, S-12, S-26, S-28, S-35, S-39 (Allpay listing), S-42 (CDTFA), S-50 (CBP interim final rule), S-48 (Payoneer page). Dissenting: S-45 (tariffs gutted margins; seller left the US market), S-49 (claim that no business licence is needed; holds for PayPal only, not cards), S-53 (Payoneer "not a merchant account").

## Findings

### A. Card acceptance from Israel on Shopify
| Provider | Published price (before VAT) | Shopify surcharge | Requirement | Evidence |
|---|---|---|---|---|
| Grow (ex-Meshulam) | 0.75% (Grow) / 1% (Grow Light); ₪59–69/mo (Grow), ₪29/mo annual (Light); refund ₪6.90 | 0.6% | "not required" acquirer contract per provider; business registration not stated | S-37, S-38 (practitioner) |
| Hyp | by quote | not stated | existing terminal required | S-38 |
| Cardcom | by quote; refund ₪7.90, 0.6% not returned on refunds | 0.6% | works with existing acquirer | S-37, S-38; listing status disputed Sep–Nov 2026 |
| Tranzila PayTech | not published | not stated | merchant account with an acquirer | S-28 (primary listing, Apr 2024, 0 reviews) |
| PayPlus | not published | not stated | merchant account required per setup guide | S-38 |
| iCount | not in sources | | | S-37 |
| Allpay | free install; "external charges billed separately" | not stated | none stated; Israel-only; Sep 2025, 0 reviews | S-39 (primary listing) |
| PayPal | 3.4% + ₪1.20 + 1% US buyers + 2.5% FX | PayPal exempt from Shopify fee only with Shopify Payments, so 2% applies | personal/business account; IL document list Unknown | S-10, S-26 |
| Payoneer Checkout | not published | | Israel eligibility not named on page; one community reply says available | S-48, S-53 |
| Stripe / Shopify Payments | n/a | | not available to Israeli businesses | S-02, S-37 |
Plus Shopify's own 2% third-party fee on Basic on every transaction (S-03, S-26). Whether a provider surcharge and Shopify's fee stack on the same order is unresolved (S-38 says get it in writing).

Fee stack used from now on in unit economics for a US order paid by card through Grow: 0.75% + 0.6% + 2% = 3.35% + ₪59/mo fixed; by PayPal: 4.4% + ₪1.20 + 2.5% FX + 2% = ~8.9% + ₪1.20. The Phase 0 model used 6.4% blended; it stays until the gateway is chosen.

Verdict on the "no business" path (S-49): PayPal alone can start without a registered business, cards cannot. A card gateway contract is signed by an adult with a business number. The order of operations is therefore registration → gateway → store live, not the reverse.

### B. Registration in Israel with a minor operator
- A minor registers as a dealer only through a parent or legal guardian who signs every document; the Tax Authority file is opened by the parent (S-40, kolzchut, via search snippet). The simpler and equivalent path, consistent with the hard constraint, is the business in the mother's name.
- Steps (S-41): VAT file first (form 821: ID, bank proof), then income tax (form 5329), then National Insurance (form 6101). Not possible online except through a representative (accountant or tax adviser). S-41 is undated; confirm.
- Ceiling: ₪122,833 for 2026 (S-21, secondary; gov.il refused). ≈ $38,750/year ≈ $3,230/month at ₪3.17 (S-33). The ceiling counts turnover (gross sales), not profit.
- Consequence: the M1 bar (≥ 30 orders over ≥ 14 days) is well under the ceiling, but the M2 scaling path crosses it within months. Crossing it means becoming עוסק מורשה, charging VAT where it applies, and filing periodic VAT returns (S-21). Whether an Israeli-registered dropshipper's sales to US customers of goods that never touch Israel are zero-rated is Unknown: §30(a)(1) zero-rates goods exports only with an export declaration (S-22), which cannot exist for goods shipped from a US warehouse to a US address. If VAT at 18% applies to such sales, breakeven ROAS rises from 1.80 to about 2.45 under the Phase 0 assumptions. This is the single largest open number in the program and goes to the accountant first.
- Income attribution: the business income is the mother's; her marginal income-tax rate and National Insurance status (employee + self-employed) are Unknown and change net profit. Sections 82–84 anti-avoidance attribution applies to income assigned to a minor (S-51), which is not the structure chosen.

### C. US sales tax
- Economic nexus: $100,000 in 41 states; California, Texas $500,000; New York $500,000 and 100 sales; 15 states still have a 200-transaction alternative (S-43 as of 8/1/2026, S-44). California states the rule covers "foreign sellers located outside of the United States" (S-42, primary).
- At any revenue the program's Phase 0 base case reaches in year one, no state threshold is crossed. Rule: review per-state sales each January; register in a state the month its threshold is crossed. Shopify's tax settings can be left off until then.

### D. US import duties and who pays
- EO 14324 suspended duty-free de minimis for every country from Aug 29, 2025 (S-35). CBP's 2026 interim final rule for mail: duties are assessed by an ad valorem or a specific per-package method and paid by carriers or qualified parties; where not prepaid, "the recipient will pay the duties, taxes, and fees owed... at the local post office prior to the recipient taking possession" and duties may "be collected upon delivery of such shipments to addressees" (S-50). Statutory end of de minimis July 1, 2027 (S-35, S-50).
- Seller experience: one named seller reported "about a 33% decrease in revenue", border holds, refund demands, and moved sales from the US to Europe (S-45, Apr 2025). Vendor view: a 20% tariff on a $30 product takes margin from 36.7% to 26.7% (S-47); some goods faced tariffs "as high as 104 percent" in May 2025 (S-46).
- Decision for Phase 1 product sweep: only two supplier types are eligible: (1) US-warehouse stock, (2) DDP shipping where the supplier or carrier prepays duties and the landed cost is known at checkout. "Customer pays at the post office" is excluded: it violates the delivery-time promise the FTC rule requires (S-34) and feeds PayPal disputes (S-12).

### E. Who holds which account
| Account | Holder | Operator's access | Evidence |
|---|---|---|---|
| Shopify (owner, billing, payouts) | mother | staff account with full access | S-01 (18+), S-52 (community reply: owner and payout details under the guardian; staff account for the minor) |
| Card gateway / PayPal | mother, with the business number | none on money; drafts only | S-28, S-38, S-10 |
| AutoDS | mother (18+) | works under her login with her knowledge | S-05 |
| Meta Business portfolio and ad account | mother; payment method hers | Unknown whether a 15-year-old may be added as a business user | S-13 (13+ personal), S-14, S-09 |
| Domain | bought through Shopify under the owner | | S-25 |
| Israeli business file | mother | | S-40, S-41 |

## Candidates extracted (go through Phase 1.3 before any registry ID)
| Candidate | Family | Mechanism | Who exploits it | Cost to test | Prior P(pass) | Negative result looks like |
|---|---|---|---|---|---|---|
| O-c1: Grow as card gateway, PayPal as second method | operations/payments | lowest published fee stack; no separate acquirer | Israeli Shopify merchants (S-37) | ₪59–69/mo + onboarding hours | 60% that Grow accepts a new עוסק פטור (Unknown, to ask) | Grow declines or requires עוסק מורשה |
| O-c2: Business registered as עוסק פטור in mother's name, switch to מורשה planned at ~₪100k | operations/tax | simplest legal path under the ceiling | standard small-business path | accountant fee (Unknown) | high for registration; VAT-on-foreign-sales answer is Unknown | accountant says VAT applies at 18% to US sales → breakeven ROAS ~2.45 |
| P-family constraint: US-warehouse or DDP suppliers only | product | duties and delivery time known at checkout | US-warehouse dropship suppliers (S-46, S-47) | sweep 2 | n/a | no such supplier for a candidate product |

## Accountant question list (for the mother to bring; in Hebrew)
1. העסק יירשם על שמי (האם). הבן (15) מפעיל בפועל בידיעתי. מה המבנה הנכון, ומה המשמעות לחבות שלי?
2. מכירות אונליין ללקוחות בארה"ב של מוצרים שנשלחים ממחסן בארה"ב ולא נוגעים בישראל: כעוסקת פטורה, האם יש מע"מ? וכשאעבור לעוסקת מורשית, האם המכירות האלה בשיעור אפס (סעיף 30(א)(1) דורש רשימון יצוא שאין כאן) או חייבות ב-18%?
3. תקרת העוסק הפטור ל-2026 (₪122,833 לפי מקורות משניים): מתי בדיוק עוברים, ומה קורה בחודש המעבר?
4. ביטוח לאומי: אני שכירה/לא שכירה (לפי המצב), מה המשמעות של הכנסה מעסק עצמאי קטן?
5. הוצאות מוכרות: מנויים ל-Shopify, AutoDS, כלי AI, פרסום ב-Meta שמשולמים בדולרים בכרטיס אשראי. מה נדרש כדי להכיר בהן?
6. הכנסות בדולר דרך PayPal/שער סליקה: איך רושמים, באיזה שער, ומה עם עמלות המרה?
7. האם יש חובת דיווח או רישום בארה"ב (מס מכירה) בהיקפים של עשרות אלפי דולרים בשנה? (לפי מקורותינו: לא מתחת ל-$100k למדינה.)
8. כמה עולה פתיחת התיקים דרך המשרד, וכמה הנהלת החשבונות השנתית לעוסק פטור?

## Research synthesis block
```
Searched: Shopify Israel gateways; registration path for a minor-run, mother-held business; VAT on foreign sales; US sales tax nexus for foreign sellers; US postal duties after de minimis; who pays duties; account ownership rules.
Strongest sources: CBP interim final rule 2026-12669 (S-50) - primary, defines recipient-pays; CDTFA Wayfair page (S-42) - primary, foreign sellers covered; PayPal IL merchant fees (S-10) - primary; practitioner gateway comparisons dated Nov 2026 (S-37) and Sep 2026 (S-38) - cross-checked against app listings (S-28, S-39).
Candidates found: 3, in 3 families (payments, tax structure, supplier constraint); 0 families previously failed.
Patterns: every card path needs a registered business and an adult signatory; Shopify adds 2% on top of any gateway; the exempt-dealer ceiling is reached at ~$3.2k/month revenue; US postal parcels without prepaid duty are paid by the recipient at the post office.
Failure modes specific to this field: VAT at 18% on foreign sales if not zero-rated (unresolved); customer-paid duties → refunds and disputes; new-seller holds coinciding with scaling.
Cumulative P(any passes): not applicable (no hypotheses registered yet); the tax answer is a gate, not a hypothesis.
Assumptions and gaps: Grow's acceptance of a new עוסק פטור; PayPal IL business-account documents; Meta business-user age; VAT answer; mother's tax bracket and NI status; accountant price.
```

## Right-For-You check for the one instruction that follows
```
Instruction:         Mother contacts an accountant or tax adviser with the 8 questions above, asks the price of a first consultation before booking, and brings the answers back
Who acts:            guardian (mother); program drafted the questions
Legal and policy:    no platform gate; Israeli registration must exist before card acceptance (S-28, S-38, S-40, S-41)
Cost:                external $ Unknown until quoted; approve before paying; research line $150 untouched; operator hours 1
Expected value:      resolves the largest open number (VAT on US sales: 0% vs 18% of revenue) and the registration path; without it no gateway instruction can pass its check
Reversible?          yes
Evidence:            Observed (S-21, S-22, S-40, S-41) that registration precedes card acceptance and that the VAT question is unresolved in public sources
What makes it wrong: an accountant who quotes a fee above what the ledger can carry before the first sale; then ask the Tax Authority's free hotline first
Cheaper alternative: Tax Authority phone service (free) for questions 2–3 only; it will not confirm the structure in writing
Verdict:             advise with conditions (get the price first; any payment is entered in ledger.md before it happens)
```
