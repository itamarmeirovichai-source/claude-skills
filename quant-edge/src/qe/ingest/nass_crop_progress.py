"""Build cal_nass_crop_progress from archived NASS Crop Progress report text (ESMIS, publication crop-progress).

Outcome-free: reads only the report text. One row per (report, crop) with the national good+excellent share for 'this week'
(the 'NN States' total row) and 'Previous week', from the Corn / Soybean Condition tables. ts = release instant (16:00 ET
on the release date in the archive index) in UTC.
"""
import json
import re
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from .. import paths
from . import common

RAW = paths.DATA_ROOT / "raw" / "nass_crop_progress"
HDR = {"corn": re.compile(r"^Corn Condition - Selected States"), "soybeans": re.compile(r"^Soybean Condition - Selected States")}
NUM = re.compile(r"\(NA\)|-|\d+")


def _vals(line: str):
    part = line.split(":", 1)[1] if ":" in line else ""
    toks = NUM.findall(part)
    if len(toks) != 5:
        return None
    if any(t == "(NA)" for t in toks):
        return None
    return [0 if t == "-" else int(t) for t in toks]


def parse_report(text: str) -> dict:
    lines = text.splitlines()
    out = {}
    for crop, rx in HDR.items():
        for i, l in enumerate(lines):
            if rx.match(l.strip()):
                this = prev = None
                for l2 in lines[i + 1:i + 60]:
                    s = l2.strip()
                    if this is None and re.match(r"^\d+ States", s):
                        this = _vals(s)
                    elif s.startswith("Previous week"):
                        prev = _vals(s)
                        break
                out[crop] = (this, prev)
                break
    return out


def build() -> pd.DataFrame:
    idx = json.loads((RAW / "index.json").read_text())
    rows = []
    for f in sorted((RAW / "txt").glob("*.txt")):
        txt = f.read_text(encoding="latin-1")
        m = re.search(r"Released\s+([A-Z][a-z]+\.?\s+\d{1,2},\s+\d{4})", txt)
        # the report's own 'Released <date>' line wins over the archive index date (index dates are sometimes off)
        date = pd.Timestamp(m.group(1).replace(".", "")).strftime("%Y-%m-%d") if m else f.name[:10]
        date_src = "report text" if m else "archive index"
        rep = parse_report(txt)
        ts = pd.Timestamp(f"{date} 16:00", tz=ZoneInfo("America/New_York")).tz_convert("UTC")
        for crop in ("corn", "soybeans"):
            this, prev = rep.get(crop, (None, None))
            ge = this[3] + this[4] if this else None
            gp = prev[3] + prev[4] if prev else None
            rows.append({"ts": ts, "date_local": date, "time_local": "16:00", "tz": "America/New_York", "crop": crop,
                         "ge": ge, "ge_prev": gp, "delta": (ge - gp) if (ge is not None and gp is not None) else None,
                         "has_table": crop in rep, "file": f.name, "date_source": date_src, "index_date": f.name[:10]})
    df = pd.DataFrame(rows)
    return df


def main():
    df = build()
    info = common.land("cal_nass_crop_progress", df, "calendars/cal_nass_crop_progress.csv", fmt="csv",
                       source="https://esmis.nal.usda.gov/publication/crop-progress (report .txt files)", licence_status="free",
                       resolution="event", tz_note="ts = release instant (16:00 ET on the archived release date) in UTC",
                       notes=f"national good+excellent % this week and previous week; corn and soybeans; release date from the report text (Released <date>) else archive index; {common.today()}")
    print(info)


if __name__ == "__main__":
    main()
