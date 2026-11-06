# quant-edge/data — manifest, spend ledger, licence register (no market data here)

Market data lives under `~/quant-edge-data/` (DATA_ROOT), never in the repository.

## Databento spend-ledger header (filled from Itamar's confirmation, Day 0 item 1)

| field | value | source |
|---|---|---|
| remaining credit (USD) | UNCONFIRMED | portal Billing page, read by Itamar |
| credit expiry date | UNCONFIRMED | same |
| signup date | UNCONFIRMED | same |
| DATABENTO_PLAN_CEILING_USD | not set (= min(94, credit − 20)) | PARAMETERS.md |
| DATABENTO_HARD_CAP_USD (portal monthly limit) | not set (= min(105, 0.85 × credit)) | PARAMETERS.md |
| pay-as-you-go state | unknown (ask: is a request beyond the credit refused when it is off?) | |
| key present in environment | no (2026-11-03) | `env` check, value never read |

Rule: before every paid request, `metadata.get_cost`, `get_record_count`, `get_billable_size` with identical arguments;
estimate row written first; submit only if est_usd ≤ min(ceiling − cumulative, monthly limit − month_to_date) − 1.
