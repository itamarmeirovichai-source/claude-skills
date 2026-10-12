# W3-F2: Is higher-volatility sizing real and safe?

**Verdict.**

- **Maximum safe volatility is 20% a year** at FTMO Swing 2-Step and at Crypto Fund Trader 2-Phase. It holds only with three things:
  - a bot that closes everything for the day at about 80% of the daily loss limit;
  - the same volatility on every copied account;
  - no rebalancing in the last 2 hours before a weekend or holiday close (FTMO).
- **30% breaks it** at both firms. The daily loss limit is then likely to be hit within a year, and the discretionary "overexposure / account rolling" clauses come into play.
- **Blue Guardian's funded 2-Step has no safe level between 12% and 30%.** Its Guardian Shield (−2% total open P&L; first hit cuts the split to 50%, second hit ends the account) needs roughly 8% or less.
- **Sharpe needed for $20k a year per $100k, after every stress** (the post-hoc decision row F2-12):

  | Firm | 20% vol | 15% | 12% |
  |---|---|---|---|
  | FTMO | **1.46** | 1.96 | 2.44 |
  | CFT | 1.66 | 2.09 | 2.54 |

  D1's "about 1.5 at 20%" survives at FTMO. The stresses move FTMO's dollars by only 2–6% at a 20% cap. **The contract, not fat tails, sets the ceiling.**
- **The Sharpe-0 "lottery" does not survive at a contract-safe volatility.** D1's $11k a year at zero edge needs about 40% volatility. At a 20% cap, after stress, zero edge pays FTMO $2.0k per slot-year. The median slot nets about $0.2k a year, and 46% of slots lose money in years 2–3.
  - Under the pre-registered test (40% allowed) it formally "survives" at FTMO ($7.0k) and Blue Guardian ($5.2k), and fails at CFT (median slot −$0.1k a year).
  - But 40% at FTMO is exactly what its own gambling page calls "account rolling".

F2, wave 3, 12 Oct 2026. No firm was contacted, signed up with or paid. Every quote below was read on the firm's own pages on 12 Oct 2026; the full quote files are in `agents/daily/w3-volrisk/clauses-{ftmo,blueguardian,cft}.md`. Every number comes from `agents/daily/w3-volrisk/` (`results.json`, `tables.md`). Pre-registration is `agents/prereg/F2.csv`:

- F2-01 to F2-11 were committed (744e031) before any run.
- F2-12 to F2-15 were added after the model red team and committed (b41874c) before being run.

---

## Part 1. Contract clauses

The book being judged:

- fully automatic and diversified;
- rebalanced daily: dozens of small forex, index, metal and energy CFD positions (crypto at CFT);
- held overnight and over weekends;
- copied on up to 4 accounts;
- sized to 15%, 20% or 30% annual volatility of the $100K account, which is a daily standard deviation of 0.95%, 1.26% or 1.9%.

### FTMO, Swing 2-Step 100K (`clauses-ftmo.md`)

Sources: Challenge T&C PDF "last updated on 4 August 2026" (S1), Forbidden Trading Practices page (S2) and the gambling article it incorporates (S3), Trading Objectives (S4), FAQs. **The funded "FTMO Account" agreement is not public.** It unlocks only after identity checks, and a sample is available only by e-mail, which we did not send.

**1. Gambling and all-or-nothing**
- T&C 7.4: "we retain the discretion to implement any measures we consider appropriate to prevent activities we deem analogous to gambling".
- FTP: "(e.g., overleveraging, overexposure, one-sided bets, account rolling)".
- S3: "What looks like a diversified position could simply be one big dollar bet." / "professionals usually risk only 1%".
- No page uses the words "all-or-nothing".

**2. Maximum risk per trade and position size**
- No numeric cap and no stop-loss requirement ("We do not require you to use a Stop-loss").
- T&C 7.5: avoid "7.5.1 opening substantially larger position sizes compared to your other simulated trades, on any of your accounts; 7.5.2 opening substantially smaller or larger number of positions … regardless of which of your accounts are concerned, and 7.5.3 undertaking repeated simulated trading activity that results in higher Risk per Trade Idea".
- 7.6.6 lets FTMO "enforce the limitation on Risk per Trade Idea to the maximum limit we determine".
- Server limits: "200 orders at a time and 2000 max positions per day".

**3. Consistency**
- The Best Day Rule (50%) "applies to the FTMO Challenge: 1-Step as well as the FTMO Account (1-Step)". **It does not apply to the 2-Step.**
- "Provided you maintain sustainable risk management practices, there are no additional consistency requirements".
- 7.6.9 allows "temporary or permanent consistency measures".

**4. Account review and refusal of rewards**
- 7.6: FTMO may "cancel, consolidate or reclassify" trades, end services, and so on. The FTP adds "forfeiture of any potential Rewards".
- 7.7: "we are not required to notify you before taking such action."
- 7.8: a forbidden practice on one account lets FTMO "terminate all Agreements relating to all FTMO Challenge Accounts you have".
- 7.9: "You are also not entitled to any refund of the FTMO Challenge Fee."
- "Unrealistic" is not used. The equivalents are "replicable with the same or highly similar execution conditions" (7.1) and "not reasonably replicable in the actual market" (FTP).

**5. Repeated evaluation purchases**
- "There is no limit to the number of accounts you may have. However … $400,000 per trader or strategy".
- 3.14.2: for "an unusually large number of Orders" FTMO may "suspend any further Orders by you or invoke a cool-down period".
- S3 calls account rolling "a form of gambling specific to prop trading firms": "If someone is ordering accounts more than is healthy, according to mathematical probabilities…".
- 13.2.3(b): a Challenge held at a loss of 8–10% "for a period longer than thirty (30) calendar days" may be terminated.

**6. Leverage per asset (Swing)**
- FX majors 1:30; NZD pairs and exotics 1:20.
- Metals, major indices, WTI and Brent 1:15.
- Minor indices, natural gas and heating oil 1:9; DXY 1:5.
- Softs, crypto and stocks 1:1.

**Model-critical rules**
- **Daily loss:** "recalculated daily at 00:00 CE(S)T as the difference between: the account balance recorded at 00:00 CE(S)T … and … 5% of the Initial Simulated Capital". It is breached on equity, so a floating loss carried past midnight reduces the next day's room one for one.
- **Maximum loss:** static, at $90,000 equity.
- **Fee refund:** "refunded with your first Reward withdrawal". Failed Challenges are never refunded. 1-Step fees are not refunded.
- **Gap-trading ban:** no "opening simulated trades … two hours or less before a relevant financial market is closed for at least two hours". The Swing exemption covers holding positions, not opening them.

| Clause | 15% | 20% | 30% |
|---|---|---|---|
| Daily loss 5% (hard) | OK | risk; fine with an intraday kill switch | **breach likely** within a year |
| Maximum loss 10% (hard) | edge decides | edge decides | high risk |
| Overexposure, one-sided bets, gambling (discretionary) | OK | low risk | **risk** |
| 7.5 size and count consistency across accounts | low | low | risk; run one vol target on all copies |
| Risk per Trade Idea in correlated symbols | low | risk | **risk** |
| Leverage caps | OK (margin 7–20% of equity) | OK | OK |
| Gap trading near closes | risk at every level; schedule the rebalance around it | same | same |
| Account rolling, repeated purchases | OK | low | **risk** |
| $400k per trader or strategy | 4 accounts exactly | same | same |

### Blue Guardian, 2-Step Standard 100K (`clauses-blueguardian.md`)

**1. Gambling and all-or-nothing**
- "Blue Guardian has a strict policy against "all or nothing" trading behavior." / "Trading activity will be classified as gambling if margin usage exceeds 80% in any running trade(s)".
- T&C bans "a. Excessive risk taking in terms of the % of an account risked in a single simulated-trade; b. Excessive cumulative risk taking in terms of the % of an account risked in a series of overlapping simulated-trades; c. … a "Boom or Bust" approach".

**2. Maximum risk per trade**
- No numeric cap.
- **Guardian Shield (funded only):** "If your PnL on open trades reaches a 2% loss … Guardian Shield will, in most cases, automatically close all open trades for all symbols." / "1st Breach: Profit split reduced to 50%." / "2nd Breach: The account is permanently breached." / "The Guardian Shield does not reset once triggered".

**3. Consistency**
- None on 2-Step Standard.
- Minimum days: "at least 3 trading days … where at least 0.5% profit is achieved".

**4. Account review**
- "Blue Guardian may perform a risk review on accounts at any stage" / "deny a withdrawal request if it is deemed a customer has abused margin availability on an account or not applied an appropriate risk management strategy".
- Banned: "Utilizing one strategy to pass an assessment and then utilizing a different strategy in a funded account". So de-risking only after passing, to survive the Shield, is itself a risk.

**5. Repeated purchases**
- "You may purchase and trade as many challenge accounts as you like". But the T&C says: "Traders are limited to one active account per challenge level, absent prior written approval".

**6. Leverage**
- FX 1:50; indices 1:10; commodities 1:10; crypto 1:2.

**Model-critical rules**
- **Daily loss:** 4% of the initial balance below "the higher figure of either the account balance or account equity" at 5 pm EST, checked on equity.
- **Maximum loss:** 8%, static.
- **Fee refund:** "fully refundable after your fourth payout … If your account is hard-breached before reaching the fourth payout, the fee will not be refunded."

| Clause | 15% | 20% | 30% |
|---|---|---|---|
| **Guardian Shield** | **breach**: second trigger within months | **breach** | **breach** |
| Daily loss 4% from the higher of balance or equity | risk | risk, breach-prone | likely breach |
| Margin over 80% = gambling | OK (9–43%) | OK | OK |
| Excessive cumulative risk, deny withdrawal | low risk | risk | **high risk** |
| Strategy change between evaluation and funded | risk | risk | risk |

### Crypto Fund Trader, 2-Phase 100K (`clauses-cft.md`)

**1. Gambling and all-or-nothing**
- "We also do not allow gambling-style trading, all-in trading, abusive hedging, or any trading behavior that shows a lack of proper risk management."
- T&C 7.1 vi: "operations that use all the available margin for individual positions, operations that result in excessively large fluctuations in unrealized gains/losses".
- 7.1 xv: "we do not allow in any case the non-investment, i.e., gambling; being the company's choice the right to decide on such consideration."

**2. Maximum risk per trade: a $10k profit cap (hard)**
- "The maximum simulated profit allowed per day and/or per trade is $10,000 … any amount above the $10,000 limit may be deducted."
- "The demo profit limit is applied per user". It is measured from "the balance at 12:10 AM UTC".
- No lot cap: "There is no fixed maximum lot size."
- A 2%-per-trade limit with a stop-loss on every trade is only a condition for a reset or a review after a suspension.

**3. Consistency**
- "The Consistency Rule applies only to Break Final Stage accounts." None applies to 2-Phase.

**4. Account review**
- Interview: "may require an interview at any time".
- §14.2: CFT "does not guarantee the payment of the paid scholarship to the trader".
- §3.1.10: "terminate accounts … at our sole discretion, without providing any reason".
- FAQ: "exploitative or unrealistic strategies are not allowed".

**5. Repeated purchases**
- "There is no limit on the number of evaluations a user can purchase or have active at the same time". Funded allocation is capped at $300k per user.

**6. Leverage**
- 1:100 on every class (crypto, forex, indices, commodities, stocks) on MT5 and Match-Trader.

**Model-critical rules**
- **Daily loss:** 5% of the balance at 00:05 UTC, checked on equity, every calendar day.
- **Maximum loss:** 10%, static.
- **Fee:** $660 for $100K, **never refunded** with a payout. It comes back only if CFT refuses to pay or ends the program without a breach.

| Clause | 15% | 20% | 30% |
|---|---|---|---|
| Daily loss 5% from the balance | OK | **risk**; needs an equity kill switch | **breach likely** |
| $10k per day per user (3 accounts) | risk for a fleet | **risk** | **breach plausible**, about 14 times a year |
| Gambling, "excessively large fluctuations" | OK | OK, low | risk |
| Leverage 1:100 | OK | OK | OK |
| Interview, no payout guarantee | risk | risk | risk |

**Part 1 answer.**

- **No firm has a numeric per-trade risk limit or a consistency rule that 20% breaks.** The hard constraints that bind are the daily loss limits, both measured from a closed balance or a higher-of reference, plus Blue Guardian's Shield and CFT's $10k-per-user day cap.
- **At 20%,** FTMO and CFT are workable with a kill switch.
- **At 30%,** the daily loss limit is expected to be breached and the discretionary gambling clauses start to fit.

---

## Part 2. Model robustness

**Model.** `stress_model.py` re-implements D1's daily simulator with switches. With every switch off it reproduces D1 bit for bit, which is unit-tested; 21 tests pass. Each (firm, Sharpe) run simulates D1's whole volatility grid once, with n = 3000 and common random numbers, and reads every vol cap off the same paths.

| Row | What changes |
|---|---|
| F2-01 | D1 as is: t5, 4 equity checks a day, daily loss from day-start equity |
| F2-02 | Student-t with 3 degrees of freedom |
| F2-03 | Overnight gap of 25% of each day's variance plus a Monday weekend gap of one extra day, annual vol held fixed; bot kill switch at 80% of the daily loss limit |
| F2-04 | Kill switch only (control for F2-03) |
| F2-05 | GARCH-like clustering, persistence 0.98 |
| F2-06 | Daily loss on equity including floating P&L, from the higher of balance or equity; closed balance realises 10% of open P&L a day; 24 checks a day |
| F2-07 | Firm-exact rules from Part 1: FTMO and CFT balance reference; Blue Guardian higher-of reference, 4% limit and Shield; CFT $660 with no refund and $3,333 a day per account |
| F2-08 | Blue Guardian, book realised daily |
| F2-09 | All combined (pre-registered decision row) |
| F2-10, F2-11 | Calendar chains: fees when paid, refund on the date of the refund payout |
| **F2-12** | **Post-hoc, decides.** F2-09 with each day exactly t3 and a Brownian intraday path; GARCH cap fixed; payout-day reference fixed; Blue Guardian bot stop at −1.6% open P&L |
| F2-13 | F2-12 with the book realised every day, at a cost of 0.47 Sharpe in spread |
| F2-14 | Calendar chains for F2-12 and F2-13 |
| F2-15 | Four more seeds, to measure noise |

**Why F2-12 replaced F2-09.** The model red team (`redteam-model.md`) found three problems:

- **Fat tails were washed out.** In F2-09 a day was the sum of 24 small t3 shocks, which is close to Gaussian, so 24 checks a day undid the fat-tail stress. F2-09 came out *better* than firm-exact rules alone at high volatility (FTMO, 40%, Sharpe 1.0: $26.6k against $21.0k), which is the symptom.
- **Two small bugs:** the GARCH cap, and the payout-day reference.
- **No bot stop before the Shield** on Blue Guardian.

F2-12 fixes all three and was pre-registered before it ran. F2-09 is kept in the tables.

### $ per slot-year, pre-tax, after stress (F2-12) against D1 (F2-01)

| Firm | Sharpe | 12% | 15% | 20% | 30% | no cap (40%) |
|---|---|---|---|---|---|---|
| FTMO | 0 | 0.7k (D1 1.7k) | 1.2k (2.9k) | 2.0k (4.5k) | 3.8k (8.1k) | 7.0k (10.8k) |
| FTMO | 1.0 | 7.2k (7.9k) | 9.4k (10.6k) | 13.4k (14.2k) | 19.9k (20.6k) | 27.5k (24.7k) |
| FTMO | 1.5 | 11.5k (12.0k) | 14.8k (15.7k) | **20.6k (21.1k)** | 31.2k (29.0k) | 42.0k (33.4k) |
| FTMO | 2.0 | 16.0k (16.3k) | 20.5k (21.3k) | 28.2k (28.5k) | 42.8k (38.4k) | 56.7k (43.1k) |
| Blue Guardian | 1.0 | 6.8k (6.4k) | 8.3k (7.5k) | 10.8k (8.3k) | 14.3k (10.1k) | 18.2k (10.7k) |
| Blue Guardian | 1.5 | 10.7k (9.7k) | 13.0k (10.7k) | 16.8k (11.6k) | 22.5k (13.7k) | 27.7k (14.5k) |
| CFT | 0 | 0.5k (1.9k) | 0.6k (3.1k) | 1.0k (4.7k) | 1.2k (8.5k) | 1.2k (10.9k) |
| CFT | 1.0 | 6.6k (8.2k) | 8.4k (11.0k) | 11.1k (15.0k) | 13.5k (21.6k) | 14.6k (25.2k) |
| CFT | 1.5 | 10.8k (12.2k) | 13.5k (16.2k) | 17.7k (21.8k) | 22.9k (29.4k) | 24.9k (33.6k) |
| CFT | 2.0 | 15.2k (16.4k) | 19.0k (21.6k) | 24.8k (29.2k) | 32.7k (39.1k) | 36.5k (43.6k) |

(F2-13, realising every day, is worse in every cell, so it never decides. Monte Carlo s.e. of one cell is $25–$300.)

### What each stress does (cap 20%, Sharpe 1.5, change against D1)

| Stress | FTMO | Blue Guardian | CFT |
|---|---|---|---|
| t3 tails (F2-02) | −3% | −2% | −5% |
| Gaps, with kill switch (F2-03) | 0% | +6% | 0% |
| Kill switch alone (F2-04) | +1% | +8% | 0% |
| Clustering (F2-05) | −2% | +3% | −3% |
| Strictest daily loss on equity (F2-06) | −18% | −35% | −16% |
| Firm-exact rules (F2-07) | −16% | −25% | **−36%** |
| All, corrected (F2-12) | **−2%** | +45% | −19% |

How to read this:

- **The equity-based daily loss carried from a closed balance is the stress that matters.** Gaps and t3 barely move anything, because a static 10% drawdown with a 5% daily limit is 4σ a day away at 20% volatility.
- **A kill switch at 80% of the limit almost cancels it** for FTMO. That is why F2-12 lands within 2% of D1.
- **At zero edge the stresses bite harder:** FTMO −55% at 20%, CFT −78%. The lottery lives on near-misses.
- **CFT is cut by its contract.** The $10k-per-user day cap removes the right tail that high volatility exists to harvest. The extra gain from 20% to 30% shrinks to $2.4k, and from 30% to 40% to $1.1k (Sharpe 1). It has no refund either.
- **Blue Guardian rises above D1 only because D1's proxy was harsher** than the real rule plus a bot stop. D1 treated the Shield as a hard 2% daily loss that ended the account. The real Shield is a 50% split cut, then a breach, and our bot stops at −1.6%.
  - The model lets the bot re-enter the next day with no loss of edge. A trend book stopped out this often would lose Sharpe in reality.
  - At a fixed 12% volatility the Shield still fires about 2 times per funded life in F2-07, which means the account ends.
  - **Treat the Blue Guardian dollars as an upper bound on a contract we judge unsafe.**

### Sharpe needed for $20k per slot-year (pre-tax)

| Firm | Scenario | 12% | 15% | 20% | 30% | 40% |
|---|---|---|---|---|---|---|
| FTMO | D1 (F2-01) | 2.42 | 1.88 | 1.42 | 0.96 | 0.69 |
| FTMO | **stressed (F2-12)** | **2.44** | **1.96** | **1.46** | 1.00 | 0.70 |
| CFT | D1 | 2.41 | 1.85 | 1.37 | 0.90 | 0.68 |
| CFT | **stressed** | **2.54** | **2.09** | **1.66** | 1.35 | 1.29 |
| Blue Guardian | D1 | 2.89 | 2.71 | 2.52 | 2.26 | 2.11 |
| Blue Guardian | stressed (upper bound, see above) | 2.60 | 2.18 | 1.76 | 1.36 | 1.09 |

Linear interpolation on a Sharpe grid with steps of 0.25. Bold cells are inside the contract-safe range.

### Maximum safe volatility (rule fixed in F2-09; noise from F2-15)

| Firm | Cap | Net at Sharpe 1.0 | Gain over the next lower cap (s.e.) | Clauses (a) | Breach before first payout |
|---|---|---|---|---|---|
| FTMO | 15% | 9.6k | +2,353 (169) | pass | 4% |
| FTMO | **20%** | 13.4k | +3,807 (144) | **pass** | 7% |
| FTMO | 30% | 20.1k | +6,769 (160) | **fail** | 14% |
| CFT | **20%** | 11.0k | +2,552 (128) | **pass** | 9% |
| CFT | 30% | 13.4k | +2,395 (134) | **fail** | 19% |
| Blue Guardian | 12–30% | 6.8k–14.5k | | **fail at every level** (Shield) | 4–20% |

- **Rule (b), that more volatility still earns more, passes at every step.** The model always prefers more volatility. So the limit comes from rule (a), the clauses: **20% for FTMO and CFT, and none of the tested levels for Blue Guardian.**

### Real fee and refund timing (calendar chains, F2-14a, per slot)

| Firm, Sharpe, cap | Year-1 mean | P(year-1 loss) | Years 2–3 mean | Median | p10 |
|---|---|---|---|---|---|
| FTMO 1.5, 20% | 11.4k | 13% | 22.0k | 21.6k | 11.6k |
| FTMO 1.5, 12% | 3.5k | 40% | 13.0k | 12.9k | 6.0k |
| FTMO 0, 20% | 0.4k | 79% | 1.9k | 0.2k | −0.8k |
| FTMO 0, 40% | 4.2k | 52% | 6.6k | 4.8k | −2.0k |
| CFT 1.5, 20% | 9.4k | 16% | 19.1k | 19.1k | 9.5k |
| CFT 0, 20% | −0.6k | 86% | 0.9k | −0.3k | −1.3k |

- **Year 1 is lean.** At 20%, a slot earns about half of its steady state in year 1, because passing takes months and the refund only arrives with the first payout. At 12% it earns about a quarter.

### Does the Sharpe-0 lottery survive?

| Firm | D1 | F2-09 net / median slot | F2-12 net / median | F2-13 net / median | Pre-registered test (F2-11 / F2-14) |
|---|---|---|---|---|---|
| FTMO | 10.8k | 9.1k / 7.2k | 7.0k / 4.8k | 2.0k / −0.5k | survives / survives (at 40% vol) |
| Blue Guardian | 4.3k | 3.1k / 2.5k | 5.2k / 3.9k | 1.2k / 0.4k | survives / survives (at 40% vol) |
| CFT | 10.9k | 1.8k / 1.1k | 1.2k / −0.1k | −0.2k / 0.0k | barely survives / **does not** |

- **Mechanically, yes at FTMO, but only at 40% volatility.** At 40% volatility FTMO's 5% daily loss is 2σ a day.
- **At 40% you are doing what FTMO's own gambling page calls "account rolling":** buying evaluations because "according to mathematical probabilities, he has a pretty good chance of succeeding on several accounts". FTMO may then suspend orders (3.14.2), forfeit rewards and end every agreement at once (7.8). None of that is in the model.
- **At the contract-safe 20%,** zero edge earns $2.0k a year on FTMO with a median of $0.2k, and nothing on CFT. **The lottery is not a business.**

---

## What is not modelled (direction)

**Optimistic for high volatility:**
- The kill switch and Blue Guardian bot stop fill at the checked price, with no slippage, and lose no edge on re-entry.
- Discretionary reviews: refused rewards, account rolling, the FTMO 13.2.3(b) 30-day rule, CFT interviews.
- Running the whole fleet at once against one firm event.
- FTMO's funded agreement, which is not public.

**Pessimistic:**
- Weekend gaps are applied to CFT's crypto, which actually trades on weekends.
- The balance lags equity at 10% a day, a choice of the bot; partial realisation would help CFT's cap.
- No scaling plans.

**Not a market test.** Every Sharpe here is assumed. The gate (t ≥ 3.5745) does not apply; F2 priced risk and contracts, not an edge. The measured strategies (synthesis) are far below Sharpe 1.5.

## Files

All in `agents/daily/w3-volrisk/`:

- `stress_model.py`: model.
- `test_stress_model.py`: 21 tests.
- `scenarios.py`, `run_f2.py`: runs (`run_f2.log`, `run_f2_posthoc.log`).
- `results.json`, `make_report.py` → `tables.md`: every table.
- `clauses-*.md`: quotes.
- `redteam-model.md`: red team.
- `verify.md`: independent re-run.
