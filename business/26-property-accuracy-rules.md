# 26 — Property Accuracy Rules

**This document is law. It overrides creative preference, customer request, deadline pressure,
and commercial interest.** Where it conflicts with anything else in this system, this document
wins.

A public version of the checklist in §4 is published on our website — it is a reason to believe
([12](12-positioning.md) RTB-4), and publishing it is what makes it a commitment rather than an
intention.

---

## 1. Why this exists

| Evidence | Consequence |
|---|---|
| **E-11** | Airbnb will require removal of listing content where AI or digital technology was used to edit flaws, hide damage, add amenities or attributes not part of the listing, or otherwise misrepresent it. Enforcement escalates: education → warning → forced removal → **suspension or removal of the listing, loss of Superhost, cancellation of reservations, and refunds taken from the host's payout** |
| **E-12** | Guests obtain refunds where a property is "materially different" from advertised — **size misrepresentation, missing amenities, and significant photo discrepancies are named** |
| **E-17** | FTC truth-in-advertising: representations must be truthful and not misleading |
| **E-14 / E-15** | California B&P §10140.8 (from 1 Jan 2026) and Wisconsin Act 69 require disclosure of digitally altered property images by licensees. **Scope caveat: both address real property *sales* by *licensees*, which likely does not cover an STR owner marketing a rental.** We adopt disclosure as policy anyway |
| **E-16** | NAR: AI should "show possibilities," not "rewrite reality" |

**The asymmetry that decides everything:** the upside of an exaggerated video is one marginal
booking. The downside is a suspended listing, cancelled reservations, and money clawed back from
a customer's payout. **No creative gain justifies that trade, and it is not our risk to take on a
customer's behalf.**

---

## 2. The governing principle

> **Motion may be added. Reality may not.**

Everything in this document follows from that sentence.

| Acceptable enhancement | Unacceptable alteration |
|---|---|
| Adding camera motion to a still photograph | Adding, removing, extending or changing a **view** |
| Colour grading within the light the photograph actually contains | Inventing light sources, windows, or time of day the space doesn't get |
| Exposure and contrast correction | Brightening a dark room until it reads as a different room |
| Stabilisation, sharpening, upscaling that invents no new detail | Upscaling that hallucinates texture or detail |
| Cropping and reframing | Changing proportions or apparent dimensions |
| Choosing which real features to show | Adding furniture, appliances, decor or amenities |
| Sequencing real spaces | Implying an adjacency that does not exist |
| Omitting an unflattering angle (as a photographer would) | **Concealing damage, hazards, or a material defect** |
| Music and typography | Generating ambient sound that implies a sensory fact (waves, birdsong, quiet) |
| Showing a room tidy, as photographed | "Cleaning," repairing, or removing clutter generatively |

**The line between the last "acceptable" and "unacceptable" pair is the subtle one.** A
photographer choosing a flattering angle is normal practice. Generatively erasing water damage
from that angle is the E-11 case exactly. The test: **did we choose among real things, or did we
change a thing?**

---

## 3. Absolute prohibitions

These are hard rejects. There is no score threshold, no customer waiver, no deadline exception.
A video containing any of them is not delivered.

1. **Views.** No generative creation, extension, or alteration of anything visible through a
   window or from outdoor space. Every frame of view content must trace to a supplied photograph.
2. **Rooms and layout.** No invented rooms, doorways, corridors, or connections. No implied
   adjacency between spaces that do not adjoin.
3. **Dimensions.** No alteration of apparent room size, ceiling height, or proportions.
4. **Capacity.** On-screen capacity must reconcile exactly to the signed fact sheet and to
   visible sleeping surfaces. Bunk rooms and sofa beds are shown as what they are.
5. **Amenities.** Nothing shown that is not present: pools, hot tubs, fireplaces, air
   conditioning, appliances, parking, outdoor structures.
6. **Accessibility.** **Nothing that implies step-free access, wider doorways, grab rails,
   accessible bathrooms, or level thresholds unless verified.** Highest-harm category — a guest
   who cannot enter the property has suffered more than a disappointment.
7. **Location.** No implication of proximity, views, or access that the fact sheet does not state
   as a measured value.
8. **Safety.** No implication of pool fencing, stair gates, alarms, or lighting that is not
   present. No concealment of a hazard that is present.
9. **Condition.** No generative repair, cleaning, or removal of damage, wear, or clutter.
10. **Sound.** No generated ambience implying a sensory property (quiet, ocean, birdsong).

---

## 4. Gate 1 — the accuracy review

Run by a **human**, on **every** video, before Gate 2. **Never delegated to a model**
([39](39-data-and-agent-architecture.md)). Target 12 minutes.

### The checklist

For each clip, with the source photograph open side by side:

**Provenance**
- [ ] Every clip maps to a named source photograph
- [ ] No clip derived from another clip (no chaining)
- [ ] No frame contains content absent from its source photo

**Structure**
- [ ] Room order matches the property's real layout
- [ ] No implied adjacency that does not exist
- [ ] No invented doorway, window, corridor or opening
- [ ] Proportions consistent with the source photograph
- [ ] Straight architectural lines remain straight

**Facts**
- [ ] Every on-screen number traces to the signed fact sheet
- [ ] Capacity reconciles to visible sleeping surfaces
- [ ] Every claimed amenity is visible or fact-sheet confirmed
- [ ] Distances and times are stated values, not inferences
- [ ] No accessibility implication unless verified

**Views and exteriors**
- [ ] Every window view traces to a supplied photograph
- [ ] No extension of a view beyond the photo's frame
- [ ] Outdoor space shown at its real extent

**Condition**
- [ ] No damage, wear or hazard removed
- [ ] No generative cleaning or repair
- [ ] Lighting plausible for the property's orientation and the stated time

**Sound and text**
- [ ] No generated ambience implying a sensory fact
- [ ] Captions factually correct against the fact sheet
- [ ] No claim outside [21](21-claim-register.md)

**Vrbo cut specifically** (E-03–E-06)
- [ ] 15–60 seconds
- [ ] No added music
- [ ] No contact details anywhere in frame
- [ ] Area footage ≤20% of runtime, timed

### Outcomes

| Outcome | Action |
|---|---|
| **Pass** | Proceed to Gate 2. Record reviewer and timestamp |
| **Fix** | Specific clip re-cut or removed, then **the full checklist is re-run** — not just the changed item |
| **Hard reject** | Any §3 prohibition. Clip removed or re-storyboarded. **Never delivered.** If it cannot be fixed, the deadline moves and the customer is told why |

**The rule that makes this real: a high average score never overrides a single factual error.**
There is no aggregate. One failed factual item fails the video, even if every other item passes.
Scoring belongs to Gate 2 ([27](27-quality-rubric.md)); Gate 1 is binary.

---

## 5. Permissions and records

Before production:

| Record | Requirement |
|---|---|
| **Property Fact Sheet** | Signed/confirmed by the customer. **The single source of truth for every property fact.** No model, and no member of our team, may supply a fact that is not on it ([39](39-data-and-agent-architecture.md)) |
| **Rights confirmation** | Written statement that the customer holds or controls the rights to the supplied photography **and** has authority to market the property ([38](38-rights-and-security.md)) |
| **Owner authority (PM orders)** | For managed property, written confirmation that the manager may market each named property this way ([19](19-property-manager-sales.md)) |
| **Portfolio permission** | Separate, explicit, opt-in. **Never assumed from the order.** A customer may buy without ever appearing in our portfolio |
| **Area imagery rights** | For VC-7, rights cleared for every non-property image |

After delivery:

| Record | Retention |
|---|---|
| Fact sheet as signed | Duration of the customer relationship + 2 years |
| Accuracy review record: reviewer, date, outcome, items fixed | Same |
| Source photo hashes per clip | Same |
| Prompts, model, settings, attempts | Same |

**Why hashes:** if a customer or a platform later asks what a clip was derived from, we can prove
it. That is the difference between a documented process and a claimed one.

---

## 6. Disclosure

We adopt disclosure as **policy**, ahead of any determination that E-14/E-15 apply to our
customers (they probably do not — see the scope caveat in §1).

| Where | What |
|---|---|
| Our website and proposals | "These videos are made with AI assistance and reviewed by a person before delivery" |
| Delivery message | A note that the customer may disclose AI assistance in their own posting if they wish, and a suggested line |
| **Never** | We do not require the customer to disclose. That is their decision and their jurisdiction's question, not ours to impose |

We tell customers what we did. We do not advise them on their legal obligations — that requires a
lawyer and their jurisdiction ([38](38-rights-and-security.md)).

---

## 7. Escalation

| Situation | Action |
|---|---|
| Photo and fact sheet disagree | **Stop. Ask the customer.** Never resolve it internally |
| Customer asks for a prohibited alteration | Decline, cite the reason, offer the compliant alternative (OBJ-15, [17](17-objection-library.md)) |
| Customer insists | **Decline the order.** Refund if already paid. This is not negotiable at any price |
| A defect reaches a customer | Treat as our error ([14](14-offer-specification.md) category 1): free fix, prioritised, logged as a **gate escape** |
| A gate escape occurs | **Review the gate itself, not just the clip.** Two escapes in 20 orders means the checklist or the reviewer's time budget is wrong |
| A platform contacts a customer about our media | Full cooperation, provide provenance records, refund the order, **and treat it as a business-critical incident** — re-review every video delivered with the same technique |

## 8. Acceptance criteria

- [ ] Gate 1 recorded on 100% of delivered videos, with reviewer and timestamp
- [ ] Zero delivered videos containing a §3 prohibition
- [ ] Zero gate escapes in the first 20 orders
- [ ] 100% of orders have a signed fact sheet and rights confirmation before production
- [ ] Zero facts appearing on screen that are absent from a fact sheet
- [ ] Gate 1 median time between 8 and 15 minutes — **under 8 minutes suggests it is not being
      done properly**
