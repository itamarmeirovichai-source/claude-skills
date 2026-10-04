"""SEC EDGAR -> :class:`~pumpwatch.models.Filing` records (pure parsing, no network).

Inputs are the JSON documents served by SEC:

* ``https://www.sec.gov/files/company_tickers.json`` - current ticker -> CIK map.
* ``https://data.sec.gov/submissions/CIK##########.json`` - company metadata plus
  ``filings.recent`` (the latest ~1000 filings as *columnar* arrays) and
  ``filings.files`` (names of older pages, each a bare columnar object).

No look-ahead
    ``Filing.day`` is always ``filingDate``: the day the document became public
    on EDGAR. ``reportDate`` (the period or event date) can be days or months
    earlier and was not knowable to the market until the filing appeared, so it
    is never used as the event day.

Titles
    ``Filing.title`` is built only from what the data says: the primary
    document description plus, for 8-K/6-K style forms, the item codes
    translated to words (``1.01`` -> "entry into a material definitive
    agreement", ...). Nothing is inferred beyond the item codes, so e.g. a name
    change filed under item 5.03 reads "amendments to articles of incorporation
    or bylaws; change in fiscal year", not "name change".

Name changes
    EDGAR's ``formerNames`` list gives each old name with a ``from``/``to``
    date range. For each one we emit a synthetic ``Filing(form="NAME-CHANGE",
    title="name change from OLD to NEW")`` dated the day *after* ``to`` (the
    last day EDGAR shows the old name, so the new name is public from the next
    day). Changes that only reformat the name ("Limited" -> "Ltd") are skipped.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Any, Iterable, Iterator

from ..models import Filing

NAME_CHANGE_FORM = "NAME-CHANGE"

# Form 8-K item codes (post-2004 numbering). Wording follows the SEC item
# titles, lightly shortened. Unknown codes are kept as "item X".
ITEM_WORDS: dict[str, str] = {
    "1.01": "entry into a material definitive agreement",
    "1.02": "termination of a material definitive agreement",
    "1.03": "bankruptcy or receivership",
    "1.04": "mine safety violations",
    "1.05": "material cybersecurity incident",
    "2.01": "completion of acquisition or disposition of assets",
    "2.02": "results of operations and financial condition",
    "2.03": "creation of a direct financial obligation",
    "2.04": "triggering events that accelerate a financial obligation",
    "2.05": "costs of exit or disposal activities",
    "2.06": "material impairments",
    "3.01": "notice of delisting or failure to satisfy a listing rule",
    "3.02": "unregistered sales of equity securities",
    "3.03": "material modification to rights of security holders",
    "4.01": "auditor change (changes in certifying accountant)",
    "4.02": "non-reliance on previously issued financial statements",
    "5.01": "change in control of registrant",
    "5.02": "departure or appointment of directors or officers",
    "5.03": "amendments to articles of incorporation or bylaws; change in fiscal year",
    "5.04": "temporary suspension of trading under employee benefit plans",
    "5.05": "amendments to the code of ethics",
    "5.06": "change in shell company status",
    "5.07": "submission of matters to a vote of security holders",
    "5.08": "shareholder director nominations",
    "6.01": "ABS informational and computational material",
    "6.02": "change of ABS servicer or trustee",
    "6.03": "change in ABS credit enhancement",
    "6.04": "failure to make a required ABS distribution",
    "6.05": "securities act updating disclosure",
    "7.01": "regulation FD disclosure",
    "8.01": "other events",
    "9.01": "financial statements and exhibits",
}

_ITEM_FORMS = ("8-K", "6-K")  # also matches 8-K/A, 8-K12B, 6-K/A ...


# ---------------------------------------------------------------------------
# company_tickers.json
# ---------------------------------------------------------------------------
def cik10(cik: Any) -> str:
    """Zero-padded 10-digit CIK string as used in EDGAR URLs."""

    return f"{int(str(cik).strip()):010d}"


def parse_company_tickers(json_obj: Any) -> dict[str, str]:
    """``{"0": {"cik_str": 320193, "ticker": "AAPL", "title": ...}, ...}`` -> ``{"AAPL": "0000320193"}``.

    Also accepts the ``{"fields": [...], "data": [[...], ...]}`` layout of
    ``company_tickers_exchange.json``. When a ticker appears twice the first
    entry wins (SEC lists the primary listing first).
    """

    out: dict[str, str] = {}
    if isinstance(json_obj, dict) and "fields" in json_obj and "data" in json_obj:
        fields = list(json_obj["fields"])
        rows: Iterable[dict] = (dict(zip(fields, r)) for r in json_obj["data"])
        key_cik = "cik"
    else:
        rows = json_obj.values() if isinstance(json_obj, dict) else json_obj
        key_cik = "cik_str"
    for row in rows:
        ticker = str(row.get("ticker") or "").strip().upper()
        cik = row.get(key_cik, row.get("cik"))
        if ticker and cik is not None and ticker not in out:
            out[ticker] = cik10(cik)
    return out


# ---------------------------------------------------------------------------
# submissions
# ---------------------------------------------------------------------------
def describe_items(items: str) -> str:
    """``"1.01,9.01"`` -> ``"entry into a material definitive agreement; financial statements and exhibits"``."""

    words = []
    for code in (c.strip() for c in (items or "").split(",")):
        if code:
            words.append(ITEM_WORDS.get(code, f"item {code}"))
    return "; ".join(words)


def build_title(form: str, items: str = "", description: str = "") -> str:
    """Human-readable title from the primary document description and 8-K/6-K items."""

    description = (description or "").strip()
    if description.upper() == form.upper():
        description = ""  # "S-1" as a description adds nothing
    item_text = describe_items(items) if form.upper().startswith(_ITEM_FORMS) else ""
    if description and item_text:
        return f"{description}: {item_text}"
    return description or item_text


def _rows(columns: dict) -> Iterator[dict]:
    """Iterate a columnar EDGAR block (``{"form": [...], "filingDate": [...]}``) as row dicts."""

    keys = [k for k, v in columns.items() if isinstance(v, list)]
    n = len(columns.get("form", []))
    for i in range(n):
        yield {k: (columns[k][i] if i < len(columns[k]) else None) for k in keys}


def _in_window(day: date, start: date | None, end: date | None) -> bool:
    return (start is None or day >= start) and (end is None or day <= end)


def parse_submissions_page(
    json_obj: dict, ticker: str, start: date | None = None, end: date | None = None
) -> list[Filing]:
    """Parse one columnar block: ``filings.recent`` or an older ``CIK...-submissions-NNN.json`` page."""

    ticker = ticker.strip().upper()
    out: list[Filing] = []
    for row in _rows(json_obj):
        form = (row.get("form") or "").strip()
        filed = (row.get("filingDate") or "").strip()
        if not form or not filed:
            continue
        day = date.fromisoformat(filed[:10])
        if not _in_window(day, start, end):
            continue
        title = build_title(form, row.get("items") or "", row.get("primaryDocDescription") or "")
        out.append(Filing(ticker, day, form, title))
    return out


_SUFFIX = {"limited": "ltd", "incorporated": "inc", "corporation": "corp", "company": "co"}


def _norm_name(name: str) -> str:
    words = re.findall(r"[a-z0-9]+", name.lower())
    return " ".join(_SUFFIX.get(w, w) for w in words)


def name_change_filings(
    json_obj: dict, ticker: str, start: date | None = None, end: date | None = None
) -> list[Filing]:
    """Synthetic NAME-CHANGE filings from ``formerNames``, dated the day after each ``to`` date."""

    former = [f for f in json_obj.get("formerNames") or [] if f.get("name") and f.get("to")]
    former.sort(key=lambda f: f["to"])
    names = [f["name"] for f in former] + [json_obj.get("name") or ""]
    out: list[Filing] = []
    for i, f in enumerate(former):
        old, new = f["name"].strip(), names[i + 1].strip()
        if not new or _norm_name(old) == _norm_name(new):
            continue
        day = date.fromisoformat(f["to"][:10]) + timedelta(days=1)
        if _in_window(day, start, end):
            out.append(Filing(ticker.strip().upper(), day, NAME_CHANGE_FORM, f"name change from {old} to {new}"))
    return out


def parse_submissions(
    json_obj: dict, ticker: str, start: date | None = None, end: date | None = None
) -> list[Filing]:
    """Filings from ``filings.recent`` plus synthetic name changes, deduplicated and sorted by day.

    Older pages (see :func:`extra_page_names`) are parsed separately with
    :func:`parse_submissions_page` and merged with :func:`merge_filings`.
    """

    recent = (json_obj.get("filings") or {}).get("recent") or {}
    return merge_filings(
        parse_submissions_page(recent, ticker, start, end),
        name_change_filings(json_obj, ticker, start, end),
    )


def merge_filings(*groups: Iterable[Filing]) -> list[Filing]:
    """Union of filing lists with exact duplicates removed, sorted by (ticker, day, form, title)."""

    seen = {f for g in groups for f in g}
    return sorted(seen, key=lambda f: (f.ticker, f.day, f.form, f.title))


def recent_coverage_start(json_obj: dict) -> date | None:
    """Earliest ``filingDate`` in ``filings.recent`` (older filings live in extra pages)."""

    dates = ((json_obj.get("filings") or {}).get("recent") or {}).get("filingDate") or []
    return date.fromisoformat(min(dates)[:10]) if dates else None


def extra_page_names(json_obj: dict, start: date | None = None, end: date | None = None) -> list[str]:
    """Names of older submissions pages (``filings.files``) overlapping ``[start, end]``.

    Fetch each from ``https://data.sec.gov/submissions/<name>``.
    """

    out = []
    for f in (json_obj.get("filings") or {}).get("files") or []:
        lo = date.fromisoformat(f["filingFrom"][:10]) if f.get("filingFrom") else None
        hi = date.fromisoformat(f["filingTo"][:10]) if f.get("filingTo") else None
        if start is not None and hi is not None and hi < start:
            continue
        if end is not None and lo is not None and lo > end:
            continue
        out.append(f["name"])
    return out


def earliest_filing_date(json_obj: dict) -> date | None:
    """Earliest filing date EDGAR knows for this CIK (from page ranges or the recent block)."""

    candidates = [
        date.fromisoformat(f["filingFrom"][:10])
        for f in (json_obj.get("filings") or {}).get("files") or []
        if f.get("filingFrom")
    ]
    recent = recent_coverage_start(json_obj)
    if recent:
        candidates.append(recent)
    return min(candidates) if candidates else None
