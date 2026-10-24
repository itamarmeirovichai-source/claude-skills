# 29 · Website strategy: the studio site around the "orbit" hero

Research brief, 2026-10-08. It plans the studio's own website: sitemap, page plan, full copy, the character's lines, tracking and risks. It builds on `28-sales-mastery` (offer, tiers, two-yes CTAs, honesty rules), `25-studio-thinking`, `23-what-actually-sells`, `22-viral-ai-ads-teardown`, `27-ai-creators-study` and `14-rourke-heath-study` (business). It does not repeat them.

**The hero is fixed** (client decision): a stylised "human-but-weird" AI character stands centre, a ring of our films orbits it, the visitor picks one, the character points, the film enlarges and plays, the character says "pick another, or continue" (ElevenLabs voice), and on "continue" it reaches out of the frame and pulls the site up over the hero. It then reappears in about 6 places. This file is about everything around that hero, and about the guardrails that let it convert.

**Evidence.** Studio sites were read with WebFetch on 2026-10-08 (text only: the tool sees copy and structure, not motion). Conversion data is mostly vendor or old case-study data; it is marked as such. Two YouTube transcripts were fetched with `yt-dlp` subtitles at 45–105 s spacing (Priestley, Chris Do); others had no subtitles. `[inf]` = our inference. `[law]` = legal point, not legal advice.

---

## 1. What the best studio sites do (2025–26)

| Site | Hero | How work is shown | CTA | Lesson for us |
|---|---|---|---|---|
| **Silverside** (Coke, Svedka) | One statement: "An AI innovation lab helping the world's best brands revolutionize their marketing ecosystem" + client-logo strip ([site](https://silverside.ai)) | Grid of campaign thumbnails, case carousel, "From the Lab" experiments with tools named | "Contact Us", "Ready to Transform Your Marketing?" | Names AI everywhere; a lab section shows craft. Logo strip is their proof (we can't copy it) |
| **Genre.ai** (PJ Accetturo) | "At the Forefront of Every Era of AI"; meta: "The AI Studio Behind the Internet's Most Shareable Videos" ([site](https://genre.ai)) | Barely on-page; points to YouTube/Instagram | "START A PROJECT" in the header, repeated | Reputation lives off-site (315M+ views). A newcomer can't rely on that `[inf]` |
| **Promise** (Dave Clark; bought Curious Refuge) | Domain did not resolve for our fetcher; press frames it as a gen-AI studio with its own production tool, MUSE ([Maginative](https://www.maginative.com/article/meet-promise-a-new-studio-reimagining-storytelling-with-generative-ai/), [THR](https://www.hollywoodreporter.com/business/digital/ai-studio-promise-vfx-generation-company-1236397636/)) | — | — | Positioning = "process you can trust", not "AI magic" |
| **Asteria** / **Wonder Project** | "Ethical AI" studio on a copyright-cleared model ([NME](https://www.nme.com/news/natasha-lyonne-to-direct-a-dystopian-film-made-with-ethical-ai-3859817)) / AI "augments assets… already created" ([Runway](https://runway.com/customers/how-house-of-david-used-runway-to-become-amazons-latest-hit-series)) | — | — | Trust stories: clean rights, real inputs. Ours: licensed tools, flagged AI, your real product photo |
| **Buck** | Wordmark + one sentence: "…brings brands, stories, and experiences to life through art, design, and technology" ([site](https://buck.co)) | 3 featured project cards, one line each | Newsletter: "all fam, no spam"; office emails | Big studios convert by referral, not page CTAs `[inf]` |
| **Tendril** | "Most innovation goes unseen. We make it impossible to miss." ([site](https://tendril.studio)) | Grid, "Client \| Project" titles + 1–2 line goal | Contact link, newsletter | A problem → promise headline in 9 words |
| **Scholar** (ex-Gentleman Scholar) | "We are an award-winning creative company driven by craft & curiosity" ([site](https://helloscholar.com/)) | Grid; client in large type; "+ 3D ANIMATION" tags with a filter row | Two emails: "Potential projects" / "General inquiries" | Tag filter = let buyers find their category fast |
| **Hey Studio** / **Phantom** | "Hey" ([site](https://heystudio.es)) / "Technology-led creative agency…" ([site](https://phantom.land)) | Recognition cards / "92 projects" by year with tags | "Contact" / cards only | Fame and volume as proof: not available to us |
| **Curious Refuge** | "THE WORLD'S FIRST HOME FOR AI STORYTELLERS" ([site](https://www.curiousrefuge.com)) | Community films | "TRY FOR FREE", "7-day happiness guarantee" | Free entry + named guarantee: the conversion pattern closest to ours |
| **Higgsfield** | Stacked looping-video cards; every preset has "Recreate" ([site](https://higgsfield.ai)) | Muted loops, each one click from "Start generating" | "Start generating", "Try Free AI Influencer" | Work-as-interface: each loop is a door, which is what our orbit is |
| **Igloo Inc** (Awwwards SOTY 2024) | Immersive WebGL scene ([case](https://awwwards.com/igloo-inc-case-study.html)) | Click ice blocks for products | — | A reviewer "didn't realize you could click on the ice blocks" ([CCRMA](https://ccrma.stanford.edu/~devig17/256A/rr3/)): say "Pick a film" in words |

**Patterns** `[inf]`:
1. Famous studios run *brand* sites (wordmark, sentence, grid, email) and convert on reputation. We have none yet, so ours is a **landing page dressed as a studio site**: one offer, repeated CTAs, objection handling.
2. Work is shown as **muted loops in a grid, tagged by category**, one click to a full film page.
3. AI-native studios **say AI loudly** and pair it with a trust story (lab, process, clean rights).
4. Nobody we read publishes prices; Curious Refuge (a product) does guarantees. Our free frames + approval-based balance is unusual for a studio, and that is our edge.

---

## 2. Conversion rules that shape the plan

### 2.1 Attention, speed, interactive intros
- **The first screen gets most of the attention.** NN/g 2018 (120 users, 130k fixations): 57 % of viewing time above the fold, 74 % within the first two screenfuls ([NN/g](https://www.nngroup.com/articles/scrolling-and-attention/)). → The hero must *say* what we sell and show the CTA, not only perform.
- **Speed.** 53 % of mobile visits are abandoned if a page takes >3 s to load (Google, 10k+ domains, 2016) ([Marketing Dive](https://www.marketingdive.com/news/google-53-of-mobile-users-abandon-sites-that-take-over-3-seconds-to-load/426070/)). Response limits: 0.1 s feels instant, 1 s keeps flow, 10 s loses attention ([NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/)).
- **Intros.** Nielsen (2000): intros "delay users' ability to get what they came for"; "skip intro" is a partial fix ([NN/g](https://www.nngroup.com/articles/flash-99-percent-bad/)). Old, Flash-era, but the mechanism (delay before value) still applies `[inf]`.
- **Scrolljacking.** Most test users were "at least mildly disoriented"; task-driven prospects got "severely agitated and just move on". NN/g: mix with normal scrolling, keep key text out of hijacked sections, skip it on mobile, put it after the main CTA ([NN/g](https://www.nngroup.com/articles/scrolljacking-101/)). → The "pull up" must be a **click-triggered transition, never a scroll lock**.
- **Video vs image heroes:** published tests are thin and mixed ([VWO](https://vwo.com/success-stories/device-magic)). We found **no bounce data on interactive-character heroes**: treat ours as a hypothesis with kill switches (§7).

### 2.2 Hard technical constraints on the hero
- **The voice cannot play on load.** Chrome: "Muted autoplay is always allowed"; sound needs user activation (a click/tap) or high media engagement; Web Audio starts suspended until a gesture ([Chrome](https://developer.chrome.com/blog/autoplay)). Safari is stricter `[inf]`. → The **first pick (click) is the gesture**; the character speaks only after it. Before that it "speaks" in captions.
- **Accessibility.** Moving content that starts automatically and lasts >5 s needs pause/stop/hide (WCAG 2.2.2, [W3C](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)); audio playing >3 s needs a pause/volume control (WCAG 1.4.2). Honour `prefers-reduced-motion` (orbit stops, pull-up becomes a fade).

### 2.3 The character: stylised beats realistic, and it can't endorse
- Uncanny-valley evidence leans to **stylised or imperfect** virtual influencers. A 2024 comment-mining study found engagement fell as avatars approached human appearance; a 2025 ANZMAC pre-study found a human-like avatar caused discomfort; results vary by culture and disclosure ([summary of studies](https://ciencia.iscte-iul.pt/publications/how-uncanny-are-virtual-vs-human-influencers-a-text-mining-approach/107467), [Syracuse 2025](https://news.syr.edu/2025/11/25/how-much-do-we-trust-virtual-influencers/)). Small, directional. → "Human-but-weird" is the right call; keep it **clearly non-human** (odd proportion, colour or texture).
- The FTC's 2023 Endorsement Guides count **virtual influencers as endorsers**; the advertiser answers for what they say, and an avatar can't truthfully claim to have used a product ([BakerHostetler](https://www.bakerlaw.com/insights/updated-ftc-endorsement-guides-hold-virtual-influencers-to-actual-standards/)) `[law]`. → **Our character is a host, never a reviewer.** It never praises results, never says "clients love…", never implies it is a customer.

### 2.4 Copy frameworks applied
- **Awareness (Schwartz).** Most early traffic will come from our cold emails (28): people who already got one idea and an offer of frames, so they are **product-aware of us** and need the offer + proof, not education. Social traffic (spec films) is problem/solution-aware `[inf]`. → Lead with the offer straight after the hero; put "why" lower.
- **Headlines (Ogilvy):** "five times as many people read the headlines as read the body copy"; no blind headlines ([swipefile](https://swipefile.com/five-times-as-many-people-read-the-headlines-david-ogilvy)). → Every section headline must make sense alone.
- **Joanna Wiebe:** match the button to awareness; write "calls to value" that finish "I want to…" ([CoSchedule interview](https://coschedule.com/blog/how-to-use-conversion-psychology-to-get-better-results-with-joanna-wiebe-from-copyhackers-amp080)). → "Get my 5 free frames", not "Submit".
- **StoryBrand (SB7):** customer = hero, brand = guide; header says what you do + outcome + CTA; a 3-step plan; stakes; repeated CTA ([Knapsack](https://knapsackcreative.com/blog/a-deep-dive-into-storybrands-website-framework)). → The founder's product is the hero; our character is literally a guide. Nice fit.
- **Hormozi value equation:** Value = (dream outcome × perceived likelihood) / (time delay × effort) ([summary](https://www.ecomcrew.com/100m-offers-book-summary/)). Mapping: dream = "a film that makes my product look expensive"; likelihood = frames on *your* product first + balance on approval; time = frames in 3–5 days, film in 7–8; effort = one photo, no call, no shoot.
- **Priestley (scorecard funnel):** two hook types, "frustration" and "readiness"; ask name + email first, phone optional; then **qualifying questions** (current situation, 90-day goal, obstacle, preferred solution as a budget proxy) ([YouTube](https://youtu.be/az1Zh-FNSno), transcript). His "20–40 % start" figure is self-reported. → We borrow the **two-step form**: short step 1, optional qualifiers on step 2.
- **Chris Do:** never drop price; trade scope, "have-to-haves" vs "nice-to-haves" ([YouTube](https://youtu.be/Abi8kwkfZbA)). Hence "From $750" is a smaller scope, not a discount.

### 2.5 Forms, proof, pricing
- **Fields.** Fewer usually helps, but the gains are smaller than the famous anecdotes (Expedia "$12M", 11→4 fields "+120 %"); one Unbounce test *lost* 14 % by removing fields people wanted; making phone optional doubled one form's conversion ([CXL](https://cxl.com/blog/reduce-form-fields/)). No study isolates **file-upload** fields; instrument it ourselves. → Upload is **optional**, with a "use the photos on my site" fallback.
- **Benchmarks.** Unbounce: agency landing pages median 1.7–2.4 % (2019–20), top quartile ~23 % ([Unbounce](https://unbounce.com/industry/advertising/)).
- **Proof without logos.** No fake clients, testimonials or stats: the FTC's 2024 rule bans fake/AI testimonials (28 §9) `[law]`. Replace social proof with **sample proof** (frames on their own product), **process proof** (BTS breakdowns, which "often beat the spec", 20 §1), **risk reversal**, and a **real founder**.
- **Pricing.** No controlled evidence on publishing agency prices; most agencies don't. MarketingSherpa (via a vendor) says B2B buyers want budget ranges early ([Vengreso PDF](https://inbound.vengreso.com/hs-fs/hub/11964/file-13107174.pdf)). For a $750–$5,000 offer sold to founders, a visible range pre-qualifies and avoids a "too pricey to ask" bounce `[inf]`. Show tiers high → low (anchoring), three real options, one recommendation (28 §8; single-option aversion, Mochon 2013).

---

## 3. Sitemap

```
/                 Home (hero + long page; everything below)
/frames           Lead-magnet landing page. No intro. Link target for cold emails and ads
/frames/thanks    Step 2 qualifiers + "what happens next"
/work             All films, filter by category (Beauty, Fragrance, Drinks, Home, Accessories)
/work/[film]      One film: player, 9:16/4:5 cuts, one-paragraph idea, BTS breakdown, "spec · invented brand" label
/pricing          Same as home pricing section, plus the contract terms in plain English
/about            Itamar: real photo, face video (30 s), why the studio exists, Boca Raton address
/ai               How we use AI: tools, disclosure, rights, what we won't do
/terms  /privacy
```
Every page ends in the frames CTA. **Cold-email links go to `/frames?b=[brand]`, never to the hero**: those readers already know the offer (§2.4), and the hero is a delay for them `[inf]`. `/frames` gets a muted 6 s strip of the orbit at the top as a teaser and a "See the full show" link back home.

---

## 4. Home page plan, in order, with copy

`[NAME]` = the character's name (to pick). Character pop-ups: **6** (P1–P6). Rules for all pop-ups: max 1 line, max ~2.5 s, enter from the edge, never cover a headline, CTA or form; one per section; dismiss with ✕ ("Hide [NAME]" removes all, remembered in `localStorage`); voice only if the visitor turned sound on in the hero; off for reduced motion.

### S0 · Hero (the orbit) — fixed concept, our guardrails
**Purpose:** show the craft in one interaction and state the offer.
**Layout (desktop):** character centre; 6–8 film loops in the ring (muted 3 s, ≤600 kB each, poster image first). **Static layer visible at 0 s:** H1 top-left, subhead, two CTAs, "Skip the show ↓" bottom-centre, sound toggle, pause button. Caption bubble beside the character.
**Mobile:** ring becomes a swipeable arc of 5 at the bottom third; character upper middle; H1 above. Pull-up = tap "Continue" or plain scroll (no lock).
**Flow:** load → caption "Pick one. I'll press play." → visitor picks (first gesture: unlock audio) → character points, film enlarges with controls (unmuted only if sound on; default **sound on after a click** with a visible mute) → after the film or after ✕ → "Pick another, or continue?" → Continue → hand reaches out, pulls S1 up (≤1.2 s). Scroll at any moment = the same pull-up. Returning visitors land with the hero collapsed to a 40 vh strip `[inf]`.
**Character role:** host. Points, reacts, speaks ≤8 words per line.

**Headline options** (test A vs B; C is the alternative):
- A: **"Product films your customers stop scrolling for."**
- B: **"15-second product films. No shoot. Made with AI."**
- C: **"Your product, in a film you'd never pay a crew for."**

**Subhead:** "Premium 15–25 s ads for founder-led brands, directed by a human and made with AI in Boca Raton. Start with 5 free frames of your product."
**CTAs (two yes):** [ Pick a film ▶ ] [ Get 5 free frames → ]
**Micro-line under CTAs:** "Everything here is AI-made, including [NAME]."

### S1 · The offer (what the character pulls up)
**Purpose:** convert product-aware visitors immediately (Schwartz).
**Layout:** split. Left: headline, 3 bullets, CTA. Right: a before/after slider: *a plain product photo → one of our frames*. Use our own invented-brand product or a product we photographed, never a real brand without permission (28 §5) `[law]`.
**Character:** **P1** sits on the panel's edge it just pulled up: "Five frames. Your product. Free."

- **H2:** "See your product in our world before you spend a cent."
- **Sub:** "Send one product photo. In 3–5 business days you get 5 cinematic frames, the storyboard of your ad. Judge the look on *your* product, not on our reel."
- Bullets:
  - "5 frames, 1 concept, built around your product"
  - "No call needed. No card. No strings."
  - "Marked 'AI concept'. Yours to keep and share inside your team"
- **CTA (two yes):** [ Frames for my bestseller ] [ Frames for my next launch ] → both open the same form with the choice prefilled.

### S2 · The problem (stakes)
**Purpose:** name the frustration (Priestley); one sourced fact. **Layout:** a large line, three cards, no character.
- **H2:** "Your best ad is getting tired. A new shoot means weeks and a crew."
- Cards:
  - "**Ads wear out fast.** The median Meta ad creative lives about 22 days (Benly, 271K creatives, Q1 2026)." (source: 23 §1)
  - "**Shoots are slow.** Casting, location, crew, edit: by the time it's live, the moment's gone."
  - "**UGC all looks the same.** Some shots are hard to film: a guava splitting in slow motion, a bottle catching the sunset."
- Closing line: "We make the shots that are hard to film, fast enough to keep up with your ads."

### S3 · The work
**Purpose:** proof of craft, honestly labelled. **Layout:** 6-tile grid of muted loops (9:16), category tags + filter (Scholar pattern), click opens the film page or a lightbox with sound. Each tile label: "**Spec film · invented brand · 100 % AI · 20 s**".
**Character:** **P2** peeks from behind a tile: "These brands don't exist. Yours does."
- **H2:** "Three brands that don't exist. Films that look like they do."
- **Sub:** "We invented AURUM, VESPER and SOL to show what we can do with nothing but a product and an idea. Your film starts from your real product photo."
- **CTA:** [ See all films ] [ Get my 5 free frames ]

### S4 · How it works (the plan)
**Purpose:** cut effort and uncertainty (Hormozi; SB7 plan). **Layout:** 3 numbered steps with a timeline bar; one small frame per step.
**Character:** **P3** walks along the timeline: "You approve every step."
1. "**Frames (free, 3–5 days).** One photo in, 5 frames out. You tell us what's off."
2. "**Film (7–8 days from kickoff).** Storyboard day 2, first cut day 5, final day 7–8. Two revision rounds."
3. "**Variants.** Every film ships as a 20 s hero, an 8 s loop and cut-downs in 9:16 and 4:5, with 3 different openings to test." (23 §6)
- **H2:** "From one product photo to a finished ad in about a week."
- **CTA:** [ Start with step 1 → ]

### S5 · Proof without logos
**Purpose:** answer "who are you?" honestly. This replaces the logo strip.
**Layout:** a short, plain statement + 4 proof blocks + founder photo and 30 s face video (a real human balances an AI host `[inf]`).
**Character:** **P4**, small, by the heading: "No logos yet. Be the first."
- **H2:** "No client logos yet. Here's what you get instead."
- **Intro:** "We're new, and we won't pretend otherwise: no fake logos, no made-up reviews. So we take the risk instead of you."
- Blocks:
  1. "**Proof on your product.** The 5 free frames show you the result before you pay."
  2. "**Pay the balance only if you approve.** 50 % to start. If the final cut doesn't win you over after two revision rounds, you don't pay the rest."
  3. "**See how it's made.** Every film comes with a breakdown: product photo → frames → final." (link one BTS)
  4. "**Clean and disclosed.** Commercially licensed AI tools, every generated element flagged, every prompt and version logged. No real person's face without written consent."
- **Founder:** "I'm Itamar. I direct every film myself. [one real line of background]. Boca Raton, FL." (Fill with true facts only.)

### S6 · Pricing
**Purpose:** pre-qualify, anchor, recommend one. **Layout:** three cards, high → low, middle highlighted; retainer as a band below; risk reversal under the cards. (Tiers from 28 §8 plus a top tier to match the $750–$5,000 range.)
**Character:** **P5** taps the middle card: "Itamar's pick for most launches."
- **H2:** "Clear prices. Pick the size that fits this quarter."

| **Campaign** — $5,000 | **Launch pack** — $2,500 ★ Recommended | **Starter** — $1,200 |
|---|---|---|
| 2 concepts, 2 hero films (20 s) + 12 variants | 1 hero film (20 s) + 6 variants | 1 hero film + 3 cuts |
| 3 openings per concept, 9:16 / 4:5 / 1:1 | 3 openings, 9:16 / 4:5 / 1:1 | 9:16 + 4:5 |
| About 2 weeks | About 1 week | About 1 week |

- Band: "**Always-on** — $3,500/mo (3-month minimum): 8–12 new variants a month + 1 new concept, so you always have something fresh to swap in."
- Small line: "Need just one 15 s film? From $750."
- Under the cards: "All plans: 50 % to start, balance on approval. 2 revision rounds per film. Music licensed for paid social. Perpetual licence for your brand's ads."
- **CTA (two yes):** [ Start with free frames ] [ Book a 15-min call ]

### S7 · FAQ (objections)
**Layout:** accordion, 10 questions, first one open. No character (it would be noise).

1. **Is it really all AI?** — Yes. Every frame is generated with AI tools, from your real product photos, then directed, edited, graded and sound-designed by a human. We say so, proudly.
2. **Won't it look fake?** — Most AI ads do: waxy skin, melting labels. That's why you see frames on your product first. If they look fake, we stop there and you've lost nothing. Product scenes without people are where AI is strongest.
3. **Will Meta or TikTok label it as AI?** — It might. Platforms can add an "AI info" label to ads with AI-generated content. We flag every generated element so you can disclose correctly. (Check current platform policy at delivery.) `[law]`
4. **Who owns the film?** — On full payment you get a perpetual, worldwide licence to use it in your brand's ads, and we promise not to reuse it. Honest note: purely AI-generated material may not be copyrightable in the US, so exclusivity is our promise, not a legal guarantee (US Copyright Office, 2025). `[law]`
5. **What do you need from me?** — One good product photo (more is better), your website, and 10 minutes of feedback per round.
6. **What if I don't like the final cut?** — You get two revision rounds. If it still doesn't work for you, you don't pay the balance. The deposit covers the work done.
7. **Can you put people in it?** — Hands, silhouettes and stylised characters, yes. Realistic AI people pretending to be customers, no: that misleads buyers and breaks FTC rules.
8. **Can the ad make health or results claims?** — Only claims you supply and can back up. We don't write medical or performance claims.
9. **Do you guarantee sales or ROAS?** — No one honest can. We guarantee the work: on time, as scoped, approved by you.
10. **Why are the frames free? What's the catch?** — No catch. It's the fastest way for you to judge a new studio. One concept, one round of light tweaks. If you like them, they become your storyboard.

### S8 · Final CTA + form
**Purpose:** the conversion point for long-scroll visitors. **Layout:** full-width; left: the headline; right: the form (same as `/frames`, §5).
**Character:** **P6** leans in beside the button: "I'll be waiting with your frames."
- **H2:** "Your product deserves a film. Start with five frames."
- **Sub:** "Free, no call, ready in 3–5 business days."

### S9 · Footer
Studio name · AI video ads · [street address or PO box], Boca Raton, FL (same as the email footer, 28 §1.2) · "Everything on this site is AI-made and labelled. Spec films are for invented brands." · /ai · /terms · /privacy · email.

---

## 5. Form and microcopy (`/frames` and S8)

**Step 1 (required minimum: 3 fields + optional upload):**

| Field | Type | Label / helper | Error |
|---|---|---|---|
| Email | email, required | "Work email" / "Where we send your frames." | "That email doesn't look right. Check for a typo?" |
| Brand website | url, required | "Your website" / "We'll study your brand look here." | "Add your site, e.g. yourbrand.com" |
| Product | text, required | "Which product?" / "Name one. We'll build all 5 frames around it." | "Tell us which product." |
| Photo | file, optional, up to 3, JPG/PNG/HEIC/WebP, 20 MB each | "Product photo (optional)" / "A clean shot on a plain background works best. No photo? We'll use the ones on your site." | "That file is too big (20 MB max). Try a smaller copy?" / "Upload failed. Try again, or skip it and we'll use your site." |
| Look | two radio cards | "Which look?" **[ Clean studio, all about the product ]** **[ In a world, with a story ]** | — (default to first) |
| First name | text, optional | "First name (optional)" | — |

- **Button:** "Get my 5 free frames" (calls to value, Wiebe). Loading state: "Sending… (big photos take a few seconds)".
- **Under the button:** "Free. No card, no call. You'll get them by email in 3–5 business days, marked 'AI concept'."
- **Privacy line:** "We use your photos only to make your frames. We don't post them or share them outside the studio. [Privacy]" `[law]`: keep it true for every AI tool used; check each tool's data terms.
- **Spam:** honeypot field + server-side rate limit (no CAPTCHA unless abused) `[inf]`.
- **Capacity line** (only when true): "I make frames for [N] brands a week. This week: [n] spots left." Never fake it (28 §9).

**Step 2 (`/frames/thanks`, all optional; Priestley's qualifiers):**
- Headline: "Got it. Your frames are on the way."
- "What happens next: 1) I study your brand today. 2) Frames land in your inbox in 3–5 business days. 3) If you like them, we talk film. If not, tell me what's off."
- "Help me aim the frames (30 seconds, optional):"
  - "Where will the ad run?" Meta / TikTok / YouTube / Website / Not sure
  - "What would make this a win in the next 90 days?" New launch / Fresh ads for a tired winner / Test a new look / Just exploring
  - "What's the hardest shot to get right now?" (short text)
  - "Roughly what do you spend on ads a month?" Under $5k / $5–20k / $20–50k / $50k+ / Prefer not to say
- Two-yes CTA: "When the frames are ready, should I **email them**, or **walk you through them on a 15-minute call**?" (28 §4)

---

## 6. The character's spoken lines (ElevenLabs; captions always on)

Rules: ≤8 words; host, never reviewer (§2.3); no claims about clients or results; same voice everywhere; every audio line also shown as a caption; nothing plays before the first click.

| Moment | Line |
|---|---|
| Idle, before first click (caption only) | "Pick one. I'll press play." |
| Idle after 6 s without a pick (caption) | "Go on. Any film." |
| On pick (rotate) | "Good eye." / "Watch the light on this one." / "That brand? I made it up." |
| After the film (fixed) | "Pick another, or continue?" |
| On a second pick | "Greedy. I like it." |
| On "continue" (during pull-up) | "Hold on. Bringing the rest up." |
| On "Skip the show" | "Fair. I'll be around." |
| P1 offer | "Five frames. Your product. Free." |
| P2 work | "These brands don't exist. Yours does." |
| P3 process | "You approve every step." |
| P4 proof | "No logos yet. Be the first." |
| P5 pricing | "Itamar's pick for most launches." |
| P6 form | "I'll be waiting with your frames." |
| Hover on the "AI-made" line | "Yes. I'm AI too." |
| Form success | "Got it. Itamar's on it." |

ElevenLabs: confirm the plan's commercial-use terms before launch (free tiers have historically been non-commercial with attribution; verify the current terms) `[inf]` (see 13).

---

## 7. Conversion-tracking plan

**Tools (free tiers, no spend):** a cookieless analytics tool or GA4 for events and funnels; Microsoft Clarity for session recordings and heatmaps (it shows where people skip or get stuck in the hero); form backend logs; a simple prospect sheet joining site leads to 28's pipeline `[inf]`. Disclose analytics in the privacy policy; collecting personal info from Californians triggers a privacy-policy duty (CalOPPA) `[law]`.

**UTMs:** cold email `utm_source=email&utm_medium=cold&utm_campaign=batch-01`; spec posts `utm_source=linkedin|instagram|tiktok&utm_content=[film]`. Avoid one-off per-person tracking links unless disclosed `[inf]`.

**Events:**

| Group | Events (properties) |
|---|---|
| Hero | `hero_loaded` (LCP ms, device), `film_pick` (film_id, nth_pick), `film_progress` (25/50/100 %), `sound_on`, `sound_off`, `hero_pause`, `continue_click`, `skip_click`, `scroll_past_hero` (s since load), `pullup_done` |
| Page | `section_view` (S1–S8, ≥50 % visible 1 s), `work_open` (film_id), `bts_open`, `pricing_view`, `tier_click` (tier), `faq_open` (q_id) |
| Character | `pop_seen` (P1–P6), `pop_click`, `character_hide` |
| Form | `cta_click` (location, label), `form_start`, `field_error` (field), `upload_start`, `upload_ok` (MB), `upload_fail` (reason), `form_submit` (look, has_photo), `step2_submit` (spend band), `call_booked` |
| Offline | `frames_delivered`, `frames_call`, `proposal_sent`, `deal_won` (tier, $), `deal_lost` (reason) |

**KPIs and first thresholds** `[inf]`, to be replaced with our own baseline after ~300 sessions:
- Hero: **skip rate** in the first 5 s; **pick rate** (≥40 % is healthy); time to first pull-up (median ≤25 s). Mobile and desktop separately.
- Page: S1 view rate after the hero (≥70 %), pricing view rate.
- Form: `form_start` / `section_view S1` and `form_submit` / `form_start` (aim ≥50 %); upload failure rate (<5 %).
- Business: lead → frames → call → paid (the number that matters).

**Kill switches for the hero** (decide on ~300 sessions per device `[inf]`):
1. If >40 % of mobile visitors leave before any scroll or pick → ship the mobile default as a static hero with the orbit as a "Play the show" button.
2. If LCP >2.5 s on 4G → cut ring loops to posters until hover/tap.
3. If pick rate is high but S1 view is low → the pull-up confuses; add a visible "Continue ↓" earlier.

**Testing with low traffic.** At a few hundred visits a month, A/B tests will not reach significance on form submits `[inf]`. Use (a) sequential changes with a fixed 2–3-week window each, (b) Clarity recordings of 20 sessions per change, (c) 5 founder hallway tests ("What does this studio sell? What would you click?"). Test only big swings: headline A vs B, hero-first vs `/frames`-first for cold traffic, prices shown vs "from $750".

---

## 8. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | **The hero delays the offer** (NN/g intros, scrolljacking) and founders on phones bounce | H1 + CTAs + "Skip" visible at 0 s; scroll never locked; cold traffic to `/frames`; kill switches (§7) |
| 2 | **Voice silently fails** (autoplay rules) or startles people at work | Voice only after a click; captions always; mute visible; remember the choice |
| 3 | **Heavy page** (WebGL + 8 videos) misses the 3 s mobile budget | Posters first, 3 s loops ≤600 kB, full films on demand, lazy-load below the fold |
| 4 | **Character reads as creepy, or as "gimmick over substance"** | Stylised, clearly non-human; ≤8-word lines; 6 pop-ups max with a hide switch; test with 5 founders |
| 5 | **Accessibility** (WCAG 2.2.2, 1.4.2, keyboard users can't pick from a ring) | Pause button, reduced-motion mode, ring items are real buttons with labels, captions on every film |
| 6 | **Honesty slips**: spec films mistaken for client work, a pop-up implying clients | "Spec · invented brand" label on every tile and film page; character never endorses (FTC 2023 guides) `[law]` |
| 7 | **Using a real brand in the before/after or the frames** without permission | Only our invented brands publicly; prospect frames stay private (28 §5) `[law]` |
| 8 | **Risk reversal gets abused** (client takes the cut, refuses the balance) | Watermarked cut until paid; balance = final unwatermarked files; offer only with the 50 % deposit (28 §8) |
| 9 | **Lead-magnet overload**: more frame requests than one person can make | Capacity line (true numbers), step-2 qualifiers to prioritise, auto-reply with a real date |
| 10 | **Copyright and data**: AI output may not be copyrightable; uploaded photos pass through AI tools | Say it plainly in the FAQ; check each tool's data terms before promising privacy `[law]` |
| 11 | **ElevenLabs/voice and tool licences** not commercial on free tiers | Verify before launch (13) `[inf]` |
| 12 | **SEO invisibility** of a JS-only hero | Server-render all copy as HTML; film pages with text |
| 13 | **Prices inconsistent** with emails/proposals; **AI backlash** (22 §5) | One source of truth (28 §8); craft first, human director visible, disclose proudly |

---

## 9. Gaps
- Promise's and Asteria's own sites could not be read (domain/fetch); Awwwards jury notes not fetched. All site reads are text-only (no motion).
- No study measures bounce on interactive-character heroes or on file-upload fields: our own data must decide (§7).
- Only 2 YouTube transcripts (Priestley, Chris Do); Hormozi's had no subtitles, Harry Dry's hit HTTP 429.
- Conversion numbers are vendor or old case-study data; treat as directional.
