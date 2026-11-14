# The Creative Brain: how this studio thinks (read FIRST, before any brief work)

We are an ad studio. A visual effect is not an idea. **Spectacle without a point is a demo**, and demos don't get shared, commented on or bought from.

**Step 0: pick the TONE first** (aesthetic brand film · ASMR ritual · comedy sketch · UGC). The default for this studio's client is an **aesthetic brand film**: clean, premium, brand recognisable in every shot, no talking heads. For an aesthetic film the "punchline" is a **visual payoff** (the reveal, the cold-proof moment, the logo resolve), not a joke.

Every ad must have a **PUNCHLINE**: a final turn that makes the viewer laugh, gasp or nod, and that **only works because of the product**.

## 1. The four laws (an ad that breaks one is killed, however pretty it is)
1. **INSIGHT.** A true, recognizable human truth about the audience. ("In Florida, locals act like 98° is normal. It isn't.")
2. **TENSION.** A situation that escalates that truth into conflict, absurdity or stakes in the first 3 seconds.
3. **TWIST (the punchline).** The last 20–30% reframes everything before it. The viewer re-reads the opening in a new light.
4. **BRAND IN THE TWIST.** Remove the product and the joke dies. If the twist still works with a competitor's logo, rewrite it.
5. **DESIRE (the law the F01 animatic broke).** A funny ad that doesn't make you *want the product* is a sketch, not an ad. The joke earns attention; the product shots must earn the purchase.
   - **Crave shots ≥ 30% of runtime**, shot like the best beverage/beauty stills (see §1b), not "a bottle in a scene".
   - **The product appears in the first 2 s**, as a gorgeous object, before the story starts. The story then explains why everyone wants it.
   - **Prove the benefit sensorially:** cold → frost, condensation sliding, ice cracking, a breath of vapour; taste → pour, splash, bubbles, the first sip in slow motion.
   - **Everything moves.** A still is only for the animatic. In the final ad, every product shot has motion: drips sliding, a light sweep, a rotating bottle, a splash, a push-in.
   - **Test:** mute the ad and remove the jokes. Do the product shots alone make you thirsty? If not, reshoot them.

## 1b. Crave cinematography (the Celsius-shot standard)
The reference standard is a top-tier drink still: one hero product, a **colour world** matched to the flavour or brand (backdrop gradient, props and light share 1–2 hues), **real flavour props** in the frame (fruit, ice, botanicals), **cold proof** (dense droplets, puddles, frost), a **glossy reflective surface** that doubles the product, hard key light with crisp specular highlights, and a centred product filling ≥ 40% of the frame height.
- Every ad gets **3 hero recipes** before story shots: (a) studio colour-world hero, (b) macro cold proof (drop running across the logo), (c) action hero (splash, pour, mid-air spin).
- **Brand colour world:** pick it from the pack (e.g. AURUM = champagne gold + glacier teal). Every chyron, end card and grade leans into it.
- Story shots should still glamorise the product: the bottle gets its own light (rim light, glow), even inside a messy scene.
- **Motion recipes for crave shots** (Kling 3.0 Pro i2v or Seedance): slow push-in + droplets sliding down; 180° turntable with a light sweep; a splash crown frozen into slow motion; ice cubes dropping into frame; the cap twisting off with a vapour puff.

## 2. Punchline mechanisms (pick one deliberately; never "and then a nice packshot")
| # | Mechanism | Shape | Example |
|---|---|---|---|
| 1 | **Misdirection reveal** | We think it's X; it was Y all along | A tense standoff turns out to be over a drink |
| 2 | **Escalation to absurd** | Each beat bigger until it snaps | Heat → sweating → melting → the street signs melt |
| 3 | **Role reversal** | The expected roles swap | The alligator is the one begging for the drink |
| 4 | **Literalization** | An idiom made literally true | "Dying of heat" → a mock funeral |
| 5 | **Deadpan understatement** | Huge event, flat reaction | A news anchor calmly reports total chaos |
| 6 | **Confession** | The brand admits something | "Sorry, the snow was us." |
| 7 | **Callback** | The first line returns with new meaning | The opening question is answered by the can |
| 8 | **Format hijack + wrong content** | Familiar format, absurd story | A nature doc about "the Florida tourist" |
| 9 | **POV twist** | The camera's identity is the reveal | We were watching from inside the cooler |
| 10 | **The real reason** | Why something weird happens, revealed | Everyone at the office "works late"… for the fridge |
| 11 | **Anti-ad** | Mocks advertising itself | "This is the part where we show the can in slow-mo." |
| 12 | **Local truth / identity** | A joke only the target group fully gets | "First summer?" (locals vs tourists) |

## 3. Virality mechanics (design them in, don't hope for them)
- **0–1 s curiosity gap:** a frame that demands "wait, what?" (sound-off readable).
- **Identity:** "Only in Florida", "every mom", "every gym bro". People share what describes them.
- **Comment trigger:** a debatable detail, a question, or a "Florida Man" headline people will riff on. Plan the pinned comment.
- **Rewatch layers:** easter eggs in chyrons and background gags. The punchline makes the start funnier on a second view.
- **Send-to-a-friend test:** who exactly would you send it to, and with what message?
- **Loop:** the last frame flows back into the first when possible.
- **Brand early, but as part of the story** (the cooler, the can), not as an interruption.

## 4. Gates before ANY generation (all must pass; write the answers)
1. Tell the ad as a **joke in one sentence**. If you can't, there is no idea.
2. Do the **last 3 seconds reframe the first 3**?
3. **Remove the product:** does the punchline die? (It must.)
4. **What's the top comment** people will write? Write it.
5. **Who gets it sent to them?**
6. **Is it producible realistically** with today's models (camera style that hides AI flaws: news cam, phone, doc, CCTV, macro, stylized)?
7. **Legal:** fictional brand, no fake testimonials, no health claims, no real people, stations or logos.
8. Run `director.py rank` on the 3 finalists. The winner needs the best mix of shares and comments, **plus a punchline score ≥ 4/5** (a judgment call, stated).

## 5. The full-stack output contract (the "prompt creator" delivers ALL of this)
1. **Concept card:** title, one-line joke, insight, mechanism, tagline, CTA, pinned comment.
2. **Script table:** time | picture | dialogue (on-camera, generated in Seedance) | VO (ElevenLabs) | super/chyron | SFX | music cue. **Mark the punchline beat and the silence before it.**
3. **Shot list:** shot size, lens, camera style, action with physics, model and why, references used, takes, cost.
4. **Image prompts** (image-direction.md template), per start frame or reference.
5. **Video prompts** (video-realism.md templates), timecoded, with identity locks and audio lines.
6. **Voice direction (ElevenLabs v3):**
   - Voice choice and why.
   - Audio tags inline: `[deadpan]`, `[sighs]`, `[whispers]`, `[excited]`, `[clears throat]`, `[laughs softly]`.
   - Pacing ≤ 2.5 words/s.
   - Stability 0.35–0.5 for acting, 0.6+ for announcer reads.
   - Style 0.3–0.6.
7. **Sound design** (ElevenLabs SFX, each with timing):
   - Ambience bed.
   - Foley per action.
   - Transition hits.
   - **The comedic tools:** record scratch, silence, a sting on the punchline.
   - A 1-second sonic logo.
8. **Music prompt** (ElevenLabs Music): genre, BPM, instrumentation, structure with timestamps matched to the beats ("drop out at 0:19 for the silence beat, return at 0:21").
9. **Edit spec** (reel-studio JSON):
   - Cuts on the beat.
   - Comedy timing: hold a 0.5–1 s beat before the punchline, then smash cut.
   - Freeze frames.
   - Chyrons and supers inside safe zones.
   - Word-timed captions that emphasize the punch word.
   - An end card with logo, tagline and CTA.
   - Versions: 30 s master, 15 s cutdown, 3 hooks.
10. **QC plan:** K1–K8, R1–R4, the rubric ≥ 80, the punchline test with a cold viewer.
11. **Retro (after delivery):** what landed, what didn't, what changes in the brain next time. Append to the lab NOTEBOOK.

## 6. Comedy and drama craft notes
- **Specific beats generic.** "98 degrees in Boca" beats "a hot day". "Grandma's cooler" beats "a cooler".
- **Commit to the bit:** characters play it 100% straight. The absurdity is funnier when nobody acknowledges it.
- **Rule of three:** setup, reinforce, subvert on the third.
- **The silence before the punch is the joke's drumroll.** Drop the music.
- **End on the button:** a tiny extra laugh after the tagline (the gator burps; the anchor slowly sips).
- **Realism hides in formats:** news footage, CCTV, phone video and nature docs forgive AI imperfections and add believability.

## 7. Upgrades v2 (writers' room → animatic → controlled performance)
1. **Writers' room, fast and wide:**
   - 20 premises in 10 minutes across at least 6 mechanisms. Kill 17.
   - For the 3 survivors: **3 alternative punchlines + 3 alternative buttons + 3 taglines each**, then pick the sharpest combination.
   - The tagline should *echo the joke* ("Worth wrestling for" beats a generic benefit line).
2. **Synthetic audience panel** (Claude role-plays honestly, before spending):
   - Five viewers: a Florida local, a Gen-Z scroller, a busy mom, a cynical marketer, the brand manager.
   - Each answers four questions: Did you get it at 0:03? Did you laugh or gasp at the twist? What would you comment? Would you send it, and to whom?
   - Fix anything two or more viewers flag.
3. **Retention beat map:**
   - Write one line per second for the whole ad.
   - Every 3–4 s there must be a **re-hook**: a new image, a sound, a line, a reveal.
   - Mark the silence-before-the-punch and the button.
4. **Character bible before video:**
   - Every recurring person or animal gets a cheap character sheet (Soul v2, batch of 4, ~$0.02). Pick one.
   - Use that image as the identity reference in every image and video prompt. This prevents face drift across shots.
5. **Animatic before video (the biggest money saver):**
   - Generate a still for every shot (cheap), record VO, dialogue, SFX and music with ElevenLabs, and cut a **still animatic** in reel-studio with the real timing.
   - Watch it and test the punchline. Only then spend on video.
   - Bad timing costs cents here instead of dollars.
6. **Controlled performance:**
   - Generate on-camera dialogue with ElevenLabs first: one consistent voice per character, eleven_v3 tags for acting.
   - Pass those lines to Seedance 2.5 as `audio_urls` references (they don't count as billable video input), so the lip-sync follows *our* delivery and timing.
   - Re-lay the clean ElevenLabs audio in the edit.
7. **Format camera specs** (realism through format):
   - **News studio:** locked-off, cool key, a slight broadcast sharpening look.
   - **Field news:** shoulder cam, auto-exposure pumping, a wind-noise feel.
   - **Phone bystander:** vertical, digital zoom jumps, focus hunting, compression.
   - **CCTV:** high angle, fisheye, timestamp added in post, 15 fps feel.
   - **Nature doc:** long lens, shallow DOF, slow pans.
8. **Kill-your-darlings check:** if a shot doesn't serve the joke or the brand, cut it, however pretty.
