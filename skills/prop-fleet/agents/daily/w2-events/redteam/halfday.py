import sys; sys.path.insert(0, '.')
import pandas as pd, loaders as L
s = L.load_spy(); r = L.rth(s)
tr = pd.read_csv(L.SCR / "e2_trades.csv", parse_dates=["date"])
hd = ["2019-07-03","2019-11-29","2019-12-24","2020-11-27","2020-12-24","2021-11-26","2022-11-25","2023-07-03","2023-11-24","2024-07-03","2024-11-29","2024-12-24"]
for d in hd:
    x = r[r.date == pd.Timestamp(d).date()]
    pre = x.between_time("09:30","12:59").v.mean(); post = x.between_time("13:00","15:59")
    t = tr[(tr.date == d) & (tr.market == "SPY")].variant.tolist()
    print(d, len(x), "vol/bar pre13", int(pre), "post13 bars", len(post), "vol/bar", int(post.v.mean()) if len(post) else 0, "SPY trades:", t)
