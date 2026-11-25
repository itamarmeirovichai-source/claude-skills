# Post / account findings (my own retrieval; PRIMARY source = x.com server-rendered profile page)
Fetched 2026-11-23T04:13:20Z with plain `curl -L https://x.com/Dan1ro0` (HTTP 200, 215,708 bytes); raw saved at scratchpad/post/https___x_com_Dan1ro0_.out;
full note text at scratchpad/post/post_2124255865645502610_note.txt.
Blocked/unavailable: sotwe mirror (HTTP 403), xcancel (HTTP 451), syndication.twitter.com timeline (HTTP 429), nitter.net (200 but no content). Not bypassed.
WebSearch (2 queries with exact figures) returned no independent page containing "$10,847.63", "82,540 holders", "3,825 launches".

## The post
- ID 2124255865645502610 → https://x.com/Dan1ro0/status/2124255865645502610 (ID taken from `edit_tweet_ids` + media `expanded_url` in the primary payload; I did not load the permalink page itself).
- created_at_ms 1795297039000 = 2026-11-21 21:37:19 UTC. Has a video (not viewed). Quotes own earlier status 2112255845903778017.
- Engagement at access: 1,258 likes, 156 reposts, 96 replies, 10 quotes, 1,361 bookmarks.
- Text (verbatim opening): "I used Claude Fable 5.2 and GPT-6 Astra to build a self-learning trading algorithm / The result: +$10,847.63 in 21 days /
  3,825 launches tracked. 82,540 holders analyzed. 185 wallet clusters detected. Only 19 tokens passed every check, each scoring 85+/100 /
  I MADE THE CORE SCORING CODE OPEN SOURCE (210+ STARS) / GitHub: github.com/QuantumOrb/QuantOrb / QUANTUMORB IS FULLY OPERATIONAL /
  The website, scanner, RADAR and Tg bot are publicly accessible / Three recent Solana launches:
  - Nov 20, 20:45 UTC: $BTC (BartCoin) launched → RADAR alert at 20:52 ($58K cap) → 24x from the alert
  - Nov 21, 04:26 UTC: $PUNANI launched → RADAR alert at 04:39 ($50K cap) 58x from the alert
  - Nov 21, 05:07 UTC: $MAYA launched → RADAR alert at 05:19 ($75K cap) → 50x from the alert"
  then describes modules RADAR / SHIELD / SCANNER / CARTOGRAPHER / GUARD / ORB and two formulas
  (Q_risk = F × Σ Share_i ; P_after/P_before = (R/(R+Q_risk))²), ends "QUANTUMORB IS LIVE".
- Matches the user's transcription of the screenshot on every listed claim (the screenshot image itself was NOT received by me).
- NOT in the post: any wallet address, exchange account, tx signature, trade list, starting capital, deposits/withdrawals, fees, losing trades,
  list of the other 16 "passed" tokens, mint addresses of the 3 examples, statement that the author traded these tokens,
  definition of what the "+$10,847.63" measures.

## The account
- @Dan1ro0 "Daniro", rest_id 906916544504107009, created 2017-09-10, blue-verified since 2025-10-27, 10,422 followers / 151 following, 3,369 posts.
- Bio: "Researching AI-driven trading systems, models & frameworks | 100+ Quant strategies analyzed • 1M+ transactions processed"; bio URL: github.com/QuantumOrb.
- Author presents as the project's builder ("I used … to build", "I MADE THE CORE SCORING CODE OPEN SOURCE") → self-promotion, not independent review.
- Other recent posts on the same page follow one template of large-PnL headlines about third parties:
  2026-11-19 "This guy turned Grok Bot into Quant trading desk and it made $2,727 a day on Polymarket … +$490,861 PnL in first 180 days";
  2026-11-20 "$12.5M traded, +$101,923.74 in 46 days. This guy's Grok Bot has a hedge fund track record";
  2026-11-22 "This guy used Grok Bot to build a Quant Kalman system and it made $3,748 a day on Polymarket … +$475,961 PnL in 127 days".
- Internal contradictions with the project's own repo: post says "self-learning trading algorithm"; README.md:67 says "a fixed, written set of rules, not a black box";
  repo has no ML and no trade-execution code; repo/site contain no PnL or track record; none of the post's four statistics appear in repo or site;
  site showed 0 bot alerts in its rolling 24h counter at 2026-11-23 ~03:57 UTC; no "85+" threshold or "passed every check" state exists in the open rules (bands are 80/60/40).

## Token state at the moment the post was published (2026-11-21 21:37 UTC) — GeckoTerminal hourly candles (price × 1e9)
- BartCoin: already ≈ $1.5K (first hourly close below 10% of on-chain alert-time mcap: 2026-11-21 10:00 UTC, i.e. ~11.5 h BEFORE the post).
- PUNANI: 21:00 candle O $1.005M / L $656K / C $720K, falling; $577K at 22:00; $1,773 by 2026-11-22 00:00 (≈2.4 h after the post).
- MAYA: 21:00 candle O $1.61M / L $867K / C $986K, falling; $227K at 2026-11-22 01:00; ≈$1.6K by 04:00 (≈6 h after the post).
