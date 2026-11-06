# IBKR connectivity diagnosis: afternoon disconnects and the 32-minute data lag

Department G (Connectivity Engineer), 2026-11-06. Nothing here has been applied to Itamar's PC, IBKR account or bot.
Itamar applies every step himself. No setting is changed before five sessions have been measured.

---

## חלק 1: מה לעשות (לאיתמר, עמוד אחד)

**המטרה:** לפני שמשנים משהו, למדוד חמישה ימי מסחר. כל ניתוק נרשם, עם שעון ישראל ושעון ניו יורק, ואז מתאימים אותו לסיבה.

**התקנה, פעם אחת (5 דקות):**
1. מעתיקים את `quant-edge/engineering/ibkr_watchdog.py` לתיקייה חדשה במחשב, למשל `C:\ibkr-watchdog\`.
2. פותחים חלון פקודה בתיקייה ומריצים: `pip install ib_async`
3. בדיקה עצמית שלא צריכה Gateway: `python ibkr_watchdog.py --selftest`. צריך לראות בסוף `0 failed`.

**בכל יום מסחר, חמישה ימים ברצף:**
1. מפעילים את IB Gateway כרגיל ומתחברים.
2. בחלון פקודה נפרד: `python ibkr_watchdog.py --port 4002` (בחשבון אמיתי: `--port 4001`). משאירים את החלון פתוח כל היום, גם בזמן שהבוט רץ. הכלי **רק קורא**: הוא לא שולח, לא משנה ולא מבטל פקודות, ומתחבר עם מספר לקוח 917 כדי לא להתנגש בבוט.
3. בכל פעם שאתה נכנס ל-IBKR מהטלפון, מהאתר או מ-TWS, רשום את השעה בפתק. זה חשוד מספר אחת (פירוט בנספח).
4. בדוק פעם אחת: Gateway ← Configure ← Settings ← Lock and Exit. צלם את המסך: האם מסומן Auto restart או Auto logoff, ובאיזו שעה.
5. אם המחשב נכנס לשינה או התעדכן, רשום את השעה.
6. פעם אחת: פתח בדפדפן את https://www.interactivebrokers.com/en/software/systemStatus.php וצלם את טבלת שעות התחזוקה (מכאן הדף חסום, ורוצים לאמת את השעות).

**איפה הלוג:** קובץ `ibkr_watchdog_log.csv` באותה תיקייה. כל שורה: שעון UTC, שעון ישראל, שעון ניו יורק, סוג האירוע וקוד השגיאה.

**מה לשלוח בחזרה אחרי חמישה ימים:**
1. הקובץ `ibkr_watchdog_log.csv`.
2. הפלט של `python ibkr_watchdog.py --summary ibkr_watchdog_log.csv`.
3. צילום המסך של Lock and Exit, והפתק עם שעות הכניסה מהטלפון/אתר.
4. אם יש: לוג הבוט של אותם ימים (רק השורות עם disconnect/reconnect/error), ושורות לוג מה-Gateway מאותן שעות.

**מה לא לעשות בשבוע המדידה:** לא לשנות הגדרות, לא לעדכן את ה-Gateway, ולא להתקין IBC. משנים דבר אחד בכל פעם, ורק אחרי המדידה.

**מה כבר ידוע:** אף חלון תחזוקה של IBKR לא נופל אחר הצהריים בישראל. הם בבוקר (בערך 07:15–08:45). לכן הסיבה כמעט בטוח אצלנו ולא אצל IBKR. החשודים העיקריים: כניסה מהטלפון או מהאתר עם אותו שם משתמש, ההפעלה היומית של הבוט ב-16:20, והגדרת האתחול של ה-Gateway. העיכוב של 32 דקות מגיע כנראה ממקור הנתונים של הבוט (Yahoo דרך yfinance), לא מ-IBKR.

---

## Part 2: English technical appendix

### A. What the inherited record says (evidence, not assumptions)

| # | fact | source |
|---|---|---|
| E1 | The bot's **signal prices come from yfinance** (`data.feed.MarketDataFeed().get_ohlcv(symbol, "1h")`, a Yahoo continuous series); IBKR is used for orders. "the setups were recorded against yfinance's continuous series"; "if yfinance rolled early or late, that is what the bot saw". | `~/quant-edge-inherited/pr4/skills/prop-fleet/scripts/futures_bars.py` lines 15, 32–35, 118–130, 302–306 |
| E2 | The bot "fires at 9:20 each trading day, IBC brings the Gateway back after its nightly restart, and the daily report lands at 16:05" (New York time). 09:20 ET is **16:20 Israel** for most of the year and 15:20 Israel in the US-DST/Israel-winter gap weeks (zoneinfo, see C). | `references/schedule.md` line 343; `references/email.md` "16:20 שעון ניו יורק" |
| E3 | IBKR order ids restart after a Gateway restart: trades 57 and 58 share `broker_order_id = 98`. Any reconcile keyed on order id alone is wrong. | `references/schedule.md` lines 450–452 |
| E4 | The bot connects to the paper Gateway on port 4002; inherited scripts use clientId 77 and `ib_async` → `ib_insync` fallback. | `scripts/futures_bars.py` lines 70–71, 325–341 |
| E5 | An earlier price-drift diagnosis found a stale source of the "cache whose TTL never expires or whose refresh fails silently" type (a 15-day lag), i.e. the feed layer has silently served old data before. | `SKILL.md` lines 238–256, 300–345 |
| E6 | The bot itself wakes every 300 s and reads one price; it never sees the bar. | `SKILL.md` lines 384–390 |

The bot repository is not attached to this session; `broker/ibkr.py`, `data/feed.py` and the bot's logs were not read.
Every statement about the bot below is therefore a hypothesis to be confirmed by the measurement.

### B. IBKR's own documentation (fetched 2026-11-06)

| topic | what it says | URL | status |
|---|---|---|---|
| message codes | 1100 "Connectivity between IB and the TWS has been lost" — "can occur because of an internet connectivity issue, a nightly reset of the IB servers, or a competing session." 1101 restored, data lost; 1102 restored, data maintained; 2103 "A market data farm is disconnected" — "Outside of the nightly IB server reset, this typically indicates an underlying ISP connectivity issue"; 2104 farm OK; 2105/2106 historical farm down/up; 2107/2108 farm "inactive but should be available upon demand"; 2110 "Connectivity between TWS and server is broken. It will be restored automatically" — "usually only occur during the IB nightly server reset"; 2158 "Sec-def data farm connection is OK"; 326 client id already in use; 10197 "No market data during competing session"; intro: "You are very likely to loose connectivity to our servers at least once a day due to our daily server maintenance downtime". | https://interactivebrokers.github.io/tws-api/message_codes.html (IBKR's deprecated-but-live API page) | verified (fetched) |
| reset windows | Brief values: North America 00:15–01:45 ET, Europe 06:25–07:45 CET, Saturday 00:00–02:00 ET. The live status page could not be read (see blocked hosts). Search snippets of IBKR pages: "during the Friday evening reset period, all services will be unavailable in all regions"; the Web API (Client Portal) resets differ ("approximately 0100 local time by region") and do **not** apply to the Gateway socket API. | https://www.interactivebrokers.com/en/software/systemStatus.php ; https://www.interactivebrokers.com/docs/web-api/trading/usage-and-availability/scheduled-server-maintenance | snippet only (403 to fetch) |
| Gateway auto-restart | "In TWS/ IB Gateway – 'Global Configuration' – 'Lock and Exit', you can choose the time of your TWS being shut down"; API users should choose "Never lock" and "Auto restart"; auto-logoff "shuts down TWS completely at the specified time"; "the weekly authentication cycle starts on every Monday". | https://www.interactivebrokers.com/docs/tws-api/doc/tws-settings/daily-weekly-reauthentication | snippet only (403 to fetch) |
| one session per username | "Only a single active brokerage session can exist for any username across all IBKR services"; a second username is the documented way to use TWS / IBKR Mobile / Client Portal at the same time. | https://www.interactivebrokers.com/docs/web-api/authentication/multiple-sessions | snippet only (403 to fetch) |
| IBC user guide | auto-restart "allows TWS or Gateway to automatically restart each day without need for repeated authentication" (IBC ≥ 3.15.0, `AutoRestart` in Lock and Exit); "authentication is only required the first time during the week that TWS or Gateway run after 01:00 ET on Sunday"; on Sunday "IB will prevent that session running any further because the session credentials expire"; `ExistingSessionDetectedAction=primaryoverride` for when IBKR Mobile or Client Portal "causes your TWS/Gateway session to be shut down"; Windows: Task Scheduler runs `StartGateway.bat` with `/INLINE`, "Run only when user is logged on"; the self-updating TWS does not work with IBC, use the offline installer; 2FA window "currently 3 minutes". | https://github.com/IbcAlpha/IBC/blob/master/userguide.md | verified (fetched) |
| IBC config.ini | `ExistingSessionDetectedAction` default `manual` (values primary / primaryoverride / secondary / manual); `ReloginAfterSecondFactorAuthenticationTimeout` default `no`; `SecondFactorAuthenticationTimeout` 180 s; `SecondFactorAuthenticationExitInterval` 60 s; `AutoRestartTime` "HH:MM AM/PM"; `ColdRestartTime` "a time in your local timezone that is after 01:00 US/Eastern" (Sundays); `AcceptIncomingConnectionAction` default `manual`, `reject` + IP allow-list recommended; `ReadOnlyApi`; `TradingMode` live/paper; `CommandServerPort` 0 = off. | https://raw.githubusercontent.com/IbcAlpha/IBC/master/resources/config.ini | verified (fetched) |
| IBC release | latest 3.24.2 ("21 Aug", year not shown), supports TWS/Gateway "10.48 onwards". | https://github.com/IbcAlpha/IBC/releases | verified (fetched) |
| Yahoo delay | CME and CBOT futures on Yahoo: **10 min delay** (ICE Data Services); NYMEX/COMEX 30 min. | https://help.yahoo.com/kb/SLN2310.html | verified (fetched) |
| ib_async | PyPI `ib_async` 2.1.0, uploaded 2025-12-08, Python ≥ 3.10 (ib_insync's repository was archived in March 2024, search snippet of github.com/erdewit/ib_insync issue 413). | https://pypi.org/pypi/ib_async/json | verified (fetched) |

**Blocked hosts (reported, not routed around):** WebFetch to `www.interactivebrokers.com` and `www.interactivebrokers.co.uk` returned HTTP 403 for the system-status page, the Web API maintenance pages, the TWS API system-codes page and the re-authentication page. A curl retry with a browser user agent was refused by this session's policy as bot-check circumvention and was not pursued. `www.timeanddate.com` returned 403; time-zone conversions were done with Python `zoneinfo` instead. **Action for Itamar (step 6 of the Hebrew page):** open https://www.interactivebrokers.com/en/software/systemStatus.php in a browser and photograph the reset table, so the windows can be marked verified.

### C. Reset windows in Israel time (Python zoneinfo, run 2026-11-06)

| window (own zone) | Israel, normal weeks | Israel, US-DST/Israel-winter gap (2027-03-14…03-26, 2027-10-31…11-07) |
|---|---|---|
| NA daily 00:15–01:45 ET | 07:15–08:45 | 06:15–07:45 |
| EU daily 06:25–07:45 CET | 07:25–08:45 | 07:25–08:45 (only 2027-03-26…03-27, Israel already on summer time and CET not yet: 08:25–09:45) |
| Saturday 00:00–02:00 ET | Sat 07:00–09:00 | Sat 06:00–08:00 |
| weekly session expiry after Sun 01:00 ET (IBC) | Sun 08:00 | Sun 07:00 |
| bot start 09:20 ET (E2) | **16:20** | 15:20 |
| US cash open 09:30 ET | 16:30 | 15:30 |

Offset changes 2026–2027 (zoneinfo): US 2026-03-08, 2026-11-01, 2027-03-14, 2027-11-07; Israel 2026-03-27, 2026-10-25, 2027-03-26, 2027-10-31.
**No IBKR reset window touches 12:00–20:00 Israel** (also asserted in `--selftest`). An afternoon disconnect is not IBKR's maintenance.

### D. Ranked hypotheses for the afternoon disconnect (what each predicts in the log)

| rank | hypothesis | evidence | what the watchdog log will show |
|---|---|---|---|
| H1 | **Competing session**: Itamar (or another app) logs in with the same username via IBKR Mobile, Client Portal or TWS around the US open; IBKR ends the Gateway's brokerage session. | IBKR: one brokerage session per username (B); 1100 note names "a competing session"; IBC's guide describes Mobile/Client Portal shutting the Gateway session down. The time of day (US open, 16:20–16:30 Israel) is when a trader checks the phone. | 1100 and/or 10197 within a minute of a login noted on the paper; Gateway shows "existing session detected" dialog; with `manual` the Gateway stays logged out until someone clicks. |
| H2 | **The bot's own daily start at 09:20 ET (16:20 Israel)**: the scheduled start launches a second instance or reconnects with a clientId still held (error 326), or the job restarts the Gateway itself. | E2 (fires 09:20 ET), E4 (fixed clientId). This is the one daily event in the record that lands in the Israeli afternoon. | 326 or `api_disconnected` of the bot's socket at 16:20 ± 2 min every trading day, while the watchdog's own socket (clientId 917) stays up and no 1100 appears. |
| H3 | **Gateway Lock-and-Exit time or IBC restart time set in the wrong zone**: the PC runs on Israel time; a time copied from an ET guide (e.g. "4:15 PM", "11:45 PM ET") or an `AutoRestartTime` entered as if ET lands in the Israeli afternoon. The Gateway restarts and every API client is dropped. | IBC config: times are local to the PC (`ColdRestartTime` "in your local timezone"); E2 says a nightly restart exists; the setting itself has not been seen. | `api_disconnected` for **both** the bot and the watchdog at the same minute every day, no 1100 before it, Gateway window restarts; matches the screenshot of Lock and Exit. |
| H4 | **Farm messages read as disconnects**: 2103/2105/2108 (farm inactive or down) are logged or alerted by the bot as "disconnected". 2108 inactivity is routine after quiet periods. | IBKR codes table (B): these are not connection losses. | `farm_notice` / 2103–2108 rows with no 1100 and no `api_disconnected`; bot alerts at the same minutes. |
| H5 | **Host events**: Windows sleep/hibernate, Windows Update restart, Wi-Fi power saving or ISP drop. | IBKR: 2103 outside reset = ISP. Not yet observed. | `host_gap` rows (tick > 90 s), or 2103/2105 then 1100 with ping loss; Windows Event Viewer System log entries (Kernel-Power 42/107, WindowsUpdateClient 19/43) at the same minute. |
| H6 | **2FA / weekly re-authentication** not completed after a restart (IB Key prompt missed, 3-minute window). | IBC guide (B). Predicts a Sunday/Monday or post-restart failure, not every afternoon. | Gateway at login screen; `connect_failed` 502 rows until a manual login. |

### E. The 32-minute data lag (one occurrence)

The bot's prices come from yfinance (E1), not from IBKR. Yahoo's own page lists CME futures at a **10-minute** delay (B), so the
floor of the bot's staleness is ~10 min plus the bar's own length (a 5-minute bar is stamped at its start) plus any cache or
retry in `data/feed.py` (E5: the feed has silently served old data before) and Yahoo's rate limiting (HTTP 429 recorded in
`references/insider-H0018.md` line 60). 32 min = 10 min exchange delay + one missed or cached refresh cycle is the simplest
reading, but it is a hypothesis: `data/feed.py` has not been read. The watchdog measures the IBKR 1-minute NQ bar age next to it,
which settles whether IBKR itself was ever late. If IBKR bars stay fresh (age < 120 s) while the bot reports a lag, the fix is the
data source, not the connection: the bot should read its bars from IBKR (requires the CME real-time market-data subscription on
the username that runs the bot; without it IBKR serves delayed data, code 10167) and must apply the stale-data rule (G) either way.

### F. Measurement plan (five sessions, nothing changed)

1. Run `ibkr_watchdog.py` beside the bot every trading day for five sessions, from before 16:00 Israel to after the US close (23:00 Israel). Own clientId 917, read-only.
2. Logged per row: UTC, Israel and New York timestamps; event (`api_connected`, `api_disconnected`, `ib_message`, `farm_notice`, `bar_age`, `clock_check`, `host_gap`, `connect_failed`); IBKR code, category, `connection_loss` flag; last 1-minute NQ bar time and age every 60 s; stale verdict; NTP offset every 10 min; the IBKR reset window, if any, the event falls in (±10 min).
3. Itamar notes by hand: each login on phone / web / TWS; the Lock-and-Exit screenshot (auto-restart vs auto-logoff, time); whether IBC is installed and its `config.ini` values for `AutoRestartTime`, `ExistingSessionDetectedAction`, `ReloginAfterSecondFactorAuthenticationTimeout`; sleep/updates.
4. Optional, Windows: export Event Viewer → System for the five days filtered to Kernel-Power, Power-Troubleshooter, WindowsUpdateClient, NDIS/Netwtw (Wi-Fi) events; `w32tm /query /status` once a day.
5. Bot side: the bot's own log lines for disconnect/reconnect/error with timestamps, and the Telegram alert times.

### G. Decision tree (one change at a time, each followed by ≥ 3 re-measured sessions)

1. Losses sit inside a reset window → expected; handle with reconnect-and-reconcile (H), no setting change.
2. 1100/10197 within ±2 min of a noted phone/web login → H1. Change: create a second IBKR username for the phone/web (IBKR's documented route; market data is billed per username), or stop logging in during the session. Under IBC, set `ExistingSessionDetectedAction=primary` on the Gateway so a secondary login cannot take it over. Re-measure.
3. Bot socket drops at 16:20 ± 2 min with the watchdog unaffected, or 326 → H2. Change the bot only (patch plan P2/P3): single-instance lock, unique clientId, connect once and stay connected. Re-measure.
4. Both sockets drop at the same minute daily with no 1100 → H3. Change: set Lock and Exit to **Auto restart** at a time inside the Israeli morning reset window (e.g. 07:30 Israel, i.e. inside 00:15–01:45 ET) and confirm the PC's time zone. Re-measure.
5. Only farm messages (2103–2108) → H4. Change the bot's classification (P4); no Gateway change.
6. `host_gap` rows or Event-Viewer sleep/update events → H5. Change: power plan "never sleep" while plugged in, Windows Update active hours 15:00–24:00 Israel, wired Ethernet or Wi-Fi power saving off. Re-measure.
7. Gateway waiting at login → H6. Change: IBC with `ReloginAfterSecondFactorAuthenticationTimeout=yes`, `TWOFA_TIMEOUT_ACTION=restart`, IB Key on the phone; accept one IB Key approval per week (Sunday after 01:00 ET = 08:00 Israel).
8. Nothing explains it → send logs + Gateway log files (`ibgateway\<version>\...\launcher.log` and the dated log in the Gateway settings directory) to IBKR's API support with the timestamps.

### H. Target configuration (after the measurement confirms it; recommended, not yet applied)

- **IB Gateway under IBC** (offline Gateway installer ≥ 10.48, IBC 3.24.x), started by Windows Task Scheduler (`StartGateway.bat /INLINE`, "Run only when user is logged on").
- Gateway Lock and Exit: **Auto restart** (not auto-logoff), at a time inside the morning reset (07:30 Israel).
- IBC `config.ini`: `TradingMode=paper` (or live), `ExistingSessionDetectedAction=primary`, `ReloginAfterSecondFactorAuthenticationTimeout=yes`, `AcceptIncomingConnectionAction=reject` with 127.0.0.1 in Trusted IPs, `CommandServerPort=0`; credentials only in IBC's config on his PC, never in the repository or chat.
- IB Key (IBKR Mobile) as second factor: one approval per week after the Sunday expiry.
- A second username for phone/web use while the bot runs.
- Clock: Windows time sync on (`w32tm /resync`), offset < 500 ms verified by the watchdog.

### I. Stale-data rule (for the bot)

No new order if **(a)** the last bar used for the signal is older than 2 × scan interval = **600 s**, or **(b)** |clock offset vs NTP| > **500 ms**, or **(c)** the connection state is not "connected and reconciled" (H/J). Age = now(UTC) − bar timestamp, using a tz-aware UTC timestamp from the data source (not the PC's local clock). Missing age or offset counts as stale. The rule blocks entries only; exits and the flat-by deadline keep running on the broker's position report. Implemented and tested in `ibkr_watchdog.py` (`stale_verdict`, `parse_ntp`).

### J. Reconnect-and-reconcile sequence

1. On 1100 / 2110 / `disconnectedEvent`: mark state `DISCONNECTED`; block new orders; do not cancel resting brackets (they live at IBKR); alert once (Telegram), not every scan.
2. Reconnect with backoff (5, 10, 20, 40, 60 s, then every 60 s), same unique clientId; on 326 wait 30 s and retry (another instance is alive — alert).
3. On 1102 (data maintained): re-check; on 1101 (data lost) or a fresh socket: re-subscribe every market-data and keepUpToDate request.
4. Before any signal: `reqPositions` → positions; `reqAllOpenOrders` / `openTrades()` → working orders; `reqExecutions` since session start → fills missed while down; compare with the bot's database **keyed by permId and conId, never by orderId** (E3); write a reconcile row; on mismatch alert and stay `HALTED` (no new orders) until a human looks.
5. Wait for one fresh bar (age < 600 s) and clock offset < 500 ms; state `READY`; resume scanning.
6. Log every transition with UTC and Israel timestamps (same CSV format as the watchdog).

### K. Files

- `quant-edge/engineering/ibkr_watchdog.py` — the logger; `--selftest` 26 checks, no Gateway needed (`python3 quant-edge/engineering/ibkr_watchdog.py --selftest` → "26 passed, 0 failed", run 2026-11-06 in this sandbox with no ib library installed).
- `quant-edge/engineering/bot-patch-plan.md` — the smallest bot changes, to become a pull request when the bot repository is attached.
