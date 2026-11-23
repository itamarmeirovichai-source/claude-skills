"""Command line for Solana Launch Lab.  `python -m launchlab serve` starts the dashboard."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
from pathlib import Path
from typing import Any

from . import __version__, audit, backfill, db, ingest, paper
from .config import Settings, load_settings
from .providers import solana_rpc
from .providers.base import HttpClient, ProviderError
from .server import NOT_ADVICE, App, make_server


def _print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def _live(settings: Settings, flag: bool) -> Settings:
    """Live connectors are opt-in: LAUNCHLAB_MODE=live or an explicit --live on the command."""
    if flag and not settings.live_enabled:
        return dataclasses.replace(settings, mode="live")
    return settings


def cmd_serve(args: argparse.Namespace, settings: Settings) -> int:
    settings = _live(settings, args.live)
    app = App(settings)
    if not args.no_seed:
        seeded = app.ensure_demo()
        if seeded:
            print(f"Seeded synthetic demo data: {seeded['seeded']['n_tokens']} fake tokens (seed {seeded['seeded']['seed']}).")
    server = make_server(app, args.port)
    host, port = str(server.server_address[0]), int(server.server_address[1])
    print(f"Solana Launch Lab {__version__} — http://{host}:{port}/")
    print(f"Mode: {settings.mode.upper()}" + (" — read-only public-data connectors enabled" if settings.live_enabled
                                              else " — synthetic data only, no network calls"))
    print(NOT_ADVICE)
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


def cmd_seed_demo(args: argparse.Namespace, settings: Settings) -> int:
    _print(App(settings).reset_demo(args.seed, args.tokens))
    return 0


def cmd_paper_run(args: argparse.Namespace, settings: Settings) -> int:
    conn = db.connect(settings.db_path)
    run = paper.run_book(conn, settings, args.book, synthetic=args.book == "demo")
    _print({"run": run, "metrics": paper.book_metrics(conn, args.book, settings)})
    return 0


def cmd_ingest(args: argparse.Namespace, settings: Settings) -> int:
    settings = _live(settings, args.live)
    conn = db.connect(settings.db_path)
    _print(ingest.ingest_mint(conn, settings, args.mint, ingest.Clients.for_settings(settings)))
    return 0


def cmd_discover(args: argparse.Namespace, settings: Settings) -> int:
    settings = _live(settings, args.live)
    conn = db.connect(settings.db_path)
    _print(ingest.discover(conn, settings, ingest.Clients.for_settings(settings)))
    return 0


def cmd_watch(args: argparse.Namespace, settings: Settings) -> int:
    """Collect live launches on a timer for the paper study. Read-only; stop with Ctrl+C."""
    settings = _live(settings, args.live)
    conn = db.connect(settings.db_path)
    clients = ingest.Clients.for_settings(settings)
    done = 0
    try:
        while args.cycles is None or done < args.cycles:
            started = time.time()
            result = ingest.watch_cycle(conn, settings, clients, max_new=args.max_new)
            done += 1
            print(json.dumps({"cycle": done, **result}, default=str), flush=True)
            if args.cycles is None or done < args.cycles:
                time.sleep(max(0.0, args.interval - (time.time() - started)))
    except KeyboardInterrupt:
        print("stopped", file=sys.stderr)
    return 0


def cmd_backfill(args: argparse.Namespace, settings: Settings) -> int:
    """Backtest: read an unselected sample of past launches from the chain and paper-trade the fixed rules."""
    settings = dataclasses.replace(_live(settings, args.live), db_path=Path(args.db).resolve())
    conn = db.connect(settings.db_path)
    workers = max(1, min(args.workers, 6))

    def make_client() -> HttpClient:
        client = solana_rpc.make_client(min_interval_s=0.25 * workers, max_retries=4)
        client.enabled = settings.live_enabled
        return client

    result = backfill.run_backfill(conn, settings, make_client(), settings.solana_rpc_url, hours=args.hours, sample=args.sample,
                                   max_launches=args.max, progress=lambda msg: print(msg, file=sys.stderr, flush=True),
                                   workers=workers, worker_setup=lambda: (db.connect(settings.db_path), make_client()))
    _print(result)
    return 0


def cmd_backfill_report(args: argparse.Namespace, settings: Settings) -> int:
    """Print the finished backtest: plan, coverage, both books, split by launch type, sensitivity runs. No network."""
    path = Path(args.db).resolve()
    if not path.is_file():
        raise ValueError(f"no backtest store at {path}; run `python -m launchlab backfill --live` first")
    _print(backfill.report(db.connect(path), dataclasses.replace(settings, db_path=path)))
    return 0


def cmd_audit(args: argparse.Namespace, settings: Settings) -> int:
    settings = _live(settings, args.live)
    if not settings.live_enabled:
        raise ProviderError("launchlab", "disabled", "audit needs live public data: add --live or set LAUNCHLAB_MODE=live")
    clients = ingest.Clients.for_settings(settings)
    _print(audit.check_claim(clients.gecko, args.mint, audit.parse_utc(args.alert), claimed_cap_usd=args.claimed_cap,
                             claimed_multiple=args.claimed_multiple, rpc=clients.rpc if args.onchain else None,
                             rpc_url=settings.solana_rpc_url))
    return 0


def cmd_verify_log(args: argparse.Namespace, settings: Settings) -> int:
    result = db.verify_event_chain(db.connect(settings.db_path))
    _print(result)
    return 0 if result["ok"] else 1


def cmd_status(args: argparse.Namespace, settings: Settings) -> int:
    _print(App(settings).status())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="launchlab", description="Read-only Solana launch research and paper trading. " + NOT_ADVICE)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    live_help = "enable read-only public-data connectors for this command"

    p = sub.add_parser("serve", help="start the local dashboard")
    p.add_argument("--port", type=int, default=None)
    p.add_argument("--no-seed", action="store_true", help="do not create synthetic demo data on first run")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_serve)

    p = sub.add_parser("seed-demo", help="regenerate the synthetic demo universe and its paper book")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--tokens", type=int, default=300)
    p.set_defaults(fn=cmd_seed_demo)

    p = sub.add_parser("paper-run", help="record new signals and update paper positions")
    p.add_argument("--book", choices=["demo", "live"], default="demo")
    p.set_defaults(fn=cmd_paper_run)

    p = sub.add_parser("ingest", help="fetch public data for one exact mint address")
    p.add_argument("mint")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_ingest)

    p = sub.add_parser("discover", help="import the newest Pump.fun launches from the provider's new-pools list")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_discover)

    p = sub.add_parser("watch", help="repeat: discover new launches, ingest a few, update the live paper book")
    p.add_argument("--interval", type=float, default=60.0, help="seconds between cycles (default 60)")
    p.add_argument("--max-new", type=int, default=2, help="new launches to read in detail per cycle (rate limits)")
    p.add_argument("--cycles", type=int, default=None, help="stop after this many cycles (default: run until Ctrl+C)")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_watch)

    p = sub.add_parser("backfill", help="backtest: sample past launches from the chain and paper-trade the fixed rules")
    p.add_argument("--hours", type=float, default=24.0, help="length of the past window to sample (default 24)")
    p.add_argument("--sample", type=int, default=500, help="number of launches to sample, every k-th (default 500)")
    p.add_argument("--workers", type=int, default=1,
                   help="parallel readers, 1-6. Only useful with your own RPC endpoint: the public one caps getTransaction per IP (default 1)")
    p.add_argument("--db", default="data/backtest.sqlite3", help="separate store for the backtest (default data/backtest.sqlite3)")
    p.add_argument("--max", type=int, default=None, help="read at most this many launches in this run; rerun to resume")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_backfill)

    p = sub.add_parser("backfill-report", help="print a finished backtest with sensitivity runs (no network)")
    p.add_argument("--db", default="data/backtest.sqlite3")
    p.set_defaults(fn=cmd_backfill_report)

    p = sub.add_parser("audit", help="check an 'alert at time T, N× later' claim against market data")
    p.add_argument("mint")
    p.add_argument("--alert", required=True, help="alert time, ISO-8601, UTC assumed (e.g. 2026-11-20T20:52:00Z)")
    p.add_argument("--claimed-cap", type=float, default=None, help="market cap in USD the claim states for the alert")
    p.add_argument("--claimed-multiple", type=float, default=None, help="multiple the claim states, e.g. 24")
    p.add_argument("--onchain", action="store_true", help="also read pool balances from the block at the alert second")
    p.add_argument("--live", action="store_true", help=live_help)
    p.set_defaults(fn=cmd_audit)

    p = sub.add_parser("verify-log", help="verify the hash chain of the event log")
    p.set_defaults(fn=cmd_verify_log)

    p = sub.add_parser("status", help="print counts, provider health and settings (RPC URL redacted)")
    p.set_defaults(fn=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.fn(args, load_settings()))
    except ProviderError as exc:
        print(f"error: {exc.provider}: {exc.message}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
