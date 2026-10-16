# W3 · F2: volatility sizing and contract safety

**Verdict:**

- **The Sharpe needed rises as volatility comes down.** To earn $20k a year per $100K FTMO Swing slot, after every stress (F2-09: fat tails, gaps, volatility clustering, a daily-loss limit on equity, the firm's exact rules), a strategy needs:
  - net Sharpe **≈2.4 at 12% annual volatility**;
  - **≈1.9 at 15%**;
  - **≈1.5 at 20%**.
- **CFT is close to FTMO at low volatility, but its exact rules hurt it above 20%.** The binding rule is its $10k cap on profit per day or per trade.
- **Blue Guardian needs Sharpe ≥2.5 at every volatility level.** Its 4% daily limit and the Guardian Shield (open loss of −2% closes everything) do the damage.
- **The Sharpe-0 "lottery" mostly disappears under stress and in calendar terms.**
  - FTMO at 12% volatility: $1.2k a year per slot.
  - The chance of losing money in year 1 is 84%.
  - Even with no volatility cap, year-1 p10 is −$8.7k per slot.
  - It is not a business.

**Contracts.**

- None of the three firms sets a numeric volatility limit.
- FTMO's forbidden-practices list and its gambling article (linked from that list) call "overleveraging" and over-exposure gambling. FTMO says it monitors this, without a number, and its blog cites 1% risk as the professional norm.
- Blue Guardian treats margin use above 80% as gambling, and runs risk reviews at any stage.
- CFT bans "all-in" trading. To claim profits after a suspension, every trade needs a stop loss and at most 2% risk.

A diversified, stop-protected book at 15–20% annual volatility (about 1–1.3% daily) is defensible, but it is a judgement call. At 30% or more it is not.

**Sources.**

- Clause quotes: `agents/daily/w3-volrisk/clauses-*.md`.
- Model and tests: `agents/daily/w3-volrisk/` (21 tests pass).
- Pre-registration: `agents/prereg/F2.csv`. F2-01..11 were pre-registered before any run. F2-12..15 were added after the model red team, but before they were run.
- The run was finished in the director session after the F2 session stopped mid-run.
- Full tables: `agents/daily/w3-volrisk/tables.md`.
