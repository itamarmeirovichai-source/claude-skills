# Legit control cases: rejected candidates

Team B (Legit Controls). These candidates were considered for `legit_cases.csv` and left out. Each one has a reason.

How candidates were found: daily Yahoo bars were pulled for about 6,000 Nasdaq/NYSE tickers that are still listed. Days with a close-to-close gain of 30% or more since 2019 were flagged, giving 15,973 jump days. These were filtered to a rough market cap of $30M to $300M and a previous close of at least $1. Each remaining jump was then matched to the 8-K or 6-K filed that day or the day before, using EDGAR submissions and exhibit text. EDGAR full-text searches (FDA approval, met primary endpoint, contract, per share in cash, unsolicited proposal, license/collaboration upfront payment) were also run and matched against the same jump days.

## Market cap above $300M (checked against the 10-Q/40-F cover)
| Ticker | Jump day | Why rejected |
|---|---|---|
| ANNX (Annexon) | 2024-06-04 | Pivotal Phase 3 GBS readout, +30.8%. The XBRL dei share count was stale (38.6M shares from 2022). The Q1-2024 10-Q cover shows 92,412,866 shares, so at the $4.58 previous close the market cap was about $423M, which is over $300M. |
| ELVA (Electrovaya) | 2026-07-15 | Amazon commercial relationship, +49%. XBRL dei gave 34.1M shares (FY2024), but the FY2025 40-F cover shows 42,108,920 shares. At $7.89 that is about $332M, which is over $300M. |
| SEPN (Septerna) | 2025-05-14 | Novo Nordisk collaboration, +51%. Screen market cap was $299.1M. That is too close to the limit, so it was dropped for precision. |
| GLUE (Monte Rosa) | 2025-09-15 | Novartis collaboration, +44%. Screen market cap was $297.1M, too close to the limit. |

## Timing does not match the filing (news came after the jump day closed)
| Ticker | Jump day | Why rejected |
|---|---|---|
| DXLG (Destination XL) | 2025-12-11 | The FullBeauty merger 8-K was accepted at 17:24 ET and the earnings 8-K at 16:49 ET, both after the close on the jump day. The +44% move that day is not explained by these filings. |
| ACHV (Achieve Life Sciences) | 2026-04-16 | The only same-day 8-K is a $354M private placement, accepted at 16:47 ET after the close. The +35.5% move is unexplained. |
| CLPS | 2019-01-08 | The only 6-K was an auditor appointment. No qualifying news. |

## Not a qualifying news type, or news is ambiguous
| Ticker | Jump day | Why rejected |
|---|---|---|
| ACIU (AC Immune) | 2023-06-27 | FDA Fast Track designation is not an approval or a pivotal result. The 2024-05-13 Takeda deal was used for this company instead. |
| TCX (Tucows) | 2026-07-31 | The 8-K covers only a credit-agreement amendment and a Ting Fiber investment/sale (items 1.01/1.02), with no press-release exhibit. The driver is ambiguous. |
| RCAT (Red Cat) | 2022-03-14 | Selected to compete in the Army SRR Tranche 2 program, which is not a contract award. The ticker also has a heavy social-media/retail-hype history. |
| MIST (Milestone) | 2020-07-23 | FDA regulatory guidance on trial design, not an approval or a pivotal readout. A financing was announced the same day. |
| EOLS (Evolus) | 2021-02-19 | IP litigation settlement (AbbVie/Medytox), not one of the target news types. |
| VHC (VirnetX) | 2019-01-15 | Court affirmed a patent judgment (litigation). The ticker is also a known retail/meme name. |
| LQDA (Liquidia) | 2022-07-19 | Patent (IPR) ruling, not a target news type. |
| SGHT (Sight Sciences) | 2025-10-17 | Medicare fee-schedule establishment (reimbursement), not a target news type. |
| PRCH (Porch) | 2024-10-28 | Insurance regulatory approval of a reciprocal exchange, not a target news type. |
| MYO (Myomo) | 2024-03-01 | CMS fee schedule, not a target news type. |
| LFCR (Lifecore) | 2023-05-23 | Mixed financing plus supply agreement. The company's 2026-09-28 takeover was used instead. |
| CTEV / FOSL / SCOR | various | Refinancings and recapitalizations (CTEV 2024-12-27, FOSL 2025-08-15, SCOR 2025-09-29). Not target news types. |
| ANRO, ENGN, ACRV, DNTH, AGEN | various | The jump coincided with a PIPE/private placement. Financing is not a target news type. |
| CSPI | 2024-02-22 | Stock-split announcement. |
| BRIA, GDEV | 2025 | Dividend declarations. |

## Ticker renamed or reassigned, or company repurposed (the ticker-confusion rule)
| Ticker | Jump day | Why rejected |
|---|---|---|
| CTOS (Nesco Holdings, NSCO at the time) | 2020-12-03 | Acquirer jump on the Custom Truck deal. The ticker and company identity changed afterwards. |
| MAGN (Glatfelter, GLT at the time) | 2024-02-07 | Berry spin-merge (RMT). Now Magnera under a new ticker. |
| MCHB (HomeStreet, HMST at the time) | 2024-01-16 | FirstSun merger announcement. The ticker was later reassigned to Mechanics Bancorp. |
| LITS (MEI Pharma, MEIP at the time) | 2020-04-14, 2021-11-30 | Trial and partnership news, but the ticker and company were repurposed (now "Lite Strategy", a crypto-treasury company). |
| ELVN (IMARA), PVLA (Pieris), IMDX (OncoCyte), WHWK (Aerpio/Aadi), CLYM (Eliem), TE (FREYR) | various | Reverse mergers or renames make the current ticker misleading. |

## Possibly tainted or hype-driven (precision first)
| Ticker | Jump day | Why rejected |
|---|---|---|
| FLNT (Fluent, Cogint/IDI before) | 2020-01-15 | Genuine earnings pre-announcement (+40.6%, about $168M) that passed the screens. It was dropped because an EDGAR full-text hit (OPKO DEF 14A) links Phillip Frost, a defendant in the SEC's 2018 Honig-group pump-and-dump complaint, as a former Vice Chairman of Cogint/Fluent. Fluent itself was not alleged to be manipulated, but this is excluded for precision. |
| UMAC (Unusual Machines) | 2024-11-27/29 | Celebrity-advisor news (Donald Trump Jr.). Social-media hype. |
| BMNR, EMPD (Volcon), NAKA (KindlyMD) | 2025 | Crypto-treasury pivots and PIPEs. Classic social-media momentum. |
| WFCF | 2020-12-08 | OTC at the time, +300% one-day print. Data reliability is doubtful. |
| GLSI, ATER, WATT, APT, BMRA and other March-to-May 2020 COVID moves | 2020 | COVID-era hype and market-wide rebound days (for example GIII, PLAY, CHEF, BJRI and OSW on 2020-03-19/24). These are not idiosyncratic company news. RVP (2020-05-04) was kept because it is a specific, documented HHS delivery order. |
| PHUN (Phunware) | 2019-01-03 | Known retail-pump history. |

## Could not be verified (no Yahoo data: acquired and delisted)
Several well-known small-cap takeovers were left out because the Yahoo chart API returns "No data found, symbol may be delisted". Without bars, `pct_move` and `end` cannot be computed. Examples: Poseida (PSTX, 2024-11-26), Harpoon (HARP, 2024-01-08), Cidara (CDTX, 2025-11), Inozyme, Vigil, Regulus, Checkpoint and Paratek. This biases the control set toward companies that are still listed.

## Covered but not used (biotech share capped at about one third)
These are valid-looking biotech catalysts left out to keep biotech under 50% (it is 15 of 46). They were not individually re-verified:
CRBU 2023-07-06 (Pfizer $25M investment), TCRX 2023-05-09 (Amgen collaboration), RLYB 2024-04-11 (J&J collaboration), EYPT 2023-12-04 (Phase 2 DAVIO 2), PHVS 2022-12-08 (Phase 2), QURE 2024-07-09 (Phase 1/2 interim), OVID 2021-03-03 (Takeda royalty deal), ACRS 2024-11-18 (Biosion license).
