# Runbook: M0 setup, US path, Florida (rewritten 2026-11-11; supersedes the Israeli path)

Each step is an instruction with its Right-For-You check. **Held** steps wait for the fact named in "Evidence". Nothing here is a purchase yet.

## Step 0 (now): facts answered 2026-11-11 (Florida; SSN and US bank in the mother's name; store independent of the family business). Two professionals: (1) the family's immigration attorney confirms, in one sentence, that the E-2S spouse owning and running a small online store is fine (USCIS: employment authorized incident to status, S-187); (2) a US CPA chooses sole proprietorship vs single-member LLC for that state and sets up sales-tax registration. Email draft: `runbooks/accountant-email.md`. Cost: $0 for the questions; a CPA consultation is a ledger line only after a quote.

## Step 1 — business form and numbers (held: Step 0 answers)
```
Instruction:         Mother registers as the CPA advises: Florida sole proprietorship with a fictitious name (~$50, Sunbiz) or single-member LLC ($125 + $138.75 annual report, secondary S-190; Sunbiz pages refused); free EIN from the IRS; Florida sales tax registration (online or DR-1, S-196) before the first sale; Annual Resale Certificate for supplier purchases (S-197)
Who acts:            guardian
Legal and policy:    E-2S employment authorized (S-187); Schedule C taxation (S-189); physical nexus in the home state (S-194)
Cost:                external: ≈ $50 (sole prop + fictitious name) or ≈ $264 first year (LLC); ledger line before paying; insurance for P-0001 is a separate line later
Expected value:      unlocks Shopify Payments and a bank account in the business's name
Reversible?          partly
Evidence:            Observed S-187, S-189, S-196, S-199; fees secondary (S-190) → held only on the attorney's one line and the CPA's entity choice
What makes it wrong: attorney advises against self-employment on E-2S; or the CPA prefers running the store under the existing E-2 business
Cheaper alternative: sole proprietorship at $0 if the CPA agrees liability is small at this scale
Verdict:             advise with conditions → held
```

## Step 2 — Shopify account, mother as owner, operator as staff (held: Step 1)
Shopify $1/month × 3 months (S-03), Basic; Shopify Payments activated with the mother's SSN/ITIN, date of birth, US address and US bank account (S-191); operator added as staff with full access (S-52). Cost $1. Reversible.

## Step 3 — payments (held: Step 2)
Shopify Payments as primary (2.9% + 30¢ on Basic, no third-party fee, S-03/S-26); PayPal US business account as second method (3.49% + 49¢ Checkout, S-192). No Israeli gateway. Cost $0 fixed.

## Step 4 — supplier accounts and real landed costs (held: Step 2)
Free sign-ups on Doba and Eprolo (US stock shown publicly, prices on sign-up, S-166/S-167) and the AutoDS $0.99 trial (S-04/S-05, no add-ons). Replace the provisional landed costs in P-0001..P-0004, rerun `phase1/unit_economics.py`, re-commit the registry.

## Step 5 — tracking and one real order (held: Steps 2–4)
Facebook & Instagram app with Conversions API on (S-86); test purchase visible once in Events Manager and once in Shopify (rule T1); one sample order of P-0002 to the home address to measure delivery days and packaging. Cost ≤ $40. M0 external estimate (Florida): $1 + $0.99 + ≤ $40 + domain ≈ $15 + $50 (sole prop) ≈ $107, or + $264 (LLC) ≈ $321. The LLC path exceeds the $300 M0 cap by ≈ $21 and needs an explicit ledger decision by the operator and mother before Step 1.

## Step 6 — store policies and sales tax before any ad
Policies from `runbooks/store-policies.md`; Shopify Tax enabled for Florida after registration (6% + county surtax by delivery address, S-196; S-193); delivery time per SKU (S-56); no imported reviews (S-36); no "was" prices (D3); AI visuals labeled (D1).
