# VEE (Valéry): canonical character bible (DRAFT, 2026-10-08)

Vee is the second half of VXO ("Valéry × Otto"). Otto is the director, the craft. Vee is the producer, the deal. **This file is the single source of truth once a master image is approved.** Until then it is a draft: design and personality are fixed, and the master image is pending.

## Why two characters (from 30 §1 and 26 §2.7)
- Each character speaks to one of the two things a founder worries about when buying:
  - Otto answers **"will it look premium?"** (craft, taste, the frame).
  - Vee answers **"how fast, how much, does it sell?"** (deadline, price, results).
- The comedy comes from the gap between them. Otto wants one more take; Vee clicks her stopwatch: "It's perfect. Ship it."
- Personality before pixels:
  - **Want:** films out on time that move product.
  - **Flaw:** impatient with Otto's perfectionism.
  - **Behaviour:** clicks the silver stopwatch when she makes a point.

## Identity (never changes)
- **Face:** a woman in her late 30s, angular face with high cheekbones, warm olive skin with real texture (pores, a faint freckle cluster on the left cheekbone), strong straight dark brows, and dark brown eyes.
- **Signature (the "weird" feature):** a **platinum-white close-cropped buzz cut**, combined with **perfectly round oversized vermilion-red tinted spectacles** in thin gold wire frames.
  - The silhouette is instantly different from Otto's dark spiral moustache: light head and red circles versus dark spirals.
- **Mouth visible.** She does the talking, while Otto's mouth is never seen. That keeps lip-sync work on her only.

## Wardrobe (locked)
- an oversized ivory double-breasted suit (wide lapels, soft structure)
- a vermilion silk scarf knotted at the neck
- a vintage **silver stopwatch** on a short silver chain, clipped to the lapel

The palette complements Otto's: ivory, vermilion and silver against his charcoal, oxblood and brass.

## Expression range
- **Default:** composed, half-smile, one corner of the mouth up; eyes direct and quick, "I already know the answer".
- **Allowed:** deadpan at Otto, a sharp grin when the numbers are good.
- **Never:** vacant, glamour-pout, over-beautified or doll-like.

## Look
- the same studio language as Otto (seamless backdrop, soft 45° key, subtle rim)
- backdrop **warm stone-beige** with a cool silver rim, so the two can share a frame without merging
- grade: the same film recipe as Otto

## Prompt anchor block (paste at the start of every Vee prompt, after the master exists)
```
Image 1 is the identity reference: keep this exact woman — late 30s, angular face, high cheekbones, warm olive skin with real texture and a faint freckle cluster on the left cheekbone, strong straight dark brows, dark brown eyes, platinum-white close-cropped buzz cut, perfectly round oversized vermilion-tinted spectacles in thin gold wire frames. Same oversized ivory double-breasted suit, vermilion silk scarf knotted at the neck, silver stopwatch on a short chain clipped to her lapel. Composed half-smile, direct quick eyes.
```
**Ban list:** no HDR, no oversaturation, no beauty smoothing, no plastic skin, not a doll, not glamour makeup, no text or logos. Also never let her resemble a real public figure. If a candidate does, reject it.

## Consistency plan (mirrors OTTO)
1. Explore with Soul Cinema (cheap), then render 2 Flare finals and approve one master.
2. Make 24 Qwen edits of the master (angles, expressions, 3 lights, close/medium/full), QC them, and train a Soul ID (`cinema`).
3. Every clip starts from an approved Vee still and/or carries the Soul ID.

## Decision log
- 2026-10-08: design fixed (draft); the master is pending generation.
