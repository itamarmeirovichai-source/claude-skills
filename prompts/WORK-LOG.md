# Work log: quant-research master prompt

(עברית: קובץ ההמשך. אם איתמר אומר "תמשיך מאיפה שעצרת", קוראים את הקובץ הזה קודם וממשיכים מהשלב הפתוח הראשון, בלי לחזור על מה שכבר סומן כגמור.)

## Goal of this work item

Produce one "mega master prompt" that Itamar pastes into a brand-new Claude Code session. That session must run a multi-department research and engineering program (sub-agents, internet, Databento within the existing account credit only) to find a fully automated edge for funded prop-firm accounts that pays at least $20,000 a year per $100,000 funded, or prove honestly that none exists and stop. Deliver the prompt in chat and as a file in this folder; the prompt body is English (precision), with an instruction to communicate with Itamar in Hebrew.

## Decisions already taken (do not reopen)

- Prompt body in English; the agent reports to Itamar in Hebrew. Short Hebrew preamble inside the prompt.
- Databento: spend only the credit already in the account (Itamar, 3 Nov). Hard rule in the prompt: `metadata.get_cost` before every download, a spend ledger, a hard cap at about 85% of the credit, shrink requests instead of exceeding. Never let the card be charged.
- The Databento key is never written into this repo (public). It lives in the session scratchpad only (`scratchpad/secrets/databento.key`, mode 600) and should become the env var `DATABENTO_API_KEY` in the AI Trading environment. Itamar should rotate the key after that because it was pasted in chat.
- The prompt includes the keyword `ultracode` so the new session opts into heavy multi-agent orchestration.
- The prompt must carry the closed hypothesis families (280 variants, 4 waves) so the new team never re-tests them, and must point at `skills/prop-fleet/` on branch `claude/friendly-galileo-eakzlm` (PR #4) as the record of everything done so far.

## Facts established (sources in this repo)

- Research record: branch `claude/friendly-galileo-eakzlm`, `skills/prop-fleet/` (SKILL.md, agents/ORG.md, agents/board.md, agents/ledger.csv with N = 280, agents/prereg/*, references/w1-synthesis.md, references/w1-firms.md, references/w3-volrisk.md, references/w4-*.md, scripts/*, `.claude/workflows/prop-fleet-daily.js`).
- Gate used so far: pre-registration, out-of-sample, realistic costs, day-clustered bootstrap p5 > 0, one-sided Bonferroni 0.05/N (z about 3.56–3.59 at N 280–304), beta benchmark at matched exposure, verifier re-implementation, red team.
- Economics: $20k per $100k at FTMO Swing needs net Sharpe about 2.4 at 12% vol, 1.9 at 15%, 1.5 at 20% (F2 stress). Sizing tricks (CPPI, barrier-aware) make it worse. Skew does not help. The Sharpe-0 lottery dies under stress.
- Safe-list firms (11 Oct): FTMO, MyFundedFutures, Lucid, Topstep (Express Funded via API, own PC only), TradeDay. Conditional: Bulenox, The5ers, FXIFY, E8, Funding Pips, Tradeify. Out: Apex and others. Futures firms force flat by close. Only FTMO-type CFD firms allow overnight. No safe firm offers VIX.
- Databento cost check (3 Nov, see `research/databento-cost-check-2026-11-03.md`): ohlcv-1m is $70/GB; one liquid root for 2010–2026 at 1m costs about $20–21; 37 roots at 1m cost $545; 1h bars about $0.97 per root; 1d about $0.05 per root; ES one year of mbp-10 is $427, trades $154. Within $125, plan B (1m for ES, NQ, GC, CL + 1h and 1d for 37 roots) costs about $120; 1h+1d for 37 roots costs about $37.

## Research lanes (status)

Outputs are written by sub-agents to `scratchpad/research/<lane>.{json,md}` (ephemeral) and are copied into `prompts/research/` here once a lane finishes. A lane is DONE only when its file exists in `prompts/research/`.

| Lane | Where | Status |
|---|---|---|
| digest: hypotheses ledger | workflow wf_fa4cff3c-648 | running (started 03:17 UTC 3 Nov) |
| digest: firms + economics | workflow wf_fa4cff3c-648 | running |
| digest: data, infra, bot, procedures | workflow wf_fa4cff3c-648 | queued |
| web: Databento operations + data plan | background agent | running (started 03:32) |
| web: prop-firm rules Nov 2026 | background agent | running |
| lit: academic sweep | background agent | running |
| lit: practitioner + code | background agent | running |
| lit: microstructure / order flow | background agent | running |
| lit: FTMO CFD + sessions | background agent | running |
| web: statistics + backtest standards | background agent | running |
| web: prompt engineering | background agent | running |
| web: alternative data sources | background agent | running |
| web: engineering + execution | background agent | running |
| critic: completeness | not started | run after all lanes |

Note: the workflow would also run the ten web lanes after the digests (cap 2 concurrent agents on this 4-CPU box). Stop the workflow once the three digests are done to avoid duplicate work; completed workflow results are in its `journal.jsonl`.

## Steps

1. [x] Scout repo, read prop-fleet research, PR #4, user skills (skill-prompt-architect, minds).
2. [x] Databento free cost check with the user's key; results saved.
3. [ ] Research lanes finish; copy outputs into `prompts/research/`; run the completeness critic.
4. [ ] Draft the master prompt → `prompts/quant-edge-master-prompt.md`.
5. [ ] Judge panel (5–6 lenses: AI/prompt master, quant/statistician, prop-firm risk officer, systems engineer, the user's advocate, skeptic) → one focused revision.
6. [ ] Final QA against `skills/minds/references/craft.md` (no AI tells) and the skill-prompt-architect template; deliver in chat (Hebrew summary + the prompt) and push.

## Resume protocol

1. Read this file, then `git log --oneline -5` on this branch.
2. `ls prompts/research/` → whatever is there is done. For lanes not there, check the scratchpad path above; if the scratchpad is gone, re-run only the missing lanes (the lane briefs are in the session transcript; if unavailable, rebuild from the table above).
3. Continue from the first unchecked step. Never redo a checked step.
