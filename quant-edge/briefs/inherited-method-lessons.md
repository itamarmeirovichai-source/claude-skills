# Inherited method lessons: the checklist (Scribe, 2026-11-03)

`PF` = `~/quant-edge-inherited/pr4/skills/prop-fleet/`; `PR26` = `~/quant-edge-inherited/pr26/prompts/research/`. Sources: `PR26/digest-hypotheses-ledger.md` (prompt_rules, METHOD LESSON facts), `PF/agents/board.md` (5 Oct), the statistician audits, the wave files and the department red teams. Tick every line before a result is read.

## Clock and DST
- [ ] Label every bar by its OPEN time (09:30 bar = 09:30:00–09:30:59) (`PF/agents/daily/2026-10-06-0247/data_hunter/loader_spec.txt` OUTPUT FRAME).
- [ ] HistData 1m files (SPXUSD, GRXEUR, ETXEUR, JPXJPY) are New York local time WITH DST, not the fixed EST the vendor documents; shift 0 in US winter, -60 min in US summer against UTC Oanda (`PF/agents/daily/w1-breadth/clock_xcorr.txt`; `PF/references/w1-breadth.md` "Data checks"). Oanda v20 is UTC, Databento ts_event is UTC, FirstRate is NY-naive, Polygon is epoch-ms UTC, IBKR/mario carry NY offsets (loader_spec INPUT RULES 1).
- [ ] Verify any new file with an outcome-free diagnostic: mean |1m return| by minute around known opens, winter vs summer; DST test 2020-03-09 and 2020-11-02 09:30 NY → 13:30Z / 14:30Z (loader_spec TESTS; `.../statistician/clock_check.py` output in `audit_run.txt`).
- [ ] Use the CME equity-index calendar for ES/NQ and drop CME-only sessions (FirstRate has 44); NYSE half-days have 210 RTH bars (loader_spec rules 2, OUTPUT FRAME). Sessions are trading sessions, not calendar days; SPXUSD reopens 18:00 NY in both seasons (`audit_run.txt`).
- [ ] FOMC statement minute in SPXUSD is unconfirmed before 2013-03-20; drop those days (`PF/agents/prereg/E2_rules.md` §1; `w2-events/clock_check.txt`).

## Rolls
- [ ] Databento `.c.0` (calendar roll) has no RTH bars on quarterly expiry Fridays (30 days 2019–2026) and sits in the illiquid expiring contract for ~6 sessions (RTH volume 0.09–0.32× prior-month median; prices 2–75 pt off FirstRate/hindsight) (`.../data_hunter/xcheck.txt`, `eric_profile.txt`). Prefer explicit contracts or volume-rolled series (`X.v.0`, `PR26/databento-cost-check-2026-11-03.md`).
- [ ] Decide in the prereg: drop roll weeks (Mon–Fri of the third-Friday week plus the following Monday; `PF/agents/daily/orb-H0020/loaders.py` `roll_excluded`) or splice; never change after results (loader_spec rule 4). Roll weeks averaged -10.7 bp in F1 (`w3-ensemble/redteam/findings.md`).
- [ ] FirstRate ES rolls 1–3 days before Databento; the two match on 1,191 of 1,257 days outside roll weeks (`2026-10-05/data_hunter/second_sources.txt`).

## Look-ahead
- [ ] No eligibility rule may read the trade day's own bar count, its 15:59 bar or any post-entry bar; IBS was flattered by 0.22R (`2026-10-05/statistician/audit.txt` §4; H0012 line 18 → H0017 companion, `PF/agents/board.md` "Look-ahead pattern").
- [ ] Run the future-truncation harness (delete every bar after the entry minute; nothing about day d may change) before reading any number (`2026-10-06-0247/statistician/test_future_truncation.py`; D4 G5 in `PF/agents/prereg/D4-spec.md` §7; D3 54 cuts, E1 20/20).
- [ ] Truncation and perturbation tests cannot catch loader errors: hand-check rate lags, quote directions, cross construction, swap on gross notional, cost timing (`PF/references/w1-fxtrend.md` §7 D).
- [ ] Vol scalers and sizing use past data only; the first giants stack used full-sample vol and understated drawdown by a third (`PF/references/what-the-giants-do.md` §3; `PF/scripts/test_stack_backtest.py`). D2's scaler saw 16:00 index closes against noon FX (`w1-fxtrend.md` §7).
- [ ] GEX/DIX is published ≈17:52 ET; usable only for the next day (`dix_pubtime.txt`).

## Bar stamping and execution (bot replay traps, `PF/SKILL.md` "Replaying the valid setups")
- [ ] A 15:58 cutoff still admits the 15:55 5m bar; the last usable bar starts 15:50.
- [ ] A target counts only when the bar CLOSES beyond it; a bar touching stop and target is the stop (print the other convention too); gaps through level and stop are shown at -1R; risk = planned level-to-stop distance, not the fill.
- [ ] `.values` on a tz-aware pandas series silently converts to UTC; `resample('ME')` mislabels weekend month-ends; evening-session resting limits fill where the setup means nothing; trailing stops are evaluated at the bot's scan interval, not bar extremes.
- [ ] Entries at the next bar's open after the signal bar; measure decay with 1- and 5-minute delays (`PR26/lit-practitioner.md` prompt rule 9).

## Bootstrap and statistics
- [ ] Cluster by trading day with a cluster-robust SE around the trade mean, not the mean of daily means (SKILL.md "The gate").
- [ ] A one-sided 0.05/N quantile needs ≥ 50/alpha draws (430,000 at N = 430); 5,000 draws leave ~1.4 draws in the tail (`2026-10-05/eng_head/ledger_gate.py`; `audit.txt` §2). Never use `gate.py bootstrap_ci` or `tjr_backtest.boot_mean` for rule 3 (`PF/agents/board.md` "Gate rule 3 in code").
- [ ] t = min(iid t, Newey–West lag-10 t); p5 = min(10,000 iid, 10,000 block-20, seed 0) for daily series (`PF/agents/prereg/D2_rules.md` §6, `D3.csv` D3-00).
- [ ] Horizons in days-with-a-trade (~14 per month), not 21 trading days; the gate's one-sided bound needs ~3× the sample of a two-sided 95% bound (`2026-10-06-0247/statistician/audit_run.txt` horizon_at_gate).
- [ ] Headline chosen by in-sample Sharpe before any OOS read; worse of lag-1/lag-2, close/next-open, as-written/ex-ante decides; nothing passes "on 1× cost only" (digest prompt_rules; `w1-fxtrend.md` §2).
- [ ] A max-minus-min across groups is a selection (`PF/scripts/test_dashboard.py` null test requires zero survivors over four seeds); post-hoc slices (US-only G2, crypto weekends, TJR wide stops) are information, never findings.
- [ ] A bug fix after results needs before/after numbers in the report (`D4-spec.md` §8; D2 run moved D2-06 → D2-08, `w1-fxtrend.md`).

## Vol scaling, benchmark and prop fit
- [ ] Compare every long-biased result with buy-and-hold of the same basket at the same exposure (G2 alpha t negative vs Sharpe 0.72; crypto TSMOM = BTC; TOM vs 0.76) and remove the 20 best days (wave 4 rule, `PF/agents/wave-2026-10-11.md`).
- [ ] Scale to the vol the target needs and count 5% daily-loss and 10% max-loss breaches over rolling windows (F1 -6.74%; G2 19/35 days; crypto 37–56% of 1-year windows, `w1-crypto.md`).
- [ ] Negative skew and barrier/CPPI sizing do not lower the Sharpe needed (`PF/references/w1-synthesis.md` 12 and 16 Oct).

## Licence and provenance
- [ ] FirstRate and Databento third-party copies are a licence hold: cross-checks only, never a gated result, until Itamar rules (`PF/agents/board.md` Decision 8); F1-01 nonetheless used a pinned NQ.c.0 5m splice (digest gaps).
- [ ] Pin every file by sha256 in the loader and refuse on mismatch; never commit files > 1 MB; keep data in scratch (`orb-H0020/loaders.py`; wave rules).
- [ ] Never mix dividend-adjusted and raw files (Ascensao SPY is back-adjusted, ratio 0.9936 → 1.0000; `second_sources.txt`); index opens before 2010 and some Yahoo opens are stale (`PF/data/README.md`; `G2_rules.md` §1); Binance keeps zero-volume rows after delisting and moved to 4h/1h funding in 2023 (`w1-crypto.md` red team).
- [ ] Process: a script refuses market data without a registered id (`2026-10-06-0247/hypothesis.py`); commit the prereg before code exists; an independent verifier re-implements from the spec without reading the code (tolerances in `w1-synthesis.md` verification facts); the red team's default is "refuted" and attacks negative verdicts too.
