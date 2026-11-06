# qe.engine conventions (Department D, 2026-11-04)

Every number the engine prints follows the rules below. A rule that needs a different convention gets a new row and a
documented reason; the conventions themselves never change after a result exists.

## 1. Bars and clocks (`bars.py`, `qe.sessions`)

- A bar frame has `ts` (tz-aware UTC, the bar **OPEN**), `open, high, low, close`, optional `volume`, sorted, unique `ts`,
  in nanoseconds (pandas ≥ 3 parses strings to microseconds; `validate()` coerces). Bars are start-stamped: the 09:30 bar
  covers 09:30:00–09:30:59.
- Session tags come only from `qe.sessions.tag_minutes`: `ny_minute` (New York wall clock, DST-aware), `tday_minute`
  (minutes since the 18:00 ET Globex reopen: 18:00 ET = 0, 09:30 ET = 930, 16:00 ET = 1320, 16:10 ET = 1330, 17:00 ET =
  1380), `trading_day` (CMES session label = calendar date of the close), `in_session` (18:00–17:00 ET), `is_rth`
  (XNYS 09:30 to the 16:00 or 13:00 ET close), `has_rth`, `is_half_day`, `is_roll_week` (Mon–Fri of the week holding
  the third Friday of Mar/Jun/Sep/Dec plus the next Monday), `rth_close_minute`, `session_close_minute`,
  `tday_close_minute`, plus `day_id` (0..n−1) and `bar_minutes`.
- The trading day starts at the 18:00 ET reopen: a hold opened after 18:00 ET and closed before the next afternoon's
  deadline is inside ONE trading day (briefs/00-common.md, firm structure 1). Bars 17:00–17:59 ET belong to the
  closing day but are `in_session = False`. A calendar date without an XNYS session (Thanksgiving, Good Friday …) is a
  CME-only session: `has_rth = False`, no RTH entry is ever generated.
- Resampling (`resample_intraday`) buckets by `tday_minute // n` inside the trading day (no bar straddles 18:00 ET),
  labels by the **open** of the first constituent and adds `complete_ts` = last constituent open + one source bar: a
  resampled bar may be read only at or after `complete_ts`. `daily_from_bars` builds one row per trading day; its
  `close` is known at the session close only. `prior_day_features(lag ≥ 1)` is the only way day-level values reach the
  bars of a day: day d never sees its own daily bar.
- Registry windows (`IS=a..b`) are UTC calendar-date windows on bar-open timestamps; `run.load_registered` drops the
  trading day that straddles a window boundary from **both** sides (keep `start < trading_day ≤ end` for intraday
  frames, `start ≤ trading_day ≤ end` for daily frames). One trading day is lost at each boundary; none is shared.

## 2. Information set (`rules.py`, asserted by `harness.py`)

- `target[i]` is the position held over bar i (open[i] → open[i+1]) and may depend only on bars 0..i−1 and on day-level
  values of earlier trading days. `orders(bars).entry_idx = i` means "decided at the information set of open[i]" with
  the reference price `open[i]`.
- The future-truncation harness deletes every bar after the entry minute of a sampled day d and requires the decisions
  of day d up to that minute to be identical; the perturbation harness multiplies every later bar by noise and requires
  the same. A rule fails if it reads the day's close, the day's bar count, the day's high/low, or any post-entry bar.
- Vol scaler: `clip(target_vol / σ_ex-ante, floor, cap)` with σ from the previous `window` daily close-to-close returns
  (days d−window … d−1), annualised; constant inside a trading day; 0 exposure until `window` returns exist. Row field
  format: `window=20;cap=3;floor=0.3;target=0.15` (the Day-1 prose "ex-ante 20d realized, cap 3x, floor 0.3x" parses too).

## 3. Fills (`fills.py`)

- **Market orders** fill at the next bar open relative to the deciding bar: a change of target decided from bars < i
  fills at `open[i]` (the base case, "lag 1"). The lag harness also runs the optimistic "signal at close, fill at close"
  (`close[i−1]`) and "lag 2" (`open[i+1]`); the worse decides. Entry delay of 1 and 5 bars shifts the whole target /
  entry series later; bracket distances stay relative to the ORIGINAL reference open.
- **Costs** are charged per side in points: `slippage floor × window multiplier + commission / point value`. Floors
  (00-common.md, market orders, RTH): ES 0.30 pt + $2.50, MES 0.25 pt + $0.80, NQ 0.25 pt + $2.50, MNQ as MES
  (assumed), SPY 0.5 bp, CFD index/FX 1.0 bp (range 0.5–1.5), gold 1 bp, WTI 2.5 bp, natgas 8 bp, crypto perp 7 bp
  (funding not modelled). Multiplier 2× inside 02:00–02:05 ET, 09:30–09:32 ET, 18:00–18:02 ET, 15:59–16:01 ET and
  16:14–16:16 ET (settlement). Fill prices in the trade table are the reference prices and the cost is a separate
  column, so the 1× and 2× runs share one trade path and the 2× column is exactly double.
- **Limit orders** fill only when price trades THROUGH the limit: a long target at L fills when `high > L` (strictly),
  a short target when `low < L`; a touch (`high == L`) is not a fill. A gap through the limit at the open fills at the
  limit price (conservative). Limit fills pay commission, no slippage.
- **Stop orders** are sampled at bar granularity: a long stop at S triggers when `low ≤ S` and fills at S; when the bar
  OPENS through the stop the fill is the open (gap-through fills at the open). Stops pay slippage.
- **Bar ambiguity**: when one bar touches both the stop and the target, the **stop is assumed first**. (With 1R = 8
  points and 1-minute bars this bias is immaterial; the driftless 2R/1R calibration returns mean R within 1 s.e. of 0.)
- **Flat-by**: the exit market order is sent at the open of the first bar whose `tday_minute ≥ deadline − N`
  (`flat_by_margin_minutes`, default 2); no entry at or after that minute. Deadlines (`qe.sessions.FLAT_BY`, clauses
  dated 2026-10-11): Topstep 15:10 CT, Bulenox 15:59 CT, MFFU 16:10 ET, Tradeify/Lucid 16:45 ET, FTMO intraday 23:55
  Prague. On a half day the deadline is min(firm deadline, RTH early close): 2024-11-29 exits at 12:58 ET. A day
  without a bar at or after the flat-by minute closes at the last bar of its session (`flat_by_lastbar`, counted).
  `intraday_only` also forces the target to zero at the last bar of every trading day and outside the session.
- One position at a time in bracket mode (entries while a position is open are skipped and counted); a delayed fill
  that is already through the stop or the target exits at once at the fill price.

## 4. P&L (`pnl.py`)

- Per-bar mark-to-market: `pos_before × (close[i] − close[i−1]) + Σ fills at bar i of qty × (close[i] − price)`; the
  round-trip cost of a bracket trade is booked on its exit bar. Daily P&L is the bar P&L summed over the trading day
  (18:00 ET boundary); its sum equals the sum of trade P&L (tested). Units: points, ticks, money (point value), R.
- R: `config.r_points`, else the median stop distance of the run's trades, else one ex-ante daily standard deviation
  of the close in points. Trade-level R (`r_mult`) = gross / stop distance.
- Standard tables: gross, net 1×, net 2× (same run) in points / ticks / money / R per day; t = min(iid, NW lag
  max(10, longest hold in days)); Sharpe with the Mertens/Opdyke SE and Lo factor; max drawdown; worst day; by-year
  (a year counts with ≥ 200 days; need round-half-up(0.7 × years) positive; no year or month > 50% of net); by vol
  tercile (trailing 20-day realized vol, ex ante; bounds fixed in sample via `vol_tercile_bounds`, otherwise computed and
  flagged); session-edge share (first/last 5 RTH minutes, reopen, settlement) and roll-week share; best-20-days
  fragility; turnover, trades per day/year, days with a trade, holding times, longest gap between trades.
- Preliminary path-wise breach counts at the run's size: FTMO 5% daily loss from the 00:00 Europe/Prague equity
  (floating P&L included), FTMO 10% static max loss, and an EOD-trailing drawdown plan (`trailing_dd_usd`, floor locks
  at the starting balance) with the guard at `guard_fraction` of the limit. Department F's prop-fit simulation is the
  authority (criterion 11); these counts are information for Gate 3.

## 5. Harness (`harness.py`)

- Random-entry null (≥ 10,000 paths): same trade count, side mix and holding-time distribution (resampled), entries
  uniform over the bars of the same session type (RTH when every entry is in RTH, else the whole session) before the
  flat-by minute, exit at the open after the hold (capped at the session end when `intraday_only`); gross per trade
  compared (costs are shared by construction up to limit-vs-market exits; a net version with market exits both sides
  is also reported).
- Shuffled-signal permutation: the position path is permuted across trading days in 20-day blocks against the realised
  close-to-close bar returns; p = (1 + #{perm ≥ observed}) / (n + 1), gross.
- Buy-and-hold at matched exposure: (a) long over the strategy's in-market bars at its mean |position|; (b) always long
  in session at the same average exposure; alpha t (min of iid and NW) of the strategy's daily net 1× on each.
- Gate statistics: criterion 3 (net 2× mean > 0, t ≥ 1.65), criterion 4 (net 1× t_min ≥ 3.6807 or 3.8538 for an
  unfixed sign, bootstrap lower bound at 0.05/430 > 0 from 430,000 draws: iid whole-day resampling for strategies flat by
  the session end, stationary blocks of mean 20 days otherwise; p5 reported beside it), criterion 7 arithmetic.
  Neighbourhood: ±25% on each continuous parameter, one step on each discrete one, run once; never changes the headline.

## 6. Provenance

- `pnl.simulate` refuses a frame that is neither marked by `run.run_registered` (which calls `qe.gateway.load`, the
  only door, which logs the read) nor produced by `bars.synthetic_walk` / `synthetic_daily_walk` (`attrs["synthetic"]`).
  There is no third way to get P&L out of the engine. `report.write_result` prints the `registry_reads.log` lines of
  the id, the commit, the seeds, the command and the config.

## 7. Performance (measured 2026-11-04, 4 shared cores, numba cache warm)

- Synthetic 16-year full-session one-minute frame: 5,666,220 bars, generation + tagging ≈ 15 s, 436 MB.
- `simulate` on 1.06 M bars (3 years) ≈ 0.4 s; on the 5.67 M-bar 16-year frame 2.6 s (36,746 bracket trades).
- `tests/test_engine_calibration_16y.py` (opt-in, `QE_SLOW=1`), measured 2026-11-04 while two other agents ran:
  generation + tagging 15.3 s, simulate 2.6 s, gate statistics (430,000 draws) + 10,000 random-entry paths + 1,000
  block permutations + lag variants 194.9 s, **total 212.8 s** (3 min 33 s); mean R = 0.0120 ± 0.0070 (s.e.) at zero
  cost on the driftless walk. The 430,000-draw stationary bootstrap dominates (≈ 9 s per 500 trading days).

## 8. Left for Departments C and D

- C: `qe.sessions` internals (per-root templates, exact CME early-close minutes, the CME-only session list, a roll
  calendar from Databento definitions, FTMO's 00:00 CE(S)T day boundary, firm clauses verified by the Rules Keeper).
- D (variant work, never shared code): the rule classes themselves; FTMO swap charges per calendar day held (not in
  `fills.py`; a swing row adds them in its rule's cost model); crypto funding; 1-second bars for the ≤ 10 s hold share
  (reported as 0 at one-minute resolution); a tested bp-cost path for CFD instruments on real data.
