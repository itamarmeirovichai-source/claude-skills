# ElevenLabs mastery: VO, music, SFX for premium 9:16 ads (verified 2026-10-07)

**Sources and method**
- Docs index: https://elevenlabs.io/docs/llms.txt
- **[E05]** = tested in our lab: `research/ai-video-reels/lab/experiments/E05_elevenlabs/` (`results.json` per subfolder, scripts in `scripts/`). `[inf]` = our inference.
- Judged by measurement, not by ear: duration, words/sec (wps), LUFS, pitch (f0), brightness (spectral centroid), silencedetect, plus scribe_v2 STT/audio-event checks. **Audition the mp3s before locking a voice.**

## 0. Six things that changed or surprised us
1. **Eleven v4 exists** (`eleven_v4`) and is ElevenLabs' recommended model.
   - It obeys tags far more: `[whispers]` gave a true whisper on v4 (voiced ratio 0.31, −26 LUFS) but only breathiness on v3 (0.53, −19 LUFS). [E05/b]
   - v4 has **no Style/Speed** (accepted, ignored); only Stability and Similarity. It reads inline IPA `"/ˈnwɑːr/"`.
   - https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4
2. **SFX now goes to 30 s** (not 22). `prompt_influence` defaults to **0.3** (ours: 0.4). https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
3. **Our `music` command silently uses `music_v1`** (API default, "outclassed" per the docs). Send `model_id: "music_v2_5"`. https://elevenlabs.io/docs/overview/models
4. **Composition plans are the only trustworthy timing.** Hard stops and impacts landed within ~50 ms of chunk boundaries; a timestamped prompt ignored the silent intro and the final hit. Plans reject `force_instrumental` (HTTP 422): put "instrumental" in styles and "vocals" in negatives. [E05/c]
5. **SFX loudness varies wildly** (−70 to −7 LUFS) and onsets drift 0–1.1 s. **Always trim to onset and normalise.** [E05/d]
6. **Shared Voice Library voices work directly by `voice_id`**; no add-to-library step on Creator tier. [E05/a]

## 1. Verified API parameters
**TTS** `POST /v1/text-to-speech/{voice_id}[/with-timestamps|/stream]`

| Field | Values / notes |
|---|---|
| `model_id` | `eleven_v4` (10k chars), `eleven_v3` (5k), `eleven_multilingual_v2` (stable long-form; SSML `<break>` ≤3 s), `eleven_flash_v2_5` (fast/cheap). **No `<break>` on v3/v4.** |
| `voice_settings` | `stability` 0–1 (0.5), `similarity_boost` (0.75), `style` (0, v2/v3), `use_speaker_boost`, `speed` 0.7–1.2 (v2/v3). v3 accepted stability 0.3 [E05]. |
| Continuity | `seed`; `previous_text`/`next_text`; `previous_request_ids`/`next_request_ids` (≤3) for VO split into lines. |
| Other | `language_code`, `apply_text_normalization` auto/on/off, `pronunciation_dictionary_locators` (≤3). |
| `output_format` | `mp3_44100_128` default; use **`pcm_48000`/`wav_44100` for mastering**. |
| Timestamps | Return `alignment` + `normalized_alignment`. On v4, tag characters such as `[softly]` are included (our `chars_to_words` strips them). [E05] |
| Cost | Read the `Character-Cost` header. Observed: v3 ≈0.45, v4 ≈0.13 credits/char. [E05] |

**SFX** `POST /v1/sound-generation`
- Fields: `text`, `duration_seconds` 0.5–30 (null = auto), `prompt_influence` 0–1, `loop` (v2 only), `model_id: eleven_text_to_sound_v2`.
- Output: MP3, or WAV 48 kHz for non-looping sounds.
- Docs bill 40 credits/s when a duration is set; observed usage was lower. https://elevenlabs.io/docs/overview/capabilities/sound-effects

**Music** `POST /v1/music`
- Returns audio plus a `Song-Id` header. Related endpoints: `/v1/music/detailed` (JSON + audio, `with_timestamps`), `/stream`, `/v1/music/plan` (prompt → editable plan).
- Fields: `model_id` music_v1 | v2 | v2_5; `music_length_ms` 3,000–600,000; **`prompt` XOR `composition_plan`**; `seed`; `force_instrumental` (prompt only); `store_for_inpainting`; `finetune_id`; `sign_with_c2pa`.
- v2 plan shape: `{"chunks":[{text, duration_ms 3,000–120,000, positive_styles ≤50, negative_styles ≤50, context_adherence low|medium|high}]}`.
  - At most 30 chunks; total 3 s–10 min.
  - The first chunk sets the genre: give it 6–7+ styles.
  - `text` = `[Section]`, lyric lines, `{inline cue}`, `(ooh)`.
- Also: inpainting (`source_from`), **video-to-music** (≤10 videos/600 s/200 MB + description and tags), stem separation.
- https://elevenlabs.io/docs/api-reference/music/compose · https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans

**Other endpoints**

| Endpoint | Key params | Use |
|---|---|---|
| `POST /v1/text-to-voice/design` | `voice_description`, `text` 100–1,000 chars, `model_id` `eleven_ttv_v3`/`eleven_multilingual_ttv_v2`, `guidance_scale` 5, `loudness` −1..1, `seed`, `reference_audio_base64` + `prompt_strength` (ttv_v3) | 3 previews; save one via `POST /v1/text-to-voice` (uses a slot). https://elevenlabs.io/docs/api-reference/text-to-voice/design |
| `POST /v1/text-to-dialogue[/with-timestamps]` | `inputs[{text, voice_id}]` (≤10 voices, ≤2,000 chars), `model_id` v3 (default)/v4, `settings`, `seed` | Multi-voice scenes. https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert |
| `POST /v1/forced-alignment` | multipart `file` + `text` → word/char times + `loss` | Captions for VO recorded elsewhere. |
| `POST /v1/speech-to-speech/{voice_id}` | multipart `audio`, `eleven_multilingual_sts_v2`, `remove_background_noise` | Re-voice our own timed guide read. |
| `GET /v1/shared-voices` | `search`, `use_cases`, `gender`, `age`, `accent`, `language`, `sort=usage_character_count_1y` | Voice casting. |
| `POST /v1/speech-to-text` | `model_id=scribe_v2`, `tag_audio_events=true` | Automatic QA (WER, event tags). |

## 2. Best voices per niche [E05/a]
Setup: eleven_v3, stability 0.5, seed 7, same line per niche. Every take had WER 0 (tech 0.08, only for US spelling "organized").

**Luxury fragrance** — *"Some things are never said... only remembered. Noir Vesper. The scent of after midnight."* (speed 0.9)

| # | Voice / ID | Evidence → why |
|---|---|---|
| 1 | **Jenna – Warm, Soft, Sultry** `qFjcP4hHD9WIdODvuJOJ` (F) | Darkest (centroid 1,602 Hz), 1.67 wps, f0 174 Hz. Intimate; tags move her strongly (§3). |
| 2 | **Frederick Surrey – Smooth, Velvety** `j9jfwdrw7BRfcR43Qohk` (M, UK) | f0 89 Hz, controlled 8-semitone range: "maison" baritone without melodrama. |
| 3 | **Edward – British, Dark, Seductive** `goT3UYdM9bhm0n2lmKQx` (M) | 96 Hz, theatrical 22.5 st range: bold noir/oud scents, too much for florals. |
| Custom | **Voice Design** ttv_v3: *"Native English. Female, early 40s. Studio-quality recording. Low, warm, slightly husky timbre with a soft breathy edge; slow, deliberate, intimate pacing… luxury perfume film."* | f0 142–150 Hz (~25 Hz lower than any library female we tried), 1.6–1.8 wps. IDs in `g_voice_design/design.json`. |

**Energetic beverage** — *"Crack it open. Feel the cold hit. VOLT. Zero sugar. All charge."* (speed 1.05)

| # | Voice / ID | Evidence → why |
|---|---|---|
| 1 | **Allison – Energetic, Clear, Bubbly** `xctasy8XvGp2cVO9HL9k` (F) | Loudest (−13.6 LUFS), 1.88 wps, f0 250 Hz: bright, cuts through a drop. |
| 2 | **Charlie** (premade) `IKne3meq5aSn9XLyUdCD` (M, AU) | Widest intonation (24.6 st): punchy; low centroid sits under synths. |
| 3 | **Christina – Energetic Commercial** `BuaKXS4Sv1Mccaw3flfU` (F) | Classic ad cadence, even 0.5–0.7 s pauses: safe client read. |

Avoid Liam (premade): fast but flat (8.5 st) and quiet; sounds like a creator, not a brand.

**Calm tech** — *"Your day, quietly organised. Halo listens, learns, and gets out of the way."*

| # | Voice / ID | Evidence → why |
|---|---|---|
| 1 | **Lucius – Calm, Reassuring** `HaUDdkOAoitiVjpiet1i` (M) | Warmest (1,198 Hz), 1.91 wps, very even (LRA 1.3): keynote calm [inf]. |
| 2 | **Hope – Natural, Clear and Calm** `OYTbf65OHHFELVut7v2H` (F) | Most even (LRA 1.2), 2.39 wps: conversational, modern. |
| 3 | **Emily E. – Premium Female Commercial** `CXoGcuszI2UkuF6sqV8W` (F, UK) | 1.91 wps, deliberate comma pause: polished. |

Fallbacks: River `SAz9YHcvj6GT2YYXdXww`, Miles `rNzVNTrvSffyxdrTbLKv`.

**Pacing rule:** premium VO runs **1.6–1.9 wps including pauses**. Budget ~10–12 words per 6 s and ~28–35 per 20 s. Fragrance VO should fill ≤50% of runtime.

## 3. v3/v4 tag cheat-sheet [E05/b]
Tagline *"Noir Vesper. The scent of after midnight."*, Jenna, seed 11. Plain v3 baseline: 3.44 s, −13.1 LUFS, voiced 0.74.

| Markup | Measured effect | Use |
|---|---|---|
| `...` | **+1.0–1.2 s pause each** (a period ≈0.6 s); 3.4 → 5.3 s | The most reliable timing lever. Put pauses on the cuts. |
| CAPS `AFTER` | +0.3 s, +0.5 st | Stress one word per line, no more. |
| `[whispers]` v3 | −5.7 dB, voiced 0.53, +600 Hz air | Breathy fragrance read. |
| `[whispers]` **v4** | −13 dB, voiced 0.31 (true whisper) | ASMR closes; make up the gain in the mix. |
| `[softly]` v3 | −2.5 dB, voiced 0.62, +0.5 s | **Default for luxury**: warm with body. |
| `[softly] ... [whispers] … MIDNIGHT` | v3: −2.8 dB, intelligible. v4: voiced 0.13 (nearly all whisper) | v3 for spoken→whispered arcs. On v4 use `[softly]` only. |
| `[breathy, intimate, slow]` | +1.1 s, −21 Hz | Free-form tags work; v4 docs favour explicit ones like `[low, gravelly voice]`. |
| Stability 0.0 vs 1.0 | Range 13.6 vs 7.0 st; pause 1.1 vs 0.6 s | 0 = emotive, 0.5 = default, 1.0 = exact legal/brand lines. |
| `[pause]` / `[exhales]` | `[pause]` = 1.6 s gap; `[exhales]` is rendered as an audible sigh | Breath before the brand name. |

- Other documented tags: `[laughs] [sighs] [excited] [curious] [sarcastic] [shouts] [clears throat] [strong X accent]`.
- Tags are natural language. Match them to the voice: a calm voice won't shout.
- Tags can be read as sound effects, so describe delivery explicitly. https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v4

**Which model:** v4 for real whispers, tag obedience, IPA brand names and lower cost. v3 when you need `speed`/`style`, or if a voice sounds better there; v4 changes timbre, so A/B both.

**Pronunciation:** v4 inline IPA `"/vɛsˈpɛr/"`; v2 `<phoneme>` (flash_v2), `.pls` alias dictionaries or respellings. Spell out prices ("forty-nine dollars").

## 4. Music: plan templates [E05/c]
**Measured on music_v2_5 plans** (`plan_v25_beverage_22s`, `plan_v25_bev2`)
- A first chunk of "near silence / single hum" rendered **digital silence (−138 dB) for 3 s**: an SFX-only opening for free.
- `[Break]` with "hard stop, total silence" and negatives drums/bass/melody: stop at **15.05 s for a 15.0 s boundary**.
- `[Outro]` at adherence **low** with "one massive cinematic impact on the downbeat, loud": **hit at exactly 18.00 s**, +70 dB.
- **What failed:**
  - "Breath + resolve" without a loud cue just faded out, with no hit.
  - Drops placed *inside* a chunk drifted (1.5 s late once; another peaked 4 s in). **Put hard events on boundaries** and double them with an SFX hit.
- The prompt-only version ("0:00–0:03 near silence…") had music from 0.25 s, no final hit, and a stop 0.5 s late.
- **Minimum chunk is 3 s**: a 6 s cutdown is at most 2 chunks, and a 1.5 s breath must be cut in the edit.
- Plans come out hot (−9.8 LUFS, LRA 23). Normalise the bed to −20 LUFS.

**A. Fragrance 20 s** (verified: piano enters 1.5 s, swell, peak ~13 s, decay). JSON: `c_music/plan_v25_frag.request.json`
- `[Intro]\n{room tone}` 3000: luxury fragrance commercial, cinematic neo-classical, 72 BPM, D minor, instrumental, felt piano single notes, close-mic'd, tape warmth, very sparse / *vocals, drums, EDM*.
- `[Swell]` 8000: low cello drone enters, slow string swell, breathy pads / *percussion*.
- `[Peak]` 5000: full lush strings, deep low pulse, wide cinematic reverb / *EDM drop, trap drums*.
- `[Resolve]\n{final chord}` 4000 (medium): sustained piano and string chord, D major resolution, long natural decay / *new melody, abrupt cut*.

**B. Beverage 22 s** (verified boundaries 3.5 / 15.05 / 18.00 s). JSON: `c_music/plan_v25_bev2.request.json`
- `[Intro]\n{near silence}` 3000: minimal electronic, premium energy drink commercial, 124 BPM, F minor, instrumental, single sub-bass hum only, very quiet / *vocals, drums, melody, loud*.
- `[Build]\n{filtered kick}\n{riser}\n{drop gap}` 6000: low-pass filtered kick, white-noise riser, ends with a half-beat of silence / *full drop*.
- `[Drop]\n{drop hits on the first beat}` 6000: punchy kick and clap, distorted synth stabs, maximum energy / *intro, build-up, fade in*.
- `[Break]\n{silence}` 3000 (low): hard stop, total silence, tape stop / *drums, bass, melody*.
- `[Outro]\n{one huge impact}\n{chord rings out}` 4000 (low): one massive cinematic impact on the downbeat, loud, F minor stab chord, long reverb tail / *silence, fade in, quiet*.

**C. Calm tech 20 s** [inf, not generated]
- `[Intro]` 3 s: minimal ambient electronica, 96 BPM, E major, soft glassy pluck arpeggio, warm analog pad.
- `[Groove]` 9 s: light sidechained pulse, soft rimshot, rounded sub.
- `[Lift]` 5 s: pad opens, arpeggio up an octave.
- `[Outro]` 3 s (low): E major chord rings out, single glass mallet note.

**6 s cutdown:** `[Hook/impact]` 3 s + `[Logo/ring-out]` 3 s, or cut the 20 s plan at its boundaries.

**Prompt craft:**
- Decide genre, mood, instruments, BPM/key and era, or the model picks "the most average" option.
- Studio words move real levers: *sidechained, close-mic'd, bone-dry, tape saturation, plate reverb*.
- Narrate the arrangement ("start with just…, then bring in…") and mark the silences.
- Styles must be in English. Artist names → `bad_composition_plan`. https://elevenlabs.io/docs/overview/capabilities/music/best-practices

## 5. SFX prompt library [E05/d]
Each sound was run as plain @0.3, "pro" @0.3 and pro @0.8, with scribe_v2 event tags as a blind check. Pro prefix: `"Close-mic'd studio foley, dry, no music: "`.

| Sound | Winner | Failure seen |
|---|---|---|
| Glass cap | plain `"glass perfume bottle cap"` @0.3 ("bottle opening"); clink at 1.1 s, so trim | "heavy faceted glass stopper…" → near-silent @0.3, a thud @0.8 ("heavy" = thud) |
| Spray | pro `"…one short perfume atomizer spray, soft pump click then a fine pressurized mist hiss"` @0.8 | plain read as typing |
| Can crack | plain `"soda can opening"` @0.3; pro @0.8 adds 1 s of fizz | — |
| Pour | any wording; pro `"…sparkling soda poured into a tall glass over ice, liquid glug and rising fizzing bubbles"` @0.3 is longest | — |
| Ice | pro `"…three ice cubes dropped one by one into an empty crystal tumbler, bright clinks…"` **@0.8** | same @0.3 = "shattering glass" |
| Fabric | pro `"…a single slow sweep of heavy silk satin, soft airy swish"` @0.3 | all takes quiet (−35 to −41 LUFS) |
| Click | pro `"…one premium tactile click of a small machined aluminium button, ultra short and crisp"` @0.3 (90 ms) | plain "button click" silent (−70 LUFS) |
| Whoosh | plain `"whoosh"` + a separate sub layer | "whoosh with deep low-end swell" = a 180 Hz boom, not air |

**Rules**
- One action + one object + one material.
- Influence 0.8 for ambiguous nouns (ice, glass); 0.3 for textures.
- Always set duration. Make 2–3 takes (results swing ±30 dB).
- Sequence with "…, then…" and layer in the edit rather than one combined prompt.
- Vocabulary: impact, whoosh, braam, drone, glitch; musical stabs work ("brass stabs in F minor"). https://elevenlabs.io/docs/help-center/product/core-capabilities/sound-effects/how-do-i-prompt-for-sound-effects

## 6. Sonic logo (2 s) [E05/e]
- **SFX cannot play exact notes.** "E–G#–B marimba" came back as a glide from D#4 to C5.
- **Music can.** `music_v2_5`, 3 s (the minimum), *"three-note ascending glass marimba motif E, G sharp, B, then a soft warm synth pad chord in E major rings out… instrumental, no drums"* → E4→G#4→E5 in key, −40 dB by 1.9 s. Trim to 2.0 s with a 0.3 s fade.
- SFX for textures:
  - "one crystal glass chime struck once…" @0.6 → clean A6 ring, gone by 1.1 s.
  - "can-tab snap → swoosh → punchy sub-bass hit" → snap 0.2 s, B1 hit 0.3–0.7 s (swoosh barely there).
- **Recipe:** music motif + one SFX texture on the first note + the plan's outro impact, all in one key. **Reuse the exact file in every ad.**
- Raw SFX logos came out at −7 LUFS / 0 dBTP, so limit them.

## 7. Mixing levels (verified: `f_mix/frag_demo_mix.wav`)

| Stem | Normalise each to | Notes |
|---|---|---|
| VO | −16 LUFS, TP −2 | — |
| Music bed | −20 LUFS | Duck under VO: `sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350`; 10–15 dB of ducking. |
| Foley | −22 to −24 LUFS | Trim to onset; layer low/mid/high. |
| Whoosh / ambience | peak ≈ −9 dBFS / ≈ −24 dB | per 08-post-production |
| Logo | −20 LUFS | then the master limiter |
| **Master** | **−14 LUFS, ≤ −1 dBTP** | Demo: −14.6 LUFS, −1.0 dBTP, LRA 3.9. Reels/TikTok normalise around −14 to −13 [web, approx.] |

- **ffmpeg gotcha:** `asplit` → `sidechaincompress` → `amix` hung for 5 minutes until we added `apad=whole_dur=` on the VO branch. [E05]
- Normalise stems in separate passes; run `loudnorm` on the master last.
- Web guidance: https://openclip.app/learn/loudness-standard · https://sounddesign.irpr.agency/guides/what-is-lufs-loudness/

## 8. Gaps in `scripts/elevenlabs.py`
1. **music:** add `--model` (default `music_v2_5`), `--plan plan.json` (omit `force_instrumental`), `--seed`, `--detailed`. Save the `Song-Id`. New `music-plan "PROMPT"` command (`/v1/music/plan`).
2. **tts:** add `--seed`, `--similarity`, `--language`, `--prev/--next`, `--format pcm_48000`, `--dict`, `--takes N`. Accept `eleven_v4` (warn that style/speed are ignored). Log `Character-Cost`.
3. **sfx:** default influence 0.3; add `--takes`, `--format wav`, and **auto onset-trim + `--normalize -22`**. Update the docstring to 30 s.
4. **New commands:**
   - `voices --library` (shared-voices).
   - `design` (Voice Design previews + `--save`).
   - `dialogue script.json`.
   - `align` (forced alignment → words.json).
   - `sts`.
   - `stt-check --ref` (WER + event tags; port `E05_elevenlabs/scripts/ana.py`).
   - `report` (duration, wps, LUFS, pauses, voiced ratio).
5. **Errors:** surface the 422 `detail.message` (it is human-readable).

## 9. Production recipe
1. Write the VO at 1.6–1.9 wps, with `...` at cut points and at most one CAPS word.
2. Shortlist 3 voices (§2). Generate on v4 and v3 with one seed, then stt-check and audition.
3. Snap captions and cuts to the `with-timestamps` word times.
4. Build the composition plan with chunks = edit sections, and hard events on boundaries.
5. Make SFX per on-screen action (2–3 takes), trim, normalise, and layer.
6. Lay the fixed sonic-logo file over the outro impact.
7. Mix per §7 and master to −14 LUFS / −1 dBTP.
