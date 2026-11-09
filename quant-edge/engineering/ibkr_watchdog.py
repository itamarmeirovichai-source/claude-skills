#!/usr/bin/env python3
"""
ibkr_watchdog.py - read-only IB Gateway / TWS connection logger (quant-edge Department G, 2026-11-06).

What it does
    Connects to a paper or live IB Gateway on the port you give it, with its OWN client id, in read-only mode.
    Logs every connect / disconnect / reconnect and every message from the `error` callback (1100, 1101, 1102,
    2103-2110, 2157/2158, 326, 10197, ...) to a CSV with UTC, Israel and New York timestamps.
    Every 60 s it records the age of the last 1-minute NQ bar from a keepUpToDate historical subscription,
    the host's wall-clock jumps (sleep / hibernate / clock change), and every 10 min the clock offset against NTP.

What it never does
    It never places, modifies or cancels an order. It connects with readonly=True, never calls any order method,
    and wraps the IB object so that any order method raises. It does not touch the bot, its database or its config.

Install (on Itamar's PC, in the same Python the bot uses, or a fresh venv):
    pip install ib_async          # maintained successor of ib_insync (PyPI 2.1.0, 2025-12-08); ib_insync also works

Run (Gateway already logged in; paper Gateway default port 4002, live Gateway 4001):
    python ibkr_watchdog.py --port 4002
    python ibkr_watchdog.py --port 4001 --client-id 917 --csv ibkr_watchdog_log.csv
Summarize a log (what to send back):
    python ibkr_watchdog.py --summary ibkr_watchdog_log.csv
Self-test (no Gateway, no network, no ib library needed):
    python ibkr_watchdog.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import os
import socket
import struct
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

UTC = timezone.utc
IL = ZoneInfo("Asia/Jerusalem")
ET = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Zurich")

SCAN_INTERVAL_S = 300                 # the bot's scan interval
STALE_BAR_S = 2 * SCAN_INTERVAL_S     # stale-data rule: last bar older than twice the scan interval
MAX_CLOCK_OFFSET_MS = 500.0           # stale-data rule: clock offset limit
BAR_CHECK_S = 60
NTP_CHECK_S = 600
SLEEP_GAP_S = 90                      # a 60 s tick that took longer than this = host slept / froze / clock jumped
PIP_LINE = "pip install ib_async    (or: pip install ib_insync)"

# --- message-code table (IBKR TWS API message codes, https://interactivebrokers.github.io/tws-api/message_codes.html,
#     fetched 2026-11-06). connection_loss is True only for codes that mean the Gateway<->IBKR link is down.
CODES = {
    1100: ("conn_lost", True, "Connectivity between IB and TWS/Gateway lost (internet, nightly reset, or competing session)"),
    1101: ("conn_restored_data_lost", False, "Connectivity restored - data lost: market data must be re-subscribed"),
    1102: ("conn_restored_data_ok", False, "Connectivity restored - data maintained"),
    1300: ("socket_port_reset", True, "TWS socket port reset; reconnect on new port"),
    2103: ("md_farm_down", False, "A market data farm is disconnected (outside reset: usually ISP)"),
    2104: ("md_farm_ok", False, "Market data farm connection is OK (notice, not an error)"),
    2105: ("hist_farm_down", False, "A historical data farm is disconnected"),
    2106: ("hist_farm_ok", False, "A historical data farm is connected (notice)"),
    2107: ("hist_farm_inactive", False, "Historical farm inactive, available on demand (notice)"),
    2108: ("md_farm_inactive", False, "Market data farm inactive, available on demand (notice)"),
    2110: ("tws_server_broken", True, "Connectivity between TWS and server is broken; restored automatically"),
    2157: ("secdef_farm_down", False, "Sec-def data farm disconnected"),
    2158: ("secdef_farm_ok", False, "Sec-def data farm connection is OK (notice)"),
    326: ("client_id_in_use", True, "Client id already in use (two programs with the same clientId)"),
    502: ("cannot_connect", True, "Couldn't connect to TWS/Gateway (not running, wrong port, API disabled)"),
    504: ("not_connected", True, "Not connected"),
    10197: ("competing_session", False, "No market data during competing session (same username logged in elsewhere)"),
    162: ("hist_data_error", False, "Historical market data service error (incl. pacing violation)"),
    354: ("no_md_subscription", False, "Requested market data is not subscribed"),
    10167: ("delayed_md", False, "Displaying delayed market data (no real-time subscription)"),
}
FARM_NOTICES = {2104, 2106, 2107, 2108, 2158}

# IBKR reset windows (brief 00-common/G; IBKR pages listed in the diagnosis document), in their own zone.
# (name, zone, weekday set (Mon=0), start h, start m, end h, end m)
RESET_WINDOWS = [
    ("NA daily reset 00:15-01:45 ET", ET, {0, 1, 2, 3, 4, 5, 6}, 0, 15, 1, 45),
    ("EU daily reset 06:25-07:45 CET", CET, {0, 1, 2, 3, 4, 5, 6}, 6, 25, 7, 45),
    ("Saturday maintenance 00:00-02:00 ET", ET, {5}, 0, 0, 2, 0),
    ("Weekly session expiry after 01:00 ET Sunday (IBC guide)", ET, {6}, 1, 0, 2, 0),
]

FIELDS = ["utc", "israel", "new_york", "event", "code", "category", "connection_loss", "detail",
          "bar_ts_utc", "bar_age_s", "stale", "clock_offset_ms", "reset_window"]


def stamps(t: datetime) -> tuple[str, str, str]:
    t = t.astimezone(UTC)
    return (t.isoformat(timespec="milliseconds"),
            t.astimezone(IL).isoformat(timespec="milliseconds"),
            t.astimezone(ET).isoformat(timespec="milliseconds"))


def in_reset_window(t: datetime) -> str:
    """Names of the IBKR reset windows containing instant t (+-10 min tolerance), joined by '; ', or ''."""
    found = []
    for name, tz, days, sh, sm, eh, em in RESET_WINDOWS:
        local = t.astimezone(tz)
        for d in (local.date(), local.date() - timedelta(days=1)):
            if d.weekday() not in days:
                continue
            start = datetime(d.year, d.month, d.day, sh, sm, tzinfo=tz) - timedelta(minutes=10)
            end = datetime(d.year, d.month, d.day, eh, em, tzinfo=tz) + timedelta(minutes=10)
            if start <= t <= end and name not in found:
                found.append(name)
    return "; ".join(found)


def classify(code: int) -> tuple[str, bool, str]:
    return CODES.get(int(code), ("other", False, "see IBKR message codes"))


def stale_verdict(bar_age_s: float | None, clock_offset_ms: float | None) -> bool:
    """The bot's stale-data rule: no new order if bar too old or clock off by > 500 ms. Unknown = stale."""
    if bar_age_s is None or bar_age_s > STALE_BAR_S:
        return True
    if clock_offset_ms is not None and abs(clock_offset_ms) > MAX_CLOCK_OFFSET_MS:
        return True
    return False


class CsvLog:
    def __init__(self, path: Path, echo: bool = True):
        self.path = Path(path)
        self.echo = echo
        new = not self.path.exists() or self.path.stat().st_size == 0
        self.fh = open(self.path, "a", newline="", encoding="utf-8")
        self.w = csv.DictWriter(self.fh, fieldnames=FIELDS)
        if new:
            self.w.writeheader()
            self.fh.flush()

    def write(self, event: str, t: datetime | None = None, **kw) -> dict:
        t = t or datetime.now(UTC)
        u, i, n = stamps(t)
        row = {k: "" for k in FIELDS}
        row.update(utc=u, israel=i, new_york=n, event=event, reset_window=in_reset_window(t))
        row.update({k: ("" if v is None else v) for k, v in kw.items() if k in FIELDS})
        self.w.writerow(row)
        self.fh.flush()
        try:
            os.fsync(self.fh.fileno())
        except OSError:
            pass
        if self.echo:
            print(f"{i[:19]} IL | {event} {row['code']} {row['category']} {row['detail']}"[:160], flush=True)
        return row

    def close(self):
        self.fh.close()


# --- SNTP (RFC 4330) clock offset, no dependency ---
NTP_DELTA = 2208988800


def _ntp_ts(sec: int, frac: int) -> float:
    return sec - NTP_DELTA + frac / 2**32


def parse_ntp(packet: bytes, t1: float, t4: float) -> float:
    """Clock offset in ms = ((t2 - t1) + (t3 - t4)) / 2, from a 48-byte NTP reply."""
    if len(packet) < 48:
        raise ValueError("short NTP packet")
    f = struct.unpack("!12I", packet[:48])
    t2 = _ntp_ts(f[8], f[9])
    t3 = _ntp_ts(f[10], f[11])
    return ((t2 - t1) + (t3 - t4)) / 2 * 1000.0


def ntp_offset_ms(server: str = "pool.ntp.org", timeout: float = 3.0) -> float | None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        t1 = time.time()
        s.sendto(b"\x1b" + 47 * b"\0", (server, 123))
        data, _ = s.recvfrom(512)
        t4 = time.time()
        s.close()
        return parse_ntp(data, t1, t4)
    except OSError:
        return None


class ReadOnlyIB:
    """Wraps an IB object; every order method raises. The watchdog only ever holds this wrapper."""
    BLOCKED = {"placeOrder", "cancelOrder", "reqGlobalCancel", "bracketOrder", "oneCancelsAll",
               "whatIfOrder", "exerciseOptions", "reqAutoOpenOrders"}

    def __init__(self, ib):
        object.__setattr__(self, "_ib", ib)

    def __getattr__(self, name):
        if name in ReadOnlyIB.BLOCKED:
            raise PermissionError(f"ibkr_watchdog is read-only: {name} is blocked")
        return getattr(object.__getattribute__(self, "_ib"), name)


def import_ib():
    """Return (IB, ContFuture, Future, library name) or None if neither library is installed."""
    for mod in ("ib_async", "ib_insync"):
        try:
            m = __import__(mod)
            return m.IB, m.ContFuture, m.Future, mod
        except ImportError:
            continue
    return None


class Watchdog:
    def __init__(self, ib, log: CsvLog, args, ContFuture=None, Future=None):
        self.ib = ReadOnlyIB(ib)
        self.log = log
        self.args = args
        self.ContFuture, self.Future = ContFuture, Future
        self.bars = None
        self.contract = None
        self.offset_ms = None
        self.connected = False

    # event handlers (signatures match ib_async / ib_insync)
    def on_connected(self):
        self.connected = True
        self.log.write("api_connected", detail=f"{self.args.host}:{self.args.port} clientId={self.args.client_id}")

    def on_disconnected(self):
        self.connected = False
        self.bars = None
        self.log.write("api_disconnected", connection_loss=True,
                       detail="socket to Gateway closed (Gateway restart/exit, PC sleep, or Gateway logged out)")

    def on_error(self, reqId, errorCode, errorString, *rest):
        cat, loss, meaning = classify(errorCode)
        ev = "farm_notice" if errorCode in FARM_NOTICES else "ib_message"
        self.log.write(ev, code=errorCode, category=cat, connection_loss=loss,
                       detail=f"reqId={reqId} {str(errorString)[:200]} | {meaning}")
        if errorCode == 1101:
            self.bars = None  # data lost: re-subscribe on the next tick

    def subscribe(self):
        if self.contract is None:
            cf = self.ContFuture(self.args.symbol, self.args.exchange)
            q = self.ib.qualifyContracts(cf)
            if not q:
                self.log.write("contract_error", detail=f"could not qualify {self.args.symbol} {self.args.exchange}")
                return
            self.contract = self.Future(conId=q[0].conId, exchange=self.args.exchange)
            self.ib.qualifyContracts(self.contract)
            self.log.write("contract", detail=f"{q[0].localSymbol} conId={q[0].conId}")
        self.bars = self.ib.reqHistoricalData(self.contract, endDateTime="", durationStr="3600 S",
                                              barSizeSetting="1 min", whatToShow="TRADES", useRTH=False,
                                              formatDate=2, keepUpToDate=True)
        self.log.write("bars_subscribed", detail=f"{len(self.bars or [])} bars")

    def bar_age(self, now: datetime):
        if not self.bars:
            return None, None
        ts = self.bars[-1].date
        if not isinstance(ts, datetime):
            return None, None
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        return ts, (now - ts).total_seconds()

    def tick(self, now: datetime):
        if self.connected and self.bars is None:
            try:
                self.subscribe()
            except Exception as e:  # pragma: no cover - needs a Gateway
                self.log.write("subscribe_error", detail=str(e)[:200])
        ts, age = self.bar_age(now)
        self.log.write("bar_age", bar_ts_utc=ts.isoformat() if ts else "", bar_age_s=None if age is None else round(age, 1),
                       stale=stale_verdict(age, self.offset_ms),
                       clock_offset_ms=None if self.offset_ms is None else round(self.offset_ms, 1),
                       detail="" if self.connected else "not connected")

    def try_connect(self):
        try:
            self.ib.connect(self.args.host, self.args.port, clientId=self.args.client_id, timeout=20, readonly=True)
        except Exception as e:
            self.log.write("connect_failed", connection_loss=True, detail=str(e)[:200])

    def run(self):  # pragma: no cover - needs a Gateway
        ib = self.ib
        ib.connectedEvent += self.on_connected
        ib.disconnectedEvent += self.on_disconnected
        ib.errorEvent += self.on_error
        self.log.write("watchdog_start", detail=f"lib={self.args.lib} py={sys.version.split()[0]} "
                       f"host_tz={time.strftime('%Z')} stale>{STALE_BAR_S}s offset>{MAX_CLOCK_OFFSET_MS}ms")
        self.try_connect()
        last_wall, last_mono = time.time(), time.monotonic()
        next_ntp = 0.0
        end = time.monotonic() + self.args.duration_h * 3600 if self.args.duration_h else None
        try:
            while end is None or time.monotonic() < end:
                ib.sleep(BAR_CHECK_S) if self.connected else time.sleep(BAR_CHECK_S)
                wall, mono = time.time(), time.monotonic()
                gap = wall - last_wall
                if gap > SLEEP_GAP_S or abs((wall - last_wall) - (mono - last_mono)) > 5:
                    self.log.write("host_gap", connection_loss=False,
                                   detail=f"tick took {gap:.0f}s wall / {mono - last_mono:.0f}s monotonic: "
                                          "PC sleep, freeze, or clock change")
                last_wall, last_mono = wall, mono
                if mono >= next_ntp:
                    self.offset_ms = ntp_offset_ms(self.args.ntp_server)
                    self.log.write("clock_check", clock_offset_ms=None if self.offset_ms is None else round(self.offset_ms, 1),
                                   detail="NTP unreachable" if self.offset_ms is None else self.args.ntp_server)
                    next_ntp = mono + NTP_CHECK_S
                if not ib.isConnected():
                    self.connected = False
                    self.try_connect()
                self.tick(datetime.now(UTC))
        except KeyboardInterrupt:
            pass
        finally:
            self.log.write("watchdog_stop")
            try:
                ib.disconnect()
            except Exception:
                pass


def summarize(path: Path) -> str:
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    out = [f"rows: {len(rows)}  file: {path}"]
    loss = [r for r in rows if r["connection_loss"] == "True"]
    out.append(f"connection-loss events: {len(loss)}")
    for r in loss:
        out.append(f"  {r['israel'][:19]} IL | {r['new_york'][11:19]} NY | {r['event']} {r['code']} {r['category']}"
                   f" | window={r['reset_window'] or 'NONE'}")
    by_hour: dict[int, int] = {}
    for r in loss:
        h = int(r["israel"][11:13])
        by_hour[h] = by_hour.get(h, 0) + 1
    out.append("losses by Israel hour: " + ", ".join(f"{h:02d}h={n}" for h, n in sorted(by_hour.items())))
    out.append(f"outside any IBKR reset window: {sum(1 for r in loss if not r['reset_window'])}")
    ages = [float(r["bar_age_s"]) for r in rows if r["event"] == "bar_age" and r["bar_age_s"]]
    if ages:
        ages.sort()
        out.append(f"bar age s: median {ages[len(ages)//2]:.0f}, max {ages[-1]:.0f}, "
                   f"stale ticks {sum(1 for r in rows if r['event']=='bar_age' and r['stale']=='True')}")
    offs = [abs(float(r["clock_offset_ms"])) for r in rows if r["event"] == "clock_check" and r["clock_offset_ms"]]
    if offs:
        out.append(f"clock |offset| ms: max {max(offs):.0f}")
    for ev in ("host_gap", "farm_notice", "competing_session", "client_id_in_use"):
        n = sum(1 for r in rows if r["event"] == ev or r["category"] == ev)
        out.append(f"{ev}: {n}")
    return "\n".join(out)


# ------------------------------------------------------------------ self-test (no Gateway, no network)
class _Evt:
    def __init__(self):
        self.h = []

    def __iadd__(self, f):
        self.h.append(f)
        return self

    def emit(self, *a):
        for f in self.h:
            f(*a)


class _Bar:
    def __init__(self, date):
        self.date = date


class _FakeIB:
    def __init__(self):
        self.connectedEvent, self.disconnectedEvent, self.errorEvent = _Evt(), _Evt(), _Evt()
        self.calls = []

    def placeOrder(self, *a):  # must never be reachable through ReadOnlyIB
        self.calls.append("placeOrder")

    def isConnected(self):
        return True


def selftest() -> int:
    ok = fail = 0

    def check(name, cond):
        nonlocal ok, fail
        ok, fail = (ok + 1, fail) if cond else (ok, fail + 1)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    print("ibkr_watchdog selftest (no Gateway, no network)")
    lib = import_ib()
    print(f"  ib library: {lib[3] if lib else 'none installed -> live mode needs: ' + PIP_LINE}")
    # 1 reset windows converted to Israel time (zoneinfo)
    t = datetime(2026, 11, 9, 0, 15, tzinfo=ET)
    check("NA reset 00:15 ET Mon 2026-11-09 = 07:15 Israel", t.astimezone(IL).strftime("%H:%M") == "07:15")
    t = datetime(2027, 3, 17, 0, 15, tzinfo=ET)
    check("US-DST/Israel-winter gap week: 00:15 ET = 06:15 Israel (2027-03-17)", t.astimezone(IL).strftime("%H:%M") == "06:15")
    check("EU reset 06:25 CET = 07:25 Israel", datetime(2026, 11, 9, 6, 25, tzinfo=CET).astimezone(IL).strftime("%H:%M") == "07:25")
    check("07:30 Israel Monday is inside a reset window", in_reset_window(datetime(2026, 11, 9, 7, 30, tzinfo=IL)) != "")
    hits = [in_reset_window(datetime(2026, 11, 9, h, m, tzinfo=IL)) for h in range(12, 20) for m in (0, 30)]
    check("no IBKR reset window between 12:00 and 20:00 Israel", not any(hits))
    check("Saturday 01:50 ET (08:50 IL) is in the Saturday window",
          "Saturday" in in_reset_window(datetime(2026, 11, 7, 1, 50, tzinfo=ET)))
    check("Monday 16:20 Israel (bot start 09:20 ET) is in no reset window",
          in_reset_window(datetime(2026, 11, 9, 9, 20, tzinfo=ET)) == "")
    # 2 code classification
    check("1100 is a connection loss", classify(1100)[1] is True)
    check("2104/2106/2158 are notices, not losses", all(not classify(c)[1] for c in (2104, 2106, 2158)))
    check("2103/2105/2108 are not connection losses", all(not classify(c)[1] for c in (2103, 2105, 2108)))
    check("1101 = data lost, 1102 = data kept", classify(1101)[0].endswith("data_lost") and classify(1102)[0].endswith("data_ok"))
    check("unknown code -> 'other'", classify(99999)[0] == "other")
    # 3 stale rule
    check("bar age 599 s, offset 10 ms -> fresh", stale_verdict(599, 10) is False)
    check("bar age 601 s -> stale", stale_verdict(601, 10) is True)
    check("offset 501 ms -> stale", stale_verdict(30, 501) is True)
    check("unknown bar age -> stale", stale_verdict(None, 0) is True)
    # 4 SNTP parse on a synthetic reply: server 0.25 s ahead
    t1 = 1_700_000_000.0
    t4 = t1 + 0.020

    def enc(x):
        s = int(x) + NTP_DELTA
        return s, int((x - int(x)) * 2**32)
    pkt = struct.pack("!12I", *([0] * 8), *enc(t1 + 0.010 + 0.25), *enc(t1 + 0.010 + 0.25))
    check("SNTP offset parsed = +250 ms", abs(parse_ntp(pkt, t1, t4) - 250.0) < 1.0)
    # 5 read-only guard
    fake = _FakeIB()
    ro = ReadOnlyIB(fake)
    try:
        ro.placeOrder("x", "y")
        blocked = False
    except PermissionError:
        blocked = True
    check("placeOrder through the wrapper raises and never reaches IB", blocked and fake.calls == [])
    src = Path(__file__).read_text(encoding="utf-8")
    calls = [ln for ln in src.splitlines() if ".placeOrder(" in ln and "ro.placeOrder" not in ln]
    check("source holds no order-placing call", calls == [])
    # 6 handlers + CSV round trip + summary, with simulated events
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "log.csv"
        log = CsvLog(p, echo=False)

        class A:
            host, port, client_id, symbol, exchange = "127.0.0.1", 4002, 917, "NQ", "CME"
        wd = Watchdog(fake, log, A)
        fake.connectedEvent += wd.on_connected
        fake.disconnectedEvent += wd.on_disconnected
        fake.errorEvent += wd.on_error
        fake.connectedEvent.emit()
        fake.errorEvent.emit(-1, 2104, "Market data farm connection is OK:usfarm", None)
        fake.errorEvent.emit(-1, 1100, "Connectivity between IB and Trader Workstation has been lost.", None)
        fake.errorEvent.emit(-1, 1101, "Connectivity ... restored - data lost.", None)
        fake.disconnectedEvent.emit()
        now = datetime(2026, 11, 9, 14, 40, tzinfo=UTC)  # 16:40 Israel
        wd.connected, wd.bars = True, [_Bar(now - timedelta(seconds=1920))]  # a 32-minute-old bar
        wd.tick(now)
        log.close()
        rows = list(csv.DictReader(open(p, encoding="utf-8")))
        check("CSV has header + 6 rows", len(rows) == 6)
        check("both clocks written (UTC and Israel)", rows[0]["utc"].endswith("+00:00") and "+02:00" in rows[0]["israel"])
        check("2104 logged as farm_notice, not loss", rows[1]["event"] == "farm_notice" and rows[1]["connection_loss"] == "False")
        check("1100 logged as connection loss", rows[2]["code"] == "1100" and rows[2]["connection_loss"] == "True")
        check("1101 clears the bar subscription (re-subscribe)", rows[3]["category"] == "conn_restored_data_lost")
        check("32-minute-old bar flagged stale", rows[5]["stale"] == "True" and float(rows[5]["bar_age_s"]) == 1920.0)
        s = summarize(p)
        check("summary counts 2 connection losses, both outside reset windows",
              "connection-loss events: 2" in s and "outside any IBKR reset window: 2" in s)
    print(f"selftest: {ok} passed, {fail} failed")
    return 0 if fail == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Read-only IB Gateway connection watchdog (never places orders).")
    ap.add_argument("--selftest", action="store_true", help="run built-in tests; needs no Gateway")
    ap.add_argument("--summary", metavar="CSV", help="summarize an existing log and exit")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4002, help="paper Gateway 4002, live Gateway 4001 (TWS 7497/7496)")
    ap.add_argument("--client-id", type=int, default=917, help="must differ from the bot's clientId")
    ap.add_argument("--csv", default="ibkr_watchdog_log.csv")
    ap.add_argument("--symbol", default="NQ")
    ap.add_argument("--exchange", default="CME")
    ap.add_argument("--ntp-server", default="pool.ntp.org")
    ap.add_argument("--duration-h", type=float, default=0, help="stop after N hours (0 = until Ctrl+C)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.summary:
        print(summarize(Path(a.summary)))
        return 0
    lib = import_ib()
    if lib is None:
        print("No IB library found. Install one first:\n    " + PIP_LINE)
        return 2
    IB, ContFuture, Future, a.lib = lib
    log = CsvLog(Path(a.csv))
    Watchdog(IB(), log, a, ContFuture, Future).run()
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
