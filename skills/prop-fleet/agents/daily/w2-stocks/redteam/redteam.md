# E1 red team (wave 2, 2026-10-11)

Scope: E1_rules.md, stocks.py, data.py, the FTMO symbol JSON and pages, and independent re-computations in
`redteam/rt_checks.py` (output in `redteam/rt_checks.txt`). I did not edit the engine or the prereg files.

## Verdict
**The negative conclusion stands.** I found no bug that suppresses gross returns or inflates costs. The gate
needs an OOS net t ≥ 3.56 over about 11.8 years, which is a net Sharpe of about 1.04. The best **zero-cost** OOS t of any
variant is 2.66 (E1-09 B, which turns over 252×/yr), and every other variant is at 1.9 or below. So no cost model, swap
reading or lag choice can make a variant pass. E1-05, E1-06 and E1-11 (PEAD and STACK) are not in results.csv yet.

## Engine audit (stocks.py)
- **Lag** (L268, L293). `W.shift(1+lag)` means weights set at close t earn r_{t+1} at lag 0. Correct. The E1-01 look-ahead tests give 20/20.
- **Signs.** `rank_w` (L82–87) puts the highest signal long.
  - E1-01/02/03 use the signal −(5-day return), so losers are long. Correct.
  - E1-04 puts weight ∝ (median − rank) on the lower half. Correct.
  - E1-10 uses −(overnight) on the intraday leg, so names with high past overnight returns are short intraday. Correct.
- **Overnight/intraday split** (L41–47). The dividend factor is applied to the open, so (1+on)(1+id) = 1+r. Correct.
  - No open falls outside [L, H] (the bad-open count is 0).
  - About 0.3–1.3% of stock-days have exactly zero overnight return, which is harmless.
- **Swap** (L278, L287). It is charged on the positions held over each close, times the calendar nights. The OOS mean is 1.4528 nights/day against 365/252 = 1.4484, so including holidays adds only +0.3%. Swap is correctly 0 for the intraday-only E1-10.
- **O/I costs** (L282). Each day costs 2 × Σ|w| × (half-spread + 2 bp). That matches the spec: a flat book enters and exits every day.
- **Hedge** (L292–299). A short US500 receives +0.42%/yr, and the 1.3% dividend is removed from SPY total return. Consistent with the spec.
- **Weekly holding.** Constant weights within a week imply daily rebalancing. A buy-and-hold drift simulation of E1-02 A gives an OOS gross t of 1.22, against 1.17 with constant weights. Negligible.
- **Events.** PEAD enters at the close of d0+1. Its sign uses only the abnormal returns of d0 and d0+1. GAPVOL enters at the close of day t. Holding is 20 days, from close e to close e+19. Correct.
- **Minor, no effect on the verdict:**
  - The worse lag is picked on the OOS mean (L418–419). The spec only says "worse lag", so this is fine, and it is conservative.
  - The beta in `resid` includes the same day t. That is allowed: it uses no information after close t.

## Independent re-computation
- **E1-01 rebuilt as an equal-weight quintile long/short:** IS Sharpe 1.30 (t 5.17), OOS 0.53 (t 1.81). This matches the engine (1.36 / 0.48).
- **Gross return by year:** it was strong from 1999 to 2011 and has been near zero since 2012, apart from 2020 (+23%) and 2026.
- **LPS overnight persistence, decile long/short on 21-day overnight returns:**
  - overnight leg: IS Sharpe 3.22, OOS 0.47;
  - intraday leg: IS −2.21, OOS −0.50;
  - by year, it earned 15–35%/yr before 2011 and about 0–8% from 2012.
- **Literature fit.** This is the documented post-publication decay of short-term reversal in large caps and of the Lou–Polk–Skouras overnight/intraday effect. An OOS gross Sharpe of 0.2–0.8 is plausible. The engine reproduces the strong historical effect, which is evidence against a hidden sign or lag bug.
- **No-swap run** (spread and commission kept, OOS t at lag 0 / lag 1):
  - E1-04 B: 1.26 / 1.04;
  - E1-07 B: 1.40 / 0.86;
  - E1-02 A: 0.07 / −0.47;
  - E1-03 A: 0.07 / 0.06;
  - E1-01 A: −0.60 / −0.66.

## Swap interpretation
- **FTMO's own wording.** FTMO's blog says: "In the specifications … a swap is stated in points per lot." For stocks `contractSize` is 1 and `digits` is 2, so 1 point = $0.01 per share per night.
- **The same semantics hold elsewhere in the same JSON:**
  - EUR/USD long −9.41 points (digits 5, lot 100k) is about $9.41/night, or about 2.9%/yr. That is a sensible rate differential plus markup.
  - US500 −177.1 / +8.94 points is −8.4% / +0.4% per year.
- **The points scale with price.** They imply an almost constant 7.8–8.7% (long) and 6.2–6.9% (short) per year across all 46 names. They are derived from a percentage rate, and the dividend is not netted per stock. So total-return accounting plus swap is the right model, with no double count.
- **Implied markup.** About 7.5%/yr each side. That is punitive but internally consistent.
- **Not found.** No FTMO page gives a worked stock-swap example or a % figure. A web search found nothing FTMO-specific. No host was blocked.
- **Not confirmed.** Which weekday carries the triple swap. It does not matter, because the calendar-night total is the same.
- **Bottom line.** Even with no swap at all, nothing passes.
