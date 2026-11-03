import csv, json, os, subprocess, sys, importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("register", HERE.parent / "tools" / "register.py")
register = importlib.util.module_from_spec(spec); spec.loader.exec_module(register)

GOOD = {
    "id": "Q-0001", "date": "2026-11-04", "owner": "Dept D", "family": "test-family", "lane": "3",
    "hypothesis": "test", "rules": "enter at 02:00 ET, exit 03:00 ET", "parameters": "none", "grid": "single configuration",
    "sign": "long", "instruments": "ES", "holding": "60 min", "firm_structure": "overnight-session-futures",
    "data": "es_1m_rth", "data_sha256": "pending-purchase", "split": "IS=2010-06-06..2014-12-31;OOS=2015-01-01..2024-12-31;HOLDOUT=2025-01-01..",
    "vol_scaler": "ex-ante 20d realized, cap 3x, floor 0.3x", "guard_fraction": "0.7", "decay_haircut": "0.5",
    "cost_model": "ES 0.30 pt + $2.50 per side; 2x run attached", "decision_rule": "OOS net mean > 0, t >= 3.6807, p_alpha > 0", "count": "1",
}


def _reg(tmp_path):
    p = tmp_path / "registry.csv"
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=register.COLUMNS); w.writeheader()
        w.writerow({c: "" for c in register.COLUMNS} | {"id": "H0012", "source": "inherited", "count": "1", "family": "overnight-gap-fade"})
    return p


def test_good_row_registers_and_stamps(tmp_path):
    reg = _reg(tmp_path)
    assert register.validate(GOOD, register.load(reg)) == []
    register.append(GOOD, reg)
    rows = register.load(reg)
    assert rows[-1]["source"] == "program" and rows[-1]["status"] == "registered" and rows[-1]["registered_commit"] == "PENDING"
    register.stamp("Q-0001", "abc1234", reg)
    assert register.load(reg)[-1]["registered_commit"] == "abc1234"


def test_refusals(tmp_path):
    reg = _reg(tmp_path)
    bad = dict(GOOD, sign="unfixed(2 counts)", count="1")
    assert any("unfixed" in e for e in register.validate(bad, register.load(reg)))
    bad = dict(GOOD, split="IS=2010-06-06..2014-12-31;OOS=2015-01-01..2018-12-31;HOLDOUT=2025-01-01..")
    assert any("under 5" in e for e in register.validate(bad, register.load(reg)))
    bad = dict(GOOD, cost_model="ES 0.30 pt per side")
    assert any("2x" in e for e in register.validate(bad, register.load(reg)))
    bad = dict(GOOD, result_mean_R="0.1")
    assert any("empty at registration" in e for e in register.validate(bad, register.load(reg)))
    register.append(GOOD, reg)
    assert any("already exists" in e for e in register.validate(GOOD, register.load(reg)))


def test_family_cap(tmp_path):
    reg = _reg(tmp_path)
    for i in range(5):
        register.append(dict(GOOD, id=f"Q-{i+1:04d}"), reg)
    errs = register.validate(dict(GOOD, id="Q-0006"), register.load(reg))
    assert any("cap is 5" in e for e in errs)


def test_cli_dry_run(tmp_path):
    reg = _reg(tmp_path)
    rowfile = tmp_path / "row.json"; rowfile.write_text(json.dumps(GOOD))
    out = subprocess.run([sys.executable, str(HERE.parent / "tools" / "register.py"), str(rowfile), "--registry", str(reg), "--dry-run"],
                         capture_output=True, text=True)
    assert out.returncode == 0 and "would be appended" in out.stdout
    assert len(register.load(reg)) == 1
