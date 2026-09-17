---
name: live-results
description: Report still-accumulating numbers (forward test, A/B test, campaign) with the base rate that says whether they mean anything. Use when asked how a live run is doing; not for backtests or build status.
---

# Live Results

A status update on something still running. The reader gets two things: where it stands right now, and whether that number has earned any conclusion yet. One screenful, no spin, no cheerleading, no burying the loss.

The hard part isn't the number. It's the last line — the one that tells the reader how much to care.

## The shape

Six moves, in order. Drop any that has no content. Never reorder.

1. **Headline in two units.** The measure plus what it means in the reader's real terms. `−2.15% after 14 days counted` is abstract alone; `−2.15% after 14 days counted, so −$2,154 on a $100K account` lands. Percent for comparison, money (or hours, or users) for weight.
2. **Say whether it moved.** "No change since the last check" is information — it tells the reader nothing needs their attention. Re-reporting yesterday's figure as if it were news wastes them.
3. **Three anchors, not one.** Latest period, best, worst. The spread is what lets someone judge the headline; a single number hides whether −2.15% came from one bad day or fourteen mediocre ones.
4. **Name what's missing, when it lands, why.** "Sept 10 is still waiting on Asian prices. The bot computes it tonight at 18:30, about 45 minutes out." Exact reason, exact time, exact wait. Never present a partial count as if it were complete — say how many periods are actually in the number.
5. **The base rate.** Whether the sample is big enough to mean anything, backed by a frequency: *"After 14 days this is still noise. Even when the strategy performs exactly like the backtest, roughly 1 window in 12 looks like this."* Not "it's normal." Not "too early to tell." A quantity the reader can check.
6. **No action item when there's no action.** If the honest read is that the number hasn't earned a decision, stop at move 5. Inventing a next step ("consider tightening the stop") from noise is the most expensive thing this format prevents.

## Getting the base rate right

This is the move that separates an honest update from a reassuring one, and it's the one you can fake without noticing. Rules:

- **Derive it, don't feel it.** Take the distribution you already have — backtested daily returns, last quarter's campaign variance, the historical spread — and count how often a window *of this length* lands at or past *this level*. That fraction is the line. Show the method in one clause if the reader might want to check it.
- **State it as a frequency, not a p-value.** "1 window in 12" beats "8.3%" beats "not statistically significant." People reason about counts.
- **No distribution, no frequency.** If you don't have one, say exactly that in the same breath: "I don't have a spread to compare against yet, so 14 days tells us nothing either way." Never invent a number to sound rigorous — a fabricated base rate is worse than none, because it reads as measured.
- **It cuts both ways.** Apply the same line to a good result. A +6% run that a third of random windows beat is noise too, and saying so is the whole point of having the format.
- **Say when it stops being noise.** One clause: "ask again at 60 days" or "this separates from noise around 200 trades." Gives the reader a date instead of a vibe.

## Voice

Bottom line first. Short sentences, varied length. Write in the reader's language — the specimen is Hebrew because that's who it was for.

- Exact signed figures: −0.69%, +1.08%. A number without its sign is a lie of omission.
- Bad news in the same register as good news. No softening clause in front of the loss, no exclamation behind the win.
- No bold, no emoji bullets, no headers on a five-line update. Plain sentences and, at most, a short list.
- The last line is the base rate. Never close with an offer to help, a question, or "let me know."
- Don't explain what the reader already lives with. They know what the bot is.

## When not to use this

- **The sample is conclusive.** Then report the conclusion. Base-rate framing on settled evidence is just hedging.
- **A backtest, post-mortem, or historical study.** That's analysis, not a live count — different shape, different obligations.
- **Build, CI, or deploy status.** Report what broke and what's next.
- **The user asked for a decision, not a status.** Then decide, and use the numbers as the argument.

## Reference

Read `references/specimen.md` for the gold-standard example with its moves annotated, a same-prompt before/after against an ordinary status update, and worked variants for an A/B test, an ad campaign, and the case where no base rate exists.
