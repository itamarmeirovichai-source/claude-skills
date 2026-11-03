# Brief: Connectivity Engineer, week 1 — IBKR afternoon disconnects and the 32-minute data lag (output: quant-edge/engineering/)

Context: Itamar's live bot (ICT/SMC "TJR" on NQ through Interactive Brokers, Python, 300-second scan, Telegram alerts, daily email; described in
`~/quant-edge-inherited/pr4/skills/prop-fleet/SKILL.md` and `references/email.md`, grep for Gateway, disconnect, reconnect, farm, 2FA) drops its connection
every afternoon Israel time and once delivered data 32 minutes late. The bot repository is NOT attached to this session; nothing on his PC can be touched.
Deliverable: a document he applies himself, plus scripts he runs himself. No change is proposed without a measurement first.

Write `quant-edge/engineering/ibkr-connectivity-diagnosis.md`: (1) Hebrew step-by-step for Itamar (≤ 1 page): what to run for five sessions, where the log
lands, what to send back; (2) English technical appendix: the measurement plan (log every disconnect/reconnect, error codes 1100/1101/1102/2103/2104/2105/
2106/2108/2110/2158 with UTC and Israel timestamps; IBKR reset windows converted to Israel time: North America 00:15–01:45 ET, Europe 06:25–07:45 CET,
Saturday 00:00–02:00 ET, none in an Israeli afternoon; the Gateway's configured auto-restart / auto-logoff time; host sleep, Windows/macOS update and network
events; 2FA re-authentication prompts; the data-farm disconnect messages that are NOT connection losses); the decision tree (one setting changed at a time,
re-measured); the recommendation to run the Gateway under IBC with auto-restart and IB Key auto re-authentication; the stale-data rule for the bot (no new
order if the last bar is older than twice the scan interval or the clock offset exceeds 500 ms; NTP check); a reconnect-and-reconcile sequence (positions and
open orders re-read from the broker before any signal). Write `quant-edge/engineering/ibkr_watchdog.py`: a stand-alone read-only logger using `ib_insync`
(or `ibapi`) that connects to a paper or live Gateway on a port he sets, subscribes to connection events and `error` callbacks, logs them with both clocks
to a CSV, measures the age of the last 1-minute NQ bar every 60 s, and never places an order; with a `--selftest` mode that runs without a Gateway.
Also write `quant-edge/engineering/bot-patch-plan.md`: the smallest set of changes to his bot for IBC, reconnect handling and the stale-data rule, as a
patch plan to become a pull request when the repository is attached. Read first: `quant-edge/briefs/00-common.md`, `WORK-LOG.md`. Web: IBKR's own pages
on reset times, Gateway settings and IBC documentation (URL + fetch date). Hebrew for the user-facing page, English elsewhere. Do not commit.
