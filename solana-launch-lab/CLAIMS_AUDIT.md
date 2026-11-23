# Claims audit — the QuantumOrb post by @Dan1ro0

Audit date: **2026-11-23** (all access times UTC). Auditor: this repository's research session.
Scope and method are in [RESEARCH.md](RESEARCH.md); data-source definitions are in [DATA_SOURCES.md](DATA_SOURCES.md).

> **Nothing here is financial advice, a buy/sell signal, or a forecast.** A claim marked "unverified" is not
> called false; it means no reproducible, time-stamped evidence for it was found.

## 0. What was audited, and what was not available

| Item | Status |
|---|---|
| Screenshot attached by the user | **Not received.** No image reached this session. The audit uses the user's transcription of the screenshot, which was then compared with the primary source below and matches it on every listed claim. |
| Original post (primary source) | **Found.** `https://x.com/Dan1ro0/status/2124255865645502610`, published **2026-11-21 21:37:19 UTC**. Text, timestamp and post ID were read from the server-rendered payload of `https://x.com/Dan1ro0` fetched 2026-11-23 04:13 UTC. The permalink page itself and the attached video were not loaded. |
| Secondary mirror (sotwe) | Blocked (HTTP 403). Not used, not bypassed. |
| Author | "Daniro" `@Dan1ro0`, account created 2017-09-10, verified since 2025-10-27, 10,422 followers. Bio links to `github.com/QuantumOrb`. The post says "I used … to build" and "I made the core scoring code open source", so the author presents as **the project's builder, not an independent reviewer**. |
| Engagement at access | 1,258 likes · 156 reposts · 96 replies · 10 quotes · 1,361 bookmarks. |

Things the post does **not** contain: any wallet address, exchange account, transaction signature, trade list,
starting capital, fee accounting, losing trades, the other 16 "passed" tokens, the mint addresses of the three
examples, or a statement that the author traded those three tokens.

## 1. Summary table

Confidence scale: **high** (reproduced from primary data) · **medium** · **low** · **unverified** (no evidence either way).

| # | Exact claim | Verdict | Confidence in verdict |
|---|---|---|---|
| 1 | "+$10,847.63 in 21 days" | **Unverified.** No account, wallet or trade history is linked anywhere. | unverified |
| 2 | "3,825 launches tracked" | **Unverified.** Self-reported; appears nowhere in the repo or on the site. | unverified |
| 3 | "82,540 holders analyzed" | **Unverified.** Same. | unverified |
| 4 | "185 wallet clusters detected" | **Unverified.** Same. The clustering code is in the closed part of the project. | unverified |
| 5 | "Only 19 tokens passed every check, each scoring 85+/100" | **Unverified, and inconsistent with the published rules** (no "85" threshold exists; the three examples breach a published hold rule). | medium |
| 6a | BartCoin launched Nov 20, 20:45 UTC | **Confirmed** (on-chain creation 20:45:13 UTC). | high |
| 6b | "RADAR alert at 20:52 ($58K cap)" | Alert existence/time **unverified**. The "$58K cap" is **contradicted** for 20:52: on-chain value ≈ **$497K**. | high (for the price) |
| 6c | "24x from the alert" | **Not reproducible from the stated alert time**: best case ≈ 4.1× before any cost. | high |
| 7a | PUNANI launched Nov 21, 04:26 UTC | **Confirmed** (04:26:25 UTC). | high |
| 7b | "RADAR alert at 04:39 ($50K cap)" | Alert **unverified**; cap **contradicted**: on-chain ≈ **$304K** at 04:39. | high (for the price) |
| 7c | "58x from the alert" | **Not reproducible**: best case ≈ 12.9× before any cost. | high |
| 8a | MAYA launched Nov 21, 05:07 UTC | **Confirmed** (05:07:34 UTC). | high |
| 8b | "RADAR alert at 05:19 ($75K cap)" | Alert **unverified**; cap **contradicted**: on-chain ≈ **$767K** at 05:19. | high (for the price) |
| 8c | "50x from the alert" | **Not reproducible**: best case ≈ 5.4× before any cost. | high |
| 9 | "self-learning trading algorithm" | **Contradicted by the project's own repository**: fixed rules, no ML, no trading code. | high |
| 10 | "core scoring code open source" | **Partly inaccurate**: the code is published but under an all-rights-reserved licence that forbids reuse; about a tenth of the code is public. | high |

"Best case" means: bought at the on-chain price in the first second of the stated alert minute and sold at
the single highest one-minute high that occurred afterwards, with zero fees, zero slippage and zero delay.
Nobody can trade that. It is an upper bound, not an estimate of achievable profit.

## 2. Context that changes how the three examples should be read

These facts were read directly from Solana transactions (public RPC, 2026-11-23 03:55–04:40 UTC).

1. **All three tokens were fully bundled launches using the same template.** In the creation slot itself,
   19 wallets that co-signed three transactions bought **793.1M tokens = 79.3% of total supply — the entire
   bonding curve — for about 85 SOL (≈ $5.7K)**. A twentieth co-signer bought another 3.6–5.1% from the new
   pool inside the migration transaction. After the first slot, 20 wallets held **82.9% (BartCoin), 82.9%
   (PUNANI), 84.4% (MAYA)** of supply. The bonding-curve phase lasted under one second.
2. **Per-wallet amounts are nearly identical across the three tokens** (e.g. 1.41M / 2.11M / 2.80M / 4.17M in
   the first transaction of both BartCoin and PUNANI). Wallets that co-sign one transaction are coordinated by
   construction. Across tokens, the first-funder addresses of the BartCoin and PUNANI wallets overlap, and all
   20 MAYA wallets were funded by one address 3 seconds before launch. This is a *probabilistic* indication
   that the launches share an operator or a launch service; it does not identify a person.
3. **Those wallets sold into the rise, including during the stated alert minute.** Decoded examples for
   BartCoin: one bundle wallet sold 1.417M tokens for 11.58 SOL at 20:52:17 and 1.743M for 13.95 SOL at
   20:52:51; another sold 1.635M for 13.13 SOL at 20:52:22. Each sale was followed seconds later by a SOL
   transfer out. **None of the 60 slot-0 wallets holds a meaningful balance today** (under 0.01M tokens in total
   per token).
4. **All three tokens are now near zero.** DexScreener, 2026-11-23 03:56 UTC: market cap **$1,444 / $1,853 /
   $1,630**, i.e. about −99.9% from peak and −99.6% to −99.8% from the on-chain alert-time value. 97.5% of
   BartCoin's supply is back in the pool.
5. **BartCoin had already collapsed before the post was published.** Its first hourly close below 10% of
   the alert-time value was 2026-11-21 10:00 UTC (≈ $1.6K), about 11.5 hours *before* the post advertised
   "24x from the alert". PUNANI and MAYA collapsed to ≈ $1.7K within about 3.5 and 5.5 hours *after* the post.
6. **The project's own published rule would hold these launches.** `rules/limits.js:16` in the public repo
   reads `slot0Max: 0.30 /* HELD if 30% or more of supply was bought in the launch slot */`. On-chain, 79.3%
   was bought in the launch slot. Whether the closed production system applied this rule is unknown.

What this does **not** establish: who controls the launch wallets; that the post's author is connected to
them; that the alerts were not sent; or that the author did or did not trade these tokens.

## 3. Claim-by-claim detail

### Claim 1 — "+$10,847.63 in 21 days"

| Field | Finding |
|---|---|
| Exact claim | "The result: +$10,847.63 in 21 days" |
| Original source | X post 2124255865645502610, published 2026-11-21 21:37:19 UTC; accessed 2026-11-23 04:13 UTC |
| Evidence found | None beyond the sentence itself. The post links only the GitHub repo. The repo and website contain no PnL, track record, wallet or trade list (repo audit, 2026-11-23). |
| Independent verification method | Search post text, author profile, repo, website for a wallet/exchange account; web search for the exact figure. |
| Contradictory or conflicting evidence | (a) The public code cannot trade: no signing, keys, RPC client or swap code. (b) The post calls the system a "trading algorithm"; the repo describes a scanner that outputs verdicts. (c) The site's rolling 24h counter showed **0 bot alerts** at 2026-11-23 ~03:57 UTC. (d) The project's public site is about 20 days old, so "21 days" equals the whole life of the product. None of these proves the figure false. |
| Confidence | **Unverified** |
| Evidence needed to settle | A wallet or account demonstrably controlled by the author (e.g. a signed message), its complete transaction history for the period, starting balance, deposits and withdrawals, realized vs unrealized PnL, open positions at period end, all fees and failed transactions, and the full list of signals including losers. |

Missing-evidence checklist for a verified PnL (Phase 3):

| Required evidence | Present? |
|---|---|
| Starting capital | No |
| Deposits and withdrawals | No |
| Realized vs unrealized PnL | No |
| Open positions at period end | No |
| Exact entries and exits | No |
| Fees, failed transactions, priority fees, price impact | No |
| All trades and signals including losers | No (3 of 19 "passed" tokens named; none of the non-passing alerts) |
| Link between an account/wallet and the author/system | No |

Three different things must not be conflated: (1) a token's later market-cap multiple — partly measurable,
see claims 6–8; (2) the profit of a hypothetical trader under a stated execution rule — computable only as a
model, see section 4; (3) a real, realized, independently verified PnL — **no evidence exists**.

### Claims 2–4 — "3,825 launches tracked", "82,540 holders analyzed", "185 wallet clusters detected"

| Field | Finding |
|---|---|
| Original source | Same post |
| Evidence found | None. The figures do not appear in the repo or on the site. The site shows only rolling 24-hour counters (at 2026-11-23 ~03:57 UTC: 8,478 launches, 5,047 held, 1,302 wallets read, 87 scans, 18 operators), which are not cumulative and do not match. |
| Verification method | Compare with repo/site; look for a public alert archive or dataset. |
| Conflicting evidence | 8,478 launches in one rolling day versus 3,825 "tracked" in 21 days are different definitions at best. Wallet-link detection is explicitly in the closed part (`rules/operators.js:4`), so "clusters detected" cannot be reproduced or error-checked. |
| Confidence | **Unverified** |
| Evidence needed | A dated, exported list of launches, holders and clusters with the definitions of "tracked", "analyzed" and "cluster", plus a labelled sample to estimate clustering error. |

### Claim 5 — "Only 19 tokens passed every check, each scoring 85+/100"

| Field | Finding |
|---|---|
| Evidence found | Three tokens are named; sixteen are not. No scores for any token are published. |
| Verification method | Read the published rules; compare the three named tokens' on-chain launch structure with those rules. |
| Conflicting evidence | (a) The open rules define bands at 80/60/40 (`rules/score.js:39`); there is no "85" threshold or "passed every check" state. (b) The published Guard rule holds any launch where ≥30% of supply was bought in the launch slot; the three named tokens had 79.3%. (c) On the live site one token was observed scoring 94, then 85, then "DANGER 70" within two hours, so a score is a moving reading, not a stable property. |
| Confidence | **Unverified** for the count; **medium** that the three examples are inconsistent with the published rules. |
| Evidence needed | The 19 mints with the timestamped score and inputs at the moment each "passed", and outcomes for all 19 under a fixed, pre-stated rule. |

### Claims 6–8 — the three token examples

Identity (each mint verified independently on DexScreener, GeckoTerminal and Solana RPC; a ticker is not an identifier):

| | BartCoin (`BTC`) | PunaniCoin (`PUNANI`) | Maya The Samoyed (`MAYA`) |
|---|---|---|---|
| Mint | `CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump` | `2TngN4B7XaoGSKsYvttq5bFAdM4Z4xCSnuyRwGiFpump` | `FJKt1LxbWBpTRt9BaDEB6Wr2qL5LZzjFF5sx8rXnpump` |
| Token program | Token-2022 | Token-2022 | Token-2022 |
| Creation (on-chain block time, UTC) | 2026-11-20 20:45:13, slot 471875967 | 2026-11-21 04:26:25, slot 472004485 | 2026-11-21 05:07:34, slot 472015921 |
| Bonding-curve account | `ACUSZ93r…tY41` | `8cDzEmxo…DK7t` | `2WA1EaQn…xRcS` |
| Bonding-curve phase | < 1 s (same slot) | < 1 s (same slot) | < 1 s (same slot) |
| Market after that | PumpSwap pool `5q1eZo7m…7aoJ` | PumpSwap pool `CnZHS2nm…4hWA` | PumpSwap pool `51edMriY…PCbo` |
| LP tokens | minted and burned in the migration tx | same | same |
| Claimed launch time | 20:45 ✔ | 04:26 ✔ | 05:07 ✔ |

Note the ticker of BartCoin is literally `BTC`. It is unrelated to Bitcoin.

Market-cap definition used throughout: **price × 1,000,000,000** (the fixed pump.fun supply; identical to
what DexScreener and GeckoTerminal report as FDV for these tokens, and DexScreener reports `marketCap` =
`fdv`). Because 83–84% of supply sat in 20 launch wallets, this number is a quotation, not an amount anyone
could realize. On-chain price = (pool WSOL balance + 17.5845 SOL) ÷ pool token balance; the 17.5845 SOL term
is a constant moved out of the pool by the migration's `InitBoost` instruction and still counted in pricing
(checked against DexScreener's live price: (2.34 + 17.58) ÷ 971.82M = 2.05e-8 SOL vs reported 2.062e-8).
SOL/USD at each alert minute taken from GeckoTerminal (67.58, 65.74, 65.90).

Market cap at the stated alert time:

| | BartCoin | PUNANI | MAYA |
|---|---|---|---|
| Claimed alert time (UTC) | Nov 20 20:52 | Nov 21 04:39 | Nov 21 05:19 |
| Claimed cap | ~$58K | ~$50K | ~$75K |
| **On-chain cap, first second of alert minute** | **$497,342** | **$303,721** | **$766,853** |
| On-chain cap +30 s / +59 s | $538K / $563K | $337K / $351K | $829K / $888K |
| GeckoTerminal alert-minute candle (O / H / L / C) | $492K / $577K / $442K / $555K | $306K / $372K / $262K / $348K | $769K / $916K / $727K / $901K |
| On-chain ÷ claimed | **8.6×** | **6.1×** | **10.2×** |
| On-chain cap 3–10 s after launch | ≈ $291K | ≈ $238K | ≈ $247K |
| Cap right after the migration tx (slot 0) | ≈ $40.8K | ≈ $39.6K | ≈ $47.9K |

Two independent sources (direct pool balances from Solana blocks, and GeckoTerminal's candles) agree with
each other within a few percent and both disagree with the post by 6–10×. A cap of $50–75K existed only for
roughly the first one or two seconds after launch, before the first outside buys. The most likely reading is
that the tool's "alert cap" is a value captured at detection in the first seconds, while the stated alert
time is 7–13 minutes later; the post then divides a later high by that early value. This reading is an
inference. It is equally consistent with a stale price feed. Either way the multiple was **not available to
someone acting on an alert at the stated time**.

Multiples:

| | BartCoin | PUNANI | MAYA |
|---|---|---|---|
| Claimed multiple | 24× | 58× | 50× |
| Peak one-minute high after alert (GeckoTerminal) | $2.04M at Nov 20 21:40 | $3.91M at Nov 21 19:02 | $4.13M at Nov 21 16:52 |
| Peak ÷ **on-chain alert-time cap** | **4.1×** | **12.9×** | **5.4×** |
| Peak ÷ alert-minute close | 3.7× | 11.2× | 4.6× |
| Peak ÷ entry one minute later | 3.5× | 9.9× | 3.9× |
| Peak ÷ *claimed* cap | 35× | 78× | 55× |
| Minutes (of first ~1,000) closing ≥ 10× alert-minute close | 0 | 1 | 0 |
| Minutes closing ≥ 20× | 0 | 0 | 0 |
| Cap when the post was published (Nov 21 21:37) | ≈ $1.5K | ≈ $0.7–1.0M, falling | ≈ $0.9–1.6M, falling |
| Cap on 2026-11-23 03:56 (DexScreener) | $1,444 | $1,853 | $1,630 |

| Field | Finding (applies to 6b/6c, 7b/7c, 8b/8c) |
|---|---|
| Evidence found | Launch times confirmed on-chain. No public, timestamped alert archive was found, so the existence and time of each alert are unverified. |
| Independent verification method | (1) `getSignaturesForAddress` + `getTransaction` on each bonding-curve account for creation, buyers and migration; (2) `getBlock` at the alert second for pool balances; (3) GeckoTerminal minute and hour OHLCV for both pools; (4) DexScreener current state. Scripts and raw responses were kept in the session scratchpad; the method is re-runnable with `python -m launchlab audit` (see README). |
| Contradictory evidence | Alert-time cap is 6–10× the claimed cap in both independent sources. Multiples from the alert time are 4–13× at the theoretical best, not 24–58×. |
| Explanation of discrepancy with earlier third-party pages | Earlier leads suggested a timing/price mismatch for PUNANI and MAYA. Rechecked: the mismatch is real and also applies to BartCoin. It is not caused by time zones (launch times match to the minute), token identity (exact mints), pool transition (the PumpSwap pool exists from slot 0), or FDV-vs-market-cap definitions (identical here). |
| Confidence | **High** that launch times are right; **high** that the claimed caps and multiples do not describe the stated alert times; alert delivery itself **unverified**. |
| Evidence needed | The raw alert messages with server timestamps and the price snapshot each used, from an archive the author cannot edit after the fact (e.g. a public Telegram channel's message history). |

### Claims 9–10 — "self-learning trading algorithm", "core scoring code open source"

| Field | Finding |
|---|---|
| Evidence found | Repo at commit `cb61b091` (2026-11-05). `README.md:67`: "a fixed, written set of rules, not a black box". No ML code or model files. No signing, key handling, RPC/HTTP client, swap or bundle-submission code. `README.md:178`: "About a tenth of QuantumOrb's code is open here". Closed parts listed at `README.md:219-221`, including "finding the links between wallets". |
| Licence | `LICENSE:2` "All rights reserved". `LICENSE:10-12`: "You may not … copy, modify, merge, publish, distribute, sublicense or sell any part of this repository, or use the code in it in another product or service". This is source-available for inspection, not open source. |
| Tests | Unit tests on synthetic fixtures (`README.md:276-277`: "every token, wallet and figure on them is made up"). They show the rules compute what the rules say. They contain no outcome labels, backtest, error rates or PnL. |
| Confidence | **High** |

## 4. Hypothetical trader versus the claim (model, not evidence of real profit)

Constant-product arithmetic on the on-chain BartCoin pool state shows why a quoted multiple overstates what
a trade can capture even with perfect timing. Effective reserves at 20:52:00 were 362.9 SOL and 49.31M
tokens. At the start of the peak minute (21:40:00) they were 706.5 SOL and 25.99M tokens.

| Position bought at 20:52:00 | Tokens received (no fee) | SOL back if sold alone at 21:40:00 | Realized multiple | Quoted multiple at that instant |
|---|---|---|---|---|
| 1 SOL (≈ $68) | 135.5K | 3.66 SOL | 3.66× | 3.69× |
| 15 SOL (≈ $1.0K) | 1.957M | 49.5 SOL | 3.30× | 3.69× |
| 75 SOL (≈ $5.1K) | 8.445M | 173.3 SOL | 2.31× | 3.69× |

These rows assume no fees, no failed transactions, instant execution, nobody else selling first, and exit at
the best minute — which could only be identified afterwards. The paper-trading engine in this repository
exists to replace that hindsight with rules fixed in advance.

## 5. Commercial context and incentives (Phase 2 summary)

| Question | Finding |
|---|---|
| Public repo contents | 78 files, 21 commits, one author, first commit 2026-10-22. Deterministic rule calculator (`rules/`), chain decoders (`chain/`), pool selection (`market/`), bot message formatting (`bot/`), tests, synthetic examples, docs. No network code. |
| Closed | Wallet-link discovery, launch stream, Radar, site and API, bot commands, alert loops, database. |
| Scoring | Fixed weighted rules: biggest operator 35, fresh wallets 25, received-not-bought 20, unsold snipers 10, top-20 share 10. No machine learning. |
| Trade execution | None in the public code. |
| Own token | Yes. `README.md:249-252` gives mint `EiN69j8KVE5uYKheVkeVwptEVwRP5JtDhJDMGm1ppump` (symbol QORB on DexScreener). Verified 2026-11-23 04:15 UTC: FDV **$1,383**, liquidity $1,495, 24h volume **$1.81**, pair created 2026-11-04. |
| Paid plans | "Pro Subscription" is on the roadmap as planned (`README.md:173`: "No scan limits, and a live list of fresh tokens scoring 90+ in the bot"); the bot is currently free. |
| Incentive | The author builds the product, the product has a token and a planned subscription, and the account's other recent posts follow one template of large third-party PnL headlines. Readers should treat the post as marketing by an interested party. |
| Disclaimers in repo | "Nothing here is financial advice" (`LICENSE:20`); example data declared made up. |

"The project exists" is established. "Its PnL is verified" is not.

## 6. Limits of this audit

- Solana public RPC and two free market-data APIs were the only data sources; no paid indexer was used.
- Wallet funding links were read from each wallet's first transaction only; deeper tracing was not done.
- The total SOL extracted by the launch wallets was not summed (thousands of transactions).
- The post's video, its replies, and the Telegram bot were not examined.
- The closed production system was not observable; statements about "the published rules" refer to the
  public repository only.
- Provider data can be revised. Every number above carries its access time; re-running the audit later may
  give slightly different candle values.
