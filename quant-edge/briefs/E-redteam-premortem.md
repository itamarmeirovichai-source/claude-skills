# Brief: Red Team — Day-0 pre-mortem (output: quant-edge/daily/2026-11-03/redteam-premortem.md)

Role: Red Team of the Statistics department. Default verdict is "refuted". You attack the program plan itself.

Task: write a one-page pre-mortem (≤ 900 words plus one table). Premise: it is 19 December 2026 and the program failed
(verdict N1 that was avoidable, or a false S1/S2, or P1 by drift, or a process breach that voided the answer). Write how it
happened, as a post-mortem would. Rank 8–12 failure modes by probability × damage. For each: the mechanism, the earliest observable
warning sign, the one fact or measurement that would flip it, and the cheapest mitigation. Separate "statistical" (bar, power, leaks,
multiple testing, hold-out misuse), "data" (licence holds, Databento credit expiry, clock/roll errors, Alpaca keys never arriving),
"economics" (decay haircut, swaps, consistency rules, Topstep trailing MLL, payout denials), "process" (agent deaths, unregistered OOS
reads, budget of 150 variants spent on low candidates, deadline), and "client" (Day-0 items never confirmed, letters never sent).

Read first: `quant-edge/briefs/00-common.md`, `quant-edge/WORK-LOG.md`, `quant-edge/board.md`, `quant-edge/PARAMETERS.md`.
Then grep (never load whole): `~/quant-edge-inherited/pr26/prompts/quant-edge-master-prompt.md` (sections <mission>, <process_and_gates>,
<standards_gate_v2>, <resources_and_budget>), `~/quant-edge-inherited/pr26/prompts/research/digest-hypotheses-ledger.md` (sections
gaps_or_inconsistencies and prompt_rules), `~/quant-edge-inherited/pr4/skills/prop-fleet/references/second-opinion-audit.md`,
`~/quant-edge-inherited/pr4/skills/prop-fleet/references/w1-synthesis.md`, `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w3-volrisk/redteam-model.md`.

Output format: title, one-paragraph narrative, the ranked table (mode | P | damage | warning sign | flipping fact | mitigation), then
"Three things the Director must change in the plan this week" and "Accepted risks I would sign". End with the files you read.
Write the file early and extend it. No numbers from memory presented as measured; cite the file or say "estimate".
