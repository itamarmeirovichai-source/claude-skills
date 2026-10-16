"""H0018: list missing tickers that the first Yahoo pass named in a YFRateLimitError line.
Usage: python -I extract_ratelimited.py <fetch_prices.out> <prices.parquet.missing.csv> <out.csv>"""
import re, sys, pandas as pd
rl = set()
for l in open(sys.argv[1]).read().splitlines():
    if "RateLimit" in l or "Too Many Requests" in l:
        m = re.match(r"\[(.*?)\]:", l)
        if m: rl |= set(re.findall(r"'([^']+)'", m.group(1)))
miss = pd.read_csv(sys.argv[2]).ticker.astype(str)
print("missing", len(miss), "rate-limited among missing", miss.isin(rl).sum())
pd.Series(sorted(rl & set(miss)), name="ticker").to_csv(sys.argv[3], index=False)
