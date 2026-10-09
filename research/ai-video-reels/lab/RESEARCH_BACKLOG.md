# Research backlog (the daily routine works it top-down)

## Next up (from `lab/WEAKNESSES.md`, 2026-10-09). Work these BEFORE anything below
Each one unblocks a sale or an owner decision listed in WEAKNESSES.md §3. Zero spend; never send anything.

- [ ] **Send-day live re-check kit.** Add a `products.json` hidden-SKU check (`redirect-to-404`, `exclude`, `available:false`, empty body) next to `scripts/research/ad_library.py`. Run both on Foggy, Moment and AUrate the morning of each send. Propose making them mandatory in `vxo-leads` §1 (W#10, W#9).
- [ ] **Red Light re-cut edit decision list** from existing scratchpad media ($0, never commit media): a 1.5 s can flash-forward, a fix for the 2.9 s freeze, a can packshot + offer end card, 15 s and 4:5 cuts, `qc_report.py` before/after. Ready for owner decision 7 (W#5, W#13, W#24).
- [ ] **Fidelity-proof shot plan:** which real product (collar / tennis bracelet / can), the phone-photo spec, the 3-panel before/after layout, checks (embroidery, stone count, label letter by letter, ΔE ≤ 3). Ready for decision 8 (W#6, W#17).
- [ ] **Off-holiday redrafts** of the Foggy, Moment and AUrate DMs/emails: a Dec 1–20 refresh, January drops, Dry January; Moment without "coupe" or cocktail-hour cues; Foggy pitched as a tool for her in-house content lead (Finn & Gray handover). Drafts only, for decisions 10, 13 and 14 (W#11, W#14, W#16).
- [ ] **Verify top 3 first:** the Instagram one-message rule as of Oct 2026, the AI-disclosure rules for commercial ads (Meta, TikTok, YouTube), and 10 live competitor AI-studio price pages (see Verify below; W#18, W#19, W#25).
- [ ] **Next 30 sends ready:** re-check HOT_NEW_30 live with `ad_library.py` and the hidden-SKU check, starting with Leaf Shave, The GLD Shop and Baked by Melissa, so 10 a day are ready after the first sends (W#1, W#31).
- [ ] **Outcome tracker + one spend ledger design** (see the queue item below), ready for decision 19 (W#28).

Rules:
- `vxo-daily` Step 2 takes the top 3 unchecked items of **Verify**; Step 3 takes the top unchecked item of **Research**.
- Whenever you check a Research item, add up to 2 new ones, at most one "nobody asked, but it would make us better". Every topic must help find leads, close them, or make the films better. **No pivots** (LESSONS, 2026-10-09).
- Ranked by how close the item sits to money: the message the owner sends next, the price, the policy that can get a client's ad rejected, then craft.

## Verify: decision-critical `[unverified]` facts (from the 2026-10-09 ops audit)
Docs 41–62 carry 380 `[unverified]` tags. Most are brand revenue bands (low stakes). These are the ones that steer a decision:

- [ ] **Founder-led status of every prospect we might message** (53 and 55 tables: Supply, Leaf Shave, Scotch Porter, Fulton & Roark, GhostBed, Helix "No (portfolio)", Silk & Snow, Coop, Slip and ~30 more are `[unverified]`). "Founder-led and reachable" is 10 points of the score and the whole ICP. Method: the brand's About page, LinkedIn company page (public view), press. Mark each `[m]` or drop it from the ICP.
- [ ] **Competitor AI-studio prices** (45 D45 MAW AI Studios $500 / $2,000; D49 Genre.ai ~$100k per 30 s; 48 "live-action jewelry macro shoot well above $5K"). These anchor Short $1,200. Find 10 live public price pages of AI ad studios selling to DTC in 2026 and record the price per finished 15–30 s film.
- [ ] **AI-disclosure rules for commercial ads** (45 lines 308–310: Meta "AI info" label scope, C2PA detection and undisclosed AI as a rejection reason; Google/YouTube commercial ads have no checkbox `[unverified]`; TikTok AIGC label). A client's ad being rejected or labelled is the first objection after price. Primary policy pages only.
- [ ] **Meta weapons-in-fiction and police imagery** (45 lines 287, 299). The Red Light film (the owner's "this is the bar") is a chase. Confirm what a paid version may show.
- [ ] **AI-UGC vs human performance and consumer trust** (45 D37 `[vendor][unverified]`; 47 "31 % trust the brand less", Klaviyo/Datalily via search summary). Used in DMs and objection replies. Find the primary reports or stop quoting them.
- [ ] **Meta CPA/ROAS medians** (45 D21/D22, 51 N8, 56 D2: Triple Whale page 403, text and table disagree). Used to sell "one Short pays back in N orders". Get the page in headless Chromium or replace the source.
- [ ] **Hook-rate benchmarks** (45 D17, relayed from Motion via vendors). Used as our QC/reporting target.
- [ ] **Meta "sensitive category" optimisation loss for health/wellness** (55 N6 "30–40 % efficiency drop" `[unverified]`). Decides whether sleep/supplement leads can even buy performance from a film.
- [ ] **Seedance 2.5 / Higgsfield 1080p is native or upscaled** (43 line 388). Decides whether "1080p" on our delivery spec is honest (doc 64 measured real detail).
- [ ] **Kling multi-shot honours `last_image_url`** (43 line 135). Decides the end-frame/packshot plan for 6–10 cut films.
- [ ] **Instagram one-message rule for non-followers** (63 §0.3, TechCrunch 2023). The whole channel plan rests on it; confirm it still holds in Oct 2026 from Instagram's help centre.

## Research: queue
- [ ] **Meta Ad Library long-runner study, now unblocked.** `skills/ad-director/scripts/research/ad_library.py page <id> --json` gives start dates and formats for the top ~30 cards per Page (Meta's default order; logged-out scrolling is rate-limited, so 30 is the ceiling). For 20 brands in our niches, record what the ads running 60+ days have in common (format, length, hook, video vs still). This replaces the old Motion-snapshot evidence with live data.
- [ ] **Calibrate the lead score against live data.** Run `ad_library.py` on the brands in `prospects/` (HOT_NEW_30, HEAT_50, us-dtc, us-beverage): active ads, card video share, ads started in the last 30 days. Check which score components actually separate brands, re-weight "Running paid ads" and "Creative need", and mark brands whose data went stale.
- [ ] **Outcome tracking design.** One file (`leads/PIPELINE.md` or a CSV) that records, per message: channel, date sent, opened/replied, positive?, frames requested, sale, revenue, days to reply. Define the weekly review: which observation, idea type and channel got replies. Retire `launch/tracker.csv` (EXAMPLE rows only) or merge it.
- [ ] **One spend ledger.** Spend lives in per-experiment ledgers (`lab/experiments/*/ledger.md`, `packages/ledger.jsonl`, `pipeline.py` spend.jsonl) and `vxo-film` points client jobs at `W01_site_films/ledger.md`. Design one cumulative ledger with per-client cost of goods, so the owner knows the margin on a $1,200 Short.
- [ ] **Video understanding without Gemini.** Compare, on 5 of our films and 5 winning ads: frame strips read by Claude vs a local open model (CPU-only, zero spend) vs nothing. What hook/sync/continuity faults does each catch? Decide whether a Gemini key is worth asking the owner for.
- [ ] **TikTok Creative Center "Top Ads" for our categories**: hooks, length, CTA, captions. First check whether it loads in headless Chromium without login.
- [ ] **Lead dossier speed** (was: "Lead dossier sources"): how to read a brand in 20 minutes per lead with `ad_library.py`, `products.json`, review mining, founder interviews and job posts. Write it as a checklist inside `vxo-leads`.
- [ ] **Cold DM/email reply rates for creative services to DTC founders in 2025–2026** (doc 63 has vendor B2B numbers only): find creative-service-specific data.
- [ ] **Re-purchase and retention for creative services**: what makes DTC brands rebook monthly (ad fatigue cycles, seasonal calendars, reporting results), and how the Season plan renews.
- [ ] **Pricing psychology for creative services**: anchors, packages, guarantees, pilot credits (after the competitor-price Verify item).
- [ ] **Case studies: AI ad studios that won their first 20 clients in 2025–2026** (public interviews only).
- [ ] **Brand voice design**: how agencies pick a VO voice per brand; ElevenLabs voice-design practice (research only, no calls).
- [ ] **Music for ads**: licensing-safe AI music, beat-matching cuts, when silence sells.
- [ ] **Upscaling and finishing**: the best way to take a 480p take to 1080p (Topaz-style, available APIs, ffmpeg chains). Measure the quality on existing takes; no new renders.
- [ ] **Hands and product interaction**: why AI hands fail with cans, bottles and jars; prompt fixes with examples.
- [ ] **Packshot lighting** for glass, metal, liquid and cosmetics, said in prompt language.
- [ ] **Food and liquid physics in AI video**: pours, fizz, steam, melt; what works per model.
- [ ] **Comedy timing in 15 s**: frame counts for setup, pause and payoff in the best ad comedies.
- [ ] **Retention editing**: pattern interrupts every 2–3 s; measure them in top reels.
- [ ] **Prompt-reveal reels** ("comment X for the prompt") for VXO's own account, and turning the comments into conversations.
- [ ] **Instagram growth for a studio account**: series formats, cadence, collabs (public data).
- [ ] **Localisation**: Spanish versions of a film (lip-sync, captions, VO) for Hispanic US audiences of our clients.
- [ ] (nobody asked) **Sound-off design and captions**, since most viewers watch muted.
- [ ] (nobody asked) **Contract language for AI films**: IP assignment, model/likeness releases, AI disclosure, revisions (research only; the owner takes legal advice).
- [ ] (nobody asked) **Stale-data sweep**: list every number in docs 41–65 and the dossiers that came from a snapshot older than 30 days (Motion "refreshed 4 months ago", Triple Whale 2025) and tag it `[stale]`.

## Superseded (kept for the record)
- [~] Hook-module pricing and test design (3 s hook transplants). Superseded 2026-10-09: the owner fixed the direction ("we're not changing direction"); hook modules are not a product unless he asks. Hook craft stays in the film research above.
- [~] Affiliate seed films for TikTok Shop. Superseded 2026-10-09 for the same reason: it presents a new buyer.
- [~] Meta Ad Library deep-dive on 20 beverage/fragrance/candle ads. Folded into the long-runner study above, now that the Ad Library loads.

## Done
- [x] 2026-10-09: viral AI reel teardowns (42), model mastery (43), action and comedy craft (44), what sells (45), sound and QC tools (46).
- [x] 2026-10-09: niche docs 47–52 (beauty, fashion, food, wellness, gadgets/home, pets/kids/outdoor).
- [x] 2026-10-09: deep niche docs 53 (men's grooming, oral care) and 54 (hair tools, nails).
- [x] 2026-10-09: niche docs 55–62, outreach (63), quality-gap audit (64), offer and site (65).
- [x] 2026-10-09: ops audit. Built `scripts/research/ad_library.py` (live Meta Ad Library counts, tested on today's 4 leads), `references/marketing/00-INDEX.md`, the Verify section above, and a rewritten `vxo-daily` (preflight, pipeline first, push-blocked fallback).
