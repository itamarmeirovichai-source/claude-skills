# Runbook: M0 setup, US path (rewritten 2026-11-11; supersedes the Israeli path)

Each step is an instruction with its Right-For-You check. **Held** steps wait for the fact named in "Evidence". Nothing here is a purchase yet.

## Step 0 (now): three facts from the operator, then two professionals
Facts: (a) which state the family lives in; (b) whether the mother has an SSN or ITIN and a US bank account in her name; (c) whether a family E-2 business already exists. Professionals: (1) the family's immigration attorney confirms, in one sentence, that the E-2S spouse owning and running a small online store is fine (USCIS: employment authorized incident to status, S-187); (2) a US CPA chooses sole proprietorship vs single-member LLC for that state and sets up sales-tax registration. Email draft: `runbooks/accountant-email.md`. Cost: $0 for the questions; a CPA consultation is a ledger line only after a quote.

## Step 1 — business form and numbers (held: Step 0 answers)
```
Instruction:         Mother registers as the CPA advises: sole proprietorship (DBA if the state requires one) or single-member LLC in the home state; gets a free EIN from the IRS; registers with the state department of revenue for sales tax before the first sale
Who acts:            guardian
Legal and policy:    E-2S employment authorized (S-187); Schedule C taxation (S-189); physical nexus in the home state (S-194)
Cost:                external: $0 (sole prop, EIN) to ~$70–300 filing + annual fees (LLC, by state, S-190); ledger line before paying
Expected value:      unlocks Shopify Payments and a bank account in the business's name
Reversible?          partly
Evidence:            Observed S-187, S-189; state fees Unknown until the state is known → held
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
Facebook & Instagram app with Conversions API on (S-86); test purchase visible once in Events Manager and once in Shopify (rule T1); one sample order of P-0002 to the home address to measure delivery days and packaging. Cost ≤ $40. M0 external estimate: $1 + $0.99 + ≤ $40 + domain ≈ $15 + state fees (if LLC) ≈ $57–360 → the $300 M0 cap holds only on the sole-proprietor path or a cheap-fee state; an LLC in California breaks it and needs an explicit ledger decision.

## Step 6 — store policies and sales tax before any ad
Policies from `runbooks/store-policies.md`; Shopify Tax enabled for the home state after registration (S-193); delivery time per SKU (S-56); no imported reviews (S-36); no "was" prices (D3); AI visuals labeled (D1).
