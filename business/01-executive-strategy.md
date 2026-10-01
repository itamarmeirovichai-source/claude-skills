# 01 — Executive Strategy

## The business in one paragraph

We take the photographs a vacation rental operator already owns and turn them into a pack of
short marketing videos they can actually publish — on Instagram and TikTok, on their direct
booking site, in email to past guests, on their Vrbo listing, and on their Google Business
Profile. We do it without a site visit, in three to five business days, for a price between a
DIY tool and a videographer. Our discipline is that the video never shows a property that does
not exist: we treat platform accuracy rules as the product specification, not as fine print.

## Why this shape, and not the obvious shape

The obvious business is "AI videos for your Airbnb listing." That business does not work.
**Airbnb does not accept host-uploaded video in the listing gallery** (E-01). The single largest
channel our customers use cannot display our product. Every competitor SEO page optimising for
"Airbnb listing video" is selling into a premise the platform does not support.

This forces three consequences that define the strategy:

1. **We sell assets for channels the operator controls**, not for the OTA that controls them.
   That means social, direct booking site, email, and the two OTA-adjacent surfaces that do
   accept video: Vrbo (E-03) and Google Business Profile (E-08).
2. **The buyer worth having is the one who has those channels and is unhappy with them.**
   E-28: 70% of operators have a direct booking site; 62% of them get under 25% of bookings
   through it. That is an active, funded, frustrated buyer. The Airbnb-only single-property host
   with no direct site has no place to put our product and is the wrong first customer.
3. **Accuracy is the moat, because the platform made it one.** Airbnb will require removal of
   content where AI was used to edit flaws, hide damage, or add amenities that are not there,
   with an enforcement ladder up to listing suspension and refunds taken from host payouts
   (E-11). A generative-video vendor that does not manage this is selling its customers a risk.
   We make the accuracy review a named, visible part of the deliverable.

## What we sell, at what price

Authoritative: [14 — Offer Specification](14-offer-specification.md) and
[15 — Financial Model](15-financial-model.md). Summary:

| | Starter | **Standard (lead offer)** | Portfolio |
|---|---|---|---|
| Price (hypothesis, to test) | $149 | **$279** | from $199/property, 5+ |
| Properties | 1 | 1 | 5+ |
| Creative concepts | 1 | 2 | 1 per property, shared template |
| Deliverable files | 3 | 7 | 5 per property |
| Vrbo-compliant cut (no music, no on-screen contact) | — | ✅ | ✅ |
| Revision rounds included | 1 | 1 | 1 per property |
| Turnaround | 5 business days | 3–5 business days | negotiated |

Prices are **hypotheses carrying A-07**, not established. The price test is the second-most
important experiment we run.

## Who we sell to first

Authoritative: [08 — Segment Selection Matrix](08-segment-selection-matrix.md).

**Initial ICP:** a US-based operator of **3 to 25 vacation rental units** who already runs a
direct booking website and at least one active social account, who has professional or
semi-professional photography for most units, and who is within ten weeks of a high season.
Typically a small property manager, a serious multi-property owner, or a design-led boutique
operator.

**We decline:** single-listing Airbnb-only hosts with no direct site and no social presence
(nowhere to use the deliverable); anyone asking us to show a property feature that does not
exist; anyone whose photos are too few, too low-resolution, or not rights-cleared; anyone
requesting a booking guarantee; anyone whose deadline is inside 48 hours on a first order.

## Why someone pays us instead of using an AI tool themselves

The honest answer, which we will say out loud:

> A host with two spare hours, good taste, and 30 decent photos can make a passable property
> video themselves with a $20/month tool. If that is you, do it. What we sell is the two hours,
> the editorial judgment about which twelve of your forty photos to use and in what order, an
> accuracy review against the platform rules, and seven finished files in the right shapes for
> the places you actually publish — instead of one file you then have to re-crop.

That is a real answer, it disqualifies people honestly, and it survives contact with a skeptic.
The alternative answers ("better quality", "AI-powered") do not.

## What we will not claim

Authoritative: [21 — Claim Register](21-claim-register.md).

We will not claim our video increases bookings, occupancy, or revenue. **No causal evidence for
that claim exists in public** (E-20), and we have none of our own. We will not use Airbnb's
logo or branding (E-13). We will not show illustrative work as client work. We will not invent
testimonials, case studies, or results. At launch we have **no results**, and our marketing must
read as though that is true, because it is.

## The economics, honestly

Authoritative: [15 — Financial Model](15-financial-model.md); runnable at
[`tools/financial_model.py`](tools/financial_model.py).

At the Standard price of $279, with estimated generation cost ~$15 (A-09), payment fees ~$8.40
(E-25), and ~$4 of amortised software and storage, contribution margin before founder time is
roughly **$251**. At an assumed 2.0 hours of founder time per order (A-10), that is about
**$126 per hour** — good, *if* the time assumption holds.

The model is fragile in exactly three places, and all three are the same variable: **how long an
order actually takes.** If hands-on time is 4 hours instead of 2, effective earnings halve to
~$63/hour. If the revision rate is 70% instead of 35%, add roughly half an hour per order on
average. If the generation failure rate is triple our estimate, generation cost goes to ~$45 and
margin drops ~12%. Note the ranking: **time is the dominant risk; generation cost is a rounding
error.** That is counter-intuitive and it should drive where we optimise — toward ruthless scope
control and template reuse, not toward cheaper models.

Break-even CAC at Standard is ~$251. A sane **target CAC is $75**, giving a 3.3:1 contribution-
to-acquisition ratio on a first order with **no assumed repeat value** (A-05).

## The 30-day shape

Authoritative: [43 — Launch Plan](43-launch-plan.md).

- **Days 1–5:** verify the nine blocked primary sources (E-ledger verification queue). Produce
  10 self-funded practice videos on rights-clear imagery. **Measure real time and real cost.**
  This replaces A-03, A-09 and A-10 with data before a single customer is exposed to us.
- **Days 6–12:** build the site and the intake form. Publish the first 8 pieces of organic
  content. Open for orders at full price.
- **Days 13–30:** 20 qualified conversations. Target 5 paid orders. Run one $300 ad test with an
  account spending limit set (E-34 — daily budgets are not caps). Deliver every order and
  measure.

**The go/no-go at day 30 is not "did it feel promising."** It is: 5 paid orders from strangers,
median hands-on time under 3 hours, zero accuracy incidents, and at least one customer who says
unprompted that they will order again.

## The strategic risks, ranked

1. **Nobody buys** (A-01). The most likely failure. Mitigation: validate with money in 30 days,
   at full price, before building anything else.
2. **Orders take four hours, not two** (A-10). The second most likely failure, and the quiet
   one — it looks like success while destroying the hourly rate. Mitigation: time-track from
   order one; hard scope-change tree in [14](14-offer-specification.md).
3. **Interiors are the worst case for generative video** (A-03). Architectural geometry warps and
   humans notice instantly. Mitigation: the practice run in days 1–5 exists precisely to find
   this before a customer does; the fallback product is template-based motion, not generation.
4. **An accuracy incident harms a customer's listing** (E-11). Low probability, severe
   consequence, and it would end the business's credibility. Mitigation:
   [26](26-property-accuracy-rules.md) is written as law, with a two-stage human gate that
   cannot be automated away.

## How this system connects evidence to action

Every consequential recommendation in these documents follows the same chain, and you can audit
it: **Evidence (`E-NN`) → interpretation → decision (`D-NN` in [04](04-decision-log.md)) →
implementation artifact → measurement ([41](41-measurement-definitions.md)) → the condition that
would reverse it.** Where a link in that chain is missing, the gap is registered as an assumption
(`A-NN`) with a kill condition, not smoothed over.
