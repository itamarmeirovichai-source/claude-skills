# Automation route — engineer, 2026-10-04

Sources: agents/daily/2026-10-04/rules_matrix.csv (today's rules worker), PyPI JSON API,
GitHub raw READMEs of project-x-py and async_rithmic. Vendor doc hosts were
EGRESS_BLOCKED from here: gateway.docs.projectx.com, api.topstepx.com, api.tradovate.com,
www.rithmic.com (proxy CONNECT 403). Every firm fact below is a claim to verify.

## Which API per allowed firm
| Firm | API the bot would speak | Note |
|---|---|---|
| Topstep (Express Funded) | ProjectX Gateway (REST https://api.topstepx.com/api + SignalR hubs rtc.topstepx.com) | API not on Live Funded; VPS prohibited, own device only; ~$29/mo (third party) |
| Bulenox | Rithmic (Protocol Buffer API) | Rithmic only; +$100/mo for third-party Rithmic API connection; one Rithmic user id, 5 Master accts |
| Lucid | Rithmic (or Tradovate) | firm publishes Rithmic setup + copier guides |
| Tradeify | Rithmic only in practice | help-center: Tradovate API is LIVE accounts only; ProjectX dropped |
| MyFundedFutures | ProjectX or Rithmic (third party) | automation rule conflicting across sources; verify first |

Tradovate is not a route: the only firm-side statement found says its API serves live
accounts only. Two adapters cover all five firms: ProjectX (Topstep, maybe MFFU) and
Rithmic (Bulenox, Lucid, Tradeify, maybe MFFU).

## Libraries (PyPI, checked today)
- project-x-py 4.4.0, MIT — async ProjectX SDK; env PROJECT_X_API_KEY / PROJECT_X_USERNAME;
  native gateway brackets on place_order, SignalR user/market hubs, multi-account.
- async-rithmic 1.6.6, MIT — Rithmic protobuf API, auto-reconnect/retry; README says it does
  not handle failure handling or correctness under load.
- tradovate 0.0.1 (2022) — data only, not usable.
- bot today: IBKR (ib_insync 0.9.86 last release 2023; maintained fork ib_async 2.1.0).

## What the bot needs (bot repo not attached — these are proposals)
1. A Broker interface behind which IBKR becomes one implementation: connect, account list,
   positions, place_bracket(symbol, side, qty, entry, stop, target), cancel, flatten_all,
   fills stream, heartbeat.
2. Native-futures orders: MES/ES (MNQ/NQ) contract ids and roll, size in contracts. No
   ETF->futures ratio conversion (the defect-1 / proxy-bug path in references/schedule.md).
   Signals computed on ES bars in R already map directly.
3. Per-account risk guard enforcing each firm's rule locally (EOD/trailing DD, DLL,
   consistency, news blackout, max contracts) before every order, plus flatten-before-close.
4. Fan-out: one signal -> N accounts as N independent orders (own accounts, same direction,
   which Topstep/Tradeify/Lucid/MFFU say is permitted), with per-account reconciliation of
   fills vs intended and a kill switch.
5. Ops: runs on Itamar's own computer (Topstep forbids VPS; Tradeify forbids VPS login),
   credentials from env/keychain, alert on disconnect.

## Smallest first step
Offline, no account, no money: add the Broker interface and a ProjectX adapter built on
project-x-py, tested against a recorded/fake gateway (pytest, no network), with one test
proving a bracket for MES built from (entry, stop, target in ES points, 1 contract) is sent
with exact prices and size — the test that would have caught the proxy bug. Needs the bot
repository attached to this session; until then it is a proposal. Rithmic adapter second
(async-rithmic), since it covers three firms but likely requires Rithmic conformance
approval and a paid API add-on (unverified; rithmic.com blocked).
