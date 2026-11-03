import csv, os, sys, importlib.util
HERE = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location("registry_n", os.path.join(HERE, "..", "tools", "registry_n.py"))
registry_n = importlib.util.module_from_spec(spec); spec.loader.exec_module(registry_n)

def test_bar_is_fixed():
    assert registry_n.N_TOTAL == 430
    assert abs(registry_n.Z_BAR - 3.6807) < 1e-3
    assert abs(registry_n.Z_BAR_TWO_COUNT - 3.8538) < 1e-3
    assert registry_n.MIN_BOOT_DRAWS == 430000

def test_inherited_rows_sum_to_280():
    path = os.path.join(HERE, "..", "registry.csv")
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    inherited = [r for r in rows if r["source"] == "inherited"]
    assert len(inherited) == 105
    assert sum(int(r["count"] or 0) for r in inherited) == 280

def test_running_n_rejects_bad_count(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("id,count\nX1,abc\n")
    try:
        registry_n.running_n(str(p)); assert False
    except ValueError:
        pass

def test_power_numbers():
    assert abs(registry_n.power(1.5, 5) - 0.37) < 0.02
    assert abs(registry_n.power(1.5, 10) - 0.86) < 0.02
