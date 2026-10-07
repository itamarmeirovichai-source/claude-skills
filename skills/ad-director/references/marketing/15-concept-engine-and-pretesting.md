# 15 · Concept engine and zero-cost pre-testing (product → many ideas → 3 storylines)

Research brief, 2026-10-07. It covers what happens **before** step 3 (strategy card) of `00-master-playbook`. Awareness levels, JTBD, the 15 gates and Andromeda's "8–15 really different concepts" are in `01-fundamentals` and are not repeated here. `[inf]` marks our own inference rather than a sourced finding.

The machine works in five stages: client product → research → **generate ~60 concepts** → hard gates → **LLM-jury rubric** → **persona-panel pairwise tournament** → stills round → **3 storylines with a twist** → client picks one. The only spend is LLM tokens plus about 18 cheap stills.

---

## 1. How top strategists generate concepts at volume

### 1.1 The hierarchy everyone converges on
Practitioners split an ad into four layers and change **one layer per test**. The layers are concept (the big idea), angle (the reason-to-buy it argues), hook (the first ~2–3 s) and format (UGC, static, motion, skit and so on). A new hook on an old concept counts as an iteration; a new concept is a new bet ([Chatterbuzz](https://www.chatterbuzzmedia.com/blog/ad-creative-testing/), [hawky.ai](https://hawky.ai/blog/creative-strategy-frameworks)). Sources disagree on which layer moves results most: one says format does (200–300 % swings), others say concept or angle does (2–5×). After Meta's Andromeda change, the consensus is that only **diversification** (a new persona, angle or "emotional world") gives the algorithm new signal. Iteration (hooks, copy, thumbnails) refines a winner but does not count as variety ([Motion talk](https://motionapp.com/library/talk/andromeda-2-0-explained-how-meta-s-algorithm-actually-picks-your-winning-ads/), [1800DTC](https://1800dtc.com/reads/agency-insights-what-metas-andromeda-update-actually-changed-and-how-were-adapting-our-ads)).

**Our hierarchy** `[inf]` adds one level on top for the premium-film style our client likes:

| Level | Question it answers | Example (fictional candle brand) |
|---|---|---|
| **Territory** (anchor) | Which pain or desire? | "Desire: make a rented flat feel like mine" |
| **Angle** | Persona × anchor → core truth | "Renter, 29: can't paint walls, *can* change the air" |
| **Concept / storyline** | Which creative template dramatises it? Where is the twist? | Time-leap: the same bare room, a lit candle, and the room "remembers" a year of evenings |
| **Hook** (0–3 s) | First frame + text overlay + sound | Close-up of a match strike, with the text "Landlord said no nails." |
| **Format / execution** | Container and craft | 20 s AI cinematic, no faces, VO tagline |

### 1.2 Persona × desire × objection grid (Motion's Creative Strategy Engine)
Motion's master framework ([Creative Strategy Engine](https://motionapp.com/library/frameworks/creative-strategy-engine)):

1. Choose the anchor. **Pain** is the default; **desire** is for aspirational or luxury products, which suits our premium client.
2. List 3–5 persona segments per pain/desire bucket. A persona is a life context, not a demographic.
3. Write one **messaging angle per pain × persona intersection**. Each angle document holds the use case, deepest desire, feature/benefit priorities and **top objections**.
4. Express each angle at every awareness stage, then write **3–5 hooks per angle per stage**, then pick formats by purpose: educate or reveal early, prove mid-funnel, drive action late.
5. Run a coverage and gap map to find missing personas, pains or stages.

Research inputs that feed the grid:
- **Review mining.** Motion's Review Audit pulls five buckets from reviews: pain points, trigger moments, objections, transformations and standout language ([Motion frameworks](https://motionapp.com/library/frameworks/)).
- **Dara Denney's method.** Mine *both* positive and negative reviews for angles and objection handling. Rank personas by **frequency in reviews × emotional intensity**. Compare "who the customers actually are" with "who the ads currently target"; the gap is the opportunity. "Without a diagnosis you don't have a strategy, you just have testing." She also ranks creator/messaging above format, because angles travel across platforms and formats don't ([Motion · Dara Denney](https://motionapp.com/library/talk/dara-denney-stop-guessing-start-diagnosing-ad-creative-testing/), [AMA 2022](https://motionapp.com/library/talk/ama-creative-strategy-dara-denney/)).
- **Organic-feed research (Barry Hott, via Alex Cooper).** Study the organic content the audience consumes, not competitors' ads, to avoid a "sea of sameness". **Clear beats clever.** Optimise **hook relevance, not hook rate**: some winners had hook rates under 15 % because they stopped the *right* people ([Alex Cooper](https://alexcooper.beehiiv.com/p/7-facebook-advertising-lessons-i-learned-from-barry-hott), [Practical Ecommerce](https://www.practicalecommerce.com/ugly-ads-perform-best-marketer-says)).

For no-client-data situations: if there are no reviews, mine competitor reviews and Reddit/Amazon category reviews instead `[inf]`.

### 1.3 Hook frameworks
Motion's **8 hook triggers**: pattern interrupt, identity call-out, pain agitation, curiosity gap, social proof/credibility, contrarian/myth-bust, aspiration/desire, urgency/stakes. **The strongest hooks combine two triggers.** Each video hook is written as three parts (visual, text overlay, spoken/VO), and the spoken part must work without the visual.

Bans: no "Introducing…/Discover…/Are you looking for…", no brand name in line 1, no hook that fits any product, no trigger reused across a set.

([Hook Writing](https://motionapp.com/library/frameworks/hook-writing))

Savannah Sanchez: keep the body constant and swap only the first ~3 s (cheap split tests); short hook-driven cuts for prospecting, longer objection-handling cuts for warm audiences; ~80 % of her ideas start from an ad or organic TikTok she has seen ([Motion summary](https://motionapp.com/library/talk/savannah-sanchez-shares-her-top-43-ad-hooks-for-apps-and-services/), [2026 talk](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/)).

Our client forbids talking heads, so we translate spoken triggers into **visual + text-overlay** triggers. For example, "identity call-out" becomes an overlay like "For people who rent." on a sensory first frame `[inf]`.

### 1.4 Twist and punchline engine: the creativity templates
The best-evidenced generator of "clever" ideas is **Goldenberg, Mazursky & Solomon (1999, *Marketing Science*)**:
- 89 % of 200 award-winning ads fit **six templates**.
- In a second study, **50 % of award winners but only 2.5 % of non-winners** were explained by them.
- People *trained* on the templates produced ads judged more creative, with better brand attitude and recall, than people using free association ([paper PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/3384/fundamental.pdf)).
- A replication on effectiveness awards (the Cassies) found 71 % template presence ([Humber](https://mediaarts.humber.ca/current-students/resources/research/past-projects/can-the-creativity-templates-of-quality-advertising-also-predict-market-effectiveness.html)).

We use the templates as the **twist slots** of the generator:

| Template (versions) | Twist mechanic for a 15–30 s film |
|---|---|
| **Pictorial analogy** (replacement) | A symbol of the benefit replaces the product, or the reverse. The reveal is that "it was the product all along" (like 00-playbook's "sun sets into the bottle"). |
| **Extreme situation** (absurd alternative, extreme attribute, extreme worth) | Show the ridiculous lengths someone goes to without the product, or an attribute pushed to an impossible limit. |
| **Consequences** (extreme, inverted) | Show the far-off or unexpected result of using it, or of *not* using it. |
| **Competition** (attribute, worth, uncommon use) | The product beats something unexpected (not a rival brand), or someone chooses it over something precious. |
| **Interactive experiment** | The viewer is asked to do or notice something (a "pause and look" moment) that proves the claim. |
| **Dimensionality alteration** (time leap, new parameter connection, multiplication, division) | Jump in time, change scale, split the product into parts, or link it to an unrelated dimension. |

**Rules for twists, from humor and incongruity research:**
- Surprise is necessary but not sufficient. An incongruity has to be **easy to resolve**, otherwise it reads as confusing or even fearful (Alden, Mukherjee & Hoyer 2000, *J. Advertising*, via [Khan thesis](https://e-space.mmu.ac.uk/638190)).
- When viewers decode an incongruity, they credit the **advertiser** with competence ([Hoang, Knoeferle & Warlop](https://www.marketing.uni-frankfurt.de/research-talks/calendar-details/cal/event/tx_cal_phpicalendar/2018/04/24/749.html)).
- Extreme incongruity hurt brand memorability, while moderate incongruity did not ([Khan 2024](https://e-space.mmu.ac.uk/638190)).

The resulting rule `[inf]`: the twist must **resolve into the product's single-minded claim**. If the joke works without the product, kill it. This reconciles "clear beats clever": the twist is the *delivery mechanism* of a clear claim.

**Beat sheet for a twist ad** (Setup → Shift → Specific proof → Payoff, [RocketShip HQ](https://www.rocketshiphq.com/mobile-ad-script-structure/)). The timings for 20 s are ours `[inf]`:
- 0–2 s: hook frame. **Plant** one ordinary-looking detail.
- 2–9 s: escalate the expectation (the viewer "knows" where this is going).
- 9–13 s: **turn**. The planted detail changes meaning, and the product is the resolution.
- 13–17 s: one proof or mechanism shot.
- 17–20 s: **echo payoff**: the planted detail returns, plus packshot, tagline and CTA.

### 1.5 Volume and diversity of LLM ideation
- GPT-4 product ideas out-scored MBA students' on real purchase-intent surveys (≈47 % vs 40 %). **35 of the top-40 (top-decile) ideas were AI-made**, and AI quality had higher variance ([Girotra, Meincke, Terwiesch & Ulrich](https://mackinstitute.wharton.upenn.edu/2023/new-working-paper-finds-chatgpt-a-better-innovation-ideator-than-mba-students/), [Wharton Exec Ed](https://executiveeducation.wharton.upenn.edu/thought-leadership/wharton-at-work/2025/06/supercharging-innovation-with-ai/)). Variance plus a good filter is exactly the economics of this machine.
- LLM idea pools are **less diverse** than human groups. Of 35 prompting strategies tested, **chain-of-thought** (first generate many short titles, then develop them) gave the most diverse and most unique ideas. Persona prompts ("think like Steve Jobs") helped only slightly ([Meincke, Mollick & Terwiesch](https://papers.ssrn.com/abstract=4708466)).
- What we do with this `[inf]`:
  - Force diversity structurally: one generation call per grid cell, never "give me 60 ideas".
  - Rotate templates.
  - Embed every logline and merge pairs with cosine > 0.85.

---

## 2. Zero-cost pre-testing: what the evidence supports

### 2.1 Synthetic respondents (LLM consumer panels)

| Study | Finding | What we borrow |
|---|---|---|
| Brand, Israeli & Ngwe, HBS WP 23-062 ([PDF](https://www.hbs.edu/ris/Publication%20Files/23-062_47458a4a-8be2-4b53-a3a3-9b5af20578b1.pdf)) | GPT willingness-to-pay looked realistic; conjoint results were close to real surveys; income conditioning moved WTP the right way. All data cost < $100. The authors frame it as a **filter for dozens to hundreds of ideas**. The follow-up needed fine-tuning to predict truly new features ([MSI](https://www.msi.org/working-paper/using-llms-for-market-research-2/)). | Use the panel as a **filter, not an oracle**. Novel concepts are where the panel is weakest. |
| Maier et al. (PyMC Labs × Colgate), **Semantic Similarity Rating** ([arXiv 2510.08338](https://arxiv.org/abs/2510.08338)) | 57 concept surveys, 9,300 humans. Asking the LLM for a Likert number directly gives a collapsed distribution (mostly "3"; KS similarity 0.26). Letting it **answer in free text and then mapping the text by embedding similarity** to five anchor statements reached **90 % of human test-retest correlation, KS 0.88**. Removing demographics kept the mean right but dropped ρ from 92 % to **50 %**. Image stimuli beat text-only. | Never ask for a number. Use free text plus SSR. **Persona demographics are necessary** for ranking signal. Show *stills*, not just text. |
| Toubia et al., **Twin-2K-500** ([arXiv 2505.17479](https://arxiv.org/abs/2505.17479), [CBS](https://business.columbia.edu/insights/AI-digital-twins-may-pay-off)) | Individual twins reached 72 % accuracy (88 % of test-retest), but **replicated only about half of experimental effects**. Critics note that a midpoint guess gets about 75 % on bounded scales ([Pebblous summary](https://blog.pebblous.ai/report/llm-survey-twin-validation-gap/en/)). | Always ask "compared to what?" Include a **null baseline** (a randomly shuffled concept) and a known-weak control. |
| Gui & Toubia, causal-inference view ([arXiv 2312.15524](https://arxiv.org/abs/2312.15524)) | Changing one variable in the prompt silently changes unstated confounders (flat demand curves). The fix is **unblinding**: state the design and hold everything else explicitly fixed. | Every panel prompt states the same feed context, price, placement and brand familiarity. Only the ad differs. |
| Li et al., "not A Man but Das Man" ([arXiv 2507.02919](https://arxiv.org/pdf/2507.02919)) | Silicon samples are **homogenised** and over-produce the modal answer for a subgroup. | Expect personas to agree too much. Use high temperature, several model families, and *pairwise* choices. |
| Taste study 2026 ([alphaxiv 2606.30085](https://www.alphaxiv.org/abs/2606.30085.md)); social-desirability study ([arXiv 2512.22725](https://arxiv.org/abs/2512.22725)) | **Systematic positive liking bias**; socially approved answers. Neutral third-person wording helped. | Do not trust absolute "would buy" levels, only **relative** ranks. Ask in the third person ("Would someone like you stop?") and ask for the *skip reason* first. |
| Arora, Chakraborty & Nishimura, *J. Marketing* 2025 ([AMA](https://www.ama.org/press-releases/how-the-human-ai-hybrid-approach-can-lead-to-efficiency-and-effectiveness-gains-in-marketing-research/)) | Synthetic interviews were rich, and **human + LLM hybrids beat either alone**. | The client's pick and later live data are the human half of the loop. |

### 2.2 LLM-as-judge: biases and the protocols that beat them
- **Absolute scores are poorly calibrated; pairwise works.** Si, Yang & Hashimoto could not get LLMs to predict review scores, but pairwise "which was accepted?" reached **71.4 %** with Claude-3.5-Sonnet. They ranked thousands of ideas with a **Swiss tournament**: pair similar scores, winner +1, N rounds. The top/bottom separation peaked around 5 rounds ([arXiv 2409.04109](https://arxiv.org/pdf/2409.04109)).
- **Pairwise ranking prompting** beats pointwise and listwise LLM ranking, and can run in linear time with sliding-window variants ([Qin et al. 2306.17563](https://arxiv.org/abs/2306.17563)).
- **Position bias.** It is real, varies by judge, and is worst when the two candidates are close in quality. The fix is to run every pair in **both orders** and count a flip as a tie ([Shi et al. 2406.07791](https://arxiv.org/abs/2406.07791)).
- **Self-preference.** GPT-4 showed the strongest bias. Its root cause is **low perplexity**: judges favour text that is familiar to them, whoever wrote it ([Wataoka et al. 2410.21819](https://arxiv.org/abs/2410.21819)). Self-preference ranges from −38 % to +90 % across judges ([UDA 2508.09724](https://arxiv.org/pdf/2508.09724)).
- **Juries beat judges.** A panel of smaller models from **disjoint families** (PoLL) correlated better with humans, showed less intra-family bias and cost 7× less than one GPT-4 judge ([Verga et al. 2404.18796](https://arxiv.org/abs/2404.18796)).
- **Hard limits.**
  - Zero-shot frontier LLMs (GPT-4o, Claude 3.5, GPT-4V) were at **~50 %, i.e. chance**, at picking which of two real ad images had higher CTR. A specially trained reward model reached only 56–59 % ([arXiv 2502.06823](https://arxiv.org/pdf/2502.06823)).
  - Humans still beat LLMs at ranking New Yorker caption-contest humor ([Hessel et al., ACL 2023](https://aclanthology.org/2023.acl-long.41)).
  - So `[inf]`: the panel can filter **clarity, relevance, persuasion logic, comprehension and objection handling**. It cannot reliably predict **click-level performance or how funny a joke lands**. Present results to the client as "strongest strategic candidates", never as "predicted winners".

### 2.3 Commercial pre-testing (what the pros measure)
- **System1 Test Your Ad.** Viewers pick one of 7 Ekman emotions (or neutral) on a pictorial scale (FaceTrace; self-report, not camera coding). The tool also measures emotional intensity and **brand fluency** (how fast the brand is recognised). It outputs a **Star rating (1–5.9, long-term growth)** and a **Spike rating (short-term sales)**. It is validated against the IPA databank and, for digital, against Pinterest in several markets. Only about 1 % of ads reach 5 stars. System1's own position is that stated purchase intent predicts behaviour poorly ([MrWeb](https://www.mrweb.com/drno/news35073.htm), [The Drum](https://www.thedrum.com/news/best-ads-august-new-balance-gatorade-and-hershey-s), [Annual report 2026](https://system1group.com/wp-content/uploads/2026/08/2026_Annual_Report_and_Accounts.pdf)). → We copy two of these signals: **emotion intensity** and **brand-ID speed**.
- **Kantar LINK AI.** A model trained on 260–300k LINK tests. It works on **finished films, animatics and statics**, in under 5 minutes. Kantar claims "comparable to survey" for more than 7 in 10 ads and an 8/10 hit rate on top-30 % ads. Kantar's own caveat: never validate AI on a handful of ads ([Kantar](https://www.kantar.com/inspiration/agile-market-research/can-ai-really-decode-creative-effectiveness)). → Its metrics are branded impact, enjoyment and persuasion, which become our rubric axes.
- **Attention heatmaps.** Neurons claims 95 % pixel-level and 98 % AOI agreement with eye tracking on 100–150 people. This is vendor-run validation ([Neurons](https://knowledge.neuronsinc.com/how-neurons-ai-works)). We found no public validation for Dragonfly AI. → Optional paid add-on for the final stills. A free proxy is a "5-second glance" LLM-vision question: "What do you see first? Is the product/brand visible?" `[inf]`.
- **Storyboards and animatics.** Reynolds & Phillips (JAR; 240 ads, 5,500 viewers) found that the strategic assessment of animatics matched finished films ([WARC](https://www.warc.com/newsandopinion/news/pretesting_animatic_tv_ads_can_be_effective/42827)). Zappi finds that animatics match finished films on reach but **under-score on emotion** ([Zappi](https://learn.zappi.io/article/172-animatic-guidelines)). → Rough stills are valid for testing *strategy*. Judge emotion on stills generously and compare stills only against stills.
- **Live proxies once money is spent.** Hook rate (3-s views ÷ impressions): about 25–35 % is a typical Meta target, and hold rate is about 18 % median ([Motion glossary](https://motionapp.com/library/glossary/thumbstop-rate), [Jetfuel](https://jetfuel.agency/creative-performance-metrics-for-dtc-video-ads-hold-rate-thumbstop-and-thruplay-benchmarks-2026/)). Barry Hott warns these must be read **for relevance**.

---

## 3. The protocol (runs with an LLM and about 18 cheap stills)

### Stage 0. Intake and research (≈20 min of agent time)
1. **Product facts sheet:** what it is, ingredients or materials, price, how it's sold. No invented claims.
2. **Review audit** (own or competitor reviews) → the five buckets, plus verbatim phrases.
3. **Personas: 6.** Rank them by review frequency × intensity and keep 4 *buyers* plus 2 *skeptics*.
   - Persona card: name, age, income band, life context, situation/JTBD, deepest desire, top objection, media diet, verbatim phrase, scroll mood ("tired, 23:40, in bed").
   - Use the demographic fields: SSR showed ranking signal collapses without them.
4. **Territories: 3 anchors.** Premium default: 2 desire + 1 pain. Write the single-minded claim and the mechanism (per 00-playbook).

### Stage 1. Generate 60 concepts (diverge)
- Grid: **3 territories × 4 buyer personas = 12 angles**. For each angle generate **5 concepts**, each forced into a different template from §1.4 plus "big-idea literal shot" (00-playbook) → **60 loglines**.
- One call per angle. CoT pattern: list 10 raw titles → pick the 5 most different → develop each.
- Use the **generator model family A** at high temperature.
- Concept card (≤90 words):
  - territory / persona / template
  - logline (1 sentence)
  - planted detail → turn → payoff
  - hook frame (visual + overlay + sound)
  - proof beat
  - punchline / tagline (≤7 words)
- Dedupe by embedding (cosine > 0.85). Expect **~45** concepts to survive `[inf]`.

### Stage 2. Hard gates (pass/fail, single cheap judge)
Kill a concept if it: violates compliance (01/02, FTC testimonial rule); needs talking heads, lip-sync, small readable text or complex hand/liquid physics (02-niches); **has a twist that works without the product**; needs a claim >7 words; or can't be told in ≤6 shots. Expect ~30 survivors.

### Stage 3. Rubric pre-score (jury, pointwise, used only to prune to 16)
Normalise first (anti-self-preference):
- A **neutral rewriter from model family C** rewrites every card into the identical template, length and plain register. This removes stylistic "familiarity" (the perplexity cause in Wataoka) `[inf]`.
- Labels are random IDs.

Score 1–5 with anchored descriptors. Jury = 2 different model families (B and C, never A). Each judge writes its rationale *before* the score.

| # | Criterion | Weight | What a 5 looks like | Source logic |
|---|---|---|---|---|
| 1 | **Hook stopping power and relevance** | 20 | The first frame is sensory or odd *and* self-selects the persona | Motion triggers; Hott relevance |
| 2 | **Claim clarity after one view** | 15 | A cold viewer can state the product, the benefit and the action | Hott "clear > clever"; 00-playbook QC |
| 3 | **Twist quality** (surprise × ease of resolution × product is the resolution) | 15 | "Didn't see it coming, and *of course*" | Incongruity research; templates |
| 4 | **Emotional intensity** (one peak) | 12 | A strong single emotion, not mild "interest" | System1 Star logic |
| 5 | **Brand linkage / fluency** | 12 | The brand or distinctive asset is unmissable by 3 s and owns the payoff | System1 fluency; Kantar branded impact |
| 6 | **Persuasion: objection answered + mechanism shown** | 10 | The top objection is answered visually | Creative Strategy Engine |
| 7 | **Distinctiveness vs category** | 8 | It would not fit a competitor's logo | Hook rule "could fit any product" |
| 8 | **AI-production feasibility and cost** | 8 | Every shot is in our proven recipes (09–14) | Library |

Weighted score = Σ(w × s)/5, out of 100. Keep the **top 16**. Also force-keep the best of any template or territory with zero survivors, so the tournament is not homogeneous `[inf]`.

### Stage 4. Persona-panel Swiss tournament (the "A/B test without ad money")
**Stimulus.** Each concept is rendered as a 5-beat text storyboard (later, stills). Each persona gets the *same* unblinded context: "You are scrolling Instagram Reels at [time/mood]. Two sponsored posts appear one after the other. Same price [€X], same brand familiarity (unknown). Nothing else differs." (Gui & Toubia unblinding.)

**Match prompt** (free text first, choice last):
1. "Describe in one sentence what you'd do at second 2 of each ad, and why."
2. "Which would make you stop? Which would you remember tomorrow? Which would make you want it?"
3. "Final: A or B overall."

**Panel per match.** 3 personas (2 buyers + 1 skeptic, rotated across all 6) × **2 orders (AB/BA)** × **2 judge families (B, C)** = 12 votes. A flip across orders = a tie (Shi et al.). Generator family A **never votes**.

**Format.**
- 16 concepts, **5 Swiss rounds** (Si et al. peak) = 40 matches ≈ 480 calls.
- Fit **Bradley-Terry** strengths on all votes (e.g. Python `choix` or a 30-line MM fit).
- Bootstrap 200× over votes for a 90 % CI.
- Concepts with overlapping CIs are "statistically tied". Break ties with the rubric score.

**Secondary SSR read** (for the client deck, not for ranking): for each top-8 concept × each persona, ask "How likely are you to buy after seeing this?" in free text. Map the text with **SSR**: embed it, compute cosine to 5 anchor statements, normalise to a distribution, and average over 2–3 anchor sets. Report a **relative index** vs the panel mean, never as an absolute "48 % will buy" (positive-liking bias).

Example anchors (1→5): "I would not buy this." / "Probably not for me." / "Not sure either way." / "I'd probably try it." / "I'd definitely buy this."

**Sanity controls inside the bracket** `[inf]`:
- (a) A **deliberately weak control**: generic product-on-table, no twist. It must finish in the bottom quartile.
- (b) A **shuffled control**: the hook from one concept with the payoff of another. It must lose.
- (c) **Self-preference check**: if family B's win-rate for concepts it rewrote or polished exceeds family C's by >15 points, drop B's votes.

If a control places in the top half, the panel is not discriminating. Fix the prompts before trusting the rank.

### Stage 5. Stills round (top 6 → ~18 stills, the only spend)
For the top 6 by Bradley-Terry, generate **3 key frames each**: hook frame, turn frame, payoff/packshot frame. Use the cheapest still model in 12-higgsfield, ≈ $0.30 × 18 ≈ $5.40.

Run three tests:
1. **Re-run the tournament multimodally** with the same panel protocol on stills plus a 1-line VO/overlay per frame (SSR showed image stimuli beat text). Use 3 rounds.
2. **Cold-viewer comprehension test.** A fresh judge (family C, no brief) sees only the 3 frames and answers "What is the product? What's the one benefit? What's the twist?" Score the % correct across 5 samples. **Below 60 % → rework or drop** `[inf]`.
3. **5-second glance test** on the hook frame: "What do you notice first? Where is the brand?" This is a free proxy for attention heatmaps. Neurons/Dragonfly is an optional paid add-on.

Score emotion on stills leniently and comparatively. Animatics under-score on emotion (Zappi).

### Stage 6. Select the final 3 (diversity-constrained)
Pick the top 3 by final Bradley-Terry, with these constraints:
- No two share the same **territory**.
- No two share the same **template**.
- At least one is the "safe-clear" storyline (highest comprehension) and one is the "bold-twist" storyline (highest twist score).

If a constraint binds, swap in the next-ranked concept. This mirrors Andromeda logic: the client chooses between *different bets*, not three versions of one bet `[inf]`.

### 3.1 What the client sees (per storyline, one page or slide)
1. **Title + one-line idea** (≤12 words) and the **punchline/twist line** in large type.
2. **Territory → persona → angle** (one line each), plus the single-minded claim.
3. **The 3 stills** (hook / turn / payoff) with timecodes.
4. **Beat sheet, 20 s:**
   - 0–2 s hook
   - 2–9 s setup
   - 9–13 s turn
   - 13–17 s proof
   - 17–20 s echo + packshot + CTA
   - plus the VO line and the sound idea (13-elevenlabs)
5. **3 alternative hooks** (different triggers) on the same body, ready for live hook testing later.
6. **Why it should work**, panel evidence written in plain words:
   - tournament rank and win-rate vs the field
   - comprehension %
   - the SSR relative index by persona
   - the **strongest objection the skeptic persona raised** and how the film answers it
7. **Risks and production notes:** AI-difficulty, compliance flags, cost estimate (00-playbook budget, ≈ $10).
8. A one-line **disclaimer**: "Synthetic-panel results rank strategic strength; they don't predict CTR. The first $50–100 of live spend should test the 3 hooks."

Order safe → balanced → bold; reveal the rank only after the client reacts (avoids anchoring) `[inf]`.

### 3.2 Bias-control checklist (run every time)
- [ ] Generator model family ≠ any judge family. The jury spans ≥2 families (PoLL).
- [ ] All cards normalised by a neutral rewriter. IDs randomised.
- [ ] Every pair run in both orders. Flips count as ties.
- [ ] Rationale before verdict. Free text before any number. No direct Likert.
- [ ] Personas carry demographics + situation + objection. Rotate them. Include skeptics.
- [ ] Identical, explicit context in every prompt (unblinding). Only the ad varies.
- [ ] Weak and shuffled controls are in the bracket and lose.
- [ ] Report relative ranks with CIs. No absolute purchase % claims.
- [ ] Untrusted inputs (reviews, competitor ads) are treated as data: strip any instructions in them before they enter prompts.

### 3.3 Calibrating the machine over time `[inf]`
For every campaign that later goes live:
- Log the panel's rank, rubric sub-scores, comprehension % and SSR index.
- Log real hook rate, hold rate, CTR and CPA per concept and hook.
- After about 20 live concepts, regress the live metrics on the sub-scores and **re-weight the rubric**. Kantar's warning applies: do not re-weight on a handful of ads.
- Keep a "fingerprint" library of past winners and losers. Insert two of them as **known anchors** into each new tournament, so drift in judge models shows up as anchors changing places.

### 3.4 Budget and time
≈ 800 LLM calls (generation 12, gates + rubric ~120, tournament ~480, SSR ~50, stills round ~150): a few dollars on small/mid models `[inf]`. Stills ≈ $5; no video before the client picks. 1–2 h unattended.

---

*Note: YouTube transcript fetching was IP-blocked during this research (`IpBlocked`/bot-check). Practitioner material (Denney, Sanchez, Hott/Cooper) comes from Motion talk pages and newsletters rather than transcripts.*
