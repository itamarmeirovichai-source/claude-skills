# Inherited method lessons: the checklist (Scribe, 2026-11-03)

Paths: PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`, D=`PF/agents/daily`, R=`PF/references`, PR26=`~/quant-edge-inherited/pr26/prompts/research`. Sources: `PR26/digest-hypotheses-ledger.md` (prompt_rules), `PF/agents/board.md` (5 Oct), the statistician audits, wave files and department red teams. Tick every line before a result is read.

## Clock and DST
- [ ] Label bars by OPEN time: 09:30 bar = 09:30:00–09:30:59 (`D/2026-10-06-0247/data_hunter/loader_spec.txt`).
- [ ] HistData 1m (SPXUSD, DAX, ESTX50, JPXJPY) is New York time WITH DST, not the documented fixed EST; Oanda and Databento are UTC, FirstRate NY-naive, Polygon epoch-ms UTC (loader_spec rule 1; `D/w1-breadth/clock_xcorr.txt`).
- [ ] Verify every new file's clock outcome-free: mean |1m return| by minute around known opens, winter vs summer; 2020-03-09 and 2020-11-02 09:30 NY must map to 13:30Z/14:30Z (loader_spec TESTS; `D/2026-10-06-0247/statistician/audit_run.txt`).
- [ ] CME equity-index calendar for ES/NQ, drop the 44 CME-only sessions; half-days have 210 bars; SPXUSD's FOMC minute is unconfirmed before 2013-03-20 (loader_spec rule 2; `PF/agents/prereg/E2_rules.md` §1).

## Rolls
- [ ] Databento `.c.0` has no RTH bars on 30 expiry Fridays and sits in the dying contract for ~6 sessions (volume 0.09–0.32×); prefer explicit contracts or `.v.0` (`D/2026-10-06-0247/data_hunter/xcheck.txt`, `eric_profile.txt`; `PR26/databento-cost-check-2026-11-03.md`).
- [ ] Fix roll handling in the prereg: drop roll weeks (`D/orb-H0020/loaders.py` `roll_excluded`) or splice; never change it after results; roll weeks averaged -10.7 bp in F1 (`D/w3-ensemble/redteam/findings.md`).
- [ ] FirstRate rolls 1–3 days before Databento; they agree on 1,191 of 1,257 days outside roll weeks (`D/2026-10-05/data_hunter/second_sources.txt`).

## Look-ahead
- [ ] Eligibility may not read the trade day's bar count, 15:59 bar or any post-entry bar; IBS was flattered by 0.22R (`D/2026-10-05/statistician/audit.txt` §4; `PF/agents/board.md` "Look-ahead pattern").
- [ ] Run the future-truncation harness before any number: delete bars after the entry minute, nothing about day d may change (`D/2026-10-06-0247/statistician/test_future_truncation.py`; `PF/agents/prereg/D4-spec.md` G5).
- [ ] Truncation tests miss loader errors: hand-check rate lags, quote directions, swap on gross notional, cost timing (`R/w1-fxtrend.md` §7 D).
- [ ] Scale by past volatility only; a full-sample scaler understated drawdown by a third (`R/what-the-giants-do.md` §3; `PF/scripts/test_stack_backtest.py`).
- [ ] GEX/DIX is published ≈17:52 ET: next-day use only (`D/2026-10-06-0247/data_hunter/dix_pubtime.txt`).

## Bar stamping and execution (`PF/SKILL.md` "Replaying the valid setups")
- [ ] Bars are start-stamped: a 15:58 cutoff admits the 15:55 5m bar, so the last usable bar starts 15:50; a target counts only when the bar CLOSES beyond it; a bar touching stop and target is the stop; risk = planned level-to-stop distance.
- [ ] `.values` on a tz-aware series silently converts to UTC; `resample('ME')` mislabels weekend month-ends; resting limits in the evening session fill meaninglessly; trailing stops at the bot's scan interval, not bar extremes.
- [ ] Fill at the next bar's open and measure decay with 1- and 5-minute delays (`PR26/lit-practitioner.md` rule 9).

## Bootstrap and statistics
- [ ] Cluster by trading day with a cluster-robust SE around the trade mean (`PF/SKILL.md` "The gate").
- [ ] A one-sided 0.05/N bound needs ≥ 50/alpha draws (430,000 at N=430); never `gate.py bootstrap_ci` or `tjr_backtest.boot_mean` (`D/2026-10-05/eng_head/ledger_gate.py`; `PF/agents/board.md` "Gate rule 3 in code").
- [ ] Daily series: t = min(iid, Newey–West lag 10), p5 = min(10,000 iid, 10,000 block-20, seed 0) (`PF/agents/prereg/D2_rules.md` §6); horizons in days-with-a-trade (~14/month), the gate needs ~3× a two-sided-95% sample (`audit_run.txt` horizon_at_gate).
- [ ] Headline chosen by in-sample Sharpe before OOS; the worse of lag1/lag2, close/next-open, as-written/ex-ante decides; nothing passes on 1× cost alone (digest prompt_rules; `R/w1-fxtrend.md` §2).
- [ ] A max-minus-min across groups is a selection (`PF/scripts/test_dashboard.py` null test); post-hoc slices are information, not findings; a bug fix after results needs before/after numbers (`D4-spec.md` §8).

## Vol scaling, benchmark, prop fit
- [ ] Compare every long-biased result with same-exposure buy-and-hold and drop the 20 best days (`PF/agents/wave-2026-10-11.md` wave 4; `R/w4-meanrev.md`).
- [ ] At the target volatility count 5% daily-loss and 10% max-loss breaches over rolling windows (F1 worst day -6.74%, G2 19–35 days, crypto 37–56% of windows; `R/w3-ensemble.md`, `R/w1-crypto.md`).
- [ ] Skew and barrier/CPPI sizing do not lower the Sharpe needed (`R/w1-synthesis.md`, 12 and 16 Oct).

## Licence and provenance
- [ ] FirstRate and Databento third-party copies are a licence hold, cross-checks only (`PF/agents/board.md` Decision 8); F1 nevertheless used an NQ.c.0 5m splice (digest gaps).
- [ ] Pin every file by sha256 and refuse on mismatch; data stay in scratch; nothing > 1 MB is committed (`D/orb-H0020/loaders.py`; wave rules).
- [ ] Never mix adjusted and raw files (Ascensao SPY is back-adjusted; `second_sources.txt`); pre-2010 index opens and some Yahoo opens are stale (`PF/data/README.md`; `G2_rules.md` §1); Binance keeps delisted rows and moved funding to 4h/1h in 2023 (`R/w1-crypto.md`).
- [ ] Process: scripts refuse market data without a registered id (`D/2026-10-06-0247/hypothesis.py`); prereg committed before code; a verifier re-implements from the spec without reading the code; the red team's default is "refuted" (`R/w1-synthesis.md`).
