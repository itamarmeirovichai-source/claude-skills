"""qe.engine — the shared, registered-id-gated backtest engine (Department D, brief briefs/D-engine.md).

Modules: bars (frames, tagging, resampling, synthetic walks), rules (Rule interface, VolScaler), fills (instruments,
slippage, market/limit/stop/bracket fills, flat-by), pnl (simulate, daily P&L, standard tables, breach counts),
harness (leak tests, lag variants, neighbourhood, nulls, benchmark, gate statistics), report (research/results/<id>.md),
run (run_registered -> qe.gateway.load). Conventions: src/qe/engine/CONVENTIONS.md.
"""
from . import bars, fills, harness, pnl, report, rules, run  # noqa: F401
from .pnl import Result, RunConfig, UnregisteredRunError, simulate  # noqa: F401
from .run import run_registered  # noqa: F401
