"""Clock diagnostic for SPXUSD 1m (pre-registered step; looks at no trade outcome)."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import tjr_backtest as tj

m1 = tj.load_minutes()
r = m1["c"].pct_change().abs()
r = r[(r.index.to_series().diff() == np.timedelta64(1, "m")).values]
hm = r.index.strftime("%H:%M")
sel = (hm >= "07:00") & (hm <= "11:59")
for mon, name in ((1, "January"), (7, "July")):
    x = r[sel & (r.index.month == mon)]
    prof = x.groupby(x.index.strftime("%H:%M")).mean()
    top = prof.sort_values(ascending=False).head(5)
    print(name, "top-5 minutes by mean |1m ret| (data clock):",
          ", ".join(f"{k} {v*1e4:.2f}bp" for k, v in top.items()))
