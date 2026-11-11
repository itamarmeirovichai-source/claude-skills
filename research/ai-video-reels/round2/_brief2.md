# Round 2 brief (read fully)

Goal: the user (Israeli creator, Hebrew) wants Claude to MASTER (1) writing prompts in every format — whole videos, individual shots/parts, images/keyframes, reference images — and (2) assembling/editing finished reels programmatically (Claude edits via ffmpeg: cuts, layouts, transitions, effects, Hebrew captions, music/SFX) so the user can later say "add effects" and Claude does it.
Today: 2026-10-05. Existing research: research/ai-video-reels/ (README.md, chapters/00..13). Skim README.md + chapters/00-visual-analysis.md first; chapters/03-craft.md and 07-prompt-library.md are the current knowledge on prompting/editing — your job is to go BEYOND them with new primary material.

## Tools & constraints
- WebSearch quota of this session is EXHAUSTED. Do not rely on WebSearch.
- YouTube works great via yt-dlp (installed, use `--impersonate chrome` only if needed):
  - search: `yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(view_count)s|%(duration)s|%(upload_date)s" "ytsearch25:<query>"` (prefer 2026 uploads; add "2026" or model names to queries)
  - transcripts (no video download): `yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt -o "<dir>/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=<id>"` then strip VTT timing/dup lines with a small python script.
  - video (low res for analysis): `yt-dlp -f "b[height<=720]/b" -o "<dir>/%(id)s.%(ext)s" <url>`
  - Be gentle: sleep 3-5s between calls; on 429 wait 60s and retry.
- Instagram reels: `yt-dlp --impersonate chrome -f b https://www.instagram.com/reel/<ID>/` works (rate-limited; sleep 20s).
- Web pages: WebFetch, or `curl -s https://r.jina.ai/<full-url>` for blocked pages.
- ffmpeg 6.1 with libass, xfade, zoompan, lut3d, scdet, frei0r, vidstab is installed. faster-whisper is installed (python). Hebrew font: download Heebo with `curl -sL -o heebo.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/heebo/Heebo%5Bwght%5D.ttf"`.
- Scratch dir for downloads (NOT the repo): /tmp/claude-0/-home-user-claude-skills/aaa2c01d-bf13-5125-acac-effcc169b0f4/scratchpad/r2/<your-id>/ . Delete big videos when done. Never commit videos.
- Known new models seen on YouTube (Oct 2026): Kling 4.0, GPT Image 2.5, Suno v6, "GPT 6 Astra" — verify what they are.

## Output rules
- Write your notes to research/ai-video-reels/round2/notes/<your-id>.md (Hebrew explanations; ALL prompts/templates/commands in English; cite YouTube video IDs/titles + timestamps as sources, e.g. [YT:FJfMTvZvX7w 04:12]).
- Concrete > generic: exact prompt structures, exact settings, real examples copied from tutorials (mark [מתוך מדריך]), failure modes + fixes, numbers.
- Do NOT git commit.
