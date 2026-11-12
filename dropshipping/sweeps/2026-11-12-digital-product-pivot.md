# Sweep 8 (2026-11-12): should the program pivot to a self-made digital product instead of dropshipping?

Operator question: "Is it worth more to come with a digital product we create, no shipping, something of quality, and advertise it?" Decision frame: same cap ($2,000), same operator (15, mother holds accounts), same laws (truth before goal, register before look, policy as hard constraint). Sources S-224..S-232; most are secondary and say so. Depth is below the 15-source minimum for a full area; this is a decision sweep, re-opened to full depth only if the operator chooses the track.

## 1. What changes in the arithmetic (computed, `phase1/unit_economics.py` logic, Shopify Payments 2.9% + $0.30, no landed cost)

| price | refund allowance | contribution | share | breakeven ROAS | CVR needed to break even at CPC $0.78 | at CPC $1.72 |
|---|---|---|---|---|---|---|
| $19 | 5% | $17.20 | 0.91 | 1.10 | 4.5% | 10.0% |
| $29 | 5% | $26.41 | 0.91 | 1.10 | 3.0% | 6.5% |
| $29 | 10% | $24.96 | 0.86 | 1.16 | 3.1% | 6.9% |
| $39 | 5% | $35.62 | 0.91 | 1.09 | 2.2% | 4.8% |
| $49 | 5% | $44.83 | 0.91 | 1.09 | 1.7% | 3.8% |

Compare the physical candidates: share 0.37–0.50, breakeven ROAS 2.0–2.7. A digital product keeps 86–91% of every dollar and breaks even at ROAS ≈ 1.1. **But the price is lower, so the cost per purchase must be lower too.** Meta cold-traffic conversion for ecommerce is ~1.5–1.6% across vendor benchmarks (S-226; the same number as sweep 6). At $29 the product needs 3–7% conversion from cold ads to break even: 2–4× the typical rate. At $49 it needs 1.7–3.8%: reachable only at the low end of CPC. Conclusion: **paid Meta ads for a digital product are not easier than for a physical one; they are easier only above ≈ $49, or with a channel that costs less than $0.78 a click.** Those channels exist for digital goods and not for dropshipped goods: Etsy search, Pinterest, TikTok/Shorts organic, and the operator's own content.

Stop rule if a digital hypothesis is registered (same two-tranche design): at $29, T1 $120 continue if purchases ≥ 5, T2 $120 pass if ≥ 2 (P(pass|good) 0.70, P(pass|bad) 0.07); at $49, T1 $120 continue if ≥ 2, T2 $240 pass if ≥ 5 (0.73 / 0.07).

## 2. What is better (Observed unless marked)

- No supplier, no shipping, no FTC 30-day shipping rule, no lithium, no customs, no sample order, no working capital tied in goods. The per-order cost is the processor fee. Fulfilment is the free Shopify Digital Products app (4.8 from 1,463 reviews, "Set access limits and send digital asset links after purchase", S-228), so the store already opened serves both tracks.
- Platform fee alternatives: Gumroad 10% + $0.50 per direct sale, 30% on Discover sales, Gumroad as merchant of record since Jan 1, 2025 (primary, S-224); Etsy ≈ $0.20 listing + 6.5% transaction + 3% + $0.25 processing for US sellers (secondary, S-225; Etsy's own fee page refused fetch).
- Refund allowance lower than physical: ebooks/templates 2–5%, courses 5–12%, chargebacks 0.2–0.6% (all vendor estimates, S-229). Used here as 5–10%.
- The operator can make the product with the skills they have; nothing is bought.

## 3. What is worse or unknown

- **Demand and saturation.** Every vendor guide rates printables, planners and Notion templates as very high competition; Semrush-based proxy (Oct 2026) says Canva templates and budget spreadsheets rising, Notion templates, digital planners and printable wall art cooling (S-230, secondary). AI has removed the skill and time barriers, which is the mechanism of flooding; no source measures the effect (Unknown).
- **Typical earnings.** No primary data. Secondary claims conflict: $340 median monthly for active Gumroad sellers with 5+ products vs "$1,000–5,000" elsewhere; both unverifiable (S-224 notes). Outliers (Thomas Frank $2.5M on Notion templates) are not evidence about the median (S-230). Label: Unknown.
- **Meta policy.** "Unrealistic outcomes" standard: no promises of economic outcomes, no testimonials promising results without qualification (S-227, official page refused direct fetch, text via snippets). Income-themed digital products (make-money courses, side-hustle templates) sit in the business-opportunity class with higher review risk; health-themed ones (diet plans, fitness programs) hit the health-claim class. A digital product for this program must be in neither: utility, design, learning, hobby.
- **Review mining still applies (LP5):** no digital product is built without ≥ 30 real reviews of comparable products.

## 4. Verdict (Inferred from §1–§3)

1. **Not instead; in addition.** The dropshipping track already has a store, a supplier app and four registered hypotheses with packages; cancelling it saves nothing (fixed cost $1). The digital track costs $0 to build and shares the store. Running both is allowed by the ledger and by the serial-test rule (one *paid* test at a time; organic distribution of a digital product spends no ad dollars and is not a tranche).
2. **Paid Meta ads are not the digital product's channel at launch.** Organic first (Etsy listing, TikTok/Shorts demos, Pinterest), because the arithmetic needs clicks under ≈ $0.50 or conversion above 3%. A $120 Meta tranche only after the product has sold ≥ 10 copies organically (proof of demand and page conversion), or if it is priced ≥ $49 with proof it is worth it.
3. **Candidate families that fit the operator and the policies** (to be screened with the same table as `sweeps/candidates-2026-11-10.md`: Ad Library/Etsy demand, competition, price ≥ $29 or bundle, ≥ 30 reviews mined): (a) a tool for a hobby the operator knows better than adults do (templates, trackers, guides for a game, a sport, a school subject in the US system); (b) design assets (Canva templates for a specific profession, not "social media templates"); (c) study/planning systems for students the operator's age, sold to parents at $29–49. Excluded: income/side-hustle products, health/diet/fitness, anything with AI-generated bulk content sold as original, anything using others' IP (game assets, fonts, brand names).
4. **Registration gate:** a digital hypothesis is registered as D-0001 only with: the product built and finished, a page built from ≥ 30 real reviews, price and stop rule from §1, a channel plan that starts organic, and a prior P(pass) stated before any listing.

## 5. Honest base rate
No census of digital-product sellers exists; the $340-median figure is unverified. The same sentence as for dropshipping applies: most people who try earn little, a few earn a lot, and nothing in the sources identifies in advance who is who except the quality of the product and the depth of the niche. Belief changes none of these numbers.
