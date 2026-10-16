"""G1 step 1: does any allowed firm list a tradable volatility product?

Fetches each firm's own symbol / permitted-product page and searches it for
VIX, VX, VXM, VXX, SVXY, UVXY, "volatility index", Cboe and CFE.
Writes evidence/<firm>.txt (product list excerpt + every hit) and prints a
summary table. Read-only: plain GETs of public pages, no logins.

Usage: python3 -I symbol_gate.py
"""
import html
import json
import pathlib
import re
import subprocess

OUT = pathlib.Path(__file__).with_name("evidence")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
PAT = re.compile(r"(?i)\bvix\b|volatility index|\bVXM?\b|\bcboe\b|\bCFE\b|\bvxx\b|\bsvxy\b|\buvxy\b")

# (firm, url, kind, marker to start the product-list excerpt)
PAGES = [
    ("ftmo_cfd", "https://ftmo.com/wp-json/ftmo/symbols", "json", None),
    ("ftmo_futures", "https://ftmo.com/en/futures/faq/which-instruments-can-i-trade-with-ftmo-futures/", "html", "Standard and Mini"),
    ("topstep", "https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade", "html", "Permitted Products"),
    ("mffu", "https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list", "html", "CME Instrument Name"),
    ("lucid", "https://support.lucidtrading.com/en/articles/11508978-approved-products-and-commissions", "html", "Symbol Name"),
    ("tradeday", "https://tradeday.freshdesk.com/en/support/solutions/articles/103000008862-what-are-the-permitted-products-guidelines-", "html", "TradeDay only allows"),
    ("blueguardian", "https://help.blueguardian.com/en/articles/9661525-platform-rules", "html", "Tradable Instruments"),
    ("blueguardian_search_vix", "https://help.blueguardian.com/en/?q=VIX", "html", "couldn't find"),
    ("mffu_search_vix", "https://help.myfundedfutures.com/en/?q=VIX", "html", None),
    ("cft_faq", "https://cryptofundtrader.com/faq", "html", "What instruments can I trade"),
    ("cft_help", "https://help.cryptofundtrader.com/", "html", None),
]


def fetch(url):
    r = subprocess.run(
        ["curl", "-sSL", "--compressed", "-m", "40", "-A", UA, "-w", "\n__HTTP__%{http_code}", url],
        capture_output=True, text=True, errors="ignore")
    body, _, code = r.stdout.rpartition("\n__HTTP__")
    return code.strip() or "000", body, r.stderr.strip()


def to_text(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for firm, url, kind, marker in PAGES:
        code, body, err = fetch(url)
        lines = [f"url: {url}", f"http: {code}"]
        if err:
            lines.append(f"error: {err}")
        hits = []
        if code == "200" and kind == "json":
            syms = json.loads(body)["data"]["symbols"]
            classes = {}
            for s in syms:
                classes.setdefault(s["assetClass"], []).append(s["code"])
                blob = json.dumps(s)
                if PAT.search(s["code"] + " " + s["name"]) or re.search(r"(?i)vix|volatility", blob):
                    hits.append(s["code"] + " | " + s["name"])
            lines.append(f"symbols: {len(syms)}")
            for c, codes in sorted(classes.items()):
                lines.append(f"{c} ({len(codes)}): " + ", ".join(sorted(codes)))
            n = len(syms)
        elif code == "200":
            text = to_text(body)
            n = len(text)
            i = text.find(marker) if marker else -1
            lines.append("excerpt: " + (text[i:i + 3500] if i >= 0 else text[:1500]))
            for m in PAT.finditer(text):
                hits.append(text[max(0, m.start() - 120):m.end() + 120])
        else:
            n = 0
        lines.append(f"hits: {len(hits)}")
        lines += ["  " + h for h in hits]
        (OUT / f"{firm}.txt").write_text("\n".join(lines) + "\n")
        rows.append((firm, code, n, len(hits)))
    print(f"{'source':26s} http  size  vol-hits")
    for r in rows:
        print(f"{r[0]:26s} {r[1]:>4s} {r[2]:6d} {r[3]:5d}")


if __name__ == "__main__":
    main()
