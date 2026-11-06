# Brief: Economist — F2-12 re-run and refreshed required-Sharpe table (output: quant-edge/economics/required-sharpe-2026-11.md)

Role: Economist, Department F. This is an economics model re-run: it reads no market data and adds nothing to N.

Task:
1. Copy the inherited stress model to a scratch directory (never edit the worktree): `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w3-volrisk/`
   (`stress_model.py`, `scenarios.py`, `run_f2.py`, `make_report.py`, `test_stress_model.py`; logs `run_f2.log`, `run_f2_full.log`; `tables.md`, `redteam-model.md`).
   Read the registered specifications of F2-09, F2-12, F2-13, F2-14, F2-15 in `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/prereg/F2.csv` and
   the synthesis `~/quant-edge-inherited/pr4/skills/prop-fleet/references/w3-volrisk.md`. Run the tests first.
2. Re-run F2-12 (and F2-13 as the alternative book; the better of the two per cell is the verdict, as F2-13 says) for FTMO Swing 100K two-step at
   annual volatility 12%, 15% and 20%, at net Sharpe S in {1.0, 1.5, 2.0, 2.4, 3.0}. Report net $/slot-year to Itamar (after split, fees, resets,
   failed accounts), p10/p90, evaluation pass probability, time to first payout, accounts burned per year, and the Monte Carlo s.e. (F2-15's seeds).
   Solve for the Sharpe that reaches $20,000 and $30,000 per slot-year at each volatility. Check `run_f2.log` for runtime first and shrink paths or
   S-grid before exceeding ~60 minutes of CPU; report the s.e. you achieved.
3. Futures-firm frame, first pass only: run `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-prop/prop_model.py` (with `firms.py`, `rules.csv`,
   `test_prop_model.py`, `tables.md`) for the inherited plans and state the R/trade × trades/day pairs that reach 20% of nominal. Label every firm
   parameter "inherited (fetched 2026-10-11)". Note which inputs the Rules Keeper must refresh (Topstep real-time trailing MLL with +$2,000 lock,
   MFFU Rapid intraday trailing, EOD-trailing plans, payout caps) before any intraday variant is registered.
4. Write the report: every number with the script path, command, seeds and run time; a "required net Sharpe" table (12/15/20% vol × $20k/$30k) labelled
   "re-run 2026-11-03" beside the inherited F2-09 figures labelled "inherited"; both tax readings (business income vs capital gains) as a note on the
   required edge (±≈ one third). Put the copied code and logs under `quant-edge/economics/f2_rerun/` (no data files, nothing over 1 MB).
Read first: `quant-edge/briefs/00-common.md`, `quant-edge/WORK-LOG.md`, `quant-edge/board.md`. Write the output file early and extend it.
