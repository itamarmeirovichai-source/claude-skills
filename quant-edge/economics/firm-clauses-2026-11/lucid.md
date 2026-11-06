# Lucid Trading — clauses (Rules Keeper, 2026-11-06) — SNIPPET / INHERITED ONLY

**lucidtrading.com returns HTTP 403 from this environment (D-007). Nothing was fetched from the firm's own site and no route around the block was tried.**
Note for the Director: the 2026-10-11 program read Lucid's help center on a separate host (support.lucidtrading.com). Per instruction it was not tried
today; whether that host counts as "the blocked site" is a Director decision. Until then every Lucid cell is S (snippet) or U (unknown).

## Sources
1. Inherited, page-level on 2026-10-11 (support.lucidtrading.com, quoted in `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-firms/clauses-futures.md` §4):
   - "Automated trading systems and trade copiers are permitted. All automated activity must comply with Lucid Trading rules. Traders are fully responsible for any software errors, malfunctions, or unintended outcomes."
   - "HFT is strictly prohibited." Microscalping: "You will be flagged if: More than 50% of your profits are generated from trades held for 5 seconds or less".
   - Hedging: "strictly prohibits all forms of hedging, including ... Hedging across multiple accounts held by the same user · Hedging between different users' accounts · Hedging between different firms or funded platforms".
   - "Up to 10 active evaluation accounts per household or family ... Up to 5 active funded accounts per household or family." "Up to 5 active LucidLive accounts per household or family."
   - "Not allowed on Daily — Trading red folder news on the LucidDaily is a hard breach. Allowed on Flex, Pro and Direct".
   - "All live transitions occur at the discretion of the Lucid risk team." "Traders may hold positions until 4:45 PM EST on Tradovate Live accounts, or 4:15 PM EST on Rithmic Live accounts".
   - Lucid ToS: never read (blocked in October too).
2. Third-party snippet, 2026-11-06: tradetanto.com "Lucid Trading Rules Explained" ("Last updated November 4, 2026"), WebFetch summary archived at
   `~/quant-edge-data/firm-pages/2026-11-06/lucid/SNIPPET-tradetanto-rules-2026-11-04.txt`. Same automation, caps, hedging and microscalping rules; adds:
   - LucidDaily funded news window: flat "one minute before through one minute after" any US high-impact red-folder event (hard breach).
   - Hours: close by 4:45 PM EST (auto-flatten), resume 6:00 PM EST; no overnight on Live.
   - New invite-only plan LucidMaxx; LucidScale DLL (60% of peak EOD balance); payouts min $500; 5 payouts before Live on Pro/Flex/Direct.
   - Live move: one Live account per funded account with ≥ 1 payout; remaining sim accounts closed; auto-move after 24 h without a choice; Live starts at $0.
3. WebSearch 2026-11-06 (crosstrade.io, traderspost, tradingfunder.com ...): consistent with 1–2; none from Lucid's own pages.

## Not known
Owner/entity, ToS text, restricted countries (Israel), payout rails, platform/API fees, inactivity rule, VPS/remote-signal policy. All asked in `letters/lucid.md`.
