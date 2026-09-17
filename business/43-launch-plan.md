# 43 — Launch & Expansion Plan

## The smallest thing that can produce real value and collect real money

> **One property. One customer. $279. Seven files. Five days.**

That is the whole business at minimum viable scale. Everything else in this system exists to make
that transaction repeatable, profitable and safe. **Nothing should be built that is not required
for that first transaction**, until that transaction has happened five times.

---

## The 30-day validation plan

### Days 1–5 — Verify and measure *(no customer contact)*

| Day | Action | Output | Blocks |
|---|---|---|---|
| 1 | **V-0**: read the 9 blocked primary sources ([42](42-validation-plan.md)) | Evidence upgraded to grade A; ⏳ claims released or removed | Everything |
| 1 | Engage a lawyer (customer agreement) and an accountant (entity, sales tax) | In progress | First paid order |
| 2 | **V-1 begins**: produce 3 practice packages | First time and cost data | — |
| 3 | **Competitor pricing sweep** ([11](11-competitor-analysis.md) V-1) | Real competitor pricing | Final price confirmation |
| 3–4 | V-1 continues: 7 more packages, including 3 difficult interiors | 10 packages | — |
| 5 | **Replace A-03, A-09, A-10 with measurements.** Re-run `financial_model.py` | Measured unit economics | **Pricing** |

**Day 5 checkpoint — the first honest decision point:**

| If | Then |
|---|---|
| Accepted-clip yield <1-in-4 | Switch to template motion. Re-price. Continue |
| Median time >3h and effective hourly <$60 | **Raise the price or shrink the scope before selling anything** |
| V-0.1 contradicts E-01 | **Stop. Re-run positioning and segment selection** |
| All clear | Proceed |

### Days 6–12 — Build the minimum

| Day | Action |
|---|---|
| 6 | Site: home, pricing, examples (illustrative, labelled), accuracy checklist, PM page, form |
| 7 | **AD-2 and AD-3 landing pages** ([34](34-website-specification.md) §5) |
| 8 | Stripe, order record, upload flow, Property Fact Sheet form |
| 9 | Run [40](40-testing-plan.md) §1–§15. **All 12 critical failures must clear** |
| 10 | Publish organic posts 1–8 ([29](29-content-calendar.md)) |
| 11 | Open 3 partner conversations ([33](33-partnership-plan.md)) |
| 12 | **Open for orders at full price** |

### Days 13–30 — Sell, deliver, measure

| Day | Action |
|---|---|
| 13 | **Set the Meta account spending limit to $300** (D-09), then launch AD-T1 |
| 13–30 | Organic daily. Target 20 qualified conversations |
| 13–30 | **Deliver every order. Time-log every step. Both gates, every time** |
| 15–25 | 12 interviews ([09](09-interview-guide.md)) |
| 22 | AD-T1 decision ([31](31-experiment-design.md)) |
| 28 | Day-21 publication question on early orders |
| 30 | **Gate review** |

---

## Prioritised actions

Ranked by impact × confidence ÷ (cost + founder time). Top ten:

| Rank | Action | Impact | Confidence | Cost | Hours | Why here |
|---|---|---|---|---|---|---|
| 1 | **V-0 primary source verification** | High | High | $0 | 4 | Blocks everything and costs nothing |
| 2 | **V-1: 10 practice packages with time logs** | **Very high** | High | ~$150 | 20 | Replaces the three assumptions that decide viability |
| 3 | **Lawyer + accountant** | High | High | $$$ | 2 | Blocks the first paid order |
| 4 | Site + form + payment | High | High | ~$50 | 12 | No transaction without it |
| 5 | **Run the test suite** | High | High | $0 | 4 | 12 launch-blocking failures |
| 6 | Organic posts 1–8 | Medium | Medium | $0 | 6 | Slow, compounding, cheap |
| 7 | Partner conversations | Medium | **High** | $0 | 3 | Highest buying intent available |
| 8 | AD-T1 with spending limit | Medium | Medium | $300 | 4 | Fastest message evidence |
| 9 | 12 interviews | Medium | Medium | $0 | 8 | Resolves A-02, A-05, A-06 |
| 10 | Competitor pricing sweep | Medium | High | $0 | 2 | Fills honestly empty cells |

**Note ranks 1, 2 and 5 are all "find out whether this works before spending on it."** That
ordering is deliberate: they are cheap, they are blocking, and they are the ones most likely to be
skipped under enthusiasm.

---

## Go / no-go gates

Each gate specifies evidence, owner, decision rule, and what happens on failure. **A gate that
is not met is not a delay to work around — it is the answer.**

### Gate 1 — Accept payments *(day 12)*

| | |
|---|---|
| **Evidence required** | V-0 complete · V-1 complete with measured economics · effective hourly ≥$60 at measured values · lawyer-reviewed agreement · all 12 critical failures clear · ⏳ claims resolved |
| Owner | Founder |
| **Decision rule** | **All six. Not five.** |
| On failure | Do not open. Fix the failing item. **Taking money before the agreement and the gates are ready is how a small problem becomes a legal one** |

### Gate 2 — Increase advertising *(day 30+)*

| | |
|---|---|
| **Evidence** | ≥8 qualified leads from AD-T1 · cost per qualified lead <$30 · ≥1 order attributable to paid · zero claim violations |
| Owner | Founder |
| **Decision rule** | All four, **and** the 3× effect threshold met ([31](31-experiment-design.md)) |
| On failure | Do not increase. Diagnose which funnel stage broke ([31](31-experiment-design.md) §Diagnosing failure) before spending more |

### Gate 3 — Introduce a subscription or bundle *(day 90+)*

| | |
|---|---|
| **Evidence** | **≥3 customers repurchased unprompted** within 90 days · a repeating trigger identified · ≥20 delivered orders |
| Owner | Founder |
| Decision rule | All three (D-10) |
| On failure | **Stay one-time.** Re-evaluate at 180 days. Do not build a subscription to manufacture recurring revenue |

### Gate 4 — Hire a contractor *(when reached)*

| | |
|---|---|
| **Evidence** | H1–H4 ([37](37-capacity-and-contractors.md)): ≥15 orders with time logs · demand over capacity 3 consecutive weeks · cash buffer ≥$2,000 · **the task documented well enough for a stranger** |
| Decision rule | All four |
| On failure | Absorb with capacity limits and the delivery buffer. **Hiring to avoid writing the process down produces a contractor who needs supervision** |

### Gate 5 — Expand automation *(ongoing, one action at a time)*

| | |
|---|---|
| **Evidence** | The specific action has its own eval, passing 20+ consecutive times · zero critical failures · a human rollback path exists |
| Decision rule | **One action promoted at a time**, each with its own eval (D-15) |
| On failure | Stays human-approved |

### Gate 6 — Add a channel *(day 60+)*

| | |
|---|---|
| **Evidence** | The primary channel is producing qualified leads at target cost · founder hours available without cutting production · the new channel's rules verified |
| On failure | Deepen the primary channel. **Adding a second channel to fix a first channel that is not working produces two channels that do not work** |

### Gate 7 — Add a product *(day 90+)*

| | |
|---|---|
| **Evidence** | Current offer delivered 20+ times · effective hourly ≥$80 · customers asking for the specific thing, unprompted · it reuses the existing pipeline |
| On failure | No new product. **Product proliferation is the most common way a solo service business dilutes itself into unprofitability** |

---

## The conditional 90-day plan

**Every phase is conditional on the previous gate. If a gate fails, the plan stops there and the
work becomes fixing that gate.**

### Days 31–60 — *only if Gate 1 passed and ≥5 orders delivered*

| Focus | Actions |
|---|---|
| **Delivery economics** | Drive median time per order below 2h via templating. **The highest-leverage work available** ([15](15-financial-model.md) §7) |
| Evidence | Convert measured performance into permitted claims ([21](21-claim-register.md)) |
| Proof | First real testimonials, with written permission |
| **Partnerships** | Convert 1–2 conversations into active referral relationships |
| Segment | Re-score [08](08-segment-selection-matrix.md) with real conversion data |
| Price | Run PR-T1 if price is the top lost reason |
| Channels | Deepen the primary. Add nothing (Gate 6) |

### Days 61–90 — *only if days 31–60 held*

| Focus | Actions |
|---|---|
| **Portfolio economics** | Deliver and **time** one real 5-property PM job. **Only then quote volume pricing** ([19](19-property-manager-sales.md) PS-6) |
| Repeat | Measure unprompted repeat. Evaluate Gate 3 explicitly — including deciding *not* to |
| Search | Publish the three content pages ([32](32-search-email-remarketing.md)) |
| Paid | Scale only if Gate 2 passed |
| Capacity | Evaluate Gate 4 |
| Segments | Consider S4/S5 **only if** 15+ delivered jobs give a portfolio ([08](08-segment-selection-matrix.md)) |

---

## What not to spend time or money on yet

| Not yet | Until |
|---|---|
| A subscription | Gate 3 |
| Contractors | Gate 4 |
| Google Ads | A measured conversion rate and margin to fund it |
| Remarketing | 1,000 monthly visitors ([32](32-search-email-remarketing.md)) |
| Industry events | Revenue exists |
| A second product | Gate 7 |
| Luxury and boutique segments | 15 delivered jobs |
| Cold outreach | V-2 and a portfolio |
| White-label partnerships | 90 days ([33](33-partnership-plan.md)) |
| **A logo, brand identity, or anything aesthetic beyond a clean site** | Ever, until there is revenue. **It is the most enjoyable way to avoid finding out whether anyone will buy** |
| Long-form YouTube | Probably never |
| Automating anything not yet done manually 20 times | It has been done manually 20 times |

---

## The single most important thing

**Day 5.** The ten practice packages and their time logs.

Everything downstream — the price, the capacity, the CAC target, whether the business is worth
doing at all — is derived from three numbers we currently do not have: accepted-clip yield,
generation cost, and **minutes per order**. They cost about 20 hours and $150 to obtain, they
require no customer, and they can be obtained before anything is risked.

**A founder who skips day 5 and goes straight to selling will find out the same things, more
slowly, in front of customers, with their money already taken.**
