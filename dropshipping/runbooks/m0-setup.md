# Runbook: M0 setup (draft; instructions open only after the accountant's answer)

Each step below is an instruction with its Right-For-You check. Steps marked **held** stay withheld until the fact named in "Evidence" exists. Nothing here is a purchase yet.

## Step 0 (now): accountant questions — advised (see sweep 1 and the memo).

## Step 1 — business file in the mother's name (held: accountant's answer on structure and VAT)
```
Instruction:         Mother opens the business file (עוסק פטור unless the accountant says otherwise): VAT form 821, income tax 5329, National Insurance 6101, via the accountant or in person (S-41)
Who acts:            guardian
Legal and policy:    required before any card gateway (S-28, S-38); minor cannot hold it (S-40)
Cost:                external: accountant's fee (Unknown until quoted) + ₪0 state fees stated in sources; hours 2–4
Expected value:      unlocks card acceptance; without it PayPal-only checkout
Reversible?          partly (closing a file is paperwork)
Evidence:            Observed S-21, S-40, S-41; VAT treatment Unknown → held
What makes it wrong: accountant advises a different structure, or VAT at 18% on US sales makes the model unviable at the planned margins
Cheaper alternative: start with PayPal-only checkout and no business file: not advised, because PayPal holds (S-11) and no card acceptance halve conversion, and Israeli law requires registration before the first sale (S-40)
Verdict:             advise with conditions → held until Step 0 answer
```

## Step 2 — Shopify account in the mother's name, operator as staff (held: Step 1 done)
```
Instruction:         Mother creates the Shopify account (owner, billing, payouts) on the $1/month × 3 months offer (S-03), Basic plan; adds the operator as staff with full store access (S-52)
Who acts:            guardian creates; operator builds pages
Legal and policy:    owner must be 18+ (S-01); staff may be a minor (S-52, community reply)
Cost:                external $1/mo for 3 months, then $39/mo; ledger after: $1 / $2,000
Expected value:      store exists; needed for every later step
Reversible?          yes (cancel before month 4)
Evidence:            Observed S-01, S-03
What makes it wrong: Step 1 not done (gateway cannot be connected); or operator time < 5 h/week for page building
Cheaper alternative: none cheaper than $1
Verdict:             advise with conditions → held until Step 1
```

## Step 3 — gateway (held: Step 1 done; Grow's answer on new exempt dealers)
```
Instruction:         Mother applies to Grow (or the provider that confirms acceptance of a new עוסק פטור in writing) and connects it in Shopify Payments settings; PayPal business account added as the second method
Who acts:            guardian
Legal and policy:    adult signatory + business number (S-37, S-38)
Cost:                external ₪59–69/mo (≈ $19–22) + 0.75% + 0.6% + Shopify 2%; ledger after ≈ $23 / $2,000
Expected value:      card acceptance in the US (most buyers) vs PayPal only
Reversible?          yes (monthly)
Evidence:            Observed S-37, S-38; acceptance of a new exempt dealer Unknown → held
What makes it wrong: provider requires עוסק מורשה or a terminal; then compare Hyp/Tranzila quotes
Cheaper alternative: PayPal only ($0 fixed, ~8.9% variable, 21-day holds): acceptable for tranche 1 only
Verdict:             advise with conditions → held
```

## Step 4 — AutoDS trial and supplier link (held: Step 2 done; candidate SKUs from the scan)
```
Instruction:         Mother opens AutoDS on the $0.99 trial (S-04), connects the store, no add-ons (non-refundable, S-05); operator imports only the scanned candidate SKUs from US-warehouse suppliers
Who acts:            guardian opens; operator operates under her login with her knowledge
Legal and policy:    18+ (S-05)
Cost:                external $0.99, then plan ≈ $26.90–39.90/mo (S-24, secondary); ledger after ≈ $25
Expected value:      automated fulfillment from day one (law 16)
Reversible?          partly: cancel within 24 h of a monthly charge for a refund (S-05)
Evidence:            Observed S-04, S-05; plan price Unknown on the live page → mother reads it
What makes it wrong: no candidate SKU has a US-warehouse supplier reachable through AutoDS; then Zendrop/Spocket app instead
Cheaper alternative: Zendrop Flex $29 or Spocket $39.99 if the chosen supplier is there (S-56, S-59)
Verdict:             advise with conditions → held
```

## Step 5 — tracking and one real order (held: Steps 2–4)
Facebook & Instagram app, Conversions API on, Pixel on (S-86); test purchase visible in Events Manager and Shopify once each (rule T1); one real sample order of the first candidate to a US address through the supplier to measure delivery days and landed cost (overlay §8 day 1). Cost: sample ≤ $40. M0 external cap check: $1 + $23 + $25 + $40 + domain ≈ $15 = ≈ $104 ≤ $300.

## Step 6 — store policies before any ad
Delivery time on product page = supplier's per-SKU stated days + 2 (S-34, S-56); refund within 7 working days of cancellation (S-34); no imported reviews (S-36); no "was" prices (D3); AI visuals labeled (D1).
