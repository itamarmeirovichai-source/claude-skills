# Public Social Data Access: legal paths per platform

**Status / confidence:** DRAFT for legal review. Confidence is **high** for the quoted clauses below, because each one was copied from the official page opened today. It is **medium** for prices and rate limits, which change often and sometimes only show inside developer consoles. It is **low** wherever a line is marked **UNVERIFIED**. **This is not legal advice.** Section 13 lists the questions for our lawyer.

**Checked on 2026-10-04 via live web access.** Quotes are copied verbatim from the official pages. Each source line gives its check date (all 2026-10-04) and, where the page shows one, its "last updated" date. A few official pages blocked automated fetching (HTTP 403/503). For those I read the same article through the platform's public help-centre JSON API or its official GitHub docs repository, and I say so next to the quote.

Owner: Team Lead (B) Public Social Data Access, Detection Science.
Scope: the S4 signal (sudden mention spikes with hype language) and the S5 signal (identical wording, and the same accounts promoting ticker after ticker). See `RESEARCH.md` §2. Our ingestion record is `Post(source, author=opaque id, day, text, tickers)`, defined in `src/pumpwatch/models.py`.

---

## 0. Bottom line (read this first)

1. **No platform gives us a free, clearly-licensed, commercial right to monitor users and sell alerts about them.** Every major platform's terms contain at least one clause that hits PumpWatch's core use case. The clauses are about surveillance or tracking users, about inferring a "crime", about commercialising the data, or about ML. **Before production, every source needs written permission or a lawyer's sign-off.**
2. **X is the only major platform with a self-serve paid commercial path today.** It is pay-per-use at **$0.005 per post read**, capped at 3M post reads per month. Its Developer Agreement, however, forbids "investigating or tracking X users" without written approval. It also forbids storing inferences about "alleged or actual commission of a crime". Government end users need an Enterprise plan. **S4 (counts and aggregates) fits easily. S5's account-tracking half needs X's written approval.**
3. **Telegram is the most important source for pump schemes and the riskiest legally.** The MTProto API is free and technically reads public channels. However, Telegram's *Content Licensing and AI Scraping Terms*, which apply to "all users, businesses, and third-party services", forbid access "for any purpose other than ordinary, legitimate, and intended use of the Telegram platform as its user". The Telegram API Terms also forbid using Telegram data in the "deployment of artificial intelligence, machine learning models". **Commercial monitoring of Telegram is not clearly allowed. Do not build a production Telegram collector until the lawyer has reviewed it and, ideally, Telegram has given written permission.**
4. **Reddit now requires approval for any API access.** Commercial use needs a separate written agreement. Reddit's Developer Terms explicitly forbid using Reddit data "for law enforcement or surveillance purposes".
5. **StockTwits has closed its developer registrations.** The only route is a negotiated data licence.
6. **The cheapest legal MVP:**
   - Backtest on SEC/DOJ complaints, which are public records.
   - Use X pay-per-use for cashtag *counts and text*, with roughly $100–$300 a month of credits.
   - Use the Meta Ad Library API, which is free, to find paid ads that recruit victims into "investment clubs" on WhatsApp and Telegram.
   - Use the Bluesky Jetstream feed, which is free and open.
   - Use YouTube comments within the free quota and its 30-day storage rule.
   - Apply to Reddit and email StockTwits and Telegram in parallel.

   Details are in §12.

---

## 1. Telegram

### 1.1 Access methods

| Method | How | Who can use it | Fit for PumpWatch |
|---|---|---|---|
| **MTProto client API** (official) | Log in to <https://my.telegram.org> with a real phone-number account, fill in "API development tools", and receive an `api_id` and `api_hash`. Use a client library such as Telethon or TDLib. Resolve a **public** channel by its `@username` and call `messages.getHistory`. | Any Telegram user. The API is free. | Technically the best: full text, timestamps and sender ids for public channels. **Licensing is the problem (§1.3).** |
| **Bot API** | Create a bot via @BotFather. | Anyone. | **Not usable for monitoring.** A bot only receives channel messages where it is a member, and a channel adds it only through its admin. You cannot invite yourself into scam channels, and that would also breach our red line. |
| **Telegram Desktop "Export chat history"** (JSON) | Desktop app → open the chat → ⋯ → *Export chat history* → JSON. | Any account that legitimately sees the public channel. | Manual and small-scale. Useful for building **labelled backtest cases** from channels that SEC/DOJ complaints name. Personal-data and licensing rules still apply to what we do with the export. |
| Public web preview `t.me/s/<channel>` | HTML page. | n/a | **Do not scrape it.** The ToS ban on scraping applies to all users. |

**A correction to the brief:** there is no method called `channels.getHistory`. The official method page `https://core.telegram.org/method/channels.getHistory` returns "Page not found". The right method is **`messages.getHistory`**, used with an `InputPeerChannel`.

The official `messages.getHistory` page says (checked 2026-10-04):
- "Returns the message history in a peer."
- "Only users can use this method". **Bots cannot call it.**
- Error `CHANNEL_PRIVATE`: "You haven't joined this channel/supergroup".

Reading a **public** broadcast channel *without joining* is standard client behaviour: it is how the "preview channel" view works in the apps. **UNVERIFIED in the official docs:** no official page says in so many words that public channels can be read without joining. The community libraries rely on this behaviour, and we must test it before relying on it.

### 1.2 Rate limits

Telegram publishes **no fixed numbers** for user accounts. Limits are enforced dynamically.

Official error docs (<https://core.telegram.org/api/errors>, checked 2026-10-04):
- `420 FLOOD`: "the maximum allowed number of attempts to invoke the given method with the given input parameters has been exceeded".
- `FLOOD_WAIT_X`: "A wait of X seconds is required (where X is a number)".
- There is also `FLOOD_PREMIUM_WAIT_X`.

**Design rules for our collector:**
- Always sleep for the full X seconds and never rotate accounts to dodge a wait.
- Run a single account per `api_id`.
- Poll at a low frequency, for example each watched channel every 5–15 minutes.

From <https://core.telegram.org/api/obtaining_api_id> (checked 2026-10-04):
> "all accounts that log in using unofficial Telegram API clients are automatically put **under observation** to avoid violations of the Terms of Service."
> "If you use the Telegram API for flooding, spamming, faking subscriber and view counters of channels, you **will be banned forever**."

### 1.3 Terms that matter (verbatim)

**Telegram ToS**, <https://telegram.org/tos>. Checked 2026-10-04. No date shown.
> "Telegram additionally prohibits data scraping as part of its Content Licensing and AI Scraping Terms, which apply to all users, businesses, and third-party services accessing the platform."

**Terms of Service for Content Licensing**, <https://telegram.org/tos/content-licensing>. Checked 2026-10-04. No date shown.
> "Access to user-generated content for any purpose other than ordinary, legitimate, and intended use of the Telegram platform as its user is prohibited."
>
> "As a limited exception, Telegram permits access to data required to launch and operate a legitimate third-party Telegram Client, Telegram Bot, or Telegram Mini App, provided that it operates in full compliance with the Telegram Terms of Service, and, by extension, the Telegram API Terms of Service and the Terms of Service for Bot Developers. Any such data is licensed on a retractable, limited, non-exclusive, non-transferable and non-sublicensable basis solely to the extent strictly required to operate the relevant service …"
>
> "For clarity, Telegram firmly prohibits the scraping, indexing, harvesting, aggregation or use of data obtained from its platform to train, fine-tune, validate or otherwise engage in the development, enhancement, benchmarking or deployment of artificial intelligence, machine learning models and similar technologies."

**Telegram API Terms of Service**, <https://core.telegram.org/api/terms>. Checked 2026-10-04. No date shown.
> "1.5. Your use of the Telegram API is further subject to the Telegram Terms of Service for Content Licensing and AI Scraping. As such, you are prohibited from using, accessing or aggregating data obtained from the Telegram platform to train, fine-tune or otherwise engage in the development, enhancement or deployment of artificial intelligence, machine learning models and similar technologies."
>
> "3.1. Developers are allowed to monetize their coding efforts through advertising or other legitimate means."
>
> "2.2. We offer our API free of charge …"

**What this means for PumpWatch, clause by clause:**

| Topic | Answer |
|---|---|
| Cost | Free. |
| Commercial use | API Terms 3.1 allows monetising a *client app*. The Content Licensing terms limit data access to what is "strictly required to operate" a client, bot or Mini App, and to "ordinary … intended use … as its user". **A server-side monitoring service that sells derived alerts is very likely outside that exception.** Needs a lawyer, and ideally written permission from Telegram. |
| ML | **Forbidden** ("deployment of … machine learning models"). If PumpWatch ever uses Telegram data in an ML scorer, including only at inference time, that breaches the terms. **Telegram data, if used at all, must go through rule-based, transparent signals only, such as counts, keyword lists and exact or near-duplicate hashing.** Even "aggregation" appears in the banned list. That is the point the lawyer must resolve. |
| Retention / deletion | The API Terms say nothing specific. GDPR still applies (§10). We honour deletions by re-polling: when a message disappears from the channel, we delete it from our store. |
| Redistribution | The licence is "non-transferable and non-sublicensable". **Never pass raw Telegram messages to customers.** Pass only our own alert, with a ticker, a time, a score and a short evidence summary. |
| Surveillance / government | There is no explicit surveillance or government clause. The "ordinary use as its user" wording is the binding constraint. |
| Bot API | Only chats the bot is a member of. A channel adds a bot only via its admins, so this route is useless for monitoring third-party channels. |

---

## 2. Reddit

### 2.1 Access method and status (as of 2026-10-04)

- **Approval is now required for all Data API access.** This changed in November 2025, when self-service access was closed.

  *Responsible Builder Policy* (official help-centre article <https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy>). The browser page returns 403 to bots, so I read it via the help-centre JSON API on 2026-10-04. It was last edited 2026-06-05.
  > "Approval is required: You must request access and get explicit approval before accessing any Reddit data through our API, and you must agree to comply with all applicable terms."
  >
  > "If you'd like to use Reddit data for commercial purposes, you'll need to get explicit written approval. You can contact us here and our team will be in touch if your proposal fits our criteria."
  >
  > "You must not sell, license, share, or otherwise commercialize Reddit data without express written approval. This extends to commercial and non-commercial mining, scraping, or using data for purposes like ads targeting or to train machine learning or AI models."
  >
  > "You are strictly prohibited from processing data to derive or infer potentially sensitive characteristics about Reddit users … you must never attempt to re-identify, de-anonymize, or reverse engineer data about Redditors including by matching data with off-platform identifiers."

- **OAuth is mandatory.** The client must send a descriptive User-Agent of the form `<platform>:<app ID>:<version> (by /u/<username>)`.

### 2.2 Rate limits and cost

*Reddit Data API Wiki*, <https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki>. Read via the help-centre JSON API on 2026-10-04. Last edited 2026-05-11.
> "We enforce rate limits for those eligible for free access usage of our Data API. The limit is: 100 queries per minute (QPM) per OAuth client id. QPM limits will be an average over a time window (currently 10 minutes) to support bursting requests."
>
> "Traffic not using OAuth or login credentials will be blocked …"

**Cost:**
- **Free tier:** 100 QPM, *only for approved non-commercial use*.
- **Commercial:** a separate contract. The Data API Terms §3.1 (below) say so.
- **The 2023 figure:** in June 2023 Reddit announced **$0.24 per 1,000 API calls** for large-scale or commercial apps. **Current status is UNVERIFIED.** Reddit publishes **no commercial rate card** on any official page I could open today. Third-party blogs from 2026 still quote $0.24/1k and mention $12k minimums, but those are not official. Treat commercial pricing as "negotiated".

### 2.3 Terms (verbatim)

**Data API Terms**, <https://redditinc.com/policies/data-api-terms>. "Effective June 19, 2023. Last Revised July 20, 2026". Checked 2026-10-04.
> "3.1 Fees … If you are interested in using the Data APIs for commercial purposes, research in excess of rate limits, or for any use that is not expressly permitted under the Data API Terms, then you will need to enter into a separate agreement with Reddit."
>
> "use the Data APIs to encourage or promote illegal activity or violation of third party rights (including using User Content to train a machine learning or AI model without the express permission of rightsholders in the applicable User Content);"
>
> "sell, lease, or sublicense the Data APIs or access thereto or derive revenues from the use or provision of the Data APIs, whether for direct commercial or monetary gain unless there is express written approval from Reddit;"
>
> "use or retain any User Content, Materials, or data accessed through the Data APIs beyond your approved use case, and you must immediately delete any data not required for it"
>
> §6: on termination, delete everything. "This includes any data or models that were derived from User Content and Materials that were accessed from the Data APIs or our other Services."

**Developer Terms**, <https://redditinc.com/policies/developer-terms>. "Effective September 24, 2024. Last Revised March 24, 2026". Checked 2026-10-04.
> "access or use the Reddit Services and Data through any means (including by accessing our API or indexing, caching, or crawling our Reddit Services and Data) to train large language, artificial intelligence, or other algorithmic models or related services without our permission;"
>
> "… or (e) uses the Reddit Services and Data **for law enforcement or surveillance purposes**"
>
> "U.S. government entities are prohibited from accessing and using the Reddit Licensed Materials without our prior written approval …"
>
> §7.3: delete data when "retaining it is no longer necessary for your App's stated and approved functionality … Reddit requests you delete it; the applicable App User requests you delete it; or required by applicable laws or regulations."

**Deletion rule** (Data API Wiki, 2026-10-04):
> "When a user account is deleted, you must delete all related user ID info (e.g., t2_*). You must also delete all references to the author-identifying information … To best comply with this policy, we strongly recommend routinely deleting any stored user data and content within 48 hours. Note that retention of content and data that has been deleted–-even if disassociated, de-identified or anonymized–-is a violation of our terms and policies."

**Implications:**
- **Our hashed author ids are explicitly in scope.** When a Reddit author or post is deleted, we must delete the related `Post` rows and their author hash. "De-identified" does not save us. In practice, plan for a **48-hour rolling window for raw Reddit posts** and keep only *ticker-level aggregates* longer.
- **The "surveillance" and "law enforcement" bans** matter if we sell to regulators such as the SEC, FINRA, the ISA or ESMA, and arguably to broker compliance teams too. Ask Reddit for written approval that names the use case.

**Pushshift:** since May 2023 it has been restricted to **approved Reddit moderators, for moderation use only**. This comes from Pushshift and Reddit announcements in r/pushshift (2023). The status was confirmed only through secondary sources on 2026-10-04, so it is **UNVERIFIED** on an official page today. **Not usable by PumpWatch.** Unofficial dumps such as "Arctic Shift" and torrents are **not licensed. Do not use them.**

---

## 3. X (Twitter)

### 3.1 Tiers and prices (as of 2026-10-04)

Official pricing page <https://docs.x.com/x-api/getting-started/pricing>, checked 2026-10-04:
> "The X API uses pay-per-usage pricing. No subscriptions—pay only for what you use."

| Resource | Unit cost |
|---|---|
| Posts: Read | **$0.005 per resource** |
| User: Read | $0.010 per resource |
| Following/Followers: Read | $0.010 per resource |
| Post: Create | $0.015 per request |

More rules from the same page:
> "Pay-per-usage plans are capped at 3 million Post reads per monthly billing cycle. If you need higher volume, upgrade to an Enterprise plan."
>
> "All resources are deduplicated within a 24-hour UTC day window."
>
> Free credits (<https://docs.x.com/x-api/getting-started/free-credits>): "A one-time $20 in free credits when an account saves its first eligible card" plus a match of the first auto-recharge "up to $50".

**Legacy tiers:**
- **Free / Basic / Pro** are no longer offered to new sign-ups. No official 2026 page lists them as purchasable.
- The **figures and dates below are UNVERIFIED** and come from third-party sources only: Basic $200/mo, Pro $5,000/mo. Legacy Basic is said to have been migrated to pay-per-use after 1 June 2026 and Pro after 1 September 2026.
- **Enterprise:** custom contract and price; the documentation says "Request Access". Enterprise is *required* if any Government End User receives X content (see below).

**Cost estimate for PumpWatch:**
- Watching about 300 microcap cashtags with recent-search pulls of about 300k distinct posts a month costs about $1,500/mo.
- A lean MVP of about 30k posts a month costs about **$150/mo**.
- The deduplication rule means re-reading the same post on the same day is free.
- **Counts are billed (verified by the department head, 2026-10-04):** the official price table lists "Counts: Recent $0.005 per request" and "Counts: All $0.010 per request". One request returns a whole time series for one query, so hourly counts for a ticker over 7 days should cost about $0.005, not $0.005 per post (whether a 7-day hourly series ever paginates is UNVERIFIED). **For S4, counts are the cheapest and most privacy-friendly input.**

### 3.2 Rate limits

Official page <https://docs.x.com/x-api/fundamentals/rate-limits>, checked 2026-10-04:
- `GET /2/tweets/search/recent`: **450 / 15 min per app**, 300 / 15 min per user, 100 results per page.
- `GET /2/tweets/search/all` (full archive): **1 request/sec and 300 / 15 min per app**, 500 results per page.
- Filtered stream: 1 connection, 1,000 rules, "250 posts/sec".

### 3.3 Developer Agreement and Policy (verbatim)

**Developer Agreement**, <https://developer.x.com/en/developer-terms/agreement>. "Last Updated: April 27, 2026". Checked 2026-10-04.
> "B. User Protection. Unless explicitly approved by X in writing, you shall not use, or knowingly display, distribute, or otherwise make X Content, or information derived from X Content, available for purpose of: (a) **conducting or providing surveillance or gathering intelligence, including but not limited to investigating or tracking X users or X Content**; (b) conducting or providing analysis or research for any unlawful or discriminatory purpose or in a manner that would be inconsistent with X users' reasonable expectations of privacy; … (d) targeting, segmenting, or profiling individuals based on sensitive personal information, including … negative financial status or condition, … **X Content relating to any alleged or actual commission of a crime** …"
>
> "C. Government Use. If you display, distribute, or otherwise make available any X Content to Users that are, or that act on behalf of, any government-related entity (each a "Government End User"); (a) **you must apply for (or already subscribe to) an Enterprise plan** …; (b) you shall identify all such Government End Users when submitting your use case for review to X … You shall not use, or knowingly display, distribute, or otherwise make X Content, or information derived from X Content, available to any Government End User whose primary function or mission includes conducting surveillance or gathering intelligence."
>
> "B. Removals. If X Content is deleted, gains protected status, or is otherwise suspended, withheld, modified, or removed from the X Applications …, you will make all reasonable efforts to delete or modify that X Content … as soon as possible, and in any case within twenty four (24) hours after a written request to do so by X or by an X user …"
>
> "(d) sell, rent, lease, sublicense, distribute, redistribute, syndicate, … the Licensed Material to any third party except as expressly permitted in this Agreement"

**Developer Policy**, <https://developer.x.com/en/developer-terms/agreement-and-policy>. Checked 2026-10-04.
> "If you provide X Content to third parties, including downloadable datasets or via an API, you may only distribute Post IDs, Direct Message IDs, and/or User IDs (except as described below)."
>
> "If you store X Content offline, you must keep it up to date with the current state of that content on X. Specifically, you must delete or modify any content you have if it is deleted or modified on X."
>
> "Finally, please note that X may monitor your use of the X API … to examine any commercial use, and to ensure your compliance with your approved use case and this Policy."
>
> "You may not register multiple applications for a single use case …"

**Restricted uses**, <https://developer.x.com/en/developer-terms/more-on-restricted-use-cases>. Checked 2026-10-04.
> "Never derive or infer, or store derived or inferred, information about a X user's: … Negative financial status or condition … **Alleged or actual commission of a crime**"
>
> "**Aggregate analysis of X content that does not store any personal data (for example, user IDs, usernames, and other identifiers) is permitted**, provided that the analysis also complies with applicable laws and all parts of the Developer Agreement and Policy."

**Implications for PumpWatch:**

| Topic | Answer |
|---|---|
| Commercial OK? | **Yes** for pay-per-use with an approved use case. We must describe our use case honestly in the Developer Console. |
| S4 (ticker mention spikes) | Allowed as **aggregate analysis without storing user identifiers**. Store only counts, n-grams and hype-word scores per ticker per hour. |
| S5a (identical wording) | Mostly OK if we hash the *text* and do not keep user ids. |
| S5b (the same accounts promoting many tickers) | **This is "tracking X users".** It also produces an inference about an "alleged … commission of a crime". **It needs X's written approval.** Until then, S5b must not use X data. |
| Selling to regulators | Any government user requires an **Enterprise** plan and disclosure. Agencies whose primary mission is surveillance or intelligence are banned outright. A securities regulator is probably not a "surveillance/intelligence" agency, but **ask the lawyer and X.** |
| Displaying posts to customers | Show Post IDs or links rather than copies, and remove anything deleted on X within 24 hours. |
| ML training | The Agreement has no explicit ban on ML for *our own* models. Separately, the user-protection clause above applies. Treat this as **UNVERIFIED and to be confirmed with X.** |

---

## 4. StockTwits

- **Public API:** <https://api.stocktwits.com/developers>, checked 2026-10-04:
  > "we are currently reviewing all of our APIs, documentation and terms. We unfortunately won't be accepting new registrations until we have finished our review … For any questions please email developers@stocktwits.com."

  **Registrations are closed.** The page footer is dated 2021, so this "temporary" state has lasted years.
- **Terms**, <https://stocktwits.com/terms>. "Last Revised: July 10, 2026". Checked 2026-10-04.
  > "You may not scrape, harvest, mirror, frame, deep-link to, data-mine, or otherwise extract data or content from the Service by automated means except as expressly authorized by us in writing or through an approved API, widget, developer offering, or other product rule."
  >
  > "You may not … use the Service through an unauthorized third-party … scraping service, automation service, signal service …"
- **Enterprise / partner data feeds:** StockTwits licenses its data and sentiment to institutions; Trading Central and Polygon.io have been reported as partners. **Prices and terms are UNVERIFIED.** No official public price page exists; contact sales or developers@stocktwits.com.
- **Verdict:** this is a high-value source, because it is cashtag-native and microcap retail is heavily represented. **The only legal route is a written licence.** Scraping is forbidden. Ask for a quote early.

---

## 5. Discord

- **Access:** only through a **bot account** that a **server admin invites** to *their* server, using OAuth2 scopes `bot` plus the needed permissions. Reading message text needs the **privileged Message Content intent**.
  - Below 100 servers, the developer can toggle this intent on.
  - Verified bots in 100+ servers need Discord's approval.
  - **These thresholds are UNVERIFIED on an official page today.** They come from third-party docs, because the official docs host blocked automated fetching.
- **No self-bots.** Support article "Automated User Accounts (Self-Bots)", read via the help-centre JSON API on 2026-10-04:
  > "Automating normal user accounts (generally called "self-bots") outside of the OAuth2/bot API is forbidden, and can result in an account termination if found."
- **Discord ToS**, <https://discord.com/terms>. "Effective: September 29, 2025". Checked 2026-10-04. It forbids:
  > "scraping our services without our written consent, including by using any robot, spider, crawler, scraper, or other automatic device, process, or software; selling, licensing, or otherwise commercializing content or data obtained from our services"
- **Developer Policy** (support-dev.discord.com article 8563934450327). "Effective date: July 8, 2024". Read via the help-centre JSON API on 2026-10-04.
  > "15. Do not use API Data for any purpose outside of what is necessary to provide your stated functionality."
  >
  > "16. Do not use API Data to: profile Discord users, their identities, or their relationships with other users …"
  >
  > "17. Do not disclose API Data to data brokers, advertising networks or services, or any other monetization-related service."
  >
  > "18. Do not sell, license, or otherwise commercialize API Data …"
  >
  > "19. Do not attempt to re-identify, de-anonymize, unscramble, unencrypt, or reverse hash or reverse engineer API Data from the form in which you obtain it."
  >
  > "20. Do not mine or scrape any data, content, or information available on or through Discord services …"
  >
  > "21. Do not use message content obtained through the APIs to train machine learning or AI models (including large language models) unless express permission is granted by Discord."
- **Developer Terms of Service** (article 8562894815383). "Effective date: July 8, 2024". Read via JSON API on 2026-10-04. Delete API Data when it is no longer necessary, when Discord or the user asks, or when the app stops operating; "You will give users an easily accessible way to ask for their API Data to be modified and deleted."
  - The current Developer Terms contain **no explicit "surveillance/law enforcement" clause**. The earlier 2020 version did, according to secondary sources; **UNVERIFIED**.
  - The binding limits are items 15, 16 and 18 above.
- **Cost:** free. Rate limits are per-route and dynamic (HTTP 429 with `retry_after`).
- **Verdict:** Discord is **not viable for monitoring pump servers.** Their admins will not invite our bot, and joining under false pretences breaches our red line. Profiling users and commercialising API Data are both banned. The **only** legitimate Discord use is a partnership: a broker or community admin invites a *moderation-safety* bot to their **own** server, with disclosure. Low priority.

---

## 6. YouTube

- **Access:** YouTube Data API v3 with an API key, which is enough for public data. Use `commentThreads.list` with `videoId` or `allThreadsRelatedToChannelId`.
  > "A call to this method has a quota cost of 1 unit." (<https://developers.google.com/youtube/v3/docs/commentThreads/list>, last updated 2026-09-14, checked 2026-10-04)
- **Quota.** Getting Started page, checked 2026-10-04:
  > "Projects that enable the YouTube Data API have a default quota allocation of 100 search.list calls, 100 videos.insert calls, and 10,000 units per day combined for all other endpoints."

  More quota requires an **API Compliance Audit**.
- **Cost:** free within the quota.
- **YouTube API Services Developer Policies**, <https://developers.google.com/youtube/terms/developer-policies>. Last updated 2026-09-14. Checked 2026-10-04.
  > "API Clients may temporarily store limited amounts of Non-Authorized Data for as long as is necessary for the purposes of the API Client but not longer than 30 calendar days. … after 30 calendar days, the API Client must either delete or refresh the stored data."
  >
  > "an API Client must not store statistics retrieved as Non-Authorized Data for more than 30 days."
  >
  > "**Do not aggregate API Data** except that you may only aggregate API Data relating to YouTube channels that are under the same content owner … Do not aggregate API Data or otherwise use API Data or YouTube API Services to gain insights into YouTube's usage, revenue, or any other aspects of YouTube's business."
  >
  > "You and your API Clients must not … directly or indirectly, scrape YouTube Applications or Google Applications, or obtain scraped YouTube data or content."
  >
  > Prohibited: "sell, purchase, lease, lend, convey, redistribute, or sublicense all or any portion of YouTube API Services"; "sell YouTube API Services or access to any components of YouTube API Services unless you obtain YouTube's prior written approval"
- **Surveillance:** the pages checked contain no explicit surveillance or government clause. ML is not addressed in what I read.
- **Implications:**
  - Keep a hard **30-day TTL** on raw YouTube comments.
  - The **"Do not aggregate API Data"** clause is a real question for cross-channel mention counts (S4). **Lawyer question.**
  - We may sell our *alerts*, but not the YouTube data itself.
  - Low-to-medium priority. "Finfluencer" videos that pump microcaps are relevant, but comments are noisy.

---

## 7. Meta (Facebook / Instagram)

### 7.1 Ad Library API (free, and the most useful Meta source)

- **What it covers.** Official reference <https://developers.facebook.com/docs/graph-api/reference/ads_archive/>, checked 2026-10-04:
  - `ad_type` values include `POLITICAL_AND_ISSUE_ADS` and **`FINANCIAL_PRODUCTS_AND_SERVICES_ADS`**, the latter "returns ads related to financial products, services, or institutions".
  - `ad_reached_countries`: "Note: Ads that did not reach any location in the EU will only return if they are about social issues, elections or politics."
  - `search_terms`: "The limit of your string is 100 characters or less."
  - In short, the API returns **all ads delivered to the EU** (the DSA transparency regime) and political or social-issue ads globally.
  - Note that **Meta stopped political, electoral and social-issue ads in the EU from October 2025** (secondary source; **UNVERIFIED** on an official page).
- **Who can access.**
  - A Meta developer account plus a user access token.
  - Meta's Ad Library API page (<https://www.facebook.com/ads/library/api>) returned **403** today, so the **identity-confirmation requirement is UNVERIFIED** today. Historically, Meta required ID and location confirmation before granting access.
  - Rate-limit error 613 exists; **thresholds are not published.**
- **Why it matters for PumpWatch:** the 2024–2026 "ramp-and-dump" schemes recruit victims through **Facebook and Instagram ads that lead to WhatsApp "investment clubs"**. EU-delivered ads, and in some markets financial-services ads, are searchable by keyword: "stock club", "WhatsApp", ticker names, "free stock picks". This gives **a legal window into the WhatsApp funnel without touching WhatsApp.** These are **advertiser** records, not private individuals, which lowers privacy risk.
- **Terms:** use is governed by Meta Platform Terms and the Ad Library API terms. **I did not open them today: UNVERIFIED.**

### 7.2 Meta Content Library and API (researchers only)

Official page <https://transparency.meta.com/researchtools/meta-content-library>, checked 2026-10-04:
> Eligibility: "Affiliation with an academic institution or other non-university organization, institute, or society which operates as a not-for-profit entity".
>
> Cost: "There are no fees associated with access or computation …"

Access runs through Meta's Secure Research Environment or the SOMAR Virtual Data Enclave.

**Not available to a commercial company like PumpWatch.** An academic partner could use it for a *published study* only, never for our product.

### 7.3 General scraping of Facebook and Instagram is prohibited

**Automated Data Collection Terms**, <https://www.facebook.com/legal/automated_data_collection_terms>. Checked 2026-10-04.
> "You will not engage in Automated Data Collection without first obtaining Meta's express written permission or in any manner that is not explicitly authorized by Meta."
>
> "All other Uses are prohibited, including, but not limited to, transferring, selling, licensing or sublicensing Collected Data and data derived from Collected Data to any third party."

**No FB or IG scraping, including of "public" groups and pages.**

---

## 8. WhatsApp: out of scope

**WhatsApp Terms of Service**, <https://www.whatsapp.com/legal/terms-of-service>. Checked 2026-10-04. The page shows "Effective January 4, 2021" (US version). Users must not:
> "collect information of or about our users in any impermissible or unauthorized manner"
>
> "sending illegal or impermissible communications such as bulk messaging, auto-messaging, auto-dialing, and the like"
>
> "create accounts for our Services through unauthorized or automated means"

**Why it is out of scope, even though it is where the fraud happens:**
- Pump groups on WhatsApp are **private, invitation-only, end-to-end encrypted** chats.
- There is **no API to read groups**. The WhatsApp Business API only serves a business's *own* customer conversations.
- The only ways in are joining under a fake identity and automating a user account. Both breach the ToS **and** our red lines (§11).
- The Chinese and Korean "ramp-and-dump" rings that impersonate advisers in WhatsApp clubs are therefore covered by:
  - **S7 consent-based victim reports.** A user voluntarily submits screenshots of messages *they received* through our "report suspicion" button, and we store them as `VictimReport(ticker, day, note)` with minimal personal data. The reporter is the data subject for their own messages. Third parties' names and phone numbers in screenshots must be **redacted on ingestion**.
  - **Meta Ad Library**, which shows the ads that funnel victims into those groups (§7.1).
  - Broker-side flow data under contract (S6).

---

## 9. Optional platforms

| Platform | Access | Commercial / terms | Verdict |
|---|---|---|---|
| **Bluesky** | The AT Protocol firehose and **Jetstream** (JSON) are open and need no API key for public data. The official firehose doc page returned 503 today, so the auth details are **UNVERIFIED** today. | Bluesky Developer Guidelines (official `bsky-docs` repo on GitHub, read 2026-10-04): "All services must have a method for deleting content a user has requested to be deleted." "Don't spam." Developer **guidelines** contain no ban on commercial use or ML. Bluesky's main ToS was **not opened (UNVERIFIED)**. Funded or commercial users are expected to run their own relay or pay an infrastructure provider. | **Free, good for MVP**, but microcap pump volume there is low (**UNVERIFIED**). Must process `delete` events. |
| **Mastodon / fediverse** | Each server's public timeline API. | Terms are **per instance**, and many instances' rules forbid commercial data collection or AI use. **Not checked: UNVERIFIED.** | Low priority. Needs per-instance permission. |
| **TikTok Research API** | Official page <https://developers.tiktok.com/products/research-api/> (checked 2026-10-04): academic or not-for-profit researchers in the US, EEA, UK, Canada or Switzerland. Applicants must be "independent of commercial interests and able to conduct research on a not-for-profit or non-commercial basis." | **No commercial use.** TikTok's Commercial Content API covers ads only; **not checked: UNVERIFIED.** | Out for the product. Possible academic partnership only. |
| **Truth Social** | No public developer API. The ToS page returned 403 today. | **UNVERIFIED.** | Out. |

---

## 10. Privacy and compliance design

### 10.1 Why GDPR and Israeli law apply even to "public" posts

Public posts are still **personal data** when they relate to an identifiable person: a handle, a username or a Telegram user id. Our customers are in the EU, the US and Israel, and some posters are in the EU. GDPR applies through Art. 3(2)(b), because we monitor the behaviour of people in the EU. Israel's Privacy Protection Law applies to our Israeli processing.

### 10.2 GDPR lawful basis

- **Art. 6(1)(f), legitimate interests:**
  > "processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject …" (gdpr-info.eu, checked 2026-10-04)

  Our interest is preventing market-abuse fraud against retail investors. That interest is also our customers' MAR and FINRA surveillance duty. We need a **written Legitimate Interests Assessment (LIA)** covering purpose, necessity and balancing, and a **DPIA** under Art. 35, because this is systematic monitoring of publicly accessible data at scale.
- **Art. 9 (special categories):** we must not infer health, politics, religion and the like. The keyword lists must avoid these, and we must not store free text longer than needed.
- **Art. 10 (criminal offences):** **this is the key risk.** An alert that says "account X is likely a pump promoter" is arguably *personal data relating to (alleged) criminal offences*. Art. 10 allows that only "under the control of official authority" or where Union or Member State law authorises it with safeguards. *I paraphrase Art. 10; the text was not re-quoted today.*

  **Design answer:**
  - Alerts are **about tickers, not people**.
  - Author-level signals (S5b) stay internal as opaque hashes and are **never shipped to customers as named individuals**.
  - **No "promoter list" product.**

  This also lines up with X's ban on inferring "alleged … commission of a crime" and with Reddit's and Discord's profiling bans.
- **Art. 14 (information to data subjects when data is not collected from them):** Art. 14(5)(b) gives a "disproportionate effort" exemption, but in that case "the controller shall take appropriate measures … including making the information publicly available". **We publish a clear privacy notice on our website** describing the collection, the sources and how to object.
- **Art. 21, right to object:** provide an opt-out or objection channel and honour it by adding the hashed id to a suppression list.

### 10.3 Pseudonymisation: salted hashes are still personal data

GDPR Recital 26, gdpr-info.eu, checked 2026-10-04:
> "Personal data which have undergone pseudonymisation, which could be attributed to a natural person by the use of additional information should be considered to be information on an identifiable natural person."

**`author` in `Post` is an opaque id, but it is pseudonymous personal data, not anonymous data.** Whoever holds the salt can re-link it, and the platform can too, since it knows the original id. Reddit says explicitly that de-identified deleted data must still be deleted, and Discord item 19 bans reverse-hashing.

**Design:**
1. `author = HMAC-SHA256(key_k, platform + ":" + platform_user_id)`, truncated to 128 bits. Use a **keyed HMAC, not a plain salted hash**. The key lives in a KMS and never sits in the database.
2. **Key rotation every 30 days.** After rotation, old hashes can no longer be linked to new ones. S5b therefore only works **within a 30-day window**, which is enough for pump cycles that last days to weeks.
3. Destroy old keys after the retention period, which acts as crypto-shredding.
4. **Never store handles, display names, avatars or profile URLs.** For an evidence pointer, store the platform's post id only (X allows distributing Post IDs). Delete it per platform rules.
5. **Separate the stores.** Raw text with short TTLs, versus ticker-day aggregates with no author field, which are kept long-term.

**Note (UNVERIFIED, not re-opened today):** the CJEU judgment in *EDPS v SRB* (C-413/23 P, September 2025) suggests pseudonymised data may be non-personal *for a recipient* who cannot re-identify it. That helps for what we send customers, but **not for us**, since we hold the key.

### 10.4 Israel: Privacy Protection Law, Amendment 13

- In force **14 August 2025**, per secondary legal-firm sources (Pearl Cohen, Meitar); I did not open the official Knesset text today, so the date is **UNVERIFIED** on an official source.
- The amendment:
  - broadens "personal information", explicitly covering online identifiers;
  - creates a category of "information of special sensitivity", which includes criminal records and financial details;
  - requires a DPO for some controllers, with enforcement from 31 Oct 2025 per secondary sources;
  - gives the **Privacy Protection Authority (PPA)** administrative-fine powers and expands transparency duties when collecting data.
- **For us:**
  - Register or assess our database obligations.
  - Assess whether we must appoint a DPO, since systematic monitoring at scale and data of special sensitivity can trigger it.
  - Keep data minimal.
  - Allow access and correction requests.
- **Lawyer question:** does monitoring public posts and producing fraud-risk scores amount to processing "information of special sensitivity" about posters?

### 10.5 Retention (proposed defaults; strictest platform rule wins)

| Data | Retention | Driver |
|---|---|---|
| Raw Reddit post text plus author hash | **≤ 48 h** rolling, re-checked for deletion | Reddit Data API Wiki |
| Raw YouTube comments | **≤ 30 days**, then delete or refresh | YouTube Developer Policies |
| Raw X posts | ≤ 30 days; delete within 24 h of a removal request or a deletion on X | X Agreement and Policy |
| Raw Telegram messages | ≤ 30 days, if lawyer-approved at all; delete when gone from the channel | GDPR minimisation; Telegram licence |
| Bluesky raw posts | ≤ 30 days; process `delete` events immediately | Bluesky guidelines |
| Author HMAC ids | key rotated every 30 days; old keys destroyed | GDPR Recital 26 |
| Ticker-day aggregates (no author field) | long-term | not personal data |
| Victim reports (S7) | per consent, default 12 months, redacted | consent; GDPR Art. 7 |
| Alerts sent to customers | per customer contract and record-keeping law; **contain no third-party personal data** | contract |

### 10.6 Deletion propagation

1. Use each platform's deletion signal: X compliance endpoints and streams, re-polling Reddit, Bluesky `delete` events, re-polling Telegram, the YouTube 30-day refresh.
2. A deletion job removes the raw rows and **any derived per-author features**. Reddit says derived data and models must go too on termination.
3. Ticker-level aggregates without author fields may stay.
4. Every deletion is logged by id and timestamp only, as proof of deletion, which Reddit and Discord may request.

---

## 11. HARD RED LINES (policy, verbatim; no exceptions without written board and lawyer sign-off)

1. **No fake identities to join private groups.**
2. **No WhatsApp scraping.**
3. **No buying access to private groups.**
4. **Authors stored only as opaque hashed ids.**
5. **Minimal personal data.**
6. **No trading on alerts.**

These also follow from the policies above:
- **No scraping of any platform** (web pages, `t.me/s/`, FB/IG, StockTwits, YouTube) and **no unofficial data dumps** (Pushshift mirrors, torrents).
- **No self-bots or user-account automation** (Discord, WhatsApp). Telegram user-API use must stay within limits and must not interfere with read statuses.
- **No customer-facing "lists of people".** Alerts are about tickers.
- **No ML on Telegram, Reddit or Discord data without written permission.**

---

## 12. Comparison and recommended MVP data plan

### 12.1 Comparison table

| Platform | Method | Cost (2026-10-04) | Rate limit | Commercial OK? | Priority for PumpWatch MVP |
|---|---|---|---|---|---|
| **X** | API v2 pay-per-use: recent search, counts, filtered stream | $0.005/post read; $0.01/user read; 3M reads/mo cap; $20–$70 free credits | recent search 450/15 min per app; full archive 1/s | **Yes**, with an approved use case. Tracking users or government users needs written approval or Enterprise. | **P1** (S4 aggregates now; S5b after approval) |
| **Meta Ad Library** | Graph API `ads_archive` | Free | Unpublished (error 613) | Likely yes for analysis (**terms UNVERIFIED**) | **P1** (WhatsApp funnel ads) |
| **Telegram** | MTProto `messages.getHistory` on public channels; Desktop JSON export for backtests | Free | Dynamic `FLOOD_WAIT_X` | **Unclear, likely no** without permission: content-licensing "ordinary use" rule plus ML ban | **P1 for research and backtest only**; production on hold pending lawyer and Telegram |
| **Bluesky** | Jetstream / firehose | Free (or self-host a relay) | n/a | No ban seen in the developer guidelines (main ToS **UNVERIFIED**) | P2 (cheap, low volume) |
| **YouTube** | Data API v3 `commentThreads.list` | Free | 10,000 units/day plus 100 `search.list`/day by default; audit for more | Can sell our app, not the data. 30-day storage. "Do not aggregate" clause is a question. | P2 |
| **Reddit** | Data API (OAuth) after approval | Free non-commercial (100 QPM); **commercial = negotiated contract** (2023 figure $0.24/1k calls; current price **UNVERIFIED**) | 100 QPM per client id | **Only with written approval.** Surveillance and law-enforcement uses are banned. | P2 (apply now; use after the contract) |
| **StockTwits** | Data licence only (API registration closed) | **Negotiated, UNVERIFIED** | n/a | Only under a written licence | P2 (request a quote now; high signal value) |
| **Discord** | Admin-invited bot only | Free | Per-route 429s | **No.** Commercialising or profiling API Data is banned. | P3 / out |
| **Meta Content Library** | Researcher platform | Free | n/a | **No** (not-for-profit only) | Out |
| **TikTok Research API** | Researcher API | Free | n/a | **No** (non-commercial only) | Out |
| **WhatsApp** | none | n/a | n/a | **No.** ToS ban plus red line. | Out (use S7 victim reports) |
| **Mastodon / Truth Social** | per-instance API / none | n/a | n/a | **UNVERIFIED** | Out |

### 12.2 Recommended MVP data plan: the cheapest legal path to S4 and S5

**Phase A: backtest (weeks 1–2, about $0–$50).**
1. Build a labelled set of past pumps from **SEC and DOJ complaints**, which are public records. The complaints quote the promoters' Telegram, X and Discord messages, so we get the ground truth without collecting anything ourselves.
2. For a handful of those cases where the **public** Telegram channel still exists, a team member exports it once by hand with **Telegram Desktop → Export chat history (JSON)**, from their own real account.
   - Use it **only for offline rule tuning**: no ML, per Telegram terms.
   - Hash the authors on import.
   - Delete the raw exports after feature extraction (≤ 30 days).
   - **The lawyer confirms this step first.**
3. Run **X full-archive search** for the same tickers and dates. At $0.005 a post, 10k posts cost $50. Use the $20–$70 free credits first.

**Phase B: live MVP (about $150–$300 a month).**
1. **S4 on X:**
   - Hourly cashtag mention counts (counts endpoint, if available) plus a sample of recent-search text for the watch list of OTC and microcap tickers that S1 and S3 flag first. Pull social data **only for tickers that already show market-data anomalies**, which keeps cost low and collection minimal.
   - Store only ticker-hour aggregates and a hype-lexicon score.
   - Raw text has a 30-day TTL, and **no user ids**.
2. **S5a on X and Bluesky:** compute near-duplicate text clusters with MinHash over normalised text, **without author ids**. "37 posts in 2 hours with the same 25-word template" is enough evidence.
3. **S5b (repeat promoters):** start only after **X gives written approval** for the use case. Then use keyed-HMAC author ids with 30-day key rotation, keep it internal-only, and never show it to customers.
4. **Meta Ad Library:** run a daily keyword sweep, for example "stock club", "WhatsApp group", "free stock picks", "股票" and the watch-list tickers, over EU-delivered and financial-services ads. Store advertiser page ids and ad ids, which are business data.
5. **Bluesky Jetstream:** a free cashtag filter, with deletes honoured.
6. **S7:** the "Report suspicion" upload with explicit consent and automatic redaction of third-party names and phone numbers. **This is our only WhatsApp coverage.**

**Phase C: in parallel, at no cost now.**
1. **Reddit:** submit an access request that describes the commercial fraud-prevention use case honestly, and ask for written approval for broker and regulator customers.
2. **StockTwits:** email developers@stocktwits.com for a data-licence quote.
3. **Telegram:** after the lawyer reviews our position, ask Telegram for written permission for public-channel fraud monitoring with no ML. Without it, **live** Telegram monitoring stays off.
4. **X:** ask in writing whether (a) S5b-style account clustering for fraud prevention and (b) delivery to securities regulators via Enterprise are acceptable.

---

## 13. Questions for our lawyer

1. **Telegram:** does a commercial server that reads **public** channels through the official MTProto API fall within the Content Licensing "limited exception" for a "legitimate third-party Telegram Client"? Or is it "access … for any purpose other than ordinary … use … as its user"? Does rule-based (non-ML) scoring avoid the AI clause, given that the clause lists "aggregation"?
2. **Telegram Desktop export:** may we use manually exported JSON from public channels for internal backtesting? May a team member's personal account be used for this?
3. **X:** is ticker-level aggregate analysis plus repeat-account clustering "tracking X users"? Does a securities regulator count as a "Government End User", and does its mission count as "surveillance or gathering intelligence"? Should we apply for Enterprise up front?
4. **Reddit / Discord "surveillance and law enforcement" bans:** do they cover selling compliance alerts to **private broker-dealers**, given that brokers are themselves under a legal duty to surveil? And to regulators?
5. **YouTube "Do not aggregate API Data":** does counting ticker mentions across many channels' comments breach it?
6. **GDPR Art. 10:** is an internal "likely promoter" score on a pseudonymous id "personal data relating to criminal offences"? If yes, which Member State law or exemption, if any, lets a private company process it? Is ticker-only output enough to stay outside Art. 10 for customers?
7. **GDPR Art. 14(5)(b):** is a public privacy notice enough, or must we notify posters individually? What should our LIA and DPIA contain, and do we need an EU representative under Art. 27?
8. **Pseudonymisation:** is HMAC with 30-day key rotation and key destruction adequate? After key destruction, are the remaining aggregates anonymous? How does *EDPS v SRB* (2025) affect data we share with customers?
9. **Israel Amendment 13:** are we a "database" owner that must register or appoint a DPO? Is fraud-risk scoring of posters "information of special sensitivity"? What transparency duties apply to data not collected from the data subject?
10. **US:** any state-law issues (CCPA/CPRA "publicly available" exemption; Illinois, Texas or Washington laws) with collecting public posts? Any CFAA or contract-law risk if a platform revokes access and we keep derived aggregates?
11. **Victim reports (S7):** what consent text is required? How do we lawfully handle third parties' data, such as scammers' and other group members' names and numbers, in screenshots? What retention period applies?
12. **Liability:** if an alert names a ticker that turns out to be clean, is there defamation or market-manipulation exposure, for the issuer or for us? What disclaimers belong in customer contracts?
13. **Trading ban:** what internal-controls wording do we need for "no trading on alerts", given employees, contractors and the information-barrier policy?

---

## 14. Sources (all checked 2026-10-04)

- Telegram:
  - ToS <https://telegram.org/tos>
  - Content Licensing <https://telegram.org/tos/content-licensing>
  - API Terms <https://core.telegram.org/api/terms>
  - Obtaining api_id <https://core.telegram.org/api/obtaining_api_id>
  - Errors <https://core.telegram.org/api/errors>
  - messages.getHistory <https://core.telegram.org/method/messages.getHistory>
  - Bots FAQ <https://core.telegram.org/bots/faq>
  - Export tool <https://telegram.org/blog/export-and-more>
- Reddit:
  - Data API Terms <https://redditinc.com/policies/data-api-terms>
  - Developer Terms <https://redditinc.com/policies/developer-terms>
  - Data API Wiki <https://support.reddithelp.com/hc/en-us/articles/16160319875092> (via help-centre JSON)
  - Responsible Builder Policy <https://support.reddithelp.com/hc/en-us/articles/42728983564564> (via help-centre JSON)
- X:
  - Pricing <https://docs.x.com/x-api/getting-started/pricing>
  - Free credits <https://docs.x.com/x-api/getting-started/free-credits>
  - Rate limits <https://docs.x.com/x-api/fundamentals/rate-limits>
  - Developer Agreement <https://developer.x.com/en/developer-terms/agreement>
  - Developer Policy <https://developer.x.com/en/developer-terms/agreement-and-policy>
  - Restricted uses <https://developer.x.com/en/developer-terms/more-on-restricted-use-cases>
- StockTwits:
  - Developers <https://api.stocktwits.com/developers>
  - Terms <https://stocktwits.com/terms>
- Discord:
  - ToS <https://discord.com/terms>
  - Developer Policy <https://support-dev.discord.com/hc/en-us/articles/8563934450327> (via JSON)
  - Developer Terms <https://support-dev.discord.com/hc/en-us/articles/8562894815383> (via JSON)
  - Self-bots <https://support.discord.com/hc/en-us/articles/115002192352> (via JSON)
- YouTube:
  - Developer Policies <https://developers.google.com/youtube/terms/developer-policies>
  - API Services ToS <https://developers.google.com/youtube/terms/api-services-terms-of-service>
  - Getting started <https://developers.google.com/youtube/v3/getting-started>
  - commentThreads.list <https://developers.google.com/youtube/v3/docs/commentThreads/list>
- Meta:
  - ads_archive <https://developers.facebook.com/docs/graph-api/reference/ads_archive/>
  - Content Library <https://transparency.meta.com/researchtools/meta-content-library>
  - Automated Data Collection Terms <https://www.facebook.com/legal/automated_data_collection_terms>
  - Ad Library API page <https://www.facebook.com/ads/library/api> (403 today)
- WhatsApp ToS <https://www.whatsapp.com/legal/terms-of-service>
- TikTok Research API <https://developers.tiktok.com/products/research-api/>
- Bluesky Developer Guidelines (official repo `bluesky-social/bsky-docs`, `docs/support/developer-guidelines.md`)
- GDPR text: <https://gdpr-info.eu/art-6-gdpr/>, <https://gdpr-info.eu/recitals/no-26/>, <https://gdpr-info.eu/art-14-gdpr/>
- Israel Amendment 13 (secondary): Pearl Cohen <https://www.pearlcohen.com/israel-significant-amendment-to-the-privacy-law-takes-effect/>
