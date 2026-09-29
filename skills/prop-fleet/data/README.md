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
