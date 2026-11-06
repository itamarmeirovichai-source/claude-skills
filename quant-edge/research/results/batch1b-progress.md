# Batch 1b progress (Dept D Backtest Engineers) — Q-0007, Q-0008, Q-0009

Registration commit 0a46ddd (stamped eb0270a). Notes appended as work proceeds (UTC). Same procedure, standards and output format as batch 1 (`batch1-progress.md`, `Q-0001.md`).

- 2026-11-06 start: read the three prereg JSONs, batch1-progress, Q-0001.md, research/batch1 + q0001/q0005 code, 00-common, PARAMETERS, WORK-LOG D-008..D-020, engine CONVENTIONS, data/qa for SPX/NSX/JPX/UKX/FRX/GRX/ETX/HKX. Before any read: `registry_reads.log` holds no line for Q-0007/8/9.
- Plan: per row, code under research/q000N/ (new files only; shared gate arithmetic re-used read-only from research/batch1/gatekit.py), IS stage (harness truncation + perturbation, IS info), dry run on IS, then exactly one OOS read per dataset. Q-0009: Stage 1 (IS, A's bootstrap p5) decides whether any OOS is read.
- 02:38 structure-only IS read of SPXUSD for Q-0009 (columns/dtypes; `<stdin>` line in the log).
- 02:41 Q-0009 IS stage (`research/q0009/q0009.py --stage is`): harness truncation + perturbation pass for A/B/C (30/30 days each); a planted look-ahead fails both (17/30, 12/30 violations). STAGE 1 at the written 0.6 pt: A n 1951, gross -0.017 R, net -0.120 R, bootstrap p5 -0.167 R (<= 0); B net -0.135 R (p5 -0.176); C net -0.177 R (p5 -0.248). **Stage 1 FAILED -> Q-0009 refuted in-sample; NO OOS read for Q-0009 (A, B, C); family orb-30min closed.** Result `research/results/Q-0009.md`.
- next: Q-0008 (HK50 AHT fade) code + IS stage, then Q-0007.
- 02:44 Q-0008 IS stage (`research/q0008/q0008.py --stage is`): harness truncation + perturbation pass (30/30); planted look-ahead fails both (14/30, 16/30). IS info: 888 sessions, 116 trades, net 1x -12.6 bp/trade, t -1.78 (information only; only the |m| tercile bounds 0.823%/1.087% are taken from IS). Gate-2 precondition on IS (information): first bar 09:15 in 99.1% of sessions; gap visible only 9% because the outcome-free bar profile shows HKEX's OLD schedule until 2016-07-22 (day close 16:15, AHT open 17:00); 2016-07-25..11-11 share visible 0.987. The precondition is decided on the OOS sessions as registered.
- 02:46 Q-0008 dry run on IS (2015-01..2016-11 as the pretend window) clean. Next: the single Q-0008 OOS read.
- 02:47 Q-0008 OOS read (one, 02:46:53; precondition on OOS passed 0.997 / 0.998), result `research/results/Q-0008.md`: 431 trades, net1x +3.64 bp/trade, t_min 1.09, boot lower -8.27 bp/trade (p5 -1.83), 2x t 0.05, criterion 7 failed (max year share 0.52) -> FAIL. Gross t 2.14 disclosed (not an edge).
- next: Q-0007 (seven index CFDs, cross-index overnight reversal).
- 02:52 Q-0007 IS stage (`research/q0007/q0007.py --stage is`): joint harness on all seven instruments at the 09:32 entry instant: as_written fails truncation 30/30 by construction (the registered 300-of-384 coverage test reads post-entry bar availability), passes perturbation 30/30; ex_ante passes both; planted look-ahead (signal at 15:55 of d) fails both (30/30, 29/30). IS info: 1017 trading days, 936 traded, net 1x -4.47 bp/day, t -3.58 (information only; only SPX vol tercile bounds taken from IS). Structure: JPX and ETX pass the 300-of-384 coverage test on only ~30-35% of IS days (sparse US-hours quotes), so the traded universe is mostly 5.
- 02:53 Q-0007 dry run on IS (2013-01..2014-12 as the pretend window) clean. Next: the Q-0007 OOS read (seven datasets, one each).
- 02:55 Q-0007 OOS read (seven datasets, one each, 02:53:50-02:54:01), result `research/results/Q-0007.md`: 2321 traded days, gross +0.01 bp/day, net1x -4.52 bp/day, t_min -4.81, boot lower -7.96 bp/day (min of day-cluster, iid-day, stationary-20), 2x t -9.61, criterion 7 failed (0 of 10 years positive) -> FAIL.
- All three rows done. Remaining: pytest, final summary.

## Batch 1b summary (as registered; every verdict under the row's own rule)

| row | OOS | n | net 1x mean | deciding t_min | bootstrap lower (0.05/430) | 2x-cost t | verdict |
|---|---|---|---|---|---|---|---|
| Q-0007 | 2015-01-02..2024-12-31 | 2321 days / 4642 legs | -4.52 bp/day (gross +0.01) | -4.81 | -7.96 bp/day | -9.61 | FAIL |
| Q-0008 | 2016-11-14..2024-12-31 | 431 trades | +3.64 bp/trade (gross +7.11, t 2.14) | 1.09 | -8.27 bp/trade (p5 -1.83) | 0.05 | FAIL |
| Q-0009 | not read | IS: A 1951 trades | IS A net -0.120 R (p5 -0.167 R) | n/a | n/a | n/a | FAIL (refuted in-sample; NO OOS read; family orb-30min closed) |

`python3 -m pytest -q quant-edge/tests`: 61 passed, 1 skipped (opt-in slow test). Nothing committed. Hold-out not read.
