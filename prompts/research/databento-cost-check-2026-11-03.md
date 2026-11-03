# Databento cost check (2026-11-03, free metadata endpoints only, nothing downloaded)

Dataset GLBX.MDP3 (CME, CBOT, NYMEX, COMEX). Range 2010-06-06 to 2026-11-02 for ohlcv/trades/tbbo/mbp/statistics/definition; mbo and cmbp-1 from 2017-05-21. Continuous symbols `X.v.0` (volume-based roll). All numbers are what `metadata.get_cost` returned for the user's account.

## Unit prices (USD per GB, historical)

| schema | $/GB |
|---|---:|
| ohlcv-1s | 70.0 |
| ohlcv-1m | 70.0 |
| ohlcv-1h | 190.0 |
| ohlcv-1d | 190.0 |
| trades | 28.0 |
| tbbo | 28.0 |
| bbo-1s | 18.0 |
| bbo-1m | 18.0 |
| mbp-1 | 1.8 |
| mbp-10 | 0.5 |
| mbo | 1.8 |
| statistics | 1.0 |
| definition | 1.7 |
| status | 4.0 |

## Cost per root, full history

| Root | 1m bars ($) | 1m records (M) | 1d bars ($) |
|---|---:|---:|---:|
| ES | 20.94 | 5.74 | 0.050 |
| GC | 20.77 | 5.69 | 0.050 |
| CL | 20.71 | 5.67 | 0.050 |
| 6E | 20.59 | 5.64 | 0.050 |
| 6J | 20.41 | 5.59 | 0.050 |
| NQ | 20.30 | 5.56 | 0.050 |
| YM | 20.16 | 5.52 | 0.050 |
| 6A | 20.14 | 5.52 | 0.050 |
| HG | 19.40 | 5.31 | 0.050 |
| ZN | 19.22 | 5.26 | 0.050 |
| 6B | 19.21 | 5.26 | 0.050 |
| SI | 19.20 | 5.26 | 0.050 |
| 6C | 18.71 | 5.13 | 0.050 |
| ZF | 17.94 | 4.92 | 0.050 |
| ZB | 17.82 | 4.88 | 0.050 |
| NG | 17.29 | 4.74 | 0.050 |
| 6S | 16.70 | 4.58 | 0.050 |
| UB | 15.89 | 4.35 | 0.050 |
| PL | 15.14 | 4.15 | 0.050 |
| HO | 14.41 | 3.95 | 0.050 |
| ZT | 13.78 | 3.77 | 0.050 |
| RB | 13.75 | 3.77 | 0.050 |
| ZS | 13.41 | 3.67 | 0.042 |
| MGC | 13.40 | 3.67 | 0.049 |
| ZL | 12.49 | 3.42 | 0.042 |
| ZC | 12.04 | 3.30 | 0.042 |
| ZW | 11.67 | 3.20 | 0.042 |
| RTY | 11.25 | 3.08 | 0.029 |
| ZM | 11.25 | 3.08 | 0.042 |
| MNQ | 9.65 | 2.64 | 0.023 |
| MES | 9.64 | 2.64 | 0.023 |
| M2K | 9.14 | 2.50 | 0.023 |
| BTC | 6.97 | 1.91 | 0.028 |
| MCL | 6.59 | 1.81 | 0.016 |
| MBT | 5.09 | 1.39 | 0.017 |
| LE | 5.03 | 1.38 | 0.041 |
| HE | 4.99 | 1.37 | 0.041 |

1h bars: about $0.97 per root for the full history (measured on ES, NQ, GC, CL, ZN, 6E). 1d bars for all 37 roots: $1.61.

## Plan options

| Plan | USD |
|---|---:|
| A. 1m for 6 roots (ES NQ GC CL ZN 6E), full history | 122.52 |
| B. 1m for 4 roots (ES NQ GC CL) + 1h for 37 roots + 1d for 37 roots | 120.06 |
| C. 1h + 1d for 37 roots only | 37.35 |
| D. 1m for 8 roots (ES NQ GC CL ZN 6E ZB RTY) from 2016 (about 63% of the range) | 95.50 |
| E. 1m for all 37 roots, full history | 545.08 |
| F. 1m for the 31 standard roots, full history | 491.58 |

## ES, one year (2025), finer schemas

| schema | USD | records (M) | GB |
|---|---:|---:|---:|
| ohlcv-1s | 41.26 | 11.3 | 0.63 |
| trades | 154.19 | 123.2 | 5.91 |
| tbbo | 256.99 | 123.2 | 9.85 |
| mbp-1 | 252.88 | 1885.6 | 150.85 |
| mbp-10 | 427.41 | 2494.2 | 917.85 |
| statistics | 0.01 | 0.2 | 0.01 |
| definition | 0.00 | 0.0 | 0.00 |

Parent symbology daily bars (every contract, for roll adjustment): ES.FUT $0.30, CL.FUT $7.75, ZN.FUT $0.17. One day of ES 1m bars (1,380 records): $0.005.

## What this means

- The earlier assumption that 1-minute history for 20+ roots over 15 years fits in a $125 credit was wrong by about 4x.
- Within $125 with a margin, the realistic shape is plan B or a variant: a few roots at 1 minute, the whole universe at 1 hour and 1 day.
- Order-book and tick schemas are out of budget except for tiny pilot samples.
- Metadata calls (`get_cost`, `get_record_count`, `get_billable_size`, `list_unit_prices`, `get_dataset_range`) cost nothing; call them before every download.

