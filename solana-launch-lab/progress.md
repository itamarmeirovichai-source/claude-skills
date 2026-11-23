# Progress

Last updated: **2026-11-23** (UTC). Branch: `claude/solana-launch-research-lab-7eckwo`.

## State in one paragraph

Research, audit and a working local MVP are done. The audit found that the post's launch times are right,
its alert-time market caps are 6–10× too low against two independent sources, its multiples are not
reproducible from the stated alert times, and its PnL figure has no evidence behind it. The application
runs with one command, works offline on labelled synthetic data, reads live public data through three
read-only adapters, and keeps a paper ledger with a pre-registered evaluation plan. All checks pass.
**No evidence of positive expected value exists yet**; the live paper book has zero resolved candidates.

## Completed

| Phase | Output |
|---|---|
| 0. Environment inventory | Recorded below under "Tools used and unavailable" |
| 1. Post and claims audit | [CLAIMS_AUDIT.md](CLAIMS_AUDIT.md); primary post found and read; three tokens verified on-chain |
| 2. Repository and commercial context | CLAIMS_AUDIT.md sections 3 (claims 9–10) and 5; notes in `research-notes/repo_audit.md` |
| 3. PnL verification | CLAIMS_AUDIT.md claim 1: unverified, with the missing-evidence checklist |
| 4. Market, methods, failure cases | [RESEARCH.md](RESEARCH.md), [DATA_SOURCES.md](DATA_SOURCES.md), `research-notes/literature.md` |
| 5. Specification | [PROJECT_SPEC.md](PROJECT_SPEC.md) |
| 6. MVP | `launchlab/` (18 Python modules, static dashboard), `pyproject.toml`, `uv.lock`, `.env.example` |
| 7. Validation | 72 tests, ruff, mypy, headless-browser smoke test, live runs of `audit`, `ingest`, `watch` |

## Validation actually run (2026-11-23)

| Check | Command | Result |
|---|---|---|
| Unit and integration tests | `python -m pytest` | 72 passed |
| Lint incl. security rules | `ruff check .` | All checks passed |
| Types | `mypy` | no issues in 18 source files |
| Demo end to end | `python -m launchlab seed-demo` then `paper-run --book demo` | 300 synthetic tokens; 56 candidates, 244 rejections; 46 closed, 10 unsellable, 24 failed attempts; gross −6.69, fees 0.76, net −7.46 SOL; expectancy −26.6% per candidate (interval −38.3% … −13.4%); verdict "mechanics demo" |
| Dashboard | Playwright script against `serve`: tokens, token detail, replay, paper ledger, live book, claim tab, health, exact-mint search | all steps completed, 0 console errors |
| Refusal paths | curl: wrong Host, cross-origin POST, path traversal, live ingest in demo mode | 403, 403, 404, 503 |
| Live claim check | `audit CUfphq…pump --alert 2026-11-20T20:52:00Z --claimed-cap 58000 --claimed-multiple 24 --live` | alert-minute open $491,715; peak $2,035,864; best case 4.14×; claim not reproducible |
| Live ingest | `ingest CUfphq…pump --live` | on-chain launch time and creator read; "20 wallets bought 82.9% of supply in the creation slot"; co-signer groups 5/7/7; LP burned; holders unknown (public RPC refused) |
| Live collection loop | `watch --live --cycles 1 --max-new 1` | 17 launches discovered, 1 ingested, 18 signals recorded (all rejected), event log intact |

The Playwright script and the ad-hoc audit scripts lived in the session's temporary directory and are not
in the repository; the app's `audit` and `ingest` commands reproduce the audit numbers.

## Known gaps and blockers

| Gap | Effect | What would close it |
|---|---|---|
| The user's screenshot never reached the session | Audit used the user's transcription, later matched to the primary post | Re-attach if a visual check of the image itself is wanted |
| No immutable alert archive | Alert existence and timing are unverified | A public channel history or signed alert log from the author |
| No wallet or account behind the PnL | Claim 1 stays unverified | See CLAIMS_AUDIT.md claim 1 |
| Public RPC refuses holder queries | `ownership_concentration` is usually `unknown` live | Custom RPC in `.env`, or an indexer adapter |
| No creator-history source | `creator_history` is `unknown` live | Indexer adapter (Bitquery is the candidate; paid after a trial) |
| Busy curves outrun the 6,000 signatures read | Launch structure `unknown` for the hottest launches | WebSocket log subscription at launch time, or an indexer |
| Provider terms unread or unclear (GeckoTerminal, DexScreener caching) | Raw storage off by default; nothing redistributed | Read the terms before enabling storage or publishing derived data |
| `InitBoost` pool mechanic is observed, not documented | Pool pricing model rests on three on-chain observations | Official documentation or a wider sample |
| Live paper book is empty of candidates | Verdict `inconclusive` | Run `watch` continuously for at least 14 days |
| Work is committed locally only | The container is temporary | Push the branch (needs the owner's go-ahead; the brief said not to push) |

## Exact next steps

1. Decide whether to push the branch. Until then the work exists only in this container.
2. Review `launchlab/policy.py` and fix the decision and exit rules **before** collecting live data. Bump
   `RULESET` on any change.
3. Start collection: `python -m launchlab watch --live --interval 60 --max-new 2` and leave it running.
   Check progress in the dashboard's Paper ledger with the `live` book.
4. After 14 days and 200 resolved candidates, read the verdict. Evaluate the holdout (last 30% by time) once.
5. Add a holder/creator-history adapter if the unknown rate of those two checks is too high to be useful.
6. Re-run the three `audit` commands in a week to see whether provider candles were revised.
7. Add a WebSocket launch listener so the creation slot is read as it happens.

## Resume commands

```bash
cd solana-launch-lab
python -m launchlab status                 # what is in the local store
python -m launchlab serve                  # dashboard at http://127.0.0.1:8765/
python -m pytest && ruff check . && mypy   # all checks
python -m launchlab verify-log             # event-log integrity
```

Re-run the audit rows:

```bash
python -m launchlab audit CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump --alert 2026-11-20T20:52:00Z --claimed-cap 58000 --claimed-multiple 24 --live
python -m launchlab audit 2TngN4B7XaoGSKsYvttq5bFAdM4Z4xCSnuyRwGiFpump --alert 2026-11-21T04:39:00Z --claimed-cap 50000 --claimed-multiple 58 --live
python -m launchlab audit FJKt1LxbWBpTRt9BaDEB6Wr2qL5LZzjFF5sx8rXnpump --alert 2026-11-21T05:19:00Z --claimed-cap 75000 --claimed-multiple 50 --live
```

## Tools used and unavailable

| Tool | Status |
|---|---|
| Shell, file tools, Python 3.13, Node 22, uv, pytest, ruff, mypy | Available and used |
| Web search and page fetch | Available and used |
| Headless Chromium (Playwright) | Available; used for the dashboard smoke test and to render the audited site |
| Direct HTTPS to DexScreener, GeckoTerminal, Solana public RPC, arXiv, GitHub (public, read-only), x.com | Reachable |
| `sotwe.com` mirror | HTTP 403; not used, not bypassed |
| `xcancel.com`, X syndication endpoint | HTTP 451 and 429; not used |
| `solana.com` docs site | HTTP 429 to direct fetch; read through the docs' source repository instead |
| The user's screenshot | Not received |
| Frontend Design plugin | Not installed: not present in this environment and not needed for a static dashboard |
| Trading, wallet, signing or execution plugins | None installed, by design |
| Paid data APIs (Helius, Birdeye, Bitquery, Solscan, Dune) | Not used: keys required and several terms unsuitable; see DATA_SOURCES.md |
| One research sub-agent (post search) | Blocked by the environment's permission system; the search was done directly with plain fetches instead |

No package was installed into the application. Three development tools are pinned in `uv.lock`.
