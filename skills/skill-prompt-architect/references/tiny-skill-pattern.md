# Tiny Skill Pattern — single-file behavioral skills for claude.ai

Source case study: `smooth-brain` by Jesse Rurka (@jesserurka) —
https://glamorous-pencil-2e4.notion.site/smooth-brain-make-Claude-actually-pick-388f8ee1272181ee83f9d45e3b49ce51
A 2.6 KiB single-file skill that turns Claude from "well, it depends…" into "No. Here's your answer." Shipped as a finished product with install page, demo, and safety note. Proof that tiny + one-job beats big + comprehensive when the goal is changing Claude's *response behavior*.

## When this track applies
All four must hold:
1. Audience uses **claude.ai** (or any Claude surface) — no Claude Code, no terminal.
2. The skill changes **how Claude answers** (style, format, decision behavior) — not what tools it runs.
3. Zero scripts, zero network, zero file operations.
4. **One job.** If you need "and also…", it's two skills or the Full Package track.

If any fail → Full Package track (main SKILL.md workflow).

## Design rules (extracted from smooth-brain)

1. **One behavior, not a toolkit.** The skill does exactly one thing to Claude's output. Name states the behavior; description states the trigger.

2. **The response IS the spec.** Write the exact target answer before writing any instructions. smooth-brain's spec is literally: `"No. Don't text them. If it was a good idea, you wouldn't be asking."` — verdict + one-line reason, nothing else. Design the skill backwards from that string.

3. **Before/after is the design test.** Take one flagship prompt, write Stock-Claude's answer and With-Skill answer side by side. No dramatic visible diff → don't ship. This before/after pair is also the core eval AND the core marketing asset.

4. **Generalize with a behavior table.** 4–5 rows of `You ask → Claude does` prove the skill works beyond the flagship example:
   | You ask | Claude does |
   |---|---|
   | "What should I build next?" | Picks one. Tells you why in a sentence. |
   | "What should I charge?" | Gives a number, not a pricing framework. |
   If you can't fill 4 honest rows, scope is too narrow for a skill — it's a prompt.

5. **No escape hatch.** The instruction must close Claude's default outs explicitly (hedging, menus, "it depends", frameworks instead of answers, follow-up questions instead of commitment). The value of a behavioral skill is the model *refusing* to waffle.

6. **Honest boundary — "when NOT to use" is part of the product.** State where the behavior is wrong (e.g., medical/legal/irreversible calls where "it depends" is the honest answer). One sentence framing: the behavior is a feature, not a substitute for judgment.

7. **Trust by transparency.** The whole skill must be readable in a text editor in under a minute. No fetches, no code, nothing outside the chat. Teach users the habit: *read any skill file before loading it* — include that line on the distribution page.

## Size + shape targets
- Whole SKILL.md: **≤ 3 KiB** (~60 lines). Frontmatter + behavior contract + 2–3 examples + boundary.
- Description frontmatter: < 200 chars (claude.ai limit-safe), trigger words the end-user would actually type.
- No references/, no scripts/, no assets/. One file.

## Packaging as `.skill` for claude.ai
- Official format: zip the skill folder (SKILL.md at root), rename extension to `.skill`:
  ```bash
  cd <parent-dir> && zip -r <skill-name>.skill <skill-name>/
  ```
- smooth-brain ships as plain readable text — for a single-file skill, keep the inner SKILL.md the only payload so the "open it in a text editor" promise stays true.
- Install (put these exact steps on the distribution page):
  1. Download `<name>.skill`.
  2. claude.ai → Settings → Capabilities → Skills → upload.
  3. Registers once, stays on across every chat — never pasted again.
- Fallback (Skills UI not rolled out): attach the file in a chat + "load this skill and use it from now on."

## Distribution page
Every tiny skill ships with a share page. Structure in `assets/distribution-page-template.md`. Non-negotiable sections: before/after demo, behavior table, 30-second install, copy-paste usage prompts, when-not-to-use, read-the-file-first safety note.

## Evals for this track
Minimum three: (1) flagship before/after prompt, (2) one behavior-table row verified live, (3) one should-NOT-trigger prompt from the "when not to use" list confirming the skill stays out of the way (or degrades honestly).
