# Research log — Solana launch signals

Research date: **2026-11-23**. This file records scope, method, findings, confidence and open questions.
The claim-by-claim audit is in [CLAIMS_AUDIT.md](CLAIMS_AUDIT.md); provider facts are in
[DATA_SOURCES.md](DATA_SOURCES.md).

> No strategy in this file has been shown to have positive expected value. The current answer to the
> long-term research question is **inconclusive, leaning negative**: every independent study found reports
> that following early signals loses money after costs.

## 1. Scope and method

What was searched, and how far:

| Area | What was done | Limits |
|---|---|---|
| The post and author | Fetched `https://x.com/Dan1ro0` (server-rendered payload) once; extracted post ID, timestamp, full text, engagement, bio and four neighbouring posts. Two exact-phrase web searches. | The permalink page, replies and the video were not loaded. The sotwe mirror returned 403, xcancel 451, the syndication endpoint 429; none were bypassed. The user's screenshot did not arrive. |
| Repository and site | Read-only clone of `QuantumOrb/QuantOrb` at `cb61b091` (2026-11-05); every tracked file read; no code executed. Site rendered in a headless browser, text dumped. | The closed scanner, API and Telegram bot were not observable. |
| Token examples | Solana public RPC (`getSignaturesForAddress`, `getTransaction`, `getBlock`, `getBlockTime`, `getTokenAccountsByOwner`), GeckoTerminal OHLCV and pool lists, DexScreener token endpoint. | No paid indexer. Wallet funding traced one hop only. |
| Official docs | Pump.fun docs and public-docs repo, Solana RPC docs, DexScreener and GeckoTerminal API references, six other providers' pricing/terms. | Several terms pages blocked; see DATA_SOURCES.md. |
| Literature | 52 entries fetched the same day, each tagged full text / abstract / metadata only. | "The whole internet" was not read. SSRN, CoinGecko and Dune pages were blocked. No study tests a 7–13 minute alert delay. |

Rules followed: primary sources over mirrors; exact mint addresses, never tickers; every number carries an
access time; measured facts are separated from inference; no AI model's output is used as evidence that a
strategy works.

Working notes produced during the session are kept in [`research-notes/`](research-notes/) (repository
audit, documentation tables, the full literature review, on-chain findings, post findings). Those notes were
written by research sub-agents and by scripts; the three top-level documents are the reviewed summaries.

## 2. Findings about the post and project (summary)

Measured:

- The post exists, was published 2026-11-21 21:37:19 UTC, and is written by the project's builder.
- Launch times of the three example tokens match on-chain creation times to the minute.
- At each stated alert time the on-chain market cap was 6–10× the cap the post states.
- From the stated alert time to the best later one-minute high the move was 4.1×, 12.9× and 5.4×, not 24×,
  58× and 50×.
- Each launch was a same-slot bundle: 19 co-signing wallets bought the entire bonding curve (79.3% of
  supply) for about 85 SOL; the same template was used three times.
- Those wallets sold from the first minute onward, including inside the stated alert minute, and now hold
  nothing. All three tokens trade near $1.5K market cap.
- One of the three had already collapsed about 11.5 hours before the post was published.
- The public repository is a deterministic rule calculator with no ML and no trading code, under a
  licence that forbids reuse.
- The project has its own token (FDV about $1.4K, 24h volume $1.81 on 2026-11-23) and a planned paid plan.

Not found:

- Any wallet, exchange account or trade history behind "+$10,847.63".
- Any archive of alerts with timestamps.
- Any source for the four headline counts.

Inference (labelled as such): the post's "alert cap" figures look like prices captured in the first one or
two seconds after launch, while the alert times are minutes later. A stale price feed would produce the same
pattern. Either reading means the stated multiples were not available at the stated times.

## 3. Literature

Status key: **PR** peer-reviewed · **PP** preprint · **IND** industry or vendor report · **LEGAL** court document ·
**DOC** official documentation. Full entries, datasets and limitations are in
[`research-notes/literature.md`](research-notes/literature.md).

### 3.1 The three papers named in the brief

| Paper | Status | Data | What it measured | Limits for our question |
|---|---|---|---|---|
| Gafarov, "Early-Buyer Groups and Fast-Wallet Teams … pump.fun", arXiv:2610.39458 v1, 29 Oct 2026. <https://arxiv.org/abs/2610.39458> | PP, single author, 66 pages | 200,443 launches over 88.3 hours, 26–30 Sep 2026 | A follower entering at the earliest group signal loses in all 32 tested configurations (−4% to −11% net) and does no better than random entry. A gross +5.4% per trade becomes −9.9% after a 2% fee floor, 1.5% slippage and 1 s latency; each extra second costs about one percentage point. Curve SOL at 60 s alone gives AUC 0.939 for graduation; adding wallet-group features changes AUC by 0.000. | 3.7 days of data; tests 1–5 s latency, so it does not measure a 7–13 minute delay directly; predicts graduation, not profit. |
| Chen et al., "From Hype to Collapse: Investigating Rug Pull Scams on Solana", arXiv:2603.24625 v2, 31 May 2026. <https://arxiv.org/abs/2603.24625> | PP. **v1 (25 Mar 2026) was titled "SolRugDetector" and claimed a detector outperforming existing tools; v2 drops that claim.** Use v2 only. | 100,063 new Orca/Raydium/Meteora tokens, H1 2025 | 76,469 labelled rug-pull candidates; audited false-positive rate 0.26%; median lifecycle about 35 minutes; at least $151M extracted. | Excludes pump.fun-only tokens. Labels are retrospective, so they cannot be used as a live signal without leakage. |
| Marino, Naviglio, Tarantelli, Lillo, "Predicting the success of new crypto-tokens: the Pump.fun case", arXiv:2602.14860 v1, 16 Feb 2026. <https://arxiv.org/abs/2602.14860> | PP | 655,770 tokens, September 2025 | Graduation rate about 0.63% as stated (0.66% from the paper's own counts). Median time to graduation 4.4 minutes. P(graduate) = 0.100 once the curve holds 20 real SOL. 92.22% of tokens with 30+ swaps show a dump. | One month. Graduation is the target, not trader profit; by the paper's own formula the breakeven probability for buy-and-hold at that point is about 0.189, above the measured 0.100 (our calculation). |

### 3.2 Other sources that bear on the decision

| Source | Status | Finding | Caveat |
|---|---|---|---|
| Gafarov, "Retrospective Analysis of Team-Following Trading Profitability …", arXiv:2611.11436, 8 Nov 2026. <https://arxiv.org/abs/2611.11436> | PP | Across ten windows 2024–2026, hindsight "team-following" always looks profitable, yet 9 of 19 teams were identifiable only after their last launch and 17–94% of equity is unrealized marks. | Direct demonstration of look-ahead and mark-to-market inflation. |
| Szwajcok et al., "Meme Coin Factories", arXiv:2609.10246 (ACM CCS 2026). <https://arxiv.org/abs/2609.10246> | PR | 15.2M coins; 1.02% graduate; at least 17% of trades are wash trades; the top 1% of creator clusters make 58.6% of coins. | Funder-based clustering with a leave-one-out check; no ground-truth error rate. |
| Hu et al., "MELT", arXiv:2602.13480 v2. <https://arxiv.org/abs/2602.13480> | PP | 36.5% of supply at migration sits in bundled accounts; about 73% of graduates fall below 40% of migration price within 20 minutes. | Dataset paper. |
| Li et al., "Catching the Rug", arXiv:2608.20271 v2. <https://arxiv.org/abs/2608.20271> | PP | Classifiers on the first 5 minutes reach MCC about 0.25–0.39 in-venue and near zero across venues. | Early prediction is weak and does not transfer. |
| Kamat, arXiv:2607.02795 v4 and arXiv:2607.02823 v4. <https://arxiv.org/abs/2607.02795>, <https://arxiv.org/abs/2607.02823> | PP. **Author withdrew all numerical results of the first paper in Oct 2026** (buyer records had included sells) and withdrew an earlier "24-hour graduation rate". | A pre-registered model's AUROC fell from 0.86 to 0.46 on the next two weeks. | Do not cite the withdrawn numbers. The drift result is the useful part. |
| Mongardini & Mei, "A Midsummer Meme's Dream", arXiv:2507.01963 (USENIX Security 2026). <https://arxiv.org/abs/2507.01963> | PR | 82.8% of tokens returning over 100% show artificial growth. | Multi-chain. |
| Gerzon et al., "Quantifying the Threat of Sandwiching MEV on Jito", ACM IMC 2025. DOI 10.1145/3730567.3764493 | PR | 521,903 Jito sandwiches, over $7.7M lost, median loss about $5. | Measures one MEV type on one client. |
| Zheng et al., "Why Does My Transaction Fail?", ISSTA 2025, arXiv:2504.18055. <https://arxiv.org/abs/2504.18055> | PR | Failed transactions on Solana are common, especially for bots. | The widely repeated 58.43% bot failure figure was seen only second-hand; not used here. |
| Bailey, Borwein, López de Prado, Zhu, "The Probability of Backtest Overfitting", J. Computational Finance 20(4), 2017 | PR | Framework (CSCV) for estimating how likely a chosen backtest configuration is overfit. | Method, not a finding about memecoins. |
| Bailey & López de Prado, "The Deflated Sharpe Ratio", J. Portfolio Management 40(5), 2014 | PR | Adjusts a Sharpe ratio for the number of trials and non-normal returns. | Same. |
| Harvey, Liu, Zhu, "… and the Cross-Section of Expected Returns", Review of Financial Studies 29(1), 2016 | PR | Multiple testing raises the bar for a new factor (t-stat above about 3). | Equity factors; the logic transfers. |
| White (2000) "A Reality Check for Data Snooping"; Hansen (2005) "A Test for Superior Predictive Ability" | PR | Bootstrap tests for the best of many rules. | Verified by metadata only. |
| Wang & Pang, arXiv:2611.01951, 1 Nov 2026. <https://arxiv.org/abs/2611.01951> | PP | A published crypto factor's Sharpe falls from 2.08 to 0.01 after look-ahead fixes. | Crypto-specific example of leakage. |
| *Aguilar v. Baton*, S.D.N.Y., opinion of 31 Aug 2026 | LEGAL | Plaintiffs allege about 60% of wallets ended net negative and $4–5.5B in retail losses; some RICO counts survive a motion to dismiss. | **Allegations, not findings of fact.** |
| Solidus Labs, "2025 Rug Pull Report". <https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance> | IND | 98.6% of pump.fun tokens fell below $1,000 liquidity. | Vendor report. Pump.fun publicly disputed the framing (CoinDesk, 8–9 May 2025); Solidus did not correct it. Treat as contested. |
| Pump.fun "Fees" page, updated 16 Nov 2026 | DOC | 1.25% per side on the curve; tiered 1.25%→0.30% on PumpSwap. | "May change … by updating this page." |

Corrections and withdrawals found, and how they are handled: Chen et al. v1 detector claim (dropped in v2);
Kamat's sniper-ring numbers and 24-hour graduation rate (withdrawn); Solidus 98.6% (disputed, not
corrected); Dune dashboard statistics on wallet profitability (two press figures for March 2026 conflict —
about 50% losing versus 70% profitable — and neither could be traced to a query we could load). None of
these disputed figures is used as an input to the simulator.

### 3.3 Base rates for study design

| Quantity | Value | Source, period | Type |
|---|---|---|---|
| Graduation rate | 0.63–0.66% | Marino et al., Sep 2025 | measured |
| Graduation rate | 1.02% | Szwajcok et al., 2024–26 | measured |
| Graduation rate | 2.8% of complete launches (about 2.1% of all) | Gafarov, Sep 2026 | measured / our arithmetic |
| Reach 80 SOL within the first hour | 0.23–1.10% | Gafarov (2611.11436), ten windows | measured |
| Never hold more than 1 SOL | 53% | Gafarov, Sep 2026 | measured |
| At most 3 trades | 26.3% | Gafarov, Sep 2026 | measured |
| Dead or drained within 1 hour | 60.8% | Li et al., Nov 2024 – Jun 2025 | our arithmetic from stated counts |
| Median time to graduation | 4.4 minutes | Marino et al., Sep 2025 | measured |
| Mean post-reference peak | about 49 s after the 60 s mark | Gafarov, Sep 2026 | measured |
| Graduates below 40% of migration price within 20 min | about 73% | Hu et al. | measured |

Graduation rates differ by a factor of about four between studies and periods. That is itself evidence of
regime change and definition drift; a study must measure its own base rate in its own window.

No source gives "share at zero within N days" or an unconditional time-to-peak, and no peer-reviewed
measure of the share of pump.fun wallets that lose money was found.

## 4. Competing hypotheses

Confidence is our subjective weight after this session; "prior" is where we started before looking.

### H1 — Holder and creator analysis adds useful risk information

- **For:** Creator concentration is extreme and persistent (top 1% of creator clusters make 58.6% of coins,
  Szwajcok, PR). Bundled supply at migration is large (36.5%, Hu). In our own three-token check, a single
  on-chain read of the creation slot showed 79.3% of supply bought by co-signers — decisive risk
  information available within one second of launch.
- **Against:** Gafarov finds wallet-group features add 0.000 AUC over curve state for predicting graduation.
  Li et al. find early classifiers barely beat chance across venues. Clustering has no published error rate
  on Solana.
- **Reading:** useful for **avoiding** specific structural risks (bundles, dev share, serial creators);
  **no evidence** it predicts returns.
- **Confidence:** prior medium → **medium-high as a risk filter; low as a return predictor.**
- **Would disprove:** on a time-ordered holdout, tokens flagged by structural checks lose no more often
  than unflagged tokens with the same curve state.

### H2 — Early curve state explains most of the signal; wallet clusters add little

- **For:** Gafarov (AUC 0.939 from curve SOL at 60 s alone; clusters add nothing). Marino et al. show
  graduation probability rising steeply with real SOL in the curve.
- **Against:** Both predict graduation, not profit. The three audited tokens "graduated" instantly because
  insiders filled the curve themselves, so curve state there measured the operator's own spending.
- **Confidence:** prior medium → **medium-high for graduation prediction; untested for profit.**
- **Would disprove:** a pre-registered model with cluster features beats the curve-only model on later data
  by more than its bootstrap interval.

### H3 — Some alerts precede large moves, but latency and exit costs erase the opportunity

- **For:** Gafarov: each second of delay costs about one point; gross +5.4% becomes −9.9%. Our audit: stated
  multiples of 24–58× shrink to 4–13× from the stated time before costs, and price impact cuts a 15 SOL
  position's best-case BartCoin exit from 3.7× to 3.3×. Hu: 73% of graduates lose 60% within 20 minutes.
  Gerzon: sandwiching is routine.
- **Against:** Large later moves did occur (PUNANI held above 5× the alert-minute price for hundreds of
  minutes), so a rule-based exit could in principle have been profitable on that one token.
- **Confidence:** prior medium → **high** that costs and delay remove most of the quoted move;
  **unknown** whether anything is left.
- **Would disprove:** a pre-registered entry/exit rule with realistic delay and fees shows positive net
  expectancy with a confidence interval above zero on at least 200 consecutive, unselected signals.

### H4 — Published examples are selected winners; unsuccessful alerts are omitted

- **For:** The post names 3 of 19 "passed" tokens and none of the rest. One of the three was already near
  zero when the post went out. The site's own counter showed 0 bot alerts in the prior 24 hours. Gafarov
  (2611.11436) documents how hindsight selection manufactures profitable-looking track records.
- **Against:** No list of the other 16 exists to check, so the size of the selection effect is unknown.
- **Confidence:** prior medium-high → **high** that the examples are selected; magnitude **unknown**.
- **Would disprove:** a complete, timestamped alert log published before outcomes, showing the three are
  typical.

### H5 — The discrepancies come from market-cap definitions or data providers

- **For:** Provider field definitions are undocumented; DexScreener's `liquidity.usd` omits the 17.58 SOL
  boost; GeckoTerminal's `market_cap_usd` is null; supply differs slightly from 1e9 after burns.
- **Against:** Here FDV and market cap coincide; two independent sources (pool balances from blocks, and
  provider candles) agree within a few percent; launch times match to the minute, excluding a time-zone
  error; the gap is 6–10×, far beyond any definitional difference found.
- **Confidence:** prior medium → **low** as an explanation of the main gap; definitions explain only
  single-digit-percent differences.
- **Would disprove (i.e. rescue H5):** the tool's raw alert payloads showing a documented cap definition
  that reproduces $58K / $50K / $75K at the stated times.

### H6 — No tested strategy has a reliable edge after execution costs

- **For:** Every independent study that models costs reports negative follower returns (Gafarov, both
  papers). Models decay within weeks (Kamat: AUROC 0.86 → 0.46). Crypto factor results often vanish after
  leakage fixes (Wang & Pang). No verified track record was found for the audited system.
- **Against:** Absence of published edges is not proof of absence; a profitable operator has no reason to
  publish. Our own simulator has only been run on synthetic data.
- **Confidence:** prior medium → **medium-high.** This is the working null hypothesis for the paper-trading
  study.
- **Would disprove:** the result described under H3, replicated on a second, later window without retuning.

### Own backtest, 2026-11-23 (see BACKTEST.md)

One day, 500 sampled launches, plan committed before the data was read. Entering every priced launch at
90 seconds: −6.9% per trade (95% interval −9.7% … −3.3%), mostly the round-trip cost on launches where nothing
happened. The `baseline-v1` filter accepted 13 launches, all of which lost (−32.5%). Evidence **for** H3 and H6
from this window; it does not change their confidence much on its own, because it is a single day.

## 5. Failure modes a study must guard against

| Bias | How it appears here | Control in this project |
|---|---|---|
| Look-ahead | Using the later peak as the exit; labelling "teams" after their last launch; using final holder lists for early decisions | Features are built only from observations with `observed_at ≤ as_of`; a test adds future data and asserts the signal is unchanged; exits use fixed rules |
| Survivorship | Analysing only tokens that still have a pool or a listing | Every discovered launch is stored, including those with no later data; missing outcome ≠ dropped |
| Selection | Reporting three winners | Every candidate and every rejection is written to the ledger before its outcome |
| Overfitting / multiple testing | Tuning thresholds on the same tokens | Ruleset is versioned; holdout window is fixed in advance; number of rulesets tried is recorded for a deflated-Sharpe-style adjustment |
| Regime change | Fee schedule changes, slot time changes, new launch templates | Each trade stores the fee schedule and config hash in force; results are reported per window |
| Stale or revised data | Provider caches, corrected candles | `observed_at` and `ingested_at` stored separately; stale flag; provider conflicts recorded |
| Mark-to-market inflation | Counting open positions at quoted price | Open and unsellable positions are reported separately and can be marked to zero |

## 6. Open questions

1. Did the alerts exist at the stated times? Needs an immutable alert archive.
2. Is there any account behind the PnL figure?
3. What is the true outcome distribution of all 19 "passed" tokens, and of the tokens that did not pass?
4. Does a structural filter (bundle share, dev share) reduce loss rates on unselected launches? Testable
   with this app once enough live launches are logged.
5. What does `InitBoost` do officially, and does it change how much SOL a seller can actually receive at
   the tail of a pool? We observed it on-chain but did not find it documented.
6. How large is the fill uncertainty from one-minute candles relative to the measured edge?
7. Can full holder lists be obtained within provider terms without a paid indexer?
