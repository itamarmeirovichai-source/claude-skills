# Candidate table, program-side pass (2026-11-10)

Operator rule (2026-11-10): the program does everything it can; the operator completes the remainder. This file is the program's half of `runbooks/ad-library-scan.md`.

What the program could do: cross five trend lists (S-109..S-113) for products named by ≥ 2 independent-looking sources, apply the exclusions from sweep 2, record price and sourcing bands where given, and check that the two advertisers TrendTrack names actually exist.
What the program could not do: open the Meta Ad Library (403 to the program), open Zendrop/Spocket/CJ catalogs (login or bot wall), or use Motion's brand tools (the account has no workspace). Those are the three operator columns.

## תקציר בעברית
12 מועמדים עברו את הסינון שלי. לכל אחד נשאר לך לבדוק שלושה דברים בלבד, עם קישור מוכן: (1) בספריית המודעות: כמה מפרסמים בארה"ב, ומה תאריך ההתחלה של המודעה הוותיקה ביותר; (2) אצל ספק: האם יש גרסה ש"נשלחת מארה"ב" ומה העלות + המשלוח; (3) מחיר מכירה בפועל אצל מפרסם אחד. כל שורה שבה מספר המפרסמים בארה"ב > 5 נפסלת (רוויה). כל שורה בלי ספק אמריקאי נפסלת. מה שנשאר נרשם כ-P- בשלב 2.

## Exclusion refinement (sweep 2 §D)
Products with a small rechargeable cell installed in the device are mailable under USPS PI 9D (≤ 20 Wh per cell, UN3481 mark; S-61) and are **allowed** when shipped by a US-warehouse supplier that handles the marking; standalone batteries and power banks remain excluded. Heated vests and jump starters (large cells, >100 Wh risk) remain excluded.

## Table

Library link pattern (replace the term): `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&media_type=video&search_type=keyword_unordered&q=TERM`

| # | Product | Family | Named by | Price band (secondary) | Sourcing band (secondary) | Exclusions | Program note | Operator: Library (US advertisers / oldest start date) | Operator: US-warehouse supplier + landed cost | Operator: observed sale price |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | No-drill vacuum suction hooks (bathroom/kitchen) | F1 home | TrendTrack (Roha Home, "572 days"), Walmart/Fruugo clones (S-114) | $15–45 per pack | $3–8 (Fruugo/Walmart retail $15–17 suggests low cost) | none | Advertiser verified: roha-home.com exists, Trustpilot 3.5/5 from ~1,042 reviews, complaints about delivery and returns (S-114). Strong demand signal, **high saturation risk**: many clones at Walmart | term: `suction hooks no drill` | Zendrop/Spocket/CJ "ships from US"; Doba | |
| 2 | Elevated / tilted pet bowl (stainless, adjustable) | F2 pet | TrendTrack ("Petzrella"), crevio (slow feeders), search summaries | $30–50 | $8–20 | none | "Petzrella" **not found** anywhere by search (S-115): TrendTrack's advertiser claim unverified. Doba lists an elevated double bowl "ships from United States", 3 business days processing (S-115) | term: `elevated dog bowl` | Doba listing first; then Zendrop/Spocket | |
| 3 | Automatic pet feeder (app or timer) | F2 pet | TrendTrack (Paw & Co, 98 days), crevio category | $50–90 | $20–35 | mains/USB power; installed cell OK | Returns on electronics ~8–10% (S-72); app-support tickets likely | term: `automatic pet feeder` | Zendrop/Spocket US; WOpet ships from own US warehouse (brand, not dropship) | |
| 4 | Candle warmer lamp (timer/dimmer) | F1 home | AutoDS Nov list ($22.99 → $47.72), eBay/Faire US listings | $40–55 | $20–25 | mains 110V; must be US-plug | Q4 gift fit; fragile (glass/lamp) → damage claims; Faire lists US-shipping wholesale (S-116) | term: `candle warmer lamp` | Zendrop/Spocket US; Faire wholesale needs stock (not dropship) | |
| 5 | Electric scalp massager (waterproof, cordless) | F1 personal care | copyfy (#3), crevio (#7), Kohl's/eBay US | $35–55 | $15–22 | installed Li cell ≤ 20 Wh: allowed; no health claims in copy (S-08) | Many Kohl's/eBay sellers → saturation check matters | term: `scalp massager` | Zendrop/Spocket US | |
| 6 | Magnetic car phone mount (MagSafe-style) | F3 car | crevio (#19), Baseus/eBay US | $20–35 | $5–12 | none | Branded players (Baseus) advertise; avoid "MagSafe" trademark in copy (use "magnetic") | term: `magnetic car mount` | Zendrop/Spocket/CJ US | |
| 7 | Gravity electric salt & pepper grinder set | F1 kitchen | copyfy (#1), search summaries | $30–40 | $11–15 | AA batteries (customer-supplied) or installed cell | Gift season fit | term: `electric salt pepper grinder` | Zendrop/Spocket US | |
| 8 | Rechargeable neck reading light | F1 home | copyfy (#6, "low saturation") | $25–35 | $13–16 | installed cell ≤ 20 Wh: allowed | Low price → needs bundle (2-pack) to carry $30 CPA | term: `neck reading light` | Zendrop/Spocket US | |
| 9 | Motion-sensor under-cabinet / closet lights (rechargeable) | F1 home | crevio (#15) | $20–35 per pack | $6–12 | installed cell: allowed | Multi-pack bundles; mature category | term: `motion sensor closet light` | Zendrop/Spocket/CJ US | |
| 10 | Heatless curling rod set | F1 personal care | crevio (#6) | $20–30 | $3–8 | no body-image claims (S-08) | Very cheap to source; saturation on TikTok Shop likely | term: `heatless curler` | Zendrop/Spocket US | |
| 11 | Lick mat / slow feeder bundle (pet) | F2 pet | crevio (#3), sellthetrend category | $20–30 (bundle) | $3–8 | none | Only works as a bundle; silicone, light, cheap shipping | term: `lick mat dog` | Spocket/Zendrop US | |
| 12 | Anti-slip ice cleats for shoes | F1 seasonal | copyfy (#10, "low saturation", ~70% margin) | $20–30 | $4–7 | sizing (S/M/L) → some returns | US winter window Nov–Feb; needs size chart | term: `ice cleats` | Zendrop/Spocket US | |

Rejected from the lists, with reason: magnesium/sleep supplements and skincare sets (health/beauty claims, S-08, FTC); shapewear and clothing (sizing returns 24–40%, S-72); USB heated vest and car jump starter (large lithium cells, S-61); LED face masks (cosmetic-device claims); kids' advent calendars and squishies (children's product, S-60); Bluetooth trackers (compatibility claims, S-113 itself warns); Temu/Tefal/Joe's Doors items (brands, not dropship).

## Pass criteria for the operator's three columns (from the registry template)
- Price point (added 2026-11-10 from sweeps 6–7, rule LP4): the observed sale price must be ≥ $49, or the row becomes a bundle that reaches ≥ $49 with contribution ≥ 55%. Reason: at benchmark CPC $0.57–1.72 and ~1.5% conversion, cost per purchase is $38–115, above the breakeven CPA of a $40 product. Rows 8, 10, 11, 12 (neck light, heatless curler, lick mats, ice cleats) need bundles; rows 1, 6, 7 are borderline.
- Library: ≥ 2 advertisers with the oldest start ≥ 21 days ago (demand) and ≤ 5 US advertisers for the same product (not saturated).
- Supplier: a SKU that shows "ships from US" with landed cost (product + US shipping) and stated days; no blended estimates.
- Contribution: (observed sale price − landed cost) ÷ price ≥ 0.55.
Rows passing all three become P-0001.. in `registry.md` in the order of contribution share.

## Sources added
S-109 TrendTrack "best products on Meta for dropshipping 2026" (vendor; reach/growth figures; contains an editorial note that fashion data was reused); S-110 copyfy November 2026 top 10 (vendor; prices updated Oct 27, 2026); S-111 AutoDS November 2026 list (vendor; Oct 15, 2026; TikTok ad reviews, two AutoDS scores); S-112 crevio Q4 2026 list (vendor; Oct 29, 2026; category-level TikTok Shop data); S-113 sellthetrend pet page (vendor; Nov 8, 2026; internally inconsistent margins); S-114 roha-home.com + Trustpilot; S-115 "Petzrella" search (not found) + Doba US-ship listing; S-116 Faire/eBay US listings for candle warmer lamps.

## Program fill of the operator columns (2026-11-11)

Operator asked the program to do the columns itself. Result: column 2 (US supplier) and column 3 (observed sale price) filled from public pages; column 1 (Ad Library) remains the operator's, 12 link-clicks, because facebook.com/ads/library returns 403 to the program and has no public API for commercial ads (S-63, S-64). Doba and Eprolo show US stock and delivery days publicly but hide unit prices behind a free sign-up (S-166, S-167): the mother reads those prices at M0 step 4 (one free account, no card).

| # | Product | Col 2: US-warehouse supplier (program) | Col 3: observed sale prices (program, public pages) | Price test LP4 (≥ $49) | Program verdict before the Library check |
|---|---|---|---|---|---|
| 1 | No-drill vacuum suction hooks | not found on Doba/Eprolo by search (sites poorly indexed); Walmart/Fruugo retail $15–17 per 2–4 pack implies sourcing ≤ $5; supplier to confirm on Doba/Eprolo search at sign-up | Fruugo $15–17; Kohl's 2-pack; Walmart multiple; Roha Home price not visible, "Free worldwide shipping for order over €50" (S-114, S-168) | fails alone; 6–8-pack bundle could reach $49 | bundle only; saturation high (dozens of Walmart clones) |
| 2 | Elevated / tilted pet bowl | **Doba: "Ships from United States, Est. delivery time 3-7 days", 3 business days processing, suppliers AOSOM/PawHut and Grace Paws, price on sign-up (S-166); Eprolo: "in US Warehouses", "2 - 3 Business days", price unrendered (S-167)** | Chewy Yamazaki tilted $28.00, Necoichi $25.28; Fruugo $27.95; Walmart Pet Life $15.99; Fruugo ceramic $89 outlier (S-169) | fails at $25–28 market; passes only as a premium ceramic/wood design at $49–59 | keep as design-led variant; verify Doba price |
| 3 | Automatic pet feeder | Eprolo lists a 4.5 L app feeder with US-warehouse field, "2 - 3 Business days", price unrendered (S-167); Doba not found by search | Taavita (dropship-style store) $96.95, free US shipping, 2–10 business days, "Sale ends soon" badge (S-170); Walmart $30.99–33.79; small stores $20–27 (S-171) | passes ($49–97 observed) | **strongest on price**; electronics returns 8–10%; app-support load |
| 4 | Candle warmer lamp | Faire wholesale "Ships from United States" (stock purchase, not dropship) (S-116); Doba/Eprolo not found by search | Grove $34.99 silver hobnail; Candle Warmers Etc $35–45; Walmart dimmable; AutoDS claims $47.72 (S-111, S-172); candlewarmersshop.it.com unreachable from this session (host not allowed) | borderline at $35–48; passes at $49 with timer/dimmer design | keep; fragile → packaging check at sample |
| 5 | Electric scalp massager | not found on Doba/Eprolo by search; Walmart third-party sellers $14.99–56.99 imply sourcing $8–20 | Target (HONGGE) $53.99; Walmart $14.99–56.99; Kohl's $118.96 outlier (S-173) | passes at $49–55 | keep; no health claims in copy (S-08) |
| 6 | Magnetic car phone mount | not found on Doba/Eprolo by search; Fruugo "Shipping from China ~3 weeks" listings dominate | Fruugo $18–29; Walmart $11.50; Scosche $34.02; avenova.it.com dropship store (price not fetched) (S-174) | fails at $18–34 | bundle (mount + cable) or drop |
| 7 | Gravity electric salt & pepper grinder set | not found on Doba/Eprolo by search | zyrestore.com (dropship-style) $18.97, "regular price" $27.97, sold out; Walmart/Costco $19.97 two-pack; Kalorik at Lowe's (S-175) | fails at $19–28 | drop unless premium set at $49 |
| 8 | Rechargeable neck reading light | not found; Glocusent is the dominant brand | Walmart $19.99–30.64; reach.dog $21.98 (S-176) | fails | drop (brand-dominated, $20) |
| 9 | Motion-sensor closet lights (3-pack) | not found | Ironsmith Lighting 3-pack $36.99 (sold out); Fruugo $21.95; eBay $17.99 (S-177) | fails alone; 6-pack at $49 possible | bundle only |
| 10 | Heatless curling rod set | not found | Fruugo $7.50–30.95; Gimme Beauty, Kitsch brand sets (S-178) | fails | drop |
| 11 | Lick mat / slow feeder bundle | not found | PetSmart/Chewy $5.97–19.99 (S-179) | fails alone; 3-mat bundle ≈ $30 | drop |
| 12 | Anti-slip ice cleats | not found | Yaktrax Pro $29.99; Action Traction $20.99; generics $5–10 (S-180) | fails | drop |

### What this means
- The price criterion from sweeps 6–7 (LP4) removes 7 of 12 rows outright and leaves 3 that pass on observed prices: **automatic pet feeder (3), candle warmer lamp (4), electric scalp massager (5)**, plus 2 bundle-only rows (1, 9) and 1 design-led variant (2). This is a result, not a setback: the list came from vendor trend posts, and most of what they list sells at Walmart for $15–30.
- Column 1 (Ad Library) is still required for the survivors: 6 rows → 6 link-clicks for the operator (products 1–5 and 9). The links are in the main table above.
- Supplier prices for rows 2–3 come from a free Doba/Eprolo sign-up at M0 step 4 (mother). Until then the landed cost is bounded by Walmart retail (sourcing ≤ 50% of Walmart's price is the usual relation; Inferred).
- A network note for the record: `candlewarmersshop.it.com` did not resolve from this session (host not in the session's allowed network); it was a sale-price source only and is not needed.
