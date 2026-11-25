# NEWS-1 — pre-registration

Written on 2026-11-25, **before the stock list was built and before any signal was recorded**. The commit
history of this file is the evidence of that order. Nothing below may change while the experiment runs.

> Paper experiment on public data. No broker, no orders, no keys, no real money. Not advice and not a
> forecast. The expected outcome is that the idea fails; the purpose is a clear answer.

## Question

Does a language model reading overnight company headlines predict the **same-day open-to-close return** of
liquid US stocks, after costs?

## Why only forward in time

A model may remember what happened to a stock after an old headline, so a test on past news can look
excellent with no forecasting ability at all (Glasserman & Lin 2023, arXiv:2309.17322). Only signals written
to the log before the market opens count. There is no backtest and none will be added.

## Fixed design

| Item | Value |
|---|---|
| Universe | 120 US common stocks, frozen in `universe.json`, built once right after this commit |
| Universe rule | Nasdaq stock list: country United States, name contains "Common Stock" or "Common Shares", no warrants, units, rights, preferred, depositary shares or notes, symbol of 1–5 letters, price ≥ $5, latest-day dollar volume ≥ $25M. Candidates are put in the order of `sha256("NEWS-1/2026-11-25:" + symbol)` and accepted while their 20-day average dollar volume is ≥ $25M and last close ≥ $5, until 120 are accepted |
| Universe changes | None. A stock that stops trading simply produces no signals. No replacements |
| News source | Yahoo Finance search endpoint (public, keyless, unofficial). Only items whose related tickers include the stock |
| News window | 16:00 ET on the previous trading day to 09:00 ET on the signal day, or to the fetch time if earlier |
| Headlines per stock | The 3 newest in the window. A stock with none gets no signal |
| Scoring | One verdict per stock (1 good, −1 bad, 0 unclear) using the text in `PROMPT.txt`, sha256 `ef552a5bf493cc4400b46441ed376d7f0efce3538c86e85af97559bf186e7ef7` |
| Scorer | The Claude model serving the runner session. Its identifier is recorded with every day's batch. If the model changes, results are also reported per model |
| Trade (simulated) | 1 = long, −1 = short, from the day's opening price to its closing price (daily bar), equal weight across that day's non-zero verdicts. Verdict 0 is logged and not traded |
| Costs | 5 basis points per side. Also reported at 2.5 and 10 |
| Deadline | The log refuses a day's signals from 09:25 ET. One batch per day. The push time of the commit is a second, independent timestamp |
| Missed days | A day with no run, or a failed fetch, has no signals. Nothing is ever filled in afterwards |
| Missing prices | A signal whose stock has no daily bar that day is excluded and counted |

## Metric and decisions

- **Primary metric:** the mean daily net return of the long-short book, over days with at least one trade,
  with a t-statistic on the daily series.
- **Stage 1 — the first 60 such days.** If the mean net return at 5 bp per side is ≤ 0, the idea is
  **closed**. No changes, no second version, no "it almost worked".
- **Stage 2 — only if stage 1 is positive.** Continue unchanged to 250 days. The idea passes only if
  t ≥ 3.68 over those 250 days. This is test number 302 in the owner's quant-edge ledger, and 3.68 is that
  ledger's bar.
- **Real money:** not considered before stage 2 passes, and the owner cannot hold a brokerage account before
  the age of 18 in any case.

## What will not be done

No change of prompt, universe, window, costs or thresholds. No filtering of results by sector, verdict side,
weekday or model after the fact, except as a labelled, non-deciding description. No rescue variants. No
selective exclusion of days.

## Known limits, stated in advance

| Limit | Direction of the error |
|---|---|
| Our orders do not move the opening or closing price | Favourable |
| Shorts are assumed always available, with no borrowing cost | Favourable |
| The daily bar's open and close can differ slightly from the primary exchange's auction prices | Either way |
| Headline timestamps come from the provider and can lag the original publication | Unfavourable (news is older than it looks) |
| The scoring model can be updated by its provider during the experiment | Unknown |
| Same-day trades are correlated; the daily series, not single trades, is the unit of analysis | Handled |
| The provider's endpoint is unofficial and may fail on some days | Fewer days, no bias |

## Differences from the plan first described to the owner (chat, 2026-11-23)

Ticker-tagged press-release feeds turned out to be unreachable from the cloud environment (HTTP 403), so the
design uses a per-stock headline source. Consequences, all decided before any data: a fixed sample of 120
stocks instead of the whole liquid market; one verdict from up to 3 headlines instead of the first item per
stock; no cap of 20 trades a day, because the unit of analysis is the daily book.

## Prior and literature

The honest prior is low (the author's estimate: under 10%). Lopez-Lira & Tang (arXiv:2304.07619) report that
such signals predicted next-day returns, but also that returns fall as model use spreads and that only
participants with very low costs can exploit them. FINSABER (arXiv:2505.07078) finds that reported
advantages of language-model strategies often vanish under broader evaluation.
