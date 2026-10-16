"""Truncation and perturbation look-ahead tests (E1_rules.md section 6) per variant."""
import sys
import stocks as S
from data import panels

D = S.prepare(panels())
for vid in sys.argv[1:]:
    for u in ("A", "B"):
        t, p, n = S.lookahead(vid, D, u, n=20)
        print(f"{vid} {u}: truncation {t}/{n}  perturbation {p}/{n}", flush=True)
