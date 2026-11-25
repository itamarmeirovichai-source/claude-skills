# NEWS-1

A forward-only **paper** experiment: does a language model reading overnight company headlines predict the
same-day return of liquid US stocks after costs? The rules were fixed in advance in
[PREREGISTRATION.md](PREREGISTRATION.md).

> Read-only public data. No broker, no orders, no keys, no real money. Not advice. The expected outcome is
> that the idea fails.

## Commands

Run from this folder. Python 3.11 or newer; standard library only.

| Command | What it does | Network |
|---|---|---|
| `python -m news1 open-fetch` | Fetch today's headlines for the 120 stocks and print them for scoring. Records nothing | read-only |
| `python -m news1 record <verdicts.json> --model <id>` | Write today's verdicts to the log. Refused from 09:25 ET, on closed days, twice a day, or if a stock is missing | none |
| `python -m news1 settle` | Open-to-close returns for finished days, then the running statistics | read-only |
| `python -m news1 status` | Running statistics and the stage decision | none |
| `python -m news1 verify` | Check the log's hash chain | none |
| `python -m news1 build-universe` | Build the frozen stock list. Refused once `universe.json` exists | read-only |

## Daily run (for the scheduled session)

Follow exactly. Change no file other than the two data files. On any refusal or error: stop and report it;
do not work around it.

1. `python -m news1 verify`, then `python -m news1 settle`.
2. `python -m news1 open-fetch`. If it is refused because the market is closed, stop here.
3. Score the headlines it printed using the text of `PROMPT.txt` and nothing else. Save the JSON object to
   `data/pending/<date>.verdicts.json`.
4. `python -m news1 record data/pending/<date>.verdicts.json --model <model id of this session>`.
5. Commit `data/ledger.jsonl` and `data/results.jsonl` with the message `NEWS-1 <date>` and push.
6. Report in one line: signals recorded, trades settled, and the decision line from `status`.

## Files

| File | Purpose |
|---|---|
| `PREREGISTRATION.md` | The fixed design, metric and decisions |
| `PROMPT.txt` | The fixed scoring instruction |
| `universe.json` | The frozen stock list |
| `data/ledger.jsonl` | Append-only, hash-chained log of every day's batch and signals. Headline text is not stored, only identifiers and links |
| `data/results.jsonl` | Settled open-to-close returns (derived from public prices) |
| `news1/` | Source. `tests/` holds 26 tests, including refusals after the deadline |

## Safety properties

| Property | Enforced by |
|---|---|
| Read-only: the client can only send HTTPS GET requests | `news1/http.py`; test |
| No keys, orders or third-party packages | source scan and import allowlist in the tests |
| No look-ahead | news window ends at 09:00 ET; the log refuses signals from 09:25 ET, for another day, or twice a day; tests |
| Tamper-evident history | hash chain; test edits and deletes lines |
| No silent omissions | every stock with headlines must get a verdict; zeros are logged |
