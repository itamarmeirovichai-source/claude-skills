"""Paper-trading simulator, ledger and metrics. No real order is ever created.

Order of operations per token (strictly time-ordered, see PROJECT_SPEC.md section 9):
  1. build features from observations with observed_at <= as_of  (look-ahead guard)
  2. record the signal — candidate or rejected — BEFORE any outcome is computed
  3. simulate entry after latency, with failures, partial fills, fees and slippage
  4. exit only by the fixed rule; execution happens one latency after the trigger
"""

from __future__ import annotations

import hashlib
import json
import random
import sqlite3
import time
from typing import Any

from . import amm, db, policy, risk
from .config import PaperConfig, Settings
from .costs import FEE_SCHEDULE_VERSION, NetworkCosts, venue_fee_rate

FINAL_STATUSES = ("closed", "unsellable", "not_filled")
DEFAULT_PLAN: dict[str, Any] = {
    "min_resolved_candidates": 200,
    "min_span_days": 14,
    "development_share": 0.70,
    "rulesets_tried": 1,
    "primary_metric": "mean net return per candidate (not-filled, failed and unsellable included)",
    "confidence": 0.95,
}


def det_uniform(seed: int, *parts: Any) -> float:
    """Deterministic pseudo-random number in [0, 1) so a run can be reproduced exactly."""
    digest = hashlib.sha256(("|".join([str(seed), *map(str, parts)])).encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


# --------------------------------------------------------------------------------------------
# features and signals
# --------------------------------------------------------------------------------------------

def build_features(conn: sqlite3.Connection, mint: str, as_of: float) -> dict[str, Any]:
    """Everything the decision rule may see. Reads only observations with observed_at <= as_of."""
    launches = db.observations(conn, mint, "launch", as_of=as_of)
    lp = launches[-1]["payload"] if launches else {}
    market = risk.latest_market(conn, mint, as_of)
    mp = market["payload"] if market else {}
    by_wallet = {b["wallet"]: b["share"] for b in lp.get("slot0_buyers") or []}
    cosigned = sum(by_wallet.get(w, 0.0) for g in lp.get("cosigner_groups") or [] for w in g)
    liquidity = mp.get("liquidity_sol")
    if liquidity is None and mp.get("liquidity_usd") and mp.get("sol_usd"):
        liquidity = mp["liquidity_usd"] / mp["sol_usd"] / 2
    return {
        "as_of": as_of,
        "launch_status": lp.get("status") if launches else None,
        "slot0_share": lp.get("slot0_share"),
        "creator_share": lp.get("creator_share_at_launch"),
        "cosigned_share": cosigned if launches else None,
        "creator_prior_launches": lp.get("creator_prior_launches"),
        "creator_prior_completed": lp.get("creator_prior_completed"),
        "price_sol": mp.get("price_sol"),
        "venue": mp.get("venue"),
        "liquidity_sol": liquidity,
        "market_age_s": (as_of - market["observed_at"]) if market else None,
        "market_provider": market["provider"] if market else None,
        "n_market_obs": len(db.observations(conn, mint, "market", as_of=as_of)),
    }


def register_study(conn: sqlite3.Connection, book: str, plan: dict[str, Any] | None = None) -> dict[str, Any]:
    """Store the evaluation plan once per book. Later calls return the stored plan unchanged."""
    row = conn.execute("SELECT plan FROM study WHERE book = ?", (book,)).fetchone()
    if row:
        return json.loads(row["plan"])
    plan = {**DEFAULT_PLAN, **(plan or {}), "ruleset": policy.RULESET}
    conn.execute("INSERT INTO study (book, plan, registered_at) VALUES (?, ?, ?)", (book, db.canonical(plan), time.time()))
    db.log_event(conn, "study_registered", {"book": book, "plan": plan})
    return plan


def record_signal(conn: sqlite3.Connection, book: str, mint: str, as_of: float, features: dict[str, Any],
                  decision: str, reasons: list[str], settings: Settings, recorded_at: float | None = None) -> int:
    features_hash = hashlib.sha256(db.canonical(features).encode()).hexdigest()
    cur = conn.execute(
        "INSERT INTO signals (book, mint, as_of, ruleset, config_hash, decision, reasons, features, features_hash, recorded_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (book, mint, as_of, policy.RULESET, settings.config_hash(), decision, db.canonical(reasons), db.canonical(features),
         features_hash, time.time() if recorded_at is None else recorded_at),
    )
    signal_id = int(cur.lastrowid or 0)
    db.log_event(conn, "signal_recorded", {"signal_id": signal_id, "book": book, "mint": mint, "as_of": as_of, "decision": decision,
                                           "reasons": reasons, "features_hash": features_hash, "ruleset": policy.RULESET})
    return signal_id


# --------------------------------------------------------------------------------------------
# fills
# --------------------------------------------------------------------------------------------

def _usable(obs: dict[str, Any]) -> bool:
    return risk.usable_price(obs) and not obs["stale"]


def _first_usable(market: list[dict[str, Any]], start: float, end: float) -> dict[str, Any] | None:
    for obs in market:
        if obs["observed_at"] > end:
            return None
        if obs["observed_at"] >= start and _usable(obs):
            return obs
    return None


def _fee_rate(payload: dict[str, Any], cfg: PaperConfig) -> float:
    if cfg.venue_fee_override is not None:
        return cfg.venue_fee_override
    venue = payload.get("venue") or "pool"
    price = payload.get("price_sol")
    return venue_fee_rate(venue, price * amm.TOTAL_SUPPLY if price else None)


def _uncertainty(payload: dict[str, Any]) -> dict[str, Any]:
    candle = payload.get("candle")
    if isinstance(candle, dict) and candle.get("l") and candle.get("h"):
        return {"source": "one candle; intra-candle order unknown", "price_low_sol": candle["l"], "price_high_sol": candle["h"]}
    return {}


def buy_fill(obs: dict[str, Any], size_sol: float, cfg: PaperConfig) -> dict[str, Any]:
    """Simulate spending up to `size_sol` on the state described by one observation."""
    p = obs["payload"]
    fee_rate = _fee_rate(p, cfg)
    slip = cfg.extra_slippage_bps / 10_000
    quote, base = p.get("quote_reserve_sol"), p.get("base_reserve")
    partial = False
    if quote and base:
        cap = cfg.max_pool_share * float(quote)
        spend = min(size_sol, cap)
        partial = spend < size_sol
        tokens, fee, _ = amm.buy(amm.Reserves(float(quote), float(base)), spend, fee_rate)
        tokens *= 1 - slip
        model = "constant-product on observed reserves"
    else:
        spend = size_sol
        liquidity = p.get("liquidity_sol")
        if liquidity is None and p.get("liquidity_usd") and p.get("sol_usd"):
            liquidity = p["liquidity_usd"] / p["sol_usd"] / 2
        impact = spend / liquidity if liquidity else 0.0
        fee = spend * fee_rate
        tokens = (spend - fee) / (p["price_sol"] * (1 + impact)) * (1 - slip)
        model = "observed price + impact from reported liquidity" if liquidity else "observed price + fixed slippage (depth unknown)"
    return {"tokens": tokens, "spent_sol": spend, "venue_fee_sol": fee, "price_sol": spend / tokens if tokens else 0.0,
            "quoted_price_sol": p["price_sol"], "fee_rate": fee_rate, "partial": partial, "model": model, "uncertainty": _uncertainty(p)}


def sell_fill(obs: dict[str, Any], tokens: float, cfg: PaperConfig) -> dict[str, Any]:
    """Simulate selling `tokens`. `sellable` is False when exit depth is below the configured minimum."""
    p = obs["payload"]
    fee_rate = _fee_rate(p, cfg)
    slip = cfg.extra_slippage_bps / 10_000
    quote, base = p.get("quote_reserve_sol"), p.get("base_reserve")
    liquidity = p.get("liquidity_sol")
    if liquidity is None and p.get("liquidity_usd") and p.get("sol_usd"):
        liquidity = p["liquidity_usd"] / p["sol_usd"] / 2
    if liquidity is not None and liquidity < cfg.min_exit_liquidity_sol:
        return {"sellable": False, "reason": f"exit depth {liquidity:.3f} SOL below minimum {cfg.min_exit_liquidity_sol:g} SOL"}
    if quote and base:
        out, fee, _ = amm.sell(amm.Reserves(float(quote), float(base)), tokens, fee_rate)
        if liquidity is not None:
            out = min(out, max(liquidity - fee, 0.0))  # cannot take out more real SOL than the venue holds
        model = "constant-product on observed reserves"
    else:
        gross = tokens * p["price_sol"]
        impact = min(gross / liquidity, 0.95) if liquidity else 0.0
        gross *= 1 - impact
        fee = gross * fee_rate
        out = gross - fee
        model = "observed price + impact from reported liquidity" if liquidity else "observed price + fixed slippage (depth unknown)"
    out *= 1 - slip
    return {"sellable": True, "out_sol": out, "venue_fee_sol": fee, "price_sol": out / tokens if tokens else 0.0,
            "quoted_price_sol": p["price_sol"], "fee_rate": fee_rate, "model": model, "uncertainty": _uncertainty(p)}


# --------------------------------------------------------------------------------------------
# one position
# --------------------------------------------------------------------------------------------

def simulate_position(conn: sqlite3.Connection, signal: sqlite3.Row | dict[str, Any], market: list[dict[str, Any]],
                      settings: Settings, exit_rule: policy.ExitRule, *, final: bool) -> str:
    """Simulate entry and exit for one candidate signal and store the result. Returns the status, or
    'pending' when live data needed to decide has not arrived yet (nothing is stored in that case)."""
    cfg = settings.paper
    net = NetworkCosts(cfg.base_fee_sol, cfg.priority_fee_sol, cfg.tip_sol)
    mint, signal_id, book = signal["mint"], signal["id"], signal["book"]
    last_time = market[-1]["observed_at"] if market else None
    detail: dict[str, Any] = {"fee_schedule": FEE_SCHEDULE_VERSION, "exit_rule": exit_rule.__dict__, "config_hash": settings.config_hash()}

    def store(status: str, **cols: Any) -> str:
        conn.execute("DELETE FROM fills WHERE position_id IN (SELECT id FROM positions WHERE signal_id = ?)", (signal_id,))
        conn.execute("DELETE FROM positions WHERE signal_id = ?", (signal_id,))
        fills = cols.pop("fills", [])
        cols.setdefault("detail", detail)
        cols["detail"] = db.canonical(cols["detail"])
        names = ["signal_id", "book", "mint", "status", *cols]
        cur = conn.execute(f"INSERT INTO positions ({', '.join(names)}) VALUES ({', '.join('?' * len(names))})",
                           (signal_id, book, mint, status, *cols.values()))
        for f in fills:
            conn.execute("INSERT INTO fills (position_id, side, filled_at, price_sol, tokens, quote_sol, venue_fee_sol, network_fee_sol,"
                         " model, uncertainty, observation_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (cur.lastrowid, f["side"], f["filled_at"], f["price_sol"], f["tokens"], f["quote_sol"], f["venue_fee_sol"],
                          f["network_fee_sol"], f["model"], db.canonical(f["uncertainty"]), f["observation_id"]))
        db.log_event(conn, "position_" + status, {"signal_id": signal_id, "mint": mint, "book": book,
                                                  "net_pnl_sol": cols.get("net_pnl_sol", 0.0), "exit_reason": cols.get("exit_reason")})
        return status

    def attempt(side: str, start: float) -> tuple[dict[str, Any] | None, int, float, str]:
        """Try to land a transaction. Returns (observation or None, failed attempts, network SOL spent, why)."""
        failed, spent = 0, 0.0
        for k in range(cfg.max_attempts):
            t_k = start + k * cfg.retry_delay_s
            spent += net.per_attempt
            if det_uniform(cfg.seed, mint, side, k) < cfg.fail_prob:
                failed += 1
                continue
            obs = _first_usable(market, t_k, t_k + cfg.max_wait_s)
            if obs is None:
                return None, failed, spent, "no usable market data within the wait window"
            return obs, failed, spent, ""
        return None, failed, spent, "every attempt failed"

    # ---- entry ------------------------------------------------------------------------------
    entry_start = signal["as_of"] + cfg.latency_s
    entry_obs, failed_buy, entry_network, why = attempt("buy", entry_start)
    if entry_obs is None:
        window_end = entry_start + cfg.max_attempts * cfg.retry_delay_s + cfg.max_wait_s
        if not final and why.startswith("no usable") and (last_time is None or last_time < window_end):
            return "pending"
        return store("not_filled", cost_sol=entry_network, fees_sol=entry_network, net_pnl_sol=-entry_network,
                     gross_pnl_sol=0.0, failed_attempts=failed_buy, exit_reason=why)
    bought = buy_fill(entry_obs, cfg.size_sol, cfg)
    tokens, entry_time = bought["tokens"], entry_obs["observed_at"]
    cost = bought["spent_sol"] + entry_network + cfg.token_account_rent_sol
    buy_row = {"side": "buy", "filled_at": entry_time, "price_sol": bought["price_sol"], "tokens": tokens, "quote_sol": bought["spent_sol"],
               "venue_fee_sol": bought["venue_fee_sol"], "network_fee_sol": entry_network, "model": bought["model"],
               "uncertainty": bought["uncertainty"], "observation_id": entry_obs["id"]}
    detail.update(entry_quoted_price_sol=bought["quoted_price_sol"], entry_delay_s=entry_time - signal["as_of"])
    base_cols = {"opened_at": entry_time, "tokens": tokens, "cost_sol": cost, "partial": int(bought["partial"]), "failed_attempts": failed_buy}

    def finish(status: str, reason: str, *, out_sol: float = 0.0, sell_fee: float = 0.0, exit_network: float = 0.0,
               closed_at: float | None = None, sell_row: dict[str, Any] | None = None, failed_sell: int = 0, mark: float | None = None) -> str:
        proceeds = out_sol - exit_network
        fees = bought["venue_fee_sol"] + sell_fee + entry_network + exit_network + cfg.token_account_rent_sol
        net_pnl = proceeds - cost
        cols = {**base_cols, "closed_at": closed_at, "proceeds_sol": proceeds, "fees_sol": fees, "net_pnl_sol": net_pnl,
                "gross_pnl_sol": net_pnl + fees, "exit_reason": reason, "mark_price_sol": mark,
                "failed_attempts": failed_buy + failed_sell, "fills": [buy_row, *([sell_row] if sell_row else [])]}
        return store(status, **cols)

    # ---- exit -------------------------------------------------------------------------------
    for obs in market:
        if obs["observed_at"] <= entry_time or obs["stale"]:
            continue
        reason = policy.exit_trigger(bought["price_sol"], entry_time, obs["observed_at"], obs["payload"].get("price_sol"), exit_rule)
        if reason is None:
            continue
        exit_obs, failed_sell, exit_network, why = attempt("sell", obs["observed_at"] + cfg.latency_s)
        if exit_obs is None:
            if not final and why.startswith("no usable"):
                break  # live data may still arrive
            return finish("unsellable", f"{reason}: {why}", exit_network=exit_network, closed_at=obs["observed_at"], failed_sell=failed_sell)
        sold = sell_fill(exit_obs, tokens, cfg)
        if not sold["sellable"]:
            return finish("unsellable", f"{reason}: {sold['reason']}", exit_network=exit_network, closed_at=exit_obs["observed_at"], failed_sell=failed_sell)
        detail.update(exit_trigger_at=obs["observed_at"], exit_delay_s=exit_obs["observed_at"] - obs["observed_at"],
                      trigger_price_sol=obs["payload"].get("price_sol"))
        sell_row = {"side": "sell", "filled_at": exit_obs["observed_at"], "price_sol": sold["price_sol"], "tokens": tokens,
                    "quote_sol": sold["out_sol"], "venue_fee_sol": sold["venue_fee_sol"], "network_fee_sol": exit_network,
                    "model": sold["model"], "uncertainty": sold["uncertainty"], "observation_id": exit_obs["id"]}
        return finish("closed", reason, out_sol=sold["out_sol"], sell_fee=sold["venue_fee_sol"], exit_network=exit_network,
                      closed_at=exit_obs["observed_at"], sell_row=sell_row, failed_sell=failed_sell)
    last_price = next((o["payload"]["price_sol"] for o in reversed(market) if o["payload"].get("price_sol") is not None), None)
    if final:
        return finish("unsellable", "market data ended while holding; no exit could be simulated", closed_at=last_time, mark=last_price)
    return finish("open", "awaiting exit trigger", mark=last_price)


# --------------------------------------------------------------------------------------------
# a whole book
# --------------------------------------------------------------------------------------------

def run_book(conn: sqlite3.Connection, settings: Settings, book: str, *, synthetic: bool,
             decision_rule: policy.DecisionRule | None = None, exit_rule: policy.ExitRule | None = None,
             now: float | None = None) -> dict[str, Any]:
    """Record signals for tokens that have none yet, then (re)simulate positions that are not final."""
    decision_rule = decision_rule or policy.DecisionRule()
    exit_rule = exit_rule or policy.ExitRule()
    now = time.time() if now is None else now
    cfg = settings.paper
    register_study(conn, book)
    new_signals = 0
    tokens = conn.execute("SELECT mint, launch_time FROM tokens WHERE is_synthetic = ? AND launch_time IS NOT NULL ORDER BY launch_time",
                          (int(synthetic),)).fetchall()
    conn.execute("BEGIN")
    try:
        for tok in tokens:
            as_of = tok["launch_time"] + cfg.decision_delay_s
            if not synthetic and now < as_of:
                continue  # too early to decide; never decide with a clock that is ahead of the data
            if conn.execute("SELECT 1 FROM signals WHERE book = ? AND mint = ?", (book, tok["mint"])).fetchone():
                continue
            features = build_features(conn, tok["mint"], as_of)
            decision, reasons = policy.decide(features, decision_rule)
            record_signal(conn, book, tok["mint"], as_of, features, decision, reasons, settings,
                          recorded_at=as_of if synthetic else now)
            new_signals += 1
        simulated: dict[str, int] = {}
        pending = conn.execute(
            "SELECT s.* FROM signals s LEFT JOIN positions p ON p.signal_id = s.id"
            " WHERE s.book = ? AND s.decision = 'candidate' AND (p.id IS NULL OR p.status = 'open') ORDER BY s.as_of", (book,)).fetchall()
        for sig in pending:
            market = db.observations(conn, sig["mint"], "market", after=sig["as_of"])
            status = simulate_position(conn, sig, market, settings, exit_rule, final=synthetic)
            simulated[status] = simulated.get(status, 0) + 1
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {"book": book, "new_signals": new_signals, "simulated": simulated}


def reset_book(conn: sqlite3.Connection, book: str) -> None:
    conn.execute("DELETE FROM fills WHERE position_id IN (SELECT id FROM positions WHERE book = ?)", (book,))
    conn.execute("DELETE FROM positions WHERE book = ?", (book,))
    conn.execute("DELETE FROM signals WHERE book = ?", (book,))
    conn.execute("DELETE FROM study WHERE book = ?", (book,))
    db.log_event(conn, "book_reset", {"book": book})


# --------------------------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------------------------

def bootstrap_mean_ci(values: list[float], confidence: float = 0.95, n_resamples: int = 2000, seed: int = 1) -> tuple[float, float] | None:
    if len(values) < 2:
        return None
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(rng.choice(values) for _ in range(n)) / n for _ in range(n_resamples))
    alpha = (1 - confidence) / 2
    return means[int(alpha * n_resamples)], means[min(int((1 - alpha) * n_resamples), n_resamples - 1)]


def max_drawdown(pnls_in_time_order: list[float]) -> float:
    """Largest peak-to-trough fall of the cumulative PnL curve (a non-negative number of SOL)."""
    peak = cum = worst = 0.0
    for pnl in pnls_in_time_order:
        cum += pnl
        peak = max(peak, cum)
        worst = max(worst, peak - cum)
    return worst


def book_metrics(conn: sqlite3.Connection, book: str, settings: Settings) -> dict[str, Any]:
    cfg = settings.paper
    signals = conn.execute("SELECT * FROM signals WHERE book = ? ORDER BY as_of", (book,)).fetchall()
    positions = [dict(r) for r in conn.execute("SELECT * FROM positions WHERE book = ? ORDER BY COALESCE(closed_at, opened_at, 0), id", (book,))]
    plan_row = conn.execute("SELECT plan FROM study WHERE book = ?", (book,)).fetchone()
    plan = json.loads(plan_row["plan"]) if plan_row else {**DEFAULT_PLAN, "ruleset": policy.RULESET}
    synthetic_rows = conn.execute("SELECT COUNT(*) AS n FROM signals s JOIN tokens t ON t.mint = s.mint WHERE s.book = ? AND t.is_synthetic = 1",
                                  (book,)).fetchone()["n"]
    is_synthetic = bool(signals) and synthetic_rows == len(signals)
    reasons: dict[str, int] = {}
    for s in signals:
        if s["decision"] == "rejected":
            for r in json.loads(s["reasons"]):
                key = r.split(":")[0]
                reasons[key] = reasons.get(key, 0) + 1
    by_status: dict[str, int] = {}
    for p in positions:
        by_status[p["status"]] = by_status.get(p["status"], 0) + 1
    resolved = [p for p in positions if p["status"] in FINAL_STATUSES]
    open_pos = [p for p in positions if p["status"] == "open"]
    returns = [p["net_pnl_sol"] / cfg.size_sol for p in resolved]
    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r <= 0]
    alpha = (1 - float(plan.get("confidence", 0.95))) / max(1, int(plan.get("rulesets_tried", 1)))
    ci = bootstrap_mean_ci(returns, confidence=1 - alpha, seed=cfg.seed)
    filled = [p for p in positions if p["opened_at"] is not None]
    spans = [(p["opened_at"], p["closed_at"] or p["opened_at"], p["cost_sol"]) for p in filled]
    events = sorted([(a, c) for a, _, c in spans] + [(b, -c) for _, b, c in spans])
    peak = running = 0.0
    for _, change in events:
        running += change
        peak = max(peak, running)
    times = [s["as_of"] for s in signals]
    span_days = (max(times) - min(times)) / 86400 if len(times) > 1 else 0.0
    enough = len(resolved) >= int(plan["min_resolved_candidates"]) and span_days >= float(plan["min_span_days"])
    if is_synthetic:
        verdict, verdict_note = "mechanics demo", "Synthetic data: shows that the ledger works. It is not evidence about any market."
    elif not enough:
        verdict = "inconclusive"
        verdict_note = (f"{len(resolved)} resolved candidates over {span_days:.1f} days; the pre-registered minimum is "
                        f"{plan['min_resolved_candidates']} over {plan['min_span_days']} days.")
    elif ci and ci[0] > 0:
        verdict, verdict_note = "positive-needs-replication", "Interval above zero on this window. Requires an untouched second window before any claim."
    elif ci and ci[1] < 0:
        verdict, verdict_note = "negative", "Interval below zero: this ruleset lost money after costs on this window."
    else:
        verdict, verdict_note = "inconclusive", "Interval for mean net return includes zero."
    buckets = [(-1e9, -0.9, "≤ −90%"), (-0.9, -0.5, "−90…−50%"), (-0.5, -0.1, "−50…−10%"), (-0.1, 0.0, "−10…0%"),
               (0.0, 0.1, "0…+10%"), (0.1, 0.5, "+10…+50%"), (0.5, 1.0, "+50…+100%"), (1.0, 1e9, "> +100%")]
    return {
        "book": book, "is_synthetic": is_synthetic, "ruleset": plan.get("ruleset"), "plan": plan, "config_hash": settings.config_hash(),
        "signals": len(signals), "candidates": sum(s["decision"] == "candidate" for s in signals),
        "rejected": sum(s["decision"] == "rejected" for s in signals), "rejection_reasons": dict(sorted(reasons.items(), key=lambda kv: -kv[1])),
        "positions_by_status": by_status, "resolved": len(resolved), "open": len(open_pos),
        "filled": len(filled), "partial_fills": sum(p["partial"] for p in positions),
        "failed_attempts": sum(p["failed_attempts"] for p in positions), "unsellable": by_status.get("unsellable", 0),
        "gross_pnl_sol": sum(p["gross_pnl_sol"] for p in resolved), "fees_sol": sum(p["fees_sol"] for p in resolved),
        "net_pnl_sol": sum(p["net_pnl_sol"] for p in resolved),
        "open_marked_to_last_sol": sum((p["tokens"] * (p["mark_price_sol"] or 0.0)) - p["cost_sol"] for p in open_pos),
        "open_marked_to_zero_sol": -sum(p["cost_sol"] for p in open_pos),
        "win_rate": len(wins) / len(returns) if returns else None,
        "avg_win": sum(wins) / len(wins) if wins else None, "avg_loss": sum(losses) / len(losses) if losses else None,
        "expectancy": sum(returns) / len(returns) if returns else None,
        "median_return": sorted(returns)[len(returns) // 2] if returns else None,
        "expectancy_ci": list(ci) if ci else None, "ci_confidence": 1 - alpha,
        "max_drawdown_sol": max_drawdown([p["net_pnl_sol"] for p in resolved]),
        "exposure_sol_hours": sum((b - a) * c for a, b, c in spans) / 3600, "peak_concurrent_capital_sol": peak,
        "distribution": [{"label": label, "count": sum(lo < r <= hi for r in returns)} for lo, hi, label in buckets],
        "span_days": span_days, "verdict": verdict, "verdict_note": verdict_note,
        "return_definition": "net PnL ÷ configured position size; not-filled, failed and unsellable outcomes are included",
    }
