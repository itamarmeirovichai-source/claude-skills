# f2_rerun — code and logs of the F2-12 / F2-13 re-run (Economist, Department F, 2026-11-03)

Report: `quant-edge/economics/required-sharpe-2026-11.md`. Brief: `quant-edge/briefs/F-economist-f2-12.md`.
Everything here was run in the scratch copy
`/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad/f2_rerun/` and copied here unchanged.
No market data was read or stored; the JSON files are Monte Carlo model outputs. No file is over 1 MB.

## Layout

| path | what | origin |
|---|---|---|
| `w3-volrisk/stress_model.py`, `scenarios.py`, `run_f2.py`, `make_report.py`, `test_stress_model.py` | the inherited F2 stress model, **verbatim** | `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w3-volrisk/`, commit e0f5e59 (`claude/friendly-galileo-eakzlm`) |
| `w1-prop/prop_model.py`, `firms.py`, `test_prop_model.py`, `run_d1.py`, `make_tables.py` | the inherited D1 model that `stress_model.py` imports, **verbatim** (firm parameters fetched 2026-10-11) | `.../agents/daily/w1-prop/`, same commit |
| `SHA256SUMS` | hashes of the copies; they equal the worktree files (checked 2026-11-03) | this run |
| `time_job.py` | timing of one F2-12 job (sizing the CPU budget) | this run |
| `run_f2_rerun.py` | the re-run driver: grid jobs (eval + funded simulation on the sigma grid, capped optimum, diagnostics) and the calendar-chain stage | this run |
| `futures_frame.py`, `futures_frame_1tpd.py` | futures-firm first pass: trade-level frame (Apex-era plans) and daily Sharpe/vol frame (five futures programs) | this run |
| `make_rerun_tables.py` → `tables_rerun.md` | every table in the report | this run |
| `results_rerun.json`, `futures_frame.json`, `futures_frame_1tpd.json` | raw outputs (per job: parameters, seeds, wall and CPU seconds) | this run |
| `logs/pytest_w3.log`, `logs/pytest_w1.log` | 21 + 14 tests passed before any run | this run |
| `logs/time_job.log`, `logs/run_rerun.log`, `logs/futures_frame.log`, `logs/futures_frame_1tpd.log` | run logs with timestamps and per-job CPU | this run |

Not copied (read from the worktree): `rules.csv`, `rules/*.csv`, the inherited logs, `tables.md`, `redteam-model.md`, `clauses-*.md`.
Decision D-003 says inherited material is read from the worktrees and not copied into this branch; the brief for this run asked for the
copied code to be placed here. The ten inherited `.py` files are included so the run is reproducible from this folder alone; the
Director may drop them and keep `SHA256SUMS`, since the commands below also run from the worktree copy.

## Commands, in the order run (all from the scratch folder; Python 3.13.18, numpy 2.5.3)

```
cd w3-volrisk && python3 -m pytest -q test_stress_model.py        # 21 passed in 8.39 s
cd w1-prop  && python3 -m pytest -q test_prop_model.py            # 14 passed in 0.25 s
python3 time_job.py                                                # 41 s CPU per job on sigma <= 20%, 53 s on the full grid
python3 run_f2_rerun.py --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 --seeds 11 101 202 303 404 \
        --n 3000 --sigmax 0.20 --procs 4 --out results_rerun.json  # 50 jobs, 35.5 CPU-min, 11.7 min wall
python3 run_f2_rerun.py --scen F2-12 F2-13 --S 3.5 4.0 --seeds 11 --n 3000 --sigmax 0.20 --procs 4 --out results_rerun.json
                                                                   # 4 jobs, 2.9 CPU-min
python3 run_f2_rerun.py --scen F2-09 --S 1.0 --seeds 11 --n 3000 --sigmax 0.40 --caps 0.12 0.15 0.20 0.30 0.40 \
        --procs 1 --out results_rerun.json                         # replication of the inherited F2-09 row, 1.8 CPU-min
python3 run_f2_rerun.py --seq --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 3.5 4.0 --procs 4 --out results_rerun.json
                                                                   # 42 calendar-chain jobs, 2.5 CPU-min
python3 futures_frame.py                                           # 9.8 CPU-min
python3 futures_frame_1tpd.py                                      # 3.3 CPU-min
python3 make_rerun_tables.py > /dev/null                           # writes tables_rerun.md
```

Seeds: grid jobs eval 11 / funded 12 (F2's base pair) and F2-15's pairs 101/102, 202/203, 303/304, 404/405; calendar chains seed 21
(eval 21, funded 22, chain 23, as inherited); futures frame A seed 11, frame B seeds 11/12 (D1 defaults).
Total CPU of everything that ran, tests and timing included: about 57.6 minutes.
