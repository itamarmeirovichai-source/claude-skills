"""Command line for NEWS-1. Run from the project folder: python -m news1 <command>"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import config, core, ledger, universe
from .http import FetchError, Http


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:+.3f}%"


def _print_stats(s: dict[str, Any]) -> None:
    print(f"Decision: {s['decision']}")
    print(f"Recorded days {s['recorded_days']} | signals {s['signals']} (long {s['long']}, short {s['short']}, unclear {s['unclear']})")
    print(f"Settled trades {s['settled_trades']} | without a price bar {s['no_bar']}")
    for label, key in (("gross", "gross"), ("net 5 bp/side", "net"), ("net 2.5 bp/side", "net_low_cost"), ("net 10 bp/side", "net_high_cost")):
        row = s[key]
        t = "n/a" if row["t"] is None else f"{row['t']:.2f}"
        print(f"  {label:<16} mean per day {_pct(row['mean'])}  t {t}  days {row['days']}")
    print(f"Log: {s['log']['lines']} lines, {s['log']['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="news1", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build-universe", help="build the frozen stock list (once, after the pre-registration)")
    sub.add_parser("open-fetch", help="fetch today's headlines for scoring; records nothing")
    rec = sub.add_parser("record", help="write today's verdicts to the log (refused from 09:25 ET)")
    rec.add_argument("verdicts", help="JSON file mapping every ticker to 1, -1 or 0")
    rec.add_argument("--model", required=True, help="identifier of the model that scored the headlines")
    sub.add_parser("settle", help="compute open-to-close returns for finished days")
    sub.add_parser("status", help="running statistics and the stage decision")
    sub.add_parser("verify", help="check the log's hash chain")
    args = parser.parse_args(argv)
    now = datetime.now(UTC)
    http = Http()
    try:
        if args.command == "build-universe":
            if config.UNIVERSE.exists():
                raise core.Refused("universe.json already exists: the universe is frozen")
            data = universe.build(http, now)
            config.UNIVERSE.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
            print(f"{len(data['tickers'])} tickers chosen after checking {data['checked']} of {data['first_pass']} candidates")
        elif args.command == "open-fetch":
            pending = core.open_fetch(http, core.load_universe(), now)
            config.PENDING.mkdir(parents=True, exist_ok=True)
            path = config.PENDING / f"{pending['date']}.json"
            path.write_text(json.dumps(pending, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"# {pending['date']}  window {pending['window'][0]} .. {pending['window'][1]}")
            print(f"# tickers with news {len(pending['tickers'])} of {pending['universe_size']}, fetch errors {len(pending['errors'])}")
            for ticker, items in sorted(pending["tickers"].items()):
                for item in items:
                    print(f"{ticker} | {item['publisher']} | {item['title']}")
            print(f"# saved to {path}")
        elif args.command == "record":
            day = core.today_et(now).isoformat()
            pending = json.loads((config.PENDING / f"{day}.json").read_text(encoding="utf-8"))
            verdicts = json.loads(Path(args.verdicts).read_text(encoding="utf-8"))
            written = core.record(pending, verdicts, args.model, now, config.LEDGER, core.prompt_sha())
            signals = [e for e in written if e["type"] == "signal"]
            counts = {v: sum(e['verdict'] == v for e in signals) for v in (1, -1, 0)}
            print(f"recorded {len(signals)} signals for {day}: long {counts[1]}, short {counts[-1]}, unclear {counts[0]}")
        elif args.command == "settle":
            rows = core.settle(http, config.LEDGER, config.RESULTS, now)
            print(f"settled {sum(r['status'] == 'ok' for r in rows)} trades, {sum(r['status'] != 'ok' for r in rows)} without a price bar")
            _print_stats(core.stats(config.LEDGER, config.RESULTS))
        elif args.command == "status":
            _print_stats(core.stats(config.LEDGER, config.RESULTS))
        elif args.command == "verify":
            ok, lines, message = ledger.verify(config.LEDGER)
            print(f"{lines} lines: {message}")
            return 0 if ok else 1
    except (core.Refused, FetchError, FileNotFoundError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
