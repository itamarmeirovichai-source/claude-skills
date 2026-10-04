# PumpWatch red team: how a fraudster beats each signal

> **Date:** 4 October 2026, against engine core `e7a145f`.
>
> Team C ran every tactic marked **[demo]** against the real code, using default `Config`.
> - The demo scripts are in the QA session's scratch space.
> - The numbers below are what they printed.
> - Tactics marked **[QA ✓]** were also reproduced by the head of QA, or are pinned by a test.
>
> **Likelihood:**
> - **High:** cheap, already common in 2024–25 ramp-and-dump schemes.
> - **Medium:** needs some effort or money.
> - **Low:** rarely worth it.

## Headline: a full pump that never alerts

A 2.41x ramp-and-dump with **48 copy-paste shill accounts** produced **0 alerts** (peak score 43.75, families = `social` only). The fraudster made three cheap moves:
1. **A press release every trading day.** Wire PRs cost about $300–1,000 each.
2. **One day above +25% every ~20 sessions.** This breaks S2's "no single big jump" rule.
3. **No dilutive filing within 120 days**, and no broker feed.

The social signals alone exceed the 35 threshold, but the two-family rule blocks the alert. Without the PRs, the same pump alerts at **76.8**. **[demo]**

The engine's convergence rule is its strength against real news. It is also its single point of failure: **remove one family cheaply and nothing fires.**

---

## S1: abnormal dollar volume without news

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S1-1 | **A press release as cover.** File any `PR`/`NEWS`/`8-K`/`6-K` on the spike day or the day before. The news check only looks at the form, never the content. 2024–25 small-cap and ADR pumps routinely ran paid wire releases ("LOI signed", "AI partnership", "corporate update"). | **High** | [demo] A 40x spike gives 0.943; with a PR the same day or the day before it gives `None`. A 10-day pump gets 10/10 S1 hits without PRs and **0/10 with daily PRs**. [QA ✓] pinned by `test_news_filing_on_spike_day_vetoes_s1_today`. | News should *damp* S1, never veto it: multiply strength by about 0.5. Only substantive 8-K items (2.02 results, 1.01 material agreement with a named counterparty) may suppress. Add a sub-signal: "spike coincides with a press release from a low-tier wire" or "3 or more PRs in 10 days". |
| S1-2 | **Stay just under 5x.** Spread the buying so no day crosses the trigger. | **High** | [demo] 20 days at 4.9x move about $780k of extra volume with **0 hits**. | A cumulative excess-volume test, for example Σ(ratio−1) over 10 days ≥ 25, or a 5-day mean ratio ≥ 3x. |
| S1-3 | **Build the baseline gradually.** The baseline is the median of the last 60 bars, so it rises with the ramp. Wash and matched trading by "teacher" groups does exactly this. | **Medium-High** | [demo] Volume growing ×1.05 per day for 60 days reaches **19x the original with 0 hits**. Only ×1.08 or more trips it. After 31 days held at 10x, a spike of 40x the original gives `None`. | A second, frozen long baseline (median of 250 bars excluding the most recent 40), plus a slope test on log(volume). |
| S1-4 | *(False positive, not evasion)* S1 uses **dollar** volume, so a rising price alone inflates the ratio. A 3x volume day during a rally reads as "5.6x". | — | [demo] | Use share volume or float turnover. Report price and volume effects separately. |

## S2: quiet accumulation

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S2-1 | **One day above +25%** inside the window vetoes S2 for 20 sessions. A single gap-up day is easy to paint. | **High** | [demo] The reference climb fires at 0.613; with one +26% day it gives `None`. | Winsorise the largest return, or allow one outlier day. Test the trend with a regression slope and R², not a hard max-day veto. |
| S2-2 | **A choppy climb** with fewer than 55% up days. Flat (no-trade) days count as "not up". | **High** | [demo] Alternating +5.5% and −1% gives +54% gain at 48% up days, `None`. Alternating +4.5% and unchanged gives +55%, `None`. | Replace `up_share` with the sum of positive returns as a share of total absolute return. |
| S2-3 | **A slower climb**, under +30% per 20 sessions. | **High** | [demo] A **+65% climb over 60 sessions: 0 hits.** | Evaluate 20-, 40- and 60-session windows with thresholds scaled to window length. |
| S2-4 | **Pre-load volume** 40 days before the climb, to lift the "prior" median. | **Medium** | [demo] Gives `None`. | Use the same frozen long baseline as S1-3. |

## S3: suspicious filings

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S3-1 | **Title wording outside the list.** The list is matched as plain substrings, and the `" ai "` entry needs spaces on both sides. 2025 shells used "digital asset treasury" and "AI-powered". | **High** | [demo] All of these gave `None`: "AI-powered", "AI, quantum", "A.I.", "digital asset treasury", "Bitcoin treasury", "Web3/DeFi", "share consolidation 1-for-50", "rebranding and symbol change", "resignation of CEO / new directors", "receivership", "convertible debenture", "equity line of credit". | Tokenise on word boundaries (`\bai\b`, `a\.?i\.?`). Add synonyms: treasury strategy, digital asset, bitcoin, consolidation, symbol change, receivership, debenture, ELOC, securities purchase agreement, resignation. Use 8-K item numbers 3.02, 5.01, 5.02, 5.03 instead of titles. |
| S3-2 | **Forms outside `DILUTION_FORMS`.** | **High** | [demo] All gave `None`: S-3ASR, S-1MEF, 424B2, 424B7, 1-A/A, 253G1, S-4, F-3ASR, DEF/PRE 14C (reverse-split information statements), SC 14F1 (change of control), 10-12G. | Match by prefix family (`S-1*`, `S-3*`, `F-1*`, `F-3*`, `424B*`, `1-A*`, `253G*`). Add 14C, 14F1 and 10-12G. |
| S3-3 | **File the dilution more than 120 days ahead.** A shelf or S-1 goes effective months before the pump. | **Medium-High** | [demo] Filed 120 days before fires; 121 days before gives `None`. | A 365-day lookback for registration forms. Weight by the effective date and 424B takedowns. |
| S3-4 | **Keep the shell "non-dormant"** with trivial filings (NT 10-K, 15c2-11 paperwork). | **Medium** | [demo] 2 years of silence then an 8-K scores 0.4. An NT 10-K every 300 days gives `None`. A trivial 8-K 200 days before the real one also gives `None`, because the gap is only measured before the *first* filing in the window. | Count only substantive filings (10-K/10-Q/20-F) for dormancy. Use the largest gap in the last 365 days. |
| S3-5 | *(False positive)* Routine S-8 or Form D filings and ATM 424B5 takedowns fire S3. **One S-8 keeps the corporate family on for about 87 sessions.** | — | [demo] | Weight S-8 and D near 0 unless the registered shares exceed about 10% of float. Give full weight only to micro-caps (< $300M), OTC names or ADRs. |

## S4: hype burst

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S4-1 | **Slow mention ramp.** The 2025 WhatsApp and Telegram "group warm-up" over weeks raises the 30-day mean, so the 5x ratio never trips. | **High** | [demo] The greedy ramp that never fires: 20 posts per day needs 17 days, 100 per day needs 28, 1,000 per day needs 43. With a flat background of B posts per day, a blast of up to 5B−1 is invisible. | Compare against a 90-day *median* baseline that excludes the last 14 days. Add a 7-day-sum growth test and an absolute floor on the number of hype posts. |
| S4-2 | **Dilute with neutral posts.** The gate is the *mean* hype score. | **High** | [demo] 3 posts at 1.0 plus 7 neutral average 0.30, which evades. | Gate on the count or share of posts with hype ≥ 0.5 (for example at least 5 posts or at least 20%). |
| S4-3 | **Lexical evasion.** Synonyms, leetspeak (`t0 th3 m00n`), s p a c e d text, 🌕⬆️🤑, image-only posts, and the 2025 "professor's team… follow the plan at 10:30" adviser tone. LLM-written copy is the norm. | **High** | [demo] All scored **0.000**, against 1.000 for the control. | A leetspeak map and spaced-letter collapsing. Add adviser and signal-group phrases (professor, teacher, assistant, VIP group, "follow the plan", "entry price", a time-of-day call). Plug in the `HypeScorer` LLM classifier. Use OCR for images. |
| S4-4 | **Invisible characters and homoglyphs.** Zero-width spaces, soft hyphens, Cyrillic `о`. | **High** | [QA ✓] FINDINGS **QA-6**: "to the m​oon" scores 0.0. | Strip Cf characters (QA-6 fix) and apply a UTS#39 confusables skeleton. |
| S4-5 | **Weekend blasts.** S4 is only evaluated on trading days, against that day's posts. | **Medium-High** | [QA ✓] FINDINGS **QA-4**. Before a Monday holiday the Tuesday S5 window (Sun–Tue) also misses a Saturday blast: [demo] S4 = 0 and S5 = 0. | QA-4 fix: score every post since the previous session. |
| S4-6 | **Keep the ticker out of `Post.tickers`.** Write `HYPE`, `$ HYPE`, `#HYPE`, `＄HYPE`, `$НYPE` (Cyrillic Н), or a company name instead of a cashtag. | **High** | [demo] All extract `()`. [QA ✓] QA-6 and QA-17 cover `＄`, ZWSP and Hebrew prefixes. | Normalise (QA-6) plus a confusables skeleton before extraction. Accept `#TICK`, `$ TICK`, and bare upper-case tokens or company names that are in the known universe. |
| S4-7 | **Private-only coordination.** The pitch lives entirely in closed WhatsApp or Telegram groups, so public S4 and S5 see nothing. This is the dominant 2025 pattern. | **High** | By design, public data cannot see it. | Rely on footprints that cannot be hidden: S6 broker flow, S7 reports, and S1/S2. When public social data is empty but a micro-cap shows first-timer flow, raise S6 and S7 weight or treat social as unavailable (renormalise) rather than zero. Never join private groups (red line). |

## S5: coordinated copy-paste promotion (4-word shingles, Jaccard ≥ 0.6, at least 3 authors, 3-day window)

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S5-1 | **Paraphrase per account** (LLM "spinning"). | **High** | [demo] Evenly spaced word edits needed to drop below 0.6: 10 words needs 2, 20 words needs 2, 40 words needs 4 (random edits: 1, 2, 3). Inserting "bro" every 4 words gives J = 0.125; swapping adjacent words gives 0.224. [QA ✓] a one-word change in an 18-word pitch gives 0.55 (**QA-20**), and 2 edits in 19 words give 0.36. | Character 5-gram shingles (QA-20 fix: one-word paraphrase goes from 0.55 to 0.78). Then MinHash plus *containment* (shared / min) at about 0.4. Cluster on shared URLs, invite links, and ticker-plus-price-target combinations. Add an embedding-similarity option for spun copy. |
| S5-2 | **Zero-width characters and homoglyphs** inside words. | **High** | [demo] One ZWSP every 4th word gives J = 0.0. Six Cyrillic `о` give 0.5. [QA ✓] **QA-6**. | Normalise inside `shingles()` (QA-6 fix) plus a confusables skeleton. |
| S5-3 | **Fewer than 3 accounts per cluster,** or one handle reused across sources. | **Medium-High** | [demo] 2 accounts × 5 copies each gives `None`. One handle on x, reddit, telegram and stocktwits gives `None`, because authors are counted by handle string. | If one cluster has at least 6 messages, fire at reduced strength. Count `(source, author)` pairs, and count cross-source copies by one handle as amplification. |
| S5-4 | **Space posts beyond the 3-day window.** | **Medium** | [demo] 6 accounts posting one copy every 3 days get 0 hits on every day. | A rolling 14-day window with time-decay weights. |
| S5-5 | *(False positive)* **Short generic replies** cluster ("What happened?", "Thanks!"). | — | [QA ✓] **QA-16**. | A minimum message length (QA-16 fix). |

## S6: broker flow (customer data)

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S6-1 | **Split victims across brokers.** Groups tell victims to "use any app". | **High** | [demo] 80 new buyers at one broker fires; the same 80 spread over 5 brokers (16 each) gives `None`. | Pool counts across customers through a hashed consortium feed (aggregate counts only, no client identities). Lower `flow_min_new_buyers` when at least 50% are first-timers. |
| S6-2 | **Trickle in under the minimum.** | **Medium** | [demo] 19 new buyers per day for 10 days: 0 hits. | Add a rolling 10-day sum test next to the daily test. |
| S6-3 | **Seed the baseline with mule accounts.** | **Medium** | [demo] 6 mule buys per day for 20 days, then a burst of 29, gives `None`. | Use a 90-day median baseline that excludes the last 20 days. Weight first-time micro-cap buyers more. |
| S6-4 | *(False positive)* **Cold start.** The first day of a feed fires on every busy ticker. | — | [QA ✓] **QA-10**. | Require a minimum baseline history (QA-10 fix). |

## S7: victim reports

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| S7-1 | **Frame a rival with a fake report.** Competing promoters and short-and-distort crews could submit reports to trigger an alert (and a broker restriction) on someone else's ticker. | **Medium** | [demo] A hype-only ticker scored 41.18 with no alert. **One fake report** raised it to 44.12 and **produced an alert**, with families client and social. [QA ✓] 8 shill posts score 53.85 with 0 alerts; adding one report gives an alert with families `('client', 'social')`. | S7 must not count toward `min_families` until there are at least 3 independent reports from verified customers. De-duplicate by reporter, rate-limit new accounts, and keep the weight low. |
| S7-2 | **Suppress reports.** Victims of private groups are told the drop is a "shakeout, hold". | **High** | Not testable in code. | Treat S7 as confirmation only. Never let its absence lower a score. |

## Cross-cutting tactics

| # | Tactic | Likelihood | Evidence | Counter-measure |
|---|---|---|---|---|
| X-1 | **Split the campaign across tickers.** 2025 groups rotate several ADR and small-cap names. | **Medium-High** | [demo] 4 tickers, each with 2 accounts, 4 copy-paste posts and 4.5x volume: **0 hits and 0 alerts on all of them.** | Cross-ticker clustering: the same template (cashtags are already stripped from shingles) or the same author set hitting more than one ticker within 7 days merges their evidence into a "campaign" object. |
| X-2 | **Time the families apart** so they never overlap within the 5-day memory. | **Low-Medium** | [demo] Moving the social blast 7 days after the spike drops the score from 77.7 to 51.8. Combined with S1-1 and S2-1, the families never meet. QA-21 shortens memory further over weekends. | Per-family memory (social 10 sessions, client 14 sessions, corporate already 120 days), or a campaign accumulator per ticker. Fix QA-21. |
| X-3 | **Cooldown abuse.** Trigger a weak decoy alert first; the real pump inside the 10-day cooldown is never surfaced. | **Medium** | [demo] A decoy on Monday (53.5) and the real pump on Thursday (68.75) produce **no second alert**. | Re-alert inside the cooldown when the score rises by at least 15 points or a new family appears. |
| X-4 | **The `min_families = 2` ceiling.** A social-only campaign can never alert, however strong. | **High** (follows from S1-1 and S4-7) | [demo] Peak 43.75 with 0 alerts. [QA ✓] 53.85 with 0 alerts. | Add a "watch" tier (not a broker alert) for S4 and S5 both ≥ 0.9 with at least 20 accounts. Or count S4 and S5 as separate families when their evidence is independent. |
| X-5 | **Ticker symbol change mid-campaign.** A name or symbol change resets every per-ticker baseline. | **Medium** | Inferred from the code: contexts are keyed by ticker string. | Key the history by a stable identifier (CIK/FIGI) and map old tickers to new ones. |

## Recommended order of work (impact divided by effort)

1. **Stop PR/NEWS forms vetoing S1** (S1-1). One line, and it closes the headline evasion.
2. **Text normalisation:** Cf-strip (QA-6), quote folding, confusables and leetspeak. Apply it in cashtags, hype and shingles.
3. **Character-gram plus containment near-duplicate detection** (QA-20, S5-1) and cross-ticker campaign clustering (X-1).
4. **Long frozen baselines** for S1, S4 and S6, plus cumulative-excess tests (S1-2, S1-3, S4-1, S6-2).
5. **Score weekend posts** (QA-4), and **re-alert on escalation** inside the cooldown (X-3).
6. **Gate S7 on corroboration** (S7-1) before any customer can submit reports.
7. **Add a regression test for each evasion as it is fixed.** Team C's demo scripts make good starting fixtures, so turn each into a `test_redteam_*.py` case.
