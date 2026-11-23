# Primary-source notes: Pump.fun, Solana RPC, market-data providers, execution costs

Scope: READ-ONLY public-data research tool (no wallets, no signing, no trading).
All sources accessed **2026-11-23** unless stated. Raw copies of everything read are under
`/tmp/claude-0/-home-user-claude-skills/f0c43923-e51b-5ffb-bff6-ddef9f7ca9b2/scratchpad/research/raw/`.

Provenance labels used in the "confidence" column:

| label | meaning |
|---|---|
| DOC | Read in official documentation / official repo / official SDK source this session |
| CHAIN | Observed directly this session on mainnet (public RPC) or on a provider's live API. Primary, but a point-in-time observation, not a documented guarantee |
| DERIVED | Arithmetic from DOC/CHAIN constants (formula shown) |
| MEMORY | From model memory, NOT confirmed in an official source this session |
| NOT FOUND | Looked for it in the official source, it is not stated there |

Sources that could not be read (blocked): `https://solana.com/docs/*` (Vercel checkpoint, HTTP 429 — read the same
content from the docs source repo `github.com/solana-foundation/solana-com` @ `82d49aed`, 2026-11-20 instead);
`https://www.geckoterminal.com/dex-api` (403 Cloudflare challenge, curl + WebFetch + headless Chromium);
`https://www.coingecko.com/en/api_terms` (403); `https://dune.com/terms` (403).

---

## A. Pump.fun

Sources:
- S1 `https://solana.pump.fun/docs` (index), `/docs/bonding-curve`, `/docs/fees` ("Last Updated: 16 November 2026"),
  `/docs/create-coin`, `/docs/mayhem-mode` ("Last Updated: 12 November 2025"), `/docs/terms-and-conditions`
  ("Last Updated: 16 November 2026"), `/docs/custom-pairs`
- S2 `https://github.com/pump-fun/pump-public-docs` @ commit `bc35796` (2026-11-21): `README.md`, `docs/*.md`,
  `docs/instructions/*.md`, `idl/pump.json`, `idl/pump_amm.json`, `idl/pump_fees.json`
- S3 npm `@pump-fun/pump-sdk@4.1.0` ("Official Pump program SDK", MIT), files `src/bondingCurve.ts`, `src/fees.ts`
- S4 mainnet via `https://api.mainnet-beta.solana.com` (slot ~472,800,000, node `solana-core 4.4.0`)

### A1. Program IDs and fixed addresses

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Bonding-curve ("Pump") program | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` (mainnet + devnet) | S2 `docs/PUMP_PROGRAM_README.md`; `idl/pump.json` `address` | 2026-11-23 | DOC |
| PumpSwap AMM ("pump_amm") program | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` | S2 `docs/PUMP_SWAP_README.md`; `idl/pump_amm.json` | 2026-11-23 | DOC |
| Fee ("pump_fees") program | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` | S2 `idl/pump_fees.json` `address`; seen invoked on-chain (`GetFeesWithQuoteMint`) | 2026-11-23 | DOC + CHAIN |
| Mayhem program | `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e` | S2 `docs/instructions/COIN_CREATION.md`; S1 `/docs/mayhem-mode` | 2026-11-23 | DOC |
| Pump `Global` account | `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf` (PDA `["global"]`) | S2 `PUMP_PROGRAM_README.md` | 2026-11-23 | DOC |
| PumpSwap `GlobalConfig` | `ADyA8hdefvWN2dbGGWFotbzWxrAvLW83WG6QCVXvJKqw` (PDA `["global_config"]`) | S2 `PUMP_SWAP_README.md` | 2026-11-23 | DOC |
| Fee config account | `8Wf5TiAheLUqBrKXeYg2JtAFFMWtKdG2BSFgqUcPVwTt` (pump_fees PDA `["fee_config", pump_program_id]`) | S2 `docs/instructions/TRADE_V3.md` | 2026-11-23 | DOC |
| Bonding-curve PDA | seeds `["bonding-curve", mint]` under the Pump program | S2 `PUMP_PROGRAM_README.md` | 2026-11-23 | DOC |
| Mint-authority PDA | seeds `["mint-authority"]`; address `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` | seeds: S2 `COIN_CREATION.md`. Address: recalled from memory, then **verified on-chain**: `getSignaturesForAddress` on it returns only txs containing `Instruction: CreateV2` | 2026-11-23 | DOC (seeds) + CHAIN (address) |
| PumpSwap pool PDA | `["pool", index, creator, baseMint, quoteMint]`; pools created by Pump `migrate` use index 0 ("canonical pool", creator = Pump `pool-authority` PDA of the mint) | S2 `PUMP_SWAP_README.md`, `FEE_PROGRAM_README.md` | 2026-11-23 | DOC |
| Token programs | SPL Token `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`, Token-2022 `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`, ATA `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` | S2 `COIN_CREATION.md`, `idl/pump.json` | 2026-11-23 | DOC |
| Protocol fee recipients | 8 normal + 8 reserved (mayhem) + 8 buyback addresses listed in `docs/FEE_RECIPIENTS.md`. **Rotation:** 8 new protocol fee recipients (list in `README.md`/`FEE_RECIPIENT_ROTATION.md`), old ones stop working after **November 25 (2026)** | S2 `FEE_RECIPIENTS.md`, `FEE_RECIPIENT_ROTATION.md` | 2026-11-23 | DOC |

### A2. Bonding-curve account layout (`BondingCurve`, Anchor discriminator `[23,183,248,55,96,216,172,96]`)

Field order from `idl/pump.json` (S2). Older accounts are shorter: "read the missing trailing fields as `0` / `false` /
`Pubkey::default()`" (`PUMP_PROGRAM_README.md`). SDK README: `BONDING_CURVE_SIZE` 166 bytes for the current layout.

| # | field | type | note | confidence |
|---|---|---|---|---|
| 1 | `virtual_token_reserves` | u64 | | DOC |
| 2 | `virtual_quote_reserves` | u64 | renamed from `virtual_sol_reserves` | DOC |
| 3 | `real_token_reserves` | u64 | tokens still purchasable on the curve | DOC |
| 4 | `real_quote_reserves` | u64 | renamed from `real_sol_reserves`; lamports for SOL coins | DOC |
| 5 | `token_total_supply` | u64 | | DOC |
| 6 | `complete` | bool | set `true` at the end of a buy when `real_token_reserves == 0` | DOC |
| 7 | `creator` | pubkey | where creator fees accrue (added May 2025) | DOC |
| 8 | `is_mayhem_mode` | bool | | DOC |
| 9 | `is_cashback_coin` | bool | cashback deprecated; no new cashback coins | DOC |
| 10 | `quote_mint` | pubkey | `Pubkey::default()` (all zeros) for SOL-paired coins | DOC |
| 11 | `creator_fee_bps` | u64 | custom-pair coins only; 0 = standard schedule | DOC |
| 12 | `can_edit_creator_fee` | bool | reserved, always false | DOC |
| 13 | `is_holder_reward` | bool | creator fee routed to holders | DOC |
| 14 | `creator_fee` | u64 | un-swept creator fee kept on the curve (v3 trades) | DOC |
| 15 | `protocol_fees` | u64 | un-swept protocol fee kept on the curve (v3 trades) | DOC |
| 16 | `depth` | u8 | 0 for SOL/USDC/listed quotes; >0 when quoted in another pump coin | DOC |
| 17 | `initial_virtual_quote_reserves` | u64 | | DOC |
| 18 | `post_complete_base_out` | u64 | pool-part of the completing v3 buy ("synthetic migration") | DOC |
| 19 | `post_complete_quote_in` | u64 | | DOC |

Migrated curve test used by the official SDK: `real_quote_reserves == virtual_quote_reserves == real_token_reserves ==
virtual_token_reserves == 0` (`isBondingCurveMigrated`, S3).

### A3. Initial constants

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| `initial_virtual_token_reserves` | 1,073,000,000,000,000 base units = 1,073,000,000 tokens | S2 `PUMP_PROGRAM_README.md`; S4 `getAccountInfo(Global)` decoded at slot 472,800,065; also in 3 live `CreateEvent`s | 2026-11-23 | DOC + CHAIN |
| `initial_virtual_sol_reserves` | 30,000,000,000 lamports = 30 SOL | same | 2026-11-23 | DOC + CHAIN |
| `initial_real_token_reserves` (tokens sold on the curve) | 793,100,000,000,000 = 793,100,000 tokens | same | 2026-11-23 | DOC + CHAIN |
| `token_total_supply` | 1,000,000,000,000,000 = 1,000,000,000 tokens | same | 2026-11-23 | DOC + CHAIN |
| Decimals | 6 | S2 `COIN_CREATION.md` ("initialized with `decimals = 6`"); S4 parsed mints | 2026-11-23 | DOC + CHAIN |
| Tokens that go to the PumpSwap pool at migration | 206,900,000 (= supply − tokens sold on curve) | S3 comment "the migration deposit, `tokenTotalSupply - initialRealTokenReserves`" | 2026-11-23 | DOC + DERIVED |
| Initial `real_sol_reserves` | 0 | S2 `PUMP_PROGRAM_README.md` | 2026-11-23 | DOC |
| USDC-paired coins: `Global.initial_virtual_quote_reserves` | 4,292,000,000 = 4,292 USDC (6 dp). Whitelisted stable quote mint = USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | S4 Global decode; S3 `fees.ts` `STABLE_QUOTE_MINTS` | 2026-11-23 | CHAIN + DOC |
| Mayhem Mode supply | "the Agent will mint 1,000,000,000 additional tokens (2,000,000,000 total token supply)"; unsold agent tokens burned after 24 h; "starting market cap and the initial amount of liquidity is exactly the same" | S1 `/docs/mayhem-mode`; S4: mayhem mint `9nQCcW…pump` supply = 2,000,000,000,000,000 | 2026-11-23 | DOC + CHAIN |
| `Global.pool_migration_fee` | 15,000,001 lamports | S2 README JSON; S4 decode | 2026-11-23 | DOC + CHAIN |
| `Global` fallback fees (used only if no FeeConfig) | `fee_basis_points` = 95, `creator_fee_basis_points` = 5 on-chain today (README JSON snapshot shows older 100 / 0) | S4 decode vs S2 README | 2026-11-23 | CHAIN |
| Other live `Global` flags | `create_v2_enabled`=1, `mayhem_mode_enabled`=1, `buyback_basis_points`=5000, `creator_fee_configurable`=1, `max_configurable_creator_fee_bps`=100, `is_holder_reward_enabled`=1, `max_curve_depth`=5 | S4 decode (layout from `idl/pump.json`) | 2026-11-23 | CHAIN |
| Derived: initial price | 30 / 1,073,000,000 = 2.7959e-8 SOL per token | formula A4 | 2026-11-23 | DERIVED |
| Derived: initial market cap | 30e9 × 1e15 / 1.073e15 = 27.959 SOL | formula A5 | 2026-11-23 | DERIVED |
| Derived: quote needed to empty the curve (pre-fee) | 793.1e12 × 30e9 / 279.9e12 + 1 = 85,005,359,057 lamports ≈ **85.005 SOL** (≈ 86.07 SOL incl. 1.25% fee) | formula A4 | 2026-11-23 | DERIVED |
| Derived: curve state at completion | virtual SOL 115.005, virtual tokens 279,900,000, price 4.1088e-7 SOL, **market cap ≈ 410.88 SOL** | formulas A4/A5 | 2026-11-23 | DERIVED |
| Derived: pool at migration (SOL coin, no synthetic leg) | 206,900,000 tokens / (85.005 − 0.015) = 84.990 SOL → price 4.1078e-7 SOL | S2 `SYNTHETIC_MIGRATION.md` pool-to-be formula | 2026-11-23 | DERIVED |
| Derived: USDC curve | initial mcap exactly 4,000 USDC; raise ≈ 12,161 USDC; mcap at completion ≈ 58,783 USDC | same formulas with 4,292 USDC | 2026-11-23 | DERIVED |

### A4. Pricing formula (official SDK source, S3 `src/bondingCurve.ts`; S2: "based on Uniswap V2 and uses synthetic x and y reserves")

All integer math (BN), `x` = `virtual_quote_reserves`, `y` = `virtual_token_reserves`.

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Buy, exact tokens out `a` (pre-fee quote cost) | `cost = a * x / (y - a) + 1` where `a = min(amount, real_token_reserves)` | S3 `getBuySolAmountFromTokenAmountQuote` | 2026-11-23 | DOC |
| Buy, exact quote in `q` (net of fee) | `tokens = q * y / (x + q)`, capped at `real_token_reserves` | S3 `getBuyTokenAmountFromSolAmountQuote` | 2026-11-23 | DOC |
| Net input from a gross budget | `q = (budget - 1) * 10000 / (10000 + protocolFeeBps + creatorFeeBps)` | S3 `getBuyTokenAmountFromSolAmount` | 2026-11-23 | DOC |
| Sell `a` tokens (gross quote out) | `out = a * x / (y + a)`; seller receives `out - fee(out)` | S3 `getSellSolAmountFromTokenAmountQuote` | 2026-11-23 | DOC |
| Fee amount | `fee(amount, bps) = ceil(amount * bps / 10000)`, charged separately for protocol and creator bps; buyer pays `cost + fees`, seller receives `out − fees` | S3 `fees.ts` `fee`, `getFee` | 2026-11-23 | DOC |
| Reserve updates | buy: virtual & real quote reserves +cost, virtual & real token reserves −tokens; sell is the reverse | S2 `PUMP_PROGRAM_README.md` | 2026-11-23 | DOC |
| Completing buy with v3 instructions ("synthetic migration", since Oct 2026) | curve part at curve price, then remainder priced on the pool-to-be: `pool_base = curve_token_balance − remaining`, `pool_quote = real_quote_reserves + curve_quote − pool_migration_fee` (SOL coins); `quote_in = ceil(pool_quote*out/(pool_base−out))`. Both parts pay the bonding-curve fee schedule. Not for mayhem coins | S2 `docs/SYNTHETIC_MIGRATION.md` | 2026-11-23 | DOC |
| PumpSwap quoting | constant product on base vault balance vs **effective quote reserves** = `pool_quote_token_account.amount + Pool::virtual_quote_reserves` (i128, may be negative since 30 Sep 2026) | S2 `PUMP_SWAP_README.md`, `NEGATIVE_VIRTUAL_QUOTE_RESERVES.md` | 2026-11-23 | DOC |

### A5. "Market cap" definition

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Bonding-curve market cap (quote base units) | `virtualQuoteReserves * mintSupply / virtualTokenReserves` (i.e. spot price from **virtual** reserves × supply) | S2 `docs/FEE_PROGRAM_README.md`; S3 `bondingCurveMarketCap` | 2026-11-23 | DOC |
| Supply used | fee logic passes `ONE_BILLION_SUPPLY` (1e15 base units) for normal coins and the actual mint supply for mayhem coins | S3 `fees.ts` `getFee` | 2026-11-23 | DOC |
| PumpSwap canonical-pool market cap | `quoteReserve * baseMintSupply / baseReserve`; fee page: "current price of the token in SOL or USDC multiplied by 1 billion tokens" | S2 `FEE_PROGRAM_README.md`; S1 `/docs/fees` | 2026-11-23 | DOC |

### A6. Graduation / migration

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Complete condition | `complete` set `true` "at the end of a `buy` instruction, when `real_token_reserves == 0`" | S2 `PUMP_PROGRAM_README.md` | 2026-11-23 | DOC |
| Site wording | "Once a coin's market cap on the bonding curve hits the graduation threshold, the curve is closed and the entire liquidity pool is migrated atomically to PumpSwap … Graduation is automatic and irreversible." No numeric threshold is published on the site | S1 `/docs/bonding-curve` | 2026-11-23 | DOC (threshold number NOT FOUND; ≈410.9 SOL / ≈58.8k USDC DERIVED) |
| Migration instruction | `migrate` / `migrate_v2`: permissionless, idempotent, moves liquidity of a completed curve to PumpSwap; after completion every curve trade fails with `BondingCurveComplete` until migration | S2 `PUMP_PROGRAM_README.md`, `SYNTHETIC_MIGRATION.md`, IDL | 2026-11-23 | DOC |
| LP tokens | "The LP tokens received from the PumpSwap pool are then burnt." Site: "Pump.fun does not seed or remove this liquidity after graduation. The pool is owned by the protocol." | S2 `PUMP_PROGRAM_README.md`; S1 `/docs/bonding-curve` | 2026-11-23 | DOC |
| Migration fee | "0.015 SOL, for every coin regardless of the asset it is paired with. For a SOL-paired coin it is deducted from the bonding curve…" | S1 `/docs/fees` | 2026-11-23 | DOC |
| Raydium (historical) | `withdraw` is "a now-disabled instruction which allowed the `withdraw_authority` … to withdraw the liquidity of a completed bonding curve and migrate it to Raydium from an off-chain server"; coins "already migrated to Raydium" get no creator fee. Program error 6005 text still reads "…liquidity migrated to raydium." | S2 `PUMP_PROGRAM_README.md`, `PUMP_CREATOR_FEE_README.md`, `idl/pump.json` | 2026-11-23 | DOC |
| Date PumpSwap replaced Raydium as destination | ~20 March 2025 | not stated in the docs read (repo starts 2025-04-04) | — | MEMORY |
| Migration events | `CompleteEvent {user, mint, bonding_curve, timestamp, quote_mint}`; `CompletePumpAmmMigrationEvent {user, mint, mint_amount, sol_amount (= quote amount), pool_migration_fee, bonding_curve, timestamp, pool, quote_mint}`; PumpSwap `CreatePoolEvent` | S2 `idl/pump.json`, `idl/pump_amm.json` | 2026-11-23 | DOC |

### A7. Fee schedule (current: `/docs/fees`, "Last Updated: 16 November 2026")

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Create a coin | "No platform fee, for any pairing" (network fee + account deposits only) | S1 `/docs/fees` | 2026-11-23 | DOC |
| Bonding curve (SOL and USDC coins) | creator **0.300%** + protocol **0.95%** + LP **0%** = **1.25%** | S1 `/docs/fees`; S4: `pfee…GetFeesWithQuoteMint` return data = lp 0 / protocol 95 / creator 30 bps on a live curve buy | 2026-11-23 | DOC + CHAIN |
| PumpSwap canonical pool, SOL-denominated, by market cap | see tier table below (1.25% → 0.30%) | S1 `/docs/fees` | 2026-11-23 | DOC |
| PumpSwap non-canonical pools | creator 0% + protocol 0.05% + LP 0.25% = 0.30% | S1 `/docs/fees` | 2026-11-23 | DOC |
| Custom-pair coins (quote ≠ SOL/USDC) | curve 0.30/0.95/0 = 1.25%; canonical pool 0.05/0.05/0.20 = 0.30% flat; Holder-Rewards rate 0.01%–3% may replace creator fee | S1 `/docs/fees` | 2026-11-23 | DOC |
| Fee asset | "Every fee is collected in the quote asset of the pool on which it is charged, never in the coin being traded." | S1 `/docs/fees` | 2026-11-23 | DOC |
| Platform Fee (interface fee) | "From 17 October 2026, every trade you place through the pump.fun web app or the pump.fun mobile app carries a Platform Fee": **0.45%** (no referral) / **0.40%** (with referral); "not charged on trades placed through Terminal or any third-party interface" | S1 `/docs/fees` | 2026-11-23 | DOC |
| Buyback slice | "The buyback part of the protocol fee is still paid in the trade"; `Global.buyback_basis_points` = 5000 on-chain | S2 `TRADE_V3.md`; S4 | 2026-11-23 | DOC + CHAIN (that 5000 bps means 50% *of the protocol fee* is my reading — not stated verbatim) |
| v3 trades: fee custody | protocol + creator fee stay on the curve/pool (`BondingCurve.protocol_fees`/`creator_fee`) until permissionless `sweep_*`; "Same prices, same fees" | S2 `README.md`, `SWEEP_FEES.md` | 2026-11-23 | DOC |
| Mayhem coins | protocol fees go to separate "reserved" recipients (insurance fund), not tracked on fees.pump.fun; agent pays no protocol fees | S1 `/docs/mayhem-mode` | 2026-11-23 | DOC |
| Change log: creator fee introduced | Program upgrade "Mainnet on Monday, May 12, 11:00 AM UTC" (2025); fee page: applicable "from the date of May 13th 2025" | S2 `PUMP_CREATOR_FEE_README.md` (commit 2025-05-08); S1 `/docs/fees` | 2026-11-23 | DOC |
| Change log: dynamic market-cap fee tiers | "On Monday, September 1, 20:00 UTC … the programs fee structure will change … to a dynamic fee structure depending on the current market cap" (2025; commit 2025-08-29) | S2 `FEE_PROGRAM_README.md`, `docs/fees.png` | 2026-11-23 | DOC |
| Before those changes | `Global.fee_basis_points == 100 bps` (1% curve fee); PumpSwap `lp_fee_basis_points == 20`, `protocol_fee_basis_points == 5` (0.25%) | S2 README JSON snapshots | 2026-11-23 | DOC |
| Change log: other dated protocol changes | Mayhem Mode + `create_v2` (Token-2022) Nov 2025; cashback Feb 2026, deprecated Sep 2026 (holder rewards added); USDC-paired coins May 2026; pool `virtual_quote_reserves` Jul 2026 (negative from 30 Sep 2026); v3 trades / multi-hop / synthetic migration / fee sweeps 8 Oct 2026; depth-2 pump-coin quotes 13 Oct 2026; fee-recipient rotation cut-off 25 Nov 2026 | S2 `git log`, `README.md` | 2026-11-23 | DOC |
| "Project Ascend" name for the Sept-2025 tiers | — | name does not appear in the docs read | — | MEMORY |

PumpSwap canonical-pool tiers, SOL-denominated (S1 `/docs/fees`, DOC). Columns: creator / protocol / LP / total.

| market cap (SOL) | creator | protocol | LP | total |
|---|---|---|---|---|
| 0 – 420 | 0.300% | 0.930% | 0.020% | 1.250% |
| 420 – 1470 | 0.950% | 0.050% | 0.200% | 1.200% |
| 1470 – 2460 | 0.900% | 0.050% | 0.200% | 1.150% |
| 2460 – 3440 | 0.850% | 0.050% | 0.200% | 1.100% |
| 3440 – 4420 | 0.800% | 0.050% | 0.200% | 1.050% |
| 4420 – 9820 | 0.750% | 0.050% | 0.200% | 1.000% |
| 9820 – 14740 | 0.700% | 0.050% | 0.200% | 0.950% |
| 14740 – 19650 | 0.650% | 0.050% | 0.200% | 0.900% |
| 19650 – 24560 | 0.600% | 0.050% | 0.200% | 0.850% |
| 24560 – 29470 | 0.550% | 0.050% | 0.200% | 0.800% |
| 29470 – 34380 | 0.500% | 0.050% | 0.200% | 0.750% |
| 34380 – 39300 | 0.450% | 0.050% | 0.200% | 0.700% |
| 39300 – 44210 | 0.400% | 0.050% | 0.200% | 0.650% |
| 44210 – 49120 | 0.350% | 0.050% | 0.200% | 0.600% |
| 49120 – 54030 | 0.300% | 0.050% | 0.200% | 0.550% |
| 54030 – 58940 | 0.275% | 0.050% | 0.200% | 0.525% |
| 58940 – 63860 | 0.250% | 0.050% | 0.200% | 0.500% |
| 63860 – 68770 | 0.225% | 0.050% | 0.200% | 0.475% |
| 68770 – 73681 | 0.200% | 0.050% | 0.200% | 0.450% |
| 73681 – 78590 | 0.175% | 0.050% | 0.200% | 0.425% |
| 78590 – 83500 | 0.150% | 0.050% | 0.200% | 0.400% |
| 83500 – 88400 | 0.125% | 0.050% | 0.200% | 0.375% |
| 88400 – 93330 | 0.100% | 0.050% | 0.200% | 0.350% |
| 93330 – 98240 | 0.075% | 0.050% | 0.200% | 0.325% |
| 98240 and up | 0.050% | 0.050% | 0.200% | 0.300% |

USDC-denominated tiers (same page): 0–59,000 USDC 0.300/0.930/0.020 = 1.25%; 59k–300k 1.20%; 300k–500k 1.15%;
500k–700k 1.10%; 700k–900k 1.05%; 900k–2M 1.00%; 2–3M 0.95%; then −0.05% per 1M to 10–11M 0.55%; 11–12M 0.53%;
12–13M 0.50%; 13–14M 0.48%; 14–15M 0.45%; 15–16M 0.43%; 16–17M 0.40%; 17–18M 0.38%; 18–19M 0.35%; 19–20M 0.33%;
≥20M 0.30% (protocol 0.05%, LP 0.20% above the first tier). Tier lookup rule: below first threshold → first tier,
else highest tier whose `marketCapLamportsThreshold <= marketCap` (S2 `FEE_PROGRAM_README.md` `calculateFeeTier`).
"The pump.fun platform may change these fees from time to time by updating this page."

### A8. Token program and authorities

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Token program for new coins | `create_v2`: "New Token-2022 mint account … initialized with `decimals = 6`, `mint_authority`, `token_program`, and metadata pointer set to `mint`". IDL doc: "Creates a new spl-22 coin and bonding curve." | S2 `COIN_CREATION.md`, `idl/pump.json` | 2026-11-23 | DOC |
| Legacy coins | legacy `create` uses SPL Token + Metaplex metadata (`metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s`); "Token-2022 … for `create_v2` coins, SPL Token for older coins" | S2 `idl/pump.json`, `TRADE_V3.md` | 2026-11-23 | DOC |
| Site wording still says | "Name, symbol, and image are immutable. They're part of the SPL token metadata." | S1 `/docs/create-coin` | 2026-11-23 | DOC |
| Mint/freeze authority after creation | NOT stated in the official docs. Observed on 3 mints created 2026-11-23 (`9nQCcWhnEQNxA5XYr44ErGMREVh5FjpCXNPiDiGDpump`, `7d3TagyZKHks9mDXMtWHy7bP3N9eGDieT5YsDZ6bKbS3`, `ikfJwJZQ6gVkNw5fj9GEc76EtuBjqHVb1QAsjywpump`): owner Token-2022, `mintAuthority: null`, `freezeAuthority: null`, decimals 6, extensions `metadataPointer` (authority None) + `tokenMetadata` (updateAuthority None); create tx logs show `MintTo` then `SetAuthority`. Legacy sample `Coyj3L…pump`: SPL Token, both authorities null | S4 `getAccountInfo` jsonParsed, `getTransaction` | 2026-11-23 | CHAIN (docs: NOT FOUND) |
| Mint address suffix | Not all new mints end in `pump` (1 of 3 sampled did not) — do not use the suffix as a filter | S4 | 2026-11-23 | CHAIN |
| Token-2022 quote mints | a Token-2022 quote mint "may only carry the xStock operable extension set (metadata pointer/metadata, permanent delegate, initialized default account state, scaled UI amount, pausable, confidential-transfer mint, and a transfer hook with no program)" — applies to *quote* assets, relevant for custom pairs | S2 `idl/pump.json` create_v2 docs | 2026-11-23 | DOC |

### A9. Events and read-only launch detection

Event discriminators (first 8 bytes) from `idl/pump.json` (S2, DOC):
`CreateEvent [27,114,169,77,222,235,99,118]`, `TradeEvent [189,219,127,211,78,230,97,238]`,
`CompleteEvent [95,114,97,156,212,46,152,8]`, `CompletePumpAmmMigrationEvent [189,233,93,185,92,148,234,148]`,
`PostCompleteBuyEvent [111,176,109,139,49,108,213,251]`, `SweepBondingCurveFeeEvent [116,43,77,189,17,122,72,43]`.
PumpSwap (`idl/pump_amm.json`): `CreatePoolEvent [177,49,12,210,160,118,167,116]`, `BuyEvent [103,244,82,31,44,245,119,119]`,
`SellEvent [62,47,55,10,165,3,220,42]`.

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| `CreateEvent` fields (borsh, in order) | `name:string, symbol:string, uri:string, mint, bonding_curve, user, creator, timestamp:i64, virtual_token_reserves:u64, virtual_sol_reserves:u64, real_token_reserves:u64, token_total_supply:u64, token_program, is_mayhem_mode:bool, is_cashback_enabled:bool, quote_mint, virtual_quote_reserves:u64, creator_fee_bps:u64, is_holder_reward:bool, depth:u8` | S2 `idl/pump.json` | 2026-11-23 | DOC |
| `TradeEvent` fields | `mint, sol_amount:u64, token_amount:u64, is_buy:bool, user, timestamp:i64, virtual_sol_reserves, virtual_token_reserves, real_sol_reserves, real_token_reserves, fee_recipient, fee_basis_points, fee, creator, creator_fee_basis_points, creator_fee, track_volume, total_unclaimed_tokens, total_claimed_tokens, current_sol_volume, last_update_timestamp, ix_name:string, mayhem_mode, cashback_fee_basis_points, cashback, buyback_fee_basis_points, buyback_fee, shareholders:vec, quote_mint, quote_amount, virtual_quote_reserves, real_quote_reserves, holder_rewards_bps, holder_rewards, creator_fee_unclaimed` (reserves are post-trade) | S2 `idl/pump.json` | 2026-11-23 | DOC |
| v3 trade specifics | `ix_name` ∈ `buy_v3`/`buy_exact_quote_in_v3`/`sell_v3`; `fee_recipient` is the zero key (fee kept on curve); payouts appear later as `SweepBondingCurveFeeEvent` — "Do not count both as income" | S2 `TRADE_V3.md`, `SWEEP_FEES.md` | 2026-11-23 | DOC |
| Completing v3 buy emits 3 events | `TradeEvent` (curve part) → `CompleteEvent` → `PostCompleteBuyEvent` (pool part); buyer total = TradeEvent + PostCompleteBuyEvent amounts | S2 `SYNTHETIC_MIGRATION.md` | 2026-11-23 | DOC |
| How events are emitted | Docs: instructions carry `event_authority` (`["__event_authority"]`) + `program` accounts "generated by `#[event_cpi]`"; docs also refer to "`BuyEvent` and `SellEvent` logs". Observed on mainnet: each event appears **twice** — (1) a `Program data: <base64>` log line whose decoded bytes start with the 8-byte event discriminator, and (2) an inner self-CPI instruction to the program whose data = `e445a52e51cb9a1d` + discriminator + borsh body | S2 `COIN_CREATION.md`; S4 txs `3vUeih3v…` (SellV3), `4e136ZNs…` (Buy) | 2026-11-23 | DOC + CHAIN |
| Detect new launches (read-only) | (a) `logsSubscribe {"mentions":["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"]}` and decode `Program data:` lines with the CreateEvent discriminator (log line `Program log: Instruction: CreateV2` / `Create` also present); or (b) poll `getSignaturesForAddress` on the low-traffic mint-authority PDA `TSLvdd1p…` (only create txs reference it) then `getTransaction`; program-wide polling is impractical: a 120-signature page (the limit requested) was filled by a single slot | S4; RPC docs (section B) | 2026-11-23 | CHAIN (method is my recommendation, not a pump.fun statement) |
| `getTransaction` must allow v1 | With `maxSupportedTransactionVersion: 0` many current Pump transactions fail: `-32015 "Transaction version (1) is not supported by the requesting client…"`; use `1` | S4; Solana docs (B) | 2026-11-23 | CHAIN + DOC |
| CU guidance | "recommended to use a static big enough CU limit like `100_000`" for buy/sell (observed: SellV3 61,899 CU; mayhem Buy via agent 141,197 CU) | S2 `docs/FAQ.md`; S4 | 2026-11-23 | DOC + CHAIN |

### A10. Official API / terms of use

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Official public REST/WebSocket data API | None documented. The docs site pages and the `pump-public-docs` repo contain no REST/WebSocket data API reference; official developer surface = on-chain programs, IDLs, `@pump-fun/pump-sdk`, `@pump-fun/pump-swap-sdk`, `pump-rust-client` | S1, S2 | 2026-11-23 | DOC (absence) |
| `frontend-api-v3.pump.fun` | Appears only as `<link rel="preconnect">`/`dns-prefetch` in the site HTML; no documentation, no terms granting access | S1 page source | 2026-11-23 | observed in page HTML / docs: NOT FOUND |
| Terms §21(h) (prohibited conduct) | "(i) except as expressly permitted under Section 6.1, use any deep linking, web crawlers, bots, spiders or other automatic devices, programs, scripts, algorithms or methods, or any similar or equivalent manual processes to access, obtain, copy or monitor any part of the Pump Platform and/or Pump Services … in order to obtain or attempt to obtain any materials, documents or information in any manner not purposely provided by the Pump Platform and/or Pump Services; … (v) take any actions that impose an unreasonable or disproportionately large load on the infrastructure…" | S1 `/docs/terms-and-conditions` | 2026-11-23 | DOC |
| Terms §6.1 | "You may access the Pump Platform and Pump Services through such automated means (including bots) as we expressly permit from time to time, provided that such access complies with these Terms, including Section 21(h)." | S1 `/docs/terms-and-conditions` | 2026-11-23 | DOC |
| Implication for this tool | Reading on-chain data via Solana RPC is outside the Pump Platform; calling the undocumented frontend API is automated access "not purposely provided" → treat as not permitted | my reading of the above | 2026-11-23 | interpretation |
| Community updates channel | Footer link "Tech updates" → `https://t.me/pump_tech_updates`; revenue dashboard `https://fees.pump.fun/` | S1 page source | 2026-11-23 | DOC |

---

## B. Solana JSON-RPC

Sources:
- R1 solana.com docs source: `github.com/solana-foundation/solana-com` @ `82d49aed` (2026-11-20),
  `apps/docs/content/docs/en/rpc/**`, `references/clusters.mdx`, `core/fees/*`, `tokens/basics/*`, `defi/exchange.mdx`.
  Canonical URLs: `https://solana.com/docs/rpc/http/<method>`, `https://solana.com/docs/references/clusters`.
  (Docs cite agave `v3.1.8` source.)
- R2 Anza validator docs `https://docs.anza.xyz/operations/setup-an-rpc-node`,
  `https://docs.anza.xyz/implemented-proposals/rpc-transaction-history`
- R3 live `https://api.mainnet-beta.solana.com` / `https://api.mainnet.solana.com`

### B1. Methods

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| `getSignaturesForAddress` params | `address`; config `commitment` (`confirmed`/`finalized` only — "does not accept `processed`", default `finalized`), `minContextSlot`, `limit` "between 1 and 1,000", default 1000, `before` (search backwards from this signature), `until` | R1 `rpc/http/getsignaturesforaddress.mdx` | 2026-11-23 | DOC |
| `getSignaturesForAddress` result | array newest→oldest: `signature`, `slot`, `err`, `memo`, `blockTime` (i64 or null), `confirmationStatus`. Matches txs "that reference the supplied address in `accountKeys`" | same | 2026-11-23 | DOC |
| … observed extra field | live responses also carry `transactionIndex` | R3 | 2026-11-23 | CHAIN |
| `getTransaction` params | `signature`; config `commitment` (no `processed`), `maxSupportedTransactionVersion` (values `0`, `1`: "If you omit this parameter, only legacy transactions will be returned—any versioned transaction will result in an error"; `1` also returns v1 transactions), `encoding` (`json` default, `jsonParsed`, `base64`, `base58`) | R1 `rpc/http/gettransaction.mdx` | 2026-11-23 | DOC |
| `getTransaction` result | `null` if not found/confirmed; `slot`, `blockTime`, `version`, `transaction`, `meta` {`err`, `fee`, `preBalances`, `postBalances`, `innerInstructions` (may be null), `logMessages` (may be null), `preTokenBalances`, `postTokenBalances` {`accountIndex`, `mint`, `owner`, `programId`, `uiTokenAmount`}, `loadedAddresses`, `returnData`, `computeUnitsConsumed`, `costUnits`} | same | 2026-11-23 | DOC |
| `getAccountInfo` | `pubkey`; `commitment` (processed/confirmed/finalized, default finalized), `encoding` (protocol default is deprecated `binary`; "New integrations should explicitly request `base64`"; `base58` limited to ≤128-byte data; `jsonParsed` → `{program, parsed, space}` for `spl-token`, `spl-token-2022`, …), `dataSlice`, `minContextSlot` | R1 `rpc/http/getaccountinfo.mdx` | 2026-11-23 | DOC |
| `getMultipleAccounts` | "up to a maximum of 100" pubkeys; returns `null` for missing accounts; same encodings | R1 `rpc/http/getmultipleaccounts.mdx` | 2026-11-23 | DOC |
| `getTokenLargestAccounts` | "Returns the 20 largest token accounts for an SPL Token mint"; value = "Array of up to 20" `{address (token account, not owner), amount, decimals, uiAmount, uiAmountString}` | R1 `rpc/http/gettokenlargestaccounts.mdx` | 2026-11-23 | DOC |
| `getTokenSupply` | `{amount, decimals, uiAmount (deprecated), uiAmountString}` | R1 `rpc/http/gettokensupply.mdx` | 2026-11-23 | DOC |
| `getTokenAccountsByOwner` | owner + filter `{mint}` or `{programId}`; use `encoding: "jsonParsed"` for parsed token accounts | R1 `rpc/http/gettokenaccountsbyowner.mdx` | 2026-11-23 | DOC |
| `getProgramAccounts` | program pubkey; `filters`: "up to 4 filter objects", all must match: `memcmp {offset, bytes (base58 default; decoded ≤128 bytes), encoding}`, `dataSize`, `tokenAccountState`; `dataSlice`; `withContext`; `sortResults` (default true). No pagination parameter documented | R1 `rpc/http/getprogramaccounts.mdx` | 2026-11-23 | DOC |
| `getBlockTime` | slot → Unix seconds; "calculated from the stake-weighted mean of the Vote timestamps"; `null` when block available but no time recorded; error when unavailable | R1 `rpc/http/getblocktime.mdx` | 2026-11-23 | DOC |
| `getSlot` | highest slot at commitment (default finalized) | R1 `rpc/http/getslot.mdx` | 2026-11-23 | DOC |
| `logsSubscribe` (WebSocket) | filter `all` / `allWithVotes` / `{ "mentions": [<pubkey>] }` — "The `mentions` filter currently supports exactly one address. Listing more than one returns an `Invalid params` error." Notification `value`: `signature`, `err`, `logs[]`; `context.slot`. Commitment default finalized | R1 `rpc/websocket/logssubscribe.mdx` | 2026-11-23 | DOC |
| WebSocket durability | "Subscription notifications are not a durable event log, so reconcile state with HTTP after reconnecting." | R1 `rpc/providers.mdx` | 2026-11-23 | DOC |
| Commitment default | "If a method or subscription accepts `commitment` and you omit it, the default is typically `finalized`." | R1 `rpc/index.mdx` | 2026-11-23 | DOC |

### B2. Public endpoint limits, history, restricted methods

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Public mainnet endpoint name in docs | `https://api.mainnet.solana.com` ("Solana Labs hosted API node cluster, backed by a load balancer; rate-limited"). `api.mainnet-beta.solana.com` is no longer the name printed in the docs but still answers with identical rate-limit headers | R1 `references/clusters.mdx`, `rpc/index.mdx`; R3 | 2026-11-23 | DOC + CHAIN |
| Mainnet rate limits (documented) | "Maximum number of requests per 10 seconds per IP: 100"; "…per IP for a single RPC: 40"; "Maximum concurrent connections per IP: 40"; "Maximum connection rate per 10 seconds per IP: 40"; "Maximum amount of data per 30 seconds: 100 MB" | R1 `references/clusters.mdx` (`https://solana.com/docs/references/clusters`) | 2026-11-23 | DOC |
| Caveat on those numbers | "Public endpoint rate limits are subject to change. The specific rate limits listed on this document are not guaranteed to be the most up-to-date." | same | 2026-11-23 | DOC |
| Not for production | "The public RPC endpoints are not intended for production applications. Please use dedicated/private RPC servers when you launch your application… rate limits may change without prior notice. Likewise, high-traffic websites may be blocked without prior notice." | same | 2026-11-23 | DOC |
| Error codes | 403 = "Your IP address or website has been blocked"; 429 = "exceeding the rate limits. Slow down! Use the Retry-After HTTP response header" | same | 2026-11-23 | DOC |
| Observed response headers | `x-ratelimit-tier: free`, `x-ratelimit-method-limit: 50` (getAccountInfo), `x-ratelimit-rps-limit: 250`, `x-ratelimit-conn-limit: 40`, `x-ratelimit-connrate-limit: 40`, `x-ratelimit-pubsub-limit: 5`; `getProgramAccounts` → `x-ratelimit-method-limit: 10` | R3 | 2026-11-23 | CHAIN (undocumented; units/window not stated) |
| `getTokenLargestAccounts` on public RPC | Both public hostnames returned HTTP 429 `"Too many requests for a specific RPC call"` with `x-ratelimit-method-limit: 0`, `retry-after: 10` on the first call → effectively disabled | R3 | 2026-11-23 | CHAIN (no official statement found listing disabled methods) |
| `getProgramAccounts` on public RPC | A Token-2022 query with one `memcmp` (mint) + `dataSlice` succeeded for a brand-new mint | R3 | 2026-11-23 | CHAIN |
| Official list of methods disabled on public RPC | none found in solana.com docs; providers guide only says to ask "Are any methods disabled or priced separately?" | R1 `rpc/providers.mdx` | 2026-11-23 | NOT FOUND |
| Ledger retention (node operators) | "it is not practical for an RPC node to store the entire blockchain on the machine. Instead, RPC operators use the `--limit-ledger-size` flag … If the user of the RPC node needs historical blockchain data, then the RPC server will have to access older blocks through a Solana bigtable instance." | R2 `/operations/setup-an-rpc-node` | 2026-11-23 | DOC |
| Long-term history design | "The current history, on the order of days, is insufficient… an external data store is necessary… Google's BigTable product is selected"; affected endpoints include getSignaturesForAddress/getTransaction (listed under their old `getConfirmed*` names), `getBlockTime`, `getFirstAvailableBlock` | R2 `/implemented-proposals/rpc-transaction-history` | 2026-11-23 | DOC |
| History checks | "`minimumLedgerSlot` reports the lowest slot retained in the node's ledger, while `getFirstAvailableBlock` reports the lowest confirmed block slot that has not been purged. Neither alone guarantees that every historical method or transaction is available, so test a known old signature…" | R1 `rpc/providers.mdx` | 2026-11-23 | DOC |
| Observed on public RPC | `getFirstAvailableBlock` = 0; `minimumLedgerSlot` = 472,711,146 (≈ 90k slots ≈ 10 h behind tip) | R3 | 2026-11-23 | CHAIN |
| Account indexes | `--account-index program-id` ("used by getProgramAccounts"), `spl-token-mint` ("used by getTokenAccountsByDelegate, and getTokenLargestAccounts"), `spl-token-owner` ("used by getTokenAccountsByOwner…"); without them scans "may perform poorly" | R2 `/operations/setup-an-rpc-node` | 2026-11-23 | DOC |

### B3. Why "all holders" needs getProgramAccounts or an indexer

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Top-20 only | `getTokenLargestAccounts` returns at most 20 token accounts (addresses of token accounts; owners need a further lookup) | R1 | 2026-11-23 | DOC |
| No per-mint enumeration method | Standard RPC has by-owner and by-delegate token-account methods but no "by mint" method; the documented way to scan is `getProgramAccounts` on the token program with filters | R1 method list (`rpc/http/*`) | 2026-11-23 | DOC (absence) |
| SPL Token account layout | `mint` (offset 0, 32 bytes), `owner` (offset 32), `amount` u64 (offset 64); size 165 bytes | R1 `tokens/basics/create-token-account.mdx` (struct), `getprogramaccounts.mdx` example uses `{"dataSize":165}` + `memcmp offset 0` (+ offset 32) on `Tokenkeg…` | 2026-11-23 | DOC |
| Token-2022 difference | "RPC indexes SPL Token-2022 accounts, but they must be queried separately with program id `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`"; "Because of extensions, however, accounts may be larger than 165 bytes"; ATAs "take a minimum of 170 bytes" | R1 `defi/exchange.mdx` | 2026-11-23 | DOC |
| Consequence for Pump coins | Current Pump mints are Token-2022 → `dataSize: 165` on `Tokenkeg…` returns nothing. Query `Tokenz…` with `memcmp {offset:0, bytes:<mint>}` and no 165 filter (observed holder account `space: 170`); use `dataSlice {offset:32,length:40}` for owner+amount. Legacy Pump coins: `Tokenkeg…` + `dataSize 165` + memcmp | R1 + R3 | 2026-11-23 | DOC + CHAIN |
| Token-2022 account-type byte at offset 165 (=2 for token accounts) as an extra filter | — | not in the docs read | — | MEMORY |
| Practical limits | Unpaginated, single response, 100 MB/30 s data cap and low per-method limit on public RPC; zero-balance accounts are included; several accounts per owner possible → aggregate by owner. Holder *history* is not available from account state at all → needs an indexer or replay of transactions | R1 limits + reasoning | 2026-11-23 | DOC + interpretation |

---

## C. Market-data providers

### C1. DEX Screener

Sources: D1 `https://docs.dexscreener.com/api/reference` (+ `.md`), D2 `https://docs.dexscreener.com/api/api-terms-and-conditions`
("Last updated: August 18, 2023"), D3 `https://docs.dexscreener.com/faq`, D4 `https://docs.dexscreener.com/api/websockets`,
D5 `https://docs.dexscreener.com/privacy/terms-and-conditions` ("Last updated: April 26, 2025"), D6 live `https://api.dexscreener.com`.

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| API key | none required for the documented endpoints (base `https://api.dexscreener.com`); FAQ calls it "our free API" | D1, D3 | 2026-11-23 | DOC |
| Endpoints @ 60 req/min | `GET /token-profiles/latest/v1`, `/token-profiles/recent-updates/v1`, `/community-takeovers/latest/v1`, `/ads/latest/v1`, `/token-boosts/latest/v1`, `/token-boosts/top/v1`, `/orders/v1/{chainId}/{tokenAddress}`, `/metas/trending/v1`, `/metas/meta/v1/{slug}` | D1 | 2026-11-23 | DOC |
| Endpoints @ 300 req/min | `GET /latest/dex/pairs/{chainId}/{pairId}`, `/latest/dex/search?q=`, `/token-pairs/v1/{chainId}/{tokenAddress}` (pools of a token), `/tokens/v1/{chainId}/{tokenAddresses}` ("up to 30 addresses", comma-separated) | D1 | 2026-11-23 | DOC |
| Pair schema | `chainId, dexId, url, pairAddress, labels, baseToken{address,name,symbol}, quoteToken, priceNative (string), priceUsd (string, nullable), txns{m5,h1,h6,h24:{buys,sells}}, volume, priceChange, liquidity{usd (nullable), base, quote} (nullable), fdv (nullable), marketCap (nullable), pairCreatedAt (integer, nullable), info{imageUrl,websites,socials}, boosts{active}` | D1 OpenAPI | 2026-11-23 | DOC |
| Definitions of `marketCap` vs `fdv` vs `liquidity.usd` vs `pairCreatedAt` vs `priceUsd` | **Not defined** in the reference — only types. | D1 | 2026-11-23 | NOT FOUND |
| Historical candles / OHLCV / trades | No such endpoint in the public reference; WebSocket API streams only token profiles, boosts, community takeovers, ads | D1, D4 | 2026-11-23 | DOC (absence) — confirms "no historical candles via public API" |
| Data origin | "All DEX Screener data comes directly from the blockchains it tracks, without the use of any external APIs or data sources." | D3 | 2026-11-23 | DOC |
| Pump.fun pairs — observed | New bonding-curve coin → `dexId: "pumpfun"`, `pairAddress` = bonding-curve PDA, **`liquidity: null`**, `pairCreatedAt` = CreateEvent timestamp × 1000 (ms), `fdv == marketCap`. Graduated coin → `dexId: "pumpswap"`, `liquidity {base, quote, usd}` with `usd` ≈ 2 × quote-side value. For a Mayhem coin (2B supply) `fdv` = price × 1e9, i.e. half of GeckoTerminal's FDV | D6 `/token-pairs/v1/solana/<mint>` | 2026-11-23 | CHAIN (undocumented; could change) |
| Response caching — observed | `cache-control: public, max-age=30` | D6 | 2026-11-23 | CHAIN |
| API terms — licence | "limited, non-exclusive, non-transferable, non-assignable, and revocable license"; may not build "a product or service whose primary purpose is to compete directly with DEX Screener's product or the API Services itself" (§1) | D2 | 2026-11-23 | DOC |
| API terms — redistribution | "prohibited from … making the API Services, or any portion thereof, available for third parties" (§2) | D2 | 2026-11-23 | DOC |
| API terms — commercial use | "The API Services may be used for both non-commercial and commercial purposes, subject to the limitations set forth in this Agreement." (§4) | D2 | 2026-11-23 | DOC |
| API terms — data ownership | "Users do not gain ownership of any technological or intellectual property rights in or to the API Services or the data obtained through it." (§3) | D2 | 2026-11-23 | DOC |
| Caching / local storage / attribution | No clause addresses caching, storage or attribution | D2 | 2026-11-23 | **unclear** (not prohibited, not expressly permitted; do not redistribute) |

### C2. GeckoTerminal public API

Sources: G1 `https://api.geckoterminal.com/docs/v2/swagger.json` (linked from `https://api.geckoterminal.com/docs/index.html`,
title "GeckoTerminal API V2", version `v2-beta`), G2 `https://docs.coingecko.com` (where `apiguide.geckoterminal.com` now
redirects): `/demo/reference/pool-ohlcv-contract-address`, `/demo/reference/pool-trades-contract-address`,
`/demo/reference/token-data-contract-address`, `/docs/errors-and-rate-limits`, `/demo/reference/authentication`;
G3 live `https://api.geckoterminal.com/api/v2`.

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Base URL / key | `https://api.geckoterminal.com/api/v2`, no key. Version header recommended: `Accept: application/json;version=20230203`. "The API is in its Beta release, and is subject to frequent changes." | G1 | 2026-11-23 | DOC |
| Rate limit (public) | "This Public API is limited to approximately **10 calls/minute**, which may fluctuate based on network traffic." | G1 | 2026-11-23 | DOC |
| … CoinGecko keyed alternative | Same data as `/onchain` endpoints on `https://api.coingecko.com/api/v3/onchain/...`: "Demo plan: 100 calls/min"; "Keyless (no API key): IP-based rate limiting — shared across all users on the same IP"; "All requests count toward your per-minute rate limit — including `4xx` and `5xx` errors" | G2 `/docs/errors-and-rate-limits` | 2026-11-23 | DOC |
| … observed | 2 of 3 calls spaced ~7 s apart from a shared egress IP returned 429 | G3 | 2026-11-23 | CHAIN |
| Freshness | "All endpoints listed below are cached for **1 minute**"; data "updated as fast as 2-3 seconds after a transaction is confirmed" | G1 | 2026-11-23 | DOC |
| Token endpoints | `GET /networks/{network}/tokens/{address}` (`include=top_pools`, `include_composition`), `/tokens/multi/{addresses}` ("up to 30 addresses"), `/tokens/{address}/info` (metadata), `/tokens/{token_address}/pools` (page max 10), `/simple/networks/{network}/token_price/{addresses}` (up to 30; `include_market_cap`, `mcap_fdv_fallback`, …) | G1 | 2026-11-23 | DOC |
| Pool endpoints | `/networks/{network}/pools/{address}`, `/pools/multi/{addresses}` (up to 30), `/networks/{network}/new_pools` (page max 10), `/networks/new_pools`, `/networks/{network}/dexes/{dex}/pools`, `/search/pools`, trending pools | G1 | 2026-11-23 | DOC |
| OHLCV | `GET /networks/{network}/pools/{pool_address}/ohlcv/{timeframe}`; `timeframe` ∈ `day`, `hour`, `minute`; `aggregate`: day `1`; hour `1`,`4`,`12`; minute `1`,`5`,`15`; `before_timestamp` (epoch seconds); `limit` default 100, **maximum 1000**; `currency` `usd`/`token`; `token` `base`/`quote`/address; `include_empty_intervals` (default false) | G1 | 2026-11-23 | DOC |
| OHLCV row / paging | `[timestamp, open, high, low, close, volume]`; "Each call retrieves a max 6-month range — use `before_timestamp` for older data"; intervals with no swaps skipped by default | G2 `/demo/reference/pool-ohlcv-contract-address` | 2026-11-23 | DOC |
| OHLCV depth | "Historical Access by Plan: Basic: past 6 months; Analyst and above: September 2021 to present (depending on pool tracking start)" (statement is for the CoinGecko API plans; the keyless GeckoTerminal host does not state a depth) | G2 | 2026-11-23 | DOC (public-host depth: unclear) |
| Trades | `GET /networks/{network}/pools/{pool_address}/trades` — "query the last 300 trades in the past 24 hours"; `trade_volume_in_usd_greater_than`; longer `trading_period` (7d/30d), `cursor`, `per_page` are "Pro API only" | G1; G2 `/demo/reference/pool-trades-contract-address` | 2026-11-23 | DOC |
| Trade fields | `block_number, block_timestamp, tx_hash, tx_from_address, kind, from_token_address, to_token_address, from_token_amount, to_token_amount, price_from_in_usd, price_to_in_usd, volume_in_usd, is_anomalous` | G1 | 2026-11-23 | DOC |
| FDV vs market cap | `fdv_usd` = "Fully diluted valuation in USD"; `market_cap_usd` = "Market cap in USD". "Unverified token market cap returns `null` — the displayed value on GeckoTerminal may match FDV and might not be accurate. Verified market cap is sourced from CoinGecko and may exceed FDV if it includes tokens on other networks." `total_reserve_in_usd` "represents the total reserve of the requested token only across all its pools, not both tokens in a pair." | G2 `/demo/reference/token-data-contract-address` | 2026-11-23 | DOC (exact FDV formula NOT FOUND; observed = price × on-chain total supply) |
| Pump.fun bonding-curve coverage | "Bonding curve tokens (non-graduated launchpad tokens) include a `launchpad_details` object with graduation status." Observed for a 1-minute-old coin: pool id = bonding-curve PDA, dex id **`pump-fun`**, `launchpad_details {graduation_percentage: 3.87, completed: false, completed_at: null, migrated_destination_pool_address: null}`, `market_cap_usd: null`, `fdv_usd` = price × 2,000,000,000 (mayhem supply), `reserve_in_usd` non-zero | G2; G3 | 2026-11-23 | DOC + CHAIN |
| Terms / attribution | `https://www.geckoterminal.com/dex-api` and `https://www.coingecko.com/en/api_terms` returned 403 (bot challenge) — **not read** | — | 2026-11-23 | NOT CONFIRMED → storage/attribution: **unclear** |

### C3. Other providers (official docs only)

| provider | key required? | free-tier limits | local caching / storage per terms | source URL | access date | confidence |
|---|---|---|---|---|---|---|
| **Helius** | Yes (`?api-key=`) | Free $0: 1M credits/mo, RPC 10 req/s, DAS 2 req/s, Enhanced APIs 2 req/s, `getProgramAccounts` 5/s; standard RPC 1 credit, `getProgramAccounts` 10 credits, DAS (incl. `getTokenAccounts`) 10 credits, Enhanced Transactions 100 credits. Enhanced Transactions is "a legacy product in maintenance mode" (successor: Parsed Events, 10 credits/req, all plans). DAS `getTokenAccounts` takes `mint` and/or `owner` with `page`/`limit`/`cursor` pagination (that the `mint` parameter gives a paginated by-mint holder scan is my inference from the parameter list; the page's own summary only mentions accounts "owned by a wallet address") | Cloud Services Agreement (Last Updated: September 28, 2026): no caching/storage clause found; restrictions target the Services ("sell, resell, sublicense, rent, distribute, or provide the Services to third parties"; "copy, modify, or create derivative works of the Services"). **But:** Customer will not "(xi) use or access the Services in any personal, household, or familial capacity, or for any purpose other than a lawful business purpose." → storage **unclear**; personal-capacity use is excluded by the text | `https://www.helius.dev/docs/billing/plans`, `/billing/rate-limits`, `/billing/credits`, `/api-reference/das/gettokenaccounts`, `/enhanced-transactions`, `https://www.helius.dev/terms` | 2026-11-23 | DOC |
| **Birdeye** (Birdeye Data Services, Wings Lab) | Yes ("This key is required in the header of all your requests") | Standard: $0, 30,000 compute units/month, 1 rps, limited endpoint set (rate-limit page: "Limited to 3 specific endpoints"; the accessibility table marks e.g. `/defi/ohlcv`, `/defi/history_price`, `/defi/historical_price_unix` for Standard and excludes multi-price — the two pages are not fully consistent) | Terms (Last updated: 11-April-2025) §10.2: "you shall not directly or indirectly: 1. copy, scrape, extract, download, store, reproduce, replicate, record, or otherwise capture any data, content, or information from the Services … in any form or by any means, whether manual or automated"; also no sharing with third parties "whether for commercial or non-commercial purposes" → local snapshots **not permitted** as written | `https://data.birdeye.so/docs/guides/payment/pricing`, `/guides/api-access/rate-limiting/index`, `/guides/data-accessibility-by-packages`, `/resources/faqs`, `/resources/terms` | 2026-11-23 | DOC |
| **Bitquery** | Yes (API key / account) | No permanent free tier on the pricing page: "7-day trial … 1,000 API points, 100 MCP credits, 2 simultaneous streams, 17 stream-minutes and 0.2 GB"; cheapest plan "Personal $29/mo … 100k API points a month, no streaming … 30 req/min · 3 simultaneous"; archive history "is a separate add-on". Has documented Pump.fun GraphQL/stream APIs | Professional Service Agreement §3.3: "Subscriber may use the Services and any data or results obtained through the Services for any lawful commercial or non-commercial purpose…"; restrictions: no circumventing rate limits, no use that "directly substitutes for the Services for a third party". No storage limit stated → storage **appears permitted** (for own use) | `https://bitquery.io/pricing`, `https://bitquery.io/terms-of-service`, `https://docs.bitquery.io/llms.txt` | 2026-11-23 | DOC |
| **Jupiter Price API** | No for testing ("Keyless access is available at 0.5 RPS on `api.jup.ag`"); free key → 1 RPS | Keyless 0.5 RPS (30/min); Free 1 RPS (60/min), "Unlimited credits, rate-limited only"; 60-second sliding window; `GET https://api.jup.ag/price/v3?ids=` up to 50 mints; price = "last swapped price (across all transactions)" filtered by heuristics → "you may face many tokens where a price is not available" (expect gaps for fresh pump coins) | SDK & API License Agreement: prohibited to "use the API in conjunction with, or combine content from the API with, content obtained through scraping or any other means outside the API"; 8.4 product "shall prominently display … 'Powered by Jupiter'". No caching/storage clause found → **unclear** | `https://developers.jup.ag/docs/price/index`, `/portal/rate-limits`, `/portal/plans`, `/legal/sdk-api-license-agreement` | 2026-11-23 | DOC |
| **Solscan Pro API** | Yes | A Free plan exists (terms: may be throttled or disabled "at any time and without prior notice"); its numeric limits were not on the pages read. Lite plan: $49/mo, 20,000,000 CU, 1,000 requests / 60 s, excludes `Market/price-ohlcv` and multi endpoints | API Terms: "The Free and Lite Plans are licensed for Personal and Research Use only" (incl. "non-commercial academic, educational or independent research"); attribution "Powered by Solscan.io APIs" wherever data is displayed/published — "Attribution is not required for purely private use that is not displayed or made available to any other person"; no "caching, storage, or retention of API Data or Output beyond the retention period otherwise permitted under these Terms" (no retention period found in the text) → personal research OK, long-term storage **unclear** | `https://docs.solscan.io/solscan-api/solscan-api-terms-and-services`, `/solscan-api/solscan-api-lite-plan`, `/solscan-api/solscan-pro-api-faq` | 2026-11-23 | DOC |
| **SolanaFM** | Not determined from the page read | Free: $0, 10 RPS, 1 GB bandwidth; `/v1/tokens/:hash/holders` 5 RPS, `/v1/tokens/:hash/supply` 5 RPS, `/v1/addresses/:hash/tokens` 1 RPS (page `updatedAt: 2025-04-22`) | Terms not located → **unclear** | `https://docs.solana.fm/reference/rate-limits-1` | 2026-11-23 | DOC (terms/key: NOT CONFIRMED) |
| **Dune** | Yes | "Free (view-only): API access — Not available"; Plus 70 rpm (write/execute) / 200 rpm (read); 1000 rps per IP. "API usage requires an active trial or a paid plan." | `https://dune.com/terms` returned 403 → **unclear** | `https://docs.dune.com/api-reference/overview/rate-limits` | 2026-11-23 | DOC (terms NOT CONFIRMED) |

---

## D. Execution-cost facts (for a paper-trading cost model only)

| fact | value | source URL | access date | confidence |
|---|---|---|---|---|
| Base fee | 5,000 lamports per signature (`lamports_per_signature`), 50% burned / 50% to validator; charged whether the tx succeeds or fails | R1 `core/fees/fee-structure.mdx` (`https://solana.com/docs/core/fees/fee-structure`) | 2026-11-23 | DOC |
| Priority fee | `prioritization_fee = ceil(compute_unit_price[µ-lamports/CU] × compute_unit_limit / 1,000,000)` lamports; 100% to validator; default CU price 0; "based on the requested CU limit, not actual CU usage"; default limit 200,000 CU per non-builtin instruction. v1 transactions set an absolute lamport total instead | same | 2026-11-23 | DOC |
| Observed Pump tx fees | SellV3: fee 78,768 lamports, 61,899 CU consumed; mayhem-agent Buy: fee 25,000 lamports, 141,197 CU | R3 `getTransaction` | 2026-11-23 | CHAIN (two samples, not a distribution) |
| Jito bundle tip minimum | "Jito enforces a minimum tip of 1000 lamports for bundles… this minimum tip might not be sufficient"; tip = SOL transfer to one of 8 tip accounts; for `sendTransaction` a "70/30 split between priority fee and jito tip" is recommended; default rate limit "1 request per second per IP per region" | `https://docs.jito.wtf/lowlatencytxnsend/` | 2026-11-23 | DOC |
| Jito landed-tip floor (live) | `https://bundles.jito.wtf/api/v1/bundles/tip_floor` at 2026-11-23T04:09Z: p25 1.00075e-6 SOL, p50 1.001e-6, p75 1.001e-6, p95 7.33e-6, p99 1.163e-5, EMA p50 2.38e-6 SOL | Jito endpoint named in the docs above | 2026-11-23 | CHAIN |
| ATA rent — documented | SPL Token ATA 165 bytes → 2,039,280 lamports (0.00203928 SOL); Token-2022 ATA (immutable owner) 170 bytes → 2,074,080 lamports; formula `(account_size + 128) × 3,480 lamports/byte-year × 2 years`; "Do not hard-code these balances… Query `getMinimumBalanceForRentExemption`" | R1 `tokens/basics/create-token-account.mdx`, `core/accounts/index.mdx` | 2026-11-23 | DOC |
| ATA rent — **live mainnet value differs** | `getMinimumBalanceForRentExemption`: 165 → **1,488,440** lamports (0.00148844 SOL); 170 → **1,513,840** lamports (0.00151384 SOL); 0 → 650,240; 82 → 1,066,800. Implies 5,080 lamports per byte × (size + 128). A Token-2022 Pump holder account was observed with exactly 1,513,840 lamports / 170 bytes | R3 | 2026-11-23 | CHAIN — **use these, re-query at runtime** |
| Why it differs | SIMD-0437 "Incrementally Reduce lamports_per_byte to 696": steps 6960 → 6333 → **5080** → 2575 → 1322 → 696, each behind its own feature gate. Live value matches step 2; further cuts possible. (The SIMD file header still says `status: Idea`; activation dates not confirmed.) | `https://github.com/solana-foundation/solana-improvement-documents/blob/main/proposals/0437-incremental-rent-reduction.md` @ `6cf17cb` | 2026-11-23 | DOC (proposal) + CHAIN (value); activation status NOT CONFIRMED |
| Rent is a refundable deposit | "Closing an empty token account transfers all of its lamports, including the minimum storage balance, to the destination specified by the close instruction." | R1 `tokens/basics/create-token-account.mdx` | 2026-11-23 | DOC |
| Other first-trade deposits on Pump | `user_volume_accumulator` "Rent for 137-byte account if missing: 0.0018444 SOL" (figure predates the rent cut: (137+128)×6960 = 1,844,400; at 5,080 it would be 1,346,200 lamports) | S2 `docs/instructions/BUY.md`, `TRADE_V3.md` | 2026-11-23 | DOC + DERIVED |
| Pump bonding-curve trade fee | 1.25% of quote amount (0.95% protocol + 0.30% creator), each rounded up; **+0.45% / 0.40% Platform Fee only if routed through the pump.fun web/mobile app** (from 17 Oct 2026) | section A7 | 2026-11-23 | DOC |
| PumpSwap canonical pool fee | 1.25% at mcap < 420 SOL, stepping down to 0.30% at ≥ 98,240 SOL (table A7); non-canonical pools 0.30% | section A7 | 2026-11-23 | DOC |
| Migration fee | 0.015 SOL, deducted from the curve for SOL coins (not paid by an ordinary trader unless their trade triggers migration of a non-SOL coin) | section A6 | 2026-11-23 | DOC |
| Price impact (model input) | Curve: exact formulas in A4 against virtual reserves; pool: constant product on base vault vs effective quote reserves | section A4 | 2026-11-23 | DOC |

---

## E. Not confirmed from an official source

1. Numeric graduation threshold in USD or SOL — the site only says "graduation threshold"; ≈410.9 SOL / ≈58.8k USDC market
   cap and ≈85 SOL raised are DERIVED from on-chain constants.
2. Date PumpSwap replaced Raydium (~20 Mar 2025) and the name "Project Ascend" — MEMORY only.
3. Official statement that mint and freeze authority are revoked — not in the docs; only observed on-chain (3 new mints + 1 legacy).
4. Meaning of `buyback_basis_points = 5000` (share of the protocol fee vs. of the trade) — inferred from wording, not stated.
5. Any official Pump.fun data API, its rate limits, or permission to call `frontend-api-v3.pump.fun` — none documented.
6. Official list of RPC methods disabled on the public Solana endpoint — none found; `getTokenLargestAccounts` blocked is an observation.
7. Current public-RPC limits: documented (100 / 40 per 10 s) vs observed headers (method-limit 50, rps-limit 250) disagree; windows of the header values unknown.
8. Activation dates/status of the rent reduction (SIMD-0437 step 2) — live value confirmed, governance status not.
9. DEX Screener field definitions (`marketCap`, `fdv`, `liquidity.usd`, `pairCreatedAt`) and any caching/attribution rule — not in docs.
10. GeckoTerminal public-API terms, attribution wording and OHLCV depth on the keyless host — terms pages blocked (403).
11. CoinGecko API terms, Dune terms, SolanaFM terms / key requirement, Solscan Free-plan numeric limits and "retention period".
12. Token-2022 account-type discriminator byte (offset 165) as a holder-scan filter — MEMORY.
13. Whether `fees.png`-era tier boundaries in the on-chain `FeeConfig` exactly equal today's website table — only the bonding-curve tier (95/30/0 bps) was verified on-chain.
