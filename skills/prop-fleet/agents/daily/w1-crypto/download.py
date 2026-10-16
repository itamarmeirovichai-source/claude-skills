"""Download Binance public data (data.binance.vision) for D3. Writes parquet to DATA dir (not committed)."""
import io, sys, zipfile, os, concurrent.futures as cf
import requests, pandas as pd

DATA = sys.argv[1] if len(sys.argv) > 1 else "data"
BASE = "https://data.binance.vision/data"
CANDS = ("BTC ETH BNB XRP ADA SOL DOGE DOT LTC LINK BCH TRX AVAX MATIC POL ATOM ETC XLM EOS FIL UNI NEAR AAVE "
         "ALGO VET ICP SHIB APT ARB OP SUI LUNA FTT WAVES XMR NEO IOTA ZEC DASH XTZ SAND MANA AXS FTM APE GALA "
         "CHZ CRV INJ TON PEPE WIF HBAR THETA EGLD").split()
PERP = {"SHIB": "1000SHIB", "PEPE": "1000PEPE"}
MONTHS = pd.period_range("2018-07", "2026-09", freq="M").strftime("%Y-%m")
KCOLS = ["open_time", "open", "high", "low", "close", "volume", "close_time", "qvol", "n", "tb", "tq", "ign"]
S = requests.Session()


def get(url):
    for _ in range(4):
        try:
            r = S.get(url, timeout=60)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            return z.read(z.namelist()[0])
        except Exception:
            continue
    raise RuntimeError(url)


def kl(raw):
    df = pd.read_csv(io.BytesIO(raw), header=None)
    if not str(df.iloc[0, 0]).isdigit():
        df = df.iloc[1:]
    df = df.iloc[:, :12]; df.columns = KCOLS
    t = df.open_time.astype("int64")
    t = t.where(t < 1e14, t // 1000)  # 2025+ spot files use microseconds
    df.index = pd.to_datetime(t, unit="ms"); df.index.name = "t"
    return df[["open", "high", "low", "close", "volume", "qvol"]].astype(float)


def fund(raw):
    df = pd.read_csv(io.BytesIO(raw), header=None)
    if not str(df.iloc[0, 0]).isdigit():
        df = df.iloc[1:]
    t = df.iloc[:, 0].astype("int64")
    return pd.Series(df.iloc[:, 2].astype(float).values, index=pd.to_datetime(t, unit="ms"), name="f")


def job(kind, c):
    out = f"{DATA}/{kind}_{c}.parquet"
    if os.path.exists(out):
        return kind, c, "cached"
    parts = []
    for m in MONTHS:
        if kind == "spot1h":
            raw = get(f"{BASE}/spot/monthly/klines/{c}USDT/1h/{c}USDT-1h-{m}.zip"); f = kl
        elif kind == "perp1d":
            s = PERP.get(c, c); raw = get(f"{BASE}/futures/um/monthly/klines/{s}USDT/1d/{s}USDT-1d-{m}.zip"); f = kl
        else:
            s = PERP.get(c, c); raw = get(f"{BASE}/futures/um/monthly/fundingRate/{s}USDT/{s}USDT-fundingRate-{m}.zip"); f = fund
        if raw is not None:
            parts.append(f(raw))
    if not parts:
        return kind, c, "MISSING"
    df = pd.concat(parts).sort_index()
    df = df[~df.index.duplicated()]
    (df.to_frame() if isinstance(df, pd.Series) else df).to_parquet(out)
    return kind, c, f"{len(df)} rows {df.index[0]}..{df.index[-1]}"


if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    jobs = [(k, c) for k in ("spot1h", "perp1d", "funding") for c in CANDS]
    with cf.ThreadPoolExecutor(16) as ex:
        for k, c, msg in ex.map(lambda a: job(*a), jobs):
            print(k, c, msg, flush=True)
