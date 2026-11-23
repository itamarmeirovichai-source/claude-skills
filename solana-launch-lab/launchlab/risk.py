"""Explainable risk components, computed "as of" a point in time from stored observations only.

There is deliberately no single score. A component is a statement plus its evidence, source, timestamp and
confidence; when the data to compute it is absent the component says `unknown`. Nothing in a risk report is
an expected-return estimate.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from . import amm, db

DISCLAIMER = ("Risk-of-loss indicators only. Not a buy signal, price forecast or return estimate. "
              "A launch with no flags can still go to zero.")

# Default thresholds for the low / elevated / high labels. They are presentation choices, not findings.
THRESHOLDS = {
    "slot0_share": (0.10, 0.25),
    "creator_share": (0.04, 0.10),
    "top10_share": (0.25, 0.50),
    "liquidity_sol": (30.0, 5.0),        # below first = elevated, below second = high
    "price_drop_if_top_sell": (0.40, 0.80),
}


def _level(value: float, bounds: tuple[float, float]) -> str:
    return "high" if value >= bounds[1] else "elevated" if value >= bounds[0] else "low"


def _component(name: str, status: str, level: str, value: Any, evidence: list[str], source: str | None,
               observed_at: float | None, confidence: str, note: str = "") -> dict[str, Any]:
    return {"name": name, "status": status, "level": level, "value": value, "evidence": evidence,
            "source": source, "observed_at": observed_at, "confidence": confidence, "note": note}


def _unknown(name: str, why: str) -> dict[str, Any]:
    return _component(name, "unknown", "n/a", None, [why], None, None, "none")


def _latest(conn: sqlite3.Connection, mint: str, kind: str, as_of: float | None) -> dict[str, Any] | None:
    rows = db.observations(conn, mint, kind, as_of=as_of)
    return rows[-1] if rows else None


def usable_price(obs: dict[str, Any]) -> bool:
    """A market observation whose price means something: it has one, and it is not from a drained or dust pool."""
    return obs["payload"].get("price_sol") is not None and not obs["payload"].get("negligible_liquidity")


def latest_market(conn: sqlite3.Connection, mint: str, as_of: float | None) -> dict[str, Any] | None:
    """The market observation to describe the token by: the latest reading of each pool, then the deepest pool
    among those read within two minutes of the newest. A token can have several pools; a dust pool must not win."""
    rows = [r for r in db.observations(conn, mint, "market", as_of=as_of) if usable_price(r)]
    if not rows:
        return None
    per_pool: dict[tuple[str, str], dict[str, Any]] = {}
    for r in rows:
        per_pool[(r["provider"], str(r["payload"].get("pool_address")))] = r
    newest = rows[-1]["observed_at"]
    recent = [r for r in per_pool.values() if newest - r["observed_at"] <= 120]

    def depth(r: dict[str, Any]) -> tuple[bool, float, float, float]:
        p = r["payload"]
        return (bool(p.get("quote_reserve_sol") and p.get("base_reserve")), float(p.get("liquidity_sol") or 0.0),
                float(p.get("liquidity_usd") or 0.0), r["observed_at"])

    return max(recent, key=depth)


def risk_report(conn: sqlite3.Connection, mint: str, as_of: float | None = None, *, paper_size_sol: float = 0.5) -> dict[str, Any]:
    token = conn.execute("SELECT * FROM tokens WHERE mint = ?", (mint,)).fetchone()
    if token is None:
        raise KeyError(mint)
    launch = _latest(conn, mint, "launch", as_of)
    holders = _latest(conn, mint, "holders", as_of)
    market = latest_market(conn, mint, as_of)
    comps: list[dict[str, Any]] = []
    lp = launch["payload"] if launch else {}
    launch_ok = bool(launch) and lp.get("status") in ("known", "partial")
    partial = lp.get("status") == "partial"

    # 1. creation-slot concentration -----------------------------------------------------------
    if not launch_ok:
        why = lp.get("reason") if launch else "creation-slot transactions have not been read"
        comps.append(_unknown("launch_slot_concentration", str(why)))
        comps.append(_unknown("creator_at_launch", str(why)))
        comps.append(_unknown("wallet_relationships", str(why)))
    else:
        assert launch is not None
        share = float(lp.get("slot0_share") or 0.0)
        buyers = lp.get("slot0_buyers") or []
        comps.append(_component(
            "launch_slot_concentration", "partial" if partial else "known", _level(share, THRESHOLDS["slot0_share"]), share,
            [f"{len(buyers)} wallet(s) bought {share:.1%} of total supply in the creation slot",
             *(["the bonding curve completed and migrated inside the creation slot"] if lp.get("migrated_in_creation_slot") else [])],
            launch["provider"], launch["observed_at"], "medium" if partial else "high",
            "Lower bound: only part of the creation slot was read." if partial else "Read directly from the creation-slot transactions."))
        creator_share = float(lp.get("creator_share_at_launch") or 0.0)
        comps.append(_component(
            "creator_at_launch", "partial" if partial else "known", _level(creator_share, THRESHOLDS["creator_share"]), creator_share,
            [f"creator {str(lp.get('creator'))[:10]}… bought {creator_share:.2%} of supply in the creation transaction"],
            launch["provider"], launch["observed_at"], "medium" if partial else "high"))
        groups = lp.get("cosigner_groups") or []
        by_wallet = {b["wallet"]: b["share"] for b in buyers}
        cosigned = sum(by_wallet.get(w, 0.0) for g in groups for w in g)
        funders = lp.get("shared_first_funders") or []
        evidence = [f"{len(g)} wallets co-signed one creation-slot transaction" for g in groups]
        evidence += [f"{f['count']} wallets share first funder {str(f['funder'])[:10]}… (probabilistic link)" for f in funders]
        if not evidence:
            evidence = ["no co-signed purchases found in the creation slot"]
        comps.append(_component(
            "wallet_relationships", "partial" if partial else "known", _level(cosigned, THRESHOLDS["slot0_share"]), cosigned, evidence,
            launch["provider"], launch["observed_at"], "high" if groups else "low",
            "Co-signing one transaction shows coordination, not identity. A shared funder is a probabilistic link: "
            "exchanges and launch services fund many unrelated wallets. Neither proves common ownership."))

    # 2. creator history -----------------------------------------------------------------------
    launches, completed = lp.get("creator_prior_launches"), lp.get("creator_prior_completed")
    if not launch or launches is None or completed is None:
        comps.append(_unknown("creator_history", "needs an indexer of all launches by the creator; not available from the configured sources"))
    else:
        assert launch is not None
        rate = completed / launches if launches else None
        level = "high" if launches >= 5 and (rate or 0) < 0.10 else "elevated" if launches >= 2 and completed == 0 else "low"
        comps.append(_component("creator_history", "known", level, {"prior_launches": launches, "prior_completed": completed},
                                [f"{launches} earlier launch(es) by this creator, {completed} completed the curve"],
                                launch["provider"], launch["observed_at"], "medium"))

    # 3. ownership concentration ---------------------------------------------------------------
    top10 = None
    if not holders or not holders["payload"].get("holders"):
        comps.append(_unknown("ownership_concentration",
                              "holder accounts could not be read (the public RPC refuses this query; a custom RPC or indexer is needed)"))
    else:
        hp = holders["payload"]
        top = sorted(hp["holders"], key=lambda h: -h.get("share", 0.0))[:10]
        top10 = sum(h.get("share", 0.0) for h in top)
        complete = bool(hp.get("complete"))
        comps.append(_component(
            "ownership_concentration", "known" if complete else "partial", _level(top10, THRESHOLDS["top10_share"]), top10,
            [f"top {len(top)} non-pool accounts hold {top10:.1%} of supply", f"scope: {hp.get('scope', 'unspecified')}"],
            holders["provider"], holders["observed_at"], "medium" if complete else "low",
            "" if complete else "Only the largest accounts were readable; smaller related wallets are not counted."))

    # 4. liquidity and 5. sale impact ----------------------------------------------------------
    mp = market["payload"] if market else {}
    liquidity_sol = mp.get("liquidity_sol")
    if liquidity_sol is None and mp.get("liquidity_usd") and mp.get("sol_usd"):
        liquidity_sol = mp["liquidity_usd"] / mp["sol_usd"] / 2  # provider liquidity counts both sides
    if not market or liquidity_sol is None:
        comps.append(_unknown("liquidity", "no pool or curve depth in the stored observations"))
    else:
        level = "high" if liquidity_sol < THRESHOLDS["liquidity_sol"][1] else "elevated" if liquidity_sol < THRESHOLDS["liquidity_sol"][0] else "low"
        burned = lp.get("lp_burned_at_migration")
        comps.append(_component(
            "liquidity", "known", level, liquidity_sol,
            [f"about {liquidity_sol:.2f} SOL of quote-side depth on the {mp.get('venue') or 'unknown venue'}",
             {True: "LP tokens were burned in the migration transaction", False: "LP tokens were NOT burned at migration",
              None: "LP control not read"}[burned if burned in (True, False) else None]],
            market["provider"], market["observed_at"], "medium",
            "Depth is what a seller can actually take out; a quoted market cap is not."))
    base, quote = mp.get("base_reserve"), mp.get("quote_reserve_sol")
    if not base or not quote:
        comps.append(_unknown("sale_impact", "pool reserves are not in the stored observations"))
    else:
        assert market is not None
        res = amm.Reserves(float(quote), float(base))
        evidence = [f"a {paper_size_sol:g} SOL buy would pay about {amm.buy_price_impact(res.quote, paper_size_sol):.1%} above the quoted price"]
        value: dict[str, Any] = {"buy_impact_at_paper_size": amm.buy_price_impact(res.quote, paper_size_sol)}
        level = "low"
        if top10 is not None:
            ratio = amm.price_ratio_after_sale(res.base, top10 * amm.TOTAL_SUPPLY)
            drop = 1 - ratio
            value["price_drop_if_top10_sell"] = drop
            evidence.append(f"scenario: the top-10 non-pool accounts ({top10:.1%} of supply) sell everything → price falls about {drop:.0%}")
            level = _level(drop, THRESHOLDS["price_drop_if_top_sell"])
        else:
            evidence.append("scenario 'top holders sell' not computed: holdings unknown")
        comps.append(_component("sale_impact", "known" if top10 is not None else "partial", level, value, evidence,
                                market["provider"], market["observed_at"], "medium",
                                "Constant-product estimate, P_after/P_before = (R/(R+Q))². Ignores fees and other traders."))

    # 6. data quality ---------------------------------------------------------------------------
    all_obs = db.observations(conn, mint, as_of=as_of)
    stale = sum(1 for o in all_obs if o["stale"])
    missing = sum(1 for o in all_obs if o["missing"])
    args: list[Any] = [mint]
    sql = "SELECT COUNT(*) AS n FROM conflicts WHERE mint = ?"
    if as_of is not None:
        sql += " AND observed_at <= ?"
        args.append(as_of)
    conflicts = conn.execute(sql, args).fetchone()["n"]
    dq_level = "high" if not market else "elevated" if (stale or missing or conflicts) else "low"
    comps.append(_component("data_quality", "known", dq_level,
                            {"observations": len(all_obs), "stale": stale, "with_missing_fields": missing, "provider_conflicts": conflicts},
                            [f"{len(all_obs)} observation(s); {stale} stale; {missing} with missing fields; {conflicts} provider conflict(s)"],
                            "local store", as_of, "high"))

    known = [c for c in comps if c["status"] != "unknown"]
    return {
        "mint": mint, "as_of": as_of, "is_synthetic": bool(token["is_synthetic"]), "components": comps,
        "summary": {"high": sum(c["level"] == "high" for c in comps), "elevated": sum(c["level"] == "elevated" for c in comps),
                    "low": sum(c["level"] == "low" for c in comps), "unknown": len(comps) - len(known),
                    "completeness": len(known) / len(comps)},
        "disclaimer": DISCLAIMER,
    }
