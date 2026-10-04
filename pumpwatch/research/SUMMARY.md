# PumpWatch: Market & Regulation summary (one page)

*Market & Regulation dept., 2026-10-04. Details and sources: [competitors.md](competitors.md), [customers.md](customers.md), [pricing.md](pricing.md), [regulation.md](regulation.md). Desk research, not legal advice. Each file marks anything not confirmed from a source as UNVERIFIED. The department head re-checked the key claims below against their primary sources.*

## The 5 most important findings

**1. The biggest risk is permission to use the data. The market is not the main problem.** The social sources PLAN.md relies on are banned for this use by their own terms:
- **X:** the Developer Agreement (updated 2026-04-27) bans "conducting or providing surveillance or gathering intelligence, including … investigating or tracking X users". It also bans profiling people over "alleged or actual commission of a crime", unless X approves in writing.
- **Telegram:** its terms ban access to user content "for any purpose other than ordinary … use … as its user". Bot developers may not scrape "public group or channel contents". Using Telegram data for AI/ML is "firmly prohibited".
- **Reddit:** bans "surveillance purposes".
- **StockTwits** is the exception: its terms say it licenses data to financial institutions.

*Confidence: high on what the clauses say (read directly). How they apply to PumpWatch needs a lawyer.*

**2. The wedge is partially taken.**
- **Exchanges and regulators:** taken. Stockpulse sells social-media pump-and-dump surveillance covering Telegram, Discord and X to Deutsche Börse, Bursa Malaysia and Nasdaq's US market-surveillance team. Korea's exchange, India's SEBI and Hong Kong's SFC built their own tools.
- **Brokers and trading apps:** looks open. That means public social signals, plus market data, plus EDGAR filings, turned into a per-ticker warning before the dump. We found no one selling this.
- **Closest broker-facing product:** OTC Markets' Promotion flag. It is curated by staff, refreshed twice a day, and covers paid promotion only.
- **Most likely to close the gap fast:** Stockpulse, Nasdaq and OTC Markets.

*Confidence: medium (~60%). Not finding a competitor does not prove there is none.*

**3. Regulatory pressure is real and rising, but no rule requires social-media monitoring by name.**
- **What regulators are doing:** the FINRA 2026 Oversight Report names social-media "investment club" scams in small caps. FINRA opened a sweep of small-cap underwriters and omnibus firms (Oct 2025). The SEC set up a Cross-Border Task Force (Sep 2025). Nasdaq's $25M minimum IPO for China-based issuers was approved in May 2026.
- **What small firms pay:** fines of about $250k–$1.3M plus a mandatory consultant. Examples: Velox $1.3M (2025), Pictet $610k and Blue Ocean ATS $550k (2026), TradeStation $700k for pump-and-dump alerts it never escalated.
- **The usual failure:** surveillance not tailored to the firm's risks, and alerts not escalated to AML/SAR. Missing data is not the cause. The product therefore has to produce an **auditable escalation trail**, not just alerts.
- **Downside:** the tighter Nasdaq listing rules may shrink the pool of easy targets.

**4. The best first buyers are small and mid-size clearing and self-clearing firms with foreign omnibus or low-priced flow.**
- Firms already under a FINRA consultant order have a deadline and a budget.
- Next come retail apps, short-locate brokers (the least conflicted buyers) and banking-as-a-service platforms.
- Underwriters are under the most pressure, but they are conflicted and a reputational risk.
- The broker conflict of interest is real: brokers earn on pump volume and retail buyers carry the loss. The pitch is protecting **the firm's regulatory record**, not saving victims.

**5. Pricing must start lower than PLAN.md, and SOC 2 does not fit the budget yet.**
- Comparable tools small brokers buy cost a median of about $7k–$23k a year (Smarsh, Global Relay, Vanta). Enterprise AML platforms cost a median of about $123k–$182k (Unit21, NICE Actimize). These figures are crowd-sourced from Vendr.
- Recommended prices: a paid 90-day pilot at $1.5k–3k, then a small tier at $1.5k–3k a month (not up to $5k) and a mid tier at $5k–12k a month.
- A first SOC 2 costs about $25k–80k and takes 4–11 months, roughly the whole $30k budget. Defer it until a customer requires it.

## What this means for Gate A (go/no-go)

**Verdict: CONDITIONAL GO for Gate A's cheap work (calls and the paper backtest). NO-GO for any build or data collection until the data question is answered.**

1. **Bring the legal question forward.** Book the 1–2 hour lawyer session (planned for Gate B) during Gate A. The top questions: the scope of X's surveillance clause, any lawful path to Telegram, investment-adviser status, and GDPR Art. 10 / Israeli sensitive-data rules. Ask X and StockTwits in writing about commercial licensing for this use.
2. **Add a test to Gate A2: does the system still work without X and Telegram?** Run the 20-case paper backtest twice:
   - first with only market data, EDGAR filings and licensed or allowed social data (StockTwits, social evidence quoted in SEC/DOJ filings);
   - then with everything.
   If signals S1–S3 plus StockTwits alone give warnings at least 2 days ahead in about 10 of 20 cases, the business survives the terms problem. If not, Gate A fails on data access even if the customer pain is real.
3. **Change the call targets and script.** Start with clearing and self-clearing firms (customers.md §7). Ask every call:
   - Do you already license OTC Markets promotion data or Stockpulse?
   - Would derived signals with no raw posts be acceptable?
   - Would you pay for a $1.5k–3k pilot?
4. **Design defaults:** score tickers and anonymised clusters, not named people. Publish no public "pumped stocks" report naming people (defamation risk). Never trade on alerts.

**Overall confidence:** high that the problem and regulatory pressure are real. Medium that the broker wedge is open. **Low that the planned social data sources can be used legally as PLAN.md assumes.** That last point decides go/no-go, and only a lawyer and the platforms themselves can settle it.
