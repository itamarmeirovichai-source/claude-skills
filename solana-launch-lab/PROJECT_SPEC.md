# Solana Launch Lab — project specification

Version 0.1 · written 2026-11-23, before implementation · working name only, no affiliation with any
project audited in this folder.

## 1. Purpose

A local, read-only research tool that (a) collects public data about new Pump.fun token launches,
(b) explains structural risks with the evidence behind each statement, and (c) paper-trades fixed,
pre-registered rules under realistic costs so that the question "does any rule have positive expected value
after costs?" can be answered with data instead of screenshots.

It is **not** a trading bot, a signal service, or a predictor. A clean risk reading never means "likely to
profit".

## 2. Hard constraints

| Constraint | How it is enforced |
|---|---|
| No wallet, key, seed phrase, exchange credential | No code path accepts or stores one. `.env.example` contains only an optional RPC URL and tuning values. |
| No signing, no transaction submission, no live buy/sell | The Solana adapter exposes an allowlist of read methods; anything else raises before a request is built. `tests/test_safety.py` scans the source tree for signing/sending identifiers and fails if any appear. |
| No copied code, brand, screenshots or styling from the audited project | Independent implementation from official chain documentation and general AMM mathematics; its repository licence forbids reuse. |
| Demo data can never be mistaken for live data | Every row carries `is_synthetic`; synthetic mints start with `SYNTH`; synthetic and live results live in separate books; the UI shows a fixed banner and per-row badges. |
| No fabricated values | Missing fields stay `null` and render as "unknown"; checks that cannot be computed report `status: unknown`. |
| No secrets in files or logs | Config loader redacts any URL query string and credentials when logging. |
| Local only | Server binds `127.0.0.1`; state-changing endpoints require a same-origin JSON request. |

## 3. Stack and why

- **Python ≥ 3.11, standard library only at runtime** (`sqlite3`, `http.server`, `urllib`, `hashlib`, `json`).
  The repository's only other project is an unrelated Node/TypeScript PWA, so there was no stack to extend.
  Standard-library Python gives persistent storage, an HTTP server and exact integer arithmetic with zero
  third-party packages to audit.
- **Dashboard:** static HTML, CSS and vanilla JavaScript served by the same process. No build step, no CDN.
- **Dev tools only:** `pytest`, `ruff`, `mypy`, pinned in `uv.lock`.
- **Storage:** one SQLite file under `data/` (git-ignored).

## 4. Architecture

```
launchlab/
  config.py          settings from environment / .env (no secrets required)
  db.py              schema, connection, append-only event log with hash chain
  amm.py             bonding-curve and constant-product arithmetic, price impact
  costs.py           fee tiers and transaction-cost model (all values configurable)
  providers/
    base.py          Provider interface, HTTP client: timeout, retry, backoff, rate limit
    dexscreener.py   current market state for an exact mint
    geckoterminal.py pools, OHLCV history, newest pools
    solana_rpc.py    read-only allowlist: creation tx, launch-slot buyers, pool balances
    synthetic.py     seeded demo generator, clearly labelled
  ingest.py          combine providers → observations, quality flags, conflicts
  risk.py            explainable risk components as of a point in time
  policy.py          the pre-registered decision and exit rules (versioned)
  paper.py           paper-trading simulator, ledger, metrics, uncertainty
  audit.py           re-check a "alert at time T, N× later" claim against candles
  backfill.py        backtest: unselected sample of past launches read from the chain
  server.py          JSON API + static dashboard
  __main__.py        command line
  static/            dashboard
tests/               unit, integration and safety tests
```

Data flow: provider → raw snapshot (optional, per-provider switch) → normalized **observation** with
`provider`, `observed_at`, `ingested_at`, `definition`, quality flags → risk report and signals computed
"as of" a timestamp → paper orders and fills → metrics. Every step appends to the event log.

## 5. Data model

| Table | Key columns | Notes |
|---|---|---|
| `tokens` | `mint` (PK), `name`, `symbol`, `creator`, `launch_time`, `launch_source`, `token_program`, `is_synthetic` | Exact mint is the only identifier. |
| `observations` | `id`, `mint`, `kind` (`market`, `launch`, `holders`, `pool`), `provider`, `observed_at`, `ingested_at`, `payload` (JSON), `is_synthetic`, `stale`, `missing` (JSON list) | Append-only. |
| `raw_snapshots` | `id`, `provider`, `url`, `fetched_at`, `sha256`, `body` | Written only when that provider's storage switch is on. |
| `conflicts` | `mint`, `field`, `provider_a`, `value_a`, `provider_b`, `value_b`, `rel_diff`, `observed_at` | Disagreements above tolerance. |
| `signals` | `id`, `book`, `mint`, `as_of`, `ruleset`, `decision` (`candidate`/`rejected`), `reasons`, `features`, `features_hash`, `recorded_at` | Written before any outcome is computed. |
| `orders` | `id`, `signal_id`, `side`, `requested_at`, `size_sol`, `status`, `attempts` | |
| `fills` | `id`, `order_id`, `filled_at`, `price_sol`, `tokens`, `quote_sol`, `fee_sol`, `network_fee_sol`, `model`, `uncertainty` | `model` says how the fill was derived. |
| `positions` | `id`, `signal_id`, `book`, `mint`, `status` (`open`, `closed`, `unsellable`, `not_filled`), cost and proceeds, `exit_reason` | |
| `events` | `id`, `ts`, `type`, `payload`, `prev_hash`, `hash` | Tamper-evident chain. |
| `provider_health` | `provider`, `last_ok`, `last_error`, `error_count`, `rate_limited_until` | Shown in the UI. |
| `study` | `book`, `plan` (JSON), `registered_at` | Pre-registered sample size, period, ruleset, holdout date. |

## 6. Public-data ingestion (requirement A)

- **Import by exact mint** (`launchlab ingest <mint>` or the dashboard): DexScreener current state,
  GeckoTerminal pools and token record, Solana RPC creation transaction and launch-slot buyers via the
  bonding-curve account address taken from GeckoTerminal's pool list.
- **Discover new launches** (`launchlab discover`): GeckoTerminal `new_pools`, filtered to dex `pump-fun`.
  This is a documented endpoint. It is sampled, not a complete stream; the gap is recorded.
- **Stored per token:** mint, creator, launch time (UTC, on-chain block time when available, else the
  provider's pool-creation time, with `launch_source` saying which), bonding-curve state, launch-slot
  transactions, holders when readable, liquidity, market observations, ingestion time.
- **Quality labels:** `missing` (field absent in the response), `stale` (older than the provider threshold),
  `delayed` (observation older than the request by more than one cache period), `synthetic`, `conflict`.
- **Failure handling:** timeouts, HTTP errors, 429 with backoff and a cool-down recorded in
  `provider_health`, malformed JSON, schema drift (unknown fields ignored, missing fields flagged). A failing
  provider never blocks the others and never produces a fabricated value.

## 7. Explainable risk analysis (requirement B)

Each component returns `{name, status, level, value, evidence, source, observed_at, confidence, note}`.
`status` is `known`, `partial` or `unknown`. `level` is `low`, `elevated`, `high` or `n/a`.

| Component | Reads | Method | When unknown |
|---|---|---|---|
| `launch_slot_concentration` | creation-slot transactions | share of total supply bought in the creation slot; number of co-signing buyers | launch transactions not read |
| `creator_at_launch` | creation transaction | creator's own share bought in the creation transaction | same |
| `creator_history` | indexer (not available in the MVP's live mode) | prior launches and how many completed the curve | always in live mode; available in demo data |
| `ownership_concentration` | largest token accounts | share held by the top 10 non-pool, non-curve accounts | holder read refused or absent; top-20-only reads are `partial` |
| `wallet_relationships` | transaction co-signers, first funder | co-signing one transaction = coordinated by construction; shared first funder = **probabilistic** link | no transactions read |
| `liquidity` | pool reserves or provider liquidity | quote-side depth; whether LP tokens were burned when decoded | no pool data |
| `sale_impact` | reserves + holder shares | constant-product price after a stated sale: "the top-N non-pool holders sell everything" and "an order of size S"; `P_after / P_before = (R / (R + Q))²` | reserves or holdings unknown |
| `data_quality` | flags on the inputs | counts of stale, missing, conflicting inputs | never |

Rules of presentation:

- Inferred wallet relationships are worded "likely coordinated" / "shared funder" with the evidence listed;
  never "same owner".
- There is **no single score**. The report lists components, a count of high/elevated/unknown items, and
  a data-completeness figure.
- Risk-of-loss analysis and expected-return analysis are separate objects. The risk report has no field
  that could be read as a forecast, and the UI says so next to it.

## 8. Dashboard (requirement C)

| View | Content |
|---|---|
| Header | Mode banner: **"DEMO — SYNTHETIC DATA, NOT A MARKET"** or "Live public data (read-only)"; provider health; study status. |
| Tokens | Search by exact mint (validated base58); table with launch time, source, data age, flags, synthetic badge. |
| Token detail | Identity; market table with price, FDV, market cap **and which definition**, liquidity, volume, provider, observed-at, age; risk components with evidence and unknowns; signals and alerts with timestamps; provider conflicts. |
| Replay | A time slider that recomputes the risk report and shows only observations known at that moment. |
| Paper ledger | Every candidate and rejection with reasons; orders, fills, positions; gross and net PnL; drawdown; exposure; win/loss distribution; expectancy; unsellable cases; bootstrap interval; verdict (`inconclusive` until the pre-registered sample is reached). |
| Claim check | Enter a mint, an alert time and a claimed cap/multiple; get the candle-based comparison. |
| Data health | Provider errors, rate limits, conflicts, event-log integrity. |

Visual direction: own design, neutral palette, no borrowed branding.

## 9. Paper-trading ledger (requirement D)

Order of operations for each token, strictly time-ordered:

1. **Decide** at `as_of = launch + decision_delay`, using only observations with `observed_at ≤ as_of`.
   Write the signal (candidate or rejected, with reasons and a hash of the features) to the ledger.
2. **Enter** at the first observation at or after `as_of + latency`. If none arrives within
   `max_wait`, record `not_filled`.
3. **Fill model.** With pool reserves: constant-product output on effective reserves after the fee for the
   current market-cap tier. Without reserves: observed price worsened by configured slippage plus an impact
   term from reported liquidity. Each attempt can fail with a configured probability (deterministic from a
   seed); a failed attempt still pays network and priority fees and adds latency. Orders larger than a
   configured share of the pool are filled partially.
4. **Exit** by fixed rule only: take-profit multiple, stop-loss fraction, or time stop, evaluated on each
   later observation; the exit executes at the first observation at or after `trigger + latency`, not at
   the trigger price. **The later all-time high is never an input.** Exit proceeds count the position's own
   SOL as still in the pool: with recorded reserves `(Q, B)` and `x` tokens held, gross proceeds are
   `Q·x / (B − x)`. The older, harsher pricing `Q·x / (B + x)` capped by recorded real SOL is available as
   `own_liquidity = false` and is reported as a conservative bound. (Added in 0.1.1, before the first
   backtest; see BACKTEST.md.)
5. **Unsellable.** If no observation arrives within `max_wait` of the exit trigger, or exit liquidity is
   below the configured minimum, the position is closed as `unsellable` at zero.
6. **Still open at the end of data:** reported separately, marked at the last price and also at zero.

Costs (defaults from DATA_SOURCES.md, all configurable): venue fee by tier, base fee per signature, priority
fee, optional tip, token-account rent on entry, extra slippage.

Reported: counts of signals / candidates / rejections / fills / failures / partials; gross PnL (price
effect including impact, before fees) and net PnL; win and loss distribution; expectancy per trade; maximum
drawdown of cumulative net PnL; exposure (capital-time and peak concurrent capital); unsellable count;
bootstrap 95% interval for mean net return; verdict.

Reproducibility: config hash and ruleset version on every signal; seeded randomness; append-only hash-chained
event log; raw snapshots where the provider's terms allow.

## 10. Evaluation plan (pre-registered defaults)

| Item | Default | Why |
|---|---|---|
| Unit of analysis | one signal per token, first decision only | avoids counting one token many times |
| Minimum resolved candidates | 200 | with per-trade return standard deviation near 100%, the standard error of the mean is about 7 points; fewer cannot distinguish a small edge from zero |
| Minimum calendar span | 14 days, covering at least 2 weekends | regime and day-of-week variation |
| Split | first 70% of signals by time = development; last 30% = holdout, evaluated once | time-ordered, no shuffling |
| Rulesets tried | recorded; verdict requires the holdout interval to exclude zero after a Bonferroni adjustment for the number tried | multiple testing |
| Primary metric | mean net return per candidate, including not-filled, failed and unsellable outcomes | no dropping of bad outcomes |
| Verdict labels | `inconclusive` (default), `negative`, `positive-needs-replication` | "positive" always needs a second window |

Synthetic demo results are never evaluated against this plan; the UI labels them "mechanics demo".

## 11. Assumptions

- Pump.fun supply is 1e9 unless a provider reports otherwise (Mayhem-mode coins differ; flagged when seen).
- PumpSwap pools price on real quote balance plus the `InitBoost` amount (observed, not documented).
- The simulator's quote currency is SOL; USD figures use the SOL/USD rate observed with each data point.
- Candle data gives one price per minute; fills inside a minute carry that candle's range as uncertainty.
- The paper order does not move the market for other participants and is not front-run beyond the
  configured slippage. Real execution would be worse, never better.

## 12. Failure modes and responses

| Failure | Response |
|---|---|
| Provider down or rate-limited | Mark health, back off, continue with others; UI shows which values are missing. |
| Provider schema changes | Unknown fields ignored; required fields missing → observation flagged, not guessed. |
| Providers disagree | Both kept; conflict row written; UI shows both with sources. |
| Stale cache | Flagged; excluded from fills when older than `max_fill_staleness`. |
| RPC history pruned | Launch structure `unknown`; token still tracked. |
| Wrong token (ticker collision) | Only exact mints accepted; search never matches by symbol alone. |
| Clock skew | All times UTC; `ingested_at` from local clock, `observed_at` from the source. |
| Database tampering or partial write | Hash chain verification in Data health; transactions per ingest. |
| User misreads a risk reading as advice | Fixed wording in the UI and README; no score, no ranking by "quality". |

## 12a. Backtest (added in 0.1.1)

`launchlab backfill` reads an unselected sample of past launches from the chain and applies two rulebooks to
the same data: the filter above and a baseline that enters every priced launch. The plan is written and
committed before the data is read; see [BACKTEST.md](BACKTEST.md). A backtest can show that a rule loses; it
cannot show that one wins.

## 13. Out of scope for 0.1

Live transaction streaming over WebSocket; complete holder enumeration; creator history in live mode;
funding-graph tracing beyond one hop; Telegram or any other alert delivery; any execution.
