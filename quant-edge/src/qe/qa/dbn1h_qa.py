"""Outcome-free QA of the Databento 1h continuous bars (structure only: bar presence at the rows' hours, rolls, price levels).
No return, no P&L, no event-conditional statistic is computed. Writes quant-edge/data/qa/dbn1h_qa.md."""
import pandas as pd
import exchange_calendars as xc
from .. import paths

HOURS = {"ES": [9, 10, 11, 14, 15], "NQ": [9, 10, 11, 14, 15], "YM": [9, 10, 11, 14, 15], "EMD": [9, 10, 11, 14, 15],
         "NKD": [9, 10, 11, 14, 15], "UB": [18, 19, 14, 15], "ZN": [18, 19, 14, 15], "ZC": [20, 21, 9, 12, 13],
         "ZS": [20, 21, 9, 12, 13], "NG": [18, 19, 9, 12, 14]}


def main():
    cal = xc.get_calendar("XNYS")
    sess = set(d.date() for d in cal.sessions_in_range("2010-06-07", "2024-12-31"))
    lines = ["# QA: Databento GLBX ohlcv-1h continuous (.v.0) bars, IS+OOS files (outcome-free)", "",
             "Share of XNYS sessions (evening hours: the calendar day before the session) with a bar at each ET hour the rows use; "
             "rolls = instrument_id changes; close min/max = price levels (units as delivered).", ""]
    for root, hrs in HOURS.items():
        df = pd.read_parquet(paths.DATA_ROOT / f"derived/dbn_glbx_1h_{root}.parquet")
        et = df["ts"].dt.tz_convert("America/New_York")
        keys = set(zip(et.dt.date, et.dt.hour))
        df["y"] = et.dt.year
        lines += [f"## {root}", "", "| year | sessions | " + " | ".join(f"h{h:02d}" for h in hrs) + " | rolls | close min | close max |",
                  "|" + "---|" * (len(hrs) + 5)]
        for y in range(2010, 2025):
            ss = [d for d in sess if d.year == y]
            cells = []
            for h in hrs:
                if h >= 18:
                    n = sum(((d - pd.Timedelta(days=1)), h) in keys for d in ss)
                else:
                    n = sum((d, h) in keys for d in ss)
                cells.append(f"{n / max(len(ss), 1):.3f}")
            g = df[df["y"] == y]
            rolls = int((g["instrument_id"].diff().fillna(0) != 0).sum())
            lines.append(f"| {y} | {len(ss)} | " + " | ".join(cells) + f" | {rolls} | {g['close'].min():.4g} | {g['close'].max():.4g} |")
        lines.append("")
    out = paths.PROGRAM_ROOT / "data" / "qa" / "dbn1h_qa.md"
    out.write_text("\n".join(lines) + "\n")
    print(out)


if __name__ == "__main__":
    main()
