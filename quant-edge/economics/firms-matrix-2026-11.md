# Firm matrix, November 2026 (Rules Keeper, Department F) — IN PROGRESS

Fetch date 2026-11-06 unless a cell says 2026-11-03 (letters agent's fetch, `economics/firm-pages-fetched-2026-11-03.md`).
Labels: **V** = verified on the firm's own page (URL + date in the clause file), **S** = snippet / third-party / inherited only,
**U** = unknown (not found). Quoted clauses: `economics/firm-clauses-2026-11/<firm>.md`. Archive (not in the repo):
`~/quant-edge-data/firm-pages/2026-11-06/<firm>/<slug>.txt`. lucidtrading.com is blocked (403, D-007): Lucid cells are S or U.

Status: skeleton written 2026-11-06; firms are filled in one by one below.

## 1. FTMO (CFDs; plan = 2-Step $100K Swing, with Standard and FTMO Futures where they differ)

Sources: `firm-clauses-2026-11/ftmo.md` (all fetched 2026-11-06). V = verified, S = snippet/inherited, U = unknown.

| item | 2-Step Swing 100K (FTMO Account) | label |
|---|---|---|
| automation | "algorithmic trading or EAs" allowed; third-party EA risks the allocation cap; ≤ 200 orders at a time, 2,000 positions/day, > 2,000 server requests/day forbidden; unattended not addressed (no oversight clause found) | V |
| VPS / VPN / own code / remote signal | VPN/VPS "generally allowed" (not geolocated to the US); no own-code requirement; remote signal not addressed | V |
| multi-account | number of Challenges not capped, but $400,000 Initial Simulated Capital "per client, per strategy and per ultimate beneficial owner" (T&C 5.8.5(c), 6.3); identical/similar trading across accounts above the cap → suspension; Prime raises the cap to $600,000; one Instant Account; 3.14.2 "unusually large number of Orders" → cool-down | V |
| fee / reset / monthly | €540 one-time (promo €439, Standard only); refunded with the first Reward; no reset product named; no monthly fee | V |
| profit target / min days | 10% + 5%; 4 trading days per phase; none on the FTMO Account | V |
| consistency | none on 2-Step (1-Step 50%, Instant 30%); soft cross-account size/count rules T&C 7.5; FTP bans spreading profit across days to dodge Best Day/Consistency | V |
| drawdown | 10% static on equity (Balance + open P/L ± swaps − commissions) | V |
| daily loss and clock | 5% of initial capital below the balance at 00:00 CE(S)T, checked on equity incl. floating P/L and swaps | V |
| news | Swing exempt; Standard FTMO Account ±2 min, incl. SL/TP/pending, only on affected symbols (USD list: Fed rate, NFP, unemployment, Advance GDP, FOMC minutes, CPI) | V |
| gap-trading clause | FTP forbids *opening* trades ≤ 2 h before a ≥ 2 h close or when major news is scheduled; applies to Swing (Swing exempts holding only) | V |
| holding / flat-by / day boundary | Swing: holds overnight and weekends; Standard: no holds through breaks > 2 h; trading day 00:00–23:59:59 CE(S)T | V |
| inactivity | 30 days without a trade → termination right (13.2.3(a)); loss of 8–10% held > 30 days (13.2.3(b)); Futures: 30-day warning + 30 days → closed | V |
| payout | first Reward request ≥ 14 days after first trade; 80% default, 90% with Scaling Plan or Premium; rollover allowed | V |
| scaling | +25% every 4 months (10% net profit, 2 Rewards in the 4 months) up to $2,000,000 across FTMO Accounts | V |
| closure after N payouts / Live | none found; funded-stage agreement unread | U |
| countries / Israel | Israel not restricted (excluded: Iran, Syria, Myanmar, N. Korea + residency table) | V |
| payout rails (Israel) | bank wire, Visa Direct/Mastercard Send ≤ $20,000, Skrill ≤ $3,000, crypto; FTMO charges no fee; Israeli-specific rail not stated | V (rail list) / U (Israel) |
| platforms / API | MT4, MT5, cTrader, TradingView; MT server time GMT+2 +DST; no separate fee | V |
| termination | 7.8 one FTP finding on any Account → all Agreements; 13.2.4 either party on 5 business days without cause; T&C changes on 7 days' notice | V |
| funded-stage agreement | FTMO Account Terms and Conditions unlocked only after KYC in the Client Area; sample only by email (contact forbidden) | U |
| swaps | charged nightly; table `research/sweep/ftmo-swaps-2026-11-04.csv` (e.g. US500.cash long −185.14 pts, GER40 −509.88, JP225 −962.27, BTCUSD −30%/yr both sides) | V (2026-11-04) |

**FTMO Futures (new product, not on the inherited matrix).** "Automated trading is permitted" (no HFT/latency arbitrage); "Copy trading across accounts registered to the same trader is permitted"; up to 3 Sim-Funded accounts (Growth + Pro) and no capital cap; trading day 6:00 p.m. ET → 4:10 p.m. ET; no position or resting order past session end; EOD trailing drawdown locking at initial capital; daily loss $1,000–$3,000; cross-operator hedging banned; Futures T&C document not read (U). All V except the T&C.

## 2. Topstep (CME futures; plans 50K / 100K / 150K Trading Combine → XFA Standard or Consistency; LFA)

Sources: `firm-clauses-2026-11/topstep.md` (help-center Markdown + Terms of Use dated 2026-11-04, all fetched 2026-11-06).

| item | Combine / XFA (50K · 100K · 150K) | label |
|---|---|---|
| automation | own bots via TopstepX/ProjectX API on Combine and XFA; no HFT; "no exceptions ... for errant trades or malfunctions"; LFA: no API, no automation | V |
| VPS / VPN / remote signal | "All trading activity must originate from your personal device"; VPS/VPN/remote servers prohibited; "your server can watch and record, but it cannot trade"; ToU §28 now also bans "remote access tools" used to mask location | V |
| API fee | $29/month, $14.50 with code "topstep"; one key covers every account on the profile | V (new) |
| multi-account | Combines unlimited; ≤ 5 active XFAs (1 for Shoulder Tap); one profile; copier Lead = lowest MPS, Combine/XFA only; cross-account hedging and coordinated trading banned | V |
| fee / reset / activation | $49·$99·$199/month + $149 activation, or $95·$149·$229/month no activation; resets same; Back2Funded $599·$699·$829 | V |
| profit target / min days | $3,000·$6,000·$9,000; ≥ 2 days (best day < 55% of target) | V |
| consistency (eval / funded) | Combine 55% best-day target; XFA Standard none; XFA Consistency 40% (largest day ÷ net profit), reset after each payout | V |
| drawdown | MLL $2,000·$3,000·$4,500, trails the end-of-day balance, enforced in real time incl. unrealized P&L; XFA starts at $0, MLL locks at $0 once balance reaches +MLL (+$2,000 on 50K); after first payout MLL = $0 permanently | V |
| daily loss limit | optional (at purchase $1,000·$2,000·$3,000, fixed; or personal DLL); soft breach, not a violation; clock 5:00 PM–3:10 PM CT; automatic in LFA | V (changed) |
| news | **new**: Tier-1 window ±5 min (CPI, FOMC decision + press conference, NFP, PPI): no new opening mini positions in equity index and metals, micros capped (3·6·9), pending orders do not fill; energies/rates/FX unaffected; plus no full MPS into major news | V (new) |
| min hold | none stated; sim-fill exploitation ("tight brackets or auto-breakeven") banned | V |
| flat-by / day boundary | flat by 3:10 PM CT (auto-flatten from 3:08, ~10 s before close); trading day 5:00 PM CT (= 18:00 ET) → 3:10 PM CT; no session-to-session holds | V |
| inactivity | XFA with no trading > 30 days may be closed | V |
| payout | Standard: 5 winning days ≥ $150; Consistency: 3 days + 40%; 50% of balance per request, caps $2,000/$3,000 · $3,000/$4,000 · $5,000/$6,000 (doubled under a limited-time offer if DLL bought at checkout); min $125; 90/10 | V |
| closure / Live | Live call-up closes all XFAs (accept or close); one LFA; no API on LFA; LFA size = average of XFAs | V |
| max contracts / scaling | 5·10·15 minis (10:1 micros); XFA Scaling Plan by balance; volatility caps (CL/GC 3·6·9, SI/HG/PL 0) | V |
| countries / Israel | eligibility by citizenship and residency; Israel on neither list | V |
| payout rail (Israel) | Wire/SWIFT, 5–10 business days, $30; Wise only China/Canada/UK | V |
| platforms | TopstepX (own), API via ProjectX; Quantower via TopstepX credentials; L1 data included, L2 $38/month | V |
| termination | ToU §27: one Prohibited Conduct finding → withdrawals from all other accounts forfeited; Terms change "effective upon such notice" | V |

## 3. MyFundedFutures (CME futures; 50K plans shown: Rapid · Rapid EOD · Builder · Pro)

Sources: `firm-clauses-2026-11/myfundedfutures.md` (all fetched 2026-11-06).

| item | Rapid 50K | Rapid EOD 50K | Builder 50K | Pro 50K | label |
|---|---|---|---|---|---|
| automation | own-settings automation allowed if it does not "exploit the favorable fills"; no HFT; tight brackets banned; silent on unattended / VPS / remote signal | same | same | same | V (silence = U) |
| multi-account | ≤ 10 evals; ≤ 5 sim-funded if only 25K/50K, 3 if any 100K/150K; copy trading "across all account types"; Terms §23.1.3.3 bans using multiple accounts to "hedge, mirror, copy, or coordinate trades in a manner that provides an unfair advantage or manipulates simulated results" | max 3 funded | max 1 funded | as Rapid | V |
| fee (one-time, since 2026-08-25) | $209 list / $125 promo | $225 / $135 | $153 / $92 (MLL $1,500 option $125) | $265 / $159 | V |
| activation / monthly | $0 / none | $0 / none | $0 / none | $0 / none | V |
| target / min days | $3,000 / 2 | $3,000 / 4 | $3,000 / 1 | $3,000 / 2 | V |
| consistency eval / funded | 50% / none | 30% / none | — / 50% at payout | 50% / none | V |
| drawdown eval → funded | EOD $2,000 → **intraday trailing $2,000 from the equity high-water mark**, locks at $100 | EOD → EOD trailing $2,000, locks at $100 | EOD $2,000 (or $1,500) both stages | EOD $2,000; static at $50,100 after first payout | V |
| daily loss | none stated | none stated | $1,000 soft pause | none stated | V |
| news (funded) | no positions or orders ±2 min around FOMC, FOMC minutes, Employment, CPI (+EIA/ag) | same | allowed | same as Rapid | V |
| flat-by / day boundary | trading day 6:00 PM → 4:10 PM ET; auto-close 4:10 PM ET (holiday early closes: trader must close) | same | same | same | V (new: was U on 2026-11-03) |
| inactivity | 7 calendar days without a trade → may close as breach | same | same | same | V |
| payout | buffer $2,100; daily; min $500; 90/10 | buffer $2,100, then +$500 net per payout; daily; uncapped | 48 h after first trade; $2,000 cap; ≤ 5 sim payouts; 80/20 | 14 days; buffer $2,100; min $1,000; $100,000 per user; 80/20 | V |
| Live / closure | automatic Live at $10,000 net profit in one session; accounts "combined into one Live account"; all sim accounts suspended | Live transition (merge) | 5 sim payouts then Live path | review after 3 consecutive payouts / $100k cap / $20k profit | V |
| max contracts | 5 minis / 50 micros | 3 / 30 | per plan page | per size | V |
| countries / Israel | not restricted | | | | V |
| payout rail (Israel) | not published (processors Riseworks, Wise, Confirmo named in Privacy Policy 2026-11-03) | | | | U |
| platforms | Tradovate, NinjaTrader, TradingView, Volumetrica, Quantower, ATAS, DeepChart; copier Tradesyncer / Tradovate group copier | | | | V |
| discretion | Terms amend "at any time, with or without notice"; profits from prohibited practices confiscated | | | | V |

## 4. TradeDay (CME futures; 50K Quick Pay Intraday / Quick Pay EOD / Fast Pass EOD; Funded Sim → Funded Live)

Sources: `firm-clauses-2026-11/tradeday.md` (Freshdesk articles + Terms of 2026-08-11 + home, fetched 2026-11-06).

| item | Quick Pay 50K | Fast Pass 50K | label |
|---|---|---|---|
| automation | own ATS only inside NinjaTrader, Tradovate, TradingView, Jigsaw or Quantower; "We do not make platform APIs available"; Tradovate API not exposed; third-party-bought bots forbidden; > 200 trades/day forbidden; "If multiple users are making the same trades" → all accounts shut | same | V |
| VPS / VPN / remote signal | VPS not allowed; trade from the registered address; IP checks at Funded Live, payouts and the $10k review (a "similar" trading day from the registered location); remote signal not addressed | same | V |
| multi-account | ≤ 10 accounts total (≤ 10 eval, ≤ 5 Funded Sim active, rest queued, ≤ 5 Funded Live); one broker; one user per household; copier allowed across own TradeDay accounts and from a personal account elsewhere | same | V |
| fee / reset / activation | $131/month list, $59 promo; reset $59; no activation fee | $175 list / $79 promo | V (promo prices move) |
| target / min days / consistency (eval) | $3,000; 5 days; 30% | $3,000; 3 days; 45% | V |
| drawdown | eval intraday ($2,000) or EOD option; **Funded Sim always intraday trailing**, real-time, trails to starting balance | EOD trailing in eval and Funded Sim | V |
| daily loss | none stated | none stated | V |
| news | auto-liquidation 2 min before → reopen 2 min after FOMC (decision, minutes), CPI, NFP for all products; EIA for energy, crop reports for ags; tier-1 profits not returned on loss of a funded account | same | V |
| min hold | microscalping review if most trades or most profit come from holds under ~5–10 s; order-splitting flagged | same | V (new) |
| flat-by / day boundary | flat 10 min before the product's close; auto-liquidation at 3:50 PM CT; trading day 5:00 PM CT (= 18:00 ET) → next-day close; overnight session allowed, no hold through the close | same | V (new: was U) |
| inactivity | 30 days dormant → may be offboarded; Tradovate archives after > 1 month without login | same | V |
| payout | no buffer; min $250; 1 day to payout; split 50/50 below $4,000 profit, 80/20 above; 90/10 Funded Live | 5 profitable days × $100; min $250; 80/20 sim, 90/10 live | V |
| Live / closure | review at $10,000 gross profit per account: account paused, excess above threshold removed, usually moved to Funded Live; no new purchases while in Funded Live | Fast Pass route to Funded Live | V |
| max contracts | 5 (50 micros) | 1 → +1 per $2k EOD profit, max 2 minis (per card) | V |
| countries / Israel | not restricted | | V |
| payout rail (Israel) | Riseworks: international wire $15 or crypto (L1 $2.5 + gas, L2 free) | | V |
| termination | Terms: Prohibited Conduct → withdrawals from all other accounts forfeited | | V |

## 5. Lucid Trading (CME futures; LucidPro · LucidFlex · LucidDaily · LucidDirect · LucidMaxx) — S/U only (lucidtrading.com 403)

Sources: `firm-clauses-2026-11/lucid.md` (inherited page quotes of 2026-10-11 + third-party snippet dated 2026-11-04).

| item | value | label |
|---|---|---|
| automation | "Automated trading systems and trade copiers are permitted"; no HFT; trader liable for errors | S |
| VPS / VPN / remote signal | no rule found | U |
| multi-account | per household: 10 evals, 5 funded, 10 total, 5 Live; hedging banned across own accounts, other users **and other firms** | S |
| fees | one-time purchase, no subscription; amounts unknown | S / U |
| drawdown | EOD on Pro/Flex/Direct; LucidDaily funded intraday by default | S |
| daily loss | optional at checkout; soft; LucidScale 60% of peak EOD balance on some plans | S |
| consistency | Pro 40% funded; Flex 40% eval; Daily 30–50% eval; Direct 20% | S |
| news | allowed except LucidDaily funded: flat ±1 min around US red-folder events (hard breach) | S (window new) |
| min hold | > 50% of profit from holds ≤ 5 s → flagged | S |
| flat-by / day boundary | 4:45 PM ET (Rithmic Live 4:15 PM ET); resume 6:00 PM ET | S |
| inactivity | not found | U |
| payout | min $500; 5 payouts before Live on Pro/Flex/Direct | S |
| Live / closure | Live at risk-team discretion; remaining sim accounts closed; auto-move after 24 h; Live starts at $0 | S |
| countries / Israel; payout rails; platforms/fees | not read | U |

## 6. Bulenox (conditional; CME futures via Rithmic) — unchanged since 2026-11-03

| item | value | label |
|---|---|---|
| automation | allowed only after "reviewed and approved by the Bulenox management team"; $100/month API fee "does not constitute approval"; "refuse to claim any profit" on suspected abuse | V |
| multi-account | up to 5 Master-level accounts; one profile per household | V |
| drawdown / daily loss | trailing (no scaling) or EOD (scaling + soft daily loss limit) | V |
| news | allowed | V |
| flat-by / day boundary | 3:59 PM CT; trading day 5:00 PM → 4:00 PM CT; no overnight | V |
| Live | Funded Account after 3 payouts at Bulenox's discretion; decline → Master closed | V |
| countries / payout rails / FAQ answers | not read | U |
