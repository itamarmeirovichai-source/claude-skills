# Automation route — engineer, 2026-10-05

Inputs: `rules_keeper/rules_matrix.csv` and `redteam/automation_evidence.txt` (today), and
`lib_probe.txt` (PyPI, GitHub raw and package introspection, run today). Every firm fact here
is a search-snippet claim that still needs checking, not a fact. No firm page or vendor doc host could be fetched.

## Tests
`scripts/`: 470 passed and 0 failed across 22 test files (`pytest_run.txt`). I changed no script.
Today's `data_hunter/test_data_fetch_more.py` passed 4 of 4. The new `engineer/test_broker_contract.py` passed 17 of 17
with the library venvs present, and 15 passed with 2 skipped without them.

## API per allowed firm
| Firm | Tier | API | Status from today's evidence |
|---|---|---|---|
| Bulenox | A | Rithmic protobuf (async-rithmic) | Bots are allowed only if user-built. Third-party algos need approval. +$100/mo for a third-party Rithmic API connection (FAQ snippet). "DTC Protocol Bridge API" is banned (red team). |
| Lucid | A | Rithmic (async-rithmic). Its CQG/Tradovate side has no stated API | The support page permits automation, but the agreement requires PRIOR WRITTEN APPROVAL (red team, conflict) |
| Topstep XFA | B | ProjectX Gateway (project-x-py) | Allowed on XFA. No API on Live, and call-up closes all XFAs. No VPS. |
| Tradeify | hold | Rithmic. Tradovate API is Live-only | Bans running the same bot at other firms, which is incompatible with a multi-firm fleet |
| MFFU | hold | Rithmic or Tradovate via platforms. No API statement | Firm text and third parties conflict on human oversight |

**Tradovate is not a route.** Tradeify's help center says its API serves only live accounts,
and the only PyPI client (`tradovate` 0.0.1) is a 2022 data stub. Two adapters cover every
eligible firm: **Rithmic** (Bulenox, Lucid, and Tradeify/MFFU if they come off hold) and
**ProjectX** (Topstep XFA).

## What the bot (IBKR only today) would need
1. **A `Broker` interface** with accounts, positions, place_bracket, cancel_all and flatten_all, plus
   fill and heartbeat streams. IBKR becomes one implementation of it. The draft is in `broker_contract.py`.
2. **Two processes, not one.** project-x-py 4.4.0 and async-rithmic 1.6.6 are *unsatisfiable
   in one environment*: websockets <15 conflicts with pysignalr's websockets ≥15.0.1 (uv resolver, today).
   Each adapter runs in its own venv as a small service, and the strategy core talks to both over a local queue.
   ProjectX also needs Python ≥3.12. 3.12 and 3.13 are on this machine, and the repo tests run on 3.11.
3. **An exact translation layer**, the part that is easiest to get wrong:
   - Side encodings differ: ProjectX BUY=0/SELL=1, Rithmic BUY=1/SELL=2.
   - ProjectX brackets take absolute prices. Rithmic brackets take relative `stop_ticks`/`target_ticks`.
   - Prices must sit on the 0.25 grid (all 11,580 sampled ES/NQ prices do).
   - Contracts are integers. There is no ETF→futures ratio, which was the old proxy-bug path.
4. **Rithmic orders flagged AUTO.** async-rithmic defaults `manual_or_auto` to MANUAL (1).
   A bot that sends orders tagged MANUAL would misdeclare itself, so the adapter must set AUTO (2).
   A test now pins this.
5. **A per-account risk guard before every order.** It enforces the firm's DD/DLL, max contracts and the
   flat-by time: Topstep 3:10 PM CT, Bulenox 3:59 PM CT, Lucid sim 4:45 PM ET (rules_matrix).
   It also handles flatten-on-disconnect and a kill switch.
6. **Fan-out with reconciliation.** One signal becomes N independent orders, and fills are checked
   against intent for each account. Note that Topstep and Lucid ban "coordinated trading" across
   unconnected accounts (red team). Whether that wording covers one person's own accounts at two firms
   is a written question for Itamar.
7. **Ops.** The bot runs on Itamar's own computer, because Topstep forbids VPS. Credentials come from
   env/keychain. It sends alerts.

## Gating items outside engineering (only Itamar can act; nothing was sent)
- Rithmic production gateway URLs require passing Rithmic's **conformance test** (async_rithmic
  docs/connection.rst). Only the test gateway example is public. rithmic.com is blocked from here.
- Written approval at Lucid, and at Bulenox if a self-built program counts as "third-party".
- A ProjectX API subscription (~$29/mo, third-party figure).

## Smallest first step (done today, offline)
`engineer/broker_contract.py` and `test_broker_contract.py`: the broker-neutral `BracketIntent`,
plus validated translators to ProjectX `place_bracket_order` kwargs and Rithmic `submit_order` kwargs.
Two of the tests check those kwargs against the real installed library signatures, with no network and
no account. **Next:** once the bot repo is attached, port the contract plus tests into it as a PR, then
write a fake-gateway test of the ProjectX adapter. The Rithmic adapter comes second, after conformance.
**No live adapter is built before a strategy passes the gate.**
