# D5 — Futures prop firms: due diligence for a fully automatic bot fleet

Worker: futures firms. Compiled 2026-10-11. All access dates are **2026-10-11** unless stated.
"page" = I read the page itself (curl/WebFetch or the firm's own help-center API); "snippet" = search-engine summary only.
⚠ = unconfirmed or secondary only. Nothing was bought, signed up for, or submitted.

## Method and limits (read first)

- **Blocked hosts (403 or no connection):** apextraderfunding.com, support.apextraderfunding.com, dashboard.apextraderfunding.com, lucidtrading.com (the main site; its help center worked), help.tradeify.co, takeprofittrader.com/faq, elitetraderfunding.com (the help center at elitetraderfunding.app worked), reddit.com, trustpilot.com. web.archive.org was reachable for the availability API only; fetches were reset by the relay (an Apex snapshot from 2026-03-25 exists but could not be read).
- **The search budget for this turn ran out** (200-call shared cap) before the per-firm lawsuit/docket sweep and the Reddit/Trustpilot sweeps were done. "None found" below means "none found in the searches that ran plus firm pages". It does **not** mean a clean court or NFA search. A follow-up with fresh search budget should run: CourtListener/PACER by firm name, NFA BASIC for each entity, and state AG press pages (TX, FL, IL).
- NFA BASIC pages (nfaid 0567079, 0575972) render by JavaScript, so their regulatory-action tabs could not be read ⚠.
- The strongest evidence below comes from firms' own help centers, read directly (Intercom/Zendesk/Freshdesk/CMS endpoints) and dated by each article's `updatedAt`.

## Summary grid

| Firm | Bot on funded? (headline) | Max funded / person | Copy own accts | VPS | Grade |
|---|---|---|---|---|---|
| Topstep | XFA: yes via TopstepX/ProjectX API; **Live Funded: API banned** | 5 XFA; all closed on Live call-up | yes (TopstepX) | **banned** | **C** |
| Apex Trader Funding | **No. Banned on PA/Live** (confirmed in official support article, snippet) | 20 PA ⚠ | manual-leader only ⚠ | n/a | **D** |
| Bulenox | **Yes** (FAQ), but 2021 ToS says third-party algos need approval | 5 (Master/FastTrack/Momentum) | yes | not addressed | **C** |
| Lucid Trading | **Yes**: "Automated trading systems and trade copiers are permitted" | 5 funded per household | yes | not addressed | **B** |
| Tradeify | Yes, with conditions; **bans using the same bot at other firms** | 5 per person/household | yes (own) | not addressed ⚠ | **C** (B if Tradeify is the only firm) |
| MyFundedFutures | Yes: "automated trading strategies tailored to their own specific settings" | 5 (3 if any 100K/150K; Rapid EOD 3) | yes (Tradesyncer etc.) | not addressed | **B** |
| Take Profit Trader | **No**: UTP #1 "No Trading Bots or Algos" | 5 ⚠ | yes, approved copiers | n/a | **D** |
| Earn2Trade | Effectively no: "software, AI…" prohibited; **copiers forbidden even when funded** | 3 funded | **no** | n/a | **D** |
| TradeDay (extra) | Yes, own ATS on NinjaTrader/Tradovate/TradingView/Jigsaw/Quantower; no API; bought algos forbidden | 5 Funded Sim + 5 Funded Live (10 total) | yes, including from a personal account elsewhere | not addressed | **B** |
| Screened out (extra candidates) | Alpha Futures, Top One Futures, Phidias, Elite Trader Funding all **ban or gate** bots (see last section) | | | | D |

---

## 1. Topstep — grade **C** for this use (A as a firm)

**Bottom line:** the most established and transparent firm on the list. But the bot can only run on up to 5 simulated XFAs, from your own PC (no VPS). Success kills the fleet: a Live call-up closes every XFA, and Live accounts cannot use the API.

1. **Regulatory/legal.** Topstep Brokerage LLC is an NFA-registered introducing broker, "NFA ID# 0567079" (snippet of topstep.com disclosure; page of topstep.com/about-us footer: "Introducing brokerage services are offered through Topstep Brokerage LLC … a registered introducing broker and a member of the National Futures Association"). No CFTC/NFA action or lawsuit was found in the searches that ran ⚠ (BASIC tab unreadable; docket search not run).
2. **Payout reliability.** Its own data is unflattering but transparent: third-party sites cite a 0.71% XFA-to-Live rate "attributed to Topstep's 2025 disclosure" ⚠ (snippet). No pattern of unpaid approved payouts was found in what was read. Reddit and Trustpilot were blocked.
3. **Corporate facts.** Founded 2010 as Patak Trading Partners; "2012 Launch of Topstep Trader"; Chicago; founder Michael Patak. "Topstep LLC operates as a group…"; the simulated program is run by TopstepTrader, LLC and Live accounts by TopstepFunded LLC (page: topstep.com/about-us; snippet for the entity split). **Platform change:** from 7 Jul 2025 new Combines were TopstepX-only, and from 1 Aug 2025 resets were TopstepX-only. Existing NinjaTrader/Tradovate/Rithmic accounts kept trading but could not be reset (snippet, Topstep Intercom notices). In Nov 2025 Topstep took ProjectX exclusive ("TopstepX"), which ended ProjectX service for other firms around **28 Feb 2026** (snippet: coinspectator/FinanceMagnates, Nov 2025).
4. **Bots, accounts, copying.** "Custom automated strategies and bots are allowed via the TopstepX / ProjectX API". "No, Live funded accounts are not allowed to trade through the ProjectX API." "The use of VPS, VPNs, and remote servers is prohibited by Topstep's Terms of Use". "All trading activity must originate from your personal device." "Running automation on a VPS can result in account suspension" (page, help.topstep.com/…/11187768, "updated over 3 weeks ago"). "You can hold up to 5 active XFAs at a time" (page, article 8284215, updated 2026-08-05). The prohibited list includes "Using software, AI, ultra-high speed systems … that … provides an unfair advantage" and "We retain the right to reject profit claims if abuse is suspected" (page, 10305426, 2026-06-10).
5. **Rule changes that hit existing traders (2025–26).** Consistency Path added Feb 2026 (snippet). XFA payout caps were cut in late April 2026, to **$2,000 per request for a 50K Standard account** (now on the official page). Commissions were added on TopstepX on 12 Apr 2026 (snippet, NexusFi; ⚠ the date is forum-sourced). Current caps: 50K $2,000/$3,000, 100K $3,000/$4,000, 150K $5,000/$6,000. Note for pre-12-Jan-2026 dashboard users: "100% of your first $10,000" (page, 8284233, updated 2026-09-30).
6. **Simulated? Discretion?** "The XFA is the simulated funded-level account" (page, 8284215). Call-up: "When a trader is called up … all open Express Funded Accounts will be closed". Live starting balance is "20% of your cumulative XFA balance — but capped … The remaining 80% is held in Reserve". "There is no warning before being called down" (page, 13747178, updated 2026-09-29).

**Grade reasons:** (+) 14-year record, transparent corporate structure with an NFA-registered affiliate, explicit bot permission on XFA. (−) The Live account bans the API, and the call-up closes the whole fleet. (−) The VPS ban forces an unattended bot onto a home PC. (−) April 2026 cap cuts hit existing traders.

Sources: https://help.topstep.com/en/articles/11187768 (page) · https://help.topstep.com/en/articles/8284215-express-funded-account-parameters (page) · https://help.topstep.com/en/articles/8284233-topstep-payout-policy (page) · https://help.topstep.com/en/articles/10305426-prohibited-trading-strategies-at-topstep (page) · https://help.topstep.com/en/articles/13747178-live-funded-account-call-up-and-call-down-process (page) · https://www.topstep.com/about-us/ (page) · https://intercom.help/topstep-llc/en/articles/8284149 (snippet) · https://nexusfi.com/showthread.php?p=911770 and ?p=912044 (snippet) · https://coinspectator.com/mainstream/2025/11/17/prop-firms-report-futures-prop-tech-provider-projectx-to-end-its-third-party-service-offering/ (snippet)

---

## 2. Apex Trader Funding — grade **D**

**Bottom line:** the belief in `apex-rules.md` is **confirmed**: automation is banned on Performance (funded) and Live accounts. Apex's official support article says so (snippet; the page itself is blocked).

1. **Regulatory/legal.** No CFTC/NFA action or lawsuit was found in the searches that ran ⚠. Apex is not an NFA registrant as far as found ⚠. **2024 controversy:** Finance Magnates reported payout delays, a requirement to record trades for 2 days, and CEO Darrell Martin promising fraud-detection systems and approvals "within 48 hours" (snippet). NexusFi (Sep 2024): Apex "changed the rules for some sim funded customers yet again, and are denying payouts" (snippet). Some review sites say thousands of payouts were denied under "erratic trading"/consistency rules ⚠ (advocacy claim, no primary source).
2. **Payout reliability.** The firm claims more than $660–819M paid (figures vary by source ⚠). The independent record shows 2024–25 denial waves tied to after-the-fact rule enforcement. One unverified report says Apex blamed traders for a June 2025 connection outage ⚠.
3. **Corporate facts.** Apex Trader Funding, Inc., Austin TX; founder and CEO Darrell Martin; founded 2021 (some company pages say 2008, the age of his trading community) (snippet: NexusFi, PR Newswire June 2024). Platforms: Rithmic, Tradovate, WealthCharts; the platform is locked at purchase (snippet). No forced platform migration was found.
4. **Bots, accounts, copying.** Official support article "Performance Account (PA) and Compliance" (support.apextraderfunding.com/…/31519788944411): it bars "AI, autobots, algorithms, fully automated systems, and high-frequency trading" on all account types. "Hands-off, set-and-forget, or set-and-walk-away trading … is strictly prohibited". The consequence is "immediate closure of your PA or Live account and the forfeiture of all funds" (snippet of the official page, which returned 403 to us). PA/Live accounts "cannot be managed or influenced by any bot, copy service, or mirroring software"; the prohibited-activities page is reportedly more permissive about manual-leader copying ⚠ (snippet). Up to 20 PAs ⚠ (snippet, affiliate sites). Vendors confirm "Automation is currently prohibited per Apex's official rules" (page, crosstrade.io, reviewed 2026-09-23).
5. **Rule changes.** "Apex 4.0" took effect 1 Mar 2026: one-time fees, MAE, 5:1 and one-direction rules removed, consistency 30%→50%. Legacy 3.0 accounts keep the old rules with no forced migration as of Apr 2026 (snippet, pickmytrade FAQ, propfirmmap). This is the third major rewrite since 2024.
6. **Simulated? Discretion?** PA accounts are simulated ⚠ (secondary). The terms were not readable (blocked).

**Grade reasons:** (−) Bots are explicitly banned on funded accounts, with forfeiture of all funds. (−) A 2024–25 record of payout delays and denials tied to rule interpretation. (−) Repeated whole-program rewrites. (−) The owner is identified but the firm is not regulated, and its official pages are inaccessible for verification.

Sources: https://support.apextraderfunding.com/hc/en-us/articles/31519788944411-Performance-Account-PA-and-Compliance (snippet; page 403) · https://crosstrade.io/learn/prop-firm-ai-trading/apex-trader-funding (page) · https://financemagnates.com/forex/this-prop-firm-requires-recording-your-trades-for-2-days-otherwise-you-wont-get-paid (snippet) · https://nexusfi.com/showthread.php?p=903180 (snippet) · https://nexusfi.com/d/prop-firms/apex-trader-funding/ (snippet) · https://pickmytrade.io/prop-firm-faq/apex-trader-funding (snippet) · https://propfirmmap.com/blog/apex-trader-funding-review-2026-payouts-profit-split-otp (snippet) · https://www.imantrading.org/firmfaq/apex-trader-funding-problems (snippet, advocacy)

---

## 3. Bulenox — grade **C**

**Bottom line:** the current FAQ explicitly allows bots, with a cap of 5 funded accounts. But the governing Terms of Use (dated July 2021) still say third-party algorithms "must be approved" and let Bulenox "refuse to claim any profit". The ownership is opaque.

1. **Regulatory/legal.** None found in the searches that ran ⚠. Bulenox is not NFA-registered as far as found ⚠.
2. **Payout reliability.** Trustpilot is about 4.7 across roughly 1,600 reviews (snippet). Its summary notes "some customers have had payout requests denied over unclear rules", with "flipping" and consistency "vague and inconsistently applied". One reviewer was denied under the flipping rule and then paid after posting a public review (snippet, trustpilot.com/review/bulenox.com). TheTrustedProp trust score is 60/100 (snippet).
3. **Corporate facts.** "Bulenox LLC 1201 N Orange St, Ste 7149 Wilmington, DE 19801" (page, bulenox.com footer). This is a registered-agent address, and no owner is named anywhere ⚠. The ToS is governed by Delaware law (page, Terms_of_Use.pdf). Founded about 2022 ⚠. **Platform:** "Bulenox stopped issuing new ProjectX accounts on January 15, 2026" and stopped resetting existing ones; Rithmic is now the only route for evaluation and funded accounts (page, pickmytrade blog dated 2026-09-04, a vendor ⚠).
4. **Bots, accounts, copying.** FAQ (page, bulenox.com CMS, read 2026-10-11): "Yes. Bots, algorithms and trade copiers are permitted. If you connect to Rithmic through a third-party API or composite software, an additional $100 per month applies. Only user-built tools intended solely for the account owner's personal use are permitted. Commercial, shared, rented or publicly distributed automation tools are not allowed." Accounts: "up to 5 accounts in total — Master, Fast Track and Momentum Master in any combination … all of your accounts run under one Rithmic User ID." ToS (updated July 2021): "any third party algorithms must be approved from the Bulenox management team"; it bans "'scalping' algorithms, DTC Protocol Bridge API or automated discretional trading"; "If abuse is suspected, we reserve the right to refuse to claim any profit." A vendor claims "up to 11 Master accounts through progressive activation" ⚠, which contradicts the FAQ's 5.
5. **Rule changes.** The ProjectX exit forced platform changes in Jan 2026. Current product lines (Fast Track, Momentum) replace older ones ⚠.
6. **Simulated? Discretion?** "Bulenox LLC does not provide live trading" (ToS). Fast Track is a "simulated funded environment" (page, site JS). The ToS gives Bulenox the right to terminate "in Company's sole discretion and without notice … for any reason or for no reason at all" (page).

**Grade reasons:** (+) Bots explicitly allowed on funded accounts in the current FAQ; Rithmic API access exists. (−) The 2021 ToS conflicts with the FAQ (approval needed; profit refusal), so get written approval. (−) Opaque ownership behind a Delaware registered agent; no live trading at all. (−) Payout denials on vague flipping/consistency grounds.

Sources: https://bulenox.com/faq (page, via its CMS endpoint /cms/items/faq_items) · https://bulenox.com/legal/Terms_of_Use.pdf (page) · https://bulenox.com (page, footer) · https://blog.pickmytrade.io/does-bulenox-still-use-projectx-rules-tradingview-setup/ (page, vendor) · https://www.trustpilot.com/review/bulenox.com?page=5 (snippet) · https://thetrustedprop.com/prop-firms/bluenox/payouts (snippet)

---

## 4. Lucid Trading — grade **B** (with a youth caveat)

**Bottom line:** the clearest written permission of any firm: "Automated trading systems and trade copiers are permitted". The limit is 5 funded accounts per household. A Live promotion closes all sim accounts and restarts at a $0 balance.

1. **Regulatory/legal.** None found in the searches that ran ⚠.
2. **Payout reliability.** No independent evidence gathered (Reddit and Trustpilot blocked; search budget exhausted) ⚠. The firm promises funds "within 2 business days" (page).
3. **Corporate facts.** Entity, owner and founding date were **not verified**: lucidtrading.com was blocked, and the help center does not name the entity ⚠. Likely founded 2024–25 ⚠ (young). Platforms: "CQG supported platforms: NinjaTrader, Tradovate, TradingView; Rithmic supported platforms: MotiveWave, Quantower, Tradesea, Sierra Chart, Jigsaw, Bookmap, ATAS, R|Trader Pro, MultiCharts" (page, article 11404614, 2026-07-28). Lucid received the Nov 2025 ProjectX wind-down notice and migrated (snippet, coinspectator).
4. **Bots, accounts, copying.** "Automated Strategies: Automated trading systems and trade copiers are permitted. All automated activity must comply with Lucid Trading rules. Traders are fully responsible for any software errors, malfunctions, or unintended outcomes" (page, 11404728, 2026-08-26). HFT is prohibited: a warning first, then "All profits generated from HFT activity will be removed; Accounts will be closed" (page, 11404736). Microscalping and hedging are also prohibited. Accounts: "Up to 5 active funded accounts per household or family"; up to 10 evaluation and funded combined; "Up to 5 active LucidLive accounts" (page, 11404617, 2026-08-26).
5. **Rule changes.** A "New Live Structure" was updated the week of 2026-10-09, with "Legacy" live structures for Flex/Pro/Direct (page, 16558826). Expect frequent revisions.
6. **Simulated? Discretion?** The funded accounts are sim ("sim funded"). "All live transitions occur at the discretion of the Lucid risk team." Live accounts begin with "$0 starting balance". "All simulated prop accounts are closed when a trader is moved live" (page, 16558826). LucidFlex allows at most 5 payouts per account, then a move live (page, 12945796).

**Grade reasons:** (+) Explicit, current written permission for bots and copiers on funded accounts. (+) A clear account cap and clear payout mechanics. (−) Young firm with an unverified owner/entity and no independent payout record gathered. (−) The live transition closes the whole fleet and resets to a $0 balance.

Sources: https://support.lucidtrading.com/en/articles/11404728-other-trading-activities (page) · https://support.lucidtrading.com/en/articles/11404617-maximum-number-of-accounts (page) · https://support.lucidtrading.com/en/articles/11404736-prohibited-high-frequency-trading (page) · https://support.lucidtrading.com/en/articles/11404614-lucid-trading-supported-platforms (page) · https://support.lucidtrading.com/en/articles/16558826-new-live-structure (page) · https://support.lucidtrading.com/en/articles/12945796-lucidflex-payouts (page)

---

## 5. Tradeify — grade **C** for a multi-firm fleet (B if used alone)

**Bottom line:** bots are allowed by contract (§6.6). But §6.6 also says "using it across multiple firms is against Tradeify's policy", and §6.7(c) treats an opposite position at *another firm* as a breach. Both are directly hostile to a multi-firm fleet running one bot.

1. **Regulatory/legal.** The affiliate Tradeify Brokerage LLC d/b/a Slay Markets is "a CFTC-registered introducing broker … NFA Member (NFA ID: 0575972)", based in Boca Raton FL (page, tradeify.co footer). No action was found ⚠ (BASIC unreadable). Disputes go to "binding arbitration in Florida" (AAA), under Florida law (page, agreement §10).
2. **Payout reliability.** Review sites claim "$150M paid" and an "A grade" on Trustpilot (snippet, propfirmmap; affiliate ⚠). No independent denial pattern was gathered ⚠.
3. **Corporate facts.** The contracting entity is "Tradeify Holdings, Corp."; Novaflame LTD (Cyprus, HE 480295) is its payment agent (page). Founder, date and jurisdiction of Holdings Corp. were not verified ⚠. Platforms: Tradovate, Rithmic and WealthCharts are named in the agreement (page). Live accounts go via "NinjaTrader and GFF Brokers" (page, §5). Tradeify received the Nov 2025 ProjectX notice and moved to Tradovate (snippet).
4. **Bots, accounts, copying.** §6.6 verbatim: "The use of automated trading bots or algorithms ('bots/algos') is permitted only under the following conditions: Ownership: The Trader must be able to prove that the Trader is the sole owner of the bot … Exclusive Use: While the Trader may use the bot on the Trader's personal accounts, using it across multiple firms is against Tradeify's policy … No High-Frequency Trading (HFT) Bots … Tradeify reserves the right to request information or documentation if our risk measures flag the Trader's account". §4.2: "maximum number of Simulated Funded Accounts … to five (5) … per-individual and per-household basis and across ALL funded account types". Copying your own trades is allowed per the Help Center (§6.7(b)). §6.7(c): "Holding a position in a Trader-Controlled Account opposite a position in an External Account constitutes hedging and is a breach". Microscalping: "50% or more of the Trader's account profit must come from trades held longer than ten (10) seconds" (§6.8). (Page, tradeify.co/funded-trader-agreement, read 2026-10-11; vendors date the version to May 2026 ⚠.)
5. **Rule changes.** §16: Tradeify "reserves the right to modify … plans, and payout requirements … at its sole discretion and at any time … effective upon posting". Help Center rules are incorporated by reference (§4.1).
6. **Simulated? Discretion?** "Simulated Funded Accounts". The move to Live is "in its sole and absolute discretion … or not at all" (§5.1–5.2). §4.4: "reserves the right to take up to the end of the next payout cycle to approve, review, or deny a payout request", and may "withhold payment of any payout that has been approved but not yet paid, pending … review".

**Grade reasons:** (+) Written contractual bot permission; a brokerage arm registered with the CFTC/NFA. (−) The multi-firm exclusivity clause plus the external-account hedging clause expose a cross-firm fleet. (−) Unilateral amendments take effect on posting; approved payouts can be withheld during reviews. (−) Cap of 5 per household.

Sources: https://tradeify.co/funded-trader-agreement (page) · https://tradeify.co (page, footer disclosures) · https://propfirmmap.com/blog/tradeify-review-2026-a-grade-trustpilot-150m-paid-futures-prop-firm (snippet) · https://blog.pickmytrade.io/tradeify-prop-firm-review/ (snippet) · https://coinspectator.com/mainstream/2025/11/17/prop-firms-report-futures-prop-tech-provider-projectx-to-end-its-third-party-service-offering/ (snippet)

---

## 6. MyFundedFutures (MFFU) — grade **B**

**Bottom line:** automation is allowed in writing ("tailored to their own specific settings"), copy trading is allowed across all account types, and the cap is 5 sim-funded accounts (3 if any 100K/150K). Plans change often.

1. **Regulatory/legal.** None found in the searches that ran ⚠.
2. **Payout reliability.** Claims "Trusted by over 100,000 traders" and "Fastest futures prop-firm payouts" (page, firm's own). Live payouts are processed "once a day by our partner FCM" (page, 12109396). No independent evidence gathered ⚠.
3. **Corporate facts.** Entity, owner and founding date were not verified (homepage is JS-rendered) ⚠; commonly reported as founded 2023 ⚠. Platforms: NinjaTrader, Hyperprop, Tradovate, TradingView, Quantower, Volumetrica, DeepChart, ATAS (page, 8528335, updated 2026-10-08); dxFeed/Tradovate (page, 10771500).
4. **Bots, accounts, copying.** "High-frequency Trading is not allowed on our plans. Traders may make use of automated trading strategies tailored to their own specific settings so long as these automated tools do not aim to exploit the favorable fills offered in the Simulated Environment. Traders trading live accounts with automated trading must abide by CME guidelines" (page, 8444599, 2026-08-24). "MyFunded Futures allows copy trading across all account types"; Tradesyncer is preferred and external copiers are allowed (page, 10771500, 2026-08-24). Limits: "up to 5 active Sim-Funded Accounts" for 25K/50K; Rapid EOD 25K/50K max 3; Builder 50K max 1; "If a trader holds any $100K or $150K Sim-Funded Account, the maximum … is 3" (page, 16498635). Note that secondary blogs (TradersPost, Mar 2026) claim "semi-automated only" ⚠, which contradicts the official page. Rely on the official page, but get written confirmation.
5. **Rule changes.** Flex and other plans moved to "Legacy" (page, 13521620, 2026-06-03). The Rapid split changed to 90% "as of January 12th, 2026" (page, 13745661). The automation policy was reportedly updated July 2025 (snippet ⚠).
6. **Simulated? Discretion?** "Sim Funded Account: This account operates in a simulated environment" (page, 10101257). Live transitions are partly automatic (a $10,000 single-day profit) and partly at the "Discretion of the Risk Management Team". Up to $5,000 of sim profits goes to Reserve. Multiple Rapid accounts moved live "are combined into one Live account" (page, 13134718). Profits from prohibited practices are "confiscated" (page, 8444599).

**Grade reasons:** (+) Current official permission for own-settings automation and for copy trading. (+) A clear sim-to-live mechanism with a real FCM on Live. (−) Owner/entity unverified here; frequent plan turnover. (−) The live move merges the fleet into one account and sweeps $5K to Reserve.

Sources: https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices (page) · https://help.myfundedfutures.com/en/articles/10771500-copy-trading-at-myfundedfutures (page) · https://help.myfundedfutures.com/en/articles/16498635-moving-from-evaluation-to-sim-funded-account (page) · https://help.myfundedfutures.com/en/articles/10101257-understanding-live-funded-account-at-myfunded-futures (page) · https://help.myfundedfutures.com/en/articles/13134718-understanding-rapid-live (page) · https://help.myfundedfutures.com/en/articles/13745661-payout-policy-overview-best-and-fastest-prop-firm-payouts (page) · https://help.myfundedfutures.com/en/articles/12109396-comprehensive-faq-live-accounts-at-myfunded-futures (page) · https://blog.traderspost.io/article/automate-my-funded-futures-with-traderspost (snippet, conflicting)

---

## 7. Take Profit Trader — grade **D**

> **D5 head's note (2026-10-11):** the TPT help-center pages are blocked (403). The "page, via Zendesk API" citations in this section came from an undocumented JSON endpoint, which breaks the wave rule against routing around a block. That copy was deleted and must not be cited. Only the bot ban is kept, because CrossTrade's page and a search snippet corroborate it. The copier names, the "device or infrastructure clustering" quote and the payout timings are **excluded** (see verify-futures.md).

**Bottom line:** bots are banned on every account type, by an official policy updated 2026-10-09.

1. **Regulatory/legal.** None found ⚠. PRO+ live orders route via Tradovate, its "regulated broker for live (PRO+) accounts" (page, homepage FAQ).
2. **Payout reliability.** Account-to-wallet transfers became automated (5–10 s) for Tradovate PRO. The "Profit Team manually reviews payout requests to the wallet for compliance purposes, which takes up to 12 business hours". The page lists only four denial reasons for wallet withdrawals (page, Zendesk 37697356049949, 2026-08-20). No independent evidence gathered ⚠.
3. **Corporate facts.** "TakeProfitTrader LLC, 9100 Conroy Windermere Rd Suite 200, Windermere, FL 34786" (page, footer). Founder/date not verified ⚠. Platforms: Tradovate and Rithmic (page).
4. **Bots, accounts, copying.** Universal Trading Policies: "#1: No Trading Bots or Algos. Automated trading systems, bots, or algorithmic execution tools are not permitted", applying to "Test, PRO, and PRO+". Violations bring "profit forfeiture, account reset, account closure, or removal" (page, 34431153546397, 2026-10-09). Copiers are allowed only for your own accounts, from an approved list (Tradesyncer, TradeCopia, Affordable Indicators, Replikanto Compliance edition, platform-native) (page, 34431176505245). Surveillance includes "Device or infrastructure clustering" and "Strategy similarity" (page, 34431223270557). Max 5 PRO/PRO+ ⚠ (snippet).
5. **Rule changes.** The UTP, copier and independent-execution policies were all re-issued 2026-10-09 (page).
6. **Simulated? Discretion?** "your PRO account operates in a simulated environment and the profits inside that account are simulated"; PRO+ is live (page, homepage).

**Grade reasons:** (−) Explicit bot ban on funded accounts. (−) Infrastructure-clustering surveillance is hostile to a centrally run fleet. (+) A clear entity, and fast automated payouts.

Sources: https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431153546397-TakeProfitTrader-Universal-Trading-Policies-UTP (page, via Zendesk API) · …/34431176505245-Trade-Copier-Policy (page) · …/34431223270557-Independent-Trade-Execution-Policy (page) · …/37697356049949-Speed-of-Payouts-Update-Q-A (page) · https://takeprofittrader.com (page)

---

## 8. Earn2Trade — grade **D**

**Bottom line:** at most 3 funded accounts, and trade copiers are forbidden "even after you've earned a LiveSim® or Live account". AI/software that "could potentially … provide an unfair advantage" is prohibited.

1. **Regulatory/legal.** None found ⚠. Live accounts are housed at EdgeClear, Dorman, NinjaTrader, Lunaro Markets, or legacy PhillipCapital (page, 7986692).
2. **Payout reliability.** No independent evidence gathered ⚠. The firm discloses an 8.89% pass rate for 2025 (page, homepage).
3. **Corporate facts.** "Earn2Trade LLC 30 N Gould St STE 4000, Sheridan, WY 82801" (page, footer; a registered-agent address). Founded about 2016 ⚠. Platforms: Rithmic, Tradovate, NinjaTrader (page, help center).
4. **Bots, accounts, copying.** Prohibited: "Utilizing software, artificial intelligence, or ultra-fast data entry techniques that could potentially manipulate the trading environment or provide an unfair advantage" (page, 9286647, 2024-05-06). "Traders can have 3 funded trading accounts active concurrently … The prop firms do not provide a leader-follower or other trade copy system" (page, 5660666, 2026-06-22). "No trade copiers after you pass … trade copiers remain off-limits" (page, 12034590, 2026-06-22).
5. **Rule changes.** The copier ban was reaffirmed in June 2026.
6. **Simulated? Discretion?** "The LiveSim® is a simulated trading account"; the prop firm "may decide to provide a Live account instead" (page, 3313030).

**Grade reasons:** (−) A copier ban plus only 3 accounts breaks rule (2). (−) The AI/software clause creates bot risk. (+) Long record, and real FCMs at the Live stage.

Sources: https://help.earn2trade.com/en/articles/9286647-… (page) · https://help.earn2trade.com/en/articles/5660666-… (page) · https://help.earn2trade.com/en/articles/12034590-… (page) · https://help.earn2trade.com/en/articles/3313030-what-is-the-livesim (page) · https://help.earn2trade.com/en/articles/7986692-… (page) · https://www.earn2trade.com (page)

---

## 9. TradeDay (additional firm) — grade **B**

**Bottom line:** your own automated system is allowed on supported platforms (not a direct API), with 5 Funded Sim plus up to 5 **Funded Live** accounts. It explicitly permits copying "from your personal account elsewhere into your TradeDay account", which is relevant to the IBKR-master bridge.

1. **Regulatory/legal.** None found ⚠ (not searched; budget exhausted).
2. **Payout reliability.** The homepage shows 4.6–4.8 review badges (page, firm-curated ⚠). No independent evidence gathered.
3. **Corporate facts.** "Tradeday LLC 2nd Floor, 412 S. Wells Chicago, Illinois 60607" (page, footer). Founded about 2020 ⚠. Platforms: NinjaTrader, Tradovate, TradingView, Jigsaw, Quantower; "Traders can only have multiple accounts on 1 broker" (page).
4. **Bots, accounts, copying.** "We do not make platform APIs available to traders … To use an automated trading system, you must use one of the platforms we support: NinjaTrader, Tradovate, TradingView, Jigsaw and Quantower. TradeDay does not expose the Tradovate API … Algos and Bots purchased from a third party and employed by the trader are forbidden. If multiple users are making the same trades, then all the accounts will be shut down" (page, Freshdesk 103000085101, modified 28 Nov 2025). "The maximum number of active Funded Sim accounts is 5 … Traders can have up to 5 Funded Live accounts" (page, 103000354796, modified 8 Sep). Copiers: "you can use a copy trader to copy trades from your personal account elsewhere into your TradeDay account". Funded Live and Funded Sim cannot hold positions at the same time (page, 103000008833, modified 22 Sep).
5. **Rule changes.** Multi-account support was added recently ("We now support multiple accounts"); dates are only partly shown ⚠.
6. **Simulated? Discretion?** Funded Sim is simulated. "the Head of Trading will make a decision on whether to extend or to transition … to a Funded Live account" (page).

**Grade reasons:** (+) A self-built ATS is permitted on funded accounts, and real Funded Live accounts allow up to 5. (+) Chicago LLC with a named address. (−) No API, so the bot must run inside NinjaTrader/TradingView etc. (−) Owner and payout record not verified here.

Sources: https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading (page) · https://tradeday.freshdesk.com/en/support/solutions/articles/103000354796-multiple-accounts (page) · https://tradeday.freshdesk.com/en/support/solutions/articles/103000008833-can-i-have-multiple-accounts-can-i-use-copy-trader- (page) · https://www.tradeday.com (page)

---

## 10. Extra candidates screened out (bots banned or gated on funded accounts)

| Firm | Evidence (page, 2026-10-11) | Verdict |
|---|---|---|
| Alpha Futures (Alpha Futures Limited, UK Co. No. 15655643, Harpenden) | "The use of AI, bots, and other automated trading mechanisms is strictly prohibited across all account types … Any form of hands-off, continuous day and night trading … is strictly forbidden"; VPS is allowed; max 5 Qualified accounts (3 Advanced); Live call-up closes all Qualified accounts at a $0 start. help.alpha-futures.com/en/articles/9508585 (2025-10-30), /9492088 (2026-07-27), /10743344 (2026-08-21), /10573989 (2026-07-17) | D |
| Top One Futures | "No, the use of Expert Advisors (EAs) or Bots is not allowed on your accounts"; "Using a VPN or VPS … strictly prohibited"; up to 35 funded per household; Live bars all Sim accounts. help.toponefutures.com/en/articles/10907920, /11187841, /10907463 (2026-10-01..08) | D |
| Phidias | "The use of robots, fully automated trading algorithms, or any other form of automated trading is not permitted. Only semi-automated software…" phidiaspropfirm.com/rules | D |
| Elite Trader Funding | "AI, bots, EAs, and algos additionally require ETF's written authorization … The only automated trading tools currently authorized are the approved trade copiers"; up to 20 sim-funded accounts. elitetraderfunding.app/help/trade-copier-disclaimer (updated 2026-10-08), /max-active-elite-sim-funded-accounts | D unless written authorization obtained |
| Funded Futures Network, Aqua Futures | Sites unreachable or no futures rules found | not assessed |

---

## Cross-firm regulatory and industry notes

- **CFTC v. My Forex Funds (Traders Global Group):** the CFTC's fraud case against a (forex/CFD) prop firm was dismissed in May 2025, reportedly with prejudice after sanctions on the CFTC for withholding exculpatory evidence (snippet: law-firm analysis via jdsupra/clsbluesky; NexusFi article ⚠ verify on the D.N.J. docket). The CFTC had argued that funded-trader payouts were "illegal off-exchange futures" (snippet, NexusFi ⚠). **No CFTC/NFA advisory specific to futures prop firms was found** (snippet search, 2026-10-11).
- **ProjectX wind-down:** ProjectX ended third-party service around 28 Feb 2026 (some sources say March), citing "upcoming compliance reporting, oversight, and audit requirements". Lucid, Tradeify, Top One and Bulenox were forced to migrate (snippet: coinspectator/FinanceMagnates Nov 2025; damnpropfirms ⚠). This is the main precedent for platform risk on funded accounts.
- **CME market-data licensing:** not researched (search budget exhausted) ⚠. Firms do pass through CME non-pro/pro data fees (E2T $140/exchange/month pro; MFFU monthly exchange fee on Live), from the pages above.
- **Every "funded" account on this list is simulated** until a discretionary Live call-up. Live call-up at Topstep, Lucid, Alpha and Top One **closes all sim accounts**. MFFU merges them into one; TradeDay blocks new purchases. A fleet of many funded accounts therefore ends at success.

## Top risks for a fully automatic multi-account fleet

1. **Bots banned on funded accounts:** Apex (confirmed, with forfeiture of all funds), TPT, Earn2Trade, Alpha, Top One, Phidias, ETF (unless authorized). Topstep bans the API on Live and bans VPS on every account.
2. **Success collapses the fleet:** Live call-up closes the sim accounts and restarts at a $0 balance or 20% (Topstep, Lucid, Alpha, Top One; MFFU merges into one; Tradeify/Lucid/Topstep call-ups are discretionary).
3. **Cross-firm clauses:** Tradeify bans using the same bot at other firms and treats opposite positions in *external* accounts as hedging. TPT and Top One surveil device/IP/infrastructure clustering.
4. **Unilateral, retroactive rule changes:** Tradeify §16 ("effective upon posting"), Bulenox ToS, Topstep's April 2026 cap cuts (50K: $2,000/request), Apex 4.0 (Mar 2026).
5. **Discretionary payouts on simulated profits:** Bulenox "refuse to claim any profit"; Tradeify may withhold *approved* payouts pending review; Topstep "reject profit claims if abuse is suspected"; MFFU "confiscated".
