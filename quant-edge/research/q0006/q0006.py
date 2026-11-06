#!/usr/bin/env python3
"""Q-0006 gold dip swing (registered 93cb97a): same rule code as Q-0005 (research/q0005/dipswing.py), root GC,
1 bp per side + 3%/yr markup (2x: 2 bp, 6%/yr). Usage: python3 quant-edge/research/q0006/q0006.py --stage {is,dryrun,oos}"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "q0005"))
import q0005  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["is", "dryrun", "oos"])
    a = ap.parse_args()
    q0005.main("Q-0006", a.stage, f"python3 quant-edge/research/q0006/q0006.py --stage {a.stage}")
