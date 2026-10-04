"""Adapters that turn raw public data into PumpWatch records.

Everything in this package is pure: functions take already-downloaded JSON
objects (or explicit paths / file objects for the CSV helpers) and return
``models`` records. No network access happens here; downloading lives in
``scripts/fetch_real_data.py`` so the parsing can be tested offline against
recorded fixtures.

* :mod:`.edgar`      - SEC EDGAR ``company_tickers.json`` and submissions API.
* :mod:`.market_csv` - Yahoo chart JSON and the project's bars/filings CSVs.
"""

from . import edgar, market_csv

__all__ = ["edgar", "market_csv"]
