# Store build sheet (one store, four products; written 2026-11-11 ahead of M0 step 2)

What the operator prepares now in a document, and what the mother clicks at M0 step 2 (Shopify $1/month × 3, S-03). Rules: LP1 (no surprise costs, delivery days visible), LP2 (speed: lightest free theme, ≤ 3 apps, images ≤ 150 KB, LCP ≤ 2.5 s mobile), LP6 (no fake trust), D1–D3, FM1–FM7, S-117 (no dark patterns).

## 1. Identity
- Store name: a neutral home-and-pet name the mother approves; checked once on USPTO TESS and as a .com before purchase (domain ≈ $15, ledger line first; FM4 no brand names of others). Not "official", not a brand we do not own.
- Legal footer: business name as registered in Florida, mother's name as owner, registered address, support email, response time 1 business day (store-policies.md).
- Operator role: staff account with full access, not owner (S-52). The owner email, bank and tax identity are the mother's.

## 2. Theme and speed
- Theme: the lightest free Shopify theme available at M0 (Dawn or its current equivalent); no purchased theme before M1.
- Settings: no autoplay video above the fold; hero image ≤ 150 KB WebP; product images ≤ 150 KB; no slideshow; no pop-ups; no countdown, stock counter or "N people viewing" (S-117, FM).
- Apps (≤ 3 before M1): (1) Facebook & Instagram by Meta (pixel + Conversions API, S-86); (2) a reviews app with a free tier that sends the request **after delivery** with no sentiment filter and imports nothing (S-36); (3) optional: a product-personalisation field app only if P-0002 variant A runs. Nothing else: no upsell pop-up, no "trust badge" app, no fake-social-proof app.
- Check before launch: Google PageSpeed on the P-0002 page, mobile, LCP ≤ 2.5 s (S-140). Fail → remove images/apps until it passes.

## 3. Navigation
Home · Shop (4 products) · Shipping & Returns · Contact · (footer) Privacy · Terms. One collection, no sub-menus. Home page = the current test product's hero and the three others as cards; no "best sellers" label (none exist).

## 4. Checkout
Guest checkout on; Shop Pay, cards (Shopify Payments), PayPal; shipping = free (price includes it, LP1); Shopify Tax on for Florida after registration (S-193, S-196); no tipping prompt; no pre-ticked marketing box (S-117); order confirmation shows the per-SKU delivery window.

## 5. Email flows (Shopify built-in notifications, edited; no marketing app before M1)
1. Order confirmation: thanks, order number, "ships in [1–2] business days from a US warehouse, delivered in [3–7] business days", support email.
2. Shipping confirmation: tracking link, carrier, "if it is late past the window we told you, reply to this email and we fix it" (FTC 30-day rule context, S-34).
3. Delivery + 3 days (reviews app): one request, "tell us what you think, good or bad; we read every one". No incentive, no filter (S-36).
4. Refund/cancellation: within 7 working days, states the amount and method (store-policies.md).
No abandoned-cart discount emails before M1 (discounts corrupt the price test and the no-"was"-price rule).

## 6. Product pages
From the four build packages: `p-0002-build.md` §4, `p-0004-build.md` §4, `p-0003-build.md` §4, `p-0001-build.md` §4. Each page's [brackets] are filled only from the supplier spec or the sample (claim ledgers). A page with an unfilled bracket is not published.

## 7. Legal pages
`store-policies.md` (shipping, returns, reviews, pricing, privacy summary, contact) + Shopify's generated privacy and terms, read once by the mother. Privacy page names Meta pixel/CAPI (S-75) and the opt-out.

## 8. Tracking (M0 step 5)
Pixel + CAPI via the Meta app; one test purchase ($0.01 test or a real sample order) seen once in Events Manager and once in Shopify with the same event_id (dedup, S-75); UTM scheme `p000X_a/b`; the daily sheet from `daily-numbers.md` is the only ROAS source (A1).

## 9. Launch gate (all true before the first ad dollar)
- [ ] Policies live and linked in footer · [ ] Shopify Tax Florida on · [ ] Guest checkout + PayPal + cards tested with one real order · [ ] PageSpeed mobile LCP ≤ 2.5 s on the test product page · [ ] No timers/counters/"was" prices anywhere (search the theme) · [ ] Reviews app set to post-delivery, unfiltered · [ ] CAPI dedup test passed · [ ] Ledger line for T1 entered
