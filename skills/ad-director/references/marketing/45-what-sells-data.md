# 45 · What sells: the data behind films that get views *and* purchases

Research brief, 2026-10-09. Question: which video ads actually earn views and purchases for US founder-led DTC brands in beverage, fragrance, candles and home? What does that mean for the films VXO makes (Short $1,200 · Premiere $2,500 · Season $3,500/mo · "5 free frames" lead magnet)?

This doc **builds on** `23` (coded long-runner sample, Benly, Motion 2026 hit rates), `38` (hooks, Meta×Toluna, hook-rate benchmarks) and `32` (positioning, competitor prices). It does not repeat them in full. It adds:
- AI-ad studies (disclosure, AI vs human, neuro);
- platform policy on weapons, violence, police, AI labels and impersonation;
- outcome benchmarks (CPA/ROAS/CTR);
- founder evidence;
- AI-studio competitor pricing;
- a ranked rule set and the next 6 portfolio films.

**Tags:**
- `[unverified]`: we could not confirm the figure or rule against a primary source.
- `[inf]`: our own inference.
- `[vendor]`: the number comes from a company that sells the thing being measured.

---

## 0. Method and limits (read first)

| Source asked for | Result |
|---|---|
| **Motion Creative Analytics MCP** | **Auth failed for data purposes.** `get_auth_context` returned `organizations: []`, `defaultWorkspaceId: null`. Every insight, Inspo, glossary and brand tool needs a `workspaceId`, so we pulled **no** top creatives, hook/hold metrics, Inspo creatives or glossary values. The same thing happened on 2026-10-08 (`23` §0). Fix: create or join a Motion workspace (free trial) and re-run §9. |
| Motion 2026 Creative Benchmarks (public page) | Read in full. 550K+ Meta ads, 6K advertisers, ~$1.3B spend, Sep 2025 to Jan 2026. Hit rate = share of ads reaching ≥10× account-median spend. |
| Meta / TikTok / Google policy pages | Meta weapons policy and TikTok violence policy were read **directly**. The AI-label rules for Meta and TikTok ads come from secondary sources, so they are tagged. |
| Billo H1 2026 benchmarks | Read directly. 88,329 sales-objective Meta video ads, $122M spend. |
| Triple Whale benchmarks | Page returned 403. Numbers are from search snippets; the page's text and its table disagree, so tagged `[unverified]`. |
| Varos, Northbeam, Atria, Foreplay | **No public benchmark report found** for hook, hold or CPA. Northbeam: one case study only (Vessi). Do not cite these brands for benchmarks. |
| TikTok Creative Center Top Ads | Not scrapeable without a signed session (`23` §0). We use TikTok's published policy pages and its one widely cited length stat. |
| Peer-reviewed AI-ad studies | Abstracts and summaries only. Full texts were not read. |

**Bias warning.** Most hit-rate data measures *spend scaling* (Motion) or *survival* (Benly, `23`). Neither is purchases. Brands scale what converts, so both are proxies for purchases, not the real thing `[inf]`. The only direct purchase-side measures here are Meta×Toluna (stated purchase intent), Billo/Triple Whale ROAS, and founder anecdotes.

---

## 1. Data table (with sources)

### 1.1 Formats and assets: what scales on Meta

| # | Finding | Number | n / scope | Source | Status |
|---|---|---|---|---|---|
| D1 | Only a small share of ads become winners | **5–8 %** hit rate; ~half never get meaningful spend | 550K ads | [Motion 2026](https://motionapp.com/thumbstop-pulse/creative-benchmarks-2026) | Read |
| D2 | Asset type hit rate: text-only / product image + text / lifestyle-product / **UGC / high production** / animation | 11.6 / 8.75 / 7.59 / **7.56 / 6.97** / 4.57 % | same | same | Read |
| D3 | Format hit rate: **unboxing 9.83**, offer-first banner 8.68, BTS 8.64, **founder 8.57**, POV 8.28, **demo 8.11**, influencer 7.71, montage 7.02, **cinematic b-roll 6.85**, how-to 6.62, testimonial 6.57, before/after 6.07, review 4.89 % | — | same | same | Read |
| D4 | Visual style hit rate: letter 10.83, unconventional text placement 9.63, **ASMR 8.58**, founder 8.57, sign 7.86, UGC overlay 6.73, us-vs-them 6.52 % | — | same | same | Read |
| D5 | Hook hit rate: **newness 11.37, sale 11.35, price anchor 10.89**, urgency 9.73, confession 8.74, curiosity 7.77, bold claim 7.19 … **question 5.47**, storytelling 6.23 % | — | same | same | Read |
| D6 | Home & lifestyle: "demonstration and process matter most"; fashion: culturally fluent, playful visuals | qualitative | same | same | Read |
| D7 | Beauty: UGC ≈ studio ≈ product shot on survival; home: **product shot 66 vs lifestyle 30** (effectiveness index) | index | 271K creatives | [Benly Q1 2026](https://benly.ai/benchmarks/q1-2026) via `23` §1.1 | Read 10-08 |
| D8 | Fragrance creatives have the shortest life of our niches: **27 d**; coffee/tea 38 d | days | same | same | Read 10-08 |

### 1.2 Purchase-intent drivers (Reels)

| # | Finding | Lift | Source | Status |
|---|---|---|---|---|
| D9 | Product + context/USPs | **5.3×** top-20 % purchase intent | Meta×Toluna 2024, 100 ads × 100 viewers ([ppc.land](https://ppc.land/meta-and-toluna-study-finds-emojis-lift-reels-purchase-intent-2-5x/)), see `38` §1.1 | Secondary; stated intent |
| D10 | Brand on screen for ≤25 % of the duration | 4.8× | same | same |
| D11 | Product shown 2+ times | 2.7× | same | same |
| D12 | CTA, visual or spoken | 1.9× | same | same |
| D13 | Brand + message in the first 5 s | 1.7× | same | same |
| D14 | Hook uses visual **and** audio cues | 1.5× | same | same |
| D15 | 9:16 + sound + safe zone vs image ads | 2× delivery, **"134.5 % lower CPA"** | Meta creator event summary ([coolerinsights](https://coolerinsights.com/2025/04/insights-from-metas-first-creator-event-in-singapore/)) | `[unverified]`: a >100 % reduction is not arithmetically meaningful; directional only |

### 1.3 Attention benchmarks

| # | Metric | Value | Source | Status |
|---|---|---|---|---|
| D16 | Meta hook rate (3 s plays ÷ impressions), sales ads | **25.44 %** avg, H1 2026 (up from 24.42 %) | [Billo H1 2026](https://billo.app/blog/h1-2026-video-ad-benchmarks/), 88,329 ads, $122M | Read |
| D17 | Hook-rate median / top 10 %: Meta 28/45 %, TikTok 33/55 %, YouTube 22/38 % | — | Motion data relayed by novoads/segwise (`38` §1.2) | `[unverified]` (relayed) |
| D18 | Hold rate (15 s ÷ 3 s plays) | avg 40–50 %, >60 % strong | [Motion blog](https://motionapp.com/blog/key-creative-performance-metrics) | Definitions vary; some practitioners use 20–25 % on other definitions ([kompozy](https://kompozy.io/guides/paid-social-creative-performance-2026)) |
| D19 | Health & Beauty CTR 2.36 % (best of 14 categories), ROAS 1.82 (11th) | — | Billo H1 2026 | Read. High clicks ≠ high ROAS |
| D20 | Cross-industry ROAS on sales video ads fell 2.41 → 2.17 over H1 2026 | −10 % | Billo H1 2026 | Read |

### 1.4 Outcome benchmarks

| # | Metric | Value | Source | Status |
|---|---|---|---|---|
| D21 | Meta median CPA / CPM / ROAS / CVR, 2025 | ~$38 / $13.5–14.2 / 1.86–1.93 / 1.57 % | [Triple Whale](https://triplewhale.com/blog/facebook-ads-benchmarks) | `[unverified]`: page 403, and text vs table conflict |
| D22 | Meta ROAS by vertical: Beauty 1.57, Food & Bev 1.56 | — | Triple Whale via [Influee](https://influee.co/blog/facebook-ads-benchmarks) | `[unverified]` |
| D23 | Video wins CTR in nearly every account; **static matched or beat video on ROAS** in most large, cleanly tracked accounts | 83 brands (ROAS comparison on 5) | [Jetfuel](https://jetfuel.agency/facebook-ad-creative-strategy-the-optimal-meta-media-mix-for-roas-and-reach/) | `[vendor]`; small ROAS n |
| D24 | Median account mix: 61 % static, 39 % video | 67K ads | MisfitMarketing via [Segwise](https://segwise.ai/blog/static-video-ratio-meta-ads.md) | Secondary |
| D25 | Vessi: video cut CAC −42 % and lifted ROAS +61 % against the brand's own baseline | 1 brand | [Northbeam case](https://www.northbeam.io/post/creative-iteration-and-optimization-at-vessi-through-trustworth-first-party-metrics) | `[vendor]` |

### 1.5 Length

| # | Finding | Source | Status |
|---|---|---|---|
| D26 | 1 in 4 top-performing TikTok videos run 21–34 s, with ~1.6× impressions | TikTok, relayed ([onlinemarketing.de](https://onlinemarketing.de/social-media-marketing/3-minuten-videos-tiktok-videolaengen-vergleich)) | `[unverified]`: about organic content, not ads |
| D27 | Shorts ads: keep within **10–60 s**; vertical is prioritised; a swipe skips (no 5 s countdown) | [Google Ads help](https://support.google.com/google-ads/answer/16042150) | Primary |
| D28 | Reels: buyers report 15–30 s performing best (up to 90 s allowed) | [adadvisor](https://adadvisor.ai/blog/facebook-reels-ads) | `[vendor]` |
| D29 | Our long-runner median is 21 s and bimodal: ≤15 s editorial/loops and >30 s speech-led explainers | `23` §2.2 (n=35) | Own data |

### 1.6 AI-generated ads

| # | Finding | Source | Status |
|---|---|---|---|
| D30 | AI-generated banner images **matched stock photos; the best got up to +50 % CTR** (field test, 173K impressions) | Hartmann, Exner & Domdey, *IJRM* 2025 ([abstract](https://ideas.repec.org/a/eee/ijrema/v42y2025i1p13-31.html)) | Peer-reviewed; abstract only |
| D31 | AI ad images lift CTR **only if they don't look like AI**; human faces make them look AI and cancel the gain | Oxford Internet Institute, >2M daily ad observations ([OII](https://www.oii.ox.ac.uk/news-events/events/ai-in-disguise-ai-generated-ads-outperform-human-made-ads-if-they-dont-look-like-ai/)) | Working paper; summary only |
| D32 | AI ads produced **weaker memory activation** (EEG) even when rated high quality; low-quality visuals add cognitive load; possible negative halo on the brand | [NIQ, Dec 2024](https://nielseniq.com/global/en/news-center/2024/niq-research-uncovers-hidden-consumer-attitudes-toward-ai-generated-ads/), 2,000+ people, EEG on ~150 | Commercial research |
| D33 | AI **disclosure** lowered purchase intent through lower ad credibility, more so for AI-sceptics | Bui 2025, *JRIM*, n=358 ([manuscript](https://ray.yorksj.ac.uk/id/eprint/12761/3/Accepted%20manuscript_JRIM.pdf)) | Peer-reviewed; single study |
| D34 | AI labels have a dual effect: **novelty up** (helps), **authenticity down** (hurts) | Shi & Jiang, *SAGE Open* 2026 ([DOI](https://journals.sagepub.com/doi/10.1177/21582440261417793)) | Peer-reviewed; abstract only |
| D35 | AI disclosure alone did not change purchase intent for a video ad (n=246), or ad credibility for medium-involvement products (n=125) | Lisbon thesis ([UCP](https://repositorio.ucp.pt/entities/publication/f3a910bd-ef4c-4de7-a76e-dc26ea617e88/full)), Twente ([essay](https://essay.utwente.nl/essays/107069)) | Theses; small n |
| D36 | Coca-Cola's AI "Holidays Are Coming" (2024) scored **5.9/6** on System1, with 3 % contempt; viewers weren't told it was AI. McDonald's NL pulled its AI Christmas ad within days (Dec 2025) after a backlash over "creepy" visuals | [MediaPost](https://www.mediapost.com/publications/article/401376/not-everyone-hated-that-ai-generated-coca-cola-hol.html), [NBC](https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590) | Press |
| D37 | AI UGC ≈ human UGC on CTR for AOV < $100; trust-heavy categories still favour real people | [FluxNote](https://fluxnote.io/guides/are-ai-ugc-ads-effective), [Segwise $115k test](https://segwise.ai/blog/115k-ai-ugc-platform-test-findings) | `[vendor]` `[unverified]` |

### 1.7 Founders and category evidence

| # | Finding | Source | Status |
|---|---|---|---|
| D38 | Poppi: the founder telling her story to camera was "still our number one converting ad" after ~2 years of paid spend; "incremental returns as much as 10×"; ~15 % of sales from TikTok, 80–90 % of commenters bought in store | [Modern Retail, 2023](https://www.modernretail.co/marketing/your-dollar-goes-a-little-bit-further-smaller-brands-are-finding-tiktok-to-be-a-more-profitable-advertising-channel/) | Founder claim |
| D39 | Liquid Death: one launch film ($1.5k production + $3k Facebook spend) → 3M views; brand built on entertainment, not DR | [secondary](https://startupbahrain.com/blog/liquid-death-turning-h2o-into-a-killer-brand) | `[unverified]` |
| D40 | Goose Creek Candles: 5.26× ROAS on YouTube with **UGC that highlights product attributes**, one video per campaign | [ATTN case](https://www.attnagency.com/case-studies/how-goose-creek-candles-scaled-youtube-to-75m-impressions-with-attn) | `[vendor]` |
| D41 | Snif (fragrance): ~10 new Meta creatives/week; library leans on headline 18 %, testimonial 17 %, split screen 7 %. Phlur: emotional narrative on Meta; TikTok as the demand engine | [Motion library](https://motionapp.com/library/snif), [adlibrary](https://adlibrary.com/brands/phlur) | Ad-library inference |
| D42 | Candle ads: specific *occasion* hooks beat "treat yourself"; gifting peaks in Q4 | [MHI](https://mhigrowthengine.com/candle-fragrance-brands-facebook-ads-agency/) | `[vendor]` `[unverified]` |
| D43 | Our long runners: product visible by 2 s in **83 %**; message-bearing text in **89 %**; hands-only ads lived ≥98 d in 6 of 8 cases | `23` §2.2 | Own data, n=35 |

### 1.8 Competitor pricing (AI studios)

| # | Who | Price | Source | Status |
|---|---|---|---|---|
| D44 | AI UGC operators | $50–500 per video; 10-video pack $500–3,000 | [Ciela](https://ciela.ai/blogs/ai-ugc-as-a-service-for-agencies) | `[vendor]` |
| D45 | MAW AI Studios | Spark **$500** (one 15–30 s spot, 2 revisions); Ignite **$2,000** (suite + 3 cutdowns) | via [studiolist](https://studiolist.co/guides/ai-video-production-cost/) | `[unverified]` |
| D45b | Live price pages read 2026-10-10 [m] | **ReelForge** (samedayads): $500 one 30 s video (1 format, 1 revision, 48 h); **$1,200** one ≤60 s video with 3 platform cuts, unlimited revisions, 4K, 24 h; $2,500 for 4 videos × 6 cuts. **Shhots** done-for-you: $499/mo for 30 videos (~$17 each). **1BVP**: $7,500 flat per 30 s spot, 7-day delivery (its own comparison page also lists a $2,000–9,000 market range and MaiDreamsLab €1,500–3,500, both secondary) | [ReelForge pricing](https://samedayads.lovable.app/pricing), [Shhots pricing](https://shhots.ai/pricing/), [1BVP](https://1bvp.com/ai-commercial-production/) | 3 of the 10 pages the backlog asks for. **Consequence:** a template studio sells a $1,200 film with 3 cuts and unlimited revisions, so our $1,200 Short can't win on price or asset count alone; it wins on the product-caused punchline, the physics/claims/QC sheet and the 4+ finished assets. Anchor against $7,500 studio spots, never against volume shops |
| D46 | MaiDreamsLab (IT) | €1,500–3,500 per 15–60 s spot | [MaiDreamsLab](https://maidreamslab.ai/en/blog/how-much-ai-commercial-pricing-2026/) | Self-published |
| D47 | 1BVP | $7,500 published; Genre.ai and Silverside: price on request | [1BVP list](https://1bvp.com/ai-commercial-production/) | Self-published |
| D48 | AI-native studios generally: $1–10k per 30–60 s spot; $10–20k a campaign with cutdowns | [Panda Studios](https://panda-studios.com/ai-commercial-cost-2026) | `[vendor]` |
| D49 | Genre.ai (PJ Accetturo): Kalshi NBA Finals spot, $2,000 production + "five-figure fee"; reported ~$100k per 30 s | [Wrapbook podcast](https://www.wrapbook.com/on-production-podcast/the-real-economics-of-ai-native-production-featuring-pj-accetturo), [CO/AI](https://getcoai.com/news/i-made-this-in-like-two-days-in-my-underwear-ai-studios-slash-advertising-production-costs/) | The $100k figure is `[unverified]` |

**Where VXO sits** `[inf]`: Short $1,200 and Premiere $2,500 are in the mid band of AI-native studios. That is above MAW's $500/$2,000 and below the $7.5k+ studios. The upper band sells **brand fame** (Kalshi, Coca-Cola). The lower band sells **volume**. The open lane is **conversion-grade product films**: AI craft plus DR structure, sold with proof.

---

## 2. Answers

### Q1. Which formats drive purchases for DTC beverage, fragrance and candles?

Ranked by the strength of the evidence for **purchases** (not views):

1. **Product-in-use / demo / process.** This is our best-supported faceless format.
   - Motion: demo 8.11 %, unboxing 9.83 %, ASMR 8.58 % (D3, D4).
   - Home is "demonstration and process" (D6).
   - Meta×Toluna: product + context = 5.3× (D9).
   - Benly home: product shot 66 vs lifestyle 30 (D7).
   - Beverage: pour, condensation, can-crack. Candle: match strike, melt pool, scent throw shown as a room changing. Fragrance: spritz, bottle in hand, skin.
2. **Founder.** Hit rate 8.57 % as both a format and a style (D3, D4). Poppi's #1 converting ad was a founder talking to camera (D38). This is the strongest *purchase* anecdote in beverage. VXO makes faceless films, so we can't produce this format, but we can **frame** it (see the founder-insert format in §4).
3. **UGC / creator.** Hit rate 7.56 % vs high production 6.97 %: a near tie (D2). It wins on **trust-heavy, high-consideration** claims (D37, D40). Fragrance creators drive TikTok demand (Phlur, D41), but creator ads lived shorter in our sample (`23` §2.1).
4. **Offer / newness / price-anchor hooks.** These are the top three hook types at ~11 % (D5). They are short-lived by design (`23` §2.2), and they are the cheapest way to turn a *beautiful* film into a *selling* one: a launch card, "new scent", or "$X per can".
5. **Comparison / us-vs-them.** 6.52 % (D4). Useful for beverage, e.g. "vs soda: 5 g sugar". Weak for fragrance and candles, where comparing on attributes cheapens the brand `[inf]`.
6. **Cinematic hero / b-roll.** **6.85 %**, below the 7–8 % median of the formats listed (D3). It works as a **brand and fame asset** and as raw footage for cutdowns, not as a standalone DR ad. (Exception: Pique's 6 s pour loop and Brilliant Earth's render each ran >100 d in `23`, both short and product-filled.)

By niche `[inf]`, built from D3–D8 and D38–D42:

| Niche | Lead format | Second | Must-have layer |
|---|---|---|---|
| Beverage | Pour/ASMR product-in-use, 6–15 s | Founder or creator story (real person) | Taste/benefit claim + price per can |
| Fragrance | Bottle-in-hand + named moment ("The summer I wore…"), 10–15 s | Creator reaction / blind-buy story | Scent notes as text; refresh every ~4 weeks (D8) |
| Candles / home | Process: strike, burn, room glow, 15–20 s | UGC attribute walkthrough (D40) | Occasion hook (gift, Sunday reset) + burn hours |

### Q2. Where do cinematic AI films win, and where do they lose?

**Where they win:**
- **Novelty / visual intrigue.** Visual intrigue is the #1 hook in fashion, food and home (`23` §1.1). AI labels raise perceived novelty (D34). Ipsos found unique visuals 1.5× more effective (`23` §1.3).
- **Product-only scenes with no human face.** AI images beat human ones on CTR *when they don't look AI* (D30, D31). Faces are what give AI away (D31).
- **Impossible shots that show a product truth.** Scent becoming a room, a can in a glacier, a candle lighting a city. These are things a $3–10k shoot can't do (`32`).
- **Fame moments** with media behind them: Kalshi, Coca-Cola's 5.9/6 System1 score (D36, D49).
- **Variant volume.** One world → many hooks. Andromeda rewards *concept* diversity, and the agency rule of thumb is 8–20 distinct concepts per ad set `[unverified]` ([Atria](https://www.tryatria.com/blog/meta-andromeda-update), [Jon Loomer](https://www.jonloomer.com/meta-andromeda/)).

**Where they lose:**
- **Trust and efficacy claims** (skincare actives, supplements, "does it work?"). Disclosure lowers credibility (D33), and real people win these (D37, `23` §5).
- **Memory.** NIQ's EEG shows weaker memory activation even for high-quality AI ads (D32). Pure mood is forgotten, so **brand cues have to do the remembering**: pack in frame, sonic cue, a recurring visual signature.
- **Uncanny humans and emotional holiday stories.** McDonald's NL was pulled (D36). Faces cancel the AI CTR gain (D31).
- **Pure b-roll with no message.** Cinematic b-roll scaled at 6.85 % vs 11.6 % for text-only (D2, D3). Lifestyle-only scored 30 in home (D7).
- **Low-AOV volume testing.** At $50–500 per AI UGC clip (D44), a $2,500 film loses on cost per test unless it ships variants.

**How to combine them: the "Hero + DR stack"** `[inf]`, built on D9–D14 and `23` §5–6:
1. **0–1 s:** the cinematic frame **is** the product (pack legible). Add one native text hook: a claim, newness, or a named moment.
2. **1–5 s:** a motion onset plus a sound transient. Brand appears in context, in the scene (D13, D14).
3. **5–12 s:** product in use + **one proof line** (a number, ingredient or process). Show the product a second time (D11).
4. **Last 2–3 s:** CTA + offer/price if real (D12). The logo appears ≤25 % of the runtime (D10).
5. Ship each film as **hero 15–20 s + 6–8 s loop + DR cut** (VO-mechanism or native layer: iMessage, review card, offer UI), each with 3 hooks.

### Q3. Hook benchmarks, what moves them, and length by placement

**Targets** (Meta sales video, cold) `[inf]`, from D16–D18:

| Metric | Floor | Good | Top |
|---|---|---|---|
| Hook rate (3 s ÷ impressions) | 20 % | ≥25–30 % | ≥40–45 % |
| Hold (15 s ÷ 3 s) | 30 % | 40–50 % | >60 % |
| Outbound CTR | 0.8 % (food/drink) | 1.0–1.5 % | >2 % (beauty avg 2.36 %, D19) |
| CPA | the brand's breakeven | ≤ $38 (Meta median) `[unverified]` | — |

**What moves hook rate** (evidence in brackets):
- Product or product-in-use in frame 1, big [D43, D9].
- A text hook on screen at 0.0–0.5 s: newness, price anchor, confession or curiosity. These beat questions, which scored 5.47 % [D5].
- Visual + audio together: a diegetic transient such as a can crack, match strike or spritz hiss [D14].
- A motion onset in the first 0.5 s, not constant camera drift [`38` §1.3].
- Unconventional text placement or a letter/sign style [D4].
- No logo card, fade-in or black frame [`38` §1.4].

**Hook rate ≠ purchases.** Billo's Health & Beauty has the best CTR and only the 11th-best ROAS (D19). So score films on hold + CTR + CPA, not on hook rate alone.

**Length by placement:**

| Placement | Hero | Also cut | Evidence |
|---|---|---|---|
| Meta Reels / Stories | 15–20 s | 6–8 s loop; 30 s VO-mechanism DR | D28, D29, `23` §6 |
| Meta Feed (4:5) | 10–15 s | static from the hero still | D23, D24 (statics often match video on ROAS) |
| TikTok In-Feed | 15–25 s, native-styled | 21–34 s story version `[unverified]` | D26 |
| YouTube Shorts | 15–30 s, vertical, front-loaded | 6 s bumper | D27 |
| Website hero / PDP | 6–10 s silent loop | — | `33` |

### Q4. Policy constraints

See the cheat-sheet in §5. In short: VXO's action-comedy films (the AURUM heist, the car chase in `41`) are **fine as entertainment** on Meta, which explicitly allows weapons in fiction. They are **high-risk on TikTok**, which bans displaying police gear and "dangerous, harmful, or violent acts". The *ad cut* therefore needs a policy-safe variant.

### Q5. What a DTC founder needs to see in our portfolio, and which films to make next

What a founder needs to see `[inf]`, from D1, D9–D14, D38 and `32`:
1. **Their category, with the product big and the label sharp.** Fidelity is the AI objection.
2. **A selling structure, not just beauty.** Every tile shows the hero *and* its DR cut side by side, with the proof line and CTA visible.
3. **Variant math.** "1 film → 9 ads" (3 hooks × 3 lengths), because winners are 5–8 % of tests (D1).
4. **Test numbers when we have them.** Until then, use honest proxies: a $50–100 self-funded Meta test per spec (hook rate, hold, CTR), labelled "spec brand, test spend $X". Until a test runs, no invented numbers (`32` §5).
5. **AI handled responsibly.** Labelled, no fake people or fake reviews, policy-checked. This reassures buyers who fear a backlash (D33, D36).

The 6 films are in §4.

---

## 3. Top 15 rules, ranked

Ranked by (evidence strength × impact on purchases). The number in brackets is the evidence row.

1. **Frame 1 = the product, legible, filling ≥30 % of the frame.** No mood opener [D43, D9, D7].
2. **Every film carries one proof line on screen**: a number, ingredient, process or test. Beauty without proof is what fails [D9 5.3×, `23` §5].
3. **Ship a DR cut with every hero**: CTA, show the product twice, logo ≤25 % of the runtime [D10–D12].
4. **Lead the text hook with newness, offer or a price anchor when the brand has one.** Otherwise use confession or curiosity. Avoid opening with a question [D5].
5. **Hook with sound and picture together**: a diegetic transient in the first 0.5 s, plus speech or music later [D14, `38`].
6. **Never show an AI human face as a customer.** Hands, silhouettes and products only. Faces make AI look like AI, cancel the CTR gain, and bring NY/FTC disclosure duties [D31, §5].
7. **Demo and process are the default for faceless films**: pour, strike, spritz, melt, unbox [D3, D6].
8. **Make one film into a variant pack**: 3 hooks × (hero 15–20 s, 6–8 s loop, 30 s DR) × 9:16/4:5, plus 3 stills. Winners are 5–8 % of tests, and statics often match video on ROAS [D1, D23].
9. **Brand in context, not as an overlay**: pack in frame by 1 s, a sonic cue by 2 s, no floating logo bug. This counters AI's weak memory activation [D32, `23` §1.3].
10. **Have one ownable visual signature per brand** (a colour field, prop or move). Uniqueness beats brand time on screen [`23` §1.3, D34 novelty].
11. **Polish is not the enemy, but message-free polish is.** Cinematic b-roll scales at 6.85 % vs 11.6 % for text-led work. Add the text layer [D2, D3].
12. **Add a native layer to the DR cut** (iMessage, review card, cart/offer UI, "POV:" caption). It costs $0 in post [D4 letter/sign/UGC overlay].
13. **Fragrance: refresh hooks every ~4 weeks; candles: occasion hooks; beverage: pour ASMR + price per serving** [D8, D42, D3].
14. **Label AI work and keep a provenance log.** Never fake a review, testimonial, founder or real person. Platform labels may cost some credibility, but a rejection or FTC case costs more [D33–D35, §5].
15. **Keep weapons, police, crashes and fights out of the ad cut.** Keep them for the brand/portfolio film, and make a policy-safe swap for paid placement [§5].

---

## 4. Recommended portfolio: the next 6 films

Current portfolio: AURUM (drinks; incl. "Top Shelf", "From the top" and the heist one-takes), VESPER (fragrance), SOL (candles), Tabletop City (`33`). It shows **craft and entertainment**. It does **not yet show selling structure, proof lines, variants or test data**, and its action pieces carry policy risk in paid use.

Each new film ships as **hero + 6–8 s loop + DR cut × 3 hooks, 9:16 + 4:5, 3 stills**, with a label ("Spec film · invented brand · AI-made") and a one-line "why this sells" note citing the rule numbers. ZERO spend is authorised in this task; budgets follow `33` §6 when approved.

| # | Film (niche) | Format & structure | Why it sells (rules / data) | Founder it convinces |
|---|---|---|---|---|
| **F1** | **AURUM "Pour proof"** (beverage), 15 s + 6 s loop + 30 s DR | Macro pour/condensation ASMR on frame 1; text "5 g sugar. Real fruit." Can shown twice; price-per-can end card; iMessage DR variant | Demo + ASMR (D3, D4); product + USP 5.3× (D9); price anchor 10.89 % (D5). This is the **DR twin of the existing AURUM**, proving we sell, not just entertain | Beverage founders running static ads |
| **F2** | **VESPER "Named moment"** (fragrance), 12 s × 3 hooks | Bottle in hand at 0 s, spritz transient; persistent text "The night I wore VESPER"; scent notes as text; hooks = newness / confession / named moment | Fragrance life is 27 d, so a hook pack is the product (D8); Dossier pattern (`23` §3); confession 8.74 % (D5) | Fragrance founders who need volume every 4 weeks |
| **F3** | **SOL "Sunday reset"** (candle/home), 18 s | Process film: match strike → melt pool → room warms (an impossible light shift); text "50-hour burn · soy · lead-free wick"; gift/occasion DR cut | Home = demonstration and process (D6); product shot 66 vs lifestyle 30 (D7); occasion hook (D42) | Candle and home founders before Q4 |
| **F4** | **Unboxing / gift drop** (new spec, e.g. a fragrance or candle gift set), 15 s | Hands-only unbox in one continuous take, tissue sound ASMR, "New: the Winter set" text, offer-first 6 s variant | Unboxing is the #1 format at 9.83 %; newness 11.37 % and offer-first 8.68 % (D3, D5). Q4 timing | Every gifting brand (Oct–Dec) |
| **F5** | **"Founder-insert" hybrid** (any niche), 20–30 s | VXO's AI product world plus a slot for the client's **real** founder clip or VO (phone-filmed, 5–10 s) and their own words in text. Shown on a spec with an ElevenLabs VO clearly labelled as a placeholder | Founder format 8.57 % (D3); Poppi's #1 converting ad (D38). It is the honest way to sell trust: the AI does the impossible shots, a real human does the claim (D33, D37) | Founder-led brands (our exact ICP) |
| **F6** | **Policy-safe action cut** of the AURUM heist / "From the top" | Re-edit the existing one-takes (**no new generation**): remove guns, police cars and crash beats; keep the stunt rhythm, the product punchline and the comedy; add "Stunt is AI. Don't try this at home." Ship a 15 s ad-safe cut beside the brand version | Shows we know the rules (§5); keeps the fame/novelty upside (D34, D36). TikTok bans police gear and violent acts in ads | Brands wanting "viral" with legal comfort |

**Why this six** `[inf]`:
- F1–F3 turn the three existing worlds into **proof of selling**. They are cheap (existing assets and characters) and they cover the three target niches.
- F4 catches the Q4 gifting window and the highest-hit format.
- F5 answers the founder's biggest doubt ("AI can't build trust") with the format that has the best purchase anecdote.
- F6 de-risks the most eye-catching work we already have.

Deprioritise for now: jewelry and skincare macros (`32` §5.3). They are outside the three priority niches in this brief, and skincare needs efficacy proof that AI can't supply.

**Test plan to turn the specs into data** `[inf]`: once spend is approved, run $50–100 per film on Meta. Use a broad audience and a link to a landing page for the spec brand, labelled as a spec. Log hook rate, hold, CTR and CPC per hook. Publish the numbers on the work page as "spec test, $X spend, n impressions". Real numbers beat every adjective in the portfolio.

---

## 5. Policy cheat-sheet (Meta · TikTok · YouTube/Google · US law)

`P` = read on the primary page. `S` = secondary source. Rules change; re-check before each campaign.

### 5.1 Weapons and violence

| Topic | Meta | TikTok | Google/YouTube | VXO rule |
|---|---|---|---|---|
| Guns, ammo, BB/paintball guns, tasers, non-culinary blades in ads | Can't *promote sale or use*. "**Pure depictions of weapons with no discussion or advocacy**" are prohibited (P, [Meta](https://transparency.meta.com/en-gb/policies/ad-standards/restricted-goods-services/weapons-ammunitions-explosives/)) | Ads and landing pages may not "**show or promote**" dangerous weapons, ammo, explosives, batons, pepper spray, tasers (P, [TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-dangerous-products-or-services)) | Weapons are a restricted category `[unverified]`: not checked this session | **No real-looking guns in any ad cut.** |
| Weapons in fiction / film | **Allowed** in fictional contexts (films, TV, games); toy guns allowed (P) | Toys that don't look real, and "depictions of weapons in TV dramas, films, and cartoon scenes", are allowed **in some cases** (S, same page) | `[unverified]` | Brand/portfolio film: OK on Meta. TikTok: avoid. |
| Fireworks / explosions | Allowed in a celebratory, non-violent context (P) | Explosives prohibited | — | A celebration spark is OK; no blasts in TikTok cuts. |
| Violence, crime, cruelty | — | "Display of crime, excessive violence" and "dangerous, harmful, or violent acts" are prohibited (P, [TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-violence-and-dangerous-activities)) | — | Heists and chases count as "crime" on TikTok. Use the F6 cut. |
| Stunts | — | Clearly professional stunts may run; if easy to copy, restrict to 18+ and maybe add "**Do not try this at home**"; "extreme parkour" (height/risk) is prohibited (P) | — | Tower dives = extreme parkour risk. Add the warning; prefer an obviously impossible, non-imitable stunt. |
| Dangerous use of vehicles/tools | — | "Potentially inappropriate use of dangerous tools, vehicles" is prohibited (P) | — | Car chases are out of TikTok ad cuts. |
| War / soldiers | — | No glorifying war; soldiers only if respectful and memorial (P) | — | Avoid. |

### 5.2 Police imagery and impersonation

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| Police uniforms, vests, handcuffs, batons | TikTok: ads may not "**display**, promote, sell" police or military gear | P ([TikTok dangerous products](https://ads.tiktok.com/help/article/tiktok-ads-policy-dangerous-products-or-services)) | No police uniforms or cruisers in TikTok ads. |
| Police on Meta | Weapons in police contexts are allowed if non-violent and nothing is sold (P). No specific police-imagery ad rule found | `[unverified]` | OK in a brand film; a chase *with* police counts as violence/crime, so keep it out of paid. |
| Government / business impersonation | FTC Impersonation Rule (in force 1 Apr 2024): no material impersonation of government or businesses, including seals and logos. Purely artistic costume is outside the rule | [FTC via ppc.land](https://ppc.land/ftc-announces-impersonation-rule-goes-into-effect-today/) | No real agency names, badges or seals (no "NYPD", "FBI"). Fictional "City Police" only, and only in non-paid brand work. |
| Real people / celebrity likeness | TikTok ads reportedly ban synthetic media with a real person's likeness; public figures need consent | S ([NBC](https://www.nbcnews.com/tech/mrbeast-ai-tiktok-ad-deepfake-rcna118596), [cinerads](https://www.cinerads.com/blog/tiktok-ai-content-policy)) | **Never** a lookalike or soundalike of a real person, ever. |
| Real brands | Spec work for real brands is not published without permission (`32` §5) | — | Invented brands only. |

### 5.3 AI labels and disclosure

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| Meta ads | **Verified 2026-10-10 against Meta's own newsroom post (3 Feb 2025, updated 1 Jun 2026)** [c]: no significant edit and no photorealistic human → no label; significant edits with Meta's GenAI tools → "AI info" in "About this ad"; **an AI-generated photorealistic human → the label sits next to "Sponsored"**, visible in feed; third-party AI is auto-detected "through industry-standard signals" (C2PA) and labelled in "About this ad". The post does **not** say undisclosed AI is a rejection reason: that 2026 claim stays `[unverified]` (agency blogs only) | [Meta newsroom](https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/) [c]; S ([SocialMediaToday](https://www.socialmediatoday.com/news/meta-updates-ai-content-disclosure-tags/739221/), [CTC](https://commonthreadco.com/blogs/coachs-corner/meta-ai-ad-labels-mandatory-disclosure-ecommerce-2026)) | Expect a label in "About this ad". Never strip C2PA metadata. **No generated people = no visible label next to "Sponsored"**: a selling point for our hands-and-objects rule. |
| TikTok ads | AIGC label required for realistic AI; auto-applied from C2PA; reportedly mandatory for ads from 21 Jul 2026. Re-searched 2026-10-10: still secondary sources only (dates and penalties disagree), TikTok's own ad-policy page not reached `[unverified]` | S ([cinerads](https://www.cinerads.com/blog/tiktok-ai-content-policy), [novoads](https://novoads.ai/blog/tiktok-ai-ad-disclosure-rules), [Stellar Search](https://www.stellarsearch.co.uk/insight/tiktoks-ai-ad-disclosure-rules-are-live-what-brands-running-ai-creative-need-to-do-now)) | Turn the AIGC toggle on for every VXO ad. |
| Google/YouTube ads | Mandatory synthetic-content disclosure checkbox for **election** ads; inconsequential edits exempt | P ([Google](https://support.google.com/adspolicy/answer/15142358)) | Commercial ads: no mandatory checkbox found `[unverified]`. Label anyway. |
| **New York law** (GBL §396-b) | Ads must **conspicuously disclose synthetic performers** (AI humans not recognisable as a real person); in force **9 Jun 2026**; $1,000 first / $5,000 per later violation; applies to ads shown to NY audiences | [Cooley](https://www.cooley.com/news/insight/2026/2026-01-29-new-york-enacts-synthetic-performer-disclosure-law-for-advertisements-including-those-using-generative-ai), [Hunton](https://www.hunton.com/privacy-and-information-security-law/new-york-enacts-law-regulating-the-use-of-ai-generated-synthetic-performers-in-advertising) | **Any AI human in a US ad → on-screen disclosure** (e.g. "Features AI-generated people"). Hands-only shots are likely outside the rule `[inf]`. |
| EU AI Act Art. 50 | Transparency obligations from 2 Aug 2026 | `37`, `03` | Matters only if a client targets the EU. |
| FTC fake reviews rule | Bans fake testimonials, including from AI or people who don't exist; up to **$51,744 per violation**; in force 21 Oct 2024 | [Hunton](https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots), [DWT](https://dwt.com/insights/2024/08/ftc-finalizes-rule-banning-fake-consumer-reviews) | **No AI "customer" saying they love the product. No made-up review cards.** Review cards only with real, verbatim reviews the client supplies. |

### 5.4 Pre-flight checklist (paid cut)

- [ ] No real-looking firearm, blade, taser, explosion; no police uniform, cruiser or badge.
- [ ] No crime, chase, crash, fight or injury; stunts are impossible, not imitable, and carry "Don't try this at home".
- [ ] No real person, celebrity, brand or agency likeness or logo besides the client's own.
- [ ] Any AI human → on-screen disclosure (NY) + platform AI label; C2PA metadata kept.
- [ ] Every claim (sugar grams, burn hours) comes from the client in writing; reviews are real and verbatim.
- [ ] TikTok version checked against the stricter TikTok rules (§5.1–5.2).

---

## 6. What to do next to replace proxies with data

1. **Motion workspace.** Join or create one, then pull:
   - `get_inspo_creatives` for Poppi, Olipop, Liquid Death, Phlur, Snif, Dossier, Boy Smells, Otherland, Homesick (`withGlossary: true`, `LAST_90_DAYS`, ACTIVE);
   - `get_glossary_values` for the format/hook taxonomy.

   Code which formats each brand keeps running for 60+ days.
2. **Spec tests (when spend is approved):** $50–100 per film (§4).
3. **Re-check the policy pages** before the first client campaign: Meta's AI-info Help Center, the TikTok AIGC ad policy, Google's restricted weapons policy.
4. **Read the full texts** of D30, D31 and D33 before quoting them on the site.

## Sources

All URLs are inline in §1 and §5. Internal cross-references: `23` (long-runner coding, Benly, Ipsos, System1), `38` (Meta×Toluna, hook benchmarks, attention science), `32` (positioning, pricing, portfolio gaps), `33` (site, portfolio ring), `37`/`41` (action films, disclosure).
