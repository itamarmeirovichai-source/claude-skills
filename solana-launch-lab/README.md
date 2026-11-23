# Solana Launch Lab

A local, **read-only** research tool for Pump.fun token launches on Solana. It collects public data,
explains structural risks with the evidence behind each statement, and paper-trades fixed rules under
realistic costs.

It was built alongside an audit of a social-media trading claim. The audit is in
[CLAIMS_AUDIT.md](CLAIMS_AUDIT.md); the research behind it is in [RESEARCH.md](RESEARCH.md).

> **This is not a trading bot and gives no financial advice.** It cannot connect a wallet, hold a key,
> sign, or send a transaction. A risk reading is not a buy signal or a forecast. No strategy here has been
> shown to make money; the published evidence so far says followers of early launch signals lose after costs.

## Run it

Requires Python 3.11 or newer. There is nothing to install: the application uses the standard library only.

```bash
cd solana-launch-lab
python -m launchlab serve
```

Open <http://127.0.0.1:8765/>. On first start it creates `data/launchlab.sqlite3` and fills it with 300
**synthetic** tokens so every screen works offline. Synthetic data is marked by a striped banner, a
`SYNTHETIC` badge on every row, and mint names starting with `SYNTH` (which cannot be real addresses).

To allow read-only requests to public data providers:

```bash
python -m launchlab serve --live        # or set LAUNCHLAB_MODE=live in .env
```

No API key is needed for either mode.

## Commands

| Command | What it does | Network |
|---|---|---|
| `python -m launchlab serve [--port N] [--live] [--no-seed]` | Start the dashboard | only with `--live`, and only when you press a live button |
| `python -m launchlab seed-demo [--seed N] [--tokens N]` | Regenerate the synthetic universe and its paper book | none |
| `python -m launchlab paper-run --book demo\|live` | Record new signals, update paper positions, print metrics | none |
| `python -m launchlab ingest <mint> --live` | Fetch public data for one exact mint | read-only |
| `python -m launchlab discover --live` | Import the newest Pump.fun launches from the provider's new-pools list | read-only |
| `python -m launchlab watch --live [--interval 60] [--max-new 2] [--cycles N]` | Repeat: discover, ingest a few, update the live paper book | read-only |
| `python -m launchlab audit <mint> --alert <UTC time> [--claimed-cap USD] [--claimed-multiple N] [--onchain] --live` | Check an "alert at T, N× later" claim against candles | read-only |
| `python -m launchlab verify-log` | Verify the hash chain of the event log | none |
| `python -m launchlab status` | Counts, provider health, settings (RPC URL redacted) | none |

Example, reproducing one row of the audit:

```bash
python -m launchlab audit CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump \
  --alert 2026-11-20T20:52:00Z --claimed-cap 58000 --claimed-multiple 24 --live
```

## What the dashboard shows

| Tab | Content |
|---|---|
| **Tokens** | Search by exact mint address (tickers are not unique and are never matched). Each token page lists market observations with provider, venue, price, FDV, market cap **and which definition each number uses**, liquidity, volume, observation time and data age; the risk components with evidence, source, confidence and unknowns; recorded signals and the paper position; provider disagreements. A replay slider recomputes everything from what was stored up to a chosen moment. |
| **Paper ledger** | Every signal, including rejections and why. Gross and net PnL, fees, drawdown, exposure, win/loss distribution, expectancy with a bootstrap interval, unsellable and failed cases, and a verdict that stays `inconclusive` until the pre-registered sample is reached. |
| **Claim check** | The `audit` command as a form. |
| **Data health** | Provider errors and rate limits, conflict count, event-log integrity, settings in effect. |

## How the risk analysis reads

Eight components, each with a status (`known`, `partial`, `unknown`), a level (`high`, `elevated`, `no flag`),
its evidence and its source: creation-slot concentration, creator's own buy, wallet relationships, creator
history, ownership concentration, liquidity, sale impact, data quality.

- There is **no single score** and no ranking by "quality".
- Missing data is reported as `unknown`, never as "no flag".
- Wallets that co-sign one transaction are described as coordinated. A shared first funder is described as
  a *probabilistic* link. Neither is described as common ownership.
- On the public Solana RPC, holder lists and creator history are usually `unknown`; see
  [DATA_SOURCES.md](DATA_SOURCES.md) for why and what would fix it.

## How the paper trading works

1. At `launch + 90 s` the decision rule looks only at data observed up to that moment and records
   `candidate` or `rejected` with reasons. The signal is written before any outcome is computed.
2. A candidate is "bought" at the first observation after a latency, using pool reserves when known,
   with venue fees by market-cap tier, network fees, token-account rent, extra slippage, a failure
   probability per attempt, and a cap on pool share.
3. It is "sold" only by a fixed rule (take-profit, stop-loss, or time stop), one latency after the trigger.
   A later all-time high is never an input.
4. No exit data or too little depth means `unsellable` at zero.

**The rules are yours to set.** They live in [`launchlab/policy.py`](launchlab/policy.py):
`DecisionRule` (which launches qualify) and `ExitRule` / `exit_trigger` (when to exit). The exit rule is the
most consequential choice in the study: tight stops are hit by noise on thin pools, wide targets give back
the common round trip, short time stops miss slow movers. Decide before looking at outcomes, and change
`RULESET` whenever you change a rule so results from different rules are never pooled.

The evaluation plan (minimum 200 resolved candidates over 14 days, time-ordered split, adjustment for the
number of rulesets tried) is in [PROJECT_SPEC.md](PROJECT_SPEC.md) section 10.

## Configuration

Copy `.env.example` to `.env` to change a default. Every value is optional and none is a secret. If you use
your own Solana RPC endpoint and its URL contains an access token, keep it only in `.env` (git-ignored);
the app redacts the URL wherever it is displayed or stored.

Raw provider responses are stored locally only for providers whose switch is on
(`STORE_RAW_SOLANA_RPC=1` by default; the two market-data providers are off because their storage terms
are unclear). Nothing is ever uploaded.

## Dependencies

| Package | Used for | Where |
|---|---|---|
| *(none)* | The application runs on the Python standard library | runtime |
| `pytest` | Test runner | development only |
| `ruff` | Linter, including security rules | development only |
| `mypy` | Static type checking | development only |

Development tools are pinned in `uv.lock`. With [uv](https://docs.astral.sh/uv/):

```bash
uv sync                 # creates .venv with the three dev tools
uv run pytest           # 72 tests
uv run ruff check .
uv run mypy
```

Without uv, any environment that has the three tools works: `python -m pytest`, `ruff check .`, `mypy`.

## Safety properties, and the tests that hold them

| Property | Enforced by |
|---|---|
| No signing, sending or key-handling code | `tests/test_safety.py` scans every source file for such identifiers |
| RPC access is an allowlist of read methods | `providers/solana_rpc.py`; tests assert write methods are refused before a request is built |
| Demo mode makes no network call | HTTP clients are disabled unless live mode is on; tested |
| Demo data cannot pass as live | row flag, banner, badge, impossible mint names, separate books; tested |
| No look-ahead in signals or risk reports | `as_of` filtering; tests add future data and assert nothing changes |
| The later high is never an exit | test with a deliberate price spike between trigger and fill |
| Local only | loopback bind, Host and Origin checks, JSON-only POST; tested |
| Tamper-evident history | hash-chained event log; test edits and deletes rows |

## Limitations

- Results on synthetic data demonstrate the mechanics only.
- Live launch discovery samples one provider's newest-pools list; launches between polls are missed.
- Holder lists and creator history need a custom RPC or an indexer.
- A very busy bonding curve can outrun the history depth read on a public endpoint; its launch structure is
  then `unknown`.
- Fills are modelled, not matched against real trades. Real execution would be worse, never better.
- One-minute candles hide the order of trades inside a minute.
- Pump.fun's fee schedule and program behaviour change; the fee table is dated and versioned in the code.

## Files

| File | Purpose |
|---|---|
| [CLAIMS_AUDIT.md](CLAIMS_AUDIT.md) | Claim-by-claim verification of the audited post |
| [RESEARCH.md](RESEARCH.md) | Method, findings, literature, competing hypotheses |
| [DATA_SOURCES.md](DATA_SOURCES.md) | APIs, terms, rate limits, definitions, gaps |
| [PROJECT_SPEC.md](PROJECT_SPEC.md) | Requirements, architecture, evaluation plan, failure modes |
| [progress.md](progress.md) | Current state, next steps, resume commands |
| [research-notes/](research-notes/) | Working notes from the research session |
| `launchlab/` | Application source |
| `tests/` | Test suite |

## Independence and licence note

This project was implemented from official chain documentation and general AMM mathematics. It contains no
code, screenshots, branding or styling from the project it audits, whose repository licence reserves all
rights. No licence has been chosen for this folder yet; that is the repository owner's decision.
