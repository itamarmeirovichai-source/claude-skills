# D5 citation verification: forex.md, clauses-fx-crypto.md, crypto.md, fraud.md
Verifier run on 2026-10-11. Method: I re-fetched each cited URL myself with curl through the configured proxy, converted it to text and grepped for the quoted wording. Raw fetches are in `scratchpad/d5v/pages/`. I used 4 WebSearch calls in total, only where the cited host blocked me. Nothing was bought, signed up for or submitted, and no firm was contacted. Where a host returned 403 or 429 I marked the claim UNREACHABLE and did not route around it. I used no undocumented API endpoints. CourtListener's public RECAP search page (the ordinary web UI) returned 200, so I used it for the dockets instead of the blocked Justia pages.

Verdicts:
- **C** = CONFIRMED (verbatim)
- **CDW** = CONFIRMED-DIFFERENT-WORDING
- **W** = WRONG
- **U** = UNREACHABLE
- **SOC** = SNIPPET-ONLY-CORROBORATED (only third-party pages agree)
- **UNS** = UNSUPPORTED (the cited source does not say it)

## A. Bot/EA rules, caps, copy, VPS and discretion (forex.md, clauses-fx-crypto.md)
| # | File | Claim (short) | Cited URL | Verdict / note |
|---|---|---|---|---|
| 1 | forex, clauses | FTMO FAQ: "no reasons for limiting… algorithmic trading, EAs, etc." | ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/ | **C** |
| 2 | clauses | FTMO third-party EA "risk of being denied the FTMO Account if you exceed the maximum capital allocation" | same | **C** |
| 3 | clauses | FTMO "Modus Operandi being repeated on more accounts" | same | **C** |
| 4 | forex, clauses | FTMO "$400,000 per trader **or strategy**"; identical strategies across accounts above the cap → suspension | ftmo.com/en/faq/how-many-accounts-can-i-have/ | **C** |
| 5 | clauses | FTMO T&C PDF "LAST UPDATED ON 4 AUGUST 2026"; cap "calculated in aggregate per client, per strategy and per ultimate beneficial owner"; USD 400,000 in 6.3 | cdn.ftmo.com T&C PDF | **C**. The contracting entity is **FTMO Evaluation Global s.r.o.** (ID 092 13 651). forex.md says "FTMO s.r.o." and that the PDF was not read, which is out of date |
| 6 | forex, clauses | FTMO FTP bans EAs causing ">2,000 server requests per day" | ftmo.com/en/forbidden-trading-practices/ | **C** |
| 7 | clauses | FTMO FTP "alone or in concert… between connected accounts" | same | **C** |
| 8 | clauses | FTMO T&C 7.3 discretion; 7.7 "not required to notify you"; 7.8 terminate all agreements | PDF | **C** |
| 9 | clauses | FTMO 7.5.2 "regardless of which of your accounts" | PDF | **C** |
| 10 | clauses | FTMO 13.2.4 termination without cause on 5 business days' notice; 15.1 amendments on 7 days' notice; Czech law (18) | PDF | **C** |
| 11 | clauses | FTMO 9.5 must disclose "same device" shared with another user | PDF | **C** |
| 12 | clauses | FTMO VPN/VPS "generally allowed" (US exception) | ftmo.com/en/faq/can-i-travel-or-use-vpn-vps/ | **C** |
| 13 | forex | FTMO "all accounts… are demo accounts with fictitious funds" | ftmo.com/en/terms-and-conditions/ | **C** |
| 14 | forex | FTMO ToS page dateModified 2026-08-26 | same (JSON-LD) | **C** |
| 15 | forex | FTMO swing account: no news or overnight/weekend restrictions | ftmo.com/en/faq/ftmo-swing-account-type/ | **C** |
| 16 | forex | FTMO paid "more than $450 million" (FM, 29 Sep 2025) | financemagnates …ftmo-announces-over-450-million… | **C** |
| 17 | forex, clauses | The5ers T&C: prior written approval at "sole discretion"; third-party Automated Trading Software prohibited | the5ers.com/terms-and-conditions/ | **C** |
| 18 | clauses | The5ers "only one Account per User" except with prior written approval | same | **C** |
| 19 | clauses | The5ers: Israeli law; changes binding "effective immediately upon posting"; rules change "with or without notice" | same | **C** |
| 20 | forex | The5ers entities UK 12553363 and Israel 515864007; Evaluation "entirely simulated" | same | **C** |
| 21 | forex, clauses | The5ers PTP (last update 28 Jul 2026) bans "copy trading with other traders or accounts" and "Bulk trading… clearly showing a trader is not behind the strategy"; applies to "evaluation phases and funded accounts" | the5ers.com/faqs/prohibited-trading-practices/ | **C** |
| 22 | forex | The5ers FAQ: EAs OK except listed types; trader must own source code | the5ers.com/faqs/can-i-use-an-ea… | **C** (forex.md marked this as a snippet; the page is readable, updated 22 Jul 2026) |
| 23 | forex | The5ers Bootcamp max 4 accounts | the5ers.com/faqs/how-many-bootcamp-accounts-can-i-have/ | **C** |
| 24 | forex | The5ers futures "$500K total per user across all programs" | the5ers.com/futures-faqs/how-many-the5ers-futures-accounts-can-i-have/ | **W**. The page was updated 6 Oct 2026 and now reads: "a maximum of 5 purchases per account size for both $25K and $50K accounts". That is a $375k ceiling |
| 25 | forex, clauses | FundedNext: EAs only on MT4/MT5 below $50k; "$50,000 and above must trade manually"; no EAs on cTrader or Match-Trader; non-refundable add-on fee; "$300,000 for each EA… strategy"; challenge-passing EAs banned | help.fundednext.com/en/articles/8020763… | **C** (lastUpdatedDate 2026-09-08) |
| 26 | clauses | FundedNext copy ban between funded accounts "whether it belongs to the same individual"; detection by "Identical Trades"; 1st violation = no reward for the cycle, 2nd = termination | help.fundednext.com/en/articles/8019805… | **C** |
| 27 | clauses | FundedNext "maximum aggregate simulated capital of $300,000" | …/8027523… | **C**. forex.md's headline "per-person cap: $300k per EA strategy" is incomplete: the **per-person total is also $300k** |
| 28 | clauses | FundedNext device rule: a device "shared with another trader is strictly prohibited"; VPN allowed outside restricted countries | …/9351758… | **C** |
| 29 | clauses | **FundedNext CFD Terms 9.8: USD 25,000 penalty "for each such breach and/or… for each trade, strategy pattern, account, device…"** | fundednext.com/cfd-challenge-terms | **C** (Last updated 5 May 2026) |
| 30 | clauses | FundedNext CFD Terms 8.14: no "bots… AI agents… not expressly authorised" | same | **C** |
| 31 | clauses | FundedNext ToS: GrowthNext F.Z.E., Ajman; Ajman/UAE law; 6-month time bar; payouts create no "vested right" | fundednext.com/terms-of-service | **C**. forex.md is **wrong** to say the terms URL is 404 and that the entity is "not clearly identified". The ToS (5 May 2026) names GrowthNext – F.Z.E., reg. no. 28831, Ajman Free Zone; payment processing through Incenteco Trading Ltd (Cyprus HE 307114); and a Mwali (Comoros) technical entity |
| 32 | forex, clauses | FTUK "allows the use of any risk management EAs"; HFT means "within 30 seconds" | faq.ftuk.com/en/articles/14364398… | **C** |
| 33 | forex, clauses | FTUK "up to 3 forex accounts and 3 futures accounts"; different strategy and asset per account; no copying between FTUK accounts | …/12339786… | **C** |
| 34 | clauses | FTUK "Placing the same trades on multiple FTUK accounts is a violation" | …/12339773… | **C** |
| 35 | forex, clauses | FTUK VPS/VPN allowed only if trades "originate from the same IP address" | …/12339813… | **C** |
| 36 | clauses | FTUK ToS: "not rely on signals, bots or software"; bans "third-party, off-the-shelf"; Dutch law; profits lost on platform migration | ftuk.com/terms-of-service | **C**. forex.md is **wrong** that the terms page is 404 and the model is "⚠ simulated". The ToS is readable: the operator is **Nexdata-Solutions, Utrecht, Netherlands**, and it provides "simulated-funded trading accounts". The "Funded Trader Ltd #11955073" entity is not supported by the ToS |
| 37 | forex, clauses | ACG: "Automated EAs that execute trades independently… strictly prohibited… under any circumstances"; only trade-management EAs; same EA across traders counts as group trading | help.alphacapitalgroup.uk/…/6934236… | **C** (dated 7 Sep 2026) |
| 38 | clauses | ACG copy between own ACG accounts allowed after giving Master/Slave numbers | …/8786973… | **C** (6 Jul 2026) |
| 39 | clauses | ACG VPN/VPS needs a static dedicated IP and prior email notice, otherwise closure | …/8420522… | **C** |
| 40 | forex | ACG caps: $300k per strategy, $400k per household | thegodfunded (snippet) | **SOC**. A search found only thegodfunded.com. The ACG T&C still returns **403 (U)** |
| 41 | forex, clauses | Blue Guardian T&C: "one active account per challenge level, absent prior written approval"; bans "third-party strategy, off-the-shelf strategy"; bans "account multiplication… exceeding… maximum capital allocation" | blueguardian.com/terms-and-conditions | **C** |
| 42 | clauses | Blue Guardian: "VPS services linked to multiple trader accounts" banned; flagged at payout | help.blueguardian.com/…/9661512… | **C** (25 Jun 2026) |
| 43 | clauses | Blue Guardian: $400k max active funded allocation; extra accounts stay inactive | …/15846933… | **C** (6 Jul 2026) |
| 44 | clauses | Blue Guardian: "EAs are allowed… your own strategy"; copying between own accounts allowed; VPN/VPS must not be used to bypass copy rules; ±5-min news window on funded | …/14062291… | **C** |
| 45 | clauses | Blue Guardian: platform migration only if no trades yet; Dubai arbitration | …/9661525…; T&C | **C** |
| 46 | forex | Blue Guardian "All trading activity is conducted in a virtual environment"; Iconic Exchange FZCO | T&C | **C** |
| 47 | forex, clauses | FundingTraders ToS 1.2.1: no EAs "unless the… Risk Team has granted such an exception"; §8 risk-management only, "off-the-shelf bots are forbidden" | fundingtraders.com/terms-of-service | **C** (effective 1 Sep 2026) |
| 48 | clauses | FundingTraders: own-profile replication permitted; 1-minute same-direction coordination test across users; 5-business-day termination | same | **C** |
| 49 | forex | FundingTraders entities FT US Inc (Miami Beach) and Funding Traders Group Ltd (St Lucia 2025-00298); "simulated trading services" | same | **C** |
| 50 | forex | FundingTraders "Reward Protection": $500 cash plus $500 credits | fundingtraders.com | **C** |
| 51 | forex | FundingTraders swing accounts "no longer available" | help article 12838492 | **C** |
| 52 | forex, clauses | Maven: "EA: EAs are not permitted under any circumstances across all our platforms" and also "prohibited unless you have received prior approval" (conflict) | maventrading.com/terms-and-conditions | **C** (Last Amended 22/10/2025) |
| 53 | forex | Maven Edu-FZCO reg. 006-0060823-070425; "demo accounts with simulated funds"; self-claimed DIFC/DMCC/ADGM compliance | same | **C** |
| 54 | clauses | Maven: "register only once"; terminate "as it seems appropriate"; courts of "Al 'Ulan" | same | **C** |
| 55 | forex | Audacity: AudaCity Global LTD, Anjouan licence L15850/WL; gag clause on "negative reviews"; no remuneration "unless expressly agreed otherwise" | audacity.capital/en/terms-and-conditions/ | **C** |
| 56 | forex | Audacity: EAs and copy trading permitted on MT5; news and weekend allowed; combined allocation "over $2 million"; "since 2012" | audacity.capital/en/funded-trader-program/ | **C** |
| 57 | forex | FXIFY: EAs allowed on 1/2/3-phase plans and their funded stage "upon review… and pre-approval" | fxify.com/faqs/…/can-i-use-an-expert-advisor… | **C**. The host now returns 200, so forex.md's "403, snippet" can be upgraded to page |
| 58 | forex | FXIFY Instant Funded bans EAs | fxify.com/faqs/…/instant-funded-faq/… | **C**: "EA's, bots and copy traders is prohibited" |
| 59 | forex | FXIFY cap: one account per size from $5k to $400k, "about $785k"; rule effective 25/11/24 | fxify.com/faqs/all-faqs/what-the-max-allocation/ | **W (minor)**. One each of 5k, 10k, 15k, 25k, 50k, 100k, 200k and 400k adds up to **$805k**. The firm's own worked example omits the 10k account ($795k). The 25/11/24 date and the $800k cap for older customers are confirmed |
| 60 | forex, clauses | E8: "one strategy per user"; $500k per market per household/IP | help.e8markets.com | **U** (403). **SOC**: a search returns the same wording only from third parties (propfirmmap, tradetanto, thegodfunded) |
| 61 | forex, clauses | Funding Pips: own EA with proof of ownership; third-party EA only as trade/risk manager; $400k cap | help.fundingpips.com (403), fundingpips.com/terms (429) | **U** for the firm. **SOC**: pickmytrade.trade FAQ (page, "checked against FundingPips' own help center", reviewed 7 Oct 2026) states the same |
| 62 | clauses | **Funding Pips VPN/VPS ban**: "connecting to a VPN or VPS while accessing your trading account is not permitted" | help.fundingpips.com | **U** for the firm. **SOC**: pickmytrade.trade ("No VPN or VPS while you access your FundingPips trading account; disable it first") and propvator.com/funding-pips/rules ("VPN and VPS banned"), both read as pages. Exact firm wording is still unverified |
| 63 | forex | Funding Pips PRIME: T&Cs effective 15 May make PRIME "mandatory"; CEO said "is and will remain optional" (5 Jun); ~70% of a ~100-trader pool migrated; ×12.5; "reward becomes the maximum loss limit" | financemagnates …fundingpips-invited-traders-into-prime… | **C** (FM 22 Sep 2026) |
| 64 | clauses | Breakout bans "third-party strategy, off-the-shelf"; "multiple accounts from the same household, devices, or IP address" | breakoutprop.com/program-rules/ | **U** (403). Not otherwise verified |

## B. Crypto (crypto.md, clauses-fx-crypto.md)
| # | Claim | Cited URL | Verdict |
|---|---|---|---|
| 65 | HyroTrader §3.2 "All trading activity conducted under the Service is simulated", including the Funded Trader Phase | hyrotrader.com/terms-and-conditions/ | **C** (Last updated 29 Sep 2026) |
| 66 | HyroTrader §10.2(e) "Automation of your own strategy is permitted…"; FAQ "Yes, as long as the strategy is your own… agent tokens" | T&C; FAQ bot page | **C** |
| 67 | HyroTrader §10.2(b) bans "any strategy that relies on simulated positions taken across two or more Trading Accounts"; §4.5 "only one Account for each program type"; §10.2A(b) bans hedging across own accounts | T&C | **C** |
| 68 | HyroTrader entities: HYRO TECHNOLOGIES FZ-LLC (RAKEZ) is the provider; HYROTRADER TECHNOLOGIES LTD (BVI) is the Funded Trader Entity under a separate agreement (§P.4) | T&C | **C** |
| 69 | HyroTrader §6.3 non-retroactivity; §20.3 termination for convenience on 30 days' notice; RAK law; JAMS NY for US users; Sumsub KYC; USDC/USDT payouts | T&C | **C** |
| 70 | HyroTrader FAQ footer "There is no real-capital stage at any point" | hyrotrader.com/faq/hyrotrader-account/ | **C** |
| 71 | CFT: SWISS RLCRATES AG, Zug; §1.1.5 "not real"; §14.2 "does not guarantee the payment of the paid scholarship"; §3.1.10 terminate "without providing any reason"; max 5 Final-Stage Break accounts; copy ban on own accounts in Final Stage; Bybit 20 subaccounts | cryptofundtrader.com/terms-and-conditions/ | **C**. The forum clause is in §12 "Disputes" (Courts of Zug); §16.1 is "Applicable law" |
| 72 | Velotrade: HK entity; §5.1 "No live trading or real capital"; §4.3 one Account, $200k combined; 8.2(h) replication ban; §8.3 EAs permitted; first two payouts capped at 20× the fee, excess forfeited; ToS 1 Jul 2026 | velotrade.com/terms | **C** |
| 73 | Bitfunded: "Every trade has to be placed manually"; one funded account per size; "simulated environment" | bitfunded.com/faq | **C** |
| 74 | Kraken Prop: up to $200k; evaluation is simulated; "Kraken covers any trading losses beyond that" | kraken.com/prop | **CDW** |
| 75 | Kraken Prop launched 27 May 2026; $200k aggregate per trader; Breakout Terminal only; unregulated; operated by Payward Oceanic Ltd | finance.yahoo.com/…kraken-prop-inside-funded-trader… | **C** |
| 76 | Kraken Funded launched 30 Jul 2026, $1k–$10k tiers, USD payouts; Payward Oceanic; "not a regulated investment product" | fxnewsgroup Kraken Funded | **C** |
| 77 | Trustpilot figures and suspensions (CFT, Velotrade, HyroTrader, Breakout) | trustpilot.com | **U** (403 to curl this run; the earlier "page" reads cannot be re-checked) |
| 78 | Breakout founders and the "$100k per account / $200k" figures from The Block | theblock.co | **U** (403) |

## C. Fraud, regulatory and court claims (fraud.md; MFF line in forex.md)
| # | Claim | Cited URL | Verdict / note |
|---|---|---|---|
| 79 | CFTC v. Traders Global (MFF), D.N.J. 3:23-cv-11808 | kslaw.com | **C** for the docket number. **W (minor)** on the date: the complaint was filed **28 Aug 2023** and the SRO was entered 29 Aug 2023 (Willkie). fraud.md says "29 Aug 2023 (complaint)" |
| 80 | CFTC release 8771-23 / cftc.gov | cftc.gov | **U** (403) |
| 81 | B-book allegation "counterparty to substantially all customer trades"; pretextual terminations; manipulative software; OSC "fraud, unregistered trading…" | FM 4 Sep 2023 | **C** |
| 82 | Special Master Linares: CFTC acted "willfully and in bad faith on several occasions"; CAD 31.5M "unidentified Kazmi account" was tax payments; emails of 16 Jun and 17 Aug 2023 | Willkie article plus Special Master report PDF | **C** (both read as pages; the PDF is readable, so fraud.md's "snippet" can be upgraded) |
| 83 | **Dismissal with prejudice by Judge Kiel, 13–14 May 2025, plus sanctions** | kslaw; FM | **C**. FM: "order signed on May 13, 2025"; K&S: "On May 14, 2025… dismissed… with prejudice, imposed sanctions… ordered the CFTC to pay… legal fees" |
| 84 | Staff placed on administrative leave (4 lawyers + 1 investigator) | FM; kslaw | **CDW** (FM: "five staff members"; K&S: "pending an OIG investigation") |
| 85 | **~$3.1M fee award; date unclear** | law360.co.uk/amp/articles/2364442 | **C** (headline and lede readable): "ordered the… CFTC on Friday to pay back over $3.1 million in attorney fees", in an article dated **14 Jul 2025**. The order is therefore dated **Fri 11 Jul 2025**, which resolves the ⚠ |
| 86 | Ontario court released "nearly all" assets; $10M escrow plus $500k; OSC investigation "ongoing" with no notice of allegations | wealthprofessional.ca | **C** (dated 10 Dec 2025) |
| 87 | Ontario court ordered OSC to pay C$80,000, "the highest such amount imposed" | news.bgov.com | **C** (page partly readable; datePublished **26 Feb 2026**) |
| 88 | MFF "We will tell our story soon" (6 Oct 2025) | FM comeback article | **C** |
| 89 | CONSOB 8 Jul 2024: "congegnata…", "beneficio economico", "effetto gaming" | consob.it | **C** |
| 90 | FSMA Mar 2024 "shadow investment game" | FM FSMA article | **C** (dated 7 Mar 2024). The "difficult for a consumer to determine" sentence was not found verbatim; FM paraphrases it as "leaving consumers in the dark regarding their entitlement to any potential commissions", so that sentence is **CDW** |
| 91 | ESMA: CySEC chair, 2 Jul 2026, "ESMA is not currently engaged in any substantive discussions…" | theindustryspread.com | **C** |
| 92 | CFTC "no official statement on prop-firm legality" since MFF | same | **C** |
| 93 | Topstep is an NFA member and CTA; Tradeify launched Slay Markets IB | same | **C** (citing FM, 21 May 2026) |
| 94 | **FTMO–OANDA acquisition closed 1 Dec 2025** | ftmo.oanda.com press release | **C** (the last regulatory approval came in November; closed 1 Dec). The $422M price and $250M loan are **U** (brokerchooser 403) and remain snippet-only |
| 95 | **Kraken–Breakout: announced 4 Sep 2025, effective 1 Sep 2025** | payward.com press release | **C** ("Effective September 1"; "up to $200,000 in notional capital"). BusinessWire, Blockworks and The Block returned 403 |
| 96 | **McCrudden v. Topstepfunded, M.D. Fla. 3:26-cv-00816, filed 9 Apr 2026** | dockets.justia.com | Justia **U** (403). **C** via the CourtListener RECAP public search: 3:26-cv-00816, filed 9 Apr 2026, Judge Wendy W. Berger, parties include Vincent McCrudden and Topsteptrader LLC / Topstep LLC. "Pro se" and "moved toward arbitration" are **not verified** |
| 97 | **McCrudden v. Apex Trader Funding, M.D. Fla. 3:26-cv-01073, filed 30 Apr 2026** | dockets.justia.com | Justia **U**. **C** via the CourtListener RECAP search (filed 30 Apr 2026, Judge Berger). "8 individual defendants" and "pro se" are **not verified**. The docket shows an "Appear Pro Hac Vice" entry (doc #3, 1 May 2026), so someone has outside counsel. Treat "pro se" as ⚠ |
| 98 | Riot v. Apex (W.D. Tex. 1:24-cv-01557), agreed judgment 20 Aug 2026 | pacermonitor.com/public/case/56230904/ | **U** (404 on refetch) |
| 99 | **FundingTicks: Dec 2025 rules (1-min hold, higher daily profit, lower split); "previously valid trades and profits were reduced or invalidated"; Jan 2026 wind-down; refunds of evals and masters; formulas for live accounts** | coinspectator syndication of FM (Tareq Sikder), 19 Jan 2026 | **C** (FundingTicks' tweet is dated 18 Jan 2026; support was open to 31 Jan). **UNS**: "the retroactive application was later reversed" is not in this article. The FM "lessons from FundingTicks" piece is **sponsored** content |
| 100 | **Alpha Futures, Jul 2026**: NinjaTrader cut it off over a disputed $225.7k; all active Premium accounts closed with activation-fee refunds only; PFM delisting quote | tradingviewapi.com (FM 14 Jul 2026) | **C**. Note: Alpha Futures did not close as a company. Only the Premium plan was liquidated |
| 101 | **Seacrest/MyFundedFX**: accounts closed 6 Feb 2026; claim deadline 28 Feb 2026 | FM Seacrest article | **C** (page now readable; upgrade from snippet). propfirmmap: "Traders with pending payouts lost out" (**CDW** for "difficulty getting final payouts") |
| 102 | Funding Pips halted 14 Feb 2024; CEO quote "abruptly halt services due to active US accounts…"; BlackBull "forced to immediately shut down Funding Pips" | FM 18 Feb 2024 | **C** |
| 103 | FTMO US: positions closed by Friday; moved to DXtrade; "MetaQuotes did not publicly confirm"; only 3 of 122 firms had cTrader/DXtrade | same | **C** |
| 104 | True Forex Funds halted Feb 2024 (MT licences); "flagged by the CFTC last year" | FM 6 Feb 2024 | **C** |
| 105 | SurgeTrader closed 24 May 2024; Match-Trade notice 5 Apr, effective 30 Jun; "inability to fulfill the formal obligations" | FM 26 May 2024 | **C** |
| 106 | TFT 13 Mar 2024 internal audit pausing payouts; "Coordinated propaganda"; $150M self-claimed, not audited | FM 14 Mar 2024 | **C** |
| 107 | Funding Pips Trustpilot suspended Jun 2024, "increase in reviews related to recent media attention" | FM 13 Jun 2024 | **C** (in effect from 7 Jun 2024) |
| 108 | Smart Prop Trader: stopped onboarding 27 Nov, wound down 29 Dec 2024, "citing Eightcap's withdrawal"; FM "at least 50" closed in 2024 | FM 28 Nov 2024 | Dates and "at least 50" **C**. **UNS**: the article attributes the Eightcap withdrawal to **Funds For Traders**, not to Smart Prop Trader, which gave no reason beyond a "new product" |
| 109 | FTMO Australia move, FTMO "only prop firm offering MT5 to US", UniCredit $625M, CFTC 9284-26, propfirmmatch/Trustpilot/FPA user reports | various | Not re-checked (not load-bearing; most remain snippet-only). cftc.gov is 403 (**U**) |

## Counts (109 rows; rows 109 and 64 are partly unchecked)
| Verdict | Count |
|---|---|
| CONFIRMED (C) | 85 |
| CONFIRMED-DIFFERENT-WORDING (CDW) | 3 (rows 74, 84, 90 partial; 101 partial) |
| WRONG (W) | 5 (rows 24, 31 [404/entity], 36 [404/entity], 59, 79 [date]) |
| SNIPPET-ONLY-CORROBORATED (SOC) | 4 (rows 40, 60, 61, 62) |
| UNSUPPORTED (UNS) | 2 (rows 99 partial, 108 partial) |
| UNREACHABLE (U) | 8 (rows 64, 77, 78, 80, 94 price, 98, plus Justia for 96/97 [resolved via CourtListener]) |

Rows 31 and 36 are counted as WRONG only for their "terms 404 / entity unclear" statements; the clause quotes in clauses-fx-crypto.md are confirmed. Some rows carry two verdicts, so the counts overlap and do not sum to 109.

## Must-fix corrections for the final report
1. **FundedNext entity and ToS (forex.md §3).** The ToS is readable. It names GrowthNext – F.Z.E., Ajman Free Zone, reg. 28831; payments go through Incenteco Trading Ltd (Cyprus); governing law is Ajman/UAE; ToS and CFD Terms are dated 5 May 2026. Remove "terms 404", "Simulated ⚠" and "not clearly identified".
2. **FundedNext cap.** The per-person cap is **$300k aggregate across all FundedNext accounts**, not just "$300k per EA strategy". Bring the **USD 25,000-per-breach/per-account penalty (CFD Terms 9.8)** and the own-account copy ban into forex.md as well; at present they appear only in clauses-fx-crypto.md.
3. **FTUK entity and ToS (forex.md §4).** The ToS is readable. The operator is Nexdata-Solutions, Utrecht, NL; Dutch law; "simulated-funded trading accounts"; profits are lost on a forced platform migration. Drop "Funded Trader Ltd #11955073" and "terms 404".
4. **The5ers futures cap.** Replace "$500K total per user" with "max 5 accounts each of $25K and $50K (≈$375k), page updated 6 Oct 2026".
5. **FXIFY.** The host is readable now (upgrade from snippet to page). The cap is one account per size from $5k to $400k, which totals **$805k**, not ~$785k. Instant Funded bans EAs, bots and copy traders (confirmed).
6. **FTMO contracting entity.** The Challenge T&C (4 Aug 2026) is with **FTMO Evaluation Global s.r.o.**, not only FTMO s.r.o., and the PDF *was* readable. Cite it for the per-UBO cap, 7.5.2 cross-account comparison, 7.8 terminate-all, and 13.2.4 termination without cause on 5 business days.
7. **MFF dates.** The complaint was filed **28 Aug 2023**; the SRO was entered 29 Aug. The fee award of **>$3.1M was ordered Fri 11 Jul 2025** (Law360, 14 Jul 2025), so remove the ⚠ "date unclear". The OSC C$80k costs article is dated 26 Feb 2026.
8. **Smart Prop Trader.** Remove "citing Eightcap's withdrawal". In the FM source, that reason belongs to Funds For Traders.
9. **FundingTicks.** Remove or ⚠ "the retroactive application was later reversed": it is not in the cited FM/coinspectator text. Flag the FM "lessons from FundingTicks" piece as sponsored.
10. **McCrudden suits.** Docket numbers and filing dates are now **verified via CourtListener RECAP** (both before Judge Berger, M.D. Fla.). "Pro se", "8 individual defendants" and "moved toward arbitration" are not verified, and the Apex docket has a pro hac vice appearance, so mark "pro se" ⚠.
11. **Alpha Futures wording.** Say "liquidated its Premium plan" rather than implying the firm closed.
12. **Funding Pips VPN/VPS ban.** This is still not read on the firm's own site (403/429). It is corroborated by two independent third-party rule pages (PickMyTrade, reviewed 7 Oct 2026; Propvator). Keep the ⚠ and describe it as "secondary, consistent".
13. **E8 (all clauses) and ACG caps** remain snippet or third-party only. Keep the ⚠.
14. **Upgrades from snippet to page** where the report says "snippet": Seacrest (FM), Special Master PDF, FXIFY FAQs, The5ers EA FAQ.

## Grades I think are wrong given what I verified
- **FundedNext: C → D for this client.** For a one-bot, many-account fleet the verified terms are prohibitive: no EAs at $50k and above; own-account copying between funded accounts banned, with termination on the second offence; $300k total per person; and a USD 25k contractual penalty "for each… account, device" that can be set off against rewards. The "opaque entity" part of the C rationale is wrong (the entity is clearly named), but that does not rescue the grade.
- **The5ers: B → C for the bot use case.** Bots need prior written approval at the firm's sole discretion; only one Account per User; "copy trading with other traders **or accounts**" and "bulk trading… not behind the strategy" are banned on funded accounts. Counterparty quality alone may justify B, but not as a bot-fleet venue.
- **E8: B → B⚠/C.** Every bot and cap rule is still unread on the firm's site (403), and the cap is per household/IP.
- **FTMO: keep A for firm quality, but caveat for the fleet.** The verified T&C counts the $400k cap per client, **per strategy and per UBO**; compares position counts across all your accounts (7.5.2); lets FTMO terminate *all* agreements over one account's FTP (7.8); and allows termination without cause on 5 business days' notice (13.2.4). The FTMO Account (funded-stage) agreement was still not read.
- Others (Alpha D, Maven D, FundingTraders D, FTUK D, Blue Guardian C, Funding Pips C, HyroTrader C, CFT D, Velotrade D, Bitfunded D, Breakout B-/C) are consistent with the verified text.

Sources added during verification: courtlistener.com RECAP search (public search page, read 2026-10-11); law360.co.uk/amp/articles/2364442 (page header); coinspectator.com/mainstream/2026/01/19/following-profit-cuts-and-trading-limits-prop-firm-fundingticks-begins-winding-down/ (page); pickmytrade.trade/prop-firm-faq/fundingpips-faq/ (page); propvator.com/funding-pips/rules/ (page); payward.com/press-release/kraken-acquires-breakout-for-global-prop-trading (page); ftmo.oanda.com press release (page).
