# WORK-LOG

## 2026-11-10 — turn 1 — Phase 0
- Repo had no `dropshipping/` folder; program started fresh on branch `claude/charming-cori-l1zixh`.
- Fetched 36 sources (free). Primary pages that refused: gov.il, kolzchut, Meta Business Help (JS-only body), Namecheap, Triple Whale, Higgsfield pricing (images), FedEx PDF. A Playwright attempt to render bot-protected pages was refused by the session permission policy; not retried.
- Built `phase0/goal_math.py`: breakeven ROAS 1.80 under stated assumptions; $200k/month needs ≈ $91k ads and ≈ $182k working capital at a 21-day hold; compounding outcome dominated by ROAS decay k, which has no source and becomes the M2 measurement target.
- Frame frozen, council held, ladder frozen with three changes (gateway + FTC delivery disclosure in M0; 60-day no-order stop; k measured at M2).
- Operator message mid-turn: destination market = US; asked whether to buy anything. Added US constraint rows S-34–S-36. Answer: nothing to buy yet.
- Wrote all deliverable files, checkpoint, memo. Spend: $0.

## 2026-11-10 — turn 2 — Phase 1 sweep 1
- Operator answered: 15 years old, mother to hold accounts, adult card + PayPal exist, 10–15 h/week; did not understand "רו"ח" (explained).
- Sweep 1 (finance, payments, registration, US tax and duties): 16 new sources (S-37..S-53), 4 new primary (Allpay listing, CDTFA, CBP interim final rule via pdftotext, Payoneer page). Federal Register HTML redirected to an unblock page; PDF read locally instead. Allpay listing rate-limited once (429), succeeded on retry.
- Findings: card acceptance from Israel needs a registered business and an adult signatory; Grow has the only published fee stack; exempt-dealer ceiling ≈ $3.2k/month revenue; VAT on US sales by an authorized dealer unresolved (0% vs 18%, breakeven ROAS 1.80 vs ~2.45); US postal duties are remitted by carriers or qualified parties and not collected from addressees under the 2026 CBP rule (first draft misread the old-process sentence; corrected same turn); suppliers restricted to US-warehouse or DDP.
- Memo, frame addendum, curriculum, checkpoint updated. Spend $0.

## 2026-11-10 — turn 3 — Phase 1 sweep 2
- Operator instruction: continue automatically; stop only for a question, needed information, a purchase, or a limit risk. Recorded.
- Sweep 2 (products and suppliers for US delivery): 20 new sources (S-54..S-73), 12 primary. Refusals: AutoDS supplier-regions article (404), CJdropshipping (bot validation), Amazon policy (login), Ad Library UI (403), voc.ai (500).
- Outputs: supplier route table, exclusions (Amazon, China-direct, blended estimates), category exclusions, 5 candidate families, runbook `runbooks/ad-library-scan.md` for the operator ($0), category return allowances replacing the flat 8%.
- Sweep 3 (Meta Ads mechanics): 16 new sources (S-74..S-89), 6 new primary (developer docs, ad standard, newsroom). Insights-parameters doc 404; Shopify data-sharing page empty; learning-stage API doc not found. Rules T1–T2, C1, L1–L2, S1, H1–H4, A1 written into the sweep for the registry.
- Sweep 4 (creative, statistics, AI tooling): 13 new sources (S-90..S-102), 4 primary. Computed the two-tranche stop rule in `phase1/test_stop_rule.py` (T1 $120 ≥5 purchases, T2 $120 ≥3; P(pass|good) 0.77, P(pass|bad) 0.07). Canva terms 403, Adobe guidelines 404, FTC FAQ truncated at 100k chars.
- Tooling unit: official Meta ads MCP (Jul 2026) and Shopify Dev MCP identified as first-party; 7 GitHub candidates vetted by README (two rejected for third-party credential paths or scraping, one unreadable); nothing installed. P- entry template and M0 runbook (held) written. Memo rewritten as the Phase 1 report. Program now blocked on operator inputs (candidate table, accountant answers). Spend $0.
- Phase 3 harness built ahead of data: `phase3/reconcile.py` (8 checks) + self-test with planted fake order, future leak, duplicate; placebo clean; exit codes for CI-style use. Runbook `daily-numbers.md`. Operator asked whether they can shut the computer: yes, cloud session; recorded.
- Stop reason: Phase 2 needs the operator's candidate table and the accountant's answers (allowed stop under §11.5).

## 2026-11-10 — turn 4 — program-side candidate pass
- Operator rule: program does what it can, operator the remainder. Ad Library (403), CJ (bot wall), Zendrop/Spocket (login), TrendTrack article (404 at first URL, found at second), Motion (no workspace) all unreachable to the program.
- Built `sweeps/candidates-2026-11-10.md`: 12 candidates from 5 vendor trend lists after exclusions; "Roha Home" advertiser verified (site + Trustpilot), "Petzrella" not found; Doba shows a US-shipping elevated bowl. Lithium exclusion refined (installed small cells allowed). Sources S-109..S-116. Spend $0.
- Operator: continue automatically, table later. Built `phase1/unit_economics.py` (per-row calculator; breakeven band now 2.3–3.6 with category refunds and VAT scenarios; memo corrected). Sweep 5 failure modes: 11 new sources (S-117..S-127), FTC report read via pdftotext; Visa page 404, Moneris PDF 403, Square article missing, PayPal US legal pages empty, Shopify IP page 404. Rules FM1–FM7.
- Sweeps 6–7 (consumer psychology; copy and landing pages): 17 new sources (S-128..S-145), 6 primary incl. PNAS, JCP, PLOS ONE, Baymard, Google/Deloitte, Spiegel (pdftotext). Rules LP1–LP6; price criterion ≥ $49 added to candidates and memo.
- Runbooks written without research: store-policies.md (FTC-compliant drafts), ad-brief-template.md, cs-templates.md (10 tickets), accountant-email.md (Hebrew). Depth audit added to checkpoint: statistics and AI tooling below the 15-source minimum; top-up queued.
- Top-up: statistics (S-146..S-155) and AI tooling (S-156..S-165); both areas now at depth. Rules ST5–ST7, TL3–TL6. Nothing left that needs no operator input; program paused on the candidate table and the accountant. Spend $0.

## 2026-11-11 — turn 6 — program fills the candidate columns
- Operator: "do it yourself". Ad Library still 403; Doba/Eprolo not indexed by search but direct product pages show US stock and delivery days with prices behind free sign-up; sale prices gathered from Chewy, Target, Walmart, Fruugo, Grove, two dropship-style stores (Taavita $96.95 feeder; zyrestore $18.97 grinder). One host (candlewarmersshop.it.com) not resolvable from the session network; one store returned 402.
- Result: price test LP4 leaves 3 passing rows, 2 bundle-only, 1 design-led; 6 drop. Operator task reduced to 6 Library clicks. Sources S-166..S-180. Spend $0.
