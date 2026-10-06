# Rules keeper, 2026-10-05: method, blocked hosts, changes that matter

Method: no firm page could be fetched. "verified" means a domain-restricted WebSearch (allowed_domains = the firm's own help-center domain) returned a summary attributed to that page. The search engine paraphrases, so these are snippets, not quotes. "corroborated" means a third-party site. Full table: rules_matrix.csv (54 rows, 6 firms x 9 fields).

Blocked today (curl through the proxy: "CONNECT tunnel failed, response 403"; WebFetch: EGRESS_BLOCKED):
help.myfundedfutures.com, bulenox.com, help.tradeify.co, lucidtrading.com, support.lucidtrading.com,
help.topstep.com, support.apextraderfunding.com, apextraderfunding.com, blog.traderspost.io, crosstrade.io

Changes that affect other divisions:
1. Topstep XFA 50K payout cap is $2,000 per request (Standard), not $5,000. The $5,000 is the 150K Standard cap
   (help.topstep.com/en/articles/8284233). daily/2026-10-04/economist_run.py sets Topstep cap=5_000.
2. MyFundedFutures 50K capacity is set per plan: at most 3 Rapid EOD 50K and 1 Builder 50K Sim-Funded accounts, not 5
   (help.myfundedfutures.com/en/articles/16498635). Rapid (non-EOD) funded uses an intraday trailing drawdown.
   One search result title marks Flex as "(Legacy)" (articles/13521620), which the economist's MFFU Flex 50K row may need to reflect. Unverified.
3. Tradeify Select Flex 50K: 50% of profit, capped at $2,500 per payout for accounts bought after 1 Sep 2026. The economist used Select Daily at $1,000.
4. Flat-by rule: Topstep 3:10 PM CT, Bulenox 3:59 PM CT, MFFU 4:10 PM ET, Tradeify 4:45 PM ET (all account types,
   Live included), Lucid sim accounts 4:45 PM ET (LucidLive may hold). No overnight holding is allowed on any funded sim account
   at the five non-Apex firms. Turn-of-the-month and the overnight sleeve are therefore ineligible there.
5. Automation conflicts still open: MFFU (firm text allows automated strategies; a TradersPost blog, via search summary,
   says fully autonomous bots without human oversight are prohibited). Bulenox now says third-party algorithms
   need management approval, but whether a self-built Rithmic-API program counts as "third-party" is not stated.
   Tradeify forbids using the same bot at other firms, which conflicts with a multi-firm fleet running one bot.
6. VPS: Topstep prohibits it. Tradeify allows it after a normal login, at the trader's own risk. No firm rule was found for MFFU, Bulenox or Lucid.
