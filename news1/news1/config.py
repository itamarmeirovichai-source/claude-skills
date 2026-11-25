"""Fixed parameters of NEWS-1. They are part of the pre-registration: changing one voids the experiment."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get("NEWS1_DATA_DIR") or ROOT / "data")
LEDGER = DATA / "ledger.jsonl"
RESULTS = DATA / "results.jsonl"
PENDING = DATA / "pending"
UNIVERSE = ROOT / "universe.json"
PROMPT = ROOT / "PROMPT.txt"

SEED = "NEWS-1/2026-11-25"
UNIVERSE_SIZE = 120
MIN_PRICE = 5.0
MIN_ADV_USD = 25_000_000.0
ADV_DAYS = 20
MAX_HEADLINES = 3

COST_PER_SIDE = 0.0005
COST_SENSITIVITY = (0.00025, 0.0010)

STAGE1_DAYS = 60
STAGE2_DAYS = 250
STAGE2_T = 3.68

# Eastern Time, (hour, minute)
WINDOW_START = (16, 0)  # on the previous trading day
WINDOW_END = (9, 0)  # on the signal day
RECORD_DEADLINE = (9, 25)
SETTLE_AFTER = (16, 20)
