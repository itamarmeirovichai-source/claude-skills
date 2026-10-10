---
name: vxo-daily
description: The daily self-improvement routine for VXO. Each day keep the lead pipeline fresh and measured, re-verify live signals, verify the most decision-critical unverified facts, research one topic that changes how we sell or film, find up to 5 HOT leads with dossiers and drafted messages (never sent), and write a dated daily note. Zero generation spend. Used by the scheduled daily routine; also run when the owner says "daily", "learn more", or "keep researching".
---

# VXO daily: pipeline first, then learn, then leads (zero spend)

**Why the order changed (2026-10-09 ops audit).** By 2026-10-09 we had 65+ research docs, ~85 drafted messages and **zero sends, zero replies, zero daily notes** (`daily/` was empty because the routine's push was blocked and nothing was saved elsewhere). More research does not fix that. The routine now keeps the pipeline honest first, verifies the facts we are about to quote, and researches second.

**Rules (never change):**
- Read `research/ai-video-reels/lab/LESSONS.md` first. LESSONS beats every doc and this skill.
- Zero generation spend: never call `hfgen.py batch/run`, `elevenlabs.py`, or any paid API.
- Never send, post, submit or comment anything to anyone. No logins. Public data only.
- Never read, print or commit API keys. Never commit media (films, frames, downloads stay in the scratchpad).
- The direction is fixed (Short / Premiere / Season films through the agreed funnel). A finding is a way to make THOSE films sell; never write it up as a new product or a new buyer.
- Commit only docs and scripts to branch `research/ai-video-reels`.

Commit trailer (exactly):
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_012RfHc9yUsHmHnJmjYqioEL
```

## Step 0 · Preflight (5 minutes; never skip)
1. `git pull --rebase origin research/ai-video-reels`. Then `git push --dry-run origin HEAD:research/ai-video-reels`.
   - If the dry run fails, **keep working**, but write everything to the repo AND copy the daily note to the scratchpad (`$SCRATCH/daily/YYYY-MM-DD.md`). Put `PUSH BLOCKED: <error line>` as the first line of the Hebrew summary so the owner sees it on his phone. Commit locally; the next run pushes both days.
   - On a rejected push: `git pull --rebase origin research/ai-video-reels` and push again (max 3 tries).
2. Source health check. Record each as OK / BLOCKED / DEGRADED in the daily note's "Sources" line:
   - Meta Ad Library: `python3 skills/ad-director/scripts/research/ad_library.py page 525487920847043 --label probe` (The Foggy Dog; expect a count, ~200+). curl gets 403; the headless browser works.
   - Web search: budget **20 searches per run**. Write the query list first, spend searches only on the top items, and fall back to WebFetch of known primary URLs when the quota runs out (it ran out mid-run on 2026-10-09).
   - TikTok: `yt-dlp` works. YouTube: usually bot-blocked (429); use TikTok, the brand's own site videos, or Ad Library video URLs instead. Don't burn the run retrying YouTube.
   - Video understanding: there is no Gemini key. Use ffmpeg frame strips (4–10 fps around the hook, 1 fps overall) plus Claude reading the images, `ffmpeg ebur128` for loudness, and the QC tools in `skills/ad-director/scripts/qc/`. Say "frame-read, not model-read" next to any finding that rests on it.
3. Read: LESSONS, the last 3 files in `research/ai-video-reels/daily/` (or the scratchpad copies if the push was blocked), `leads/PIPELINE.md`, the top of `lab/RESEARCH_BACKLOG.md`, and `skills/ad-director/references/marketing/00-INDEX.md`.

## Step 1 · Pipeline upkeep (before any new research)
For every lead in `leads/PIPELINE.md` that isn't `won`, `lost` or `hold`:
1. **Re-verify the live signals** if they are older than 7 days, or if the lead is next to send: `ad_library.py brand "Name@domain"` (active ads, video filter share AND card video share, ads started in the last 30 days), the store's `/products.json` (new products, stock of the products the message names), and the contact address on the brand's own site. Update the dossier's Verification table with the date. A Motion or other third-party snapshot older than 30 days **may not be quoted** anywhere; replace it with a live read or drop it.
2. **Check the message still holds:** a named product still public and in stock, no hidden SKUs (`redirect-to-404`, `hidden`, `available: false`), no claim LESSONS bans. If it broke, fix the draft and say so.
3. **Status and next action:** every line ends with a status (`found / approved / sent / replied / frames sent / won / lost / hold`) and a dated next action. Follow-ups that are due today go at the top of the daily note.
4. **Outcomes:** if the owner reported sends or replies since the last run, log them in PIPELINE.md and update the scoreboard (Step 5). Never mark anything `sent` unless the owner said so.

## Step 2 · Verify before you learn (30 minutes max)
Take the top 3 unchecked items in the backlog's "Verify" section (decision-critical `[unverified]` facts). For each: find a primary source or measure it yourself, then edit the doc in place: replace `[unverified]` with the source, or mark it `[refuted YYYY-MM-DD]` with the correct figure. Check it off. If a fact feeds a client message, a price or a policy rule, also fix that message, price note or rule.

## Step 3 · Learn one thing deeply
1. Take the top unchecked topic in the backlog's "Research" section.
2. Research it with the sources from Step 0. Analyse at least 3 real examples (frame strips you look at, audio onsets, Ad Library cards with start dates).
3. **Extend an existing doc when one fits** (use 00-INDEX). Only start a new doc when nothing fits. To pick a number, run `git fetch origin && git ls-tree --name-only origin/research/ai-video-reels skills/ad-director/references/marketing/` and `ls` the folder; take the next number free in **both**. Then add or update its row in `00-INDEX.md`.
4. Tag every claim: `[m]` measured today, `[c]` the company's own claim, `[v]` vendor, `[inf]` inference, `[unverified]` no primary source. No numbers without a tag.
5. **"Done" means something changed.** The topic is done only when it produced at least one concrete edit to `vxo-film`/`vxo-leads`, a `[self]` rule in LESSONS, a fixed draft, or a backlog item it resolved. If it changed nothing, say so in the note and pick a more useful topic tomorrow.
6. Check the topic off and add up to 2 new topics, at most one of them "nobody asked, but it would make us better". New topics must serve finding leads, closing them, or making the films better; no pivots.

## Step 4 · Find leads (vxo-leads)
Run the `vxo-leads` skill. Write up to 5 HOT (70+) leads with dossiers and drafted messages to `research/ai-video-reels/leads/YYYY-MM-DD.md` and append them to `leads/PIPELINE.md`. Not sent.
- Live ad counts come from `ad_library.py`, never from a stale snapshot. Quote both the filter share and the card share.
- **If the queue already holds 5+ approved-but-unsent leads, find at most 1 new lead today** and spend the time on Step 1 instead. Unsent drafts go stale (stock, launches, ad counts change weekly).

## Step 5 · Daily note
Write `research/ai-video-reels/daily/YYYY-MM-DD.md` in this order:
1. **Hebrew summary at the top**, at most 8 lines, for the owner's phone. Line 1: `PUSH BLOCKED` if it was, else the single most important thing he must do today (usually: approve or send message X).
2. **Scoreboard** (cumulative): leads found · approved · sent · replies · positive replies (frames requested) · frames delivered · sales · revenue · generation spend this week (from the ledgers; it must be $0 for this routine). Target from doc 63: ≥ 2 positive replies per 30 sends; if below after 30 sends, change channel/sender first, then the idea, last the wording.
3. **Sources:** Ad Library / web search (used n of 20) / TikTok / YouTube / video understanding: OK, BLOCKED or DEGRADED.
4. **Pipeline:** follow-ups due, leads re-verified (what changed), drafts fixed.
5. **Verified today:** the 3 facts and what they changed.
6. **Learned:** 3 bullets, plus what changed in our system (files).
7. **Leads found** (names, scores).
8. **One film idea of the day** (hook in second 1, product-caused punchline).
9. **Questions for the owner** (only decisions only he can make).

## Step 6 · Commit and push
`git add` only the files you changed (never `-A`; never media). Commit with the trailer above, push, and on rejection pull with rebase and push again. If the push still fails, leave the commit local, keep the scratchpad copy, and say so in the Hebrew summary.
