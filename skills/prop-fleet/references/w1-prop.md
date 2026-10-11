# W1-D1: prop-firm structure and economics

**Verdict.** For a fully automatic bot that holds positions overnight, the best three structures
are:

1. **FTMO Swing 2-Step $100K**: 4 accounts.
2. **Blue Guardian 2-Step $100K**: 4 accounts.
3. **Crypto Fund Trader 2-Phase $100K**: 3 accounts.

All three have a static drawdown of 8–10%, no evaluation clock, and allow overnight and weekend
holding. They allow bots on funded accounts. At a net Sharpe of 1.17 and 12%/yr volatility, the
11 accounts make about **$96k a year**:

- That figure is the steady state, before tax. Year 1 makes about $40k.
- The 10th percentile of the fleet is about $21k a year.
- The cost is $5.2k of fees up front, then about $2.9k a year.

**Each of the three needs a Sharpe of 0.3 or less to reach the bar we set:** 20% a year, after
tax, on the money spent. **The bar is met even at Sharpe 0.** A refundable or cheap fee buys a
call option on a $100K account. So "20% on fees" is not a test of edge. What actually limits income:

- the cap on accounts per person;
- the volatility the firm tolerates;
- whether the firm keeps paying.

Every futures firm forces you flat each day, so the measured multi-day trend edge (Sharpe 1.17)
cannot run on any of them. Apex bans bots on funded accounts outright.

Department D1, wave 1, 11 Oct 2026. Every number here comes from code that was run
(`agents/daily/w1-prop/`) or from a firm page cited in `agents/daily/w1-prop/rules.csv`.
Pre-registration: `agents/prereg/D1.csv`. D1-01 to D1-05 were committed before any firm run;
D1-06 was committed before the bug-fixed run. No firm was contacted, signed up with or paid.

---

## 1. What we can run where

The full table is `agents/daily/w1-prop/rules.csv`: 369 cells across 17 firms and 25 programs.

- **Sources.** Every cell has the firm-page URL it came from, a status, and a note.
- **Status.** 325 cells are verified on the firm's own domain (fetched, or a search snippet from
  that domain), 9 are corroborated by two or more independent third parties, and 35 are
  unverified.
- **Independent re-check.** A separate verifier re-checked the 198 decisive cells:
  - 189 confirmed;
  - 4 corrected (two of them fees, which the model now uses);
  - 2 downgraded;
  - 3 could not be checked.

  See `rules/verifier.csv`.
- **Blocked sites.** No host was blocked by our network proxy. Some firm sites block automated
  readers themselves (Cloudflare: Lucid, Apex, E8, Alpha, Breakout, part of Tradeify). There the
  rows rest on search snippets from the firm's own domain, and the CSV says so.

Short form, for the standard program per firm. Status is **V** verified, **C** corroborated or
**U** unverified.

| Firm, program | Bot on FUNDED | Platform / API | VPS | Cap per person | Copy own accts | Drawdown | Daily loss | Eval clock | Overnight / weekend | Split, payouts | Fee |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **FTMO** Swing 2-Step 100K | yes, third-party EAs ok (V) | MT4/5, cTrader, TradingView (V) | yes (V) | $400K per trader/strategy (V) | yes, within cap (V) | 10% static (V) | 5% of initial, from midnight balance, hard (V) | none; 4 min days/phase (V) | yes / yes (V) | 80% to 90%; first after 14 days, then bi-weekly (V) | EUR 439–540, refunded with 1st payout (V) |
| **The5ers** High Stakes 100K | yes, must own source; visible SL (V) | MT5, cTrader, TradingView (V) | not stated (U) | **1** High Stakes acct (V) | yes (V) | 8% static (V; FAQ elsewhere says 10%) | 4% hard (V) | none (V) | yes / yes; +-2 min news (V) | 80% rising to 100%; 14 days; cap $4k per payout (V) | $455, 70% refunded (V) |
| **FundedNext** Stellar 2-Step | EAs **banned on >=$50K**; on smaller with paid add-on, no identical trades across accts (V) | MT4/5 (V) | add-on (V) | $300K (V) | **no** (V) | 10% static (V) | 5% (V) | none (V) | yes / yes; news profits 40% (V) | 80% (verifier: 60–90% by payout option) (V) | $200 for 25K + EA add-on (V) |
| **FTUK** Flex 100K | "risk-management EAs" vs "EAs/Bots allowed" (U) | MT5 etc. (V) | – | 3 accts, each a different strategy (V) | **no** (V) | 6% trailing, locks at start (V) | 5%; -2% floating auto-close (V) | none (V) | yes / yes (V) | 60% rising to 90% by level; on demand (V) | $9 + $672 after pass (V) |
| **Alpha Capital** Swing 2-Step 100K | **no**: EAs only for trade management, need pre-approval (V) | MT5 (V) | – | $400K; one asset per funded acct (V) | with notice (V) | 10% static (V) | 5% (V) | none (V) | yes / yes (V) | 80%; on demand (V) | $577 (V) |
| **E8 Markets** Pro Forex 100K | yes, unless several users run the same trades (V) | MT5, MatchTrader, cTrader, TradeLocker (V) | not stated (U) | $500K and 5 accts **per market** (V) | yes (V) | 8% static, locks at start after 1st payout (V) | **2.5%** hard (V) | none (V) | yes / yes (V) | 80%; only **50%** of profit per request (V) | $568 (V) |
| **Blue Guardian** 2-Step 100K | yes, own EAs (V) | MT5, MatchTrader, TradeLocker (V) | yes, not shared (V) | $400K active (V) | yes (V) | 8% static (V) | 4% hard (V); **Guardian Shield: open loss -2% closes all; 1st hit split to 50%, 2nd breach** (V) | none (V) | yes / yes; +-5 min news on funded (V) | 85%, 3% processing fee; 14 days (V) | $347 with code, refunded after 4th payout (V) |
| **HyroTrader** 2-Step 100K (crypto) | yes, own bot via own API key (V) | Bybit/BloFin API (V) | own server (U) | $200K funded (V) | **mirroring banned** (V) | 10% static (V) | 5% (V) | none (V) | yes / yes (V) | 80%; on demand (V) | $579, refunded (V, corrected) |
| **Breakout** (Kraken) 1-Step 100K | **not addressed**; bans off-the-shelf strategies (U) | own terminal, DXtrade; no bot API (V) | not addressed (V) | $200K (V) | not stated (U) | 6% static (V) | 3% (V) | none (V) | yes / yes (V) | 80%; any time (V) | $800 (V) |
| **Crypto Fund Trader** 2-Phase 100K | yes, except HFT/arbitrage/news EAs (V) | MT5, MatchTrader, Bybit API (V) | – (U) | $300K (V) | only between eval accounts stated (V) | 10% static (V) | 5% (V) | none (V) | yes / yes (V) | 80%; every 15 traded days (V) | $520–598 (firm pages differ) |
| **Topstep** XFA 50K | yes via ProjectX API; **no VPS**; ends if moved to Live (V) | ProjectX API, $29/mo (V) | **banned** (V) | 5 XFAs (V) | yes (V) | $2,000 EOD trailing, locks at start (V) | optional $1,000 soft (V) | none, $49/month (V) | **no, flat 3:10 PM CT** (V) | 90%; 50% up to $2k per payout (V) | $49/mo + $149 activation (V) |
| **Bulenox** Master 50K | yes, own tools only; +$100/mo API (V) | Rithmic only (V) | – (U) | 5 (V) | yes (V) | $2,500 EOD, locks at +$100 (V) | $1,100 soft (V) | **30 days** (V) | **no** (V) | 100% of first $10k then 90%; $1.5k cap x3 (V) | $175 + $148 (V) |
| **Lucid** Flex 50K | yes; no hedging/microscalping (V) | CQG, Rithmic (V) | – (U) | 5 funded (V) | yes (V) | $2,000 EOD, locks (V) | optional soft (U) | none (V) | **no** (V) | 90%; 50% up to $2k; 5 payouts then live review (V) | ~$146 (C) |
| **Tradeify** Select 50K | yes, but **bot may be used at Tradeify only**; live video on request (V) | Tradovate, Rithmic; API on live only (V) | after login, own risk (V) | 5 (V) | yes, same direction (V) | $2,000 EOD, locks (V) | none (V) | none stated (U) | **no** (V) | 90%; 50% up to $2.5k (V) | $165 (V) |
| **MyFundedFutures** Rapid EOD 50K | own automated strategies yes; "unattended" conflicts (V/U) | Tradovate, NinjaTrader, Rithmic (C) | – (U) | **3** on this plan (V) | yes (V) | $2,000 EOD, locks (V) | none (V) | none; 7-day inactivity (V) | **no** (V) | 90%; daily after buffer (V) | $135 with code (V) |
| **Apex** EOD PA 50K | **NO: banned on all funded accounts** (V) | Rithmic, Tradovate (V) | moot | 20 (V) | copiers barred (V) | $2,000 EOD, locks (V) | $1,000–2,000 soft (V) | **30 days** (V) | **no** (V) | 100%; ladder 1.5k–3k, 6 payouts (V) | conflicting (U) |
| E8 Signature Futures 50K | **NO** (V) | – | – | 5 | – | $2,000 EOD | 2% soft | none | no | 80% | $150 |

Five things stand out:

- **All six futures firms force you flat every day.** The 1.17 trend edge holds positions for days
  to weeks, so it cannot run on any of them. A futures fleet still needs an intraday edge, and
  H0001–H0022 found none.
- **Forex/CFD and crypto firms allow overnight and weekend holding with static drawdowns.** Of the
  ten we modeled, six clearly allow a fully automatic bot on funded accounts. Breakout and FTUK are
  unknown, FundedNext is conditional, and Alpha bans it.
- **Copying one strategy across accounts** is explicitly allowed at FTMO (within $400K), The5ers,
  E8 and Blue Guardian. It is banned at HyroTrader (mirroring), FundedNext and FTUK.
- **Caps per person are small.** The largest automatic, overnight-holding allocation at one firm is
  $400–500K.
- **The rules a bot most often breaks by accident are not drawdowns.** They are open-loss shields:
  Blue Guardian -2%, FTUK -2%, Alpha -2% per asset, HyroTrader 3% per trade. Firms also flag
  identical trades across users.

## 2. Economics

### Method

The model is `agents/daily/w1-prop/prop_model.py`, a copy of `scripts/apex_model.py`. The
original Apex model is untouched; the D1 extension sits below it, with 14 tests.

1. **Daily returns.** Each day's return is drawn from a Student-t(5) distribution (fat tails),
   with Sharpe S net of trading costs and annual volatility sigma. The day is split into 4 steps so
   that intraday drawdowns and daily limits can trigger.
2. **Firm rules.** Each firm's rules are applied exactly as parameterized in `firms.py`, which
   maps every value to `rules.csv`. That covers the evaluation phases, minimum days, clock and
   monthly fee; static, trailing-EOD or trailing-intraday drawdown and its lock; hard or soft
   daily loss; and payout cycle, fraction, cap, minimum, floor, split, refund and closure after N
   payouts.
3. **Yearly income per account slot.** One slot repeats: buy an evaluation, try until you pass,
   trade the funded account until it breaches, closes or reaches 3 years, then buy again.
   Yearly income per slot is the expected profit per cycle divided by the expected cycle length.
   A second, step-by-step simulation chains attempts and funded lives in order. It gives yearly
   distributions, year 1 and p10, and agrees with the first within about 10%.
4. **Volatility.** Sigma is chosen separately for the evaluation and the funded phase, to maximize
   net dollars per slot-year.
   - **D1-01 (uncapped):** the optimizer always runs to 25–40%/yr. That is a lottery on the fee,
     which firms' gambling, max-risk and shield rules exist to stop.
   - **D1-04 (decides):** sigma is capped at 12%/yr, which is how a real trend or carry book runs.
5. **Fleet.** The fleet is the per-person cap times one slot. Accounts copy one strategy, so they
   are perfectly correlated, and fleet p10 = slots × slot p10.
6. **Return on money spent.** ROS = (payouts − fees) / fees per year, after 25% tax on positive net.

### Results at Sharpe 1.17, vol at most 12% (D1-04)

| Firm | Bot? | Overnight | Slots | Pass % | Eval days | Funded life (days) | Net $/slot-yr | Fees $/slot-yr | ROS after tax | **Fleet $/yr** | Fleet p10 | Year-1 $/slot |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FTMO Swing 2-Step 100K | yes | yes | 4 | 78 | 263 | 437 | 9,398 | 234 | 3,012% | **37,592** | 7,503 | 3,384 |
| Blue Guardian 2-Step 100K | yes | yes | 4 | 70 | 201 | 238 | 7,352 | 283 | 1,948% | **29,408** | 5,998 | 3,822 |
| Crypto Fund Trader 2-Phase 100K | yes | yes | 3 | 79 | 226 | 454 | 9,644 | 280 | 2,580% | **28,931** | 7,065 | 3,717 |
| HyroTrader 2-Step 100K | yes | yes | 2 | 78 | 263 | 413 | 9,453 | 275 | 2,574% | 18,906 | 3,477 | 3,748 |
| Breakout 1-Step 100K | unknown | yes | 2 | 69 | 151 | 146 | 8,887 | 990 | 673% | 17,775 | 2,775 | 5,105 |
| E8 Pro Forex 100K | yes | yes | 5 | 71 | 122 | 37 | 2,682 | 1,270 | 158% | 13,411 | -1,332 | 1,514 |
| The5ers High Stakes 100K | yes | yes | 1 | 69 | 220 | 301 | 9,448 | 319 | 2,221% | 9,448 | 1,849 | 4,489 |
| FTUK Flex 100K | unknown | yes | 1 | 64 | 47 | 49 | 8,011 | 1,802 | 333% | 8,011 | 3,407 | 6,585 |
| FundedNext Stellar 2-Step 25K | conditional | yes | 1 | 79 | 226 | 438 | 2,376 | 120 | 1,486% | 2,376 | 542 | 850 |
| Alpha Swing 2-Step 100K | **no** | yes | 4 | 78 | 263 | 433 | 9,191 | 266 | 2,589% | (36,762) | 6,035 | 3,182 |
| Tradeify Select 50K | conditional | **no** | 5 | 46 | 69 | 38 | 3,100 | 842 | 276% | 15,498 | 1,670 | 2,204 |
| MFFU Rapid EOD 50K | conditional | **no** | 3 | 46 | 69 | 59 | 3,492 | 576 | 455% | 10,477 | 119 | 2,238 |
| Topstep XFA 50K | conditional | **no** | 5 | 47 | 69 | 27 | 2,137 | 1,010 | 159% | 10,684 | -1,099 | 1,514 |
| Lucid Flex 50K | yes | **no** | 5 | 46 | 69 | 28 | 2,123 | 819 | 194% | 10,614 | 156 | 1,572 |
| Bulenox Master 50K | yes | **no** | 5 | 12 | 167 | 267 | 1,815 | 1,201 | 113% | 9,076 | -10,758 | -678 |
| Apex EOD PA 50K | **no** | **no** | 20 | 12 | 158 | 398 | 1,279 | 529 | 181% | (25,587) | -20,671 | -641 |

The futures rows describe a hypothetical intraday strategy with Sharpe 1.17. Our trend edge cannot
run there.

### Net dollars per slot-year by Sharpe (vol at most 12%)

| Firm | S=0 | 0.8 | 0.82 (=1.17 × 0.7, D1-03) | 1.0 | 1.17 | 1.2 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|---|---|
| FTMO Swing | 1,786 | 6,546 | 6,697 | 8,059 | 9,398 | 9,664 | 12,087 | 16,353 |
| Blue Guardian | 1,654 | 5,172 | 5,257 | 6,294 | 7,352 | 7,546 | 9,461 | 13,092 |
| Crypto Fund Trader | 1,970 | 6,867 | 7,008 | 8,356 | 9,644 | 9,894 | 12,331 | 16,548 |
| HyroTrader | 1,767 | 6,589 | 6,726 | 8,104 | 9,453 | 9,695 | 12,198 | 16,495 |
| The5ers | 1,905 | 6,575 | 6,700 | 8,101 | 9,448 | 9,692 | 12,167 | 16,632 |
| E8 Pro Forex | 266 | 1,778 | 1,824 | 2,265 | 2,682 | 2,770 | 3,719 | 5,536 |
| Tradeify | 592 | 2,159 | 2,199 | 2,636 | 3,100 | 3,186 | 4,038 | 5,649 |
| Topstep | 277 | 1,386 | 1,432 | 1,772 | 2,137 | 2,207 | 2,909 | 4,351 |
| Bulenox | -933 | 523 | 593 | 1,198 | 1,815 | 1,936 | 3,234 | 6,009 |
| Apex | -495 | 561 | 596 | 933 | 1,279 | 1,339 | 1,923 | 3,364 |

The full tables for all 16 programs are in `agents/daily/w1-prop/tables.md`:

- pass probability and funded lifetime at every Sharpe;
- uncapped results;
- every minimum-Sharpe column.

### Fleets

| Fleet | Accounts | Notional | Fees up front | S=0 | S=0.8 | S=0.82 | **S=1.17** | S=2.0 | Year 1 at 1.17 | p10 at 1.17 |
|---|---|---|---|---|---|---|---|---|---|---|
| Top 3 (FTMO 4 + Blue Guardian 4 + CFT 3) | 11 | $1.1M | $5.2k | $19.7k | $67.5k | $68.8k | **$95.9k** | $167k | $40.0k | $20.6k |
| Every bot-allowed overnight firm (+HyroTrader 2, E8 5, The5ers 1) | 19 | $1.9M | $9.7k | $26.4k | $96.1k | $98.1k | **$137.7k** | $245k | $59.5k | $24.6k |
| Futures firms that allow bots (needs an *intraday* edge) | 23 | $1.15M | $3.1k | $2.9k | $34.4k | $35.5k | $56.4k | $121k | $29.8k | -$9.9k |

Volatility cap sensitivity (D1-06), at S = 1.17:

| Fleet | Cap 8% | Cap 12% | Cap 15% |
|---|---|---|---|
| Top 3 | $60.3k | $95.9k | $119.5k |
| All eligible | $85.1k | $137.7k | $171.5k |

### Minimum Sharpe for at least 20% a year after tax on money spent

| Firm | Met already at S=0 (D1-05)? | Min S, cap 12% (D1-04) | Min S, uncapped (D1-01) | Min S, Gaussian, EOD only (D1-02) |
|---|---|---|---|---|
| All 10 forex/crypto programs | yes (ROS at S=0: 25%–332%) | at most 0.30 | at most 0.30 | at most 0.30 |
| Topstep, Lucid, Tradeify, MFFU | yes, barely (21–49%) | at most 0.30 | at most 0.30 | at most 0.30 |
| Bulenox | no | **0.76** | at most 0.30 | 0.72 |
| Apex | no | **0.59** | at most 0.30 | 0.58 |

The bisection was pre-registered on [0.3, 3.0], so "at most 0.30" is the floor of that search. The
S=0 column shows the true minimum is below zero wherever it says yes. Bulenox and Apex have a
30-day clock, so they are the only firms where edge, rather than the fee option, decides.

**Which firms make Sharpe of about 1.17 profitable?** All 16 programs earn more than 20% a year on
fees at 1.17, and also at 0.82. Only the overnight-holding firms can actually run that edge:

- FTMO, Blue Guardian, Crypto Fund Trader, HyroTrader, E8 Pro, The5ers.
- Breakout and FTUK if they confirm bots are allowed.

## 3. What the red team found, and what changed

The full report is `agents/daily/w1-prop/redteam.md`. Starting verdict: refuted. Final verdict:
weakened.

1. **A real bug, now fixed, with a test.** After a payout, the next day's daily-loss limit was
   measured from the pre-payout balance. That breached any account whose payout exceeded the daily
   limit, which punished long payout cycles. The fix raised FTMO, Crypto Fund Trader and The5ers by
   34–53% per slot and Blue Guardian by 122%. It also removed HyroTrader's false lead. Every number above
   comes from the fixed run (`run_d1.log`); the pre-fix run is `run_d1_main.log`.
2. **No bug inflates payouts or deflates fees.** Picking the best vol on one seed biases results up
   by about 4–5%. Cutting runs off at the 3-year horizon is conservative.
3. **The five static-drawdown $100K structures are tied within noise**: $9.2–9.6k per slot-year.
   So the ranking goes by how many accounts the copy rules allow and by rule risk, not by the model:
   - **FTMO** is first. It is the most verified, explicitly allows copying and VPS, and refunds the fee.
   - **Blue Guardian** is second. It explicitly allows copying and VPS. But its -2% open-loss
     shield is modeled only as a 2% daily limit. A multi-day trend book will hit it more often, so
     its $7.4k per slot is optimistic.
   - **Crypto Fund Trader** is third. It has 3 slots, but whether copying is allowed between funded
     accounts is unstated, and its fee is $520–598 depending on the page.
   - **HyroTrader** would add 2 slots, but it bans account mirroring.
   - **The5ers** gives only one account.
4. **Sharpe 1.17 is not a number for these venues.** It was measured on 54 futures, including bonds
   and short-rate futures. FTMO and Blue Guardian offer forex, index, metal and energy CFDs with
   financing costs. Crypto Fund Trader and HyroTrader offer crypto perpetuals only. The venue
   Sharpe is D2's and D3's question. At S = 0.6 the top-3 fleet makes $30k at an 8% cap and $68k at a 15% cap.
5. **Year 1 is lean.** At 12% vol, passing a 10% + 5% evaluation takes about a year (263 trading
   days at FTMO). Each top-3 slot has a 36–46% chance of losing money in year 1. The top-3 fleet makes
   about $40k in year 1, against $96k in steady state.
6. **Risks not modeled:**
   - payout denial;
   - a firm failing;
   - one event hitting every firm at once while the same strategy runs everywhere;
   - firms detecting identical trades.

   A 15%/yr chance of losing a funded account with no payout costs about 7% of the fleet. The real
   risk is all firms at once.

## 4. What this means for the wave

- **Profitable is not the question; whether the fleet is worth running is.** At the 12% cap, the
  top three make $20k a year at S=0, $67k at S=0.8 and $96k at S=1.17. The edge is worth about
  $76k a year at 1.17. The fee option alone is worth about $20k, and firms try to stop people
  harvesting that by gambling.
- **20% on notional is out of reach this way.** $96k on $1.1M notional is 8.7%. The goal was
  restated as 20% on money spent, and on that measure every eligible firm clears it: E8 by about
  8 times (158%), the others by about 100 to 150 times.
- **Unblocking the fleet takes the following, before any money is spent:**
  1. A measured Sharpe for a trend/carry book on FTMO-style CFDs (D2) and on crypto perpetuals
     (D3), net of financing.
  2. Written answers from:
     - Breakout on bots;
     - Crypto Fund Trader on copying between funded accounts;
     - Blue Guardian on how the shield treats multi-day positions;
     - FTMO on whether its "same strategy" cap is per strategy or per trader.

     These questions are ones a person would ask; this department does not contact firms.
  3. A bot that stops itself before the open-loss shields trigger.

## Files

All under `agents/daily/w1-prop/`:

- **Rules:**
  - `rules/` holds each worker's CSV and the verifier's check.
  - `rules.csv` is the merged table, with the verifier's verdict on each cell.
- **Model:**
  - `prop_model.py` is the model.
  - `test_prop_model.py` holds its 14 tests (pytest).
  - `firms.py` holds the parameters.
- **Runs:**
  - `run_d1.py` runs everything.
  - `results.json`, `results.txt`, `tables.md` (made by `make_tables.py`) and `run_d1.log` are the
    output.
- **Red team:** `redteam.md`.
- **Pre-registration:** `agents/prereg/D1.csv`.

The gate (t ≥ 3.5504) does not apply here. D1 tested no market edge; it priced structures.
