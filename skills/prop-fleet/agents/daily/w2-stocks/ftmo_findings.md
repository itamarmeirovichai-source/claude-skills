# FTMO stock CFD trading conditions (E1 wave 2, retrieved 11 Oct 2026)

Sources: only ftmo.com pages and ftmo.com's own JSON endpoints. Every host returned 200, so nothing was blocked. I did not log in, sign up or make contact. Raw downloads are in `scratchpad/ftmo/`.
Items marked ⚠ are unverified or are my inference, not FTMO's own words.

## 1. Stock CFD symbol list

- **Source:** https://ftmo.com/en/symbols/ renders its table from `https://ftmo.com/wp-json/ftmo/symbols`. The table script (`/app/themes/ftmo-com/build/js/symbols-table-Dkxn7OmE.js`) calls `fetch("/wp-json/ftmo/symbols"`. Saved as `ftmo/symbols.json`.
- **Count:** the JSON has 166 active symbols in total. **59 are `"assetClass":"Equities CFD"`**: 46 quoted in USD (US-listed, including ADRs such as ASML, AZN, BABA, RACE) and 13 quoted in EUR (EU-listed). FTMO's holiday notices call the US group "Equities I CFD (US stocks)".
- **US (46):** AAPL,AMD,AMZN,ARM,ASML,AVGO,AZN,BA,BABA,BAC,BRK.B,CSCO,CVX,DIS,FDX,GE,GM,GME,GOOG,IBM,INTC,JNJ,JPM,KO,LMT,MCD,META,MSFT,MSTR,NFLX,NKE,NVDA,PFE,PLTR,QCOM,RACE,RTX,SBUX,SNOW,SPCX,T,TSLA,V,WMT,XOM,ZM
- **EU (13):** ADSGn,AIRF,ALVG,BAYGn,BMW,DBKGn,IBE,LVMH,MBG,SAN,SIEGn,TTE,VOWG_p
- **Per-symbol detail:** see `scratchpad/ftmo_stocks.csv`.
- **Example record** (verbatim JSON): `{"code":"AAPL","name":"Apple, Spot CFD","contractSize":1,"marginPercent":30,"swapLong":-7.72,"swapShort":-6.1,"swapType":"points","commission":0.004,"commissionType":"percent","leverageStandard":3.33,"leverageSwing":1,"digits":2,"usdCommission":0.0269,"maxTradeVolume":10000,"maxTotalVolume":0}`
- ⚠ **Market caps:** there is no exchange field. I inferred the country from `profitCurrency`.

## 2. Commission, spread and contract size

- **Commission:** all 59 stocks have `"commission":0.004,"commissionType":"percent"`. The page's renderer labels this type `"PERCENT/VOLUME"` (from JS: `n==="percent"?"PERCENT/VOLUME"`). That means **0.004% of traded notional**.
  - ⚠ The page does not say whether this is per side or per round turn. The `usdCommission` field (for example AAPL 0.0269, NVDA 0.0183) is consistent with 0.004% per side, charged on both sides, on a price of about $336 for AAPL. This is my inference.
- **Commission rationale** (https://ftmo.com/en/faq/how-does-the-ftmo-technical-infrastructure-work/): "we also include simulated commissions when executing trades. All commissions applied to each symbol can be found by everyone on our website and on the trading platform."
- **Contract size:** `"contractSize":1` (1 lot = 1 share) and `"maxTradeVolume":10000` for every stock.
- ⚠ **Minimum lot / volume step:** not published in the JSON. The FAQ points to the platform: "The account specification can be seen directly in the trading platform… right-click on the relevant instrument, and choose 'Specification'" (https://ftmo.com/en/faq/what-are-the-account-specifications/).
- ⚠ **Spread:** no stock spread figures are published. FTMO says only: "We do not add hidden markups or additional slippage. Trades are executed according to the pricing visible on the trading platform." It also mentions an artificial "delay which reaches up to 200 ms" (same infrastructure FAQ).

## 3. Swap (overnight financing)

- **Type:** `"swapType":"points"` for all stocks. The point is 0.01 for 2-digit symbols, so AAPL long -7.72 points means about -$0.077 per share per night ⚠ (my interpretation).
- **Direction:** both long and short swaps are **negative** for all 59 stocks. Examples: AAPL -7.72/-6.10, NVDA -5.44/-4.30, MSFT -12.14/-9.60, TSLA -8.66/-6.85, ASML -41.33/-32.69. The full list is in the CSV.
- **Dividends are folded into swaps** (https://ftmo.com/en/trading-updates/ and every weekly update, e.g. https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/): "Overnight rollover swaps are subject to regular changes and adjustments, reflecting, among other things, interest rate differentials and dividend adjustments. … it is your responsibility to check these swaps in the contract specification for each symbol".
- **Triple swap** (https://ftmo.com/en/blog/what-is-a-swap-and-for-whom-is-it-important/): "the triple swap being charged overnight from Wednesday to Thursday." The article's example is EURUSD.
  - ⚠ Not confirmed for stock CFDs. Equity CFDs often triple on Friday, so check the "Specification" window in MT5.

## 4. Leverage and margin

- **Symbols JSON / page, all 59 stocks:** `"marginPercent":30`, `"leverageStandard":3.33`, `"leverageSwing":1`. The page renders these as "Leverage 1:3.33" and "Leverage Swing 1:1" (JS: `title:t.leverage_swing,data:\`1:${s}\``).
- **Result: Standard 1:3.33 (30% margin); Swing 1:1** (⚠ margin about 100% implied; the JSON lists one `marginPercent` only).
- **Account level** (https://ftmo.com/en/faq/what-are-the-account-specifications/): "The leverage we offer for the Standard account type is up to 1:100 and cannot be increased. The Swing account type has leverage set to up to 1:30."
  - Stocks are well below these caps.

## 5. Trading hours and shorting

- **US stocks:** the JSON `tradingHours` gives **13:35–20:00 UTC, Mon–Fri**, which is 09:35–16:00 New York.
  - This is regular session only, and the first 5 minutes are excluded. There is no pre- or post-market.
- **EU stocks:** 07:05–15:30 UTC.
- The table also says: "Trading hours are not affected by holidays" (strings.json). Holiday closures are announced separately, for example: "Equities I CFD (US stocks), Agriculture will be closed whole day" (https://ftmo.com/en/blog/trading-updates/trading-update-2-jul-2026/).
- **Shorting is allowed.** Every stock has a `swapShort` rate. The SPCX listing shows shorting is normally available, with one exception: "Please note that during the lock-up period, only buy (long) orders will be permitted. Short selling will not be available until the lock-up period expires." (https://ftmo.com/en/blog/trading-updates/trading-update-18-jun-2026/)
- **Tracking:** "This CFD symbol is designed to track the spot price of the underlying stock." (same page)

## 6. Dividends

- The only statement FTMO publishes is that swaps reflect "dividend adjustments" (quote in section 3).
- ⚠ There is no separate dividend cash adjustment or ex-dividend policy for stock CFDs on any page I checked: FAQ, symbols, trading updates, and a search of the WP API for "dividend".
- The Academy (academy.ftmo.com, returned 200) is general education only.

## 7. Swing account rules (2-Step only)

| Item | Value | Source and quote |
|---|---|---|
| Availability | 2-Step only | FAQ swing: "available exclusively within the FTMO Challenge: 2-Step" https://ftmo.com/en/faq/what-is-the-swing-account-type-and-how-does-it-work/ |
| Profit target | 10% in Phase 1, 5% in Phase 2, none on the FTMO Account | "10% for the FTMO Challenge / 5% for the Verification … There is no Profit Target on the subsequent FTMO Account (2-Step)." https://ftmo.com/en/trading-objectives/ |
| Max daily loss | 5% of initial capital, measured on equity, reset 00:00 CE(S)T from the prior balance | "the Maximum Daily Loss Amount, which is 5% of the Initial Simulated Capital" (same page) |
| Max loss | 10%, static | "static limit … Maximum Loss Amount, which is 10% of the Initial Simulated Capital"; comparison table: "Max Loss type Static" https://ftmo.com/en/comparison-table/ |
| Min trading days | 4 per phase, none on the funded account | "requires the trader to achieve at least 4 Trading Days" (trading-objectives) |
| Trading period | Unlimited | comparison table |
| Profit split | 80%, rising to 90% via Scaling or Premium | "FTMO Challenge: 2-Step: You receive 80% of the profit (increases to 90% if Scaling Plan or Premium Programme conditions are met)" https://ftmo.com/en/faq/how-do-i-withdraw-my-profits/ |
| Fee, $100k 2-Step | **€540** list price (€439 promo); refundable with the first Reward | Homepage embedded JSON `"step_2":[… {"price":"540","discounted":true,"discounted_price":"439","discounted_price_tooltip_text":"Special Deal! $100,000 FTMO Challenge for €439 – only if you don't already have one active."`. Refund: "the paid fee is refunded with your first Reward withdrawal" https://ftmo.com/en/faq/what-fees-do-you-charge-and-are-they-recurrent/ |
| Fee, Swing variant | ⚠ not stated whether Swing costs the same as Standard | Other price tooltips say "Applies to FTMO Standard accounts only" |
| Payout timing | First request on day 14 after the first trade, all positions closed | "You can request a Reward claim in the Account MetriX on the 14th or any following day after the first placed trade on the specific account. All open positions and pending orders must be closed." (withdraw FAQ) ⚠ The cadence of later cycles is not stated beyond this. |
| News and weekend holding | No restriction on Swing | "The FTMO Swing account type does not have any restrictions on trading during news releases or on holding positions overnight (longer than 2 hours after market close) or over the weekend." (swing FAQ) |
| Scaling plan | +25% every 4 months, up to $2M | "Minimum of 4 months … At least 10% net simulated profit … At least 2 processed Rewards within that same 4-month period … Positive account balance"; "Increase your FTMO Account size by 25% every 4 months"; "90% share … (valid for 2-Step only)" https://ftmo.com/en/reward-growth-and-scaling-plan/ |
| Capital cap | $400k per trader or strategy (€320k equivalent) | "the total capital allocation across all accounts is limited to $400,000 per trader or strategy (prior to any scaling)" https://ftmo.com/en/faq/how-many-accounts-can-i-have/ |
| Server limits | 200 orders at a time, 2,000 positions per day | "platform servers have 200 orders at a time and 2000 max positions per day limitation, just as the limited acceptance of the server messages (orders and order modifications such as updates of TP/ SL and updates of limit orders)" https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/ |
| Switching account type | Swing to Standard allowed, Standard to Swing not | FAQ swing: "Change from Standard to Swing: Not allowed / Change from Swing to Standard: Allowed" |

**Note on 8 Oct 2026 change:** from 12 Oct 2026 a "Consistency rule" replaces the Best Day Rule, but only for 1-Step. 2-Step / Swing shows "Consistency –" in the comparison table. (https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/)

## 8. Platforms and EAs

- **Platforms in general** (https://ftmo.com/en/faq/which-platforms-can-i-use-for-trading/): "MetaTrader 4, MetaTrader 5, cTrader or TradingView."
- **Stocks on platforms:** the SPCX listing says it "is now available for trading across all our platforms (MT4, MT5, and cTrader) and servers" (trading update 18 Jun 2026).
  - ⚠ TradingView is not named for stocks.
  - ⚠ DXtrade is not mentioned anywhere and does not appear to be offered.
- **EAs** (FTMO instruments FAQ): "we have no reasons for limiting or restricting your trading strategy, whether it's discretionary trading, algorithmic trading, EAs, etc. … You can trade all the instruments and assets that are available in your trading platform (Forex, Indices, Commodities, Stocks, Crypto,…)."
  - EAs are therefore allowed on stocks, including on MT5. The 200/2,000 server limits and the third-party-EA capital-allocation warning apply.
- **Server time:** "MetaTrader 4, MetaTrader 5 = GMT+2 +DST" (account-specifications FAQ).
