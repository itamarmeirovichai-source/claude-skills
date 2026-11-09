"""qe.engine.report — writes research/results/<id>.md with every standard table of criterion 12.

The file carries: N_total and the bar, the bar in Sharpe units for the OOS length, criterion-4 power and the joint power
(PARAMETERS.md, D-011), OOS period, costs (1x and 2x), trades per year and per day, days with a trade, R per trade,
gross and net in ticks / points / money / R, Sharpe with the Mertens-Opdyke CI and Lo's factor, max drawdown, worst day,
by-year, by-month, vol-tercile, session-edge / roll-week tables, the best-20-days fragility, the random-entry, permutation
and buy-and-hold comparisons, the lag variants, neighbourhood and entry-delay tables, the leak tests, the preliminary
breach counts, the reproducibility block (script, commit, seeds, command, manifest rows) and the registry_reads.log lines
of the id. The economics at each firm (criterion 11) are Department F's and are referenced, not computed here.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from .. import paths, stats
from . import pnl as _pnl

# PARAMETERS.md "Joint power of the simulable criteria" (tools/joint_power.py, 2,000 paths per cell, costs one third of gross)
JOINT_POWER = {5: {1.5: 0.32, 2.0: 0.67, 2.4: 0.78, 3.0: 0.88}, 8: {1.5: 0.63, 2.0: 0.82, 2.4: 0.89, 3.0: 0.94},
               10: {1.5: 0.72, 2.0: 0.85, 2.4: 0.91, 3.0: 0.96}}


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=paths.PROGRAM_ROOT, stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "unknown"


def _fmt(x, nd=2) -> str:
    if x is None:
        return "n/a"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return f"{int(x):,}"
    if isinstance(x, (float, np.floating)):
        if not np.isfinite(x):
            return "n/a"
        return f"{x:,.{nd}f}"
    if isinstance(x, tuple):
        return "(" + ", ".join(_fmt(v, nd) for v in x) + ")"
    return str(x)


def _table(df: pd.DataFrame, nd=2, index=True) -> str:
    d = df.copy()
    if index:
        d = d.reset_index()
    cols = list(d.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(_fmt(v, nd) for v in r.tolist()) + " |")
    return "\n".join(lines)


def _kv(d: dict, nd=2) -> str:
    return "\n".join(f"| {k} | {_fmt(v, nd)} |" for k, v in d.items())


def reads_log_lines(id_: str, log_path: Optional[Path] = None) -> list:
    p = log_path or paths.READS_LOG
    if not p.exists():
        return []
    return [l for l in p.read_text(encoding="utf-8").splitlines() if l.split(",")[1:2] == [id_]]


def joint_power_row(years: float) -> dict:
    k = min(JOINT_POWER, key=lambda y: abs(y - years))
    return {"nearest_oos_years": k, **{f"S={s}": v for s, v in JOINT_POWER[k].items()}}


def write_result(id_: str, res: _pnl.Result, *, gate: Optional[dict] = None, leaks: Optional[list] = None, lag: Optional[dict] = None,
                 neigh: Optional[pd.DataFrame] = None, delay: Optional[pd.DataFrame] = None, null_random: Optional[dict] = None,
                 null_perm: Optional[dict] = None, bh: Optional[dict] = None, rule_text: str = "", window: str = "",
                 oos_period: str = "", out_dir: Optional[Path] = None, seeds: Optional[dict] = None, command: str = "",
                 manifest_rows: Optional[list] = None, notes: str = "", log_path: Optional[Path] = None) -> Path:
    out_dir = Path(out_dir or (paths.PROGRAM_ROOT / "research" / "results"))
    out_dir.mkdir(parents=True, exist_ok=True)
    s = res.stats
    years = gate["years"] if gate else s["years"]
    z = gate["z_bar"] if gate else stats.Z_BAR
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    L = []
    L.append(f"# Result {id_} — {rule_text or res.mode}\n")
    L.append(f"Written {now} by qe.engine.report; window = {window or res.provenance.get('window')}; mode = {res.mode}; "
             f"provenance = {res.provenance.get('dataset')} (registered_id = {res.provenance.get('registered_id')}).\n")
    if notes:
        L.append(notes + "\n")
    L.append("## The bar\n")
    L.append("| item | value |\n|---|---|")
    L.append(_kv({"N_total": stats.N_TOTAL, "z bar (one-sided)": z, "OOS period": oos_period or "n/a", "OOS length (years)": years,
                  "bar in Sharpe units for this OOS length": stats.bar_sharpe_units(years, z),
                  "criterion-4 power at true Sharpe 1.5 / 2.0 / 2.4": tuple(stats.power(x, years, z) for x in (1.5, 2.0, 2.4)),
                  "joint power (criteria 3+4+7, PARAMETERS.md, nearest OOS length)": str(joint_power_row(years))}))
    L.append("\n## Costs and activity\n")
    L.append("| item | value |\n|---|---|")
    L.append(_kv({"cost model": s["cost_model"], "cost share of gross (1x)": s["cost_share_of_gross"], "trades": s["n_trades"],
                  "trades per year": s["trades_per_year"], "trades per day": s["trades_per_day"], "days with a trade": s["days_with_trade"],
                  "trading days in window": s["days"], "turnover (contracts per day)": s["turnover_contracts_per_day"],
                  "holding minutes median / mean / max": (s.get("hold_minutes_median"), s.get("hold_minutes_mean"), s.get("hold_minutes_max")),
                  "share of profit from holds <= 10 s": s.get("share_profit_held_le_10s"),
                  "longest gap between trades (days)": s["longest_gap_between_trades_days"], "win rate (net 1x)": s.get("win_rate"),
                  "R unit (points)": s["r_points"]}))
    L.append("\n## P&L (daily mark-to-market)\n")
    rows = []
    for k, lab in (("gross", "gross"), ("net_1x", "net 1x"), ("net_2x", "net 2x")):
        sh = s[f"{k}_sharpe"]
        rows.append({"series": lab, "total pts": s[f"{k}_total_pts"], "total ticks": s[f"{k}_total_pts"] / (res.config.instrument().tick),
                     "total usd": s[f"{k}_total_usd"], "mean usd/day": s[f"{k}_mean_usd_per_day"], "mean R/day": s[f"{k}_mean_R_per_day"],
                     "t_min": s[f"{k}_t_min"], "t_iid": s[f"{k}_t_iid"], "t_NW": s[f"{k}_t_nw"], "Sharpe": sh["sharpe"], "SE": sh["se"],
                     "CI90": sh["ci90"], "lower90 one-sided": sh["lower90"], "Lo factor": sh["lo_factor"],
                     "max DD usd": s[f"{k}_max_drawdown_usd"], "worst day usd": s[f"{k}_worst_day_usd"]})
    L.append(_table(pd.DataFrame(rows), 3, index=False))
    if "mean_R_net_1x" in s:
        L.append("\nPer trade: " + ", ".join(f"{k} = {_fmt(s[k], 4)}" for k in ("mean_R_gross", "mean_R_net_1x", "mean_R_net_2x", "se_R_net_1x", "t_R_net_1x_dayclustered",
                                                                             "net_per_trade_ticks_1x", "net_per_trade_usd_1x", "net_per_trade_usd_2x")))
    L.append(f"\nAnnualised vol of net 1x: ${_fmt(s['annual_vol_usd'])} = {_fmt(100 * s['annual_vol_frac_of_account'])}% of the ${_fmt(res.config.account_usd, 0)} account at the run's size.")
    L.append("\n## Best-20-days fragility\n")
    L.append("| item | value |\n|---|---|")
    L.append(_kv({"sum of the 20 best days (usd)": s["best20_sum_usd"], "share of net 1x": s["best20_share_of_net"], "net 1x without them (usd)": s["net_1x_without_best20_usd"]}))
    L.append("\n## By year (a year counts when the window holds >= 200 of its trading days)\n")
    L.append(_table(res.tables["by_year"], 2))
    L.append(f"\nYears positive: {s['years_positive']} of {s['years_counted']} counted (need {s['years_needed']}); max year share {_fmt(s['max_year_share'])}; max month share {_fmt(s['max_month_share'])}.")
    L.append("\n## By volatility tercile (trailing 20-day realized vol, ex ante)\n")
    L.append(f"Bounds {_fmt(s['vol_tercile_bounds'], 5)} — {s['vol_tercile_bounds_source']}.\n")
    L.append(_table(res.tables["by_vol_tercile"], 2))
    L.append("\n## Session-edge and roll-week share of P&L\n")
    L.append(_table(res.tables["session_roll"], 3, index=False))
    if "exit_reasons" in res.tables:
        L.append("\n## Exit reasons\n")
        L.append(_table(res.tables["exit_reasons"], 0))
    if gate:
        L.append("\n## Gate arithmetic (criteria 3, 4, 7)\n")
        L.append("| item | value |\n|---|---|")
        L.append(_kv({"criterion 3 (2x cost)": str(gate["criterion_3_2x_cost"]), "criterion 4 (significance)": str(gate["criterion_4_significance"]),
                      "criterion 7 (stability)": str(gate["criterion_7_stability"])}))
    if leaks:
        L.append("\n## Leak tests (criterion 8)\n")
        for t in leaks:
            L.append(f"- {t['test']}: {'PASS' if t['passed'] else 'FAIL'} on {t['n_checked']} sampled days; violations: {t['violations'][:5]}")
    if lag:
        L.append("\n## Execution-lag variants (the worse decides)\n")
        L.append(_table(pd.DataFrame(lag["runs"]).T, 3))
        L.append(f"\nWorst: **{lag['worst']}** at {_fmt(lag['worst_net_1x_mean_usd_per_day'], 3)} usd/day net 1x.")
    if delay is not None:
        L.append("\n## Entry delay (alpha decay)\n")
        L.append(_table(delay, 3, index=False))
    if neigh is not None:
        L.append("\n## Parameter neighbourhood (+-25% continuous, one step discrete; never changes the headline)\n")
        L.append(_table(neigh, 3, index=False))
    L.append("\n## Null models and benchmark (criterion 6)\n")
    L.append("| item | value |\n|---|---|")
    L.append(_kv({"random-entry null": str(null_random) if null_random else "not run", "shuffled-signal permutation": str(null_perm) if null_perm else "not run",
                  "buy-and-hold at matched exposure": str(bh) if bh else "not run"}))
    L.append("\n## Preliminary path-wise breach counts (information for Department F, criterion 11 is theirs)\n")
    L.append("| item | value |\n|---|---|")
    L.append(_kv(s["breaches"], 2))
    L.append("\n## Reproducibility\n")
    L.append("| item | value |\n|---|---|")
    main = sys.modules.get("__main__")
    L.append(_kv({"script": os.path.basename(getattr(main, "__file__", "interactive")), "commit": _git_commit(), "command": command or " ".join(sys.argv),
                  "seeds": str(seeds or {"config.seed": res.config.seed}), "config": str(res.config), "rule": rule_text,
                  "manifest rows": str(manifest_rows or res.provenance.get("dataset")), "n_bars": s["n_bars"]}))
    L.append("\n## registry_reads.log lines for this id\n")
    lines = reads_log_lines(id_, log_path)
    L.append("```\n" + ("\n".join(lines) if lines else "(none: synthetic or no gateway read)") + "\n```")
    L.append("\nEconomics at each eligible firm (criterion 11, $/slot-year at the decayed Sharpe, the point estimate and the lower bound): Department F from this file's daily series.\n")
    p = out_dir / f"{id_}.md"
    p.write_text("\n".join(L), encoding="utf-8")
    return p
