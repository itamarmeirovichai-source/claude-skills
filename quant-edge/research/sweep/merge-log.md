# Merge log — Department B sweep, 2026-11-06

Rule: same mechanism + same instrument set = one entry. The survivor keeps its id; the absorbed block becomes a variant or diagnostic arm inside the survivor's pre-registration. Pre-sweep entries "attached" are those a scout block explicitly extends (they are not counted as separate entries). Rows with the same mechanism on a different instrument set were NOT merged (e.g. C-1-02 bond leg vs C-12-15 equity leg of month-end rebalancing; C-4-06 gold vs pre-sweep A-C21 ES/NQ VIX-gated reversal; C-3-04 Nikkei vs C-8-10 HSI session reversal; C-1-08 ES vs C-8-11 Europe vs C-8-12 Tokyo closing-auction reversal).

| absorbed | survivor | reason |
|---|---|---|
| AS C-3-02 | AS C-3-01 | same mechanism (European-open inventory drift), same instrument (ES/MES); C-3-02 is the by-hour decomposition of the same window -> run as C-3-01's diagnostic arm |
| AS C-3-05 | AS C-3-03 | Shanghai AM benchmark window (20:45-21:15 ET) lies inside the 18:00->08:20 ET gold overnight hold; same instrument (GC/MGC); kept as a sub-window variant with haircut 0.7 |
| AS C-4-03 | AS C-4-02 | same target (gold return into the 13:30 ET settlement), same instrument; C-4-03 only swaps the predictor (overnight sign instead of the whole-day sign) -> two signal variants of one row |
| pre-sweep A-C27 | AS C-3-01 | pre-sweep overnight drift 02:00-03:00 ET; C-3-01 extends it with the post-2021 null |
| pre-sweep P-C20 | AS C-3-01 | pre-sweep 18:00->09:30 MES/MNQ hold; superseded by the C-3-01 evidence (flat in ES/NQ/YM 2021-2025) |
| pre-sweep A-C09 | AF C-1-01 | variant A of C-1-01 is A-C09 verbatim |
| pre-sweep A-C07 | AF C-1-05 | Tokyo 9:55 fix 6J; C-1-05 adds the KMW magnitudes and the post-fix leg |
| pre-sweep P-C12 | AF C-1-05 | Tokyo-fix USDJPY window rules (practitioner) = same mechanism and instrument |
| pre-sweep A-C06 | AF C-1-04 | WMR London fix W-pattern; C-1-04 adds the intensity-day conditioning |
| pre-sweep P-C09 | AF C-1-09 | index-rebalance eve closing-auction short (UK100 +11.5 bp/event holdout) = same mechanism; C-1-09 adds the US futures legs |
| pre-sweep A-C14 | AF C-2-03 | EIA crude post-release; C-2-03 is the fade construction with the Krueger holdout |
| pre-sweep A-C15 | AF C-2-01 | NG storage report; C-2-01 is the announcement-day premium version |
| pre-sweep A-C16 | AF C-2-04 | WASDE post-release drift; C-2-04 adds the minute-data update and the limit-lock leg |
| pre-sweep A-C18 | AF C-2-07 | LBMA auctions/COMEX settlement; C-2-07 is the post-reform kill-test + round-imbalance leg |
| pre-sweep A-C10 | AF C-1-03 | auction-cycle concession/recovery |
| pre-sweep A-C11 | AF C-2-10 | post-FOMC drift ZN |
| pre-sweep A-C13 | AF C-1-12 | daily 4pm Treasury strike window |
| pre-sweep A-C24 | AF C-1-06 | LETF rebalancing: equity legs closed (H0006/H0019); commodity transfer kept in C-1-06 (Treasury transfer C-1-07 kept separately: different instruments) |
| pre-sweep A-C25 | AF C-1-08 | closing-auction imbalance; post-close reversal construction kept |
| pre-sweep A-C23 | AS C-4-05 | dealer-gamma regime switch; C-4-05 is the 2026 evidence update |
| pre-sweep A-C20 | AS C-4-04 | reversal after extreme 1-min moves; C-4-04 is the volume-gated drift-burst version |
| pre-sweep A-C03 | AS C-4-02 | commodity ITSM into settlement (GC leg); CL leg declined on BDLM numbers, NG/SI/PL/HO legs in C-4-08 |
| pre-sweep P-C22 | AS C-5-05 | intraday futures triplet stat-arb: CL/HO/RB leg = C-5-05; ES/NQ/RTY leg negative (Krueger 0.58 ratio; Budish et al.); GC/SI leg left untested inside C-5-05's pre-registration as a second instrument set |
| MS C-9-02 | PC C-9-03 | VPIN as an inactivity/regime gate on the same futures sleeves; one row, head-to-head vs a matched realized-vol gate |
| MS C-9-03 | PC C-9-02 | volume-clock bars from 1-min volume = dollar/volume-bar decision cadence; same construction claim (Sharpe difference vs clock time) |
| MS C-9-04 | PC C-9-02 | imbalance bars are another event sampler for the same comparison (1s pilot only) |
| MS C-10-01 | PC C-10-01 | meta-labelling with purged, embargoed k-fold on an existing primary; MS names the primaries (prereg_orb30, overnight drift) |
| pre-sweep A-C30 | PC C-7-03 | vol targeting / conditional vol scaling overlay = Carver relative-vol attenuation family |
| SC C-8-07 | PC C-8-01 | multi-day trend on FTMO CFDs with swap-netted forecast and FTMO-rule-shaped hard-DD overlay; same mechanism and instrument set as Carver trend+carry on the swap-filtered CFD map |
| IG C-11-05 | PC C-8-01 | trend + buffer-aware hard-DD guard vs FTMO 5%/10% rules on the same CFD trend sleeve |
| IG C-12-32 | MS C-9-09 | TAS-instrument prints are the direct read of the same settlement-window flow (CL/NG/GC subset); the IG scout itself calls it C-9-09's data upgrade |
| SC C-8-08 | SC C-8-01 | the US-cash-hours leg is the hour decomposition of the same non-US overnight premium on the same index CFDs (run as C-8-01's diagnostic arm) |
| SC C-8-03 | SC C-8-09 | Lunar-New-Year HK50 hold-through-closure is one event of the closure-premium panel (same mechanism, HK50 in both) |
| IG C-11-02 | SC C-8-05 | futures-curve carry (KMPV) on FTMO commodity CFDs = energy/commodity carry on FTMO's own swap sign; same mechanism, overlapping instrument set (C-8-05 is the narrower, swap-verified version) |
| pre-sweep P-C16 | SC C-8-06 | multi-day dip buy after a sharp two-day fall: commodity legs = C-8-06; index legs closed (G2) |
| IG C-12-02 | IG C-12-01 | same mechanism (prop accounts force-flattened at their firm deadline) and instrument set (ES/MES); 16:45/16:59 deadlines are additional event times of one row |
| IG C-3-07 | IG C-12-18 | weekday and Sunday 18:00 ET reopen overshoot fade: same mechanism (re-pricing burst at the Globex reopen by a thin crowd), same roots; Sunday weekend-news days are a pre-registered sub-sample |
| pre-sweep P-C11 | PC C-7-05 | vol-regime gating (breakouts in high vol, fades in low vol) = the overnight-range-percentile regime row |
| pre-sweep P-C19 | PC C-9-04 | top-of-book skew on ES -> OFI feature test = the book-skew markout measurement |
| pre-sweep P-C24 | SC C-8-06 | gold 3-day mean reversion and crude pullback = commodity multi-day dip buy at FTMO Swing |
| pre-sweep A-C38 | MS C-9-01 | bulk-volume-classified 1-min imbalance as a conditioner (reversal/continuation); MS:C-9-01 is the explicit A-C38 update with the calibration refutation |

## Declined at merge (not merges)

- AF C-1-10 ES expiration pinning: negative update / amplification kill-test: negative evidence: Elms (2026) finds no pinning in ES/SPX 2016-2025; the amplification variant is inside H0006/H0019 (last-half-hour momentum incl. GEX); A-C26 downgraded. Keep only as a documentation note.
- SC C-8-04 Gold autumn seasonality (Baur) - negative update: negative evidence: the 2024 replication (Potrykus-Augustynowicz) reverses the sign; seasonal-window family (P-C29, A-C19) without a mechanism; scout itself says do not register.
- MS C-5-11 ES <-> NQ one-minute lead-lag, 2016-2026 code-backed null: negative-evidence row "1-minute lead-lag without a mechanism" (common brief); gross 0.03-0.4 bp vs 1.2 bp RT (0.2-0.6x of cost, two independent code bases); A-C22/P-C22 confirmed dead.
- SC C-13-07 Extreme cold-forecast NG risk premium (NG1-NG2 spread): no firm structure: the only post-cost Sharpe > 1 in lane 13 (1990-2019) is a multi-day calendar-spread hold that no futures prop firm allows across the close and FTMO cannot express; the outright intraday adaptation is untested and has no mechanism of its own. Re-open only if a firm offers spreads across the close.

## Id collisions resolved by file tag

C-9-01, C-9-02, C-9-03, C-9-04, C-9-05 and C-10-01 exist in both practitioner-code (PC) and microstructure-ml (MS); C-8-01 exists in practitioner-code (Carver trend+carry) and session-cfd-swing (night-day asymmetry). Every id in candidates.md carries the file tag.
