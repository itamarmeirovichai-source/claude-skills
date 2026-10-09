---
name: vxo-daily
description: The daily self-improvement routine for VXO. Each day research one new topic, update the knowledge docs, find up to 5 HOT leads with drafted messages (never sent), and write a dated daily note. Zero generation spend. Used by the scheduled daily routine; also run when the owner says "daily", "learn more", or "keep researching".
---

# VXO daily: learn, improve, find leads (zero spend)

**Rules:**
- Zero generation spend: never call `hfgen.py batch/run` or `elevenlabs.py`.
- Never send outreach.
- Never read or print API keys.
- Commit docs only (no media) to branch `research/ai-video-reels` and push. If the push is rejected, `git pull --rebase` first.

Commit trailer:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_012RfHc9yUsHmHnJmjYqioEL
```

## Steps
1. **Remember.**
   - Read `research/ai-video-reels/lab/LESSONS.md`.
   - Read the last 3 files in `research/ai-video-reels/daily/`.
   - Read `research/ai-video-reels/lab/RESEARCH_BACKLOG.md`.
2. **Learn one thing deeply.**
   - Take the top unchecked topic from the backlog.
   - Research it with WebSearch/WebFetch. `yt-dlp` works for TikTok; YouTube may rate-limit.
   - Download and analyse at least 3 real examples (ffmpeg cuts, frame tiles you look at, audio onsets).
   - Write or extend the matching doc in `skills/ad-director/references/marketing/` (next free number), with sources.
   - Check the topic off and add 2 new topics you discovered, including at least one "nobody asked, but it would make us better" topic.
3. **Improve the system.**
   - Turn any finding that changes how we work into a concrete edit of `.claude/skills/vxo-film/SKILL.md` or `vxo-leads/SKILL.md`, or a new rule in `LESSONS.md` marked `[self]`.
4. **Find leads.**
   - Run the `vxo-leads` skill.
   - Write up to 5 HOT (70+) leads with drafted DMs to `research/ai-video-reels/leads/YYYY-MM-DD.md` and append them to `leads/PIPELINE.md`. Not sent.
5. **Daily note.**
   - Write `research/ai-video-reels/daily/YYYY-MM-DD.md` in this order:
     - 3 bullets: what I learned;
     - what I changed in our system;
     - the leads found (names and scores);
     - one film idea of the day;
     - open questions for the owner.
   - Hebrew summary at the top, at most 8 lines, for the owner's phone.
6. Commit and push.
