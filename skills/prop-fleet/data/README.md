# Data

## futures.csv, futures_list.csv, spy_1985.csv

Daily returns for 55 futures contracts, 1984-01-03 to 2016-10-31, with asset-class
metadata, and S&P 500 daily prices from 1985. Copied unmodified on 2026-09-29 from
https://github.com/rkohli3/TSMOM (`data/`), a replication of Moskowitz, Ooi &
Pedersen (2012) "Time Series Momentum". The universe matches the paper's: 13 bond,
9 currency, 9 equity-index and 24 commodity futures.

Why this and not a live feed: this environment's egress policy blocks Yahoo, Stooq,
FRED, AQR, the French library and Hugging Face; GitHub is reachable. A committed
copy also makes the run reproducible.

What was checked before use (see `scripts/trend_backtest.py --futures`):
ES daily returns correlate 0.98 with SPY over 4,816 shared days and match on
2008-10-13 / 2008-10-15 / 2011-08-08; the ES–SPY mean gap of about −2.5%/yr is
consistent with these being *excess* returns over the T-bill, which is what the
paper uses. No instrument has stale (>20% zero) days. `VF` carries no metadata and
is excluded. Seven single-day returns exceed ±25%; they are listed by the loader
and handled as documented there.

Limitation: the series ends October 2016. 2020 and 2022 — two strong trend years —
are not in it, and neither is the 2017–2019 stretch that was hard for trend.

## asset_classes.csv, asset_classes_observed.csv

Daily total-return price levels for nine investable asset classes, 1970-01-02 to
2026-09-25, and a same-shaped 0/1 table saying on which days each level is an
*observed* fund or index (1) rather than a modelled reconstruction (0). Extracted on
2026-09-29 from https://github.com/mwilczynska/financial_datasets (`data/processed/`,
columns `Adj Close` and `Quality Flag`; a flag is "observed" when it starts with
`observed_`). Nothing else was changed; the levels are the source's to six decimals.

| column | what it is | observed from | observed source |
|---|---|---|---|
| USLCAP | S&P 500 total return (SPY-like) | 1970-01-02 | ^SP500TR / CRSP large-cap TR |
| STT | 1–3y US Treasury (SHY) | 1991-10-29 | VFISX, then SHY |
| ITT | 7–10y US Treasury (IEF) | 1991-10-29 | VFITX, then IEF |
| LTT | 20+y US Treasury (TLT) | 1986-05-20 | VUSTX, then TLT |
| GOLDPM | gold, GLD-tracking | 2004-11-18 | GLD |
| CMDTY | broad commodities (DBC) | 2006-02-07 | DBC |
| GLSTOCK | global stocks (VT) | 1990-07-02 | French developed-market TR, then VT |
| GLBOND | global bonds, unhedged | 2007-10-12 | 45% BND + 55% BWX |
| GLSTBOND | global short bonds, unhedged | 2009-02-02 | SHY + ISHG/BWZ |

Before 1991-10-29 only USLCAP and LTT are observed; `trend_backtest.py --etf` starts
there (`ASSET_START`), the first day with a five-asset observed portfolio, and drops
every modelled day. `--etf-all` keeps the modelled history as a check — and the check
says what it should: the 1970–1984 commodity model is a log-linear interpolation
between bi-monthly anchor points, so it has almost no daily volatility, the
vol-scaler leverages it to 17× and the "strategy" prints a +122% year. Modelled
history is not evidence.

What was checked before use: known calendar years match the funds (SPY 2008 −37.0%,
TLT 2022 −31.2%, GLD 2013 −28.3%, DBC 2008 −31.8%); against `futures.csv` over
2002–2016, daily correlations are ES/USLCAP 0.98, US/LTT 0.93, TY/ITT 0.94,
TU/STT 0.87, GC/GOLDPM 0.88 in the GLD era (LBMA-fix vs COMEX-settle timing).
`test_trend_backtest.py` locks the masking and the known years.

The source's DATA_LICENSE.md says the code is MIT but the published series may
embed third-party data with their own terms; this copy is here for research
reproducibility, not redistribution.
