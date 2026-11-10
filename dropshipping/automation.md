# Automation (iron law 16, overlay §8)

Rule: a process is automated only after a stable runbook exists from manual runs. Fulfillment is the one day-one exception. Every automation ships with a spend ceiling, a kill switch the operator can hit alone, an anomaly alert, a two-week human-review window, and a runbook for running it by hand.

| Process | Status | Cap | Kill switch | Alert | Review window | Runbook |
|---|---|---|---|---|---|---|
| Fulfillment (order forwarding, tracking sync, supplier payment) | planned day 1 via chosen platform; tested on one real order before any ad spend | prepaid balance only | disconnect app / pause auto-order | order not forwarded within 24h | 14 days | runbooks/fulfillment.md (to write at M0) |
| Daily reconciled reporting | manual until month 2 | n/a | n/a | n/a | n/a | runbooks/daily-numbers.md (to write) |
| Creative pipeline | manual until month 2–4 | n/a | n/a | n/a | n/a | to write |
| Ad rules | manual until month 4+ | n/a | n/a | n/a | n/a | to write |

Operator code literacy milestone: not started. Each script the program writes ships with a plain-language explanation and is run by hand first.
