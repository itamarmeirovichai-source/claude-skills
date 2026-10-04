# PumpWatch: Pricing comparables and pricing hypothesis

*Customers & Pricing team. Research date: 2026-10-04. Vendr figures are crowd-sourced buyer data, not list prices. Anything not confirmed from a source is marked **UNVERIFIED**.*

---

## 1. Comparable tools: what buyers actually pay

| Tool (category) | Price / contract size | Basis | Source |
|---|---|---|---|
| **NICE Actimize** (AML / surveillance, enterprise) | Median **$182k/yr**; range $156k-$948k | Vendr buyer data | https://www.vendr.com/marketplace/nice-actimize |
| **Unit21** (AML transaction monitoring, fintech) | Median **$123k/yr**; range $26k-$221k | Vendr | https://www.vendr.com/marketplace/unit21 |
| **ComplyAdvantage** (AML screening) | Median **$53k/yr**; range $20k-$330k | Vendr | https://www.vendr.com/marketplace/complyadvantage |
| **Smarsh** (comms archiving and supervision for brokers) | Median **$22.8k/yr**; range $3.3k-$131k; $8-35+/user/month | Vendr page as read. A search snippet showed a $100k median, so the figures are inconsistent; we use the page value. | https://www.vendr.com/marketplace/smarsh |
| **Global Relay** (archiving, small brokers) | Median **$6.8k/yr**; range $1k-$7.8k | Vendr. Likely biased toward small buyers. | https://www.vendr.com/marketplace/global-relay |
| **Vanta** (compliance automation) | Median **$20k/yr**; $12k-28k small orgs, $25k-55k mid | Vendr (373 purchases) | https://www.vendr.com/marketplace/vanta |
| **Dataminr** (social/real-time alerting, corporate) | Median **$22k/yr**; range $15k-62.5k, per seat | Vendr | https://www.vendr.com/marketplace/dataminr |
| **Dataminr** (government) | Federal obligations of about $60-81M per year, FY2020-25. A 5-year ceiling contract of **$318M** with the Dept. of War. Company ARR about $200-225M (**UNVERIFIED**, secondary sources) | USAspending-derived aggregators | https://fed360.agency/contractors/dataminr-inc-W23YFXYGM2K1?tab=awards ; https://yespress.io/dataminr |
| **SEC social-media monitoring** (procurement) | 2018 solicitation budget up to **$27.5M** (stale). A 2024 sole-source award to Meltwater (amount not shown). | Gov procurement | https://www.meritalk.com/articles/sec-looking-for-social-media-monitoring-tool/ ; https://sam.gov/opp/a8275d265f9c4788bde9367780f95ad5/view |
| **Nasdaq Verafin** (bank AML) | 2,500+ financial institutions. ARR +19% y/y (Q2 2025). No price disclosed. | Nasdaq filings and results | https://ir.nasdaq.com/node/109901/pdf |
| **Eventus Validus** (trade surveillance for brokers) | Not public ("pricing on request"). $48.5M raised in total. | Vendor and press | https://www.eventus.com/ufaq-category/pricing-roi/ ; https://www.thetradenews.com/centana-growth-partners-leads-30-million-funding-round-in-eventus-systems/ |
| **RavenPack** (news/sentiment data) | Not public. Enterprise ACVs "often above $250k" | Template-blog source, **UNVERIFIED** | https://businessmodelcanvastemplate.com/blogs/how-it-works/ravenpack-how-it-works |
| **Stocktwits** (data firehose) | Not public, custom licensing | **UNVERIFIED** | https://bankinnovation.net/allposts/risk-security/stocktwits-to-add-news-api-video/ |

**Context:** fines against small firms for the exact failure we address run **$250k-$1.3M**, plus a mandatory consultant (see customers.md §4). Those consultant fees are also typically six figures (**UNVERIFIED**).

## 2. Data costs (cost of goods)

| Input | Public price | Source |
|---|---|---|
| **X API** (pay-per-use; default since 6 Feb 2026; legacy Basic/Pro migrated by Jun and Sep 2026) | **$0.005 per post read**, $0.010 per user lookup. Repeat reads of the same post within 24h are charged once. Cap of **3M post reads per month**; above that, Enterprise only. | https://docs.x.com/x-api/getting-started/pricing (official, read 2026-10-04) |
| X Enterprise | "$42,000+/month" | Secondary blogs only, **UNVERIFIED**: https://www.postproxy.dev/blog/x-api-pricing-2026/ |
| **Reddit Data API** | **$0.24 per 1,000 calls**; optional $12k/month bundle for 50M calls | Secondary, consistent across sources: https://www.techloy.com/reddit-api-pricing-in-2026-complete-guide-for-developers-and-businesses/ |
| Market data (Polygon/Massive) | $199/mo Advanced is for **individual, non-professional use only**. Commercial or business licence is separate and its price is **UNVERIFIED**. | https://apicostcalc.com/es/blog/polygon-massive-rebrand-api-pricing.html |
| SEC EDGAR | Free (rate-limited) | https://www.sec.gov/os/accessing-edgar-data |
| Telegram public channels | API is free, **but Telegram's terms prohibit this use** (non-ordinary access to user content, scraping public channels, ML use). Not a usable source without a lawyer-approved path. See regulation.md §0/§2. | https://telegram.org/tos/content-licensing ; https://telegram.org/tos/bot-developers (verified by dept. head 2026-10-04) |

**Unit economics (estimate, UNVERIFIED):**
- Social data cost is **shared across customers**, because everyone watches the same ~2,000-3,000 small-cap tickers. Each customer adds almost no data cost, so COGS is close to a fixed monthly amount.
- X is the main cost. 1M post reads/month costs $5k. At the 3M cap it costs **$15k/month**, which equals 5-10 small customers' fees. Enterprise X (≈$42k+/mo, unverified) only makes sense after about 15-20 customers.
- Reddit is cheap: 1M calls costs $240.
- Assumed data budget: Phase 1 (pilots) about **$1-3k/month** (X capped by a spending limit, plus Reddit, Stocktwits public, EDGAR, an entry market-data licence). Phase 2 (10 customers) about **$8-20k/month**.
- That means gross margin at about 10 small customers is roughly 50-70%, rising to over 80% at 25 or more customers. These are typical data-SaaS figures, **UNVERIFIED**.
- **Bigger than cost: permission.** X's Developer Agreement bans use for "surveillance or gathering intelligence" and crime-related profiling without X's written approval; Reddit bans "surveillance purposes" (see regulation.md). The X cost lines above only matter if X approves the use case in writing. Until then, budget for StockTwits (licenses to financial institutions) + EDGAR + market data.
- **Contractual risk:** X and Reddit terms may restrict redistributing raw content to third parties. Ship **derived signals and post links**, not copied posts. Check the terms before the first paid contract (**UNVERIFIED**, not yet reviewed).
- **Budget fit:** with a $30k budget, the founder cannot pay for X Enterprise. Start on pay-per-use with a hard monthly cap ($500-1,000) and focus on cashtag queries for watchlist tickers only.

## 3. Recommended pricing hypothesis

**Structure:** an annual contract, billed quarterly or annually. Price on **two axes**: firm size (active funded accounts) and coverage (exchange-listed small caps only, or also OTC). Add-ons: API/SIEM export, SAR-ready case reports, historical lookback.

| Tier | Who | Monthly | Annual | Comparable anchor |
|---|---|---|---|---|
| **Pilot** | Any | Historical backtest **free (2 wks)**; live pilot **$1,500-3,000 flat for 90 days**, credited to year 1 | n/a | A paid pilot tests real willingness to pay. Gate D needs a paid contract. |
| **S: Small** | BD or app with under ~50k funded accounts; small underwriters; short-locate brokers | **$1,500-3,000** | $18k-36k | Between Smarsh/Dataminr/Vanta medians ($20-23k) and ComplyAdvantage ($53k). |
| **M: Mid** | 50k-1M accounts; small or mid clearing firms (Velox-type) | **$5,000-12,000** | $60k-144k | Unit21 median of $123k. |
| **L: Large / BaaS / exchange** | Over 1M accounts; Apex/Alpaca-type platforms; exchanges | **$15k-40k+, custom** | $180k-500k+ | NICE Actimize median of $182k, up to $948k. |

**Sanity check against PLAN.md §7** ($1.5-5k small / $5-20k mid / custom large):
- **Small: lower the top end from $5k to about $3k/month.** The tools small brokers buy for comms archiving and compliance cost a median of about **$7k-23k/yr** (Global Relay, Smarsh, Vanta on Vendr). A brand-new single-signal tool from a solo founder will struggle at $60k/yr for a firm with fewer than 150 reps. $1.5k/month is a reasonable entry price. $5k/month only works for a small firm under a FINRA consultant mandate.
- **Mid: $5-20k/month is plausible** but at the top of the range. That equals $60k-240k/yr, which overlaps full AML platforms (Unit21 $123k, Actimize $182k). PumpWatch is an **add-on signal**, not a replacement platform, so $5-12k is more defensible until the product works as a case-management system of record.
- **Large/custom: agreed.** Buyers here may prefer a **data-feed licence** (signals delivered into their own surveillance stack, such as SMARTS or Eventus) over a UI. Price it like a data licence ($100k+/yr, **UNVERIFIED**).

**Further pricing levers:**
- **Offer a "consultant remediation package"**: a 12-month commitment with an evidence pack written for FINRA certification. It targets firms under AWC undertakings (Velox, TradeUP, Network 1, Redbridge). Their budget already exists, so the price can sit at the top of tier S or M.
- **Avoid per-alert pricing.** It rewards noisy alerts, and compliance teams dislike variable bills.
- **Annual escalator** of 5-7%, which is standard in Vendr data for comparable compliance software.
- **Revenue target check:** 10 customers at a $30k average gives $300k ARR, enough for a founder plus 1-2 staff after data costs. Reaching $1M ARR needs about 25 S-tier and 5 M-tier customers, or one BaaS/clearing deal plus about 15 S-tier customers. This is arithmetic on the hypotheses, **UNVERIFIED** against real demand.

## 4. Open questions to test on discovery calls

1. Do they already pay for trade surveillance (SMARTS, Eventus, NICE, in-house)? A social-signal add-on is priced against that existing spend.
2. Who owns the budget: AML/BSA or surveillance/compliance? (Fines cite both 3310 and 3110.)
3. Would they accept signals-only output (no raw posts), given redistribution limits on social data?
4. Is a $1,500-3,000 paid 90-day pilot acceptable, or must the pilot be free?
