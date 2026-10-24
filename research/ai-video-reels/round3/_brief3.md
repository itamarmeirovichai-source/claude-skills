# Round 3 brief: AI PRODUCT ADS across every niche (read fully)

Goal: make Claude (and the user, an Israeli creator) a true EXPERT in producing and selling AI-generated PRODUCT ADS for every niche — with beverages/drinks as a priority niche. Cover: what top-performing ads in the niche look like (structure, hooks, shots, pacing, music), how to produce them with AI (Seedance 2.5, Kling 4.0, Higgsfield Genjutsu/Ads/Marketing tools, Nano Banana/GPT Image 2.5 for packshots), exact prompts (keyframe/image prompts, per-shot video prompts, full multi-shot prompts), reference images needed (product photos, logo lock), editing/effects/sound per niche, ad formats per platform (Meta/TikTok/Reels/Shorts/YouTube), regulations & claims rules per niche (esp. Israel: alcohol advertising law, health/cosmetics claims, kids), what clients in that niche pay, how to find & pitch them, and spec-ad ideas.
Date: 2026-10-05. FX USD/ILS = 3.04.
Existing research: research/ai-video-reels/README.md and chapters/ (esp. 03-craft, 05-monetization, 07-prompt-library, 10-numbers-capacity-pricing — official prices/costs). Build BEYOND them.

## Tools & constraints (same as round 2)
- WebSearch quota of this session is EXHAUSTED — don't rely on it.
- YouTube via yt-dlp works:
  - search: `yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(view_count)s|%(duration)s|%(upload_date)s" "ytsearch25:<query>"`
  - transcripts: `yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt -o "<dir>/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=<id>"` (clean VTT with python)
  - video: `yt-dlp -f "b[height<=720]/b" -o "<dir>/%(id)s.%(ext)s" <url>`; sleep 3-5s between calls; on 429 wait 60s.
- Analyze ads you download: frame grid (`ffmpeg -i v.mp4 -vf "fps=N,scale=240:-1,tile=6x4" -frames:v 1 grid.jpg`) and VIEW it with Read; cut times via `-vf "select='gt(scene,0.3)',showinfo"`; transcript via faster-whisper (installed). Save useful grids (<=250KB) to research/ai-video-reels/round3/grids/<id>-<video>.jpg.
- Web pages: WebFetch or `curl -s https://r.jina.ai/<full-url>`.
- Scratch dir for downloads (NOT repo): /tmp/claude-0/-home-user-claude-skills/aaa2c01d-bf13-5125-acac-effcc169b0f4/scratchpad/r3/<your-id>/ ; delete videos after. Never commit videos.

## Output
research/ai-video-reels/round3/notes/<your-id>.md — Hebrew explanations, ALL prompts in English. Required sections for niche agents:
1. תקציר
2. Anatomy of winning ads in the niche (with analyzed examples + grids + YouTube IDs)
3. Shot library for the niche (20+ shot types: e.g. for drinks: pour, splash, condensation macro, ice drop, can crack, slow-mo fizz, bartender, lifestyle sip…) each with an English video prompt + required reference
4. 3 complete ad blueprints (15s / 30s / UGC-style): shot list with timecodes, keyframe prompts, video prompts, edit/effects/music notes, CTA
5. Product fidelity: how to keep label/logo/shape (reference sets, PRODUCT LOCK lines, compositing real packshot in edit)
6. Platform specs & hook library (Hebrew + English hooks)
7. Rules/claims/regulation for the niche (Israel + platforms), marked [לא מאומת] if not verified
8. Business: who buys (Israeli examples of brands/businesses in niche), what they pay (₪), packages, outreach angle + 1 Hebrew pitch message, 5 spec-ad ideas
9. Sources (YT IDs + timestamps, URLs)
Do NOT git commit.
