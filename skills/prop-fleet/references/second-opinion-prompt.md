# Second-opinion prompt — for another model to audit this engagement

Written 29/09/2026 at Itamar's request ("give me the perfect prompt for ChatGPT").
Everything below is factual as of that date and matches the documents in this
skill. No secrets, no account numbers, no keys. Answer language: Hebrew.

---

```text
ROLE
You are a senior quantitative portfolio manager and prop-trading risk officer
with 20+ years across systematic futures, market microstructure and retail
prop-firm structures. You are blunt, evidence-first, and you never quote a
return without its drawdown and its sample size. You cite sources. You
distinguish peer-reviewed evidence from SSRN working papers from marketing.

TASK
Audit the research below and answer ONE question: is there a strategy or
structure I have missed that can plausibly deliver ≥20%/year net of all costs
and Israeli tax, WITHOUT personal margin loans and WITHOUT a peak-to-trough
drawdown worse than about −15%, using the tools of a private individual with
a Mac, an IBKR account, a Python trading bot and a US futures prop-firm
account? If the answer is "no such thing exists", say so and explain the
trade-off that makes it impossible. If the answer is "yes, here", give the
evidence with numbers, and what would falsify it.

MY SITUATION
- Israeli tax resident. Capital gains 25% on real gains, at realization.
  Prop-firm payouts are ordinary income. "Buy-borrow-die" does not apply.
- Goal as originally stated: buy one Apex Trader Funding 50K evaluation,
  pass it, add one funded account per month up to 10–20, earn >20%/year on
  the total, extract 25%/year to private investments plus 25% to businesses
  and real estate from year 4, over 8 years.
- Apex rules I verified: 50K account, $2,500 trailing drawdown that trails
  intraday peak until the balance reaches +$2,600, then locks at +$100;
  evaluation target +$3,000; evaluation has a hard 30-calendar-day expiry
  (~21 trading days); futures only; intraday; consistency and max-contract
  rules apply. Monthly fee ~$150–170 per evaluation.
- Tools: a Python bot trading ES on an intraday "smart money" strategy
  (fair-value gaps, break of structure, kill zones, graded setups, min
  reward:risk 1.7). Paper-trading now against IBKR. It is a 1-trade-per-day
  bot because of an old cash-account T+1 rule that does not apply to
  futures.

WHAT I HAVE ALREADY TESTED — WITH RESULTS
1. The bot's own strategy, three independent tests:
   a. 10-year backtest: deflated Sharpe ratio 0.005 (i.e., indistinguishable
      from zero after correcting for the number of trials). Disarmed.
   b. Live replay of recorded setups: expectancy +0.101R per trade, 95%
      interval [−0.197R, +0.398R]. Inside noise.
   c. 100 parameter hypotheses with Bonferroni correction: 0 survive.
   The strategy was also tuned in-sample (min R:R lowered 2.0→1.7 and a
   lower setup grade admitted after the backtest).
2. Financial model of the Apex structure at the measured expectancy,
   n=600 trades/year, risk 4% of drawdown per trade in funded accounts,
   10% in evaluations, 25% tax, averaged over years 5–8:
   −0.197R → −2.0%/yr; +0.101R → +5.7%/yr; +0.250R → +19.9%/yr;
   +0.398R → +33.6%/yr. So the target needs a true edge of ≈+0.25R/trade.
   Decomposition: theoretical $151,500 → $81,597 actually withdrawn (54%,
   the rest lost to blown accounts and payout rules) → −2% fees → −13% tax
   → $58,179 net (38% of theoretical).
   Throughput: 1 trade/day −0.1%/yr, 2/day 3.6%, 3/day 5.8%, 4/day 7.7%,
   6/day 11.5% — at the measured +0.101R.
3. Discretionary trading on news, influencers and macro at daily-to-monthly
   horizons, researched and rejected: Barber & Odean 2000 (66,465
   households, most active earned 11.4% vs market 17.9%); Kakhbod et al.
   (SSRN 4428232, finfluencers: 56% anti-skilled, −2.3%/month); SPIVA
   persistence (1 of 169 top-quartile 2021 funds stayed top-quartile 4
   years); earnings news priced in milliseconds, post-earnings drift gone
   from non-microcaps since ~2006 (peer-reviewed).
4. Margin loans against the portfolio + Israeli real estate: IBKR margin
   5.12% tier-1, liquidation at 25% maintenance with no call; Israeli
   second-home purchase tax 8% from the first shekel (to 31.12.2026),
   50% max LTV on investment mortgages, mortgage ~4.8%, rental yield 2–5%,
   rental tax 10% flat or exemption to ₪5,654/month. The numbers do not
   close at 20%.
5. Time-series momentum (Moskowitz, Ooi & Pedersen 2012), a priori
   parameters (12-month sign, 60-day vol scaling to 10%, monthly rebalance,
   10 bps per unit turnover), stationary block bootstrap n=5000:
   a. 54 futures 1984–2016 (paper's replication data): long/short Sharpe
      1.17, bootstrap 5th percentile 0.82, all 5 lookbacks positive, all 4
      asset classes positive, max drawdown −6.9% at 3% vol, correlation
      to S&P −0.15. Scaled to 10% vol: +11.7%/yr, −21.6% DD. To 20% vol:
      +23.4%/yr, −39.6% DD, 6.7× leverage. Sub-period 2010–2016 Sharpe
      0.46.
   b. Nine investable ETF-priced asset classes 1991–2026 (SPY, VT, SHY,
      IEF, TLT, BND/BWX, GLD, DBC): long-only, no leverage: +4.5% to
      +5.2%/yr, Sharpe 1.0–1.3, 5th pct 0.8–1.06, DD −5.6% to −9.4%, with
      ~51% of the book in SHY. At 10% vol (2–3× margin): +10.6% to
      +13.1%, DD −16% to −19%. Long/short Sharpe 0.66–1.05. Out-of-sample
      11/2016–9/2026: long-only Sharpe 0.86 vs 60/40 buy-and-hold 0.92
      (+10.1%/yr). Decade Sharpes falling: 1.6 → 1.2 → 0.6 → 0.7.
   c. Prop fit: the daily return stream through a 50K/$2,500-trailing
      account, 21-trading-day horizon: at $100/day vol 0% pass; $300/day
      5% pass, 8% blow, 87% expire; $500/day 23%/24%/53%. Trend-following
      cannot pass a 21-day evaluation at any sane size. Structural
      mismatch, not a strategy failure.

WHAT I HAVE NOT TESTED (my own known gaps — start here)
- Published intraday strategies on ES/SPY that would fit the prop
  structure: Gao, Han, Li & Zhou 2018 JFE (first-half-hour predicts
  last-half-hour); Zarattini, Barbon & Aziz 2024 SSRN "Beat the Market"
  intraday momentum (claims 19.6%/yr, Sharpe 1.33, DD −20% with up to
  4× intra-contract sizing); Zarattini & Aziz 2023 SSRN opening-range
  breakout on QQQ. I have not replicated any of them and I know the SSRN
  ones are contested post-publication.
- Short-volatility / option-premium strategies (I assume tail risk and
  margin make them fail the drawdown constraint, but I did not run it).
- Multi-factor combinations (value + momentum + carry + quality) at the
  portfolio level.
- Anything involving the prop firm's rules that they prohibit (hedging
  the same trade across two firms' accounts, copy-trading) — I consider
  this rule-breaking and off the table; say so if you agree, and say why
  if you do not.

RULES FOR YOUR ANSWER
1. Every return claim must come with: drawdown, sample length, Sharpe or
   equivalent, whether it is peer-reviewed / SSRN / vendor-claimed, and
   the leverage embedded.
2. Separate three buckets explicitly: (A) things I tested wrongly or
   misread — with what the right number is; (B) things I did not test
   that have credible evidence — with the evidence; (C) things that sound
   good but fail my constraints — with the constraint they fail.
3. Give lower bounds, not point estimates, wherever you can. If a
   strategy's 5th percentile Sharpe is not known, say "unknown".
4. Do not propose anything that breaks a prop firm's terms, a broker's
   terms, or Israeli tax law. Name the rule if you decline something.
5. If the honest answer is that 20%/yr with ≤−15% drawdown and no
   personal leverage does not exist for a private individual in liquid
   markets, say it in the first sentence and then explain the
   return/drawdown trade-off with numbers. Do not pad.
6. End with: the single next experiment you would run, what data it
   needs, and what result would make you change your mind either way.
7. Answer in Hebrew. Keep source names and tickers in English.
```
