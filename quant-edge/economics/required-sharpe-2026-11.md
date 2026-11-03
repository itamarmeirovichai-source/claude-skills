# Required net Sharpe for $20k / $30k per slot-year — F2-12 re-run (2026-11-03)

Status: **in progress** (written early, extended as the run proceeds). Economist, Department F.
This is an economics-model re-run: it reads no market data and adds nothing to N (N stays 280 inherited + 0 program).

## 0. Scope and provenance

- Brief: `quant-edge/briefs/F-economist-f2-12.md` (after `quant-edge/briefs/00-common.md`).
- Inherited model (read-only worktree, commit e0f5e59 of `claude/friendly-galileo-eakzlm`):
  `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w3-volrisk/` (`stress_model.py`, `scenarios.py`, `run_f2.py`,
  `make_report.py`, `test_stress_model.py`, logs `run_f2.log`, `run_f2_full.log`, `tables.md`, `redteam-model.md`), which imports
  the D1 model `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-prop/` (`prop_model.py`, `firms.py`).
- Registered specifications: `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/prereg/F2.csv` rows F2-09, F2-12, F2-13, F2-14, F2-15
  (also rows 84–98 of `quant-edge/registry.csv`). Synthesis: `~/quant-edge-inherited/pr4/skills/prop-fleet/references/w3-volrisk.md`.
- Scratch copy used for every run (the worktree was never edited):
  `/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad/f2_rerun/`.
- Code and logs delivered under `quant-edge/economics/f2_rerun/` (no data files, nothing over 1 MB).

## 1. Summary (filled at the end)

_pending_

## 2. What the inherited record says (labelled "inherited")

- `w3-volrisk.md` verdict (from F2-09, ALL stresses, FTMO Swing 100K two-step, pre-tax net $/slot-year, renewal reward):
  net Sharpe ≈ 2.4 at 12% annual vol, ≈ 1.9 at 15%, ≈ 1.5 at 20% for $20k per slot-year.
- `tables.md` "Sharpe needed for $20k per slot-year (pre-tax)", FTMO: F2-01 (D1 baseline) 2.42 / 1.88 / 1.42 / 0.96 / 0.69 and
  F2-09 (ALL combined) 2.42 / 1.92 / 1.46 / 0.94 / 0.69 at caps 12 / 15 / 20 / 30 / 40%.
- F2-12 (the row that "REPLACES F2-09 as the decision row") and F2-13 were run (`run_f2_full.log` lists all 45 + 45 jobs done), but
  their numbers were **never written into the record**: `make_report.py` tabulates only F2-01 and F2-09, and `results.json` is
  git-ignored in that folder. So there is no inherited F2-12 figure to put beside the re-run; the inherited column below is F2-09
  (and F2-01 for reference). _(Search of the inherited trees for written F2-12 numbers: see §2.1, pending.)_

## 3. Tests run first

_pending_

## 4. Runtime budget

_pending_ (`run_f2.log` has no timings; one job was timed in the scratch copy, see `logs/time_job.log`).

## 5. Re-run F2-12 and F2-13, FTMO Swing 100K two-step, caps 12 / 15 / 20%, S in {1.0, 1.5, 2.0, 2.4, 3.0}

_pending_

## 6. Required net Sharpe table ("re-run 2026-11-03" beside "inherited")

_pending_

## 7. Calendar chain: p10 / p90 per slot-year, time to first payout, accounts burned

_pending_

## 8. Futures-firm frame, first pass (D1 `prop_model.py`, all firm parameters "inherited (fetched 2026-10-11)")

_pending_

## 9. Tax note: business income vs capital gains (±≈ one third on the required edge)

_pending_

## 10. What the Rules Keeper must refresh before any intraday variant is registered

_pending_

## 11. Failures, limits and honest caveats

_pending_

## 12. Files, commands, seeds, run times

_pending_
