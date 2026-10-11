# D5 – Crypto prop firms: due diligence (bot fleet / many accounts)
Access date for all sources: 2026-10-11. "page" = I read the page itself (WebFetch); "snippet" = search-result summary only. ⚠ = unconfirmed.
Blocked: breakoutprop.com (/terms, /program-rules) returned HTTP 403; web.archive.org unreachable from this sandbox (connection reset), so no archived versions. No firm was contacted; nothing was bought.

## Headline finding (read first)
**Every firm examined says its FUNDED stage is simulated** (or is silent on it, as with Breakout/Kraken). The "real Bybit account" story about HyroTrader is out of date: its own Sep-2026 ToS says "All trading activity conducted under the Service is simulated", and its FAQ footer says "There is no real-capital stage at any point." So a payout is a discretionary "reward"/"scholarship" from the firm's own cash flow, not a share of exchange P&L. Each firm's own contract lets it refuse that payout.
**Fleet limits are tight everywhere:** HyroTrader allows 1 account per program type; Breakout/Kraken cap total funded capital at $200k; CFT Break allows 5 Final-Stage accounts, and on Final Stage it bans copy trading or coordinated trading even between the trader's own accounts; Velotrade has one Account and $200k combined funded capital; Bitfunded bans bots outright. **No crypto firm found allows a fully automated bot on many funded accounts that run the same strategy.** Same-strategy accounts are exactly what the "mirroring/coordinated trading" bans catch.

| Firm | Bots on funded | Accounts / cap per person | Copy across own accts | Funded real? | Grade |
|---|---|---|---|---|---|
| HyroTrader | Yes, if own strategy (agent tokens issued) | 1 per program type; aggregate limits in Trading Rules | Banned (mirroring) | Simulated | C |
| Breakout / Kraken Prop | ⚠ Unclear; 3rd parties say bots allowed except HFT; terminal-only, no public API verified | $200k aggregate funded | Banned (copy between traders; cross-account hedging) | Not stated; eval simulated | B- (owner quality) / C for bot use |
| Crypto Fund Trader | Allowed with restrictions (3rd-party ⚠); ToS silent | Break: max 5 Final-Stage accts; Bybit 20 subaccounts | Banned on funded (even own accts) | Simulated ("scholarships") | D |
| Velotrade | EAs permitted (8.3); API marketed | One Account; $200k combined funded | Banned (8.2(h)) | Simulated (5.1) | D |
| Bitfunded | **Banned** ("Every trade has to be placed manually") | No limit on challenges; 1 funded per size | Banned | Simulated | D (excluded) |

---

## 1. HyroTrader
**Identity.** Founder/CEO Samuel Drnda. Prague HQ plus a Dubai office (GlobeNewswire release, Sep 2025 – snippet). The founding year varies by source: a 2022 predecessor ("HyroTrade" CFD platform), then HyroTrader launched in 2023. One 2024 press release gives "August 2023" (snippet). Trustpilot lists the address as Plynární, Praha 7, CZ (page).
Contracting entities **changed in 2026**: the ToS now names **HYRO TECHNOLOGIES FZ-LLC** (RAKEZ, Ras Al Khaimah, UAE) as the sole contracting party (§P.1). Funded-phase rewards are paid by **HYROTRADER TECHNOLOGIES LTD (BVI)** under a separate Funded Trader Agreement (§P.4). Governing law is RAK/UAE (§26). US users go to JAMS arbitration in New York with a class-action waiver (§23.5–23.6). The ToS was "Last updated" 29 Sep 2026 (page). A third-party review notes an earlier 7 Aug 2026 ToS update that introduced the UAE entity (snippet, proptradingvibes ⚠).

**Venue / real vs sim.** Traders connect their own **Bybit or BloFin demo** account via API, or use the internal "Hyro" simulation engine. A "Cleo" route uses Binance data (⚠ snippet, propfirmmap). ToS §3.2: "All trading activity conducted under the Service is simulated", and this includes the Funded Trader Phase. FAQ footer: "All trading on HyroTrader takes place on simulated (demo) accounts that run on real exchange market data… There is no real-capital stage at any point." Older marketing ("funded account with capital", "deep liquidity on Bybit and Binance") still appears on Trustpilot (snippet). ⚠ Older HyroTrader material may have implied real Bybit sub-accounts. I could not retrieve archived 2024 pages to confirm whether that has changed.

**Regulatory/legal.** None found. Searched for: HyroTrader + regulator/warning/lawsuit/CNB/investor alert. One FCA warning concerns a different brand, "hybitraders.live" (tradersunion, snippet). ⚠ I did not query the CNB, FCA, or UAE warning lists directly.

**Payout reliability.** Trustpilot (page): 4.0/5 from 229 reviews (103 in the last 12 months), 14% 1-star. The company replies to 100% of negatives. The visible negatives concern drawdown closures, spreads, and "back-office delays" after Phase 1 (Mar 2026). No explicit payout denial was visible on page 1.
PropScorer "controversy" article (page, affiliate): an anonymous payout denial ("payout denied" with no explanation; support cited a pattern "inconsistent with our risk model"). It also reports Discord bans of critics and "IP bans" with no detail. All of this is ⚠ unverified.
TheTrustedProp: "no payout-denial reports published", trust score 60/100 (snippet). Payouts are paid "in USDC or USDT unless otherwise agreed" (§11.7). The chain is not stated. **KYC is mandatory before any payout and is done via Sumsub** (§11).

**Bot/API policy (funded).** FAQ "Can I use a trading bot or an AI agent" (page): "Yes, as long as the strategy is your own. You can automate it with a bot, a script or an AI agent, and we issue agent tokens for exactly that. What is not allowed is running someone else's strategy: copy trading, account mirroring, and third-party signal services." ToS §10.2(e) says the same and bans purchased systems. Tealstreet/Tiger terminals are not available in the US or in Bybit-restricted countries.

**Accounts / allocation.** ToS §4.5: "You may hold only one Account for each program type simultaneously". The Provider may also aggregate accounts it believes the same person controls. Aggregate "simulated-capital or exposure limits" are set in the Trading Rules, which give no number on the page I read. Marketing claims scaling to $1M (HyroTrader blog, snippet). Mirroring across accounts (§10.2(b)) and "hedging across multiple accounts" are prohibited (Trading Rules page). **This means one bot copied across N accounts is not possible here.**

**Rule changes 2024–26.**
- Entity moved to UAE/BVI and the model was declared simulated (Aug–Sep 2026 ToS).
- Max drawdown was reportedly cut from 10% to 6% without warning, per early-2026 Trustpilot reviews cited by PropScorer (⚠).
- The minimum daily profit requirement was "cut by half" (company reply on Trustpilot, Sep 2026, page).
- Protections: ToS §6.3/§19.5 says Trading Rule changes do not apply retroactively to active Challenges, and §19 requires 30 days' notice. However, §20.3 allows termination "for any other reason on thirty (30) calendar days' notice".

**Grade: C.**
- (1) It allows your own-strategy bots and gives API/agent tokens, which is the best explicit bot policy found.
- (2) Only one account per program type, plus anti-mirroring and same-controller aggregation, which rules out a fleet.
- (3) Funded is simulated, payouts go through an offshore BVI entity under a separate agreement, and there is a 30-day termination-for-convenience clause.
- (4) Mixed reports: drawdown cuts, Discord bans, and one anonymous denial (unverified).

Sources:
- https://www.hyrotrader.com/terms-and-conditions/ (page)
- https://www.hyrotrader.com/faq/getting-started/can-i-use-a-trading-bot-or-an-ai-agent/ (page)
- https://www.hyrotrader.com/faq/hyrotrader-account/ (page)
- https://www.hyrotrader.com/trading-rules/ (page)
- https://www.trustpilot.com/review/hyrotrader.com (page)
- https://www.propscorer.com/blog/hyrotrader-controversy-full-story (page, affiliate)
- https://thetrustedprop.com/prop-firms/hyrotrader/payout-denials (snippet)
- https://www.streetinsider.com/Press+Releases/Crypto+Proprietary+Trading+Firm+HyroTrader+Experiences+Rapid+Growth/23749169.html (snippet)
- https://www.techdogs.com/tech-news/globe-newswire/hyrotrader-announces-global-expansion-and-industry-recognition-as-one-of-the-leading-crypto-prop-firms (snippet)
- https://proptradingvibes.com/blog/hyrotrader-rules-overview (snippet)
- https://www.hyrotrader.com/blog/hyrotrader-vs-cryptofundtrader/ (snippet, firm marketing)
- https://tradersunion.com/scam-or-safe/hybitrader-review/ (snippet; different firm)

## 2. Breakout (breakoutprop.com) → Kraken Prop / Kraken Funded
**Identity.** Founded in 2023 by TraderMayne, CryptoCred, Alex Miningham (CEO) and Abetrade (The Block, page). Pre-acquisition entity: "Breakout Trading Group, LLC", Tampa, Florida (snippet, via search summary of Finance Magnates/BusinessWire ⚠). Kraken announced the acquisition on 4 Sep 2025, effective 1 Sep 2025 (The Block page; BusinessWire/Payward press release snippet).
The funded program is now provided by **Payward Oceanic Ltd (BVI)**, a Kraken subsidiary. Kraken describes it as unregulated: "not a regulated investment product" (fxnewsgroup page; Yahoo Finance page). Payouts "must be approved by Payward Oceanic Ltd (POL)" (snippet, review site).

**Venue / real vs sim.**
- Breakout's own platform: originally DXtrade; the new **Breakout Terminal** launched 5 May 2026, with "existing DXtrade accounts stay on their current setup" (copygram page, citing Breakout announcement).
- **Kraken Prop** launched inside Kraken Pro on 27 May 2026 (Yahoo page).
- **Kraken Funded** (mobile app, $1k–$10k tiers) launched around 30 Jul 2026 (fxnewsgroup page).
- Kraken: "a simulated trading environment" for the evaluation. The funded wallet is described as "up to $200,000 of Kraken's capital… We cover any losses" (kraken.com/prop page). Whether funded trades hit the live Kraken book is **not stated** ⚠. The Funded Trader Agreement structure (POL/BVI) suggests a notional/simulated model like its peers.

**Regulatory/legal.** None found against Breakout or Payward Oceanic for the prop program. Searched for "Breakout Trading Group" lawsuit/CFTC/cease-and-desist and found only unrelated CFTC items. ⚠ I did not query NFA BASIC, Florida OFR, or court dockets directly. Kraken/Payward (parent) has separate, unrelated US regulatory history that this pass did not review.

**Payout reliability.** Trustpilot (page): 4.7/5 from 1,203 reviews (465 in the last 12 months), 3% 1-star. The firm replies to 46% of negatives. Recent complaints concern fees and leverage, not denials. The firm claims a "Flawless record of 0 payout denials" (marketing). Third parties say payouts are suspended after a breach unless the trader bought "breach insurance". Complaints focus on the daily-drawdown calculation, and one App Store user was breached by a platform-side issue that support confirmed (snippets).
Payouts: "issued exclusively via USDC using the Ethereum network (ERC-20)", on demand, $50 minimum (QuantVPS page quoting Breakout, updated 11 Oct 2026). Kraken says payouts go "directly to your Kraken account", "typically within 24 hours" (kraken.com/prop page). KYC is not needed to buy an evaluation but is required to sign the Funded Trader Agreement (QuantVPS page). Kraken Funded pays out in USD (fxnewsgroup page).

**Bot/API policy (funded).** No official clause could be read (403). Secondary sources disagree:
- Velotrade review: "Bots are permitted, but Breakout Prop bans HFT and latency exploitation", plus no copy trading/signal-following or cross-account hedging (page). **Caveat: the author, Vittorio De Angelis, is Velotrade's Executive Chairman, a competitor.**
- QuantVPS: "automating execution based on external signals crosses into prohibited territory" (page). In a snippet it also says the terminal "lacks bot and EA support".
- Copygram: "We have not verified a public Breakout trading API", and it withdrew an earlier unsourced API claim (page, reviewed 30 Sep 2026).
- Kraken's exchange does allow bots (support.kraken.com, snippet), but that does not cover Prop.

⚠ **Treat as NOT confirmed for a fully automatic bot.** Kraken Prop is "Breakout Terminal only (no MT4, MT5, or TradingView)" (Yahoo page).

**Accounts / allocation.** "$100,000 per account… up to $200,000 across multiple accounts" (The Block, Sep 2025, page). "$200,000 aggregate funded capital per trader" (Yahoo, 2026, page). The Breakout FAQ bans copying between different traders' accounts and "cross-account hedging in the same or closely correlated assets" (copygram page, quoting FAQ).

**Rule changes 2024–26.**
- Acquisition (Sep 2025).
- 2-step evaluation discontinued in May 2026; static drawdown on all plans (Velotrade review page).
- DXtrade → Breakout Terminal (May 2026).
- Rebrand into Kraken Prop (May 2026) and Kraken Funded (Jul 2026).
- The payout path moved to Kraken accounts/POL.

I found no reports that existing funded traders were forcibly changed, but none confirming they were not either ⚠.

**Grade: B- for counterparty/payout risk; C for this client's use case.**
- (1) The strongest owner in the sector (Kraken), the best Trustpilot record, and fast USDC/Kraken payouts.
- (2) Only $200k total per person, which is a hard ceiling on fleet size.
- (3) No verified public API and terminal-only access, so a fully automated bot is unconfirmed and possibly impossible.
- (4) Frequent product and platform changes in 2025–26. It is unregulated and run through a BVI entity.

Sources:
- https://www.theblock.co/post/369612/kraken-breakout-acquisition (page)
- https://www.businesswire.com/news/home/20250904012956/en/Kraken-Completes-Major-Acquisition-of-Breakout-to-Offer-Prop-Trading-to-Clients-Globally (snippet)
- https://www.payward.com/press-release/kraken-acquires-breakout-for-global-prop-trading (snippet)
- https://finance.yahoo.com/markets/crypto/articles/kraken-prop-inside-funded-trader-183521927.html (page)
- https://www.kraken.com/prop (page)
- https://fxnewsgroup.com/forex-news/cryptocurrency/kraken-expands-prop-trading-options-with-kraken-funded/ (page)
- https://www.quantvps.com/blog/breakout-crypto-prop-firm-rules (page)
- https://velotrade.com/blog/breakout-prop-review (page; competitor-authored)
- https://copygram.app/blog/prop-firms/breakout-prop-firm-review-pass-challenge-copygram (page)
- https://www.trustpilot.com/review/breakoutprop.com (page)
- https://www.breakoutprop.com/program-rules/ (403 blocked)
- https://support.kraken.com/articles/360001373983-does-kraken-allow-trading-bots- (snippet)

## 3. Crypto Fund Trader (CFT)
**Identity.** SWISS RLCRATES AG (CHE-162.567.204), Bahnhofstrasse 21, 6300 Zug, Switzerland. Swiss law applies, with courts of Zug (ToS §16.1, page). The ToS has no version date ("© 2026").

**Venue / real vs sim.** CFT runs on MT5, its own CFT platform, and a **Bybit route** where the trader supplies an API key plus subaccount (§3.3.1). Changing the key closes the account (§3.3.2). ToS §1.1.5: "any operation you perform through our service is not real". Final-Stage rewards are "performance-based educational **scholarships**" (§5.2).

**Regulatory/legal.** None found. Searched for CFT/RLCRATES + CNMV/FINMA/lawsuit; results covered only unrelated CNMV warnings. ⚠ I did not check the FINMA or CNMV lists directly.

**Payout reliability.**
- **Trustpilot has suspended the rating: "This company's rating is unavailable due to a breach of our guidelines… We've removed a number of fake reviews"** (page). It shows 1,101 reviews, 14% 1-star.
- Complaints include a payout denied after a "risk interview", a ban for "copytrdaing between many accs", a $5k+ ETH scholarship refused over an undisclosed "correlated assets" rule, Discord bans after asking for payment, and disputes over equity vs balance breaches (page/snippet).
- **ToS §14.2: "it does not guarantee the payment of the paid scholarship to the trader."** The firm may withhold even when targets are met, and the remedy is limited to a fee refund.
- §3.1.10: the firm may "refuse or cancel service, terminate accounts… without providing any reason and with immediate effect".
- KYC is mandatory before any payout (§3.1.11), and interviews may be required (§6).

**Bot/API.** The ToS is silent on EAs. Third parties say EAs are allowed but ban HFT, tick-scalping, arbitrage, news, and "multi-account reverse-trading EAs" (fundedtrading/luxalgo, snippet ⚠). HyroTrader's competitor blog calls CFT bots "Restricted" (snippet). The firm may impose VPS/VPN limits and "anti-copy-trading controls" at any time (§6).

**Accounts.** Break: "prohibited to hold more than five (5) Final Stage accounts at the same time" (§7.1 xxii). Bybit: up to 20 subaccounts (§3.3.4). Max allocation is "as determined in the website's FAQ" (§7.1 xii); the FAQ redirected and could not be read. Copy trading is prohibited on Ascend, even between own accounts, including "mirrored or coordinated trading… whether executed manually, via signals, or through automation", and "the firm's determination… is final" (§7.1 xx). On Break Final Stage it is also not permitted between own accounts (§7.1 xxiii).

**Rule changes.** §1.3.1: "may modify these Conditions or any Policy at any time at its sole discretion"; continued use counts as acceptance.

**Grade: D.**
- (1) The contract states that payment is not guaranteed.
- (2) Trustpilot has suspended its rating over fake reviews.
- (3) Payout denials are tied to multi-account and correlation findings, exactly the bot-fleet profile.
- (4) Rules can change unilaterally at any time.

Sources:
- https://cryptofundtrader.com/terms-and-conditions/ (page)
- https://www.trustpilot.com/review/cryptofundtrader.com (page)
- https://no.trustpilot.com/review/cryptofundtrader.com (snippet)
- https://thetrustedprop.com/prop-firms/crypto-fund-trader/payout-denials (snippet)
- https://fundedtrading.com/propfirm/crypto-fund-trader/ (snippet)
- https://www.luxalgo.com/prop-firms/crypto-fund-trader/ (snippet)

## 4. Velotrade (velotrade.com) – API-first newcomer
**Identity.** Velotrade Re Limited, Hong Kong. Hong Kong law applies, with HKIAC arbitration. ToS last updated 1 Jul 2026 (page). Launched Mar 2026 by ex-JP Morgan/Dresdner traders (PR Newswire release, snippet). CEO Gianluca Pizzituti; Executive Chairman Vittorio De Angelis (May 2026 sponsored release, snippet). The "founded 2016" claim refers to its predecessor invoice-finance business.

**Real vs sim.** ToS §5.1: "No live trading or real capital is involved." Payouts are in USDC/USDT. The chain is not stated in the ToS; the site says "Settled on Arbitrum" (velotrade review page, site text).

**Regulatory/legal.** None found (web search only ⚠).

**Payouts.** No independent proof found. Trustpilot shows only 8 reviews, and **the rating is suspended for a guideline breach / fake reviews removed** (page). A 1-star review (Apr 2026) claims "no single trader has passed… or even gotten a payout"; the CEO disputed it.
Terms: the first payout comes 14 days after the first trade, then weekly. **The first two payouts are capped at 20× the fee, and the excess is forfeited.** The firm may hold or reject a payout on suspicion (5.4(g)).

**Bots.** §8.3: "Use of Expert Advisors (automated trading software) is permitted", but the firm can restrict or ban specific EAs, and HFT is prohibited (8.2(c)). A full API for funded accounts is marketed (May 2026 release, snippet).

**Accounts.** §4.3: "You may maintain only one Account". Multiple challenges/funded accounts are allowed, but combined funded capital cannot exceed **USD 200,000**. "Replicating trades between your accounts" is prohibited (8.2(h)).

**Rule changes.** "We reserve the right to amend these Terms at any time" (§1). Fees and parameters can change at any time (6.4).

**Grade: D.**
- (1) Seven months old, with no independent payout evidence.
- (2) Trustpilot fake-review flag.
- (3) Payout caps and forfeiture, plus unilateral amendment rights.
- (4) Its "Breakout review" is written by its own chairman, so treat its comparative content as biased.

Sources:
- https://velotrade.com/terms (page)
- https://www.trustpilot.com/review/velotrade.com (page)
- https://www.aap.com.au/aapreleases/cision20260313ae09586 (snippet)
- https://news.marketersmedia.com/velotrade-opens-full-api-access-for-funded-crypto-traders/89192761 (snippet)
- https://velotrade.com/blog/breakout-prop-review (page)

## 5. Bitfunded (bitfunded.com) – EXCLUDED (bans bots)
**Bots:** Bitfunded's own FAQ (page): "Every trade has to be placed manually by the account holder". This covers bots, EAs, scripts, and API automation. It contradicts third-party claims that "EAs allowed" (thetrustedprop, page; velotrade compare, snippet). **The firm's own text prevails, so this firm is incompatible with rule (1).**

**Other findings:**
- "Everything happens in a simulated environment"; payouts in USDT on ERC-20/BEP-20/TRC-20 (FAQ page).
- No limit on challenges, but "only one per account size" funded (FAQ page).
- Entity is reportedly Tronovix LTD, UAE, reg. 01010149, operating since Dec 2023 (thetrustedprop page ⚠, unclaimed profile).
- Trustpilot 4.3, 207 reviews (page).
- Recent Oct 2026 complaints: **14 of 16 accounts terminated** for "system error"/"good faith"; a dispute over "multiple accounts"; an unexplained risk-assessment rejection.
- 1-star reviews describe payouts cut by 70% under an unpublished "Anti-Gambling" rule (thetrustedprop page ⚠).

**Regulatory:** none found (web search only).

**Grade: D** (bans bots; multi-account terminations reported).

Sources:
- https://bitfunded.com/faq (page)
- https://www.trustpilot.com/review/bitfunded.com (page)
- https://thetrustedprop.com/prop-firms/bitfunded (page)

## 6. Not assessed in depth
- **Hola Prime:** bot policy conflicts across third parties (FXEmpire says EAs supported; another review says no automation on futures). FXEmpire reports that Trustpilot flagged it for possible fake reviews. Entity is listed as Mauritius/US or Hong Kong (snippets only: https://fxempire.com/prop-firms/holaprime , https://www.eltraderfinanciado.com/es/review/hola-prime). ⚠ Not verified.
- **PropW, Funded Trading Plus crypto, and Bybit/Binance-linked programs:** I found no primary-source evidence that any of them allows bots on funded accounts across many accounts. No exchange-run program (besides Kraken) was found.

## Gaps / next steps
- Regulator lists (CNB, FCA, FINMA, CNMV, SFC-HK, NFA BASIC, Florida OFR) were not queried directly; "none found" means web searches only.
- Breakout/Kraken Prop terms and the Funded Trader Agreement were unreadable (403). Kraken support-center Prop articles should be read for bot/API wording.
- The HyroTrader Funded Trader Agreement (BVI entity) and Trading Rules aggregate caps were not located.
- The CFT FAQ (max allocation) redirected and was not read.
