#!/usr/bin/env python3
"""Margin guard for the gua sha store.

Sits on the Shopify orders/create webhook. For every order it recomputes the
real contribution margin from the live cost inputs and decides one of three
things: OK, WARN, STOP. It does not place supplier orders and it does not
touch AliExpress -- that is AutoDS's job, and browser automation against
AliExpress risks the account. This guards the number that actually kills
dropshipping stores: an order that ships at a loss because a supplier raised
a price and nobody noticed.

Standard library only. No install step.

    python3 margin_guard.py serve --port 8787
    python3 margin_guard.py check --price 42 --units 1
    python3 margin_guard.py replay order.json

The webhook secret comes from the environment:

    export SHOPIFY_WEBHOOK_SECRET='...'

Without it, serve refuses to start -- an unverified webhook endpoint is an
open door for anyone who finds the URL.
"""

import argparse
import base64
import csv
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE / "config.json"

OK, WARN, STOP = "OK", "WARN", "STOP"

LOG_FIELDS = [
    "logged_at",
    "order_number",
    "order_id",
    "created_at",
    "units",
    "net_revenue",
    "gross_charged",
    "product_cost",
    "packaging",
    "supplier_shipping",
    "payment_fee",
    "platform_fee",
    "refund_reserve",
    "support_cost",
    "app_cost",
    "total_cost",
    "contribution",
    "cm_pct",
    "break_even_roas",
    "verdict",
    "reasons",
]


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def load_config(path=None):
    path = Path(path) if path else DEFAULT_CONFIG
    with path.open(encoding="utf-8") as fh:
        cfg = json.load(fh)
    cfg["_dir"] = path.parent
    return cfg


def _resolve(cfg, key, fallback):
    value = cfg.get(key) or fallback
    p = Path(value)
    return p if p.is_absolute() else cfg["_dir"] / p


# --------------------------------------------------------------------------
# the economics
# --------------------------------------------------------------------------

def evaluate(cfg, *, net_revenue, gross_charged, units, line_items=None):
    """Recompute contribution for one order and return the verdict.

    net_revenue   what we keep before costs: discounted subtotal + shipping
                  charged to the customer, excluding tax.
    gross_charged what the card was actually charged, including tax. Payment
                  processors take their cut off this, not off net revenue --
                  getting that wrong understates the fee on every order.
    """
    units = max(int(units), 1)

    if line_items:
        product_cost = 0.0
        for item in line_items:
            sku = item.get("sku") or ""
            qty = int(item.get("quantity") or 0)
            unit_cost = cfg["cost_per_sku"].get(sku, cfg["default_unit_cost"])
            product_cost += unit_cost * qty
    else:
        product_cost = cfg["default_unit_cost"] * units

    packaging = cfg["packaging_per_order"] + cfg["packaging_per_unit"] * units
    supplier_shipping = (
        cfg["supplier_shipping_per_order"]
        + cfg["supplier_shipping_per_extra_unit"] * (units - 1)
    )
    payment_fee = gross_charged * cfg["payment_fee_pct"] / 100.0 + cfg["payment_fee_fixed"]
    # Shopify's third-party-gateway surcharge. Israel is not a supported
    # Shopify Payments country, so this is charged on every order for as long
    # as the store exists -- it is not a fee that goes away with volume, only
    # one that shrinks with a higher plan tier.
    platform_fee = gross_charged * cfg.get("platform_fee_pct", 0.0) / 100.0
    refund_reserve = net_revenue * cfg["refund_rate_pct"] / 100.0
    support_cost = cfg["support_cost_per_order"]
    app_cost = cfg["app_cost_per_order"]

    total_cost = (
        product_cost
        + packaging
        + supplier_shipping
        + payment_fee
        + platform_fee
        + refund_reserve
        + support_cost
        + app_cost
    )
    contribution = net_revenue - total_cost
    cm_pct = (contribution / net_revenue * 100.0) if net_revenue else 0.0
    break_even_roas = (100.0 / cm_pct) if cm_pct > 0 else float("inf")

    t = cfg["thresholds"]
    reasons = []
    verdict = OK

    if contribution <= t["stop_contribution"]:
        verdict = STOP
        reasons.append(
            f"contribution {contribution:.2f} at or below {t['stop_contribution']:.2f} "
            f"- this order ships at a loss before a cent of ad spend"
        )
    else:
        if cm_pct < t["warn_cm_pct"]:
            verdict = WARN
            reasons.append(f"CM {cm_pct:.1f}% below floor {t['warn_cm_pct']:.1f}%")
        if break_even_roas > t["warn_break_even_roas"]:
            verdict = WARN
            reasons.append(
                f"break-even ROAS {break_even_roas:.2f} above ceiling "
                f"{t['warn_break_even_roas']:.2f}"
            )

    return {
        "units": units,
        "net_revenue": round(net_revenue, 2),
        "gross_charged": round(gross_charged, 2),
        "product_cost": round(product_cost, 2),
        "packaging": round(packaging, 2),
        "supplier_shipping": round(supplier_shipping, 2),
        "payment_fee": round(payment_fee, 2),
        "platform_fee": round(platform_fee, 2),
        "refund_reserve": round(refund_reserve, 2),
        "support_cost": round(support_cost, 2),
        "app_cost": round(app_cost, 2),
        "total_cost": round(total_cost, 2),
        "contribution": round(contribution, 2),
        "cm_pct": round(cm_pct, 1),
        "break_even_roas": (
            round(break_even_roas, 2) if break_even_roas != float("inf") else None
        ),
        "verdict": verdict,
        "reasons": reasons,
    }


# --------------------------------------------------------------------------
# Shopify payload -> evaluate()
# --------------------------------------------------------------------------

def _f(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def from_shopify_order(cfg, order):
    line_items = order.get("line_items") or []
    units = sum(int(li.get("quantity") or 0) for li in line_items) or 1

    subtotal = _f(order.get("current_subtotal_price"), _f(order.get("subtotal_price")))
    shipping_charged = sum(_f(sl.get("price")) for sl in (order.get("shipping_lines") or []))
    gross = _f(order.get("current_total_price"), _f(order.get("total_price")))

    net_revenue = subtotal + shipping_charged
    if not gross:
        gross = net_revenue

    result = evaluate(
        cfg,
        net_revenue=net_revenue,
        gross_charged=gross,
        units=units,
        line_items=line_items,
    )
    result["order_id"] = order.get("id")
    result["order_number"] = order.get("order_number") or order.get("name")
    result["created_at"] = order.get("created_at")
    return result


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def append_log(cfg, result):
    path = _resolve(cfg, "log_path", "margin-log.csv")
    is_new = not path.exists()
    row = {k: "" for k in LOG_FIELDS}
    row.update({k: v for k, v in result.items() if k in LOG_FIELDS})
    row["logged_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    row["reasons"] = "; ".join(result.get("reasons") or [])
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LOG_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)
    return path


def notify(cfg, result):
    """Record the verdict, and push it onward if a webhook URL is configured.

    Deliberately dumb: a JSONL file is always written, so a failed push never
    loses the record.
    """
    payload = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "order_number": result.get("order_number"),
        "verdict": result["verdict"],
        "contribution": result["contribution"],
        "cm_pct": result["cm_pct"],
        "break_even_roas": result["break_even_roas"],
        "reasons": result.get("reasons") or [],
        "summary": summarize(result),
    }
    path = _resolve(cfg, "notifications_path", "notifications.jsonl")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    url = cfg.get("notify_webhook_url")
    if not url:
        return
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=10).read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"[margin-guard] notify push failed: {exc}", file=sys.stderr)


def summarize(result):
    roas = result["break_even_roas"]
    roas_text = f"{roas:.2f}" if roas is not None else "n/a"
    head = (
        f"{result['verdict']} order {result.get('order_number') or '?'} "
        f"- {result['units']}u, revenue {result['net_revenue']:.2f}, "
        f"contribution {result['contribution']:.2f} "
        f"({result['cm_pct']:.1f}% CM, break-even ROAS {roas_text})"
    )
    if result.get("reasons"):
        head += "\n  " + "\n  ".join(result["reasons"])
    return head


# --------------------------------------------------------------------------
# webhook server
# --------------------------------------------------------------------------

def verify_hmac(secret, raw_body, header_value):
    if not header_value:
        return False
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(expected, header_value)


def make_handler(cfg, secret):
    class Handler(BaseHTTPRequestHandler):
        server_version = "margin-guard/1.0"

        def _send(self, code, body=b"", content_type="text/plain; charset=utf-8"):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def do_GET(self):
            if self.path.rstrip("/") == "/health":
                self._send(200, b"ok")
            else:
                self._send(404, b"not found")

        def do_POST(self):
            if self.path.rstrip("/") != "/webhooks/shopify/orders-create":
                self._send(404, b"not found")
                return

            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""

            if not verify_hmac(secret, raw, self.headers.get("X-Shopify-Hmac-Sha256")):
                # Shopify retries on non-2xx; 401 is correct for a forged call.
                self._send(401, b"bad hmac")
                return

            try:
                order = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                # Malformed body will never parse on retry, so accept and drop it.
                self._send(200, b"unparseable, dropped")
                return

            result = from_shopify_order(cfg, order)
            append_log(cfg, result)
            notify(cfg, result)
            print(f"[margin-guard] {summarize(result)}", flush=True)

            # Always 200: a non-2xx makes Shopify retry, which would double-log
            # an order we have already handled.
            self._send(200, result["verdict"].encode("utf-8"))

        def log_message(self, fmt, *args):
            pass  # the verdict line above is the log

    return Handler


def cmd_serve(args):
    cfg = load_config(args.config)
    secret = os.environ.get("SHOPIFY_WEBHOOK_SECRET")
    if not secret:
        sys.exit(
            "SHOPIFY_WEBHOOK_SECRET is not set. Refusing to serve an unverified "
            "webhook endpoint."
        )
    server = HTTPServer((args.host, args.port), make_handler(cfg, secret))
    print(
        f"[margin-guard] listening on http://{args.host}:{args.port}"
        f"/webhooks/shopify/orders-create",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[margin-guard] stopped", flush=True)


def cmd_check(args):
    cfg = load_config(args.config)
    net = args.price if args.revenue is None else args.revenue
    gross = args.gross if args.gross is not None else net
    result = evaluate(cfg, net_revenue=net, gross_charged=gross, units=args.units)
    print(summarize(result))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict"] != STOP else 1


def cmd_replay(args):
    cfg = load_config(args.config)
    with open(args.order, encoding="utf-8") as fh:
        order = json.load(fh)
    result = from_shopify_order(cfg, order)
    print(summarize(result))
    if args.log:
        append_log(cfg, result)
        notify(cfg, result)
    return 0 if result["verdict"] != STOP else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", help="path to config.json")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("serve", help="run the webhook listener")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8787)
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("check", help="evaluate a hypothetical order")
    p.add_argument("--price", type=float, default=42.0, help="net revenue if --revenue omitted")
    p.add_argument("--revenue", type=float, help="net revenue, excluding tax")
    p.add_argument("--gross", type=float, help="amount charged, including tax")
    p.add_argument("--units", type=int, default=1)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("replay", help="evaluate a saved Shopify order payload")
    p.add_argument("order", help="path to an order JSON file")
    p.add_argument("--log", action="store_true", help="also write to the log and notify")
    p.set_defaults(func=cmd_replay)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
