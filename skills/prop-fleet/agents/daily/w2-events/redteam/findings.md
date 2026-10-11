# E2 red team — findings (audit of commit e1a7eca, written up by the head from the red team's report)

The red team set out to show the negative result was wrong. **Verdict: 0/12 stands.** No defect could
hide an edge or overstate a number. Fixing every calendar defect together moves no t by more than 0.25
(`cal_sensitivity.py`). Best result stays E2-04 at t +1.09 against a bar of 3.5603.

| # | where | defect | effect |
|---|---|---|---|
| C1 | `calendar_build.py` ISM rule | ISM's January release (December report) comes on the 2nd or 3rd business day, not the 1st (from memory: 2019-01-03, 2020-01-03, 2021-01-05, 2022-01-04, 2023-01-04, 2024-01-03, 2025-01-03) | 7 OOS days sit in the wrong E2-08..E2-12 group, and their 10:00 blackout lands on the wrong day |
| C2 | `calendar_build.py` minutes regex | 2019-10-11, 2020-03-03 and 2020-03-23 are unscheduled-action releases, tagged as FOMC minutes at 14:00 | a false 13:57 exit on 3 E2-10 control days |
| C3 | ALFRED rid=9 | five April annual-revision postings (2021-2025) are kept as retail-sales days | 5 extra event days |
| C4 | ALFRED | rows dated 2026-10-11 | outside the data, so no effect |
| D1 | SPY file | 12 half-days carry bars after the 13:00 close | 1 event trade, 11 control trades; negligible |
| D2 | NQ file | 35 CME holiday sessions counted as sessions | E2-10 control trades and the E2-11 window only; negligible |
| T1 | `events_bt.py` `truncation_test` | re-checks only trades taken (not no-trade days); keeps the entry bar's h/l/c; reuses the precomputed E2-11 median | no leak exists (`decide()` reads nothing after the entry minute except the entry bar's open), but the test is weaker than its label |

C1-C4 corrected (registered rules unchanged): E2-08 t -1.28 → -1.04; E2-09 -2.27 → -2.10; E2-10 +0.69 → +0.52;
E2-11 -1.14 → -0.97; E2-12 -1.37 → -1.21; E2-01..E2-07 unchanged.

No defect was found in:

- the FOMC dates: all 54 OOS statement dates match, all at 14:00;
- CPI/NFP spot checks: about 25 of each, checked from memory because bls.gov returns 403;
- the signal, side and exit logic, the blackout exits and the NQ 00:00 adjustment (2023-12-12 gap: raw +128.7 bp, adjusted -2.6 bp);
- costs: the mirror pairs give exactly ± gross (E2-01/04 ±17.20), and the 2× figure = gross − 2×cost;
- the statistics;
- the hand recomputation of e2_trades.csv rows, which matches to 4 decimals.
