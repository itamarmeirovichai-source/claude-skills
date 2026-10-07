# 18. Automation pipeline: product in, QC'd ad out (research + architecture, 2026-10-07)

Status: a research and design note. Nothing here is built yet. `[inf]` marks our own inference, as opposed to something a source states. Vendor claims are labelled as vendor claims.

---

## 1. What we already have

| Asset | What it does today | Pipeline stage |
|---|---|---|
| `director.py new` | Scaffolds the job folder (`01-brief.md` … `06-qc.md`) | Intake |
| `director.py dice / log / history` | Ledger-aware concept seeds (mechanism × format × hook × emotion × structure × look × sonic + constraint); novelty penalty against the client's history | Ideas |
| `director.py rank` | Driver scores → predicted retention, likes, shares, saves, comments, clicks and purchases, plus the weakest metric | Zero-cost test (relative only) |
| `director.py qc` | ffprobe/ffmpeg checks: resolution, fps, codec, duration, LUFS and true peak, silent hook, first cut, shot length, black and frozen frames, luma flicker outside cuts, brand-colour histogram match against the packshot. Writes `qc_sheet.jpg` with safe zones, `product_compare.jpg`, `qc_report.json` (PASS/WARN/FAIL) | Render QC |
| `director.py bench / bench-summary` | 12-test model matrix → router winners by quality, then cost | Model routing |
| `hfgen.py batch` | Plan JSON → `@file` uploads → `/estimate` per job → **refuses above `--budget`** → parallel takes → download → `manifest.json` + `gen_log.jsonl`. Idempotency key = hash(job, take, model, args, salt); a re-run skips completed takes; `--fresh` forces new takes; `--only` regenerates one shot; retries on 5xx/423/"concurrent" | Stills + motion |
| `elevenlabs.py` | `check` (credits), `voices`, `tts` (+ `words.json` alignment for captions), `sfx`, `music` (music_v2_5, `--plan` composition plans) | Sound |
| `reel-studio` (`reelstudio.py render/plan/beats/grid/cuts/captions`) | JSON edit spec → ffmpeg master: beat-synced cuts, ramps, captions, safe zones, ducking, −14 LUFS, platform exports | Edit / grade |
| `references/film_chain_warm.txt` | Corrected film-look chain (bt709-safe) | Grade |
| `references/qc-rubric.md` | K1–K8 take QC, automated layer, 100-point visual rubric (ship ≥80, no FAIL) | QC |
| `marketing/00` + NOTEBOOK | 10-step pipeline, 15 gates, client taste, BIG IDEA rule, ≈$10/flagship budget template, hard-won model rules (Soul Cinema ignores refs and renders real trademarks; Kling orbit >60° morphs labels; `sound` off saves about 50%) | Policy |

## 2. Gaps for an automated funnel

1. **No orchestrator or state.** Stage order lives in prose (SKILL.md "Stage order A → B → C"). Nothing records which stage a job is at, what was approved, or by whom. A crash or a new session has to re-derive state by reading folders.
2. **No job-level budget.** `hfgen` caps one batch, not the job. Spend is summed from `est_usd`, not the billed amount. `elevenlabs.py` has no estimate, cap or cache, so a re-run pays again.
3. **Take QC is manual.** K1–K8 depends on Claude reading images by eye. There is no label OCR against the brand kit, no trademark/logo screen (the NOTEBOOK E06 swoosh incident), no first-vs-last-frame drift metric, and no cross-shot continuity (one colour world, same bottle) check. The only product check is a colour-histogram match on the final render.
4. **No client-facing artefacts.** There is no storyline deck or stills-approval page, and no structured capture of the client's choice and comments. (The F01 lesson: stills-only animatics confuse clients.)
5. **"Zero-cost testing" is only `rank`.** It produces a relative ordering, with no structured cold-viewer or panel test and no feedback of real results into the ledger beyond a free-text `--result`.
6. **No lineage or versioning.** The chain from a prompt version to its still, its clip, and the edit that used it is implicit in file names. Revisions overwrite.
7. **No delivery packaging.** Nothing produces a manifest of masters, cutdowns, hook variants, AI-disclosure notes or licences.
8. **Research tooling note:** `youtube/fetch_yt.py` currently fails here. yt-dlp gets "Sign in to confirm you're not a bot" with no JS runtime, and `youtube_transcript_api` is missing `requests`. This round used the 80 cached transcripts plus web sources.

## 3. How others automate AI ad production (2025–2026)

### 3.1 One-click "URL → ad" products
- **Higgsfield Marketing Studio / Click-to-Ad.** You paste a product URL. It extracts images, name, features, price, brand colours and logos, then offers styles (UGC, minimal, unboxing…), an editable script, 20+ formats and 40+ avatars, and batch variants from one link. Clips are capped at about 15 s, so longer ads are stitched in post ([help center](https://higgsfield.ai/creator-hub/help-center/tools-and-workflows/how-do-i-use-marketing-studio-to-create-video-ads), [blog](https://higgsfield.ai/blog/best-ai-platforms-create-ads-from-url), Harry Blake walkthrough [youtu.be/ApmRSLNMgMk](https://youtu.be/ApmRSLNMgMk)).
- **Higgsfield MCP** (launched April 2026). 30+ models plus skill presets (UGC Factory, Marketing, Brandkit, Localization…), with saved Soul characters for cast consistency. **Agent generations always bill credits, and there is no built-in credit cap.** The page suggests asking the agent to state the cost and wait for confirmation, which is a prompt-level guard only. Its worked example: a 20 s UGC video cost 270 credits, about $13.50 ([Higgsfield MCP for marketers](https://higgsfield.ai/blog/mcp-for-marketers)). A creator's Claude + MCP "content factory" has the **user approve each batch** ([video summary](https://videohighlight.com/v/l7W3QzU8w5s), unverified).
- **Arcads / Creatify / Icon.** These are UGC-avatar ad factories. Arcads now has a public API and an MCP connector, credit-based. Creatify sells batch mode (10+ variants for A/B) and URL-to-ad; its API needs a paid plan, and only creation endpoints spend credits. Icon is positioned for agencies testing hundreds of variants, with mixed reliability reports ([yespress Arcads](https://yespress.io/products/arcads.md), [Flowjam comparison](https://www.flowjam.com/blog/arcads-vs-creatify-2026), [Creatify docs FAQ](https://docs.creatify.ai/faq), [Creatify quickstart](https://docs.creatify.ai/quickstart), [designrevision roundup](https://designrevision.com/blog/best-ai-video-ad-generators.md)). Most of these sources are vendor or affiliate content.
- **Takeaway for us [inf]:** these tools win on volume and speed for UGC. They do not fit our client's taste (premium, no talking heads, NOTEBOOK F01) and they hide the shot-level control that our label-lock rules depend on. Borrow their *patterns*: URL extraction, batch variants and per-batch approval. Keep the products themselves out of our pipeline.

### 3.2 Node canvases
- **Weavy → Figma Weave.** Figma acquired it in late 2025. Models and edit steps are chained on one canvas; you can branch to send the same instruction to several models and compare; each node holds its own instructions, so a single step can be edited without a rebuild. Demos include applying a campaign style across assets and rendering a logo onto product images ([Figma blog](https://www.figma.com/blog/connecting-figma-and-weave/), [diginomica Config 2026](https://diginomica.com/config-2026-weave-layer-precision-design-workflows-figma), [AlternativeTo](https://alternativeto.net/news/2025/11/figma-acquires-ai-content-platform-weavy-launching-node-based-image-and-video-editing-tool/)).
- **Krea Nodes + Krea Agent.** In Nodes, the output of one tool feeds the next and a whole chain runs from one trigger ([docs](https://docs.krea.ai/user-guide/features/nodes)). Krea Agent's product flow is brief → read the website into a short brand reference → stills → **self-review** → video from the best still (Seedance 2.5) → trim/caption → files into a folder. The orchestrator picks a model per step. The "Extra High" effort setting makes it check its own output and retry, and it retries most generation failures by itself. The human directs, approves, and annotates regions to revise; there is no mandatory stage gate ([Krea blog](https://www.krea.ai/blog/what-is-krea-agent)). A third-party review says the Node Agent shows compute cost before running ([yespress Krea](https://yespress.io/krea)).
- **ComfyUI.** Product pipelines are composites: a product + scene relight template (Seedream 4.5 node) ([comfy.org template](https://www.comfy.org/workflows/templates-product_scene_relight-cc23c187984a)), product relight with a light mask ([RunComfy](https://www.runcomfy.com/comfyui-workflows/comfyui-product-relighting-workflow)), IPAdapter + IC-Light background replacement ([comfyui.org](https://comfyui.org/en/mastering-background-replacement-with-ai)), and Wan 2.2 first–last-frame video ([RunComfy FLF2V](https://www.runcomfy.com/comfyui-workflows/wan-2-2-flf2v-first-last-frame-video-generation)). None of these guarantees label text. **[inf]** The robust fix is ours already: re-composite the real label or packshot pixels through a mask, and keep the label out of the generative pass.

### 3.3 n8n / Make automations
- **n8n template 11204:** Telegram (photo + idea) → OpenAI Vision analyses the product → LLM writes a UGC image prompt → Nano Banana 2 Pro (fal) → agent writes a Veo prompt + optimiser → Veo 3.1 reference-to-video, 9:16 ~8 s → Blotato posts to 6 platforms → "Published" reply. **No approval step, no error handling, no cost notes** ([n8n.io](https://n8n.io/workflows/11204-create-ai-viral-videos-using-nanobanana-2-pro-and-veo31-and-publish-via-blotato/)). Similar: Krystian's Telegram ad agent ([Automation Exchange #44](https://theautomationexchange.beehiiv.com/p/issue-44-krystian-s-ai-video-ad-agent)) and a Sheets-row-driven variant claiming about $1/video, a vendor claim ([growwstacks](https://growwstacks.com/blog/ai-ugc-video-ads-veo-n8n/)).
- **Make:** video APIs return a job id, so a second scenario polls status on a delay loop ([wireflow](https://www.wireflow.ai/blog/make-com-video-automation)). Kling via PiAPI modules are action-only, so you bring your own trigger ([hackceleration](https://hackceleration.com/resources/integrations/make/piapi-kling)).
- **Takeaway [inf]:** low-code pipelines are linear "fire and publish" chains. They are fine for UGC volume and unacceptable for brand work. The parts worth copying are the *vision-analyse-the-product-first* step and async submit/poll.

### 3.4 Agency pipelines: where the humans sit
- Strategy and concept stay human, AI does production and variation, and a human makes the final judgement ([Balistro](https://www.balistro.com/blog/ai-generated-ad-creative)). Pipelines have six stages: brief → brand spec → generate/revise loop → **named human review gate per asset** → measurement → publish with an audit trail ([Thrad](https://www.thrad.ai/content/generative-ai-advertising-creative-workflows)). Approvals are moving *earlier*: clients validate direction and inputs before full generation ([Gain](https://blog.gainapp.com/ai-content-approval-process-predictions/)). Clients increasingly ask which parts were AI and which were human-refined. Agentic demos use about two human checkpoints ([oakgen](https://oakgen.ai/blog/agentic-creative-pipelines-2026)). All of these are vendor blogs; the pattern is consistent, the numbers are unverified.

### 3.5 Automated QC: the state of the art
- **VLM artefact judges.** Artifact-Bench evaluates MLLMs on AI-video artefacts: temporal inconsistency, structural distortion, semantic incoherence, weighted by severity, frequency and perceptibility ([arXiv 2605.18984](https://arxiv.org/pdf/2605.18984)). VQQA prompts a VLM to list flaws by visual quality, text alignment and physical consistency, then iterates generation ([arXiv 2603.12310](https://arxiv.org/pdf/2603.12310)).
- **VLM reliability caveat.** The best model reached 99.4% artefact detection recall but answered all grounding questions correctly on only 53% of images, so **demand localised evidence** (frame, region) for every verdict ([SalArt-VQA](https://arxiv.org/pdf/2606.12671)).
- **Hybrid triage beats a single judge.** Scale Labs found a contact-sheet VLM linter preserved more good clips than a CV-only checker. A whole-video VLM judge over-rejected. Cheap features alone (duration solved one failure mode at AUC 0.96) often matched VLMs, and adding VLM prompts to cheap features raised AUC by only +0.0008. Their recommendation: break QC into concrete failure modes, tune thresholds per rule, show the triggering frames, and "none of these checks should automatically reject clips without human confirmation" for high-impact calls ([Scale Labs](https://labs.scale.com/blog/from-video-review-to-measurement)).
- **Continuity metrics.** VBench subject consistency = mean cosine similarity of DINO features of each frame against the first and previous frames. Background consistency uses CLIP. Temporal flicker = mean absolute frame difference on static content ([VBench](https://arxiv.org/pdf/2311.17982), [VBench++](https://arxiv.org/pdf/2411.13503)).
- **Trademark screening.** Policy-style rules: no recognisable logos or trademark text, swoosh-like marks included ([UniVBench](https://arxiv.org/pdf/2602.21835)). The UNBRANDING benchmark covers trademark-safe T2I ([arXiv 2512.13953](https://arxiv.org/pdf/2512.13953)). Industry pipelines combine logo detection + OCR + human review of ambiguous hits ([Red Points](https://www.redpoints.com/blog/logo-misuse-detection/), [Mixpeek](https://mixpeek.com/use-cases/brand-logo-video-detection), [Corsearch](https://help.zeal.corsearch.com/en/articles/91-automated-image-feature-detection)). Negative-prompting brand names helps but does not replace image-level screening ([is4.ai](https://is4.ai/blog/our-blog-1/ai-trademark-brand-confusion-guide-2026-201)).
- A proposed "agentic QC for product visualisation" checks identity, colour fidelity, artefacts and wrong branding with VLM + CLIP, then iterates or rejects. It is a design sketch, not shipped ([Manifund](https://manifund.org/projects/verified-genai-agentic-qc-for-reliable-product-visualization)).

### 3.6 Cost control, retries, caching, versioning
- **Queues.** Prefer async submit + poll or webhook. Store the queue `request_id`, not the gateway id, which changes on retry. A client timeout does **not** cancel the job, so check status before resubmitting or you pay twice. fal retries 5xx/timeouts server-side up to 10×. Download large outputs promptly because stored results expire ([fal queue](https://fal.ai/docs/model-endpoints/queue), [fal webhooks](https://fal.ai/docs/model-endpoints/webhooks)).
- **Cache keys.** Hash only artefact-defining fields (prompt inputs, model route, mode, constraints, seed). Keep retry counts, timestamps and transport idempotency keys out of the hash ([Romitelli](https://dev.to/romiteld/a-cache-key-is-an-equivalence-relation-51g5)).
- **Budget.** No vendor offers a hard per-job cap through agent connectors; Higgsfield MCP's guard is prompt-level only ([Higgsfield](https://higgsfield.ai/blog/mcp-for-marketers)). Caps must live in our code, as `hfgen` already does per batch.

## 4. Proposed architecture

### 4.1 Principles
1. **Files are the state.** Every stage writes one JSON artefact plus human-readable views. A tiny `job.json` state machine records stage, status, approvals and spend. Any session, or a subagent, can resume from disk. This is the same idea as hfgen's resumable manifest, lifted to the job level.
2. **Maker ≠ checker.** The agent that writes prompts never grades its own outputs. QC runs in a separate subagent with only the brand kit, rubric and frames (the Scale/SalArt lesson: evidence-backed, per-failure-mode verdicts).
3. **Cheap before expensive.** Text gates → $0.004 Soul plates → $0.30 Flare stills → $0.48 Kling clips. Never animate an unapproved still (NOTEBOOK and playbook step 6).
4. **Money moves only through `hfgen.py` and `elevenlabs.py`**, and both go through one job-level spend ledger.
5. **Humans own taste and legal.** Agents own volume, consistency and measurement.

### 4.2 Job folder (versioned, append-only)
```
jobs/<client>-<product>-<yyyymmdd>/
  job.json                      # state machine + budget + approvals
  spend.jsonl                   # every paid call: est, billed, stage, cache_key
  00-intake/product.json brand_kit.json packshot.png label_crop.png
  10-ideas/ideas.json           # 7+ ideas from dice + free ideas
  20-tests/tests.json           # zero-cost test results, ranking
  30-storylines/storylines.json storylines.html (client page)  approval.json
  40-shotplan/shots.json plan_stills.v1.json
  50-stills/clips/… manifest.json  stills_qc.json  approval.json
  60-motion/plan_motion.v1.json clips/… manifest.json takes_qc.json
  70-audio/audio_plan.json vo.mp3 vo.words.json bed.mp3 sfx/  cache.json
  80-edit/edit.v1.json master_v1.mp4 cutdowns/
  90-qc/qc_report.json vision_qc.json rubric.json
  99-deliver/delivery.json  (+ files)
```
Rule: plan files are **versioned** (`.v1`, `.v2`), never overwritten. Every artefact carries a `parents` list (the ids it was made from), which gives lineage from prompt to still to clip to edit.

### 4.3 Stages, artefacts, gates

| # | Stage | Who / tool | Output | Gate (auto) | Human |
|---|---|---|---|---|---|
| S0 | Intake | Claude + `director.py new`; vision read of the packshot; optional URL extraction (WebFetch) | `product.json`, `brand_kit.json` | Label text transcribed exactly; hex colours; `[ASSUMED]` flags ≤ N | — |
| S1 | Ideas | `dice -n 5` + parallel **idea subagents** (one per seed, plus 2 free) | `ideas.json` (≥7) | Kill test (shared key visual), cliché ban, legal lines, 15 gates (text) | — |
| S2 | Zero-cost test | **sceptical media-buyer subagent** scores drivers → `director.py rank`; cold-viewer test; hook ×5 per idea | `tests.json` | Top 3 from ≥2 mechanisms, one "safe-but-sharp" | — |
| S3 | 3 storylines | Claude: BIG IDEA shot, beat map, VO script, frame 0; **optional** $0.004–0.02 Soul Cinema mood plates (no product) | `storylines.json` + client page (Artifact, private) | Each has BIG IDEA + CTA + brand by 3 s | **H1: client picks 1** (+ comments) → `director.py log` (chosen and rejected) |
| S4 | Shot plan | Claude + `model-router.md` | `shots.json`, `plan_stills.v1.json` | Each product shot has the PRODUCT LOCK line, one move, a model + backup, takes budget; ≥5 shot types per 20 s; `hfgen batch --dry-run` estimate ≤ stage cap | (auto unless over cap) |
| S5 | Stills | `hfgen.py batch` (Flare / Soul plates → Flare composite) | `50-stills/manifest.json` | **G-still** (4.5) | **H2: client approves stills** (no moving clip shown before this, except one crave teaser if budget allows) |
| S6 | Motion | `hfgen.py batch` i2v / start-end frames, `sound` off | `60-motion/manifest.json` | **G-take** (4.5); auto-retake within takes budget | — |
| S7 | Audio | `elevenlabs.py` music plan, SFX, VO | `audio_plan.json`, files | Duration fits beat map; VO ≈2.5 words/s; cache hit before any spend | (VO voice pick can join H2) |
| S8 | Edit + grade | `reelstudio.py render` + film chain | `edit.vN.json`, master, cutdowns | `reelstudio plan` validates; safe zones | — |
| S9 | QC | `director.py qc` + **QC subagent** (contact sheets) + rubric | `qc_report.json`, `vision_qc.json`, `rubric.json` | No FAIL, rubric ≥80, continuity pass | **H3: final approval** (internal director, then client) |
| S10 | Deliver | packager [proposal] | `delivery.json` | Spec check per platform; AI-disclosure note; licences | — |
| S11 | Learn | `director.py log --result`, NOTEBOOK retro, bench CSV keeper ratios | ledger, notebook | — | Real performance data in when available |

The client sees exactly **three** checkpoints: storyline pick, stills approval and final cut. This matches the industry move toward "approve direction before full generation" (3.4) and our F01 lesson: no stills-only animatics for clients.

### 4.4 Core schemas (abridged JSON; full JSON Schema files to be written when building)

**`job.json`**
```json
{"job_id":"aurum-water-20261007","client":"Driftline","product":"AURUM",
 "stage":"S5","status":"awaiting_human|running|blocked|done",
 "budget":{"cap_usd":12.0,"stage_caps":{"S3":0.10,"S5":3.5,"S6":5.0,"S7":0},"reserve_usd":2.5,
           "spent_usd":4.21,"committed_usd":1.44},
 "approvals":[{"gate":"H1","by":"client","at":"2026-10-07T14:02","choice":"storyline_B","notes":"less gold"}],
 "taste":{"tone":"aesthetic_brand_film","no_talking_heads":true},
 "versions":{"plan_stills":"v2","edit":"v1"},
 "history":[{"stage":"S4","event":"done","at":"…"}]}
```

**`brand_kit.json`**: `{name, label_text:["AURUM","SOURCE 1987"], colours:{primary:"#C9A65A",secondary:"#0E6E73"}, typeface, sonic_logo, forbidden_marks:["swoosh","three stripes",…], packshot:"packshot.png", label_crop:"label_crop.png", colour_world:"champagne gold + glacier teal"}`. This file is the QC oracle for OCR, colour and logo checks.

**`storylines.json`**
```json
[{"id":"B","title":"Sunset in a bottle","seed":{…from dice…},"mechanism":"literalised claim",
  "big_idea_shot":"sun sets into the bottle","frame0":"…","claim":"Wear the golden hour",
  "beats":[{"t":[0,2],"beat":"hook","visual":"…","sound":"…"}],
  "vo":"…","cta":"Discover the sample set","drivers":{"hook":4,…},"rank":{"total":71,"weakest":"saves"},
  "est_cost_usd":9.4,"risks":["orbit >60° morphs label"],"mood_plates":["30-storylines/B_1.png"]}]
```

**`shots.json`** (one row per shot)
```json
{"id":"S03_drop","t":[4.0,5.6],"size":"macro","angle":"3/4 low","lens":"100mm macro",
 "move":"slow push-in, ends on logo","only_moves":"one droplet",
 "method":"I2V","model":"kling-video/v3.0/pro/image-to-video","backup":"seedance-2.5/i2v",
 "risk":"B","takes":2,"still_prompt":"…","motion_prompt":"…","product_lock":true,
 "parents":["storyline:B"],"prompt_version":"v2"}
```

**Take QC record** (`takes_qc.json` / `stills_qc.json` entries)
```json
{"take":"S03_drop#2","file":"60-motion/clips/S03_drop_t02.mp4","cache_key":"sha256:…",
 "auto":{"ocr_label":{"expected":"AURUM","read":"AURUM","match":1.0},
         "colour_dE":3.1,"subject_consistency":0.94,"flicker_events":0,"freeze":false},
 "vision":{"K1":"pass","K2":"pass","K6":"warn: reflection shows 2nd bottle @3.2s",
           "evidence":["qc/S03_t02_f19.jpg"],"trademark":"none","score":8},
 "verdict":"keep|retake|reroute|human","reason":"…"}
```

**`spend.jsonl`** line: `{"at","stage","tool":"hfgen|elevenlabs","job":"S03_drop#2","cache_key","est_usd","billed_usd|null","request_id","status"}`.

**`delivery.json`**: masters and cutdowns (6 s / 15 s / 30 s), aspect variants, 5 hook variants, file hashes, `qc_report` refs, `ai_disclosure`, `music_licence` (ElevenLabs plan terms), `consent:[]`, `parents`.

### 4.5 Automated QC gates (cheap first, VLM second, human last)
Following Scale Labs: a per-failure-mode rule, evidence frames, and thresholds calibrated on our own labelled takes.

**G-still** (every still, before H2):
1. **Label OCR** on the product region versus `brand_kit.label_text` (normalised edit distance ≤1 char, else retake). `[inf]` tesseract or a VLM read; Flare composites usually pass and Soul never does (12-higgsfield-mastery: "Soul Cinema can't spell").
2. **Colour fidelity**: product-crop ΔE versus the packshot palette. This extends `product_match` from a histogram to a Lab ΔE [inf].
3. **Trademark screen**: the QC subagent is asked only "list any logos, brand marks or text not in `brand_kit`", with a crop for each hit. Any hit → retake with a "plain unbranded" line (NOTEBOOK E06). Ambiguous → human.
4. **Image rubric ≥8/10** (`image-direction.md`) plus the anti-AI list (off-centre, hard light falloff, imperfections).

**G-take** (every clip):
1. **Cheap metrics (free, ffmpeg/stdlib):** freeze, black, luma flicker (existing), duration, first-vs-last-frame product-crop similarity (K2 drift proxy; DINO if available, else SSIM/histogram [inf]), OCR on 3 frames (start, middle, end) for K1.
2. **VLM contact-sheet review:** `reelstudio.py grid` at 4×3 plus 0.5× crops around contact moments, scored against K1–K8 with the frame index cited. A verdict with no evidence counts as "human".
3. **Decision:** all pass → keep. One K fail → retake with the same prompt (counts against `takes`). The same K fails twice → **reroute** to the backup model or switch method (composite the packshot, end-frame lock, shorten the orbit). Budget exhausted → `blocked`, asking the human.

**G-continuity** (across selected takes, before the edit): palette distance between shots (one colour world), product-crop similarity across shots (same bottle), and a shot-type variety count (≥5 per 20 s). It outputs a matrix flagging outlier shots [inf].

**G-render:** `director.py qc` (existing) + rubric ≥80 + cold-viewer subagent ("what is it / why want it / what do I do?") + safe-zone sheet review + legal checklist (no AI testimonials, no AI before/after, disclosure).

The VLM is never the only reason to reject at H-level gates. It routes; humans decide on ambiguous or high-impact calls ([Scale Labs](https://labs.scale.com/blog/from-video-review-to-measurement), [SalArt-VQA](https://arxiv.org/pdf/2606.12671)).

### 4.6 Budget guards
1. **Job cap + stage caps + reserve** in `job.json` (default from the ≈$10 flagship template; reserve about 25% for retakes).
2. **Pre-flight:** every paid stage runs `hfgen batch --dry-run` first. Stage estimate + `spent` + `committed` must stay ≤ cap, else stop and ask (extend `hfgen` with `--job job.json` so it reads and writes the shared ledger) [proposal].
3. **Reconcile:** record `billed_usd` from `gen_log` or the account balance delta. If billed exceeds estimate by more than 10%, pause the job [inf]. Today `spent` is only `est_usd`.
4. **Take economics:** a per-shot `takes` budget. Two consecutive same-K fails trigger a reroute, never infinite retries. Keeper ratio per model goes to the bench CSV so the router learns.
5. **ElevenLabs:** estimate characters and seconds before calling, check `elevenlabs.py check` credits, and cache by `sha256(endpoint, text|prompt, voice, model, settings, seconds)` → reuse the file. Today a re-run pays again.
6. **Free-first defaults:** `sound` off on Kling/Seedance (+50%), 720p for exploration, Soul Cinema at $0.004 for plates and moodboards, Flare only for product frames.
7. **Human spend approval:** any single call over $2, or a stage over its cap, needs an explicit "yes" (hfgen's `--yes` stays human-only; agents run `--dry-run`).

### 4.7 Caching, idempotency, versioning
- **Cache key** = sha256 of the canonical JSON of {model, args with uploaded-ref *content hashes* instead of URLs, seed, prompt_version}. Exclude salt, timestamps and retry counts ([Romitelli](https://dev.to/romiteld/a-cache-key-is-an-equivalence-relation-51g5)). hfgen's `idem_key` already hashes job + take + args; it should store a separate creative `cache_key` so the same still requested by two shots is generated once [inf].
- **Uploads:** keep the `manifest.uploads` map (already present), keyed by file hash rather than path [proposal].
- **Async safety:** on timeout, check `status(request_id)` before resubmitting; hfgen's idempotency key already protects against double-pay on Higgsfield. Download immediately ([fal queue](https://fal.ai/docs/model-endpoints/queue)).
- **Versioning:** plans and edits are `.vN`, artefacts carry `parents`, approvals pin versions (`"approved":"plan_stills.v2"`). A revision after H2 creates `v3` and invalidates downstream stages automatically.

### 4.8 Where Claude Code skills and subagents fit
| Role | Implementation | Why separate |
|---|---|---|
| **Orchestrator** | The `ad-director` skill + a new `pipeline.py` (`status`, `next`, `approve`, `spend`, `invalidate`), stdlib only, unit-tested like `director.py` [proposal] | Deterministic state; any session resumes |
| Idea generators (×5–7, parallel) | Subagents, each given one dice seed + brief + `creative-brain.md` | Diversity; no anchoring on idea 1 |
| Sceptical media buyer | Subagent scoring drivers blind to the idea's author | Avoids self-grading inflation |
| Storyline writer | Main agent (needs whole-job context) | — |
| **QC judge** | Subagent with brand kit + rubric + frames only, no prompts | Maker ≠ checker; evidence-based |
| Legal / trademark screener | Subagent with legal lines + `forbidden_marks` | Narrow, high-precision |
| Cold viewer | Subagent given only the final contact sheet + VO text | Simulates a first view [inf: a weak proxy, not real data] |
| Editor | Main agent writing `edit.json` → `reel-studio` | — |
| Client pages | Artifact (private) for storylines and stills approval; choices recorded back into `approval.json` by Claude | Clear human checkpoint |


### 4.9 Failure handling
| Failure | Detection | Action |
|---|---|---|
| API 5xx / 423 / concurrency | hfgen `_request` | Built-in retry with backoff (exists) |
| Client timeout while the job is still running | poll timeout | `status(request_id)`, never blind resubmit |
| `nsfw` / safety refusal | status `nsfw` | Rewrite the prompt with the safer framing from the NOTEBOOK (hand + blazer instead of bare shoulder); counts as a take |
| Label drift (K1) ×2 | G-take OCR | Reroute: shorter or ≤60° move, end-frame lock, or composite the real label in post |
| Trademark hit | G-still / G-take screen | Retake with "plain unbranded"; never deliver with a hit |
| Continuity outlier | G-continuity | Regenerate that still from the approved still as a reference, or regrade |
| Over budget | pre-flight / reconcile | `blocked`, with options: fewer takes, 720p, cut a shot, raise the cap (human) |
| Client rejects a storyline or stills | H1/H2 | Log `rejected` with reasons in the ledger; re-roll dice with locks; at most 2 rounds before a call |
| Render QC FAIL / rubric <80 | G-render | Top-3 fixes by point gain (existing rule), new `edit.vN` |
| Crash mid-stage | `job.json` stage = running | Re-run the stage; manifests skip completed work |

### 4.10 "Zero-cost testing" (S2) concretely
1. `director.py rank` on drivers scored by the sceptical subagent (exists).
2. Five hook variants per finalist, as text + frame-0 descriptions, scored blind by a second subagent [inf].
3. Cold-viewer comprehension test on the storyline text: is the product, desire and action clear within 3 s of description?
4. Optional near-zero step: 4 Soul Cinema mood plates per storyline (about $0.02) for the H1 page. No product in plates, because Soul ignores product refs.
5. Real tests (paid media, about $10/hook) stay **after** delivery. Their results go back into the ledger via `log --result` and into `live-results` reporting. Synthetic scores only order options; they never forecast numbers (SKILL.md 4b).

## 5. Build order (when we build)
1. `pipeline.py` + `job.json`/`spend.jsonl` + tests; wire `hfgen --job` to the shared ledger. (Smallest change with the biggest safety gain.)
2. ElevenLabs cache + estimate.
3. G-take cheap metrics (OCR, first/last drift, continuity matrix) in `director.py qc-take`.
4. QC-judge subagent prompt + evidence contact sheets.
5. Client approval pages (Artifacts) for H1/H2.
6. Delivery packager.

Calibrate thresholds on 50–100 of our own labelled takes before trusting automatic retakes [inf].
