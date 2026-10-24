#!/usr/bin/env python3
"""Public Meta Ad Library reader for lead scoring (zero spend, no login).

Loads the PUBLIC Meta Ad Library (facebook.com/ads/library) in headless Chromium and returns,
per brand Page: active US ad count, the video/image filter counts, and a card-level read of the
ads the page server-renders (format, start date, days running, video share, AI-media flag).

Why a browser: plain curl gets HTTP 403, but the page still renders because the data ships inside
the HTML as JSON (`search_results_connection`). We read that JSON, not the pixels.

Usage
  # 1. find a brand's Page ID (keyword search, grouped by Page)
  python3 ad_library.py find "The Foggy Dog"
  python3 ad_library.py find "Moment@drinkmoment.com"   # NAME@DOMAIN: rank Pages whose ads link to the domain

  # 2. read one or more Pages (ID from step 1, or from the dossier)
  python3 ad_library.py page 525487920847043 --label "The Foggy Dog"
  python3 ad_library.py page 525487920847043 1234567890 --json out.json

  # 3. one step: resolve the brand, then read it. Give the shop domain whenever you know it:
  #    generic names ("Moment") match dozens of advertisers; the domain pins the right Page.
  python3 ad_library.py brand "The Foggy Dog@thefoggydog.com" "AUrate@auratenewyork.com"

  # offline parser check (no network)
  python3 ad_library.py --selftest

Output: a markdown table on stdout (or JSON with --json PATH, '-' for stdout).

Honest limits (keep these in every dossier that quotes the numbers)
  * Counts flicker: about one load in four renders "No ads match". Every count is read up to
    --tries times and must be confirmed by a second load that agrees within 10 %; otherwise it is
    marked `unconfirmed`.
  * The media_type=video filter counts any ad holding ONE video asset, including dynamic (DCO)
    ads that are mostly stills. `video_filter_share` therefore OVERSTATES video. The card-level
    `card_video_share` (first ~30 cards, Meta's default order = highest impressions first) is the
    better "creative need" signal; quote both.
  * Only the first page of cards (~30) is server-rendered. --scroll N tries to load more, but on
    2026-10-09 Meta answered every logged-out scroll request with "Rate limit exceeded", so expect
    30 cards; the result says so in `scroll_note`. Never log in to get around it.
  * "Running 60+ days" is a longevity proxy for a winner, not a performance fact.
  * Public data only. No login, no cookies, no API key, nothing is posted. Be polite: one load at a
    time with --delay seconds between loads.

Requires: playwright (python) and a Chromium build. Default executable:
/opt/pw-browsers/chromium-1194/chrome-linux/chrome (override with --chrome or $AD_LIB_CHROME).
Outbound traffic goes through $HTTPS_PROXY when set; the proxy CA is already in the browser NSS store,
so TLS verification stays ON (never add --ignore-certificate-errors).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

DEFAULT_CHROME = os.environ.get("AD_LIB_CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
BASE = "https://www.facebook.com/ads/library/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")


# ----------------------------------------------------------------------------- URLs
def page_url(page_id: str, media: str = "all", country: str = "US") -> str:
    q = {"active_status": "active", "ad_type": "all", "country": country,
         "is_targeted_country": "false", "media_type": media,
         "search_type": "page", "view_all_page_id": page_id}
    return BASE + "?" + urllib.parse.urlencode(q)


def keyword_url(term: str, media: str = "all", country: str = "US", exact: bool = True) -> str:
    q = {"active_status": "active", "ad_type": "all", "country": country,
         "is_targeted_country": "false", "media_type": media,
         "q": f'"{term}"' if exact else term,
         "search_type": "keyword_exact_phrase" if exact else "keyword_unordered"}
    return BASE + "?" + urllib.parse.urlencode(q)


# ----------------------------------------------------------------------------- parsing
SCRIPT_RE = re.compile(r'<script type="application/json"[^>]*>(.*?)</script>', re.S)
COUNT_TXT_RE = re.compile(r"(~?)([\d,]+) results?")


def _walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                yield v
            yield from _walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v, key)


def parse_connections(html: str, extra_bodies: list[str] | None = None) -> list[dict]:
    """Return every `search_results_connection` object found in the HTML and in GraphQL bodies."""
    out = []
    blobs = [m for m in SCRIPT_RE.findall(html) if "search_results_connection" in m]
    for b in extra_bodies or []:
        if "search_results_connection" not in b:
            continue
        b = b.removeprefix("for (;;);")
        blobs.extend(line for line in b.splitlines() if "search_results_connection" in line)
    for b in blobs:
        try:
            j = json.loads(b)
        except ValueError:
            continue
        out.extend(c for c in _walk(j, "search_results_connection") if isinstance(c, dict))
    return out


def ads_from_connections(conns: list[dict]) -> list[dict]:
    ads, seen = [], set()
    for c in conns:
        for e in c.get("edges") or []:
            for r in (e.get("node") or {}).get("collated_results") or []:
                aid = r.get("ad_archive_id")
                if aid and aid not in seen:
                    seen.add(aid)
                    ads.append(r)
    return ads


def classify(ad: dict) -> str:
    """'video' if the creative carries any video, else 'image' (or 'other' when empty)."""
    s = ad.get("snapshot") or {}
    if s.get("videos") or s.get("extra_videos"):
        return "video"
    cards = s.get("cards") or []
    if any(c.get("video_hd_url") or c.get("video_sd_url") for c in cards):
        return "video"
    if s.get("images") or s.get("extra_images") or any(c.get("original_image_url") or c.get("resized_image_url") for c in cards):
        return "image"
    return "other"


def summarize_cards(ads: list[dict], now: float | None = None) -> dict:
    now = now or time.time()
    n = len(ads)
    if not n:
        return {"cards_read": 0}
    kinds = [classify(a) for a in ads]
    fmts: dict[str, int] = {}
    for a in ads:
        f = (a.get("snapshot") or {}).get("display_format") or "?"
        fmts[f] = fmts.get(f, 0) + 1
    days = []
    for a in ads:
        sd = a.get("start_date")
        if isinstance(sd, (int, float)) and sd > 0:
            days.append(int((now - sd) // 86400))
    starts = sorted((a.get("start_date") for a in ads if isinstance(a.get("start_date"), (int, float))), reverse=True)
    vid = kinds.count("video")
    return {
        "cards_read": n,
        "card_video": vid,
        "card_image": kinds.count("image"),
        "card_video_share": round(vid / n, 3),
        "display_formats": dict(sorted(fmts.items(), key=lambda kv: -kv[1])),
        "started_last_30d": sum(1 for d in days if d <= 30),
        "running_60d_plus": sum(1 for d in days if d >= 60),
        "oldest_days": max(days) if days else None,
        "newest_start": datetime.fromtimestamp(starts[0], timezone.utc).date().isoformat() if starts else None,
        "ai_flagged": sum(1 for a in ads if a.get("contains_digital_created_media")),
        "platforms": sorted({p for a in ads for p in (a.get("publisher_platform") or [])}),
    }


def text_count(txt: str) -> tuple[int | None, bool]:
    """(count, approximate) from the visible '~220 results' line, or (0, False) for 'No ads match'."""
    m = COUNT_TXT_RE.search(txt or "")
    if m:
        return int(m.group(2).replace(",", "")), bool(m.group(1))
    if txt and "No ads match" in txt:
        return 0, False
    return None, False


# ----------------------------------------------------------------------------- browser
class Library:
    def __init__(self, chrome: str, delay: float, tries: int, wait_ms: int, verbose: bool):
        self.chrome, self.delay, self.tries, self.wait_ms, self.verbose = chrome, delay, tries, wait_ms, verbose
        self._pw = self._browser = None
        self._last = 0.0

    async def __aenter__(self):
        from playwright.async_api import async_playwright  # imported late so --help works without it
        self._pw = await async_playwright().start()
        kw = {"headless": True}
        if os.path.exists(self.chrome):
            kw["executable_path"] = self.chrome
        if os.environ.get("HTTPS_PROXY"):
            kw["proxy"] = {"server": os.environ["HTTPS_PROXY"]}
        self._browser = await self._pw.chromium.launch(**kw)
        return self

    async def __aexit__(self, *exc):
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()

    def log(self, *a):
        if self.verbose:
            print("[ad_library]", *a, file=sys.stderr, flush=True)

    async def load(self, url: str, scroll: int = 0) -> dict:
        """One fresh context per load (no cookies carried over). Returns html, text, gql bodies."""
        gap = self.delay - (time.time() - self._last)
        if gap > 0:
            await asyncio.sleep(gap)
        ctx = await self._browser.new_context(user_agent=UA, locale="en-US", viewport={"width": 1366, "height": 900})
        pg = await ctx.new_page()
        bodies: list[str] = []

        async def on_resp(r):
            if "graphql" in r.url:
                try:
                    bodies.append(await r.text())
                except Exception:
                    pass
        pg.on("response", on_resp)
        status = None
        html = txt = ""
        try:
            resp = await pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            status = resp.status if resp else None
            await pg.wait_for_timeout(self.wait_ms)
            for _ in range(scroll):
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await pg.wait_for_timeout(2500)
            for _ in range(6):  # the page re-navigates once to add sort params
                try:
                    html = await pg.content()
                    txt = await pg.inner_text("body")
                    break
                except Exception:
                    await pg.wait_for_timeout(2500)
        finally:
            await ctx.close()
            self._last = time.time()
        return {"status": status, "html": html, "text": txt, "gql": bodies}

    async def count(self, url: str) -> dict:
        """Read the result count, retrying flicker; confirm with a second agreeing load."""
        reads: list[int] = []
        approx = False
        first_load = None
        for i in range(self.tries):
            r = await self.load(url)
            c, ap = text_count(r["text"])
            conns = parse_connections(r["html"], r["gql"])
            if conns and isinstance(conns[0].get("count"), int):
                c = conns[0]["count"]  # exact server count beats the rounded "~220" text
                ap = False
            self.log("load", i + 1, "status", r["status"], "count", c)
            if first_load is None and ads_from_connections(conns):
                first_load = r  # keep a load that actually carried ad cards
            if c is None or c == 0:
                continue  # 'No ads match' flicker or failed render: try again
            reads.append(c)
            approx = approx or ap
            if len(reads) >= 2 and abs(reads[-1] - reads[-2]) <= max(2, 0.1 * reads[-1]):
                break
        if not reads:
            return {"count": 0, "confirmed": False, "reads": [], "approx": False, "load": first_load}
        confirmed = len(reads) >= 2 and abs(reads[-1] - reads[-2]) <= max(2, 0.1 * reads[-1])
        return {"count": reads[-1], "confirmed": confirmed, "reads": reads, "approx": approx, "load": first_load}


# ----------------------------------------------------------------------------- commands
def total_needs_cards(r: dict) -> bool:
    return bool(r.get("count"))


async def read_page(lib: Library, page_id: str, label: str | None, country: str, scroll: int) -> dict:
    allr = await lib.count(page_url(page_id, "all", country))
    vidr = await lib.count(page_url(page_id, "video", country))
    imgr = await lib.count(page_url(page_id, "image", country))
    ads = []
    if allr["load"]:
        ads = ads_from_connections(parse_connections(allr["load"]["html"], allr["load"]["gql"]))
    for _ in range(2 if total_needs_cards(allr) and not ads else 0):  # count came from text only: fetch cards
        r = await lib.load(page_url(page_id, "all", country))
        ads = ads_from_connections(parse_connections(r["html"], r["gql"]))
        if ads:
            break
    if scroll:
        r = await lib.load(page_url(page_id, "all", country), scroll=scroll)
        more = ads_from_connections(parse_connections(r["html"], r["gql"]))
        known = {a["ad_archive_id"] for a in ads}
        ads += [a for a in more if a["ad_archive_id"] not in known]
        scroll_limited = any("Rate limit exceeded" in b for b in r["gql"])
    else:
        scroll_limited = None
    page_name = next((a.get("page_name") for a in ads if a.get("page_name")), None)
    total = allr["count"]
    res = {
        "label": label or page_name or page_id,
        "page_id": page_id,
        "page_name": page_name,
        "country": country,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": page_url(page_id, "all", country),
        "active_ads": total,
        "active_confirmed": allr["confirmed"],
        "active_reads": allr["reads"],
        "video_filter": vidr["count"],
        "image_filter": imgr["count"],
        "filters_confirmed": vidr["confirmed"] and imgr["confirmed"],
        "video_filter_share": round(vidr["count"] / total, 3) if total else None,
    }
    res.update(summarize_cards(ads))
    if scroll_limited:
        res["scroll_note"] = ("Meta answered the scroll requests with 'Rate limit exceeded' (logged-out viewers get "
                              "only the first ~30 cards); card stats cover those cards only.")
    if not total:
        res["note"] = "No active ads seen in any load (or the page never rendered). Re-run before scoring 0."
    return res


async def find(lib: Library, term: str, country: str, domain: str | None = None, scroll: int = 2) -> list[dict]:
    """Keyword search (exact phrase) → Pages, ranked: exact name, name contains term, ad links to domain."""
    dom = (domain or "").lower().removeprefix("www.")
    queries = [term]
    if dom:  # ads link to the shop: the domain stem ("drinkmoment") pins generic names ("Moment")
        queries.append(dom.split(".")[0])
    ads: list[dict] = []
    for q in queries:
        got: list[dict] = []
        for _ in range(2):  # the keyword page flickers too
            r = await lib.load(keyword_url(q, "all", country), scroll=scroll)
            got = ads_from_connections(parse_connections(r["html"], r["gql"]))
            if got:
                break
        ads += got
        if dom and any(dom in json.dumps(a.get("snapshot") or {}).lower() for a in got):
            break  # found the shop's ads; no need for the fallback query
    pages: dict[str, dict] = {}
    for a in ads:
        pid = a.get("page_id")
        if not pid:
            continue
        snap = a.get("snapshot") or {}
        p = pages.setdefault(pid, {"page_id": pid, "page_name": a.get("page_name"), "ads_in_sample": 0,
                                   "likes": snap.get("page_like_count"), "profile": snap.get("page_profile_uri"),
                                   "domains": set()})
        p["ads_in_sample"] += 1
        links = [snap.get("caption") or "", snap.get("link_url") or ""]
        links += [(c.get("link_url") or "") + " " + (c.get("caption") or "") for c in snap.get("cards") or []]
        for l in links:
            m = re.search(r"([a-z0-9-]+\.[a-z.]{2,})", l.lower())
            if m:
                p["domains"].add(m.group(1).removeprefix("www."))
    norm = _norm(term)
    for p in pages.values():
        name = _norm(p["page_name"] or "")
        p["exact_name_match"] = name == norm
        p["name_contains"] = bool(norm) and (norm in name or (len(name) >= 4 and name in norm))
        p["domain_match"] = bool(dom) and any(dom in d for d in p["domains"])
        p["domains"] = sorted(p["domains"])[:5]
    return sorted(pages.values(), key=lambda p: (not p["domain_match"], not p["exact_name_match"],
                                                 not p["name_contains"], -p["ads_in_sample"]))


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def to_markdown(rows: list[dict]) -> str:
    h = ("| Brand | Page ID | Active ads (US) | Video filter | Card video share | Cards read | "
         "Started ≤30 d | Running ≥60 d | AI-flagged | Confirmed |\n|---|---|---|---|---|---|---|---|---|---|")
    lines = [h]
    for r in rows:
        if "error" in r:
            lines.append(f"| {r.get('label')} | {r.get('page_id')} | error: {r['error']} | | | | | | | |")
            continue
        vfs = f"{r['video_filter']} ({r['video_filter_share']:.0%})" if r.get("video_filter_share") is not None else str(r.get("video_filter"))
        cvs = f"{r['card_video']}/{r['cards_read']} ({r['card_video_share']:.0%})" if r.get("cards_read") else "—"
        conf = "yes" if r["active_confirmed"] and r["filters_confirmed"] else "partial" if r["active_confirmed"] else "NO"
        lines.append(f"| {r['label']} | {r['page_id']} | {r['active_ads']} | {vfs} | {cvs} | {r.get('cards_read', 0)} | "
                     f"{r.get('started_last_30d', '—')} | {r.get('running_60d_plus', '—')} | {r.get('ai_flagged', '—')} | {conf} |")
    lines.append("")
    lines.append("Source: public Meta Ad Library, US, active, read with skills/ad-director/scripts/research/ad_library.py "
                 f"on {datetime.now(timezone.utc).date().isoformat()}. Video filter counts any ad with one video asset "
                 "(overstates video); card share = first ~30 cards in Meta's default order. Quote both.")
    return "\n".join(lines)


async def amain(a) -> int:
    rows: list[dict] = []
    async with Library(a.chrome, a.delay, a.tries, a.wait_ms, a.verbose) as lib:
        if a.cmd == "find":
            for term in a.terms:
                name, _, dom = term.partition("@")
                res = await find(lib, name, a.country, dom or None)
                rows.append({"term": term, "pages": res})
                if not a.json:
                    print(f"## {term}")
                    if not res:
                        print("no Pages found in the first page of results (flicker? re-run)")
                    for p in res:
                        flag = ("DOMAIN " if p["domain_match"] else "") + ("EXACT " if p["exact_name_match"] else "NAME " if p["name_contains"] else "")
                        print(f"{flag}{p['page_id']}  {p['page_name']}  ads_in_sample={p['ads_in_sample']}  likes={p['likes']}  {','.join(p['domains'])}  {p['profile'] or ''}")
        else:
            targets: list[tuple[str, str | None]] = []
            if a.cmd == "page":
                targets = [(pid, a.label if len(a.ids) == 1 else None) for pid in a.ids]
            else:  # brand
                for spec in a.names:
                    name, _, dom = spec.partition("@")
                    cands = await find(lib, name, a.country, dom or None)
                    # accept: the domain matches, or (no domain given) exactly one exact-name Page
                    ok = [c for c in cands if c["domain_match"]] if dom else [c for c in cands if c["exact_name_match"]]
                    if len(ok) != 1 and not (dom and ok):
                        rows.append({"label": name, "page_id": None,
                                     "error": f"{len(ok)} Pages matched; run `find` and pass the ID with `page`",
                                     "candidates": [{k: c[k] for k in ("page_id", "page_name", "domains")} for c in cands[:5]]})
                        continue
                    targets.append((ok[0]["page_id"], name))
            for pid, label in targets:
                try:
                    rows.append(await read_page(lib, pid, label, a.country, a.scroll))
                except Exception as e:  # keep going for the other brands
                    rows.append({"label": label or pid, "page_id": pid, "error": f"{type(e).__name__}: {e}"})
            if not a.json:
                print(to_markdown(rows))
    if a.json:
        s = json.dumps(rows, indent=2, ensure_ascii=False)
        if a.json == "-":
            print(s)
        else:
            with open(a.json, "w") as f:
                f.write(s)
            print(f"wrote {a.json}", file=sys.stderr)
    return 0 if rows and not any("error" in r for r in rows) else 1


def selftest() -> int:
    """Offline check of the parser on a synthetic page (no network)."""
    now = time.time()
    def ad(i, video, days):
        card = {"video_hd_url": "v.mp4"} if video else {"original_image_url": "i.jpg"}
        return {"ad_archive_id": str(i), "page_id": "1", "page_name": "Brand", "start_date": int(now - days * 86400),
                "contains_digital_created_media": i == 0, "publisher_platform": ["FACEBOOK"],
                "snapshot": {"display_format": "VIDEO" if video else "DCO", "cards": [card], "videos": [], "images": []}}
    conn = {"count": 218, "edges": [{"node": {"collated_results": [ad(0, True, 5), ad(1, False, 70), ad(2, False, 10), ad(2, False, 10)]}}]}
    blob = json.dumps({"require": [{"result": {"data": {"ad_library_main": {"search_results_connection": conn}}}}]})
    html = f'<script type="application/json" data-x="1">{blob}</script>'
    ads = ads_from_connections(parse_connections(html))
    s = summarize_cards(ads, now)
    assert len(ads) == 3, ads
    assert s["card_video"] == 1 and s["card_image"] == 2 and s["started_last_30d"] == 2 and s["running_60d_plus"] == 1, s
    assert s["ai_flagged"] == 1 and parse_connections(html)[0]["count"] == 218
    assert text_count("~220 results") == (220, True) and text_count("No ads match") == (0, False)
    print("selftest OK")
    return 0


def main(argv=None) -> int:
    if (argv or sys.argv[1:])[:1] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--country", default="US")
    ap.add_argument("--json", metavar="PATH", help="write JSON to PATH ('-' = stdout) instead of markdown")
    ap.add_argument("--delay", type=float, default=4.0, help="seconds between page loads (be polite)")
    ap.add_argument("--tries", type=int, default=4, help="max loads per count (flicker retries)")
    ap.add_argument("--wait-ms", type=int, default=9000, help="render wait per load")
    ap.add_argument("--chrome", default=DEFAULT_CHROME)
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find", help="keyword search → candidate Pages (NAME or NAME@domain)")
    f.add_argument("terms", nargs="+")
    p = sub.add_parser("page", help="read Page IDs")
    p.add_argument("ids", nargs="+")
    p.add_argument("--label")
    p.add_argument("--scroll", type=int, default=0, help="scroll N times to load more cards")
    b = sub.add_parser("brand", help="resolve NAME or NAME@domain to one Page, then read it")
    b.add_argument("names", nargs="+")
    b.add_argument("--scroll", type=int, default=0)
    a = ap.parse_args(argv)
    if a.cmd == "find":
        a.scroll = 0
    return asyncio.run(amain(a))


if __name__ == "__main__":
    sys.exit(main())
