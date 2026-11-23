# Data sources — APIs, terms, limits, definitions, gaps

All facts were read on **2026-11-23 (UTC)**. Labels: **DOC** = read in an official source that day ·
**CHAIN** = observed on Solana mainnet that day · **DERIVED** = computed from DOC/CHAIN facts ·
**UNCLEAR** = could not be confirmed. Longer working notes with per-fact URLs are in
[`research-notes/docs_providers.md`](research-notes/docs_providers.md).

This project is **read-only**. It never signs or submits a transaction and never needs a wallet or key.

## 1. Which source the app uses for what

| Need | Adapter | Key needed | Used by default |
|---|---|---|---|
| Current price, FDV/market cap, liquidity, volume, pair creation time for an exact mint | `dexscreener` | No | Yes (live mode) |
| Pools of a mint, OHLCV history, newest pools (launch discovery) | `geckoterminal` | No | Yes (live mode) |
| Creation transaction, launch-slot buyers, pool balances, supply, largest accounts | `solana_rpc` | No (public endpoint) or your own endpoint via `SOLANA_RPC_URL` | Yes (live mode) |
| Offline demo | `synthetic` | No | Yes (demo mode) |

Not used: the pump.fun website or its undocumented frontend API. Pump.fun's terms §21(h) prohibit using
"web crawlers, bots, spiders or other automatic devices … to access, obtain, copy or monitor any part of the
Pump Platform" except as §6.1 permits (DOC, `solana.pump.fun/docs/terms-and-conditions`). On-chain data read
through a Solana RPC node is not the Pump Platform.

## 2. Pump.fun mechanics (official docs + chain)

Sources: `https://solana.pump.fun/docs/bonding-curve`, `/docs/fees` (page dated 16 Nov 2026), `/docs/mayhem-mode`,
`github.com/pump-fun/pump-public-docs` (commit `bc35796`), npm `@pump-fun/pump-sdk` 4.1.0.

| Fact | Value | Label |
|---|---|---|
| Bonding-curve program | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | DOC |
| PumpSwap AMM program | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` | DOC |
| Fee program | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` | DOC |
| Curve account address | PDA of seeds `["bonding-curve", mint]` | DOC |
| Total supply / decimals | 1,000,000,000 / 6 (Mayhem-mode coins: 2,000,000,000) | DOC + CHAIN |
| Initial virtual reserves | 1,073,000,000 tokens and 30 SOL | DOC + CHAIN |
| Tokens sold on the curve | 793,100,000 (79.31% of supply) | DOC + CHAIN |
| Tokens migrated to the pool | 206,900,000 | CHAIN |
| Buy on curve (tokens out for `q` quote in) | `q · y / (x + q)`, with `x` virtual quote, `y` virtual tokens | DOC |
| Sell on curve (quote out for `a` tokens in) | `a · x / (y + a)` | DOC |
| Curve market cap | `virtualQuote · totalSupply / virtualTokens` | DOC |
| Initial market cap | 30 / 1.073e9 × 1e9 ≈ 27.96 SOL | DERIVED |
| Completion ("graduation") | `complete` when `real_token_reserves == 0`; anyone may call `migrate` to PumpSwap; LP tokens are burnt; 0.015 SOL migration fee | DOC |
| SOL raised at completion / market cap then | ≈ 85.005 SOL / ≈ 410.9 SOL | DERIVED (matches CHAIN) |
| `InitBoost` at migration | exactly 17.584505288 WSOL moves from the new pool's quote account to a per-pool vault, and pricing still behaves as if it were in the pool | CHAIN (three pools); **not found in official docs**, interpretation is ours |
| Token program | coins made with `create_v2` are Token-2022; older coins are SPL Token | DOC |
| Mint / freeze authority | null on sampled mints | CHAIN (not documented) |
| Transaction version | v1 transactions are live. `maxSupportedTransactionVersion: 0` fails with error −32015; use `1` | CHAIN |
| Slot time | ≈ 0.218 s per slot (measured across the audited launches) | CHAIN |
| Official data API | none documented | DOC |

Fees (DOC, `/docs/fees`, "may change … by updating this page"):

| Venue | Fee per side |
|---|---|
| Bonding curve | 0.95% protocol + 0.30% creator = **1.25%** (95/30 bps also seen on-chain) |
| PumpSwap canonical pool, market cap < 420 SOL | 1.25% |
| 420–1,470 SOL | 1.20% |
| 1,470–2,460 / 2,460–3,440 / 3,440–4,420 SOL | 1.15% / 1.10% / 1.05% |
| 4,420–9,820 SOL | 1.00% |
| 9,820–14,740 … 49,120–54,030 SOL | 0.95% falling by 0.05% per tier to 0.55% |
| 54,030–98,240 SOL | 0.525% falling by 0.025% per tier to 0.325% |
| ≥ 98,240 SOL | 0.30% |
| Non-canonical PumpSwap pool | 0.30% |
| Extra "Platform Fee" via the pump.fun web/mobile app only (from 17 Oct 2026) | 0.45% / 0.40% |

History: before 1 Sep 2025 the curve fee was 1% and the pool fee 0.25%; creator fees began 12–13 May 2025.
Any backtest that spans those dates must use the schedule in force at each trade.

The app's default cost model implements the tier table above in `launchlab/costs.py` and lets every number
be overridden in configuration.

## 3. Solana JSON-RPC

Sources: solana.com RPC docs (via `github.com/solana-foundation/solana-com` commit `82d49aed`), `docs.anza.xyz`.

| Fact | Value | Label |
|---|---|---|
| Public mainnet endpoint | `https://api.mainnet-beta.solana.com` (docs now also list `api.mainnet.solana.com`) | DOC |
| Public rate limits | 100 requests / 10 s per IP; 40 / 10 s per method; 40 concurrent connections; 100 MB / 30 s | DOC |
| Intended use | "not intended for production applications" | DOC |
| `getSignaturesForAddress` | newest first; `limit` 1–1,000; `before` / `until` cursors; no time filter | DOC |
| `getMultipleAccounts` | ≤ 100 accounts | DOC |
| `getTokenLargestAccounts` | returns the 20 largest accounts only; **returned HTTP 429 with method limit 0 on the public endpoint** | DOC + CHAIN |
| `getProgramAccounts` | ≤ 4 filters, no pagination; heavily limited on the public endpoint | DOC + CHAIN |
| History retention | nodes prune the ledger (`--limit-ledger-size`); older data needs an archival provider | DOC |
| Base fee | 5,000 lamports per signature | DOC |
| Priority fee | `ceil(compute-unit price × compute-unit limit / 1e6)` lamports | DOC |
| Jito minimum tip | 1,000 lamports | DOC (`docs.jito.wtf`) |
| Token-account rent | live value 1,488,440 lamports (SPL) / 1,513,840 (Token-2022); older docs say 2,039,280 / 2,074,080. Query at runtime. | CHAIN vs DOC conflict |

Consequences for this app:

- **Holder lists are incomplete on the public endpoint.** There is no "holders of mint" method. A full list
  needs `getProgramAccounts` on the token program with a `memcmp` on the mint (Token-2022 accounts are 170
  bytes, so the classic `dataSize: 165` filter misses current pump coins) or a paid indexer. The app reports
  ownership concentration as **unknown** when it cannot read it, and labels a top-20 reading as partial.
- **Busy pools cannot be paged back to launch cheaply.** One audited pool had more than 150,000 signatures
  in 42 hours. The app reads a specific moment with `getBlock` at the computed slot instead.
- Methods allowed in `launchlab/providers/solana_rpc.py` are an explicit read-only allowlist. `sendTransaction`,
  `simulateTransaction`, `requestAirdrop` and every other write or signing path are absent and a test asserts it.

## 4. DEX Screener

Source: `https://docs.dexscreener.com/api/reference` and its API terms.

| Fact | Value | Label |
|---|---|---|
| Key | none | DOC |
| Rate limits | 300 requests/min for pairs, search and tokens (≤ 30 addresses per call); 60/min for profiles and boosts | DOC |
| Historical candles | no endpoint | DOC |
| Field definitions (`marketCap`, `fdv`, `liquidity.usd`, `pairCreatedAt`) | **not defined in the docs** | UNCLEAR |
| Observed behaviour | bonding-curve pairs have `dexId: pumpfun` and `liquidity: null`; graduated pairs `pumpswap`. For the audited tokens `marketCap == fdv`. `liquidity.usd` = USD value of base side + quote side as held in the pool accounts, which for PumpSwap understates the pricing reserve by the `InitBoost` amount. `pairCreatedAt` equalled the token creation time, not a later pool time. | CHAIN |
| Terms | usable "for both non-commercial and commercial purposes"; may not make the API services "available for third parties" | DOC |
| Caching / local storage / attribution | no clause | UNCLEAR |

App policy: store parsed fields with source and timestamp; raw response storage **off by default**
(`STORE_RAW_DEXSCREENER=0`); never redistribute.

## 5. GeckoTerminal

Source: `https://api.geckoterminal.com/docs/v2/swagger.json`, `docs.coingecko.com`.

| Fact | Value | Label |
|---|---|---|
| Key | none for the public host | DOC |
| Rate limit | "approximately 10 calls/minute"; responses cached about 1 minute | DOC. We hit HTTP 429 at one call per 2.5 s. |
| OHLCV | minute (1, 5, 15), hour (1, 4, 12), day (1); `limit` ≤ 1,000; `before_timestamp`; up to 6 months per call | DOC |
| Trades | last 300 trades within 24 h | DOC |
| New pools | `/networks/solana/new_pools` lists newest pools including dex `pump-fun` (the pool address is the bonding-curve account) | DOC + CHAIN |
| Market cap | `market_cap_usd` is `null` unless verified; `fdv_usd` = price × total supply | DOC + CHAIN |
| Terms / attribution | pages returned a bot challenge and were **not read** | UNCLEAR |

App policy: minimum 6.5 s between calls, exponential backoff on 429, raw storage **off by default**
(`STORE_RAW_GECKOTERMINAL=0`). Read the provider's terms before enabling it or publishing anything derived.

## 6. Providers evaluated but not integrated

| Provider | Key | Free tier | Terms note | Why not integrated in the MVP |
|---|---|---|---|---|
| Helius | yes | 1M credits/month, 10 req/s | terms bar use "in any personal, household, or familial capacity" | key required; licence unsuited to personal research as written |
| Birdeye | yes | 30,000 compute units/month, 1 req/s | §10.2 forbids "copy, scrape, extract, download, store" | storage prohibited |
| Bitquery | yes | 7-day trial, then paid | data usable "for any lawful commercial or non-commercial purpose" | no lasting free tier; good candidate for full launch history later |
| Jupiter Price v3 | no (0.5 req/s) | — | storage unclear | many new tokens unpriced |
| Solscan | yes | Free/Lite "Personal and Research Use only" | attribution on publication | key required |
| SolanaFM | unclear | 10 req/s stated | terms not found | unclear |
| Dune | yes | no API on the free tier | terms unread | no free API |

Adding one later means writing a class with the `Provider` interface in `launchlab/providers/base.py`; nothing
else changes.

## 7. Data definitions used by the app

| Term | Definition in this project |
|---|---|
| `price_usd` | provider-reported USD price of one whole token at `observed_at` |
| `fdv_usd` | `price_usd × total_supply`. For pump.fun coins total supply is 1e9. Always labelled FDV. |
| `market_cap_usd` | only what a provider explicitly reports as market cap; stored with `market_cap_definition` naming the provider's field. Never silently equated with FDV. |
| `curve_market_cap` | `virtualQuote × supply / virtualTokens` while the token is on the bonding curve |
| `liquidity_usd` | provider-reported; for PumpSwap also `quote_reserve_effective` when pool balances were read on-chain |
| `observed_at` | the time the data describes (candle time, block time, or fetch time for "current" endpoints) |
| `ingested_at` | wall-clock time this app stored it |
| `stale` | `ingested_at − observed_at` exceeds the provider's freshness threshold (config) |
| `synthetic` | generated by the demo generator; never mixed into live results |
| `conflict` | two providers disagree on the same field at about the same time by more than a configured tolerance |

## 8. Known gaps

- No complete holder list without a custom RPC or indexer; top-20 at best.
- No creator launch history without an indexer. The `creator_history` check is **unknown** in live mode.
- No full trade tape. Fills are modelled from pool reserves or candles, never from a matched historical trade.
- GeckoTerminal minute candles do not reveal intra-minute order, so a simulated fill inside a minute is
  uncertain by that candle's high–low range. The simulator records this range as fill uncertainty.
- SOL/USD comes from the same providers as token prices; no independent oracle is used.
- Public-RPC history can be pruned. Old launches may be unreadable later.
- Provider numbers can be revised after the fact. Stored observations keep their fetch time for that reason.
