"""H0018 stage 1b: classify officer/director open-market purchases as routine vs opportunistic
(Cohen-Malloy-Pomorski 2012, rule as pre-registered in ledger.csv row H0018).
Fixed implementation choices (set before any return was computed):
 - Form 4 only (DOCUMENT_TYPE == "4", amendments ignored), non-derivative table.
 - "Traded" for the routine test = any open-market purchase (P) or sale (S) by the same reporting
   owner (RPTOWNERCIK), in any issuer, dated by TRANS_DATE.
 - Routine = owner traded in the same calendar month (of the purchase's TRANS_DATE) in each of the
   3 prior calendar years. Everything else = opportunistic.
 - Purchase = TRANS_CODE P and acquired (A); owner relationship contains Officer or Director.
 - Trade year >= 2009 (so all 3 look-back years are inside the 2006+ data).
 - Signal month = month of FILING_DATE. Ticker = ISSUERTRADINGSYMBOL, upper-cased, stripped.
Usage: python -I build_signals.py <sec_ps.parquet> <out_csv>"""
import sys, pandas as pd
df = pd.read_parquet(sys.argv[1]).dropna(subset=["TRANS_DATE", "FILING_DATE"])
df["y"], df["m"] = df.TRANS_DATE.dt.year, df.TRANS_DATE.dt.month
hist = set(zip(df.RPTOWNERCIK, df.y, df.m))
rel = df.RPTOWNER_RELATIONSHIP.fillna("")
b = df[(df.TRANS_CODE == "P") & (df.TRANS_ACQUIRED_DISP_CD == "A") &
       rel.str.contains("Officer|Director") & (df.y >= 2009)].copy()
b["routine"] = [all((o, y - k, m) in hist for k in (1, 2, 3)) for o, y, m in zip(b.RPTOWNERCIK, b.y, b.m)]
b["ticker"] = b.ISSUERTRADINGSYMBOL.fillna("").str.upper().str.strip().str.replace(".", "-", regex=False)
bad = b.ticker.isin(["", "NONE", "N/A", "NA", "NULL"]) | b.ticker.str.contains(r"[^A-Z0-9\-]")
b = b[~bad]
b["sig_month"] = b.FILING_DATE.dt.to_period("M")
g = b.groupby(["sig_month", "ticker", "routine"]).agg(
    first_filing=("FILING_DATE", "min"), n_trades=("ACCESSION_NUMBER", "size"),
    med_px=("TRANS_PRICEPERSHARE", "median"),
    dollars=("TRANS_SHARES", lambda s: (s * b.loc[s.index, "TRANS_PRICEPERSHARE"]).sum()),
    issuer_cik=("ISSUERCIK", "first")).reset_index()
g.to_csv(sys.argv[2], index=False)
print("purchase rows", len(b), "| routine share", round(b.routine.mean(), 3))
print(g.groupby("routine").ticker.nunique().rename("unique tickers"))
