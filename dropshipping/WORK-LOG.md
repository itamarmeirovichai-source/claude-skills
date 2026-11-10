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
