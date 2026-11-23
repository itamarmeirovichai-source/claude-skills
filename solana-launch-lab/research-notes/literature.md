# Literature review: Pump.fun / Solana memecoin launch signals, scam detection, execution costs and backtest validity

Compiled 2026-11-23. Every source below was fetched in this session on 2026-11-23 (access date for all entries). Nothing is cited from memory alone.

## How to read this document

- **Verification levels.** `[FT]` = full text read (PDF converted to text). `[ABS]` = arXiv abstract page and metadata read; selected passages of the PDF read where numbers are quoted. `[META]` = bibliographic metadata verified (Crossref or RePEc) but the paper's text was not read; any description of content is attributed to the source that describes it. `[2ND]` = secondary press article fetched; the primary dataset was not reachable. `[SNIP]` = seen only in a search-result snippet; treat as unverified.
- **Status labels.** Peer-reviewed venue and year, preprint, industry report, dashboard, court document, regulator statement.
- **"My calculation" / "my inference"** marks anything I derived rather than read.
- Numbers are quoted as the sources state them. Where a source is internally inconsistent I say so.
- arXiv metadata came from `https://arxiv.org/abs/<id>` pages (the export API returned HTTP 429). Full texts came from `https://arxiv.org/pdf/<id>`.

---

# Part A. The three arXiv IDs

## A1. arXiv:2610.39458 — exists `[FT]`

- **Citation.** Fail Gafarov (Kazan Federal University). "Early-Buyer Groups and Fast-Wallet Teams on a Bonding-Curve Launchpad: A Prospective Measurement Study of pump.fun on Solana." arXiv:2610.39458v1. https://arxiv.org/abs/2610.39458
- **Submission and versions.** v1 only, submitted Thu 29 Oct 2026 06:29:11 UTC (602 KB); the PDF is dated October 30, 2026. No revision, withdrawal or correction on arXiv as of 2026-11-23.
- **Category.** Primary physics.soc-ph; cross-listed cs.SI and q-fin.TR. Comments: "66 pages".
- **Publication status.** Preprint. No journal-ref. Only the arXiv-issued DataCite DOI (10.48550/arXiv.2610.39458, shown as "pending registration"). The text refers to "the review of an earlier version of this paper" and labels several tests "added in response to review", but no venue is named. Single author.
- **Dataset.** Purpose-built block-by-block collector (WebSocket subscription with RPC fallback), not a third-party API. One window: 2026-09-26T19:00:23 to 2026-09-30T11:16:00 UTC (88.3 hours). 200,443 token launches, of which 154,045 have a complete creation record; 15,854,121 bonding-curve trades; 51,025,958 SOL transfers; 5,565,871 PumpSwap trades; 5,862 graduations; 21,183,236 protocol transactions. Addresses are salted-hashed in the public release.
- **Method.** Prospective (time-ordered) wallet-group discovery from co-buying, shared funding, joint signing, transfers and consolidation, giving 23,710 groups. Label-free validation: out-of-sample link prediction, independent non-trading links, comparison with naive co-buy clustering at equal numbers of flagged tokens. Permutation nulls, inverse-probability weighting, matching, E-values. Follower simulation on exact protocol-reported reserves: 0.05 SOL position, latency 1, 2, 3 or 5 s, two cost conventions ("project": max(event fee, 2%) per side plus 1.5% slippage per side; "event": recorded fee plus 0.3% slippage), policy chosen on the first 70% of signals and tested on the last 30%. Gradient-boosted entry ranking with a purged 55/15/30 chronological split. A final hold-out block with frozen rules.
- **Key definitions.**
  - *Group*: wallets that behave in a coordinated way by explicit observable rules; the author does not claim common ownership and does not label any group manipulative.
  - *Group token*: at least two known members and two other buyers among first-minute buyers. *Control token*: no members among at least four early buyers.
  - *Outcomes*: curve reaches 20 SOL or 60 SOL (round numbers chosen in advance, not protocol thresholds), and graduation (migration to PumpSwap). *Prospective outcome*: token still below 20 SOL at 60 s reaches 20 SOL later.
  - *Team signal*: at least three team members among first-minute buyers (first 5 s for fast-wallet communities).
  - *Bundle*: the paper uses it for buys in the same slot as the first trade of the token (community c2 does this in 75% of its tokens). *Snipers*: fast-wallet communities c0 and c3 that enter a few slots after the first trade.
  - *Complete token*: observation not cut; incomplete launches (23.1%) are excluded from outcome statistics.
- **Headline numbers (as stated).**
  - Base rates among complete tokens: 53% never hold more than 1 SOL; 25% never exceed 0.1 SOL; 26.3% have at most 3 trades; 7.7% reach 20 SOL; 2.4% reach 60 SOL; 2.8% graduate (4,250 of 154,045).
  - Naive co-buy clustering puts 94% of connected wallets into one component, yet as a signal it ranks tokens at least as well as the discovery groups. For the prospective outcome, precision of the top 500: about 29.3% (naive components) versus 10.2% (discovery groups); base rate 1.8%.
  - Being accepted by the discovery rules adds nothing at equal co-buy count: odds ratio 0.94 (interval includes one).
  - Concentration: Gini of tokens per group 0.86; top 1% of groups account for 43% of attributed tokens; 43% of groups are a single wallet.
  - Creator-linked single-wallet signals reach 20 SOL in 2.5% of tokens (lift 0.33); buyers-only groups of 13–29 wallets in 44.2% (lift 5.73).
  - Members buy about 4.3 s earlier than other early buyers (11 s versus 15 s after creation).
  - Members' net cash flow exceeds a matched placebo by 0.17 SOL per token [0.12, 0.23]; late buyers' mean cash flow is −2.34 SOL per token.
  - Price path after a 60 s reference: 8.8% of group tokens at least double versus 2.8% of weighted controls; time to peak 48.7 s versus 49.7 s; price at 10 minutes relative to reference 0.99 versus 0.96 (difference +0.03 [−0.05, +0.15], not distinguishable). Restricted to common support the doubling difference is +0.7 pp [−0.3, +1.6].
  - Follower: out-of-sample mean net return is negative in all 32 configurations, between −7% and −4% (event costs) and −11% and −8% (project costs). Buyers-only follower at 1 s latency: −7.8% versus −7.9% for random entry (project costs); −4.0% versus −3.6% (event costs). Winning trades 24–35%.
  - Latency on identical trades: about one percentage point of return per additional second for all signals.
  - Cost decomposition for a fixed momentum rule on 15,000 random tokens: +5.4% with no costs; +3.7% with a 2% fee floor; +0.6% after 1.5% slippage per side; −9.9% after 1 s latency.
  - Learned ranking: top 5% of test decisions −5.8% [−7.1, −4.4]; best validation cell falls from +2.3% to −2.9% out of sample; no cell has an interval above zero.
  - Evaluation pitfalls: an evaluator that needs a later observed quote leaves 88% of exits unresolved and shows capital 1.198 from 1 SOL on 43 positions; adding the trader's own position leaves 3% unresolved, 332 positions, capital 0.504. A shared label/feature column name produced a spurious +300% mean return with a 100% win rate.
  - Large team (126 wallets): its tokens reach 20 SOL in 53% of cases versus 9.0% overall; weighted difference +32.2 pp [30.6, 33.6]; reach-60 +4.5 pp; graduation +0.6 pp [−0.0, +1.3]. A follower entering after the third member's buy earns −5% per trade [−6, −4].
  - Creator's initial buy alone: AUC 0.82 for reaching 20 SOL; snipers alone 0.70; both 0.88. Within strata of initial buy, sniper presence multiplies the odds of reaching 20 SOL by 8.0.
  - Final hold-out (36,532 tokens, base rate 8.6%): frozen rules keep precision of 50.4%, 70.6% and 73.0%; 26–40% of those signals fired when the curve already held 20 SOL; one team supplies 62–79% of flagged tokens.
  - Incremental value: curve SOL at 60 s alone gives AUC 0.939 and AP 0.364; adding group features changes AP by −0.015 [−0.030, +0.004] and AUC by 0.000; group features alone give AUC 0.793.
- **Limitations the author admits.** One 88-hour window in one market regime; no ground truth for ownership; one-second time resolution, so submission order, tips and bundle membership are unobserved and sub-second traders are not represented; no real transactions sent; one team dominates large-team results; incomplete covariate balance; the hold-out is a later block of the same window, not an independent sample; about a quarter of launches excluded; no multiplicity correction. The author states the conclusion conditionally: no strategy tested earned a positive out-of-sample return under these assumptions, not that none can.
- **Limitations I see.**
  - Reported reach-60 (2.4%) is below the graduation share (2.8%), which is hard to reconcile if graduation needs about 85 SOL. The figure caption says graduated tokens are shown separately, so the reach metrics may be computed on a different basis. Unresolved from the text.
  - Sole-author preprint with no code or data URL visible in the text I read (a "replication package" is mentioned).
  - Position size 0.05 SOL; results for larger sizes shown only up to 0.5 SOL.
  - The window is 26–30 September 2026; fee schedules and platform rules change (see B31).
- **Generalizability to an alert 7–13 minutes after launch.** Limited and indirect. Every signal studied fires within the first 60 seconds, and simulated latencies are 1–5 s. The paper does not test entries at 7–13 minutes. What it does say that bears on that horizon: the post-reference peak arrives about 49 s after the 60 s mark on average, and by 10 minutes the price ratio of group tokens and controls is indistinguishable. My inference: a 7–13 minute alert built on early-buyer structure acts after the period in which that structure was associated with price moves in this window, so the paper gives no support for an edge at that delay and some reason to expect none. It does not prove a loss at that delay.

## A2. arXiv:2603.24625 — exists `[FT]`

- **Citation.** Jiaxin Chen, Ziwei Li, Zigui Jiang, Ruihong He, Yantong Zhou, Jiajing Wu, Zibin Zheng (Sun Yat-sen University). "From Hype to Collapse: Investigating Rug Pull Scams on Solana." arXiv:2603.24625v2. https://arxiv.org/abs/2603.24625
- **Submission and versions.** v1 Wed 25 Mar 2026 02:31:31 UTC; v2 Sun 31 May 2026 10:48:32 UTC. **The revision is substantive.** v1 was titled "SolRugDetector: Investigating Rug Pulls on Solana" and its abstract claimed a detection system that "outperforms existing tools on the labeled dataset". v2 drops the detector and the outperformance claim, retitles the paper, and reframes it as dataset construction and measurement. v2 states its numbers are "dataset quality indicators ... rather than detection performance".
- **Category.** cs.CR primary; cs.CY.
- **Publication status.** Preprint. No journal-ref, no publisher DOI. Formatted in IEEE journal style.
- **Dataset.** (i) Benchmark-117: 117 confirmed rug-pull tokens from 68 manually verified community reports (Chainabuse, SlowMist, CertiK), compared with 65 legitimate tokens (Jupiter-verified, Organic Score at least 80). (ii) ITW-76469: 100,063 tokens newly issued on Orca, Raydium and Meteora between 1 January and 30 June 2025, from Solana RPC and Solscan; 76,469 labelled rug-pull candidates. **Pump.fun tokens that never created a liquidity pool are excluded.**
- **Definitions.**
  - *Rug pull*: developers attract capital by deceptive marketing or manipulation, then sell off or withdraw liquidity.
  - *Freeze Authority Abuse*: creator keeps freeze authority and at least one FreezeAccount instruction was executed against a user.
  - *Liquidity Withdrawal*: a creator-related address makes a profitable liquidity removal followed by collapse below the activity threshold.
  - *Pump-and-Dump*: within a sustained post-launch window holder count and pool token balance decline monotonically and the holder reduction exceeds τ_down = 0.73.
  - Pre-filter: average transaction rate over the trailing 24 hours below 5 per hour.
  - *Lifecycle*: time from creation to the first confirmed fraud-related profit-taking transaction.
- **Headline numbers (as stated).** 76,469 of 100,063 labelled (my calculation: 76.4%): 60,402 Pump-and-Dump, 15,606 Liquidity Withdrawal, 461 Freeze Authority Abuse. Audit of 382 sampled candidates found one false positive: 0.26%, 95% upper bound 1.45%. Of 100 sampled non-rug tokens, 9 were missed cases, and roughly 15% of the correctly excluded ones were still trading normally six months later. Median lifecycle 0.0246 days overall (my calculation: about 35 minutes), 0.0221 days for Pump-and-Dump, 75th percentile 0.0646 days. Benchmark rug pulls: median lifespan 0.0116 days, median 9 holders. At least $151,089,437.80 in direct losses across 7,322 profiting addresses ($133.3M in SOL, $17.8M in stablecoins). 78 large groups (16 single-address, 62 multi-participant); members 1–169, median 36. Only 19.0% of labelled tokens disclose an X account and 14.3% a website. The paper also reports that price, percentage change and FDV for the same token at the same timestamp "often differ" across GMGN, Birdeye, DexTools and DexScreener.
- **Limitations the authors admit.** Retrospective by design and not a pre-attack warning; 24-hour observation window; labels are a high-precision lower bound; slow scams and very low-activity tokens are missed; loss figures are conservative.
- **Limitations I see.** The false-negative check is 9 of 100, so recall is unmeasured beyond a small sample. The Pump-and-Dump rule (monotone holder decline of 73%) cannot distinguish deliberate fraud from a token that simply lost attention; "rug pull" here is a behavioural label, not a finding of intent. The detector comparison from v1 is gone, so there is no evaluated classifier to reuse. Loss tracing covers creator and pool-creator liquidity operations only.
- **Generalizability to an alert 7–13 minutes after launch.** Weak for bonding-curve trading: Pump.fun-only tokens are excluded, so the sample starts where a pre-graduation alert ends. Useful as a base rate for tokens that already have a DEX pool: about three quarters were labelled rug-pull candidates and the median time from creation to first profit-taking was about 35 minutes, so a 7–13 minute alert sits inside the typical life of these tokens. The labels cannot be computed in real time.

## A3. arXiv:2602.14860 — exists `[FT]`

- **Citation.** Giulio Marino, Manuel Naviglio, Francesco Tarantelli, Fabrizio Lillo (Pisa, Scuola Normale Superiore, Bologna). "Predicting the success of new crypto-tokens: the Pump.fun case." arXiv:2602.14860v1. https://arxiv.org/abs/2602.14860
- **Submission and versions.** v1 only, Mon 16 Feb 2026 15:53:13 UTC (327 KB). No revisions.
- **Category.** q-fin.ST.
- **Publication status.** Preprint. No journal-ref or publisher DOI on arXiv as of 2026-11-23.
- **Dataset.** Parsed directly from the Pump.fun and PumpSwap programs. 1 September to 1 October 2025. 655,770 tokens created by 243,123 creator addresses; 2,600,790 trader addresses; 4,338 graduations.
- **Definitions.**
  - *Success* = graduation, i.e. the bonding curve reaching 115 virtual SOL (30 virtual plus 85 real), "approximately 85 SOL raised and a market capitalization of about $69,000" in the sample period.
  - *vSol*: virtual SOL in the curve (starts at 30).
  - *isBot = 1*: transaction calls the contract directly rather than through the pump.fun website front end.
  - *Successful traders*: top wallets by realised SOL profit in the first two weeks, evaluated in the second two weeks.
  - *Top creators*: at least 50 tokens, graduation ratio above 0.001, tokens with at least 10 trades; identified in the first half, evaluated in the second.
  - *Dump*: first log-return below −4 robust (MAD-based) standard deviations, on tokens with at least 30 swaps.
  - Fees: 1.25% per swap (0.30% creator, 0.95% protocol).
- **Headline numbers (as stated).**
  - Graduation frequency "approximately 0.63%" and "about 0.6%". My calculation from the paper's own counts: 4,338 / 655,770 = 0.66%.
  - Median time to graduation about 4.4 minutes; median 457 bonding-curve steps.
  - Conditional graduation probability given the curve ever exceeded a vSol level: 0.100 at vSol 50 (40,817 tokens), 0.354 at 80 (11,557), 0.638 at 100 (6,417).
  - Naive buy-and-hold breakeven: profitable only if p > vSol² / 115². My calculation: 0.189 at vSol 50, 0.484 at 80, 0.756 at 100. The baseline curve lies below breakeven throughout, so buying on curve level alone and holding to graduation has negative expected return before fees.
  - Reaching a given vSol in fewer trades is "the single most informative predictor" among the variables studied.
  - Non-bot share above 0.3: 0.112, 0.436, 0.748 at vSol 50, 80, 100. Top-100 traders: 0.104, 0.427, 0.741. Top-100 creators: 0.073, 0.409, 0.745. All remain below breakeven over most of the range; only the top-10-creator curve exceeds it at late stages, on a small sample the authors flag.
  - Dumps: 169,938 of 184,282 tokens with at least 30 swaps (92.22%) show at least one dump; only 2.55% of those tokens graduate; 56.41% of dump episodes are single-wallet.
  - Selling just before graduation yields more SOL than selling just after, because virtual liquidity disappears at migration.
- **Limitations the authors admit.** The breakeven ignores fees and gas and is a deliberately naive strategy; top-creator estimates have limited statistical support; identification of successful traders "can embed ex-post information"; bot detection and trader definitions could be made more robust "reducing look-ahead bias"; no hazard model or censoring treatment yet.
- **Limitations I see.** One month in one regime. The abstract says conditioning "significantly improves" predictive power while the conclusion says prolific creators do "not improve predictive performance relative to the baseline"; the text is not fully consistent on creators. No out-of-sample classification metric (AUC, calibration) is reported; results are conditional frequency curves. The curves condition on curve level, not on token age. The front-end versus direct-call bot proxy will mislabel retail users of third-party trading terminals as bots (my inference). Graduation rate stated as 0.63% does not match the stated counts.
- **Generalizability to an alert 7–13 minutes after launch.** Partly useful. The curves answer "given the curve is at X SOL, how often does it graduate?" and show that level alone does not clear breakeven. But the median graduate finishes in 4.4 minutes, so by 7–13 minutes more than half of eventual graduates have already migrated (my inference from the median). The paper gives no probability conditional on a token still being on the curve at that age; such tokens are a slower, probably weaker subset, consistent with the finding that slow accumulation predicts failure.

---
# Part B. Other relevant work

Each entry: citation and URL; status; data and dates; method and definitions; headline numbers; limitations; generalizability. Access date for all: 2026-11-23.

## Topic 1. Pump.fun and Solana memecoin launches

**B1. Gafarov, F. "Retrospective Analysis of Team-Following Trading Profitability in Pumpfun Meme Coins Using Funding Networks." arXiv:2611.11436v1, 8 Nov 2026.** https://arxiv.org/abs/2611.11436 `[ABS + large parts of FT]`
- Status: preprint (physics.soc-ph; cs.SI; q-fin.TR), 42 pages, v1 only. Follow-up to A1 by the same sole author.
- Data: ten separately recorded Pump.fun windows from April 2024 to September 2026 (about 24 to 79 hours each and 11,916 to 84,821 launches each, as I read the paper's Table 5; the PDF text extraction of that table is jumbled), from `getBlock`, reconstructed from real-SOL reserve states. The author warns that decoded data "may contain inaccuracies".
- Method: "teams" are directed SOL-funding groups ranked in hindsight; finite-capital account starting with 1 SOL; exits at reserve thresholds; random cohorts that repeat the threshold search; selection-matched nulls with Holm adjustment; online (prospective) re-qualification.
- Definitions: *team* = candidate coordination group from funding links, "not a verified organisation, beneficial owner or fraud label". *Marks* = model value of unclosed positions, kept separate from free cash. *Collapse* = closing reserve falls 50% from a running peak of at least 8 SOL.
- Numbers: with hindsight thresholds the account ends above 1 SOL in all 8 windows that have a qualifying team (1.10 to 11.32 SOL), but free cash exceeds 1 SOL in only 5; marks are 17–94% of equity. Recognised online, 9 of 19 teams become identifiable only after their last launch. Only 3 of 40 selection-matched tests are rejected after Holm adjustment. 73% of opened positions are still open at the end of their hour and hold 67% of invested SOL. With 2% fee and 5% slippage per side the account ends between 0.77 and 8.93 SOL. In the best window (2024-10) 24 seed positions produce +8.98 of the +8.61 SOL total; the other 40 positions produce −0.37 SOL.
- Base rates across the ten windows (first hour, eligible tokens): median maximum real reserve 2.36–4.00 SOL; 90th percentile 9.6–23.1 SOL; share reaching 40 real SOL 2.26–4.95%; share reaching 80 real SOL 0.23–1.10%.
- Limitations (author): every threshold chosen in hindsight; funding links use the full window even in the "online" step; windows "chosen for interest"; no rival responses, priority, failed inclusion or migration modelled; "conditional retrospective model accounts, not executable profits".
- Generalizability: a direct demonstration of how hindsight selection manufactures apparent profit. Not a tradable result.

**B2. Szwajcok, N., Tsuchiya, T., Liu, E., Soska, K., Payer, M., Christin, N. "Meme Coin Factories: Uncovering Large-Scale Manipulations on pump.fun." arXiv:2609.10246v1, 9 Sep 2026.** https://arxiv.org/abs/2609.10246 `[ABS + large parts of FT]`
- Status: peer-reviewed; arXiv comments state "Proceedings of the 2026 ACM SIGSAC Conference on Computer and Communications Security (CCS'26)". Authors from EPFL, ETH Zürich, Carnegie Mellon, Fullstack.
- Data: all 15,245,966 coins created 14 Jan 2024 to 14 Jan 2026 (metadata); full transactions for a random 1% coin sample and all coins of a 5-day sample, over 87 million transactions.
- Definitions: *graduation* = curve retains about 85 SOL and the coin moves to a DEX. *WT1 wash trade* = buy and sell in the same transaction (only possible outside the web interface). *WT2* = same address buys and sells the same amount at about the same price within a window. *Creator obfuscation* = creator addresses clustered by first funder (1 to 3 hops), with Arkham labels used to remove services. *Coordinated sell* = tokens consolidated from several addresses into one that dumps. *Bundling* = many trades inside one transaction.
- Numbers: 1.02% of coins graduate. Lower bound of 4 million wash trades, 17% of all trading transactions, but only 1.32% of volume. Graduation rate 2.0% for wash-traded coins versus 0.90%; doubling wash trades raises graduation odds by about 19%. WT2 flags 12.38% of coins at a 1 s window, 44.05% at 5 s and 88.5% at one day, which the authors read as false positives. Top 1% of creator clusters create 58.6% of all coins; over half of 5,826,346 creator addresses fall into a multi-address cluster; largest cluster 10,531 addresses. 4,402 dumps under the strict rule (1% sample), median 7 senders. At least 1.5 million copycat coins (over 10%). 3.5 million coins (23.5%) created after Twitter or Truth Social posts. A community's graduation rate "drops significantly after the first coin".
- Limitations: funding-graph clustering errs if a service address is unlabelled (Arkham's 98% accuracy is a vendor claim the authors cite); they mitigate with a leave-one-address-out check. Results are associations. Transaction analysis rests on samples.
- Generalizability: the strongest peer-reviewed evidence that volume, comments and apparent holder dispersion on pump.fun are manipulable, and that creator clustering reveals serial launchers.

**B3. Hu, S., Tekin, S. F., Xu, Y., Liu, L. "MELT: A Behavioral Trace Dataset for High-Risk Memecoin Launch Detection." arXiv:2602.13480v2, 21 May 2026 (v1 13 Feb 2026).** https://arxiv.org/abs/2602.13480 `[ABS + parts of FT]`
- Status: preprint (cs.CR; cs.LG).
- Data: Pump.fun launches from 1 Dec 2024 to 1 Mar 2025 that completed migration: 41,470 tokens, over 200 million transactions. Bundle traces from shared transactions, shared funders and Jito bundle IDs (crawled for 22,668,222 pre-migration trades).
- Definitions: *min_price_ratio* = minimum price within 20 minutes after migration divided by migration price. *High-risk* = min_price_ratio below 0.3 or manually judged manipulated (manual check via the GMGN interface for tokens with ratio at least 0.5). *Low-risk* = ratio at least 0.7 and not manipulated. *Bundle* = accounts sharing a transaction, funder or Jito bundle ID.
- Numbers: 84.13% of migrated tokens are high-risk; about 73% fall below 40% of migration price within 20 minutes; 36.5% of supply at migration is held by bundled accounts; merging bundles raises the top-10 holder share by 24 points for high-risk tokens versus 6 for low-risk. Detection after filtering (16,048 high versus 5,587 normal): high-risk F1 about 0.83–0.84 for all models against 0.74 for a random baseline; normal-class F1 about 0.53–0.56 against 0.26. A selection strategy "can reduce investment losses by up to 34 percentage points".
- Limitations (mine): labels come from post-migration price, so "high-risk" means "dumped fast", not proven insider selling. The filter removes 47.8% of tokens, 95% of them high-risk, which makes the task easier. Bubble period centred on the TRUMP launch. Bundle links are heuristics with no ground truth.
- Generalizability: covers only graduated tokens; relevant to holding through migration, not to bonding-curve entries.

**B4. Ding, W., Luo, Y., Xu, J. "Decompose Market Manipulation Strategies: Evidence from On-chain Meme Coin Market."** Conference paper, Sydney Banking and Financial Stability Conference 2025: https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf `[parts of FT]`. Also listed as SSRN 5953738 (page returned HTTP 403; not read). B2 cites it with a fourth author, Chen Lin.
- Status: working paper; I could not confirm journal publication.
- Data: 6,000 Pump.fun coins (weighted sample) with on-chain trades and off-chain comments.
- Definitions: *rat bot* and *sniper bot* (concealed accumulation / front-running), *wash trading bot* (fabricated activity), *comment bot* (fabricated sentiment).
- Numbers: wash trading bots appear in about 4% of projects and raise creator profit by about $432 on average; non-creators lose $6.37 per project on average without wash bots and $4.47 with; comment bots in 26% of projects; about 50% of projects are dumped by creators; winners are disproportionately creators or snipers.
- Limitations: small sample (B2 notes about 0.04% of all coins); not verified as peer-reviewed.

**B5. Mancino, D. "The Memecoin Phenomenon: An In-Depth Study of Solana's Blockchain Trends." arXiv:2512.11850v3.** https://arxiv.org/abs/2512.11850 `[ABS]`
- Status: peer-reviewed conference paper, 2025 IEEE Symposium on Computers and Communications (ISCC), pp. 1–6, DOI 10.1109/ISCC65549.2025.11326251 (Crossref-verified).
- Data: Pump.fun, Q4 2024, on-chain.
- Numbers: Pump.fun accounted for up to 71.1% of tokens minted on Solana and 40–67.4% of DEX transactions; "fewer than 2% of tokens successfully transitioned to major decentralized exchanges"; daily active users rose from 60,000 to peaks of 260,000.
- Limitations: descriptive; one quarter.

**B6. Kamat, A. U. "Coordinated Sniper Cohorts on Pump.fun: Detection of 1,012 Persistent Wallet Rings ..." arXiv:2607.02795v4, 5 Oct 2026 (v1 2 Jul 2026).** https://arxiv.org/abs/2607.02795 `[ABS]`
- Status: preprint. **All numerical results withdrawn by the author.** The v4 abstract opens: "CORRECTION (Oct 2026): buyer records include sells and miss many buys; all numerical results below are withdrawn pending a corrected analysis."
- Withdrawn claims: 1,012 persistent cohorts from 166,098 launches (11–25 June 2026); first-30-minute buyer-count lift +16.1%; SOL-inflow lift +6.3% [−0.5%, +15.1%].
- Use: do not cite its numbers. A1 uses it only as a pointer to the research question.

**B7. Kamat, A. U. "Auditing Collector-Generated Graduation Labels on Pump.fun: Measurement Error and Temporal Non-Generalization." arXiv:2607.02823v4, 10 Sep 2026.** https://arxiv.org/abs/2607.02823 `[ABS + parts of FT]`
- Status: preprint; pre-registered; data on Zenodo (concept DOI 10.5281/zenodo.20633486).
- Data: 749,816 unique mints recorded by an off-chain collector between 12 May and 10 June 2026; 1,597 labelled GRADUATED and 748,219 TIMEOUT.
- Numbers: locked logistic model has development AUROC 0.8594 and validation AUROC 0.4642 on the next 14 days (95% interval [0.4112, 0.5196]); calibration slope 0.013; of nine automated evaluations two pass, six fail.
- Correction history (in the paper): the earlier version reported a "24-hour graduation rate" and a "3.18× decline" between two periods; both are **withdrawn** because the collector's TIMEOUT label "does not establish platform-side non-graduation".
- Limitations: single collector; sole author; not peer-reviewed.

**B8. Kamat, A. U. "Do Two On-Chain Observation Pipelines See the Same Tokens? Cross-Pipeline Coverage on the Solana pump.fun Launchpad." arXiv:2609.18975v2, 23 Sep 2026.** https://arxiv.org/abs/2609.18975 `[ABS]`
- Status: preprint; v2 "corrected v1 result".
- Numbers: over a 17.5-day window, a cohort-detection pipeline flagged 623 mints and a rejection-filter pipeline 1,742, with 5 in common (0.803% and 0.287%).
- Relevance: collector configuration shapes which tokens a study sees.

**B9. Luo, Y., Feng, Y., Xu, J., Liu, Y. "Resisting Manipulative Bots in Meme Coin Copy Trading: A Multi-Agent Approach with Chain-of-Thought Reasoning." arXiv:2601.08641v3.** https://arxiv.org/abs/2601.08641 `[ABS]`
- Status: arXiv journal-ref says Proceedings of the ACM Web Conference 2026 (WWW'26). The DOI shown (10.1145/3774904.3792635) did not resolve at Crossref when I checked.
- Claim: an LLM multi-agent copy-trading system achieves "an average copier return of 3% per meme coin investment under realistic market frictions".
- Limitations (mine): abstract only; I did not verify the friction model, the sample period or whether the test was out of time. Treat as the one positive-return claim in this set, not yet scrutinised here.

**B10. Mongardini, A. M., Mei, A. "A Midsummer Meme's Dream: Investigating Market Manipulations in the Meme Coin Ecosystem." arXiv:2507.01963v2.** https://arxiv.org/abs/2507.01963 ; venue page https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini `[ABS + venue page]`
- Status: peer-reviewed, 35th USENIX Security Symposium (2026).
- Data: 34,988 meme coins across Ethereum, BNB Smart Chain, Solana and Base; three-month longitudinal tracking.
- Numbers: among tokens with returns above 100%, 82.8% (arXiv abstract; 82.89% on the venue page) show artificial growth such as wash trading or liquidity-pool-based price inflation; over 17,000 victim addresses with realised losses above $9.3 million.
- Relevance: high-return examples are disproportionately manipulated ones.

## Topic 2. Rug pulls and scam-token detection

**B11. Li, J., Kuznetsov, P., Yanovich, Y., Nott-Whaley, K., Vodolazov, I. "Catching the Rug: Early Prediction of Fraudulent Memecoins on Solana via Machine Learning." arXiv:2608.20271v2, 8 Nov 2026 (v1 20 Aug 2026).** https://arxiv.org/abs/2608.20271 `[ABS + parts of FT]`
- Status: preprint (cs.AI). v1 and v2 have the same file size.
- Data: 30 Nov 2024 to 30 Jun 2025; 6,304,235 PumpFun tokens and 97,965 Raydium tokens.
- Definitions: *rug pull* = TVL falls 99% from its peak **or** the token is idle for more than 80% of its lifetime, evaluated at 1 hour. Features come only from the first 5 minutes; tokens already rugged within 5 minutes are dropped.
- Method: forward rolling-window validation with a 3-month training window, explicitly to avoid look-ahead and to handle concept drift.
- Numbers: PumpFun test set has 2,931,946 rug-pull and 1,893,539 non-rug tokens (my calculation: 60.8% positive). Same-platform MCC about 0.25–0.36; fusion-to-PumpFun MCC 0.3947 (XGBoost); Raydium-to-PumpFun transfer gives MCC "approaching zero or becoming negative".
- Limitations (mine): the idle rule labels dead tokens as rug pulls, so the label mostly measures "died within the hour". MCC of 0.25–0.39 is modest. No profitability test.

**B12. Alhaidari, A., Kalal, B., Palanisamy, B., Sural, S. "SolRPDS: A Dataset for Analyzing Rug Pulls in Solana Decentralized Finance." arXiv:2504.07132.** https://arxiv.org/abs/2504.07132 `[ABS]`
- Status: peer-reviewed dataset paper; arXiv comments say accepted at ACM CODASPY 2025.
- Data: 2021–2024, derived from 3.69 billion transactions; 62,895 suspicious liquidity pools; 22,195 tokens show rug-pull patterns. Labels are inactivity states.

**B13. Mazorra, B., Adan, V., Daza, V. "Do not rug on me: Zero-dimensional Scam Detection." arXiv:2201.07220.** https://arxiv.org/abs/2201.07220 `[ABS]`
- Status: arXiv preprint (I did not verify a journal version). Uniswap V2.
- Numbers: best model accuracy 0.9936, recall 0.9540, precision 0.9838 "prior to the malicious maneuver".
- Caution (mine): very high accuracy on an EVM dataset where most tokens are scams; B11 and B7 show such figures do not carry across platforms or time.

**B14. Wu, H. et al. "RPHunter: Unveiling Rug Pull Schemes in Crypto Token via Code-and-Transaction Fusion Analysis." arXiv:2506.18398v3.** https://arxiv.org/abs/2506.18398 `[ABS]`
- Status: preprint (cs.SE). EVM. 645 manually analysed incidents; precision 95.3%, recall 93.8%, F1 94.5%; in the wild 4,801 tokens at 90.7% precision. Relies on contract code, which does not transfer to Solana SPL tokens (A2 makes this point).

**B15. Sun, D., Ma, W., Nie, L., Liu, Y. "SoK: Comprehensive Analysis of Rug Pull Causes, Datasets, and Detection Tools in DeFi." arXiv:2403.16082.** https://arxiv.org/abs/2403.16082 `[ABS]`
- Status: preprint. 34 root causes; existing datasets (2,448 instances) cover 7 of 34; 14 tools cover 25 of 34; wash trading and freeze account are among nine causes no tool covers.

**B16. Naviglio, M., Tarantelli, F., Lillo, F. "Price manipulation schemes of new crypto-tokens in decentralized exchanges." EPJ Data Science 15, 10 (2026). arXiv:2502.10512.** https://arxiv.org/abs/2502.10512 `[ABS]`
- Status: peer-reviewed (DOI 10.1140/epjds/s13688-025-00602-5, Crossref-verified).
- Uniswap V2 new tokens: liquidity trapped in honeypots; a buy-and-hold test exposes rug pulls and sandwich attacks; sandwiches are more profitable in low-liquidity pools. A3 states that this paper finds about 88% of Uniswap V2 launches in late 2024 were manipulation schemes (as reported by A3; I did not read the full text).

**B17. Cernera, F., La Morgia, M., Mei, A., Sassi, F. "Pump-and-Dump meets Honeypot Tokens: Detection and Analysis of Telegram Bait-and-Trap Schemes." arXiv:2610.10149, 7 Oct 2026.** https://arxiv.org/abs/2610.10149 `[ABS]`
- Status: preprint. 83 Telegram channels, 3,677 events on BNB Smart Chain and Ethereum. Organisers gain in 99.3% of cases, over $7 million. EVM only.

**B18. Solidus Labs Research. "The 2025 Rug Pull Report: Rug Pulls and Pump-and-Dumps on Solana." May 2025.** https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance `[page fetched]`
- Status: **industry report by a vendor that sells a detection product (Token Sniffer).** Not academic.
- Data: Pump.fun tokens created January 2024 to March 2025; 388,000 Raydium V4 pools (dates not stated).
- Definitions: a Pump.fun token is treated as worthless when liquidity falls under $1,000 in SOL. Raydium "soft rug pull" = liquidity sweep identified by LP-token burns at a 90% threshold.
- Numbers: "Over 7 million tokens deployed with at least five trades, but only 97,000 tokens maintain liquidity above $1,000." Headline share is printed as 98.7% in the summary, 98.6% in the body and 98% in the conclusion. Raydium: about 93% of pools; median about $2,832; largest $1.9 million.
- Dispute: CoinDesk (Oliver Knight, published 8 May 2025, updated 9 May 2025 to add the response) quotes pump.fun spokesperson Troy Gravitt: "What Solidus Labs lacks is a basic understanding of memecoins." https://www.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says `[2ND]`
- Limitations (mine): the 98.6% figure measures "ended with under $1,000 of liquidity", which is failure, not proven fraud. Tokens that migrated to Raydium are excluded. Not corrected by Solidus as far as I found.

## Topic 3. Wash trading, fake volume and wallet clustering

**B19. Victor, F., Weintraud, A. M. "Detecting and Quantifying Wash Trading on Decentralized Cryptocurrency Exchanges." The Web Conference 2021, pp. 23–32. arXiv:2102.07001.** https://arxiv.org/abs/2102.07001 `[ABS; Crossref]`
- Status: peer-reviewed (WWW '21). IDEX and EtherDelta order books on Ethereum. Lower bound of $159 million in wash volume; more than 30% of traded tokens affected; on EtherDelta 10% of tokens almost exclusively wash traded.

**B20. Cong, L. W., Li, X., Tang, K., Yang, Y. "Crypto Wash Trading." Management Science 69(11):6427–6454, 2023. arXiv:2108.10984.** https://arxiv.org/abs/2108.10984 `[ABS; Crossref]`
- Status: peer-reviewed. 29 centralised exchanges; statistical tests (first-digit distributions, size rounding, tail distributions). Wash trading "averaged over 70% of the reported volume" on unregulated exchanges. Centralised venues, not DEXs.

**B21. Möser, M., Narayanan, A. "Resurrecting Address Clustering in Bitcoin." Financial Cryptography and Data Security 2022. arXiv:2107.05749v2.** https://arxiv.org/abs/2107.05749 `[ABS]`
- Status: peer-reviewed (per arXiv comments). The abstract says current clustering heuristics "have not been rigorously evaluated or optimized"; the authors build a ground-truth set of transactions with known change and warn of "cluster collapse". Specific false-positive rates (for example 0.026 for one heuristic) appeared only in a search snippet `[SNIP]`; I did not verify them in the text.

**B22. Kappos, G., Yousaf, H., Stütz, R., Rollet, S., Haslhofer, B., Meiklejohn, S. "How to Peel a Million: Validating and Expanding Bitcoin Clusters." arXiv:2205.13882.** https://arxiv.org/abs/2205.13882 `[ABS]`
- Status: arXiv; a search result points to a USENIX Security 2022 version, which I did not fetch. Validates clustering with a ground-truth dataset. Error-rate figures seen only in a snippet `[SNIP]`.

**B23. Background, metadata only `[META]`.** Meiklejohn et al., "A fistful of bitcoins", IMC 2013, pp. 127–140 (DOI 10.1145/2504730.2504747). Victor, "Address Clustering Heuristics for Ethereum", FC 2020, LNCS, pp. 617–633 (DOI 10.1007/978-3-030-51280-4_33). Both Crossref-verified; not read.

**Solana-specific clustering evidence** is in A1 (naive co-buy clustering collapses into one component holding 94% of connected wallets; non-trading links add no persistence at equal co-buy counts), B2 (funder-based clusters with a leave-one-out check) and B3 (Jito bundle IDs). **I found no study that measures clustering error rates against ground truth on Solana.**

## Topic 4. MEV, sandwiching, Jito, fees, failed transactions, price impact

**B24. Gerzon, N., Weintraub, B., In, J., Mislove, A., Nita-Rotaru, C. "Quantifying the Threat of Sandwiching MEV on Jito: A Measurement of Solana's Leading Validator Client." ACM Internet Measurement Conference 2025, pp. 937–943.** PDF: https://cnitarot.github.io/papers/imc26_solana.pdf (DOI 10.1145/3730567.3764493, Crossref-verified) `[parts of FT]`
- Status: peer-reviewed (IMC '25, short paper).
- Data: over four months of Jito bundle data from early 2025.
- Numbers: 521,903 sandwich attacks; over $7.7 million in victim losses (lower bound: 28% of attacks had no SOL leg and were not valued); median sandwiched transaction lost roughly $5; attacks fell from over 15,000 per day to roughly 1,000 per day; sandwiches are 0.038% of measured Jito bundles; users spent over $2.4 million on defensive bundling; over 86% of single-transaction bundles carry tips too low for priority placement.
- Limitations: Jito bundles only; sandwiches executed outside Jito's auction are not seen.

**B25. Heimbach, L., Solmaz, O., Öz, B., Torres, C. F. "No Place to Hide: An Analysis on Protected Order Flow Sandwich Attacks." arXiv:2609.28115, 23 Sep 2026.** https://arxiv.org/abs/2609.28115 `[ABS]`
- Status: preprint. Three-year study across six chains. 28.0 million sandwich attacks on Solana against transactions "intended to be protected", versus 30,607 on Ethereum. Reports validator- and application-level exposure on Solana. Count is far larger than B24's because scope and heuristics differ (wide and cross-block attacks, three years).

**B26. Zheng, X., Wan, Z., Lo, D., Xie, D., Yang, X. "Why Does My Transaction Fail? A First Look at Failed Transactions on the Solana Blockchain." Proc. ACM Softw. Eng. 2 (ISSTA), 1489–1512, 2025. arXiv:2504.18055.** https://arxiv.org/abs/2504.18055 `[ABS; Crossref]`
- Status: peer-reviewed. Over 1.5 billion failed transactions across more than 72 million blocks. The bot failure rate of 58.43% is quoted by A2 and by a repository abstract seen in search results; the truncated abstract I fetched did not include it, so treat the exact figure as `[SNIP]` plus citation in A2.

**B27. Zheng, X. et al. "Demystifying Solana Bots: From GitHub Blueprints to On-Chain Fingerprints." arXiv:2607.28424v2.** https://arxiv.org/abs/2607.28424 `[ABS]`
- Status: arXiv comments say accepted at ASE 2026. 586 bot repositories and 200 bot addresses with over 44 million transactions; bot-related DEX volume above $250 million per day in January 2026.

**B28. Helius. "Solana MEV Report."** https://www.helius.dev/blog/solana-mev-report `[page fetched]`
- Status: **industry report** (RPC provider); author and date not shown on the page; latest data early January 2025.
- Numbers: one sandwich program made 1.55 million sandwich transactions in 30 days (7 Dec 2024 to 5 Jan 2025) for 65,880 SOL ($13.43 million), 88.9% success, average 0.0425 SOL ($8.67) per attack, and is credited with nearly half of all Solana sandwiches. Over 3 billion Jito bundles and 3.75 million SOL in tips in a year. Reverted transactions peaked at 75.7% of non-vote transactions in April 2024.

**B29. Chorus One. "Transaction Latency on Solana: Do swQoS, Priority Fees, and Jito Tips Make Your Transactions Land Faster?" 3 Dec 2024.** https://chorus.one/reports-research/transaction-latency-on-solana-do-swqos-priority-fees-and-jito-tips-make-your-transactions-land-faster `[page fetched]`
- Status: **industry report by a validator operator that sells a swQoS service** (conflict of interest).
- Data: slots proposed by one validator, 18–25 Nov 2024.
- Findings: time-to-inclusion peaks at 63 s, 17 s and 5 s; "Priority Fees minimally affect landing times"; Jito tips "negligible latency benefits"; stake-weighted QoS helps most. Does not measure drop or failure rates. Internally inconsistent in places (25% versus 30% for one statistic).

**B30. Angeris, G., Kao, H.-T., Chiang, R., Noyes, C., Chitra, T. "An analysis of Uniswap markets." arXiv:1911.03380v7.** https://arxiv.org/abs/1911.03380 `[META via arXiv page]`
- Status: arXiv (I did not verify the journal version). Standard reference for constant-product pricing; not read in this session.

**B31. Pump.fun. "Fees" (official documentation). "Last Updated: 16 November 2026".** https://pump.fun/docs/fees `[page fetched]`
- Bonding curve: creator 0.300%, protocol 0.95%, LP 0%, total 1.25% per trade. PumpSwap canonical pools: tiered by market cap from 1.250% (0–420 SOL) down to 0.300% (98,240 SOL and up). Migration fee 0.015 SOL.
- Note: A3 reports the same 1.25% for September 2025. The Aguilar opinion (B42) recites an alleged 1% fee for an earlier period. Fees have changed over time.

**Price impact on the bonding curve (my derivation from the formulas in A3, not a measured result).** With virtual SOL reserve x and a buy of Δx SOL after fees, the average execution price exceeds the pre-trade spot price by the factor (x + Δx) / x, so impact is about Δx / x. The curve starts at 30 virtual SOL, so a 0.5 SOL buy moves the price at least 1.7% at launch and proportionally less later. A round trip on the curve costs 2 × 1.25% = 2.5% in fees before impact, priority fees and tips. A1's measured decomposition (a gross +5.4% per trade becomes −9.9% after a 2% fee floor, 1.5% slippage per side and 1 s latency) is the empirical counterpart.

## Topic 5. Backtest methodology

**B32. Bailey, D. H., Borwein, J. M., López de Prado, M., Zhu, Q. J. "The Probability of Backtest Overfitting." Journal of Computational Finance 20(4), 2017 (Crossref: published Sept 2016, DOI 10.21314/jcf.2016.322).** Author PDF (revised Feb 2015): https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf `[abstract read]`
- Status: peer-reviewed. Abstract: holdout "tend[s] to be unreliable and inaccurate in the context of investment backtests"; proposes the probability of backtest overfitting (PBO) estimated by combinatorially symmetric cross-validation (CSCV).

**B33. Bailey, D. H., López de Prado, M. "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality." Journal of Portfolio Management 40(5):94–107, 2014 (DOI 10.3905/jpm.2014.40.5.094).** Author PDF: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf `[abstract read]`
- Status: peer-reviewed. Abstract: "Not controlling for the number of trials involved in a particular discovery leads to over-optimistic performance expectations"; DSR corrects for selection bias under multiple testing and non-normal returns.

**B34. Harvey, C. R., Liu, Y., Zhu, H. "… and the Cross-Section of Expected Returns." Review of Financial Studies 29(1):5–68, 2016 (DOI 10.1093/rfs/hhv059).** NBER WP 20592: https://www.nber.org/papers/w20592 `[abstract page read]`
- Status: peer-reviewed. A newly discovered factor "needs to clear a much higher hurdle, with a t-ratio greater than 3.0"; "most claimed research findings in financial economics are likely false".

**B35. White, H. "A Reality Check for Data Snooping." Econometrica 68(5):1097–1126, 2000 (DOI 10.1111/1468-0262.00152).** https://ideas.repec.org/a/ecm/emetrp/v68y2000i5p1097-1126.html `[META]`
**B36. Hansen, P. R. "A Test for Superior Predictive Ability." Journal of Business & Economic Statistics 23(4):365–380, 2005 (DOI 10.1198/073500105000000063).** https://ideas.repec.org/a/bes/jnlbes/v23y2005p365-380.html `[META]`
**B37. Sullivan, R., Timmermann, A., White, H. "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap." Journal of Finance 54(5):1647–1691, 1999 (DOI 10.1111/0022-1082.00163).** `[META]`
- Status: all peer-reviewed; metadata verified, abstracts not available on the pages fetched. Characterisation taken from B1's related-work section: White's Reality Check "formalizes testing a best discovered model against a benchmark"; Hansen's test "addresses sensitivity to irrelevant alternatives and the construction of the comparison statistic"; Sullivan et al. evaluate technical rules "while accounting for the larger rule universe from which a reported winner is selected".

**B38. Wang, Y., Pang, Z. "The Cryptocurrency Trend Factor Revisited: Predictive Information, Portfolio Construction, and Pricing Claims." arXiv:2611.01951, 1 Nov 2026.** https://arxiv.org/abs/2611.01951 `[ABS]`
- Status: preprint (also SSRN 7669458 per arXiv). A replication and code audit of a published crypto factor. After correcting future-information use and other issues, mean weekly gross return goes from 4.07% to 0.05%, annualised Sharpe from 2.08 to 0.01, and weekly net return under the lowest cost assumption from 2.93% to −0.87%.
- Relevance: a crypto-specific case where look-ahead and accounting errors produced the whole reported effect. Not yet peer-reviewed; the original authors' response is unknown to me.

**B39. Anghel, D.-G. "A reality check on trading rule performance in the cryptocurrency market: Machine learning vs. technical analysis." Finance Research Letters 39, 2021 (DOI 10.1016/j.frl.2020.101655).** https://ideas.repec.org/a/eee/finlet/v39y2021ics1544612320304414.html `[abstract page read]`
- Status: peer-reviewed. After correcting for data snooping and frictions, statistically significant positive excess returns are rarely achieved.

**B40. Hudson, R., Urquhart, A. "Technical trading and cryptocurrencies." Annals of Operations Research 297:191–220, 2021 (DOI 10.1007/s10479-019-03357-1).** `[abstract via Crossref]`
- Status: peer-reviewed. Almost 15,000 rules; reports significant profitability that survives multiple-testing procedures, but "there is no predictability for Bitcoin in the out-of-sample period, although predictability remains in other cryptocurrency markets".
- Relevance: evidence both ways; shows regime dependence.

**B41. Context, lightly verified.** Fieberg, Liedtke, Metko, Zaremba, "Cryptocurrency factor momentum", Quantitative Finance 23(12):1853–1869, 2023 (replicates 34 anomalies on over 3,900 coins, 2014–2022) `[abstract page read]`. Liu, Tsyvinski, Wu, "Common Risk Factors in Cryptocurrency", Journal of Finance 77(2):1133–1177, 2022 `[META]`.

## Topic 6. Retail outcomes

**I found no peer-reviewed study that measures the share of Pump.fun wallets that lose money.** The closest academic evidence is indirect: A1 (late buyers' mean cash flow −2.34 SOL per token), B4 (non-creators lose $4.47–$6.37 per project on average), B10 (17,000 victim addresses), A2 ($151M extracted). Everything below is non-academic.

**B42. Aguilar et al. v. Baton Corporation Ltd d/b/a Pump.fun et al., No. 1:25-cv-00880 (CM), S.D.N.Y., Opinion and Order granting in part and denying in part motions to dismiss, Document 184, filed 31 Aug 2026 (McMahon, J.).** https://storage.courtlistener.com/recap/gov.uscourts.nysd.635992/gov.uscourts.nysd.635992.184.0.pdf `[parts of FT]`
- Status: **court document.** Allegations are allegations, not findings.
- Content: plaintiffs "estimate that retail traders collectively lost between $4 billion and $5.5 billion trading Pump.fun tokens". The court notes plaintiffs "allege that approximately sixty percent of the relevant wallets ended net negative", and reasons that "approximately forty percent did not". Plaintiffs allege insiders "bundled" transactions across wallets and obtained priority execution.
- Holding: RICO and RICO-conspiracy counts survive only as asserted by Carnahan and Okafor against Baton, Cohen, Kerler and Tweedale; all claims by Aguilar and all claims against the Solana defendants dismissed; Securities Act and unjust-enrichment counts dismissed. Jito defendants had earlier been voluntarily dismissed.

**B43. Dune dashboard statistic by analyst Adam Tehc (@adam_tehc), January 2025 — disputed.** Reported in Cointelegraph, 11 Jan 2025 (Ciaran Lyons): https://cointelegraph.com/news/pump-fun-crypto-traders-majority-do-not-realize-profits-dune-data `[2ND]`
- Status: **dashboard, via press.** I could not load the Dune dashboard itself.
- Numbers: of 13.55 million wallet addresses, about 55,296 (0.412%) had realised more than $10,000; 0.048% more than $100,000; about 293 more than $1,000,000. Realised profit only.
- Dispute: pump.fun co-founder (handle @a1lon9) said the analysis has "many issues": it omits trades after tokens bonded to Raydium, omits unrealised profit, and counts bots ("About 30% of wallets have only made one transaction"). Source: ChainCatcher, 11 Jan 2025, https://www.chaincatcher.com/en/article/2161945 `[2ND]`. Cointelegraph describes the critic only as a pseudonymous analyst "Alon". **I found no reply or revision from the dashboard author.**

**B44. crypto.news, "Only 0.76% of pump.fun wallets made $1,000 or more" (Toghrul Aliyev), 26 Aug 2024.** https://crypto.news/only-0-76-of-pump-fun-wallets-made-1000-or-more-cn-research/ `[2ND]`
- Status: press analysis using its own queries "inspired by" Dune analysts @adam_tehc, @hashed_official and @evelyn233.
- Numbers: 29,601,462 wallets; 59.9% negative PnL; 37.6% positive; 0.76% made $1,000 or more; 0.046% made $10,000 or more. 33,683 of 1,883,578 tokens reached Raydium (1.79%). Methodology not described.

**B45. crypto.news, "Over 60% of pump.fun traders saw losses ..." (Trisha Husada), 5 Jun 2025.** https://crypto.news/over-60-pump-fun-traders-saw-losses-less-than-0-01-made-over-1m/ `[2ND]`
- Source cited: Dune query https://dune.com/queries/5233371/8602592 (author not named) and dashboard https://dune.com/jhackworth/pumpfun.
- Numbers: more than 4.2 million wallets over six months; 62.5% with losses; 311 wallets made over $1 million.
- **Internally inconsistent:** it states 244,130 profitable wallets and also a 27.2% profitable share; 244,130 / 4.2 million is 5.8% (my calculation). Do not rely on it.

**B46. crypto.news, "Pump.fun data shows 49% of March traders in the red ..." (Andrew Folkler), 30 Mar 2026.** https://crypto.news/pump-fun-data-shows-49-of-march-traders-in-the-red-as-platform-locks-fees/ `[2ND]`
- Source: Dune dashboard by pseudonymous analyst @oladee. About 1.4 million wallets in March 2026; 49–50.6% net losses; 45.4–45.6% profits under about $500; about 4% above that; two wallets over $1 million.

**B47. CoinGecko Research, "Pump.fun traders are making a comeback" (2026).** Primary page returned a bot challenge (HTTP 403); numbers below are from CryptoPotato's summary: https://cryptopotato.com/solana-based-meme-coin-launchpad-pump-fun-traders-see-turnaround-in-2026-coingecko/ `[2ND; primary not reachable]`
- Numbers: share of profitable wallets "rarely exceeded 50%" from April 2024 to late 2025, low of 30.1% in June 2025; about 57% in February 2026, 70% in March 2026, 73.3% in April 2026. April 2026: 65.1% of wallets earned $1–$500; 5.4% earned more than $1,000; 0.8% lost more than $1,000. Monthly active wallets fell from 5.2 million (May 2025) to 1.8 million (Dec 2025). Search snippets say the study counts realised PnL only and acknowledges this understates losses `[SNIP]`.
- **Conflict:** B46 reports about half of wallets in loss for March 2026; B47 reports 70% in profit for the same month. Different dashboards, wallet universes and PnL definitions. Unreconciled.

**B48. Graduation-rate press reports.**
- The Block (James Hunt), 27 Feb 2025: graduation rate peaked at 2.1% in June 2024, was 1.6% in early 2025 and 0.7% in the week of 24 Feb 2025; defines graduation as market cap reaching "approximately $100,000". https://www.theblock.co/post/343742/pump-fun-rapid-decline-graduating-tokens-memecoin-frenzy-fizzles-out `[2ND]`
- Cointelegraph (Yohan Yun), 14 Mar 2025, citing Dune (dashboard not named): below 1% for four straight weeks from 17 Feb 2025; best week 1.67% in November 2024. https://cointelegraph.com/news/pump-fun-memecoins-are-dying-at-record-rates-less-than-1-survive `[2ND]`
- A DEXTools article claiming a 0.26% graduation rate in 2026 returned HTTP 404; **not verified.**

**B49. U.S. SEC, Division of Corporation Finance. "Staff Statement on Meme Coins." 27 Feb 2025.** https://www.sec.gov/newsroom/speeches-statements/staff-statement-meme-coins `[page fetched]`
- Status: regulator staff statement, not a rule. Meme coins "typically have limited or no use or functionality" and "tend to experience significant market price volatility"; transactions in the meme coins described "do not involve the offer and sale of securities"; fraud may still be actionable under other laws. Contains no loss statistics. **I found no regulator report quantifying Pump.fun retail losses.**

**B50. $TRUMP coin loss counts (Chainalysis, via press).**
- Fortune (Sasha Rogelberg), 11 Feb 2025, citing a Chainalysis analysis commissioned by the New York Times: 813,294 wallets lost about $2 billion in the first 19 days, counting both sold-at-a-loss and held positions. https://fortune.com/crypto/2025/02/11/trump-memecoin-traders-2-billion-dollar-loss-family-100-million-fees/ `[2ND]`
- CNBC via NBC News (MacKenzie Sigalos), 6 May 2025, citing "fresh data" from Chainalysis: about 764,000 losing wallets of around 2 million buyers; 58 wallets made over $10 million each (about $1.1 billion). https://www.nbcnews.com/tech/crypto/58-crypto-wallets-made-millions-trumps-meme-coin-764000-lost-money-dat-rcna205237 `[2ND]`
- The later count is lower than the earlier one. Neither article explains the difference, and I found no statement that the first figure was corrected. Not a Pump.fun token.

**B51. Kamat, A. U. "What auditing 832,941 Pump.fun launches taught me about memecoin success." Brave New Coin, 14 Oct 2026.** https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success `[2ND, by the dataset maintainer]`
- Status: author's own non-academic article. States that the 0.198% "24-hour graduation" figure "was never the 24-hour graduation rate" and was withdrawn, and that the corrected dataset treats every timeout row as censored. Consistent with B7's text. The article gives a Zenodo DOI whose link target differs from the DOI printed; verify before citing the dataset.

**B52. Nansen on $LIBRA (Feb 2025).** 86% of traders (wallets with gain or loss above $1,000) lost a combined $251 million. `[SNIP]` — seen only in search results (The Block, Bloomberg headlines); not fetched. Not a Pump.fun token.

---
# Part C. Synthesis

Strength of evidence, in general: the two most rigorous sources on trading outcomes (A1, B1) are sole-author preprints from the last four weeks. The strongest peer-reviewed sources (B2, B10, B24) measure manipulation and costs, not strategy returns. Nothing in this set tests an alert that fires 7–13 minutes after launch.

## H1. Holder and creator analysis adds useful risk information

**For**
- A1: a creator-linked single-wallet signal (a serial creator) marks tokens that reach 20 SOL in 2.5% of cases against a 7.7% base rate (lift 0.33); creator-linked signals stay below base rate on every day. The creator's initial buy alone predicts reaching 20 SOL with AUC 0.82; a creator who buys again within 10 s is a negative sign.
- B2 (peer-reviewed): the top 1% of funder-linked creator clusters create 58.6% of coins; a community's graduation rate drops after its first coin.
- B3: 36.5% of supply at migration sits in bundled accounts; merging bundles raises top-10 concentration by 24 points for high-risk tokens versus 6 for low-risk. Models beat a random baseline (high-risk F1 about 0.83 versus 0.74).
- A3: tokens with a higher non-bot share graduate more often at every curve level (0.436 versus 0.354 at vSol 80).
- B4: about half of projects are dumped by their creators; winners are disproportionately creators or snipers.
- A2: 78 large deployment groups; Benchmark rug pulls have a median of 9 holders.
- B11: first-5-minute features predict "dead or drained within the hour" with MCC up to 0.39.

**Against**
- A1: at 60 s, group and team features add nothing to curve level for the prospective outcome (ΔAUC 0.000); membership accepted by the discovery rules adds nothing at equal co-buy count (odds ratio 0.94).
- A3 conclusion: conditioning on prolific creators "does not improve predictive performance relative to the baseline"; the top-trader effect is "at most a modest uplift".
- B7: a pre-registered model with development AUROC 0.86 scored 0.46 on the next two weeks.
- B11: a model trained on Raydium has MCC near zero or negative on PumpFun.
- No Solana clustering method has a measured error rate (Topic 3). B6's cohort numbers were withdrawn.
- "Risk information" is not "profit": B3's result is loss reduction; A1's follower still loses.

**What would falsify H1.** A pre-registered, out-of-time test in which a model using curve state plus creator and holder features has no better calibration or loss-avoidance than curve state alone at the alert time, across at least two separate market periods. Equivalently: creator-history and bundled-supply features showing zero incremental AP at equal numbers of flagged tokens.

## H2. Early curve state explains most of the signal; wallet clusters add little predictive value

**For**
- A1 (the only direct test): curve SOL at 60 s alone gives AUC 0.939 and AP 0.364; all first-minute non-group features 0.938 and 0.372; adding group features 0.938 and 0.357 (ΔAP −0.015 [−0.030, +0.004]). Group features alone reach only 0.793. Naive co-buy counts, a crowd-size proxy, rank tokens better than the curated groups. In the lower four quintiles of curve SOL at 60 s almost no token later reaches 20 SOL whatever the signal.
- A3: curve level gives a monotone baseline, and the strongest added predictor is how few trades it took to get there, which is a property of the curve path, not of wallet identity.
- B1: nearly half of funding-group "teams" could not be recognised in time (9 of 19 identifiable only after their last launch).

**Against**
- A1 itself: within strata of the creator's initial buy, sniper-community presence multiplies the odds of reaching 20 SOL by 8.0, and AUC rises from 0.82 to 0.88 when sniper presence is added. Within the top curve quintile, tokens with a team signal later reach 20 SOL in 12.4% of cases versus 4.1%. The 126-wallet team's excess survives a within-creator contrast (+32 pp).
- B3: bundle features separate high- and low-risk tokens after migration.
- B2: wash-trade counts (an actor-level feature) predict graduation.
- The direct test is one 88-hour window, one outcome (reaching 20 SOL), and one horizon (60 s). It says nothing about loss-avoidance outcomes or about later horizons.

**What would falsify H2.** At the actual alert time (7–13 minutes), a model with wallet-cluster features beating a curve-state-only model on held-out later periods, at equal alert counts, with a confidence interval that excludes zero, in more than one window. A1's top-quintile result is the place to look first.

## H3. Some alerts identify large later price moves, but realistic latency and exit costs erase the opportunity

**For**
- A1: flagged tokens do run (frozen rules: 50–73% reach 20 SOL against 8.6%; group tokens double after the reference in 8.8% of cases against 2.8%), yet a follower loses in all 32 configurations and does no better than random entry. A gross +5.4% per trade becomes −9.9% once a 2% fee floor, 1.5% slippage and 1 s of latency are applied. Each extra second costs about one percentage point. 26–48% of team signals fire after the level was already reached.
- B1: hindsight accounts reach 1.10–11.32 SOL but free cash exceeds 1 SOL in only 5 of 8 windows; 73% of positions never close.
- A3: graduation probabilities sit below the buy-and-hold breakeven p > vSol²/115² almost everywhere.
- Costs measured independently: 1.25% per side in fees (B31); median sandwich loss about $5 per victim transaction (B24); 28.0 million sandwiches against "protected" flow on Solana over three years (B25); bot failure rate 58.43% as cited in A2 (B26); priority fees and tips do little for landing time in one validator's data (B29).
- B3: about 73% of graduates fall below 40% of migration price within 20 minutes, so exits must be fast.

**Against**
- B9 claims +3% per coin for copy trading "under realistic market frictions" (abstract only; not scrutinised).
- B40: technical rules profitable after data-snooping controls in several crypto markets (not Bitcoin out of sample; not memecoins).
- B1: some teams that qualify online still end above 1 SOL (7 of 10 with free cash above 1 SOL), though funding links there still use the full window.
- A1 does not represent sub-second or co-located traders and says so. Insiders and MEV bots do profit (B4, B28), so the opportunity exists for someone.
- No source tests 7–13 minute latency. H3 at that horizon is an extrapolation from 1–5 s results.

**What would falsify H3.** A forward paper-trading log, with entries priced on post-alert reserves including the trader's own position, official fees, measured slippage and a realistic landing delay, showing a positive mean net return whose interval excludes zero and exceeds random entry into tokens at the same curve level and age.

## H4. Published examples are selected winners and omit unsuccessful alerts

**For**
- B1 quantifies the mechanism: teams ranked in hindsight always look profitable; when recomputed online, 9 of 19 could not have been known in time; marks of positions that never reached their exit are 17–94% of equity; in the best window the seed tokens used to define the teams produce more than the whole profit.
- A1 §7.4: an evaluator that silently drops trades without an observable exit (88% of them) reports a profit; including them turns 1.198 into 0.504. A label leak produced a 100% win rate.
- B10 (peer-reviewed): 82.8% of tokens that returned more than 100% show artificial growth, so "winners" are a manipulated subset.
- B7, B8: two pipelines from one programme shared 5 of 623 mints; "not seen graduating" was mislabelled as failure.
- B38: a published crypto factor's Sharpe ratio of 2.08 fell to 0.01 after timing and accounting corrections.
- B32–B37: the general theory and tests for selection among many trials.
- B18: 97,000 of over 7 million tokens kept $1,000 of liquidity, so any gallery of survivors is a small tail.

**Against / limits**
- **I found no audit of any alert service's published track record against its full alert log.** The evidence for H4 is about the mechanism and its size, not a measured omission rate for a specific publisher.
- Academic sources here do report losses and null results (A1, B1, B7), so "published" is not uniformly "selected".

**What would falsify H4.** A complete, time-stamped log of every alert a publisher issued (including those never showcased), matched to on-chain outcomes, showing that the showcased examples have the same return distribution as the full log.

## H5. Apparent discrepancies come from different market-cap definitions or data providers

**For**
- A2: price, percentage change and FDV of the same token at the same timestamp "often differ" across GMGN, Birdeye, DexTools and DexScreener because of trade-matching sources, pool selection and outlier handling.
- The graduation threshold is described as about 85 real SOL / 115 virtual SOL / "$69,000" market cap (A3, B11), "approximately $100,000" (B48, The Block), and "80% sold" (B3).
- Graduation rate by source: 0.63–0.66% (A3, Sept 2025), 1.02% (B2, 2024–2026), under 2% (B5, Q4 2024), 2.8% of complete tokens (A1, Sept 2026), 0.98% reaching 80 SOL in the first hour (B1, Sept 2026), and a collector-observed 0.21% that the author says is not a graduation rate (B7). A1 and B1 are by the same author and both cover September 2026, yet 2.8% and 0.98% differ almost threefold. They are different quantities (graduated at any time among complete launches, versus reached 80 SOL within the first hour among eligible launches); my reading is that cohort, horizon and censoring rules explain the gap, but neither paper reconciles them.
- "Scam share" by definition: 98.6% (under $1,000 liquidity, B18), 76.4% (behavioural rules, A2), 60.8% (TVL −99% or idle, B11), 84.1% of graduates (price ratio, B3).
- Retail outcome for March 2026: about half losing (B46) versus 70% profitable (B47). January 2025: 0.412% above $10,000 realised, disputed for excluding post-migration trades and unrealised gains (B43).
- Fees: 1% alleged for an earlier period (B42) versus 1.25% now (B31).

**Against**
- Some differences are real regime change measured within one source: The Block's series falls from 2.1% (June 2024) to 0.7% (February 2025).
- Some are plain errors, not definitions: B6 (sells counted as buys), B38 (future information), B45 (arithmetic).
- A1 versus A3 on P(graduate | reached 20 real SOL): about 36% (my calculation, 2.8 / 7.7) versus 10.0%. Both use on-chain reserves; this looks like a period effect or a cohort effect, not a market-cap definition. Unresolved.
- I could not fetch DexScreener's own market-cap/FDV documentation (HTTP 503), so the provider-formula part of H5 rests on A2's statement only.

**What would falsify H5.** Recomputing each disputed quantity from raw on-chain reserves under one written definition and finding that the gap between sources persists.

## H6. No tested strategy has a reliable edge after execution costs

**For**
- A1: 32 of 32 follower configurations negative out of sample; the learned ranking's top 5% loses 5.8%; no cell has an interval above zero; team followers lose on all four teams; results repeat on each of four days.
- B1: nothing was tested prospectively; 3 of 40 nulls rejected.
- A3: curve-level buy-and-hold is below breakeven.
- B39: after data-snooping correction, significant excess returns are rare in crypto. B38: a headline factor's net return turns negative after correction.
- B7, B11: classifiers lose discrimination out of time or across venues.

**Against**
- B9 reports a positive net return per coin (unverified detail).
- A3: top-10 creators exceed breakeven late on the curve (small sample, flagged by the authors).
- A1 Table A14: one cell is +0.3% [−4.3, +5.1], indistinguishable from zero in either direction, so "no edge" there is "none detected".
- B40: in-sample and some out-of-sample profitability for technical rules in non-Bitcoin markets.
- Insiders, snipers and sandwich bots earn positive returns (B4, B28; A1's members beat placebo by 0.17 SOL per token). H6 holds, at most, for outside followers.
- "No tested strategy" covers few tests: two sole-author preprints, short windows, one-second resolution.

**What would falsify H6.** One pre-registered rule, frozen before data collection, that earns a positive net return with a deflated Sharpe ratio above conventional thresholds on a later untouched period, with every alert and every failed fill logged.

## Base rates for a paper-trading study design

"Measured" means the source reports it from data. Inferences are mine.

| Quantity | Value | Period | Source | Kind |
|---|---|---|---|---|
| Graduation rate, all launches | "approximately 0.63%" (4,338 of 655,770 = 0.66%) | Sept 2025 | A3 | Measured |
| Graduation rate, random sample | 1.02% | Jan 2024 – Jan 2026 | B2 | Measured |
| Tokens reaching a major DEX | under 2% | Q4 2024 | B5 | Measured |
| Graduation rate, complete launches | 2.8% (4,250 of 154,045) | 26–30 Sept 2026 | A1 | Measured |
| Same, over all 200,443 launches | about 2.1–2.2% | 26–30 Sept 2026 | A1 | My calculation |
| Reach 80 real SOL within first hour | 0.23–1.10% across ten windows; 0.98% in Sept 2026 | Apr 2024 – Sept 2026 | B1 | Measured |
| Reach 40 real SOL within first hour | 2.26–4.95% | Apr 2024 – Sept 2026 | B1 | Measured |
| Reach 20 SOL / 60 SOL | 7.7% / 2.4% of complete launches | 26–30 Sept 2026 | A1 | Measured |
| Weekly graduation rate (press series) | 2.1% peak (June 2024); 1.67% best week (Nov 2024); 0.7% (late Feb 2025) | 2024–2025 | B48 | Dashboard via press |
| P(graduate given curve reached 20 real SOL) | 10.0% | Sept 2025 | A3 | Measured |
| Never hold more than 1 SOL | 53% of complete launches | 26–30 Sept 2026 | A1 | Measured |
| Never exceed 0.1 SOL | 25% of complete launches | 26–30 Sept 2026 | A1 | Measured |
| At most 3 trades | 26.3% | 26–30 Sept 2026 | A1 | Measured |
| Median maximum real reserve, first hour | 2.36–4.00 SOL | Apr 2024 – Sept 2026 | B1 | Measured |
| At least one 4-sigma dump (tokens with 30+ swaps) | 92.22% | Sept 2025 | A3 | Measured |
| Labelled dead or drained within 1 hour | 60.8% of PumpFun test tokens | Nov 2024 – Jun 2025 | B11 | My calculation from stated counts |
| Graduates below 40% of migration price within 20 min | about 73% | Dec 2024 – Mar 2025 | B3 | Measured |
| Below $1,000 liquidity at measurement date | 98.6% of tokens with 5+ trades | Created Jan 2024 – Mar 2025 | B18 | Industry; disputed |
| New DEX-pool tokens labelled rug-pull candidates | 76.4% | H1 2025 | A2 | Measured labels; excludes Pump.fun-only tokens |
| Median time to graduation (graduates only) | 4.4 minutes | Sept 2025 | A3 | Measured |
| Mean time to post-reference peak | 48.7 s after the 60 s mark (about 1.8 min after creation) | 26–30 Sept 2026 | A1 | Measured, tokens with early buyers |
| Median first-trade age | 5.0 s | 26–30 Sept 2026 | A1 | Measured |
| Median creation-to-first-profit-taking, DEX rug pulls | 0.0246 days (about 35 min) | H1 2025 | A2 | Measured |
| Bonding-curve fee | 1.25% per side | Nov 2026 | B31 | Official |
| Return lost per second of latency (first minute) | about 1 percentage point | 26–30 Sept 2026 | A1 | Measured in simulation |
| Median loss per sandwiched transaction | roughly $5 | early 2025 | B24 | Measured |
| Wallets net negative | about 60% (alleged); 59.9% (2024 press); 49–50.6% (Mar 2026 dashboard) | various | B42, B44, B46 | Allegation / dashboards |

**"Go to about zero within N days."** No source reports this with a fixed N for all launches. The nearest measured facts are the three A1 rows (most launches never hold 1 SOL at all), B11 at one hour, and B18 at its measurement date. My inference: for planning, treat well over half of launches as dead within the first hour, and measure the exact share in your own window.

**Time to peak.** No source reports the unconditional distribution of time-to-peak across all launches. My inference from the rows above: for most tokens the peak falls inside the first one to five minutes, so an alert at 7–13 minutes arrives after the peak for most tokens that will fail and after migration for more than half of those that will graduate.

**Design points that follow from the literature** (my recommendations): fix rules and metrics before collecting data; log every alert, including unfilled and unresolved ones; price entries and exits on reserves that include your own position; apply the official fee plus measured slippage and a landing delay; split by time with a purge; compare against "curve level and age only" at equal alert counts; report free cash separately from marks; treat "not seen graduating" as censored; record the data provider and the market-cap formula for every number; count every variant tried and deflate accordingly (B32, B33).

---

# Searched for but not found, or not verifiable

- **Dune dashboards themselves.** Not loaded. Query authors are named only through press: Adam Tehc (@adam_tehc), jhackworth, hashed_official, evelyn233, rsuthar94, oladee. Dune query 5233371's author is not named in the article that cites it.
- **A correction by a Dune dashboard maintainer.** None found. What I found instead: a dispute by pump.fun's co-founder of Adam Tehc's January 2025 figures (B43); full withdrawal of results by dataset maintainer A. U. Kamat (B6, B7, B51); a vendor report disputed by pump.fun but not corrected (B18); a lower later Chainalysis count for $TRUMP with no stated reason (B50).
- **CoinGecko's research page** (bot challenge, HTTP 403), **SSRN page for Ding et al.** (403), **DexScreener help article** (503), **CrowdfundInsider** (403), **DEXTools "0.26% graduation" article** (404). Claims that depend on them are marked.
- **Peer-reviewed measurement of the share of Pump.fun wallets that lose money.** Not found.
- **Regulator report with Pump.fun loss statistics.** Not found; only the SEC staff statement (qualitative).
- **Any study of alerts at 7–13 minutes after launch.** Not found.
- **Ground-truth error rates for wallet clustering on Solana.** Not found. Bitcoin figures were seen only in snippets.
- **White (2000) and Hansen (2005) abstracts.** Metadata verified; abstracts not on the pages fetched.
- **Nansen's LIBRA report** and the **58.43% bot failure rate** in its primary source: seen in snippets or via A2's citation only.
- **One DOI I tried from memory (10.1145/3665869) resolved to an unrelated paper** and is not used. The WWW'26 DOI listed on arXiv for B9 returned 404 at Crossref.
- **arXiv API** returned HTTP 429; abstract pages were used instead.
