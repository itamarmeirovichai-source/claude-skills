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
- Library: ≥ 2 advertisers with the oldest start ≥ 21 days ago (demand) and ≤ 5 US advertisers for the same product (not saturated).
- Supplier: a SKU that shows "ships from US" with landed cost (product + US shipping) and stated days; no blended estimates.
- Contribution: (observed sale price − landed cost) ÷ price ≥ 0.55.
Rows passing all three become P-0001.. in `registry.md` in the order of contribution share.

## Sources added
S-109 TrendTrack "best products on Meta for dropshipping 2026" (vendor; reach/growth figures; contains an editorial note that fashion data was reused); S-110 copyfy November 2026 top 10 (vendor; prices updated Oct 27, 2026); S-111 AutoDS November 2026 list (vendor; Oct 15, 2026; TikTok ad reviews, two AutoDS scores); S-112 crevio Q4 2026 list (vendor; Oct 29, 2026; category-level TikTok Shop data); S-113 sellthetrend pet page (vendor; Nov 8, 2026; internally inconsistent margins); S-114 roha-home.com + Trustpilot; S-115 "Petzrella" search (not found) + Doba US-ship listing; S-116 Faire/eBay US listings for candle warmer lamps.
