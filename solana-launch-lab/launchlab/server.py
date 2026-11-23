"""Local JSON API and static dashboard. Loopback only; no authentication because nothing leaves the machine."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from . import __version__, audit, db, ingest, paper, policy, risk
from .config import Settings, is_synthetic_mint, is_valid_mint
from .providers import synthetic
from .providers.base import ProviderError

STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
}
BOOKS = {"demo": True, "live": False}  # book name -> uses synthetic tokens
MAX_BODY = 64 * 1024
NOT_ADVICE = ("Research and paper trading only. Nothing here is financial advice, a buy or sell signal, or a forecast. "
              "No wallet is connected and no transaction can be sent.")


class ApiError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status, self.message = status, message


class App:
    """Holds the single database connection and serialises access to it."""

    def __init__(self, settings: Settings, conn: sqlite3.Connection | None = None, clients: ingest.Clients | None = None):
        self.settings = settings
        self.conn = conn if conn is not None else db.connect(settings.db_path)
        self.clients = clients if clients is not None else ingest.Clients.for_settings(settings)
        self.lock = threading.RLock()

    # ---- helpers ----------------------------------------------------------------------------
    def ensure_demo(self, seed: int = 7, n_tokens: int = 300) -> dict[str, Any] | None:
        """Seed the synthetic universe and its paper book if there is no synthetic data yet."""
        with self.lock:
            if self.conn.execute("SELECT 1 FROM tokens WHERE is_synthetic = 1 LIMIT 1").fetchone():
                return None
            return self.reset_demo(seed, n_tokens)

    def reset_demo(self, seed: int = 7, n_tokens: int = 300) -> dict[str, Any]:
        with self.lock:
            paper.reset_book(self.conn, "demo")
            seeded = synthetic.seed_database(self.conn, synthetic.SyntheticConfig(n_tokens=n_tokens, seed=seed))
            run = paper.run_book(self.conn, self.settings, "demo", synthetic=True)
            return {"seeded": seeded, "paper": run}

    def _token(self, mint: str) -> sqlite3.Row:
        if not (is_valid_mint(mint) or is_synthetic_mint(mint)):
            raise ApiError(400, "enter an exact mint address (tickers are not unique and are not searched)")
        row = self.conn.execute("SELECT * FROM tokens WHERE mint = ?", (mint,)).fetchone()
        if row is None:
            raise ApiError(404, "this mint is not in the local store yet")
        return row

    # ---- GET --------------------------------------------------------------------------------
    def status(self) -> dict[str, Any]:
        with self.lock:
            c = self.conn
            counts = {
                "tokens_synthetic": c.execute("SELECT COUNT(*) FROM tokens WHERE is_synthetic = 1").fetchone()[0],
                "tokens_live": c.execute("SELECT COUNT(*) FROM tokens WHERE is_synthetic = 0").fetchone()[0],
                "observations_synthetic": c.execute("SELECT COUNT(*) FROM observations WHERE is_synthetic = 1").fetchone()[0],
                "observations_live": c.execute("SELECT COUNT(*) FROM observations WHERE is_synthetic = 0").fetchone()[0],
                "conflicts": c.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0],
                "raw_snapshots": c.execute("SELECT COUNT(*) FROM raw_snapshots").fetchone()[0],
            }
            health = [dict(r) for r in c.execute("SELECT * FROM provider_health ORDER BY provider")]
            return {
                "version": __version__, "mode": self.settings.mode, "live_enabled": self.settings.live_enabled,
                "server_time": time.time(), "counts": counts, "provider_health": health,
                "event_log": db.verify_event_chain(c), "settings": self.settings.public_dict(),
                "ruleset": policy.RULESET, "decision_rule": policy.DecisionRule().__dict__, "exit_rule": policy.ExitRule().__dict__,
                "notice": NOT_ADVICE,
            }

    def tokens(self, q: str = "", scope: str = "all", limit: int = 200) -> dict[str, Any]:
        with self.lock:
            sql = ("SELECT t.*, (SELECT COUNT(*) FROM observations o WHERE o.mint = t.mint) AS n_obs,"
                   " (SELECT MAX(observed_at) FROM observations o WHERE o.mint = t.mint) AS last_observed,"
                   " (SELECT decision FROM signals s WHERE s.mint = t.mint ORDER BY s.id DESC LIMIT 1) AS decision"
                   " FROM tokens t WHERE 1 = 1")
            args: list[Any] = []
            if q:
                sql += " AND t.mint = ?"  # exact match only
                args.append(q.strip())
            if scope in ("synthetic", "live"):
                sql += " AND t.is_synthetic = ?"
                args.append(int(scope == "synthetic"))
            sql += " ORDER BY t.is_synthetic, COALESCE(t.launch_time, t.first_seen_at) DESC LIMIT ?"
            args.append(max(1, min(int(limit), 1000)))
            rows = [dict(r) for r in self.conn.execute(sql, args)]
            for r in rows:
                r["is_synthetic"] = bool(r["is_synthetic"])
                r["meta"] = json.loads(r["meta"])
            return {"tokens": rows, "query": q, "exact_match_only": True}

    def token(self, mint: str, as_of: float | None = None) -> dict[str, Any]:
        with self.lock:
            row = self._token(mint)
            obs = db.observations(self.conn, mint, as_of=as_of)
            latest: dict[tuple[str, str, str], dict[str, Any]] = {}
            for o in obs:
                if o["kind"] == "market":
                    latest[(o["provider"], str(o["payload"].get("pool_address")), str(o["payload"].get("venue")))] = o
            launch = next((o for o in reversed(obs) if o["kind"] == "launch"), None)
            holders = next((o for o in reversed(obs) if o["kind"] == "holders"), None)
            series = [{"t": o["observed_at"], "price_sol": o["payload"].get("price_sol"), "provider": o["provider"], "stale": o["stale"]}
                      for o in db.observations(self.conn, mint, "market") if o["payload"].get("price_sol") is not None]
            signals = [dict(r) for r in self.conn.execute("SELECT * FROM signals WHERE mint = ? ORDER BY as_of", (mint,))]
            for s in signals:
                s["reasons"], s["features"] = json.loads(s["reasons"]), json.loads(s["features"])
            positions = [dict(r) for r in self.conn.execute("SELECT * FROM positions WHERE mint = ?", (mint,))]
            for p in positions:
                p["detail"] = json.loads(p["detail"])
                p["fills"] = [dict(f) for f in self.conn.execute("SELECT * FROM fills WHERE position_id = ? ORDER BY filled_at", (p["id"],))]
            token = dict(row)
            token["is_synthetic"] = bool(token["is_synthetic"])
            token["meta"] = json.loads(token["meta"])
            times = [o["observed_at"] for o in db.observations(self.conn, mint)]
            return {
                "token": token, "as_of": as_of, "now": time.time(),
                "market": list(latest.values()), "launch": launch, "holders": holders, "series": series,
                "time_range": {"first": min(times), "last": max(times)} if times else None,
                "risk": risk.risk_report(self.conn, mint, as_of, paper_size_sol=self.settings.paper.size_sol),
                "signals": signals, "positions": positions,
                "conflicts": [dict(r) for r in self.conn.execute("SELECT * FROM conflicts WHERE mint = ? ORDER BY observed_at DESC LIMIT 50", (mint,))],
                "notice": NOT_ADVICE,
            }

    def paper_book(self, book: str) -> dict[str, Any]:
        if book not in BOOKS:
            raise ApiError(404, "unknown book")
        with self.lock:
            rows = [dict(r) for r in self.conn.execute(
                "SELECT s.id AS signal_id, s.mint, s.as_of, s.decision, s.reasons, s.ruleset, s.features_hash, s.recorded_at,"
                " p.status, p.opened_at, p.closed_at, p.cost_sol, p.proceeds_sol, p.gross_pnl_sol, p.fees_sol, p.net_pnl_sol,"
                " p.exit_reason, p.partial, p.failed_attempts, t.symbol, t.is_synthetic"
                " FROM signals s LEFT JOIN positions p ON p.signal_id = s.id JOIN tokens t ON t.mint = s.mint"
                " WHERE s.book = ? ORDER BY s.as_of", (book,))]
            cum = 0.0
            curve = []
            for r in rows:
                r["reasons"] = json.loads(r["reasons"])
                r["is_synthetic"] = bool(r["is_synthetic"])
            for r in sorted((r for r in rows if r["status"] in paper.FINAL_STATUSES), key=lambda r: r["closed_at"] or r["as_of"]):
                cum += r["net_pnl_sol"]
                curve.append({"t": r["closed_at"] or r["as_of"], "cum_net_sol": cum, "mint": r["mint"]})
            return {"book": book, "uses_synthetic_tokens": BOOKS[book], "metrics": paper.book_metrics(self.conn, book, self.settings),
                    "ledger": rows, "equity_curve": curve, "notice": NOT_ADVICE}

    def events(self, limit: int = 100) -> dict[str, Any]:
        with self.lock:
            rows = [dict(r) for r in self.conn.execute("SELECT id, ts, type, payload, hash FROM events ORDER BY id DESC LIMIT ?",
                                                       (max(1, min(int(limit), 500)),))]
            for r in rows:
                r["payload"] = json.loads(r["payload"])
            return {"events": rows, "chain": db.verify_event_chain(self.conn)}

    # ---- POST -------------------------------------------------------------------------------
    def do_ingest(self, body: dict[str, Any]) -> dict[str, Any]:
        mint = str(body.get("mint", "")).strip()
        if not is_valid_mint(mint):
            raise ApiError(400, "enter an exact mint address")
        with self.lock:
            return ingest.ingest_mint(self.conn, self.settings, mint, self.clients)

    def do_discover(self, body: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            return ingest.discover(self.conn, self.settings, self.clients)

    def do_paper_run(self, body: dict[str, Any]) -> dict[str, Any]:
        book = str(body.get("book", "demo"))
        if book not in BOOKS:
            raise ApiError(404, "unknown book")
        with self.lock:
            return paper.run_book(self.conn, self.settings, book, synthetic=BOOKS[book])

    def do_demo_reset(self, body: dict[str, Any]) -> dict[str, Any]:
        seed = int(body.get("seed", 7))
        n = max(10, min(int(body.get("n_tokens", 300)), 1000))
        return self.reset_demo(seed, n)

    def do_audit(self, body: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.live_enabled:
            raise ProviderError("launchlab", "disabled", "live connectors are off (LAUNCHLAB_MODE=demo)")
        mint = str(body.get("mint", "")).strip()
        try:
            alert = audit.parse_utc(str(body.get("alert_time", "")))
        except ValueError as exc:
            raise ApiError(400, "alert_time must be ISO-8601, e.g. 2026-11-20T20:52:00Z") from exc

        def number(key: str) -> float | None:
            raw = body.get(key)
            if raw in (None, ""):
                return None
            try:
                return float(raw)
            except (TypeError, ValueError) as exc:
                raise ApiError(400, f"{key} must be a number") from exc

        try:
            with self.lock:
                return audit.check_claim(self.clients.gecko, mint, alert, claimed_cap_usd=number("claimed_cap_usd"),
                                         claimed_multiple=number("claimed_multiple"),
                                         rpc=self.clients.rpc if body.get("onchain") else None, rpc_url=self.settings.solana_rpc_url)
        except ValueError as exc:
            raise ApiError(400, str(exc)) from exc


def make_handler(app: App) -> type[BaseHTTPRequestHandler]:
    get_routes = {
        "/api/status": lambda q: app.status(),
        "/api/tokens": lambda q: app.tokens(q.get("q", ""), q.get("scope", "all"), int(q.get("limit", "200"))),
        "/api/token": lambda q: app.token(q.get("mint", ""), float(q["as_of"]) if q.get("as_of") else None),
        "/api/paper": lambda q: app.paper_book(q.get("book", "demo")),
        "/api/events": lambda q: app.events(int(q.get("limit", "100"))),
    }
    post_routes = {
        "/api/ingest": app.do_ingest, "/api/discover": app.do_discover, "/api/paper/run": app.do_paper_run,
        "/api/demo/reset": app.do_demo_reset, "/api/audit": app.do_audit,
    }

    class Handler(BaseHTTPRequestHandler):
        server_version = f"LaunchLab/{__version__}"
        protocol_version = "HTTP/1.1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - signature fixed by the base class
            return  # quiet; request paths could contain nothing secret, but there is no need to log them

        def _allowed_hosts(self) -> set[str]:
            port = int(self.server.server_address[1])  # type: ignore[index]  # always an (host, port) tuple for TCP
            return {f"127.0.0.1:{port}", f"localhost:{port}", f"[::1]:{port}"}

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: Any) -> None:
            self._send(status, json.dumps(payload, default=str).encode(), "application/json; charset=utf-8")

        def _guard_host(self) -> bool:
            if self.headers.get("Host", "") not in self._allowed_hosts():  # blocks DNS-rebinding
                self._json(403, {"error": "this server only answers on its loopback address"})
                return False
            return True

        def _run(self, fn: Any) -> None:
            try:
                self._json(200, fn())
            except ApiError as exc:
                self._json(exc.status, {"error": exc.message})
            except ProviderError as exc:
                status = 503 if exc.kind in ("disabled", "rate_limited", "timeout") else 502
                self._json(status, {"error": exc.message, "provider": exc.provider, "kind": exc.kind, "retry_at": exc.retry_at})
            except (KeyError, ValueError) as exc:
                self._json(400, {"error": f"bad request: {exc}"})

        def do_GET(self) -> None:
            if not self._guard_host():
                return
            parts = urlsplit(self.path)
            if parts.path in STATIC_FILES:
                name, ctype = STATIC_FILES[parts.path]
                self._send(200, (STATIC_DIR / name).read_bytes(), ctype)
                return
            route = get_routes.get(parts.path)
            if route is None:
                self._json(404, {"error": "not found"})
                return
            query = {k: v[0] for k, v in parse_qs(parts.query).items()}
            self._run(lambda: route(query))

        def do_POST(self) -> None:
            if not self._guard_host():
                return
            origin = self.headers.get("Origin")
            if origin is not None and urlsplit(origin).netloc not in self._allowed_hosts():
                self._json(403, {"error": "cross-origin requests are refused"})
                return
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                self._json(415, {"error": "send application/json"})
                return
            route = post_routes.get(urlsplit(self.path).path)
            if route is None:
                self._json(404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if not 0 <= length <= MAX_BODY:
                self._json(413, {"error": "request body too large or missing length"})
                return
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                self._json(400, {"error": "body is not valid JSON"})
                return
            if not isinstance(body, dict):
                self._json(400, {"error": "body must be a JSON object"})
                return
            self._run(lambda: route(body))

    return Handler


def make_server(app: App, port: int | None = None) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((app.settings.host, app.settings.port if port is None else port), make_handler(app))
    server.daemon_threads = True
    return server
