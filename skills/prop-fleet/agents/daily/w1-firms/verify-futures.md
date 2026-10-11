# D5: citation check of futures.md and clauses-futures.md

Verifier: D5 citation checker. Every page below was fetched again on **2026-10-11** with curl (browser user agent) and searched for the quoted text. Local copies are in `scratchpad/vf/pages/`. `raw/` was used only to find leads.
Blocks were respected. Apex (support and dashboard), TPT Zendesk HTML, takeprofittrader.com/terms and help.tradeify.co all returned **403**, and I did not route around them. The TPT Zendesk JSON API was **not** used. For Bulenox, the FAQ answers render by JavaScript, so a plain fetch and WebFetch return only the questions. My one attempt to read the site's CMS content endpoint was refused by the session permission system, so I did not pursue it. WebSearch worked for 5 queries.

Verdicts: **C** = CONFIRMED · **CDW** = CONFIRMED-DIFFERENT-WORDING · **W** = WRONG · **U** = UNREACHABLE · **SOC** = SNIPPET-ONLY-CORROBORATED · **UNS** = UNSUPPORTED

## Verdict table

| # | File | Claim (short) | URL checked | Verdict | Note |
|---|---|---|---|---|---|
| 1 | both | Topstep: "Custom automated strategies and bots are allowed via the TopstepX / ProjectX API" | help.topstep.com/en/articles/11187768 | C | verbatim; "Updated over 3 weeks ago" |
| 2 | both | Topstep: "No, Live funded accounts are not allowed to trade through the ProjectX API" | same | C | verbatim |
| 3 | both | Topstep: "All trading activity must originate from your personal device. The use of VPS, VPNs, and remote servers is prohibited…" + "Running automation on a VPS can result in account suspension or removal" | same | C | verbatim |
| 4 | clauses | Topstep: "The line is order transmission: your server can watch and record, but it cannot trade." | same | C | verbatim |
| 5 | clauses | Topstep: "Your API key grants full trading access to every eligible account…" / "Orders executed via the API are final" | same | C | |
| 6 | clauses | Topstep LFA: "automated strategies are not possible at this time in the Live Funded Account" | help.topstep.com/en/articles/10657969 | C | |
| 7 | both | Topstep: "You can hold up to 5 active XFAs at a time" (Aug 5, 2026) | …/8284215 | C | date August 5, 2026 shown. Also: "Shoulder Tap account holders are limited to 1 XFA" |
| 8 | futures | Topstep: "The XFA is the simulated funded-level account" | …/8284215 | CDW | the page says "The Express Funded Account® (XFA) is the simulated funded-level account" |
| 9 | futures | Topstep call-up: "When a trader is called up … all open Express Funded Accounts will be closed" cited to 13747178 | …/13747178 | **W** (wrong cite and wording) | That text is not on 13747178. The fact is on LFA page 10657969: "When you receive a Live Funded Account, all Express Funded Accounts are closed." |
| 10 | futures | Topstep: Live start "20% of your cumulative XFA balance — but capped… remaining 80% is held in Reserve" | …/13747178 | C | |
| 11 | futures | Topstep: "There is no warning before being called down" | …/13747178 | C | |
| 12 | both | Topstep prohibited: "Using software, AI, ultra-high speed systems… unfair advantage" and "We retain the right to reject profit claims if abuse is suspected" (June 10, 2026) | …/10305426 | C | date confirmed |
| 13 | clauses | Topstep: "Using tight brackets or auto-breakeven to take advantage of favorable SIM fills" | …/10305426 | C | |
| 14 | clauses | Topstep ToU §28: "Using any VPN or VPS on Accounts is strictly prohibited and may result in account termination and forfeiture of profits" ("Last updated: September 21, 2026") | topstep.com/terms-of-use | C | |
| 15 | clauses | Topstep ToU cross-account forfeiture: "…any other account maintained with Topstep, all of which will be forfeited and closed immediately" | same | C | |
| 16 | clauses | Topstep ToU: "only permitted to have one Account"; JAMS arbitration in Wilmington | same | C | |
| 17 | clauses | Topstep copier: "Live Funded Account® accounts cannot use the Trade Copier"; Lead account must have lowest MPS; Followers unlinked on payout | …/14434175 | C | |
| 18 | clauses | Topstep: "Exchange rules limit you to 1 device/browser at a time" | …/14434175 | C | |
| 19 | clauses | Topstep Combine: "Can I use automated trading strategies? Yes, with conditions." | …/8284197 | C | |
| 20 | clauses | Topstep conduct: VPN/proxy ban; "within 2% of a product's price lock limit" | …/10296582 | C | |
| 21 | futures | Topstep caps 50K $2,000/$3,000, 100K $3,000/$4,000, 150K $5,000/$6,000; "100% of your first $10,000" (pre-12-Jan-2026 users) | …/8284233 | C | Missing from the report: a limited-time offer (from June 2) doubles the caps if a Daily Loss Limit is added at Combine checkout (50K Standard $4,000) |
| 22 | futures | Topstep: April 2026 cap cut "hit existing traders" | tradecovex.com/guides/topstep-rule-changes-2026 (page); phidiaspropfirm.com/education/topstep-payout-rules (page) | **W** (secondary) | The cut was **28 Apr 2026** and applies to **new** $50K/$100K No Activation Fee Combines. "Existing accounts retain their original caps even after rebill or Reset" (Tradecovex). The official page shows the current caps but no date. |
| 23 | futures | Topstep Consistency Path added Feb 2026 | tradecovex (page) | SOC | Standard/Consistency split dated 5 Feb 2026 (secondary) |
| 24 | futures | TopstepX commissions from 12 Apr 2026 | — | UNS | not re-checked (NexusFi 403); stays ⚠ |
| 25 | futures | Topstep Brokerage NFA ID 0567079, introducing broker | topstep.com/about-us | C | the footer is on the page; not snippet-only |
| 26 | futures | Topstep founded 2010 as Patak Trading Partners | topstep.com/about-us | C | |
| 27 | both | ProjectX ended third-party service at end of Feb 2026, citing "upcoming compliance reporting, oversight, and audit requirements" | coinspectator (page) | C | "end of February 2026"; PickMyTrade gives "February 28, 2026" |
| 28 | futures | Coinspectator shows Lucid "received the … notice and migrated", Tradeify "moved to Tradovate", and Bulenox was forced to migrate | coinspectator (page) | **UNS** | The article only lists Lucid ("Trading Lucid") and Tradeify ("Tradify") among ProjectX users. It says nothing about migration or Tradovate, and it does not name Bulenox. The Bulenox date (15 Jan 2026) comes only from PickMyTrade. |
| 29 | futures | Bulenox stopped new ProjectX accounts on 15 Jan 2026 | blog.pickmytrade.io/does-bulenox-still-use-projectx… | C (vendor page) | verbatim |
| 30 | both | Apex: automation banned on PA/Live ("AI, autobots, algorithms, fully automated systems, HFT"), with closure and forfeiture | support.apextraderfunding.com/…/31519788944411 | U → **SOC** | 403. Corroborated by PickMyTrade (page): "bans AI systems, autobots, algorithms, fully automated trading systems, and high-frequency trading outright, on every account type". CrossTrade (page) agrees. **"Confirmed" in futures.md overstates this**: the wording is not verified on the official page. |
| 31 | futures | CrossTrade: "Automation is currently prohibited per Apex's official rules" | crosstrade.io/learn/prop-firm-ai-trading/apex-trader-funding | CDW | The actual text is "explicitly bars automation or algorithm usage" and "requires you to enter each order manually". It also says not to let an agent trade "an Apex evaluation, PA, or live account". "Last reviewed: 2026-09-23" ✓ |
| 32 | clauses | Apex UA "initiated manually… for each individual order"; "pre-programs, batch-submits, or auto-executes" | dashboard.apextraderfunding.com/legal/user-agreement | U / SOC | 403. CrossTrade paraphrases it the same way |
| 33 | apex-rules.md | Apex **Evaluation = automation permitted** | (as above) + WebSearch | **W / unresolved** | No source I could reach supports this. PickMyTrade quotes the compliance page's ban as applying "on every account type", and CrossTrade warns against automating evaluations too. One PickMyTrade summary (search snippet) still says evals allow bots. Treat evaluation automation as **likely prohibited, unconfirmed**. apex-rules.md must change. |
| 34 | futures | Apex up to 20 PAs | — | U | secondary only; unchanged ⚠ |
| 35 | both | Bulenox FAQ: "Yes. Bots, algorithms and trade copiers are permitted… $100 per month… Only user-built tools… Commercial, shared, rented or publicly distributed automation tools are not allowed." | bulenox.com/faq | U (JS) → **SOC** | Live HTML shows the question only. Corroborated by crosstrade.io/prop-firms/bulenox (page) and funded.now/propvator (snippet). |
| 36 | both | Bulenox up to 5 Master-level accounts (Master/Fast Track/Momentum) under one Rithmic ID | crosstrade.io/prop-firms/bulenox | SOC (vendor page) | the firm's page is JS-only for me; raw lead agrees |
| 37 | both | Bulenox ToU: "If abuse is suspected, we reserve the right to refuse to claim any profit"; "any third party algorithms must be approved from the Bulenox management team"; "Updated July 2021" | bulenox.com/legal/Terms_of_Use.pdf | C | verbatim, PDF re-read |
| 38 | both | Bulenox ToU: "Bulenox LLC does not provide live trading" | same | C | ToU text confirmed. **But** see #39 |
| 39 | futures | Bulenox grade reason "no live trading at all" | ToU vs help center | **W** (overstated) | The firm's own help center (raw lead; clauses-futures §3h) describes a discretionary "Funded (live) transition" after 3 payouts and "progress to live trading with Bulenox funding". This is a ToU-vs-help-center conflict, not a fact. |
| 40 | futures | Bulenox address 1201 N Orange St Ste 7149, Wilmington DE; Delaware law, Kent County | bulenox.com; ToU | C | |
| 41 | both | Lucid: "Automated trading systems and trade copiers are permitted…" (Aug 26, 2026) | support.lucidtrading.com/en/articles/11404728 | C | |
| 42 | both | Lucid: up to 5 funded per household; 10 eval+funded; 5 LucidLive | …/11404617 | C | |
| 43 | both | Lucid HFT: "All profits generated from HFT activity will be removed"; accounts closed | …/11404736 | C | |
| 44 | clauses | Lucid hedging ban incl. "Hedging between different firms or funded platforms"; reset to "prior days balance" | …/11404734 | C | "Updated this week" |
| 45 | clauses | Lucid microscalping: ">50% of profits from trades held 5 seconds or less" | …/11404742 | C | |
| 46 | both | Lucid live: "at the discretion of the Lucid risk team"; "$0 starting balance"; "All simulated prop accounts are closed when a trader is moved live" | …/16558826 | C | |
| 47 | futures | Lucid platforms list (Jul 28, 2026); LucidFlex "up to 5 payouts… then moved live" | …/11404614, …/12945796 | C | |
| 48 | both | Tradeify §6.6: sole owner; "using it across multiple firms is against Tradeify's policy. The bot must be solely for the Trader's own use within Tradeify." | tradeify.co/funded-trader-agreement | C | |
| 49 | both | Tradeify §4.2: max 5 Simulated Funded per individual and per household, across all types | same | C | Missing from the report: on Tradeify **Elite Live** the trader "may NOT hold ANY other funded accounts, challenge accounts…", and no household member may hold any Tradeify account. |
| 50 | futures | Tradeify §6.7(c): "Holding a position in a Trader-Controlled Account opposite a position in an External Account constitutes hedging and is a breach" | same | C | |
| 51 | clauses | Tradeify §6.7(i) cross-platform hedging; may rely on "NinjaTrader, acting… as an authorized third-party trade-monitoring service" | same | C | |
| 52 | both | Tradeify §4.4: "up to the end of the next payout cycle to approve, review, or deny"; may "withhold payment of any payout that has been approved but not yet paid, pending completion of a review" | same | C | |
| 53 | both | Tradeify §6.8: 50%+ of profit from trades held longer than ten (10) seconds | same | C | |
| 54 | both | Tradeify changes "effective upon posting"; Live move "sole and absolute discretion"; Florida AAA arbitration | same | C | |
| 55 | futures | Tradeify agreement version dated to May 2026 by "vendors ⚠" | same | CDW | The page itself says "Last modified: May 2026", so drop the ⚠. The document is now titled "Evaluation Services Agreement". |
| 56 | futures | Tradeify Brokerage LLC d/b/a Slay Markets, CFTC-registered IB, NFA ID 0575972, Boca Raton; Novaflame LTD HE 480295 | tradeify.co | C | |
| 57 | both | MFFU: "Traders may make use of automated trading strategies tailored to their own specific settings…" (Aug 24, 2026) | help.myfundedfutures.com/en/articles/8444599 | C | |
| 58 | clauses | MFFU: tight brackets prohibited; profits "confiscated"; no copying between traders; no shared device | …/8444599, …/8230018 | C | |
| 59 | both | MFFU: "allows copy trading across all account types"; Tradesyncer preferred (Aug 24, 2026) | …/10771500 | C | |
| 60 | futures | MFFU caps: 5 sim-funded (25K/50K only); 3 if any 100K/150K; Rapid EOD 3; Builder 50K 1 | …/16498635 (September 4, 2026) | C | also Builder 25K max 2 |
| 61 | clauses | MFFU "Account Limits… number itself was not found" (and table shows "⚠") | …/16498635 | **W** | The number is published: 5 / 3 as in #60. |
| 62 | both | MFFU T1 news: "No positions or orders (including limit orders) can be open 2 minutes before and after the release"; prohibited on Rapid Sim Funded and Pro Sim Funded (Aug 31, 2026) | …/8230009 | C | also "positions must be closed by 8:28:00… reopened after 8:32:00" |
| 63 | futures | MFFU sim funded "operates in a simulated environment"; Rapid live: $10K single-day trigger, $5K to Reserve, multiple accounts "combined into one Live account" | …/10101257, …/13134718 | C | Not in the report: profit above $10,000 on the trigger day "is forfeited" |
| 64 | futures | MFFU Rapid split 90% "as of January 12th, 2026" | …/13745661 | C | |
| 65 | futures | TPT UTP "#1: No Trading Bots or Algos… Test, PRO, and PRO+" sourced as "page, via Zendesk API" | takeprofittraderhelp.zendesk.com/…/34431153546397 | U (403) → **SOC** for substance | Substance is corroborated by crosstrade.io/prop-firms/take-profit-trader (page) and a propvator search snippet. The heading text "#1: No Trading Bots or Algos" is unverified. **The sourcing breaks the brief**: clauses-futures says the API was used for the index only, but futures.md quotes article bodies "via Zendesk API". |
| 66 | futures | TPT approved copier list (Tradesyncer, TradeCopia, Affordable Indicators, Replikanto…) | …/34431176505245 | **UNS** | The only source is the forbidden API read. CrossTrade confirms "only from its approved list" but not the names. |
| 67 | futures | TPT surveillance "Device or infrastructure clustering", "Strategy similarity" | …/34431223270557 | **UNS** | API-only; no permissible source |
| 68 | futures | TPT payout: automated 5–10 s transfers; manual review "up to 12 business hours" | …/37697356049949 | **UNS** | API-only |
| 69 | both | TPT max 5 PRO accounts | crosstrade TPT (page) | SOC | "5 max simultaneous PRO accounts". This conflicts with apex-rules.md "Take Profit Trader 10 funded / only 5 copy-traded", which is unverified |
| 70 | clauses | TPT PRO/PRO+ news window ±1 min | crosstrade TPT (page) | SOC | |
| 71 | futures | TPT address 9100 Conroy Windermere Rd Suite 200; PRO "operates in a simulated environment"; Tradovate "regulated broker for live (PRO+)" | takeprofittrader.com | C | |
| 72 | both | E2T: "Utilizing software, artificial intelligence, or ultra-fast data entry… unfair advantage" (May 6, 2024) | help.earn2trade.com/en/articles/9286647 | C | |
| 73 | both | E2T: 3 funded concurrently; "The prop firms do not provide a leader-follower…" (Jun 22, 2026) | …/5660666 | C | |
| 74 | both | E2T: "Even after you've earned a LiveSim® or Live account, trade copiers remain off-limits"; "not allowed on any of our programs" (Jun 22, 2026) | …/12034590 | C | |
| 75 | futures | E2T LiveSim "is a simulated trading account"; firm "may decide to provide a Live account instead" | …/3313030 | C | |
| 76 | futures | E2T 8.89% pass rate 2025; Sheridan WY address; T&C bots clause; Wyoming law | earn2trade.com, /terms-and-conditions | C | |
| 77 | futures | TradeDay: no platform APIs; third-party algos forbidden; "If multiple users are making the same trades…shut down" (modified 28 Nov 2025) | tradeday.freshdesk.com/…/103000085101 | C | |
| 78 | futures | TradeDay: max 5 Funded Sim; up to 5 Funded Live; "only have multiple accounts on 1 broker" (modified 8 Sep) | …/103000354796 | C | the "1 broker" line is on this article, not the homepage as the report implies |
| 79 | futures | TradeDay: copy from "your personal account elsewhere into your TradeDay account"; Funded Live and Sim cannot trade at the same time (modified 22 Sep) | …/103000008833 | C | |
| 80 | futures | TradeDay address 412 S. Wells, Chicago | tradeday.com | C | |
| 81 | futures | Alpha Futures: "AI, bots… strictly prohibited across all account types" | help.alpha-futures.com/en/articles/9508585 | C | |
| 82 | futures | Top One: "No, the use of Expert Advisors (EAs) or Bots is not allowed"; "Using a VPN or VPS (strictly prohibited)" | help.toponefutures.com/…/10907920, /11187841 | C | also bans "Trading multiple accounts from the same IP" |
| 83 | futures | Phidias: "The use of robots, fully automated trading algorithms… is not permitted" | phidiaspropfirm.com/rules | C | |
| 84 | futures | ETF: "AI, bots, EAs, and algos additionally require ETF's written authorization" | elitetraderfunding.app/help/trade-copier-disclaimer | C | |

## Counts

84 claims checked.

| Verdict | Count | Rows |
|---|---|---|
| CONFIRMED | 62 | |
| CONFIRMED-DIFFERENT-WORDING | 3 | #8, #31, #55 |
| SNIPPET-ONLY-CORROBORATED (official page 403 or JS-only; secondary page or snippet agrees) | 8 | #23, #30, #32, #35, #36, #65, #69, #70 |
| WRONG | 5 | #9, #22, #33, #39, #61 |
| UNSUPPORTED | 5 | #24, #28, #66, #67, #68 |
| UNREACHABLE, no corroboration | 1 | #34 |

## Must-fix corrections

1. **TPT sourcing (futures.md §7) breaks the brief.** The UTP, Trade Copier, Independent Execution and Payout-speed articles are labelled "page, via Zendesk API". clauses-futures.md says the contents were *not* read, so the two files contradict each other.
   - Relabel the bot ban as "403; secondary page (CrossTrade) + snippet".
   - Delete or ⚠ the copier-name list, "Device or infrastructure clustering / Strategy similarity", and the 5–10 s / 12-hour payout claims. They have no permissible source.
   - `raw/tpt_api.json` (500 KB) holds the forbidden pull. The lead should decide whether to delete it.
   - Grade **D is unaffected**.
2. **Topstep April 2026 cap cut.** The date is **28 Apr 2026**, and per secondary sources it applies to **new** $50K/$100K No Activation Fee Combines only; existing accounts keep their caps.
   - Remove "hit existing traders" from §1.5, the grade reasons and Top risk #4. Replace it with "after-the-fact change for new purchases".
   - Add the DLL limited-time doubling of caps (official page).
3. **Topstep call-up citation.** The quote "all open Express Funded Accounts will be closed" is not on 13747178. Cite LFA 10657969: "When you receive a Live Funded Account, all Express Funded Accounts are closed."
4. **MFFU account cap in clauses-futures.md.** It is not unknown. Official 16498635 (4 Sep 2026): 5 sim-funded (25K/50K only), 3 if any 100K/150K held, Rapid EOD 3, Builder 25K 2, Builder 50K 1. Fix §6g, Fleet-killer (3) and the summary-table cell.
5. **Apex wording.** Change "confirmed" to **"corroborated by secondary quotes; official page 403"**.
   - **apex-rules.md must change**: Evaluation automation "permitted" is not supported by any reachable source. The latest quotes of the compliance page say "every account type". Mark it ⚠ "likely prohibited".
   - Also unverified: "Apex 20 accounts, copy permitted across all 20" and "TPT 10 funded / 5 copy-traded". The latter conflicts with CrossTrade's "5 max simultaneous PRO accounts".
6. **Bulenox "no live trading at all"** (grade reasons). Restate it: the 2021 ToU says "does not provide live trading", but the current help center describes a discretionary Funded (live) transition after 3 payouts. This is a conflict.
   - Also relabel the FAQ quote as "JS-rendered; corroborated by vendor page". I could not re-read it live.
7. **ProjectX attribution.** Coinspectator does not say Lucid or Tradeify migrated, does not mention Tradovate, and does not name Bulenox. Relabel these as unsupported, or cite PickMyTrade for Bulenox only.
8. **Tradeify additions.**
   - Drop the ⚠ on the date: the page says "Last modified: May 2026", and the document is now titled "Evaluation Services Agreement".
   - Add the Elite Live restriction: no other Tradeify accounts for the trader or the household while Live is active. Like the other call-ups, success collapses the fleet.
9. Minor: TopstepX commission date (12 Apr 2026) is still forum-only ⚠. TradeDay's "1 broker" line belongs to the article, not the homepage. MFFU Rapid live forfeits profit above $10,000 on the trigger day.

## Grades

No letter grade changes are required by these findings. All load-bearing bot, VPS and account-cap rules for Topstep, Lucid, Tradeify, MFFU, E2T, TradeDay and the screened-out firms were confirmed verbatim.

- **Topstep C**: the reasoning should drop "cuts hit existing traders", but the VPS ban and the Live API ban alone justify C.
- **Apex D**: holds, though it rests on secondary evidence.
- **Bulenox C**: holds, with the live-trading reason rewritten.
- **Lucid B**: arguably B− for a multi-firm fleet because of the confirmed cross-firm hedging ban ("Hedging between different firms or funded platforms"). The same exposure is what drops Tradeify to C, so the grids should flag Lucid's clause as well.
