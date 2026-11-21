# 39 · Story-scroll site: the VXO home page as one continuous take

Research brief, 2026-10-08, for the site redesign (`site/`, Astro + GSAP + Lenis). Founder's brief: "The site doesn't look good enough. Make it a STORY, smoother. As you start scrolling the character comes up from below; before you reach it, it tells you it's here; you keep scrolling and it arrives. Think like a salesman. Make the characters' lips move. Luxury."

This file **extends** `29` (strategy), `31` (engineering), `33` (master plan) and `30` (mascot). Where it conflicts with `33` on the **home-page order and character beats**, this file wins. Copy rules, honesty rules, prices and the form spec from `33`/`29` still apply. Tags: `[S#]` = source at the end, `[inf]` = our inference, not evidence. No statistic here is invented; where we found no evidence we say so.

---

## 0. The idea in one screen

**The page is shot like our product: one take, no cuts.** VXO's signature is "One take. No cuts." (`site/src/data/site.json`). So the home page is one continuous camera move. Eight acts, each a scene, joined by camera moves instead of hard section breaks. Otto (director) and Vee (producer) are the crew guiding a founder through the shoot of *their* product. The founder's product is the hero; the crew are guides (StoryBrand, `29` §2.4).

Ten rules:
1. **H1, offer and CTA are on screen at 0 s.** The story adds to the sales page. It never gates it (NN/g: 57 % of viewing time is above the fold [S1]).
2. **No more than ~30 % of the scroll is pinned. Normal scrolling between pins.** No horizontal hijack (NN/g scrolljacking findings [S2]).
3. **Key copy never lives *only* inside a scrubbed animation.** Every headline lands and stays readable [S2].
4. **Characters anticipate, then arrive.** Peek, caption, rise. Three beats, driven by scroll (§2.3).
5. **Voice only after a tap on "Sound on".** Scrolling is not a user activation in the HTML spec, so it can never unlock audio [S3][S4]. Captions are always on.
6. **One line per act, maximum. Never replay a line.** At least two acts have no character, so the crew stays special (Clippy lesson [S5]).
7. **Honest:** spec films say "invented brand", AI is disclosed, no clients, logos, testimonials or stats that we don't have (`28` §9, `29` §2.3).
8. **Luxury = restraint.** One accent colour, generous space, slow cinematic reveals and fast UI feedback (§4).
9. **60 fps or cut it.** On mobile we drop the scrub before we drop the frame rate (§1.4).
10. **Reduced motion gets the same story, told in stills and captions** (§1.5).

---

## 1. Scrollytelling patterns that feel luxurious and smooth

### 1.1 What the reference sites do

| Reference | Pattern | What we take `[inf]` unless cited |
|---|---|---|
| **Apple product pages** (AirPods Pro, iPhone) | Pinned canvas + pre-rendered image sequence mapped to scroll (147 JPEG frames in the AirPods hero, per GreenSock's reconstruction) [S6][S7]. Text arrives in short delayed, eased reveals; the type carries the page and the visuals support it [S8] | Scrubbed product moment in Act III. Headlines are typography-first, and the film is supporting |
| **Lusion — Oryzo AI** (Awwwards Site of the Month, Apr 2026; Developer Award) | A whole cinematic product story built around an ordinary cork coaster: a mundane object treated as a legend [S9][S10] | Exactly our pitch: an ordinary product filmed like a legend. One object, one world, one camera |
| **Igloo Inc** (Awwwards SOTY 2024, see `29` §1) | Immersive WebGL world. A reviewer didn't realise the ice blocks were clickable | Say the action in words ("Pick a film"). Never rely on discoverability |
| **Hermès** (Jan 2026 homepage) | 12 hand-drawn illustrations by Lina Merad, one per section, with creatures interacting with the products. Coverage reads it as editorial, not a hard-sell showcase, and as a "human-made" answer to AI imagery [S11][S12] | One illustrated or character "host" per section is luxury-compatible when it plays *with the product*. Since we are openly AI, our counter is radical honesty plus craft (BTS) |
| **Aesop** | Neutral grotesk (reported as Suisse Int'l) with a humanist serif kept for the wordmark and display. Copy reads "like a label rather than an advertisement"; restrained scale [S13][S14] | Calm, exact, full-sentence copy. A small UI type scale beside large display moments |
| **Bottega Veneta** | Identity without logos: material (intrecciato) carries recognition, and campaigns have almost no copy [S15] | Let the films carry the brand. The VXO wordmark stays small |
| **darkroom.engineering** (ex-Studio Freight) | Built Lenis, now the de facto smooth-scroll layer for award sites: lerp 0.1 by default, smooth wheel, native touch [S16] | We already ship Lenis. Configure it, don't replace it (§1.4) |
| **NYT "Snow Fall"** (2012) | Usually cited as the origin of scrollytelling: text + media that change as you read [S17] | Chapters with titles, so the scroll feels like a story and not a long page |

### 1.2 The pattern toolkit (and where VXO uses each)

| Pattern | Mechanic | Luxury setting `[inf]` | VXO act |
|---|---|---|---|
| **Pinned scene** | `ScrollTrigger` `pin:true`, `scrub`, an `end` of 100–200 % of viewport height | ≤ 2 pinned scenes on desktop, ≤ 1 on mobile. Never pin the form | I (hero take), III (frame → film) |
| **Scrubbed video** | `video.currentTime = progress × duration` from a scrubbed timeline. Needs an all-intra encode (§1.4) [S18][S19] | 4–6 s of footage stretched over 150–200 vh: slow, viscous, expensive | I, III |
| **Image-sequence canvas** | Apple-style frames drawn to `<canvas>` [S6][S7] | Fallback for iOS if video seeking stutters. 60–90 WebP frames at render size | III (mobile fallback) |
| **Character entrance** | Keyed clip (stacked alpha, `31` §4) translated by scroll: peek → caption → rise | The rise is scroll-linked (feels physical), and the talk clip plays on a trigger (time-based, so lip-sync never scrubs) | I, II, V, VII, VIII |
| **Parallax depth** | 2–3 layers moving at 0.9× / 1× / 1.1× | Tiny deltas (≤ 8 % offset). NN/g: parallax "often create[s] usability issues" and triggers vestibular problems [S20], so keep it decorative and turn it off under reduced motion | Film tiles (IV), backgrounds |
| **Typographic reveal** | Line-by-line mask (`overflow:hidden`, `yPercent:100 → 0`), `stagger` 0.08 s, ease-out | Serif display, one line at a time, 0.9–1.2 s. Text then **stays put** | Every act headline |
| **Scroll fading** | Animation *triggered* at a point without changing scroll speed; NN/g separates this from scrolljacking [S21] | Default for everything not explicitly pinned | II, IV–VIII |
| **Act/chapter structure** | Small sticky chapter mark ("I · The take") + a thin progress line | Film-slate language: "Scene 3 · Take 1". A map *and* an escape hatch (NN/g: sticky nav rescues lost users [S2]) | Global |

### 1.3 Evidence on scroll hijacking (why our pins are short)
NN/g's testing [S2]: most participants were "at least mildly disoriented". Long scrolljacks were read as bugs. Task-oriented users had little patience. The guidelines: keep them short, mix in normal scrolling, keep important text out, don't switch vertical → horizontal, avoid them on mobile, put them below the fold, and give sticky navigation. Acceptable when it "gradually adds supporting information to lessen cognitive load and support storytelling." → Our two pins are storytelling pins. Act I's pin is short and the H1 and CTA are readable at frame 0; on mobile Act I does not pin (§1.4).

### 1.4 Performance rules (60 fps on a mid-range phone)

**Scrubbed video encoding** [S18][S19]:
```bash
# all-intra (every frame a keyframe) at the element's largest rendered size, no audio
ffmpeg -i take.mov -vf "scale=1280:-2,fps=30" -c:v libx264 -crf 23 -g 1 -pix_fmt yuv420p -an -movflags +faststart take.scrub.mp4
ffmpeg -i take.mov -vf "scale=1280:-2,fps=30" -c:v libvpx-vp9 -crf 32 -b:v 0 -g 1 -row-mt 1 -pix_fmt yuv420p -an take.scrub.webm
# mobile: 720 wide, 24 fps, 4–5 s max. Compare -g 1 vs -g 6 (a smaller file; one CodePen reports it as enough) on a real iPhone
```
- All-intra costs size. At ~1280 px / 30 fps one write-up reports ~8 MB (MP4) and ~13 MB (WebM) versus 1–2 MB for a normal encode, and >100 MB is possible at 1080p [S18]. → Keep scrub clips **4–6 s**, never above render size.
- `preload="auto"`, `muted`, `playsinline`. Never call `play()` on a scrub video. Wait for `loadedmetadata` before setting `currentTime` [S18]. Only the *next* pinned scene preloads. Start the fetch when the previous act enters (IntersectionObserver `rootMargin: 100%`) [inf].
- Smooth the seek: write `currentTime` inside the GSAP ticker from a lerped target (`scrub: 0.6–1`), not on every scroll event [S22][inf].

**Scroll engine** (`lenis@1.3.x` + `gsap@3.15`, both already in `package.json`):
- One RAF driver: `lenis.on('scroll', ScrollTrigger.update)`, `gsap.ticker.add(t => lenis.raf(t*1000))`, `gsap.ticker.lagSmoothing(0)` [S16].
- **Touch devices: native scroll (no Lenis smoothing, `syncTouch:false`)**. GSAP staff advise disabling Lenis on touch when it lags, and never mixing it with `normalizeScroll` [S23]. `syncTouch` is unstable below iOS 16 [S16].
- `data-lenis-prevent` on the form, modal player and any inner scroller [S16].
- Animate **only `transform` and `opacity`**. No `filter: blur()` on scroll, no layout-affecting properties, `will-change` only while pinned [inf].
- Decoders: **≤ 3 playing videos on phones, ≤ 5 on desktop**, via the existing `MediaManager` (`31` §4.5). Character clips release their `src` when off-screen.
- CSS scroll-driven animations (`animation-timeline: view()`) are fine for simple reveals as progressive enhancement: Chrome 115+, Safari 26. Firefox still keeps it behind a pref per Mozilla staff, so wrap it in `@supports` [S24].
- Budget: LCP is the hero poster (a static frame of the take), never a video. Field target p75 LCP < 2.5 s, INP < 200 ms (`31` §6.1).

### 1.5 Reduced motion and accessibility
- WCAG 2.3.3 (AAA): non-essential motion *triggered by interaction, including scroll* must be disableable. `prefers-reduced-motion` is a sufficient technique; parallax is the W3C's own example [S25]. WCAG 2.2.2 (A): auto-moving content > 5 s needs pause (`29` §2.2).
- Implementation: `gsap.matchMedia()` with `{reduce: "(prefers-reduced-motion: reduce)"}`. In `reduce`, create **no pins, no scrubs**. Acts become stacked sections. Scrub videos are replaced by their poster plus a "Play" button. Characters appear as a still frame plus caption with no rise [S26].
- Site-level "Motion: on/off" toggle in the header as well (W3C lists a user setting as sufficient) [S25].
- Captions are real text in the DOM (`aria-live="polite"` only for the line that just triggered). Every character clip is `aria-hidden`.

---

## 2. Character-guided narrative

### 2.1 What the evidence says about guides
- **The persona effect** (Lester et al., CHI '97, 100 students): a lifelike agent improved how learners *perceived* the experience, even when it was not expressive [S27]. Later studies are mixed on which features matter [S27]. → A guide raises warmth and perceived help. It is not proof it raises conversion; test it (`33` kill switches).
- **Clippy, the counter-example.** Users hated it for interrupting at the wrong time on shallow triggers and for being hard to dismiss. Microsoft's own PM wrote that a 50/50 split was "not good enough" when the negative half felt strongly, and it was turned off by default. A Stanford thesis (Swartz 2003) blamed both concept and implementation: agents must keep users in charge and follow social etiquette [S5].
- **Uncanny valley and FTC**: stay stylised and never let a character endorse (`29` §2.3).
- **Guide-led scroll tours** (e.g. auto-narrated step guides that read each step aloud and glide to the next, with pause/replay/jump) [S28]: the user still controls the pace. That is the model, not a "presenter" who talks over the page.

### 2.2 When characters speak
| Rule | Why |
|---|---|
| **Captions first, always.** Each line appears as a subtitle-style caption next to the character the moment its trigger fires | Works muted, which is the default state [S3] |
| **Voice only after "Sound on"**, a persistent pill bottom-left ("Sound on · meet the crew"). Tapping it plays Vee's intro line *inside the click handler* (synchronous `play()`, `31` §4.5) | Autoplay with sound needs user activation; scroll/wheel are not activation events [S3][S4]. A swipe's `touchend` is on the spec list, but browsers treat a touch that scrolls as a cancelled pointer [inf], so don't count on it |
| **Speak on arrival, not on approach.** The line fires when the character's rise completes, and only if scroll velocity is low (e.g. `ScrollTrigger.getVelocity() < 1500` px/s) | Skimmers aren't interrupted (Clippy's timing failure) [inf] |
| **Once per session per line.** Scrolling back up shows the caption, silent | Repetition = gimmick fatigue [inf] |
| **≤ 8 words, ≤ 3 s of audio** | `29` §6 rule; lip-sync is cleanest on short lines (`30` §2.5) |
| **Host, never reviewer** | FTC Endorsement Guides apply to virtual influencers (`29` §2.3) |
| **"Mute the crew"** in the same pill: hides captions *and* characters (the page still works) | Control, Swartz's first lesson [S5] |

### 2.3 Anticipation: the founder's "it tells you it's here" beat
Three scroll-linked beats per entrance, built with one ScrollTrigger timeline per character entrance `[inf]`:

1. **Peek (0–25 % of the entrance range).** The top 12–18 % of the character rises above the bottom viewport edge: Otto's hat brim and moustache tips, Vee's stopwatch hand. A looped "peek" clip (eyes up, small twitch). A caption chip appears above it: **"Down here. ↓"** (Otto) / **"Hold on, coming in."** (Vee). Arrow nudges 4 px, twice, then stops.
2. **Hold (25–60 %).** Content of the act scrolls normally. The character stays docked at the edge (`position: fixed` inside the act's bounds), so it feels like it's waiting for you.
3. **Arrive (60–100 %).** The rise clip is scroll-scrubbed into its mark (the rise is mostly body translation, so scrubbing it reads as physical). On completion, swap to the talking clip (time-based playback) and fire the line.
Exit: characters leave by **sinking below the frame** (Otto) or **walking off-frame right** (Vee). Exits use ease-in and are shorter than entrances (NN/g: entrances ~300 ms vs exits ~200–250 ms in UI; we scale both up for cinema) [S29].

### 2.4 Avoiding gimmick fatigue (budget)
- Characters appear in **6 of 9 scenes**. Acts IV (work) and VI (proof) are character-free on purpose: the films and the facts speak.
- Total spoken lines on the home page: **≤ 10** (including two optional ones).
- The crew **never covers** a headline, a price or a CTA. Safe zone: bottom-right 28 % on desktop, a bottom strip ≤ 22 vh on mobile, and the caption sits above the character.
- After the form is submitted, characters go quiet for the session except the success line.
- Kill-switch metrics (add to `31` §8 events): `crew_muted` rate, scroll-depth to Act VII, `frames_submit`. If `crew_muted` > ~15 % or depth drops versus the crew-off variant, cut lines first, then entrances [inf].

---

## 3. Sales architecture of a story site

### 3.1 Acts mapped to the buyer journey
| Journey stage | Act | Job | Primary CTA |
|---|---|---|---|
| Hook / message match | I · The take | Say what we sell + show it in 1 s | Get my 5 free frames |
| Problem | II · The tired ad | Name the pain in their words | (soft) See what we'd make |
| Wow demo | III · One photo in | Plain photo → frame → film, scrubbed | Inline mini-form (email + product URL) |
| Range / work | IV · Four films | Spec films, labelled invented | Watch with sound / Get frames |
| How it works | V · The schedule | 3 steps, dated | Start with step 1 |
| Proof + risk reversal | VI · What you risk | No logos, honest. Frames free, 50 % on approval, inline objections | Get my 5 free frames |
| Offer | VII · The price | Three tiers high → low, one recommended | Choose Premiere / Start with frames |
| Close | VIII · Your product next | Full form + crew | Send my product |

### 3.2 Evidence that shapes it
- **Attention:** 57 % of viewing time above the fold, 74 % in the first two screenfuls (NN/g, 130k fixations) [S1]. → Offer + CTA in Act I; the story *rewards* scrolling, it doesn't *require* it.
- **Speed:** 53 % of mobile visits abandon if > 3 s (Google 2016, `29` §2.1). → Hero LCP is a still.
- **Message match:** landing headline should mirror the ad that was clicked (Unbounce definition [S30]). The widely cited "+212 %" message-match lift is a single Disruptive Advertising/Moz case we could not verify [S31], so treat it as directional. → Act I H1 swaps by `utm_content` (same layout, 3 variants max; see §5 Act I).
- **Readability:** Unbounce's 2024 benchmark: median landing-page conversion 6.6 % across industries [S32]. A secondary summary says pages at 5th–7th-grade reading level converted at 11.1 %; we could not confirm it on Unbounce's own page [S32]. → Short words, short lines anyway.
- **Forms:** fewer fields usually help, but less than famous anecdotes claim. Making phone optional doubled one form's conversion. One test *lost* 14 % by removing wanted fields (CXL, `29` §2.5). Baymard: 22–26 % of shoppers have abandoned checkouts for being too long or complex [S33]. → Two-step form, step 1 = email + product URL.
- **Sticky CTA:** published tests are mostly e-commerce add-to-cart and vendor-reported: +6.2 % CR (AFTCO), +~10 % (PerTronix, not significant), +16 % (apparel, two-week read), an outlier +253 % mobile orders. Desktop is often flat [S34]. → Ship a sticky CTA, mobile first, and A/B it. Expect single digits, not miracles.
- **Risk reversal:** we found **no controlled study** on guarantees for service businesses; the evidence is practitioner anecdote [S35]. → Our risk reversal is structural rather than a promise: free frames before money, 50 % on approval, two revision rounds. Say it plainly and don't call it a "guarantee" unless the terms are written.
- **Tiers:** the decoy/compromise effect is real in lab studies (Huber, Payne & Puto 1982). SaaS numbers ("60–70 % pick the middle") are practitioner benchmarks, not studies [S36]. → Three real tiers, high → low, Premiere recommended (already in `pricing.json`).
- **Scroll hijack cost:** see §1.3. Pins are short; the sticky CTA and chapter nav are the escape hatches [S2].

### 3.3 CTA placement and the sticky CTA
- **In-flow CTAs:** Act I (hero, two-yes), end of III (inline mini-form), IV, V, VI, VII (per tier), VIII (full form). That is seven, roughly one per screenful after the demo `[inf]`.
- **Sticky CTA:** a pill "5 free frames →" appears once Act I's CTA scrolls out of view. On mobile it is a bottom bar 56 px tall, safe-area aware, with "Sound" on its left. It **hides** while any in-flow CTA or form is in view (no double CTAs) and while the Act III pin is scrubbing (no covering the demo). It opens `/frames` or scrolls to Act VIII (A/B).
- **Header:** wordmark + "Work · Pricing · How we use AI" + "Get 5 free frames". Always present (sticky nav = escape hatch [S2]).

### 3.4 Lead magnet placement ("5 free frames")
1. **Act I** button → scrolls to Act VIII form (desktop) or `/frames` (mobile; test).
2. **Act III inline mini-form** right after the wow moment, when desire peaks `[inf]`: `Email` + `Product page URL` + [Get my 5 free frames]. Submitting goes to `/frames/thanks` step 2 (qualifiers, optional photo upload, `29` §5).
3. **Act VIII full form:** the same two fields, the photo upload optional, and the "what happens next" timeline next to it.
4. **Exit-intent** (desktop only, once): "Before you go: 5 frames of your product, free." Vee's pop (existing `vee_pop_*`).

### 3.5 Objection handling inline (not only in the FAQ)
Place a single-line "objection chip" exactly where the doubt arises; tap to expand 2–3 sentences `[inf]`:
| Where | Objection | Chip copy |
|---|---|---|
| Act I under CTA | "Is it really free?" | "Free means free. No card, no call." |
| Act III after demo | "Will it look like *my* product?" | "We build from your photos. Your label, your shape." |
| Act IV | "Are these real clients?" | "No. Invented brands, made to show the range." |
| Act V | "AI disclosure on Meta/TikTok?" | "We label AI and hand you the right settings." (link `/ai`) |
| Act VI | "Who owns it?" | "You do, for your digital ads, organic and site." (from `pricing.json` `allPlans`) |
| Act VII | "What if I hate the film?" | "Second half is due on approval. Two revision rounds." |

---

## 4. Luxury visual language

### 4.1 What makes a site read "expensive" (evidence + inference)
- **White space signals prestige.** Pracejus, Olsen & O'Guinn (*JCR* 2006): consumers and creative directors share the reading of conspicuous white space as refined/upscale. A 2012 survey of 31 agency creative directors lists "convey brand prestige" among its uses [S37]. → Generous spacing is an argument, not decoration.
- **Restraint over decoration.** Aesop opts out of Didones and scripts; its neutral sans and label-like copy *is* the luxury signal [S13]. Bottega: material over logo [S15]. Hermès: one crafted illustration per section, editorial over showcase [S11].
- **Human craft is the new luxury signal** in the AI era (coverage of Hermès [S12]). → We can't claim "human-made". We counter with **process proof**: show the frames, the takes, the director's notes (BTS in Act VI) `[inf]`.
- **Cheap tells to avoid** `[inf]`: stock gradients, more than one accent colour, bouncy/elastic easing, spinning loaders, emoji, exclamation marks, countdown timers, "limited spots!!!" banners, auto-carousels, generic 3D blobs, every element animating.

### 4.2 Tokens (keep the existing ones in `site/src/styles`)
- **Colour:** warm ink `--ink-0 #0f0e0d` → `--ink-3`, bone text `--text #ede6da`, one accent `--brass #b08d57` (hover `--brass-hi`). Oxblood only for Vee's stopwatch and the single "recording" dot. Ivory `--ivory #f3ede2` inverted section **once** (Act VII pricing) as a "lights up" moment `[inf]`.
- **Type pair:** display `Instrument Serif` (already loaded) for H1/H2 and the act titles, italics for one word per headline at most. UI/body `Inter Variable`. Paid upgrades if budget allows: a contrast serif (e.g. GT Super / Canela class) + a Swiss grotesk (Suisse/Neue Haas class) `[inf]`.
- **Scale:** H1 `clamp(2.6rem, 7vw, 6.5rem)`, line-height 1.0–1.05, tracking −0.01 em. Body 16–18 px, 1.55. Captions 13–14 px Inter, uppercase-free. Eyebrows 11–12 px, letter-spacing +0.12 em, brass.
- **Space:** section padding `clamp(96px, 16vh, 200px)`. Max text measure 32 ch for headlines, 60 ch for body. One idea per screen.
- **Grain:** a static 2–3 % film grain PNG overlay on ink sections (not animated: animated grain costs GPU) `[inf]`.

### 4.3 Motion
| Element | Duration | Ease |
|---|---|---|
| UI feedback (buttons, toggles, chips) | 100–200 ms | ease-out (NN/g: ~100 ms for simple feedback) [S29] |
| Modals/player open | 250–300 ms in, 200 ms out | ease-out in, ease-in out [S29] |
| Headline line reveal | 900–1200 ms, stagger 80 ms | `expo.out` / `cubic-bezier(0.16,1,0.3,1)` |
| Image/film reveal (clip-path or scale 1.06 → 1) | 1200–1600 ms | `power3.out` |
| Character rise (scroll-linked) | scrub 0.8 | `none` inside scrub; the ease comes from the lerp |
| Section-to-section "camera move" | scroll-linked | — |
NN/g's 100–400 ms ceiling is for *UI* motion [S29]. Cinematic reveals are deliberately slower because they are content, not controls, and they never block input `[inf]`. No bounce, no elastic, no overshoot >2 %.

### 4.4 Sound design (off by default)
- Pill: "Sound on · meet the crew". One tap enables the crew's voices, a quiet room tone (−30 dB below voice), Vee's **stopwatch click** (series sound, `36` §3) and a two-note brass sting on the form success. Nothing else: no hover sounds, no scroll whooshes `[inf]`.
- WCAG 1.4.2: any audio > 3 s needs pause/volume control (`29` §2.2). The pill toggles back to "Sound off".
- AudioContext is created *inside* the tap handler and `resume()`d (Chrome autoplay policy [S3]).

### 4.5 Micro-interactions
- Cursor on desktop: native cursor. Over a film tile, a small brass ring with "Play ▸" (no custom cursor everywhere; it hurts usability) `[inf]`.
- Buttons: 1 px brass underline grows left → right in 200 ms. Primary button fill shifts ink → brass.
- Film tiles: hover = the muted loop plays; leave = it fades to poster. Click = player with sound (the first activation also unlocks the crew's audio).
- Form fields: label floats, 150 ms. Errors in plain words beside the field.
- Success: the "slate" closes (two bars meet), the sting plays, and Otto's line runs.

---

## 5. DELIVERABLE · VXO home-page scroll script

Legend: **Pin** = pinned length in viewport heights (vh). **Clip IDs** refer to §6. Lines ≤ 8 words; captions always; voice only after "Sound on". Otto = deadpan, slow, dry. Vee = quick, clipped, warm. Copy is calm, exact and sensory; all films are AI and say so. Desktop first; mobile changes in *italics*.

### Global chrome
- Header (sticky, 64 px): `VXO` · Work · Pricing · How we use AI · [Get 5 free frames].
- Left edge (desktop): chapter mark "Scene 1 · The take" + a 1 px progress line. *Mobile: chapter mark in header.*
- Bottom-left pill: "Sound on · meet the crew" / "Mute the crew". *Mobile: in the sticky CTA bar.*
- Footer line on every page: "Everything here is made with AI, including Otto and Vee."

---

### Act I · The take (hook + message match) — Pin 150 vh *(mobile: no pin, 100 vh)*
- **Pinned:** full-bleed scrub video `sol.scrub` (5 s of the SOL one-take, slow push-in), headline layer above.
- **At 0 s, static, before any scroll:** poster frame + H1 + sub + both CTAs + objection chip + "AI-made" micro-line.
- **H1 (default):** "Your product, filmed in one unbroken take."
- **H1 variants by `utm_content`** (message match): `launch` → "Your launch, filmed in one unbroken take." · `fatigue` → "A new hero ad. No shoot, no crew." · `frames` (cold email) → "Your 5 free frames start here."
- **Sub:** "Thirty-second product films for brands people have to smell, taste or touch. Made with AI, directed by a human. Start with 5 free frames."
- **CTAs:** [Get my 5 free frames →] [Watch a film ▸] · chip: "Free means free. No card, no call."
- **Scroll 0 → 100 % of the pin:** the take plays forward (camera glides around the bottle). The H1 drifts up 6 % and stays readable.
- **Otto entrance (the founder's beat):**
  - 0–20 %: **peek** from bottom-centre-right, hat + moustache tips (`O-PEEK`). Caption chip: **Otto: "Down here. ↓"**
  - 20–70 %: holds docked at the edge.
  - 70–100 %: **rises** into the lower right third (`O-RISE`, scrubbed), lands, swaps to `O-TALK-01`.
  - **Line O1 (on arrival):** "I'm Otto. I don't do cuts." (6 words)
- **Sound pill tapped any time in Act I:** Vee pops in from the left edge (`V-POP-IN`), **Line V1:** "Sound's on. I'm Vee. Producer." (5 words); then Otto plays O1 if he has arrived.
- **Exit to Act II:** the take's last frame pulls back (scale 1 → 0.86) into a framed "monitor", and Otto turns to look at it (`O-LOOK`).
- *Mobile:* no pin. The SOL loop autoplays muted (not scrubbed). Otto peeks from the bottom edge for 1.2 s after the first scroll, then rises as Act I's bottom reaches 60 % of viewport (time-based 900 ms tween, not scrubbed).

### Act II · The tired ad (problem) — normal scroll
- **Scrolls:** three headline lines reveal one by one, each alone on screen.
- **Headline:** "Your best ad is getting tired."
- **Lines:** "The hook still works. The feed stopped noticing." · "A reshoot means a studio, a crew and three weeks." · "UGC can't film a perfume in slow light."
- **Fact (sourced, from `33` S2):** "The median Meta ad creative lives about 22 days." with source link (Benly, Q1 2026, as cited in `33`). If we can't re-verify the source at launch, cut the line.
- **Vee entrance:** from the right edge. Peek (`V-PEEK`, stopwatch hand) with caption **Vee: "Hold on, coming in."** → walks in to the lower right (`V-WALK-IN`) → clicks the stopwatch (`V-CLICK`).
  - **Line V2:** "Ads expire. Shoots take weeks. Not ours." (7 words, `V-TALK-02`)
- **CTA (soft):** "See what we'd make from one photo ↓"
- Vee exits right as Act III's pin approaches (`V-EXIT-R`).

### Act III · One photo in (the wow demo) — Pin 200 vh *(mobile: pin 120 vh, image-sequence fallback)*
- **Pinned:** centred 4:5 frame. Scroll scrubs three states in one continuous move:
  1. 0–30 %: a plain phone photo of an invented product on a kitchen counter (`ba_before.webp`). Caption: "Your photo. Any light."
  2. 30–60 %: it resolves into a storyboard frame (`ba_after.webp`). Caption: "Frame 3 of 5. Free."
  3. 60–100 %: the frame *becomes* the moving take (`aurum.scrub`, 5 s all-intra). Caption: "The film. One take."
- **Headline (left column, static during the pin):** "One photo in. A film that looks like a shoot."
- **Body:** "Send one product photo. In 3–5 business days you get 5 frames: the light, the palette and the camera path of your film. Judge us on your product, not our reel."
- **Otto:** already standing at the left edge of the frame like a director at a monitor (`O-FRAME-HANDS`: makes a finger frame at 30 %). At 100 %:
  - **Line O2:** "Same bottle. Better afternoon." (4 words, `O-TALK-02`)
- **After the pin releases: inline mini-form** (§3.4): "Get 5 free frames of your product." `[Email] [Product page URL] [Get my 5 free frames]` · chip: "Will it look like my product? We build from your photos."
- Otto sinks out of frame (`O-EXIT-DOWN`) as the form scrolls up.

### Act IV · Four films (range) — normal scroll, no characters
- **Scrolls:** four tiles (SOL, VESPER, AURUM, OTTO) in a staggered 2 × 2 grid with a light parallax (≤ 6 %). Muted loops play when ≥ 50 % visible (≤ 3 at once on phones).
- **Headline:** "Brands that don't exist. Films that look like they do."
- **Sub:** "We invented these brands to show what we make from a product and an idea. Each is one continuous take, 100 % AI, directed by a human."
- **Tile label:** "Spec film · invented brand · AI · 30 s".
- **Interaction:** click = player with sound (counts as the audio unlock).
- **CTA:** [See all films] [Get my 5 free frames] · chip: "Are these real clients? No. Invented, to show the range."

### Act V · The schedule (how it works) — short pin 100 vh *(mobile: no pin, vertical stepper)*
- **Pinned:** a horizontal "call sheet" (a 3-column table on desktop); progress fills a brass line under the steps as you scroll. Scrolling stays vertical; only the fill moves.
- **Headline:** "From one photo to a finished ad in about a week."
- **Steps:**
  1. "**Frames** — free, 3–5 business days. Five frames that fix the light, palette and camera path."
  2. "**Film** — final by day 7–8. One unbroken 30-second take. Two revision rounds."
  3. "**Variants** — hooks, lengths and 9:16 + 4:5 cuts for paid social."
- **Vee** stands at the right of the call sheet (`V-CLICK` at each step: three clicks over the pin).
  - **Line V3 (at step 3):** "Frames by day five. Film by eight." (7 words, `V-TALK-03`). This matches the Premiere tier timing (`pricing.json`: final day 7–8).
- **CTA:** [Start with step 1 → free frames] · chip: "AI disclosure? We label it and set it up." → `/ai`

### Act VI · What you risk (proof + risk reversal) — normal scroll, no characters
- **Headline:** "No client logos yet. Here's what you get instead."
- **Three proof cards (all true today):**
  - "**Your product first.** 5 free frames before you pay anything."
  - "**Pay half on approval.** 50 % to start, 50 % when you approve the film."
  - "**See how it's made.**" Expands to a 20 s BTS breakdown of AURUM: prompt notes, frames, takes 1–6, final.
- **Founder line:** "Directed by Itamar, from Boca Raton. Every frame is reviewed by a person before you see it." (only if accurate at launch; otherwise cut "from Boca Raton")
- **Founding offer (from `pricing.json`):** "First five brands: one extra variant, in exchange for permission to show the work once it's live and a 15-minute debrief."
- **Inline objection chips:** "Who owns it?" · "What if I hate it?" (§3.5).
- **CTA:** [Get my 5 free frames]

### Act VII · The price (offer) — normal scroll; section inverts to ivory ("lights up")
- **Transition:** ink → ivory over 40 vh (background colour tween only).
- **Headline:** "Three ways to work with us. Prices on the page."
- **Cards high → low (existing component):** Season $3,500/mo (3-month minimum) · **Premiere $2,500, Recommended for launches** · Short $1,200. Below: "All plans: 2 revision rounds, music licensed for paid social, perpetual worldwide licence for digital." Context line with DesignRush source (already in `pricing.json`).
- **Otto** enters from below the Premiere card (peek with caption **"One moment."** → rise, `O-RISE-SEATED`: he's in a director's chair). Sits beside the cards and never over them.
  - **Line O3:** "Launching something? The middle one." (5 words, `O-TALK-03`)
- **Vee** leans in from the right edge (`V-LEAN-IN`), taps the stopwatch:
  - **Line V4 (optional, A/B):** "Start free. Pay when you approve." (6 words, `V-TALK-04`)
- **CTAs per card:** Season [Book a call] · Premiere [Start with free frames] · Short [Start with free frames]. Chip: "What if I hate the film? Second half is due on approval."

### Act VIII · Your product next (close) — normal scroll; the form is never pinned
- **Two-shot:** Otto (left) and Vee (right) flank the form at 70 % scale (`D-TWO-SHOT-IDLE` loop). They enter together: Otto rises, Vee walks in, both in 1.2 s, triggered when the form is 30 % visible.
- **Headline:** "Send one photo. We'll send back five frames."
- **Sub:** "3–5 business days. No call, no card. Marked 'AI concept'. Yours to keep and share with your team."
- **Form (two-step, `29` §5):** `[Email] [Product page URL]` [Get my 5 free frames] → step 2 on `/frames/thanks`.
- **Line V5 (on form focus, first time only):** "Two fields. Twenty seconds. Go." (5 words, `V-TALK-05`)
- **Line O4 (after V5, 1.5 s later, or on hover of the button):** "Send it. I'll find the light." (6 words, `O-TALK-04`)
- **Success state:** slate closes, sting, **Line O5:** "Received. Itamar's on it." (4 words, `O-TALK-05`) + **Vee** clicks the stopwatch (`V-CLICK`, no line).

### Coda · Footer — normal scroll
- **Otto** peeks one last time from the bottom edge (`O-PEEK`). **Line O6 (caption-only unless sound on):** "One more take?" **Vee (off-screen voice, caption):** "No." (the `36` series loop joke: Otto always wants another take).
- Footer: links, "Everything here is made with AI, including Otto and Vee.", `/ai`, privacy.

### Line sheet (for ElevenLabs; fixed voices)
| ID | Speaker | Line | Words | Trigger |
|---|---|---|---|---|
| O1 | Otto | "I'm Otto. I don't do cuts." | 6 | Act I arrival |
| V1 | Vee | "Sound's on. I'm Vee. Producer." | 5 | Sound pill tap |
| V2 | Vee | "Ads expire. Shoots take weeks. Not ours." | 7 | Act II arrival |
| O2 | Otto | "Same bottle. Better afternoon." | 4 | Act III pin end |
| V3 | Vee | "Frames by day five. Film by eight." | 7 | Act V step 3 |
| O3 | Otto | "Launching something? The middle one." | 5 | Act VII arrival |
| V4 | Vee | "Start free. Pay when you approve." | 6 | Act VII (A/B) |
| V5 | Vee | "Two fields. Twenty seconds. Go." | 5 | Form first focus |
| O4 | Otto | "Send it. I'll find the light." | 6 | After V5 / CTA hover |
| O5 | Otto | "Received. Itamar's on it." | 4 | Form success |
| O6 | Otto + Vee | "One more take?" / "No." | 3 + 1 | Footer peek |
| (caption only) | Otto | "Down here. ↓" · "One moment." | — | Peeks |
| (caption only) | Vee | "Hold on, coming in." | — | Peek |
"Twenty seconds" in V5 is a claim; time the real form with 5 people before launch and change the number if it's wrong `[inf]`. Existing voice files in `site/public/media/voice/` (`vo_*`, `vee_*`) remain for `/frames` and pop-ups. The lines above are new recordings.

### Scroll budget (desktop)
Act I 150 vh pin + Act III 200 vh pin + Act V 100 vh pin = **450 vh pinned** of ≈ 1,500 vh total ≈ **30 %**. Mobile: Act III's 120 vh only, ≈ 10 %.

---

## 6. New character clips to generate

Specs for all clips: generate on a key colour, matte, encode stacked-alpha AV1 + HEVC (`30` §3, `31` §4.3). 1080 px tall master; web 720 px tall (`_hd` 1080 for desktop). Locked camera, full body unless noted, 3/4 view facing screen-left for right-side placements (mirror for the left), soft key from top-left to match the films. Talking clips: **Vee = real lip-sync** (mouth visible; face 15–40 % of frame, head nearly still, ≤ 8 s per generation, QC teeth at 100 %, `30` §2.5). **Otto = moustache-driven speech**: the moustache lifts and flutters on syllables, cheeks bob, small chin drop on stressed words, driven by the ElevenLabs file's amplitude; mouth never shown. Each talking clip starts and ends on the idle pose of its paired idle loop so swaps are invisible (A/B players, `31` §4.5).

### Otto (existing: idle, nod, point_L/R, reach, talk, pop_thumb, pop_wave)
| ID | Pose / action | Duration | Talking | Playback | Used in |
|---|---|---|---|---|---|
| O-PEEK | Only hat + eyes + moustache tips above the bottom edge (frame cut at the nose); eyes look up at viewer, moustache twitches once | 2.5 s seamless loop | No | Loop | I, VII, Coda |
| O-RISE | Rises from below the frame bottom to standing mark (as if on a stage lift), settles, straightens lapel; ends on idle | 2.0 s | No | **Scroll-scrubbed** (all-intra, alpha) | I, VIII |
| O-RISE-SEATED | Rises seated in a director's chair, crosses legs, ends still | 2.5 s | No | Scrubbed | VII |
| O-LOOK | Turns head 3/4 toward screen-left (to a monitor), then back to camera | 2.5 s | No | Triggered | I → II |
| O-FRAME-HANDS | Lifts both hands into a finger-frame, squints through it, lowers | 3.0 s | No | Triggered | III |
| O-EXIT-DOWN | Sinks straight down out of frame, deadpan | 1.5 s | No | Triggered | III, any exit |
| O-SEATED-IDLE | Seated idle loop, occasional blink + moustache settle | 4.0 s loop | No | Loop | VII |
| O-TALK-01 | Standing, line O1, moustache-driven, one small hand gesture on "cuts" | ~2.2 s | **Yes** | Triggered | I |
| O-TALK-02 | Beside monitor, line O2, slight head tilt toward frame | ~2.0 s | **Yes** | Triggered | III |
| O-TALK-03 | Seated, line O3, opens palm toward the middle card (screen-left) | ~2.2 s | **Yes** | Triggered | VII |
| O-TALK-04 | Two-shot left, line O4, raises one finger like a light meter | ~2.0 s | **Yes** | Triggered | VIII |
| O-TALK-05 | Two-shot left, line O5, small satisfied nod at the end | ~1.8 s | **Yes** | Triggered | VIII success |
| O-TALK-06 | Peek framing, line "One more take?", eyebrows up | ~1.2 s | **Yes** | Triggered | Coda |

### Vee (existing: vee_pop_1, vee_pop_2)
| ID | Pose / action | Duration | Talking | Playback | Used in |
|---|---|---|---|---|---|
| V-PEEK | Only her stopwatch hand + shoulder enter from the right edge; thumb hovers over the button | 2.0 s loop | No | Loop | II |
| V-POP-IN | Steps in from the left edge, half body, quick glance to camera, ends on idle | 1.2 s | No | Triggered | I (sound tap) |
| V-WALK-IN | Brisk walk in from the right to her mark, stops, checks the stopwatch; ends on idle | 2.0 s | No | **Scroll-scrubbed** | II |
| V-IDLE | Standing idle loop: weight shift, glance at stopwatch, blink | 4.0 s loop | No | Loop | II, V, VIII |
| V-CLICK | Raises stopwatch, clicks, looks to camera (add click SFX in post, not in the clip) | 1.2 s | No | Triggered | II, V ×3, VIII success |
| V-LEAN-IN | Leans in from the right edge, upper body only, elbow on an invisible table | 1.5 s | No | Triggered | VII |
| V-EXIT-R | Turns and walks off right | 1.2 s | No | Triggered | II, any exit |
| V-TALK-01 | Half body, line V1, lip-synced, quick smile on "Producer" | ~2.0 s | **Yes (lips)** | Triggered | I |
| V-TALK-02 | Half body, line V2, stopwatch raised on "Not ours" | ~2.8 s | **Yes (lips)** | Triggered | II |
| V-TALK-03 | Half body, line V3, taps stopwatch on "five" and "eight" | ~2.6 s | **Yes (lips)** | Triggered | V |
| V-TALK-04 | Lean-in framing, line V4 | ~2.2 s | **Yes (lips)** | Triggered | VII (A/B) |
| V-TALK-05 | Two-shot right, line V5, nods toward the form | ~2.0 s | **Yes (lips)** | Triggered | VIII |
| V-TALK-06 | Off-screen "No." Audio only; no clip needed (optional 0.8 s head-shake at the frame edge) | 0.8 s | Optional | Triggered | Coda |

### Duo
| ID | Pose / action | Duration | Talking | Playback | Used in |
|---|---|---|---|---|---|
| D-TWO-SHOT-IDLE | Otto left and Vee right, both idle; Vee glances at her stopwatch, Otto at Vee, deadpan. Generated as **one clip** so their eyelines match; both must hit the same idle poses used by O-TALK-04/05 and V-TALK-05 | 5.0 s loop | No | Loop | VIII |

**Count:** 13 Otto (6 talking) + 13 Vee (5–6 talking) + 1 duo = **27 clips**, of which **11–12 need speech**. All silent clips are reusable on `/frames`, `/pricing` and social. Priority if the budget is tight: O-PEEK, O-RISE, O-TALK-01, V-WALK-IN, V-TALK-02, V-CLICK, O-TALK-02, D-TWO-SHOT-IDLE, O-TALK-05 (this set covers the founder's "comes up from below" beat, the demo and the close).

**Scrubbed alpha clips** (O-RISE, O-RISE-SEATED, V-WALK-IN) need the all-intra rule *and* stacked alpha: encode them `-g 1` at the 720 px web size only; expect several MB each. If seek on iOS stutters, export them as 48–60 frame WebP-with-alpha sequences drawn to canvas `[inf]`.

---

## 7. Build notes for the next agent (no code changed here)
- `site/src/pages/index.astro` becomes 9 scene components: `ActTake`, `ActTired`, `ActPhotoIn`, `ActFilms`, `ActSchedule`, `ActRisk`, `ActPrice`, `ActClose`, `Coda`. `PopUp.astro` and the existing hero orbit move to `/frames` or are retired (`33` §2 S0 is superseded by Act I).
- One `lib/story.ts`: Lenis (desktop only) + `gsap.matchMedia` with three branches: `desktop`, `touch`, `reduce`. A `Crew` controller owns entrances, the caption queue, once-per-session line memory (`sessionStorage`, wrapped in try/catch) and the velocity gate.
- Events to add (`31` §8): `crew_sound_on`, `crew_muted`, `crew_line_played{id}`, `act_view{n}`, `inline_form_submit{act}`, `sticky_cta_click`, `utm_headline_variant`.
- Tests before launch: real iPhone (Safari) for scrub seek and alpha; mid-range Android at 4× CPU throttle for 60 fps on Act III; reduced-motion pass; VoiceOver pass; 5-person timing test for the "Twenty seconds" claim.

---

## Sources
- [S1] NN/g, Scrolling and attention: https://www.nngroup.com/articles/scrolling-and-attention/ (via `29` §2.1)
- [S2] NN/g, Scrolljacking 101: https://www.nngroup.com/articles/scrolljacking-101/
- [S3] Chrome autoplay policy: https://developer.chrome.com/blog/autoplay · https://www.chromium.org/audio-video/autoplay
- [S4] WHATWG HTML, activation-triggering input events (keydown, mousedown, pointerdown/up, touchend; not scroll or wheel): https://html.spec.whatwg.org/multipage/interaction.html#activation-triggering-input-event
- [S5] Clippy: Harvard Crimson on Swartz's 2003 Stanford thesis: https://www.thecrimson.com/article/2005/4/28/what-not-to-do-with-a/ · Dennis Kennedy quoting Chris Pratley: https://www.denniskennedy.com/blog/2004/05/clippy-and-user-experience/
- [S6] CSS-Tricks, Apple-style image sequence: https://css-tricks.com/?p=308477
- [S7] GreenSock image-sequence CodePen (AirPods frames): https://codepen.io/GreenSock/embed/VwgevYW
- [S8] Prototypr, Apple splash pages (delays, type-first): https://blog.prototypr.io/master-the-art-of-apples-splash-pages-with-these-tricks-62a57d30960d
- [S9] Awwwards, Lusion profile (Oryzo AI, SOTM Apr 2026): https://www.awwwards.com/lusion/
- [S10] Lusion blog, Oryzo BTS part 1: https://blog.lusion.co/oryzo-bts-part-1-7-concept-and-creative-direction
- [S11] Domus, Hermès new website (Jan 2026): https://domusweb.it/en/news/2026/01/07/herms-new-website.html
- [S12] Fast Company via The Note, Hermès hand-illustrated site: https://thenote.app/post/en/hermess-hand-illustrated-website-is-the-ultimate-luxury-vhoyi2bkvj · Bigwall Decor: https://bigwalldecor.com/hermes-hand-drawn-website-age-of-ai/
- [S13] Font Alternatives, Aesop + Suisse Int'l: https://fontalternatives.com/inspiration/aesop-suisse/
- [S14] webdesignhot, Aesop DESIGN.md (reconstruction): https://www.webdesignhot.com/design.md/aesop/
- [S15] PAP Magazine, Bottega Veneta identity without logos: https://www.pap-magazine.com/en/article/bottega-veneta-fw26-identity-without-logos · adlibrary: https://adlibrary.com/brands/bottega-veneta
- [S16] Lenis README (defaults, GSAP snippet, data-lenis-prevent): https://cdn.jsdelivr.net/npm/lenis@1.3.8/README.md
- [S17] Krishaweb, what is scrollytelling (Snow Fall origin): https://www.krishaweb.com/blog/what-is-scrollytelling.txt
- [S18] hontran.dev, scroll-scrubbed video stutters fix: https://www.hontran.dev/blog/scroll-scrubbed-video-stutters-fix
- [S19] muffinman.io, scrubbing videos with JS: https://muffinman.io/blog/scrubbing-videos-using-javascript/ · CodePen (-g 6): https://codepen.io/luis-lessrain/pen/zxGjErP · GSAP forum: https://gsap.com/community/forums/topic/38762-can-gsap-scrolltrigger-scrub-a-video-on-scroll/
- [S20] NN/g, What Parallax Lacks: https://www.nngroup.com/articles/parallax-usability/
- [S21] NN/g, Scroll Fading 101: https://www.nngroup.com/articles/scroll-fading-101/
- [S22] hontran.dev, GSAP ScrollTrigger pin/scrub/parallax: https://www.hontran.dev/blog/gsap-scrolltrigger-tutorial-pin-scrub-parallax
- [S23] GSAP forum, ScrollTrigger + Lenis on mobile: https://gsap.com/community/forums/topic/38517-scrolltrigger-and-lenis/
- [S24] Mozilla Connect (animation-timeline behind pref): https://connect.mozilla.org/t5/discussions/why-doesn-t-firefox-support-the-css-animation-timeline/m-p/60742 · MDN BCD: https://github.com/mdn/browser-compat-data/blob/main/css/properties/scroll-timeline.json · Safari 26 coverage: https://www.buildmvpfast.com/blog/css-scroll-driven-animations-replace-js-2026
- [S25] W3C, Understanding SC 2.3.3: https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions
- [S26] GSAP docs, gsap.matchMedia(): https://gsap.com/docs/v3/GSAP/gsap.matchMedia()
- [S27] Lester et al., The Persona Effect, CHI '97: https://chi1997.acm.org/proceedings/paper/jl.html · follow-up (Ryu & Ke 2018): https://koreascience.or.kr/article/JAKO201812263825311.pdf
- [S28] Guidejar, scroll view plays itself: https://feedback.guidejar.com/updates/p/scroll-view-now-plays-itself
- [S29] NN/g, Animation duration and motion: https://www.nngroup.com/articles/animation-duration/
- [S30] Unbounce, message match: https://unbounce.com/conversion-rate-optimization/gmail-ad-fail-how-poor-message-match-can-kill-your-conversion-rate/
- [S31] Secondary citations of the Moz/Disruptive +212 % case (unverified): https://www.webtonic.io/blog/message-match
- [S32] Unbounce Conversion Benchmark Report 2024: https://unbounce.com/conversion-benchmark-report/ · methodology: https://unbounce.com/conversion-benchmark-report/methodology/
- [S33] Baymard, checkout optimization: https://baymard.com/blog/checkout-optimization · https://baymard.com/research-articles/checkout-optimization-from-16-fields-to-8
- [S34] Sticky CTA tests: CleanCommit (AFTCO): https://cleancommit.io/ab-tests/sticky-mobile-add-to-cart-button/ · Blend Commerce: https://blendcommerce.com/blogs/ab-tests-shopify/10-increase-in-conversion-rate · https://blendcommerce.com/blogs/ab-tests-shopify/adding-a-sticky-cta-to-the-product-detail-page · Convertica: https://convertica.org/ecommerce-case-study-sticky-cta/ · GoodUI #41: https://goodui.org/patterns/41
- [S35] Risk reversal (practitioner only): https://predictableprofits.com/3-ways-to-increase-sales-almost-instantly-with-risk-reversal/ · https://www.awai.com/2011/12/skyrocket-response/
- [S36] Decoy/compromise effect summaries (Huber, Payne & Puto 1982; ProfitWell benchmark): https://www.getmonetizely.com/articles/the-compromise-effect-why-do-consumers-gravitate-toward-the-middle-option · https://www.atticusli.com/blog/posts/how-decoy-effect-pricing-changes-choice-on-pricing-pages/
- [S37] Pracejus, Olsen & O'Guinn, JCR 2006: https://ideas.repec.org/a/oup/jconrs/v33y2006i1p82-90.html · Olsen et al., JBR 2012 "Print advertising: White space": https://ideas.repec.org/a/eee/jbrese/v65y2012i6p855-860.html

**Gaps:** we could not load the Awwwards 2025 annual winners list (the page didn't render for our fetcher), Apple's live implementation (only reconstructions), Active Theory case material, or any controlled study of mascot-guided *sales* pages. The crew's effect on conversion is a hypothesis to A/B test (crew on vs. crew off), not a finding.
