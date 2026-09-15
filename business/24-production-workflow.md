# 24 — Production Workflow

**Authoritative source for the production pipeline.** Every order follows it. The two review
gates are not optional and cannot be skipped for a deadline
([26](26-property-accuracy-rules.md), [27](27-quality-rubric.md)).

## The pipeline

```
INTAKE → ASSET ASSESSMENT → FACT CONFIRMATION → BRIEF → STORYBOARD →
GENERATION → SELECTION → EDIT → [GATE 1: ACCURACY] → [GATE 2: QUALITY] →
EXPORT → DELIVERY → ARCHIVE
```

Target: **152 minutes** per Standard order (A-10). Every step is timed; the log is what replaces
estimates with measurements in [15](15-financial-model.md).

---

### 1. Intake — 15 min

| Step | Detail |
|---|---|
| Verify payment cleared | No production before payment ([15](15-financial-model.md) §9) |
| Receive assets | Photos + Property Fact Sheet + rights confirmation |
| **Start the clock** | **Turnaround counts from complete assets, not from payment.** Confirm the date in writing now |
| Create order record | [39](39-data-and-agent-architecture.md) |

**Stop condition:** assets incomplete → order parks, customer notified once, reminder at 48h and
5 days ([35](35-customer-operations.md)). Do not start partial work.

### 2. Asset assessment — 10 min

| Check | Threshold | If it fails |
|---|---|---|
| Photo count | ≥15 (Starter) / ≥20 (Standard) | Request more; park if unavailable |
| Resolution | ≥1500px long edge | Exclude the photo; if <15 remain, park |
| Coverage | All spaces the brief requires | Request specific missing shots |
| Rights | Confirmation received and unambiguous | **Stop. Do not proceed** ([38](38-rights-and-security.md)) |
| Currency | Nothing showing a removed feature | Ask the customer |
| Duplicates | Near-identical shots | Remove |

**Output:** a shortlist of 12–16 usable photos, ranked, per the shot selection guide
([23](23-scripts-and-storyboards.md)).

### 3. Property fact confirmation — 5 min

Reconcile the fact sheet against the photographs. **This is where accuracy problems are cheapest
to catch** — before a single frame is generated.

| Check | Example of a catch |
|---|---|
| Capacity reconciles to visible sleeping surfaces | Fact sheet says sleeps 10; photos show 4 beds and no sofa bed. **Ask** |
| Every claimed amenity appears in a photo, or is acknowledged as unphotographed | "Hot tub" claimed, no photo. Ask before assuming |
| Nothing in the photos contradicts the fact sheet | Photo shows a fireplace; fact sheet says no fireplace. Ask |
| Distances and times are stated, not inferred | "Near the beach" is not a fact. "[N] minutes' walk" is |

**Rule: where a photo and the fact sheet disagree, production stops and the customer is asked.**
We never resolve the conflict ourselves, and we never let a model resolve it
([39](39-data-and-agent-architecture.md)).

### 4. Brief — 10 min

Complete the six-field messaging framework
([10](10-traveler-decisions-and-property-messaging.md) §2). Select concept (VC-N) and storyboard
(ST-N). **Field 6 — what must not be implied — is mandatory and specific to this property.**

### 5. Storyboard — 5 min

Map each shot to a specific source photo filename, a camera move (P-NN), and a duration. **Every
clip is bound to a photograph before generation begins.** A clip with no source photo is a clip
that will invent something.

### 6. Generation — 25 min

| Rule | |
|---|---|
| One photo → one clip | **Never chain outputs.** Drift compounds invisibly |
| Generate 5s, use 2–3s | First and last frames carry the artifacts |
| Low motion strength | If a shot needs high motion to work, the photo is wrong |
| Prompts from the library only | [23](23-scripts-and-storyboards.md). No freehand content prompts |
| Log every attempt | Prompt, model, settings, accepted/rejected, source photo |
| **Budget cap** | Stop at **3× the estimated generation cost** for the order and escalate to manual review. Do not keep rolling the dice |

**Output:** accepted clips + the attempt log (which feeds the A-09 measurement).

### 7. Selection — 5 min

Choose the best take per shot. **Reject on artifacts before aesthetics** — a beautiful clip with
a bending doorframe is rejected, and a plainer clip that is geometrically sound is kept.

### 8. Edit — 30 min

Assemble to the storyboard. Captions, music, grade, pacing. Build the master timeline so all
seven exports derive from it — **this is where multi-format delivery becomes cheap rather than
seven times the work.**

### 9. GATE 1 — Accuracy review — 12 min

[26](26-property-accuracy-rules.md). Human, mandatory, checklist-driven, never delegated to a
model. **A hard-reject here stops delivery regardless of deadline.**

### 10. GATE 2 — Quality review — 8 min

[27](27-quality-rubric.md). Technical defects. Hard-reject list applies.

**The gates are in this order deliberately.** Accuracy first, because a technically flawless
video of a property that does not exist is worse than a slightly flickery one of a property that
does.

### 11. Export — 10 min

Per the export checklist ([23](23-scripts-and-storyboards.md)). Seven files. **Check the GBP file
size on disk** — E-08's 75MB limit is the one spec that silently fails.

### 12. Delivery — 8 min

Per the delivery checklist. Files named by destination, the Where To Post This one-pager, and the
delivery message ([20](20-brand-voice-and-copy.md)).

### 13. Archive — 5 min

Production metadata ([22](22-creative-concepts.md)), selected files, attempt log, review records,
time log. Retention per [38](38-rights-and-security.md).

---

## Stop conditions

Production halts, and the customer is contacted, whenever:

| Condition | Action |
|---|---|
| Photo and fact sheet disagree | Ask. Never resolve it ourselves |
| Rights confirmation missing or ambiguous | Stop until resolved |
| Assets insufficient after assessment | Park the order; offer a refund if unresolvable |
| Generation budget cap hit | Escalate to manual review; consider a template-motion fallback |
| A hard-reject defect cannot be fixed in 2 attempts | Re-storyboard that shot, or cut it |
| The customer changes the brief mid-production | Scope decision tree ([14](14-offer-specification.md) §4) |
| We will miss the promised date | **Tell them before the date, not after** ([35](35-customer-operations.md)) |

## Batching

Multi-property orders batch by *step*, not by property: assess all assets, then all briefs, then
all generation, then all edits. Gate 1 and Gate 2 remain **per property** — batching a review is
how a portfolio-wide accuracy error ships.

This batching is the mechanism by which per-unit time is supposed to fall below 2.0 hours
([19](19-property-manager-sales.md) PS-6). **It is a hypothesis until a real 5-property job is
timed.**

## Fallback: when generation fails

If accepted-clip yield is unworkable for a property, fall back to **template-based motion** —
programmatic pan and scale on the source photographs, with no generative model involved. It is
less impressive and completely safe. Better a plainer video delivered on time than a missed
deadline or a shipped artifact. The customer is told which method was used.

## Acceptance criteria

After 10 orders:
- [ ] Every order has a complete time log, per step
- [ ] Every order has an attempt log with the accepted/rejected ratio
- [ ] Both gates recorded on 100% of orders
- [ ] Zero deliveries with a skipped gate
- [ ] Median total time ≤ 180 min
- [ ] Measured generation cost replaces the A-09 estimate in
      [15](15-financial-model.md)
