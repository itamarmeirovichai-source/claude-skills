# Brief: Department D Backtest Engineer + Execution Realism Engineer — the shared engine (output: quant-edge/src/qe/engine/, tests)

Build the shared, registered-id-gated backtest engine every batch-1 variant will run on. Nothing variant-specific; shared code is committed with
its tests before use (Gate 1 exemption). Data enters only through `qe.gateway.load(id, window)`.

Engine (`src/qe/engine/`): (1) `bars.py`: 1-minute and daily bar frames (UTC `ts` = bar OPEN), session tagging from `qe.sessions` (RTH flag, trading-day
id starting at the 18:00 ET reopen, half-day flag, roll-week flag), resampling that labels by open time and never reads the closing bar of the day
being decided; (2) `rules.py`: a small declarative interface: `signal(bars) -> target position per bar` computed from information available at the bar's
open (asserted by the future-truncation harness), with the ex-ante volatility scaler (window, cap, floor from the registry row); (3) `fills.py`: fill
models: market order at next bar open + slippage (per-instrument floor from 00-common.md, extra at 02:00 ET, opens and settlements), limit fills only when
price trades through the limit, stop orders with the bar-ambiguity convention FIXED and documented (when a bar touches both stop and target the stop is
assumed first; stops sampled at bar granularity, gap-through fills at the open), flat-by enforcement at the firm deadline minus N minutes, an optional
one-minute and five-minute entry delay; (4) `pnl.py`: daily mark-to-market P&L in ticks, points, money and R; costs at 1× and 2× in the same run; turnover,
trades per day, days with a trade, holding times, best-20-days fragility, by-year / by-month / by-vol-tercile tables, session-edge and roll-week share of P&L,
a preliminary path-wise breach count against FTMO 5%/10% and a trailing-drawdown plan at the row's guard fraction; (5) `harness.py`: the future-truncation
harness (delete every bar after the entry minute of day d; nothing about day d may change), the perturbation test, the execution-lag variants (close vs next
open; lag 1 vs lag 2; as-written vs ex-ante eligibility; the worse decides), the ±25% neighbourhood runner, random-entry nulls with the same holding
distribution (≥ 10,000), shuffled-signal permutations in 20-day blocks, buy-and-hold at matched exposure; (6) `report.py`: writes `research/results/<id>.md`
with every standard table of criterion 12 plus N_total, the bar in Sharpe units for the OOS length, criterion-4 power and the joint power from PARAMETERS.md,
and the `registry_reads.log` lines for the run. numba for the inner loops: a 16-year 1-minute test must run in minutes on 4 CPUs.

Tests (pytest, synthetic data only): a driftless random walk with a 2R target and 1R stop returns mean R ≈ 0 (within 3 s.e.) at zero cost and negative at
floor cost; a planted look-ahead rule (uses the day's close) is caught by the truncation harness; a rule that reads only past bars passes it; bar-ambiguity
convention test; flat-by enforcer closes at the deadline on a half day; the 2× cost run halves the net of a known edge; daily P&L sums to trade P&L; the
engine refuses to run without a registered id (calls `gateway.load`). Document conventions in `src/qe/engine/CONVENTIONS.md` (English).
Read first: `briefs/00-common.md`, `briefs/inherited-method-lessons.md`, `briefs/inherited-code-reusable.md` (reuse ideas from the inherited `scripts/` only by
re-implementation, never by import), `PARAMETERS.md`. Run the whole suite before finishing. Do not commit.
