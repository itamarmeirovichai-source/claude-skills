# D5 — Futures prop-firm contract clauses vs. a fully automated multi-account bot fleet

Compiled 2026-10-11. All access dates are **2026-10-11**. "page" = I read the firm's page text myself (curl/WebFetch); "snippet" = only a search-engine summary or a third-party page quoting the firm; "secondary" = affiliate or vendor page. Quotes in "…" are verbatim from the source named. ⚠ = unconfirmed.

**Access log**
- Readable directly (page): topstep.com Terms of Use, help.topstep.com, bulenox.com/legal/Terms_of_Use.pdf + bulenox.com/help-center (content loaded from the site's own public CMS endpoint `bulenox.com/cms/items/help_items`, the same call the help-center page makes), support.lucidtrading.com, tradeify.co/funded-trader-agreement, help.myfundedfutures.com + myfundedfutures.com/terms, help.earn2trade.com + earn2trade.com/terms-and-conditions.
- **Blocked (403 / Cloudflare):** apextraderfunding.com, support.apextraderfunding.com, dashboard.apextraderfunding.com (User Agreement), help.tradeify.co, takeprofittrader.com/terms, takeprofittraderhelp.zendesk.com (HTML), lucidtrading.com (main site, so the Lucid ToS was not read), bulenox.com/help (the old path; the new /help-center path worked).
- **web.archive.org was unreachable** from this environment (the proxy tunnel closed; WebFetch said "unable to fetch"). The archive.org availability API worked: it lists an Apex prohibited-activities snapshot dated 2026-03-25 that I could not open.
- The **WebSearch budget ran out** partway through (shared 200-call limit). MFFU's account cap and Lucid's VPS/ToS were still open at that point. Take Profit Trader's blocked pages were then covered only through the two vendor pages that quote them (CrossTrade, PickMyTrade).
- ⚠ Disclosure: TPT's Zendesk **JSON API** (`/api/v2/help_center/en-us/articles.json`) answered 200 while the HTML help center was 403. I pulled only the **article index** (titles and updated dates) and then stopped, because reading the contents that way could count as routing around a block (brief rule). Nothing from those articles is quoted here. Lead (D5) should decide whether that access path is acceptable.

---

## 1. Topstep (Topstep LLC, Delaware)

Sources: ToU https://www.topstep.com/terms-of-use ("Last updated: September 21, 2026", page) · API https://help.topstep.com/en/articles/11187768-topstepx-api-access ("Updated over 3 weeks ago", page) · Prohibited Strategies https://help.topstep.com/en/articles/10305426 (June 10, 2026, page) · Prohibited Conduct https://help.topstep.com/en/articles/10296582 ("Updated over a week ago", page) · XFA Params https://help.topstep.com/en/articles/8284215 (Aug 5, 2026, page) · Consistency https://help.topstep.com/en/articles/8284208 (page) · Hedging https://help.topstep.com/en/articles/13747047 (Jul 27, 2026, page) · TopstepX https://help.topstep.com/en/articles/14434175 (page) · LFA https://help.topstep.com/en/articles/10657969 (page) · Combine https://help.topstep.com/en/articles/8284197 (page)

**a. Automation**
- Evaluation and XFA (sim) via API: "Yes. Custom automated strategies and bots are allowed via the TopstepX / ProjectX API, subject to standard platform rules and our prohibition on highfrequency trading (HFT)… You remain the owner of your bot and are solely responsible for its design, performance, and behavior" (API page).
- **Live Funded:** "No, Live funded accounts are not allowed to trade through the ProjectX API. The API Gateway is built for the simulated environment and isn't available on Live." Also: "Can I use automated strategies in my LFA? … automated strategies are not possible at this time in the Live Funded Account." (LFA page)
- Combine FAQ: "Can I use automated trading strategies? Yes, with conditions. Topstep won't help set up or troubleshoot automated strategies, and no exceptions are made for errant trades or malfunctions."
- ToU §27 Prohibited Conduct: "Using any software, artificial intelligence, ultra-high speed, or mass Data entry which might manipulate, abuse, or give User an unfair advantage while using the Site or Services;" and "…for example, by engaging in any short term or high frequency trades or simultaneously entering into opposite positions;"
- API key: "Your API key grants full trading access to every eligible account under your profile." "Orders executed via the API are final — no review, adjustment, or reversal." "A rule violation is treated the same whether it originates from manual trading or third-party automation."

**f. VPS / device (the key blocker for an unattended bot)**
- API page: "**All trading activity must originate from your personal device.** The use of VPS, VPNs, and remote servers is prohibited by Topstep's Terms of Use. Running automation on a VPS can result in account suspension or removal from the program." The page's table lists "Not allowed on a private server: Placing, modifying, or cancelling orders · Any automated trigger that can reach the order endpoints · Routing or relaying orders on your behalf". It sums up: "**The line is order transmission: your server can watch and record, but it cannot trade.**"
- ToU §28: "Using any VPN or VPS on Accounts is strictly prohibited and may result in account termination and forfeiture of profits."
- Conduct page: "VPNs, proxy services, TOR, geo-location obfuscation, and other identity-masking services are not permitted at Topstep." TopstepX: "Exchange rules limit you to 1 device/browser at a time."
- Topstep runs IDV: "You may be asked to re-verify at any time."

**b. Prohibited strategies** (Strategies page, verbatim headings): "Account Stacking", "Using Unfair Technology", "Trading Outside Real Market Behavior", "Trading Outside the Best Bid or Offer", "**Trading Maximum Position Size into Major News Events**". On the simulator: "Exploiting the simulator will get you removed from the program… We retain the right to reject profit claims if abuse is suspected." Examples include "Running scalping algorithms designed to exploit unrealistic SIM fills", "Making hundreds of rapid trades…", "**Using tight brackets or auto-breakeven to take advantage of favorable SIM fills**", and "usually hundreds or thousands of trades per day, with average durations measured in seconds".
- Conduct page adds: "Using an external or slow data feed", "Coordinated trading", "Cross-account hedging (single-user)", "Exploiting platform deficiencies", "**Holding a position within 2% of a product's price lock limit**", and the catch-all "Any other conduct that Topstep determines, at its sole discretion, is uncommercial, games the market, is not a viable strategy, or is not responsible trading". Penalties: "Delay or denial of a Payout request", "Permanent account closure".
- Hedging: a real-time modal, then auto-liquidation, then a signed acknowledgement. The page says copy trading and API use "can affect the potential for hedging" (no "gambling" clause was found).

**c. Copy trading:** TopstepX has a built-in Trade Copier: "mirror trades from a Lead account to 1 or more Follower accounts automatically". "Trade copying is only available for Trading Combine® and Express Funded Account® accounts. **Live Funded Account® accounts cannot use the Trade Copier.**" "The Lead account must have the lowest Maximum Position Size". "When a Payout request is submitted, Follower accounts are automatically unlinked." Across people: ToU "Trading on behalf of others including but not limited to sharing any incentives as part of any business arrangement".

**d. Consistency / payouts:** Combine: "Your single best day of profit must stay at or below 55% of your Profit Target… 55% is a hard line." XFA Standard: "5 winning days of $150+". XFA Consistency: "3 days traded, 40% consistency target… Consistency = Largest Winning Day ÷ Total Net Profit"; "Max Payout 50% of balance, up to $5,000*/$6,000*"; split 90/10. LFA: "$150+ Net P&L on 30 non-consecutive days" unlocks daily payouts.

**e. News:** only "Purposefully trading your full Maximum Position Size directly into a scheduled major news event" is prohibited.

**g. Accounts:** "You can hold up to 5 active XFAs at a time." "You can only have one (1) Live Funded Account active. **When you receive a Live Funded Account, all Express Funded Accounts are closed.**" ToU §16: "you are only permitted to have one Account" (the user profile). "All Trading Combines, Express Funded Accounts, and Live Funded Accounts must be under 1 Topstep profile."

**h. Discretion / legal:** ToU §27: "If you are found to have profited from taking advantage of the simulated environment… or otherwise deemed to have engaged in other Prohibited Conduct… **you will not be entitled to receive any withdrawals from any other account maintained with Topstep, all of which will be forfeited and closed immediately.**" §21: "reserves the right to refuse to permit or to terminate your access… at any time at its sole discretion." §32: "These Terms may change from time to time." Refund: "all fees are final, non-cancelable, and non-refundable." Law: Delaware; "arbitration in Wilmington, Delaware before one arbitrator… administered by JAMS"; "EACH WAIVES THE RIGHT TO PARTICIPATE IN A CLASS ACTION."

**i. Platform change:** ToU §12: "Topstep reserves the right to modify, change, replace, add, or remove any elements and functions". API access is "governed by the ProjectX Terms of Use, including fair-use limits" and is billed by a third party ("Sim2Funded Solutions"). Data: Topstep "bears no responsibility" for "any interruption of, or delay or inaccuracy, in the market information".

**FLEET KILLERS — Topstep:** (1) **No VPS / remote server may transmit orders. "All trading activity must originate from your personal device."** An unattended cloud bot is out, so the bot must run on Itamar's own PC. (2) **No API and no copier on Live Funded; call-up to Live closes every XFA.** Success ends automation. (3) ToU §27 cross-account forfeiture: one "Prohibited Conduct" finding (e.g. "software, artificial intelligence… unfair advantage", or sim-fill exploitation with "tight brackets") voids withdrawals from **all** accounts.

---

## 2. Apex Trader Funding — ALL OFFICIAL PAGES BLOCKED (snippet/secondary only)

Official URLs (403): https://support.apextraderfunding.com/hc/en-us/articles/40463668243099-Prohibited-Activities · …/31519788944411-Performance-Account-PA-and-Compliance · …/40463003786267-Performance-Account-PA-Trading-Rules · https://apextraderfunding.com/help-center/getting-started/prohibited-activities/ · https://apextraderfunding.com/help-center/performance-accounts-pa/how-many-paid-funded-accounts-am-i-allowed-to-have/ · https://apextraderfunding.com/help-center/additional-helpful-items/50-consistency-requirement/ · User Agreement https://dashboard.apextraderfunding.com/legal/user-agreement (and /agreement/user-agreement)

**a. Automation (snippet).** This part conflicts with our `apex-rules.md` belief:
- A search summary of the PA-and-Compliance support article (snippet) says "automation is strictly prohibited **on all account types**, including any form of AI, Autobots, algorithms, fully automated trading systems, and high-frequency trading". It also bars "hands-off, set-and-forget, or set-and-walk-away trading", with "immediate closure of your PA or Live account and forfeiture of funds".
- User Agreement (snippet, dashboard.apextraderfunding.com/legal/user-agreement): trading activity "must be initiated manually by the User through a discrete and intentional action for each individual order"; any method that "pre-programs, batch-submits, or auto-executes orders" is prohibited. Tools that only "generate trade alerts or signals" are allowed if they "do not place, modify, or cancel orders". Exceptions require "prior written consent from the Company".
- An older help text (snippet) allowed semi-automated software "actively monitored by the trader at all times", only to "assist with the speed and accuracy". ⚠ The newer article does not repeat that exception.
- **Correction to apex-rules.md:** our table says Evaluation = "permitted (actively monitored automation)". The newest snippet says the ban covers **all account types**, and the UA's manual-per-order requirement reads as program-wide. ⚠ Treat evaluation automation as **not confirmed permitted**.

**c. Copy trading (secondary, TradeDupe quoting the Apex help center "as of October 2026")**: "Copy trading across PA accounts under your personal name and business name is allowed." "However, the hedging rule still applies; all PAs must trade in the same direction and not hedge against correlated assets." "trade copying with other traders is strictly forbidden". "No Automation or Algorithm Usage allowed." "No Hedging of Any Kind – Directional Trading only." Tradovate Group Copier article: "forbids the use of Bracket orders (ATMs)" ⚠.
- Conflict (snippet of PA-Compliance): accounts "cannot be managed or influenced by any other party, person, system, automated trading bot, copy trading service, or trade mirroring software". ⚠ This is unresolved against "copy trading… is allowed".
- CrossTrade (secondary, reviewed 2026-09-23) paraphrases the UA's "Manual Order Submission Requirement" exception: manually place each order in one account and the other Apex accounts may mirror it exactly. It says TradingView webhooks and Strategy Sync are **not** allowed without written approval.

**d. Consistency:** "no single trading day accounts for more than 50% of your total accumulated profit at the time of a payout request" (secondary quoting the help center). Snippet: "Being above the 50% consistency does not fail your account". 30% applies to legacy accounts per a third party ⚠.

**g. Accounts:** "The total limit is 20 active PA accounts across all people in the same house, companies, and connections," "whether the accounts are with Rithmic, Tradovate, or WealthCharts." (secondary quoting). Snippet: exceeding the limit makes you ineligible for payouts and can lead to forfeiture or a ban. Evaluations are uncapped (secondary ⚠).

**b/e/f:** hedging is prohibited (both sides of the market, correlated instruments); "Manipulating the simulated environment, including HFT" is prohibited (snippet). Snippet: Apex "reserves the right to request additional information, including audits and verification procedures." Strategies with "'all-in' trades with maximum contract sizes, particularly at the start of a PA account" are flagged (DamnPropFirms quoting Apex). News, VPS, IP: ⚠ not found (one blog claims a household-IP cap, unsourced).

**h.** Governing law, arbitration and class waiver: ⚠ **not found** (UA blocked, and no search hit gave the text). Homepage marketing claims "no-denial payouts" (snippet), which is not contractual.

**i.** ⚠ not found.

**FLEET KILLERS — Apex:** (1) **UA "Manual Order Submission": every order "initiated manually… through a discrete and intentional action for each individual order"; anything that "pre-programs, batch-submits, or auto-executes orders" is banned without "prior written consent".** A fully automatic bot is contractually dead on PA/Live and probably on evals too. (2) Help-center ban on "any form of AI, Autobots, algorithms, fully automated trading systems, and high-frequency trading" on **all account types**, with "immediate closure… and forfeiture of funds". (3) Copy-trading wording conflict ("copy trading service, or trade mirroring software" vs "copy trading across PA accounts… is allowed"). Even the human-plus-copier shape needs written confirmation.

---

## 3. Bulenox (Bulenox LLC, Wilmington DE)

Sources: ToU PDF https://bulenox.com/legal/Terms_of_Use.pdf (header "Updated July 2021" and still the linked version, page) · Help Center https://bulenox.com/help-center (page; content from bulenox.com/cms/items/help_items) · FAQ https://bulenox.com/faq (page; bulenox.com/cms/items/faq_items)

**a. Automation**
- FAQ "Can I use bots, algos or trade copiers?": "Yes. Bots, algorithms and trade copiers are permitted. If you connect to Rithmic through a third-party API or composite software, an additional $100 per month applies. **Only user-built tools intended solely for the account owner's personal use are permitted. Commercial, shared, rented or publicly distributed automation tools are not allowed.**"
- Help Center (Qualification Rules): "If a trader chooses to connect to Rithmic through a Third-Party API or Trader Composite Software, a $100 monthly fee applies." Bulenox is "not responsible for their availability, performance, outages, malfunctions".
- ToU (2021), "ALGORITHMS AND AUTO TRADING": "You agree to not abuse the company provided service programs. It includes but is not limited to using 'scalping' algorithms, DTC Protocol Bridge API or automated discretional trading in any of the trading environments. Open and close hundreds or thousand of rapid trades by using any trading algorithms. Implementation of reckless transactions in rough markets to benefit from lack of execution. **If abuse is suspected, we reserve the right to refuse to claim any profit.** In order to avoid performance discrepancy and/or meet compliance regulations, **any third party algorithms must be approved from the Bulenox management team.**"
- ⚠ Conflict: the FAQ says no approval; the ToU says third-party algos need approval. Both are in force.

**b. Prohibited:** the items in a above. Hedging, VPS and gambling are not addressed in the help center or FAQ (⚠ none found).

**c. Copy trading:** permitted by the FAQ (above). The commercial-tool ban may cover paid copiers ⚠. Across people: not addressed.

**d. Consistency/payout:** Master: "complete at least 10 individual trading days; request at least $1,000; maintain the required Safety Threshold Reserve; **meet the 40% Consistency Rule**". "Your most profitable trading day must not represent more than 40% of your Total P&L for the applicable payout period." The first three payouts are capped ($1,500 on 50K). Payouts are processed "once a week, on Wednesdays". Fast Track: "20% for the first payout, 25% for the second and 30% from the third onwards." Momentum Master: "35%" plus "5 qualifying profitable days". Qualification: "There is no minimum trading day requirement".

**e. News:** "Yes. Trade straight through the economic calendar — CPI, FOMC, NFP and every other release. No blackout windows, no forced position closing, no penalties." Positions close by "3:59 PM CT"; "Holding positions overnight is strictly prohibited."

**f. IP/device:** ToU: "Company reserves the right at any time in its sole discretion to block certain IP addresses". There is no VPS rule (⚠ none found). "Each trader may have only one Bulenox profile and one Rithmic User ID. Creating multiple profiles or using multiple User IDs is not permitted".

**g. Accounts:** "There is no limit to the number of Qualification Accounts you can own. You may hold up to **five active Master-level accounts** in total — Master, Fast Track and Momentum Master in any combination."

**h. Discretion / legal:** Funded (live) transition: "completed at Bulenox's discretion and is not automatic after the third payout." "If you do not consent to the transition, the applicable Master Account will be closed and no additional Reward will be issued". ToU: "We retain the right to restrict or limit or terminate account(s) for any reasons at any time without prior notice." "DENY ACCESS… TO ANY PERSON FOR ANY REASON OR FOR NO REASON AT ALL". "Modifications to this Agreement shall be effective after posting." Refund: "All sales are final and no refunds shall be issued." Return Policy: "refunds are not available once an account has been created". Law: Delaware, Kent County courts; AAA binding arbitration; class procedures waived ("…utilize class action procedures"); 2-year claim limit.

**i. Platform:** all accounts sit on a single Rithmic User ID. "Bulenox cannot be held responsible for software interruptions, data feed delays, or internet connectivity issues". Under "To Services": "Company reserves the right at any time to modify or discontinue… the Company Services… with or without notice."

**FLEET KILLERS — Bulenox:** (1) **"Commercial, shared, rented or publicly distributed automation tools are not allowed."** A bot or bridge bought or rented (including a commercial copier or IBKR-to-Rithmic bridge) can void accounts. It must be user-built and single-owner. (2) ToU "any third party algorithms must be approved from the Bulenox management team" plus "If abuse is suspected, we reserve the right to refuse to claim any profit". The 2021 ToU still conflicts with the FAQ, so the firm can pick either. (3) Cap of 5 Master accounts, and Funded (live) transition "at Bulenox's discretion" (decline it and the account closes).

---

## 4. Lucid Trading

Sources (all page, support.lucidtrading.com): Other Trading Activities …/articles/11404728 (Aug 26, 2026) · Max Accounts …/11404617 (Aug 26, 2026) · Hedging …/11404734 ("Updated this week") · HFT …/11404736 (Aug 26, 2026) · Microscalping …/11404742 (Aug 26, 2026) · Integrity …/11404732 · Platforms …/11404614 (Jul 28, 2026) · Flex consistency …/12945805 · Pro consistency …/12890109 · Flex payouts …/12945796 · Pro payouts …/12890092 · Live …/16558826 · Trading times …/11404729 · Fees …/11404620. Lucid ToS: ⚠ not read (lucidtrading.com is 403).

**a. Automation:** "Automated Strategies: **Automated trading systems and trade copiers are permitted**. All automated activity must comply with Lucid Trading rules. Traders are fully responsible for any software errors, malfunctions, or unintended outcomes." No evaluation/funded split is stated. Live is not separately excluded ⚠ (confirm for LucidLive).
- HFT: "High-frequency trading (HFT) is a type of automated trading strategy that involves submitting and executing a high volume of trades within extremely short time frames… **HFT is strictly prohibited.**" Repeated offenses: "All profits generated from HFT activity will be removed. Accounts will be closed".
- Microscalping: "You will be flagged if: **More than 50% of your profits are generated from trades held for 5 seconds or less**"; continued offenses mean "All profits from microscalping activity will be forfeited".

**b. Prohibited:** "Taking advantage of system errors or update delays · Exploiting discrepancies in simulated prices · Using tactics that do not reflect real-world trading conditions". Martingale is "strongly discouraged". Flipping and DCA are allowed.
- Hedging: "strictly prohibits all forms of hedging, including… Hedging across multiple accounts held by the same user · Hedging between different users' accounts · **Hedging between different firms or funded platforms**". First flag: accounts are "reset to prior days balance". "After repeated offenses all involved accounts will be breached".

**c. Copy:** trade copiers are permitted (above). Hedging between users is banned. No max-copied number beyond the account cap.

**d. Consistency/payout:** LucidFlex eval "50% or less"; LucidFlex funded "no consistency rule"; payouts need "minimum required profit on 5 separate days" ($150 on 50K), max "50% of Profit up to $2,000" (50K), "up to 5 payouts… after which they will be moved live". LucidPro funded "40%" (35% if bought before 11/28/2025), profit goal $500 (50K), buffer = "Initial Max Loss Limit + $100". Live: "There are no consistency requirements for live accounts."

**e. News:** "Not allowed on Daily — Trading red folder news on the LucidDaily is a hard breach. Allowed on Flex, Pro and Direct".

**f. VPS/IP:** ⚠ no Lucid rule found. Accounts are capped per "household or family".

**g. Accounts:** "Up to 10 active evaluation accounts per household or family… a maximum of 10 accounts in total across evaluation accounts and funded accounts." "**Up to 5 active funded accounts per household or family.**" "Up to 5 active LucidLive accounts per household or family."

**h. Discretion:** "**All live transitions occur at the discretion of the Lucid risk team.**" If no cashout choice is made within 24h, the account auto-moves to Live. Payout: "You must not violate any Trading Rules, Terms & Conditions, or the LucidFlex Account Agreement." "Payout requests are final once submitted". "If you take a trade before your payout is processed that drops your balance below the required amount, your request may be denied." Refund, law and arbitration: ⚠ not read (ToS blocked).

**i. Platform:** both CQG (NinjaTrader, Tradovate, TradingView) and Rithmic are supported. "Traders may hold positions until 4:45 PM EST on Tradovate Live accounts, or 4:15 PM EST on Rithmic Live accounts".

**FLEET KILLERS — Lucid:** (1) Cap of **5 funded per household**, shared across plans. (2) **Cross-firm hedging ban ("between different firms or funded platforms")**. A multi-firm fleet that is ever net-opposite across firms (e.g. one firm flattening while another holds) is a breach. (3) Automated HFT and microscalp detectors (>50% of profit from ≤5s holds) with profit forfeiture. Low risk for a 1–4 trades/day bot. ⚠ Lucid's own ToS and Live-account automation terms are unread.

---

## 5. Tradeify

Sources: Funded Trader Agreement https://tradeify.co/funded-trader-agreement ("Last modified: May 2026", page). help.tradeify.co is **403**. Help-center items come from search snippets: Hedging https://help.tradeify.co/en/articles/10495868, Tradovate copier https://help.tradeify.co/en/articles/13196343, WealthCharts copier https://help.tradeify.co/en/articles/13825156 (snippet).

**a. Automation — FTA §6.6 "Automated Bots":** "The use of automated trading bots or algorithms ('bots/algos') is permitted only under the following conditions: **Ownership:** The Trader must be able to prove that the Trader is the sole owner of the bot or strategy and that no one else has access to or is using it… **Exclusive Use:** While the Trader may use the bot on the Trader's personal accounts, **using it across multiple firms is against Tradeify's policy. The bot must be solely for the Trader's own use within Tradeify.** **No High-Frequency Trading (HFT) Bots**… **Compliance & Verification:** Tradeify reserves the right to request information or documentation if our risk measures flag the Trader's account". A secondary source says Tradeify may demand "a live video of you enabling the code on your own PC" ⚠.
- §6.4: "This includes short-term or high-frequency trades." §6.5 "Consistency in Trading": "maintaining consistent trading sizes, **avoiding dollar-cost averaging** and high-frequency trading". §6.3: "Trading based on an external or delayed data feed is not allowed." §1 "Approved Platforms": "The Trader shall utilize only the trading platforms and tools explicitly sanctioned by the Company. Any deviation from this requires the Company's prior written consent."
- §6.8 Microscalping: "**50% or more of the Trader's account profit must come from trades held longer than ten (10) seconds.**"

**b. Hedging §6.7(c)**: Opposing Positions in the same product or a "Product Group" are "a breach… regardless of the Trader's intent". **§6.7(i) Cross-Platform Hedging:** opposing a position "in a Cross-Platform Account" (any other prop firm) is a breach, and "The Company may rely on information provided to it by **NinjaTrader**, acting… as an authorized third-party trade-monitoring service". §6.7(h): "every account involved… placed in violation status, and in forfeiture of any profits… whether or not those profits have been requested for payout." §6.11: Expired Contract and Non-Market Price fills may be voided "without regard to intent".

**c. Copy:** §6.7(b): "the copying or mirroring of trades between the Trader and any other person are strictly prohibited… the copying or mirroring of the Trader's own trades across the Trader's own Trader-Controlled Accounts is permitted to the extent expressly allowed by the rules published at the Help Center". Help (snippet): "Copy trading (using Trade Copier or any method) is allowed on Tradeify, but you may only copy trades between accounts that you personally own and manage." Inverting a copier, or flattening the lead while followers stay open, counts as hedging (snippet).

**d. Consistency (snippet, help center):** Growth funded 35%; Lightning funded 20/25/30% (1st/2nd/3rd+ payout); Select funded none (40% eval only). ⚠ (help center blocked).

**g. Accounts — FTA §4.2:** "maximum number of Simulated Funded Accounts… to **five (5)**. This limit applies on a per-individual and per-household basis and across ALL funded account types".

**h. Discretion / legal:** §4.4: "The Company reserves the right to take up to the end of the next payout cycle to approve, review, or deny a payout request." It "may withhold payment of any payout that has been approved but not yet paid, pending completion of a review… Payouts withheld… are subject to forfeiture". §16/§11: "The Company reserves the right to modify, amend, or update the terms, conditions, plans, and payout requirements of this Agreement, and the rules published at the Help Center… at its sole discretion and at any time… effective upon posting". Live move "in its sole and absolute discretion". §7: "All fees… are strictly non-refundable", and a chargeback means a permanent ban and "any pending or unpaid payouts will be forfeited". §10: "governed by the laws of the State of Florida… binding arbitration in Florida… (AAA)". Class waiver ⚠ not found in the FTA text.

**e/f.** News: ⚠ not in the FTA (help center blocked). VPS/IP: ⚠ not found. §6.10: "at least one trade per calendar week".

**i.** §7: no refunds for "technical malfunctions of third-party platforms".

**FLEET KILLERS — Tradeify:** (1) **§6.6 Exclusive Use: running the same bot "across multiple firms is against Tradeify's policy".** A multi-firm fleet running one bot breaches Tradeify by definition, and the firm can demand proof. (2) §6.7(i) **cross-platform hedging with NinjaTrader-supplied evidence** plus whole-account profit forfeiture without intent. (3) §4.4 open-ended withhold and forfeit of approved payouts during "review", plus unilateral rule changes "effective upon posting". Also: cap of 5 funded per household.

---

## 6. MyFundedFutures (MyFunded Futures, LLC — Texas)

Sources (page): Fair Play https://help.myfundedfutures.com/en/articles/8444599 (Aug 24, 2026) · Copy Trading …/10771500 (Aug 24, 2026) · News …/8230009 (Aug 31, 2026) · Consistency …/11994562 ("Updated over 2 weeks ago") · Someone else trade …/8230018 (Aug 24, 2026) · Refund …/11542523 (Aug 27, 2026) · Hedging …/12011241 (Nov 10, 2025) · Live FAQ …/12109396 · Chargeback …/15936848 · Terms https://myfundedfutures.com/terms (page; no revision date shown; it references a model change on "August 20, 2026")

**a. Automation (Fair Play §1):** "High-frequency Trading is not allowed on our plans. **Traders may make use of automated trading strategies tailored to their own specific settings so long as these automated tools do not aim to exploit the favorable fills offered in the Simulated Environment.** Traders trading live accounts with automated trading must abide by CME guidelines." Live: "microscalping is permitted on the live accounts."

**b. Prohibited (Fair Play §2):** "Simultaneously placing multiple limit orders at the same price to manipulate order fills is prohibited"; "Gapped or Illiquid Market Trading… not allowed"; "**Exploiting the absence of slippage and utilizing tight brackets to gain from favorable fills are not permitted**"; "Tier 1 Economic Data Trading… restricted"; "Collaborating with others to execute identical or opposite strategies across unconnected accounts is prohibited." §3: "Profits generated from prohibited trading practices will be confiscated." Hedging: "prohibits hedging of any kind… both buy and sell positions on the same underlying asset, at the same time" (micros against minis count). Terms §23.1.11 catch-all: "Any other type of behavior that the Company deems, in its sole and reasonable discretion, to be unlawful, unethical, deceptive, manipulative, high-risk…". §23.3: "The Company reserves the right to determine, at its own discretion, whether certain trades, practices, strategies, or situations are Prohibited Conduct."

**c. Copy:** "MyFunded Futures allows copy trading across all account types." Tradesyncer is the "preferred" partner; Tradovate group copier and "External copy trading solutions can also be used". "the user explicitly and irrevocably assumes full responsibility". Across people: "Traders are not permitted to copy trade one another". Terms §23.1.3.3 prohibits using "multiple accounts to hedge, mirror, copy, or coordinate trades **in a manner that provides an unfair advantage or manipulates simulated results**".

**d. Consistency:** "30% on our Rapid EOD plans and 50% for Rapid Intraday and Pro plans… Builder plans have a 50% consistency rule in the simulated funded stage." "Exceeding the consistency targets does not breach the account."

**e. News:** "Ensuring no open positions or orders are active in the order book 2 minutes before and after any data release." Tier 1 (FOMC, Minutes, Employment, CPI; EIA; Ag reports): "No positions or orders (including limit orders) can be open 2 minutes before and after the release." "Trading on T1 News events is **prohibited** for: Rapid Sim Funded, Pro Sim Funded". Permitted for all evaluations and Builder. Prohibited everywhere: "strategies that exploit immediate news bursts, such as straddles or strangles". Live: "Yes, you can trade news."

**f. Device:** "Each individual trader may not use the same device (tablet, phone or computer) as used by another trader." "The use of shared devices is strictly forbidden and may result in a breach". "all accounts participating in our challenges are exclusively traded by the account owner". No VPS rule found ⚠.

**g. Accounts:** Terms define "Account Limits" as "the maximum number and size of accounts a User may hold, as published by the Company and updated from time to time". §23.1.3.4 prohibits exceeding it. ⚠ **The number itself was not found** (search budget exhausted). Live: "Multiple live accounts… reserved solely for high-performing traders". "rejecting the move to a Live Funded Account is not possible once you are selected."

**h. Discretion / legal:** Terms §3.2: "The Company may unilaterally amend, modify, or update these Terms at any time, with or without notice." §16.2.3: "Withholding or forfeiture of funds, payouts, or rewards"; §16.5: "sole and absolute discretion in determining whether a violation has occurred". §17.1: may terminate "at any time and for any reason". §7 Dormant: no trade in 7 days means possible closure "as a breach". Refund: full refund only if no trades and within 14 days; "Breached accounts are not eligible". Law: Texas (Collin County); JAMS arbitration, Collin County; "each party expressly waives any right to participate in a class action"; arbitration costs shared evenly. Chargebacks mean a permanent bar.

**i.** §15.7: may "modify, suspend, or terminate the Sites or Services" after force majeure "without liability". Live costs (data, etc.) are deducted from the live balance.

**FLEET KILLERS — MFFU:** (1) **Tier-1 news blackout (±2 min, no resting orders) on Rapid/Pro sim-funded.** A bot that leaves a resting bracket through CPI/FOMC/NFP breaches. Every account needs a hard calendar kill-switch. (2) Automation allowed only if it does "not aim to exploit the favorable fills", with "tight brackets" named as prohibited and judged at "sole and reasonable discretion". (3) §23.1.3.3 copying across own accounts banned when it "manipulates simulated results", plus an unpublished "Account Limits" number ⚠.

---

## 7. Take Profit Trader — OFFICIAL PAGES BLOCKED (secondary only)

Official (403): https://takeprofittrader.com/terms · help center takeprofittraderhelp.zendesk.com. The index (seen via the JSON API, contents **not** read ⚠) lists: "TakeProfitTrader Universal Trading Policies (UTP)" (updated 2026-10-09), "Independent Trade Execution Policy" (2026-10-09), "Trade Copier Policy" (2026-10-09), "Rules for Multiple Accounts" (2026-09-15), "Rule 5: Be Consistent" (2026-09-22), "Rule 6: No Counter Positions", "Sustainable Trading Policy" (2026-08-27), "Being Connected in Two Places At the Same Time". **Three automation/copy articles were all revised 2 days ago.**

Secondary sources: CrossTrade https://crosstrade.io/prop-firms/take-profit-trader (page) and PickMyTrade https://pickmytrade.io/prop-firm-faq/take-profit-trader/ (page).
- **a.** CrossTrade: "Take Profit Trader's Universal Trading Policies state that **automated trading systems, bots, or algorithmic execution tools are not permitted**, and they apply to Test, PRO, and PRO+ accounts. TPT's PRO rules add that **all trades must be manually executed by the trader**." PickMyTrade: "Universal Trading Policies (search excerpt): automated systems, bots and algorithmic execution tools not permitted; all trades must be placed manually. Applies to Test, PRO, PRO+."
- **c.** CrossTrade: "TPT allows trade copiers only for accounts you own and control, and **only from its approved list**". PickMyTrade: "Trade Copier Policy excerpt: copiers allowed only across accounts you own and control, using approved copiers." ⚠ The approved list is unknown.
- **e.** CrossTrade: "PRO and PRO+: no open positions or orders from 1 minute before to 1 minute after prohibited news".
- **b.** "TPT prohibits opposing positions on the same instrument or closely related products across all account types" (CrossTrade). "TPT automatically closes any open position at 4:55 PM ET."
- **g.** CrossTrade: "5 max simultaneous PRO accounts". apex-rules.md says "10 funded / only 5 copy-traded". ⚠ Conflict, unverified.
- **d/f/h/i:** ⚠ not obtained.

**FLEET KILLERS — TPT (⚠ secondary):** (1) UTP: "automated trading systems, bots, or algorithmic execution tools are not permitted" on Test, PRO and PRO+, i.e. **every stage**. (2) "all trades must be manually executed by the trader" (an "Independent Trade Execution Policy" revised 2026-10-09). (3) Copiers only from an approved list.

---

## 8. Earn2Trade (Earn2Trade, LLC; funded accounts held by partner prop firms Helios / Appius / Kronos)

Sources (page): T&C https://www.earn2trade.com/terms-and-conditions (no revision date shown) · Prohibited Conduct https://help.earn2trade.com/en/articles/9286647 (May 6, 2024) · Copy Trades …/12034590 (Jun 22, 2026) · Multiple accounts …/5660666 (Jun 22, 2026) · Consistency …/3849975 (May 7, 2026) · Trading times …/3224526 (Nov 13, 2025) · Refund …/6803441 · Data feed …/8572729 · Prop partners …/1585409 (Nov 7, 2025)

**a. Automation:** no explicit bot permission or ban was found. Prohibited conduct includes "**Utilizing software, artificial intelligence, or ultra-fast data entry techniques that could potentially manipulate the trading environment or provide an unfair advantage**" (help and T&C). T&C: "You shall not create or use any program, tags, markers, bots… to automatically access or manipulate the Service". ⚠ Automation status is ambiguous and must be asked in writing.

**b.** "Executing an unrealistic number of contracts in a single day"; "Collaborating to manipulate… trading between connected accounts… or executing trades that hedge or pool risks among unrelated accounts"; "Trading in a manner that does not align with actual market practices"; "Bypassing geographical or other technical restrictions"; "Trading on behalf of others". Purpose: "to discourage **gambling-like actions**, prevent rule evasion, and avoid unrealistic order executions." Consequences range from a warning to "Permanently closing the trader's account".

**c. Copy — banned:** "**The use of trade copiers is not allowed on any of our programs.**" "If you pass the exam and are found to have used trade copiers to pass your accounts, you may be denied your accounts or withdrawals." "Even after you've earned a LiveSim® or Live account, trade copiers remain off-limits." T&C: "you will receive only one account (LiveSim® or Live Account)… You are not permitted to use trade copiers on your live / LiveSim® account once you have passed, either." "The prop firms do not provide a leader-follower or other trade copy system between the accounts."

**d.** "no single trading day can account for 30% or more of your total PnL" (eval only); "does not apply on the LiveSim and/or Live accounts."

**e.** "You are allowed to trade during news events — there are no restrictions on trading around economic announcements." (evaluation; flat by 3:50pm CT)

**g.** "up to **five** evaluation accounts concurrently"; "**3 funded trading accounts** active concurrently… 3 livesims, or 2 livesims and 1 live". "We suggest only trading a single account".

**h.** T&C: "E2T, in its sole discretion, may terminate your password, account or use of the Service if you breach". "E2T reserves the right to modify the terms… at any time, effective upon posting". Refund: "our company does not provide refunds". Law: "governed by Wyoming law"; non-binding mediation, then "final and binding arbitration" (AAA, Austin TX); 1-year claim limit. Class waiver ⚠ not seen.

**i.** Funded accounts are run by third-party prop firms (Helios etc.). "you will still have to execute through the Helios data feed". Evaluations use Rithmic.

**FLEET KILLERS — Earn2Trade:** (1) **Trade copiers banned at every stage, with withdrawal denial.** (2) **Cap of 3 funded accounts**, with funding by third-party partners whose own agreements are unread ⚠. (3) "software, artificial intelligence, or ultra-fast data entry… unfair advantage" is a discretionary hook against any bot.

---

## Cross-firm summary for a fully automatic, many-account bot

| Firm | Bot on eval | Bot on funded (sim) | Bot on live | Copier own accts | Funded cap | VPS | News on funded | Consistency (funded payout) | Law / forum |
|---|---|---|---|---|---|---|---|---|---|
| Topstep | yes (API) | yes (API) | **no** | yes (not LFA) | 5 XFA, then 1 LFA (XFAs close) | **banned for orders** | no max-size into major news | Std: 5×$150 days; Cons: 40% | DE, JAMS, class waiver |
| Apex ⚠ | ⚠ likely **no** | **no** (manual per order) | **no** | ⚠ conflicting | 20 PA/household | ⚠ | ⚠ | 50% | ⚠ |
| Bulenox | yes (own tool; ToU says approval) | yes | ⚠ | yes | 5 Master | none found | allowed | 40% Master; 20–30% FT; 35% Mom. | DE, AAA, class waiver |
| Lucid | yes | yes | ⚠ | yes | 5/household | ⚠ | Flex/Pro/Direct ok; Daily banned | Pro 40%; Flex none | ⚠ |
| Tradeify | yes (own, Tradeify-only) | yes (own, Tradeify-only) | ⚠ | yes, own only | 5/household | ⚠ | ⚠ | Growth 35%; Lightning 20/25/30%; Select none | FL, AAA |
| MFFU | yes (no sim-fill exploit) | yes | CME rules | yes | ⚠ "Account Limits" | none found | **T1 ±2 min banned** (Rapid/Pro) | 30%/50% by plan | TX, JAMS, class waiver |
| TPT ⚠ | **no** | **no** | **no** | approved list only | 5 PRO ⚠ | ⚠ | ±1 min banned (PRO/PRO+) | ⚠ | ⚠ |
| Earn2Trade | ⚠ ambiguous | ⚠ ambiguous | ⚠ | **banned** | 3 | none found | allowed (eval) | 30% eval only | WY, AAA |

**Structural findings**
1. **No firm allows a fully automatic bot on a live (real-capital) account in plain terms.** Topstep explicitly blocks it. Apex and TPT block automation everywhere. The others are silent or ⚠ on live.
2. **Multi-firm fleets have two specific traps:** Tradeify §6.6 bans using the bot "across multiple firms". Tradeify §6.7(i) and Lucid ban **cross-firm hedging**, with NinjaTrader data as evidence. A desync between firms (one flat, one short) can count as hedging.
3. **Per-household caps** (Apex 20, Lucid 5, Tradeify 5, Topstep 5, Bulenox 5, E2T 3) bound the fleet. A household is a defined unit at Apex, Lucid and Tradeify.
4. **The IBKR bridge** collides with Topstep (personal device, no remote order relay), Bulenox ("commercial… automation tools are not allowed", $100/mo third-party API fee), Tradeify ("Approved Platforms… prior written consent") and Apex (manual per order).
5. **Unilateral change clauses everywhere:** Topstep §32, Tradeify §16 ("effective upon posting"), MFFU §3.2 ("with or without notice"), Bulenox ("effective after posting"), E2T. TPT revised three automation/copy articles on 2026-10-09.
