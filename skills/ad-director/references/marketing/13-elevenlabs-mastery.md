# ElevenLabs mastery: VO, music, SFX for premium 9:16 ads (verified 2026-10-07)

**Sources**
- Docs index: https://elevenlabs.io/docs/llms.txt
- Every claim marked **[E05]** was tested in our lab. Files are in `research/ai-video-reels/lab/experiments/E05_elevenlabs/` (each subfolder has a `results.json`).
- `[inf]` marks our own inference.
- "Sounds right" was judged by measurement, not by ear: duration, words/sec, LUFS, F0, spectral centroid, silencedetect, and a scribe_v2 speech-to-text / audio-event check. **Audition the mp3s before you lock a voice.**

## 0. The six things that changed or surprised us
1. **Eleven v4 exists.** `eleven_v4` is ElevenLabs' recommended TTS model. It follows tags much more strongly than v3:
   - `[whispers]` on v4 gave a near-true whisper: voiced ratio 0.31, −26 LUFS.
   - The same tag on v3 only made the voice breathier: voiced ratio 0.53, −19 LUFS. [E05/b]
   - v4 has **no Style or Speed**. They are accepted by the API but ignored. Only Stability and Similarity work.
   - v4 supports IPA pronunciation inline as `"/ˈnwɑːr/"`.
   - Sources: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 and https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
2. **SFX can now be up to 30 s** (0.5–30 s; 0.1 in the overview), not 22 s. The `prompt_influence` default is **0.3**; ours is 0.4. Model: `eleven_text_to_sound_v2`. Source: https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
3. **Our `music` command silently uses `music_v1`.** That is the API default, and the docs call it "outclassed". Always send `model_id: "music_v2_5"`. Source: https://elevenlabs.io/docs/overview/models
4. **Composition plans are the only way to get timing you can trust.**
   - Hard stops and impacts landed within about 50 ms of the section boundaries. [E05/c]
   - A prompt with written timestamps ignored the silent intro and the final hit.
   - Plans reject `force_instrumental` with HTTP 422. Put "instrumental" in the styles instead and "vocals" in `negative_styles`.
5. **SFX loudness is all over the place:** −70 to −7 LUFS for the same kind of request. Onsets drift between 0 and 1.1 s. **Always trim to the onset and normalise loudness** before you place a sound. [E05/d]
6. **Shared Voice Library voices work directly by `voice_id` in TTS.** No "add to library" step is needed on the Creator tier. [E05/a]

## 1. Verified API parameters
**TTS:** `POST /v1/text-to-speech/{voice_id}[/with-timestamps|/stream]`

| Field | Values / notes |
|---|---|
| `model_id` | `eleven_v4` (10k chars, 90+ languages), `eleven_v3` (5k chars, 70+ languages), `eleven_multilingual_v2` (most stable long-form; supports SSML `<break>` up to 3 s), `eleven_flash_v2_5` (fast, cheap). **v3 and v4 do not support `<break>`.** |
| `voice_settings` | `stability` 0–1 (default 0.5)<br>`similarity_boost` (0.75)<br>`style` (0; v2/v3 only)<br>`use_speaker_boost` (true)<br>`speed` 0.7–1.2 (v2/v3 only) |
| v3 stability | The API accepts any float. 0.3 was accepted [E05]. Low = "Creative", 1.0 = "Robust". |
| `seed` | 0–4294967295, best effort. Use it so takes can be compared like for like. |
| `previous_text` / `next_text`, `previous_request_ids` / `next_request_ids` (max 3) | Keep prosody continuous when the VO is split into lines. |
| `language_code`, `apply_text_normalization` (`auto`/`on`/`off`), `pronunciation_dictionary_locators` (max 3) | — |
| `output_format` | `mp3_44100_128` (default), `mp3_44100_192`, `pcm_48000`, `wav_44100`, `opus_48000_192`. Use **pcm_48000 or wav for mastering**. |
| Response | The with-timestamps response returns `alignment` and `normalized_alignment`. On v4 the tag characters (`[softly]`) **are included**, so strip them (our `chars_to_words` already does). [E05] |
| Cost | The `Character-Cost` response header gives the credits used. Log it.<br>Observed: v3 ~0.45 credit/char, v4 ~0.13 credit/char on this plan. [E05] |

**Sound effects:** `POST /v1/sound-generation`
- Body: `text`; `duration_seconds` (0.5–30, null = auto); `prompt_influence` (0–1, default 0.3); `loop` (bool, v2 model only); `model_id: eleven_text_to_sound_v2`.
- Output: MP3, or **WAV 48 kHz for non-looping sounds**.
- Billing: 40 credits per second when a duration is specified, per the docs. Observed usage in E05 was far lower.
- Source: https://elevenlabs.io/docs/overview/capabilities/sound-effects

**Music:** `POST /v1/music` (audio, with a `Song-Id` header), `/v1/music/detailed` (multipart JSON plus audio; `with_timestamps` for lyrics), `/v1/music/stream`, `POST /v1/music/plan` (prompt → editable plan).
- `model_id`: `music_v1` (default), `music_v2`, `music_v2_5`.
- `music_length_ms`: 3,000–600,000.
- `prompt` **or** `composition_plan`, never both.
- Other fields: `seed`, `force_instrumental` (prompt only), `store_for_inpainting`, `sign_with_c2pa`, `finetune_id`.
- v2/v2.5 plan:
  - `{"chunks":[{text, duration_ms 3,000–120,000, positive_styles ≤50, negative_styles ≤50, context_adherence low|medium|high}]}`
  - Up to 30 chunks; total length 3 s–10 min.
  - The first chunk's styles set the genre: give it 6–7 or more.
  - `text` holds `[Section]`, lyric lines, `{inline cue}` and `(ooh)` vocal sounds.
- v1 plans use `positive_global_styles` and `sections[]` instead.
- Also available: inpainting (`source_from`/`song_id`), **video-to-music** (multipart, up to 10 videos / 600 s / 200 MB, plus description and tags), and stem separation.
- Sources: https://elevenlabs.io/docs/api-reference/music/compose, https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans, https://elevenlabs.io/docs/api-reference/music/video-to-music

**Voice Design:** `POST /v1/text-to-voice/design`
- `voice_description` (required).
- `text`: 100–1,000 characters, or `auto_generate_text`.
- `model_id`: `eleven_multilingual_ttv_v2` or `eleven_ttv_v3`.
- `guidance_scale` (default 5), `loudness` (−1 to 1; 0 ≈ −24 LUFS), `seed`, `should_enhance`, `quality`.
- `reference_audio_base64` and `prompt_strength` (ttv_v3 only).
- Returns 3 previews, each with a `generated_voice_id`. Save one with `POST /v1/text-to-voice` (this uses a voice slot).
- Source: https://elevenlabs.io/docs/api-reference/text-to-voice/design

**Text to Dialogue:** `POST /v1/text-to-dialogue[/with-timestamps]`
- `inputs[{text, voice_id}]`: at most 10 unique voices; keep the total at or under 2,000 characters.
- `model_id`: `eleven_v3` (default) or `eleven_v4`.
- `settings{stability, similarity}`, `seed`, `previous_text`/`future_text` (100 characters each).
- Source: https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert

**Other endpoints**
- **Forced alignment:** `POST /v1/forced-alignment`, multipart `file` + `text`. Returns word and character times plus `loss`. Use it to caption VO recorded outside ElevenLabs.
- **Speech-to-speech:** `POST /v1/speech-to-speech/{voice_id}`, multipart `audio`, `model_id: eleven_multilingual_sts_v2`, `remove_background_noise`. Use it to re-voice a guide read we record ourselves and keep our timing.
- **Shared library:** `GET /v1/shared-voices`, with `search`, `use_cases`, `gender`, `age`, `accent`, `language`, `descriptives`, `sort=usage_character_count_1y|trending|cloned_by_count`, `page_size≤100`.
- **STT QA:** `POST /v1/speech-to-text`, `model_id=scribe_v2`, `tag_audio_events=true`.

## 2. Best voices per niche [E05/a]
Method:
- All takes on eleven_v3, stability 0.5, seed 7, identical line per niche.
- Every take passed STT with WER 0. Tech takes scored 0.08, but only for the US spelling "organized".
- Metrics: wps = words per second of speech; f0 = median pitch; range = pitch range in semitones (5th–95th percentile); centroid = brightness.

**Luxury fragrance.** Line: *"Some things are never said... only remembered. Noir Vesper. The scent of after midnight."* (speed 0.9)

| Rank | Voice (ID) | Evidence | Why |
|---|---|---|---|
| 1 | **Jenna – Warm, Soft, Sultry** `qFjcP4hHD9WIdODvuJOJ` (F) | Darkest centroid of the set (1,602 Hz); 1.67 wps; f0 174 Hz; dense −13 LUFS | Intimate and close. Tags move her strongly (§3). |
| 2 | **Frederick Surrey – Smooth, Velvety** `j9jfwdrw7BRfcR43Qohk` (M, British) | f0 89 Hz; controlled 8 st range | A smooth "maison" baritone without melodrama. |
| 3 | **Edward – British, Dark, Seductive, Low** `goT3UYdM9bhm0n2lmKQx` (M) | 96 Hz; 22.5 st range (theatrical) | Use for bold noir or oud scents. Too dramatic for soft florals. |
| Alt | Lily (premade) `pFZP5JQG7iQjIQuC4Bku`; Allison – Velvety `Se2Vw1WbHmGbBbyWTuu4` | Lily: slowest (1.55 wps) but quiet (−19 LUFS) and adds extra pauses. Allison: f0 213 Hz, bright. | — |
| Custom | **Voice Design** (ttv_v3): *"Native English. Female, early 40s. Studio-quality recording. Low, warm, slightly husky timbre with a soft breathy edge; slow, deliberate, intimate pacing… luxury perfume film."* | Previews came out at f0 142–150 Hz, about 25 Hz lower than any female library voice we tried; 1.57–1.8 wps | Generated IDs are in `g_voice_design/design.json`. |

**Energetic beverage.** Line: *"Crack it open. Feel the cold hit. VOLT. Zero sugar. All charge."* (speed 1.05)

| Rank | Voice (ID) | Evidence | Why |
|---|---|---|---|
| 1 | **Allison – Energetic, Clear, Bubbly** `xctasy8XvGp2cVO9HL9k` (F) | Loudest (−13.6 LUFS); 1.88 wps; f0 250 Hz | Bright, forward, cuts through a drop. |
| 2 | **Charlie – Deep, Confident, Energetic** (premade) `IKne3meq5aSn9XLyUdCD` (M, Australian) | Widest intonation of the set (24.6 st) | Reads as punchy. Low centroid (1,377 Hz), so it sits under synths. |
| 3 | **Christina – Energetic Commercial** `BuaKXS4Sv1Mccaw3flfU` (F) | Classic ad cadence; even 0.5–0.7 s pauses | A safe client-friendly read. |
| — | Liam (premade) `TX3LPaxmHKxFdv7VOQHJ` | Fastest (1.92 wps) but flat (8.5 st) and quiet (−24 LUFS) | Sounds like a creator, not a brand voice. |

**Calm tech.** Line: *"Your day, quietly organised. Halo listens, learns, and gets out of the way."*

| Rank | Voice (ID) | Evidence | Why |
|---|---|---|---|
| 1 | **Lucius – Calm, Pleasant, Reassuring** `HaUDdkOAoitiVjpiet1i` (M) | Warmest centroid (1,198 Hz); 1.91 wps; very even (LRA 1.3) | Unhurried, Apple-keynote calm [inf]. |
| 2 | **Hope – Natural, Clear and Calm** `OYTbf65OHHFELVut7v2H` (F) | Most even (LRA 1.2); 2.39 wps | Conversational and modern. One of the most-used library voices. |
| 3 | **Emily E. – Premium Female Commercial** `CXoGcuszI2UkuF6sqV8W` (F, British) | 1.91 wps; deliberate 0.9 s comma pause | Premium and polished. |
| — | River (premade, neutral) `SAz9YHcvj6GT2YYXdXww`; Miles – Technical British `rNzVNTrvSffyxdrTbLKv` | — | Fine as fallbacks. Miles is more animated (16.8 st). |

**Pacing rule from the data:**
- Premium VO lands at **1.6–1.9 words/s**, including the pauses.
- Budget about **10–12 words for a 6 s cutdown** and **28–35 words for 20 s**.
- Fragrance VO should fill no more than 50% of the runtime.

## 3. v3 / v4 tag cheat-sheet (tested on one tagline) [E05/b]
Tagline *"Noir Vesper. The scent of after midnight."*, voice Jenna, seed 11. Baseline (v3, plain): 3.44 s, −13.1 LUFS, voiced ratio 0.74.

| Markup | Measured effect | Use it for |
|---|---|---|
| `...` (ellipsis) | **Adds about 1.0–1.2 s of pause each.** A period gives about 0.6 s. Total length 3.4 → 5.3 s. | The most reliable timing lever. Write pauses as `...` and line them up with the cuts. |
| CAPS (`AFTER`) | +0.3 s; slight pitch lift (+0.5 st) | Subtle stress on one word. Don't use more than one per line. |
| `[whispers]` v3 | −5.7 dB, voiced 0.53, +600 Hz air | Breathy rather than fully whispered. Good for fragrance. |
| `[whispers]` **v4** | −13 dB, voiced 0.31: a real whisper | ASMR-style closes. Make up the level in the mix. |
| `[softly]` v3 | −2.5 dB, voiced 0.62, +0.5 s | Gentle warmth without losing body. **Best default for luxury.** |
| `[softly] ... [whispers] … MIDNIGHT` v3 | −2.8 dB; still intelligible | Arc from spoken to whispered. |
| Same combo on **v4** | Voiced 0.13: almost fully whispered | Too far for a brand name. Use `[softly]` only on v4. |
| `[breathy, intimate, slow]` (free-form) | +1.1 s, pitch −21 Hz | Descriptive tags work. v4 docs recommend explicit voice-quality tags such as `[low, gravelly voice]`. |
| Stability 0.0 vs 1.0 (same combo) | Pitch range 13.6 st vs 7.0 st; pause 1.1 s vs 0.6 s | 0 for emotive reads, 0.5 for normal reads, 1.0 for exact legal or brand lines. |
| `[exhales]` / `[pause]` | `[pause]` gave a 1.6 s gap. `[exhales]` was rendered as an audible sigh (STT tagged it as `[sighs]`). | Breath before the brand name. |

Other tags from the docs: `[laughs]`, `[sighs]`, `[excited]`, `[curious]`, `[sarcastic]`, `[mischievously]`, `[shouts]`, `[clears throat]`, `[strong X accent]`.
- Tags are **natural language, not an enum**.
- Match the tag to the voice: a calm voice won't shout convincingly.
- Tags can be read as sound effects (`[applause]`), so describe delivery explicitly.
- Source: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v4

**Which model:**
- **v4** for whispers, real tag obedience, IPA pronunciation of brand names, and lower cost.
- **v3** when you need `speed`/`style` or a voice that sounds better on v3. v4 changes how some voices sound, so A/B both.

**Pronunciation:**
- v4: inline IPA, e.g. `"/vɛsˈpɛr/"`.
- v2: `<phoneme>` tags (flash_v2), alias dictionaries (`.pls`), or respellings ("trapezIi").
- **Spell out numbers and prices** ("forty-nine dollars").

## 4. Music: plan templates per niche [E05/c]
**What the composition plan honoured, measured in plan_v25_bev2 and plan_v25_beverage:**
- A first chunk asking for "near silence / single hum" rendered **digital silence** (−138 dB) for the full 3 s. Use that time for SFX-only openings.
- `[Break]` with negatives `drums, bass, melody` and "hard stop, total silence": the stop came at **15.05 s for a 15.0 s boundary**, then decayed to −83 dB.
- `[Outro]` with `context_adherence: "low"` and styles "one massive cinematic impact on the downbeat, loud": **the hit landed at 18.00 s exactly** and rose 70 dB.
- **What failed:**
  - Asking for "breath + resolve" without a loud cue just gave one long fade, with no final hit.
  - Exactly where the drop falls inside a section is not reliable. In one take the drop came 1.5 s late, with a nice 0.45 s pre-drop gap. In another take the energy peaked 4 s into the drop chunk.
  - **Place hard events on chunk boundaries**, and back them with an SFX hit.
- The prompt-only version ("0:00–0:03 near silence…") played music from 0.25 s and had no final hit. It only roughly honoured the stop (0.5 s late).
- **Minimum chunk is 3 s**, so a 6 s cutdown has at most two chunks. A 1.5 s "breath" must be cut in the edit or covered with SFX.
- Loudness: plans come out hot and dynamic (−9.8 LUFS, LRA 23). Normalise the bed to about −20 LUFS before the VO goes in.

**Template A: Fragrance 20 s** (verified: silence → piano at 1.5 s, swell, peak around 13 s, decay to the end)
```json
{"chunks":[
 {"text":"[Intro]\n{room tone}","duration_ms":3000,"positive_styles":["luxury fragrance commercial","cinematic neo-classical","72 BPM","D minor","instrumental","felt piano single notes","close-mic'd, intimate","tape warmth","very sparse"],"negative_styles":["vocals","drums","EDM","bright pop"],"context_adherence":"high"},
 {"text":"[Swell]","duration_ms":8000,"positive_styles":["low cello drone enters","slow string swell","breathy pads","growing warmth"],"negative_styles":["vocals","percussion","fast tempo"],"context_adherence":"high"},
 {"text":"[Peak]","duration_ms":5000,"positive_styles":["full lush strings","deep low pulse","emotional peak","wide cinematic reverb"],"negative_styles":["vocals","EDM drop","trap drums"],"context_adherence":"high"},
 {"text":"[Resolve]\n{final chord}","duration_ms":4000,"positive_styles":["single sustained piano and string chord","D major resolution","long natural decay"],"negative_styles":["vocals","new melody","abrupt cut"],"context_adherence":"medium"}]}
```

**Template B: Beverage 22 s.** Hook silence → build → drop → breath → logo hit. Verified boundaries at 3.5 / 15.05 / 18.00 s.
```json
{"chunks":[
 {"text":"[Intro]\n{near silence}","duration_ms":3000,"positive_styles":["minimal electronic","premium energy drink commercial","124 BPM","F minor","instrumental","single sub-bass hum only","very quiet","pristine modern production"],"negative_styles":["vocals","drums","melody","loud"],"context_adherence":"high"},
 {"text":"[Build]\n{filtered kick}\n{riser}\n{drop gap}","duration_ms":6000,"positive_styles":["low-pass filtered kick","white-noise riser","tension building fast","ends with a half-beat of silence"],"negative_styles":["vocals","full drop"],"context_adherence":"high"},
 {"text":"[Drop]\n{drop hits on the first beat}","duration_ms":6000,"positive_styles":["drop starts immediately on beat one","punchy kick and clap","distorted synth stabs","maximum energy"],"negative_styles":["vocals","intro","build-up","fade in"],"context_adherence":"high"},
 {"text":"[Break]\n{silence}","duration_ms":3000,"positive_styles":["hard stop","total silence","tape stop"],"negative_styles":["drums","bass","melody","vocals"],"context_adherence":"low"},
 {"text":"[Outro]\n{one huge impact}\n{chord rings out}","duration_ms":4000,"positive_styles":["one massive cinematic impact on the downbeat","loud","F minor stab chord with long reverb tail","brand sonic logo"],"negative_styles":["vocals","silence","fade in","quiet"],"context_adherence":"low"}]}
```

**Template C: Calm tech 20 s** [inf; built from the same rules, not yet generated]
- Chunk 1, `[Intro]` 3 s: "minimal ambient electronica, 96 BPM, E major, instrumental, soft glassy pluck arpeggio, warm analog pad, airy, clean modern production"; negatives: vocals, drums, distortion.
- Chunk 2, `[Groove]` 9 s: "light sidechained pulse, soft rimshot, rounded sub bass".
- Chunk 3, `[Lift]` 5 s: "pad opens, arpeggio doubles an octave up, gentle optimism".
- Chunk 4, `[Outro]` 3 s, `context_adherence: low`: "E major chord rings out, single glass mallet note".

**6 s cutdown:** two chunks, 3 s each: [Hook / impact] and [Logo / ring-out]. Or simply cut the 20 s plan at its boundaries.

**Prompt craft (docs):**
- Answer genre, mood, instruments, BPM/key and era, or "the model answers with the most average choice".
- Use studio words: *sidechained, close-mic'd, bone-dry, tape saturation, plate reverb*.
- Narrate the arrangement with *start with… just… then… bring in*. Write the silences explicitly.
- Styles must be in English. Naming a copyrighted artist returns `bad_composition_plan` with a suggested alternative.
- Source: https://elevenlabs.io/docs/overview/capabilities/music/best-practices

## 5. SFX prompt library [E05/d]
Each sound was tested three ways: plain prompt at influence 0.3, pro prompt at 0.3, and pro prompt at 0.8. scribe_v2 audio-event tags were used as a blind check.

| Sound | Winning prompt (influence) | What failed |
|---|---|---|
| Glass cap | Plain `"glass perfume bottle cap"` @0.3 (STT: "[bottle opening]"). Clink at **1.1 s**, so trim it. | "heavy faceted glass stopper…" @0.3 came out almost silent (−61 LUFS); @0.8 a dull thud (677 Hz). The word "heavy" pushes it toward a thud. |
| Spray mist | `"Close-mic'd studio foley, dry, no music: one short perfume atomizer spray, soft pump click then a fine pressurized mist hiss"` @0.8 (6.6 kHz hiss) | Plain "perfume spray" was read as typing. |
| Can crack | Plain `"soda can opening"` @0.3 (STT: "[opening can]"). The pro prompt @0.8 adds 1 s of fizz tail. | — |
| Pour | Any wording works (STT: "pouring" every time). The pro prompt @0.3 gives the longest pour (2.2 s active). | — |
| Ice | Pro prompt (`"…three ice cubes dropped one by one into an empty crystal tumbler, bright clinks…"`) **@0.8**: "[ice clinking]" | The same prompt @0.3 gave **"shattering glass"**: low influence plus "crystal" leans toward breakage. |
| Fabric | `"…a single slow sweep of heavy silk satin, soft airy swish"` @0.3 | All takes were quiet (−35 to −41 LUFS). Gain them up. |
| Click | `"…one premium tactile click of a small machined aluminium button, ultra short and crisp"` @0.3 (90 ms, 7 kHz) | Plain "button click" came out silent (−70 LUFS). |
| Whoosh | Plain `"whoosh"` (bright, 0.3 s) **plus** a separate low layer | "…whoosh with a deep low-end swell" put the energy at 180 Hz: a boom, not air. **Generate air and sub as separate layers.** |

**Rules**
- Use the prefix `"Close-mic'd studio foley, dry, no music: "` plus **one action, one object and one material**.
- Use 0.8 when the noun is ambiguous (ice, glass). Use 0.3 for textures.
- Always set `duration_seconds`.
- Generate 2–3 takes and pick one. Results swing ±30 dB.
- Doc tips:
  - Write sequences in time order ("…, then…").
  - Useful vocabulary: *impact, whoosh, braam, drone, glitch, one-shot, stem*.
  - Musical requests work too ("brass stabs in F minor").
  - Combining several effects into one prompt is worse than layering them in the edit.
  - Source: https://elevenlabs.io/docs/help-center/product/core-capabilities/sound-effects/how-do-i-prompt-for-sound-effects
- Emotional substitutes still apply (08-post-production): a pour can become an ocean wave, a cap a glacier crack.

## 6. Sonic logo (2 s) [E05/e]
- **The SFX model cannot play exact notes.** Asking for "E–G#–B marimba" gave a gliding sweep from D#4 to C5.
- **The Music API can.** `music_v2_5`, 3 s (the minimum), prompt *"three-note ascending glass marimba motif E, G sharp, B, then a soft warm synth pad chord in E major rings out… instrumental, no drums"* gave E4 → G#4 (0.1 s) → E5 (0.4 s), in key. It decayed to −40 dB by 1.9 s, so it can be trimmed to 2.0 s with a 0.3 s fade.
- SFX is good for **texture logos**:
  - Fragrance "one crystal glass chime struck once…" @0.6: a clean A6 ring that decays by 1.1 s.
  - Beverage "can-tab snap → swoosh → punchy sub-bass hit": snap at 0.2 s, B1 sub hit 0.3–0.7 s. The swoosh was barely there.
- **Recipe:**
  1. Music motif (3 s, trimmed to 2 s).
  2. Plus one SFX texture layered on the first note (crystal, snap, click).
  3. Plus the impact from the end of the plan.
  4. Make all three at the same key and seed, and **reuse the exact file in every ad.** A sonic logo only works if it repeats.
- The raw SFX logos came out at about −7 LUFS / 0 dBTP, so limit them.

## 7. Mixing levels (verified in `f_mix/frag_demo_mix.wav`)

| Stem | Normalise to (each stem first) | Notes |
|---|---|---|
| VO | −16 LUFS, TP −2 | Trim leading silence. Our TTS takes had none. |
| Music bed | −20 LUFS | Sidechain-duck under the VO: `sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350`. Aim for 10–15 dB of ducking under the voice, rising in the gaps. |
| Foley | −22 to −24 LUFS | Trim to onset. Layer low, mid and high. |
| Whoosh | Peak around −9 dBFS at the fastest frame | Per 08-post-production. |
| Ambience | About −24 dB | Never leave dead air. |
| Logo | −20 LUFS, then final limiter | — |
| **Master** | **−14 LUFS integrated, ≤ −1 dBTP** | Demo measured −14.6 LUFS / −1.0 dBTP / LRA 3.9. Platforms normalise around −14 to −13 (the TikTok/Reels target is about −13). [web, approximate] |

- **ffmpeg gotcha:** with `asplit` → `sidechaincompress` → `amix`, add `apad=whole_dur=` to the VO branch. Without it, the graph hung for 5 minutes. [E05]
- Normalise each stem in a separate pass, and run `loudnorm` on the master last.
- Web guidance used for the master target: https://openclip.app/learn/loudness-standard and https://sounddesign.irpr.agency/guides/what-is-lufs-loudness/

## 8. Gaps in `scripts/elevenlabs.py` and suggested additions
1. **`music`:**
   - Add `--model` (default `music_v2_5`), `--plan plan.json`, `--seed` and `--detailed`.
   - Drop `force_instrumental` when a plan is used, to avoid the 422.
   - Print or save the `Song-Id` header, needed for inpainting.
   - Add a `music-plan "PROMPT" --seconds` subcommand (`POST /v1/music/plan`) and save the plan JSON so it can be edited.
2. **`tts`:**
   - Add `--seed`, `--similarity`, `--language`, `--prev/--next` text, `--format pcm_48000` and `--dict` (pronunciation locators).
   - Accept `eleven_v4`, and warn that v4 ignores style and speed.
   - Log the `Character-Cost` header.
   - Add a `--takes N` option that varies the seed.
3. **`sfx`:**
   - Change the default influence to 0.3, matching the API.
   - Add `--takes N`, `--format` (WAV 48k) and `--model`.
   - **Auto-trim to the onset** (first frame above peak −20 dB) and `--normalize -22` LUFS. Onsets of 0–1.1 s and levels of −70 to −7 LUFS make this essential.
   - Update the docstring: SFX limit is 30 s.
4. **New subcommands:**
   - `voices --library` (`/v1/shared-voices` with use_cases, gender, sort).
   - `design "DESC" --text …` (previews to mp3, plus `--save ID`).
   - `dialogue script.json`.
   - `align audio.mp3 "TEXT"` (forced alignment to words.json for captions).
   - `stt-check file --ref TEXT` (scribe_v2 WER plus audio-event tags as automatic QA; port `research/ai-video-reels/lab/experiments/E05_elevenlabs/scripts/ana.py`).
   - `sts guide.wav --voice`.
5. **QA helper:** a `report` subcommand that prints duration, words/sec, LUFS, pauses and voiced ratio. These are the metrics used throughout this file.
6. **Retries:** we retry 429/5xx, which is good. Also surface the 422 `detail.message` text, which is human-readable (e.g. the force_instrumental error).

## 9. Production recipe (premium 9:16)
1. Write the VO at 1.6–1.9 wps. Mark pauses with `...` at the cut points, and use one CAPS word at most.
2. Shortlist three voices from §2 and generate on v4 and v3 with the same seed. Run the stt-check and audition.
3. Get word times from `with-timestamps` and snap captions and cuts to them.
4. Build a composition plan with chunks equal to the edit sections. Hard events go on chunk boundaries: 3 s silent intro, break, outro impact.
5. Create SFX per on-screen action (2–3 takes each), trim to onset, normalise, and layer low/mid/high.
6. Lay the sonic logo (fixed file) over the plan's outro impact.
7. Mix to the levels in §7. Master to −14 LUFS, −1 dBTP.
