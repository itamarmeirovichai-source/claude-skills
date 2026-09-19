# Apex rule values used by the model

Collected from public sources, September 2026, after the firm's March 2026 rules
change. **Sources disagree on several values.** Everything marked ⚠ must be
confirmed against the firm's own help center before money is spent. The model in
`scripts/apex_model.py` reads these numbers from its `PLANS` table — change them
there when the firm changes them.

## 50K EOD Performance Account

| Rule | Value | Confidence |
| --- | --- | --- |
| Trailing drawdown | $2,500 | corroborated |
| Safety net | $52,600 (`start + dd + 100`) | corroborated |
| Floor locks at | $50,100 (`start + 100`), permanently | corroborated |
| Evaluation profit target | $3,000 (6% of balance) | corroborated |
| Evaluation time limit | 30 calendar days, expires 6:00 PM ET day 30, no extension | corroborated |
| Minimum trading days (evaluation) | none on post-March-2026 accounts | corroborated |
| Qualifying days for a payout | 5, each with profit ≥ $200 | corroborated |
| Consistency rule | 50% ⚠ (some sources say 30%) | conflicting |
| Minimum payout | $500 | corroborated |
| Payout ladder | 1500 / 1500 / 2000 / 2500 / 2500 / 3000 | corroborated |
| Lifetime total | $13,000 | derived |
| Payouts before closure | 6, then the account closes | corroborated |
| Profit split | 100% on accounts opened on or after 1 Mar 2026 | corroborated |
| Contract limit | 10 (half until the safety net) | corroborated |

50K **Intraday** ladder differs: 1500 / 2000 / 2500 / 2500 / 3000 / 3000 = $14,500.
Intraday trails from the intraday high rather than the close, which is worse for a
strategy that holds toward a distant target. EOD is the default recommendation.

## 150K account — treat every number here as provisional

| Rule | Value | Confidence |
| --- | --- | --- |
| Trailing drawdown | $5,000 ⚠ (one source says $4,000; the quoted $155,100 safety net implies $5,000) | conflicting |
| Safety net | $155,100 | corroborated |
| Evaluation profit target | $9,000 (6%) | corroborated |
| Qualifying day minimum | $350 | corroborated |
| Per-payout cap | rises from $2,500 to $5,000 across six ⚠ (another source caps every cycle at $3,500) | conflicting |
| Lifetime total | unknown — the model assumes a conservative $18,000 | assumption |

Because the ladder is unresolved, the 150K figures throughout the report are a
**conservative** estimate. The real number is likely higher, not lower.

## Costs

| Item | Value |
| --- | --- |
| Evaluation fee | one-time, not a subscription, since March 2026 |
| List price | $147–$517 by account size |
| Discounted | commonly 50–90% off; ~$35–50 for a 50K |
| Activation fee (funded) | $79–$149, promo codes do not apply |
| Model assumption, 50K | $40 evaluation + $85 activation = $125 per attempt |

Never buy at list price. Across ~300 evaluations over eight years the difference
between $40 and $147 is about $32,000.

## Account and copy-trading limits

| Firm | Max accounts | Copy trading |
| --- | --- | --- |
| Apex | 20 | permitted across all 20 |
| Take Profit Trader | 10 funded | only 5 copy-traded |
| Tradeify | 5 | restricted |
| Topstep | restricted | restricted |

Apex is the only firm on which a 10–20 account copy-traded plan runs at all. That
is a concentration risk with no hedge: a rules change at one firm moves the whole
plan.

## Confirm before paying

1. The exact payout ladder for the plan and size you are buying, EOD and Intraday
   stated separately.
2. The 150K drawdown — $4,000 or $5,000.
3. The consistency rule percentage.
4. **Whether automated order copying from an external API is permitted, and through
   which tool.** Get this in writing. If the bot's order path is not permitted,
   accounts close and payouts are voided — the only risk in the plan that is not
   bounded by fees.
5. What happens after the sixth payout: closure, or re-qualification.
