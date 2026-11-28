# 36 · Emotion, punchline and virality: what sells, what spreads, what gets clicked

Research brief, 2026-10-08. The founder asked for ads with "emotion and punchline so it sells, gets clicks, and trends". This file checks that goal against published evidence, then turns it into two tools: a **scorecard** we run on every script before spending money (§4), and a **30-day Instagram plan** for VXO's own account built on Otto and Vee (§5).

Rules for this file: every number has a source next to it. Vendor and self-reported data are labelled. `[inf]` marks our own inference. Where we looked and found nothing, we say so; we do not fill the gap with a guess. Findings already in `01`, `15`, `23` and `30` are cross-referenced rather than repeated.

---

## 0. Method and limits

| Source type | What we did | Status |
|---|---|---|
| Web search + primary pages | IPA, System1, Kantar, Zappi, TikTok, Meta (secondary), academic papers, earnings coverage | Done. Primary pages read where reachable (System1 *Look out* summary PDF, Kantar humour article, System1 characters blog, System1×TikTok coverage, Motion humour report coverage) |
| YouTube transcripts | 8 queries (Duolingo social team, Mosseri on ranking, looping reels, Ryanair, AI influencer growth, humour DTC ads, Orlando Wood talk, hook-rate) with 10 s spacing | **Blocked.** The first transcript request returned HTTP 429, so we stopped as instructed. Nothing in this file depends on a transcript |
| Ipsos "Short-Form Social Misfits" | Both Ipsos pages fetched | They contain no numbers on emotion or humour. The quantified Ipsos points we use come from `23` §1 |
| Kantar humour, 2024–26 | Searched | The latest Kantar humour analysis we could read is from 2023 |
| A published, controlled **punchline vs beauty ad** CTR/CPA comparison | Searched several ways | **Not found.** §3.4 explains what exists instead and how we test it ourselves |

---

## 1. Emotion and sales: what the evidence says

### 1.1 The big studies (most robust first)

| Finding | Sample | Source | Strength |
|---|---|---|---|
| Emotional campaigns produce more brand and business effects than rational ones, and over the long term are **almost twice as likely to deliver top-box profit growth**. Optimum budget split is about 60:40 brand:activation, which Binet & Field call a principle rather than a rule | 996 IPA campaigns, 700+ brands, 83 categories, 30 years | Binet & Field, *The Long and the Short of It* (IPA 2013), via [Murrell summary](https://www.alexmurrell.co.uk/summaries/les-binet-and-peter-field-the-long-and-the-short-of-it); caveats in [Ritson](https://marketingscience.info/mark-ritson-binet-and-fields-research-may-not-be-perfect-but-that-doesnt-make-it-wrong) | Strong for long-term brand effects. It is TV-era data and says little about a 30 s Reel's CPA |
| Ads in the **top 25 % on overall emotion are, on average, about twice as likely to drive immediate sales** (trade write-ups say "nearly twice") | 4,000+ ads, 1.6M+ US consumer responses (Zappi Amplify) | Zappi × VaynerMedia, *2025 State of Creative Effectiveness* ([AgileBrand](https://agilebrandguide.com/zappi-and-vaynermedia-unveil-2025-state-of-creative-effectiveness-report-benchmarking-the-real-performance-of-advertising-today/), [MarTech Series](https://martechseries.com/sales-marketing/programmatic-buying/zappi-and-vaynermedia-unveil-2025-state-of-creative-effectiveness-report-benchmarking-the-real-performance-of-advertising-today/)) | Medium-strong, and it is the most useful one for us because it covers **short-term** sales. It is vendor survey data validated against sales by Zappi, not by us |
| Ads with a high emotional response had **30 % greater sales impact** than low-response ads. Strong reactions, positive or negative, earned **16 % more attention** | 140+ consumers, 15 TV ads (Australia) | ThinkTV / Karen Nelson-Field ([Mumbrella](https://mumbrella.com.au/emotional-ads-will-lead-sales-study-suggests-487548), [AdNews](https://www.adnews.com.au/news/emotional-advertising-drives-greater-sales-thinktv-finds)) | Weak to medium (small sample) |
| Facial-coding emotion data correctly classified ads as low or high sales impact **75 % of the time** | 22,000+ viewers, 149 ads, 35 brands, 6 countries | Realeyes × Mars × Ehrenberg-Bass ([Research Live](https://www.research-live.com/article/news/emotion-measurement-predicts-sales-lift-with-75-accuracy/id/5020232)) | Medium. It shows emotion *predicts* sales; it does not show which emotion |
| Creatively awarded campaigns were about **12× more efficient** than non-awarded ones in 1996–2008, but only about **4×** in 2006–2018. Field blames short-termism and "disposable" ideas | ~600 IPA case studies | Peter Field, *The Crisis in Creative Effectiveness* (IPA 2019), via [Contagious](https://www.contagious.com/news-and-views/the-creative-awards-crisis-is-an-advertising-crisis) (single secondary source) | Medium. The lesson for us is that a one-off gag is weaker than a campaign idea that repeats `[inf]` |

**There is no reliable "Nielsen 23 %" figure.** We searched for it and found nothing behind it, so do not quote it. The same goes for unsourced "31 % vs 16 %" figures on blogs.

### 1.2 Which emotions: sales vs shares

**For sharing, arousal matters more than whether the emotion is positive.** Berger & Milkman, *What Makes Online Content Viral?* (Journal of Marketing Research, 2012), studied about 7,000 NYT articles ([Scientific American](https://www.scientificamerican.com/article/the-secret-to-online-success-what-makes-content-go-viral), [DOI 10.1509/jmr.10.0353](https://www.citedrive.com/en/discovery/what-makes-online-content-viral/)):
- Content that evokes **high-arousal** emotions was shared more. That includes positive ones (**awe**) and negative ones (**anger, anxiety**).
- **Low-arousal** emotions (**sadness**) were shared less.
- Positive content beat negative overall. Being **surprising, interesting or practically useful** also predicted sharing.
- In a lab follow-up, physically aroused subjects (jogging in place) shared more (via WSJ; treat the exact figure with care).

**For selling, humour is the emotion with the best effectiveness record**:
- **Kantar** ([2023 article](https://www.kantar.com/inspiration/advertising-media/starting-to-laugh-again-the-slow-return-of-humour-in-advertising)): 32 % of ads use humour, and digital use of humour has declined for five years.
  - Ads *intended* to be funny score above average on distinctiveness, emotional connection and engagement.
  - Ads that actually make people **laugh out loud** do better still: they are **more persuasive and better branded**, and they build equity. Kantar gives no percentages for this gap.
  - Kantar's own advice is to test whether the joke lands, because intent is not enough.
- **Motion** (DTC paid social; [Net Influencer, Feb 2025](https://netinfluencer.com/motion-report-dtc-brands-see-humor-ads-driving-higher-engagement)):
  - Humour is **25 % of DTC ads with more than $1M in spend**, but only **14 % of all social ad content**.
  - The report gives no ad count, coding definition or CPA. It shows over-representation among scaled ads, not causation.
- **System1** (*Look out* summary, [IPA PDF](https://ipa.co.uk/media/11169/system1_a-glimpse-of-look-out_november2021.pdf)): across roughly 2,200 US and UK ads, there is a "steady fall" in viewers saying they feel "amused".
- **System1** on Cannes winners ([Research Live](https://www.research-live.com/article/news/system1-analysis-finds-increased-humour-in-uk-and-us-cannes-lions-winners/id/5127523)): **75 %** of US/UK Cannes Film Lion winners used humour in 2024, up from 52 % in 2023.
- **Humour helps attention and liking more reliably than it helps credibility.** Eisend's meta-analysis is *A meta-analysis of humor in advertising*, JAMS 37(2), 2009, 38 papers ([Marketing Week](https://marketingweek.com/three-ways-humour-helps-brands-sell)). We could not read its effect-size table. The direction is commonly reported as positive for attention, ad liking and brand liking, and weaker or mixed for purchase intent and source credibility. **Treat this as unverified until the table is read.** `[inf]` For a DTC ad, the product proof has to carry credibility; the joke cannot.
- **Academic social-video data** (2,911 videos; [Nova](https://scholars.nova.edu/en/publications/humor-effectiveness-in-social-video-engagement/)): videos were received better when humour dominated than when it sat under the message. Humour may also reduce comments.

**Synthesis for VXO** `[inf]`:

| Goal | Lead emotion | Why |
|---|---|---|
| Sales (paid) | **Amusement** with a product-linked payoff, or **surprise/awe** at a product truth | Humour has the best effectiveness record (Kantar, Motion over-representation). Awe and surprise are high-arousal and premium-safe (Berger & Milkman) |
| Shares (organic) | **Amusement, awe, "that's so us" recognition** | High arousal, and a reason to send it to a specific person |
| Avoid | Sadness and mild "nice" (low arousal), outrage at real people (high arousal but against our brand and our ethics) | Berger & Milkman; brand safety |
| Nostalgia / warmth | Fine as *texture* inside a funny or beautiful film (System1 lists warmth and "references to the past" among right-brain features) | We found no 2024–26 short-form sales data that isolates nostalgia. Do not claim any |

### 1.3 Right-brain cues: what makes an ad feel alive (System1 / Orlando Wood)

From the *Look out* summary (System1/IPA, [PDF](https://ipa.co.uk/media/11169/system1_a-glimpse-of-look-out_november2021.pdf)), whose underlying data is 195 US TV ads (TVision + System1) and 43 IPA campaigns / 137 ads (2016–20):
- **Right-brain features** were the most effective at **capturing attention and eliciting emotion**. Campaigns skewed toward them were "far more likely" to produce **very large business effects**.
- The features named are:
  - human uniqueness, movement and connection
  - **character, incident and place**
  - **humour, music**
  - warmth and vividness of colour
  - characters relating to each other in a space (Levi's "Launderette" is the worked example)
- **Left-brain features** are associated with ads that "push people away" and are becoming more common. The summary names:
  - **close-up product shots**
  - **"the stare"** (facial frontality, a face looking dead into camera)

  More generally, it describes **fixity over movement**, **directness over the implicit** and **rhythm over music**.
- Caveat: reviewers note that it is "not so simple as left-brain bad". A product ad still needs the product `[inf]`.

**What this means for a 30 s single-take product film** `[inf]`:
- **Put the product inside a scene with a character and an incident.** A product isolated on a sweep with a slow push-in is the left-brain default, and it is exactly what AI makes easiest. That makes it our biggest risk.
- **Show implicit reactions between people**, such as Otto's deadpan look at Vee, instead of a VO that explains.
- **Use real music or a sonic cue** rather than a generic beat bed.
- **Avoid "the stare" talking-head.** Vee may address camera, but she should talk *to Otto* at least half the time.

### 1.4 Characters (fluent devices)
- **System1 × TikTok** (887 short-form ads, 92K viewers, 8 markets; [Chief Marketer](https://chiefmarketer.com/system1-tiktok-study-branding-elements-and-creator-led-content-improve-short-form-video-ads/)):
  - A **fluent character** (a mascot playing a role) gave a **+57 %** boost to brand-awareness lift.
  - A **sonic asset in the first 2 s** gave **+191 %**, and a **logo in context** +182 %. **Logo overlays reduced lift.**
  - Exceptional early branding meant **57 % more happiness** and 48 % less negative sentiment.
  - Creator-led ads got **39 % more attention**.
- **System1 on characters** ([blog](https://system1group.com/blog/creating-memorable-characters-in-advertising)): in 300+ IPA campaigns since 1992, those with a fluent device were "much more likely" to gain share and profit. The blog gives no percentages; `30` §0 cites a ~30 % figure from a second source. System1's rules:
  - appear early and often
  - give the character **agency and a story that evolves** (Kevin the Carrot gained a family and villains)
  - give it a name and use it everywhere
- **For VXO**: Otto and Vee are our fluent devices. They must appear in the first 2 s of every VXO post, and they must *do* something rather than present `[inf]`.

### 1.5 What kills effectiveness (evidence-backed)
1. **Low or no emotion** ("mild interest"). The emotion studies above all point the same way.
2. **Humour that is intended but does not land**: it beats no humour, but loses to real laughs (Kantar).
3. **Left-brain execution**: isolated close-ups, the stare, explaining VO, rhythm without music (Wood).
4. **Late or overlay-only branding**: logo overlays reduced lift; branding in context and a sonic cue in 2 s helped (System1×TikTok).
5. **Disposable one-offs** instead of a repeatable idea (Field 2019: the awarded-work advantage shrank as ideas became short-term).
6. **Near-duplicate variants**. Meta's Andromeda retrieval groups near-identical ads. Meta's April 2025 guidance names creative diversification as the main lever ([Jon Loomer quoting Meta](https://www.jonloomer.com/meta-andromeda/)). Ten colour swaps count as roughly one concept (agency reports; directional).

---

## 2. Virality and trend mechanics on Reels and TikTok (2025–26)

### 2.1 What the platform ranks on (Instagram)
- **Three signals.** Adam Mosseri named **watch time**, **likes per reach** and **sends per reach** (DM shares) as the key Reels signals in January 2025. We know this from secondary coverage; we did not find his original clip.
  - He has called sends per reach "one of the most important signals".
  - Likes matter more for reach among followers; **sends matter more for reach to non-followers** ([SEJ](https://searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/521389), [fanpage karma](https://www.fanpagekarma.com/insights/?p=9293)).
  - A "3–5×" weight for sends over likes circulates, but it is a third-party estimate, not a Mosseri figure.
- **Audio and completion.** Instagram's own ranking text lists the likelihood you will reshare a reel, **watch it all the way through**, like it, and **go to the audio page** ([quoted by Chartlex](https://www.chartlex.com/blog/marketing/trending-audio-instagram-reels-algorithm-2026)).
- **Replays count as views.** Insights splits initial plays from **replays**, and a view is any start or replay ([SocialCrawl, 425 posts](https://www.socialcrawl.dev/blog/how-instagram-counts-views)). `[inf]` A loop that makes people watch twice raises views and watch time per viewer.
- **Original content is favoured.** Since 2022, reposted content is ranked down. Since 2024, aggregators that repost 10+ times in 30 days are removed from recommendations ([Gigazine 2024](https://www.gigazine.net/gsc_news/en/20240502-instagram-updated-algorithm-prioritizes-original-content)).
- **Trial Reels** (launched late 2024; widely reported, but we did not fetch Instagram's announcement) show a reel to non-followers first. That is our free hook-testing lab (§5).
- **Mosseri's year-end post (Jan 2026)** ([TechRadar](https://www.techradar.com/ai-platforms-assistants/ai-slop-won-in-2025-fingerprinting-real-content-might-be-the-answer-in-2026), [BetaNews](https://betanews.com/2026/01/01/adam-mosseri-suggests-highlighting-real-media-rather-than-ai-content-on-social-media/)):
  - "authenticity is becoming infinitely reproducible"
  - people will pay more attention to *who* is posting and why
  - platforms should label AI and give context about accounts

  `[inf]` For an AI studio, that is an argument for being **loudly and charmingly AI**, with two named, consistent characters and a visible human founder behind them, rather than passing as real.

### 2.2 The hook and the 3-second hold
- **Message early.** TikTok: "over **63 %** of all videos with the highest CTR highlight their key message or product within the first 3 seconds" ([TikTok Auction Ads Creative Tips PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf)). This is a correlation, with no date or sample given.
- **Hook-rate benchmarks** (3 s plays ÷ impressions, Meta) disagree with each other:

  | Source | Median / average | Other figures |
  |---|---|---|
  | [Benly 2026](https://benly.ai/learn/ad-creative/ad-creative-benchmarks-2026) | **28 %** all placements | Instagram Reels 31 %; top quartile 37 %, bottom quartile 18 % |
  | Billo via [Novoads](https://novoads.ai/blog/video-ad-benchmarks-2026) | **25.4 %** average (H1 2026) | — |

  Practitioners call **30 %+ good** and **under 20 % a first-frame problem** ([admakeai](https://admakeai.com/blog/hook-rate)). Use your own trailing average once you have one.
- **Meta CTR on video sales ads:** about **1.56 %** in H2 2025 across 80K+ ads (Billo, [summary](https://billo.app/blog/what-is-a-good-ctr/)). That is vendor data.
- **Hook types that survive on Meta** (Benly Q1 2026, in `23` §1.1): **visual intrigue** and **bold statement** lead in every vertical we sell to. A visual-intrigue first frame suits a single-take AI film `[inf]`.

### 2.3 Rewatch loops
- **Mechanism.** Replays count as views, and watch time is a top signal (§2.1). A seamless loop also stops the "ending" cue that makes people scroll `[inf]`.
- **Patterns that work** `[inf]`, drawn from `16` (seamless flow) and `30` §3.4 (loops):
  1. The last frame matches the first frame's composition, so the cut is invisible.
  2. The first line of dialogue completes the last one (Vee: "…ship it." → loops to Otto: "One more take.").
  3. A detail is planted that you only see on the second watch: a hidden label, or Otto's moustache moving the "wrong" way.
- **Caution.** Loops inflate views, not sends. Judge loops on **sends/reach** and **saves**, not plays `[inf]`.

### 2.4 Shareability: "send this to someone"
- Sends drive reach to non-followers (§2.1). People send things that are **high-arousal** (Berger & Milkman) and that say something about **them or the person they send it to** `[inf]`.
- **For a B2B audience of DTC founders, the send targets are specific** `[inf]`:
  - a cofounder ("this is literally you on our last shoot")
  - a marketer ("we need this hook")
  - a creative agency friend
- Write every VXO post with a named send target in the script, e.g. "Send to the cofounder who wants one more reshoot".
- A light, honest send CTA is fine. A "send this or bad luck" style chain bait is not.

### 2.5 Comment bait (honest versions)
**What the data says.** Socialinsider-attributed data says Instagram shares per post rose 12 % year on year while public comments fell 16 % (secondary, [Outfame](https://www.outfame.com/blog/instagram-engagement-rate-statistics)). Comments are getting scarcer, and DMs and sends are where the action is `[inf]`.

**Honest comment prompts.** Each gives a real reason to answer:
- a **binary choice** ("Take 1 or take 2 — which would you ship?")
- a **guess** ("Real or AI? Answer before the reveal.")
- a **request** ("Comment your product and we'll storyboard one frame").

**Keyword-to-DM automation.** "Comment FRAME" triggers an automatic DM through ManyChat or similar. It turns comments into DMs, which is the conversion the founder wants. Only vendor claims exist on performance ([ManyChat](https://manychat.com/meet-marketingharry); InstantDM's calculator inputs are assumptions). There is **no independent comparison with link-in-bio**, so test it (§5.4).

### 2.6 Trending audio vs original sound
- **We found no controlled, large-sample comparison.** Claims such as "up to 3× reach from trending sounds" are vendor assertions without method ([IQHashtags](https://iqhashtags.com/trending-instagram-reels-audio-2026)).
- **What is solid:**
  - Instagram ranks on likelihood to visit the audio page (§2.1).
  - System1×TikTok found a **sonic asset in 2 s gave +191 %** brand-awareness lift.
- **Our rule** `[inf]`:
  - **Own a sound for the series**: Vee's stopwatch click plus a 2-note sting.
  - Put trending audio **under** it only when the trend's meaning fits the joke.
  - Paid ads always use licensed or original audio. Commercial accounts often cannot use the full trending library anyway, so check in-app before planning around a song.

### 2.7 The "is this AI?" curiosity
- **AI realism stops thumbs.** The AI "bunnies on a trampoline" clip (fake Ring-camera framing, July 2025) reached a reported **183M–200M+ TikTok views**, and a wave of "I fell for it" reaction posts followed ([404 Media](https://www.404media.co/ai-bunnies-on-trampoline-causing-crisis-of-confidence-on-tiktok/), [PetaPixel](https://petapixel.com/2025/07/31/people-are-falling-for-an-ai-video-of-bunnies-bouncing-on-a-trampoline), [Lead Stories](https://leadstories.com/hoax-alert/2025/07/fact-check-bunnies-trampoline-video.html)). The engagement came from **deception**, and the backlash was about **scams**. That is the opposite of a trust brand.
- **The honest version for VXO** `[inf]`: "Real or AI?" as a **game with a reveal**, always disclosed in the caption and on screen by the end. The joke is that Otto insists he is real.
- **How disclosure affects trust:**
  - **Experiments**: small controlled studies (n = 138, n = 125) found AI disclosure did **not** significantly lower purchase intent, brand trust or ad credibility for ordinary products ([UvA](https://dare.uva.nl/id/dc6a541b-3dac-4913-9f07-a6573b5764f0?page=391), [EUR thesis](https://thesis.eur.nl/pub/76583/)).
  - **Surveys**: a Harris Poll at Cannes 2026 found **73 %** say they would trust an ad *suspected* of being AI less, and 63 % would be less likely to buy from brands that lean heavily on AI ([FingerLakes1](https://www.fingerlakes1.com/2026/08/27/poll-finds-ai-labels-can-undercut-trust-in-advertising/)). That is stated attitude, not behaviour.

  `[inf]` The word that matters in the survey is *suspected*. Being caught is worse than saying so up front.
- **Rules (hard):**
  - The **FTC Consumer Reviews and Testimonials rule** has been in force since 2024-10-21. It bans reviews and testimonials that materially misrepresent that the reviewer exists or used the product. A virtual influencer is allowed only if it does not misrepresent its existence or experience ([Covington](https://www.insideprivacy.com/advertising-marketing/ftc-issues-final-rule-on-reviews-and-testimonials/), [K&H](https://www.khlaw.com/ftc-finalizes-rule-against-fake-reviews-and-testimonials)).
  - So: **no AI "customers", no AI testimonials, no AI before/after results.** Otto and Vee are characters, never reviewers.
  - **Meta's "AI info" label.** Meta applies it from C2PA/IPTC metadata or self-disclosure. Reports say photoreal AI people need the label shown visibly. All of this comes from secondary sources, so check Meta's Business Help Center before every campaign ([cinerads](https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy)).

### 2.8 Recurring-character series: what blew up and why

| Account | What happened | Evidence quality | Pattern to borrow `[inf]` |
|---|---|---|---|
| **Duolingo (Duo)** | TikTok grew from ~50K followers (Sept 2021) to millions, per speaker bios and agency pages (figures vary from 9M to 17M by date) ([HubSpot](https://blog.hubspot.com/marketing/duolingo-unhinged-content)). The Feb 2025 "Duo is dead" stunt (hit by a Cybertruck; revived after users earned 50B XP) got **~1.7B impressions at "essentially nothing"** in cost, per the CEO on the Q1 2025 call. Q1 DAU was 46.6M (+49 %), not attributed to the stunt ([Campaign](https://campaignlive.com/article/duolingo-ceo-raves-marketing-team-q1-earnings-call/1916660), [TechCrunch](https://techcrunch.com/2025/02/18/duolingo-killed-its-mascot-with-a-cybertruck-and-its-going-weirdly-well)). The social team had autonomy to post without senior sign-off | CEO statement and filings; growth attribution unproven | An **unhinged mascot with one obsession** (your streak). **Story arcs** with stakes. **Speed**: they ran the death stunt in about 6 days |
| **Scrub Daddy** | The CEO said TikTok brought "demonstrable sales growth" and that the brand got "a little more edgy" ([Inquirer](https://inquirer.com/business/scrub-daddy-tiktok-strategy-duolingo-20220420.html)). UK TikTok Shop sales were reported up 98 % over two months in 2025 ([Housewares Live](https://housewareslive.net/where-entertainment-meets-e-commerce/)) | Company statements | The **product itself is the character**: a face on a sponge, with skits around it |
| **Ryanair** | Became the biggest airline on TikTok (1.5M followers and 42M likes at the time of reporting). Its head of social credited "lose the corporate tone of voice". It uses a plane-face filter and self-deprecating replies to complaints ([Travel Weekly](https://www.travelweekly.com.au/article/ryanair-has-overseas-fans-desperate-to-fly-with-it-after-blowing-up-on-tik-tok/), [Socialinsider](https://socialinsider.io/blog/ryanair-social-media-strategy)) | Trade press | **Self-deprecation about your known weakness**. For an AI studio that weakness is "AI is fake and soulless", so Otto takes it personally. **Replies become content** |
| **Granny Spills** (AI character, Blur Studios) | Reported **~1M Instagram followers in 22 days** after its July 2025 launch (single source citing TIME). CreatorDB lists ~2.1M Instagram and ~907K TikTok followers in July 2026 ([Medium](https://medium.com/@renzo7/the-first-native-ai-influencer-just-hit-one-million-fans-guess-who-an-ai-grandma-f888bf266b62), [CreatorDB](https://creatordb.app/creatorstats/grannyspills/)) | Third-party estimates | **An archetype plus contrast**: a sweet grandma who gives savage dating advice. **One repeatable format**, with high volume (~170 posts at the 1M mark) |
| **Bigfoot / Yowie vlogs** (Veo 3) | Started late May 2025 after the Veo 3 release. "Big Yowie" reached ~150K TikTok and ~280K Instagram followers ([Kapwing interview](https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/)). The creator's first experiments did not perform | Creator self-report | **A known character doing a mundane format** (a vlog). The first attempts flop, so iterate the format, not the character |
| **Italian Brainrot** (Tung Tung Tung Sahur and others) | Absurd AI characters with mock-Italian voiceovers, which spread to merchandise and sports clubs in 2025 ([Daily Mirror LK](https://www.dailymirror.lk/print/life/Italian-Brainrot-The-AI-memes-only-kids-know/243-316838)) | No reliable account metrics | **Absurd names and a sonic signature** carry the meme. The audience is kids, which is the wrong fit for VXO |

**Common pattern across all six** `[inf]`:
- One clear **character contrast**: Otto the perfectionist against Vee and her stopwatch.
- One **repeatable format** that can be produced daily.
- **Story arcs** with stakes.
- **Replying in character** to comments.
- An **owned sound**.
- **Self-deprecation about the obvious objection.**

None of these accounts won by selling in every post. They won attention, and the sales story came later (Duolingo's sales story is unproven, Scrub Daddy's is self-reported).

---

## 3. Click mechanics for paid Meta and TikTok

### 3.1 Thumb-stop
- **Front-load the product or message** (TikTok's 63 % finding).
- **Use a visual-intrigue or bold-statement first frame** (Benly).
- **Show a fluent character or sonic cue in 2 s, and the logo in context** (System1×TikTok).
- **Never open on a logo card or a slow fade-up** `[inf]`.

### 3.2 Open loops and the withheld payoff
- **Curiosity is an information gap** (Loewenstein 1994). Curiosity rises when the gap feels small and closable ([summary](https://blog.taboola.com/why-does-mystery-entice-people-to-click)).
- **Too much mystery hurts.** Studies on the Upworthy A/B archive suggest clickbait does **not** consistently raise engagement, and that headlines can carry too much *or too little* information. That suggests an inverted U ([Cambridge talk abstract](https://talks.cam.ac.uk/talk/index/210730/)).
- **The rule for a 30 s ad** `[inf]`: open a small, specific question in second 0–2, such as "Why is Otto refusing to shoot this serum?".
  - Answer it **with the product**: the payoff *is* the product truth.
  - Put the product **on screen early** (by 3 s) while the *answer* waits. TikTok's 63 % finding concerns the product or key message being visible, not the joke resolving.
- **Never withhold the product itself to the end.** Motion's report notes that Meta data shows long comedic ads can reveal the product at 40–50 s and still perform. That works for long-form comedy, not for our 30 s format `[inf]`.

### 3.3 Offer, price and CTA phrasing
- **Match the button to audience temperature.** No controlled public study ranks "Shop Now" against "Learn More". The one widely quoted "+40 % for Shop Now" figure is unsourced, so do not use it. Practitioner consensus, which is opinion, is "Learn More" for cold audiences and "Shop Now" for warm ones ([AdEspresso test design](https://adespresso.com/blog/best-cta-facebook-ads/amp/); [1Digital](https://www.1digitalagency.com/blog/use-call-action-buttons-facebook/)).
- **Price and offer.** We found no 2024–26 creative study isolating on-screen price in short video. `[inf]` Show a price only to warm audiences or when the price is itself the surprise ("$2,500, frames in 2 days"). For cold audiences, sell the **next micro-step** (a free storyboard frame), not the purchase.
- **CTA lines that work as part of the joke** `[inf]`: the CTA is delivered by a character as a punchline, e.g. Vee: "Two days. Click before Otto asks for a third." This keeps the CTA inside the emotional peak instead of after it.

### 3.4 Punchline ad vs beauty ad: CTR and CPA
**We found no published, controlled comparison.** The closest evidence:

| Evidence | What it shows | What it does not show |
|---|---|---|
| Motion: humour is 25 % of $1M+-spend DTC ads vs 14 % of all social ads | Humour scales more often than its base rate | CTR, CPA, causation |
| Kantar: ads that really make people laugh beat intended humour on persuasion and branding | Execution quality matters more than intent | Paid-social CPA |
| Zappi 2025: top-quartile emotion ≈2× likelier to drive immediate sales | Any strong emotion beats a flat ad | Humour vs awe |
| Benly 2026: in fashion, watches and jewellery the top asset is **lifestyle/editorial** and the top hook is **visual intrigue** (`23` §1.1) | Beauty-led ads survive in luxury-coded categories | That jokes fail there |

**Working hypothesis** `[inf]`:
- **Punchline ads** should win **hook rate, sends and CTR** in mass-premium categories (home, food, gadgets, personal care).
- **Beauty ads** should hold **CPA** better in luxury-coded categories (fragrance, jewellery, fashion), where a joke can cheapen the product.
- **The best ad for most clients is "beautiful *and* one beat of wit"**: a premium frame with one deadpan turn. It is not a sketch.

**How we settle it per client** `[inf]`:
1. Make the same product and offer in two concepts, A (punchline) and B (beauty), with three hooks each.
2. Use one ad set with Advantage+ creative off, and equal budget.
3. Run to at least 50 purchase or lead events per concept, or 7 days, whichever comes later.
4. Read hook rate → hold → CTR → **CPA**.
5. Log it in `15` §3.3.

---

## 4. The Emotion & Virality Scorecard (run on every script before spend)

Score each item **0 / 1 / 2**. Two people score independently (or an LLM jury per `15` §2.2, plus one human), and you average the two. The maximum is **24**.

| # | Item | 0 | 1 | 2 | Evidence |
|---|---|---|---|---|---|
| 1 | **Thumb-stop frame** (0–1 s) | Logo card, fade-in, generic pack shot | Nice frame, nothing unexpected | Visual intrigue or pattern break you can describe in 5 words | Benly hook types; Wood "incident" |
| 2 | **Product/message by 3 s, branded in context** | Product appears after 5 s, or only as an overlay | By 3 s but as an overlay or packshot only | Product in the scene by 3 s, with a fluent character or sonic cue by 2 s | TikTok 63 %; System1×TikTok +182/+191 % |
| 3 | **One high-arousal emotion, nameable in one word** | "Nice", "informative", sad | Two competing emotions, or mild | One clear peak: amusement, surprise or awe | Zappi 2×; Berger & Milkman |
| 4 | **The punchline *is* the product truth** | No payoff, or a joke unrelated to the product (vampire humour) | Joke lands, but the product is a bystander | The laugh or gasp arrives *because* of a product feature | Kantar "laugh out loud" persuasion; `15` §1.4 |
| 5 | **Right-brain texture** | Isolated close-ups, VO explaining, a stare to camera | Some scene or character, but stiff | Character with agency, a place, an incident, implicit reactions, real music | Wood, *Look out* |
| 6 | **Open loop, small and specific** | No question, or a vague tease | A question exists but resolves before the product | A small question in 0–2 s, answered by the product | Loewenstein; Upworthy inverted U |
| 7 | **Send-ability** | You cannot name who would receive it | "Someone might like it" | The script names the recipient and why ("your cofounder who…") | Mosseri sends/reach |
| 8 | **Rewatch value** | Ends on an end card, nothing to re-see | Pleasant to rewatch | Seamless loop *or* a planted detail that rewards a second view | Replays count as views (Insights) |
| 9 | **Understood in one silent view** | Needs sound or a second watch to get it | Mostly clear | Captions plus visuals carry it; one idea | `01`, `03` platform specs |
| 10 | **Distinct concept** (not a variant) | Same structure as an existing ad | New hook only | New idea, visual structure or character situation | Meta Andromeda guidance |
| 11 | **Honest and compliant** | Fake testimonial or result, implied real person, undisclosed photoreal AI human, unprovable claim | Claims need softening | Every claim provable; characters are characters; AI disclosed where required | FTC 2024 rule; Meta AI label |
| 12 | **Clear next step that fits the temperature** | No CTA, or "Shop Now" with a price to a cold audience | Generic CTA after the peak | CTA delivered inside the peak by a character, with an offer sized to the audience | Practitioner consensus; `[inf]` |

**Approval thresholds** `[inf]`. These are our starting rules, to be recalibrated after 20 live ads against real hook rate, CTR and CPA, as `15` §3.3 describes:
- **Hard gates**: item 11 must score **2**, and items 2 and 4 must each score **at least 1**. Failing any gate means no production, whatever the total.
- **≥ 18 / 24**: approve for production.
- **14–17**: rewrite the lowest two items, then re-score once. If it is still under 18, it becomes a variant of another concept rather than a hero.
- **< 14**: kill it. Do not try to rescue it with edit tricks.
- **Organic VXO posts** use the same card, with item 12 replaced by "**Character consistency**": Otto and Vee on-model, in their voice, and in the first 2 s. The approval threshold for organic posts is **≥ 16**, since they are cheaper to test via Trial Reels.
- **Log every score** next to live metrics: hook rate, 50 % hold, sends/reach, CTR, CPA. If an item never correlates with results after 20 ads, cut it.

---

## 5. 30-day Instagram plan for @VXO (Otto & Vee)

**Goal:** DTC founders send a DM (keyword or direct) or click to book. **North-star metrics:** qualified founder DMs per week, and **sends per reach**. **Rules:**
- Every post is AI-disclosed. The bio and pinned post say "Otto & Vee are AI characters made by [founder name]'s studio".
- No fake client results, no fake testimonials, no real brand's logo or ad remade without permission.
- Numbers on screen come only from our own tests or from studies cited in this file.

### 5.1 The series (recurring formats)

| Series | Format (single take, 15–30 s) | Hook pattern | Emotion | Send target | CTA |
|---|---|---|---|---|---|
| **One More Take** (flagship) | Otto keeps asking for another take of a product shot. Vee clicks the stopwatch, and the final frame is gorgeous. The last line loops to the first | "Take 47." | Amusement → awe | "Your cofounder who never approves anything" | "Comment TAKE and we'll storyboard your product's first frame" |
| **Otto Rejects** | A generic AI product shot appears (made by us). Otto silently rejects it with a stamp, then the same product appears re-directed: light, scene, incident | "This is how most AI ads look." | Surprise; recognition | "The marketer still using stock-looking AI" | "Send us your worst product photo" |
| **Real or AI?** | A shot of a product (our own prop or a consenting client's). Vee asks "Real or AI?" and the reveal shows the frame-to-film process. Disclosed by the end | "Real or AI? 3 seconds." | Curiosity → surprise | "The friend who swears they can spot AI" | Comment your guess, and pinned reply explains how |
| **Vee's Receipts** | Vee explains one evidence point from this folder in 20 s, e.g. "Logo overlays reduced lift in 887 TikTok ads". Otto reacts deadpan | "Your logo is hurting your ad." | Surprise; usefulness | "Your media buyer" | "Save this" plus "DM RECEIPTS for the source list" |
| **Founder Fridays** (UGC-in) | A founder sends a product (opt-in via DM). We make a 6–8 s test shot on the account with written permission, and tag them | "You sent us a candle." | Warmth; aspiration | The featured founder shares it themselves | "Want yours? DM FRAME" |
| **Set Life** | 10 s vignettes: Otto's moustache gets in the shot; Vee times Otto's sigh. Pure character, no sell | Absurd action in frame 1 | Amusement | Anyone | none (reach builder) |

### 5.2 Cadence
- **5 Reels per week**:
  - 2 × One More Take or Otto Rejects (sell-adjacent)
  - 1 × Real or AI?
  - 1 × Vee's Receipts
  - 1 × Set Life or Founder Fridays
- **2 carousels per week**: process stills from `17`, frame → film. Carousels earn saves.
- **Stories daily**: polls ("Take 1 or 2?"), replies, and a behind-the-scenes look at the human founder. The human face builds trust in an AI account.
- **Trial Reels**: post 2 extra hook variants per week to non-followers only. Promote the winner by 3 s hold and sends/reach `[inf]`.
- **Reply in character** to the top 10 comments within 1 hour of posting. Turn the best reply into the next Set Life post, as Ryanair does.

### 5.3 Day-by-day (weeks repeat the rhythm; topics rotate)

| Day | Post | Hook (first line / first frame) | CTA |
|---|---|---|---|
| 1 | Pinned intro Reel: "We're Otto and Vee. We're AI. Our films aren't lazy." | Otto stares at the camera, and Vee turns him to face her | Follow + "DM FRAME" |
| 2 | One More Take #1: serum bottle | "Take 47." | Comment TAKE |
| 3 | Vee's Receipts #1: logo overlays vs logo in context | "Your logo is hurting your ad." | DM RECEIPTS |
| 4 | Real or AI? #1: coffee pour | "Real or AI? 3 seconds." | Comment guess |
| 5 | Set Life #1: moustache in frame | The moustache drifts into the shot | none |
| 6 | Carousel: 5 frames → 1 film (frame process) | "We approve stills before anything moves." | Save |
| 7 | Rest; Stories poll only | — | — |
| 8 | Otto Rejects #1: a flat AI packshot | "This is how most AI ads look." | "Send your worst product photo" |
| 9 | One More Take #2: sneaker | "Take 112. The lace." | Comment TAKE |
| 10 | Vee's Receipts #2: sends per reach | "Likes don't grow you. This does." | Save + share |
| 11 | Founder Fridays call-out: "Send us your product" | Vee holds an empty plinth | DM FRAME |
| 12 | Set Life #2: Vee times Otto's sigh | Stopwatch click | none |
| 13 | Carousel: 3 hooks for one product, which wins? | "Pick one." | Comment 1/2/3 |
| 14 | Rest; Stories: results of the poll | — | — |
| 15 | Real or AI? #2: perfume mist | "Real or AI?" | Comment guess |
| 16 | One More Take #3: candle (loop ending) | "Take 9. The flame is lying." | Comment TAKE |
| 17 | Vee's Receipts #3: the first 3 seconds (TikTok 63 %) | "Show the product by second 3." | DM RECEIPTS |
| 18 | Founder Fridays #1: first submitted product (with permission) | "You sent us a candle." | DM FRAME |
| 19 | Otto Rejects #2: the "stare" talking head | "Stop staring at me." | Send to your UGC creator |
| 20 | Carousel: our scorecard, 12 items | "We score every script before we spend a dollar." | Save + DM SCORE |
| 21 | Rest | — | — |
| 22 | Mini-arc ep. 1: "Otto quits" (he won't shoot a product with a bad label) | "I'm done." | Follow for part 2 |
| 23 | Mini-arc ep. 2: Vee finds a founder who fixed the label | "He's back." | Comment TAKE |
| 24 | Vee's Receipts #4: punchline vs beauty, "we don't know yet, so we test" | "Funny or beautiful? Nobody has published the answer." | DM TEST |
| 25 | Founder Fridays #2 | Product reveal | DM FRAME |
| 26 | Real or AI? #3 (the founder is real, Otto isn't) | Founder and Otto side by side | Comment guess |
| 27 | Set Life #3 | Absurd action in frame 1 | none |
| 28 | Rest; Stories AMA "Ask Vee about price" | — | — |
| 29 | One More Take #4, the month's best product, with a price card ("Launch film $2,500, 7–8 days", per `32`) | "Take 1. Done." (Vee's win) | "Link in bio: book a 15-min call" |
| 30 | Recap carousel: "30 days, what worked" with our own real numbers only | "Here's what 30 days taught us." | DM FRAME |

### 5.4 Measurement for the 30 days `[inf]`
- **Per post**: 3 s hold, average watch %, **sends/reach**, saves/reach, comments, keyword DMs, profile visits.
- **Weekly**: founder DMs (qualified = has a DTC brand), calls booked, cost per qualified DM if boosted.
- **Test 1, keyword-DM vs link-in-bio**: alternate weeks, same series, compare qualified DMs per 1,000 reach.
- **Test 2, hooks**: Trial Reels, two hooks per flagship episode.
- **Kill rule**: a series that sits below the account median on sends/reach for 3 episodes is replaced. Change the format, not the characters (the Bigfoot lesson).
- **Boost rule**: boost only posts that score ≥ 18 on the scorecard *and* beat the account median on sends/reach organically.

---

## 6. Top findings (one line each)
1. Emotion predicts short-term sales, not just brand: top-quartile-emotion ads are about 2× likelier to drive immediate sales (Zappi × VaynerMedia 2025, 4,000+ ads).
2. Emotional campaigns are almost 2× likelier to deliver top-box profit growth over the long term (Binet & Field, 996 IPA cases).
3. Shares follow arousal: awe and amusement spread, sadness doesn't. Surprise and usefulness also help (Berger & Milkman, ~7,000 articles).
4. Humour has the best effectiveness record, but only when it actually lands. "Intended funny" loses to "laugh out loud" (Kantar). Humour is 25 % of $1M+ DTC ads vs 14 % of all social ads (Motion).
5. Right-brain features (character, incident, place, humour, music) win attention and emotion. Isolated product close-ups and the stare push people away (Wood, *Look out*). This is AI's default failure mode.
6. A fluent character gives +57 % and a sonic cue in 2 s +191 % brand-awareness lift, while logo overlays reduce it (System1×TikTok, 887 ads). Otto and Vee must appear in the first 2 s.
7. Instagram reach to non-followers runs on sends per reach, alongside watch time and likes (Mosseri, 2025). Replays count as views, so write every post for a named recipient and a loop.
8. Over 63 % of TikTok's top-CTR videos show the product or key message in the first 3 s. Benchmark Meta hook rate is about 25–31 %, and under 20 % means the first frame is broken.
9. AI deception goes viral (bunnies, 200M+ views) but the backlash is about scams. AI labels alone haven't cut trust in experiments, but 73 % say they'd distrust *suspected* AI. Disclose up front, make the AI the joke, and never fake reviewers (FTC rule, Oct 2024).
10. No published controlled test compares punchline and beauty ads on CTR and CPA. Our default is "beautiful frame + one deadpan beat", and each client gets an A/B test (§3.4).
11. Recurring-character accounts that won (Duolingo, Ryanair, Scrub Daddy, Granny Spills) share the same traits: a character contrast, one repeatable format, arcs with stakes, in-character replies and self-deprecation about the obvious objection.
12. Meta's Andromeda treats near-duplicates as one concept. Variety of *concepts*, not colour swaps, is the lever.

## Sources (primary first)
- IPA/System1 *Look out* summary: https://ipa.co.uk/media/11169/system1_a-glimpse-of-look-out_november2021.pdf
- System1 characters: https://system1group.com/blog/creating-memorable-characters-in-advertising
- System1 × TikTok (887 ads): https://chiefmarketer.com/system1-tiktok-study-branding-elements-and-creator-led-content-improve-short-form-video-ads/
- System1 Cannes humour: https://www.research-live.com/article/news/system1-analysis-finds-increased-humour-in-uk-and-us-cannes-lions-winners/id/5127523
- Kantar humour (2023): https://www.kantar.com/inspiration/advertising-media/starting-to-laugh-again-the-slow-return-of-humour-in-advertising
- Binet & Field summary: https://www.alexmurrell.co.uk/summaries/les-binet-and-peter-field-the-long-and-the-short-of-it · Ritson: https://marketingscience.info/mark-ritson-binet-and-fields-research-may-not-be-perfect-but-that-doesnt-make-it-wrong
- Field 2019 (via Contagious): https://www.contagious.com/news-and-views/the-creative-awards-crisis-is-an-advertising-crisis
- Zappi × VaynerMedia 2025: https://agilebrandguide.com/zappi-and-vaynermedia-unveil-2025-state-of-creative-effectiveness-report-benchmarking-the-real-performance-of-advertising-today/
- ThinkTV / Nelson-Field: https://mumbrella.com.au/emotional-ads-will-lead-sales-study-suggests-487548 · Realeyes/Mars: https://www.research-live.com/article/news/emotion-measurement-predicts-sales-lift-with-75-accuracy/id/5020232
- Berger & Milkman: https://www.scientificamerican.com/article/the-secret-to-online-success-what-makes-content-go-viral
- Eisend humour meta-analysis (via Marketing Week): https://marketingweek.com/three-ways-humour-helps-brands-sell
- Motion humour report: https://netinfluencer.com/motion-report-dtc-brands-see-humor-ads-driving-higher-engagement
- TikTok Auction Ads Creative Tips: https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf
- Benly benchmarks 2026: https://benly.ai/learn/ad-creative/ad-creative-benchmarks-2026 · Billo/Novoads: https://novoads.ai/blog/video-ad-benchmarks-2026 · https://billo.app/blog/what-is-a-good-ctr/
- Instagram signals: https://searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/521389 · https://www.fanpagekarma.com/insights/?p=9293 · views/replays: https://www.socialcrawl.dev/blog/how-instagram-counts-views · originality: https://www.gigazine.net/gsc_news/en/20240502-instagram-updated-algorithm-prioritizes-original-content
- Mosseri year-end 2025: https://www.techradar.com/ai-platforms-assistants/ai-slop-won-in-2025-fingerprinting-real-content-might-be-the-answer-in-2026
- Meta Andromeda (Loomer): https://www.jonloomer.com/meta-andromeda/
- AI bunnies: https://www.404media.co/ai-bunnies-on-trampoline-causing-crisis-of-confidence-on-tiktok/ · https://petapixel.com/2025/07/31/people-are-falling-for-an-ai-video-of-bunnies-bouncing-on-a-trampoline
- AI disclosure: https://dare.uva.nl/id/dc6a541b-3dac-4913-9f07-a6573b5764f0?page=391 · https://thesis.eur.nl/pub/76583/ · Harris/Cannes 2026: https://www.fingerlakes1.com/2026/08/27/poll-finds-ai-labels-can-undercut-trust-in-advertising/
- FTC reviews rule: https://www.insideprivacy.com/advertising-marketing/ftc-issues-final-rule-on-reviews-and-testimonials/ · Meta AI labels (secondary): https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy
- Duolingo: https://campaignlive.com/article/duolingo-ceo-raves-marketing-team-q1-earnings-call/1916660 · https://techcrunch.com/2025/02/18/duolingo-killed-its-mascot-with-a-cybertruck-and-its-going-weirdly-well · https://blog.hubspot.com/marketing/duolingo-unhinged-content
- Scrub Daddy: https://inquirer.com/business/scrub-daddy-tiktok-strategy-duolingo-20220420.html · https://housewareslive.net/where-entertainment-meets-e-commerce/
- Ryanair: https://www.travelweekly.com.au/article/ryanair-has-overseas-fans-desperate-to-fly-with-it-after-blowing-up-on-tik-tok/ · https://socialinsider.io/blog/ryanair-social-media-strategy
- Granny Spills: https://medium.com/@renzo7/the-first-native-ai-influencer-just-hit-one-million-fans-guess-who-an-ai-grandma-f888bf266b62 · https://creatordb.app/creatorstats/grannyspills/
- Bigfoot vlogs: https://www.kapwing.com/resources/what-it-takes-to-make-viral-ai-video-content-we-asked-bigfoot/
- Curiosity gap: https://talks.cam.ac.uk/talk/index/210730/
