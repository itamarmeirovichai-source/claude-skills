"""H0018 stage 1a: download SEC Insider Transactions Data Sets (Form 3/4/5) quarterly zips
and extract the Form 4 non-derivative P/S rows we need into one compact parquet.
Usage: python -I fetch_sec.py <raw_dir> <out_parquet>"""
import sys, os, io, time, zipfile, requests, pandas as pd
UA = {"User-Agent": "prop-fleet research itamarmeirovichai@gmail.com"}
URL = "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{y}q{q}_form345.zip"
raw, out = sys.argv[1], sys.argv[2]
os.makedirs(raw, exist_ok=True)
frames, log = [], []
for y in range(2006, 2027):
    for q in range(1, 5):
        fn = os.path.join(raw, f"{y}q{q}.zip")
        if not os.path.exists(fn):
            r = requests.get(URL.format(y=y, q=q), headers=UA, timeout=120)
            time.sleep(0.3)
            if r.status_code != 200:
                log.append(f"{y}q{q}: HTTP {r.status_code}"); continue
            open(fn, "wb").write(r.content)
        z = zipfile.ZipFile(fn)
        rd = lambda n, cols: pd.read_csv(z.open(n), sep="\t", dtype=str, usecols=cols, quoting=3, on_bad_lines="skip")
        sub = rd("SUBMISSION.tsv", ["ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE", "ISSUERCIK", "ISSUERTRADINGSYMBOL"])
        sub = sub[sub.DOCUMENT_TYPE == "4"]
        own = rd("REPORTINGOWNER.tsv", ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNER_RELATIONSHIP"])
        # multi-owner filings: keep each owner (same transaction counted once per issuer-month later anyway)
        tr = rd("NONDERIV_TRANS.tsv", ["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES",
                                       "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"])
        tr = tr[tr.TRANS_CODE.isin(["P", "S"])]
        m = tr.merge(sub, on="ACCESSION_NUMBER").merge(own, on="ACCESSION_NUMBER")
        frames.append(m); log.append(f"{y}q{q}: {len(m)} P/S rows")
        print(log[-1], flush=True)
        os.remove(fn)  # keep disk small; parquet holds what we need
df = pd.concat(frames, ignore_index=True)
for c in ["FILING_DATE", "TRANS_DATE"]:
    df[c] = pd.to_datetime(df[c], format="%d-%b-%Y", errors="coerce")
for c in ["TRANS_SHARES", "TRANS_PRICEPERSHARE"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df.to_parquet(out)
open(out + ".log", "w").write("\n".join(log))
print("rows", len(df))
