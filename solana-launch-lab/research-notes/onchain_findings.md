# On-chain / market-data findings (my own verification, accessed 2026-11-23 ~03:55–04:40 UTC)
Sources: Solana public RPC api.mainnet-beta.solana.com (getSignaturesForAddress, getTransaction v1, getBlock accounts-mode, getBlockTime);
GeckoTerminal public API (minute/hour OHLCV, token+pools); DexScreener /tokens/v1/solana/{mint}.
Raw responses cached in scratchpad/tokens (rpc_cache/, ohlcv_*.json, dexs_*.json, gt_*.json). Scripts in scratchpad/scripts.

## Identity (exact mints verified; names from DexScreener/GT)
| token | mint | name/symbol | bonding curve acct | PumpSwap pool | creator (fee payer of CreateV2) | creation slot / blockTime UTC |
| BartCoin | CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump | BartCoin / BTC | ACUSZ93rMjtPKGwZFkWa9tBNKjYSCeQeexsJYc84tY41 | 5q1eZo7m3NjacXmSuM8BZZ8iqzGt8eqU9FtqTNus7aoJ | EGGuvXireJ5CVbpBpkAFNFeo3x9yBG16P6ztQGcrYP9n | 471875967 / 2026-11-20 20:45:13 |
| PunaniCoin | 2TngN4B7XaoGSKsYvttq5bFAdM4Z4xCSnuyRwGiFpump | PunaniCoin / PUNANI | 8cDzEmxoB7nfVMuxCpkwVi9VmVAJJfBwrRk8g2wnDK7t | CnZHS2nmRnKWTPwK9okdUSCipbrDDGHpMnpnMNpD4hWA | Ghc6EiuC… | 472004485 / 2026-11-21 04:26:25 |
| Maya The Samoyed | FJKt1LxbWBpTRt9BaDEB6Wr2qL5LZzjFF5sx8rXnpump | MAYA | 2WA1EaQnEZ7qnouPmzpwutXdrexiG3LH1Lqt7ykpxRcS | 51edMriYsoN7MWtgQxAYsoG4z9nnVhVUUpbuyY1EPCbo | EcgSRNT8… | 472015921 / 2026-11-21 05:07:34 |
Launch times in the post (20:45, 04:26, 05:07 UTC) MATCH on-chain creation blockTime to the minute. Year = 2026.
Token program: Token-2022 (TokenzQd…). Tx version 1 (need maxSupportedTransactionVersion:1). Slot time ≈ 0.218 s.

## Launch structure (identical template in all three) — all in the creation slot
- tx1 CreateV2 + BuyV3: creator + 4 co-signers buy 16.69M (BART) / 16.0M (PUNANI) / 13.95M (MAYA) tokens
- tx2 BuyV3 x7 co-signers: 181.23M / 172.65M / 183.74M tokens (curve +6.36 / +5.99 / +6.43 SOL)
- tx3 BuyV3 x7 co-signers: 595.18M / 604.44M / 595.42M tokens (curve +78.83 / +79.21 / +78.84 SOL)
- tx4 MigrateV2 signed by creator + 1 more signer: curve's 206.9M tokens + 85.005 SOL -> PumpSwap CreatePool; LP minted then BURNED in same tx;
  InitBoost moves exactly 17.584505288 WSOL from pool quote account to a separate per-pool vault; then co-signer buys from the pool with
  ~18.2 SOL: 36.12M / 36.01M / 51.29M tokens.
=> 19 co-signing wallets bought 793.1M tokens (79.31% of 1B supply = the ENTIRE curve) in the creation slot for ~85 SOL (~$5.7K);
   with the migration co-signer: ~829.2M (82.9%) BART, ~829.1M (82.9%) PUNANI, ~844.4M (84.4%) MAYA held by 20 wallets after slot 0.
   Bonding-curve phase lasted < 1 second; GeckoTerminal has exactly ONE minute candle for the pump-fun pool (vol ≈ $5.1–5.6K).
   Token amounts per wallet nearly identical across the three tokens (e.g. 1.41M/2.11M/2.80M/4.17M in tx1 of BART and PUNANI) -> same launch script.
- Pool pricing: effective quote = real WSOL balance + 17.5845 SOL boost (verified: (2.34+17.58)/971.82M = 2.05e-8 SOL = DexScreener priceNative 2.062e-8).
  Post-migration-tx mcap (price*1e9): BART 603.8 SOL ≈ $40.8K; PUNANI 602.9 SOL ≈ $39.6K; MAYA 727.6 SOL ≈ $47.9K.

## Market cap (price x 1e9 supply, USD) at claimed alert time — on-chain pool state (real+boost) vs claim
| token | claimed alert (UTC) | claimed mcap | on-chain at alert+0s | +30s | +59s | GT alert-minute O/H/L/C | launch+3..10s on-chain |
| BART | 11-20 20:52 | ~$58K | $497,342 (7359 SOL) | $538,317 | $563,061 | 491.7K/576.8K/441.8K/554.9K | $291K |
| PUNANI | 11-21 04:39 | ~$50K | $303,721 (4620 SOL) | $337,199 | $351,363 | 306.2K/372.4K/262.0K/347.6K | $238K |
| MAYA | 11-21 05:19 | ~$75K | $766,853 (11637 SOL) | $828,575 | $887,620 | 768.7K/916.2K/726.9K/900.6K | $247K |
SOL/USD used: 67.58 / 65.74 / 65.90 (GT usd price ÷ GT SOL price in the alert minute).
=> claimed alert mcap is 8.6x / 6.1x / 10.2x BELOW the on-chain mcap at the stated alert time. A ~$50–75K mcap existed only within ~1–2 s of launch.

## Peaks (GeckoTerminal minute candles, pumpswap pool)
| token | peak high mcap | peak time UTC | peak ÷ alert-minute close | peak ÷ on-chain alert+0s | peak ÷ claimed mcap | claimed multiple | claimed implied peak |
| BART | $2,035,864 | 11-20 21:40 (+48 min) | 3.7x | 4.1x | 35.1x | 24x | $1.39M |
| PUNANI | $3,909,030 | 11-21 19:02 (+863 min) | 11.2x | 12.9x | 78.2x | 58x | $2.90M |
| MAYA | $4,127,245 | 11-21 16:52 (+693 min) | 4.6x | 5.4x | 55.0x | 50x | $3.75M |
Minutes with close >= 10x alert-minute close: BART 0, PUNANI 1, MAYA 0. >=20x: 0 for all.
On-chain mcap at first second of GT peak minute: BART $1.84M, PUNANI $3.27M, MAYA $3.73M.

## Now (2026-11-23 ~03:56 UTC, DexScreener): mcap BART $1,444; PUNANI $1,853; MAYA $1,630 (≈ -99.9% from peak, ≈ -99.6..-99.8% from alert-time mcap).
Pool BART latest tx 11-22 21:20: base 971.82M (97.5% of supply back in pool), real quote 2.34 SOL. liquidity.usd per DexScreener $1,572.
Hourly: BART $764K at 00:00 → $368K 01:00 → $96K 05:00 11-21; PUNANI and MAYA held $2–3.8M through 11-21 then → ~$1.7K by 11-23.
BART pool signatures: >150,000 in ~42 h, steady ~325 tx/min for hours (bot-like uniformity), 11.8% failed.
Sum of minute volume: BART $1.20M (872 min), PUNANI $2.49M (first 1000 min), MAYA $1.95M (first 1000 min).
Thin liquidity: moving BART from ~$41K to ~$537K mcap in the first minute took only ≈$19.6K of volume.

## Slot-0 (bundle) wallets afterwards (bundle_wallets.json; accessed 2026-11-23 ~04:20 UTC)
- All 20 slot-0 wallets per token now hold 0.00 tokens (BART, PUNANI, MAYA) => they sold/transferred everything.
- Largest wallets start post-launch activity at +0.3..+1.0 min; staggered schedule (bigger wallets first, small wallets at +830..+1300 min).
- Decoded samples (BART): wallet 7rgKbsXA… PumpSwap `Sell` -1.138M tok/+9.26 SOL at 20:46:10; -1.417M/+11.58 SOL at 20:52:17;
  -1.743M/+13.95 SOL at 20:52:51 (inside the claimed alert minute 20:52), each followed seconds later by a SOL transfer OUT of the same amount.
  wallet 8HWDXW2h… Sell -2.448M/+14.93 SOL at 20:51:14; -1.635M/+13.13 SOL at 20:52:22; -1.286M/+10.46 SOL at 20:53:02.
  => launch insiders were selling into the market during the claimed alert minute.
- Funding: MAYA: 20/20 wallets first seen 3 s before launch, same first-tx fee payer Dcfvi7aD… (one funder).
  BART wallets first seen 2026-11-16 02:43–02:48; PUNANI wallets first seen 2026-11-19 16:10–16:16; first-tx fee payers overlap ACROSS the two tokens
  (A77HErqt…, iGdFcQoy…, 8DfHuYFv…, F7p3dFrj…, ABNL41Sw…, APhyMCpY…, BmFdpraQ…, DScDQ1zV…) => BART and PUNANI launches share funding infrastructure
  (probabilistic link: same operator or same launch service; co-signing of the same tx is hard evidence of coordination within one token).
- QuantOrb repo's own published Guard threshold: rules/limits.js:16 `slot0Max: 0.30  /* HELD if 30% or more of supply was bought in the launch slot */`.
  On-chain: 79.3% of supply bought on the curve in the launch slot (82.9–84.4% incl. the migration-tx buy) for all three showcased tokens.
