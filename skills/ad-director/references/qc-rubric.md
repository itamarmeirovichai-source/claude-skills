# QC rubric: the gate every clip and every ad passes

Three layers. A clip or ad moves forward only after each layer passes.

1. **Take QC (per generated clip, 20 seconds each).** Done right after generation and before editing. Keep it or regenerate it.
2. **Automated QC (per render).** Run `director.py qc final.mp4 --packshot packshot.png --duration 15`.
3. **Visual QC (per render).** Claude reads `qc_sheet.jpg` + `product_compare.jpg` + the clip at 0.25x speed, then scores the table below.

---

## Layer 1: take QC (keep / regenerate)

Watch the clip twice: once at full speed, once frame-stepped through the hard moment. Regenerate on any **KILL**.

| # | KILL if... | Where to look |
|---|---|---|
| K1 | Label text changes, smears, mirrors, or letters invent themselves | Every frame with the product. Compare against the packshot. |
| K2 | Product shape or proportion drifts (cap grows, can becomes bottle) | First vs last frame, side by side |
| K3 | Hands show 6 fingers, fused fingers, or a hand passing through the product | Frame-step the contact moment |
| K4 | Face drifts in identity, teeth melt, eyes go wrong or look in different directions | Mid-clip and last frame |
| K5 | Liquid behaves wrong (rises, vanishes, glass refills itself, volume changes) | Pour shots, frame by frame |
| K6 | A second product, a ghost logo or random text appears | Background, reflections |
| K7 | The camera move is not the one asked for, or it snaps or jumps | Full speed |
| K8 | Flicker, boiling textures or a morph between objects | Full speed, then 0.5x |

**Fixable in post (keep):** small background warping you can crop, a slightly wrong label you can composite over from the real packshot (chapter 16), and colour shifts you can grade.

**Budget rule.** Hero shots usually keep about 1 in 4–8 takes. Simple shots keep about 1 in 2. If you pass 3x the budget, change the method instead of re-rolling: switch to a start frame, a shorter clip, a different model, or cut on contact.

---

## Layer 2: automated (`director.py qc`)

| Check | Rule | Why |
|---|---|---|
| resolution / fps / codec | 1080x1920, ≥24 fps, h264/aac | Platform transcodes punish anything else |
| duration | Within 0.5 s of target, under platform max | Ad slots and cutdowns |
| loudness | -14 LUFS ±1.5, true peak ≤ -1 dBTP | Matches platform normalisation; no clipping |
| audio_hook | Sound within the first 0.6 s | The hook has to be audible |
| hook_pacing | First visual change ≤3 s (unless `--one-take`) | Retention cliff at 3 s |
| shot_length | No shot >4.5 s (unless one-take) | Drag on Reels |
| black / frozen | No black at start; no freeze mid-ad (end card is fine) | Broken encodes, stalled AI clips |
| flicker | No luma jumps outside cuts | AI flicker, exposure pops |
| product_colour | Brand-colour histogram match ≥0.5 against the packshot | Drifted packaging colour or a missing product |

The product-colour check is colour-only. It does **not** read the label. Label correctness is always checked visually with `product_compare.jpg`.

---

## Layer 3: visual score (/100). Ship at ≥80 with no FAIL.

| Area | Pts | Full marks when... | Automatic FAIL |
|---|---|---|---|
| **Hook (0–2 s)** | 15 | Frame 1 stops the thumb with sound off. A clear anomaly, question or payoff. Readable in 0.5 s. | First 2 s are a logo or a slow establishing shot |
| **Idea & brand** | 15 | Passes the brand-swap test (it only works for this brand). The product *causes* the turn. One clear message. | Works the same with a competitor's logo |
| **Product fidelity** | 20 | Label, colour, shape and cap all match the packshot in every product frame. Real packshot composited on the end card. | Any wrong text on the product; wrong colour or shape |
| **AI artifacts** | 15 | Zero K1–K8 issues visible at 1x. Nothing a viewer could screenshot as "AI fail". | Visible hand, face or label artifact |
| **Motion & physics** | 10 | Camera moves are motivated and smooth. Liquids, cloth and gravity are believable (or break exactly one law on purpose). | Physics break that looks like an error, not an idea |
| **Sound** | 10 | Sound design carries the story: foley on contact, music hits the cuts, VO clear, sonic logo at the end. | Silent, or music fighting the VO |
| **Edit & text** | 10 | Rhythm matches the music. Supers are short, inside safe zones and on screen ≥1.5 s. Cutdowns (6 s, 15 s) also work. | Text under the UI zones; typo |
| **Legal & platform** | 5 | AI disclosure, category lines (alcohol 21+, med-spa, real-estate brokerage), no fake testimonials, claims substantiated. | Unsubstantiated claim, fake testimonial, missing mandatory line |

**Scoring discipline.** Score as the client's harshest stakeholder would. A 90+ is rare: save it for a piece you would post in the studio's own portfolio. Write one sentence per area. When a score is under full marks, the sentence must name the fix.

### Before delivery: 60-second self-checks
1. **Sound off:** watch muted on a phone. Is the story still clear?
2. **3-second test:** show only the first 3 s to someone (or re-watch cold). Do they know what it is about?
3. **Brand recall:** after one view, can you name the brand? If not, the brand is too late or too small.
4. **Screenshot test:** pause at 5 random points. Is there any frame you would be embarrassed to see shared?
5. **Client-eyes test:** does the product look *better* than in reality, or *different* from reality? Better is good. Different is a FAIL.
