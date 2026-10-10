#!/usr/bin/env python3
"""Send-day product re-check for VXO outreach (zero spend, no login, public data only).

For every product a drafted message names, answers the questions in SEND_QUEUE.md's send-day
checklist: is it still public, in stock, at full price, and not tagged as hidden / final sale?

Reads the brand's public Shopify feed (`/products.json`, paged) and then loads the public
product page itself (`/products/<handle>`) to catch redirects and 404s the feed doesn't show.

Usage
  python3 products_check.py lakepajamas.com "oat heather tour"
  python3 products_check.py thefoggydog.com "gingerbread man" "evergreen candy canes"
  python3 products_check.py danarebeccadesigns.com "ava bea interval" --json out.json

Each query is a case-insensitive substring of the product title (or an exact handle).
Exit code 0 = every query has at least one clean match; 1 = something needs a human look.

Flags reported (any one makes the product unfit to name in a message):
  HIDDEN    tag contains redirect / hidden / 404 / unlisted / exclude-search / exclude-product
  FINAL     tag or title says final sale / final farewell / last chance / archive
  MARKDOWN  compare_at_price above price on any available variant (a sale, not full price)
  OOS       no variant available
  PARTIAL   some variants unavailable (fine to name, but say which ones are in stock)
  PAGE!=200 the public product page does not load as itself (redirect or error)
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
HIDDEN_WORDS = ("redirect", "hidden", "404", "unlisted", "do-not-show", "noindex",
                "exclude-search", "exclude_search", "search-exclude", "exclude-product")
# App tags such as exclude_rebuy / exclude-set only steer upsell widgets; they are listed, not flagged.
INFO_WORDS = ("exclude",)
FINAL_WORDS = ("final sale", "final-sale", "finalsale", "final farewell", "final-farewell",
               "last chance", "archive", "discontinued")


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read()


def feed(domain, max_pages=20):
    out = []
    for page in range(1, max_pages + 1):
        _, _, body = get(f"https://{domain}/products.json?limit=250&page={page}")
        items = json.loads(body).get("products", [])
        if not items:
            break
        out.extend(items)
        time.sleep(0.5)
    return out


def page_status(domain, handle):
    url = f"https://{domain}/products/{handle}"
    try:
        status, final, _ = get(url)
        same = final.rstrip("/").split("?")[0].endswith(f"/products/{handle}")
        return status if same else f"redirect->{final}"
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network trouble: report, don't guess
        return f"error:{type(e).__name__}"


def assess(domain, p):
    tags = [t.lower() for t in (p.get("tags") or [])] if isinstance(p.get("tags"), list) \
        else [t.strip().lower() for t in str(p.get("tags") or "").split(",")]
    title = p.get("title", "")
    variants = p.get("variants", [])
    avail = [v for v in variants if v.get("available")]
    flags = []
    if any(w in t for t in tags for w in HIDDEN_WORDS):
        flags.append("HIDDEN")
    if any(w in t for t in tags + [title.lower()] for w in FINAL_WORDS):
        flags.append("FINAL")
    marked = [v for v in avail if v.get("compare_at_price") and
              float(v["compare_at_price"]) > float(v.get("price") or 0)]
    if marked:
        flags.append("MARKDOWN")
    if not avail:
        flags.append("OOS")
    elif len(avail) < len(variants):
        flags.append("PARTIAL")
    status = page_status(domain, p["handle"])
    if status != 200:
        flags.append("PAGE!=200")
    prices = sorted({float(v.get("price") or 0) for v in variants})
    return {
        "handle": p["handle"], "title": title, "published_at": p.get("published_at"),
        "available": f"{len(avail)}/{len(variants)}",
        "unavailable": [v.get("title") for v in variants if not v.get("available")][:12],
        "price": prices[0] if prices else None, "price_max": prices[-1] if prices else None,
        "compare_at": max((float(v["compare_at_price"]) for v in marked), default=None),
        "page": status, "flags": flags,
        "flag_tags": [t for t in tags if any(w in t for w in HIDDEN_WORDS + FINAL_WORDS + INFO_WORDS)],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--limit", type=int, default=6, help="max matches shown per query")
    a = ap.parse_args()
    products = feed(a.domain)
    result, ok = {"domain": a.domain, "feed_size": len(products), "checked_utc":
                  time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "queries": {}}, True
    print(f"{a.domain}: {len(products)} public products in feed")
    for q in a.queries:
        ql = q.lower()
        hits = [p for p in products if p["handle"] == ql or ql in p.get("title", "").lower()][: a.limit]
        rows = [assess(a.domain, p) for p in hits]
        clean = [r for r in rows if not set(r["flags"]) - {"PARTIAL"}]
        ok &= bool(clean)
        result["queries"][q] = rows
        print(f"  [{q}] {len(hits)} match(es), {len(clean)} clean")
        for r in rows:
            fl = ",".join(r["flags"]) or "OK"
            ca = f" (was {r['compare_at']})" if r["compare_at"] else ""
            print(f"    {fl:<22} {r['available']:>6}  ${r['price']}{ca}  {r['title']}  /products/{r['handle']}  page={r['page']}")
            if r["unavailable"] and "PARTIAL" in r["flags"]:
                print(f"      out: {', '.join(map(str, r['unavailable']))}")
            if r["flag_tags"]:
                print(f"      tags: {', '.join(r['flag_tags'])}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(result, f, indent=1)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
