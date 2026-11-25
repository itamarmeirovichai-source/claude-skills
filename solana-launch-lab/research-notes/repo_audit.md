# QuantumOrb / quantorb — read-only due-diligence notes

Audit date: 2026-11-23 (UTC). Auditor ran no repository code (no npm/node/python on repo files). Only Read/Grep, `wc`, `git log`, `git fetch` (history only), curl/Playwright against the public website, and two public market-data APIs.

Legend: **[READ]** = directly read by me in the file/page cited. **[INFER]** = my inference. **[2ND]** = second-hand (WebFetch/WebSearch summary by a small model, not raw text).

Repo: `/home/user/quantumorb/quantorb`, origin `https://github.com/QuantumOrb/quantorb` (README spells it `QuantumOrb/QuantOrb`), HEAD `cb61b091` (2026-11-05 16:28:14 +0100). 78 tracked files, 21,515 "lines" by `wc` including binary PNGs.

Evidence files saved next to this note (all in `/tmp/claude-0/-home-user-claude-skills/f0c43923-e51b-5ffb-bff6-ddef9f7ca9b2/scratchpad/research/`):
- `site_home.txt` — rendered homepage innerText + links + network requests + websocket frames (Playwright, 2026-11-23T03:57:19Z)
- `site_home_raw.html`, `site_home_rawhtml_text.txt` — raw HTML via curl (2026-11-23T03:56:49Z) and tag-stripped text incl. sections hidden until a tab is opened
- `site_how.txt` (`/#how`, 03:58:46Z), `site_radar.txt` (`/#radar`, 03:58:56Z), plus `site_*.png` screenshots
- `site_api_snapshots.txt` — `/api/pulse`, `/api/stats/checks`, `/api/recent`, `/api/tape`, `/api/alerts/recent`, `/api/launches`, `robots.txt` (curl, 03:57:33Z)
- `site_roadmap.txt` — roadmap array extracted from the site JS bundle; `site_app_bundle_js.txt` — the bundle as text (not executed by me outside the headless browser)
- `ext_dexscreener_token_2026-11-23T0359Z.json`, `ext_geckoterminal_token_2026-11-23T0359Z.json` — public market data for the token mint printed in the repo

---

## Q1. What is in the public repo

Git history **[READ]**: complete after `git fetch --depth=200` (`git rev-parse --is-shallow-repository` = false). 21 commits, single author `QuantumOrb <QuantumOrb@users.noreply.github.com>`, root commit `399c72e` 2026-10-22 20:22:51 +0200 "QuantumOrb: the new site"; last `cb61b09` 2026-11-05. Commits land in same-second batches (e.g. six commits at 2026-11-05 16:28:13–14), i.e. scripted/squashed publication, not incremental development history. No tags, one branch.

| Dir | Language | Files / approx lines | Purpose (as read) |
|---|---|---|---|
| `rules/` | JavaScript | 9 `.js` = 316 lines (+45-line README) | Pure functions: score (`score.js` 55), verdict pipeline (`verdict.js` 48), thresholds (`limits.js` 27), operator grouping (`operators.js` 28), Guard (`guard.js` 60), Shield (`shield.js` 44), formatters, CLI printer (`cli.js` 35) |
| `chain/` | JavaScript | `solana.js` 147, `util.js` 93 | Program IDs, PDA derivation, account decoders (pump.fun curve, PumpSwap, Raydium CPMM, Metaplex, Token-2022 mint), a parsed-transaction reader, base58, TTL cache. No network calls. |
| `market/` | JavaScript | `pools.js` 140 | Normalises DexScreener/GeckoTerminal pool JSON, picks the price pool, aggregates volume/liquidity, market cap vs FDV. No fetching. |
| `bot/` | Python | `formatting.py` 402, `solana_util.py` 183, `shield.py` 18; tests 156 | Telegram message formatting (HTML strings), curve parsing/price/progress, serial-creator rule. No handlers, no network. |
| `test/` | JavaScript | 7 test files = 547 lines; fixtures 1,372 lines JSON | Unit tests (node:test) |
| `examples/` | JSON | 12 files = 1,285 lines (+README 50) | Scan *inputs* with embedded expected outputs |
| `docs/` | Markdown | 269 lines | architecture, scoring, guard |
| `assets/` | PNG | banner + 18 screenshots | README images |
| `.github/` | YAML | 102 lines | CI workflow + issue templates |
| root | — | README 278, CHANGELOG 93, LICENSE 20, SECURITY 19, package.json 16 | |

Total hand-written code ≈ 1,300 lines JS + ≈ 600 lines Python (excluding tests). `package.json:15-16` has no dependencies; `"private": true`.

README's own framing **[READ]** `README.md:178`: "About a tenth of QuantumOrb's code is open here: everything that decides a verdict".
Unverifiable claim **[READ]** `README.md:179-180`: "Each file is the server's or the bot's own code, not a rewrite" — the server is closed, so nothing in the repo can confirm the hosted service runs this code.

## Q2. What the repo says is closed / missing

- `README.md:217-222` "What stays closed": "Which accounts and transactions a scan asks for, in what order and under what budget; finding the links between wallets; the launch stream; the Radar; the site and its API; the bot's commands, alert loops and database; every data source's keys, limits and fallbacks; the servers."
- `README.md:221-222`: "That is what it takes to run QuantumOrb, and it is not in this repository."
- `docs/architecture.md:102-109` table, closed column: "Holders' entries and histories, and finding links between wallets"; "The launch stream, the Radar and the 1,000-launch grid"; "Fetching market data: requests, limits, caches and fallbacks"; "The bot's commands, alert loops, launch stream and database"; "The site, the API, the servers and every key and setting".
- `rules/operators.js:4`: "Finding the links on the chain is the closed part of the scanner."
- `rules/verdict.js:4-5`: "What the scanner reads from the chain to fill this input ... is the closed part."
- `rules/README.md:43-45`: "Everything that fills the input: reading the top holders from the chain, how each wallet got in, which ones are fresh or snipers, finding the links between them".
- `bot/README.md:18-19`: "What is not here: the command handlers and keyboards, the alert loops, the launch stream, the data sources and their fallbacks, the database."
- `chain/README.md:21-22`, `market/README.md:22` say the same for request ordering and fetching.
- `LICENSE:15-16`: "The rest of the QuantumOrb software (the scanner, the site, the Telegram bot and their infrastructure) is not published in this repository".
- ML: not mentioned anywhere as existing or closed (grep for machine learning/model/neural/probab/classifier: no hits in `.js/.py/.md`).

**[INFER]** The repo is a verdict calculator plus decoders. Every hard part (data collection, wallet-history classification, link detection, the launch stream, alerting, the hosted service) is closed. The open rules cannot be run on a real token without re-implementing the closed collection layer.

## Q3. Scoring: fixed rules, no ML

`README.md:67`: "The score is a fixed, written set of rules, not a black box." Code confirms: deterministic arithmetic only, no learned parameters, no randomness **[READ]**.

### Five weighted parts (`rules/score.js:8-10`, `docs/scoring.md:11-17`)
Each = weight × linear ramp, full at first mark, zero at second; parts rounded to 0.1, total to an integer (`score.js:10,27`).

| Part (key) | Weight | Full at | Zero at | Input required (all supplied by the closed scanner) |
|---|---:|---|---|---|
| Biggest operator (`operator`) | 35 | price drop ≤ 10% | ≥ 60% | `impact(big.weighted × floatTokens, reserveTokens)`; needs operators (from `links`), `floatTokens`, `reserveTokens` (`score.js:12,18`) |
| Fresh wallets (`virgin`) | 25 | ≤ 10% | ≥ 80% | share of *read, non-dev* top wallets flagged `virgin` (`score.js:19,22`) |
| Received, not bought (`transfer`) | 20 | ≤ 1% | ≥ 10% | sum of `share` where `kind === 'transfer'` (`score.js:23`) |
| Unsold snipers (`sniper`) | 10 | ≤ 1% | ≥ 15% | sum of `share` of non-dev holders with `sniper && !sold`; sniper = bought in first 30 s (`score.js:24`, `examples/README.md:46-47`) |
| Top-20 share (`concentration`) | 10 | ≤ 25% | ≥ 70% | sum of all holder shares (`score.js:20`) |

Price impact (`score.js:12`, `docs/scoring.md:31-35`): `drop = 1 − (R/(R+q))²`, a fee-less constant-product sale. `examples/README.md:48`: "Only the ratio of `reserveTokens` to `floatTokens` matters."

Bands (`score.js:39`): CLEAN ≥ 80, OK 60–79, RISKY 40–59, DANGER < 40.

### Hard red flags → DANGER regardless of number (`score.js:29-31,39`)
1. biggest operator has > 1 wallet and impact ≥ 0.5
2. `virgin ≥ 0.8` of read wallets
3. `transfer ≥ 0.10` of float

Consequence **[READ]**: the numeric score can be high while the band is DANGER (`examples/all-fresh-wallets.json:80-81` score 65 / DANGER; live site showed "$ZCRYPT DANGER 70").

### Caps → score min(total, 59) (`score.js:32-38`)
- any pack, or proven operator with ≥ 3 wallets (`score.js:32`)
- single holder with impact ≥ 0.5 (`score.js:33`)
- `liquidityUsd < 1000` when known (`score.js:34`, `limits.js:8`); unknown liquidity never caps
- ≥ 3 unread wallets with share ≥ 0.2% → state `partial` (`score.js:36`, `verdict.js:41-43`, `limits.js:7`)

### No-score states (`rules/verdict.js:27-38`, `limits.js:6,9-11`)
- TOO ESTABLISHED: `ageDays > 30 && liquidityUsd > 500000 && (mcap || fdv) > 10,000,000`
- TOO EARLY: fewer than 10 holders outside curve/pools

### Sell scenario (`score.js:40-50`)
Only on DANGER and only if drop ≥ 40%. `docs/scoring.md:74-75`: "It is a scenario, not a forecast, and it never changes the score."

### Guard — three checks (`rules/guard.js`, `limits.js:13-18`, `docs/guard.md:40-44`)
- Creator history, chain record: held if `launched ≥ 10 && graduated×100 < 10×launched` (`guard.js:21-25`). Fallback on server's own record: `launched ≥ 10 && alive/launched < 0.2`, usable only as evidence against (`guard.js:28-32`).
- First-slot buyers: held if share of supply bought in launch slot ≥ 0.30 (`guard.js:38-41`).
- Dev holdings: held if dev holds ≥ 0.15 of supply (`guard.js:43-47`).
- Tri-state: `ok: null` = not read; `pass` = no failed check, `pending` set if any null (`guard.js:49-53`).

### Shield — two checks (`rules/shield.js`, `limits.js:22-26`, `bot/shield.py:15-18`)
- Serial creator: `launched ≥ 10 && graduated×100 < 10×launched` (`shield.js:19`).
- Dev at launch: held if `devAtLaunch / supply ≥ 0.15`, supply default 1e9 (`shield.js:34-39`).
- Zero launches is "unavailable", not a pass (`shield.js:29`).

### "85+/100" and "passed every check"
**[READ]** Neither exists. Grep of repo for `85+`, `85/100`, `passed every`, `every check` returns nothing. Thresholds in code are 80/60/40 only. The only other score threshold is roadmap item 18 (planned): `README.md:173` "a live list of fresh tokens scoring 90+ in the bot". "Passed every check" is not a defined state; the nearest constructs are `guard.pass` and an empty `gates` array.

### Wallet clusters ("operators") — `rules/operators.js`, `docs/scoring.md:37-48`
- The open code does **not detect** clusters. It consumes a pre-computed `links` array `[{a, b, kind, level: 'proven'|'pack'}]` (`operators.js:7`) and groups it.
- Proven links → union-find merge, transitive (`operators.js:9-14`). Link kinds seen in examples/tests: `same_tx`, `direct`, `distributor`.
- Packs → members not already in a proven group; share weighted ×0.6 (`operators.js:17-21`).
- Docs describe detection heuristics in prose only: `docs/scoring.md:41-42` "the same buy transaction, tokens from the same ordinary wallet, direct transfers between holders"; `docs/scoring.md:44-46` "3 or more fresh wallets that entered within a couple of slots with amounts within ±30% of each other. A pack is behaviour, not proof".
- Site adds one detail not in the repo: "any address with 100 or more outgoing transfers are never used as a link" (`site_home_rawhtml_text.txt:271`).
- The word "probabilistic" is never used. Docs call links "proven" and packs "behaviour, not proof". Hedges: `README.md:268` "It sees wallets, not people. Two wallets of one person with no on-chain connection look independent."; `README.md:271-272` "The score is an automated, subjective assessment by a fixed set of criteria, on public data that can be incomplete."
- **[INFER]** "Proven" overstates it: a shared buy transaction or common funder is a heuristic, not proof of common control.

### Code/doc inconsistencies noticed **[READ]**
- Docs say a pack is 3+ wallets; code accepts 2 after proven members are removed (`operators.js:18` `w.length >= 2`; `test/operators.test.js:32-38`).
- Site `/#how` Guard text still says creator history is held when "fewer than 1 in 5 are still alive" (`site_home_rawhtml_text.txt:293`); repo docs say "under 10% of them graduated" (`docs/guard.md:42`). `examples/site-example.json:155-158` still uses the older `{launched: 65, alive: 1}` shape.
- `CHANGELOG.md:69-70` says ATH and latest trades are gone; `bot/formatting.py:212-214,314-332` still formats them.

## Q4. Transaction signing / key handling / trade execution

Grep over all text files for `sendTransaction|signTransaction|sendRawTransaction|signAllTransactions|Keypair|secretKey|privateKey|mnemonic|wallet adapter|jito|bundle|swap|jupiter|buy(|sell(|sign(|nacl|@solana|solders|anchorpy` **[READ]**:
- No signing, no key material, no transaction construction or submission, no RPC client, no HTTP client, no websocket client, no `process.env`/`os.environ`, no `child_process`/`subprocess`/`eval`.
- Hits are benign: program-ID constants incl. `JUP6` and `JUP_LOCK` (`chain/solana.js:22,24`) used only to label infrastructure accounts and to detect "a swap happened" in a parsed transaction (`chain/solana.js:45-46,127`); `bundle` is a boolean holder flag meaning "bought in the launch slot" (`rules/verdict.js:12,15`; `score.js:44`); ed25519 appears only as an on-curve test for PDA derivation (`chain/util.js:31-46`, `bot/solana_util.py:81-90`).
- "Guard" and "Shield" are pure functions that return `{pass, reason, checks, pending}` objects (`rules/guard.js:49-58`, `rules/shield.js:42`). They screen/label launches. They do not block, buy, sell, or protect funds.
- Stated posture: `README.md:267` "QuantumOrb only reads public on-chain data. It never asks for keys or seed phrases and never touches funds."; `SECURITY.md:3-4`.
- Site JS bundle: no wallet-connect, `window.solana`, Phantom/Solflare or signing strings (grep of `site_app_bundle_js.txt`).

**[INFER]** Nothing in the public code can execute a trade, so no PnL can originate from this code. The closed bot/server cannot be inspected.

## Q5. Tests and CI

`.github/workflows/test.yml` **[READ]**: triggers on push to `main` and pull requests; `permissions: contents: read`; job `js` on Node 18/20/22 runs `npm test` (= `node --test`, `package.json:12`) then `node rules/cli.js examples/site-example.json` (`test.yml:23-24`); job `bot` on Python 3.11/3.12/3.13 runs `python -m unittest discover -s bot/tests -v` (`test.yml:37`). No secrets, no network, no deploy.

What the tests do **[READ]**:
- `test/score.test.js` (151 lines): weights sum to 100, ramp endpoints, impact formula, bands, each red flag and cap, unread handling, dev exclusion, scenario gating, early/established — all on synthetic holder arrays (`score.test.js:7-10`).
- `test/operators.test.js`, `guard.test.js`, `shield.test.js`: threshold edges.
- `test/examples.test.js`: each `examples/*.json` must reproduce the `expect` block stored in the same file (`examples.test.js:16-33`).
- `test/chain.test.js`: PDA derivation for 34 mint→curve pairs (`test/fixtures/curve-vectors.json`), base58, decoders on hand-built buffers, `readTx` on a hand-built transaction (`chain.test.js:27-36,69-76`).
- `test/market.test.js`: pool-selection logic on one fixture.
- `bot/tests/test_open.py`: same 34 PDA vectors, curve parse on a synthetic account, Shield rule parity, message formatting.

What they do NOT establish **[READ + INFER]**:
- No evidence of predictive performance: no labelled outcomes, no rug/non-rug dataset, no backtest, no hit rate, no false-positive/negative rates, no returns, no PnL. Grep for `backtest|PnL|profit|win rate|ROI|accuracy|return` in docs: nothing relevant.
- Nothing about link-detection accuracy (closed) or classification of fresh/sniper wallets (closed).
- "Parity with the server" is self-referential: expected values sit in the same JSON files; nine come from "the simulated chain", three are "Made up for one rule" (`examples/README.md:9-19`).
- Fixture realism: README/CHANGELOG say "real market data" (`README.md:234`, `CHANGELOG.md:19-20`), but `test/fixtures/ant-pumpswap.json` uses placeholder addresses such as `AntAnthrpPumpSwapPoo11111111111111111111111` (line 25), `AnthrpQuoteMint1111111111111111111111111pump` (line 3), `FakeAntSameNamePoo…` (line 323). At minimum it is edited/constructed.
- The 34 "real" vectors are deterministic PDA derivations; they prove the hash math, not chain reads.
- CI passing says nothing about the hosted service.

## Q6. LICENSE

`LICENSE` (20 lines) **[READ]**: custom proprietary, source-available notice. Not MIT/Apache/GPL, not OSI open source. `package.json:7` `"license": "SEE LICENSE IN LICENSE"`.

- `LICENSE:2`: "Copyright (c) 2026 QuantumOrb. All rights reserved."
- Purpose `LICENSE:4-5`: "is published so that it can be read and so that anyone can check how QuantumOrb turns a scan into a verdict."
- Grant `LICENSE:7-8`: "You may view this repository, link to it, and run the code in rules/, test/ and examples/ to check QuantumOrb's verdicts."
- Prohibition `LICENSE:10-12`: "You may not, without prior written permission from the copyright holder: copy, modify, merge, publish, distribute, sublicense or sell any part of this repository, or use the code in it in another product or service"
- `LICENSE:13`: "use the screenshots, names or brand of QuantumOrb in another product or service."
- `LICENSE:18-20`: as-is, no warranty, no liability, "NOTHING HERE IS FINANCIAL ADVICE."

Result: reuse, modification, redistribution, commercial use and derivative works are all prohibited without written permission. Even running is granted only for `rules/`, `test/`, `examples/` — not `chain/`, `market/`, `bot/`. Yet the roadmap calls this "Open Source" (`README.md:162`) and the README says "Open code" (`README.md:176`). **[INFER]** Any reimplementation must be clean-room: ideas and public protocol facts only, no copied code, text, screenshots or branding. (Not legal advice.)

## Q7. Screenshots, sample data, disclaimers

- `README.md:276-277`: "The screens of the site come from a development build running on a simulated chain, and the bot's messages are shown on made-up data, so every token, wallet and figure on them is made up."
- `assets/README.md:6-8`: "The site's screens come from a development build running on a simulated chain, so every token, wallet and figure on them is made up."
- `README.md:123`: "The messages below are the bot's own, on made-up tokens and wallets."
- `examples/README.md:21-24`: "Every token, wallet and figure in them is made up: the simulated chain is a test double the server is developed against."
- `examples/README.md:17-19`: three files "Made up for one rule".
- `examples/site-example.json:4`: "The made-up token the home page uses".
- Screenshot `assets/screens/home.png` **[READ as image]**: counters "SCANS 24H 7 · OPERATORS FOUND 4 · DANGER VERDICTS 3 · LAUNCHES 31 · HELD BY SHIELD 7 · ALERTS SENT 0", tokens $NEBCAT/$TINYPUP/$GIGACHAD/$CTO/$BUSYBEE/$LUXBIT/$GRUMPKIN = the simulated examples.
- Screenshot `assets/screens/bot-start.png` **[READ as image]**: "/scan — on-chain intelligence: hidden ownership, wallet clusters, capital flows" under "Coming soon"; footer "Research, not financial advice."

Disclaimers:
- `README.md:263`: "The token is not an investment product and nothing here is financial advice. Do your own research."
- `README.md:269`: "A CLEAN score is not a promise. Liquidity, sentiment and the dev's off-chain plans are outside what it can read."
- `README.md:271`: "Nothing here is financial advice or a call to buy, sell or hold."
- `bot/formatting.py:242-243`: "It can be wrong, and a pass doesn't make a token safe."
- `LICENSE:20`.
- The phrase "no guarantee" does not appear; "not a promise" and "can be wrong" are the equivalents.

## Q8. Token, paid plans, token-gating, referrals, bot

### Own token **[READ]**
- `README.md:249-253`: "**The QuantumOrb token** on Solana, launched on pump.fun. The only official contract address:" `EiN69j8KVE5uYKheVkeVwptEVwRP5JtDhJDMGm1ppump`; links to pump.fun, DexScreener, Solscan (`README.md:255-257`).
- Same mint in `SECURITY.md:12` and `CHANGELOG.md:9-10`.
- HEAD commit message: "Full release: the Telegram bot, the official token, the roadmap and the open code".
- Roadmap `README.md:159-164`: "Token Launch … ✅ Done", "DexScreener Profile … ✅ Done", "Token Burns | Part of the token supply is burned | ✅ Done", "Holder Airdrops | Airdrops for QuantumOrb token holders | ✅ Done".
- The ticker is **not printed anywhere in the repo** (grep `QORB`: no hits). Ticker **QORB** comes from DexScreener and GeckoTerminal for that mint (accessed 2026-11-23T03:59:01Z): name "QuantumOrb", symbol "QORB", PumpSwap pair `HAc2f4zE9jTWGAzJAg7juZHCaqNE6dU4XzZb6HiLeMKq`.
- The website's HTML and JS bundle do **not** contain the mint, "QORB", a pump.fun link or an X link (grep). On the site the token appears only as roadmap labels (TOKEN LAUNCH, DEXSCREENER PROFILE, TOKEN BURNS, HOLDER AIRDROPS) and tooltips (`site_roadmap.txt`): "Part of the token supply is burned. Mechanics announced before the first burn."

### Token market state (public APIs, 2026-11-23T03:59:01Z) **[READ]**
- DexScreener: `priceUsd 0.000001505`, `fdv 1383`, `marketCap 1383`, `liquidity.usd 1494.61` (2.159 SOL + 893,620,855 QORB in the pool), `volume.h24 1.81`, `txns.h24 {buys: 0, sells: 1}`, `pairCreatedAt 1793819721000` = 2026-11-04T19:15:21Z. Profile socials listed there: `https://x.com/QuantumOrbApp`, `https://t.me/QuantumORB_bot`, `https://quantumorb.app/`, `https://github.com/QuantumOrb`.
- GeckoTerminal: `fdv_usd 1507.70`, `volume_usd.h24 1.82`, `normalized_total_supply 1000000000.0`, launchpad `completed_at 2026-11-04T19:15:21.000Z` (graduated to that PumpSwap pool).
- **[INFER]** ~89% of the 1B supply sits in the pool and FDV is ≈ $1.4–1.5K nineteen days after graduation: the project's own token has collapsed to near zero with essentially no trading. Supply still reads exactly 1,000,000,000, so the "Token Burns ✅ Done" claim is not reflected as a reduced mint supply (burns via an incinerator address would not show here; unverified either way). Airdrops unverified.
- **[2ND]** WebSearch snippet for solanacompass.com listed ~180 holders, top-10 concentration ≈ 58.85%, top-25 ≈ 78.69%, price $0.000015 (stale vs DexScreener). Direct fetch returned HTTP 403.

### Paid plans / token-gating
- Nothing is sold today. `README.md:103`: "free for everybody." `README.md:270`: "Five new scans a day per person."
- Planned: `README.md:173` "Pro Subscription | No scan limits, and a live list of fresh tokens scoring 90+ in the bot | Planned"; `README.md:168` "Higher Free Limits … Planned". No price stated anywhere.
- No token-gated feature in repo or site JS. The only holder benefit claimed is airdrops.
- No pricing/terms/privacy pages: `/pricing`, `/terms`, `/privacy`, `/docs`, `/roadmap`, `/token`, `/about`, `/faq` all return 404 (`site_api_snapshots.txt`).

### Referral links
- None found. Site "WATCH" links are Telegram deep links `https://t.me/QuantumORB_bot?start=w_<mint>` (`site_home.txt:523-532`) — a watch command, not a referral code. Bot messages link to pump.fun/Solscan/DexScreener without ref parameters (`bot/formatting.py:172-178`).

### Telegram bot
- `README.md:101-116`: `@QuantumORB_bot`, commands `/alerts /watch /follow /dev /token /new /list`; `/scan` is "*on the roadmap*" (`README.md:116`).
- Site counter at access time: "ALERTS SENT · 24H 0" and `/api/alerts/recent` returned `[]`.

### Incentives **[INFER]**
- The operator issued a pump.fun token and markets burns/airdrops to holders; attention to the scanner (stars, X posts, bot users) is the only visible driver of token demand. That is a direct incentive to publish impressive statistics or profit claims.
- A planned Pro tier selling "fresh tokens scoring 90+" would monetise the score as a buy signal, in tension with "not a call to buy" (`README.md:271`).
- The serial-creator screen applies to pump.fun creators; the project is itself a pump.fun token issuer.

## Q9. Website (accessed 2026-11-23, 03:56–03:59 UTC)

Single-page app on Cloudflare; title "QuantumOrb Scanner"; views `#scan`, `#radar`, `#how`, token pages `#t-<mint>`. curl returns the full static HTML (104,208 bytes); numbers are filled by `/api/*` and `wss://quantumorb.app/ws`.

### Homepage claims **[READ]** (`site_home.txt`)
- "MEMECOIN HOLDER SCANNER · SOLANA — 20 wallets can be 4 people. See who really holds it."
- "Paste a token address. In about ten seconds you see who really holds it, how far the price falls if they sell, and what the owner can still change."
- Counters at 03:57:19Z: SCANS · 24H **87** (4 / hour); OPERATORS FOUND · 24H **18**; DANGER VERDICTS · 24H **11** (13% of scans); LAUNCHES · 24H **8,478**; HELD BY SHIELD · 24H **5,047**; ALERTS SENT · 24H **0**. Check cards: WALLETS READ · 24H **1,302**; EARLY BUYERS TRACKED **1,731**. Last 1,000 launches: on the curve 989, graduated 11, launches/min 6.6.
- `/api/pulse` 14 s later: `{"scans24h":87,"operators24h":18,"danger24h":11,"launches24h":8479,"held24h":5047,"alerts24h":0,"avgScanSec":10.8,"grads1h":3}`.
- Radar view at 03:58:56Z: "HELD BY SHIELD 72% of the last 1,000 launches".
- Recently scanned (12 rows): e.g. `$ZCRYPT CLEAN 94` (01:45Z) → `CLEAN 85` (03:34Z) → `DANGER 70` (03:52Z); `$OTR CLEAN 87`; `$bill CLEAN 82`; two EARLY rows with "0 wallets hold this token outside the curve".
- Footer: "© 2026 QuantumOrb · read-only, never asks for keys or funds"; "Not financial advice. The score is an automated read of public on-chain data and can be wrong; a CLEAN token can still fall."
- `/#how` disclaimer (`site_home_rawhtml_text.txt:189`): "A good score does not mean a token is safe, and a bad one does not mean it will fall."

### Live vs static
- Live: counters changed between two reads 14 s apart (8,478 → 8,479); websocket pushed `launches`, `tape`, `token-updates` frames; recent-scan timestamps were minutes old. **[INFER]** Rolling 24-hour windows from the operator's own API; I could not independently verify they reflect real activity.
- Static/made-up: "SCAN REPORT · EXAMPLE TOKEN" (the GRUMPKIN example, score 12 DANGER) and the operator-map replay.
- Randomly generated in the browser: the "WHAT IT SENDS · EXAMPLE" bot messages (e.g. "$TURGIX graduated … +86% since you started watching", "best one reached $2.45M") are built with `Math.random` in the JS bundle. They are labelled EXAMPLE but include invented gain figures.
- The HTML carries a hidden demo mode: badge "DEMO DATA backend not connected", `title="Generated sample until the backend is connected"`, `aria-label="Demo: data on this site is generated"`; page config at access time was `"demo":false`.

### Roadmap on site (`site_roadmap.txt`)
19 items, same as `README.md:154-174`. Done (1–9): GitHub, Solana Scanner Live, X Account, Token Launch, Telegram Bot, DexScreener Profile, Open Source, Token Burns, Holder Airdrops. Up next (10): 6 New Languages. Planned (11–19): Scanner in Telegram, Faster Scans, Higher Free Limits, Rug Risk Alerts, Operator Memory, Rug Replay, Smarter Radar, Pro Subscription, New Chains (Robinhood Chain, Base, BNB Chain). No dates, no prices.

### Pricing / token on site
No pricing. Token contract not shown on the site. Daily limit text in JS: "Each person can run 5 new scans a day."

### Comparison with the X post
Claimed: "3,825 launches tracked, 82,540 holders analyzed, 185 wallet clusters detected, 19 tokens passed every check scoring 85+/100, +$10,847.63 in 21 days".

| X-post figure | Site at 03:57Z | Match? |
|---|---|---|
| 3,825 launches tracked | 8,478 launches in the last 24 h alone | No |
| 82,540 holders analyzed | 1,302 wallets read · 24 h | No such counter |
| 185 wallet clusters detected | 18 operators found · 24 h | No such counter |
| 19 tokens passed every check scoring 85+/100 | no such metric; bands at 80/60/40; "90+" only in planned Pro | No |
| +$10,847.63 in 21 days | nothing | No |

- **[READ]** None of these strings or numbers appear in the repo, the rendered site, the raw HTML, the JS bundle or the API responses (grep for `3,825|82,540|10,847|85+|passed every|holders analy|launches tracked|21 days|profit|pnl|win rate|ROI`: zero hits).
- **[READ]** The site shows only rolling 24-hour counters, no cumulative totals, so the X figures cannot be reconciled with it.
- **[READ]** No performance claim, PnL, track record, backtest, trade log or wallet address of a trading account exists anywhere in the repo or on the site. The product is described as read-only and has no trading function.
- **[INFER]** Timing: the site went public 3 Nov 2026 (`CHANGELOG.md:23`), 20 days before this audit; the token graduated 4 Nov. A "21 days" profit window would span the entire public life of the product. The X post itself could not be retrieved (x.com returned HTTP 402), so its exact wording, date and author are unverified.

## Q10. CHANGELOG, age, data sources, curve math, market cap

`CHANGELOG.md` has dated entries, no version numbers (only `package.json:3` `"version": "1.0.0"`; no git tags):

| Date | Entry (line) |
|---|---|
| 21 Oct 2026 | "the site on live data" (`:84`) |
| 22 Oct 2026 | "the repository starts over" (`:74`) — "This repository is now the public page of the new QuantumOrb" (`:76`) |
| 24–25 Oct 2026 | "the bot" (`:64`) |
| 22–27 Oct 2026 | "the site" (`:41`) |
| 1 Nov 2026 | "the repository follows the new site and bot" (`:30`) |
| 3 Nov 2026 | "the site is public" (`:23`) |
| 5 Nov 2026 | "the full release" (`:3`) — bot open, token, roadmap, more code |

Age **[READ + INFER]**: oldest changelog entry 21 Oct 2026; git root commit 22 Oct 2026; public site 3 Nov; token 4 Nov; bot 5 Nov. As of 23 Nov 2026 the repo is 32 days old, the public site 20 days, the bot 18 days, with no commits since 5 Nov. "Starts over", "the new QuantumOrb" and commit `cccf5b3` "README: links to the renamed account" indicate an earlier incarnation whose history is not in this repo.

Data sources **[READ]**:
- `docs/architecture.md:10-16`: "launch stream", "Solana chain · public RPC", "public market data", and "Dedicated RPC" (provider unnamed).
- `CHANGELOG.md:43-45`: "No pump.fun API, no paid calls; paid chain reads are only for scans and token pages."
- `CHANGELOG.md:66`: "a WebSocket stream instead of polling" (stream provider unnamed).
- Market data = DexScreener first, GeckoTerminal to fill gaps (`market/pools.js:27-30`; `test/market.test.js:3`).
- Creator history: `bot/shield.py:5-6` "one getProgramAccounts on the pump.fun program, filtered by the curve's creator field"; limitation `docs/guard.md:19-21`: launches "from before pump.fun began storing the creator on the curve (early 2025) are not in it."
- pump.fun IDL cited: `bot/solana_util.py:6-7` "github.com/pump-fun/pump-public-docs, idl/pump.json".
- Helius, QuickNode, Birdeye, PumpPortal, Jito: not mentioned anywhere.
- Scan budget: `CHANGELOG.md:59` "A budget of 250 reads and 40 seconds per scan."
- Wallet history depth (site tooltip, `site_home_rawhtml_text.txt:335`): "estimated from up to 200 earlier transactions (about two per token)".

Bonding-curve constants and math **[READ]**:
- Program `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`; curve PDA seeds `["bonding-curve", mint]` (`bot/solana_util.py:23,28,102-103`; `chain/solana.js:50`).
- Layout: discriminator 8 bytes; u64 virtual token @8, virtual quote @16, real token @24, real quote @32, total supply @40; `complete` @48; creator @49; mayhem @81; cashback @82; quote mint @83 (`bot/solana_util.py:9-20`).
- `TOKEN_DECIMALS = 6`, `SOL_DECIMALS = 9` (`bot/solana_util.py:39-40`); non-SOL quotes use 6 decimals (`chain/solana.js:62-66`).
- `INITIAL_REAL_TOKEN_RESERVES = 793_100_000` tokens (`bot/solana_util.py:41`; `bot/formatting.py:22`).
- `totalSupply: 1e9` (`rules/limits.js:20`).
- Price = virtual quote ÷ virtual token (`bot/solana_util.py:166-171`).
- Progress % = `(1 − real_token_reserves / 793.1M) × 100`; 100 if `complete`; not computed for mayhem curves (`bot/solana_util.py:174-183`; `bot/formatting.py:135-145`).
- PumpSwap canonical pool PDA: seeds `[pool, u16 0, pool-authority PDA, mint, quote]` (`chain/solana.js:52-57`).
- **Absent**: initial virtual reserves, graduation threshold in SOL/USD, fee rates, any buy/sell quote function with fees. `bot/solana_util.py:20`: "then fee fields the bot does not need." Test values (1e9 virtual tokens / 32 SOL, `bot/tests/test_open.py:45`) are synthetic, not protocol constants.

Market-cap definition **[READ]**:
- `market/pools.js:122-132` `caps()`: FDV = price × mint supply; market cap = FDV only when supply is fixed (mint authority revoked); otherwise a source-reported cap; otherwise null. Comment `:126`: "N/A, never the FDV passed off as market cap."
- Price pool: priced, liquidity ≥ $1,000 and ≥ 10% of the deepest pool, traded in 24 h, stage's own pool preferred (`market/pools.js:6,91-109`).
- Bot fallback price ≈ `usd_market_cap / supply` (`bot/formatting.py:6,126-132`).
- TOO ESTABLISHED uses `mcap || fdv` (`rules/verdict.js:27`).
- Watch milestones $10K–$100M (`bot/formatting.py:25`).

## Q11. Concepts usable for an independent clean-room reimplementation (ideas only, my wording)

1. Measure concentration against tradable float: exclude balances owned by curve, AMM, locker and burn programs/addresses, identified by owning program ID.
2. Per-holder features: acquired by purchase vs inbound transfer; prior trading history (fresh or not); entry delay after launch (first ~30 s, same slot as creation); whether it has sold since.
3. Build a wallet graph with typed edges: co-purchase in one transaction; common non-hub funding/distributing wallet; direct holder-to-holder transfer. Exclude high-fan-out hubs (exchanges, routers, bridges, addresses with very many outgoing transfers). Cluster with union-find.
4. Separate weaker behavioural clusters (several fresh wallets entering within a few slots with similar sizes) and discount their weight rather than treating them as certain.
5. Express cluster risk as price impact rather than raw share: fraction of pool reserves a cluster could dump under constant-product pricing.
6. Transparent additive score with piecewise-linear components, plus hard overrides and score caps for patterns a weighted sum hides.
7. Explicit abstention: no score when too few holders, when the token is old/large, or when too much data was unreadable; tri-state checks (pass / fail / not read) so missing data is never a pass.
8. Creator reputation from chain: enumerate launchpad curve accounts whose creator field matches a wallet (program-account query with a byte-offset filter), then graduation ratio and launch count.
9. Launch-time checks: creator's own purchase share in the creation transaction; share bought in the launch slot; creator's current share. Identify the creator as the signer of the create instruction, not the later fee recipient.
10. Curve state straight from the account: price from virtual reserves, progress from remaining real token reserves, completion flag. Verify layout and constants against the official public IDL.
11. Token-level authority checks: mint/freeze authority, mutable metadata, Token-2022 transfer-fee config; LP control (burned/locked/held).
12. Market-data hygiene: match pools by mint address only; merge sources without mixing base/quote sides; ignore dust pools for pricing; null ≠ zero; keep market cap distinct from FDV.
13. Transaction parsing via pre/post token-balance deltas per owner plus native + wrapped SOL deltas; detect swaps by set of invoked programs.
14. Budgeted scans (cap on RPC reads and wall time) with partial-result labelling.
15. What a credible version needs that this project lacks: labelled outcomes, out-of-sample evaluation, and published error rates.

## Other observations

- **[2ND]** GitHub page via WebFetch (2026-11-23): 271 stars, 90 forks, 5 watchers, 1 open issue (#1 "trading", opened 22 Nov 2026 by `aleadruam-source`), 21 commits. Profile `github.com/QuantumOrb`: personal account, handle shown as "QORB", 40 followers, 1 public repo, links to quantumorb.app and X accounts @RetroValix and @Dan1ro0 (DexScreener lists @QuantumOrbApp instead). **[INFER]** 271 stars / 90 forks on a 32-day-old, single-author repo with one issue is unusual; could not examine stargazers.
- `README.md:15` badge "dependencies none" is accurate for the published files.
- `robots.txt` contains only a content-signals comment preamble, no directives.
- Site security headers are strict (CSP `default-src 'self'`, no third-party scripts except Cloudflare Insights beacon).

## Could not access / verify

1. The X post and the @QuantumOrbApp account (x.com returned HTTP 402 to WebFetch): wording, date, author, attached media unverified.
2. The closed server, bot backend, database and link-detection code; therefore whether the hosted service runs the published rules.
3. Whether site counters reflect genuine activity (operator-controlled API); I did not check any mint on-chain.
4. Token burns and holder airdrops marked "Done"; token holder distribution; who holds/sold QORB. No Solana RPC/explorer queries were made.
5. GitHub API and raw github.com pages (blocked for this session, HTTP 403); star/fork/issue figures are second-hand summaries. Account creation date and stargazer authenticity unknown.
6. solanacompass.com (HTTP 403).
7. The Telegram bot itself was not opened or messaged.
8. No token-page scan was triggered on the site (would consume the operator's scan quota and appear in its public feed); token pages `#t-<mint>` were not rendered.
9. Screenshots other than `home.png`, `banner.png`, `bot-start.png`, `roadmap.png` were not viewed.
10. No repository code was executed, so "tests pass" is unverified by me; the CI badge status was not checked.
