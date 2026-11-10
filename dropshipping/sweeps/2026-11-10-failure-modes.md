# Sweep 5 (2026-11-10): failure modes

## תקציר בעברית
1. **צ'ארג'בקים.** Mastercard: תכנית ECM נכנסת לפעולה ב-100 צ'ארג'בקים בחודש **וגם** יחס 1.5%–2.99%; HECM ב-300 ו-3%. Visa (VAMP): המקורות המשניים סותרים זה את זה (1.5% מול 0.9% ב-2026); דף Visa עצמו לא נגיש לתכנית. בקנה המידה שלנו (עשרות הזמנות בחודש) ספי הרשתות לא רלוונטיים; מה שרלוונטי הוא PayPal והשער המקומי, שמגיבים לשיעורי מחלוקות הרבה לפני כן. יעד פנימי: מחלוקות < 0.5% מההזמנות, החזרים לפי הקצבת הקטגוריה.
2. **PayPal.** מחלוקת מקפיאה את הכסף; בלי תגובה הקונה מסלים תוך כ-4 ימים; מחלוקת שלא הוסלמה נסגרת ביום 21. "פריט לא התקבל" מוכרע לפי מעקב משלוח שמראה מסירה לכתובת שבעסקה. מסקנה: רק ספקים עם מעקב מלא עד "delivered" בארה"ב.
3. **ספק שנגמר לו המלאי.** Zendrop: החזר מלא אוטומטי, בלי פיצוי. מבקרים מדווחים על "במלאי" שהופך ל"אזל" ברגע ההזמנה, והזמנות ש"בבדיקה" 8 ימים בלי הודעה. כלל: הזמנת דגימה אמיתית לפני כל קמפיין, ובדיקת מלאי ידנית בבוקר כל יום של קמפיין.
4. **חנות שנסגרת.** Shopify יכולה להשעות חנות על תלונת IP בלי הסבר מפורט; סוחר דיווח על $4,000 מוקפאים ו-$3,000 שהושקעו. הדרך היחידה: שם חנות ומוצרים שלא דומים למותג, ותשובה מסודרת לתלונה. דף המדיניות הרשמי לא נקרא (404).
5. **דפוסי הטעיה.** דוח ה-FTC מ-2022 מונה בדיוק את מה שחנויות דרופשיפינג עושות: טיימר ספירה לאחור מזויף, "נשארו רק 2", "24 אנשים צופים עכשיו", הנחה מזויפת ממחיר שמעולם לא נגבה, עמלות שמופיעות רק בסוף. כל אלה אסורים בחנות שלנו (חוק 17), גם כשהאפליקציה מציעה אותם בלחיצה.
6. **אפליקציות.** 98.2% מ-3.59 מיליון חנויות פעילות מוציאות פחות מ-$100 בחודש על אפליקציות; ממוצע 4.1 אפליקציות. כלל: אפס אפליקציות בתשלום עד M1 חוץ מהספק.
7. **הנדרס.** סיפורי הכישלון עם מספרים נדירים ודלים ($300 בחודש ראשון: מוצר לפי טרנד, פרסום בלי בדיקה, ספק מאחר). אין פוסט-מורטם מלא עם ספר חשבונות. שלנו יהיה כזה, כולל אם נכשל.

## Sources in this area (22; primary 6; dissenting 2)
Carried: S-11, S-12, S-34, S-36, S-45, S-56, S-62, S-78, S-85, S-05, S-65. New S-117..S-127. Primary: S-117 (FTC report text), S-118 (PayPal disputes page), S-119 (Zendrop cancellation policy), S-121 (Storeleads-derived dataset), S-12, S-78. Dissenting: S-124 (failure statistics count abandoned stores), S-125 (threshold figures conflict between vendors).

## Findings and rules
### A. Disputes and chargebacks
- Mastercard ECM: ≥ 100 chargebacks in a month **and** ratio 1.5–2.99%; HECM ≥ 300 and ≥ 3% (S-125, consistent across vendors). Visa VAMP: vendors disagree (1.5% in Apr 2025, 2.2% from Jun 2025, "roughly 0.9%" from Apr 2026 per S-125; "1.5% North America Apr 2026" per another); Visa's page returned 404; conflict unresolved. At < 300 orders/month the count tests cannot trigger; the real exposure is PayPal and the local gateway.
- PayPal: funds held on dispute; escalation to claim within 20 days, auto-close day 21; "item not received" needs tracking to the transaction address (S-118; S-12 reserves). Rule FM1: every supplier must provide carrier tracking with a "delivered" scan in the US; a candidate without it is excluded. Rule FM2: internal ceilings: disputes ≤ 0.5% of orders, refunds ≤ category allowance; a week above either freezes scaling (ties to S1).
### B. Supplier stockouts and cancellations
- Zendrop: automatic full refund on out-of-stock cancellation, "We do not provide compensation for inventory-based cancellations"; shipped orders cannot be canceled (S-119). Reviewers report "in stock" flipping to "out of stock" at order time and orders held "In Review" for 8 days (S-120). Rule FM3: sample order to a US address before any campaign (M0 step 5); daily stock check during a campaign; a stockout mid-test pauses the ad set the same day (allowed early kill).
### C. Store shutdown and IP
- Shopify can restrict a store on an IP complaint; a merchant reported $4,000 held and no explanation (S-122, 2023, practitioner). Shopify's IP policy page returned 404; AUP forbids illegal sales and allows account-level action (S-65). Rule FM4: store and product names are generic; no brand terms in copy (incl. "MagSafe"); respond to any notice within 24 h through the admin.
### D. Dark patterns (law 17)
- FTC staff report (Sep 2022), examples quoted from the text: "Baseless Countdown Timer: Creating pressure to buy immediately by showing a fake countdown clock that just goes away or resets"; "False Low Stock... 'Only 1 left in stock – order soon'"; social proof "'24 other people are viewing this'"; "False Discount Claims... offering a fake" discount; "Hidden Costs... Drip Pricing... Advertising only part of a product's total price initially" (S-117). Rule FM5: no countdown timers, stock counters, viewer counters, fake "was" prices or late-added fees on the store, even when a theme or app offers them; shipping cost shown on the product page.
### E. App bloat
- 3,593,277 active stores (Storeleads, May 25, 2026): 1.8% spend > $100/month on apps; ~4.1 apps per store (S-121). Rule FM6: zero paid apps before M1 except the supplier app and the free Meta app; every app added later gets a ledger line and a 30-day removal review (law 15).
### F. Post-mortems
- Dated, numbered failure accounts are rare and thin: "$300 in my first month" from trend-based product choice, untested ads, late supplier (S-123); "I made a loss on every sale" on a print-on-demand DTC attempt (S-126, page refused, quoted via search). Vendor "case studies" with named owners and round numbers are not trusted (S-127). Dissent: failure statistics mostly count abandoned stores (S-124). Rule FM7: this program's own post-mortem is written at every FAIL in results/, with the ledger, so the denominator exists.

## Research synthesis block
```
Searched: network chargeback programs; PayPal disputes and reserves; supplier stockouts; Shopify IP shutdowns; FTC dark patterns; app spend data; failure post-mortems.
Strongest sources: FTC report text (S-117, primary); PayPal disputes page (S-118, primary); Zendrop cancellation policy (S-119, primary); Storeleads-derived app data (S-121).
Candidates found: 0 new hypotheses; 7 rules (FM1–FM7).
Patterns: the failure modes that end accounts are delivery and dispute related, not ad related; every "growth" app feature the FTC lists is a policy risk; data on failures is anecdotal.
Failure modes: mid-test stockout; untracked shipments; brand-like names; conflicting threshold numbers used as if certain.
Cumulative P(any passes): n/a.
Assumptions and gaps: Visa VAMP current threshold unresolved; PayPal seller-protection terms unread (US legal page returned no body); Shopify IP policy unread.
```
