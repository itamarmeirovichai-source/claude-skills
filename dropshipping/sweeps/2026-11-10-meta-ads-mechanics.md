# Sweep 3 (2026-11-10): Meta Ads mechanics for a $20/day test budget

## תקציר בעברית
1. **מה Meta עצמה מתעדת (מקורות סטטיים של המפתחים).** Conversions API מחובר ל-Pixel; אירועים כפולים מסוננים רק אם `event_id` ו-`event_name` זהים ובתוך 48 שעות, אחרת נספרים פעמיים. קמפיין Advantage+ למכירות דורש מטרת OUTCOME_SALES ו-Pixel, מכיל סט מודעות אחד, עד 150 שילובי קריאייטיב, ומגרסת API v25 המסלול הנפרד שלו מבוטל ומאוחד. בקרות ברמת החשבון: גיל מינימום 18–25, הדרת מיקומים.
2. **שלב הלמידה.** הדף הרשמי חסום לתכנית; מתרגלים מצטטים "כ-50 תוצאות בשבוע שאחרי העריכה האחרונה" לכל סט מודעות. ב-$20 ליום עם CPA של $30 זה בלתי אפשרי, ולכן **כל בדיקת מוצר שלנו היא "Learning Limited" מעצם התכנון**. זה לא פסול: זה אומר שהבדיקה מזהה רק אפקטים גדולים, והחלטת ההמשך נשענת על מדדי ביניים (עצירת גלילה, CTR, הוספה לסל) ועל רכישות כשער למנה השנייה.
3. **מבנה.** בדיקה: קמפיין אחד, ABO, סט מודעות אחד, ארה"ב, רחב, 2–3 קריאייטיבים שונים באמת. Advantage+ רק אחרי ≥ 15–25 המרות בשבוע (טענות ספקים, לא מאומתות). "כלל ה-20%" להעלאת תקציב הוא הרגל של מתרגלים, לא כלל של Meta; כלל ה-25% לצעד של התכנית נשאר, כחוק פנימי.
4. **מדידה.** Meta סופרת רכישות בחלון ייחוס כולל צפייה; Shopify סופרת הזמנות. הפערים לשני הכיוונים מתועדים. בדיקת geo-holdout אחת שפורסמה (ספטמבר 2026): הכנסה תוספתית $7.7–9.7k על $6.7k הוצאה, כלומר ROAS תוספתי 1.15–1.45 בעוד הדשבורד הראה יותר. **המילה האחרונה היא תמיד הזמנות Shopify ותשלומי המעבד** (חוק 11, M1).
5. **בריאות חשבון.** ציון משוב לקוחות: משוב שלילי גבוה (משלוח מאוחר, איכות) מקטין הפצה עד איבוד זכאות (Meta, 2019). תשלום שנכשל הוא טריגר להגבלה. פתיחת חשבון חדש בזמן ערעור = עקיפה = הגבלה על כל העסק. לכן: כרטיס של אימא עם מסגרת, תקרת הוצאה בחשבון, ואף פעם לא חשבון שני.

## Searched
Meta developer docs (Conversions API, deduplication, Advantage+ shopping campaigns, insights parameters [404], learning stage [not found]); Meta ad standards (unacceptable business practices); Meta newsroom (customer feedback score); Shopify help (data sharing page empty); practitioner: Lebesgue geo-holdout, Top Growth testing framework, RocketShip HQ, Common Thread, Segwise/Webtonic ABO-CBO, Jon Loomer (carried S-29), account-restriction guides, Andromeda guides; attribution discrepancy explainers.

## Sources in this area (24; primary 8; dissenting 3)
Carried: S-08, S-09, S-15, S-16, S-29, S-30. New S-74..S-89. Primary: S-74, S-75, S-76, S-77, S-78, S-79 + S-08, S-09. Dissenting: S-82 (50-conversion gate is dated), S-88 (20% rule is a habit, not Meta's), S-80 (attribution vs incrementality).

## Findings and the rules they produce

### A. Tracking (before any spend)
- Install Shopify's Facebook & Instagram app and turn on Conversions API with the Pixel kept on (S-86, practitioner; Shopify's own help page returned no body: S-26-type gap, operator verifies in admin). Deduplicate by `event_id` within 48 hours or purchases count twice (S-75, primary).
- Rule T1: no campaign starts until a test purchase shows once in Events Manager and once in Shopify.
- Rule T2: Meta-reported purchases are never the reconciliation figure (S-89; S-80). Shopify orders minus refunds, matched to processor payouts, are.

### B. Campaign structure for the $120 product test
- ABO, one campaign, one ad set, United States, broad (no interests), 2–3 genuinely different creatives (different hook, format, and claim), $20/day, 6 days (overlay §4 example; S-81, S-84).
- Advantage+ sales campaigns: OUTCOME_SALES objective, pixel required, one ad set, up to 150 creative combinations (S-76). Vendor guides say they need ≥ 15–25 conversions/week or ~$100/day to work (S-87, unverified). Rule C1: no Advantage+ before a product passes M1 and runs ≥ 15 purchases/week.
- Account-level controls to set once: minimum age 18 (required anyway for the categories we avoid), exclude Audience Network (S-76).

### C. Learning phase and what a $120 test can and cannot see
- Practitioner consensus: ~50 optimization events in 7 days per ad set, else "Learning Limited" (S-29; S-82 quotes Meta's doc as "usually after about 50 results in the week after the last significant edit").
- Arithmetic: at $20/day and a $30 CPA, the expected purchases in 6 days are 4. Every test is learning-limited by design. The dissenting view (S-82) says this gate is dated and recommends judging on delivery and early conversions instead; Top Growth (S-81) calls a test at "50 purchases per ad set or seven days, whichever comes first".
- Rule L1: the $120 tranche reads leading indicators (thumb-stop, CTR, add-to-cart) and purchases; the numeric stop rule and its false-positive rate come from sweep 4 (statistics). Rule L2: no edits to a running test ad set (budget, creative, audience) during the 6 days; edits reset learning (S-29).

### D. Scaling
- The "20% per step" rule has no Meta source; it is a habit (S-88). RocketShip reports a CPA rise of 35–60% for 48–72 hours after a reset from its own unreplicated data (S-88).
- Program rule S1 (overlay §6) stands as an internal rule: ≤ 25% per step, one step per 7 days, only after reconciled ROAS above breakeven for the window, cut back the same day on decline. It is labeled "program rule", not "Meta rule".

### E. Account health
- Customer feedback score: "a reduction in ad delivery or loss of advertising eligibility for advertisers with high levels of negative feedback" (S-78, Meta 2019). Third-party guides tie it to shipping delays and quality (S-85).
- Payment failures and disputed payments are restriction triggers; new accounts spending aggressively early are risk-scored; opening a second account during an appeal is circumvention and escalates to the whole business (S-85; S-08 "Helping anyone evade or circumvent our enforcement").
- Unacceptable business practices: "deceptive pricing, unauthorized endorsements, and guaranteed investment returns" (S-77).
- Rules H1–H4: one ad account, in the mother's business portfolio, with her card and a monthly spend cap set in Ads Manager; no fake "was" prices (also FTC); delivery time on the ad and page equals the supplier's per-SKU estimate; a strike or restriction is logged in the registry as a loss (law 17).

### F. Attribution and the dashboard
- Meta counts purchases within its attribution window including view-through; Shopify counts every order (S-89). One published geo-holdout (S-80): $6,695 spend, incremental revenue $7.7–9.7k (1.15–1.45x) against pixel-attributed $7.3–9.9k, within a six-week window and non-randomized controls.
- Rule A1: for the registry, "ROAS" means reconciled Shopify revenue (net of refunds) ÷ Meta spend, attribution 7-day click only as a secondary read.

## Candidates extracted
| Candidate | Family | Mechanism | Cost to test | Prior | Negative looks like |
|---|---|---|---|---|---|
| A-c1: broad ABO single-ad-set test beats interest-targeted test on cost per purchase at $20/day | ads | delivery system finds buyers from creative; interests only shrink the pool | 2 × $120 | 55% (practitioner consensus, no data at this budget) | interest set wins by more than noise |
| A-c2: a product test can be called in 6 days on leading indicators without false-positive rate above 20% | ads/statistics | thumb-stop and ATC are high-volume proxies | analysis only (sweep 4) | Unknown until computed | proxies do not predict purchases in the second tranche |

## Research synthesis block
```
Searched: tracking, structure, learning phase, scaling, account health, attribution.
Strongest sources: developers.facebook.com docs (S-75 dedup, S-76 ASC) - primary and static; Meta newsroom on feedback score (S-78); Lebesgue geo-holdout (S-80) - the only measured incrementality figure found; RocketShip HQ (S-82) - explicit dissent with admitted limits.
Candidates found: 2 (A-family); 0 previously failed.
Patterns: Meta's own documents say little about thresholds; vendor guides fill the gap with unsourced numbers; the only hard constraints are tracking dedup, objective/pixel requirements, and policy.
Failure modes: double-counted purchases; learning resets from mid-test edits; dashboard ROAS above reconciled ROAS; a second ad account; a failed card payment.
Cumulative P(any passes): n/a (rules, not hypotheses).
Assumptions and gaps: Meta Business Help pages (learning phase, feedback score thresholds, data-sharing levels) unread by the program; operator or mother reads them in a browser at onboarding and pastes the lines.
```
