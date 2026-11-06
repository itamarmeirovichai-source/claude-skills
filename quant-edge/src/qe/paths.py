import os
from pathlib import Path

PROGRAM_ROOT = Path(os.environ.get("QE_PROGRAM_ROOT", Path(__file__).resolve().parents[2]))
DATA_ROOT = Path(os.environ.get("QE_DATA_ROOT", Path.home() / "quant-edge-data"))
REGISTRY_CSV = PROGRAM_ROOT / "registry.csv"
READS_LOG = PROGRAM_ROOT / "registry_reads.log"
MANIFEST_CSV = PROGRAM_ROOT / "data" / "manifest.csv"
HOLDOUT_UNLOCK = PROGRAM_ROOT / "HOLDOUT_UNLOCK"
HOLDOUT_START = "2025-01-01"
