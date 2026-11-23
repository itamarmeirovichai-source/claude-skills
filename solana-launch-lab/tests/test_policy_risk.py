"""Decision rule and explainable risk components."""

from conftest import launch, market

from launchlab import db, policy, risk

MINT = "SYNTH0001test"
OK = {"launch_status": "known", "slot0_share": 0.02, "creator_share": 0.02, "cosigned_share": 0.0, "creator_prior_launches": 0,
      "creator_prior_completed": 0, "price_sol": 1e-7, "liquidity_sol": 10.0, "market_age_s": 5.0}


def codes(features):
    decision, reasons = policy.decide(features)
    return decision, {r.split(":")[0] for r in reasons}


def test_decision_rule_rejects_each_structural_problem():
    assert codes(OK) == ("candidate", set())
    assert codes({**OK, "slot0_share": 0.793}) == ("rejected", {"slot0_concentration"})   # the audited launches
    assert codes({**OK, "creator_share": 0.2})[1] == {"creator_share"}
    assert codes({**OK, "cosigned_share": 0.5})[1] == {"cosigned_supply"}
    assert codes({**OK, "creator_prior_launches": 12, "creator_prior_completed": 0})[1] == {"serial_creator"}
    assert codes({**OK, "liquidity_sol": 0.5})[1] == {"low_liquidity"}
    assert codes({**OK, "liquidity_sol": None})[1] == {"liquidity_unknown"}
    assert codes({**OK, "market_age_s": 600})[1] == {"stale_market_data"}
    assert codes({**OK, "price_sol": None})[1] == {"no_price"}


def test_unknown_launch_structure_is_a_rejection_not_a_pass():
    assert codes({**OK, "launch_status": None})[1] == {"launch_unknown"}
    assert codes({**OK, "launch_status": "unknown"})[1] == {"launch_unknown"}


def test_exit_trigger_sees_only_the_current_observation():
    rule = policy.ExitRule(take_profit=2.0, stop_loss=0.5, max_hold_s=100.0)
    assert policy.exit_trigger(1.0, 0.0, 10.0, 1.5, rule) is None
    assert policy.exit_trigger(1.0, 0.0, 10.0, 2.0, rule) == "take_profit"
    assert policy.exit_trigger(1.0, 0.0, 10.0, 0.5, rule) == "stop_loss"
    assert policy.exit_trigger(1.0, 0.0, 100.0, 1.0, rule) == "time_stop"
    assert policy.exit_trigger(1.0, 0.0, 10.0, None, rule) is None        # missing price is not a trigger


def component(report, name):
    return next(c for c in report["components"] if c["name"] == name)


def test_missing_data_is_reported_as_unknown_never_as_low_risk(conn):
    db.upsert_token(conn, MINT, is_synthetic=True, now=1.0)
    report = risk.risk_report(conn, MINT)
    by_name = {c["name"]: c for c in report["components"]}
    for name in ("launch_slot_concentration", "creator_at_launch", "wallet_relationships", "creator_history",
                 "ownership_concentration", "liquidity", "sale_impact"):
        assert by_name[name]["status"] == "unknown" and by_name[name]["level"] == "n/a" and by_name[name]["value"] is None
    assert report["summary"]["unknown"] == 7 and report["summary"]["low"] == 0
    assert by_name["data_quality"]["level"] == "high"                      # no market data at all
    assert "Not a buy signal" in report["disclaimer"]
    assert not any(k in report for k in ("score", "expected_return", "rating"))


def test_bundle_is_flagged_with_evidence_and_probabilistic_wording(conn):
    buyers = [{"wallet": f"w{i}", "tokens": 4e7, "share": 0.04} for i in range(19)]
    launch(conn, MINT, 1000.0, slot0_share=0.793, buyers=buyers, groups=[[f"w{i}" for i in range(7)], [f"w{i}" for i in range(7, 14)]])
    obs = db.observations(conn, MINT, "launch")[-1]
    funders = '[{"funder": "funderwallet123", "count": 5}]'
    conn.execute("UPDATE observations SET payload = json_set(payload, '$.shared_first_funders', json(?)) WHERE id = ?", (funders, obs["id"]))
    market(conn, MINT, 1010.0, 103.0, 170_000_000.0)
    db.add_observation(conn, MINT, "holders", "test", 1010.0, {"complete": False, "scope": "20 largest", "holders": buyers}, is_synthetic=True)
    report = risk.risk_report(conn, MINT)
    slot0 = component(report, "launch_slot_concentration")
    assert slot0["level"] == "high" and slot0["value"] == 0.793 and "19 wallet(s)" in slot0["evidence"][0]
    rel = component(report, "wallet_relationships")
    assert rel["level"] == "high" and any("co-signed" in e for e in rel["evidence"])
    assert any("probabilistic link" in e for e in rel["evidence"])
    assert "not identity" in rel["note"] and "same owner" not in str(rel).lower()
    own = component(report, "ownership_concentration")
    assert own["status"] == "partial" and own["level"] == "elevated" and abs(own["value"] - 0.40) < 1e-9
    impact = component(report, "sale_impact")
    expected_drop = 1 - (170e6 / (170e6 + 0.40 * 1e9)) ** 2                # (R/(R+Q))^2
    assert abs(impact["value"]["price_drop_if_top10_sell"] - expected_drop) < 1e-9 and impact["level"] == "high"
    for c in report["components"]:
        assert c["evidence"] and c["status"] in ("known", "partial", "unknown")


def test_risk_report_as_of_uses_only_earlier_observations(conn):
    launch(conn, MINT, 1000.0, slot0_share=0.02)
    market(conn, MINT, 1010.0, 40.0, 1_000_000_000.0)
    early = risk.risk_report(conn, MINT, as_of=1010.0)
    market(conn, MINT, 2000.0, 2.0, 1_000_000_000.0)                       # liquidity collapses later
    assert risk.risk_report(conn, MINT, as_of=1010.0) == early
    assert component(risk.risk_report(conn, MINT), "liquidity")["level"] == "high"
    assert component(early, "liquidity")["level"] == "low"
