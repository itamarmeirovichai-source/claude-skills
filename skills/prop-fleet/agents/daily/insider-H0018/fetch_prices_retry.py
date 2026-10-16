"""H0018 stage 1c (retry): Yahoo rate-limited (HTTP 429) part of the first pass, so live tickers
were wrongly marked missing. Re-request every missing ticker in small, slow batches and merge.
Only tickers named in a YFRateLimitError line of the first-pass log are retried; the others got
"possibly delisted / no data" and are genuinely absent from Yahoo.
Usage: python -I fetch_prices_retry.py <prices.parquet> <ratelimited.csv>   (updates <prices.parquet>.missing.csv)"""
import sys, time, io, contextlib, pandas as pd, yfinance as yf
out = sys.argv[1]
p = pd.read_parquet(out)
allmiss = pd.read_csv(out + ".missing.csv").ticker.astype(str).tolist()
miss = pd.read_csv(sys.argv[2]).ticker.astype(str).tolist()
rows, still, B = [p], [], 25
for i in range(0, len(miss), B):
    batch = miss[i:i + B]
    for attempt in range(4):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
            d = yf.download(batch, start="2008-12-01", end="2026-10-06", auto_adjust=False, actions=True,
                            group_by="ticker", threads=False, progress=False)
        if "Rate limit" not in buf.getvalue() and "429" not in buf.getvalue():
            break
        print("rate limited, sleeping", flush=True); time.sleep(60 * (attempt + 1))
    for t in batch:
        try:
            x = (d[t] if len(batch) > 1 else d).dropna(subset=["Close"])
        except KeyError:
            x = pd.DataFrame()
        if x.empty:
            still.append(t); continue
        spl = x["Stock Splits"].replace(0, 1.0).fillna(1.0)
        fut = spl[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
        rows.append(pd.DataFrame({"date": x.index, "ticker": t, "open": x["Open"].values,
                                  "close": x["Close"].values, "adjclose": x["Adj Close"].values,
                                  "raw_close": (x["Close"] * fut).values}))
    print(f"{i + len(batch)}/{len(miss)} still missing {len(still)}", flush=True)
    time.sleep(3)
p = pd.concat(rows, ignore_index=True).drop_duplicates(["date", "ticker"])
p.to_parquet(out)
final = sorted(set(allmiss) - (set(miss) - set(still)))
pd.Series(final, name="ticker").to_csv(out + ".missing.csv", index=False)
print("recovered", len(miss) - len(still), "| tickers with prices", p.ticker.nunique(), "| no price history", len(final))
