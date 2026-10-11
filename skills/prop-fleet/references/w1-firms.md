# W1 · D5: Firm due diligence and fraud risk

**Verdict: no firm is fully safe for a fully automatic bot on many funded accounts.** Five firms allow it in writing, are credible enough, and had their key clauses re-checked on their own pages:
- **FTMO**
- **MyFundedFutures**
- **Lucid**
- **Topstep** (simulated funded accounts only, bot on your own computer)
- **TradeDay**

Together they hold about **20 futures accounts** plus **one FTMO strategy capped at $400k**. The main danger is not fraud. It is the discretionary clauses that treat "one bot, many accounts" as copy trading, group trading or a single strategy.

Compiled 11 Oct 2026 by the D5 head. Sources were accessed on 2026-10-11. Nothing was bought, signed up for or contacted.

Five sub-agents researched, and two verifiers re-fetched **193 claims**:
- about 150 confirmed, verbatim or in different wording;
- 10 were wrong and are corrected below;
- the rest are snippet-only or unreachable, marked ⚠.

The working files and full source lists are in `agents/daily/w1-firms/`.

---

## 1. The safe list

"Safe enough" means all four of these hold:
1. The firm's **own current page** allows automated trading on **funded** accounts.
2. More than one funded account per person is allowed.
3. No credible regulator action, collapse signal or mass payout-denial event was found.
4. The key clauses were **re-fetched by a verifier**.

The table is ordered by how much of the plan each firm can carry.

| # | Firm | Grade | Bot on funded (own words, verified) | Fleet size | Must-do before buying |
|---|---|---|---|---|---|
| 1 | **MyFundedFutures** (futures) | **B−** | "Traders may make use of automated trading strategies tailored to their own specific settings so long as these automated tools do not aim to exploit the favorable fills offered in the Simulated Environment"; "allows copy trading across all account types" | 5 sim-funded (25K/50K), 3 if any 100K/150K is held | Hard news kill-switch: no positions **or resting orders** ±2 min around Tier-1 releases on Rapid/Pro funded. No tight brackets. |
| 2 | **Lucid Trading** (futures) | **B−** | "Automated trading systems and trade copiers are permitted" | 5 funded per **household** | Get the owner/entity in writing (not verified). Never be net-opposite to another firm (the hedging ban covers "different firms or funded platforms"). |
| 3 | **Topstep** (futures) | **B** (as a firm: A) | "Custom automated strategies and bots are allowed via the TopstepX / ProjectX API". Express Funded (sim) accounts only. | 5 Express Funded accounts | Bot must run on **your own computer**: "All trading activity must originate from your personal device. The use of VPS, VPNs, and remote servers is prohibited". Live Funded has **no API and no copier**, and a Live call-up closes every Express account. |
| 4 | **TradeDay** (futures) | **B−** | Own automated system allowed *inside* NinjaTrader, Tradovate, TradingView, Jigsaw or Quantower. "We do not make platform APIs available". "Algos and Bots purchased from a third party… are forbidden." | 5 Funded Sim + up to 5 **Funded Live** | Bot must live inside a supported platform. Copying "from your personal account elsewhere into your TradeDay account" is allowed, which matters for the IBKR bridge. Owner and payout record not verified ⚠. |
| 5 | **FTMO** (forex/CFD) | **B** (as a firm: A) | "we have no reasons for limiting or restricting your trading strategy, whether it's discretionary trading, algorithmic trading, EAs, etc." Swing accounts exist. | **$400k per trader *or strategy*** across all accounts (raised through scaling) | One bot equals one strategy, so many accounts do not raise the cap. Keep under 2,000 server requests a day. Standard accounts have a ±2 min news ban; Swing is exempt. |

**Conditional list.** These go on the list only after a **written** email answer to the conflict shown.

| Firm | Grade | Why only conditional |
|---|---|---|
| **Bulenox** (futures) | C | The current FAQ allows bots, but the governing Terms (dated July 2021) say "any third party algorithms must be approved from the Bulenox management team" and "If abuse is suspected, we reserve the right to refuse to claim any profit". It also bans "Commercial, shared, rented or publicly distributed automation tools", so the IBKR bridge must be self-built. Owner is hidden behind a Delaware registered agent. |
| **The5ers** (forex) | C | The T&C require "written approval from the Company prior to using any Automated Trading Software… at the Company's sole discretion". The prohibited list bans "Bulk trading … automatic trading tools that open multiple trades at the same time, clearly showing a trader is not behind the strategy" and "copy trading with other traders **or accounts**". |
| **FXIFY** (forex) | C | EAs need "review by our support team and pre-approval" and are banned on Instant Funded. One account per size, about $805k in total. |
| **E8 Markets** (forex) | C ⚠ | "One strategy per user" and a cap of $500k per market per household. The firm's terms and help center were blocked (403), so this is snippet-only. |
| **Funding Pips** (forex) | C | Own EA allowed only with proof of ownership, at the firm's discretion. A VPN/VPS ban appears on two third-party rule pages ⚠. The 2026 "PRIME" migration turned pending payouts into new simulated balance. |
| **Tradeify** (futures) | C | Usable only if Tradeify is the *only* firm running the bot. §6.6 says "using it across multiple firms is against Tradeify's policy". |

**What this means for the size of the fleet.** Futures allow at most 5 + 5 + 5 + 5–10 ≈ **20–25 accounts** across the four futures firms on the safe list, plus 5 at Bulenox if it confirms in writing. Forex allows one $400k strategy at FTMO. No crypto firm qualifies. "Many accounts" in this plan therefore means about 20 to 30, spread across 4 or 5 firms. It does not mean 100 at one firm.

---

## 2. Grades for every firm

There are two grades. **Integrity** is fraud, payout and collapse risk. **Fleet fit** is whether the firm's own clauses allow a fully automatic bot on many funded accounts. The **overall** grade is the worse of the two, adjusted for evidence quality.

Grade scale:
- **A:** long record, transparent owner, clean.
- **B:** usable with named conditions.
- **C:** serious conditions or thin evidence.
- **D:** banned for this plan, or dangerous.

### Futures
| Firm | Integrity | Fleet fit | **Overall** | Main reasons |
|---|---|---|---|---|
| Topstep | A | B− | **B** | Since 2012. NFA-registered introducing-broker affiliate (Topstep Brokerage LLC). Bots allowed on Express Funded via the API. The VPS ban, no API on Live, call-up closes the fleet. Pro se suit *McCrudden v. Topstepfunded LLC* (M.D. Fla. 3:26-cv-00816, filed 9 Apr 2026) is pending. |
| MyFundedFutures | B− | B | **B−** | Own-settings automation and own-account copying allowed (verified). Cut its profit split from 90% to 80% on Flex/Pro (Feb 2026). Owner not verified. Live promotion merges all accounts into one. |
| Lucid | C+ ⚠ | A− | **B−** | Clearest written permission. Young firm; owner and entity not verified; no independent payout record collected. Live move closes sim accounts and restarts at a $0 balance. |
| TradeDay | B− ⚠ | B | **B−** | Chicago LLC. Real Funded Live accounts. No API; third-party bots banned. "If multiple users are making the same trades, then all the accounts will be shut down". |
| Bulenox | C | B | **C** | See conditional list. Payout denials on vague "flipping"/consistency grounds reported on Trustpilot. |
| Tradeify | B | D (multi-firm) / B (alone) | **C** | §6.6 cross-firm ban. §6.7(i) treats an opposite position at another firm as hedging, even without intent, using NinjaTrader monitoring data. §4.4 lets it withhold *approved* payouts during a review. Rules change "effective upon posting". |
| Apex Trader Funding | C | D | **D** | The Performance Account compliance page bans "AI, autobots, algorithms, fully automated systems" with "forfeiture of all funds". This is corroborated by vendor quotes; the official page is blocked (403). The User Agreement requires a "discrete and intentional action for each individual order". 2024–25 payout-denial waves. Pro se suit *McCrudden v. Apex* (3:26-cv-01073). Three whole-program rewrites since 2024. |
| Take Profit Trader | B | D | **D** | "Automated trading systems, bots, or algorithmic execution tools are not permitted" on all stages (CrossTrade page plus snippet; firm help center blocked). |
| Earn2Trade | B | D | **D** | "trade copiers remain off-limits" even after funding. 3 funded accounts. Clause on "software, artificial intelligence… unfair advantage". |
| Alpha Futures, Top One, Phidias | — | D | **D** | All three ban bots outright. Alpha Futures also wiped its Premium accounts with fee-only refunds in Jul 2026. |
| Elite Trader Funding | — | D | **D** | Bots need written authorization; only approved copiers are currently allowed. |

### Forex / CFD
| Firm | Integrity | Fleet fit | **Overall** | Main reasons |
|---|---|---|---|---|
| FTMO | A | B | **B** | Since 2015. Bought broker OANDA (closed 1 Dec 2025). Says it has paid more than $450M. Bots explicitly allowed. **But:** $400k per strategy; T&C 7.8 lets one forbidden practice on one account end *all* agreements; 13.2.4 allows termination without cause on 5 business days' notice; the funded-stage agreement was not read ⚠. |
| The5ers | B | C | **C** | Approval gate, bulk-trading ban, copy ban (see above). |
| FXIFY | B− | C | **C** | Pre-approval needed. About $805k total cap. Linked to the FXPIG broker ⚠. |
| E8 Markets | B ⚠ | C ⚠ | **C** | Terms unreadable here (403). DDoS outage in Feb 2025. |
| Funding Pips | C | C | **C** | MetaQuotes cut-off (Feb 2024). Trustpilot profile suspended (Jun 2024). Sister brand FundingTicks changed rules retroactively (Dec 2025) and wound down (Jan 2026). Forced PRIME migration (2026). Unclear legal entity. |
| Blue Guardian | C | C | **C** | One active account per challenge level. Ban on "VPS services linked to multiple trader accounts". Viral "windfall rule" payout denial (Aug 2026), rule dropped the same day ⚠. |
| Audacity Capital | C | B | **C** | EAs and copying allowed; over $2M combined. The contracting entity has an Anjouan (Comoros) licence, and its T&C forbid "posting negative reviews". No payout evidence collected. |
| Goat Funded Trader | C ⚠ | C | **C ⚠** | Thin evidence. Has dropped MetaTrader more than once. |
| FundedNext | B− | D | **D** | "Traders on accounts of $50,000 and above must trade fully manually". Copying between your own funded accounts is banned and detected. CFD Terms 9.8 add a **USD 25,000 penalty per trade, pattern, account or device**, set off against payouts. $300k total cap. Entity: GrowthNext F.Z.E., Ajman. |
| FTUK | C | D | **D** | Only risk-management EAs. Max 3 forex accounts, each with a different strategy and asset. A forced platform migration resets balances (profits lost). Operator: Nexdata-Solutions, Utrecht. |
| Alpha Capital Group | B | D | **D** | "Automated EAs that execute trades independently, without human oversight, are strictly prohibited". |
| FundingTraders | C | D | **D** | No EAs without a Risk Team exception. A 1-minute same-direction "coordination" test terminates all accounts. Trustpilot profile reportedly suspended ⚠. |
| Maven | C | D | **D** | "EAs are not permitted under any circumstances across all our platforms". An alleged 50,000-account "group trading" payout sweep (Aug 2025) ⚠. |

### Crypto
| Firm | Integrity | Fleet fit | **Overall** | Main reasons |
|---|---|---|---|---|
| HyroTrader | C | D | **C** | Best bot clause in crypto: "Yes, as long as the strategy is your own… we issue agent tokens". But §4.5 allows "only one Account for each program type", and §10.2(b) bans any strategy "across two or more Trading Accounts". Funded is simulated ("There is no real-capital stage at any point"). Entity moved to the UAE, with payouts from a BVI company. |
| Breakout / Kraken Prop | B | D ⚠ | **C** | Kraken owner (acquired Sep 2025); Trustpilot 4.7. Unregulated BVI program company (Payward Oceanic). $200k aggregate cap. Terminal-only, with no verified API. Terms blocked (403). |
| Crypto Fund Trader | D | D | **D** | ToS §14.2: "does not guarantee the payment of the paid scholarship". Trustpilot rating suspended over fake reviews. |
| Velotrade | D | C | **D** | Seven months old. Trustpilot rating suspended. First two payouts capped at 20× the fee, with the excess forfeited. |
| Bitfunded | C | D | **D** | "Every trade has to be placed manually". 14 of 16 accounts terminated in one Oct 2026 complaint. |

---

## 3. The clauses that can kill a bot fleet

These are verbatim and were verified unless marked ⚠. They are ordered by how likely they are to hit Itamar's plan.

1. **"One bot = one strategy = one cap."**
   - FTMO: "$400,000 per trader or strategy… If identically traded strategies are detected across multiple FTMO accounts… FTMO reserves the right to suspend the affected accounts". T&C 6.3 counts it "per client, per strategy and per ultimate beneficial owner".
   - FundedNext: "$300,000 for each EA or trading bot's strategy".
   - E8: "one strategy per user" ⚠.

   Buying more accounts does not raise the ceiling.
2. **Same trades across your own accounts = copy or group trading.**
   - The5ers: "copy trading with other traders **or accounts**" and "Bulk trading… automatic trading tools that open multiple trades at the same time".
   - FTUK: "Placing the same trades on multiple FTUK accounts is a violation".
   - FundedNext detects identical "entry price, exit price, lot size, symbols, or trade time".
   - HyroTrader §10.2(b).
   - FTMO: "Modus Operandi being repeated on more accounts… terminating the account completely".
3. **Third-party or bought bots and tools banned.**
   - Bulenox: "Commercial, shared, rented or publicly distributed automation tools are not allowed".
   - TradeDay: "Algos and Bots purchased from a third party… are forbidden".
   - Tradeify §6.6 requires proof the trader is "the sole owner".
   - The5ers bans software "owned or developed by any third party".
   - Blue Guardian bans "third-party strategy, off-the-shelf strategy".

   **The bot and the IBKR→firm bridge must be Itamar's own code, provably.**
4. **Cross-firm clauses.**
   - Tradeify §6.6: "using it across multiple firms is against Tradeify's policy".
   - Tradeify §6.7(i) and Lucid ("Hedging between different firms or funded platforms") make any moment of opposite exposure *between firms* a breach. A firm that flattens on its own drawdown rule while another firm stays in is not opposite. One that reverses while another still holds is.
5. **Where the bot may run.**
   - Topstep: "your server can watch and record, but it cannot trade". VPS is banned, so the bot must run on Itamar's own machine.
   - Funding Pips: VPN/VPS ban ⚠.
   - Blue Guardian: "VPS services linked to multiple trader accounts".
   - FTMO, by contrast: "The use of VPN/VPS is also generally allowed".
6. **Success ends the fleet.**
   - Topstep: "When you receive a Live Funded Account, all Express Funded Accounts are closed", and Live has no API.
   - Lucid: "All simulated prop accounts are closed when a trader is moved live", restarting at a $0 balance.
   - MyFundedFutures merges the accounts into one Live account.
   - Alpha Futures and Top One work the same way.
7. **One finding voids everything.**
   - Topstep ToU §27: Prohibited Conduct means "you will not be entitled to receive any withdrawals from any other account… all of which will be forfeited".
   - FTMO 7.8: terminate "all Agreements relating to all FTMO Challenge Accounts".
   - Tradeify §6.7(h): forfeiture of profits "whether or not those profits have been requested for payout".
8. **Discretion over payouts and rules.**
   - Tradeify §4.4 lets it "withhold payment of any payout that has been approved but not yet paid… subject to forfeiture".
   - MyFundedFutures §3.2: may amend "at any time, with or without notice".
   - Bulenox: "refuse to claim any profit".
   - Topstep: "reject profit claims if abuse is suspected".
   - Fee refunds are almost nowhere available.
9. **Sim-fill exploitation clauses**, which can catch a short-horizon bot:
   - MyFundedFutures: "utilizing tight brackets to gain from favorable fills are not permitted".
   - Topstep: "Using tight brackets or auto-breakeven to take advantage of favorable SIM fills".
   - Lucid: microscalping flagged at more than 50% of profit from holds of 5 seconds or less.
   - Tradeify: 50% of profit must come from trades held longer than 10 seconds.
10. **News windows.**
    - MyFundedFutures Rapid/Pro funded: "No positions or orders (including limit orders) can be open 2 minutes before and after the release".
    - FTMO Standard: ±2 min.
    - Lucid Daily: a hard breach.
    - Bulenox, Topstep (except trading maximum size into news) and the FTMO Swing account allow news trading.

---

## 4. Every funded account is simulated

Every firm checked runs the funded stage on simulated money:
- FTMO: "demo accounts with fictitious funds".
- HyroTrader: "no real-capital stage".
- Topstep: "The XFA is the simulated funded-level account".
- MyFundedFutures, Lucid, Bulenox, Tradeify and The5ers say the same.

The exceptions are a discretionary *Live* stage (Topstep LFA, MyFundedFutures Live, TradeDay Funded Live, Lucid Live), which mostly closes the simulated fleet.

What this means:
- **Payouts are paid from the firm's own cash** (mostly fee income). They are not a share of market profit. A payout is a contractual "reward" that the firm keeps broad discretion to deny.
- **Fill quality is the firm's choice.** Clauses on "favorable SIM fills" let a firm call a bot's edge an exploit after the fact.
- **The legal status is untested.** The CFTC's case against My Forex Funds alleged exactly this model, with the firm as counterparty to "substantially all customer trades". It was **dismissed with prejudice on 13–14 May 2025 because of the CFTC's own misconduct**. The court found the CFTC "acted willfully and in bad faith" and later ordered it to pay over $3.1M in fees (11 Jul 2025). Nobody ruled on whether the model is legal. Customers' money stayed frozen from Aug 2023 to Dec 2025 regardless.

---

## 5. Collapse and enforcement history (why we grade this way)

| When | What | Lesson for the fleet |
|---|---|---|
| Aug 2023 → Dec 2025 | **My Forex Funds**: CFTC and Ontario (OSC) asset freeze over more than $310M in fees. The US case was dismissed with sanctions on the CFTC (May 2025). Ontario released assets with $10M kept in escrow (Dec 2025) and ordered the OSC to pay C$80k in costs. | A regulator action freezes payouts for years, whatever the merits. |
| Feb 2024 | **MetaQuotes cut-off**: True Forex Funds halted, then closed as insolvent. Funding Pips went offline. FTMO moved US clients off MetaTrader and force-closed their positions. | One platform vendor can stop a firm within days. |
| Mar 2024 | **The Funded Trader**: "internal audit" suspended all payouts, then operations paused, then the firm moved to the Cayman Islands. Its tech vendor sued for unpaid fees (Jul 2025). Sister firm Skilled Funded Traders shut too. | A payout "audit" is the last warning. |
| May 2024 | **SurgeTrader** shut a week after losing Match-Trader. | Platform dependence. |
| 2024 | At least 50 firms closed (Finance Magnates). Trackers say about 80–100 by early 2026 ⚠. | Base rate: years in business matter. |
| Dec 2025 → Jan 2026 | **FundingTicks** (Funding Pips group): new rules reduced or invalidated profits on earlier trades, then the firm wound down. | Sister brands fall together. |
| Feb 2026 | **Seacrest / MyFundedFX** ended prop trading, with a three-week window to claim balances. | Withdraw at every payout. |
| Jul 2026 | **Alpha Futures** lost NinjaTrader and liquidated its Premium plan with activation-fee refunds only. Earned payouts were lost. | Earned is not paid. |
| Regulators | CONSOB (Italy, 8 Jul 2024) and FSMA (Belgium, Mar 2024) warnings. Czech CNB: demo-account models are not regulated. ESMA has "no substantive discussions". **No US federal or state action against a retail prop firm was found**, and a reported Aug 2026 CFTC consultation is unverified ⚠. | Regulation is not coming to protect the trader. |

**"Karen Foo"**: no prop-firm collapse under that name was found. Karen Foo is a Singapore trading educator. Treat the premise as unverified.

**Red-flag score.** The full list is `agents/daily/w1-firms/fraud.md` Task B. Score one point per flag. **Three or more flags: no bot fleet. Five or more: do not buy at all.** The strongest predictors:
- vague "gambling", "windfall" or "behavioural" denials;
- a payout pause for an "internal audit";
- retroactive rule changes;
- sweeps for prohibited strategies such as copying, groups, hedging or shared devices;
- refunds limited to fees;
- dependence on a single platform;
- sister brands under one holding company;
- unpaid vendors.

---

## 6. Rule changes in 2024–2026 that hit existing traders (verified or flagged)

- **Funding Pips PRIME (2026):** the T&C (15 May 2026) made it mandatory when invited, after the CEO had called it optional. Pending payouts became new simulated starting balance (Finance Magnates, 22 Sep 2026).
- **FundingTicks (Dec 2025):** retroactive minimum-hold rule, then wind-down. A later reversal is ⚠ not verified.
- **FTMO:** forced Australian clients onto ASIC partner VRGK Tech (Sep 2024) and moved US clients to DXtrade (Feb 2024).
- **Apex 4.0 (1 Mar 2026):** legacy accounts kept their old rules, but this was the third rewrite since 2024.
- **MyFundedFutures:** profit split cut from 90% to 80% (Feb 2026); plans moved to "Legacy".
- **Topstep:** 50K payout caps cut to $2,000 per request (28 Apr 2026). This applied to new No-Activation-Fee Combines only, per secondary sources. *(A worker said it hit existing traders; the verifier found that unsupported.)*
- **ProjectX** ended third-party service around 28 Feb 2026, and Bulenox moved to Rithmic only. **This is the precedent for platform risk on futures funded accounts.**
- **HyroTrader:** contracting entity moved to the UAE and the service declared simulated (Aug–Sep 2026). Its ToS is the only one found that says rule changes do not apply retroactively to active accounts.
- **Take Profit Trader:** automation and copier policies re-issued 2026-10-09.

---

## 7. What Itamar should do (D5 operating rules)

1. **Buy only from the safe list.** Before the first purchase at each firm, get a **written email** answer to these questions:
   - "Fully automatic, self-built bot, running unattended, on N funded accounts, all taking identical trades. Allowed?"
   - "Which platform, API and hosting are allowed?"
   - "Does the same bot running at other firms matter?"

   Keep the answer. D1's verification letters are the right tool.
2. **Save the T&C, FAQ and rule pages as PDFs on the purchase date.** Retroactive changes are the most common way earned money is lost.
3. **Withdraw at every eligible payout.** Never let profit build up at a firm.
4. **Cap exposure per firm and per holding group:** Funding Pips with FundingTicks; Alpha Capital with Alpha Futures; Easton-style groups.
5. **The bot and the bridge must be Itamar's own code**, with version history he can show. No commercial copiers at Bulenox. TradeDay and Tradeify ban third-party bots.
6. **Run the bot on his own machine** for Topstep. For other firms, a VPS is allowed or not addressed, but check firm by firm.
7. **Hard news kill-switch**, set per firm and per account type (MyFundedFutures Tier-1, FTMO Standard, Lucid Daily).
8. **Same direction across firms at all times.** Lucid's and Tradeify's cross-firm hedging bans mean one firm must never be reversed while another still holds.
9. Plan for **Live call-up to end automation** at Topstep and possibly elsewhere. Price it into D1's yearly payout model as an account that leaves the fleet.

---

## 8. Corrections to other files in this repo

- `references/apex-rules.md` says Apex **evaluations** permit automation. **No reachable source supports this.** PickMyTrade quotes the compliance page's ban as applying to "every account type", and CrossTrade advises against automating evaluations. Treat it as ⚠ likely prohibited. *(A note was added to that file.)*
- `references/apex-rules.md` says Take Profit Trader allows "10 funded / 5 copy-traded". CrossTrade says 5 PRO accounts at most, and **bots are banned there anyway**.
- `agents/ORG.md`, "Tier A = Bulenox 5 + Lucid 5": D5 keeps Lucid, but moves **Bulenox to conditional** (the 2021 ToU approval clause and the commercial-tool ban). It adds **MyFundedFutures** and **TradeDay**, and **Topstep Express Funded on own hardware**.

---

## 9. Gaps (honest list)

- **Blocked (403, not routed around):** Apex, Take Profit Trader's help center, help.tradeify.co, E8, Funding Pips terms, Breakout, cftc.gov press pages, Justia dockets, Trustpilot, Reddit and IOSCO I-SCAN. web.archive.org was unreachable. A worker pulled Take Profit Trader articles through an undocumented JSON endpoint. That copy was **deleted** and is not cited.
- **The shared web-search budget ran out** during the worker phase. Still undone:
  - per-firm docket searches (CourtListener/PACER) and NFA BASIC checks;
  - Reddit and Trustpilot payout-pattern sweeps for Lucid, MyFundedFutures, TradeDay and Tradeify.

  "None found" in this report means "none found in the searches that ran", not a clean record.
- **Owner or entity not verified:** Lucid, MyFundedFutures, Tradeify Holdings, TradeDay principals, Goat Funded Trader.
- **Not read:** FTMO's funded-stage (FTMO Account) agreement, Lucid's ToS, the HyroTrader Funded Trader Agreement, and the Kraken Prop agreement.
- The **McCrudden suits** are confirmed on CourtListener, but "pro se" is ⚠ on the Apex case, where outside counsel appeared.
