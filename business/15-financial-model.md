# 15 — Financial Model & Financial Control

**Authoritative source for prices, costs, margin thresholds, discount rules and spending
limits.** Runnable model: [`tools/financial_model.py`](tools/financial_model.py).

## 0. The honesty rule for this document

Every cost line is tagged:
- **[MEASURED]** — observed from a real invoice or a timed order. **Currently: none.**
- **[PUBLISHED]** — a published third-party rate (E-NN).
- **[ESTIMATE]** — our judgment, carrying an assumption ID.

**As of today, zero costs are MEASURED.** That is the most important sentence in this document.
The first task of [43](43-launch-plan.md) days 1–5 is to replace the estimates with measurements
from 10 self-funded production runs, before a customer is ever quoted.

---

## 1. Price list

| Item | Price | Status |
|---|---|---|
| Starter | $149 | Hypothesis (A-07) |
| **Standard** | **$279** | Hypothesis (A-07), D-04 |
| Portfolio | from $199/property, 5+ | **Hypothesis — do not quote before §6 is measured** |
| Rush (+48–72h) | +40% | Hypothesis |
| Extra concept | +$89 | Hypothesis |
| Arrival video add-on | +$79 | Hypothesis |
| Extra revision round | +$59 | Hypothesis |
| Extra caption language | +$29 | Hypothesis |
| Raw selected clips | +$49 | Hypothesis |

Anchoring context (E-31, publicly published): local videographers charge $150–$500 for a basic
60–90s walkthrough, $300–$1,500 for agent-led tours, +$225–$500 for drone, +$50–$200 travel,
with urban markets 20–40% higher. DIY AI tools are $10–$100/month (E-32).

---

## 2. Cost structure per Standard order ($279)

| Cost line | Amount | Tag | Basis |
|---|---|---|---|
| Generation (successful clips) | $6.00 | [ESTIMATE] A-09 | ~50s usable footage. E-22: Kling $0.09–0.14/s → ~$5–7 |
| **Failed generations** | $9.00 | [ESTIMATE] A-09 | Assumes **2.5 attempts per accepted clip**. This is the least-known number in the model |
| Music licence (amortised) | $1.70 | [PUBLISHED] E-18 | Epidemic Sound Pro $203.88/yr ÷ 120 orders/yr |
| Editing software | $0.00 | [PUBLISHED] D-08 | DaVinci Resolve free tier |
| Storage & delivery | $0.50 | [ESTIMATE] | Cloud storage, 30-day hosting, archive |
| Payment processing | $8.39 | [PUBLISHED] E-25 | Stripe 2.9% + $0.30 |
| Asset prep, QC, comms, revisions | $0.00 cash | [ESTIMATE] A-10 | **Founder time — costed separately in §3** |
| **Total cash cost** | **$25.59** | | |
| **Contribution margin (cash)** | **$253.41** | | **90.8%** |

### The three lines that matter and why

1. **Failed generations ($9.00)** is a pure guess (A-09). If the attempt ratio is 6:1 rather
   than 2.5:1, this line goes to ~$27 and margin drops to ~$235 — a 7% hit. **Material but not
   fatal.**
2. **Payment processing ($8.39)** is larger than the successful generation cost. Worth noting
   before anyone spends a week optimising model selection to save $2.
3. **Founder time is the real cost and it does not appear above.** See §3. Every intuition that
   says "reduce the AI bill" is optimising the wrong variable.

---

## 3. Founder time and effective hourly earnings

Estimated time per Standard order [ESTIMATE] A-10:

| Step | Minutes |
|---|---|
| Intake review, fact sheet check, rights check | 15 |
| Asset selection and prep | 20 |
| Brief and storyboard | 15 |
| Generation runs (attended portions) | 25 |
| Edit, captions, sound | 30 |
| **Accuracy review** ([26](26-property-accuracy-rules.md)) | 12 |
| **Quality review** ([27](27-quality-rubric.md)) | 8 |
| Exports (7 formats) † | 10 |
| Delivery message and guide | 8 |
| Revision handling (weighted: 35% × 25 min, A-11) | 9 |
| **Total** | **152 min ≈ 2.5h** |

**† [MEASURED 2026-09-17]** — a full 7-file render takes **~6 minutes of machine time,
unattended** (`tools/template_motion.py`, 369s on this hardware, synthetic source images). That
is not founder time: the step is close to fully automatable, and founder attention is closer to
**1 minute** — start the job, come back. Revise this line down once the pipeline is wired up.
**Time is the dominant cost variable, so converting founder minutes into machine minutes is worth
more than any saving on generation cost.** The other steps in this table remain estimates.

| | Value |
|---|---|
| Contribution margin | $253.41 |
| Founder hours | 2.53 |
| **Effective hourly earnings** | **$100.16/h** |

That is a viable rate for a solo operator — **conditional entirely on A-10 holding.**

### Sensitivity of the only variable that really matters

| Hours per order | Effective hourly |
|---|---|
| 1.5h | $168.94 |
| 2.0h | $126.71 |
| 2.5h | $101.36 |
| **2.53h (base)** | **$100.16** |
| 3.0h | $84.47 |
| 4.0h | $63.35 |
| 5.0h | $50.68 |
| 6.0h | $42.24 |

**The business is a time business wearing a technology costume.** At 6 hours per order the
effective rate approaches what a competent freelance editor charges, and the entire premise
collapses. This is why [14](14-offer-specification.md) §4 (scope control) and
[37](37-capacity-and-contractors.md) (capacity limits) are load-bearing documents, not
administrative ones.

---

## 4. Fixed monthly costs

| Item | Monthly | Tag |
|---|---|---|
| Music licence (Epidemic Sound Pro, annual) | $17.00 | [PUBLISHED] E-18 |
| AI generation base subscription | $35.00 | [PUBLISHED] E-21 (Runway Pro tier as a planning figure) |
| Cloud storage | $10.00 | [ESTIMATE] |
| Domain + hosting | $15.00 | [ESTIMATE] |
| Email + scheduling tools | $20.00 | [ESTIMATE] |
| Accounting | $20.00 | [ESTIMATE] |
| **Total fixed** | **$117.00/mo** | |

**Break-even volume: 1 Standard order per month** covers all fixed costs (in cash terms) with
$136 to spare. The fixed base is deliberately tiny — free tools chosen wherever suitable, per
the operating constraints. This is the single best structural feature of the business: **it
cannot bleed to death slowly.** It either sells or it stops, cheaply.

---

## 5. Acquisition economics

| Metric | Value | Derivation |
|---|---|---|
| Contribution margin per Standard order | $253.41 | §2 |
| **Break-even CAC** | **$253.41** | Cash-break-even, ignoring founder time |
| Break-even CAC including founder time at $50/h opportunity cost | $126.91 | $253.41 − (2.53h × $50) |
| **Target CAC** | **$75.00** | 3.4:1 contribution:acquisition on a **first order only** (D-12) |
| Target cost per qualified lead at 25% conversion (A-13) | $18.75 | $75 × 0.25 |
| Max acceptable cost per qualified lead before pausing | $30.00 | Guardrail ([31](31-experiment-design.md)) |

**No lifetime value is used anywhere in this model (D-12).** Every CAC decision is justified
against one order. If repeat purchase is later observed ([36](36-retention-plan.md)), the target
CAC may rise — but only using a measured repeat rate, never a forecast one.

---

## 6. Portfolio pricing — do not quote before measuring

The $199/property figure assumes template reuse cuts per-unit time from 2.53h to ~1.4h. **That
is unverified.**

| | Standard (1 property) | Portfolio (5 properties) if reuse works | Portfolio if reuse fails |
|---|---|---|---|
| Revenue | $279 | $995 | $995 |
| Cash cost | $25.59 | $95.00 | $128.00 |
| Contribution | $253.41 | $900.00 | $867.00 |
| Founder hours | 2.53 | 7.0 (1.4/property) | 12.65 (2.53/property) |
| **Effective hourly** | **$100.16** | **$128.57** | **$68.54** |

**The rule: no volume discount is quoted to any customer until at least one 5-property job has
been delivered and timed.** If reuse fails, the effective rate at $199/property is materially
*worse* than selling five Standard orders — which is the classic way service businesses grow
into losses. See [19](19-property-manager-sales.md).

---

## 7. Scenarios

Assumes founder time valued at $50/h opportunity cost for the profit line.

| | Conservative | Base | Optimistic |
|---|---|---|---|
| Orders/month (steady state) | 4 | 10 | 18 |
| Avg order value | $220 | $279 | $310 |
| Revenue/month | $880 | $2,790 | $5,580 |
| Cash costs (variable) | $96 | $256 | $470 |
| Fixed costs | $117 | $117 | $117 |
| Ad spend | $0 | $300 | $750 |
| **Cash profit before founder pay** | **$667** | **$2,117** | **$4,243** |
| Founder hours/month | 12 | 25 | 45 |
| **Effective hourly** | **$55.58** | **$84.68** | **$94.29** |

**Note the shape:** the optimistic scenario's hourly rate is only marginally better than base.
Volume alone does not fix the hourly ceiling — **only reducing hours per order does.** That is
the strategic implication of this whole model, and it points at templating, scope discipline,
and eventual contractor leverage ([37](37-capacity-and-contractors.md)), not at selling more.

---

## 8. Sensitivity analysis

Base = Standard order, $279, 10 orders/month. Single-variable shocks:

Figures below are the **output of [`tools/financial_model.py`](tools/financial_model.py)**, not
hand arithmetic. Re-run the script rather than trusting this table once any input changes.

| Shock | Margin/order | After refunds | Effective hourly | Verdict |
|---|---|---|---|---|
| **Base** | $253.41 | $239.46 | **$100.16** | — |
| Failed generations 3× worse (attempt ratio 7.5:1) | $223.41 | $209.46 | $88.30 | Tolerable |
| Revision rate 35% → 70% | $253.41 | $239.46 | $94.56 | Tolerable |
| Price cut to $199 | $175.73 | $165.78 | $69.46 | Survivable, not comfortable |
| Price cut to $149 | $127.18 | $119.73 | $50.27 | **Below tripwire** — a freelance editor's rate |
| Time per order 2.5h → 4h | $253.41 | $239.46 | $63.35 | **Serious** |
| Time per order 2.5h → 5h | $253.41 | $239.46 | $50.68 | **Business is not worth doing** |
| Refund rate 5% → 20% | $253.41 | $197.61 | $100.16 | Serious — but a *symptom* of a quality problem, not an independent variable |
| CAC $75 → $150 | $103.41 after CAC | — | — | Halves the acquisition ratio; still positive |
| **Compound bad case**: $199, 4h/order, 15% refunds, 5× attempts, CAC $150 | — | $130.88 | **−$4.78 net of CAC** | **Fatal — loses $19.12 per order** |

Refunds are modelled conservatively: full revenue reversal with production costs already sunk
and not recovered.

**The compound case is the real finding.** Every one of those four shifts is individually
survivable — none alone breaks the business, and each would look like an acceptable trade in
isolation. Together they turn a $100/hour business into one that pays $19 per order for the
privilege of doing the work. **Monitor the combination, not the components.** The tripwire in
§10 exists because no single dashboard number would catch this.

**Ranking of what to worry about, from this table:**
1. Time per order (A-10) — dominates everything.
2. Price realisation (A-07) — second.
3. Refund rate — third, and it is a lagging indicator of a quality problem, not an independent
   variable.
4. Generation failure rate (A-09) — **fourth, and much less important than intuition suggests.**

---

## 9. Cash management

| Rule | Value |
|---|---|
| **Payment terms — orders ≤$500** | 100% upfront before production begins. No exceptions |
| **Payment terms — orders >$500** | 50% deposit to start, 50% on delivery before files are released |
| Cash collection timing | Deposit at order; balance within 3 days of delivery |
| **Cash buffer target** | **3 months of fixed costs + 1 month of refund exposure = $351 + $140 ≈ $500 minimum** |
| Pre-revenue spend ceiling | **$400 total** before the first paid order (tools + domain + one month of subscriptions). If the business cannot start for $400, reconsider it |
| Ad spend rule | Never exceed 25% of trailing 30-day contribution margin. At zero revenue, the ad budget is the fixed experiment budget only ([31](31-experiment-design.md)) |
| Contractor spend rule | No contractor engaged until §11 gate is met |

---

## 10. When more sales would increase losses

This is the question most businesses never ask. Ours has four specific answers:

1. **Portfolio jobs priced on unmeasured reuse (§6).** If reuse fails, every additional
   5-property job earns $68/h instead of $100/h — growth that degrades the business.
2. **Rush orders beyond capacity.** The +40% rush fee is priced against *spare* capacity. Sold
   into a full week, it buys overtime at a discount to the stress it creates, and it raises the
   accuracy-incident risk, whose downside is unbounded.
3. **Any order below $149 after discounting.** At $120 with 2.5h of work, effective earnings fall
   to ~$38/h — below the value of the founder's time spent on validation instead.
4. **Selling to declined segments** ([08](08-segment-selection-matrix.md)). An S1 host with 8
   low-resolution photos generates 5+ hours of work and a likely refund. **Every such sale is a
   loss dressed as revenue.**

**The tripwire:** if trailing-10-order effective hourly earnings fall below **$60/h**, stop
selling and fix delivery. Do not sell more.

---

## 11. Financial rules

### Discounts
- **Default: no discount.** Negotiate scope, not price
  ([13](13-consumer-psychology-and-sales-method.md)).
- Maximum discount ever: **15%**, and only in exchange for something of value — a case study
  with named permission, a 5+ property commitment, or full prepayment on a portfolio order.
- **Never discount to close a hesitant buyer.** It teaches the customer the price is fiction and
  it selects for the customers most likely to demand revisions.
- **Price floor: $149.** Below this, decline the work.

### Rush fees
- +40%, capacity permitting. Never on a first order. Never if it would push another customer's
  delivery past its promised date — the existing customer's date is not ours to spend.

### Deposits and balances
- Per §9. Files are not released before the balance clears.

### Refund review
- Policy and process: [35](35-customer-operations.md). **Financial rule:** refunds are approved
  by the founder only, never by an agent (D-15), and every refund is coded to a cause
  ([41](41-measurement-definitions.md)). A refund for an accuracy defect is always granted
  without argument.

### Pausing an unprofitable product
Any product is paused when, over its trailing 10 orders:
- Effective hourly earnings < $60/h, **or**
- Refund rate > 15%, **or**
- Revision rate > 70%

Pause means: removed from the site, not sold in conversation, existing commitments honoured.
Restart requires a written change to scope or price and a fresh 10-order measurement.

---

## 12. Acceptance criteria for this model

Replace [ESTIMATE] with [MEASURED] on:
- [ ] Generation cost per order — from 10 real production runs
- [ ] Attempt ratio (failed generations) — counted, not estimated
- [ ] Minutes per order, per step — timed on every order from #1
- [ ] Revision rate — counted over 20 orders
- [ ] Refund rate — counted over 20 orders
- [ ] Portfolio per-unit time — from one real 5-property job

Re-run [`tools/financial_model.py`](tools/financial_model.py) after each replacement. **If
effective hourly earnings at measured values fall below $60/h, the price must rise or the scope
must shrink — before scaling acquisition, not after.**
