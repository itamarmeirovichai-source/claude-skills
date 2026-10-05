# Round 4 brief: THE CREATIVE BRAIN (read fully)

Goal: turn Claude into a world-class CREATIVE DIRECTOR for AI-generated ads — able to generate the best, boldest, "crazy-but-on-brand" ideas (the kind big brands win Cannes Lions / go viral with), grounded in consumer psychology and marketing science, and then translate those ideas into shot lists and prompts for AI video (Seedance 2.5, Kling 4.0, Higgsfield Genjutsu, image models). The user is a creator in Boca Raton, FL (USA), selling AI video ads to brands and local businesses.
Date: 2026-10-05. Existing research (Hebrew): research/ai-video-reels/README.md, chapters/ (03-craft, 07-prompt-library), round2/ and round3/ notes (in progress). Build BEYOND them.

## Tools & constraints
- WebSearch quota is EXHAUSTED. Use: YouTube via yt-dlp (search: `yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(view_count)s|%(duration)s|%(upload_date)s" "ytsearch25:<query>"`; transcripts: `yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt -o "<dir>/%(id)s.%(ext)s" <url>`; video at <=720p for analysis; sleep 3-5s; on 429 wait 60s), WebFetch, and `curl -s https://r.jina.ai/<full-url>` for articles (Wikipedia, Cannes Lions, Ads of the World, AdAge, The Drum, LBBonline, Campaign, Think with Google, IPA, System1, Ehrenberg-Bass pages).
- To study an ad: download it, make a frame grid (`ffmpeg -i v.mp4 -vf "fps=N,scale=240:-1,tile=6x4" -frames:v 1 grid.jpg`) and VIEW it with Read; transcript via faster-whisper (installed).
- Scratch dir (NOT repo): /tmp/claude-0/-home-user-claude-skills/aaa2c01d-bf13-5125-acac-effcc169b0f4/scratchpad/r4/<your-id>/ ; delete videos after.

## Output
research/ai-video-reels/round4/notes/<your-id>.md — write in ENGLISH (this will become Claude's own operating knowledge), with a short Hebrew summary at the top. Be concrete: name real ads/campaigns (brand, agency, year, link), the creative MECHANISM behind each (why it worked), and actionable rules/tools. Every principle should end with "How to apply to an AI video ad" + an example prompt or concept where relevant. Cite sources. Do NOT git commit.
