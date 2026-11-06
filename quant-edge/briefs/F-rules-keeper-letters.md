# Brief: Rules Keeper — firm letters Itamar sends himself (output: quant-edge/letters/)

Role: Rules Keeper / Contract Compliance Officer, Department F. You write letters; you never send them, never contact a firm,
never sign up, never open a chat with support. Itamar sends them from his own mailbox.

Task: one ready-to-send English letter per safe-list firm, each in its own file: `ftmo.md`, `myfundedfutures.md`, `lucid.md`,
`topstep.md`, `tradeday.md`, `bulenox.md` (conditional firm, used only if the fleet needs it), plus `accountant.md` (the accountant
letter) and `README.md` in Hebrew (two paragraphs: the order to send, where to paste each letter, what to forward to the program).
Start from `~/quant-edge-inherited/pr4/skills/prop-fleet/references/verification-letters.md` (section 1 the firm letter, section 2
the accountant letter) and the clauses in `~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md` and
`~/quant-edge-inherited/pr4/skills/prop-fleet/references/w1-firms.md`. Use the firm's own product and plan names: fetch them from the
firm's site today (ToolSearch "select:WebSearch,WebFetch"; lucidtrading.com is blocked from here with 403: use the inherited clauses,
mark the product names "unverified, site blocked 2026-11-03", and say so in the Hebrew note). Record every page URL and fetch date in
a short "Sources" footer below each letter.

Every firm letter asks, in the firm's vocabulary, the three questions: (1) a fully automatic, self-built bot running unattended on N
funded accounts and taking identical trades at the same time: allowed, on which plans, with which written rule? (2) which platform,
API and hosting are permitted (own PC, VPS, cloud; remote signal source with local executor)? (3) does the same bot running at other
firms, or on several accounts here, breach any coordinated-trading, copy-trading or "one strategy" rule? Then the firm-specific
questions from the inherited open-questions list: Topstep (Express Funded call-up criteria, own-PC rule, remote signal source, copier
constraints); MyFundedFutures (unattended automation, Rapid/Pro news windows and resting orders, account caps by plan); Lucid (the
prior-written-approval clause for automated software, which plans, 5-second hold rule, payout closure after 5 payouts); TradeDay
(automation inside NinjaTrader/Tradovate/TradingView/Jigsaw/Quantower only, no API; 5 sim + 5 live cap); FTMO (bots in writing,
Swing account holds, $400k per strategy, 7.8 and 13.2.4 of the T&C, news rule on Swing vs Standard); Bulenox (definition of
"third-party algorithm" and "automated discretional trading", Funded-agreement automation terms after 3 payouts, API fee per
account or per user). Add to every letter: eligibility and payout rails for an Israeli resident (restricted-countries list, bank
wire / Deel / Rise / crypto), and a request for the answer in writing by email.

Format per file: title; "Paste into: <support email or form URL, fetched>"; the letter (≤ 350 words, polite, precise, no mention of
AI agents or this program); then two lines in Hebrew: what a usable answer must contain and what answer kills the firm for us.
Read first: `quant-edge/briefs/00-common.md`, `quant-edge/board.md`. Write each file as soon as drafted. English letters; Hebrew notes.
