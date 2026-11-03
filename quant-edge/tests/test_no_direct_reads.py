"""Every market-data read goes through qe.gateway.load (non-negotiable 3). This test fails on any direct read elsewhere."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"src/qe/gateway.py"}
ALLOWED_DIRS = ("src/qe/ingest/", "src/qe/qa/", "tools/")   # outcome-free ingestion and QA may read raw files
PATTERN = re.compile(r"(read_parquet\(|read_csv\(|read_feather\(|read_hdf\(|read_pickle\(|np\.load\(|quant-edge-data|DATA_ROOT\s*/)")


def test_no_direct_market_data_reads():
    offenders = []
    for py in list((ROOT / "src").rglob("*.py")) + list((ROOT / "research").rglob("*.py")):
        rel = py.relative_to(ROOT).as_posix()
        if rel in ALLOWED or rel.startswith(ALLOWED_DIRS) or rel == "src/qe/paths.py":
            continue
        for i, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
            if PATTERN.search(line) and not line.strip().startswith("#"):
                offenders.append(f"{rel}:{i}: {line.strip()[:80]}")
    assert not offenders, "direct market-data reads outside the gateway:\n" + "\n".join(offenders)
