# Batch 1 progress (Dept D Backtest Engineers) — Q-0001, Q-0003, Q-0005, Q-0006

Registration commit 93cb97a (stamped 2a4b581). Notes appended as work proceeds (UTC).

- 2026-11-06 start: read 00-common, PARAMETERS, method lessons, CONVENTIONS, CAL-D, the four prereg JSONs, Gate v2 (master prompt).
- Infrastructure findings BEFORE any data read for batch 1 (no batch-1 read in registry_reads.log yet):
  1. `qe.registry` splits the `data` field on "," but the batch-1 rows use ";" -> Q-0001/Q-0003 dataset names unparseable. Fix: split on "," or ";".
  2. `qe.gateway._read_file` treats a suffix-less path as CSV; the HistData datasets are partitioned parquet directories. Fix: read a directory with read_parquet.
  Both fixes change no rule, parameter, cost or window; tests added.
- 00:50 sha256 pins recomputed for all six batch datasets (`src/qe/qa/pins.py`, new): all match manifest and row pins.
- Q-0005/Q-0006 code: `research/q0005/dipswing.py` (rule), `research/q0005/q0005.py` (stages is/dryrun/oos), `research/q0006/q0006.py` (wrapper), shared arithmetic `research/batch1/gatekit.py`.
  IS stage done for both (harness truncation + perturbation pass on CL/CO/HO/GC; a planted two-bar look-ahead is caught). Dry run of the whole OOS pipeline on IS data (1987-89 as pretend window) runs clean. IS reads in the log under `interactive`/`<stdin>` = exploration of columns and the planted-leak check (IS only).
- 00:52 next: Q-0005 OOS read, then Q-0006 OOS read.
- 00:47 Q-0005 OOS read (one), result `research/results/Q-0005.md`: daily net1x -0.17 bp/day, t_min -0.88 (trade-level -1.37), FAIL.
- 00:47 Q-0006 OOS read (one), result `research/results/Q-0006.md`: daily net1x -0.44 bp/day, t_min -2.11 (trade-level -2.48), FAIL (wrong side of zero).
- next: Q-0003 code (AUDUSD FOMC day), then Q-0001.
- 00:58 Q-0003 IS stage: harness `exact` (registered skip-if-15:58-bar-missing) fails truncation 30/30 by construction (post-entry availability read), passes perturbation; `ex_ante` passes both. QA: daily_assets has no FX series (said so); substitute HistData AUDUSD vs daily_futures AD on IS dates: corr 0.907 at lag 0 (0.11 / 0.02 at lags -1/+1). Dry run clean. Next: Q-0003 OOS read.
- 00:53 Q-0003 OOS read (bars + calendar, one each), result `research/results/Q-0003.md`: net1x +9.74 bp/event (85 events), t_min 0.95, boot lower -28.0 bp, 2x t 0.63, FAIL. Next: Q-0001.
- 01:05 Q-0001 IS stage: as_written skip rule fails truncation 30/30 per pair by construction (post-entry availability), perturbation passes; ex_ante passes both on all three pairs; signal truncation/perturbation on daily_assets 61/61 unchanged. QA: no FX series in daily_assets (said so); HistData vs CME futures on IS dates corr EURUSD/EC 0.950, GBPUSD/BP 0.951, AUDUSD/AD 0.912 at lag 0. Dry run clean. Next: Q-0001 OOS read.
- 01:02 Q-0001 OOS read (3 pairs + daily_assets, one each), result `research/results/Q-0001.md`: net1x -7.39 bp/event (110 events, 327 pair-events), t_min -2.04, boot lower -20.9 bp, 2x t -2.85, FAIL. 2023-02..06 month-ends missing in HistData (flag to Dept C).
- All four rows done. Remaining: pytest, final summary.

## Batch 1 summary (OOS, net 1x, as registered; every verdict FAIL under the row's rule)

| row | OOS | n | net 1x mean | deciding t_min | bootstrap lower (0.05/430) | 2x-cost t | verdict |
|---|---|---|---|---|---|---|---|
| Q-0001 | 2015-03..2024-12 | 110 events / 327 pair-trades | -7.39 bp/event | -2.04 | -20.9 bp/event | -2.85 | FAIL |
| Q-0003 | 2014..2024 | 85 events | +9.74 bp/event | 0.95 | -28.0 bp/event | 0.63 | FAIL |
| Q-0005 | 1990..2007 | 263 trades | -0.17 bp/day (-3.05 bp/trade) | -1.37 (daily -0.88) | -1.01 bp/day | -1.14 | FAIL |
| Q-0006 | 1990..2007 | 82 trades | -0.44 bp/day (-24.9 bp/trade) | -2.48 (daily -2.11) | -1.27 bp/day | -2.47 | FAIL |

`python3 -m pytest -q quant-edge/tests`: 53 passed, 1 skipped (opt-in slow test). Nothing committed.
