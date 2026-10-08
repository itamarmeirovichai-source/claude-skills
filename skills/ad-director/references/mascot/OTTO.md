# OTTO: canonical character bible (LOCKED, 2026-10-08)

Otto is VXO's mascot: "the weird director" (Valéry × Otto). **This file is the single source of truth.** Every image or clip of Otto must match it. Never redesign him. Only pose, framing and setting may change.

## Canonical reference
- **Master image:** `otto_v2_pfp_1080.png` (Otto v2, `g1_octabox`, made 2026-10-08).
  - Local copy: `research/ai-video-reels/lab/experiments/M01_otto_pfp/v2/final/otto_v2_pfp_1080.png`. It is git-ignored; see *Storage* below.
- **Rule:** in every generation of Otto, the master image is passed as **image 1**, labelled "identity reference: keep this exact man". A new image of Otto never starts from text alone.

## Identity (never changes)
- **Face:** a man in his 50s with a long pale face, deep-set grey eyes, heavy dark brows, and real skin with pores and fine lines.
- **Signature:** an enormous charcoal-black handlebar moustache that completely covers his mouth. It is impeccably waxed real hair, sweeping out into two mirror-symmetrical upturned Dalí-style spirals with needle-thin tips.
- **Hair:** swept back, dark with silver flecks at the temples.

## Wardrobe (locked)
- tailored black turtleneck
- dark charcoal/black blazer
- deep-oxblood silk pocket square
- a vintage **brass director's viewfinder** on a thin brass chain

## Expression range
- **Default:** one brow slightly raised; eyes sharp, amused and knowing; charismatic warmth.
- **Never:** wide-eyed, startled, blank or creepy. The mouth is never shown.

## Look
- seamless charcoal backdrop with a warm brass-gold glow
- soft key at 45°, subtle rim light
- editorial magazine-portrait grade
- finished with the v1/v2 film recipe: 0.5 px soften, contrast 0.96, saturation 0.92, luma-weighted grain, light unsharp

## Prompt anchor block (paste at the start of every Otto prompt)
```
Image 1 is the identity reference: keep this exact man — long pale face, deep-set grey eyes, heavy dark brows, swept-back dark hair with silver temples, and his enormous charcoal-black waxed handlebar moustache with two mirror-symmetrical upturned Dali spirals that completely covers his mouth. Same tailored black turtleneck, dark charcoal blazer, oxblood silk pocket square, brass director's viewfinder on a thin brass chain. Relaxed brow, amused knowing eyes, never wide-eyed, never startled, mouth never visible.
```
**Always add this ban list:** no HDR, no oversaturation, no beauty smoothing, no plastic or waxy skin, no rubber moustache, not a cartoon, not a costume, no text or logos.

## Consistency roadmap
1. **Now:** the master image is passed as the reference on every call.
2. **Next (≈$2.50, needs approval):** build 20–30 approved images of Otto (turnaround plus an expression sheet, all from the master) and train a Higgsfield Soul ID (`/v1/custom-references`). That gives the strongest identity lock for all future stills and video.
3. **Video:** every clip starts and ends on an approved Otto still (Kling start/end frames).


## Locked voice and identity IDs (2026-10-08)
- **ElevenLabs voice (permanent, designed for Otto — never use another):** `IbpG1IF3UdxPgaDKhwsd` "VXO Otto (director)". Deep dry baritone (~78 Hz), subtle continental accent, slow deadpan timing. Design record: `research/ai-video-reels/lab/experiments/V01_voices/voices.json`.
- **Higgsfield Soul ID:** `26eef606-bf04-4db4-ab7a-6bdbe6dfea93` (cinema, 24 images). Status at last check: queued on Higgsfield's side.
- **Reference pack (used on every Flare/Seedance/Kling call):** master + three-quarter + profile + full body from `M02_otto_soulid/train/`. Verified in new scenes (M04 consistency test: PASS).

## Storage
Generated media is not committed to git, by project rule. The master image must live somewhere permanent, outside this container. See the decision log below.

## Decision log
- **v1 (rejected):** a safari vest that read as a tourist, a blank stare that read as creepy, a costume feel.
- **v2 (APPROVED as canonical):** the "Dalí meets Tom Ford" studio portrait.
