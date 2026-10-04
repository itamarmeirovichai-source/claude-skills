# Board — shared state of the organization

*Every agent reads this first. The director rewrites it at the end of each day.*

## Where we stand (4 Oct 2026, day 0)

- **Edge:** none that passes the gate. Four tests of the bot's ICT/TJR-style
  strategy found zero gross edge (`references/tjr.md`). Trend-following has a
  real edge (Sharpe ~1) but cannot pass a 21-day evaluation
  (`references/trend-following.md`). Beat-the-Market intraday momentum: real
  2020–2024, Sharpe ≈ 0 since 2025 per an independent replication
  (`references/second-opinion-audit.md`).
- **Firms:** Apex likely forbids bots on funded accounts. Candidates that
  reportedly allow full automation: MyFundedFutures, Bulenox, Tradeify, Lucid,
  Topstep (Express, own computer). Unverified.
- **Data available here:** S&P minute bars 2010–2018 (FutureSharks, GitHub raw);
  54 futures daily 1984–2016; nine asset classes daily to Sep 2026; S&P daily
  open/close to Sep 2026. Most market-data hosts are blocked.
- **Required edge:** annual Sharpe ~3 intraday; about +0.25R per trade at one
  trade a day.

## Open questions

1. Which intraday edge families have not been tested yet?
2. Is there fresher intraday data reachable from GitHub (2019–2026)?
3. Which of the five candidate firms really allows full automation on funded
   accounts, at how many accounts, through which API?
