# 27 — Production Quality Rubric

**Gate 2.** Technical and craft quality. Runs after [26](26-property-accuracy-rules.md), never
before.

**The separation matters:** Gate 1 asks "is this the property that exists?" and is binary. Gate 2
asks "is this well made?" and is scored. A video can score 95 on this rubric and still be
undeliverable because of one Gate 1 failure. **An average never overrides a factual error.**

---

## 1. Scoring

14 criteria, scored 0–5. Maximum 70.

| # | Criterion | 0 | 3 | 5 | Weight |
|---|---|---|---|---|---|
| Q1 | **Image artifacts** | Obvious smearing, melting, ghosting | Minor softness in one clip | Clean throughout | ×2 |
| Q2 | **Geometry** | Walls or doorframes bend; verticals lean | One brief edge distortion | Straight lines stay straight | ×3 |
| Q3 | **Texture stability** | Surfaces crawl or shimmer | Slight crawl on one texture | Stable | ×2 |
| Q4 | **Flicker** | Visible brightness pulsing | One clip pulses slightly | None | ×2 |
| Q5 | **Object continuity** | Objects appear, vanish, or morph | One object shifts slightly | Consistent | ×3 |
| Q6 | **Lighting continuity** | Light direction jumps between adjacent shots | Minor mismatch | Consistent | ×2 |
| Q7 | **Motion plausibility** | Motion a camera could not make | Slightly unnatural | Natural | ×2 |
| Q8 | **Camera movement** | Erratic, nauseating, or inconsistent in speed | Slightly uneven | Smooth and consistent | ×1 |
| Q9 | **Framing / cropping** | Subject cut awkwardly; key content in unsafe areas | Minor framing issue | Well composed at every ratio | ×1 |
| Q10 | **Text legibility** | Unreadable on a phone | Readable with effort | Clear at arm's length | ×2 |
| Q11 | **Caption accuracy** | Typos or factual errors | One minor wording issue | Correct | ×2 |
| Q12 | **Audio quality** | Clipping, abrupt cuts, wrong levels | Slightly hot or uneven | Clean, correctly levelled | ×1 |
| Q13 | **Brand consistency** | Ignores the agreed brand kit | Partially applied | Fully consistent | ×1 |
| Q14 | **Export correctness** | Wrong spec, oversize, wrong codec | One spec slightly off | All specs met | ×2 |

**Weighted maximum: 130.**

| Score | Outcome |
|---|---|
| **≥110** | Deliver |
| **90–109** | Fix the lowest-scoring items, re-review |
| **<90** | Rebuild. Do not patch |
| **Any hard reject** | Not delivered, whatever the score |

**Note the weights.** Q2 (geometry) and Q5 (object continuity) carry ×3 because they are the two
failure modes that make viewers say "this is AI" — and because interiors are the worst case for
both (A-03). They are also the two most likely to be quietly tolerated by whoever made the video,
which is exactly why they are weighted highest.

---

## 2. Hard rejection criteria

Independent of score. Any one of these blocks delivery.

| # | Defect | Why it is absolute |
|---|---|---|
| HR-1 | **Architectural geometry warps** — a wall, doorframe, window frame, or countertop visibly bends | The signature artifact. Humans detect it instantly and it reads as dishonesty, not as a glitch |
| HR-2 | **An object appears, disappears, or morphs** between frames | Implies the property contains something it does not, or loses something it does. Crosses into Gate 1 territory |
| HR-3 | **A person, animal, or reflection is generated** | Nobody consented to appear. Rights and plausibility failure |
| HR-4 | **Text is illegible on a phone at arm's length** | The deliverable does not function |
| HR-5 | **A caption states a fact absent from the fact sheet** | Gate 1 overlap. Never shipped |
| HR-6 | **Audio clips, or music is present on the Vrbo cut** | E-04 — the cut would be rejected by the platform |
| HR-7 | **Contact details appear in frame on the Vrbo cut** | E-05 — same |
| HR-8 | **A file exceeds its platform spec** (GBP >75MB or >30s; Vrbo >2min or <15s) | E-03, E-08 — unusable on its destination |
| HR-9 | **First and last frames of the silent loop do not match** | Visible jump on repeat; the deliverable does not do its job |
| HR-10 | **Motion so strong the source photograph is no longer recognisable** | At that point we are no longer showing their property |

---

## 3. Acceptable vs unacceptable — worked examples

| Situation | Verdict | Reasoning |
|---|---|---|
| Slow push into a living room; the frame edges soften very slightly | ✅ **Acceptable** | Q1 minor, geometry holds. Within normal tolerance |
| Slow push; the doorframe on the right bows outward | ❌ **HR-1** | Geometry failure, regardless of how good the rest is |
| Curtains drift gently in still air | ✅ **Acceptable** | Plausible motion, architecture static |
| A cushion changes pattern between frames | ❌ **HR-2** | Object continuity |
| A grade warms a midday interior slightly | ✅ **Acceptable** | Within the light the photo contains |
| A north-facing room graded to golden hour | ❌ **Gate 1 §3.** | Invents light the property does not get |
| Water in a pool ripples; the pool edge stays fixed | ✅ **Acceptable** | Motion, not alteration |
| The pool appears slightly longer as the camera moves | ❌ **Gate 1 §3 + HR-1** | Dimensional change |
| A caption reads "8 minutes to the beach" and the fact sheet says 8 minutes | ✅ **Acceptable** | Verified fact |
| A caption reads "steps from the beach" and the fact sheet says 8 minutes | ❌ **HR-5** | Unverified, and materially different in meaning |
| The Vrbo cut runs 52s with natural sound and no on-screen text | ✅ **Acceptable** | E-03–E-05 satisfied |
| The Vrbo cut is the social cut with the music left in | ❌ **HR-6** | Would be rejected by the platform |

---

## 4. Artistic preference vs technical failure

The most common way a quality gate degrades is by absorbing taste arguments until nobody trusts
it. The distinction:

| **Technical failure** (we fix, free) | **Artistic preference** (revision round, [14](14-offer-specification.md) §4) |
|---|---|
| Geometry warping | "I'd have used a different music track" |
| Object morphing | "Too slow / too fast for my taste" |
| Flicker, texture crawl | "I prefer warmer colour" |
| Illegible text | "Different font" |
| Wrong export spec | "Start with the kitchen instead" |
| Audio clipping | "Different shot order" |
| Caption factual error | "Different caption wording" |

**The test:** would any competent editor call it a defect? If yes, technical — we fix it at our
cost. If it depends on taste, it is a revision, and it is handled through the scope categories
without argument or resentment.

---

## 5. Human review requirements

| Requirement | |
|---|---|
| **Who** | A human. **Never a model** (D-15) |
| **When** | After Gate 1, before export |
| **How** | Watched at full speed with sound, then at full speed muted, then the flagged clips frame-stepped |
| **Device** | **At least once on a phone.** Q10 cannot be assessed on a monitor |
| **Time budget** | 8 minutes for a Standard order |
| **Record** | Score per criterion, hard-reject checks, reviewer, timestamp |
| **Independence** | On a portfolio job, review **per property.** Never batch-approve |

---

## 6. Escalation

| Situation | Action |
|---|---|
| Score 90–109 | Fix and re-review. Log which criteria failed |
| Score <90 | Rebuild from storyboard. **Do not patch** — a patched sub-90 video usually fails again on a different criterion |
| Hard reject, fixable | Re-generate that clip, maximum 2 attempts, then re-storyboard the shot |
| Hard reject, not fixable | Cut the shot. If the video cannot work without it, move the deadline and tell the customer why |
| Same criterion fails on 3 consecutive orders | **Process problem, not a clip problem.** Change the prompt library, the source-photo threshold, or the tool ([25](25-tool-comparison.md)) |
| **A defect reaches a customer (gate escape)** | Free fix, prioritised. Then review the gate itself: was the time budget too short, the checklist wrong, or the reviewer rushed? Log the cause, not just the fix |
| 2 gate escapes in 20 orders | Stop taking new orders until the gate is fixed ([37](37-capacity-and-contractors.md)) |

---

## 7. Acceptance criteria

- [ ] Gate 2 recorded on 100% of delivered videos, with scores per criterion
- [ ] Zero delivered videos with a hard-reject defect
- [ ] Median score ≥110 across the first 20 orders
- [ ] Every hard reject logged with cause and resolution
- [ ] **Zero gate escapes** in the first 20 orders
- [ ] Criterion-level failure data reviewed after every 10 orders to find process problems
- [ ] At least one review per order performed on a phone
