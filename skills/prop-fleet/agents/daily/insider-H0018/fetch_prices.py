"""H0018 stage 1c: daily prices from Yahoo (yfinance) for every signal ticker plus SPY.
Saves long-format parquet: date, ticker, open, close (split-adjusted), adjclose (split+div adjusted),
raw_close (close with later splits undone = price actually traded that day).
Usage: python -I fetch_prices.py <signals.csv> <out_parquet>"""
import sys, time, pandas as pd, numpy as np, yfinance as yf
tick = sorted(set(pd.read_csv(sys.argv[1]).ticker.astype(str)) | {"SPY"})
out, rows, missing = sys.argv[2], [], []
B = 80
for i in range(0, len(tick), B):
    batch = tick[i:i + B]
    for attempt in range(3):
        try:
            d = yf.download(batch, start="2008-12-01", end="2026-10-06", auto_adjust=False, actions=True,
                            group_by="ticker", threads=True, progress=False)
            break
        except Exception as e:
            print("retry", e); time.sleep(10)
    for t in batch:
        try:
            x = d[t] if len(batch) > 1 else d
            x = x.dropna(subset=["Close"])
        except KeyError:
            x = pd.DataFrame()
        if x.empty:
            missing.append(t); continue
        spl = x["Stock Splits"].replace(0, 1.0).fillna(1.0)
        # raw price on day d = split-adjusted close * product of split ratios effective after d
        fut = spl[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
        rows.append(pd.DataFrame({"date": x.index, "ticker": t, "open": x["Open"].values,
                                  "close": x["Close"].values, "adjclose": x["Adj Close"].values,
                                  "raw_close": (x["Close"] * fut).values}))
    print(f"{i + len(batch)}/{len(tick)} missing so far {len(missing)}", flush=True)
    time.sleep(1)
p = pd.concat(rows, ignore_index=True)
p.to_parquet(out)
pd.Series(missing, name="ticker").to_csv(out + ".missing.csv", index=False)
print("tickers with prices", p.ticker.nunique(), "| no price history", len(missing), "of", len(tick))
