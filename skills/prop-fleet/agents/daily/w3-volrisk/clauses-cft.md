# F2 clause read: Crypto Fund Trader (CFT), 2-Phase $100K

**Access date:** 2026-10-12. Read-only: nothing was bought, no account was created, no form was submitted, no one was contacted.

**Sources.** All are the firm's own pages, fetched with curl through the session proxy and converted to text. Unless a quote is marked otherwise, it comes from one of these.
| Short name | URL | Date shown / metadata |
|---|---|---|
| FAQ | https://cryptofundtrader.com/faq/ | No date on the page. WP API `modified` 2026-03-30T10:54:31 |
| T&C | https://cryptofundtrader.com/terms-and-conditions/ | No version date on the page ("© 2026"). WP API `modified` 2026-03-30T10:58:22 |
| Refund | https://cryptofundtrader.com/refund-policy/ ("Refund and Returns Policy") | WP API `modified` 2026-03-30T10:59:42 |
| EvalRules | https://cryptofundtrader.com/evaluation-rules/ (older rules page, not in the main menu) | JSON-LD `dateModified` 2025-04-23 |
| Home | https://cryptofundtrader.com/ (program cards) | n/a |
| Choose | https://cryptofundtrader.com/choose-your-challenge/ ; https://cryptofundtrader.com/bybit/ | n/a |
| Blog-FTMO | https://cryptofundtrader.com/cft-vs-ftmo-comparison/ (firm marketing blog) | `dateModified` 2026-01-21 |
| Blog-Payout | https://cryptofundtrader.com/crypto-prop-firm-payout-comparison/ (firm blog) | `dateModified` 2026-03-11 |
| Blog-Guide | https://cryptofundtrader.com/crypto-prop-firm-payout-withdrawal-guide/ (firm blog) | `dateModified` 2026-04-21 |

The WP `modified` stamps are CMS metadata. The pages show no "last updated" line, so the stamps may not reflect when the rule text changed.

**Blocked / unreachable hosts:** `help.cryptofundtrader.com` and `support.cryptofundtrader.com` did not connect (HTTP 000; they probably do not exist). `/trading-rules/` returned 404. No Cloudflare or 403 blocks were met on the main site. Not read: the funded-stage "individual agreement" (T&C §9). It is signed only after passing and is not public.

Marking: **[page]** = verbatim from the firm page fetched today. **[page, blog]** = firm's own marketing blog, which has lower authority than the FAQ or T&C. Nothing below is a search snippet. Text inside quote marks is verbatim, including the firm's typos.

Prior notes cross-checked: `w1-firms/crypto.md` §3, and the CFT rows in `w1-prop/rules.csv`. The rules.csv row `fee` ($660 for 100K 2-Phase) is now **confirmed** by T&C §5.6.1. The refundability that row left open is resolved below: **not refundable**.

---

## 1. Gambling / all-or-nothing / one-sided / overleveraging

- FAQ, "What strategies are allowed?" [page]: "However, exploitative or unrealistic strategies are not allowed. This includes, but is not limited to, high-frequency trading, tick scalping, latency arbitrage, or any strategy that does not reflect real market trading conditions." / "We also do not allow gambling-style trading, all-in trading, abusive hedging, or any trading behavior that shows a lack of proper risk management."
- FAQ, Evaluation rules › "Gambling / All-In Trading Rule" [page]: "Crypto Fund Trader does not allow gambling-style trading or all-in trading behavior." (the $10k cap follows; see §2)
- T&C §7.1 vi [page]: "The use of trading strategies that are difficult to replicate in the real market, or come with a higher risk when trying to do so. This includes, but is not limited to: operations that use all the available margin for individual positions, operations that result in excessively large fluctuations in unrealized gains/losses, etc."
- T&C §7.1 xi [page]: "Purpose that contradicts the way trading is carried out in the real market or in a manner that the Provider may suffer losses or damages as a result of the Client's activity."
- T&C §7.1 xiii [page]: "Obtain all the demo profit in a single trade." (the $10k mechanics follow; see §2)
- T&C §7.1 xv [page]: "We are a trading training company, so we do not allow in any case the non-investment, i.e., gambling; being the company's choice the right to decide on such consideration."
- T&C §7.1, closing paragraph [page]: "If the Company determines, at its discretion, that your operations constitute the aforementioned Prohibited Operations, or that they violate the Risk Management and Program Rules, or that your public statements violate the Non-Discrimination Clause, your participation will be terminated, which may include the loss of the established returns."
- EvalRules [page]: the heading reads "GAMBLING/ALL MONEY IN ONE TRADE RULE".
- **"Gambling" is not defined anywhere** beyond these phrases. No numeric "one-sided" or directional-exposure rule was found. Searched: FAQ, T&C, EvalRules, Home, Choose, Bybit page, and the site WP search for "gambling".

## 2. Max risk per trade / position size / $10k profit cap / margin

**$10,000 profit cap: a hard rule, enforced mechanically**
- FAQ, "Gambling / All-In Trading Rule" [page]: "The maximum simulated profit allowed per day and/or per trade is $10,000. If the account equity reaches more than $10,000 in simulated profit in a single day and/or from a single trade, any active trades may be closed, and any amount above the $10,000 limit may be deducted." / "The daily profit difference is calculated based on the simulated account balance at 12:10 AM UTC." / "Trades closed in multiple parts, or multiple trades opened around the same time as part of the same strategy, may be considered a single trade for the purpose of this rule."
- T&C §7.1 xiii [page]: "Obtain all the demo profit in a single trade. Once the capital reaches $10,000 of demo profit per day and/or per trade, active trades will be closed and the amount that exceeds $10,000 will be deducted. **The demo profit limit is applied per user**, the difference will be calculated based on the balance at 12:10 AM UTC. Any operation closed in several parts or several operations executed in similar time counts as a single operation." Followed by: "While in this case, future modification could be made if deemed appropriate." (Bold added.)
- EvalRules [page]: "Once the equity reached $10,000 simulated profit per day and/or per trade the active trades will be closed and the amount over $10,000 will be substracted. The difference will be calculated based on the simulated balance at 12:10 AM UTC." / "Any trade closed in several parts or several trades executed in similar time counts as a single trade."
- FAQ, Ascend [page]: "However, the maximum simulated profit limit per day and/or per trade still applies."

**Position size and margin**
- FAQ, "Is there a maximum lot size?" [page]: "There is no fixed maximum lot size. The maximum position size depends on your account's available margin and leverage."
- T&C §7.1 vi [page]: "operations that use all the available margin for individual positions" is prohibited (quoted in §1). **No numeric max-margin percentage was found.**

**Per-trade risk: 2%, but only as a condition for remedies after a suspension**
- FAQ, "What happens to my simulated profits if my final stage account is suspended?" [page]: "All trades on the final stage account must have had a Stop Loss." / "No individual trade may have exceeded 2% risk of the account size." / "You must have traded for at least 15 days."
- The same two conditions appear under FAQ, "Can I reset my final stage account after breaking a rule?" [page].
- This is **not** a trading rule. It decides whether you are eligible for the 50% "performance reward review" and for a reset after a suspension.

**Caps the firm may add later**
- T&C §6 [page]: "The Crypto Fund Trader team may, at any time and at its sole discretion, impose, modify, or remove operational restrictions on any account, evaluation, or live stage, with prior notice, to protect program integrity, risk management, compliance, or security. Restrictions may include, without limitation, leverage limits, per-trade or aggregate risk caps, maximum position size or number of simultaneous positions, news trading limits, instrument or symbol bans, prohibitions or limitations on VPS/VPN or remote access and anti-copy-trading controls. Where feasible, the firm will communicate material changes in a timely manner; however, immediate action may be taken when operationally necessary."
- Ascend accounts only, not the 2-Phase: T&C §7.1 xxi caps theoretical loss at 2% around news. Not relevant here.

## 3. Consistency rules

- **2-Phase (eval and funded): no consistency rule found.** The Home program cards for 2-Phase list only "8% Profit target / Maximum daily loss5% / Maximum overall loss10% / Minimum days traded0 / Maximum days tradedIndefinite" (Phase 1), the same with a 5% target (Phase 2), and "80% Profit Split" (Live Stage), with no consistency line [page].
- Break accounts only, which are not our product. T&C §7.1 xxiv [page]: "IN BREAK ACCOUNTS FINAL STAGE, the consistency rule set forth below must be strictly followed. On a Crypto Fund Trader Break Final Stage account, the consistency rule is a 40% limit on how much of your total profits can come from a single trading day." … "Please note that if a payout is requested and this requirement is not met, the payout request shall be rejected until the requirement is fulfilled. These conditions reset after every approved payout."
- FAQ, "What is the Consistency Rule?" [page]: "The Consistency Rule applies only to Break Final Stage accounts."
- In effect, the **$10k/day cap (§2) is a de-facto best-day cap** of 10% of a $100K account. It is applied per user.

## 4. Account review / payout denial / KYC / trade cancellation

- FAQ, "How do I reach the final stage?" [page]: "After completing the evaluation, your account may be reviewed to confirm that all program rules were followed. If approved, you may qualify for a simulated funded account".
- T&C §3.1.10 [page]: "We and our associates reserve the right to refuse or cancel service, terminate accounts, or remove or edit content at our sole discretion, without providing any reason and with immediate effect."
- T&C §3.1.11 [page]: "Upon signing the contract to receive payment for your good training, the client will have to fill out a mandatory KYC form before processing any internal incentive associated with the scholarship program."
- FAQ, "Do I need to complete KYC?" [page]: "Yes. Before any scholarship reward can be processed, your KYC must be completed and approved." … "To complete KYC, you must sign the required contract and pass the verification process."
- T&C §6, interview [page]: "The Crypto Fund Trader team may require an interview at any time as a condition to continue in the program, to receive a Ticket, or to process a scholarship. The interview may be conducted via live video, voice, screen share and written verification, as reasonably designated by the firm, and may include questions about trading approach, risk management, platform setup, and compliance with program rules. … Refusal to participate, failure to complete the interview, or providing incomplete or misleading information may result in withholding or revocation of the Ticket, cancellation of the scholarship and suspension or cancellation of the evaluation."
- T&C §7.2 ii, trade cancellation [page]: "If you have carried out or are suspected of having carried out the Prohibited Trading Practices described in Section 7.1, the Provider may consider this a breach … The Provider may: Remove the transactions that violate the prohibition from the user trading history and/or not count their results in the demo profits and/or losses achieved by the demo trading. Cancel all services provided to the user. Terminate the Agreement. Reduce the leverage offered on the account(s)." / "Failure to comply with this point is at the discretion and review of Crypto Fund Trader team … In case of account(s) cancellation, you will not be entitled to the performance-based reward or the refund of the fees paid."
- T&C §14.2, no guaranteed payout [page]: "SWISS RLCRATES AG … does not guarantee the payment of the paid scholarship to the trader. The parties agree that SWISS RLCRATES AG may, under certain circumstances, not pay the paid scholarship despite the trader's achievement, waiving any subsequent claim. … In the event that, for whatever reason, such a scholarship could not be integrated into the trader, he/she will have the right only and exclusively to the return of the fees paid for participation in the program".
- T&C §6, profits after a payout request [page]: "The demo profits generated by the user during the account lock period in case of not closing the trades after requesting a scholarship withdrawal will not be valid and may be withdrawn by the team."
- T&C §1.3.1 [page]: "The Company may modify these Conditions or any Policy at any time at its sole discretion."
- Other clauses relevant to a bot fleet [page]:
  - §7.1 iv: "Using any third-party strategy, a strategy marketed to overcome the requirements of the valuation or evaluation phase."
  - §7.1 vii: "Executing trade ideas that belong to or are inspired by third parties".
  - §7.1 viii: "operating multiple accounts from the same household, devices, or IP address/VPS".
- **"Unrealistic":** only in the FAQ, as "exploitative or unrealistic strategies are not allowed" (§1). It is not tied to a separate payout-denial clause.

## 5. Repeated evaluation purchases / resets / abuse

- FAQ, "What is the maximum allocation per user?" [page]: "The maximum simulated funded allocation per user is $300,000. This means that the total starting balance of all active final stage accounts under the same user must not exceed $300,000." / "**There is no limit on the number of evaluations a user can purchase or have active at the same time**, as long as the maximum final stage allocation limit is respected."
- T&C §7.1 xii [page]: "Exceeding the maximum capital allocation allowed as determined in the website's FAQ."
- FAQ, "Can I purchase multiple evaluations with add-ons?" [page]: "Yes. You can purchase multiple evaluations with add-ons in the same order."
- Final-stage reset (paid; conditional) [page, FAQ]: "If eligible, you have up to 30 calendar days after the rule violation to request the reset." / "$100,000 2-phase reset account – $1880." Eligibility requires all trades to have had a Stop Loss and no trade above 2% risk.
- T&C §6 [page]: "The Crypto Fund Trader team reserves the right to decide whether a user is eligible to reset their final stage account regardless of the requirements established in the FAQ. The team may choose a Reset limit at their discretion."
- **Rebuying after a failed evaluation:** no clause restricts it and none grants a discount. **No evaluation reset / retry product** was found on the firm's pages; only the final-stage reset above. A blog page "Crypto prop firm discount codes & promo offers 2026" exists (found by site search) but was not relied on.
- Anti-abuse (T&C §3.2.4) [page]: "It is strictly prohibited to lend or receive services from/for third parties of any kind, whether to boost accounts, offer benefits in exchange for accounts, profits, or any benefit from the site."

## 6. Leverage caps

**$100K 2-Phase is an "Advanced Account"** (T&C §6 list, "ADVANCED ACCOUNTS: … $100,000 2-Phase Evaluation") [page].

| Platform / account | Crypto | Forex | Indices | Commodities | Stocks |
|---|---|---|---|---|---|
| Advanced (Match-Trader & MT5): our product | 1:100 | 1:100 | 1:100 | 1:100 | 1:100 |
| Bybit (USDT perps only) | "Up to 1:100. Depending on the instrument according to the Bybit platform." | n/a | n/a | n/a | n/a |
| Student (≤$25K 2-Phase etc.), for reference | 1:5 | 1:30 | 1:20 | 1:30 | 1:5 |

- T&C §6 [page]: "ADVANCED ACCOUNTS (Match-Trader & MetaTrader 5): Forex; leverage limited to 1:100 / Commodities; leverage limited to 1:100 / Indices; leverage limited to 1:100 / Cryptos; leverage limited to 1:100 / Stocks; leverage limited to 1:100".
- FAQ [page] says the same ("Cryptos: 1:100 leverage", etc.) and for Bybit: "Leverage is available up to 1:100, depending on the instrument and the conditions provided by Bybit."
- Home [page]: "We provide leverage of 1:100 to all instruments."
- Altcoins: no separate cap is published for MT5/Match-Trader. The only altcoin differentiation is Bybit's per-instrument maximum.
- Instruments (FAQ) [page]: "556 Cryptocurrencies / 106 Forex / 15 Indices / 22 Commodities / 25 Stocks" on MT5/Match-Trader. Bybit: "only USDT crypto futures contracts are allowed. Spot trading, options trading, USDC pairs, or any other unsupported instruments are prohibited."
- The firm may cut leverage at its discretion (T&C §6 restrictions; §7.2 "Reduce the leverage offered on the account(s)").

## 7. Model parameters

**(a) Daily loss: 5%; reference is the balance at 00:05 UTC; breach is measured on equity, so floating P&L counts; there is no "higher-of" rule.**
- FAQ [page]: "Drawdown breaches are calculated based on equity." / "The daily maximum loss is calculated based on your account balance at 12:05 AM UTC each day." / "For the 2-Phase Evaluation, the daily maximum loss is 5%, and the maximum overall loss is fixed at 10% of the initial account balance."
- T&C §8 i [page]: "At no time during the '2 Phases' Evaluation or 'Ascend' Evaluation Process or Final Stage account have you registered losses in any open or closed demo trades on the same day, which exceeded in total 5% of your balance at 12:05 AM UTC or 10% of the initial demo balance."
- Add-on, T&C §5.9 [page]: "Daily Drawdown 6%: Costs 15% of the evaluation value and increases your daily loss limit to 6%."
- **What this means:** the limit is equity ≥ 0.95 × (closed balance at 00:05 UTC). **Unrealized P&L on positions open at 00:05 is not in the reference.**
  - A carried floating **loss** reduces that day's headroom one-for-one.
  - A carried floating **gain** increases it.
  - Swaps post at 00:00 UTC on MT5 (22:00 UTC on Match-Trader) (FAQ [page]), so they are in the balance before the snapshot.
  - The day runs 00:05 to 00:05 UTC, every calendar day, including Saturday and Sunday for crypto.

**(b) Max loss: static 10% of the initial balance, measured on equity.** The floor is $90,000 equity. It does not trail on 2-Phase; trailing applies only to 1-Phase and Break. Sources: the FAQ quote above, and T&C §8 i "10% of the initial demo balance".
- Add-on, T&C §5.9 [page]: "Maximum Drawdown 12%: Costs 25% of the value of the assessment and increases your maximum loss limit to 12%."
- FAQ, "What happens if I breach a trading rule?" [page]: "If you exceed any drawdown limit or breach any of our program rules, your account may be deactivated and you will be notified by email."

**(c) Fee refund: NONE with payouts.** The $100K 2-Phase fee is $660 (T&C §5.6.1 [page]: "660 USD for the Crypto Fund Trader Evaluation Process with an initial demo capital of 100,000 USD").
- T&C §5.1 [page]: "You will not be entitled to any diploma, reward, or refund if you do not fully complete the phases of our training process."
- Refund Policy §1.1 [page]: "a. You may request a withdrawal without giving a reason within fourteen (14) days. b. YOU AUTOMATICALLY LOSE YOUR RIGHT TO WITHDRAW FROM THE CONTRACT IF YOU HAVE ALREADY OPENED A POSITION ON YOUR DEMO ACCOUNT, BEFORE THE EXPIRY OF THE SPECIFIED TIME LIMIT." … "5. OUR DISCRETION Refunds are issued at our discretion and may be accepted or rejected as such."
- Blog-FTMO [page, blog]: "FTMO refunds evaluation fees with your first profit withdrawal after successfully passing both phases. CFT's fees are non-refundable regardless of outcome."
- Blog-Payout table [page, blog]: row "Fee Refund on First Payout", CFT column "No".
- The only refund paths are:
  - the 14-day withdrawal right, only before the first trade;
  - T&C §14.2, if the firm declines to pay a scholarship: "the return of the fees paid";
  - T&C §17.1: "being able to claim only the return of the payment for the training account in case it was still active at that time".
  - Under §7.2 cancellation, the refund is expressly excluded.

**(d) Payout timing**
- FAQ, "How can I request my scholarship reward?" [page]: "You can request a scholarship reward after trading for at least 15 days, or alternatively, every 30 calendar days, as long as no program rules have been violated." / "If you have the Weekly Payouts add-on, you can request a scholarship reward every 7 traded days" / "All trades must be closed before submitting a scholarship reward request. If any trades remain open, they may be manually closed."
- FAQ [page]: "The minimum number of traded days required to request a scholarship reward is 15 days, or alternatively, every 30 calendar days."
- The first payout follows the same 15-traded-days / 30-calendar-days rule for the 2-Phase. The "first scholarship reward after only 5 traded days" applies to the **3-Phase** only (FAQ, 3 Phases section [page]), which corrects the ambiguity noted in rules.csv.
- Processing, FAQ [page]: "approximately 8 hours. However, our team may take up to 48 business hours".
- Split: Home [page] "80% Profit Split"; add-on T&C §5.9 "90% Bonus Performance: Costs 20% of the evaluation price".
- Weekly add-on, T&C §5.9: "Costs 20% of the evaluation price … after just 7 active trading days".

**(e) Weekend / overnight holding: allowed.**
- FAQ [page]: "Yes. Traders are allowed to keep positions open overnight and over the weekend, regardless of the account type or instrument." / "Cryptocurrency markets are open 24 hours a day, 7 days a week."
- News is allowed on the 2-Phase: FAQ "Yes. News trading is allowed."
- Swaps apply to CFDs held at 00:00 UTC (MT5) or 22:00 UTC (Match-Trader). Bybit uses funding rates.

**Other hard rules that touch a rebalanced book**
- Reverse trading, FAQ [page]:
  - "Reverse trading is not allowed when opposite positions are opened at the same time for 60 seconds or longer."
  - "Opposite trades on the same asset with different quote currencies, such as BTC/USD and BTC/EUR, are not allowed."
  - "Opposite trades across different accounts are not allowed."
  - "You may open an opposite trade on the same instrument only if the first trade has been open for at least 24 hours."
  - T&C §7.1 xiv [page]: "Hedging or reverse trading."
- Prohibited EA types, FAQ [page]: "High-frequency trading is not allowed. This includes using programs, algorithms, bots, or automated systems to execute a large number of trades within very short periods of time." Tick scalping and arbitrage EAs are also banned. A once-daily rebalance is not HFT.

---

## Assessment: automated, diversified, daily-rebalanced book held overnight and over weekends, on $100K CFT 2-Phase

**Assumptions**
- Mostly crypto (MT5 or Match-Trader CFDs, or Bybit USDT perps) plus some FX, index and commodity CFDs.
- Account vol of 15% / 20% / 30% a year, i.e. daily s.d. of 0.95% / 1.26% / 1.9% on 365 crypto days.
- Gross notional about 0.3–0.5x at 20% (more if low-vol FX is in the mix).

**Tail rates per year.** Normal distribution vs. a fat-tailed Student-t(4) scaled to the same s.d. Real crypto books sit between the two.
| Event | 15% | 20% | 30% |
|---|---|---|---|
| One-day loss > 5% (DLL), per yr | 0.000 normal / 0.3 t4 | 0.01 / 0.9 | 1.6 / 3.7 |
| One-day gain > 10% ($10k cap, one $100K acct) | ~0 / 0.02 | ~0 / 0.07 | ~0 / 0.3 |
| Per-user $10k/day across 3×$100K funded (+3.33% day), normal | 0.1/yr | 1.5/yr | 14.5/yr |
| Whole-book gain > 10% within one 30-day payout cycle (normal, zero drift) | 3% of cycles | 7% | 17% |
| Hit −10% before +8% (Phase 1), zero-drift approximation | 44% (vol-independent; needs Sharpe to improve) | 44% | 44% |

| Clause | 15% | 20% | 30% | Reasoning |
|---|---|---|---|---|
| **Daily loss 5% of 00:05 UTC balance, equity-based** (FAQ; T&C §8 i): HARD | OK (low risk) | **RISK** | **BREACH likely within ~1 yr** | The reference excludes floating P&L, and the book never goes flat. Carried floating loss eats headroom: at 20%, a 10-day unrealized random walk has s.d. ≈ 4%, so headroom can fall to ~1–2% on a bad run. Crypto trades 7 days, so weekend crashes land in Saturday/Sunday windows with no market close to stop them. The FX/index Monday gap lands in the Sunday 00:05→Monday 00:05 window. At 30%, even with daily realization, expect ~1.5–4 breaches/yr. **Mitigation:** realize P&L (close and reopen) before 00:05 UTC. This costs ≈0.0325%/side × gross, i.e. ~0.02–0.03%/day ≈ 7–10%/yr at 0.3–0.5x gross on MT5 (more on Bybit taker fees). Alternatively realize only when carried loss exceeds ~1%. A hard intraday equity stop at ~4% below the 00:05 balance is required. The 6% DLL add-on (+15% of fee) helps materially at 20–30%. |
| **Max loss 10% static, equity** (T&C §8 i): HARD | RISK (model) | RISK | **High risk** | Static, so no trailing penalty. Pass/fail odds are set by Sharpe vs the 8%/5% targets, not by the clause. Higher vol only makes the outcome arrive faster. At 30% vol the 10% floor is ~5 daily s.d. The 12% add-on is available. |
| **$10k profit cap per day and/or per "trade"; per user; reference balance 00:10 UTC; multiple trades opened together may count as one** (FAQ; T&C §7.1 xiii): HARD and mechanically enforced | OK for one account; RISK for a fleet | **RISK** | **BREACH plausible** | (i) Single account, single day: +10% is ≳5 s.d., so negligible. (ii) **Aggregation:** "several operations executed in similar time counts as a single operation", so a daily-rebalanced book can be read as ONE trade. Its cumulative unrealized gain over a payout cycle can pass $10k (7–17% of 30-day cycles at 20–30%), triggering forced closure and deduction of the excess. (iii) The reference is the 00:10 balance, so a carried floating gain counts toward "today's" $10k. (iv) **"Applied per user"**: 3×$100K funded accounts on the same strategy share one $10k/day cap, i.e. +3.33% per day, which is routine at 30% (~14/yr) and ~1–2/yr at 20%. **Mitigation:** realize gains daily and keep per-user funded notional at ~$100K–$150K. |
| **Gambling / all-in / "excessively large fluctuations in unrealized gains/losses" / "all the available margin"** (FAQ; T&C §7.1 vi, xv): DISCRETIONARY | OK | OK–low risk | RISK | Margin use at 1:100 and 0.3–0.5x gross is ≈0.3–0.5% of equity, so there is no all-margin issue. "Excessively large fluctuations in unrealized" is undefined. Daily ±2–4% unrealized swings at 30% could be cited at payout review. "Gambling" is at "the company's choice". |
| **Max lot / margin** (FAQ): HARD only via margin | OK | OK | OK | No lot cap. Margin is far from binding at any of the three vols. |
| **Leverage 1:100 all classes (Advanced); Bybit per instrument up to 1:100** (T&C §6): HARD | OK | OK | OK | Needed leverage is ≤1–3x even with low-vol FX in the book. Note the firm may lower leverage at discretion (§6, §7.2). |
| **2%-per-trade + Stop-Loss on every trade** (FAQ, eligibility for 50% review and reset only) | Loss of safety net | Same | Same | A vol-targeted book without hard SLs forfeits the 50% suspended-account review and the $1,880 reset. If the whole book counts as one "trade", 2% risk is not met at any vol (no SL means undefined risk). Not a breach. |
| **Consistency** | N/A | N/A | N/A | None on 2-Phase. 40% best-day applies to Break Final Stage only. |
| **Reverse-trading / hedging rule** (FAQ; T&C §7.1 xiv): HARD | RISK (implementation) | Same | Same | Independent of vol. Sign flips must close before reopening. Never hold BTC/USD long with BTC/EUR short. No opposite positions on the same instrument within 24h, and none across own accounts. A fleet running different books on correlated pairs must avoid opposite exposure on the same asset across accounts. |
| **Payout: trades must be closed at request; 15 traded days / 30 calendar days** (FAQ): HARD | OK | OK | OK | The book must be flattened at each request. Profits made during the lock period while trades are open may be voided (T&C §6). The flatten also helpfully resets the $10k "trade" accumulation. |
| **Account review / interview / §14.2 no guaranteed payout / §3.1.10 terminate without reason**: DISCRETIONARY | RISK | RISK | RISK | Applies at every vol. An automated book must be explainable in a live interview ("trading approach, risk management, platform setup"). §7.1 iv/vii (third-party or marketed strategies) and §7.1 viii (multiple accounts from the same IP/VPS) matter more for a fleet than vol does. The remedy is limited to a fee refund. |
| **Fee refund** | none | none | none | $660 is sunk once the first trade is placed. There is no refund with the first payout. |

**Bottom line**
- **15%:** clean on hard rules if P&L is realized near 00:05 UTC and the per-user $10k aggregate is respected.
- **20%:** workable but DLL-sensitive, because floating losses carry into the 00:05 reference across 7-day weeks. It needs a daily realization or threshold-realization policy, an intraday equity stop at about −4% vs the 00:05 balance, and per-user funded notional kept below the level where +$10k/day is plausible. Consider the 6% DLL add-on.
- **30%:** expect DLL breaches (~1.5–4/yr). The $10k per-user / per-"trade" cap will trip on multi-account or long-held books. Not recommended.
