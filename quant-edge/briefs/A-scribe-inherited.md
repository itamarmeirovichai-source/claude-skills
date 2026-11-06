# Brief: Scribe — one-page briefs of the inherited record (output: quant-edge/briefs/inherited-*.md)

Role: Scribe, Program Office. Department heads and scouts will read your briefs instead of the 14 MB inherited tree.

Task: read the files listed under `files_to_read_first` in `~/quant-edge-inherited/pr26/prompts/research/digest-hypotheses-ledger.md`
(replace the old scratchpad prefix with `~/quant-edge-inherited/pr4/skills/prop-fleet/`), plus `data/README.md`, `.claude/workflows/prop-fleet-daily.js`
(at `~/quant-edge-inherited/pr4/.claude/workflows/`), `scripts/gate.py`, `scripts/futures_bars.py`, `scripts/integrity.py`, and the pre-sweeps
`~/quant-edge-inherited/pr26/prompts/research/lit-academic.md` and `lit-practitioner.md`. Never load a file over 100 KB whole; grep it
(ledger.csv, SKILL.md and the w1-prop rules files are large).

Write seven briefs, each ≤ 600 words, English, every claim with its file path (and line or section):
1. `inherited-closed-families.md`: one row per closed family: ids, markets, period, best gross and net result with its unit, why it died, what a new row would need.
2. `inherited-method-lessons.md`: the clock/DST, roll, look-ahead, bar-stamping, bootstrap, vol-scaling, benchmark and licence lessons as a checklist
   (source: digest prompt_rules + the audits and wave files).
3. `inherited-data-in-hand.md`: every dataset the previous program pinned (path, period, resolution, sha256 if recorded, licence status, known gaps, clock).
4. `inherited-firms.md`: the firm matrix as of 2026-10-11 (safe list, conditional, out; the key clauses; the open written questions), citing
   `~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md` and `references/w1-firms.md`, `references/verification-letters.md`.
5. `inherited-economics.md`: F2-09 vs F2-12 required-Sharpe figures, the lottery value, the futures-firm R/trade × trades/day frame, the tax note.
6. `inherited-code-reusable.md`: which scripts, loaders, gate functions, tests and the daily workflow are reusable, with their interfaces and caveats
   (e.g. ledger_gate.py vs finalize.py N disagreement; gate.py bootstrap_ci must not be used for rule 3).
7. `inherited-open-directions.md`: every direction the previous org flagged as untested or pre-registered-but-unrun (prereg_orb30, 02:00–03:00 ET window,
   futures-curve carry, hard-DD trend overlay, bond sleeve, funding carry per 8h, US-only mean reversion post-2026, hypotheses.py Z01–Z05), each with what it needs.
Read first: `quant-edge/briefs/00-common.md`, `quant-edge/WORK-LOG.md`. Write each file as soon as it is drafted; extend later.
