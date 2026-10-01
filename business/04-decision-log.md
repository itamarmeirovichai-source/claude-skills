# 04 — Decision Log

**Authoritative source for what was decided, on what evidence, and what would reverse it.**

Format for every entry: Decision → Evidence → Alternatives considered → Cost/tradeoff →
Reversal condition.

---

### D-01 — Do not build the offer around Airbnb listing video
**Decision:** The product is never described as "video for your Airbnb listing." All copy,
packaging and channel strategy assume Airbnb's gallery cannot display video.
**Evidence:** E-01 (grade B — primary blocked, multiple consistent secondaries).
**Alternatives:** (a) sell it anyway and let hosts figure out where to put it — dishonest and
generates refunds; (b) target only Vrbo-first hosts — too small; (c) reframe onto owned channels
— chosen.
**Cost:** Loses the highest-search-volume keyword set. Competitors will keep ranking for
"Airbnb listing video" and we will look absent from it.
**Reversal:** Airbnb opens gallery video to general hosts. **Check quarterly.** This would be a
major expansion, not a threat — we would already own the production system.

### D-02 — Accuracy is the product specification, not a disclaimer
**Decision:** [26](26-property-accuracy-rules.md) is binding law over all creative preference.
Two-stage human review before delivery; certain defects are hard-reject regardless of score.
**Evidence:** E-11 (Airbnb removal/suspension ladder for AI-altered listing media), E-12 (guest
refunds for material misrepresentation), E-17 (FTC truthful-not-misleading principle).
**Alternatives:** (a) treat accuracy as a customer responsibility with a liability waiver —
legally tidier, but the customer cannot evaluate what our model invented, so it is a bad-faith
transfer of risk; (b) avoid generative motion entirely — safest, kills the product's appeal;
(c) accuracy as a named deliverable with a human gate — chosen.
**Cost:** ~20 minutes per order of review time. Rejects some visually impressive output. Puts a
ceiling on how "cinematic" we can be.
**Reversal:** None foreseeable. Even if platforms relaxed, E-17 is general advertising law.

### D-03 — Initial ICP is the 3–25 unit operator with a direct booking channel
**Decision:** See [08](08-segment-selection-matrix.md).
**Evidence:** E-28 (70% have a direct site, 62% of those get <25% direct — active
dissatisfaction); E-29 (PMs rank marketing reach first); E-27 (64% of hosts use no PMS — a large
but low-tooling, low-budget majority we deliberately skip).
**Alternatives:** (a) single-property Airbnb hosts — largest count, cheapest to reach, but
no channel for the deliverable and lowest budget; (b) luxury/boutique — best margin, but tiny,
slow, referral-gated, and needs a portfolio we do not have; (c) large PMs (100+ units) — best
contract value, but 3–6 month sales cycles a solo operator cannot fund; (d) 3–25 units —
chosen: has budget, has channels, decides fast, small enough to reach a decision-maker directly.
**Cost:** Harder to reach than individual hosts. Smaller total market than the mass segment.
**Reversal:** If 20 conversations with this segment yield under 3 orders while a different
segment converts in passing, switch. Decision owner: founder, at the day-30 gate.

### D-04 — Price the lead offer at $279, not $99 and not $600
**Decision:** Standard = $279. See [15](15-financial-model.md).
**Evidence:** E-31 (human videographers $150–$500 basic, $500–$2,500 cinematic); E-32 (DIY AI
tools $10–100/mo). We sit deliberately between, closer to the low end of human production.
**Alternatives:** (a) $99 — wins price shoppers, produces an unservable hourly rate at A-10 time
assumptions, attracts the segment most likely to demand revisions; (b) $600+ — plausible against
cinematic anchors but requires a portfolio and proof we do not have at launch; (c) $279 —
chosen, defensible against both anchors, survives a 30% discount request without going negative.
**Cost:** Too expensive for the mass host segment; too cheap to signal premium to luxury buyers.
Deliberately in neither of those markets.
**Reversal:** carries **A-07** — real-estate-sale pricing may not transfer to STR. If price
objection is the top-cited loss reason in >50% of lost deals at the day-30 review, test $199.
**Do not discount ad hoc before that review** ([15](15-financial-model.md) §Discount rules).

### D-05 — No booking-lift claims, ever, at any price
**Decision:** [21](21-claim-register.md) forbids any claim that our video increases bookings,
occupancy, revenue, or ranking.
**Evidence:** E-20 (no causal evidence located); E-17 (FTC substantiation principle).
**Alternatives:** (a) cite vendor statistics — they are D-grade marketing claims about others'
products; using them is laundering; (b) hedged phrasing ("hosts report...") — we have no hosts;
(c) silence on outcomes, specificity on deliverables — chosen.
**Cost:** Removes the most persuasive sales lever in the category. Competitors will out-promise
us and some buyers will believe them.
**Reversal:** Only a controlled test we run ourselves — matched properties, one with video on a
given channel and one without, same period — would justify a narrow, caveated claim. That is
expensive and probably underpowered. **Assume this never reverses.**

### D-06 — Music-free Vrbo cut ships in every package above Starter
**Decision:** Every Standard and Portfolio order includes a cut with no added music and no
on-screen contact details.
**Evidence:** E-04 (added music is a common Vrbo rejection reason), E-05 (contact details in
frame break the rules), E-03 (15s–2min, mp4).
**Alternatives:** (a) one universal file — fails Vrbo; (b) charge extra for the compliant cut —
petty, and it is cheap to produce from the same timeline; (c) include it — chosen, and name it
in the offer so it is visible as expertise.
**Cost:** ~10 minutes per order and one extra export.
**Reversal:** Vrbo changes its policy. Re-check at V-0 and quarterly.

### D-07 — Use Epidemic Sound Pro tier for music; never platform-native editor music
**Decision:** Licence music through a subscription whose terms explicitly permit client work and
survive subscription lapse for work already delivered.
**Evidence:** E-18 (Pro includes freelancer client work, digital ads; perpetual right for
productions completed during the subscription period; sublicensing to clients under $50M
revenue); E-24 (**CapCut grants no rights to its built-in music at any tier** — the most common
licensing trap in this category).
**Alternatives:** (a) CapCut/editor stock music — free and immediately infringing; (b) Artlist
~$299/yr (E-19) — viable alternative; (c) per-track licensing — too slow.
**Cost:** ~$204/yr fixed. Must be read in full before first paid delivery (verification queue).
**Reversal:** Terms change, or Artlist proves cheaper for our volume.

### D-08 — Do not use CapCut as the primary editor for client property assets
**Decision:** Primary edit in DaVinci Resolve (free tier) or equivalent; CapCut permitted only
for our own marketing content, never for client property footage.
**Evidence:** E-24 — CapCut's ToS grants CapCut a broad licence over uploaded and created
content, and its built-in music carries no commercial grant.
**Alternatives:** (a) CapCut for speed — fastest editor in the category, and the broad content
licence over a *client's* property assets is a real conflict with the rights we promise them in
[38](38-rights-and-security.md); (b) Premiere ~$23/mo — costs money we do not need to spend;
(c) Resolve free — chosen.
**Cost:** Steeper learning curve, slower for simple social cuts.
**Reversal:** CapCut narrows its content licence, or we obtain a written enterprise term.

### D-09 — Enforce ad spend with an account spending limit, not daily budgets
**Decision:** No ad campaign runs until an account-level spending limit is set at the
experiment's maximum acceptable loss.
**Evidence:** E-34 — Meta daily budgets are not hard caps; reported single-day allowance is
daily × 1.75, with a rolling 7-day cap of 7× daily. A true ceiling requires the separate
account spending limit.
**Alternatives:** (a) trust daily budgets — the default mistake, and at a $300 test budget a
75% daily overrun is a material fraction of a solo founder's cash; (b) check dashboards daily —
fails A-15 (founder unavailable 8–10h); (c) account spending limit — chosen, and it is the only
option that works while asleep.
**Cost:** Campaigns hard-stop when the limit is reached, mid-learning. That is the point.
**Reversal:** None. This is a safety control.

### D-10 — No subscription at launch
**Decision:** Sell one-time packages. Build no recurring plan until repeat demand is observed.
**Evidence:** A-05 (repeat frequency unknown); E-27/E-28 (no data on content cadence needs).
**Alternatives:** (a) launch a $99/mo content plan — attractive cash flow, but if a
single-property host genuinely needs video once a year it is a subscription to nothing and
produces churn, refunds and reputational damage; (b) bundles/credit packs — a middle option,
revisit at 90 days; (c) one-time only — chosen.
**Cost:** No predictable revenue. Every month starts at zero.
**Reversal:** ≥3 customers repurchase **unprompted** within 90 days. Then design the recurring
offer around what they actually repurchased, not around what we wish they would.

### D-11 — No free samples; a paid trial instead
**Decision:** The smallest paid unit is the trial. No unlimited or speculative free production.
**Evidence:** A-03 (our cost per video is unknown and possibly high); general principle that
free work is a cost with unproven return.
**Alternatives:** (a) free sample per prospect — unbounded cost, attracts non-buyers, and at an
unknown production cost it is an open-ended liability; (b) a public portfolio of *illustrative*
work on rights-clear properties, clearly labelled as such — chosen as the proof substitute;
(c) paid trial at a reduced scope — chosen as the low-commitment entry.
**Cost:** Loses prospects who will only move on free work. Acceptable — they are the least
likely to pay later.
**Reversal:** If qualified-lead-to-order conversion is under 10% after 40 conversations *and*
lost-reason analysis points to "wouldn't risk money on unseen quality," test a strictly bounded
free micro-sample (one 8-second clip, one property, one per company, hard cap of 5 per month).

### D-12 — Model first-order economics only; exclude LTV
**Decision:** [15](15-financial-model.md) contains no lifetime-value figure. CAC is justified
against first-order contribution margin alone.
**Evidence:** A-05; and the structural observation that LTV assumptions are the most common way
small service businesses justify unaffordable acquisition costs.
**Alternatives:** (a) assume 2.5 orders per customer — standard practice, unfounded here;
(b) first-order only — chosen.
**Cost:** Makes our allowable CAC look smaller than competitors'. We will appear to under-bid on
ad auctions. That is correct until proven otherwise.
**Reversal:** After 90 days of observed repeat behaviour, introduce a measured, conservative
repeat rate — not a forecast one.

### D-13 — Disclose AI assistance; do not hide automation
**Decision:** Our marketing says the work is AI-assisted. Any automated customer-facing message
identifies itself as automated. We never impersonate a human employee.
**Evidence:** E-14/E-15 (regulatory direction toward disclosure), E-16 (industry norm), E-17
(truthful and not misleading), plus the practical point that a customer discovering concealed
automation during a complaint converts a small problem into a trust failure.
**Alternatives:** (a) stay quiet about the method — common in the category and increasingly
risky; (b) lead with "AI" as the selling point — attracts price shoppers and invites the
"I'll just use the tool myself" objection at the worst moment; (c) disclose plainly, sell on
judgment and finish — chosen.
**Cost:** Some buyers discount AI-assisted work on principle. We lose them early, cheaply.
**Reversal:** None.

### D-14 — Primary acquisition channel is organic short-form video; paid is a test, not the plan
**Decision:** See [28](28-channel-strategy.md). Instagram/TikTok organic is primary; a bounded
Meta test is the experiment; search content is the slow compounding bet; cold outreach is not
used at launch.
**Evidence:** E-33 (short-form mechanics), E-28/E-29 (where the buyer's attention and stated
priorities are), A-04.
**Alternatives:** (a) paid-first — fastest signal, but at a $75 target CAC and an unproven offer
we would be buying traffic to an unvalidated page; (b) cold email/DM — channel rules and
platform risk, and it burns the founder's time at the exact hours production needs;
(c) organic-first with a bounded paid test — chosen.
**Cost:** Slow. Organic may produce nothing for 30 days, which is the explicit A-04 kill
condition.
**Reversal:** Zero qualified leads after 30 days of organic + $300 paid → pivot to
partnership-led acquisition before touching the offer.

### D-15 — Keep spending, publishing, messaging and refunds behind explicit human authorization
**Decision:** [39](39-data-and-agent-architecture.md) — no agent may send an external message,
publish content, spend money, or issue a refund without a human approval step. Agents may draft.
**Evidence:** General agent-safety practice plus the specific exposures here: a model inventing a
price, a guarantee, or a property fact would create a binding-looking promise we cannot honour
and an accuracy incident we cannot detect.
**Alternatives:** (a) full automation with guardrails — the founder's 8–10h absences (A-15) make
an unattended error a multi-hour error; (b) human-in-the-loop on external effects only — chosen.
**Cost:** Slower responses. Some leads go cold overnight.
**Reversal:** After [40](40-testing-plan.md) evals pass at scale on a specific narrow action
(e.g. sending a templated delivery notification with no variable claims), that single action may
be promoted to automatic. **One action at a time, each with its own eval.**
