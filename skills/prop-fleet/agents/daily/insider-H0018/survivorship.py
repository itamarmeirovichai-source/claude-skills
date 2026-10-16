"""H0018: measure the delisting/survivorship gap - signals whose ticker has no Yahoo price history.
Usage: python -I survivorship.py <signals.csv> <prices.parquet>"""
import sys, pandas as pd
s = pd.read_csv(sys.argv[1]); s = s[~s.routine]
s["yr"] = s.sig_month.str[:4].astype(int)
have = set(pd.read_parquet(sys.argv[2], columns=["ticker"]).ticker.unique())
s["has_px"] = s.ticker.isin(have)
print("opportunistic signal tickers:", s.ticker.nunique(), "| with Yahoo history:", s[s.has_px].ticker.nunique(),
      "| without:", s[~s.has_px].ticker.nunique(), f"({1 - s[s.has_px].ticker.nunique() / s.ticker.nunique():.1%})")
for name, x in [("IS 2009-2016", s[s.yr <= 2016]), ("OOS 2017-2026", s[s.yr >= 2017])]:
    print(f"{name}: stock-month signals {len(x)}, share with no price history {1 - x.has_px.mean():.1%}, "
          f"share of purchase dollars with no price history {x.loc[~x.has_px, 'dollars'].sum() / x.dollars.sum():.1%}")
