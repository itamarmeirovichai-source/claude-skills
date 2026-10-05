# Brief for every agent in the research org (read fully before starting)

You are part of a large research organization (supervised by a lead Claude) studying viral AI-generated video reels so the user (an Israeli creator, writes Hebrew) can MAKE videos like these and EARN MONEY: (a) selling to clients/brands, (b) for own products, (c) for views/creator payouts/affiliate, (d) courses/guides.

Today is 2026-10-05. Your training data is OLDER than the tools involved (Seedance 2.5, Higgsfield Genjutsu, etc. launched Aug-Oct 2026), so you MUST use WebSearch / WebFetch (load via ToolSearch "select:WebSearch,WebFetch") heavily and prefer 2026 sources. Cite source URLs inline. Mark anything unverified as [לא מאומת].

PRIMARY SOURCES (read first):
- `research/ai-video-reels/chapters/00-visual-analysis.md` — the supervisor's frame-by-frame analysis of the 10 source reels, including the actual prompts shown on screen and transcripts. Treat as ground truth about the reels.
- `research/ai-video-reels/00-source-reels.md` — captions & stats.
- Frame grids: `research/ai-video-reels/assets/frames/<ID>.jpg` (view with Read if useful).
- Already finished worker reports: `research/ai-video-reels/workers/A1.md` (deep dive on the 10 reels) and `A2.md` (catalog of 40+ similar reels/creators + format taxonomy). Skim them to avoid duplicating; build on them.

Key facts: the reels use Higgsfield (Seedance 2.5 1080p, Genjutsu "hybrid production" video-to-video: original footage + up to ~6 reference images + one-line prompt; AI influencer; API with cashback; $1M film festival; ANERNEQ 20-min open AI film), Lovart.ai (Seedance 2.5 "infinite camera angles" from one take; workflow = timecoded shot list → Claude expands into timecoded prompt referencing @Video1 → Lovart), and creators @edbert_yienson (one passport photo + timecoded multi-shot prompt → 30s Lamborghini Dubai ad; 24K comments), @rourke, @sidequestpat_, Israeli @maorhani1 (split-screen: parking garage + cheap car → Hotel de Paris + Rolls-Royce, Hebrew dialogue preserved). All use "comment KEYWORD → DM" funnels.

Tricks: Instagram metadata: `curl -A "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)" https://www.instagram.com/reel/<ID>/` (rate-limited, sleep 20s, retry on 302). Video download: `yt-dlp --impersonate chrome -f b <url>` works (installed).

Writing rules: Hebrew (clear, practical, headings/tables), but keep tool names, technical terms and ALL example prompts in English. Concrete: numbers, prices (USD and ILS where relevant), step-by-step, real examples, copy-paste prompts. No fluff. Start with "תקציר" and end with "מקורות".

## Supervisor notes for division heads / editors (added later)
- **FX rate:** USD/ILS = **3.04** (open.er-api.com, 05.10.2026). Some workers used 3.6 — recompute ILS figures with 3.04.
- The session's WebSearch quota (200) is exhausted. Use WebFetch on specific URLs if you must verify; otherwise preserve [לא מאומת] marks.
- Sora was shut down (app 26.04.2026, API 24.09.2026) — do not recommend it.
