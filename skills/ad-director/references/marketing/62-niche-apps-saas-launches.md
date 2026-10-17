# 62 — Niche deep-dive: apps, SaaS and crowdfunded-hardware launches

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent. No media is committed.

**What this adds.** Docs 47–61 cover physical DTC products sold from a Shopify store. This doc covers the founders who sell **software or a product that does not exist yet**: consumer subscription apps, prosumer and small-business SaaS, and hardware launched through Kickstarter, Indiegogo, pre-orders or an X/Product Hunt launch video. The niche has one problem no other niche has: **the thing being sold is a screen, or a prototype**, and both are exactly what AI video renders worst and what platform rules police hardest. It adds:
- **58 ads and launch videos downloaded and measured**: 40 Meta ads from Motion's public library (29 app/SaaS, 11 launch-hardware), 16 brand TikToks, 2 X launch videos; plus metadata for 315 TikTok posts from 50 handles;
- Motion library statistics for **148 brands / 2,949 live Meta ads** in this niche, split into consumer apps, SaaS/tools and launch hardware;
- the market map (app spend, subscription-app economics, SaaS spend, Kickstarter records and success rates, Product Hunt volume), 30 brands, price bands, a launch calendar and where they advertise;
- what converts here, how a crowdfunding video differs from a paid ad, and the hard numbers on paywalls, trials and reservations;
- the AI realism traps specific to UI text, phones in hands, wearables and pre-launch prototypes, with prompt fixes tied to doc 43;
- the rules that bite here: App Store 2.3.4, Meta "non-existent functionality", Kickstarter's prototype and AI-disclosure rules, FTC AI-claims enforcement, ROSCA, the Mail Order Rule;
- the buyer, re-buy triggers, a lead-scoring add-on and a sample DM;
- 10 concepts (3 marked best, 1 single best) and 10 insights.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy), 46 (sound and QC), 51 (gadgets), 60 (structure) and the LESSONS file.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg `select='gt(scene,0.3)'`, 2 fps head tiles and a 24-frame whole-film tile that I looked at, a 0.5 s RMS envelope and onset detection (librosa), integrated LUFS and sample peak (`ebur128`), and a faster-whisper transcript.
- **[c]** = the company's or creator's own claim. **[v]** = a vendor or agency figure (directional). **[inf]** = my inference. **[unverified]** = no primary evidence fetched this run.

**Method and limits.**
- **Meta.** The Meta Ad Library blocks automated fetches (as in docs 51–60). **Motion's public brand pages** (`motionapp.com/library/<slug>`) carry real ad files, active-ad counts, new creatives per week, format tags and the number of **variants** per ad. Motion says the pages were "refreshed 4 months ago", so read them as a ~June 2026 snapshot. Variants (1–8) are the best public proxy for how much a brand invested in a concept; the mean across this niche is 3.75. Motion pages do not show days active per ad.
- **TikTok.** Harvested the newest ~10–13 post IDs from public embed pages (`tiktok.com/embed/@handle`) for 95 candidate handles; 50 returned posts; metadata for 315 posts. Embed pages only show the newest posts, so all-time winners are under-sampled. As in doc 60, millions of views at <1 % likes is the paid signature; ≥3 % reads as organic.
- **X.** yt-dlp fetches public X videos with view counts. Finding the tweet IDs of famous launches was the bottleneck (search engines do not index X status IDs well), so only 2 launch videos (Pocket, Monogram) were measured; Friend, Cluely and Daylight are covered from press and metadata.
- **Kickstarter and Indiegogo pages return HTTP 403** to every automated client this run (curl, yt-dlp, WebFetch). Funding totals come from Kicktraq (fetchable), Kickstarter's own year-in-review and press. Campaign videos themselves could not be downloaded; the eufyMake E1 launch film was measured from its TikTok copy (T02).
- **YouTube** is bot-blocked from this server (HTTP 429 → "Sign in to confirm you're not a bot"), as in docs 42–60.
- **Revenue** for private companies is a company claim [c] or a third-party estimate [unverified]. Many app numbers are founder-posted run rates.
- **Two-year window.** Oct 2024 – Oct 2026. All measured files fall inside it except where marked.

---

## 0. The ten things to know before pitching an app, SaaS or crowdfunded-hardware founder

1. **This niche already buys video at volume — but it buys screen recordings.** In 2,949 live Meta ads from 148 brands, **55.5 % are video** (automotive is 25.6 %, doc 60) and **"Screen Recording" is the #1 format at 24 %** (consumer apps 27 %, SaaS 29 %); "Cinematic B-Roll" is 3.2 % [m from Motion tags]. A VXO film is not competing with statics here; it is competing with a phone screen. The gap is the **world around the screen**: the consequence of the app working, shot as a film.
2. **The winners film the consequence, not the UI.** The most-varianted non-UGC ads in the sample show zero or almost zero interface: **Brex** — one 15 s locked shot of a woman at a New York kerb, "A three-day approval for a $40 expense" (4 variants) [m M07]; **Monzo** — a wallet tumbling in a laundromat washer, "Free 24/7 customer support", 10 s, 3 shots [m M15]; **Timeleft** — a Matrix-style red pill/blue pill hook, real dinners vs "microwave pasta alone" (8 variants) [m M01]; **Nomad** — a leather case "Day 1 / Day 100", 5 s (7 variants) [m M34]. That is VXO's craft exactly.
3. **AI hook heads are already running on founder-led app ads.** Rise Science's 7-variant ad opens on an obviously AI-generated still-to-motion of a man **skydiving with a frying pan of eggs**, framed as a tweet ("Stop getting up at 5:55AM and try going to bed at 2:15AM instead"), for 6.3 s, then cuts to a real two-man skit [m M08]. Artlist's ad is AI from frame 0 (its product is an AI platform) [m M19]. The "AI hook head + real body" module from LESSONS is proven here, on the exact buyer.
4. **The proof is always real footage, and the rules say so.** Apple: app previews "may only use video screen captures of the app itself" (Guideline 2.3.4). Kickstarter: hardware creators "are required to show working prototypes… We do not allow photorealistic renderings" (Help Center, fetched). Meta bans imagery that copies play buttons, notifications or checkboxes that don't work ("non-existent functionality"). Every VXO film in this niche therefore has a **proof slot** for the client's real screen recording or prototype footage, and AI never renders a readable UI or a function the product doesn't have (§4, §5).
5. **The market is huge, crowded and top-heavy.** Consumer app spending hit **$167B in 2025 (+10.6 %)**, non-game apps passed games for the first time ($85.5B vs $81.8B), and AI apps' in-app revenue tripled to **>$5B** ([TechCrunch](https://techcrunch.com/2026/01/21/consumers-spent-more-on-mobile-apps-than-games-in-2025-driven-by-ai-app-adoption/); [PocketGamer.biz](https://www.pocketgamer.biz/global-mobile-in-app-purchase-revenue-hit-167bn-in-2025)). But new subscription apps launch at **~14,700 a month (7× since 2022)**, and only **4.6 %** reach $10K MRR within two years ([RevenueCat 2026 via ppc.land](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/)). The buyer is a founder who needs to stand out, not one who needs to be told video matters.
6. **Kickstarter tech just had its biggest year — and it is a hardware-film market.** Design & Technology had "the biggest year in the category's history" in 2025 ([Kickstarter](https://updates.kickstarter.com/a-year-in-review-2025-kickstarter-highlights/)): eufyMake E1 **$46.76M / 17,822 backers** (the largest crowdfunding campaign ever), Snapmaker U1 **~$20.2M**, Peak Design Roller Pro ~$13.4M ([All3DP](https://all3dp.com/4/why-20000-people-just-pledged-20m-for-the-snapmaker-u1-3d-printer/); [TCF](https://www.tcf.team/blog/most-funded-kickstarter) [v]). But Technology's lifetime success rate is **23.28 %** vs Design's 42.90 % ([Kickstarter stats page](https://www.kickstarter.com/help/stats), undated snapshot). Most campaigns fail; a better pre-launch film is a survival tool, not decoration.
7. **The pre-launch ad is where the money is spent, and it is a 15–30 s product film.** Crowdfunding agencies run Meta ads to a $1 reservation page *before* launch: reported **$2.34–3.40 per email lead, $17–29 per VIP reservation**, and $1 depositors are "20–30×" more likely to back ([LaunchBoom case studies](https://launchboom.com/blog/how-we-raised-589845-for-hooke-lav-case-study) [v]). Kickstarter's own outreach lead cites **31 % of pre-launch followers becoming backers and ~29 % of funding on day one** ([ComixTribe](https://comixtribe.substack.com/p/going-all-in-on-pre-launch) [c, secondhand]). The 2–4 min campaign video is the closer; the 15–30 s ad is the opener — and the opener is what VXO sells.
8. **Founder launch videos on X are now a genre, and cinema alone loses.** Pocket's 90 s launch film: **1.38M views on X** for a $129 AI note-taker that "shipped 160,000 devices" [m X01]. Monogram's 4-min seed announcement: 1.39M [m X02]. Friend's launch film reportedly cost **$250K** and drew ~21M views [c, [Digg](https://digg.com/tech/26a55vyb); [AOL](https://www.aol.com/startup-went-viral-odd-personal-225738684.html)] — and became a symbol of AI backlash. a16z speedrun quotes a founder: "No one gives a shit about a cinematic launch video" ([speedrun](https://speedrun.substack.com/p/how-to-make-a-viral-launch-video)). What travels is **a clear job-to-be-done shown in the real world, plus proof** ("160,000 devices shipped").
9. **AI is the product for many of these founders — and their audience is primed to roast AI.** 27.1 % of subscription apps are AI-powered (61.4 % of Photo & Video) [RevenueCat via ppc.land]; Duolingo's "AI-first" memo set off a mass-unfollow wave and the brand wiped its TikTok and Instagram posts for days ([Fast Company via Slashdot](https://tech.slashdot.org/story/25/05/25/0347239/); [PR Daily](https://www.prdaily.com/?p=347594)). For an AI-app founder, an AI film is on-brand; for a "digital wellbeing" or "human connection" app it can be a liability. Ask which one you're talking to before you pitch.
10. **Brand-account organic reach is close to zero for small founders; creators and paid carry it.** Cal AI's own TikTok posts get ~800–950 views while the company claims ~$30M ARR from **250 retained influencers** ([Latka](https://getlatka.com/interviews/cal-ai-zach-yadegari-2025) [c]; [Fortune](https://dc.fortune.com/2025/09/27/gen-z-founder-treats-college-like-vacation-30-million-app-by-18)) [m]. Bee's newest posts: 180–274 views; Snapmaker ~300 [m]. A VXO film here is a **paid-social asset and a creator brief**, not a brand-feed post.

---

## 1. Market map

### 1.1 Size and growth

| Segment | Number | Growth / shape | Source |
|---|---|---|---|
| Global consumer app spending (IAP + subs), 2025 | **$167B** | +10.6 % YoY; downloads +0.8 % | Sensor Tower via [PocketGamer.biz](https://www.pocketgamer.biz/global-mobile-in-app-purchase-revenue-hit-167bn-in-2025), [TechSpot](https://www.techspot.com/news/111010-global-app-spending-overtakes-mobile-games-first-time.html) |
| Non-game app spending, 2025 | **$85.5B** | +21 %; passed games ($81.8B, +1 %) worldwide for the first time | Sensor Tower via [TechCrunch](https://techcrunch.com/2026/01/21/consumers-spent-more-on-mobile-apps-than-games-in-2025-driven-by-ai-app-adoption/) |
| AI app in-app revenue, 2025 | **>$5B** | ×3 vs 2024; 3.8B AI-app downloads; 48B hours | same |
| Global app marketing spend, 2025 | **$109B** ($78B UA +13 %; $31.3B remarketing +37 %) | Non-gaming UA $53B (+18 %); **iOS UA +35 %** | AppsFlyer via [RocketShip HQ](https://www.rocketshiphq.com/appsflyer-state-of-app-marketing-2025-summary/) |
| Subscription apps (RevenueCat panel) | 115K apps, $16B revenue | Median MRR growth **5.3 %**; top 10 % **+306 %**; bottom quartile −33 % | [RevenueCat 2026 via ppc.land](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/) |
| New subscription apps per month | **~14,700** (vs ~2,000 in Jan 2022) | Apps launched 2025+ earn 3 % of revenue; pre-2020 apps 69 % | same |
| Chance a new app reaches $10K MRR in 2 years | **4.6 %** (was 5.3 %) | $1K MRR: 17 % | [ppc.land](https://ppc.land/the-app-middle-class-is-dying-and-revenuecats-data-shows-exactly-how-fast/) |
| Worldwide SaaS end-user spending, 2025 | **$299.1B** | +19.2 % | [Gartner](https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025) |
| Indie SaaS reality | 2025 cohort median MRR **$168**; 23.5 % above $1K MRR; median MoM growth 0 % | Self-selected TrustMRR sample | [BigIdeasDB](https://bigideasdb.com/state-of-indie-saas-revenue-2026) [v] |
| Kickstarter lifetime | **$8.71B** pledged, 24.1M backers, 277K funded projects (Apr 2025) | 2025 = best Design & Tech year ever | [Wikipedia](https://en.wikipedia.org/wiki/Kickstarter); [Kickstarter 2025 review](https://updates.kickstarter.com/a-year-in-review-2025-kickstarter-highlights/) |
| Kickstarter success rate | Overall 41.39 %; **Design 42.90 %; Technology 23.28 %** | Undated live snapshot | [kickstarter.com/help/stats](https://www.kickstarter.com/help/stats) [unverified date] |
| Biggest 2025 hardware campaigns | eufyMake E1 **$46.76M** (17,822 backers, goal $500K); Snapmaker U1 ~$20.2M (20,206); Peak Design Roller Pro ~$13.4M; NestWorks C500 ~$11.9M; Makera Z1 ~$11.4M | Hardware makers, mostly Shenzhen-based | [Wide Format Impressions](https://www.wideformatimpressions.com/article/eufymake-raises-47-8-million-for-3d-texture-uv-printer-kickstarter/); [All3DP](https://all3dp.com/4/why-20000-people-just-pledged-20m-for-the-snapmaker-u1-3d-printer/); [TCF](https://www.tcf.team/blog/most-funded-kickstarter) [v] |
| A typical founder-led US hardware campaign | Halliday AI glasses: **$3,304,720 / 8,020 backers, $412 average pledge**, goal $20K, 45 days (Jan 22–Mar 8 2025) | +$3.95M on Indiegogo InDemand | [Kicktraq](https://www.kicktraq.com/projects/halliday-ai-glasses/halliday-proactive-ai-glasses-with-invisible-display/) [m from page]; [Indiegogo](https://api.indiegogo.com/projects/halliday-proactive-ai-glasses-invisible-display) |
| Product Hunt | ~500K launches all-time, ~27 % featured; ~20 featured a day; Tuesday averages 30.4 launches; top 5 needs a median 205–235 points | — | [hunted.space](https://www.hunted.space/product-hunt-pulse); [Databox on PH](https://www.producthunt.com/p/databox/best-day-to-launch-on-product-hunt-here-s-what-4-962-launches-in-2026-actually-show-2) |
| Startup launch videos (250 coded) | **64 % live action**, 36 % animation; most run just over 60 s; 60 % have only a passive CTA | Product launches best at 30–60 s; funding announcements >90 s | [Awesomic report](https://www.awesomic.com/launch-video-report) [v] |

**What it means [inf]:** the money is growing (AI apps, iOS UA, hardware crowdfunding) while the number of competitors explodes. Founders in the $1–20M band are the top decile of a brutal distribution — they have revenue, a paid-acquisition habit and a creative-volume problem.

### 1.2 Creative benchmarks for this niche (Meta, Motion public library) [m from Motion tags]

148 brand pages, the 20 newest ads each (2,949 ads). "Variants" = how many versions Motion groups under one concept.

| Group | Brands / ads | Video share | Mean variants | Top format tags |
|---|---|---|---|---|
| Consumer apps | 84 / 1,673 | **63 %** | 3.85 | Screen Recording 27 %, Demo 11 %, Headline 10 %, Yapper 10 %, Infographic 6 %, Split Screen 6 %, Listicle 6 %, **Skit 5 %**, Expert Explainer 5 % |
| SaaS / tools | 36 / 716 | 46 % | 3.80 | Screen Recording 29 %, Headline 16 %, Split Screen 10 %, Yapper 10 %, Offer-First 8 %, Greenscreen 5 % |
| Launch hardware | 28 / 560 | 47 % | 3.41 | **Demo 24 %**, Headline 14 %, Offer-First 14 %, Screen Recording 7 %, **Cinematic B-Roll 7 %**, Feature Pointout 7 % |

Variant intensity by format across all 2,949 ads (higher = brands invest more per concept): UI Mockup 4.83, UGC Overlay 4.75, Quiz 4.59, Transformation 4.54, Expert Explainer 4.39, Review 4.31, Listicle 4.26, **Skit 4.01**, Split Screen 4.00, Screen Recording 3.95, **Cinematic B-Roll 3.86**, Montage 3.71, Demo 3.65, Offer-First 3.35, Us-vs-Them 3.17 [m].

Volume (active ads / new creatives per week, Motion): the app factories ship at industrial scale — **WalkFit 426 / 192, Yoga-Go 666 / 149, Ladder 389 / 117, The Coach 273 / 110, Skylight 305 / 109, Remini 728 / 104, Hearty 222 / 84, Sintra AI 252 / 76, Finch 279 / 70, Kalshi 239 / 68**. Founder-led SaaS and hardware ship far less: **Sunsama 14 / 3, Superhuman 16 / 7, Lovable 54 / 7, Peak Design 36 / 9, PolarPro 79 / 10, Nomad 151 / 12, Opal 79 / 28, Fyxer 131 / 41** [v].

### 1.3 The 30 brands (founder-led and $1–20M marked)

"$1–20M" = the founder-led band VXO targets (✓ = evidence it is in band; ↑ = above band, kept as a reference for what the category buys). Revenue figures are company claims or estimates unless linked to a filing.

| # | Brand | What | Founder-led | Size signal | Price | Meta (active / new per wk) [v] | How they launch / advertise | Band |
|---|---|---|---|---|---|---|---|---|
| 1 | **Opal** | Screen-time blocker (iOS) | Kenneth Schlenker | **$10M ARR with 11 people** ([Speedinvest](https://speedinvest.com/blog/scaling-smart-how-opal-built-a-10m-arr-business-in-just-2-years)) [c] | subscription | 79 / 28; video 15/20; Screen Recording 38 % | Meta, creators (T08), celebrity sightings | ✓ |
| 2 | **Rise Science** | Sleep / energy app | Jeff Kahn [unverified] | n/a | subscription | video 20/20; Skit 21 %, Street Interview 9 % | Meta skits with an AI hook head (M08) | ✓ [unverified] |
| 3 | **Timeleft** | Dinners with strangers | Maxime Barbier | ~€10M ARR founder post [unverified] | ~$20/mo [unverified] | 499 / 8; 8-variant pill ad | Meta, PR, city launches | ✓ [unverified] |
| 4 | **Finch** | Self-care pet app | Nino Tsikovani, Stephanie Yuan | n/a | subscription | 279 / 70 | Meta, organic TikTok (9–13K views) | ↑ [unverified] |
| 5 | **Cal AI** | Photo calorie counter | Zach Yadegari et al. | ~$30–35M ARR claim ([Fortune](https://dc.fortune.com/2025/09/27/gen-z-founder-treats-college-like-vacation-30-million-app-by-18); [Latka](https://getlatka.com/interviews/cal-ai-zach-yadegari-2025)) [c] | $2.49/mo, $29.99/yr | — | **250 influencers on retainer**; brand TikTok ~900 views | ↑ |
| 6 | **Ladder** | Strength-training app | n/a | n/a | subscription | **389 / 117**; Demo 22 %, Yapper 19 % | Meta at volume | ✓ [unverified] |
| 7 | **Speechify** | Text-to-speech | Cliff Weitzman (in the ads) | n/a | subscription | Founder ad, 7 variants (M18) | Founder-on-camera Meta | ↑ [unverified] |
| 8 | **Hearty** | Parenting app | n/a | n/a | subscription | 222 / 84 | Meta: Screen Recording 27 %, Demo 25 % | ✓ [unverified] |
| 9 | **Endel** | Soundscapes | Oleg Stavitsky | n/a | subscription | 38 / 12; Yapper 51 % | Meta | ✓ [unverified] |
| 10 | **Umax** | Looks-rating app | teen founders (Cal AI team) [unverified] | n/a | subscription | — | Creator/meme accounts | ✓ [unverified] |
| 11 | **Fyxer** | AI email assistant | Richard & Archie Hollingsworth | **$1M → $30M ARR in 2025** ([Fyxer press](https://www.fyxer.com/press)) [c] | subscription | 131 / 41; Skit 11 % | Meta skits (finger puppets, Alexa), search | ↑ (was ✓ in early 2025) |
| 12 | **Sunsama** | Daily planner (SaaS) | Ashutosh Priyadarshy | >10K paying users [unverified] | ~$20/mo [unverified] | 14 / 3; **0 videos of 16** | Statics ("Before and After" 35 %), press | ✓ |
| 13 | **Stan** | Creator storefront | John Hu [unverified] | n/a | subscription | 29 / 14; Spokesperson 16 % | Creator spokespeople | ✓ [unverified] |
| 14 | **Sintra AI** | AI "employees" for SMBs | (Lithuania) | n/a | subscription | **252 / 76** | Meta at volume, screen recordings | ✓ [unverified] |
| 15 | **Monogram** | Visual-interface AI app | Eren Bali | **$40M seed** (DST, Lux) [c, X02] | — | — | **4-min X launch film, 1.39M views** [m] | pre-revenue |
| 16 | **Superhuman** | Email client | Rahul Vohra | acquired 2025 [unverified] | $30/mo | 16 / 7 | Waitlist mystique, statics | ↑ (reference) |
| 17 | **Lovable** | AI app builder | Anton Osika | far above band | subscription | 54 / 7; Greenscreen, street interview (M04, M05) | Meta explainers, X | ↑ (reference) |
| 18 | **Pocket** | $129 AI note-taking puck | Akshay Narisetti, Gabriel Dymowski | **$27M run-rate claim, 160,000 devices**, $11M raised (Accel, YC W26) ([TechCrunch](https://techcrunch.com/?p=3136998); [xyz.pl](https://xyz.pl/poland-unpacked/polish-founded-ai-device-pocket-raises-usd-11m-as-it-scales-in-the-us-1892/)) [c] | $129 + $200/yr optional | — | **90 s X launch film, 1.38M views** [m X01] | ✓→↑ |
| 19 | **Daylight Computer** | $729 "LivePaper" tablet | Anjan Katta | ~$15M raised ([Caplight](https://www.caplight.com/company/daylightcomputer)); first 5,000 units sold out ([Wikipedia](https://en.wikipedia.org/wiki/Daylight_Computer_Co.)) | $729 | — | Pre-order deposit page, X launch film | ✓ |
| 20 | **Halliday** | AI glasses | Gyges Labs (SF) | **$3.30M Kickstarter + $3.95M Indiegogo** [m Kicktraq] | $369–399 early, $489 MSRP | — | CES → Kickstarter → InDemand | ✓ |
| 21 | **Light Phone** | Minimalist phone | Kaiwei Tang, Joe Hollier | LP1 15K units, LP2 ~10K pre-orders (2019) ([TechCrunch](https://techcrunch.com/2019/09/04/light-phones-founders-discuss-life-beyond-the-smartphone)) | $699 (LP III) [unverified] | — | Kickstarter/Indiegogo history; organic TikTok 5–6K | ✓ |
| 22 | **Flipper Zero** | Hacker multitool | Pavel Zhovner | $4.88M Kickstarter (2020); $25M sales 2022 [c]; ~1M units [c] | ~$169 [unverified] | — | **Explainer TikToks: 2.2M at 9.4 % likes** [m T04] | ↑ |
| 23 | **Elevation Lab** | AirTag / Apple accessories | Casey Hopkins [unverified] | n/a | $15–40 | — | Kickstarter roots [unverified]; TikTok 27–45K | ✓ [unverified] |
| 24 | **Orbitkey** | Key organisers, desk mats | Rob Chen, Chris Hung [unverified] | n/a | $30–80 | — | Kickstarter-born [unverified]; TikTok skit 107K (paid) | ✓ [unverified] |
| 25 | **PolarPro** | Camera filters | Jeff Overall [unverified] | n/a | $50–400 | 79 / 10; 7-variant creator demo (M36) | Creator demos, nostalgia montage | ✓ [unverified] |
| 26 | **Peak Design** | Bags, travel, mounts | Peter Dering | **Kickstarter-native**; Roller Pro ~$13.4M (2025) | $50–700 | 36 / 9 | Kickstarter → DTC; colourway launch films (M40) | ↑ (reference) |
| 27 | **Nomad** | Leather/tech accessories | Noah Dentzel [unverified] | n/a | $30–150 | 151 / 12 | "Day 1 / Day 100" loops (M34, 7 variants) | ↑ [unverified] |
| 28 | **Friend** | AI companion pendant | Avi Schiffmann | Launch film **$250K incl. $50K equity** [c]; $1.8M domain; $1M NYC subway ads ([CNN via KVIA](https://kvia.com/news/business-technology/cnn-business-consumer/2025/11/16/how-this-tiny-device-became-a-symbol-for-the-backlash-against-ai/)) | $99–129 | — | Viral X film, provocation | ✓ (cautionary) |
| 29 | **Skylight** | Family calendar display | Founder-led [unverified] | n/a | $160–600 [unverified] | **305 / 109**; Demo, Unboxing, Skit | Meta creator challenges (M30–M33) | ↑ [unverified] |
| 30 | **Plaud** | AI voice recorders | Nathan Xu [unverified] | Started with a **$1.1M Kickstarter (2023)**; now ~$250M annualised estimate ([Sacra](https://sacra.com/research/250m-year-granola-for-plumbers)) [v] | $159–169 | — | Kickstarter → Amazon/retail | ↑ (what "winning" looks like) |

Category leaders kept for calibration (not targets): Duolingo, Notion, Perplexity, Nothing, Anker/eufyMake, Snapmaker, Even Realities, Brex, Monzo, Slack.

**Pattern [inf]:** the best VXO targets are rows 1–3, 6, 8–9, 12–14, 18–25 — founders with revenue or a funded launch, a visible product truth that can be shot in the real world, and a thin film library (Sunsama: 0 video; Peak Design 9 new per week; PolarPro 10).

### 1.4 Price bands (what the buyer sells)

| Product | Typical price | Evidence |
|---|---|---|
| Subscription app | **$5.99/week, $10/month, $34.80/year** (medians); 90th-percentile yearly $90; Education $44.99/yr | RevenueCat 2026 via [ppc.land](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/) |
| Year-1 realised LTV per payer | Global $23, **North America $32**; AI apps $30.16 vs $21.37 non-AI | same |
| Prosumer SaaS | $10–30 per seat per month [inf] | Sunsama, Superhuman, Fyxer list prices [unverified] |
| AI wearables / note-takers | $99–169 device + optional $100–200/yr | Pocket $129 + $200/yr; Plaud NotePin $169; Friend $99–129 |
| Smart glasses | $299–599 | Brilliant Labs Halo $299; Halliday $399–489; Even G2 $599 ([TechCrunch](https://techcrunch.com/?p=3140951)) |
| E-paper / minimalist devices | $699–729 | Daylight DC-1 $729; Light Phone III $699 [unverified] |
| Maker machines (UV/3D printers, CNC) | $500–3,000+ | Kickstarter top campaigns (average pledge $412 on Halliday; E1 ≈ $2,624 per backer from $46.76M / 17,822 [inf]) |
| Accessories | $15–150 | Elevation Lab, Orbitkey, Nomad, PolarPro [unverified] |

**What it means [inf]:** an app's first-year revenue per payer is ~$23–32, so a $2,500 film must lift paid conversions by ~80–110 payers to pay back — very achievable for a $1M+ ARR app, impossible for a $168-MRR hobby app. Filter leads on revenue, not on "launched an app".

### 1.5 Launch and seasonality calendar (US)

| When | What happens | Who buys a film | Evidence |
|---|---|---|---|
| **Jan 1–10** | Trial starts spike on New Year's Day; first payments ~Jan 10; install-to-paid **39.4 % mid-January vs 30.5 % in October**; Health & Fitness and Education bottom at Christmas and peak early January | Health, fitness, sleep, focus, language, finance apps — **brief them in early December** | [Adapty 2026 holiday report](https://adapty.io/blog/state-of-holidays-for-subscription-apps/) [v] |
| **Early Jan (CES)** | Hardware press moment; Halliday debuted at CES 2025 then launched on Kickstarter Jan 22 | Wearables, smart home, AI devices | [ChannelNews](https://www.channelnews.com.au/ces-2025-crowdfunded-ai-glasses-wont-make-you-look-like-a-weirdo/) |
| **Feb–May** | Main Kickstarter tech window (post-CES); E1 launched Apr 29 2025 | Crowdfunded hardware: pre-launch ads start **6–10 weeks** before | [TCF](https://www.tcf.team/blog/best-time-to-launch-a-kickstarter) [v]; [BackerKit](https://www.backerkit.com/blog/best-time-to-launch-a-kickstarter) [v] |
| Any Tue–Thu | Product Hunt launches; X launch films; funding announcements (Monogram $40M, Pocket) | SaaS, AI tools | hunted.space; X01, X02 [m] |
| **Jun (WWDC)** / **Sep (iPhone)** | New iOS features; new iPhone = new case/mount/MagSafe SKUs | iOS-first apps; Apple-accessory brands (Nomad, Elevation Lab) | [inf] |
| **Aug–Sep** | Back to school | Note-takers, study, language, productivity apps | [inf] |
| **Sep–Nov** | Second crowdfunding window; BFCM **annual-plan discounts** for apps; gifting for hardware | All | [TCF](https://www.tcf.team/blog/best-time-to-launch-a-kickstarter) [v] |
| **December** | Worst month to launch a Kickstarter (attention and CPMs); Christmas-morning installs on new phones | Apps only (gift cards, new phones) | [LaunchBoom](https://www.launchboom.com/blog/resources/what-is-the-worst-month-to-launch-kickstarter/) [v] |
| **Post-campaign** | Late pledges add "10–20 %" (vendor claim); Indiegogo InDemand; then Shopify pre-orders, Amazon | Hardware: a *second* film for the store and retail | [PledgeBox](https://www.pledgebox.com/post/kickstarter-late-pledge) [v] |

### 1.6 Where they advertise

- **Meta** is the backbone for consumer apps (Motion: 63 % of their ads are video) and for **crowdfunding pre-launch reservation ads** (the LaunchBoom model). Meta reported **+29 % ROAS for app advertisers using value optimisation** (Nov 2025, via RevenueCat/ppc.land).
- **TikTok**: creator-driven (Cal AI's 250 influencers), organic skits (Cluely's office series 150K–825K views, 9–11 % likes [m]), Spark Ads.
- **Apple Search Ads and Google App Campaigns** remain the top install sources (AppsFlyer Performance Index 2025: Google and Apple on top, Meta/TikTok/AppLovin closing in) ([AppsFlyer](https://www.appsflyer.com/resources/performance-index/)). Google App Campaigns assemble ads from uploaded videos automatically — every VXO delivery should include clean 16:9, 1:1 and 9:16 masters.
- **X** for launch films and funding news (Pocket, Monogram, Friend, Cluely); **Product Hunt** for SaaS; **LinkedIn** for B2B SaaS founders; **Kickstarter/Indiegogo** pages themselves (the 2–4 min campaign video).
- **Out-of-home as content**: Friend's $1M subway takeover was planned as a photo op ("the picture of the billboard is the billboard") [c].

---

## 2. Teardowns: 58 measured ads and launch videos (40 Meta, 16 TikTok, 2 X)

Cut rate = shots ÷ duration (detected cuts + 1). Hook = what is on screen and in the audio in second 1. LUFS / peak are as published (platform re-encode). M = Meta via Motion (signal = variants), T = TikTok (views · like rate · shares), X = X/Twitter (views · likes · reposts).

### 2.1 Full teardowns: the 20 that matter [m]

| # | Ad | Signal | Length · shots · cut rate · LUFS / peak | Shot list (timecodes) | Second 1 (hook) | Turn / punchline | Product interaction | Sound | Text / CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | **Pocket "Introducing Pocket. Officially."** (X01, [X](https://x.com/AkshayNarisetti/status/2077439335130124544)) — $129 AI note-taker | 2026-07-15 · **1.38M views · 4,039 likes · 223 reposts** | 90.1 s · 10 · 0.11/s · −21.6 / −3.3 | 0–32.2 **one locked-off wide**: a hairy, cocky lawyer in a spa bath on speakerphone, assistant "Josh" kneeling with a towel; floating translucent UI cards (transcript, summary) composited beside him · 32–36 CU of Josh · 36–43 the lawyer face-down in a massage table, face through the head hole · 43–51 the puck on a blue felt pad, two UI cards pop · 51–69 lawyer in a robe dictating into Pocket held to his mouth, UI cards stack · 69–90 courtroom: suit, "Judgment is entered for the plaintiff… $5 million in damages", end card "heypocket.com" | Already mid-call, already absurd: a man in a bath saying "4.2 is the last number" | "Pocket got me every word. You got me this skim milk." → $5M verdict | The device is held, worn, set down; **all UI is post-produced floating cards, never a phone screen** | Dialogue-led, room tone, light score | "160,000 devices shipped later" in the post copy; URL end card | **A comedy short with a job-to-be-done (note-taking for people who talk for a living) and social proof in the caption.** The UI-as-overlay trick is the solution to §4's biggest AI trap |
| A02 | **eufyMake E1 UV printer launch film** (T02, [TikTok](https://www.tiktok.com/@eufymake/video/7626544804754754829)) — the $46.76M Kickstarter | 2026-04-09 · 1.9M · 0.51 % (paid) · 2,556 | 48.3 s · 42 · 0.87/s · −19.8 / −3.5 | Machine + inks laid out (0–1.6) · machine wide, lid (1.6–4) · **a hand strokes a raised-texture dinosaur fossil print on slate** (4–6) · fingers trace a blue folk-art dachshund on a wood round (6–8) · macro: textured lizard scales (8–12) · thumbnail "built up to 5 mm" (12–14) · coasters, parrot, snake on a wallet, glass tumbler, lit acrylic, dragon earring (14–30) · rotary, laminator, roll-to-film attachments (30–40) · skateboard 10 m roll (40–44) · "Print Vivid. Feel the Texture." | VO: "What if your prints could be **felt**, not just seen?" over a flat-lay | The fingertip on the 5 mm relief | Every shot is an **output being touched**, not the machine | Female VO, light bed | Yellow karaoke captions; claims (5 mm, 10 m) | **Sell the output, prove it with touch.** The machine is on screen for <15 % of the runtime [inf from tile] |
| A03 | **Nothing Phone (3) "USB durability test"** (T01, [TikTok](https://www.tiktok.com/@nothing/video/7546600788949404951)) | 2025-09-05 · **9.1M · 5.44 % · 149,100 shares** | 30.5 s · 4 · 0.13/s · −20.3 / −6.3 | Locked macro of a white lab rig gripping the phone and cycling a USB-C plug in and out (0–4.8) · rack-focus detail (4.8–10.4) · wider rig (10.4–17.2) · full rig in profile, the arm cycling on and on (17.2–30.5) | Already moving: the machine arm mid-stroke, mechanical clack | None — the loop is the point | The product is the *victim* of a machine | Rig clacks and a minimal bed; **no words** | Caption only | **The test rig as hero.** 149K shares for 30 s of a machine doing one thing — the purest proof format in the niche, and AI-safe (machines, no faces) |
| A04 | **Brex "Time to get Brex AF"** (M07) — corporate card / spend SaaS | 4 variants | 15.0 s · **1** · 0.07/s · −13.7 / +0.4 | One locked long-lens shot on a Manhattan avenue: a woman with a carry-on tries to hail a cab, reads her phone, sighs, walks toward camera past the lens | Street noise; super "A three-day approval for a $40 expense." | Red type "TIME TO GET BREX AF*" → "*AGENTIC FINANCE" | The phone is a prop; **no UI at all** | VO + city ambience | Type over picture; brex.com/af | **A B2B SaaS sold with one cinematic frame of the pain.** The joke is the asterisk; the picture is a mood a crew could shoot in an hour — or AI could, from a real plate |
| A05 | **Monzo "Free 24/7 customer support"** (M15) — banking app | 4 variants | 10.0 s · 3 · 0.30/s · −15.0 / −1.5 | Laundromat wide, two strangers waiting (0–2.4) · CU, a man staring into the drum (2.4–4.2) · **a wallet/card tumbling in the wash, then the support chat bubble floats over the drum** (4.2–8) · red logo card, app badges (8–10) | Static wide with a held breath | The thing you lost is in the machine — and support is there at 3 a.m. | UI appears only as a single floating notification bubble | Washer rumble, short VO | "We've waited long enough." / logo + store badges | **Problem shown as an object in peril.** A wallet in a washer = "you need help now". 10 s, 3 shots, zero screen recording |
| A06 | **Timeleft "Red pill or blue pill"** (M01) — dinner-with-strangers app | **8 variants** | 20.2 s · 8 · 0.40/s · −16.8 / −0.1 | CG blue hands offering red/blue pills, "Choose fast" (0–5.2) · 3-2-1 countdown · **red pill: real phone footage of five strangers laughing, toasting, sharing a pineapple bowl** (5.2–10) · **blue pill: a man alone at night, microwave pasta** (10–18) · back to the pills "so which one did you pick?" · orange logo card | VO "Choose fast, blue pill or red pill" + countdown | "…enjoy eating your microwave pasta alone" | App never shown | VO + synth bed | Burned captions; "Book your dinner" | **A metaphor head (CG) + real proof body (UGC dinners) + a deadpan contrast.** Exactly VXO's module: AI does the metaphor, the client's real footage does the proof |
| A07 | **Rise Science "2:15 AM"** (M08) — sleep app | 7 variants | 58.9 s · 13 · 0.22/s · −23.1 / −5.4 | **AI-generated still-to-motion inside a fake tweet card: a man skydiving, screaming, holding a frying pan with two fried eggs** (0–6.3) · real skit: roommate in a blanket "Dude, why are you awake? It's 1:22 in the morning" (6.3–8.7) · desk guy: "it told me my ideal bedtime is 2:15 AM" … 12 cuts of two-shot banter … end card "Editor's Choice · Best Apps of 2024 · Take the 1-minute sleep quiz" | Absurd AI image + VO "Stop getting up at 5:55 AM…" | The night owl is *right* — the quiz says so | App shown only on the end card | Dialogue, room tone | Tweet-card hook; quiz CTA | **The AI hook head on a real UGC body is already a 7-variant winner on a founder-led app.** The AI image is deliberately absurd, so nobody mistakes it for proof |
| A08 | **Opal "the most potent drug"** (M14) — screen-time app | 7 variants | 14.9 s · 3 · 0.20/s · −21.9 / −6.7 | A man in a snowy forest points at the lens: "You are high on the most potent drug known to man… your phone" (0–2.2) · CU, "look in the mirror, you're f***ing hooked" · iPhone screen recording, blocked apps (2.2–14) | Pointing finger + confrontation | — (a confession, not a joke) | Real screen recording | Single voice, no music | Captions | **A provocation + a real UI demo.** 15 s; the hook is a sentence, the proof is the screen |
| A09 | **Speechify "Hi, I'm Cliff"** (M18) — founder ad | 7 variants | 44.2 s · 8 · 0.18/s · −19.5 / +0.6 | Founder standing waist-deep in a pool talking to camera (0–6) · "Are the voices any good? No, our voices are f***ing great" · demo cuts: photo of a book, PDF, website, each read aloud (11–22) · stats ("double your attention…") · end card | Founder in a pool, mid-sentence | The profanity beat | Real phone demos | Founder VO, no bed | Captions; "Studies show…" claims | **Founder + absurd location + real demo.** The pool is the only "production value"; founder ads score 8.57 % hit rate (doc 45 D3) |
| A10 | **Fyxer "Hey Alexa"** (M29) — AI email assistant | 6 variants (sister ad M27, finger puppets, 5 variants) | 26.9 s · 6 · 0.22/s · −21.1 / −5.9 | A man in a kitchen asks a smart speaker "how do I clear 132 emails before 9am?" (0–4.5) · the speaker "answers" with Fyxer's pitch (4.5–14) · "Wait, it writes my emails too?" · screen-recording inbox (14–27) | A question to a device | The device sells the competitor-free answer | Inbox screen recording | Two voices | "132 emails before 9am" | **A household object becomes the salesperson** — cheap, repeatable skit. Fyxer grew $1M → $30M ARR in 2025 [c] on skits like this |
| A11 | **Skylight "Silent Sync Challenge"** (M32) — family calendar device | 5 variants | 48.9 s · 46 · 0.94/s · −13.6 / +0.5 | Mom shushes six kids at the door, "Today we attempted to pull off the impossible: a silent morning routine" (0–2) · kids touch the wall display, stairs, beds, breakfast, hair, chores, all in silence, 1 cut/s (2–40) · "we technically failed at the silence piece" · kids high-five the display | A shushing finger + "the impossible" | They fail the silence but nail the morning | Kids tap the real device repeatedly | VO over silence-plus-giggles | Captions | **A challenge format with a built-in failure.** The device is touched in ~25 of 46 shots [inf from tile] |
| A12 | **Nomad "Day 1 / Day 100"** (M34) — leather case | **7 variants** | 5.4 s · 1 · silent | Two identical product photos on white: "Day 1" brown leather vs "Day 100" darker patina; "Better Every Year · Made with Horween Leather" | The comparison itself | Patina = better | Product only | **No audio track** | Two labels | **A static-to-video loop with one change.** 7 variants of a 5 s loop = a cheap, long-running format VXO can make cinematic (§8 C7) |
| A13 | **Anker "Power needs a brain"** (M39) — 160 W charger | 5 variants | 24.7 s · 7 · 0.28/s · −12.0 / +1.2 | Black title (0–2) · CG galaxy · engineer at monitors · **CG chip city: glowing PowerIQ 5.0 die, light flowing through pipelines** (6–14) · charger on a plinth, "160W = 210W" (14–20) · laptop + phones charging · night landscape | "Power needs a brain." | The math pun 160 = 210 | CG mechanism, then the real product | VO + score | Spec supers | **The "inside the machine" mechanism insert** (LESSONS) used by the category's biggest brand — the AI-safe asset with no realism expectation |
| A14 | **Flipper Zero "GPIO in under 90 seconds"** (T04, [TikTok](https://www.tiktok.com/@flipperzero/video/7639442311914540309)) | 2026-05-13 · **2.2M · 9.39 %** · 6,196 | 95.1 s · 23 · 0.24/s · −13.0 / +0.8 | Presenter at a desk: "I'm going to explain exactly what it does, pin by pin, in under 90 seconds. Start the timer." · macro inserts of each pin while he explains | A promise + a timer | Beats the clock | The device in hand, pins in macro | Fast VO | Captions, timer | **A clock as the story engine** (doc 60 insight 8) **and a fan-base that wants depth.** Organic: 9.4 % likes at 2.2M |
| A15 | **Cluely "POV: trying to socialize with Ling Long"** (T05, [TikTok](https://www.tiktok.com/@cluely/video/7691753289259437325)) | 2026-10-01 · 825K · **11.25 %** · 8,073 | 62.1 s · 15 · 0.24/s · **−7.7 / +2.1** (very hot) | Elevator two-hander, phone handheld (0–24) · office kitchen: the coworker eats "sweet and sour rabbit" (24–46) · "Where did you go to school?" "Tsinghua… the MIT of China" (46–62) | "Can you hold it?" — the elevator door | Status reversal on the school | **None.** Product never appears | Dialogue, no music | Burned captions only | **Cluely's account is a sitcom, not an ad** (episodes 30–35, 90K–644K views each). It buys attention for a company name, then converts elsewhere — the "content company" model |
| A16 | **Nothing "But will it fold?"** (T07, [TikTok](https://www.tiktok.com/@nothing/video/7686380217882955041)) — CG teaser | 2026-09-17 · 324.6K · **9.98 %** · 5,044 | 12.0 s · 1 · 0.08/s · −25.7 / −3.6 | One continuous CG pull-back from an extreme macro of a ridged black disc and a red block to reveal a slim black-and-red product on black | A red block filling the frame | The reveal of *what* it is (a mystery product) | None (CG only) | Low hum, sound design | Caption "But will it fold?" (series: "…bark?", "…cook?") | **The teaser as a question.** A 12 s CG macro reveal + a running gag caption drives 10 % likes — a pre-launch film format that needs no working prototype on camera |
| A17 | **Orbitkey "When the new girl hasn't got a key organiser yet"** (T13) | 2026-03-05 · 107K · 0.77 % · 4 | 8.3 s · 3 · 0.36/s · **−37.0 / −18.8** (near-silent export) | High angle down office stairs: she walks down, keys jangling at her hip (0–2.6) · she stops at the bottom, keys still jangling (2.6–6.3) · reverse: the whole office turns, a man on the phone glares (6.3–8.3) | The jangle | Everyone stares | Product absent — it is the *missing* product | The jangle should be the hook; it is mixed far too quietly | One-line caption | **A sound-first gag about the problem.** It works on the caption alone; with a proper mix it would work in the first second (doc 46) |
| A18 | **Even Realities "EXPOSED: Episode 1"** (T09) — smart glasses | 2026-10-08 · 334K · 0.03 % (paid) | 58.3 s · 6 · 0.10/s · −16.0 / −1.5 | Night car on a forest road · family arriving at a gothic hotel · "Even Realities presents EXPOSED" title · empty reception, a contract on the desk "privacy clause" · "Family holiday starts now" (10-episode series) | Headlights in a dark forest | A cliffhanger, no product yet | None in episode 1 | Score, dialogue | Series title card | **A paid micro-drama series** (10 × ~1 min) — Netflix grammar for a privacy-first product. Shows the money hardware brands now spend on story; the like rate shows paid reach without love |
| A19 | **Artlist "the first true AI production platform"** (M19) | 7 variants | 38.9 s · 18 · 0.46/s · −16.3 / −0.2 | AI-generated: a red-haired director on a rooftop screams "Cut!" in front of a nuclear explosion · the same face in a basketball jersey, a snowstorm, a candlelit dinner as the VO lists features ("cast your character exactly as it exists in your head… choose your angle, your lens") | A screaming close-up + "For f***'s sake, CUT!" | The same actress survives every genre switch | The output *is* the product | VO + SFX | Feature supers; logo | **All-AI ads are fine when AI is the product.** Identity held across 6 worlds is the proof |
| A20 | **Monogram launch + $40M seed** (X02, [X](https://x.com/erenbali/status/2074502671600672930)) — visual-interface AI app | 2026-07-07 · **1.39M views · 2,764 likes · 166 reposts** | 248.7 s · 21 · 0.08/s · −16.9 / +0.2 | Founder (ex-Airbnb) on a purple seamless: "When I tried ChatGPT for the first time… the user interface felt like we had gone back to the command line" (0–20) · co-founder interview, office (20–50) · "Let me show you Monogram" → **split frame: founder left, a floating phone with the real UI right**, alternating with hand-held phone inserts (55–225) · end card monogram.ai (239–249) | Founder already talking, centred | "What if AI could generate the entire user interface?" — then the demo answers it | Real UI in a clean floating phone frame on a coloured seamless | Founder VO, soft bed | Funding and thesis in the post copy | **The funding-announcement format: >90 s, founder-led, demo-heavy** (Awesomic: 75 % of investment announcements run past 90 s). The floating-phone-on-seamless frame is the clean, honest way to show UI in a film |

### 2.2 The other measured ads (one line each) [m]

| # | Ad | Signal | Length · shots · LUFS | What it is | Lesson |
|---|---|---|---|---|---|
| M02 | Timeleft "Do not watch this ad unless…" | 8 var | 16.1 s · 17 · −23.2 | Reverse-psychology warning card → 1 cut/s dinner UGC | A warning hook + real footage; too quiet (−23 LUFS) |
| M03 | Slack × MrBeast studio | 8 var | 31.0 s · 26 · −21.3 | MrBeast's creative supervisor on why Slackbot is secure; studio b-roll | B2B borrows a famous customer's world |
| M04 | Lovable "Henry Ford" | 8 var | 74.0 s · 26 · −14.2 | Greenscreen explainer: assembly line → app building ($4,700 car → $260) | A history metaphor sells "AI makes software cheap" |
| M05 | Lovable street interviews | 8 var | 62.4 s · 44 · −14.2 | Creator asks strangers for app ideas, builds them live | Live proof of speed, 0.7 cuts/s |
| M06 | Headway "14-day plan" | 8 var | 15.0 s · 1 · −21.4 | Man walking in snow + a list overlay | Static-to-video hybrid |
| M09 | Rise "Early bird vs night owl" | 7 var | 10.0 s · 1 · −19.6 | Cartoon aliens, us-vs-them stats | Cheap animation variant of A07 |
| M10 | Liven "nice guys" | 5 var | 157.7 s · 22 · −13.1 | 3D-animated motivational song | Long-form animation can run in wellness |
| M11 | Character.AI | 5 var | 25.4 s · 6 · −14.7 | Animated characters (a pug with antennae, a vending machine) | Characters as the product |
| M12 | AI Cleaner (Spanish) | 4 var | 26.3 s · 15 · −18.9 | Man buried in paper "emails", phone demo | Literalised metaphor (paper = email) |
| M13 | AI Cleaner "Hey, it's your phone" | 4 var | 24.4 s · 2 · −19.5 | A talking animated phone complains it is full | The device as a character |
| M16 | Noom "Can I (52)…" | 2 var | 10.0 s · 1 · −20.1 | Ice-skater + question card + results disclaimer | **The disclaimer is on screen** ("Individual results may vary") |
| M17 | Impulse IQ puzzle | 8 var | 25.9 s · 3 · −16.9 | "Only people with an IQ over 130 can solve it" | Challenge hook |
| M20 | Wealthsimple Visa | 7 var | 15.9 s · 8 · −16.1 | A metal card pressed into snow; ASMR | Product-as-object macro for a fintech |
| M21 | Duolingo "where are you?" | 4 var | 6.0 s · 1 · −15.1 | Duo's face cycles moods over a travel photo | Mascot guilt loop, 6 s |
| M22 | Finch chores | 5 var | 9.1 s · 6 · −22.2 | Chores tagged as in-app tasks | Life footage with UI labels |
| M23 | Fyxer yapper | 6 var | 24.6 s · 9 · **−10.8 / +0.9** | "I love this tool" + Google search → site → inbox | Native search-bar device; mix clips |
| M24 | Kalshi creator | 4 var | 18.6 s · 8 · −12.8 / +1.7 | Creator on a couch + app UI | Creator + UI split |
| M25 | Headway dinosaur | 7 var | 15.0 s · 1 · −15.0 | Before/after cartoon dinosaur bars | Static-to-video |
| M26 | Finch "when my cat judges me" | 6 var | 11.1 s · 6 · −18.4 | Cat POV meme → app clips | Meme format with a real pet (one animal) |
| M27 | Fyxer finger puppets | 5 var | 48.4 s · 13 · −21.5 | Thumbs with drawn faces discuss email | The cheapest possible skit, 5 variants |
| M28 | Finch "train for life in prison" | 5 var | 8.2 s · 9 · −18.9 | Absurd caption over chores, 1.1 cuts/s | Absurd caption = hook |
| M30 | Skylight wordless montage | 7 var | 54.4 s · 48 · −15.9 | Kids doing chores, 0.9 cuts/s | Long montage works for a family device |
| M31 | Skylight "POV: you realize how often you need to nag" | 7 var | 29.4 s · 12 · −17.2 | Unbox → wall mount → feature labels | Unboxing hit-rate format (doc 45 D3) |
| M33 | Skylight "Champion of Family" | 6 var | 33.3 s · 4 · −18.1 | Mock boxing-announcer skit in a kitchen | Sports-commentary parody |
| M35 | Nomad leather grid | 7 var | 6.6 s · 1 · silent | Leather-ageing grid swap | Second 7-variant silent loop |
| M36 | PolarPro Light Leak | 7 var | 41.0 s · 42 · −14.9 | Creator films a beach day, 1 cut/s nostalgia | The output (the footage) is the proof |
| M37 | PolarPro Cineflow | 7 var | 15.4 s · 22 · −10.8 / +1.9 | 1.4 cuts/s montage of people filming | Fast montage, clipped |
| M38 | Anker "impossible triangle" | 4 var | 29.1 s · 4 · −12.2 / +1.3 | 16:9 product film, power/heat/size | Problem-as-geometry |
| M40 | Peak Design new colourways | 4 var | 24.8 s · 9 · −13.1 | Colour-field macros of zips and straps; bag lineups | A colourway launch film = a re-buy trigger (§6.4) |
| T03 | eufyMake creator unbox | 405K · 4.19 % | 75.0 s · 37 · −13.4 | Creator review: setup → wood print → materials | The creator version of A02 |
| T06 | Duolingo chess launch | 3.7M · 4.48 % | 21.2 s · 1 · −17.6 | Mascot VO over one shot: "Yes, that chess" | A feature launch as a 1-shot joke |
| T08 | Opal creator story | 68K · 0.27 % (paid) | 55.1 s · 25 · −17.5 | Digital-detox-cabin founder admits high screen time, "Project Doom Scroll" | Creator confession > brand voice |
| T10 | Keychron Nape Pro | 209K · 2.95 % | 36.3 s · 16 · −15.8 | "What if your mouse was already where your hands are?" | "What if" hook + desk macro |
| T11 | Light Phone III intro | 6.3K · 1.1 % | 75.5 s · 3 (graded long takes) · −18.4 | Wordless cinematic montage, letterboxed, "light iii" | Cinema without a hook gets 6K on TikTok |
| T12 | Elevation Lab TimeCapsule | 26.8K · 0.69 % | 6.0 s · 3 · −23.6 | AirTag dropped into a battery case: "Upgrade your AirTag" | A 6 s loop demo; the product is the before→after |
| T14 | Perplexity (Portuguese) | 3.8M · 0.39 % (paid) | 45.9 s · 13 · −25.3 | Localised Brazil spot | Paid reach without engagement |
| T15 | Flipper Zero mobile app | 874K · 4.46 % | 44.0 s · 18 · −12.1 | "If you have a Flipper Zero and aren't using the app, you're missing out" | Owner-education content sells the ecosystem |
| T16 | Nothing Phone (3) water test | 601K · 2.68 % | 17.4 s · 21 · −15.0 | The phone inside a stripped washing-machine drum rig | The rig as hero again (with A03) |

### 2.3 Metadata only (not downloadable this run)

| Launch | What is known | Lesson |
|---|---|---|
| **Friend** (Jul 30 2024, X) | ~21M+ views on X [c]; cost **$250K incl. $50K equity** [c]; a young-adults montage (hiking, gaming, a rooftop date) where the pendant texts its wearer; read as "Black Mirror" ([Digg](https://digg.com/tech/26a55vyb); [Dazed](https://www.dazeddigital.com/life-culture/article/63276/1/ai-friend-virtual-companion-answer-humanity-loneliness-epidemic-avi-schiffmann)); ~1,000 devices activated per The Atlantic vs "200K users" claimed [c] | Reach ≠ demand. A beautiful film for a product people fear is a lightning rod |
| **Cluely launch** (Apr 2025, X) | A "cheat on everything" film: the founder uses the tool on a date to lie about his age and art knowledge ([Business Today](https://businesstoday.in/amp/technology/news/story/ai-startup-cluely-raises-53-million-to-let-users-cheat-on-everything-even-job-interviews-and-exams-472946-2025-04-22)); ~737K views on the post (eChai); company says ~20M across platforms [v]; $5.3M seed then $15M a16z | Provocation as distribution — works for a "rage-bait" brand, poison for most |
| **Daylight DC-1** (May 2024) | Quiet narrator, "It's not here to change your life. But it might change the way you think about screens"; first 5,000 units sold out ([speedrun](https://speedrun.substack.com/p/how-to-make-a-viral-launch-video); Wikipedia) | Tone as positioning: calm film for a calm product |
| **Shortcut** (Fundamental Research Labs) | ~2 min, >50 % product walkthrough, founder on screen ~15 s; **4.1M impressions** + 3.5M on the "available now" follow-up; CTA "comment for an invite" ([speedrun](https://speedrun.substack.com/p/how-to-make-a-viral-launch-video)) | Demo-dominant + a comment CTA |
| **Kalshi NBA Finals** and **Lindy AI** (AI-made, 2025) | ~$2,000 production for a TV spot; 300–400 generations for 15 clips (doc 42 #9–10) | The AI-native studio precedent for app/SaaS buyers |
| **Halliday** (Kickstarter, Jan–Mar 2025) | $3.30M from 8,020 backers after a CES debut [m Kicktraq] | CES → Kickstarter is a 3-week runway for a pre-launch film |
| **Flow (Adam Neumann)** | "20M views, mostly negative", heavy cinematic slow motion ([Flowjam](https://www.flowjam.com/blog/founder-led-launch-video-examples-2026) [v]) | Cinema without a product truth backfires |

### 2.4 What the measured set says [m]

- **Sample:** 55 files with full audio analysis (the 58 minus Nomad's 2 silent loops and X02, which is reported separately).
- **Length:** median **26.3 s** (IQR 15–48 s); Meta median 24.8 s, TikTok 45 s, X launch films 90–249 s. The 15 s Short and the 30 s Premiere fit Meta; launch films on X run longer.
- **Pace:** median **0.30 cuts/s** (a cut every 3.3 s) — slower than the 1–2 cuts/s of action reels (doc 42). Skits and talking heads hold shots; montages (Skylight, PolarPro, eufyMake) run 0.9–1.4 cuts/s.
- **Speech in second 1:** **35 of 55** speak inside the first second; median 2.5 words/s. This niche hooks with a *sentence* (a question, a confession, a challenge). A VXO film needs a spoken or written line in second 1 *as well as* motion.
- **Screens:** in the 20 full teardowns, **only 5 show a real phone screen for more than half the runtime** (A08, A10, A11, A14 partly, M-series screen recordings); the highest-signal non-UGC ads show the UI for <3 s or as a floating overlay (A01, A04, A05, A06, A07) [inf from tiles].
- **AI in the wild:** 3 of 40 Meta ads use visibly AI or CG imagery as the hook or the whole film (A06 CG hands, A07 AI skydiver, A19 all-AI), plus Anker's CG chip (A13) and Nothing's CG teaser (A16). None uses an AI *customer*.
- **Loudness:** median −16.9 LUFS; **15 of 55 below −20 LUFS** (Orbitkey −37); **15 of 55 peak above 0 dBFS** (Cluely −7.7 LUFS / +2.1). Audio craft is weak across the niche — doc 46 standards are a visible differentiator.
- **Organic vs paid:** brand-account organic hits come from **established fan bases** (Nothing, Flipper Zero, Duolingo, Cluely); every small founder-led brand handle sampled sits at 200–7,000 views per post.

---

## 3. What converts in this niche (with data)

| Question | Evidence | Answer [inf from evidence] |
|---|---|---|
| **Format** | Motion, 2,949 ads: Screen Recording 24 % (most common), Demo 11 %, Yapper 9 %, Skit 4 % (but 4.01 mean variants), Cinematic B-roll 3 % (3.86) [m]; hardware leads with Demo 24 % [m]; doc 45 D3 hit rates: unboxing 9.83 %, founder 8.57 %, demo 8.11 %, cinematic b-roll 6.85 % [v] | **Screen recording is the default, so it is the commodity.** The winners wrap it: a metaphor or skit head (A06, A07, A10), a consequence shot (A04, A05), a challenge (A11), a rig (A03). VXO sells the wrapper and leaves a slot for the screen |
| **Screen-recording vs metaphor vs UGC** | Brex (1 shot, no UI) 4 variants; Monzo (no UI) 4; Timeleft (metaphor + UGC) 8; Rise (AI metaphor + UGC skit) 7; Opal (provocation + UI) 7; Fyxer (skit + UI) 5–6; Lovable (street UGC + UI) 8 [m] | **Metaphor or consequence first (0–3 s), UGC/skit body for belief, real UI for 2–5 s as the proof.** Pure-metaphor works for brands with recognition (Brex, Monzo); smaller founders need the UI proof inside the film |
| **Proof types** | Real UI recording (Opal, Fyxer, Skylight); the output touched (eufyMake A02, PolarPro M36); a test rig (Nothing A03/T16); social proof in copy ("160,000 devices shipped", "Editor's Choice", "featured in the FT") [m]; crowdfunding: "prototype footage often beats polished brand video because buyers value credibility" ([PledgeBox](https://pledgebox.com/post/crowdfunding-facebook-ads) [v]) | **Apps: the real screen + an award/press line. Hardware: the real prototype doing one thing on camera + the output in a hand.** AI never plays the proof (LESSONS) |
| **Claims** | Numbers everywhere: "132 emails before 9am", "$40 expense, 3-day approval", "160W = 210W", "5 mm texture", "double your attention", "IQ over 130", "1–2 lbs per week… results may vary" [m] | Every number on screen is the client's documented number; health/weight/sleep/IQ claims carry the disclaimer on screen (Noom does, M16). FTC: "no AI exemption" (§5) |
| **Offers** | Apps: free trial, quiz CTA ("Take the 1-minute sleep quiz"), annual-plan discount at BFCM/January; hard paywalls convert **10.7 % by day 35 vs 2.1 % for freemium**; trials ≥17 days convert 42.5 % vs 25.5 % ([RevenueCat via ppc.land](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/)). Crowdfunding: **$1 reservation** ("20–30× more likely to back"), early-bird tier (Halliday $369–399 vs $489 MSRP) [v] | An **offer slot** in the last 3 s: "Try free for 7 days" / "Reserve for $1" / "Early bird −25 %" — client-supplied, swappable per phase |
| **Length** | Measured median 26 s; Meta winners 10–60 s; 5–6 s silent loops with 7 variants (Nomad); X launch films 90–249 s; Kickstarter campaign videos historically best at 2–4 min (film-category data: 3–4 min → 52 % success, >5 min → 37 %) ([Stephen Follows](https://stephenfollows.com/film-crowdfunding-tips/)) | Deliver **15 s + 30 s + a 6 s loop** for ads; for a crowdfunding client, VXO's 15–30 s film is the **ad and the first 15 s of the campaign video**, not the whole 3-minute pitch (the founder's talking + prototype demo stays real) |
| **Placements** | Meta Reels/Feed; TikTok creators; Apple Search Ads and Google App Campaigns (asset-based, need 16:9/1:1/9:16) ([AppsFlyer](https://www.appsflyer.com/resources/performance-index/)); X for launches; App Store product page preview (screen capture only) | 9:16 master + 1:1 + 16:9 every time; an **App Store–safe cut** is a different deliverable (real capture only, §5) |
| **AI ads performance** | AI images lift CTR when they don't look AI (doc 45 D30–D31); AI-app buyers: 27 % of subscription apps are AI-powered [v]; Rise's AI hook (7 var) and Artlist's all-AI film (7 var) are running; Duolingo's AI-first backlash [press] | **AI is safest where it is obviously fiction (an absurd hook, a metaphor) or where AI is the product.** Never an AI person presented as a user |
| **Disclosure** | Meta "AI info", TikTok AIGC label, NY synthetic-performer law (doc 45 §5.3); Kickstarter requires an "AI use" disclosure for AI-generated campaign content (§5) | Label every film; for Kickstarter clients, the AI scenes are named in the campaign's "Use of AI" section |

### 3.1 How crowdfunding videos differ from paid ads

| | Kickstarter / Indiegogo campaign video | Pre-launch and launch paid ads (Meta/TikTok) |
|---|---|---|
| Job | Close the pledge on a warm visitor; build trust in a team that has not shipped | Stop a cold scroll; earn a $1 reservation or an email |
| Length | 2–4 min (film-category data: 3–4 min best) [Follows]; launch films on X 60–120 s | 6–30 s; one idea |
| Structure | Problem → **founder on camera** → prototype demo → how it's made → rewards → risks → thank you | Hook in second 1 → one mechanism → proof → offer ("Reserve for $1") |
| Rules | **Working prototype required; no photorealistic renderings** (Kickstarter help center); risks section; AI-use disclosure | Platform ad rules (§5); claims substantiation; AI label |
| What AI can do | Context and world (the problem, the place, the metaphor), clearly not the product working | The hook head, the metaphor, the world, mechanism cutaways — with real prototype footage as the proof slot |
| Success signal | 31 % of pre-launch followers back (Kickstarter outreach, secondhand); ~29 % of funding on day 1; 70 % of projects 30 % funded in 48 h succeed (old, secondhand) | Cost per lead **$2.34–3.40**, cost per VIP $17–29, VIP→backer 39.5 %, list→backer 11.8 % (LaunchBoom cases) [v]; PledgeBox case: $2.70 CPL, **1.5 %** lead→backer [v] |
| Refresh | Once, plus updates and a late-pledge / InDemand cut | Every 1–3 weeks during a 6–10-week pre-launch; new hooks at launch day, mid-campaign slump, final 48 h |

**What it means [inf]:** a crowdfunding founder buys **several** short films across one campaign (pre-launch hooks, launch-day, stretch-goal, final-48-hours, InDemand/late-pledge, then the store launch). That is the Season plan's natural shape in this niche.

### 3.2 Answers by sub-niche [inf]

- **Consumer subscription apps (health, sleep, focus, language, social):** hook with a sentence + a visual absurdity (A07) or a consequence (A05); real UI for 2–5 s; an award or rating line; offer = trial or quiz. Brief in December for January. Watch the "wellbeing paradox": a screen-time or human-connection app should not look AI-made — film the *real world* the app gives back.
- **AI apps and tools:** AI-made is on-brand (A19). Show the output (a generated thing), not a chat window. Comedy skits around the job (A10, A15) outperform feature lists.
- **Prosumer / SMB SaaS:** one frame of the pain (A04 Brex: "$40 expense, 3-day approval"); a metaphor that makes an invisible saving visible; a 3 s screen proof; LinkedIn and Meta. Founders here run statics (Sunsama: 0 of 16 ads are video) — a film is the gap.
- **Crowdfunded hardware:** the output in a hand (A02), the rig (A03), the teaser question (A16) before launch; the founder and the prototype in the campaign video; reservation offer. Short films for the 6–10-week pre-launch, the launch, and the last 48 hours.
- **Apple-ecosystem accessories:** 5–6 s loops (A12, T12), Day 1/Day 100, the click/snap sound; new iPhone = new SKUs every September.

---

## 4. AI realism pitfalls specific to this niche, and the fixes

This audience is the most AI-literate in any VXO niche: developers, early adopters, AI-tool founders, Kickstarter backers who have been burned. **A garbled UI is this niche's six fingers; a prototype doing something it can't do is this niche's fraud.** Every fix slots into doc 43's labeled-block prompts (§2.1) and failure table (§5).

### 4.1 Screens and UI text

| Trap | What goes wrong | Prompt / reference fix | Physics to write |
|---|---|---|---|
| **Readable UI generated by the model** | Seedance "softened named on-screen text" (doc 43 [B-ADH]); Wan is weak on text; letters melt, icons drift, notifications invent words | **Never generate a readable UI.** In the prompt: "the phone screen shows only a soft, unreadable glow in the brand's colour; no text, no icons, no app interface". Composite the client's **real screen recording** in post (corner-pin + motion track) or use **floating UI cards as overlays** (Pocket A01, Monzo A05) | Screen brightness ~500–1,000 nits indoors: the screen lights the thumb and face with a cool spill; reflections of the room move with the tilt |
| **Screen replacement drift** | A tracked insert slides when the phone tilts | Shoot/generate the phone **flat to camera and mostly still** during UI moments (≤10° tilt, no fast pans); add a clean dark screen as a tracking plate; edge-light the bezel | Fingers occlude the screen: put the tap *after* the insert, or rotoscope the thumb |
| **Notification and system UI** | AI renders a fake iOS banner; Meta bans fake notifications that look interactive (§5) | Notifications only as **clearly stylised brand cards** (not iOS chrome), or the client's real capture | — |
| **Typing** | Thumbs hover, letters appear without taps; hands with six fingers | No on-screen typing in AI shots; "thumb rests on the lower third of the screen, still" ; typing only in the real capture | Typing is ~3–5 taps/s for a thumb; a 20-word message takes ~25–40 s — don't promise "instant" visually |
| **Desktop/SaaS dashboards** | Fake charts, gibberish numbers | Monitors show "soft unreadable dashboard glow" from 2 m+; numbers only from the client's real recording | A 27-inch monitor at 70 cm fills ~40° of view; from 2 m it's a lit rectangle |

### 4.2 Phones, devices and wearables in hands

| Trap | Fix (doc 43 refs) | Physics / numbers |
|---|---|---|
| **The phone's identity changes** (camera bump count, colour, size) between shots | One generic phone sheet on grey (front, back, side) as a locked reference; **no Apple logo, no real camera-bump trade dress** (§5): "a generic modern smartphone, flat back, no logos" | A modern phone is ~147–163 mm tall, 7–8 mm thick, ~170–230 g: it fills a palm and the thumb reaches ~⅔ of the screen |
| **Grip errors** (floating phone, thumb through the case) | Kling 3.0 Pro i2v from a **real photo of a hand holding the client's device**; "exactly five fingers; the phone rests on the little finger; thumb on the screen's lower third" | Weight makes the wrist tilt back ~5–10° |
| **Wearables (pins, pucks, glasses, rings)** | Product sheet + one real worn photo (front, ¾); "the pin clips flat on the left chest pocket; never floats; always the same position" | A 20–30 g pin pulls a T-shirt fabric down a few mm; glasses frames sit on the nose bridge and ears (temple tips behind the ear) |
| **Smart-glasses displays** | **Never render what the wearer sees through the lens** (it's a claim and the model can't read it); show the reaction or a stylised overlay labelled "simulated view" | Display text in real waveguides is monochrome green/white and small — a full-colour cinematic HUD is an overclaim |
| **Earbuds, rings, watches** | Kling i2v from real photos; macro only; "the ring stays on the same finger" | — |

### 4.3 Pre-launch prototypes (the legal and AI trap at once)

| Trap | Why it matters | Fix |
|---|---|---|
| **The film shows a function the prototype can't yet do** | Kickstarter: "show working prototypes… no photorealistic renderings"; "Projects can't mislead people or misrepresent facts" (§5); FTC §5 | The **product's function is shown only in real prototype footage** (proof slot). AI films the world, the problem, the person's reaction, the metaphor — and the product *at rest* from the client's photo |
| **A "photorealistic rendering" of an unbuilt product** | Explicitly banned on Kickstarter (help center); risky on Indiegogo and in ads | If the client has only CAD: stylised/clearly-CG (A16 Nothing teaser, A13 Anker chip) with a "Concept render" super, **never** photoreal in-hand use |
| **The AI product drifts from the prototype** (button count, LED colour, finish) | Backers compare the film to the delivered unit; refund demands and comment storms | Product sheet from **real prototype photos** (6 angles on grey), "never redesigned"; Kling i2v for every product close-up; continuity check (doc 46 `continuity_check.py`) on the product crops |
| **Unboxing of a box that doesn't exist yet** | Implies shipping readiness | Unbox only the real packaging sample, or skip unboxing |
| **"Ships in X weeks" visuals** (stacks of boxes, warehouses) | FTC Mail Order Rule needs a reasonable basis for any shipping promise | No logistics imagery unless the client is shipping |

### 4.4 Mechanism and metaphor shots (where AI is strongest here)

- **Inside-the-machine cutaways** (chip, signal, sensor, encryption, battery): no realism expectation (A13). Cinema Studio 4.0 single-shot or Kling i2v from a clean CG still.
- **Literal metaphors** (an inbox as a paper avalanche, M12; a phone as a drug, A08; a wallet in a washer, A05): one physical event, real-world physics, a real crew rig.
- **Absurd hook stills** (A07): deliberately impossible, so no one reads them as a claim; 3–6 s; framed as a post/tweet card.

### 4.5 Model per shot type (consistent with doc 43 §1)

| Shot type in this niche | First choice | Settings | Why |
|---|---|---|---|
| Phone/device in hand, product macro, wearable on body | **Kling 3.0 Pro i2v** from a real photo | 5 s, `sound:"off"`, `cfg_scale` 0.5, screen = dark glow | Keeps product details from the input image; one move |
| Consequence / pain scene (a street, an office, a laundromat, a kitchen) | **Seedance 2.5 r2v**, 3–5 shots, tight rigs | 8–15 s, "EXACTLY N SHOTS", "all screens unreadable glow, no text" | Multi-angle fidelity; a locked plate |
| One-take cinematic pain frame (Brex-style) | **Cinema Studio 4.0** `pacing:"single-shot"` | 8–10 s, `camera_movement:"dolly-in"` or locked | Doc 43 §7.3 |
| Comedy skit beat with a held final shot | Seedance 2.5 r2v (doc 43 §7.5) | 8–10 s; any line as VO with the mouth off-screen, or lips via Wan 3.0 r2v | LESSONS lip rules |
| Absurd hook still → motion | Image model still + Kling 3.0 Pro i2v | 3–5 s | Cheap, obviously fictional |
| Mechanism cutaway (chip, signal, sensor) | Kling 3.0 Pro i2v from a CG-style still, or Cinema Studio | 5 s | No realism expectation |
| UI | **Never generated.** Real screen recording composited in post, or brand-styled floating cards built in After Effects/Figma | — | App Store 2.3.4; text fidelity |
| Previs | Wan 3.0 480p | seed fixed | $0.05/s |

---

## 5. Policy and legal

**Not legal advice.** Facts fetched this run are linked. Facts marked [unverified] were not re-read this run; check them before the first client campaign.

### 5.1 App stores

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| **App Store preview video** | "To ensure people understand what they'll be getting with your app, **previews may only use video screen captures of the app itself**… You can add narration and video or textual overlays." Rejections cite device frames, a "self-promotional ad", footage other than the app in use | [App Store Review Guidelines 2.3.4](https://developer.apple.com/app-store/review/guidelines/) (fetched); [Apple forum](https://developer.apple.com/forums/thread/815379) | **A VXO film is never the App Store preview.** Offer an "App Store–safe cut" only as the client's real capture + VXO's narration/overlays |
| **Screenshots** | Must "show the app in use, and not merely the title art, login page, or splash screen"; overlays allowed | 2.3.3 (fetched) | VXO stills can be *ad* stills, not store screenshots unless they contain the real UI |
| **Other platforms / trademarks in metadata** | No names, icons or imagery of other mobile platforms; no third-party trademarks without permission | 2.3.10, 5.2.1 (fetched) | No Android robot in an iOS app's assets and vice versa; no competitor logos |
| **Apple marketing identity** | Use only Apple-supplied badge artwork; badge clear space = ¼ its height; min 40 px on screen; swap the pre-order badge at release; don't use images from apple.com; older guide: Apple product images only from Apple, custom photography needs approval, show devices without cases | [Apple Marketing Guidelines](https://developer.apple.com/app-store/marketing/guidelines/) (search summary); 2015 guide [unverified current] | End cards use Apple's real badge, never an AI-redrawn one. **AI must not render an iPhone with an Apple logo or iPhone trade dress** — use a generic phone; real iPhones only in the client's own footage |
| **Google Play** | Preview assets must "accurately represent the app or game"; non-compliant assets lose featuring eligibility; secondary guidance says mostly real UI footage | [Google Play best practices](https://support.google.com/googleplay/android-developer/answer/13393723?hl=en); [9to5Google](https://9to5google.com/2021/04/29/google-play-misleading-apps/) | Same as Apple: real footage for store assets |

### 5.2 Ad platforms

| Platform | Rule | Source | VXO rule |
|---|---|---|---|
| **Meta: non-existent functionality** | No imagery that copies play buttons, notifications or checkboxes that don't work; interactive-looking elements must function | [Meta ad standards](https://transparency.meta.com/policies/ad-standards/deceptive-content/non-existent-functionality/) (search summary; URL 404 on fetch) | **No fake iOS/Android notification banners, fake "Install" buttons, fake chat bubbles styled as system UI.** Brand-styled cards only |
| **Meta: depicting Meta's own UI** | No inaccurate depiction, no added effects/animation, no isolated UI elements | Meta brand-resource rules via [search](https://robpegoraro.com/tag/rules/) [unverified] | Never animate an Instagram/Facebook interface |
| **TikTok: misleading claims** | Ad and landing page must not promise or exaggerate results; products in the ad must match the landing page; no creative telling users to do things the app doesn't support | [TikTok misleading and false content](https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content) | The film shows only what the app does today |
| **All: AI labels** | Meta "AI info", TikTok AIGC label (reported mandatory for ads from 21 Jul 2026), NY synthetic-performer disclosure from 9 Jun 2026 | doc 45 §5.3 | Label; keep C2PA |
| **Google Ads** | Since Jan 2025, restricts standalone buttons in image ads that lack clear context | [rubyshore summary](https://rubyshore.com/?p=43223) [unverified] | No fake buttons in stills either |

### 5.3 Crowdfunding platforms

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| **Kickstarter hardware** | "Creators are required to show **working prototypes**… **We do not allow photorealistic renderings.**" Creators must explain how they will make it and whether they've made something like it before | [Kickstarter help center](https://help.kickstarter.com/en-us/articles/16236428-what-are-the-rules-for-hardware-and-product-design-projects) (fetched) | AI never shows the product working; product close-ups only from real prototype photos; any CG is stylised and labelled |
| **History of that rule** | 2012: renders and simulations banned; 2014: rules simplified to three principles and the render/simulation ban reported removed; the help center today again states the ban | [Engadget 2012](https://www.engadget.com/2012-09-21-kickstarter-clampdown.html); [bit-tech 2014](https://bit-tech.net/news/kickstarter-renders/1/); help center (fetched) | Treat the strict version as binding — enforcement is human review at submission [unverified how strict in practice] |
| **Honesty principle** | "Projects can't mislead people or misrepresent facts, and creators should be candid about what they plan to accomplish" | Kickstarter rules via [NoFilmSchool](https://nofilmschool.com/2014/06/kickstarter-launch-now-rule-changes) (kickstarter.com/rules returns 403) | — |
| **Kickstarter AI disclosure** | Since 29 Aug 2023, projects using AI-generated images/text/outputs must disclose which parts are AI and which are original; undisclosed AI → suspension; AI-tech projects must describe training data and consent | [TechCrunch](https://techcrunch.com/2023/08/01/kickstarter-requires-generative-ai-projects-to-disclose-additional-info/amp/); [Engadget](https://www.engadget.com/kickstarter-projects-will-soon-have-to-disclose-any-ai-use-145100394.html) [current text unverified] | **Every VXO film used on a campaign page goes into the "Use of AI" section, scene by scene.** Put this in the delivery notes |
| **Indiegogo** | Terms require good-faith fulfilment and truthful answers; hardware stage labels (Prototype / Manufacturing / Shipping) are granted after Trust & Safety review; 2016 reporting said Indiegogo tolerated renders where Kickstarter didn't | [Indiegogo terms](https://indiegogo.com/about/terms); [Indiegogo trust](https://learn.indiegogo.com/trust); [Engadget 2016](https://www.engadget.com/2016-12-08-indiegogo-terms-of-use-update.html) [current render policy unverified] | Same VXO rule as Kickstarter |
| **FTC on crowdfunding** | First case (Chevalier, 2015): a creator who spent backer money on himself; order bars misrepresentations about crowdfunding campaigns; $111,793 judgment suspended | [FTC](https://www.ftc.gov/node/47254); [Mediaite](https://www.mediaite.com/online/first-ftc-case-against-deceptive-crowdfunding-ends-in-settlement/) | Crowdfunding ads are ads: FTC §5 applies to every claim |
| **Equity crowdfunding (Reg CF)** | Ads for an offering are limited to "tombstone" content pointing to the portal [unverified] | SEC Reg CF Rule 204 [unverified] | If a founder is raising on Wefunder/StartEngine, VXO films are product ads only and say nothing about investing |

### 5.4 US law: claims, subscriptions, pre-orders

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| **AI capability claims** | FTC "Operation AI Comply" (Sep 2024): five actions incl. **DoNotPay** ("robot lawyer" that didn't work as claimed, $193K) and Rytr; "there is no AI exemption from the laws on the books" | [Orrick](https://www.orrick.com/en/Insights/2024/10/FTC-Targets-Unfair-or-Deceptive-AI-Practices-With-Five-New-Enforcement-Actions) | A film may not show the AI doing more than it does (accuracy, "replaces a lawyer/assistant", "writes like you") without the client's evidence |
| **Subscriptions** | The FTC click-to-cancel rule was **vacated by the 8th Circuit (Jul 8 2025)**; **ROSCA still applies**: clear disclosure of material terms before billing, express consent, simple cancellation; up to $53,088 per violation; state auto-renewal laws (CA, NY, MN) apply | [Cooley](https://www.cooley.com/news/insight/2025/2025-07-11-click-to-cancel-just-got-cancelled-eighth-circuit-vacates-entirety-of-ftcs-negative-option-rule); [Womble](https://www.womblebonddickinson.com/us/insights/alerts/ftcs-click-cancel-rule-vacated-remember-it-was-not-alone) | "Free trial" on screen only with the client's terms line ("then $X/yr, cancel anytime") |
| **Pre-orders** | FTC Mail, Internet, or Telephone Order Merchandise Rule: a reasonable basis to ship within the stated time (or 30 days); delay → consent or refund | [FTC rule](https://www.ftc.gov/legal-library/browse/rules/mail-internet-or-telephone-order-merchandise-rule) | No "ships next week" visuals unless true; reservation ads say "reserve", not "buy now, ships today" |
| **Health/wellness app claims** | Sleep, weight, IQ, mental-health outcome claims need competent and reliable evidence; Noom shows "Individual results may vary" on screen (M16) | FTC Health Products Compliance Guidance [unverified] | The proof slot holds the client's study or rating; outcomes are never acted by AI people |
| **Fake reviews / AI testimonials** | Up to $51,744 per violation | doc 45 §5.3 | No AI "users" endorsing; review cards only verbatim and real |
| **Impersonation / real people** | Doc 45 §5.2; Friend/Cluely-style provocation around real people is a defamation and right-of-publicity risk [inf] | — | Invented people only; no lookalikes of founders' rivals |
| **Children** | COPPA for apps aimed at under-13s [unverified]; LESSONS: never generate babies | — | Kids in family-app films (Skylight-type) come only from the client's licensed footage |

### 5.5 Pre-flight checklist additions (with doc 45 §5.4)

- [ ] **No generated readable UI** anywhere; every UI moment is the client's real capture or a brand-styled overlay card, never fake system chrome (iOS banners, Meta UI, Install buttons).
- [ ] **No Apple logo, no iPhone trade dress, no Android robot** in AI shots; App Store/Google Play badges are the official artwork.
- [ ] Product function shown only in real prototype/app footage; product close-ups from real photos; any CG labelled "concept".
- [ ] Every number (ARR, devices shipped, minutes saved, accuracy, battery, "first") traced to the client's document.
- [ ] Offer line carries the trial/renewal terms (ROSCA) or "Reserve for $1 — fully refundable" exactly as the client's page says.
- [ ] Kickstarter/Indiegogo clients: an "AI use" note per scene delivered with the film.
- [ ] No AI person as a user; any AI human → on-screen disclosure (NY) + platform label.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film [inf with evidence]

- **Founder/CEO** of a $1–20M app or SaaS: teams are tiny (Opal: $10M ARR with 11 people [c]); the founder approves every public asset, often fronts the ads (Speechify A09) and posts the launch film personally on X (Pocket, Monogram, Friend, Cluely).
- **Head of growth / performance marketer** (apps): owns Meta, TikTok, Apple Search Ads; judges creative on **cost per install, trial-start rate and day-7/day-30 revenue**, not views. Pain: creative fatigue and volume (Ladder 117 new ads a week, Finch 70, Opal 28) [v].
- **Hardware founder + a crowdfunding agency** (LaunchBoom, BackerKit Launch, Jellop and similar): the agency runs the reservation ads and often owns the creative calendar; the founder pays. VXO pitches the founder; expect the agency in the thread [inf].
- **Launch-video buyers**: founders who budget a one-off launch film. Price anchors: launch-video studios quote **$1,000–16,000 for most seed/Series A films, ~$2,940 average for 60 s** [v, [Flowjam](https://www.flowjam.com/blog/how-much-does-a-startup-launch-video-cost-2026)]; mid-market studios $5–15K; premium $15–150K; Friend's film $250K [c]. Kickstarter videos: $2,300–25,000 per production companies [v, [StartMotion](https://www.startmotionmedia.com/how-much-should-i-pay-for-kickstarter-video-production)]. AI UGC avatars: $50–500 per video (doc 45 D44).

### 6.2 What they fear (ranked)

1. **"Our users will roast AI."** This audience builds or uses AI daily and spots tells instantly; Duolingo's AI-first backlash and Friend's "Black Mirror" reception are the stories they know.
2. **Inaccuracy that costs them a store or a campaign**: a wrong UI (App Store 2.3.4 rejection, user confusion), a prototype shown doing what it can't (Kickstarter suspension, backer revolt, refund demands).
3. **It won't move CPI/trial/ROAS**: they have dashboards; a pretty film that doesn't beat their screen-recording control is a waste.
4. **Volume**: app teams ship dozens of creatives a week; one film looks small.
5. **Tone mismatch**: a calm product (Daylight, Light Phone, Opal) can be wrecked by a loud film; a provocative brand (Cluely) wants the opposite.
6. **Timing**: launches, funding announcements and Kickstarter dates don't move.

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames with *their* product**: for apps, one frame shows **their real UI composited as an overlay card** (proves the method that avoids fake UI); for hardware, frames built from their real prototype photos (correct buttons, LEDs, finish).
- **A niche spec film** (§8's best three) with a visible proof slot and an offer slot.
- **A test plan in their language**: "same body, new 3 s head — measure hook rate, CPI and trial starts against your current control". Doc 45 §1.3 benchmarks.
- **A compliance sheet**: App Store–safe cut (yes/no), Meta non-existent-functionality check, Kickstarter "Use of AI" scene list, claims sheet. This is the thing their current AI-UGC vendor does not give them.
- **A variant pack**: one film → 3 hooks × (6 s, 15 s, 30 s) × 9:16/1:1/16:9 + stills.

### 6.4 Re-buy triggers (why they rebook monthly)

| Trigger | When | Evidence |
|---|---|---|
| **Feature releases** | Apps ship updates every 2–4 weeks; each major feature is a launch (Duolingo chess, T06; Flipper's mobile app, T15) | [m] |
| **New Year and back-to-school** | Trials spike Jan 1; health/education peak early January | Adapty [v] |
| **Crowdfunding phases** | Pre-launch (6–10 weeks of reservation ads) → launch day → mid-campaign slump/stretch goals → final 48 h → late pledges/InDemand → store launch → retail | §3.1 |
| **Funding announcements** | Seed/Series A films (Monogram, Pocket) are >90 s founder films; the ad cut-downs follow | Awesomic [v]; X02 [m] |
| **Platform calendars** | WWDC (Jun), iPhone (Sep), Android/Pixel (Aug–Oct), CES (Jan) | [inf] |
| **Creative fatigue** | Brands in this niche refresh 3–192 creatives a week | Motion [v] |
| **Colourways and editions** | Peak Design "New colourways" (M40); limited editions | [m] |
| **Price/plan changes** | BFCM annual-plan discounts; new tiers | [inf] |

**Season-plan argument here:** a locked skeleton per app (the "consequence" gag) re-shot for each feature launch, each season (January, back-to-school, BFCM) and each locale (Perplexity's Portuguese spot, T14) — 2–4 films a month without a new idea each time. For a crowdfunding client, the campaign itself is a 3–4-month Season.

### 6.5 Best outreach angle

Lead with **the consequence of their product working, filmed in the real world, with their real UI in one frame** — not with "AI video". For hardware: "your prototype in one real shot, the world around it built by us, Kickstarter-compliant". Name one real, recent thing (a release note, a "coming soon" page, a funding post). Offer 5 free frames, yes/yes (per `vxo-leads` §3). Never criticise their screen-recording ads; say they are the proof and VXO builds the hook around them.

### 6.6 Sample first DM (never sent; for a founder-led focus/screen-time app that just shipped a new feature)

> Hi [first name] — "[their exact release-note line]" is your best copy this year.
> Film idea: a phone buzzes itself off a café table — nobody flinches; its owner is 20 minutes into a book. Your real screen is the proof.
> I make AI product films (no shoot), always with your real UI.
> Want 5 free frames for [feature name], or for January?

(56 words. No link. Screen-time numbers only from their own data. Status: **NOT SENT — awaiting owner approval.**)

**Crowdfunding variant (never sent):**
> Hi [first name] — saw the Kickstarter "coming soon" page for [product]; the [one real detail] shot of the prototype is excellent.
> One pre-launch ad idea: [one-line consequence gag]. Your real prototype footage stays the proof; we build the world around it, Kickstarter-compliant.
> I make AI product films (no shoot). Want 5 free frames for the pre-launch ads, or for launch day?

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on moves a lead by **−30 to +30**; HOT stays ≥ 70 after the add-on. Public pages only. (Note for the base score: in this niche "running paid ads" is checked on Motion/Meta Ad Library for apps, and on the Meta Ad Library for the crowdfunding agency's reservation page for hardware.)

| Signal | Points | How to check |
|---|---|---|
| **Kickstarter/Indiegogo "coming soon" page live, launch 3–8 weeks out** | **+10** | Kickstarter prelaunch page ("Notify me on launch", follower count if shown); the brand's site "Reserve for $1"; Kicktraq for past campaigns |
| **Reservation/pre-order ads running** (a $1 deposit or "Reserve" landing page with active Meta ads) | +8 | Meta Ad Library (manual) for the brand name; Shopify `products.json` for a "reserve"/"deposit" product (e.g. Daylight's "pre-order deposit") |
| **Funding announced in the last 60 days** (seed/Series A, YC demo day) or a launch film posted on X in the last 30 days | +6 | X, TechCrunch, YC launches; X view count via yt-dlp metadata |
| **App with revenue signals and a screen-recording-only library**: ≥1,000 App Store ratings or a public ARR claim ≥$1M, and ≥70 % of the 20 newest Meta ads are Screen Recording / Headline / static | +6 | App Store page (rating count); Motion brand page tags |
| **Season window fit**: health/sleep/fitness/focus/language apps **in Oct–Nov** (for January); education/note-takers in Jun–Jul (for back-to-school); hardware 6–10 weeks before a Feb–May or Sep–Nov campaign | +5 | Today's date vs §1.5 |
| **Product Hunt launch scheduled** (upcoming page) within 30 days | +4 | producthunt.com upcoming/ship page |
| **Monthly release cadence** (App Store version history ≤30 days between versions; changelog) | +3 | App Store "Version History"; changelog page |
| **Founder already fronts content** (founder ads, X launch films) — a body exists for a VXO hook head | +3 | Motion "Founder" tag; X |
| **Audio faults in their paid video** (peak > 0 dBFS or < −24 LUFS) — a friendly, concrete DM note | +2 | `ebur128` on one public ad (15/55 measured ads clip, 15/55 are below −20 LUFS) |
| **Pre-revenue and unfunded** (no ratings, no ads, no raise) | **−15** | App Store, Crunchbase, Ad Library |
| **Hobby/indie app** (<200 ratings, no ads) | −10 | App Store |
| **App factory** (non-founder-led publisher shipping 100+ creatives/week, no founder visible) | −10 | Motion new-per-week (WalkFit 192, Yoga-Go 149, The Coach 110) — they produce in-house at volume |
| **Gambling, prediction markets, crypto trading, "get rich" apps** | −10 | Restricted ad categories; regulator attention [unverified per platform] |
| **Unsubstantiated outcome claims** (IQ, weight-loss guarantees, "replaces your lawyer/therapist") | −8 | Their ads; FTC Operation AI Comply pattern |
| **Live campaign past day 7 below 30 % funded** | −8 | Kicktraq; low odds and no budget — offer only if they ask |
| **Past campaign that failed to deliver / backer complaints** | −15 | Kickstarter comments, Reddit, press |
| **Brand built on anti-AI or "human-only" positioning** (and no stated openness to AI) | −5 | Their site/manifesto — pitch real-world consequence films only, with care |
| **Corporate-owned / big-co** (Anker/eufyMake, Snapmaker, Nothing, Duolingo) | −5 | Ownership; the path runs through agencies |

**VERY hot in this niche looks like [inf]:** a founder-led hardware startup with a Kickstarter "coming soon" page live and a launch 4–6 weeks out, a $1 reservation page with Meta ads running, real prototype photos but no pre-launch film; **or** a $1–20M founder-led app with ≥1,000 ratings, a feature release in the last 30 days, a Meta library of screen recordings and statics, and January 8–10 weeks away. Example: base 74 + coming-soon 10 + reservation ads 8 + funding 6 + season 5 = **103 → cap at 100**.

---

## 8. Ten ready film concepts (invented brands)

Conventions:
- Invented brands; clear names on USPTO before use. Phones are **generic, logo-free devices**; no Apple/Google/Meta UI anywhere.
- **Otto and Vee appear only in C10** (VXO's own spec). Any other concept becomes a VXO spec film by casting Otto as the deadpan lead (mouth never visible) and Vee with her one stopwatch.
- Every camera position is a real rig: tripod (incl. low-mode and long-lens across a street), C-stand overhead arm, slider, dolly, handheld gimbal follow, Steadicam, a lipstick camera placed before the take. **The camera never passes through glass, walls, screens or bodies.**
- **Proof slot** in every concept = the client's real screen capture (apps) or real prototype footage (hardware). AI never renders readable UI or shows the product doing something it does not do (§4, §5).
- **UI moments** are composited in post as the client's capture or a brand-styled floating card (the Pocket A01 method).
- No dialogue on visible lips. Every film ends with a 2-line VO tagline in a locked voice over a frame with no visible lips, the logo card and an **offer slot** ("Try free for 7 days — then $X/yr" or "Reserve for $1").
- **Costs** use doc 43 §6 list prices, as in docs 56–60: Seedance 2.5 r2v 15 s = $3.09 proof (480p) + 3 × $6.93 (720p) = **$23.88**; 10 s = **$15.92**; 8 s = **$12.74**; Seedance 2.5 i2v 6 s = **$6.78**; Kling 3.0 Pro i2v 5 s sound-off × 2 takes = **$0.95**; Cinema Studio 4.0 8 s = **$5.36**; Wan 3.0 480p previs 15 s = **$0.75**; stills ≈ $0.30 each; ElevenLabs VO ≈ $0.10. Totals exclude the client's proof footage.

---

### C1 · BENDWELL (braided USB-C cable, Kickstarter pre-launch) — "Night Shift" (15 s) ★ BEST 1 · ★ SINGLE BEST

- **Idea:** A test lab, 6 p.m. A technician starts the bend tester on a BENDWELL cable and settles in. Mugs pile up, the window goes dark, then blue. At dawn he is asleep on his arms; the rig is still flexing the cable. He wakes, reaches for his phone: dead — it was charging all night on his own frayed old cable. Deadpan beat. He unplugs BENDWELL from the rig and plugs it into his phone.
- **Hook (0–1 s):** sound first — the rig's servo clack, already mid-stroke, in a macro of the cable flexing (the client's real rig footage).
- **Punchline (product-caused):** the thing on the torture rig outlasted the man running it *and* the cable he trusted; only a cable built for the rig can end the film plugged into his phone.
- **Built on:** A03/T16 Nothing test rigs (9.1M views, 149K shares, AI-safe machines), A01 Pocket's deadpan comedy, doc 44 "the held last shot is the joke", the LESSONS proof-slot rule.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Proof slot: real footage.** Client's bend-test rig, locked macro (100 mm) | The cable flexes ±90° over a mandrel, small brass weight swinging; clack |
| 2 | 1.5–3.0 | **Locked tripod, lab wide**, 35 mm, eye height, technician at ¾ back | He presses the green start button, sits, opens a laptop (screen = unreadable glow); window shows dusk |
| 3 | 3.0–5.0 | **Proof slot: real footage.** The rig's cycle counter at the client's tested number, with the test condition super | e.g. "Tested: [N] bends at ±90°, [load] g" — client document only |
| 4 | 5.0–7.0 | Same tripod, same frame, **night** | Desk lamp only; three empty mugs; he stretches, yawns (back to camera); the rig flexes, soft-focus in the background (composite of the real rig plate) |
| 5 | 7.0–9.0 | Same tripod, **dawn** | Cold blue window light; he is asleep on folded arms; rig still flexing |
| 6 | 9.0–10.5 | **Overhead C-stand arm** above the desk | His generic phone, black screen, on the end of a visibly frayed old cable (braid split, white inner jacket showing) |
| 7 | 10.5–12.5 | Tripod, medium, ¾ back | He wakes, taps the phone twice: nothing. He turns his head slowly toward the rig. Hold |
| 8 | 12.5–15.0 | **Tabletop slider**, macro, then packshot (real photo) | Hands unplug BENDWELL from the rig, plug it into the phone; a soft charging glow on the screen (no UI); logo + "Reserve for $1" |

- **Physics check:**
  - A typical flex tester runs ~40 cycles/min → a clack every **1.5 s**; 6 p.m. → 6 a.m. = 12 h ≈ **28,800 cycles** [calc]. Only the client's *real* number goes on screen (shot 3); the night is just "a long time".
  - A ~4 mm braided cable needs a bend radius ≥ ~5× its diameter (≥20 mm) — write "the cable wraps a 20 mm mandrel, never kinks" [inf].
  - The swinging weight lags the arm by ~0.1–0.2 s and settles; it never floats.
  - Light: 6 p.m. warm dusk (~3,500 K) → desk lamp (~2,700 K) → dawn blue (~8,000 K skylight) through the same window; shadows move consistently with one window.
  - Mugs accumulate (1 → 3 → 3), never vanish (doc 43 rule 12).
  - Camera never moves inside shots 2/4/5/7 — one plate, three lighting states (the cheapest safe AI construction).
- **Audio map (timecoded):**
  - 0.0: servo clack (real rig sound), repeating every 1.5 s through 12.5, ducked −8 dB under other events.
  - 1.6: chunky start-button click; 2.0: fluorescent hum in.
  - 3.0: counter tick (real); 5.0: hum out, single desk-lamp buzz, one distant car pass.
  - 6.2: a mug set down on the laminate (ceramic tick).
  - 7.0: first birds outside (dawn), 7.4 a soft snore inhale.
  - 10.6–11.2: two dull thumb taps on glass; 11.2–12.5 silence except the clack (the beat).
  - 12.9: crisp USB-C seat click; 13.2 a low two-note sonic logo.
  - 13.0: VO (dry, warm, mouth off-screen): `Built for the night shift.` [pause] `Yours, for a dollar.` 
- **Model / template:** shots 2, 4, 5, 7 = **one Seedance 2.5 r2v 10 s clip** ("EXACTLY FOUR SHOTS AND THREE HARD CUTS; the camera is a locked tripod and never moves; only the light changes"; refs: lab plate, technician from behind/¾, generic phone sheet, real rig still as background); shot 6 = **Kling 3.0 Pro i2v** from a real photo of a frayed cable and a generic phone; shot 8 = Kling i2v from real BENDWELL photos; shots 1, 3 real; Wan 3.0 previs.
- **Cost:** $15.92 + 2 × $0.95 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $21**.
- **Claim check:** the cycle number appears only in the real proof slot with its test conditions; the old cable is unbranded and visibly years-worn (no competitor implied); the rig footage is real, so Kickstarter's "working prototype, no renders" rule is met; "Reserve for $1" matches the client's page.
- **Why it's the single best:** sound-first hook built from the client's *own* proof; the punchline is caused by the product's real property (durability) without a fake demo; no faces, no UI, one locked plate → the safest generation in the niche; it is Kickstarter-compliant by construction; it re-skins for every durability product (cases, bags, hinges, keyboards, chargers) and for each campaign phase (pre-launch "Reserve", launch "Back it now", final 48 h "Last night of early-bird pricing") — a Season franchise.

### C2 · TALLYHO (receipt-capture expense SaaS for small teams) — "Receipt" (15 s) ★ BEST 2

- **Idea:** A café terrace. A gust lifts a paper receipt off the table and an office manager sprints after it across a plaza — around a bench, past a cyclist, down three steps — and loses it into a fountain. She walks back, soaked to the knee. Her colleague hasn't moved: he snapped the receipt with TALLYHO before it left the table. Deadpan sip.
- **Hook (0–1 s):** motion in frame 0: the receipt already airborne, the gust audible.
- **Punchline (product-caused):** the paper never mattered — the expense was filed the moment it was photographed.
- **Built on:** A04 Brex (B2B pain in one street frame), doc 41/44 chase coverage, doc 44 "the reversal is caused by the product".

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Low tripod at table height**, 35 mm | A receipt lifts off the café table, tumbling; two hands grab at air |
| 2 | 1.5–3.0 | **Handheld gimbal follow**, 24 mm, behind her | She sprints after it across the plaza paving, bag strap flying |
| 3 | 3.0–4.5 | **Long-lens tripod across the plaza**, 135 mm, compressed | The receipt flutters over a bench; she vaults around it; a cyclist passes in the foreground |
| 4 | 4.5–6.0 | **Low-mode tripod at step level** | Her shoes take three steps down, one skip; receipt tumbles past the lens |
| 5 | 6.0–7.5 | **Locked wide on the fountain** | The receipt lands on the water, darkens, sinks slowly; she stops at the rim, one foot in the water |
| 6 | 7.5–10.0 | **Tripod back at the table**, 50 mm, colleague ¾ back | He hasn't moved; he lifts his phone slightly (screen = glow) and sips |
| 7 | 10.0–12.0 | **Proof slot: real screen capture** composited as a floating card | The client's real "receipt captured → expense submitted" flow, 2 s |
| 8 | 12.0–15.0 | Same table tripod, wider | She returns, soaked to the knee, sits; he slides her coffee over. Logo + offer slot "Try TALLYHO free for 14 days" |

- **Physics check:** thermal receipt paper ~55 g/m², 8 × 20 cm (≈0.9 g) lifts in a ~6–8 m/s gust and **tumbles** (flutter, not glide) at ~0.5–1.5 m/s descent; it never flies in a straight line. Her sprint ~4–5 m/s, so she closes the gap in ~1–2 s — the gust must re-lift it twice (shots 3, 4) [calc]. Paper on water wets and darkens in ~1–2 s, then sinks or floats flat; it does not stay crisp. Wet trousers darken to the knee only on the leg that stepped in; the fate of the receipt is scripted (doc 43 rule 12). The cyclist stays in his lane; nobody is hurt.
- **Audio map:** 0.0 gust whoosh + paper flutter; 0.6 chair scrape; 1.5 running footsteps on stone (every 0.25 s); 3.2 bike bell (doppler); 4.6–5.2 three step slaps; 6.4 tiny splash, 6.9 shoe in water (heavier splash); 7.5 café ambience returns, cup clink at 8.6; 10.0 one soft UI chime (brand sound, not iOS); 12.2 squelch as she sits; 12.5 VO (mouth off-screen): `Lost the receipt?` [pause] `Not the expense.`
- **Model / template:** shots 1–5 = **Seedance 2.5 r2v 8 s**, "EXACTLY FIVE SHOTS AND FOUR HARD CUTS", doc 43 §7.2 adapted (a human chase, no stunts); refs: plaza plate (clean, no signage), the woman (wardrobe sheet, face mostly from behind), receipt sheet; shots 6 and 8 = **Seedance 2.5 r2v 6 s** on one table plate; shot 7 real capture.
- **Cost:** $12.74 (8 s chase clip) + $6.78 (6 s table clip, same per-second price as i2v) + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $23**.
- **Claim check:** only real features (capture, auto-fill) appear in the proof slot; "free for 14 days" exactly as the client's terms, with the renewal line (ROSCA).

### C3 · LULL (focus / screen-time app) — "Is It Dead?" (15 s) ★ BEST 3

- **Idea:** A busy café. Phones buzz on every table; on each buzz, a ring of hands reaches in unison — a Pavlovian ballet. One phone, face-down beside a woman reading, never moves. A waiter, unsettled by the silence, picks it up, taps it, then holds it to his ear like a seashell. She turns a page.
- **Hook (0–1 s):** sound first — a hard double buzz on wood, a phone already skittering in macro.
- **Punchline (product-caused):** LULL's focus session is the only reason her phone is silent; the waiter treats silence as a malfunction.
- **Built on:** A08 Opal's "phone as drug" provocation, A17 Orbitkey's sound-gag, doc 44 rule of three, the DM in §6.6.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.2 | **Low-mode tripod on a marble table**, 100 mm macro | A generic phone buzzes and creeps 2 mm; screen glow, no text |
| 2 | 1.2–2.5 | **Overhead C-stand arm** above a long communal table | Four hands shoot in at once to four phones |
| 3 | 2.5–4.0 | Same overhead, second buzz | Same four hands again, faster; one knocks over a sugar pot |
| 4 | 4.0–6.0 | **Locked tripod, medium**, 50 mm | Her: three-quarter back, reading a paperback; her phone face-down, still |
| 5 | 6.0–8.5 | **Locked tripod, wider**, from the counter | The waiter pauses with a tray, frowns at the still phone, sets the tray down |
| 6 | 8.5–10.5 | **Tripod, medium on the waiter** (profile, mouth hidden by the phone) | He taps the phone twice, turns it, then raises it to his ear like a seashell. Hold |
| 7 | 10.5–12.5 | **Proof slot: real screen capture** as a floating card | The client's real focus-session screen (e.g. "Session: [x] min left") |
| 8 | 12.5–15.0 | Same medium on her | She turns a page without looking up. Logo + offer slot |

- **Physics check:** a phone's vibration motor runs ~150–250 Hz; on hard marble a buzz walks a phone ~1–3 mm, never centimetres [inf]; face-down phones don't light the table; the reaching hands each go to *their own* phone (four phones, four owners, never swap); the sugar pot tips and stays tipped; the paperback's page turns once, right to left.
- **Audio map:** 0.0 double buzz (on wood/marble, gritty), 1.2 second wave of buzzes (stereo), 1.3 four simultaneous grabs (cloth + skin swipes), 2.5 third buzz wave, 2.9 sugar pot clatter; 4.0 café ambience drops −6 dB around her (perspective); 6.0 tray set down; 8.6 two knuckle-taps on glass; 9.6 a faint "ocean" whoosh as he holds it to his ear (the gag, diegetic room tone through a cupped hand); 12.6 page turn; 12.8 VO: `Everyone's phone is talking.` [pause] `Hers is LULL'd.` (or a client tagline).
- **Model / template:** shots 2–6, 8 = **Seedance 2.5 r2v 10 s** "EXACTLY SIX SHOTS AND FIVE HARD CUTS" on one café plate; shot 1 **Kling 3.0 Pro i2v** from a real photo of a generic phone on marble; shot 7 real capture.
- **Cost:** $15.92 + $0.95 + previs $0.75 + stills $2.40 + VO $0.10 = **≈ $20**.
- **Claim check:** no screen-time statistics on screen except the client's own; no "cures addiction" language; the waiter is comedy, not a user testimonial.

### C4 · RELIEF (texture UV printer, Kickstarter) — "Guess Who" (15 s)

- **Idea:** Game night. A blindfolded man runs his fingers over a raised print to guess what it is: "a mountain… a nose… a big nose." He pulls off the blindfold: it's a relief portrait of *him*. His friends' silence; his slow nod.
- **Hook:** fingertips already moving across a ridged surface in macro + a held breath.
- **Punchline (product-caused):** only a texture printer can make a picture you recognise by touch — even when it's an unflattering one.
- **Built on:** A02 eufyMake ("felt, not just seen", the $46.76M campaign's whole idea).

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Proof slot: real macro** of fingertips over a real relief print (client's) | Ridges up to the client's real height |
| 2 | 1.5–3.5 | **Locked tripod, living-room wide** | Blindfolded man at the table, three friends from behind |
| 3 | 3.5–5.5 | **Overhead C-stand** | His hands map the print; the print is face-down to camera (we can't see it) |
| 4 | 5.5–7.5 | Tripod medium (blindfold covers eyes, his mouth turned away) | VO-style guesses (no lip-sync) |
| 5 | 7.5–9.5 | **Over-the-shoulder tripod** | He lifts the blindfold; we see the print: his own face in relief (from a real print of a stand-in, or a client sample) |
| 6 | 9.5–12.0 | Locked wide | Friends frozen; he nods slowly, sets it on the mantel |
| 7 | 12.0–15.0 | Packshot (real photo) | Logo + "Back RELIEF on Kickstarter" |

- **Physics:** relief height only as the client states (e.g. "up to 5 mm" is eufyMake's figure — not ours); fingertips glide with light pressure, skin creases at the ridges; a print on slate/wood is rigid and doesn't flex. **Audio:** 0.0 fingertip rasp on texture; 4.0 three guesses as VO ("Mountain… nose… a big nose"); 7.6 blindfold rustle; 8.0 two-second silence; 10.2 frame set on the mantel; 12.0 VO tagline. **Model:** Seedance 2.5 r2v 8 s (shots 2–6, faces kept back/covered) + real proof shots. **Cost ≈ $16.** **Claim check:** the portrait print shown is a real print; the machine is never shown printing in AI.

### C5 · CARRYWELL (crowdfunded carry-on) — "Bin Etiquette" (15 s)

- **Idea:** Boarding. A passenger fights a bulging bag into an overhead bin; it springs back. Our hero slides CARRYWELL in wheels-first, closes the bin with room to spare; the flight attendant quietly places her sandwich in the leftover gap.
- **Hook:** a bin lid slamming and bouncing open (sound + motion at 0.0).
- **Punchline (product-caused):** the bag's real dimensions leave a sandwich-sized gap.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | **Locked tripod at aisle end**, 24 mm, mock-up cabin set | Bin lid slams on a bulging bag and bounces open |
| 2 | 1.5–3.5 | Same | Passenger shoves again; a jacket sleeve hangs out |
| 3 | 3.5–6.0 | **Proof slot: real footage** of CARRYWELL sliding wheels-first into a real bin (client's test) | — |
| 4 | 6.0–8.0 | **Tripod, under-bin low angle** | The lid closes with a clean click; visible gap |
| 5 | 8.0–11.0 | Medium, attendant ¾ back | She pauses, places a wrapped sandwich in the gap, closes the lid |
| 6 | 11.0–15.0 | Locked wide | Hero sits; the other passenger is still shoving. Logo + offer slot |

- **Physics:** US airline carry-on limit commonly 22 × 14 × 9 in (56 × 36 × 23 cm) [unverified per airline]; a typical narrow-body bin takes a carry-on wheels-first in depth; the bag is rigid-sided; the lid latches with a ~2 cm travel. **Audio:** 0.0 lid slam, 0.3 bounce; 2.0 grunt (off-screen), 6.4 clean latch click, 8.6 paper rustle, 11.0 cabin ambience + VO. **Model:** Seedance 2.5 r2v 10 s on one cabin plate (no airline branding, fictional livery); real proof. **Cost ≈ $20.** **Claim check:** "fits [airline] bins" only per the client's tested list.

### C6 · MEMOCLIP (AI note-taking pin) — "The Napkin" (15 s)

- **Idea:** A founder sketches the big idea on a napkin at a diner. A waiter clears the table — napkin gone into a bus tub. Panic. Then calm: she taps the pin on her collar; a floating summary card appears beside her (real UI). The waiter comes back… to wipe his hands on the napkin.
- **Hook:** pen nib scratching on a napkin, already mid-sketch.
- **Punchline (product-caused):** the idea survived because the pin captured it.
- **Consent detail (legal and on-brand):** the opening line is said aloud: "OK, MemoClip, we're recording" and the pin's LED is visibly on — several US states require all-party consent to record conversations [unverified per state]; Pocket's film opens with "I consent" (A01).

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Overhead C-stand, macro | Pen sketching boxes and arrows on a napkin |
| 2 | 1.5–3.0 | Tripod medium, ¾ back | She taps the pin; LED on; "we're recording" as VO |
| 3 | 3.0–5.0 | Tripod wide, diner | Waiter sweeps plates and the napkin into a tub |
| 4 | 5.0–6.5 | Tripod medium | Her hand freezes mid-air (no face) |
| 5 | 6.5–9.5 | **Proof slot: real UI** as a floating card beside her (client's summary screen) | — |
| 6 | 9.5–12.0 | Tripod wide | Waiter returns, wipes his hands on the napkin, drops it again |
| 7 | 12.0–15.0 | Kling i2v macro of the pin on the collar → logo + offer slot |

- **Physics:** a 20–30 g clip pin tugs a collar a few mm; the LED is the only light on the device; napkin paper absorbs ink — lines bleed slightly. **Audio:** 0.0 nib scratch; 1.6 pin tap; 3.2 plates into tub; 5.2 silence; 6.5 soft brand chime; 10.0 napkin crumple; 12.0 VO. **Model:** Seedance 2.5 r2v 10 s + Kling i2v pin macro + real UI. **Cost ≈ $20.** **Claim check:** summary accuracy only as shown in the real capture; no "never miss a word" unless substantiated.

### C7 · HIDEBOUND (leather MagSafe wallet) — "Day 1 / Day 365" (6 s loop + 15 s)

- **Idea:** Nomad's 7-variant loop (A12) made cinematic: one locked macro of the wallet on a desk as a year passes in light (morning → dusk → winter → spring); the leather darkens to a patina; the phone it's attached to changes three times (generic phones of different shapes). Super: "Outlives your phone."
- **Hook:** a hand sets the wallet down with a magnetic *snap* at 0.0.
- **Punchline (product-caused):** the accessory outlasts the device it accessorises.
- Shots (6): snap macro (Kling i2v, real photo) · locked macro light-change one-take (Cinema Studio single-shot) · **proof slot: client's real Day 1 vs Day 365 photos** · phone swaps (three Kling i2v inserts) · hand lifts the wallet, patina in raking light · logo. **Physics:** vegetable-tanned leather darkens gradually with light and handling (no sudden jumps); the MagSafe-style snap is a ~1 cm pull-in with a click; shadows rotate with the seasons consistently. **Audio:** 0.0 snap; 0.5–4.5 room tone shifting (birds, rain, heater) per season; 4.6 snap again (loop point). **Cost ≈ $10** (Cinema Studio $5.36 + 4 × Kling $0.95/2 takes ≈ $3.80 + stills). **Claim check:** patina = real photos; "outlives your phone" is puffery tied to a real warranty term if used.

### C8 · DUSKWISE (sleep-timing app) — "Rooster" (15 s)

- **Idea:** A farmhouse at 5:55 a.m. The rooster on the fence crows at the bedroom window — the bed is already empty. Cut to the kitchen: the farmer, rested, coffee poured, looks out at the rooster with mild pity. The rooster, mid-crow, stops.
- **Hook:** the crow (sound) over a static frame of the rooster already puffing up.
- **Punchline (product-caused):** the app woke him in light sleep before the rooster could (only if the client's app has a smart-alarm/wake-window feature).
- Shots (7): rooster wide, locked tripod (**one animal, ≤5 s, Kling i2v from a real rooster photo** — LESSONS) · bedroom wide, empty bed, tripod · kitchen medium, farmer ¾ back pouring coffee · **proof slot: real UI** of the wake-window screen · window POV from inside (tripod behind glass, camera stays inside) · rooster stops mid-crow · logo + "Take the 1-minute sleep quiz" (Rise's CTA pattern, A07). **Physics:** civil dawn light, low warm sun; coffee steam visible at ~20 °C room temp; the rooster's comb and wattles bob with the crow. **Audio:** 0.0 crow (2 s); 2.2 empty-room tone; 4.0 coffee pour; 7.0 UI chime (brand); 9.5 the crow cut short (a strangled half-note); 12.0 VO. **Cost ≈ $19.** **Claim check:** no "sleep better" outcome claim without the client's study.

### C9 · KITE (mystery desk gadget, pre-launch) — "But Will It…?" (3 × 8 s teasers)

- **Idea:** Nothing's teaser grammar (A16: 324K views, 10 % likes): three 8 s CG macro reveals of fragments of an unannounced product, each captioned with an absurd question ("But will it hum?", "…tilt?", "…wait for you?"), revealed whole on launch day.
- **Hook:** an extreme macro of a coloured surface sliding past the lens.
- **Punchline:** the question — answered only at launch.
- Shots: one continuous **CG-style** pull-back per teaser (Cinema Studio 4.0 `pacing:"single-shot"`, `dolly-out`), built from the client's CAD renders as stylised (not photoreal-in-use) frames; super "Concept render" small; launch-day reveal uses real prototype footage. **Physics:** rigid surfaces, slow constant dolly (0.1 m/s), one key light. **Audio:** a low mechanical hum + a single click at 7.5 s. **Cost:** 3 × $5.36 + stills ≈ **$18**. **Claim check:** nothing about function; Kickstarter-safe because no photoreal product-in-use and it runs off-platform as a teaser [inf]; still disclose AI/CG on the campaign page.

### C10 · VXO spec · MEMOCLIP — "Director's Notes" (15 s) — Otto & Vee

- **Idea:** Vee clips a MEMOCLIP pin on Otto's lapel before a shoot: "Give me your notes." Vee starts her one silver stopwatch. Otto stares at the monitor, utterly still, moustache unmoving, for twelve seconds. Vee stops the watch. The floating summary card reads: "Summary: —. Action items: none." Vee nods: "Same as always."
- **Hook:** Vee's stopwatch click at 0.0 and a tight shot of the pin's LED coming on.
- **Punchline (product-caused):** the pin faithfully transcribes Otto's silence.
- Shots (7): stopwatch macro click (Kling i2v from the Vee reference; **exactly one stopwatch**) · Vee clips the pin (hands only) · Otto medium, side-lit, **mouth never visible**, stillness · monitor glow on his face (unreadable) · stopwatch at 12 s (hands) · floating summary card (brand-styled, VXO's own spec — clearly fiction) · Vee walks off; VO tagline. **Physics:** a 12 s hold must contain micro-motion (breathing, a blink) — no frozen frames (doc 46 freeze check); one stopwatch in every frame. **Audio:** 0.0 click; 1.0 LED blip; 2.0–14.0 studio room tone, distant crew murmur; 14.0 second click; Vee's line as VO with her mouth off-screen; Otto silent. **Model:** Seedance 2.5 r2v 10 s with Otto/Vee sheets + Kling inserts. **Cost ≈ $21.** **Why:** shows a buyer in this niche that VXO's mascots can sell a *software* feature with zero real UI risk.

### 8.1 Ranking

| Rank | Concept | Why |
|---|---|---|
| ★ 1 (single best) | **C1 BENDWELL "Night Shift"** | Proof built from the client's own rig; durability punchline caused by the product; no faces/UI; one locked plate; Kickstarter-compliant by construction; re-skins across campaign phases and durability products |
| ★ 2 | **C2 TALLYHO "Receipt"** | Brex-grade B2B pain frame + real chase grammar + a product-caused reversal; a 2 s real UI proof; fits every receipt/expense/scan app |
| ★ 3 | **C3 LULL "Is It Dead?"** | Sound-first, rule-of-three, deadpan; the product's effect (silence) is the joke; the January-campaign film for focus apps |
| 4 | C10 "Director's Notes" | The best VXO spec for software buyers (mascots + a feature) |
| 5 | C7 HIDEBOUND "Day 1 / Day 365" | Cheapest; a proven 7-variant format made cinematic |
| 6–10 | C4, C6, C8, C5, C9 | Good; more people, more claims or an animal → more risk |

---

## 9. Ten insights nobody asked for (that would make VXO's films and outreach sell better)

1. **The UI card is the house solution to this niche's biggest AI trap.** Pocket shows its UI as floating translucent cards beside the actor (A01); Monogram shows a real capture in a clean floating phone on a coloured seamless (A20); Monzo uses one floating bubble (A05). None renders UI on a generated device. Make a **VXO UI-card template** (tracked card, brand colours, real capture inside) a standard post step for every app/SaaS film — it removes the garbled-text risk, satisfies Meta's non-existent-functionality rule, and looks premium.
2. **"Kickstarter-compliant by construction" is a sales line, not a footnote.** Kickstarter requires working prototypes and bans photorealistic renderings; it requires an AI-use disclosure. Hardware founders fear suspension and backer revolt more than a weak film. A VXO film where the product's function is *only* real prototype footage, plus a scene-by-scene "Use of AI" note, answers fear #2 before it is spoken — say it in the first reply.
3. **A crowdfunding campaign is a ready-made Season plan.** Pre-launch hooks (6–10 weeks), launch day, mid-campaign slump, final 48 hours, late pledges/InDemand, then the Shopify/Amazon launch: six or more short films on one skeleton (C1 re-skins for each). Pitch the *calendar*, priced as the Season, not one Premiere.
4. **Sell January in October.** Install-to-paid runs 39.4 % in mid-January vs 30.5 % in October and trials spike on New Year's Day (Adapty). Health, sleep, focus, language and finance apps need their January film briefed by early December — so outreach to them belongs in October–November, with "your January film" as the offer.
5. **Filter on payer economics, not on "launched an app".** Year-1 revenue per payer is ~$23 (global) to $32 (North America); a $2,500 film needs ~80–110 extra payers to pay back. That is easy above ~$1M ARR or ~1,000 ratings and impossible for the median new app ($168 MRR). The lead add-on (§7) encodes this; skip hobby apps even when they are enthusiastic.
6. **This niche hooks with a sentence.** 35 of 55 measured ads speak in the first second (median 2.5 words/s) — a question, a confession, a challenge. VXO's sensory openers (motion + sound) need a **written or spoken line in 0–1 s** here as well: put a one-line super on frame 0 and the VO on the first beat.
7. **AI tolerance is category-specific — ask before you pitch.** AI apps and creative tools run all-AI or AI-hook ads happily (Artlist A19, Rise A07); "digital wellbeing" and "human connection" products are where AI backlash lives (Duolingo's AI-first wave; Friend as the backlash symbol). For those, pitch the **real-world consequence film with no AI people** (C3 style) and say so.
8. **Test rigs are the most-shared hardware content and the safest AI film.** Nothing's USB rig: 9.1M views, **149K shares** for 30 s of a machine (A03). Machines have no faces, no lips, no UI. Build a spec **rig library** (bend, drop, press, water, hinge, zip) where the client's real rig footage is the proof and VXO builds the world, the human beat and the punchline around it (C1).
9. **Audio is broken across the niche — a friendly, concrete DM opener.** 15 of 55 measured ads clip above 0 dBFS (Cluely −7.7 LUFS / +2.1) and 15 sit below −20 LUFS; Orbitkey's whole gag is a key-jangle mixed at **−37 LUFS** (A17) — the hook is inaudible. One line in a DM ("your jangle gag is great; it's mixed 23 dB under the feed — want a version where the first second lands?") shows craft without criticising their idea.
10. **One film, two founder moments.** Founder launch films on X reach 1.4M views when they show a job-to-be-done in the real world plus one proof line ("160,000 devices shipped", A01). A VXO 15 s film can be the **cold open of the founder's own X launch film** and, cut to 3 s, the hook head on their creator ads (Cal AI's 250-influencer model) — the same deliverable, used where this buyer already spends attention.

---

## 10. QA gate additions for this niche

Add to doc 44 §10 and doc 46 §7:

- [ ] **No generated readable text or UI** in any frame (phone, laptop, monitor, watch, glasses); screens show a soft unreadable glow only.
- [ ] Every UI moment is the client's real capture or a brand-styled card; the composite is tracked (≤1 px drift at 1080p), lit to match, and the thumb occludes correctly.
- [ ] **No fake system chrome** (iOS/Android notifications, Install buttons, Meta UI); store badges are Apple/Google artwork with correct clear space.
- [ ] **Generic phone** identical across shots (shape, camera module, colour); no Apple logo or iPhone trade dress.
- [ ] Product = real prototype: button count, LED colour, finish, logo position match the reference in every crop (`continuity_check.py` on product crops ≥0.6 mean similarity).
- [ ] The product's *function* appears only in the proof slot (real footage); any CG/concept frame is labelled.
- [ ] Hands: exactly five fingers, the device rests on the little finger, the thumb never passes through the screen; wearables stay in the same position.
- [ ] Recording devices: a visible consent beat or indicator light where people are recorded.
- [ ] Hook: motion **and** a line (super or VO) in 0–1 s.
- [ ] Offer slot present with the client's exact terms (trial renewal line; "Reserve for $1 — refundable" as on their page).
- [ ] Deliverables: 9:16, 1:1, 16:9 masters; 6 s loop; optional App Store–safe cut built only from real capture.
- [ ] Kickstarter/Indiegogo clients: scene-by-scene "Use of AI" note delivered.
- [ ] Loudness −14 LUFS integrated, true peak ≤ −1.0 dBTP measured on the encoded file (doc 46).

---

## Sources

**Measured files** (not committed): `scratchpad/niche2/apps/vids/` (M01–M40, T01–T16, X01–X02), analysis in `…/apps/an/` (stats JSON, 2 fps head tiles, whole-film tiles, transcripts); Motion page parses in `…/apps/motion.json` and `motion2.json`; TikTok metadata in `…/apps/tt/meta_all.tsv`.

**Meta ads via Motion public pages** (`https://motionapp.com/library/<slug>`): timeleft (M01–M02), slack (M03), lovable-dev (M04–M05), headway (M06, M25), brex (M07), rise-science (M08–M09), liven-improving-wellbeing (M10), character-ai (M11), ai-cleaner-clean-up-storage (M12–M13), opal-1-screen-time-app (M14), monzo (M15), noom (M16), impulse-brain-training (M17), speechify (M18), artlist-io (M19), wealthsimple (M20), duolingo (M21), finch (M22, M26, M28), fyxer (M23, M27, M29), kalshi-trade-the-headlines (M24), skylight (M30–M33), nomad (M34–M35), polarpro (M36–M37), anker (M38–M39), peak-design (M40). Brand statistics from 148 brand pages (list in `…/apps/brands.txt` and `motion2/`).

**TikTok posts** (`https://www.tiktok.com/@<handle>/video/<id>`): nothing 7546600788949404951, 7686380217882955041, 7535039052710710551; eufymake 7626544804754754829, 7505127202837744942; flipperzero 7639442311914540309, 7636832220354809108; cluely 7691753289259437325; duolingo 7514320905909194030; opal 7574457767067553026; evenrealities 7694265373041986824; keychron 7672599052013423886; thelightphone 7486593460309445918; elevationlab 7530457962658155790; orbitkey 7613606994901011732; perplexity_ai 7557187103767956791.

**X launch videos:** [Pocket](https://x.com/AkshayNarisetti/status/2077439335130124544); [Monogram](https://x.com/erenbali/status/2074502671600672930).

**Market data:** Sensor Tower 2025 via [TechCrunch](https://techcrunch.com/2026/01/21/consumers-spent-more-on-mobile-apps-than-games-in-2025-driven-by-ai-app-adoption/), [PocketGamer.biz](https://www.pocketgamer.biz/global-mobile-in-app-purchase-revenue-hit-167bn-in-2025), [TechSpot](https://www.techspot.com/news/111010-global-app-spending-overtakes-mobile-games-first-time.html); RevenueCat State of Subscription Apps 2026 via [ppc.land (AI apps)](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/) and [ppc.land (middle class)](https://ppc.land/the-app-middle-class-is-dying-and-revenuecats-data-shows-exactly-how-fast/) ([report](https://www.revenuecat.com/state-of-subscription-apps)); AppsFlyer via [RocketShip HQ](https://www.rocketshiphq.com/appsflyer-state-of-app-marketing-2025-summary/) and [Performance Index](https://www.appsflyer.com/resources/performance-index/); [Adapty holidays 2026](https://adapty.io/blog/state-of-holidays-for-subscription-apps/); [Gartner cloud forecast](https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025); [BigIdeasDB indie SaaS](https://bigideasdb.com/state-of-indie-saas-revenue-2026); [Kickstarter 2025 review](https://updates.kickstarter.com/a-year-in-review-2025-kickstarter-highlights/); [Kickstarter stats](https://www.kickstarter.com/help/stats); [Wikipedia: Kickstarter](https://en.wikipedia.org/wiki/Kickstarter); eufyMake E1 ([Wide Format Impressions](https://www.wideformatimpressions.com/article/eufymake-raises-47-8-million-for-3d-texture-uv-printer-kickstarter/)); Snapmaker U1 ([All3DP](https://all3dp.com/4/why-20000-people-just-pledged-20m-for-the-snapmaker-u1-3d-printer/)); [TCF most funded](https://www.tcf.team/blog/most-funded-kickstarter); [Kicktraq: Halliday](https://www.kicktraq.com/projects/halliday-ai-glasses/halliday-proactive-ai-glasses-with-invisible-display/) and category pages; [hunted.space PH pulse](https://www.hunted.space/product-hunt-pulse); [Databox on PH](https://www.producthunt.com/p/databox/best-day-to-launch-on-product-hunt-here-s-what-4-962-launches-in-2026-actually-show-2); [Awesomic launch-video report](https://www.awesomic.com/launch-video-report); [a16z speedrun on launch videos](https://speedrun.substack.com/p/how-to-make-a-viral-launch-video); [Flowjam examples](https://www.flowjam.com/blog/founder-led-launch-video-examples-2026) and [pricing](https://www.flowjam.com/blog/how-much-does-a-startup-launch-video-cost-2026) [v]; [StartMotion Kickstarter video pricing](https://www.startmotionmedia.com/how-much-should-i-pay-for-kickstarter-video-production) [v]; [Stephen Follows crowdfunding data](https://stephenfollows.com/film-crowdfunding-tips/); LaunchBoom cases ([Hooke Lav](https://launchboom.com/blog/how-we-raised-589845-for-hooke-lav-case-study), [XION](https://launchboom.com/case-studies/xion-cyberx-case-study), [Creed's Codex](https://launchboom.com/blog/how-brendan-from-creeds-codex-raised-52277-on-kickstarter-case-study)) [v]; [PledgeBox ads playbook](https://pledgebox.com/post/crowdfunding-facebook-ads) [v]; [ComixTribe on pre-launch](https://comixtribe.substack.com/p/going-all-in-on-pre-launch).

**Companies:** [Speedinvest on Opal](https://speedinvest.com/blog/scaling-smart-how-opal-built-a-10m-arr-business-in-just-2-years); [Fortune on Cal AI](https://dc.fortune.com/2025/09/27/gen-z-founder-treats-college-like-vacation-30-million-app-by-18); [Latka Cal AI](https://getlatka.com/interviews/cal-ai-zach-yadegari-2025); [Fyxer press](https://www.fyxer.com/press); [TechCrunch on Pocket](https://techcrunch.com/?p=3136998); [xyz.pl on Pocket](https://xyz.pl/poland-unpacked/polish-founded-ai-device-pocket-raises-usd-11m-as-it-scales-in-the-us-1892/); [Daylight (Wikipedia)](https://en.wikipedia.org/wiki/Daylight_Computer_Co.), [Caplight](https://www.caplight.com/company/daylightcomputer); [Light Phone (TechCrunch 2019)](https://techcrunch.com/2019/09/04/light-phones-founders-discuss-life-beyond-the-smartphone); [Sacra on Plaud](https://sacra.com/research/250m-year-granola-for-plumbers); Friend ([Digg](https://digg.com/tech/26a55vyb), [AOL](https://www.aol.com/startup-went-viral-odd-personal-225738684.html), [CNN via KVIA](https://kvia.com/news/business-technology/cnn-business-consumer/2025/11/16/how-this-tiny-device-became-a-symbol-for-the-backlash-against-ai/)); Cluely ([Business Today](https://businesstoday.in/amp/technology/news/story/ai-startup-cluely-raises-53-million-to-let-users-cheat-on-everything-even-job-interviews-and-exams-472946-2025-04-22)); Duolingo backlash ([Slashdot/Fast Company](https://tech.slashdot.org/story/25/05/25/0347239/), [PR Daily](https://www.prdaily.com/?p=347594)); Even G2 ([TechCrunch](https://techcrunch.com/?p=3140951)).

**Rules and law (fetched):** [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) (2.3.3, 2.3.4, 2.3.7, 2.3.10, 5.2.1); [Kickstarter hardware rules](https://help.kickstarter.com/en-us/articles/16236428-what-are-the-rules-for-hardware-and-product-design-projects); [Kickstarter Meta-ads lesson](https://updates.kickstarter.com/launchboom-lessons/creating-your-meta-ads/). **Via search summaries / press (not fetched as primary):** Apple [Marketing Guidelines](https://developer.apple.com/app-store/marketing/guidelines/); Meta [non-existent functionality](https://transparency.meta.com/policies/ad-standards/deceptive-content/non-existent-functionality/) (404 on fetch); [TikTok misleading and false content](https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content); [Google Play store-listing best practice](https://support.google.com/googleplay/android-developer/answer/13393723?hl=en); Kickstarter AI policy ([TechCrunch](https://techcrunch.com/2023/08/01/kickstarter-requires-generative-ai-projects-to-disclose-additional-info/amp/), [Engadget](https://www.engadget.com/kickstarter-projects-will-soon-have-to-disclose-any-ai-use-145100394.html)); Kickstarter rule history ([Engadget 2012](https://www.engadget.com/2012-09-21-kickstarter-clampdown.html), [bit-tech 2014](https://bit-tech.net/news/kickstarter-renders/1/), [NoFilmSchool 2014](https://nofilmschool.com/2014/06/kickstarter-launch-now-rule-changes)); Indiegogo ([terms](https://indiegogo.com/about/terms), [trust](https://learn.indiegogo.com/trust), [Engadget 2016](https://www.engadget.com/2016-12-08-indiegogo-terms-of-use-update.html)); FTC crowdfunding ([FTC](https://www.ftc.gov/node/47254), [Mediaite](https://www.mediaite.com/online/first-ftc-case-against-deceptive-crowdfunding-ends-in-settlement/)); Operation AI Comply ([Orrick](https://www.orrick.com/en/Insights/2024/10/FTC-Targets-Unfair-or-Deceptive-AI-Practices-With-Five-New-Enforcement-Actions)); click-to-cancel vacatur and ROSCA ([Cooley](https://www.cooley.com/news/insight/2025/2025-07-11-click-to-cancel-just-got-cancelled-eighth-circuit-vacates-entirety-of-ftcs-negative-option-rule), [Womble Bond Dickinson](https://www.womblebonddickinson.com/us/insights/alerts/ftcs-click-cancel-rule-vacated-remember-it-was-not-alone)); [FTC Mail, Internet, or Telephone Order Merchandise Rule](https://www.ftc.gov/legal-library/browse/rules/mail-internet-or-telephone-order-merchandise-rule). **[unverified]:** SEC Reg CF Rule 204 tombstone limits; state all-party-consent recording laws; COPPA scope; FTC Health Products Compliance Guidance; airline carry-on dimensions.

**Internal:** docs 41, 42 (#9–10 Kalshi, Lindy), 43 (§1, §2.1, §5, §6, §7), 44 (§10), 45 (§1, §5), 46 (§7), 51, 60; `research/ai-video-reels/lab/LESSONS.md`; `.claude/skills/vxo-leads/SKILL.md`.
