# Pump cases: rejected candidates (Team Lead A, Enforcement Cases)

Rule applied: a row is kept only if a primary source we could fetch states a promotion start date and a collapse, dump-end or suspension date. Dates were never inferred from price data or news. All the candidates below were reviewed and left out of `pump_cases.csv`.

## A. Primary source states no start date (suspension-only "ramp-and-dump" cases)
These SEC Section 12(k) orders name the ticker and the suspension date. They do not give a promotion start date. They are good leads if another primary document (a DOJ indictment or an SEC complaint) turns up later.

| Ticker | Issuer | Suspension effective | Order URL |
|---|---|---|---|
| MAGH | Magnitude International Ltd | 2025-12-05 | https://www.sec.gov/files/litigation/suspensions/2025/34-104317-ts.pdf |
| MAMK | MaxsMaking Inc. | 2025-11-17 | https://www.sec.gov/files/litigation/suspensions/2025/34-104180-ts.pdf |
| MCTA | Charming Medical Limited | 2025-11-12 | https://www.sec.gov/files/litigation/suspensions/2025/34-104176-ts.pdf |
| LAWR | Robot Consulting Co., Ltd. | 2025-10-23 | https://www.sec.gov/files/litigation/suspensions/2025/34-104169-ts.pdf |
| PC | Premium Catering (Holdings) Limited | 2025-10-17 | https://www.sec.gov/files/litigation/suspensions/2025/34-104168-ts.pdf |
| NUTR | NusaTrip Incorporated | 2025-10-09 | https://www.sec.gov/files/litigation/suspensions/2025/34-104167-ts.pdf |
| EMPG | Empro Group Inc. | 2025-10-09 | https://www.sec.gov/files/litigation/suspensions/2025/34-104166-ts.pdf |
| PTNM | Pitanium Limited | 2025-10-06 | https://www.sec.gov/files/litigation/suspensions/2025/34-104165-ts.pdf |
| PLTS | Platinum Analytics Cayman Limited | 2025-10-06 | https://www.sec.gov/files/litigation/suspensions/2025/34-104164-ts.pdf |
| EFTY | Etoiles Capital Group Co., Ltd | 2025-10-06 | https://www.sec.gov/files/litigation/suspensions/2025/34-104163-ts.pdf |
| QMMM | QMMM Holdings Limited | 2025-09-29 | https://www.sec.gov/enforcement-litigation/trading-suspensions/34-104113-ts |
| SDM | Smart Digital Group Limited | 2025-09-29 | https://www.sec.gov/enforcement-litigation/trading-suspensions/34-104112-ts |
| JMG | JM Group Limited | 2026-01-15 | https://www.sec.gov/files/litigation/suspensions/2026/34-104613-ts.pdf |
| TCGL | TechCreate Group Ltd. | 2026-02-02 | https://www.sec.gov/files/litigation/suspensions/2026/34-104763-ts.pdf |
| HCHL | Happy City Holdings Limited | 2026-06-12 | https://www.sec.gov/files/litigation/suspensions/2026/34-105675-ts.pdf |
| CHSN | Chanson International Holding | order 2024-10-07 | https://www.sec.gov/files/litigation/suspensions/2024/34-101272-o.pdf |
| BYU | BAIYU Holdings, Inc. | order 2024-09-06 | https://www.sec.gov/files/litigation/suspensions/2024/34-100956-o.pdf |

The February–April 2021 social-media suspensions also give no start date: Bebida Beverage et al., Bangi, Affinity Beverage, Sylios, Marathon Group, All Grade Mining, SpectraScience, 1pm Industries et al., Bayport International, That Marketing Solution and Electric Car Company. The 2021 Minerco suspension has the same problem.

## B. DOJ primary documents could not be fetched from this environment
justice.gov press-release pages return an Akamai bot-challenge page, both to scripts and to WebFetch. We did not try to get around it. We found no direct `justice.gov/media/.../dl` PDF for these cases, so none were used. Each one needs a manual look at the indictment:
- OST (Ostin Technology Group): E.D. Va. indictment, unsealed Sept 2025. News leads say the promotion ran April–June 2025 and the stock collapsed on 2025-06-26.
- CLEU (China Liberal Education Holdings): N.D. Ill. case 25 CR 161. Leads say Nov 2024–Feb 2025.
- TDIC (Dreamland Limited) and other China-based issuers: S.D.N.Y. civil forfeiture complaints.
- U.S. v. Constantinescu et al. (S.D. Tex., the parallel Atlas indictment). The tickers are already covered by the SEC complaint.

## C. Dates are not specific enough
- MINE (Minerco, SEC v. Minerco et al., comp-pr2024-165): the dates given (Oct 1, 2020 and Feb 10, 2021) are price reference points, not promotion or collapse dates. The scheme is described only as "October 2019 through May 2021".
- BRZL (Scepter Holdings, SEC v. Nicosia et al.): the campaign is given as "approximately February to August 2020", month-level only.
- SOLY (Soliton, SEC v. Casey et al.): Twitter promotion started 2019-03-08, but no end date is stated.
- UPPR (Upper Street Marketing, SEC v. Earle et al. and suspension 2019-06-27): the complaint PDF has no extractable text, and the order gives no clear promotion start.
- GWPD (GP Solutions, suspension 2019-10-02): a social-media post on 2019-02-26 and "manipulative trading" from Mar 12 to Aug 27, 2019. The promotion window is ambiguous.
- HUGE (FSD Pharma, Constantin complaint para 35): only the dump day (2021-02-03) is stated. The promotion date is not.
- CHIT, PDXP, VICT (Cherubim, PDX Partners, Victura; SEC v. Einstein Investments subpoena action): "January 2018", month-level only, and the action is a subpoena enforcement, not a fraud complaint.
- Bauer et al. (comp25366: SPWZ, AHELF/UUCRF, NAMG, VOIL, BISN, LOGG): campaigns are month-level ("August 2015 to October 2015", "March 2018 to July 2018"), and all are pre-2019. BEAG is kept, sourced from its suspension order.
- Multi-year schemes with no discrete pump window: County Line Energy CYLC (SEC v. Farber et al.), Verges/Durland issuers (ALYI, PJET, PURA, VAYK, WPUR), Solar Integrated Roofing SIRC (SEC v. Rosen et al., 2021–2024), Kirk Lee issuers (AJBI, NNRX, QUOR, TALK), Carrillo issuers (ARSN, OLMM), Calabrigo et al.

## D. Not a promotion pump-and-dump, or a definitional problem
- Issuer-misstatement COVID suspensions with no alleged promotion or dumping: WMGR (Wellness Matrix), KGET (Kleangas/CaliPharms), BVTK (Bravatek), NBDR (No Borders), HBOSF (EastWest Bioscience), RBII (Rising Biosciences), View Systems.
- Andrew Left / Citron "long" tweets (XL, VUZI, GE, NVDA and others; comp-pr2024-89): large and mid caps with a fast reversal after a recommendation. This is not a microcap pump-and-dump, and the case is contested.
- EVTP (Herbatech Life, SEC v. Debo): the release describes a planned pump. We found no executed promotion window.
- MKAU (MK Automotive, Beck complaint): the issuer changed ticker to CLKA in July 2017, during the scheme. Dropped to avoid ticker ambiguity.
- Alomari complaint (comp25993, five issuers): the PDF uses a custom font encoding, so its text cannot be machine-verified. Its EBET episode is covered by the Casey complaint instead.
- Biozoom (2013), YaFarm, Jay Fung newsletters (2009–2010), Sodi (2013), CodeSmart (2013): pre-2016, with no issuer-level dates in the release text.
