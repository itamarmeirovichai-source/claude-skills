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

Each query matches when every one of its words is in the product title, in any order, ignoring
case and punctuation (or it is an exact handle). Truncated match lists say how many were cut.
Exit code 0 = every query has at least one clean match; 1 = something needs a human look.

Flags reported (any one makes the product unfit to name in a message):
  HIDDEN    tag contains redirect / hidden / 404 / unlisted / exclude-search / exclude-product,
            or a tag is exactly hide / pre-launch
  FINAL     tag or title says final sale / final farewell / last chance / archive
  MARKDOWN  compare_at_price above price on any available variant (a sale, not full price);
            printed as the per-variant "% off" range (2026-10-25: min price vs max compare-at
            made a standing 25 % promo read as 67 % off)
  OOS       no variant available
  PARTIAL   some variants unavailable (fine to name, but say which ones are in stock)
  PAGE!=200 the public product page does not load as itself (redirect or error)
  SALE-TAG  a tag names a sale event (hesale2026, black-friday, bfcm, doorbuster...), "wholesale"
            excluded. Added 2026-10-25: KREWE tagged its sale picks `hesale2026` before the drop. Tags naming a
            past year ("Doorbusters 2022") are listed under tags but not flagged.
  SALE-LIST (with --sale-scan) the product sits in a sale collection linked from the homepage
            (pre-shop / flash-sale / outlet / black-friday ...), even if its price has not dropped
            yet. Added 2026-10-24: KREWE's "pre-shop-all-sale-he26" listed 213 products, six St. Louis
            frames among them, two days before "SALE PRICES DROP SUNDAY 10AM ET".
  SITEWIDE  (with --sale-scan) the homepage announces a sitewide / checkout discount ("20% off
            everything, no code needed"), so every product is discounted at checkout even though the
            feed shows full price. Added 2026-10-25 (Hawkins October Sale). A product on the
            list is treated like a markdown: don't name it in a message that goes after the drop.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
HIDDEN_WORDS = ("redirect", "hidden", "404", "unlisted", "do-not-show", "noindex",
                "exclude-search", "exclude_search", "search-exclude", "exclude-product")
EXACT_HIDE_TAGS = ("hide", "hide-product", "hide_product", "hidden-product", "pre-launch", "prelaunch")
# App tags such as exclude_rebuy / exclude-set only steer upsell widgets; they are listed, not flagged.
INFO_WORDS = ("exclude",)
# A tag naming a sale event (KREWE "hesale2026" on 231 of 449 products, 2026-10-25, before the
# prices dropped) marks a product picked for the next sale. "wholesale" is not a sale tag.
# App permission tags ("script-sale-allowed" at Foggy, "no-sale", "sale-excluded") are not events.
SALE_TAG_RE = re.compile(r"(?<!whole)(?<!no[-_ ])sale(?!s?[-_ ]?(?:channel|rep|allowed|eligible|exclu))"
                         r"|black[-_ ]?friday|bfcm|cyber|doorbuster", re.I)


def _old_event(tag: str) -> bool:
    """True when a tag names a past year ("Doorbusters 2022"): listed, not flagged."""
    years = [int(y) for y in re.findall(r"20\d\d", tag)]
    return bool(years) and max(years) < time.gmtime().tm_year


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


SALE_WORDS = ("sale", "pre-shop", "preshop", "flash", "outlet", "clearance", "black-friday", "bfcm",
              "cyber", "doorbuster", "warehouse", "promo", "deal", "markdown", "last-chance")


# "applied at checkout" alone is too broad (KREWE's returns page: "return credit ... applied at checkout").
SITEWIDE_RE = re.compile(r"off everything|everything \d+ ?% off|sitewide|site-wide|no code needed"
                         r"|(?:discount|saving|\d+ ?%)[^.]{0,60}applied at checkout", re.I)


def sale_lists(domain):
    """Sale collections linked from the homepage → {collection handle: set(product handles)}."""
    try:
        _, _, body = get(f"https://{domain}/")
    except Exception as e:
        return {"_error": str(e)}
    handles = sorted({h for h in re.findall(r'/collections/([a-z0-9][a-z0-9_-]*)', body.decode("utf-8", "ignore"))
                      if any(w in h for w in SALE_WORDS)})
    out = {}
    # Sitewide checkout discounts never show in products.json (added 2026-10-25: Hawkins' homepage read
    # "OCTOBER SALE: 20% OFF EVERYTHING. NO CODE NEEDED ... Discount applied at checkout" while every
    # lamp we name still listed at full price). Keep the banner text; main() flags every row SITEWIDE.
    text = re.sub(r"<[^>]+>", "\n", re.sub(r"(?s)<(script|style)\b.*?</\1>", "", body.decode("utf-8", "ignore")))
    banner = sorted({ln.strip() for ln in text.splitlines() if 8 < len(ln.strip()) < 160 and SITEWIDE_RE.search(ln)})
    if banner:
        out["_sitewide"] = banner[:4]
    for h in handles[:12]:
        items = []
        for page in range(1, 9):
            try:
                _, _, b = get(f"https://{domain}/collections/{h}/products.json?limit=250&page={page}")
                got = json.loads(b).get("products", [])
            except Exception:
                break
            if not got:
                break
            items.extend(got)
            time.sleep(0.5)
        out[h] = {p["handle"] for p in items}
    return out


def norm(s):
    """Lower-case, punctuation and dashes to spaces, single-spaced."""
    return " ".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


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
    # Strong words (redirect/hidden/404...) always flag. "exclude-*" words are weaker: Rebuy
    # (upsell app) tags like "rebuy-exclude-product" only steer upsell widgets, and a product the
    # brand itself tags "searchable" is public, so neither flags on an exclude-* word (2026-10-11).
    strong = [w for w in HIDDEN_WORDS if not w.startswith("exclude")]
    weak = [w for w in HIDDEN_WORDS if w.startswith("exclude")]
    # Exact short tags ("hide", "hidden-product") are matched whole: "hide" as a substring would hit
    # "rawhide" or "hideaway" (added 2026-10-12: Kinn's pre-launch box was tagged "hide" and slipped).
    if any(t in EXACT_HIDE_TAGS for t in tags) or any(w in t for t in tags for w in strong) or (
            "searchable" not in tags and any(w in t for t in tags if "rebuy" not in t for w in weak)):
        flags.append("HIDDEN")
    if any(w in t for t in tags + [title.lower()] for w in FINAL_WORDS):
        flags.append("FINAL")
    if any(SALE_TAG_RE.search(t) and not _old_event(t) for t in tags):
        flags.append("SALE-TAG")
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
        # Per-variant discount (added 2026-10-25): "$29.25 (was 89.0)" mixed the cheapest variant's
        # price with the dearest variant's compare-at and read a standing 25 % promo as 67 % off
        # (Cuddle Clones pajamas). Report the real range, variant by variant.
        "off_pct": sorted({round(100 * (1 - float(v["price"]) / float(v["compare_at_price"])))
                           for v in marked}) or None,
        "page": status, "flags": flags,
        "flag_tags": [t for t in tags if t in EXACT_HIDE_TAGS or
                      any(w in t for w in HIDDEN_WORDS + FINAL_WORDS + INFO_WORDS) or SALE_TAG_RE.search(t)],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--limit", type=int, default=6, help="max matches shown per query")
    ap.add_argument("--sale-scan", action="store_true",
                    help="also list the homepage's sale collections and flag named products found in them")
    a = ap.parse_args()
    products = feed(a.domain)
    sales = sale_lists(a.domain) if a.sale_scan else {}
    result, ok = {"domain": a.domain, "feed_size": len(products), "checked_utc":
                  time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "queries": {}}, True
    print(f"{a.domain}: {len(products)} public products in feed")
    if a.sale_scan:
        result["sale_lists"] = {c: (sorted(hs) if isinstance(hs, set) else hs) for c, hs in sales.items()}
        print("  sale collections linked from the homepage: " + (", ".join(
            f"{c} ({len(hs)})" for c, hs in sales.items() if not c.startswith("_")) or "none") +
            (f"  [homepage error: {sales['_error']}]" if "_error" in sales else ""))
    if sales.get("_sitewide"):
        print("  SITEWIDE offer on the homepage: " + " | ".join(sales["_sitewide"]))
    for q in a.queries:
        ql = q.lower()
        # Every word of the query must appear in the title, in any order and ignoring dashes/punctuation
        # (2026-10-16: "oat heather tour" missed "Tour ... in Oat Heather", and on 10-12 "holiday hens
        # pet bandana" missed "Holiday Hens - Pet Bandana"). An exact handle still matches.
        words = norm(ql).split()
        matched = [p for p in products if p["handle"] == ql or all(w in norm(p.get("title", "")).split()
                                                                       or w in norm(p.get("title", "")) for w in words)]
        hits = matched[: a.limit]
        rows = [assess(a.domain, p) for p in hits]
        for r in rows:
            inlists = [c for c, hs in sales.items() if not c.startswith("_") and r["handle"] in hs]
            if sales.get("_sitewide"):
                r["flags"].append("SITEWIDE")
            if inlists:
                r["flags"].append("SALE-LIST")
                r["sale_lists"] = inlists
        clean = [r for r in rows if not set(r["flags"]) - {"PARTIAL"}]
        ok &= bool(clean)
        result["queries"][q] = rows
        more = f" (+{len(matched) - len(hits)} more not shown: raise --limit or use the exact handle)" \
            if len(matched) > len(hits) else ""
        print(f"  [{q}] {len(hits)} match(es), {len(clean)} clean{more}")
        for r in rows:
            fl = ",".join(r["flags"]) or "OK"
            pct = r.get("off_pct")
            ca = (f" ({pct[0]}% off)" if len(pct) == 1 else f" ({pct[0]}-{pct[-1]}% off per variant)") if pct else ""
            print(f"    {fl:<22} {r['available']:>6}  ${r['price']}{ca}  {r['title']}  /products/{r['handle']}  page={r['page']}")
            if r["unavailable"] and "PARTIAL" in r["flags"]:
                print(f"      out: {', '.join(map(str, r['unavailable']))}")
            if r["flag_tags"]:
                print(f"      tags: {', '.join(r['flag_tags'])}")
            if r.get("sale_lists"):
                print(f"      in sale collection(s): {', '.join(r['sale_lists'])}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(result, f, indent=1)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
