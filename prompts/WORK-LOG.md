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
| digest: hypotheses ledger | workflow wf_fa4cff3c-648 | DONE → research/digest-hypotheses-ledger.{json,md} |
| digest: firms + economics | workflow (failed at the usage limit) | covered by the director's own reading of w1-firms.md, w1-prop.md, w3-volrisk.md, ORG.md, board.md; no separate file |
| digest: data, infra, bot, procedures | workflow (never started) | covered by the director's own reading of data/README.md, tjr.md, email.md, second-opinion-prompt.md, what-the-giants-do.md, prop-fleet-daily.js; no separate file |
| web: Databento operations + data plan | director, direct WebFetch of databento.com docs | DONE (billing: $125 credit, 6 months, card billed only beyond credit, portal monthly limit blocks requests; rate limits 100 req/s, 20 metadata/s; continuous symbols unadjusted, v = previous-day volume; licence per dataset) |
| web: prop-firm rules Nov 2026 | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| lit: academic sweep | background agent, resumed after the limit reset | DONE → research/lit-academic.{json,md} (36 candidates, decay evidence, 13 rules) |
| lit: practitioner + code | background agent, resumed after the limit reset | DONE → research/lit-practitioner.{json,md} (30 candidates, 19 cost facts, 15 rules; ~45 pages fetched) |
| lit: microstructure / order flow | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| lit: FTMO CFD + sessions | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| web: statistics + backtest standards | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| web: prompt engineering | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| web: alternative data sources | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| web: engineering + execution | background agent (failed at the usage limit before producing output) | DROPPED for budget; the master prompt delegates this sweep to the new session and the director writes the frame from own knowledge |
| critic: completeness | folded into the judge panel (step 5) | pending |

Note (3 Nov, 04:50 UTC): the 5-hour usage limit hit at about 03:40 UTC and killed 13 of 14 workflow agents and all 10 background agents. The workflow is finished (1 result). Budget decision: resume only the two literature agents; everything else is written by the director from the repo facts and own knowledge, and the new session is told to run the full sweeps itself.

## Pull request

Draft PR for this branch: https://github.com/itamarmeirovichai-source/claude-skills/pull/26 (opened 3 Nov 04:55 UTC, subscribed).

## Steps

1. [x] Scout repo, read prop-fleet research, PR #4, user skills (skill-prompt-architect, minds).
2. [x] Databento free cost check with the user's key; results saved.
3. [ ] Research lanes finish; copy outputs into `prompts/research/`; run the completeness critic.
4. [x] Draft v1 (3 Nov ~04:50 UTC) and v2 (3 Nov ~05:10 UTC, after judge 1 and both literature lanes) of the master prompt → `prompts/quant-edge-master-prompt.md`. v2 changes: PROGRAM_ROOT quant-edge/, MAX_CONCURRENT_AGENTS 2, DATABENTO_PLAN_CEILING_USD 94 with an $84 default plan, four end states S1/S2/P1/N1 defined once, no Director discretion over counting, checkpoint schema and resume rule, pre-mortem, trading-day boundary lane, institutional change dates, measured commissions, 2-tick screening, 0.5x publication haircut, delegated reading list, craft fixes.
5. [~] Judge panel running (workflow wf_0b4aa94c-c4f). Judge 1 (prompt engineering) returned: 80/100, one focused revision; its five must-fixes are accepted (Databento plan above cap → add DATABENTO_PLAN_CEILING_USD and a $84 default plan; unify end states S1/S2/P1/N1; PROGRAM_ROOT = quant-edge/ with a checkpoint schema so the program never follows prompts/WORK-LOG.md; count column fixed at pre-registration, no Director discretion; MAX_CONCURRENT_AGENTS = 2, departments are roles, sequential runs). Also fold in from the two literature lanes: the 18:00 ET trading-day boundary (overnight-session holds allowed at futures firms), institutional change dates for OOS splits, the 0.5x publication haircut, measured commissions, the 2-ticks-per-trade screening rule. Judge 2 (prop-firm risk officer) returned 78/100: all five must-fixes applied in v3 (Economist inputs per firm and plan from w1-prop prop_model.py; Gate v2 criterion 11 measures the firm's own loss rule on the intraday equity path; flat-by enforcer, trailing-drawdown distance guard, same-direction check; S2 requires netting inside accounts; written answers from every firm, MFFU unattended question). Judge 3 (statistician) returned 78/100: all four must-fixes and four should-fixes applied in v4 (one count = one OOS read of a decision unit; sign fixed in the row; 8-year OOS default with a locked 2025+ hold-out; bar printed in Sharpe units with the gate's power; DSR/CSCV reported not gated; bootstrap at the 0.05/N quantile with 50/alpha draws; stability definitions made computable; costs per side, regular hours, swaps long and short; combination rule evaluated on the hold-out or forward data; economics at the point estimate and the 90% lower bound; F2-12 re-run). Waiting for judges 4–6 (systems engineering, client advocate, skeptic), then the final pass.
6. [ ] Final QA against `skills/minds/references/craft.md` (no AI tells) and the skill-prompt-architect template; deliver in chat (Hebrew summary + the prompt) and push.

## Resume protocol

1. Read this file, then `git log --oneline -5` on this branch.
2. `ls prompts/research/` → whatever is there is done. For lanes not there, check the scratchpad path above; if the scratchpad is gone, re-run only the missing lanes (the lane briefs are in the session transcript; if unavailable, rebuild from the table above).
3. Continue from the first unchecked step. Never redo a checked step.
