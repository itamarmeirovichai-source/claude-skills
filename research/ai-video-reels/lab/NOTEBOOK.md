# Lab notebook

Every entry has a date, an experiment, a finding, the supporting number and a decision. Reports are appended automatically by `lab.py report`.

### 2026-10-07 · setup
- Protocol, hypotheses H1–H6 and caps written **before** any generation (PROTOCOL.md).
- Budget: lab cap $45; gates at $10 / $20 / $35 / $45.
- Endpoints verified in Higgsfield docs: Seedance 2.5 (i2v/t2v/ref), Kling 3.0 (pro i2v, std t2v), Hailuo 2.3 (std i2v/t2v), Marketing Studio Flare, Soul v2.

### 2026-10-07 · run 1 (stopped before the $10 gate)
- **Pricing finding:** `/estimate` returns only a pricing *description* for token-priced models (Flare, Seedance 2.5). hfgen counted them as $0 in dry-run. Fixed on the research branch by `price_from_description` (per-second video price, $0.30 fallback for a 2k image).
- **Seedance 2.5 at 480p is $0.2056/s ≈ $1.03 per 5 s clip** (token formula from the API). The E01 cap assumed far less. Real E01 = Kling $5.71 + Hailuo $1.90 + Seedance $8.22 ≈ $15.7, above the original $12 cap (since re-budgeted to $13; the full Seedance arm still exceeds it).
- **E00:** 5 assets, 1 take each (not 2). A1 TIDEWATER can: text perfect on take 1 (Flare, high, 2k). Flare charge is not reported by the API; booked at a $0.30/take ceiling → $1.50 (E00 cap is now 1.5). Real charge: check console Billing.
- **E01 partial:** Kling 3.0 Pro + Hailuo 2.3 arms, 16/16 completed, $7.44. Seedance arm NOT run (would cross the gate and the cap).
- Spend: **$8.94 / $45**. Not blinded yet: blinding waits for the Seedance decision so all arms are scored in one blind pass.
- **Decision needed (Itamar):** run Seedance arm (all 8 = $8.22, or a subset), then blind + score E01.
