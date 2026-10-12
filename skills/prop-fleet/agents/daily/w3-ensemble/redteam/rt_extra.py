"""Red team F1 extras (diagnostics only): roll weeks, S1 weekend/weekday split, S2 cost break-even.
usage: CLAUDE_SCRATCH=<data dir> python3 rt_extra.py <cache dir>"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.argv = [sys.argv[0], sys.argv[1]]
import rt_analysis as A  # noqa: E402  (re-runs section 0-5 silently into rt_analysis.txt)
E, st, line, s1, s2, K = A.E, A.st, A.line, A.s1, A.s2, A.K
W0, W1 = E.W0, E.W1
out = []
P = lambda *a: (print(*a), out.append(" ".join(str(x) for x in a)))
P("=== extras")
S2n = s2(0.75, roll=False)
P(line("   S2 incl. roll weeks (FTMO cost) stack, headline k", E.stack(s1(), S2n, k=K).r))
x = S2n.net.loc[W0:W1] * 1e4; y = s2(0.75).net.loc[W0:W1] * 1e4
P(f"   S2 sessions in W: ex-roll {len(y)} mean {y.mean():+.2f}; incl roll {len(x)} mean {x.mean():+.2f}; "
  f"roll-week sessions only mean {x.loc[x.index.difference(y.index)].mean():+.2f} (n {len(x.index.difference(y.index))})")
b = pd.read_pickle(A.C / "s1_ftmo.pkl").loc[W0:W1]
S1 = s1().loc[W0:W1]
for nm, msk in (("weekdays", S1.index.dayofweek < 5), ("weekends", S1.index.dayofweek >= 5)):
    g = S1[msk]
    P(f"   S1 unit book {nm}: gross {g.gross.mean() * 1e4:+.2f} net {g.net.mean() * 1e4:+.2f} bp/d (n {len(g)})")
# S2 cost break-even in W
for c in (0.0, 0.1, 0.2, 0.3, 0.375, 0.5, 0.75):
    z = s2(c).net.loc[W0:W1] * 1e4
    P(f"   S2 alone in W at {c:.3f} pt/side: mean {z.mean():+.2f} bp/session t {z.mean() / (z.std() / np.sqrt(len(z))):+.2f}")
# per-year stack, and drop the best/worst year
r = A.base.r.loc[W0:W1]
for yr in (2023, 2024, 2025, 2026):
    q = r[r.index.year != yr]
    P(f"   stack without {yr}: mean {q.mean() * 1e4:+.2f} t {q.mean() / (q.std() / np.sqrt(len(q))):+.2f}")
(Path(__file__).parent / "rt_extra.txt").write_text("\n".join(out) + "\n")
