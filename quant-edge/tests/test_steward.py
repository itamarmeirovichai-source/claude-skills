import json
from datetime import datetime, timezone
import pytest
from qe import steward


class FakeMeta:
    def __init__(self, cost, recs=1000, size=12345): self.cost, self.recs, self.size = cost, recs, size
    def get_cost(self, **kw): return self.cost
    def get_record_count(self, **kw): return self.recs
    def get_billable_size(self, **kw): return self.size


class FakeClient:
    def __init__(self, cost): self.metadata = FakeMeta(cost)


def _credit(tmp_path, rem=125.0, monthly=105.0):
    p = tmp_path / "databento_credit.json"
    p.write_text(json.dumps({"remaining_credit_usd": rem, "expiry_date": "2027-04-30", "signup_date": "2026-10-30",
                             "portal_monthly_limit_usd": monthly, "confirmed_on": "2026-11-03", "pay_as_you_go": "off"}))
    return p


def test_no_credit_file_blocks_everything(tmp_path):
    with pytest.raises(steward.CreditUnconfirmed):
        steward.load_credit(tmp_path / "missing.json")


def test_ceilings_from_confirmed_credit(tmp_path):
    c = steward.load_credit(_credit(tmp_path, 125.0, 105.0))
    cc = steward.ceilings(c)
    assert cc["plan_ceiling_usd"] == 94.0 and abs(cc["hard_cap_usd"] - 105.0) < 1e-9
    c2 = steward.load_credit(_credit(tmp_path, 60.0, 51.0))
    cc2 = steward.ceilings(c2)
    assert cc2["plan_ceiling_usd"] == 40.0 and abs(cc2["hard_cap_usd"] - 51.0) < 1e-9
    with pytest.raises(steward.SpendBlocked):
        steward.ceilings(steward.load_credit(_credit(tmp_path, 60.0, 80.0)))  # monthly limit above the hard cap


def test_alignment_rule():
    cl = FakeClient(0.5)
    with pytest.raises(ValueError):
        steward.estimate(cl, dataset="GLBX.MDP3", symbols=["ES.v.0"], schema="ohlcv-1m", start="2024-01-02T14:33:00Z", end="2024-01-02T21:00:00Z")
    est = steward.estimate(cl, dataset="GLBX.MDP3", symbols=["ES.v.0"], schema="ohlcv-1m", start="2024-01-02T14:30:00Z", end="2024-01-02T21:00:00Z")
    assert est["est_usd"] == 0.5


def test_estimate_row_before_submit_and_ceiling_enforced(tmp_path):
    credit = steward.load_credit(_credit(tmp_path))
    ledger = tmp_path / "ledger.csv"
    cl = FakeClient(20.0)
    est = steward.estimate(cl, dataset="GLBX.MDP3", symbols=["ES.v.0"], schema="ohlcv-1m", start="2010-06-06", end="2024-12-31")
    calls = []
    out = steward.request(cl, registered_id="Q-0001", mode="batch", est=est, credit=credit, ledger=ledger,
                          now=datetime(2026, 11, 4, tzinfo=timezone.utc), submit=lambda c: (calls.append(1) or "GLBX-job-1"))
    assert out["status"] == "submitted" and calls == [1]
    rows = ledger.read_text().splitlines()
    assert rows[0].startswith("ts_utc,registered_id")
    assert ",estimated," in rows[1] and ",submitted," in rows[2]
    # three more $20 requests fit (cumulative 80, room 94-80-1 = 13); the fifth is refused
    for i in range(3):
        steward.request(cl, registered_id="Q-0002", mode="batch", est=est, credit=credit, ledger=ledger,
                        now=datetime(2026, 11, 4, tzinfo=timezone.utc), submit=lambda c: "job")
    st = steward.ledger_state(ledger, "2026-11")
    assert abs(st["cumulative_usd"] - 80.0) < 1e-6   # each request counts once (its last row)
    with pytest.raises(steward.SpendBlocked):
        steward.request(cl, registered_id="Q-0003", mode="batch", est=est, credit=credit, ledger=ledger,
                        now=datetime(2026, 11, 4, tzinfo=timezone.utc), submit=lambda c: "job")


def test_streaming_only_under_one_dollar(tmp_path):
    credit = steward.load_credit(_credit(tmp_path))
    cl = FakeClient(2.0)
    est = steward.estimate(cl, dataset="GLBX.MDP3", symbols=["ES.v.0"], schema="ohlcv-1m", start="2024-01-02", end="2024-02-01")
    with pytest.raises(steward.SpendBlocked):
        steward.request(cl, registered_id="Q-0001", mode="stream", est=est, credit=credit, ledger=tmp_path / "l.csv")


def test_request_needs_registered_id(tmp_path):
    credit = steward.load_credit(_credit(tmp_path))
    cl = FakeClient(0.01)
    est = steward.estimate(cl, dataset="GLBX.MDP3", symbols=["ES.v.0"], schema="ohlcv-1m", start="2024-01-02", end="2024-01-03")
    with pytest.raises(steward.SpendBlocked):
        steward.request(cl, registered_id="", mode="stream", est=est, credit=credit, ledger=tmp_path / "l.csv")
