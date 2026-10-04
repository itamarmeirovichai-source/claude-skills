# PumpWatch

Early-warning engine for social-media-driven **pump-and-dump** stock schemes.
It never needs access to private chats. It looks for the footprints a pump
has to leave in public or customer-owned data, and only alerts when several
independent footprints line up.

> **Status: v0.1, research prototype.** The engine, scoring, audit log and
> backtest are built and tested. **It has not yet been measured on real
> cases.** Synthetic results only prove the plumbing works. See `PLAN.md`
> for the go/no-go gates.

## The seven footprints

| Signal | Family | What it looks for |
|---|---|---|
| S1 abnormal volume | market | Dollar volume many times its 60-day median with **no** news filing to explain it |
| S2 quiet accumulation | market | Steady climb on rising volume with no single big jump (the promoters buying) |
| S3 suspicious filings | corporate | New-share registrations, name or control changes, a dormant shell waking up |
| S4 hype burst | social | Mentions far above normal **and** the messages read like promotion |
| S5 coordinated promotion | social | Near-identical messages from several different accounts |
| S6 broker flow | client | Many new, small, first-time micro-cap buyers (customer data, under contract) |
| S7 victim reports | client | Consent-based user reports naming the ticker |

**Alert rule:** risk score ≥ threshold **and** evidence from at least two
independent families. One loud signal on its own is what real news looks
like, so it never alerts by itself. Families without data are left out of
the score instead of counting as zero.

## Guarantees (each enforced by a test)

- **No look-ahead.** A day's score never uses data dated after that day.
- **Explainable.** Every alert lists the exact evidence behind it.
- **Tamper-evident.** Alerts can be written to a hash-chained audit log, and
  `verify-log` detects any edit, deletion or reordering.
- **Honest backtest.** The threshold is chosen on a calibration half of the
  cases and scored on a holdout half it never saw. A pump counts as caught
  only if the alert came **before** the collapse.

## Quick start

```bash
cd pumpwatch
python -m pip install -e ".[dev]"     # or: export PYTHONPATH=src
python -m pytest -q                   # run the tests
pumpwatch demo --out out/demo          # synthetic market + backtest report
pumpwatch scan out/demo/data --log out/audit.jsonl
pumpwatch verify-log out/audit.jsonl
pumpwatch backtest DATA_DIR data/cases.csv --out out/report.md
```

## Data directory format

Plain CSV files (only `bars.csv` is required):

| file | columns |
|---|---|
| `bars.csv` | ticker, day, open, high, low, close, volume |
| `filings.csv` | ticker, day, form, title |
| `posts.csv` | source, author, day, text, [tickers] |
| `broker_flow.csv` | ticker, day, new_buyers, first_time_microcap_buyers |
| `reports.csv` | ticker, day, note |

Cases for a backtest: `ticker, label (pump|legit), start, end, note`.
A template is in `data/cases_template.csv`.

## Data rules (red lines)

- Public sources and official APIs only. No fake identities to join private
  groups, no WhatsApp scraping, no buying access to private groups.
- Authors are stored as opaque ids. Keep personal data to the minimum.
- **Never trade on the alerts.** The product is the warning.

## Layout

```
src/pumpwatch/
  models.py      data records
  context.py     per-ticker view with no-look-ahead helpers
  text.py        cashtags, hype language, near-duplicate clustering
  signals/       S1–S7
  engine.py      scoring, convergence rule, alerts
  backtest.py    calibration/holdout evaluation and report
  audit.py       hash-chained alert log
  io.py          CSV data directory load/save
  synth.py       synthetic market for plumbing tests
  cli.py         command line
```
