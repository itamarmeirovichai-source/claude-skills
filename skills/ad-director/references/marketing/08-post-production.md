# Post-production: editing, grade and sound (21 YouTube tutorials read in full, 2026-10-07)

## Sources
- S1 Resolve linear WB: https://youtu.be/2wGqu_fOF_c
- S2 Artlist sound design: https://youtu.be/8LV1bqf8ZVo
- S3 sound design 2025: https://youtu.be/98CzEo5PIZ4
- S4 pro editor sound-designs a commercial: https://youtu.be/9HMLRfEDt04
- S6 motocross sound: https://youtu.be/CpE8Xdv9GF0
- S8 speed ramp AE: https://youtu.be/JNmT-wlki4c
- S9 ski commercial edit breakdown: https://youtu.be/LG9WxQkAXe0
- S10 trailer sound: https://youtu.be/LvFm-2hlMPs
- S11 Parker Walbeck, commercial editing: https://youtu.be/NVye0XagQuk
- S13 CapCut ramp: https://youtu.be/ROJgCDcL1gk
- S14 Nike breakdown: https://youtu.be/XHfyp-v4ctw
- S15 Think Media grade: https://youtu.be/jK_nYq4ZpgY
- S16 slide-ramp: https://youtu.be/kmnYxvGxLVE
- S17 sound crash course: https://youtu.be/l4fwsZWaIhc
- S19 3 sound secrets: https://youtu.be/tzfzkTAQsnE
- S21 8 speed ramps: https://youtu.be/xXTdxYYWOoo

[inf] marks our own inference; it was not stated in a source.

## Editing
- **Music first.** Split the track into sections (intro, build, peak, slow, end) and fill each with shots of matching energy [S9, S11, S14]. Snap cuts to beats ±1 frame.
- **Cut on action**, never on a still frame. If a clip overruns the beat, speed-ramp it to land on the beat instead of moving the cut [S11].
- **Give static AI shots an eased digital push-in** (fast start, slow settle, ~6%) [S11, S18].
- **Continuous motion direction** across cuts; write the direction into the prompts [S8, S16].
- **Juxtaposition:** one 4–6-frame burst of fast cuts before the hero, slow-motion holds between bursts [S14, S6, S9].
- **Let the hero breathe:** hold it 1.5–2.5 s [S9].
- **J/L cuts in sound:** start a shot's sound 6–12 frames before its picture [S2, S17].
- **Transitions:** cuts, speed-ramp whips with blur and a whoosh, or a sound-only transition [S2, S13, S16]. Avoid xfade wipes and slides. Use a crossfade only for the opening [S11].
- **Speed ramps:**
  - Stabilise first.
  - Smoothstep from 1× to 10–15× over 5–6 frames, with a slightly tilted plateau and the peak on the beat [S8, S16, S21].
  - Motion blur on the fast part (150° shutter), plus edge-only blur [S8, S9, S20].
  - ffmpeg: `minterpolate` to 120 fps → time remap → `tmix` during the peak.

## Grade (also unifies clips from different models)
1. **Neutralise and normalise each clip:** white balance with linear gain or `grayworld`; match black, mid and peak levels using `signalstats` [S1, S15].
2. **One shared look.**
   - Order: exposure → WB → contrast → saturation → LUT at ~0.2 strength (`blend` opacity 0.2–0.25) [S15].
   - Fragrance: dreamy, with lifted blacks and highlight rolloff: `curves=m='0/0.035 0.2/0.17 0.5/0.5 0.82/0.86 1/0.955'`.
   - Beverage: crisp, deep blacks.
   - Teal shadows, warm highlights: `colorbalance=rs=-0.04:bs=0.05:rh=0.04:bh=-0.03` [S7, S9, S14].
3. **Pull saturation spikes:** `vibrance=intensity=-0.15`. Desaturate the background hues to push focus to the subject [S14].
4. **Anti-AI finish [inf]:**
   - light softening (`gblur` 0.4–0.6 mixed in)
   - halation on highlights only, at 15–20%
   - **one grain pass on the final timeline** (after text)
   - subtle vignette

## Sound
- **Six layers** [S6]:
  1. music
  2. atmosphere bed (never dead air)
  3. risers and drops
  4. on-screen foley
  5. movement whooshes
  6. exaggeration
- **Ambience bed at about −24 dB**, ridden with camera speed. Crossfade 0.2–0.5 s at every boundary ("audio flows like a river") [S6, S17].
- **Foley: 3–5 layers per action**, split low/mid/high. Use emotional-realism substitutes: a pour becomes an ocean wave, a cap click becomes a glacier crack [S2, S4, S19].
- **Whoosh peak** on the fastest or most-blurred frame, about −9 dB [S3, S13]. **Riser → impact → boom** reserved for the reveal and the end card, all in one key [S10]. Reverse an impact to make a riser [S2].
- **Slow motion:** low-pass the music to about 1.8 kHz with constant-power crossfades; pitch the SFX down. Sweep a low-pass from 23.7 kHz down to 300 Hz across ramps [S6, S9].
- **Reverb glues the mix.** Distance = quieter + low-passed. Pan sounds with on-screen motion. Duck the music under the VO with a sidechain [S17, S2, S19].
- **Open with SFX only, and bring the music in on the first action.** End the music on a reverb tail [S6, S9, S19].

## Typography
- Blur-to-sharp eased reveals with a soft shadow [S5]. Scale settles from 104% to 100%.
- Text placed in depth, defocused with the scene [S14]. Put the grain over the text.
- Very quiet textural ticks to accompany type. Clean logo end card [S3, S4].

## Top 12 upgrades
1. Normalise clips before the look.
2. Full sound bed (six layers, J-cuts).
3. Cut to musical sections and on action; hold the hero.
4. Real speed ramps.
5. Motion blur at ramp peaks.
6. One grain/halation/vignette pass on the final.
7. Restrained film look (LUT ~0.2, gentle S-curve).
8. Foley layered by frequency.
9. Riser–impact–boom for reveals only.
10. Slow-motion audio treatment.
11. Eased push-ins and direction-matched cuts; no wipe presets.
12. Integrated, eased typography.
