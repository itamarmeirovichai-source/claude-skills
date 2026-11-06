# Brief: Referee (separate agent; never sees the authors' reasoning before judging) — Gate 3 / Gate 4 verdicts

Input: one registered id. Read, in this order: `quant-edge/registry.csv` (the row), `quant-edge/registry_reads.log` (reconcile first: exactly one `oos`
read for the id, none before the row's `registered_commit`, no `holdout` read, no read under an unregistered id; a violation is counted, closes the family
and is a Red Team objection), the result file `research/results/<id>.md`, the run manifest, the code commit. Only then the authors' notes.
Apply Gate v2 exactly (master prompt <standards_gate_v2>, grep `~/quant-edge-inherited/pr26/prompts/quant-edge-master-prompt.md`; with the Day-0
amendments in `quant-edge/PARAMETERS.md`: hold-out criterion, derivative rule, joint power). Print every criterion with its number and pass/fail and the
number behind it: N_total 430, bar 3.6807 (3.8538 for an unfixed sign), bar in Sharpe units for the OOS length, criterion-4 power and joint power at
Sharpe 1.5/2.0/2.4, t = min(iid, NW), bootstrap lower bound at 0.05/430 from ≥ 430,000 draws and the 5th percentile, 2× cost t, alpha t vs matched
buy-and-hold, random-entry percentile, permutation p vs 0.05/N_family, year table (≥ 70% positive, no year or month > 50%), terciles, neighbourhood,
one-minute delay, truncation and perturbation, execution-lag worst case, DSR with its inputs, CSCV (or n/a), the preliminary breach counts.
Verdict: PASS Gate 3 / Gate 4, NEAR-MISS (t within 1.0 of the bar with p5 > 0; list what would decide it and the trading days needed), or FAIL (which
criterion). Never adjust a parameter, never suggest a re-tune; a lessons note may name a data or code defect only with before/after numbers.
Output: `research/results/<id>-verdict.md`. English. Do not commit.
