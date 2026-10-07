# The Creative Brain: how this studio thinks (read FIRST, before any brief work)

We are an ad studio. A visual effect is not an idea. **Spectacle without a point is a demo**, and demos don't get shared, commented on or bought from.

Every ad must have a **PUNCHLINE**: a final turn that makes the viewer laugh, gasp or nod, and that **only works because of the product**.

## 1. The four laws (an ad that breaks one is killed, however pretty it is)
1. **INSIGHT.** A true, recognizable human truth about the audience. ("In Florida, locals act like 98° is normal. It isn't.")
2. **TENSION.** A situation that escalates that truth into conflict, absurdity or stakes in the first 3 seconds.
3. **TWIST (the punchline).** The last 20–30% reframes everything before it. The viewer re-reads the opening in a new light.
4. **BRAND IN THE TWIST.** Remove the product and the joke dies. If the twist still works with a competitor's logo, rewrite it.

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
