# 42 — Viral AI reel teardowns: why the good ones look real

Researched 2026-10-09. This doc is the evidence behind 41 (action realism checklist) and adds to 22 (ad teardowns) and 37 (action execution); it does not repeat them. No generation API was used.

Labels:
- **[m]** measured by me from the file (ffmpeg cuts, 2 fps frame strips, audio analysis).
- **[c]** the creator's or platform's own claim (caption, description, prompt doc).
- **[inf]** my inference.

## Method and limits

- **26 videos measured end to end** (10 owner reels from Instagram + 16 TikToks), plus **5 more from metadata, subtitles and storyboards** (YouTube; video bytes are bot-blocked from this server, HTTP 403/429).
- For each video:
  - **Cuts:** `select='gt(scene,0.3)',showinfo`. Letterboxed TikToks were re-run on the cropped picture (`cropdetect`), and dark trailers were re-run at threshold 0.12 with cuts under 0.4 s merged. Without the crop, a 2.39:1 trailer inside a 9:16 frame reads as "0 cuts" (Zelda, Red Rising). Without the low threshold, night scenes are under-counted by 2–3×.
  - **Frames:** 2 fps tiles, 8×4, with timestamps. All were read by eye.
  - **Audio:** an RMS envelope; a spectral-flux beat-regularity score (autocorrelation from 0.3 to 1 s; **> 0.5 means a steady music bed**, **< 0.15 means dialogue or narration with no steady beat**); and a band split (< 200 Hz for engines and impacts).
  - **Not usable:** "cuts landing on an audio onset" came out at chance level for every video because onset density was too high, so it is not used.
- **Engagement:** taken from captions (Instagram) and TikTok API counts on 2026-10-09. Brand accounts (Dreamina, Higgsfield) are paid-boosted, so their play counts are not organic. Recent posts (under 10 days old) have not matured.
- Videos and images were kept in the scratchpad only and are not committed.

---

## 1. Per-video teardown table

Columns:
- **Len / shots / ASL:** length, shot count, average shot length.
- **Hook (0–1 s):** what is on screen in the first second.
- **Turn / punchline:** when it lands.
- **Camera (real rig?):** the dominant camera moves, and whether a real crew could rig them.
- **Realism / hiding:** what sells it as real, and how AI weak spots are hidden.
- **Sound:** music bed (M), dialogue (D), native SFX (S), narration (N), with the beat score.
- **Text / CTA:** overlays and call to action.
- **Stats:** engagement where visible.

### A. Car and action (the owner's reference class)

| # | Video | Len / shots / ASL | Hook (0–1 s) | Turn / punchline | Camera (real rig?) | Realism / hiding | Sound | Text / CTA | Stats |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **"Dubai"**, @edbert_yienson, Seedance 2.5 1080p on Higgsfield [IG](https://www.instagram.com/edbert_yienson/reel/DcDrXjXsLcU/) | 30.1 s / **9** / 3.3 s, but **2.1 s after the opener** [m]. Cuts at 13.07, 15.8, 17.67, 19.43, 21.53, 24.2, 26.0, 28.6 | Straight down from the Burj Khalifa spire, **already moving** | 13 s: the car overtakes the camera (the first cut). 29 s: locked-off end, the car drives away into the horizon | **Shot 1 (0–13 s): one FPV-drone dive** from the spire to road level, then it pulls alongside the car. A real FPV pilot can fly this. Shots 2–9: side tracking (chase car), rear-view mirror, nose-on (camera car ahead), cockpit 3/4 through the window, rear-bumper 3/4, wheel hands, side pass, locked-off wide. **All rig-able** | **The man never falls.** Only the camera dives. The caption says "I filmed myself from top of skyscrapers down to the road"; the edit implies it, the pixels never show it [m]. Motion blur on every pass. The car is the same yellow Huracán in every shot. The picture fills only the top ~45% of the frame (the prompt panel covers the rest), so artifacts are tiny [m] | M + S. Beat score 0.50. The < 200 Hz band rises ~10 dB when the car enters (8 s) and peaks on the pass-bys at 12.5 s and 23.5 s: **engine layered under the music** [m] | "STEAL MY PROMPT / COMMENT 'DUBAI'", the **input passport photo** and the **scrolling timecoded prompt** on screen for all 30 s | 19K likes, **24K comments** (more comments than likes: the comment-for-prompt CTA works) [c] |
| 2 | **"ICE"** (figure skating), @edbert_yienson, Seedance 2 [TikTok](https://www.tiktok.com/@edbert_yienson/video/7691556396361370901) | 14.1 s / 4 / 3.5 s [m]. Cuts at 5.2, 6.9, 9.7 | Ultra-low tracking on the skate blade, already at speed | 8–10 s: the quad jump. **The prompt cuts to a facial close-up in slow motion mid-rotation**, so the hard part (the rotation) is never shown wide [m]. 14 s: a small smile, "Yes" | Parallel low track → overhead follow → orbit → low quarter-front → face CU. Steadicam/cable-cam grammar, all rig-able | The prompt writes the **physics per second** (knee compression → toe-pick → horizontal-to-vertical force) and a **"Forbidden visuals" list**: no anime physics, no floating or hang time, no static clothing [c]. Cold, desaturated documentary grade | S, from the prompt: "blade cuts: deep ice carving / toe pick: sharp crack / airborne: brief silence / landing: heavy impact / soft exhale + quiet 'Yes'" [c] | Same "STEAL MY PROMPT" template plus the input photo. Prompt in a public Google Doc ([doc](https://docs.google.com/document/d/13Pn7yozU3FCd66cB_v5t-J-hK3mhSaveIemB32tSJ_g/edit)) | 176 plays (7 days old) |
| 3 | **"Time Freeze — Paris"**, @edbert_yienson, Seedance 2 [TikTok](https://www.tiktok.com/@edbert_yienson/video/7691957404908424469) | 15.1 s / **1** (one take) [m] | Wide busy Paris street, the hero walking toward the lens | 3 s: the finger snap freezes the world. 11–15 s: he eats the croissant, snaps again, everything resumes | **One handheld/gimbal walk-and-talk.** Rig-able | **The physics are suspended by the story.** Frozen people and pigeons cannot break physics, so the one-take is safe. Only one moving actor [inf] | S. The prompt's **"Sound Flow"**: city ambience → snap → deep shockwave → silence → footsteps + soft pigeon → second snap → reverse wave → ambience returns [c] | Same template. Public prompt doc ([doc](https://docs.google.com/document/d/1j4ro3lBIlXDok8UJ4K3tbPMvFX4YHF0pFQuHBihuaXY/edit)) | 375 plays (7 days old) |
| 4 | **Dreamina Seedance 2.5 global launch film** (official) [TikTok](https://www.tiktok.com/@dreamina_ai/video/7668553891792964894) | 160 s / **71** / **2.25 s** [m] | A tight elevator-button insert, then a scared face. Panic in under 1 s | 3 s: she presses the button and falls out of the elevator into the sky, then into a wheat field. Each world change is cut on her motion | **Chase coverage:** pursuers walking toward camera in a backlit wide; her hiding in the hay (low CU); hand inserts; feet and boots at ground level; a following track; a saloon interior; a hand on a door. All rig-able | **Running is shown in pieces** (feet, back, shoulder, face), never as one long full-body run. Hard backlight and dust hide faces. The 30 s native-generation timeline is shown on screen [m] | M + S + D. Beat score 0.32 | Feature callouts ("30-Second Native Output", "Long-Form Video") | 13.6M plays, 50K likes: **0.37%, paid** |
| 5 | **Porsche 911 drift, Tokyo**, @baran_robin [TikTok](https://www.tiktok.com/@baran_robin/video/7606479051171056918) | 10 s / 3 / 3.3 s [m] | Nose-on at speed down a wet neon street, camera car in front | 4 s: a drift at the Shibuya crossing | Camera car ahead → high wide → rear CU, then the car pulls away into smoke. Rig-able | **Tyre smoke and rain hide the wheel–road contact.** Wet reflections | M (0.22) | none | 1.4K plays: pretty, but no person and no idea [inf] |
| 6 | **Ferrari vs white horse**, @baran_robin [TikTok](https://www.tiktok.com/@baran_robin/video/7606710717756083458) | 15 s / ~8 / ~1.9 s [m, counted by eye] | An ECU of the horse's head beside the car's nose on the grid | 14 s: a sunset silhouette | Grid wide → tracking side → wheel insert → helmet CU → rear chase → side track | The horse's gallop is never held for more than 2 s. Motion blur | M (0.33) | none | 1.4K plays |
| 7 | **Hollywood car chase**, Baran Robin (Higgsfield Genjutsu motion transfer + Seedance Edit) [YouTube](https://youtu.be/6kcagvbfEBQ) | 67 s [c]. Chapters: getaway, motorbike, double-decker bus stunt, roadblock and explosion | n/a (storyboard blocked) | n/a | **The camera and stunt choreography were transferred from real chase footage** [c] | **The motion is real; only the faces and vehicles are AI** [c] | n/a | n/a | 861 views |

### B. Character comedy and action comedy

| # | Video | Len / shots / ASL | Hook (0–1 s) | Turn / punchline | Camera (real rig?) | Realism / hiding | Sound | Text / CTA | Stats |
|---|---|---|---|---|---|---|---|---|---|
| 8 | **"If Bible characters were influencers"**, PJ Accetturo (Veo 3) [TikTok](https://www.tiktok.com/@pjacefilms/video/7511268853129809183) | 64 s / **7** / **9.2 s** [m] | Jesus on the cross, smiling into a selfie camera, talking | One punchline per character (Samson, David with Goliath walking in behind at 14 s, Moses …) | **Selfie arm, handheld.** One take per character | **The selfie phone is the camera**, so the wide-lens distortion, the shake and the eye contact are all expected. Dialogue carries it; there are no physics stunts [inf] | **D only** (beat 0.03, 15% near-silence between lines) | One persistent top caption: "If Bible characters were influencers 😂" + "(Prompts in description)" | **4.8M plays, 463K likes (9.6%)** |
| 9 | **Kalshi "NBA Finals"** TV spot, PJ Accetturo (Veo 3) [TikTok](https://www.tiktok.com/@pjacefilms/video/7515324663946317087) | 30 s / 13 / **2.3 s** [m] | A shirtless old man in a flag cape, frog-marched by police past a reporter, mid-action | Every shot is its own punchline. The ticker pays off the bet | Vox-pop TV news: locked or handheld medium-wide, with the reporter's mic in frame | **News grammar excuses the flat light and the direct address.** No stunts | D (0.10) | Persistent caption "I can't believe they aired our AI commercial during the NBA Finals" | 12K plays on TikTok; 1.14M on X (22) [c]. **300–400 generations for 15 usable clips** [c] ([eWeek](https://www.eweek.com/fr/news/ai-ad-kalshi-nba-finals/)) |
| 10 | **Lindy AI "most unhinged ad"**, PJ Accetturo (Midjourney, Kling, Veo 3) [TikTok](https://www.tiktok.com/@pjacefilms/video/7538130214031756575) | 43 s / ~24 / ~1.8 s [m] | 0.5 s: **a man bursts out through an office window**, filmed from outside | 4.5 s: the same man in a skydiving harness POV with a skyscraper far below. Then a water-gun street fight, a TV news anchor, the product UI | Locked exterior, office wide, a POV harness cam, a street tele. All rig-able | **The glass breaks around the actor, not around the camera.** The parachute shot shows **altitude** (the tower far below), so the canopy height is believable. Each stunt lasts about 1 s and is cut on impact [m] | D + M (0.19) | Persistent caption "This is the most unhinged AI ad you'll ever see" | 6.7K plays |
| 11 | **"Epic Baby Battles"**, @techhalla (2025) [TikTok](https://www.tiktok.com/@techhalla/video/7459484974446546209) | 60 s / 10 / **6.0 s** [m] | A baby facing a beaver at a riverbank, in a locked wide | None. Each fight just loops | **Locked wide only; no coverage** | **The fake benchmark:** weightless kicks, no impact frames, no inserts, no reaction shots | M (0.54). No impact SFX | Watermark only | 26.5K plays, **145 likes (0.5%)** |

### C. Long-form trailers and films (to calibrate pacing)

| # | Video | Len / shots / ASL | Hook (0–1 s) | Turn / punchline | Camera (real rig?) | Realism / hiding | Sound | Text / CTA | Stats |
|---|---|---|---|---|---|---|---|---|---|
| 12 | **"Nexus" teaser**, PJ Accetturo (Dreamina Octo + Seedance 2.0) [TikTok](https://www.tiktok.com/@pjacefilms/video/7648687477523320094) | 318 s; **first 60 s: 44 cuts, ~1.4 s** [m] | An ECU of a caged baby creature's face | 4.5 s: a cleaver against the sky (the threat) | Market handheld, ECU inserts (hand on the creature), low wides | Creature and hand-texture inserts, so faces are only on dialogue. Dust and haze | D + M + S (0.20) | Top caption "Insane teaser for my upcoming feature film 'Nexus'" | **2.9M plays, 169K likes, 37K shares** |
| 13 | **Red Rising fan teaser**, PJ Accetturo (Seedance 2.0) [TikTok](https://www.tiktok.com/@pjacefilms/video/7613909444975414558) | 161 s; first 60 s: 46 cuts, **~1.3 s** [m] | A screaming pilot in a cockpit, then a white flash | 2.5 s: the title over the ship's hull | Cockpit, space wides, armour CUs, corridor | **Low key and red practicals throughout.** Flashes are used as cut points | M + S (0.21) | Top caption "Viral Red Rising fan trailer:" | 193K plays, 16K likes, 6.3K shares |
| 14 | **R-rated Zelda trailer**, PJ Accetturo (Freepik, $300, 5 days [c]) [TikTok](https://www.tiktok.com/@pjacefilms/video/7592306442124725534) | 114 s; first 60 s: 37 cuts, ~1.6 s [m] | Fire and a laser blast in a burning village | 11.5 s: a hard cut to the quiet snow romance | Night fire chaos, then daylight snow | **Fire, smoke and silhouettes.** Monsters only in backlight | M + S (0.25) | Top caption "This R-Rated Legend of Zelda trailer is going viral" | 80K plays on TikTok; 9M on X [c] |
| 15 | **"Camelot" horror**, PJ Accetturo (Pippit) [TikTok](https://www.tiktok.com/@pjacefilms/video/7691530537265007902) | 145 s; first 60 s: 48 cuts, ~1.25 s [m] | A burning title card | A jump scare at the end, promised in the caption | Period wides, close-ups | Candlelight low key | M + S | "Wait for the jump scare 😱" | 167 plays (new, sponsored) |
| 16 | **ANERNEQ** (Higgsfield Originals, 20 min Arctic drama) [IG](https://www.instagram.com/higgsfield.ai/reel/Dd1xCWei0CF/) | 1,200 s; median shot ~4.9 s (threshold 0.18, which under-counts in snow at night) [m] | A cold-open montage: 7 shots in 7 s (fire, aurora, sled, faces), then slow | n/a | "Natural handheld camera movement" [c] | Firelight, snow texture, night | M + D + S | Comment "UNLOCK" for prompts; all prompts open-sourced [c] | 4.6K likes, 2.9K comments |
| 17 | **"Never Forget Your Beginnings"**, Hashem Al-Ghaili [TikTok](https://www.tiktok.com/@hashem.alghaili/video/7687669486974946582) | 168 s / 89 / **1.9 s** [m] | A wide of a boy working in a terraced field | A village-to-success arc | Field wides, ECU hands, a drone over the village | **Documentary coverage:** wide → medium → ECU hand → face, repeated. Real-looking available light | N + M (0.09) | Bilingual subtitles | 53.6K plays, 3.7K likes |
| 18 | **Maglev 0–800 km/h** (Hashem; **real footage, the control**) [TikTok](https://www.tiktok.com/@hashem.alghaili/video/7686043543953018134) | 112 s / 56 / 2.0 s [m] | A sled shooting down the track | n/a | Track-level POV, rail cam, control room | **This is what real high-speed footage looks like:** compression from long lenses, streaking rails, unglamorous light | N (0.04) | "Could You Survive Going 0 to 800 km/h in 5 Seconds?" | 4.9K plays |

### D. Hybrid (real performance, AI world): the owner's other reels

| # | Video | Len / shots / ASL | Hook (0–1 s) | Turn / punchline | Camera (real rig?) | Realism / hiding | Sound | Text / CTA | Stats |
|---|---|---|---|---|---|---|---|---|---|
| 19 | **"Infinite Camera Angles"**, @rourke (Lovart + Seedance 2.5) [IG](https://www.instagram.com/rourke/reel/DclqVvdqvZw/) | 60 s. Demo 0–24.5 s: **~14 AI angles cut from one real take (~1.7 s each)**, then a tutorial [m] | A split screen: AI angle on top, the original below | 24.5 s: "here's how" | Re-angled to close-up, overhead, through-a-window POV, low hero, macro of the knife on a lemon | **The performance and timing are real**; only the camera is invented | **D, the original location sound** (0.07) | Comment "AI" | **72K likes**, 8.6K comments |
| 20 | **Genjutsu + Seedance**, @sidequestpat_ [IG](https://www.instagram.com/sidequestpat_/reel/Dd6gkuVR7jS/) | 29.3 s / 12 / 2.4 s [m] | A wipe from a plain white room to a sea-view penthouse | 7 s: a wide reveals the tripod and phone ("one camera") | Re-angles of one locked phone take | The real performance carries it | D (0.14) | Comment "ANGLE" | 3.2K likes, 3.1K comments |
| 21 | **Genjutsu "AI Production" (train)**, Higgsfield [IG](https://www.instagram.com/higgsfield.ai/reel/DdwEiL4KzVS/) | 59 s / **1 continuous take** shown twice (studio below, AI train above) [m] | "You're not ready for what's next" over a subway car | 3.5 s: "Except it wasn't" | One handheld take in a studio | The real actor's motion and the real camera shake | D (0.07) | Comment "Jutsu" | 11K likes, 4.2K comments |
| 22 | **Rolls-Royce vs cheap car**, @maorhani1 [IG](https://www.instagram.com/maorhani1/reel/DdyIfcjSm3P/) | 40.7 s / 4 / 10 s [m] | Top: a luxury hotel lobby. Bottom: the same walk in a parking garage | 18.7 s: the in-car talk | **Real phone handheld**, restyled | The phone shake and the timing are real | D in Hebrew (0.36) | Comment "רולס" | 144 likes, 242 comments |
| 23 | **"Hybrid Production"**, Higgsfield [IG](https://www.instagram.com/higgsfield.ai/reel/Ddjk5fCq1VK/) | 41 s / ~14 / ~2.9 s [m] | A green-screen rider on a kiddie spring bike becomes a desert hover-bike | Before/after wipes | A showreel | Real plates | M (0.59) | Comment "JUTSU" | 8.7K likes |
| 24 | **Seedance 2.5 API cashback**, Higgsfield [IG](https://www.instagram.com/higgsfield.ai/reel/Ddwky9yq-Jt/) | 22.5 s / 7 / 3.2 s [m] | A worm's-eye view of boots and a jackhammer | 8 s: "100% CASHBACK" | Motion graphics | n/a | M (**0.72**) | Comment "API" | 4K likes |
| 25 | **AI Influencer**, Higgsfield × ChatGPT [IG](https://www.instagram.com/higgsfield.ai/reel/DeHZl65CI2G/) | 49.5 s / 13 / 3.8 s [m] | A crowd crush at a party with a flailing blond guy | The UI demo | Handheld party | n/a | M (0.53) | Comment "VIRAL" | 7.9K likes |
| 26 | **Film Festival $1M**, Higgsfield [IG](https://www.instagram.com/higgsfield.ai/reel/DdmkVEgKLE4/) | 74 s / 22 / 3.4 s [m] | An MGM-style lion logo with a child in place of the lion | A counter showing 67,223 entries | Studio | n/a | M + D | Comment "FESTIVAL" | 9.7K likes |

### E. Metadata only (from the description or subtitles; no frames)

- **Kalshi "YOLO"**, PJ Accetturo and Theo Dudley ([YouTube](https://youtu.be/mzXFURkcCt4), 68K views). About 22 shots at ~1.7 s each (storyboard count in 22). Historical "underdog" vignettes, script first, with alternate lines pitched by writers [c].
- **IM8 "Red or Green"** ([YouTube](https://youtu.be/ER5P_wH0E9Q)). The creator claims 120–233M views. **No on-camera speaking lines, "which made it easier to avoid the AI look"**; the VO was voice-cloned [c] ([newsletter](https://pjace.beehiiv.com/p/120m-views-in-two-days-how-we-made-our-new-viral-ai-ad-for-david-beckham-s-company-im8)).
- **"1 Minute One Take Scene"**, JSFILMZ ([YouTube](https://youtu.be/cyDnYXW1yhw), 5.5K views). **Connected 15 s prompt sections** make one 1-minute oner. It is a **dialogue interrogation**: low motion, two people [c].
- **Nike "It has no name"**, Wide Silvente ([YouTube](https://youtu.be/RFGfkOLGsEM), 256K views). About 35 shots at ~1.0 s, a training montage (22).
- **"TOKYO PURSUIT — A One-Take AI Parkour Film"** ([YouTube](https://youtu.be/2ugOqF4tORg)): **109 views**. A one-take action chase is not what audiences reward [m: view count only].

---

## 2. Cross-video rules, ranked by impact

Ranked by how often the rule separates the high-engagement reels from the low ones in this corpus, and how directly it fixes VXO's failures.

1. **Cut action into coverage. Use one take only when nothing in the shot can break physics.**
   - Every action or chase reel with real reach cuts every **1.3–2.3 s** [m]: Dubai after its opener, Kalshi, Lindy, Dreamina, Nexus, Red Rising, Zelda.
   - The one-takes in the corpus are a walk with frozen physics (time-stop), a selfie monologue (Bible), a dialogue scene (JSFILMZ) and a studio walk-and-talk (Genjutsu).
   - The one-take action pieces are low-view (Tokyo Pursuit 109 views) or are not action at all.
   - The Dubai "dive" is a **camera** move by an FPV drone. **No person falls.**

2. **Every camera position must be one a crew could rig.**
   - Across 26 videos, **no shot** puts the camera through glass, inside a falling body, or in a place no rig fits [m].
   - Dubai, the closest thing to "impossible", is all FPV drone, chase car, camera car ahead, mirror cam, door mount and locked tripod.
   - Lindy breaks a window **around the actor while the camera stays outside**.

3. **Write the shot list with timecodes inside one prompt. The model obeys it to about ±1 s.**
   - The Dubai on-screen prompt is a 9-line timecoded list (0:00–0:12 aerial dive, 0:12–0:15 side view …, 0:29–0:30 static locked-off). The cuts land at 13.07, 15.8 … 28.6 s [m].
   - ICE's per-second storyboard puts its cuts at 5.2 and 9.7 s, matching "4–5 s camera drops to orbit" and "9–10 s cut to facial close-up" [m].
   - [inf] The 9-shot Dubai reel is probably **one 30 s Seedance 2.5 generation**, not 9 clips spliced together. The prompt is one continuous 30 s list, and Seedance 2.5 does 30 s natively [c, [Dreamina](https://www.tiktok.com/@dreamina_ai/video/7668553891792964894)].

4. **Cut away at the moment AI can't do.**
   - ICE cuts to a slow-motion face close-up **mid-quad** [m].
   - Dreamina shows the run as feet, back and hands, never a long full-body sprint [m].
   - Ferrari vs horse never holds the gallop for more than 2 s [m].
   - Lindy holds each stunt for about 1 s and cuts on impact [m].

5. **Give the camera a reason to exist: selfie, news, documentary, FPV.**
   - The top organic hit (Bible, 4.8M plays) has an ASL of 9 s because **the selfie phone is part of the story**. Distortion, shake and eye contact are expected.
   - Kalshi borrows TV vox-pop grammar, which excuses flat light.
   - Hashem uses documentary coverage (wide → medium → hand ECU → face).
   - [inf] A diegetic camera turns AI tells into genre conventions.

6. **Put the physics and the forbidden list in the prompt, as numbers and verbs.**
   - ICE: "Toe pick plants → rapid knee extension → horizontal-to-vertical force", "Forbidden visuals: no exaggerated anime physics, no unrealistic floating or hang time, no static clothing" [c].
   - Time-stop: "No missing people or objects. Consistent physics" [c].

7. **Script the sound with the picture.**
   - The best prompts carry a sound track: time-stop's "Sound Flow", and ICE's "airborne: brief silence / landing: heavy impact" [c].
   - In Dubai the engine band swells exactly on the car passes, under a steady music bed [m].
   - The low-engagement Baby Battles has music only and no impact SFX [m].
   - **Silence just before the hit** appears in both edbert prompts.

8. **Real motion beats generated motion: hybrid wins when you can shoot.**
   - The 72K-like Rourke reel, Genjutsu, sidequestpat and maorhani all keep a **real performance and real camera shake**, and let AI change only the angle or the world [m].
   - Baran Robin's chase transfers the choreography from real chase footage [c].

9. **The hook is motion already in progress, plus a persistent one-line caption.**
   - Frame 0 is never static in the hits: the spire dive, the blade at speed, the man through the window, the scream in the cockpit.
   - PJ keeps one caption on screen for the whole video ("Wait for the jump scare 😱"), which promises a payoff [m].

10. **The CTA drives comments: "Comment X for the prompt".**
    - Dubai has **24K comments vs 19K likes** [c].
    - sidequestpat (3.1K comments vs 3.2K likes) and maorhani (242 comments vs 144 likes) show the same.
    - Showing the **input photo + prompt** on screen proves "this is AI from one selfie", which is the real hook for the AI-creator audience [inf].

11. **Spectacle without a person or a joke does not travel.**
    - Porsche drift (1.4K plays), Ferrari vs horse (1.4K) and Baby Battles (0.5% like rate) are technically fine but have no character, stakes or punchline [m].
    - Dubai has "me" (a selfie made into a hero). Bible and Kalshi have jokes.

12. **Hide AI with light and texture, not with blur filters.**
    - Night, fire, smoke and rain: Zelda, Red Rising, Camelot, Porsche.
    - Hard backlight on faces: Dreamina pursuers.
    - Small picture area: Dubai's prompt panel covers the bottom ~55%.
    - Letterbox at 2.39:1: all the PJ trailers.
    - [inf] Each one lowers the pixels-per-face the viewer can inspect.

---

## 3. Do / don't lists

### Action (stunts, falls, fights, sport)

**Do**
- Plan 6–10 shots per 30 s. Use 1.5–2.5 s shots for the action and a 3–5 s hold only for the establishing shot or the reveal.
- Put the stunt's impossible instant **between** two shots. Show the take-off and the landing, and cut to a face close-up or an insert for the middle (ICE).
- Write the physics per beat: preload → release → airborne → impact → recovery. Add a "Forbidden visuals" line (no floating, no hang time, no static cloth).
- Show altitude before a fall or canopy: the ground far below, wind on clothing, a 2–4 s freefall (41 §2).
- Script the SFX into the prompt: impact, silence, breath. Use the music bed under it, not instead of it.
- Prefer motion transfer from real stunt footage, or your own phone plate, when the move is complex.

**Don't**
- Don't put the camera through glass, walls, cars or a body. Break the glass **around the actor** (Lindy).
- Don't hold a full-body action move for more than about 2 s in one shot.
- Don't use a locked wide as the only angle for a fight (Baby Battles).
- Don't let the caption claim what the pixels can't show. Dubai's caption claims a fall; the film shows a drone dive. Let the edit imply the impossible part.

### Chase (car, foot, vehicle)

**Do**
- Cover the chase from rig positions: drone/FPV wide, chase car at bumper height, camera car ahead (nose-on), door or mirror mount, cockpit 3/4, wheel/tyre insert, locked roadside pass-by (Dubai has all of them).
- Give the chase **turns and obstacles**: a corner drift with smoke (Porsche), a crossing, a hiding place, a door (Dreamina). A straight line is not a chase.
- Show the pursuer in its own shots (Dreamina's backlit pursuers), then cut back to the hunted.
- For a foot chase, use feet, back, hands and face inserts, not a long full-body run.
- Layer the engine/whoosh SFX on every pass-by. The low band should swell on the pass (Dubai +10 dB).
- End on a locked-off wide: the car drives away into the horizon (Dubai 29 s).

**Don't**
- Don't make the whole chase one camera move.
- Don't land a person in a moving car. Cut from the dive to the driver **already in the seat** (Dubai).
- Don't hold on tyre–road contact at low speed; hide it under smoke, rain spray and motion blur.
- Don't post a pretty car with no person, no stakes and no hook. It gets about 1K plays (Baran Robin).

### Product (VXO's core)

**Do**
- The one-take is still right for sensory product beats (pour, spray, unbox), as long as nothing passes through anything (41 §1, 37).
- Use a diegetic camera when you need long takes: a selfie, a news crew, a documentary. That is what lets Bible run 9 s takes and Kalshi run vox-pops.
- Carry the brand in a device (ticker, odds, caption), not in a 5 s centred packshot (22).
- Put the hook motion in frame 0, and use a persistent one-line caption that promises a payoff.
- For "made with AI" audiences, show the input photo and prompt; ask for "Comment X".

**Don't**
- Don't make the product do physics: liquid transfer, fast rotation (37 §0).
- Don't give speaking lines to faces that must look real unless lip sync is verified. IM8 deliberately had none.
- Don't run music with no SFX on product action.

---

## 4. Five annotated gold-standard examples

### 4.1 "Dubai", @edbert_yienson: the car reel the owner keeps sending
[IG](https://www.instagram.com/edbert_yienson/reel/DcDrXjXsLcU/) · 30 s · 9 shots · Seedance 2.5 1080p · input: one passport-style headshot

Shots [m], with the on-screen prompt text [c]:

| # | Time | Framing / move | Rig | Prompt line |
|---|---|---|---|---|
| 1 | 0.0–13.1 | Top-down from the spire → dive → tilt to the horizon → road level → pulls alongside the yellow Huracán → rounds to the side | FPV drone | "Descent from the spire tip down toward street level, continuous aerial dive, the yellow supercar picked out and spotlighted on the right side of the frame as it comes into view below." |
| 2 | 13.1–15.8 | Side profile hold; the car overtakes and exits frame | Chase car | "Side view … camera holds a lateral profile position, then the car accelerates and overtakes past the camera, exiting frame." |
| 3 | 15.8–17.7 | The rear-view mirror with the driver's eyes | Interior mirror mount | "Center rear-view mirror shot … road and skyline receding behind." |
| 4 | 17.7–19.4 | Nose-on, headlights | Camera car ahead | "Front-on view … grille and headlights facing the camera." |
| 5 | 19.4–21.5 | Cockpit from the right side | Passenger-side rig | "Cockpit view of the driver … from a right-side angle." |
| 6 | 21.5–24.2 | Rear-bumper 3/4, the car pulls away in traffic | Chase car | "Driving on a straight road, camera angled from the rear bumper, 3/4 perspective." |
| 7 | 24.2–26.0 | Hands on the wheel | Interior | (no matching line in the list; the nearest is the 0:20–0:21 cockpit) |
| 8 | 26.0–28.6 | A side pass a second time | Roadside track | "Side view of the car again … passes the camera a second time." |
| 9 | 28.6–30.1 | A locked-off 3/4; the car drives through into the distance | Tripod | "Static camera, 3/4 angle, locked-off shot, the car drives through and past frame to close the sequence." |

**Why it works:**
- **The impossible part is a drone, not a man.** The hero is introduced already in the car (shot 3).
- Shots 2–9 are textbook car-ad coverage, each about 2 s.
- The engine sound rides the passes.
- The prompt panel shrinks the picture and turns the reel into a "how-to", which is why it gets more comments than likes.

**What VXO copies:** the timecoded single-prompt shot list and the rig-only camera positions.

### 4.2 Dreamina Seedance 2.5 launch: the chase
[TikTok](https://www.tiktok.com/@dreamina_ai/video/7668553891792964894) · 160 s · 71 shots · ASL 2.25 s [m]

The sequence, 0–30 s:
- 0–2 s: an elevator-button insert and a panicked face.
- 2–3 s: a finger on the button (a cause-and-effect insert).
- 3–5 s: she falls out into the sky (the world change, cut on her motion).
- 8–9 s: a wheat-field wide.
- 9 s: hiding in the hay, low CU.
- 10–12 s: pursuers walk toward camera, backlit.
- 14 s: a hand drops an object (an insert).
- 15–17 s: she runs. Shown as a wide from behind, a boot insert and a hand insert.
- 21–23 s: a low track on boots, then she enters a saloon.
- 24–29 s: reaction faces, a POV floor run, hands on a door.

**Why it works:** the chase has **geography and obstacles** (field → hay → road → saloon → door). It is always cut on motion, and no shot asks the model to render a long sprint.

**What VXO copies:** the chase-as-inserts pattern and the change of environment every 5–8 s.

### 4.3 "ICE", @edbert_yienson: physics written as a script
[TikTok](https://www.tiktok.com/@edbert_yienson/video/7691556396361370901) · 14 s · 4 shots · [prompt doc](https://docs.google.com/document/d/13Pn7yozU3FCd66cB_v5t-J-hK3mhSaveIemB32tSJ_g/edit)

The prompt structure [c]:
1. Style and genre ("ultra-realistic competitive documentary").
2. World and lighting language ("skate blades cast sharp moving shadows").
3. Visual feel ("each push and landing carries clear mass and inertial load").
4. **Forbidden visuals.**
5. A beat map.
6. Character identity lock (@image1 from a selfie-based **turnaround sheet**).
7. Physics (propulsion, rotation, balance).
8. A **per-second storyboard**, where each second gives Camera, Action, Body, Physics and VFX.
9. A sound-design list.

The cut to a face CU at 9–10 s hides the rotation [m].

**What VXO copies:** the per-second Camera / Action / Body / Physics / VFX / Sound block for every action beat, plus a Forbidden list.

### 4.4 "If Bible characters were influencers", PJ Accetturo: character comedy
[TikTok](https://www.tiktok.com/@pjacefilms/video/7511268853129809183) · 64 s · 7 shots · 4.8M plays, 9.6% likes [m]

- Each character is one selfie take of 5–13 s: a setup line and a punchline. David's punchline is visual: Goliath walks up behind him at 14 s [m].
- The audio is all dialogue (beat score 0.03) with clean gaps between characters.
- One persistent caption. "Prompts in description" [c].

**Why it works:** the **premise is the hook**; it doesn't need a 1 s visual stunt. The selfie camera justifies long takes, and the wide lens makes AI artifacts read as phone artifacts.

**What VXO copies:** for character comedy, use a diegetic camera with long takes and dialogue punchlines, and **no stunts**.

### 4.5 Lindy AI, PJ Accetturo: action comedy that does what VXO's heist tried
[TikTok](https://www.tiktok.com/@pjacefilms/video/7538130214031756575) · 43 s · ~24 shots · ~1.8 s ASL [m]

- 0–0.5 s: a locked exterior of the office tower glass. At 0.5 s **a man crashes out through the window** (the camera never moves).
- 1–3 s: office reaction shots (a CU of a woman screaming, coworkers pointing at the empty window).
- 3.5 s: the same man's face in the office (a time cut).
- 4.5 s: a POV harness shot with a skyscraper far below (**altitude is shown**).
- 6 s: a street water-gun fight on a telephoto lens.
- 8–12 s: a TV news anchor ("LINDY FEVER SWEEPS THE NATION").
- 13–16 s: the office punchline, then the product UI.

**Why it works:**
- Every stunt is 1 s, cut on impact, and seen from a rig position.
- The parachute moment shows height, not a canopy at roof level.
- Each absurd beat escalates.

**What VXO copies:** this is the fix for the F09 heist. Same ideas (glass, fall, chase), but with coverage, altitude and cuts.

---

## 5. How creators chain generations (observed)

| Method | Where seen | Notes |
|---|---|---|
| **One multi-shot generation with a timecoded shot list** (up to 30 s on Seedance 2.5) | Dubai, ICE, time-stop [c/m] | The cuts follow the timecodes to about ±1 s. Use "Static camera … locked-off" and "camera holds" to stop drift. Seedance 2.5 also has 1 s timestamp control and a 3-minute long-video mode [c, Dreamina] |
| **Connected 15 s sections for a oner** | JSFILMZ 1-min one-take [c] | Only for low-motion dialogue scenes |
| **Per-shot generation from stills, then edit** | PJ: Kalshi 300–400 gens → 15 clips, "each prompt should fully describe the scene as if Veo 3 has no context of the shot before or after" [c] | The classic agency pipeline: Gemini writes 5 prompts at a time |
| **Reference sheet first** | ICE: a selfie → a character turnaround sheet → @image1, plus an environment @image2 [c] | Identity lock across cuts |
| **Video-to-video from real footage** | Rourke (re-angle), Genjutsu (world swap), maorhani (restyle), Baran Robin (motion transfer) [c/m] | Gives the most realistic motion in the corpus |
| **Last-frame continuation** | Not observed in this corpus | Kling 3.0 offers start and end frames plus a 6-shot storyboard in 15 s ([Kling guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide), [review](https://magichour.ai/blog/kling-30-review)) |

Third-party Seedance guides agree:
- One move per shot.
- Use explicit "cut to" or numbered beats, and say which shots must not repeat.
- A reference image beats a corrective text line.
- Name the voice language and which characters are silent; otherwise Seedance invents dialogue.

Sources: [Hedra](https://mkt.hedra.com/blog/directing-seedance-2-5-with-beats), [heyuan110](https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/), [Runway guide](https://runway.com/resources/seedance-2-0-prompt-guide).

## 6. VXO failures mapped to the evidence

| VXO failure | What the corpus does instead |
|---|---|
| The camera passes through glass | The glass breaks around the actor; the camera is locked outside (Lindy 0.5 s) |
| The parachute opens at roof height | The fall is shown as altitude: the tower far below, harness POV (Lindy 4.5 s) |
| The man lands in a moving car | Cut from the drone dive to the driver already in the seat (Dubai shots 1 → 3) |
| A "chase" with no turns | A drift at a crossing (Porsche), changing geography with obstacles (Dreamina) |
| Sound doesn't match action | SFX scripted per beat in the prompt (ICE, time-stop); the engine swells on passes (Dubai) |
| No hook or punchline | Motion in frame 0 plus a persistent promise caption; one punchline per shot (Kalshi), or the premise as the joke (Bible) |
