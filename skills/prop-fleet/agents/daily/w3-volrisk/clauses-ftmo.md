# F2 clause read: FTMO, 2-Step, Swing, $100K (FTMO Challenge + Verification + FTMO Account)

Access date for all sources: **2026-10-12**. This was read-only research. Nothing was bought, no login or form was used, and nobody was contacted.
Tags: **[page]** means I read the text directly from the firm's own page or PDF (curl through the proxy). **[snippet]** means the text came only from a search snippet. Every quote below is [page] unless it says otherwise.

## Sources (all FTMO-owned)
| # | Document | URL | Last updated / modified |
|---|---|---|---|
| S1 | FTMO Challenge Terms and Conditions (FTMO Evaluation Global s.r.o.) PDF, 22 pp. | https://cdn.ftmo.com/docs%2Fterms-and-conditions%2Ff8d5ca5086964c86a6ee2a77f20bdbd7 (linked from https://ftmo.com/en/terms-and-conditions/) | "LAST UPDATED ON 4 AUGUST 2026" |
| S2 | Forbidden Trading Practices | https://ftmo.com/en/forbidden-trading-practices/ | dateModified 2026-02-02 |
| S3 | Blog "Gambling is not the right way to make money" (the FTP page links to it: "these practices are described in detail here") | https://ftmo.com/en/blog/gambling-is-not-the-right-way-to-make-money/ | dateModified 2025-11-04 |
| S4 | Trading Objectives | https://ftmo.com/en/trading-objectives/ | dateModified 2026-10-09 |
| S5 | Comparison Table | https://ftmo.com/en/comparison-table/ | dateModified 2026-10-09 |
| S6 | FAQ: account specifications (leverage) | https://ftmo.com/en/faq/what-are-the-account-specifications/ | 2026-10-05 |
| S7 | Symbols data API that feeds https://ftmo.com/en/symbols/ (fields `leverageSwing`, `maxTradeVolume`, `tradingHours`) | https://ftmo.com/wp-json/ftmo/symbols | symbols page dateModified 2026-10-08 |
| S8 | FAQ: Swing account type | https://ftmo.com/en/faq/what-is-the-swing-account-type-and-how-does-it-work/ | 2026-10-06 |
| S9 | FAQ: overnight / weekend | https://ftmo.com/en/faq/can-i-hold-positions-overnight-or-over-the-weekend/ | 2026-10-11 |
| S10 | FAQ: consistency rules | https://ftmo.com/en/faq/do-you-have-any-consistency-rules/ | 2026-10-11 |
| S11 | FAQ: entry fee refunded? | https://ftmo.com/en/faq/is-the-entry-fee-refunded/ | 2026-10-06 |
| S12 | FAQ: fees recurrent? | https://ftmo.com/en/faq/what-fees-do-you-charge-and-are-they-recurrent/ | 2026-10-04 |
| S13 | FAQ: withdraw reward | https://ftmo.com/en/faq/how-do-i-withdraw-my-profits/ | 2026-10-09 |
| S14 | FAQ: how many accounts | https://ftmo.com/en/faq/how-many-accounts-can-i-have/ | 2026-09-30 |
| S15 | FAQ: instruments and strategies | https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/ | 2026-09-30 |
| S16 | FAQ: legal relationship / FTMO Account Agreement | https://ftmo.com/en/faq/what-is-the-legal-relationship-between-an-ftmo-trader-and-ftmo-after-signing-the-ftmo-account-terms-conditions/ | 2026-10-11 |
| S17 | FAQ: trading according to a real market | https://ftmo.com/en/faq/what-is-trading-according-to-a-real-market/ | 2026-10-09 |
| S18 | FAQ: Discipline Score; balance vs equity; passed, what now; technical infrastructure; merge accounts; modify account type | https://ftmo.com/en/faq/{what-is-the-discipline-score, what-is-the-difference-between-balance-and-equity, i-have-successfully-passed-what-to-do-now, how-does-the-ftmo-technical-infrastructure-work, can-i-merge-my-accounts, can-i-modify-my-platform-or-account-type}/ | 2026-10-04 to 2026-10-11 |
| S19 | Scaling Plan | https://ftmo.com/en/reward-growth-and-scaling-plan/ | 2026-09-15 |
| S20 | Landing page "broker vs prop trading" (fee refund footnote) | https://ftmo.com/lp/broker-vs-prop-trading/ | n/a |
| S21 | How it works | https://ftmo.com/en/how-it-works/ | n/a |

**Blocked hosts: none.** Every ftmo.com and cdn.ftmo.com fetch returned HTTP 200. The only exception was the guessed URLs below, which returned 404.

**FTMO Account Terms and Conditions (FTMO Trading Global s.r.o.): NOT publicly available.** The FAQ states that the agreement is unlocked only in the Client Area after KYC: "Once you pass your KYC or KYB check, the FTMO Account Agreement will be unlocked for your review and signing in your Client Area – FTMO Traders – Contracts." It adds: "If you are interested in a sample of the contract, please contact us at [email protected] ." (S16) I did not contact FTMO, because the brief forbids it. I tried these places and found nothing:
- the guessed URLs https://ftmo.com/en/ftmo-account-terms-and-conditions/ and /en/ftmo-account-agreement/ (both 404)
- the archive.org availability API (no snapshot)
- the terms-and-policies listing at https://ftmo.com/en/terms-and-policies/, which lists only the Challenge T&C, FTP, Trading Objectives, Privacy, Cookie and Imprint pages
- 3 web searches, which returned only third-party sites

Everything below about the FTMO Account therefore comes from three places: the FTMO-wide pages (S2, S4, S8, S9, S13), Challenge T&C clauses that reach into the FTMO Account (7.6.4, 7.8, 13.2.2(f)), and the FTP page. The FTP page states it applies to "the Evaluation Process and the FTMO Account Program".

Note on the entity name: earlier notes said "FTMO Trading s.r.o.". S1 gives "FTMO Trading Global s.r.o. … Identification No.: 094 18 415".

---

## 1. Gambling, all-or-nothing, one-sided bets, overleveraging, overexposure, speculative trading

- S1 cl. 7.4 [page]: "A fundamental aspect of our mission is to educate traders and enhance their skills to cultivate responsible trading habits. We strive to maintain a secure environment for traders to engage in Simulated Trading and we retain the discretion to implement any measures we consider appropriate to prevent activities we deem analogous to gambling, unsafe for the continuation of the business or to prevent any other conduct that we, at our sole discretion, regard as misaligned with our mission and values."
- S1 cl. 7.1 [page]: "These rules ensure that your simulated trades are replicable with the same or highly similar execution conditions in typical market behaviour and are not designed to circumvent, or 'game', our offering."
- S1 cl. 7.3 [page]: "We reserve the right to determine, at our own discretion, whether certain simulated trades, practices, strategies, or situations qualify as or fall within a Forbidden Trading Practice. We may update the list of Forbidden Trading Practices from time to time."
- S2 FTP [page]: "otherwise perform simulated trades that contradict how trading is actually performed in the financial markets, or in a way that we reasonably consider might cause us financial, reputational, or other harm as a result of your activities (e.g., overleveraging, overexposure, one-sided bets, account rolling). For the avoidance of doubt, these practices are described in detail here ;" ("here" links to S3.)
- S2 FTP, gap trading [page]: "perform gap trading (a high-risk practice that carries potentially unfavourable outcomes if performed in real market conditions due to increased volatility) by opening simulated trades: when major global news, macroeconomic events, or corporate reports or earnings are scheduled and they might affect the relevant financial market (i.e., a market that allows trading of financial instruments potentially impacted by the events); or two hours or less before a relevant financial market is closed for at least two hours;"
- S3 blog, which S2 incorporates by reference [page]:
  - "A classic example of gambling seen with many traders is overleveraging."
  - "Some traders tend to trade multiple instruments to diversify their risk. However, even here it may happen that a trader opens several positions representing several instruments or currency pairs, but at the same time, the trader is exposed to more risk on one instrument or currency. A typical case may be the opening of several positions on different major pairs. What looks like a diversified position could simply be one big dollar bet."
  - "Dangerous are also situations when a trader opens a position or a combination of positions that are so large that they use the maximum potential of the available margin."
  - "In a nutshell, large positions or the sum of the sizes of a combination of several positions at the same time is a very risky approach and certainly not recommended at FTMO. … Remember that professionals usually risk only 1% and still make very interesting profits in a safe and stable environment and long term."
  - "A one-sided bet usually looks so tricky that the trader simply risks a large amount of free margin on a single market event, usually driven by macroeconomic factors."
  - "We actively monitor gambling practices and do not turn a blind eye to them."
- S8 Swing FAQ [page]: "Please be mindful of the Forbidden Trading Practices as defined in the FTMO Challenge Terms & Conditions (clause 7.3) and avoid gambling-like behaviour, some examples of which are described in this article ."
- S15 [page]: "As long as your trading is legitimate (in line with proper risk management), conforms to the real market conditions, and does not resemble forbidden practices, we have no reasons for limiting or restricting your trading strategy, whether it's discretionary trading, algorithmic trading, EAs, etc. When trading, keep in mind that your trading style should be replicable on live accounts to generate the same results as on your FTMO Account."
- No page I read uses the words "all-or-nothing" or "speculative". The closest wording is "one-sided bets" and "bet all their chances on one card" (S3).

## 2. Maximum risk per trade, position size, max lots, margin-use limits, "substantially larger position sizes"

- S1 cl. 7.5 [page]: "When using the Services you must abide by market standard risk management rules for trading on financial markets. These are defined by us at our discretion, acting reasonably, to ensure that activity is not designed to circumvent our rules and amounts to genuine Simulated Trading strategies. Genuine strategies are strategies using risk management rules a reasonable person would apply when trading on financial markets with their own money. Market standard risk management rules include, as an example, avoiding:
  7.5.1 opening substantially larger position sizes compared to your other simulated trades, on any of your accounts;
  7.5.2 opening substantially smaller or larger number of positions compared to your other simulated trades, regardless of which of your accounts are concerned, and
  7.5.3 undertaking repeated simulated trading activity that results in higher Risk per Trade Idea, thereby exposing your simulated account to cumulative exposure in a specific symbol or correlated symbols."
- S1 cl. 21.1, definition [page]: "\"Risk per Trade Idea\" means the total exposure in a specific symbol (or correlated symbols) on your account during a given moment or within a specific time period, measured as a percentage of your initial Simulated Capital, whereas the associated risk is determined by the maximum drawdown of realised or unrealised loss of the positions linked to the same trade idea."
- S1 cl. 7.6.6 and 7.6.7 (remedies) [page]: "enforce the limitation on Risk per Trade Idea to the maximum limit we determine, acting reasonably, as a percentage of the Initial Simulated Capital, which must not be exceeded in terms of realised or unrealised loss (drawdown) on any single simulated trade or combination of simulated trades out of one trade idea;" and "enforce a limitation on the volume of any specific symbol or asset class when simulated trading;"
- S2 FTP restates 7.5.1–7.5.3, with one change: 7.5.2 there reads "on any of your accounts" [page].
- S15 server limits [page]: "Please note that platform servers have 200 orders at a time and 2000 max positions per day limitation, just as the limited acceptance of the server messages (orders and order modifications such as updates of TP/ SL and updates of limit orders). If your EA causes hyperactivity to a platform server, we might alert you and ask you to adjust the EA logic or parameters of your strategy."
- S2 FTP [page]: "perform simulated trades that are operated or managed by automated robots / EAs (Expert Advisors) which cause the trading account to become hyperactive in the sense of an excessive number of more than 2,000 server requests per day on individual simulated trades or pending orders being opened, modified, or closed, causing overload of the trading server;"
- Per-order lot caps come from the S7 API field `maxTradeVolume`; `maxTotalVolume` is 0 (no total cap) for every symbol. The caps are: FX and metals 100 lots per order; index and energy cash CFDs 1000 (JP225 200, NATGAS 50); crypto 1–5; equities 10000. These caps are not binding for a $100K account.
- **No fixed numeric max-risk-per-trade rule and no stop-loss requirement** were found. S15: "We do not require you to use a Stop-loss". The only number is the soft benchmark in S3, "professionals usually risk only 1%". Clause 7.6.6 lets FTMO *impose* a numeric Risk per Trade Idea cap after the fact.

## 3. Consistency rules: do they apply to the 2-Step Swing?

- S4 [page], Best Day Rule: "To pass the FTMO Challenge: 1-Step or to be eligible for a Reward on an FTMO Account , the Best Day Rule requires that your Best Day does not represent more than 50% of your Positive Days' Profit ." and "This rule applies to the FTMO Challenge: 1-Step as well as the FTMO Account (1-Step) ." It is listed only in the 1-Step section. The 2-Step section lists only Profit Target, Maximum Daily Loss, Maximum Loss and Minimum Trading Days.
- S5 Comparison Table [page]: the "Consistency" row shows "–" for 2-Step and "50%" for 1-Step.
- S10 [page]: "Your trading consistency is primarily evaluated based on the Trading Objectives. … Provided you maintain sustainable risk management practices, there are no additional consistency requirements for your trading."
- S18 Discipline Score [page]: "Please note that the Discipline Score does not affect the Evaluation phase or your trading on an FTMO Account in any way."
- S1 cl. 7.6.9 (discretionary) [page]: "introduce any other additional measures we deem necessary, advisable or adequate in order to ensure your Simulated Trading activity reflects long term sustainability and is not aimed at the mere exploitation of our model including temporary or permanent consistency measures."
- Position-size consistency across accounts and over time is covered by 7.5.1 and 7.5.2 above ("on any of your accounts", "regardless of which of your accounts are concerned").
- **Verdict:** no hard consistency or best-day rule applies to the 2-Step Swing. A soft position-size and position-count consistency standard (7.5) applies across all accounts. FTMO can also impose consistency measures at its discretion (7.6.9).

## 4. Account review, refusing or reducing rewards, leverage cuts, trade cancellation

- S1 cl. 7.6 [page]: "If, acting reasonably, we determine that you have engaged in Simulated Trading which involves Forbidden Trading Practices or breach of the Risk Management Rules, we may, at our sole discretion: 7.6.1 consider it a failure to meet the Trading Objectives; 7.6.2 cancel, consolidate or reclassify one or more of your simulated trades or remove any transactions that violate the Rules of Simulated Trading from your trading history and/or not count their results in the profits and/or losses achieved in the Simulated Trading; 7.6.3 immediately cancel all Services provided to you, … 7.6.4 inform FTMO Trading who may take applicable steps under the FTMO Account Terms and Conditions in respect of any FTMO Accounts you may have, including cancellation of all of your FTMO Accounts or rewards thereunder and termination of the respective agreements; 7.6.5 reduce the offered leverage on any or all your accounts/ simulated trades; 7.6.6 … 7.6.7 … 7.6.8 impose restrictions on the use of the Trading Platform, and 7.6.9 …"
- S1 cl. 7.7 [page]: "We will endeavour to notify you of any action we take. However, we are not required to notify you before taking such action."
- S1 cl. 7.8 [page]: "If some or all Forbidden Trading Practices are executed on one or more of your FTMO Challenge Accounts, or accounts of various related customers, or by combining trading through FTMO Challenge Accounts and FTMO Accounts, then we are entitled to cancel all Services and terminate all Agreements relating to all FTMO Challenge Accounts you have, with immediate effect, apply other measures in Clause 7.6 in respect of all such involved accounts with us."
- S1 cl. 7.9 [page]: "We are not obliged to provide you with any compensation if we take any action against you in accordance with this Clause 7 (Rules of Simulated Trading). You are also not entitled to any refund of the FTMO Challenge Fee."
- S1 cl. 5.8.7 [page]: "This does not guarantee your acceptance into the FTMO Trader Program."
- S1 cl. 6.1 [page]: "Successfully completing the Evaluation Process does not guarantee your acceptance into the FTMO Trader Program."
- S2 FTP closing paragraph [page]: "Any breach or non-compliance with these rules may result in corrective actions, including, but not limited to, removal of simulated trades from your history, restricted access to a trading platform, disqualification from the Evaluation Process, forfeiture of any potential Rewards, or even termination of all agreements you have with us."
- S2 FTP [page]: "Further, when performing simulated trades with us, you must not engage in practices which are not reasonably replicable in the actual market, meaning that such a strategy is not in line with risk management rules a reasonable person would apply when trading on financial markets with their own money."
- S15 [page]: "If we identify intentional activities or Modus Operandi being repeated on more accounts, we reserve our right to take the necessary action to mitigate risk. This might vary from removing the conflicting positions, rebalancing the account, reducing leverage, or terminating the account completely and ceasing our cooperation altogether."
- Reward review: S13 [page] says "After you submit the withdrawal request, we will review your account and notify you within 1–2 business days." S18 (passed, what now) [page] says the Verification "account is set for review, which typically takes 1-4 business days."
- S1 cl. 13.2.4 [page]: "Either party may terminate the Agreement without cause by serving a written notice at least five (5) business days in advance on the other party."
- S1 cl. 13.2.3(b) [page], Challenge only, relevant at high vol: termination for prolonged inactivity includes when "you maintain a loss in the FTMO Challenge Account in the amount between 8% and 10% (included) of the Initial Simulated Capital for a period longer than thirty (30) calendar days, whereas (i) performing simulated trades designed to circumvent this rule will be deemed to fulfil this condition and (ii) circumventing means performing simulated trades not consistent with your previous Simulated Trading pattern."
- No page I read uses the words "unrealistic" or "non-replicable" verbatim. The equivalents are "replicable with the same or highly similar execution conditions" (7.1), "not reasonably replicable in the actual market" (FTP) and "replicable on live accounts" (S15).

## 5. Repeated evaluation purchases, re-buys, account rolling, free retakes

- S1 cl. 3.13 [page]: "Subject to Clause 3.14, you can place multiple Orders and each Order, once complete, constitutes a separate Agreement."
- S1 cl. 3.14 [page]: "We reserve the right to limit the total number of Orders you can make: 3.14.1 The total number of Orders may be limited in aggregate in case other clients connected to you are using the Services, … 3.14.2 If, at our discretion and acting reasonably, we determine that you place an unusually large number of Orders, we may notify you through the User Area as a protective precaution to mitigate potentially harmful behaviour. If the behaviour continues after such notice, we reserve the right to suspend any further Orders by you or invoke a cool-down period. If we identify that such unusual behaviour relates to your involvement in Forbidden Trading Practices, we may take any of the respective actions set out in Clauses 7 (Rules of Simulated Trading), 11 (Breach of these Terms) and 13 (Duration and termination of the Agreement). We reserve the right to determine, at our own discretion, the nature of the behaviour described above and reasonable boundaries for such determination."
- S2 FTP lists "account rolling" as an example (quoted in §1).
- S3 [page]: "An interesting case and form of gambling specific to prop trading firms is account rolling. In this case, traders will buy multiple evaluation courses at the maximum amount available. … This leads them to believe that they can open unnecessarily risky trades on the account they have received first, because if they recklessly breach that account, they can start trading in the next one almost immediately." and "If someone is ordering accounts more than is healthy, according to mathematical probabilities, he has a pretty good chance of succeeding on several accounts, while breaking many of them. … To some extent, we can also talk about abuse of the system".
- S14 [page]: "There is no limit to the number of accounts you may have. However, a maximum capital allocation limit applies. At any given time, the total capital allocation across all accounts is limited to $400,000 per trader or strategy (prior to any scaling). … If identically traded strategies are detected across multiple FTMO accounts and the total fictitious capital exceeds the maximum capital allocation limit, FTMO reserves the right to suspend the affected accounts."
- S1 cl. 5.8.5(c) [page]: you must "procure that the aggregate amount of the Initial Simulated Capital on all accounts held by you or parties affiliated with you, individually or in combination, on all accounts with us and/or members of the FTMO Group does not exceed USD 400,000."
- S1 cl. 6.3 [page]: "The total sum of the Initial Simulated Capital is calculated in aggregate per client, per strategy and per ultimate beneficial owner or executive of another client or legal entity."
- **Free retakes: no clause found.** None of S1, S4, S5, S11–S14 or S21 offers a free repeat. The trading-objectives page offers only "As many Free Trials as you need", and a Free Trial is a non-evaluating demo. Failed re-buys are simply new paid Orders.

## 6. Swing leverage caps per asset class (actual numbers)

- S6 [page]: "The leverage we offer for the Standard account type is up to 1:100 and cannot be increased. The Swing account type has leverage set to up to 1:30 . At all stages, you trade with fictitious capital; the leverage is applied to this fictitious capital only."
- S7 per-symbol `leverageSwing` (FTMO's own JSON, global site) [page]:

| Asset class (S7 `assetClass`) | Swing leverage | Standard | Symbols |
|---|---|---|---|
| Forex majors and crosses | **1:30** | 1:100 | 28 pairs (EUR/USD, GBP/USD, USD/JPY, AUD/USD, crosses) |
| NZD pairs and exotics (EUR/CZK, USD/MXN, USD/ZAR, USD/CNH, etc.) | **1:20** | 1:66.67 | 14 (plus 1 exotic at 1:30) |
| Metals (XAU, XAG, XPT, XPD, XCU) | **1:15** | 1:50 | 9 |
| Major indices (US500, US100, US30, GER40, UK100, EU50, FRA40, JP225, AUS200) | **1:15** | 1:50 | 9 |
| Minor indices (US2000, HK50, N25, SPN35) | **1:9** | 1:30 | 4 |
| Energies: USOIL, UKOIL | **1:15** | 1:50 | 2 |
| Energies: NATGAS, HEATOIL | **1:9** | 1:30 | 2 |
| DXY | **1:5** | 1:16.67 | 1 |
| Agricultural / softs (COCOA, COFFEE, CORN, SOYBEAN, WHEAT, COTTON, SUGAR) | **1:1** | 1:3.33 | 7 |
| Crypto CFDs | **1:1** | 1:3.33 | 30 |
| Equity CFDs | **1:1** | 1:3.33 | 59 |

Note: the page's JS contains a different hard-coded map with lower values, e.g. XAG and USOIL at 1:9. The code applies that map only when the path contains `/au/` (Australian site), so it does not apply to the global ftmo.com account.

## 7. Model-critical definitions

**(a) Maximum Daily Loss, 2-Step: the reference is the BALANCE at 00:00 CE(S)T, and the check runs on EQUITY, so floating P/L counts intraday.** S4 [page]:
> "The Maximum Daily Loss rule establishes a limit (the Maximum Daily Loss Limit ) below which your account equity (i.e., Balance + Open Positions P/L ± Swaps – Commissions) cannot drop. If the equity drops below this limit, the rule is considered violated.
> The Maximum Daily Loss Limit is recalculated daily at 00:00 CE(S)T as the difference between:
> the account balance recorded at 00:00 CE(S)T of the current day and
> the Maximum Daily Loss Amount , which is 5% of the Initial Simulated Capital.
> On the first day of trading, the account balance used for this calculation is the Initial Simulated Capital.
> This calculated limit remains in effect until the next recalculation at 00:00 CE(S)T of the following day.
> This rule applies to both phases (FTMO Challenge and Verification) of the FTMO Challenge: 2-Step as well as the subsequent FTMO Account (2-Step) ."

The worked example reads: "Balance at midnight CE(S)T between Day 1 and Day 2 = $102,000 / Calculation = $102,000 – $5,000 = $97,000".

S18 [page] defines balance: "Balance represents the realized value of your account and changes only when a trade is closed or when a deposit or withdrawal is processed. … Open (unrealized) positions do not affect the Balance."

- The reference is **balance only**. It is not equity, and not the higher of balance and equity.
- **Implication for an always-invested book:** the effective intraday cushion is $5,000 + (floating P/L at 00:00). If the book carries a −$2,000 floating loss into midnight, only $3,000 of further equity drop is allowed that day. If it carries a +$2,000 floating gain, the cushion is $7,000, but that gain is not protected.
- Swaps are credited to the balance at rollover, so the balance moves slightly overnight even without closes.

**(b) Maximum Loss, 2-Step: static and equity-based.** S4 [page]: "The Maximum Loss rule establishes a static limit (the Maximum Loss Limit ) below which your account equity (i.e., Balance + Open Positions P/L ± Swaps – Commissions) cannot drop. … The Maximum Loss Limit is calculated as the difference between: the Initial Simulated Capital and the Maximum Loss Amount , which is 10% of the Initial Simulated Capital. This rule applies to both phases … as well as the subsequent FTMO Account (2-Step) . Example for a $100,000 account: Maximum Loss Amount = $10,000 Limit = $90,000". The floor is equity ≥ $90,000 at every tick, and it never trails. A 2-Step reward can be rolled over to "build a larger balance and drawdown buffer" (S13).

**(c) Fee refund, 2-Step.**
- S11 [page]: "FTMO Challenge: 2-Step The entry fee may be refunded with the first Reward withdrawal. The fee is refunded using the initial payment method." For the 1-Step: "The entry fee is not refunded."
- S12 [page]: "If you successfully pass the FTMO Challenge: 2-Step and receive your first Reward on your FTMO Account , the paid fee is refunded with your first Reward withdrawal."
- S20 [page]: "*Once you have successfully completed the 2-Step Evaluation Process, obtained your FTMO Account and met the conditions for receiving your first Reward, the initial fee will be refunded to you."
- S21 [page]: "Receive a 100% refund of your initial fee with your first reward withdrawal."
- S5 [page]: Refund "Yes 100%" (2-Step).
- The T&C itself is restrictive. S1 cl. 3.12: "Unless expressly agreed otherwise, once paid, you are not entitled to a refund of the FTMO Challenge Fee under any circumstances." S1 cl. 7.9 adds no refund after any FTP or Risk Management action.
- Failed Challenge or Verification: **never refunded** (3.12, 5.8.8). Inactivity termination: "without any right to a refund" (5.8.4).
- The only other route is the consumer withdrawal right (S1 cl. 12.1): "your withdrawal right applies only before you open your first simulated trade". Once the first trade is opened, it is lost.
- Refunds may be paid as FTMO Points (S1 cl. 8.1, "When selecting the method for refund of a previously purchased FTMO Challenge Fee, we may, …"). The FAQ instead says "using the initial payment method".
- The refund depends on an actual first Reward withdrawal on the FTMO Account. It is not paid on passing.

**(d) First payout and cycle on the FTMO Account.**
- S13 [page]: "You can request a Reward claim in the Account MetriX on the 14th or any following day after the first placed trade on the specific account. All open positions and pending orders must be closed. After you submit the withdrawal request, we will review your account and notify you within 1–2 business days. … the Reward is typically sent within 1–2 business days after the invoice is approved."
- 2-Step split: "You receive 80% of the profit (increases to 90% if Scaling Plan or Premium Programme conditions are met)."
- Minimums: "$20 for bank wire withdrawals and $50 for cryptocurrency withdrawals".
- S8 refers to a "new cycle (Reference Period)" restarting after each Reward withdrawal.
- **The length of later cycles is not stated on any public FTMO page.** It sits in the unpublished FTMO Account T&C.
- "All open positions … must be closed" means the bot must flatten the whole book to claim a Reward.
- Scaling (S19): "Minimum of 4 months trading … At least 10% net simulated profit … At least 2 processed Rewards within that same 4-month period".

**(e) Weekend and overnight rules for Swing.**
- S8 [page]: "The FTMO Swing account type does not have any restrictions on trading during news releases or on holding positions overnight (longer than 2 hours after market close) or over the weekend."
- S9 [page]: "Overnight and weekend position restrictions apply only to the Standard account type . The Swing account type does not have any restrictions on holding positions overnight or over the weekend." and "you are required to close your positions shortly before the markets close for the weekend or if the rollover (market break) lasts longer than 2 hours. An exception applies only to Swing accounts."
- **The FTP gap-trading ban still applies to Swing.** Its wording targets *opening* trades "two hours or less before a relevant financial market is closed for at least two hours". The Swing exemption covers *holding*, not opening, and S8 itself points Swing traders back to the FTP.
- The S7 trading hours show daily breaks for index, metal and oil CFDs of about 75 minutes (e.g., US500 20:50–22:05 UTC) and 10 minutes for FX. Daily breaks are therefore under 2 h, and the 2-hour trigger mainly bites before the **weekend close (Friday)** and before **holiday closures and early closes**.

**Other cost note (S1 cl. 5.3.4) [page]:** "where the profit or loss of a position is denominated in a currency different from the simulated account's denomination currency, a flat adjustment fee of 0.7% from the realised profit and loss at the moment the position is closed will be applied." This affects GER40, EU50, JP225, UK100, non-USD-quoted FX crosses and similar instruments on a USD account. The fee is 0.7% of the realised P/L, not of notional.

---

## Assessment: automated, diversified, daily-rebalanced multi-asset CFD book on the $100K Swing account

Assumptions:
- Daily σ of about 0.95%, 1.26% and 1.9% for the 15%, 20% and 30% vol targets.
- Gross notional of about 1.5–4x ($150k–$400k).
- Dozens of small positions in FX, index, metal and energy CFDs, held overnight and over weekends.
- The same bot runs on up to 4 FTMO accounts.

Margin check against the Swing caps: margin = Σ notional_i / lev_i.
- Example at 4x gross with 50% in FX (1:30), 30% in indices and metals (1:15) and 20% in oil (1:15): 2.0/30 + 1.2/15 + 0.8/15 ≈ 0.067 + 0.08 + 0.053 = **~20% of equity**.
- At 1.5x gross it is about 7%.
- The exceptions are 1:1 instruments (softs, crypto, equities) and DXY (1:5): every $1 of such notional uses $1 (or $0.20) of margin.

DLL breach odds use a normal approximation for one day, the reflection principle for intraday path (≈2·(1−Φ(k))), and a cushion of 5% ± the floating P/L at midnight:

| Vol | k with 0 carry | P(breach)/day | k with −1% carry | k with −2% carry |
|---|---|---|---|---|
| 15% | 5.3σ | ~1e-7 | 4.2σ (2e-5) | 3.2σ (1.5e-3) |
| 20% | 4.0σ | ~7e-5 (≈1.8%/yr; 3–5x higher with fat tails) | 3.2σ (1.5e-3) | 2.4σ (1.7e-2) |
| 30% | 2.6σ | ~8e-3 (≈87%/yr) | 2.1σ (3.4e-2) | 1.6σ (0.11) |

### Per-clause verdict table

| Clause | 15% | 20% | 30% | Reasoning |
|---|---|---|---|---|
| Max Daily Loss 5%, balance-referenced, equity-checked (S4) | OK (hard rule; low prob) | RISK of hard breach (meaningful when carrying floating losses) | **BREACH likely** within a year | 5% = 5.3σ / 4.0σ / 2.6σ with zero carry. Because the reference is balance, any floating loss carried through midnight shrinks the cushion one for one, and an always-invested book carries floating P/L by design. At 30% the expected breach rate is near certain over a year. At 20% it is acceptable only with an intraday equity kill-switch, e.g. de-risking at −3.5% from the midnight balance. |
| Max Loss 10% static, equity (S4) | RISK (moderate) | RISK (high) | **BREACH likely** | 10% equals 0.67 / 0.5 / 0.33 annual σ. A driftless book at 30% vol hits −10% quickly. No trailing, so early profits buffer later losses. |
| 13.2.3(b): Challenge loss of 8–10% held >30 days → termination (S1) | OK | RISK | RISK | Applies only to the evaluation. Higher vol makes long stays in deep drawdown more likely. |
| FTP "overleveraging / overexposure / one-sided bets" + 7.4 gambling (S1, S2, S3) | OK | OK / low RISK | **RISK (discretionary)** | Margin use is about 7–20%, far from "maximum potential of the available margin". However, 1.9% daily σ is about 38% of the DLL per 1σ day, against FTMO's own benchmark "professionals usually risk only 1%". A trend or carry book that is net long risk assets, or net short USD across majors, can be read as "one big dollar bet". Cap net factor exposure (USD, equity beta) and show it in logs. |
| 7.5.1 "substantially larger position sizes … on any of your accounts" (S1, S2) | low RISK | low RISK | RISK | Vol-targeted daily rebalancing keeps sizes smooth. Risks: (i) vol targeting scales notional up in quiet regimes, so cap per-symbol size growth; (ii) running *different* vol targets on the 4 accounts makes one account's sizes 2x the others. **Use one vol target on all copies.** |
| 7.5.2 "substantially smaller or larger number of positions" across accounts (S1) | OK | OK | OK | The same bot gives the same position count on every account. Keep the universe identical across copies. |
| 7.5.3 / 7.6.6 Risk per Trade Idea in correlated symbols (S1) | low RISK | RISK | **RISK** | The definition aggregates "correlated symbols" and is measured as the max drawdown as a % of initial capital. Clusters such as USD-crosses, equity indices, or gold+silver could be treated as one trade idea. FTMO can impose a numeric cap after the fact. At 30% a correlated cluster's drawdown can reach several %. |
| Per-asset Swing leverage caps (S6, S7) | OK | OK | OK | 1.5–4x gross against caps of 1:30 FX, 1:20 NZD/exotics, 1:15 metals/majors indices/oil, 1:9 minor indices/natgas/heating oil, 1:5 DXY, 1:1 softs/crypto/stocks. Margin is about 7–20% of equity. Only 1:1 assets could bind; keep them small or exclude them. |
| Per-order lot caps / 200 open orders / 2,000 positions or requests per day (S7, S15, S2) | OK | OK | OK | Dozens of positions with one daily rebalance is well under 200 open and 2,000 per day. Avoid frequent SL/TP modification loops. |
| FTP gap trading: opening trades ≤2 h before a ≥2 h close, or when major news is scheduled (S2) | **RISK (hard-worded)** | same | same | This does not depend on vol. A daily rebalance on Friday in the last 2 h before the weekend, or before holiday closures and early closes, opens trades inside the banned window. The Swing "no restrictions" wording covers *holding*, not this FTP. **Schedule the rebalance outside Friday's final 2 h and before holiday closes.** The news limb is vague: a daily rebalance that happens to fall before CPI or NFP could be argued to be gap trading. Rebalance at a fixed time away from scheduled tier-1 releases. |
| Weekend / overnight holding (S8, S9) | OK | OK | OK | Swing is exempt on the FTMO Account, and the evaluation has no restriction for either type. |
| Best Day / consistency (S4, S5, S10) | OK (N/A) | OK (N/A) | OK (N/A) | The Best Day rule applies to 1-Step only. 7.6.9 allows FTMO to add consistency measures later. |
| $400k cap "per trader or strategy" (S14, S1 5.8.5(c), 6.3) | OK at ≤4×$100K | OK at ≤4×$100K | OK at ≤4×$100K | 4 × $100K equals the cap exactly. A 5th account, or anyone else running the same bot, breaches it ("identically traded strategies … suspend"). Scaling-plan growth is allowed beyond $400k. |
| "Modus Operandi repeated on more accounts" (S15) + 7.8 cross-account remedies | low RISK | low RISK | RISK | Copying is not banned and is implicitly allowed within the cap. However, a single judgement of gambling-like behaviour is applied to all 4 accounts at once (7.8), so the exposure is correlated. |
| Account rolling / unusually many Orders (S1 3.14.2, S2, S3) | OK | low RISK | **RISK** | At 30% the expected DLL breaches mean frequent re-buys. Buying many challenges, breaching and re-buying matches FTMO's own description of rolling, which can lead to notice, order suspension or a cool-down. |
| Reward review / forfeiture, leverage reduction, trade cancellation (S1 7.6, S2) | low RISK | low RISK | RISK | These are discretionary, need no prior notice (7.7), and come with no fee refund (7.9). The risk rises with the size of drawdowns and P/L swings. |
| Reward claim requires all positions closed (S13) | Operational | Operational | Operational | The bot must flatten the book to claim. Plan the claim day, e.g. a weekday away from news and not inside a Friday's last 2 h. |
| 0.7% FX conversion fee on non-USD realised P/L (S1 5.3.4) | cost | cost | cost | This is small, but daily rebalancing realises P/L more often. Prefer USD-quoted instruments, or account for the fee. |

**Bottom line:**
- **15%:** no hard breach is expected. Discretionary risk is low if sizes are uniform across accounts, the Friday and holiday 2-hour window is avoided, and net factor exposure is capped.
- **20%:** workable, with an intraday equity guard against the *balance*-based DLL, because floating losses carried over midnight eat the cushion.
- **30%:** the DLL will very likely be breached (2.6σ per day before any carried loss). It also starts to look like "overexposure / one-sided bets" and, through re-buys, "account rolling".
