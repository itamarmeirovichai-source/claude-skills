# D5: Contract clauses that matter for a fully automated bot run on many accounts (12 FX and crypto prop firms)
Accessed 2026-10-11 for every source. **[page]** means the firm's own page was read directly (curl, then text extraction). **[snippet]** means only a search-engine snippet or summary was seen. ⚠ means unconfirmed. Quotes are verbatim unless marked as a paraphrase.
**Blocked hosts:** e8markets.com and help.e8markets.com (403, Cloudflare); fundingpips.com and help.fundingpips.com (429 Vercel checkpoint, then 403); breakoutprop.com and help.breakoutprop.com (403, Cloudflare "Just a moment"); alphacapitalgroup.uk/terms-and-conditions (403). The ACG help center was readable. web.archive.org could not be used: the connection was reset through the proxy, and WebFetch refused it. Snapshots do exist for ACG T&C (2026-08-12), Funding Pips T&C (2026-10-02) and Breakout terms-of-use (2026-10-02), but none could be opened. **The shared WebSearch budget ran out partway through**, so these are still open: governing law for ACG, E8, Funding Pips and Breakout; Breakout's bot/API rule; The5ers' news rule and max-allocation figure.

---
## Cross-firm summary for a bot fleet

| Firm | Bot on funded? | Same-trade / copy across OWN accounts | Max funded allocation | Main fleet killer |
|---|---|---|---|---|
| FTMO | Allowed ("algorithmic trading, EAs") | Not banned outright. Limit applies "per trader **or strategy**" | $400k per trader/strategy | Limit counted per **strategy**. Third-party EA risks denial. 2,000 requests/day cap |
| The5ers | **Needs prior written approval**. Third-party software banned | "Trade coordination or copy trading with other traders **or accounts**" banned | Exists, figure ⚠ | Prior written approval. "Bulk trading … clearly showing a trader is not behind the strategy" |
| FundedNext | **Banned on accounts ≥$50k**. Banned on cTrader and Match-Trader | **Banned between funded accounts, even your own** | $300k | Copy ban between own funded accounts. EA ban at ≥$50k. **USD 25,000 penalty per breach** |
| FTUK | Only "risk management EAs" | **Banned**: "same trades on multiple FTUK accounts is a violation". Even trading the same asset at the same time can be flagged | 3 forex + 3 futures accounts | Own-account copy ban plus the 3-account cap. "not rely on … bots" |
| Alpha Capital | **Autonomous EAs banned** "under any circumstances" | Allowed only after declaring Master/Slave | Household cap, figure ⚠ | Ban on fully automated EAs. VPS needs advance notice and a static IP |
| E8 Markets | Allowed, but "one strategy per user" [snippet] | Allowed across own accounts [snippet] | $500k per market (E8 One/Pro) [snippet] | Same EA used by several users can mean termination |
| Blue Guardian | "EAs are allowed" (own setup) | Allowed between own accounts | $400k | T&C ban "third-party strategy, off-the-shelf strategy". "VPS services linked to multiple trader accounts" banned |
| Funding Pips | Third-party EA only as trade or risk manager [snippet] | Allowed same-direction across own accounts [snippet] | $400k [snippet] | **VPN/VPS banned while accessing the account** [snippet]. Third-party EA ban |
| FundingTraders | **Banned unless the Risk Team grants an exception** | Allowed under the same verified profile | ⚠ not stated | "EAs/Bots allowed only if used for risk management". "off-the-shelf bots are forbidden" |
| Maven | **"EAs are not permitted under any circumstances"** | Not explicit (mirroring banned on one product) | $200k starting | Total EA ban |
| HyroTrader (crypto) | **Allowed for your own strategy** (API, MCP, agent token) | **Banned**: any "strategy that relies on … positions taken across two or more Trading Accounts" | ⚠ (can aggregate connected accounts) | Cross-account strategy ban. One account per program type |
| Breakout (crypto, Kraken) | ⚠ unknown (pages blocked) | ⚠ | $200k combined [snippet] | "third-party strategy, off-the-shelf strategy" ban. No multiple accounts from the same device or IP [snippet] |

---
## 1. FTMO (FTMO Evaluation Global s.r.o., Prague)
Sources [page]:
- FTMO Challenge T&C PDF, "LAST UPDATED ON 4 AUGUST 2026": https://cdn.ftmo.com/docs%2Fterms-and-conditions%2Ff8d5ca5086964c86a6ee2a77f20bdbd7 (linked from https://ftmo.com/en/terms-and-conditions/)
- Forbidden Trading Practices (FTP): https://ftmo.com/en/forbidden-trading-practices/
- FAQs: https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/ , /how-many-accounts-can-i-have/ , /can-i-trade-news/ , /can-i-travel-or-use-vpn-vps/ , /do-you-have-any-consistency-rules/
- Trading Objectives: https://ftmo.com/en/trading-objectives/

The separate FTMO Account (funded) T&C with FTMO Trading was not read ⚠.

- **a. EAs/HFT**
  - FAQ: "we have no reasons for limiting or restricting your trading strategy, whether it's discretionary trading, algorithmic trading, EAs, etc."
  - FAQ: "if you use an EA from a third party, there might be other traders already using the same EA and therefore exactly the same strategy. By using a third-party EA, you potentially run a risk of being denied the FTMO Account if you exceed the maximum capital allocation rule. Please note that platform servers have 200 orders at a time and 2000 max positions per day limitation … If your EA causes hyperactivity … we might alert you and ask you to adjust the EA logic"
  - FAQ: "If we identify intentional activities or Modus Operandi being repeated on more accounts, we reserve our right to take the necessary action … terminating the account completely and ceasing our cooperation altogether."
  - FTP: must not "use any software, artificial intelligence, ultra-high-speed tools, or mass data entry that might manipulate, abuse, or give you an unfair advantage". Also: "perform simulated trades that are operated or managed by automated robots / EAs (Expert Advisors) which cause the trading account to become hyperactive in the sense of an excessive number of more than 2,000 server requests per day … causing overload of the trading server". Also bans exploiting "delays in their updates, or an external or slow data feed".
  - T&C 3.14.2: an "unusually large number of Orders" can lead to "suspend any further Orders … or invoke a cool-down period".
- **b. Prohibited strategies**
  - FTP bans gap trading "when major global news … are scheduled" or "two hours or less before a relevant financial market is closed for at least two hours".
  - FTP also bans "(e.g., overleveraging, overexposure, one-sided bets, account rolling)".
  - T&C 7.4: "prevent activities we deem analogous to gambling".
  - T&C 7.5: avoid "opening substantially larger position sizes … opening substantially smaller or larger number of positions compared to your other simulated trades, regardless of which of your accounts are concerned".
- **c. Copy and hedging**
  - FTP: must not trade "alone or in concert with other persons — including between connected accounts, accounts held with various operators/providers … simultaneously entering into opposite positions (with the exception of … a single simulated account)".
  - T&C 7.2.1: no third party may "perform simulated trades for you or in coordination with you".
  - No explicit ban on copying your own accounts, but see g.
- **d. Consistency and minimum days**
  - "Best Day Rule requires that your Best Day does not represent more than 50% of your Positive Days' Profit" (1-Step Challenge and 1-Step FTMO Account). Exceeding it is "not treated as a rule breach".
  - 2-Step: "at least 4 Trading Days … There is no Minimum Trading Days rule on the subsequent FTMO Account (2-Step)".
  - T&C 7.6.9 allows "temporary or permanent consistency measures".
- **e. News on funded:** Standard account: "not permitted to open or close any trades, including the execution of pending orders … within a time window starting 2 minutes before and ending 2 minutes after" selected releases. "Violating this rule may result in termination". Swing accounts are exempt.
- **f. IP/VPS:** "The use of VPN/VPS is also generally allowed". The only exception is US geolocation on MetaTrader and cTrader. T&C 9.5: "You must inform us if you use … the same device … with any other user".
- **g. Max allocation**
  - FAQ: "the total capital allocation across all accounts is limited to $400,000 per trader **or strategy** … If identically traded strategies are detected across multiple FTMO accounts and the total fictitious capital exceeds the maximum capital allocation limit, FTMO reserves the right to suspend the affected accounts."
  - T&C 6.3: "USD 400,000 … calculated in aggregate per client, per strategy and per ultimate beneficial owner".
- **h. Discretion, termination, law**
  - 7.3: "We reserve the right to determine, at our own discretion, whether certain simulated trades … qualify as … a Forbidden Trading Practice. We may update the list … from time to time."
  - 7.6 remedies include cancelling trades, terminating, reducing leverage, and "7.6.9 … any other additional measures".
  - 7.7: "we are not required to notify you before taking such action."
  - 7.8: an FTP on any account allows FTMO to "terminate all Agreements relating to all FTMO Challenge Accounts you have".
  - 7.9: "You are also not entitled to any refund of the FTMO Challenge Fee."
  - 13.2.4: "Either party may terminate the Agreement without cause by serving a written notice at least five (5) business days in advance". 13.5: no compensation.
  - 15.1: amendments take effect on 7 days' notice, and "continued use … acceptance". Rejecting them terminates all Agreements, with no compensation.
  - 18: Czech law; Czech courts; Czech COI for out-of-court consumer ADR.
- **i. Platform change:** 5.6: "We reserve the right to modify, change, replace, add, or remove any elements and functions of the Services at any time without being obliged to pay you any compensation." 7.1: restrictions "may also be imposed by third parties who provide the Trading Platform".
- **FLEET KILLERS:**
  1. The $400k limit is counted **"per trader or strategy"**. One bot on many accounts, or a bot that other buyers also run, shares one $400k cap. Accounts above it can be suspended.
  2. "Modus Operandi being repeated on more accounts", plus the third-party-EA denial warning.
  3. 7.5.2 compares trade counts "regardless of which of your accounts", and the 2,000-requests-per-day cap applies.

## 2. The5ers (Five Percent Online Ltd)
Sources [page]:
- T&C: https://the5ers.com/terms-and-conditions/ (no date on the page; footer reads ©2026)
- Prohibited Trading Practices, "last update: July 28, 2026": https://the5ers.com/faqs/prohibited-trading-practices/

- **a. EAs**
  - T&C "Use of Automated Trading Software": "User shall notify the Company in writing and obtain written approval from the Company prior to using any Automated Trading Software; no Automated Trading Software may be used unless the Company has given prior written approval for its use, which approval shall be at the Company's sole discretion … the Company may require advance testing … Notwithstanding the foregoing, the Company prohibits use of any Automated Trading Software owned or developed by any third party other than the User."
  - Trading Rules list (T&C): "High-frequency trading in which the majority of trades duration span is measured within a few seconds or less"; "Expert advisors from a third party where other traders have the same trades open"; "Using an expert advisors from a provider where the trader does not own the source code"; "Tick Scalping; Hedge Arbitrage Trading; Reverse Arbitrage Trading"; "Using any software, artificial intelligence, ultra-high speed, or mass data entry which might manipulate…".
  - PTP page: "**Bulk trading**, is when multiple trades are open simultaneously. Situation: A trader opens manually or uses automatic trading tools that open multiple trades at the same time, clearly showing a trader is not behind the strategy activity."
  - PTP page: "Using automated robots or Expert Advisors that cause the trading account to generate an excessive number of server requests per day…"
  - PTP page states the list "works both for our evaluation phases and funded accounts".
- **b. Prohibited strategies:** "One sided-bets"; "Bracketing strategy … around high-impact news"; gambling-like "speculative position-taking"; "Overleveraging or overexposure"; "Engaging in other conduct which in the sole discretion of the Company, represents uncommercial activity". Termination also covers anyone who "manipulated Our systems, whether manually or through any use of an automated system (e.g. bot)".
- **c. Copy and hedging:** "Trade coordination or copy trading with other traders or accounts"; "Cross-operator coordinated trading … across accounts held with different providers"; "Account sharing or reselling accounts".
- **d. Consistency:** the PTP bans "artificially distribut[ing] profit across multiple days". Position sizes "substantially larger or smaller … whether compared across your own accounts". No % figure was found ⚠.
- **e. News on funded:** only the bracketing ban was found. The funded news window is ⚠ (search budget exhausted).
- **f. IP/VPN:** "circumvention of geographical restrictions (including through the use of VPN …) constitutes a fundamental breach". No VPS rule was found ⚠.
- **g. Accounts**
  - "Except upon Our prior written approval in specific cases, We allow only one Account per User." This is the user profile.
  - "We impose limitations on the maximum funding capital you can purchase for Evaluation accounts." The figure is ⚠.
- **h. Discretion and law**
  - "We may modify these Terms from time to time in Our sole discretion. You shall be bound by such modifications effective immediately upon posting".
  - A fundamental breach allows the firm "to immediately terminate Your Account(s) … without any refund of fees paid … and any accrued profits or Reward Balance shall be immediately forfeited".
  - "Payout Threshold" can be amended "at any time".
  - Non-disparagement clause.
  - "governed by … the laws of Israel … exclusive jurisdiction of the competent courts of Israel". Elsewhere: "courts of Tel Aviv".
- **i. Platform change:** "We reserve the right to modify, change, replace, add, or remove any elements and functions of the Website and/or Services at any time without any compensation."
- **FLEET KILLERS:**
  1. **Prior written approval** is required for any automated software, at sole discretion, and third-party-developed software is banned outright.
  2. **"Bulk trading … clearly showing a trader is not behind the strategy"**, together with "copy trading with other … accounts". A bot firing the same orders on many accounts matches both.
  3. "EA from a third party where other traders have the same trades open", and the source-code ownership requirement.

## 3. FundedNext (GrowthNext F.Z.E., Ajman)
Sources [page]:
- Terms of Service, "Last updated: 5 May 2026": https://fundednext.com/terms-of-service
- CFDs Challenge Terms, "Last updated: 5 May 2026": https://fundednext.com/cfd-challenge-terms
- Help articles: EA https://help.fundednext.com/en/articles/8020763-do-you-allow-eas-indicators (dated September 8, 2026); copy trading /8019805-…; prohibited strategies /8020351-…; accounts /8027523-…; news /10701447-…; device /9351758-…; risk limit /14702245-…

- **a. EAs**
  - Help: "Traders on account sizes of $50,000 and above must trade manually and may not use Expert Advisors, trading bots, or any automated tools". Also: "EA and bot trading are not allowed on cTrader and Match-Trader".
  - Help, for accounts under $50k: third-party EAs are allowed "with an additional EA usage fee". "Each EA or bot is required to employ a distinct strategy, avoiding identical trades across any accounts within FundedNext. There is a maximum allocation limit of $300,000 for each EA or trading bot's strategy." Bots "designed specifically to pass Prop firm challenges are strictly prohibited".
  - CFD Terms 8.14: "must not use bots, scripts, algorithms, software, AI agents, or automated methods not expressly authorised by the Provider … mass-order behaviour … overload systems".
  - 8.2 bans latency arbitrage and "quote stuffing". Help adds "Quick Strike": profit share from trades under 30s of "30% or higher constitutes a violation".
- **b. Prohibited strategies:** 8.15 "excessive one-sided exposure, repeated 'all-in' bets, grid trading, tick scalping … account rolling". 8.7 "Group Trading; Coordinated Trading … synchronised entries/exits". Help lists "Gambling Behavior … One sided Betting, Hyperactivity".
- **c. Copy and hedging**
  - Help: "Copy trading is strictly prohibited between a FundedNext Account and any other FundedNext Account or FundedNext Challenge Account, **whether it belongs to the same individual** or another entity. This applies to both manual and automated trading setups".
  - Detection: "Identical Trades: If multiple accounts show the same entry price, exit price, lot size, symbols, or trade time".
  - Consequence: first violation means "No Performance Reward … for the affected cycle". A subsequent one means "Account Termination. No Performance Reward or Refund".
  - Challenge-to-Challenge copying is allowed up to $300k with a declared master. Cloud copiers are banned.
  - 8.8 bans cross-account hedging across own, related and other-firm accounts.
- **d. Consistency and minimum days:** 2 days (1-Step) or 5 days (2-Step and Lite). A 40% consistency rule applies under the "On-Demand" arrangement for flagged traders. A 3% max risk at any time applies on the funded account. Help: "applies to … manual or automated".
- **e. News on funded:** for trades within ±5 minutes of listed high-impact news, "40% of the profit from these profitable trade(s) will be counted".
- **f. Devices and IP:** "Using a device that belongs to or is shared with another trader is strictly prohibited". VPN is allowed if the IP is not from a restricted country. The CFD Terms 8.13 ban VPN or automation "intended to circumvent controls". A VPS-based copier is allowed only between own Challenge accounts.
- **g. Max allocation:** "maximum aggregate simulated capital of $300,000 within their FundedNext Accounts". It is $50k for some countries.
- **h. Discretion and law**
  - ToS 5.8: may "deny, withhold or reverse Performance Rewards". 12.10: past payouts create no "vested right".
  - ToS 22.1: may "at any time … modify, update, supplement or replace these Terms, Policies, Trading Rules, Programme Parameters".
  - **CFD Terms 9.8: "the Customer shall pay the Provider a contractual penalty of twenty-five thousand American dollars (USD 25,000) for each such breach and/or … for each trade, strategy pattern, account, device … constituting or evidencing a breach".** 9.9 allows set-off against rewards and refunds.
  - ToS 18.8: claims are time-barred after 6 months. 18.9: class-action waiver.
  - ToS 27: laws of Ajman and the UAE; DIAC arbitration with 1 arbitrator.
- **i. Platform change:** ToS 2.3: providers are used "at its discretion". ToS 22.1 covers changes driven by "requirements of essential third parties (including platform providers…)". No migration guarantee was found ⚠.
- **FLEET KILLERS:**
  1. **No bots on accounts of $50k or more**, and none on cTrader or Match-Trader.
  2. **Copying or identical trades between your own funded accounts is banned.** One bot on N funded accounts is exactly the pattern the firm detects.
  3. **The USD 25,000 penalty "for each … account"**, set off against payouts, plus the $300k per-strategy cap.

## 4. FTUK (Netherlands law)
Sources [page]:
- ToS: https://ftuk.com/terms-of-service (undated)
- FAQ articles: https://faq.ftuk.com/en/articles/14364398-… (EA); /12339773-is-copy-trading-allowed; /12339786-how-many-accounts-can-i-trade-simultaneously; /12339813-can-i-use-a-vpn-or-vps; /12339790-what-are-account-breaches; /12339798-what-is-the-consistency-score; /12310193-one-step-program-rules-forex. All are marked "Updated over … weeks ago".

- **a. EAs**
  - FAQ: "FTUK allows the use of any risk management EAs (trading bots), but the following strategies are strictly prohibited … Martingale, Tick scalping, Reverse arbitrage trading, Latency arbitrage trading, Hedge arbitrage trading, Grid trading or High-Frequency Trading (HFT), defined as opening and closing trades within 30 seconds."
  - ToS: "Traders should use their own strategy at all times and not rely on signals, bots or software." ToS prohibited list: "Employing third-party, off-the-shelf, or account passing services."
- **b. Prohibited strategies:** "Anti Scaling". "Any strategy designed to exploit demo account conditions".
- **c. Copy and hedging**
  - FAQ: "You are not allowed to copy trades between multiple FTUK accounts. Placing the same trades on multiple FTUK accounts is a violation."
  - Accounts FAQ: "use a different strategy on each account … at the same time, the asset being traded should not be the same - this could be flagged as copy trading."
  - ToS bans "copy trading or hedging across multiple user accounts". Copying external-to-FTUK is allowed.
- **d. Consistency and minimum days:** One-Step needs 4 trading days and 0.5% "Minimum Daily Profit". Consistency is ≤20% on Instant, Flex and Futures. The "Account Protector" closes trades at −2% floating, and repeat triggers terminate the account.
- **e. News on funded:** no restriction found ⚠.
- **f. IP/VPS:** "You are allowed to use a fixed VPS or VPN as long as the trades originate from the same IP address". ToS: "Using multiple IP addresses from many countries or masking IPs. Trading IP's must show from the same region as the billing address."
- **g. Max accounts:** "up to 3 forex accounts and 3 futures accounts at once".
- **h. Discretion and law**
  - ToS: guidelines "may change from time to time in FTUK's sole discretion". On prohibited trading, "participation in the program will be terminated and any profit share will be reduced to 0%".
  - §19: "there are no refunds on any Service". §22: the firm may "update, change or replace any part … by posting".
  - §21: laws of The Netherlands. No forum clause was found ⚠.
- **i. Platform change:** "In the event that a trading platform selected by the client becomes unavailable … complimentary transfer to an alternative supported platform … prior trading history or profits cannot be migrated … positive account balances will be adjusted to reflect the trading level initial funding balance". In other words, **profits are lost on migration**.
- **FLEET KILLERS:**
  1. Same trades on more than one FTUK account is a violation, and even trading the same asset at the same time can be flagged.
  2. The 3-forex-account cap.
  3. ToS: "not rely on … bots or software", which in practice limits EAs to risk management only.

## 5. Alpha Capital Group
The T&C page alphacapitalgroup.uk/terms-and-conditions returned 403. An archive snapshot exists (2026-08-12) but was unreachable.
Help center sources [page]:
- https://help.alphacapitalgroup.uk/en/articles/6934236-can-i-use-an-expert-advisor-ea (September 7, 2026)
- /6934275-what-are-prohibited-trading-strategies
- /8786973-is-copy-trading-allowed
- /6933901-what-is-classified-as-hedging-and-stacking
- /8420522-what-is-the-ip-rule-are-vpns-and-vpss-allowed
- /9293522-can-i-trade-news (August 25, 2026)
- /7060909-…policy-against-gambling…
- /7060898-can-i-pass-using-someone-s-signals

- **a. EAs**
  - "Automated EAs that execute trades independently, without human oversight, are strictly prohibited and will not be approved under any circumstances. … This prohibition includes third-party bots, fully automated strategies, high-frequency trading, and latency arbitrage strategies. The use of any such system will result in immediate account closure."
  - "If multiple traders are identified using the same EA and placing identical trades, this will be treated as a breach of our 'No Group Trading' policy".
  - "We require all EAs to be pre-approved before use". EAs only work on MT5.
- **b. Prohibited strategies:** "Latency trading, Arbitrage trading, High-frequency trading, Reverse trading/group hedging, Position spamming, Group trading/signal following".
  - Position spamming is "3 or more positions, each opened within 60 seconds of the previous one".
  - Gambling: "'all or nothing' … A significant change in lot size compared to the overall average".
- **c. Copy and hedging:** "Copy trading between two Alpha Capital Group accounts … is allowed; however, we still require you to provide the Master and Slave account numbers before copy trading begins". "Only one account can serve as a Master". "Hedging across two Alpha Capital Group accounts is also considered a prohibited strategy … correlated instruments may be considered."
- **d. Consistency:** "2-minute average trade duration" rule. A % figure was not obtained ⚠.
- **e. News on funded:** Pro, One, Three and Direct: "NOT permitted to execute any new trades or close existing trades on the targeted instruments … 5 minutes before and 5 minutes after". SL or TP fills inside the window count as violations, and "profits earned will not be eligible". Swing: trades opened within ±2 minutes must last more than 2 minutes.
- **f. IP/VPS:** "You are allowed to use a VPN or VPS, as long as … It must have a static dedicated IP address. You must notify our support team by email … before using it, stating the account(s) involved. Using a VPN or VPS without prior notification will be flagged … and will lead to account closure and a potential permanent ban."
- **g. Max allocation:** a "maximum allocation per household" rule exists. The figure is ⚠ (secondary sources cite qualified accounts "up to $200,000" per the help text).
- **h. Discretion:** "reserves the right to terminate agreements immediately in the event of any breach … profits from invalid trades, or the entire profits from that payout window … will be removed". Governing law, refunds and amendment terms are ⚠ (T&C blocked).
- **i. Platform change:** ⚠ not found.
- **FLEET KILLERS:**
  1. **A fully automated EA is banned "under any circumstances"**, which rules out the client's model outright.
  2. The same EA with identical trades across traders counts as group trading.
  3. Undisclosed VPS use leads to account closure.

## 6. E8 Markets (E8 Funding LLC; E8 Markets Ltd, Saint Lucia per secondary sources)
**All hosts returned 403 and no archive was found, so everything here is [snippet] from search summaries of the help center.**
- Help center articles: https://help.e8markets.com/en/articles/6929927-trading-policies-and-prohibited-trading-strategies , /5515409-can-i-use-indicators-or-expert-advisors… , /9453469-can-i-copy-trades-or-trade-as-a-team , /5515039-how-many-accounts-can-i-apply-for-at-once , /11775980-e8-one
- Terms: https://e8markets.com/e8-markets-terms-and-conditions

- **a. EAs:** third-party EAs are allowed but the firm "limits one strategy per user". Several users on the same EA "can lead to account termination", and E8 recommends each user run their own programmed EA. This is a paraphrase ⚠. HFT is prohibited: one page says more than 50% of trades held under 1 minute; the futures page says more than 300 trades per day.
- **b. Prohibited strategies:** hedging across accounts, all-or-nothing trades (risking the whole daily drawdown on one position), HFT.
- **c. Copy:** copying across your own accounts is allowed. Teams making the same trades and signal services are banned. "opening equal Long and Short trades on the same instrument across multiple accounts is strictly prohibited" (snippet quote).
- **e. News:** E8 One SimFi Performance account bans trading ±5 minutes around high-impact news. E8 Pro has no restriction (snippet).
- **f/g. Allocation:** "Max for E8 One = $500,000 allocation per market". "These allocation limits apply per household. Multiple users within the same residence/same IP must not exceed this collective maximum." Excess accounts are "kept as a reserve". The Terms say "each Participant is permitted to register and maintain only one (1) Platform account unless expressly authorized in writing" (snippet).
- **h/i.** Governing law, termination, refund and platform-change terms are ⚠ not obtained.
- **FLEET KILLERS:**
  1. "One strategy per user", with termination where multiple users share an EA. This hits a bot that is sold to or copied by others.
  2. The household/IP allocation cap.
  3. ⚠ The full Terms could not be read.

## 7. Blue Guardian (Iconic Exchange FZCO t/a Blue Guardian, Dubai; Blue Guardian Ltd, St Lucia)
Sources [page]:
- T&C: https://blueguardian.com/terms-and-conditions (undated)
- Help: https://help.blueguardian.com/en/articles/9661512-prohibited-trading-practices-account-policies (June 25, 2026); /14062291-2-step-standard-rules (September 9, 2026); /15618204-general-information-rules; /15846933-can-i-purchase-more-accounts-than-the-maximum-allocation-limit (July 6, 2026); /9661525-platform-rules (August 21, 2026)

- **a. EAs**
  - Help: "EAs are allowed. You may use EAs … that you setup to suit your own strategy". Tick scalping is defined by a 2-minute minimum hold. "Tick scalping, high-frequency trading, or arbitrage bots" are banned.
  - T&C Prohibited Trading: "**Utilizing any third-party strategy, off-the-shelf strategy or one marketed to pass challenge accounts**"; "Utilizing one strategy to pass an assessment and then utilizing a different strategy in a funded account".
- **b. Prohibited strategies:** Gambling: "Trading activity will be classified as gambling if margin usage exceeds 80%". T&C bans a "'Boom or Bust' approach". The firm may "deny a withdrawal request if it is deemed a customer has … not applied an appropriate risk management strategy".
- **c. Copy and hedging:** copying is allowed "between your own Blue Guardian accounts". "hedging between separate accounts is strictly prohibited". T&C bans "account multiplication, coordinated activity … hedging across accounts".
- **d. Minimum days and consistency:** 2-Step Standard needs 3 profitable days of 0.5% or more. Funded "Guardian Shield": a 2% floating loss auto-closes trades; the 1st time cuts the split to 50%, the 2nd breaches the account.
- **e. News on funded:** "refrain from Opening/Closing trades 5 minutes before and 5 minutes after red folder (high-impact) news events … Any profits … will be subject to removal".
- **f. Devices, IP and VPS**
  - "The use of shared devices, including mobile phones, desktops, laptops, or **VPS services linked to multiple trader accounts**, is strictly prohibited … Accounts linked to shared devices may be flagged for review during payout". Ambiguous: "multiple trader accounts" may mean multiple traders ⚠.
  - "While VPNs and VPS are allowed, using either service to bypass rules related to copy trading, group trading, or signal trading is strictly prohibited."
- **g. Max allocation:** "the maximum active funded allocation allowed at any time is $400,000 across all funded account types". Extra passed accounts "remain inactive". The scaling plan goes to $4M. T&C: "Traders are limited to one active account per challenge level, absent prior written approval".
- **h. Discretion and law**
  - "All compliance and risk-related decisions … remain final and binding".
  - "reserves the sole and absolute discretion to determine any breach and may, without prior notice, take action including … trade voiding … payout denial".
  - "reserve the right to refuse or cancel service, terminate accounts … at our sole discretion".
  - Prohibited Trading "may include forfeiture of any fees paid".
  - Terms may be changed "in its sole discretion". UAE law. ICDR arbitration seated in Dubai, with Dubai courts as fallback. Class-action waiver.
- **i. Platform change:** "Platform migration is only permitted if no trades have been executed on the account."
- **FLEET KILLERS:**
  1. The T&C ban on "third-party strategy, off-the-shelf strategy" catches any purchased bot.
  2. The ban on "VPS services linked to multiple trader accounts", with review at payout. One VPS hosting many accounts is a risk ⚠.
  3. The $400k funded cap, with breach and payout denial at "sole and absolute discretion".

## 8. Funding Pips
**fundingpips.com and the help center were blocked (429 Vercel checkpoint, then 403). Everything here is [snippet] from search summaries.**
- Terms: https://fundingpips.com/terms-and-conditions
- Help: https://help.fundingpips.com/hc/en-us/articles/34505029138449-Trading-Conduct-and-Security-Standards , /34502157694865-FundingPips-Zero , /34501809112081-2-Step-Standard
- Blog: https://fundingpips.com/blog/fundingpips-maximum-allocation

- **a. EAs:** Terms: "Using a third-party Expert Advisor is allowed only when it functions as a trade or risk manager; using any other third-party Expert Advisor is not allowed and will result in a violation of the account and the decline of your remuneration." The summary also says full automation is allowed only for your own EA with proof of ownership ⚠. The Terms ban "gap trading, high-frequency trading, toxic trading flow, server spamming, latency arbitrage, hedging, long-short arbitrage".
- **c. Copy:** copying between your own accounts in the same direction is permitted. Coordinated hedging between accounts and inbound copying from outside sources are banned. Appendix B bans hedging "across different individuals, accounts, or firms".
- **d. Consistency:** Zero: largest day ≤15%. 2-Step Standard: 35% on On-Demand and Monthly cycles.
- **e. News on funded:** Zero: trading in the window is a hard breach. 2-Step: profits made in the window are not counted.
- **f. IP/VPS:** IP region must stay consistent. "connecting to a VPN or VPS while accessing your trading account is not permitted" (summary paraphrase ⚠ worth verifying).
- **g. Max allocation:** "$400K" across Evaluation and Master accounts.
- **h/i.** Governing law, termination and refund terms are ⚠ not obtained.
- **FLEET KILLERS:**
  1. **The VPN/VPS ban**, if accurate. A 24/7 bot practically needs a VPS.
  2. Third-party EAs are allowed only as trade or risk managers.
  3. The $400k cap.

## 9. FundingTraders (FT US Inc; UAE law)
Sources [page]:
- Terms of Service, "Effective date of this version: September 1, 2026": https://fundingtraders.com/terms-of-service
- FAQ on the homepage: https://fundingtraders.com/

- **a. EAs**
  - 1.2.1: "Users may not use any EAs, scripts, or robots unless the FundingTraders Trading Evaluation Risk Team has granted such an exception."
  - §8: "EAs/Bots allowed only if used for risk management. Grid, hedge, martingale, arbitrage, and off-the-shelf bots are forbidden. All trading must originate from the trader's own analysis."
  - 5.8: "High-Frequency Trading (HFT): Not allowed for any account (defined as trades lasting 15 seconds or less)". Arbitrage, latency and HFT-like systems lead to "immediate termination".
- **b. Prohibited strategies:** 5.9 "Toxic Trading Practices … One-Sided Trading, Account Rolling/Stacking". Martingale and grid are banned. 6.3 is a strike-based "Discipline Program".
- **c. Copy:** "Replication of a user's own trades between accounts held under that user's own verified profile is permitted". The firm may deem coordination "where several users trade the same instruments in the same direction within one minute of each other … Failing to comply with this rule will result in the termination of all FundingTraders accounts owned by the user." 6.3.12 makes hedging and cross-account coordination hard breaches. The FAQ says copy-trading software between FT Instant Accounts is not allowed.
- **d. Consistency and minimum days:** 6.1: "1-STEP PRO: Your biggest trading day must not exceed 50% … IF: … 15%". 2-Step: none. Minimum days: 4.
- **e. News on funded:** 5.4: "News-influenced profits must not exceed 30% of total PnL … within 5 minutes before or after". Instant Funding: "No trading 10 minutes before or after".
- **f. IP:** 12.4: "IP addresses, device IDs, and behavioral data maps will be used by the automated risk system". "Only one user profile per verified individual … can have multiple accounts."
- **g. Max allocation:** ⚠ not stated in the ToS.
- **h. Discretion and law:** 15: the firm may modify "at any time, at its sole discretion". 11: "Either party may terminate with 5 business days notice". 3.x: no refund on termination. Breach forfeits the fee refund. UAE law (§14).
- **i. Platform change:** ⚠ not found.
- **FLEET KILLERS:**
  1. **No bots without a Risk Team exception.** Bots are otherwise allowed only for risk management, and "off-the-shelf bots are forbidden".
  2. The 1-minute same-direction coordination test, which catches a bot that other users also run, and terminates "all" accounts.
  3. 5-day termination without cause.

## 10. Maven Trading (MAVEN LLC, UAE)
Sources [page]:
- T&C, "Last Amended: 22/10/2025": https://maventrading.com/terms-and-conditions
- FAQ: https://maventrading.com/faq

- **a. EAs:** "**EA: EAs are not permitted under any circumstances across all our platforms.**" The T&C also says: "Using Expert Advisors (EAs), bots, or other automated systems is prohibited unless you have received prior approval". The two statements conflict, and the FAQ/T&C line "not permitted under any circumstances" is the stricter one. Also banned: "High-Frequency Trading, Toxic Trading Order Flow, Long/Short arbitrage, reverse arbitrage, tick scalping, and server execution", and "server flooding".
- **b. Prohibited strategies:** "Gamifying … risking a large percentage of your account on single bets with a 1:1.25 or lower risk-to-reward ratio"; "all-or-nothing trading strategies"; "single betting plans"; "Grid/Gap Trading".
- **c. Copy and hedging:** "You cannot copy trade from another individual, if found, both users will be breached." "Reverse/Group Hedging" is banned. The Prediction Markets product says "No account mirroring".
- **d. Consistency and minimum days:** "MAVEN INSTANT requires a 20% consistency score". 2-Step: "three minimum profitable trading days of 0.5%".
- **e. News:** "For all accounts, you may not place new trades or close existing trades within 2 minutes before or after 'Red Folder' news events".
- **f. IP:** "Your IP address throughout your Maven journey must match the same geographical region".
- **g. Accounts:** "Each person is allowed to register only once". "You can have up to $200,000 in starting capital on funded" (scaling to $1M).
- **h. Discretion and law**
  - "Maven LLC has the right to terminate an account as it seems appropriate". "Maven reserves the right to forfeit a traders virtual profits when deemed necessary."
  - Refunds: none, "except after receiving three payouts". The firm may limit risk to 1% "at any point".
  - Terms may change "at our sole discretion". UAE/DIEZ law; mediation, then arbitration, then the courts of "Al 'Ulan, UAE" (sic).
- **i. Platform change:** ⚠ not found.
- **FLEET KILLERS:**
  1. **A total EA ban.** The firm is incompatible with a fully automatic bot.
  2. "Prop Firm Employees" are excluded.
  3. Termination "as it seems appropriate".

## 11. HyroTrader (crypto; HYRO TECHNOLOGIES FZ-LLC, Ras Al Khaimah; funded entity in the BVI)
Sources [page]:
- T&C "Last updated: September 29, 2026", "Version 1.16": https://hyrotrader.com/terms-and-conditions/
- Rules: https://hyrotrader.com/trading-rules/

- **a. Bots and API:** §10.2(e) prohibits "any trading system, bot, expert advisor, algorithm, script, application-programming-interface client, artificial-intelligence agent or agent token that executes a strategy that is not your own — including a ready-made or purchased system … a copy-trading service, account mirroring or replication". It continues: "**Automation of your own strategy is permitted**, including through any agent token or Model Context Protocol interface the Provider makes available, provided that you remain responsible for every order".
- **b. Prohibited strategies:** "(d) repeated all-or-nothing risk patterns". §10.6A allows downgrades for "gambling-style trading". §10.2(g) covers strategies that do "not reflect genuine trading skill". Martingale is banned. Low-cap exposure is capped at 5%.
- **c. Copy and hedging**
  - §10.2(b): "coordinated multi-account trading, mirror trading, group trading, or **any strategy that relies on simulated positions taken across two or more Trading Accounts** (whether held under your Account, under any other Account of yours…)".
  - §10.2A(b): "Hedging across your own Trading Accounts is prohibited". Correlated and basket hedging are banned. (m) bans hedging against third-party exchanges.
- **d. Consistency and minimum days:** in evaluation, a profit cap of 40% per day on One-Step and Two-Step, and 50% per trade on Zero-Step. It "is not a breach". Minimum days: 1 (Zero-Step).
- **e. News:** "no news-event blackout window applies". A strategy that "depends solely on the release of news" is banned.
- **f. VPN:** §10.4: "permits the use of virtual private networks (VPNs) for privacy purposes, provided that you do not use a VPN to conceal or misrepresent the jurisdiction". §4.5A: you must disclose a shared device or wallet.
- **g. Accounts:** §4.5: "You may hold only one Account for each program type simultaneously … the Provider may aggregate Accounts … controlled by the same person". The cap figure is ⚠.
- **h. Discretion and law**
  - §6.3: rule changes are "not … applied retroactively to Accounts that are actively enrolled … unless … required by Applicable Law, or … necessary … to prevent fraud, abuse, or material harm". This is the most trader-friendly change clause of the 12.
  - §19.4: rejecting a change ends the agreement and the deposit is returned.
  - §20.2: termination "immediately, without notice, for material breach".
  - §26: laws of Ras Al Khaimah and the UAE; RAK courts. US customers: JAMS arbitration in New York.
- **i. Platform change:** §12.6(a): "the Provider determines, acting reasonably, which platform, terminal or simulation engine is made available to you, and may change that determination at any time"; (b) "no right to … continued use of, any particular" platform. For an outage that disrupts a challenge, the firm may extend, reset, or terminate and refund the deposit.
- **FLEET KILLERS:**
  1. §10.2(b): any strategy relying on positions across two or more accounts, plus "one Account for each program type". Running one bot across many accounts is squarely banned.
  2. §10.2(e): banned if the bot is "not your own" (purchased or shared).
  3. §12.6: the platform can change at any time, so API integrations can break.

## 12. Breakout (crypto; acquired by Kraken; Payward Oceanic Ltd involved)
**All breakoutprop.com hosts returned 403 (Cloudflare). Everything here is [snippet].**
- Program Rules: https://www.breakoutprop.com/program-rules/
- Evaluation Agreement: https://www.breakoutprop.com/breakout-evaluation-agreement/
- Kraken page: https://www.breakoutprop.com/kraken/

- **a. Bots and API:** ⚠ No official rule was found. Secondary reviews conflict: some say bots are allowed, some say prior approval is needed, some say there is no public API. Program Rules ban "Exploiting errors or latency in the pricing and/or platform(s)" and "Utilizing any third-party strategy, off-the-shelf strategy or one marketed to pass evaluation requirements."
- **c. Copy and hedging:** "Executing trade ideas belonging to or inspired by any third-party, including but not limited to copy trading other traders' and analysts' ideas". "hedging the same Digital Asset, or Digital Assets that exhibit a tight or substantial correlation … across multiple accounts or multiple Traders is strictly prohibited."
- **f. Device and IP:** "Account sharing of any nature, including … trading multiple accounts from the same household, devices, or IP address." Read literally, this could also catch one person running several accounts from one VPS ⚠.
- **g. Max allocation:** "combined active account sizes at $200,000" (summary).
- **h. Discretion:** "the Company has the sole discretion to determine what activities constitute Prohibited Trading" (Evaluation Agreement snippet). Governing law ⚠.
- **i. Execution:** POL may "record the idea as an internal, administrative book entry or route it externally"; traders "have no control over, or visibility into" that choice (checkout snippet).
- **FLEET KILLERS:**
  1. The ban on "trading multiple accounts from the same … devices, or IP address". A single-server bot farm fits this literally.
  2. The ban on third-party or off-the-shelf strategies.
  3. The $200k combined cap, with the bot policy unconfirmed ⚠.

---
## Patterns across firms (for the D5 synthesis)
1. **Own-account copying across funded accounts is explicitly banned** at FundedNext, FTUK, HyroTrader and The5ers ("copy trading with other … accounts"). It is allowed at Blue Guardian, FundingTraders, E8 [snippet], Funding Pips [snippet], and at ACG with declared Master/Slave.
2. **Bans on purchased or shared bots** ("third-party", "off-the-shelf", "not your own", "same EA as other traders", "source code"): The5ers, Blue Guardian, FundingTraders, HyroTrader, Breakout, FTUK, ACG, E8, FTMO (as an allocation risk), FundedNext ("distinct strategy").
3. **Firms with no realistic room for a fully automatic bot:** Maven (total ban), ACG (autonomous EAs banned), FundedNext at $50k or more, FundingTraders (needs an exception), FTUK (risk-management EAs only), The5ers (needs written approval).
4. **Caps counted per strategy, household or beneficial owner, not per account:** FTMO ($400k "per trader or strategy"), FundedNext ($300k per EA strategy), E8 (household/IP), ACG (household), HyroTrader (aggregates connected accounts).
5. **Unilateral rule changes:** most firms change rules immediately on posting or at their discretion. Exceptions: FTMO gives 7 days' notice with a right to reject (which terminates all agreements), and HyroTrader has non-retroactivity for active accounts (§6.3). FTMO and FundingTraders also allow termination without cause on 5 business days' notice.
6. **Platform change:** FTUK wipes profits on a forced migration. HyroTrader can switch platforms at will. Blue Guardian allows no migration once trades exist.
