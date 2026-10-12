# W4 · G1: Volatility risk premium (VIX term-structure carry)

**Verdict: STOP at the gate. No allowed firm offers a tradable volatility product, so no backtest was run and no variant was counted.**

None of the five safe-list firms lists a VIX product: FTMO, MyFundedFutures, Lucid, Topstep and TradeDay. That covers a VIX CFD, VX/VXM futures, and VXX/SVXY/UVXY CFDs. We could not get a symbol-level list for Blue Guardian or Crypto Fund Trader. Both are off the safe list anyway (D5 grades: C and D), so they could not carry a fleet even if they did list one.

- `agents/prereg/G1.csv` holds only the header. **0 of 15 variants were used**, so wave 4's N falls by 15 if no one else uses G1's budget.
- Checked 12 Oct 2026 with `agents/daily/w4-vrp/symbol_gate.py`. The page excerpts are in `agents/daily/w4-vrp/evidence/`.

## Step 1: the gate, firm by firm

| Firm | D5 grade | Source (firm's own page) | What it lists | VIX / VX / VXM / VXX / SVXY / UVXY? |
|---|---|---|---|---|
| **FTMO, CFD** | B | [ftmo.com/en/symbols](https://ftmo.com/en/symbols/), data from `ftmo.com/wp-json/ftmo/symbols` | 166 symbols. Forex 28, Exotics 15, Metals 9, Cash CFD 25 (indices, oil, gas, DXY, softs), Crypto 30, Equities 59 (single stocks only, no ETFs) | **No.** Zero matches in any symbol's code, name or fields. The `expiringContracts` list is empty. |
| **FTMO, Futures** | B | [Which instruments can I trade with FTMO Futures?](https://ftmo.com/en/futures/faq/which-instruments-can-i-trade-with-ftmo-futures/) | "30 instruments… 19 mini (E-mini) contracts and 11 micro contracts", all CME Group products | **No.** Also: "FTMO Futures does not allow positions to be held over the market closure… automatically liquidated/flattened at the 4:10 pm ET close." |
| **Topstep** | B | [When and What Products Can I Trade?](https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade) (updated 13 Jul 2026) | "Every tradeable CME Group product": CME, CBOT, NYMEX and COMEX | **No.** Also: "All positions must be closed by 3:10 PM CT every weekday… No swing trading." |
| **MyFundedFutures** | B− | [Futures Instrument List](https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list) (24 Aug 2026), plus the help-center search for "VIX" | CME, COMEX, CBOT and NYMEX tables | **No.** The search returns "We couldn't find any articles for: VIX". Trading hours run "6:00pm EST through 4:10pm EST". |
| **Lucid** | B− | [Approved Products and Commissions](https://support.lucidtrading.com/en/articles/11508978-approved-products-and-commissions) (26 Aug 2026) | 34 symbols, all on CME, CBOT, NYMEX or COMEX | **No.** |
| **TradeDay** | B− | [What are the permitted products guidelines?](https://tradeday.freshdesk.com/en/support/solutions/articles/103000008862-what-are-the-permitted-products-guidelines-) | "TradeDay only allows its traders to trade the CME Group futures products, specifically those listed on the CME, CBOT, COMEX, and NYMEX." | **No.** |
| Blue Guardian (CFD) | C, not on the safe list | [Platform Rules](https://help.blueguardian.com/en/articles/9661525-platform-rules) (21 Aug 2026), plus the help-center search for "VIX" | Asset classes only: "Forex (FX) Indices Gold & Commodities Cryptocurrencies". No public symbol list. | **Not found.** The search returns "We couldn't find any articles for: VIX". We cannot say more without a platform login. |
| Crypto Fund Trader | D, not on the safe list | [cryptofundtrader.com/faq](https://cryptofundtrader.com/faq) | "556 Cryptocurrencies 106 Forex 15 Indices 22 Commodities 25 Stocks". The 15 indices are not named. | **Not found.** `help.cryptofundtrader.com` was blocked by the session's egress proxy (CONNECT rejected). We did not route around it, per the wave rules. |

### Why VX/VXM fails twice at the futures firms

1. **The exchange is wrong.** VX and VXM trade on the Cboe Futures Exchange (CFE). All five futures programmes (Topstep, MFFU, Lucid, TradeDay and FTMO Futures) only permit CME Group products, and none lists a CFE contract.
2. **The holding period is impossible.** Term-structure carry earns roll yield by holding a short-vol position for days or weeks. All five programmes force you flat every day: Topstep at 3:10 PM CT, MFFU and FTMO Futures at 4:10 PM ET, and Lucid and TradeDay by session rules. A carry trade that must be closed every evening cannot collect the roll. So even if one of these firms added VX, the documented rule could not run there.

### What could change the verdict (not pursued)

- **FTMO adds a VIX CFD or a volatility ETF CFD.** FTMO is the only safe-list firm that allows overnight holding. Re-run `symbol_gate.py` to check. The FTMO symbol API is the one-line test.
- **Blue Guardian or CFT turns out to list a VIX CFD.** This would not help the fleet. Blue Guardian is grade C (one account per challenge level, the Guardian Shield, and F2's finding that it needs Sharpe ≥ 2.5 at every volatility level). CFT is grade D (ToS §14.2: "does not guarantee the payment").
- **A proxy on index CFDs.** One example: hold FTMO's US500.cash only when VIX < VIX3M. This is a contango-timed equity exposure, not the volatility premium itself. It is mostly equity beta, would need its own pre-registration and beta benchmark, and is close to what G2 already covers. G1 does not propose it.

## Step 2: not run

Per the brief ("If none does, write the report saying so and stop. Do not backtest something no allowed firm can trade"):

- no variants were pre-registered and no data was downloaded;
- no Sharpe, t, bootstrap, drawdown or $/slot figures exist for G1;
- the wave-4 bar (z 3.5914) is unaffected, and G1 used **0** of its 15-variant budget.

No sub-agents (verifier or red team) were used, because nothing looked promising enough to need them.

## Files

- `agents/daily/w4-vrp/symbol_gate.py` fetches every source above, searches for VIX, VX, VXM, VXX, SVXY, UVXY, "volatility index", Cboe and CFE, and writes the evidence files. It only makes plain GET requests to public pages, with no logins.
- `agents/daily/w4-vrp/evidence/*.txt` holds the HTTP status, a product-list excerpt and every pattern match for each source. The only matches are the two help-center searches echoing the query back with "couldn't find any articles for: VIX".
- `agents/prereg/G1.csv` is header only, because no variants were registered.
