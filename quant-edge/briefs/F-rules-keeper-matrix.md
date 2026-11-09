# Brief: Rules Keeper — Day-1 firm matrix re-fetch (output: quant-edge/economics/firms-matrix-2026-11.md)

Re-fetch each safe-list firm's rules pages, terms, FAQ and funded-stage agreement from the firm's own site today: FTMO, MyFundedFutures, Lucid (blocked
from here: 403; use the inherited clauses and any cached/third-party copy marked "snippet"), Topstep, TradeDay; conditional: Bulenox, The5ers, FXIFY, E8,
Funding Pips, Tradeify. Start from `quant-edge/economics/firm-pages-fetched-2026-11-03.md` (the letters agent's fetch list) and the inherited matrix
`~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md`, `~/quant-edge-inherited/pr4/skills/prop-fleet/references/w1-firms.md`,
`agents/daily/w1-firms/clauses-futures.md`, `clauses-fx-crypto.md`, `agents/daily/w3-volrisk/clauses-ftmo.md`.

For every firm × plan cell: automation (bots, unattended, own code, VPS/VPN, remote signal), account caps and per-plan caps, evaluation fee / reset /
activation / monthly fee, profit target, minimum days, consistency rules (evaluation and funded), drawdown type and lock (Topstep real-time trailing MLL
with +$2,000 lock and post-payout behaviour; MFFU Rapid intraday trailing from the equity high-water mark; EOD-trailing plans; FTMO 10% static max loss and
the 5% daily loss from the 00:00 CE(S)T balance incl. floating P&L), daily loss limit and its clock, news windows (the firm's own Tier-1 list and ±minutes,
resting orders), minimum holding time (Lucid 5 s, Tradeify 10 s), flat-by time and the trading-day boundary (18:00 ET reopen?), inactivity rule, payout
eligibility (winning days, buffer, consistency share, min and cap per request, frequency), closure after N payouts or Live call-up, maximum contracts and
scaling plan, restricted countries (Israel), payout rails for Israeli residents, platform/API list and fees. Label every cell verified (URL + fetch date) /
snippet / unknown; archive a dated copy of every fetched page as text under `~/quant-edge-data/firm-pages/2026-11-03/<firm>/<slug>.txt` (not in the repo)
and list them in the matrix file. Read FTMO's T&C 7.8 and 13.2.4 and the funded-stage agreement and quote them. Note every change versus the inherited matrix
in a "Changes since 2026-10-11" section. Output: `quant-edge/economics/firms-matrix-2026-11.md` (matrix + changes + the open written questions per firm)
and `quant-edge/economics/firm-clauses-2026-11/<firm>.md` (quoted clauses). No contact with any firm, no sign-up, no chat. Read first: `briefs/00-common.md`.
