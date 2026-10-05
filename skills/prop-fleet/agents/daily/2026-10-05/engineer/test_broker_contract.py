"""Tests for broker_contract.py. Offline. Run: python3 -m pytest -q test_broker_contract.py"""
import inspect
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
from broker_contract import (BracketIntent, to_projectx, to_rithmic, validate,  # noqa: E402
                             PX_SIDE, RITHMIC_SIDE)


def buy(**kw):
    d = dict(root="MES", side="BUY", qty=1, entry=5000.00, stop=4990.00,
             target=5020.00, account_id="123")
    d.update(kw)
    return BracketIntent(**d)


def sell(**kw):
    d = dict(root="MES", side="SELL", qty=2, entry=5000.00, stop=5010.00,
             target=4980.00, account_id="123")
    d.update(kw)
    return BracketIntent(**d)


def test_projectx_buy_exact_prices_and_size():
    a = to_projectx(buy(), "CON.F.US.MES.Z26", max_qty=5)
    assert a["side"] == 0 and a["size"] == 1
    assert (a["entry_price"], a["stop_loss_price"], a["take_profit_price"]) == (5000.0, 4990.0, 5020.0)
    assert a["account_id"] == 123


def test_projectx_sell_side_is_1():
    assert to_projectx(sell(), "C", max_qty=5)["side"] == 1


def test_rithmic_ticks_buy():
    a = to_rithmic(buy(), "MESZ6", "o1", max_qty=5)
    assert a["transaction_type"] == 1  # BUY in async_rithmic
    assert a["stop_ticks"] == 40 and a["target_ticks"] == 80  # 10 pt and 20 pt at 0.25
    assert a["manual_or_auto"] == 2  # AUTO, never the library default MANUAL


def test_rithmic_ticks_sell():
    a = to_rithmic(sell(), "MESZ6", "o2", max_qty=5)
    assert a["transaction_type"] == 2 and a["qty"] == 2
    assert a["stop_ticks"] == 40 and a["target_ticks"] == 80


def test_side_encodings_differ_between_apis():
    assert PX_SIDE["BUY"] != RITHMIC_SIDE["BUY"]
    assert PX_SIDE["SELL"] != RITHMIC_SIDE["SELL"]


@pytest.mark.parametrize("bad", [
    dict(qty=0), dict(qty=1.0), dict(qty=True), dict(qty=6),
    dict(stop=5001.0), dict(target=4999.0), dict(entry=5000.10),
    dict(root="SPY"), dict(side="LONG"),
])
def test_validate_rejects(bad):
    with pytest.raises(ValueError):
        validate(buy(**bad), max_qty=5)


def test_sell_with_buy_geometry_rejected():
    with pytest.raises(ValueError):
        validate(sell(stop=4990.0, target=5020.0), max_qty=5)


def _sig(venv, mod, attr):
    """Signature from a library installed in a scratch venv; skipped if absent."""
    root = os.environ.get("BROKER_VENV_ROOT", "")
    py = os.path.join(root, venv, "bin", "python")
    if not root or not os.path.exists(py):
        pytest.skip("library venv not present")
    import subprocess
    code = (f"import inspect,{mod.split('.')[0]};from {mod} import {attr.split('.')[0]} as C;"
            f"print(list(inspect.signature(C.{attr.split('.')[1]}).parameters))")
    out = subprocess.run([py, "-c", code], capture_output=True, text=True, check=True).stdout
    return eval(out)


def test_projectx_kwargs_match_library():
    params = _sig("venvpx", "project_x_py.order_manager", "OrderManager.place_bracket_order")
    assert set(to_projectx(buy(), "C", 5)) <= set(params)


def test_rithmic_named_args_match_library():
    params = _sig("venvrith", "async_rithmic.plants.order", "OrderPlant.submit_order")
    named = {"order_id", "symbol", "exchange", "qty", "transaction_type", "order_type"}
    assert named <= set(params) and "kwargs" in params
