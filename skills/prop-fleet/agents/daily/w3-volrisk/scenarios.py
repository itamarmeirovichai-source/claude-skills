"""F2 scenarios, exactly as pre-registered in agents/prereg/F2.csv.

Firm-exact rules come from the clause files in this folder (clauses-*.md,
read from the firms' own pages on 2026-10-12)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w1-prop"))
from firms import FIRMS  # noqa: E402

FIRM_NAMES = ["FTMO Swing 2-Step 100K", "Blue Guardian 2-Step 100K", "CFT 2-Phase 100K"]
CAPS = [0.12, 0.15, 0.20, 0.30, 0.40]          # 0.40 = top of D1's grid = "no cap"
S_MAIN = [0.0, 1.0, 1.5, 2.0]
S_GRID = [round(x, 2) for x in np.arange(0.0, 3.51, 0.25)]

GAPS = dict(gap_frac=0.25, weekend_var=1.0, kill=0.8)
GARCH = dict(garch=(0.10, 0.88, 16.0))
DLLEQ = dict(dll_ref="max", real_rate=0.10, sub=24)
ALL = dict(df=3, **GAPS, **GARCH, **DLLEQ)
# post-hoc corrections of ALL (red-team findings 4, 5, 6)
FIX = dict(ALL, daily_t=True, garch=(0.10, 0.88, 100.0), payout_ref_fix=True)

# Rules as read on the firms' own pages (clauses-*.md). `stress` keys here
# override the scenario's for firm-exact scenarios only.
EXACT = {
    "FTMO Swing 2-Step 100K": dict(
        params=dict(),                       # fee 510 refunded with 1st reward (D1)
        stress=dict(dll_ref="balance")),     # 5% from the 00:00 CE(S)T balance, checked on equity
    "Blue Guardian 2-Step 100K": dict(
        # D1 proxied the shield as a 2% hard daily loss on funded; the real
        # funded daily loss is 4% from the higher of balance/equity at 5pm EST
        params=dict(funded=dict(FIRMS["Blue Guardian 2-Step 100K"]["funded"], dll=0.04)),
        stress=dict(dll_ref="max",
                    shield=dict(level=0.02, cut_split=0.5 * 0.97, breach_on=2))),
    "CFT 2-Phase 100K": dict(
        # $660 fee, never refunded; 5% DLL from the 00:05 UTC balance; $10k
        # profit cap per day PER USER -> $3,333 per account in a 3-account fleet
        params=dict(fee=660., refund=0.0, day_cap=10_000. / 3),
        stress=dict(dll_ref="balance")),
}

SCEN = {
    "F2-01": dict(stress={}, sgrid=True),                  # D1 replication
    "F2-02": dict(stress=dict(df=3)),
    "F2-03": dict(stress=dict(GAPS)),
    "F2-04": dict(stress=dict(kill=0.8)),                  # control for F2-03
    "F2-05": dict(stress=dict(GARCH)),
    "F2-06": dict(stress=dict(DLLEQ)),
    "F2-07": dict(stress={}, exact=True),                  # firm-exact rules only
    "F2-08": dict(stress=dict(real_rate=1.0), exact=True, only="Blue Guardian"),
    "F2-09": dict(stress=dict(ALL), exact=True, sgrid=True),   # DECIDES
    "F2-10": dict(seq_of="F2-07", seq_S=S_MAIN, seq_caps=[0.12, 0.20, 0.40]),
    "F2-11": dict(seq_of="F2-09", seq_S=S_MAIN, seq_caps=[0.12, 0.20, 0.40]),
    # ---- POST-HOC, added after the model red team (redteam-model.md) and
    # pre-registered as F2-12..F2-15 before being run
    "F2-12": dict(stress=dict(FIX), exact=True, sgrid=True, bg_stop=0.016),
    "F2-13": dict(stress=dict(FIX, real_rate=1.0, cost_S=0.47), exact=True, sgrid=True,
                  bg_stop=0.016),
    "F2-14a": dict(seq_of="F2-12", seq_S=S_MAIN, seq_caps=[0.12, 0.20, 0.40]),
    "F2-14b": dict(seq_of="F2-13", seq_S=S_MAIN, seq_caps=[0.12, 0.20, 0.40]),
}
for _i, _sd in enumerate((101, 202, 303, 404)):
    SCEN[f"F2-15s{_i + 1}"] = dict(stress=dict(FIX), exact=True, bg_stop=0.016,
                                   S_list=[1.0], seed=_sd)


def firm_params(firm, sc):
    """Firm dict for a scenario, and the scenario's stress with firm-exact
    overrides merged in (returned through sc_stress)."""
    F = dict(FIRMS[firm])
    if sc.get("exact"):
        F.update(EXACT[firm]["params"])
    return F


def scen_stress(firm, sc):
    st = dict(sc["stress"])
    if sc.get("exact"):
        for k, v in EXACT[firm]["stress"].items():
            if k == "real_rate" and "real_rate" in sc["stress"]:
                continue
            st[k] = v
        if st.get("dll_ref") != "equity" and "real_rate" not in st:
            st["real_rate"] = 0.10           # closed balance lags equity
        if sc.get("bg_stop") and "Blue Guardian" in firm:
            st["open_stop"] = sc["bg_stop"]  # bot stop below the Guardian Shield
    return st
