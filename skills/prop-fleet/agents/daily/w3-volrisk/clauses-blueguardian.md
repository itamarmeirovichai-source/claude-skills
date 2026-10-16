# Blue Guardian: 2-Step Standard $100K, volatility and contract-safety clauses (F2)

**Access date:** 2026-10-12. Research was read-only. Nothing was bought, no logins were made and no forms were submitted. Pages were fetched with curl through the agent proxy. Raw copies are in /tmp/claude-0/f2-clauses/bg/.

**Program identified.** The current CFD two-phase program is **"2 Step Standard"**. The homepage plan JSON has `"plan":"two_step_standard"`, `"selectorLabel":"2 Step Standard"`, and the 100K price is `currentPrice 347 / originalPrice 463` with code BG25. Its sibling is "2 Step Nano". "2 Step Pro" is listed in the help center as "(Legacy Model)". "Guardian" is only the name Blue Guardian uses for a funded trader ("Guardian/Funded Trader"). No current program is called "Elite".

## Sources (all firm-owned, all HTTP 200)
| # | URL | Date shown |
|---|---|---|
| S1 | https://help.blueguardian.com/en/articles/14062291-2-step-standard-rules | September 9, 2026 |
| S2 | https://help.blueguardian.com/en/articles/9661512-prohibited-trading-practices-account-policies | June 25, 2026 |
| S3 | https://help.blueguardian.com/en/articles/9661525-platform-rules | August 21, 2026 |
| S4 | https://help.blueguardian.com/en/articles/15618204-general-information-rules | "Updated this week" (relative to 2026-10-12) |
| S5 | https://help.blueguardian.com/en/articles/9660857-how-do-payouts-work | August 31, 2026 |
| S6 | https://help.blueguardian.com/en/articles/15846933-can-i-purchase-more-accounts-than-the-maximum-allocation-limit | July 6, 2026 |
| S7 | https://help.blueguardian.com/en/articles/14187958-24-hours-payout-guarantee | "Updated over a month ago" |
| S8 | https://blueguardian.com/terms-and-conditions | undated |
| S9 | https://blueguardian.com/refund-policy | undated |
| S10 | https://blueguardian.com (homepage, including the plan JSON) | n/a |
| S11 | https://help.blueguardian.com/en/articles/16445450-2-step-nano-rules (comparison only) | n/a |
| S12 | https://help.blueguardian.com/en/articles/15859899-buy-now-pay-later-bnpl-rules (comparison only) | "Updated this week" |

Other pages searched: the help-center collections (Account Models, Payout, General Information, Prohibited Trading Practice, Platform) and https://blueguardian.com/how-it-works, which has no relevant rule text. The help-center search (`?q=`) returned no server-side results.

**Blocked hosts: none.** https://blueguardian.com/faq returned 404 (the page does not exist), which is not a block. No archive copies were used.

All quotes below are [page], copied verbatim from the fetched HTML text. They keep the firm's own typos.

---

## 1. Gambling, "all-or-nothing", "Boom or Bust", margin usage above 80%, overleveraging

- [page] S2, section "Gambling Rule": "Blue Guardian has a strict policy against “all or nothing” trading behavior." / "Trading activity will be classified as gambling if margin usage exceeds 80% in any running trade(s). This level of exposure demonstrates poor risk management and may lead to payout rejection, profit removal, or account termination."
- [page] S8, section "Trading Styles; Risk Management", sub-heading "Prohibited Strategies":
  - "Displaying insufficient risk management in a way that would not be an applicable strategy in the real market where the following hallmarks are most prevalent:"
  - "a. Excessive risk taking in terms of the % of an account risked in a single simulated-trade;"
  - "b. Excessive cumulative risk taking in terms of the % of an account risked in a series of overlapping simulated-trades;"
  - "c. Excessive risk taking exacerbated by news events. This relates to a “Boom or Bust” approach where the success or failure of the account relies upon one simulated-trade, or a series of simulated-trades connected to a major news event;"
  - "d. Simulated-trading in such a manner that if conducted in a real trading environment it would raise substantial concerns that the relevant broker or institution may suffer real financial harm resulting from the customer’s risk-taking behavior; and"
  - "e. Simulated-trading which either knowingly, or unknowingly, exploits errors or delays in pricing feeds including, but not limited to Arbitrage."
- [page] S8, under "Prohibited Trading" (relevant to holding index CFDs overnight): "Entering into an Equity CFD at or near the end of the trading day with intent of profiting from the market gap between when the market closes and reopens on the subsequent trading day, as determined by the Company in its sole and absolute discretion"
- [page] S3, section "Stop Out Level": "The trading margin Stop Out (SO) level is 100%." / "If your account falls below this level, the least profitable running trade will be closed automatically."

## 2. Maximum risk per trade or position size, and the Guardian Shield

- **No numeric per-trade or per-position risk cap and no lot-size cap were found.** The only text on this is the qualitative T&C items a and b above. S1 also says: "Stop Loss is not mandatory, but traders are fully responsible for managing their risk and staying within the account rules at all times."
- **Guardian Shield** [page], S1. Quick Overview bullet: "Guardian Shield (Funded Only): Auto-closes trades at 2% floating loss". Section "What is the Guardian Shield?":
  - "Our analysis shows that exceeding the Maximum Daily Drawdown is the main cause of account breaches, accounting for over 73% of all breaches. Our most profitable traders are those who cut losses quickly and let winning trades run. The Guardian Shield encourages proper risk management for consistent profitability."
  - "This only applies on 2step Funded Accounts:"
  - "If your PnL on open trades reaches a 2% loss (1% loss on instant account), Guardian Shield will, in most cases, automatically close all open trades for all symbols. This is a soft breach, and you may immediately begin trading afterward."
  - "Example:" / "You have a balance of $100,000 funded account and 3 open trades. Your open PnL reaches a total loss of $2,000 (2%). The Guardian Shield will automatically close all trades. You can continue trading as you like afterwards."
  - "Guardian Shield Breach Consequences:" / "• 1st Breach: Profit split reduced to 50%." / "• 2nd Breach: The account is permanently breached."
  - "Important Notice: The Guardian Shield does not reset once triggered and the profit split cannot be reinstated. These changes are permanent and cannot be reversed."
- **How to read the Shield:**
  - **What it measures:** the account-level total of floating P&L on all open trades ("PnL on open trades", "open PnL reaches a total loss"). It is not per trade and not per position.
  - **Where it is measured from:** each trade's open price. The P&L is unrealised and is not measured from the day start or from a 5 pm snapshot. Closed or realised P&L does not count.
  - **The 2% base is not defined.** The only example uses a $100,000 balance on a 100K account, so it is most likely 2% of the initial balance, $2,000 ⚠.
  - **Scope:** funded 2-Step accounts only, not the evaluation.
  - **Consequences:** the first trigger permanently cuts the split from 85% to 50%. The second trigger is a hard breach. "in most cases" means enforcement is automatic but not guaranteed.
  - **Comparison:** the 2 Step Nano page (S11) has no Shield bullet. The BNPL model (S12) has a 1% Shield.

## 3. Consistency rules and minimum profitable days

- **No consistency rule was found for 2 Step Standard**, neither 35% nor any other figure, in the evaluation or funded stage. For comparison, 2 Step Nano (S11) says: "Consistency: 50% in funded".
- [page] S1, "Minimum Trading Days": "For accounts purchased from August 20th onwards, traders must complete at least 3 trading days to pass the evaluation." / "For accounts purchased before August 20th, the existing requirement of 5 trading days will continue to apply." / "A trading day is counted on any day where at least 0.5% profit is achieved. Trading days do not need to be consecutive."
- [page] S1, "Withdrawal Condition & Eligibility Requirements": "To request a payout, traders must:" / "- Complete the minimum trading days requirement". S5 says the same: "Complete the required minimum trading days". It is ambiguous ⚠ whether the 3 days of at least 0.5% must be earned again in each payout cycle.

## 4. Account review and the right to deny withdrawals

- [page] S8, "Trading Styles; Risk Management": "Blue Guardian may perform a risk review on accounts at any stage of the process." / "Blue Guardian reserves the right to terminate an account or agreement or deny a withdrawal request if it is deemed a customer has abused margin availability on an account or not applied an appropriate risk management strategy. Such strategies include, but are not limited to those described below."
- [page] S2, intro: "To maintain a fair and secure trading environment, Blue Guardian strictly prohibits any trading activity or behavior considered unfair, abusive, or inconsistent with realistic live-market trading."
- [page] S2, "What happens if I violate a rule…": "Please note that not all violations are detected automatically. Some breaches are only identified during a manual review conducted by our Risk Team, especially during payout requests or compliance checks." / "Blue Guardian reserves the right to take action on any account found to be in violation of our Terms, even if the breach was not immediately detected by the system." / "All compliance and risk-related decisions made by the Blue Guardian Risk Team remain final and binding."
- [page] S8, "Prohibited Trading":
  - "Utilizing one strategy to pass an assessment and then utilizing a different strategy in a funded account, as determined by the Company in cooperation with Company funded at their discretion"
  - "Additionally, and before any Trader shall receive a funded account, the trading activity of the Trader under these Terms and Conditions shall be reviewed by both the Company and the Broker to determine whether such trading activity constitutes Prohibited Trading. In the case of Prohibited Trading, the Trader shall not receive a funded account."
  - "If the Company detects that your trading constitutes Prohibited Trading, your participation in the program will be terminated and may include forfeiture of any fees paid to the Company."
- [page] S8: "Company and its associates reserve the right to refuse or cancel service, terminate accounts, or remove or edit content at our sole discretion."
- [page] S5: "All payouts remain subject to compliance, account rules, and risk review."
- [page] S7: "If a payout is subject to additional compliance or risk review, the guarantee will not apply for the duration of that review."

## 5. Repeated evaluation purchases, rebuys and resets

- [page] S4, "Maximum Allocation Funding": "You may purchase and trade as many challenge accounts as you like, with no limit on the number of evaluations you can hold.However, the maximum active funded allocation allowed at any time is $400,000 across all funded account types."
- [page] S6: "Yes, you may purchase and trade as many Challenge accounts as you wish. There is no limit to the number of Challenge accounts you can own or trade simultaneously."
- [page] S8, "Account Creation" (**conflicts with S4 and S6**): "Traders are limited to one active account per challenge level, absent prior written approval by the Company."
- [page] S2, "Multiple Accounts & Promotion Abuse": "Creating multiple accounts to abuse promotions, discount codes, resets or payout conditions is strictly prohibited."
- [page] S8, "Multiple Accounts / Profiles…": "…any attempt to exploit the Company’s services - such as account multiplication, coordinated activity, use of multiple accounts to gain an unfair advantage, exceeding or exploiting the maximum capital allocation allowed per user- is strictly prohibited. This includes, without limitation, hedging across accounts, offsetting positions, exploiting pricing inefficiencies, abusing promotions, or bypassing risk management, trading limits, or payout restrictions."
- **No clause limits rebuying after a failure, and no reset product or reset limit was found.** The word "resets" appears only in the abuse clause above.

## 6. Leverage caps per asset class

[page] S3, "Leverage":
- "Evaluation x Funded (2 Step Nano & Standard)" / "- FX: 1:50" / "- Indices: 1:10" / "- Commodities: 1:10" / "- Crypto: 1:2"
- "Funded (1 Step & 2 Step Standard)" / "- FX: 1:50" / "- Indices: 1:10" / "- Commodities: 1:10" / "- Crypto: 1:2"

Metals and energies are not listed separately. S3 lists the markets as "Gold & Commodities", so both fall under "Commodities" at 1:10 (inferred).

Commissions [page] S3: "- FX: $5" / "- Indices: $0" / "- Commodities: $5" / "- Crypto: $0" (per lot).

## 7. Other rules our model needs

**(a) Daily loss.** [page] S1, "Maximum Daily Loss":
- "The maximum daily loss is limited to 4% of the initial account balance."
- "This value resets daily at 5pm EST and is calculated using the higher value between the account balance or equity at the time of the reset."
- "We calculate daily drawdown as follows: Upon the 5pm Est day change, we will take the higher figure of either the account balance or account equity and subtract a fixed 4% of the initial balance from the higher value as the daily loss limit for the new day. It is the maximum amount of loss allowed within a single trading day, which the account will be breached when daily loss exceeds this level."
- "Example 2: If on a 100K Account at 5pm EST you have an open trade with a floating loss of -$2,000, your account equity will be $98,000. Because your $100K balance is higher than your $98,000 equity, your daily drawdown limit of $4,000 will be calculated on a $100K balance. This means for the next trading day, the equity cannot drop below $96,000 ($100,000 - $4000 = $96,000)."
- S3: "The maximum daily loss limit resets at 5:00 PM EST." / "Trades left open past reset will carry into the next day’s calculations."

What this means: the floor is max(balance, equity) at 5 pm EST minus $4,000. Floating P&L is included and the breach is tested on equity. **Floating losses carried through 5 pm reduce the next day's headroom**, because the reference stays at the higher balance (Example 2 leaves only 2% headroom). The homepage tooltip says "measured from the day's starting balance" (S10). That is a generic tooltip that contradicts the rule page. The rule page is the more specific source.

**(b) Max loss.** [page] S1: "The maximum total loss allowed in 2 Step Standard account is 8%." / "Max total loss is 8% of your initial balance = $8,000. Your account equity including unrealized/floating positions must not hit/exceed below $92,000." The floor is static, on equity.

**(c) Fee refund.**
- [page] S4: "The evaluation fee for completed accounts is fully refundable after your fourth payout (excluding Instant Starter accounts). If your account is hard-breached before reaching the fourth payout, the fee will not be refunded." / "This refund policy applies to accounts purchased from January 21st, 2026 onward."
- [page] S9: "Once a purchase has been made and the evaluation credentials have been emailed to the customer, no refunds under any circumstances will be accepted." / "All sales are final."
- The earliest refund on the 14-day cycle is about day 56 of the funded stage, after four payouts. With the 7-day add-on it is about day 28.

**(d) Payout timing and fee.**
- [page] S5:
  - "Traders on Funded Accounts become eligible for payouts once:" / "- The minimum trading day requirement has been met" / "- A minimum of 14 calendar days has passed since the first trade"
  - "After the first payout, traders can request payouts every 14 days, calculated from the date of the previous payout request."
  - "- Ensure all positions and orders are fully closed (account must be flat)"
  - "- Once a payout request is made, the account will be placed into read-only mode" / "- Trading can resume once the payout has been approved"
  - "All payouts are subject to a 3% processing fee to cover payment processing and transaction costs."
  - "- Payouts are processed within 24 business hours"
  - "- Crypto payouts are available for amounts under $5,000"
- [page] S1: "Maintain the account above the initial balance". The split is 85%, or 90% with the add-on.
- Payout caps apply only to 200K–400K accounts: "First two payouts are capped at $10,000 each".

**(e) Weekend and overnight holding.**
- [page] S1: "We have no restrictions on holding trades over night or the weekend on all account types."
- Funded news rule [page] S1: "For trades executed on your Funded Account, please refrain from Opening/Closing trades 5 minutes before and 5 minutes after red folder (high-impact) news events. Any profits earned during this time or significantly influenced by news events will be subject to removal, without any account violation this also extends to trades that are maliciously attempting to bypass rule."
- Minimum hold [page] S1: "The minimum holding time is 2 minutes. If a trade is closed in under 2 minutes, it may be flagged for tick scalping, which is against our trading rules."
- The T&C clause on equity-CFD gaps is quoted in section 1.

---

## Assessment: automated, diversified, daily-rebalanced multi-asset CFD book on $100K

**Assumptions:**
- Dozens of small FX, index, metal and energy CFD positions, held overnight and over weekends.
- Annual volatility of 15%, 20% or 30% (daily standard deviation about 0.95%, 1.26% or 1.89%).
- Gross notional of 1.5x to 4x.

**Margin check.**
- At 1:50 for FX and 1:10 for the rest, margin is 2% of FX notional plus 10% of other notional.
  - 4x gross, all non-FX: 40% of equity.
  - 4x gross, 50/50 FX and non-FX: about 24%.
  - 1.5x gross, 50/50: about 9%.
- Even at an equity of $92K, 4x all non-FX is only about 43%.
- An 80% margin usage would need about 8x gross at 1:10.

**Monte Carlo** (/tmp/claude-0/f2-clauses/sim/bg_sim.py and bg_eval.py):
- 10,000 paths of 252 days, with 8 intraday sub-steps plus a weekend gap step.
- Normal and Student-t(4) shocks, annual Sharpe of 0.5.
- The Shield is modelled as total open P&L ≤ −$2,000.
- Open P&L on carried positions realises a fraction h each day. h = 1 means the whole book is closed and reopened daily; h = 0.05 means positions are about 20 days old on average.

**Guardian Shield on a funded account.** Analytically, if open P&L restarts at zero each day, the daily chance of touching −2% intraday is 2Φ(−2%/σd):

| Annual volatility | Daily chance | Days to first trigger |
|---|---|---|
| 10% | 0.15% | ~670 |
| 15% | 3.4% | ~29 |
| 20% | 11% | ~9 |
| 30% | 29% | ~3.4 |

Simulated with t(4) shocks:

| Holding | Volatility | P(1st trigger ≤20d) | P(1st trigger ≤60d) | Median days to 1st | P(2nd trigger = breach within 1y) |
|---|---|---|---|---|---|
| close/reopen daily | 15% | 45% | 80% | 24 | 81% |
| close/reopen daily | 20% | 78% | 95% | 9 | 85% |
| close/reopen daily | 30% | 94% | 96% | 3 | 80%* |
| avg age ~20d | 15% | 59% | 82% | 14 | 90% |
| avg age ~20d | 20% | 66% | 83% | 9 | 78%* |
| avg age ~20d | 30% | 68% | 74% | 4 | 45%* |

\*The lower values at high volatility arise because many paths breach the daily loss limit first (DLL breach within 1 year is 19–55%).

Carried positions make the Shield worse. Their open P&L accumulates over the holding period: the stationary s.d. is about √(1/2h)·σd ≈ 3σd for a 20-day average age, so −2% is only about 0.7 s.d. away. Keeping the Shield rare needs about 8% annual volatility or less with daily closing. Without closing, the vol must be lower still.

**Daily loss limit in the evaluation (no Shield), Phase 1 run until the 8% target, t(4):**

| Holding | Volatility | Pass | DLL breach | Max-loss breach |
|---|---|---|---|---|
| close/reopen daily | 15% | 59% | 8% | 32% |
| close/reopen daily | 20% | 54% | 18% | 28% |
| close/reopen daily | 30% | 44% | 39% | 17% |
| avg age 20d | 15% | 43% | 57% | 0% |
| avg age 20d | 20% | 40% | 60% | 0% |
| avg age 20d | 30% | 36% | 65% | 0% |

Carried floating losses are the cause: with a −3% float at 5 pm, the next day's headroom is only 1%.

### Clause table

| Clause | 15% vol | 20% vol | 30% vol | Reasoning |
|---|---|---|---|---|
| Guardian Shield, −2% total open P&L (funded only) | **BREACH (near-certain within months)** | **BREACH** | **BREACH** | The first trigger permanently cuts the split to 50%. The second, expected within about 1–3 months at 15% and within weeks at 20–30%, hard-breaches the account. It is a hard automatic rule, with no discretion needed. The book cannot run above about 8% annual volatility in funded without a risk overlay that flattens before −2% open P&L. Such an overlay is itself a near-2% stop. |
| Strategy switch between eval and funded (T&C) | RISK | RISK | RISK | De-risking only in funded to survive the Shield could be seen as "one strategy to pass… a different strategy in a funded account". The risk is discretionary. Run the same vol in both stages. |
| Daily loss 4%, higher of balance or equity at 5 pm EST, equity breach | RISK (8% per eval with daily flattening; ~57% if carried) | RISK→BREACH-prone (18% / 60%) | **Likely BREACH** (39% / 65%) | It is a hard rule. Carrying floating losses over 5 pm shrinks headroom. Flattening or re-striking positions before 5 pm EST largely removes the trap. |
| Max loss 8% static on equity | RISK (32% of evals with daily flattening) | RISK | Lower than DLL (DLL hits first) | It is a hard rule. Mostly a matter of edge and Sharpe, not of clause wording. |
| Gambling: margin usage >80% | OK | OK | OK | Margin is 9–43% of equity at 1.5x–4x gross. Hard numeric rule, not hit. |
| T&C a: "% of an account risked in a single simulated-trade" | OK | OK | OK | Dozens of small positions. |
| T&C b: "Excessive cumulative risk… overlapping simulated-trades" | Low RISK | RISK | **RISK (high)** | It is discretionary, with no number. A 1.9% daily s.d. on overlapping positions held over weekends is easy to label "excessive cumulative risk". It can be used to deny a withdrawal. |
| T&C c: "Boom or Bust" and news | OK | OK | Low RISK | Not tied to news, but the funded news window (below) applies. |
| T&C d: "real financial harm" to broker | OK | Low RISK | RISK | Discretionary. |
| Deny withdrawal for not "appropriate risk management" / "abused margin availability" | Low RISK | RISK | RISK (high) | Sole discretion; the Risk Team's decision is "final and binding". |
| Equity CFD end-of-day gap clause | Low RISK | Low RISK | Low RISK | Index CFDs held overnight and over weekends, with rebalancing near the close, could be read as gap-trading if "Equity CFD" is read to cover indices. Avoid rebalancing index CFDs "at or near the end of the trading day". |
| Funded news ±5 min (profit removal, no breach) | RISK | RISK | RISK | An automated daily rebalancer must block opens and closes on affected symbols around red-folder and FOMC events. Profits earned in the window are removed. |
| 2-minute minimum hold | OK if handled | OK | OK | The close/reopen logic must never close a ticket less than 2 minutes old. |
| Payout requires a flat account and read-only mode | Operational | Operational | Operational | The whole book must be closed before each 14-day request and stays idle until approval. |
| Minimum 3 days of ≥0.5% | OK | OK | OK | Eval: trivial. If required again in each funded 10-trading-day cycle: about 62% / 73% / 81% to get 3 such days (binomial). |
| Consistency | n/a | n/a | n/a | No consistency rule for 2 Step Standard. |
| Leverage caps (FX 1:50, indices and commodities 1:10, crypto 1:2) | OK | OK | OK | 4x gross is well below the caps. |
| Purchases and rebuys | RISK (low) | RISK (low) | RISK (low) | The help center says unlimited challenges, but the T&C says "one active account per challenge level, absent prior written approval". |

**Verdict:** Blue Guardian 2-Step Standard is **not compatible** with a 15–30% annual-volatility, multi-day-holding book in the funded stage. The Guardian Shield (−2% total open P&L, first trigger cuts the split to 50%, second hard-breaches) is near-certain to fire twice within months. The evaluation is passable, but carrying floating losses through the 5 pm EST reset makes the 4% DLL bite hard. The account suits only a book at about 8% annual volatility or less that flattens or re-strikes daily, which contradicts our design.
