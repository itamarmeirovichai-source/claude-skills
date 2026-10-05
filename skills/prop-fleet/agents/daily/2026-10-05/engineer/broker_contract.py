"""Broker contract draft (engineer, 2026-10-05). Offline, no network, no accounts.

One broker-neutral order intent -> the exact arguments each prop-firm API needs.
This is the smallest first step of the automation route (route.md). It is a
proposal for the bot repository, which is not attached to this session.

Facts encoded here and where they come from (checked 2026-10-05 by introspecting
the installed packages in a Python 3.12 venv, see lib_probe.txt):
  - project-x-py 4.4.0 OrderManager.place_bracket_order(contract_id, side, size,
    entry_price, stop_loss_price, take_profit_price, entry_type, account_id):
    ABSOLUTE prices; side BUY=0, SELL=1 (project_x_py/types/trading.py).
  - async-rithmic 1.6.6 OrderPlant.submit_order(order_id, symbol, exchange, qty,
    transaction_type, order_type, stop_ticks=, target_ticks=, account_id=, ...):
    bracket legs as RELATIVE TICKS; TransactionType BUY=1, SELL=2;
    RithmicClient default manual_or_auto = MANUAL (1); AUTO = 2.
  - ES / NQ price grid 0.25: every OHLC price in the three ES/NQ 1m samples under
    agents/daily is a multiple of 0.25 (11,580 prices checked, lib_probe.txt).
The two APIs disagree on side encoding and on price-vs-tick brackets; mapping
either one wrong flips a trade or moves a stop. The tests pin both.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

TICK = {"ES": 0.25, "MES": 0.25, "NQ": 0.25, "MNQ": 0.25}

PX_SIDE = {"BUY": 0, "SELL": 1}          # project-x-py OrderSide
RITHMIC_SIDE = {"BUY": 1, "SELL": 2}     # async_rithmic TransactionType
RITHMIC_AUTO = 2                         # async_rithmic OrderPlacement.AUTO


@dataclass(frozen=True)
class BracketIntent:
    root: str          # ES, MES, NQ, MNQ
    side: str          # BUY or SELL
    qty: int           # contracts, integer >= 1
    entry: float       # limit entry price, index points
    stop: float        # stop-loss price
    target: float      # take-profit price
    account_id: str


class Broker(Protocol):
    """What the bot needs from any broker; IBKR becomes one implementation."""
    async def accounts(self) -> list[str]: ...
    async def positions(self, account_id: str) -> dict[str, int]: ...
    async def place_bracket(self, intent: BracketIntent) -> str: ...
    async def cancel_all(self, account_id: str) -> None: ...
    async def flatten_all(self, account_id: str) -> None: ...


def validate(i: BracketIntent, max_qty: int) -> None:
    if i.root not in TICK:
        raise ValueError(f"unknown root {i.root}")
    if i.side not in ("BUY", "SELL"):
        raise ValueError(f"bad side {i.side}")
    if not isinstance(i.qty, int) or isinstance(i.qty, bool) or i.qty < 1:
        raise ValueError("qty must be an integer >= 1")
    if i.qty > max_qty:
        raise ValueError(f"qty {i.qty} exceeds firm max {max_qty}")
    t = TICK[i.root]
    for name, p in (("entry", i.entry), ("stop", i.stop), ("target", i.target)):
        if abs(p / t - round(p / t)) > 1e-9:
            raise ValueError(f"{name} {p} not on the {t} tick grid")
    if i.side == "BUY" and not (i.stop < i.entry < i.target):
        raise ValueError("BUY needs stop < entry < target")
    if i.side == "SELL" and not (i.target < i.entry < i.stop):
        raise ValueError("SELL needs target < entry < stop")


def to_projectx(i: BracketIntent, contract_id: str, max_qty: int) -> dict:
    validate(i, max_qty)
    return dict(contract_id=contract_id, side=PX_SIDE[i.side], size=i.qty,
                entry_price=i.entry, stop_loss_price=i.stop,
                take_profit_price=i.target, entry_type="limit",
                account_id=int(i.account_id))


def to_rithmic(i: BracketIntent, symbol: str, order_id: str, max_qty: int,
               exchange: str = "CME") -> dict:
    validate(i, max_qty)
    t = TICK[i.root]
    return dict(order_id=order_id, symbol=symbol, exchange=exchange, qty=i.qty,
                transaction_type=RITHMIC_SIDE[i.side], order_type=1,  # LIMIT
                price=i.entry,
                stop_ticks=int(round(abs(i.entry - i.stop) / t)),
                target_ticks=int(round(abs(i.target - i.entry) / t)),
                account_id=i.account_id, manual_or_auto=RITHMIC_AUTO)
