# 44 — Action and comedy craft: physically real action, real punchlines

**Why this exists.** The owner rejected the heist film: *"not realistic, not a real chase, a parachute can't open like that, no turns with the car, nothing."* On the earlier films: *"no punchline, no hooks."* This file is the craft base that every future action or comedy script must pass. It extends ch. 41 (action-realism checklist), ch. 35 (punchline mastery) and ch. 37 (AI action execution). Where they conflict, this file wins for action and for comedy structure.

**How to read the tags.** `[src]` means a cited source supports it (see §11). `[calc]` means we computed it from basic physics (formulas given). `[craft]` means standard industry practice or our own inference; treat it as a strong default, not a fact.

**Research note.** YouTube transcript pulls (`yt-dlp --skip-download --write-auto-subs`) were blocked from this environment (HTTP 429, then "Sign in to confirm you're not a bot"). Every claim here therefore comes from written BTS articles, stunt-coordinator interviews, police policy manuals, parachuting manuals and ad case studies. No footage was downloaded or republished.

---

## 0. The ten rules (read this if you read nothing else)

1. **Action is coverage, not one heroic camera move.** Real chases are cut together from many short shots from different rigs: chase car, in-car, static "crash cam", aerial. *Bullitt* was shot street by street, out of order, over three weeks, and assembled "like a deck of cards" in the edit [src: Hagerty/Jalopnik]. *Fury Road* has about 2,700 shots, averaging about 2.7 s each, and less in the action [src: NoFilmSchool/Vashi].
2. **A turn is the proof of a chase.** A car cannot take a 90° city corner at speed. Lateral grip is about 0.9 g, so a tight corner (radius about 8 m) caps out near 30 km/h [calc]. Every chase needs this visible sequence: nose-dive under braking → body roll → rear steps out → tyre smoke → squat as the car accelerates out. "No turns with the car" is exactly what the owner flagged.
3. **A parachute needs height and time.** From a tower, the jumper gets 2–4 s of visible freefall (20–70 m), then a pilot chute → line stretch → snatch (under 1 s) → canopy inflation (1–3 s, slider moderated) → a flying rectangular wing → steering with toggles → a flare and a run-out into the wind [src: BASE charts, CSPA, USPA]. A canopy that "pops" open at roof height and floats down like a balloon is the #1 fake tell.
4. **Gravity is a constant the audience feels.** Fall times are fixed: 1 s ≈ 5 m, 2 s ≈ 19 m, 3 s ≈ 42 m [calc]. If a fall from a 10-storey building lasts 6 seconds on screen, viewers feel it is fake without knowing why. Never slow-motion a fall without a reason established on screen.
5. **Cause → effect must be visible in adjacent shots.** If a car brakes, the next shot shows the nose dipping. If a person lands, the surface reacts: a roof dents, gravel scatters, the knees fold. Missing contact reactions are what make CGI falls look weightless [src: Physics World, Film Stories].
6. **Centre-frame the subject so fast cuts stay readable** (Miller's "crosshairs" on set) [src: Vashi Nedomansky, Eugene Wei]. Keep screen direction constant: if the hero drives left-to-right, the police also come left-to-right [craft].
7. **Police in a chase act like police.** PIT only at matched low speed (most policies cap it at 35 mph / 56 km/h), boxing-in, spike strips placed ahead, a helicopter that tracks rather than stops [src: LASD, CHP, CORSA policies]. A comedic chase can bend outcomes but not procedure.
8. **Rule of cool needs a planted rule.** Audiences forgive one impossible beat when the film has taught them the rule before it is used [src: TV Tropes, Final Draft]. Plant it in the first third, pay it off at the end.
9. **The punchline is a reversal of the expectation built by the setup, and the product causes the reversal.** VW's *The Force*: the boy "uses the Force", the dad's remote start is the product feature, and that is the punchline [src: Muse by Clio]. Old Spice: every scene flips on the line "now back to me" [src: Muse by Clio oral history].
10. **Hook in second one, payoff in the last three seconds, loop back to frame one.** The hook is a sound or an image that poses a question (a siren, a tyre screech, a man on a ledge). The last frame should rhyme with the first so the viewer replays it [src: Later, loop guides].

---

## PART A — ACTION REALISM

## 1. Car chases: how the real ones were made

### 1.1 Case notes (what to steal)

| Film | What they actually did | What to steal for a 30 s ad |
|---|---|---|
| **Bullitt (1968)** | Bill Hickman drove the Charger; McQueen did close-ups, with stunt doubles (Bud Ekins, Loren Janes) for the dangerous runs. Two weeks of practice at Cotati Speedway at over 100 mph. Shot street by street, out of order, over about 3 weeks; cars jumped every intersection on Taylor St. Continuity errors (the same green VW passed 3 times, hubcaps lost more than 4 times) because the same hill was reused from several angles [src: Wikipedia/Hickman, Hagerty, Jalopnik, IMDb goofs]. | Hill crests make the suspension compress and unload, the most "weighty" image in car film. **Continuity warning:** in AI, wheel trims, dents and background cars drift; lock them per shot. |
| **The French Connection (1971)** | No permits. Hickman drove 26 blocks at 70–90 mph; Friedkin operated a camera over Hickman's shoulder and another was bumper-mounted. Off-duty police cleared about 5 blocks in each direction; some near-misses were real [src: Take One 1971 via Lantern, Hagerty, The Autopian]. | **Bumper-height POV** plus **over-the-shoulder in-car** carries most of the fear. Show near-misses with *civilian* traffic: a pram, a delivery van. |
| **Ronin (1998)** | Frankenheimer: "not in process, not in green screens, not with computer tricks". Real speeds of 100+ mph in Paris. **Right-hand-drive cars** with a dummy wheel on the left for De Niro, so a pro could drive flat out. Camera mounts from *Grand Prix* in the front boots of Porsche 911s. Wide lenses on Super 35 for deep focus. About 100 race drivers played wrong-way traffic at about 35 mph while the heroes did more than twice that. Engine notes recorded separately at a track; gear downshifts and handbrake pulls added in the edit [src: Hagerty UK, Driven, Car Magazine]. | **Sound sells driving.** Downshift blips, handbrake ratchet, tyre squeal on every turn. **Wrong-way traffic** at half the hero's speed reads as twice as fast. **The actor's real fear** = cut to faces. |
| **Baby Driver (2017)** | Jeremy Fry did the "180 in, 180 out" between trucks for real, at 55 mph (Prescott says 70), in about 5 takes. They rehearsed it in a parking lot with cones and measured the real alley. The road was wetted for slide. A **pod car** let Fry drive from a roof pod while the actors "drove" inside. It was shot on a drone because the alley was too narrow for a helicopter. CGI was used only for clean-up [src: THR, Hagerty, CBC Day 6]. | **Rehearsable stunts only.** Every move in our scripts should be one a stunt driver could rehearse in a lot with cones. **Wet tarmac** = believable slides plus reflections. |
| **Bourne Supremacy (2004)** | Dan Bradley (2nd unit) ran the stunts; Damon called it "NAR, no acting required". Rouse's edit stacks fragments under a second long (a wheel turning, the eyes flinching) instead of wides; the handheld camera "reacts" like a passenger [src: NoFilmSchool, Hagerty, Den of Geek]. | Insert shots (wheel, foot on pedal, mirror, handbrake hand) are the cheapest realism. **Warning:** fragmented geography only works in a 2-hour film. In 30 s, keep one clear wide every 3–4 shots. |
| **Spectre (2015) Rome** | Gary Powell: "no CGI, no jump cuts". The stunt cars outran the camera helicopter and had to slow down. Top speed about 110 mph. "One entire night for four seconds of film" [src: Top Gear, NOLN]. | Budget reality check: **4 s of usable chase per night of shooting**. A 30 s ad cannot hold 10 stunts; it holds **one hero stunt plus 6–8 connective shots**. |
| **Fast & Furious** | Mixed: some real (*Furious 7*'s cars out of a plane), many CG set pieces; widely criticised as "weightless" [src: AU library blog, MovieWeb]. | When the car obeys no grip limit (cornering at 150 km/h, a safe swinging a car), the audience disengages. Spectacle has to keep mass. |
| **Mad Max: Fury Road (2015)** | About 3,500 storyboards (Mark Sexton). Miller on set: "put the crosshairs on her nose". Sixel cut 480 h down to about 2,700 shots; centre framing lets the viewer read each shot instantly. A simple route: drive out, turn, drive back [src: Vashi, Eugene Wei, NoFilmSchool]. | **Storyboard every shot. Centre-frame the subject. Keep a simple A→B geography** that the viewer could draw. |

### 1.2 Camera rigs: what each one *looks like* (write these into prompts)

| Rig | Look | Use for |
|---|---|---|
| **Russian Arm / camera car** (gyro-stabilised remote crane on a high-speed vehicle) | Smooth, sweeping moves alongside and around the car at speed; low to the road or rising over it [src: Morphic glossary] | Hero glamour pass, rising reveal, crane-over |
| **Chase car, bumper mount** (*French Connection*, *Ronin* Porsche boot mount) | Fixed, low, slight vibration, road rushing under the frame | Pursuer's POV, tension |
| **Hard mounts** (hood, door, rear bumper; suction or bolt-on) | Locked to the car, background whips past; shows driver and windshield | Driver face, reactions, mirror |
| **Pod car / biscuit rig / process trailer** | Actor "drives" while a pro drives from a roof pod or tow rig [src: THR; Morphic] | Close dialogue while moving; never show the pod |
| **Drone (camera drone)** | High wide, follows from above, can enter narrow alleys (Baby Driver) | Geography wides, top-down drift |
| **FPV drone** | Fast, banking, dives to bumper height, threads gaps. The Red Bull rig hit 350 km/h but flies only about 3 min [src: Carscoops, T3] | One-shot "follow-through" moves; transitions |
| **Static "crash cam"** | Locked-off at ground level; the car fills the frame and exits; often several angles of one take | Near-miss, pass-by, impact |
| **Helicopter** | Very high, slow-feeling wide | News-chopper look for police chases |
| **In-car handheld / over-the-shoulder** | Shaky, intimate, the windshield shows the road | Fear, the passenger's view |

**Prompt rule [craft]:** every shot names *one* rig. "Camera follows the car" is not a shot. "Low bumper-mounted camera on the chase car, 1 m behind, 40 km/h" is.

### 1.3 Driving physics (what MUST be visible)

| Event | What a real car does | Real numbers |
|---|---|---|
| **Hard braking** | Nose dives, rear lifts, the driver's body pitches forward; on old cars with no ABS, tyres lock and smoke | Street tyres about 0.8 g dry. From 50 km/h: 12 m to stop, plus 21 m of reaction at 1.5 s. From 100 km/h: 49 m plus 42 m [calc: d = v²/2a] |
| **Acceleration** | Rear squats, front lifts, wheelspin on RWD, smoke | — |
| **Cornering** | Body rolls to the outside, the outside tyres squash, it squeals near the limit | About 0.9 g max. Corner radius 8 m → about 30 km/h; 15 m → about 41; 30 m → about 59; 60 m → about 83 [calc: v = √(0.9·g·r)] |
| **Handbrake turn** (forward 180, or 90 into an alley) | Steer to load the outside tyres, pull the handbrake to lock the rears, the rear swings, release and power out | Rally schools teach it at about 30 mph (48 km/h) on tarmac, slower on loose ground [src: Team O'Neil, Wikipedia/Handbrake turn] |
| **J-turn** ("Rockford") | Fast reverse, lift, a sharp half-turn of the wheel, a brake tap, the nose swings round 180°, drive forward | Modest reverse speed (it is reverse gear); a closed lot; the classic stunt-driving move [src: Wikipedia J-turn, Fox] |
| **Drift / power slide** | The rear steps out, the driver counter-steers (front wheels point *into* the slide), smoke from the rears only | Needs RWD or AWD and power; wet roads make it easier (*Baby Driver* wetted the road) |
| **Jump / hill crest** | Suspension unloads, the wheels droop, the landing compresses the springs fully, sparks off the sump, a bounce | Bullitt's Taylor St; one jump per ad, max |
| **Near-miss** | The pass-by car's slipstream moves hair and paper; the horn dopplers | — |
| **Damage continuity** | A dent stays a dent; a lost mirror stays lost | AI drift risk: lock it per shot |

### 1.4 Police tactics (for comedic but credible chases)

| Tactic | How it really works | Ad-safe comedic use |
|---|---|---|
| **PIT (Pursuit Intervention Technique)** | Match speed, gently touch the rear quarter, quarter-turn the wheel toward it; the target spins. Most agencies cap it at **35 mph (56 km/h)**: LASD, CHP, Albuquerque, Iowa; some cap at 40–50 mph. Above 35 mph it is deadly force in OR and WI [src: LASD manual 20-001, ABQ draft 2-12, Type Investigations] | Show a *setup* for a PIT that never happens (the comedy reversal); never show the spin into traffic |
| **Boxing-in / rolling roadblock** | Two or more units surround the car and all slow down together to a stop [src: CORSA model policy; Illinois State Univ. policy 305] | Perfect comedy device: from above, the box looks like an arrest… then it turns out to be an **escort** (SOL-2) |
| **Spike strips (stop sticks)** | Laid across the road ahead; suspects swerve around them; some departments banned them [src: Police & Security News] | Show a cop placing them, then the hero politely stops *before* them |
| **Roadblock** | Static vehicles across the road, usually at a choke point | A choke point means a planned escape route: alley, tunnel, wrong-way ramp |
| **Air support** | The helicopter tracks; it cannot stop the car; it is great when suspects bail on foot [src: Police & Security News] | Searchlight beam = instant "police chase" shorthand |
| **Formation** | 2–3 cruisers max; the lead car plus a secondary; others parallel | Never 15 cop cars in a 30 s ad: it is unreadable and fake |

### 1.5 Escape tropes that read as real (pick one per ad)
- **Alley escape**: handbrake 90 into a narrow alley; the police overshoot.
- **Tunnel / parking-garage swap**: the car goes in, a different car comes out.
- **Wrong-way lane**: oncoming traffic at half the hero's speed (*Ronin*).
- **Blend-in**: the car stops at a red light among identical cars (comedy gold: it obeys the law).
- **Ramp-to-ferry / trailer swap**: drives up a ramp into a moving truck (needs speed matching; low speed only).
- **On-foot bail-out** to a rooftop or metro: the chase changes medium.

---

## 2. Stunts: BASE, parachutes, wingsuits, rooftops, falls

### 2.1 BASE jump and parachute physics

**Freefall table** (belly, terminal ≈ 55 m/s ≈ 200 km/h) [calc: v = vt·tanh(gt/vt), d = vt²/g·ln cosh(gt/vt); terminal 180–225 km/h per src: Wikipedia]

| Time from exit | Speed | Distance fallen |
|---|---|---|
| 1 s | 35 km/h | 5 m |
| 2 s | 68 km/h | 19 m |
| 3 s | 97 km/h | 42 m |
| 4 s | 121 km/h | 73 m |
| 5 s | 141 km/h | 109 m |
| 6 s | 156 km/h | 151 m |
| 8 s | 176 km/h | 244 m |
| 10 s | 187 km/h | 345 m |

**Delay vs object height** (Apex BASE pilot-chute chart, a rough guide only): about 0–1 s at 200 ft (60 m); 2–3 s at 500 ft (150 m); 4–6 s at 900 ft (275 m); 7–9 s at 1,500 ft (460 m) [src: Apex BASE chart].

**Below about 60 m** jumpers use **static line / direct bag / PCA** (the canopy is pulled out by a line tied to the object) with **slider off**, so there is effectively no freefall [src: Wikipedia BASE]. Anecdotal canopy time: about 8 s from 160 ft, about 2 s from about 100 ft [src: r/basejumping]. **A 5-storey roof (15–20 m) is not a BASE exit. Never write it.**

**The deployment sequence (write each as a beat):**
1. **Exit**: a push off the edge, arms out, stable belly, looking at the horizon.
2. **Freefall**: 2–4 s on a 150–300 m building or tower; the clothes ripple, the hair streams up.
3. **Pitch**: the hand throws the pilot chute (a small round chute) into the air beside the hip.
4. **Line stretch / snatch**: the bag lifts off the back, the lines stretch; the "snatch" is sharp, **under 1 s** [src: patent US4664342/CSPA].
5. **Inflation**: the rectangular **ram-air** canopy fills from the nose; the slider (a fabric square on the lines) moderates it over **1–3 s**. Opening shock is typically **3–7 g**, up to 12 g extreme [src: CSPA hard-openings doc; patents]. *Visual:* the body jerks upright, the legs swing forward, the head nods.
6. **Canopy flight**: it is a **wing**, not a balloon. It flies forward at roughly 30–40 km/h and sinks at about 4–6 m/s [craft: typical ram-air numbers; verify with the manufacturer]. The jumper steers with **toggles** (handles on the brake lines) above the head.
7. **Off-heading danger**: an opening that turns toward the wall is the main killer in BASE [src: BASE Brake Settings, skydivemag]. A drama beat is allowed; a comedy beat is not.
8. **Landing**: turn **into the wind**, at about 3–4 m up pull both toggles down (**flare**), forward speed bleeds off, touch down feet first and run 2–4 steps, or a PLF roll [src: USPA SIM flare drills].

**Skydiving (aircraft) cue**: deployment is at about 600–1,200 m AGL; the opening takes several hundred feet [craft; check USPA BSRs for the current minimums].

**Fake tells to ban:** a round "army" chute on a sport jumper; a canopy that opens *instantly* in under 0.3 s; opening at roof height with no freefall; a canopy that descends vertically like a balloon; landing on a moving car; landing with no flare and no run-out; packing a chute on the roof in seconds; jumping with no visible container on the back.

**Real benchmark:** *Mission: Impossible – Dead Reckoning*: Cruise did 500+ skydives and 13,000+ motocross jumps first, rode off a purpose-built ramp in Norway, did the stunt 6 times in one day, and first practised from a helicopter [src: CBS, Slashfilm]. Real BASE has months of preparation behind it; the film must show the gear and the procedure.

### 2.2 Wingsuits

| Fact | Number |
|---|---|
| Glide ratio | about 2.5:1 (modern suits up to 3:1); older suits about 2:1 [src: Wikipedia; JAFM paper] |
| Forward speed | about 100–160 km/h [src: Wikipedia; Symscape; ScienceABC] |
| Sink rate | about 40–65 km/h (vs about 195 km/h belly freefall) [src: same] |
| Needs | a high exit (a mountain or an aircraft). The suit needs several seconds and 100 m+ of fall to "inflate" and start flying [craft] |
| Ends with | a normal canopy deployment and landing. **A wingsuit never lands on its own** |

**Realism rules:** wingsuit flights in an ad come from a **mountain exit or a plane**, are filmed by a **second wingsuiter with a helmet camera** (camera flyer) or a long-lens ground camera, and end under a canopy. No wingsuit from a city rooftop.

### 2.3 Rooftop escapes (parkour)

- **Gap jumps**: a non-athlete clears about 3 m with a long run-up (40–60 ft runway suggested for 10 ft) [src: Art of Manliness]. Trained free-runners land more, especially to a **lower** roof [craft]. In ads, write **gaps of 1.5–3 m with a drop of 1–2 m**, landing into a roll.
- **Casino Royale crane chase**: done "in one" by Adam Kirley (doubling Craig and Foucan), with a wind limit of about 12 mph for crane operations [src: Total Film via PressReader, From Tailors With Love].
- **Real rooftop vocabulary**: vaults over AC units, a hanging drop off a parapet (hang first, then drop, which halves the fall), a run along a ledge, a ladder slide, a lazy vault onto a fire escape, a kong vault, a precision landing (balls of the feet on a wall).
- **Contact reactions**: gravel spits on landing, the roll takes the impact, the hands slap the parapet, breathing is heavy.

### 2.4 Falls onto vehicles: why they look fake

| Fall height | Impact speed [calc: v = √(2gh)] | Reality |
|---|---|---|
| 2 m | 23 km/h | Survivable roll; a car roof dents visibly |
| 3 m | 28 km/h | Pro stunt with a pre-weakened, padded roof |
| 5 m | 36 km/h | Serious injury without rigging |
| 10 m | 50 km/h | Not a stunt landing; descender rig or airbag only |
| 20 m | 71 km/h | Airbag territory (Ontario guideline: boxes ≤ 40 ft / 12 m, airbags ≤ 120 ft / 37 m; 2 spotters for any fall over 15 ft) [src: Ontario film safety guideline No. 25] |

**Why AI and CGI falls look fake** [src: Physics World on VFX; Film Stories "weightless"; craft]:
1. The body does not **decelerate on contact**: no knee fold, no bounce, no roof crumple.
2. **Timing is wrong** (see the freefall table): a 3-storey fall takes about 1.4 s, not 3.
3. **Superhero landing**: one knee and a fist, at 50 km/h, with no damage. Banned.
4. **The car does not react**: no suspension compression, no glass crazing, no body roll from the extra 80 kg.
5. **Landing in a moving car**: needs exact matching of speed and position; basically never done for real. Use **a stopped vehicle**, a **truck bed at walking-speed match**, or **cut away** and show the aftermath.

### 2.5 Safety vocabulary that makes BTS-style shots credible
Descender rig (a wire that brakes the fall), airbag, crash mats/boxes, spotters, safety divers, wind checks (Casino Royale had a 12 mph limit), a rehearsal in a lot with cones (*Baby Driver*), a dummy steering wheel (*Ronin*), the pod car. These also make great **deadpan comedy props** (see SOL-4).

---

## 3. Heist-film grammar

### 3.1 The five beats [src: Industrial Scripts; NPR Pop Culture Happy Hour]
1. **The Plan**: an impossible target is shown (a blueprint, a scale model, "if everything goes right" voice-over).
2. **The Team**: each member has one skill, shown in one shot each.
3. **The Execution**: cross-cutting between team members, a ticking clock (Vee's stopwatch is literally this).
4. **The Complication**: something goes wrong (an alarm, a guard, a malfunction).
5. **The Twist / Hidden Plan**: "there was a secret plan you weren't in on"; the complication was part of it. The audience is only let in once it seems to go wrong.

### 3.2 Editing grammar of heists [craft, drawn from the above]
- **Tell-then-show**: the plan is narrated over shots of it working (a flash-forward), then reality diverges.
- **Cross-cutting with a clock**: the cuts get shorter as the deadline nears (about 2 s → 1 s → 0.5 s).
- **Match-cuts between plan and reality** (the blueprint line → the real corridor).
- **Withheld information**: one shot is cut short or blocked (a hand covers something), then replayed at the reveal with the missing frame. This is the "rewind reveal".
- **Freeze/stopwatch beats**: a sound sting on each clock check.

### 3.3 The 30 s heist compression [craft]
`0–2 s` the impossible target plus the hook sound → `2–8 s` the plan in 3 cuts → `8–20 s` execution plus one complication → `20–26 s` the twist that the product causes → `26–30 s` the product hero plus the loop to frame one.

---

## 4. Plausibility: what audiences instantly flag as fake

| Category | Flag | Fix |
|---|---|---|
| **Physics: gravity** | Wrong fall time; floaty arcs; hair and clothes not reacting to the air | Use the freefall table; add wind on the clothes |
| **Physics: mass** | Cars corner with no roll; impacts with no deformation; a person lands with no knee bend | Show weight transfer and contact reactions |
| **Scale** | Debris or water drops too big or slow (miniature look) [src: Physics World] | Real-scale references in frame (a person, a door, a lamp post) |
| **Speed** | Background motion blur that doesn't match the claimed speed; trees passing too slowly | Use a known reference: lane dashes are 3 m apart in many countries [craft] |
| **Cause → effect** | Brake lights with no nose dive; a siren but no police visible for 20 s; a canopy opens with no pilot chute | Every effect has its cause in the adjacent shot |
| **Continuity** | Hubcaps, dents, wet vs dry road, the time of day, the same extra passed 3 times (*Bullitt*) | Continuity sheet per car and per character (AI: re-reference every shot) |
| **Camera** | A camera that passes through glass or cars; impossible framing; no rig could be there | Name a real rig per shot (§1.2) |
| **Behaviour** | Civilians not reacting to a chase; police not using procedure | One reaction shot of a civilian per chase (a pedestrian steps back) |
| **Sound** | No engine change on gear shifts; no tyre squeal on turns; a silent canopy opening | Write the sound into every shot (a downshift, the canopy "whump", fabric flutter) |

### 4.1 How filmmakers hide or justify the impossible ("rule of cool with grounding")
1. **Plant the rule early, pay it off late** (§0 rule 8). If AURUM's hiss stops traffic in shot 1, it can stop the police in shot 8.
2. **Ground everything around the impossible beat.** One impossible thing per ad; everything else obeys physics. The realism of the surroundings buys credit for the one cheat.
3. **Cut away at the impossible moment**, then show the aftermath (the hero is in the car, dusted off). The audience fills the gap; the Kuleshov effect does the work.
4. **Comedy licenses the impossible, but only if it is *played straight*.** Deadpan characters treat the absurd as normal (Skittles' "parallel universe", Liquid Death) [src: Creative Review, Shopify]. The world must be internally consistent even if absurd.
5. **Show the rig / BTS as the joke** (meta). Otto's world is a film set: a stunt can be revealed as a stunt (airbag, descender) and that becomes the punchline (SOL-4).
6. **Real reference over invention.** Copy the *procedure* of real stunts (pilot chute, flare, J-turn). Viewers recognise the procedure even if they could not name it.

---

## 5. Shot-coverage templates per genre (6–10 shots, 15–30 s)

Durations are targets; the final shot always holds ≥ 2.5 s for the product. Every shot names its rig.

### 5.1 Car chase (30 s, 9 shots)
| # | s | Shot | Rig | Must show |
|---|---|---|---|---|
| 1 | 1.5 | **HOOK**: tyre screech or siren over a black-to-cold-open; low front 3/4 of the car launching (squat, wheelspin smoke) | Static crash cam, low | Sound before image |
| 2 | 3 | Aerial wide: the car plus 2 police cruisers on a clear A→B street | Drone, high | Geography, screen direction L→R |
| 3 | 2.5 | Driver over-the-shoulder, the windshield road ahead, eyes to the mirror | In-car hard mount / handheld | Fear/cool face |
| 4 | 2 | Insert: the hand pulls the handbrake / a downshift | Hard mount | Cause |
| 5 | 3 | **The turn**: nose dive, the rear steps out, a handbrake 90 into an alley, smoke | Chase car, bumper height | Effect: weight transfer |
| 6 | 2 | Police overshoots the alley, brakes hard, nose dive | Static crash cam | Consequence |
| 7 | 3 | A civilian reaction / near-miss: a delivery van brakes | Static, long lens | Real world reacts |
| 8 | 6 | **Turn/punchline beat** (the reversal) | Varies | Product causes it |
| 9 | 3+ | Product hero plus super; loop frame | Locked-off | Product, callback |

### 5.2 Foot / rooftop chase (20–30 s, 8 shots)
1. HOOK: a door bursts open onto a roof, breathing, wind (handheld, 1.5 s). 2. A wide drone shot of the rooftops, the runner and pursuer, with the gap ahead visible (3 s). 3. A side tracking shot of the run-up (a gimbal operator running, 2 s). 4. **The gap jump**: profile, the full arc, landing into a roll, gravel spits (a static wide, 2.5 s; gap 1.5–3 m, drop 1–2 m). 5. The pursuer's POV stopping at the edge (handheld, 1.5 s). 6. A hanging drop from a parapet onto a fire escape (low angle, 2.5 s). 7. Turn/punchline (6 s). 8. Product hero (3 s+).

### 5.3 BASE / parachute (25–30 s, 8 shots)
1. HOOK: toes on the edge of a 200 m+ tower, the city far below, wind roar (a POV/GoPro look, 1.5 s). 2. A wide of the exit from a neighbouring rooftop: the push off, a stable belly (long lens, 2.5 s). 3. Freefall from the helmet cam: the ground rushing, 2–3 s **real duration**. 4. The pitch: the hand throws the pilot chute (a hard mount on the shoulder, 1 s). 5. The opening: the canopy fills, the body jerks upright, the legs swing (a ground long lens, 2.5 s). 6. Canopy flight: toggles, a turn into the wind (helmet cam up at the canopy, 2 s). 7. Landing: flare at about 3 m, run-out 3 steps, or PLF (a static ground wide, 3 s). 8. Turn/punchline plus product (6–8 s).

### 5.4 Wingsuit (25–30 s, 7 shots)
1. HOOK: a mountain exit; the wind; the suit's wings snap taut (a camera flyer, 1.5 s). 2. Proximity flight along the ridge, 100–150 km/h (a second wingsuiter's helmet cam, 4 s). 3. The flyer's face, the cheeks rippling (a chest mount, 1.5 s). 4. Ground long lens: the flyer crosses the frame (2 s). 5. Pitch plus canopy opening (camera flyer, 3 s). 6. Landing with flare in a meadow (static, 3 s). 7. Punchline plus product (8 s).

### 5.5 Heist (30 s, 9–10 shots)
1. HOOK: the vault door / laser grid / "impossible target", with a sound sting (1.5 s). 2. A blueprint with a finger tracing the plan; Vee's stopwatch starts (insert, 2 s). 3–5. Team member skills, one shot each (2 s each). 6. Execution cross-cut: the stopwatch insert plus the action (3 s). 7. The complication: an alarm, red light, a guard turns (2 s). 8. **Rewind reveal**: replay of a shot from earlier with the missing piece (3 s). 9. Twist payoff with the product (5 s). 10. Product hero plus a callback to the blueprint (3 s).

### 5.6 Deadpan comedy tableau (15–30 s, 6–7 shots)
1. HOOK: an absurd image presented as normal, locked-off and symmetrical (2 s). 2–4. Escalation by **rule of three**: each beat bigger, with the same framing (2–3 s each). 5. The **turn**: a reaction close-up, a held beat of silence (1.5 s, the "dead air" is the laugh). 6. The product reveal *is* the answer (3 s). 7. A tag/callback that rhymes with shot 1 (2 s, loop).

### 5.7 Product sensory one-take (from ch. 35)
Keep the one-take only for pour/sip/spray films. For action: **never**.

---

## 6. Physics cheat-sheet (real numbers)

| Quantity | Number | Source |
|---|---|---|
| g | 9.81 m/s² | — |
| Freefall distance | 1 s 5 m · 2 s 19 m · 3 s 42 m · 4 s 73 m · 5 s 109 m | [calc] |
| Skydiver terminal (belly) | about 195 km/h (range 180–225); head-down 240–290 km/h | [src: Wikipedia, ScienceABC] |
| BASE delay vs height | 60 m: 0–1 s · 150 m: 2–3 s · 275 m: 4–6 s · 460 m: 7–9 s | [src: Apex BASE chart] |
| Lowest BASE technique | under 60 m needs a static line/direct bag, slider off | [src: Wikipedia BASE] |
| Canopy snatch | under 1 s | [src: CSPA/patents] |
| Canopy inflation (slider) | about 1–3 s (BASE), several hundred feet (skydive) | [src: CSPA; craft] |
| Opening shock | 3–7 g typical, up to 12 g extreme | [src: patents/rocket-deploy doc] |
| Ram-air canopy | forward about 30–40 km/h, sink about 4–6 m/s; flare at about 3–4 m | [craft: verify] |
| Wingsuit | glide 2.5–3:1; forward 100–160 km/h; sink 40–65 km/h | [src: Wikipedia, Symscape, JAFM] |
| Fall impact speed | 2 m 23 km/h · 3 m 28 · 5 m 36 · 10 m 50 · 20 m 71 | [calc] |
| Stunt fall limits | boxes ≤ 12 m; airbags ≤ 37 m; 2 spotters over 4.5 m | [src: Ontario guideline 25] |
| Human gap jump | about 3 m untrained with a long run-up; more to a lower roof | [src: Art of Manliness] |
| Car braking (dry, street) | about 0.8 g; 50 km/h → 12 m; 100 km/h → 49 m (+ reaction 1.5 s) | [calc] |
| Car cornering | about 0.9 g; radius 8 m → 30 km/h; 15 m → 41; 30 m → 59; 60 m → 83 | [calc] |
| Handbrake turn entry | about 48 km/h (30 mph) on tarmac | [src: Team O'Neil] |
| PIT max (most US policies) | 35 mph / 56 km/h; some 40–50 | [src: LASD, CHP, ISP] |
| Real chase speeds | French Connection 70–90 mph; Ronin 80–120 mph; Spectre about 110 mph; Baby Driver alley 55–70 mph | [src: §1.1] |
| Usable chase per shoot night | about 4 s (Spectre) | [src: Top Gear] |
| Action ASL | *Fury Road* about 2.7 s overall, faster in action; Bourne inserts under 1 s | [src: NoFilmSchool] |
| FPV drone top speed | about 350 km/h (Red Bull F1 drone), about 3 min flight | [src: Carscoops, T3] |

---

## PART B — COMEDY AND PUNCHLINES FOR 15–30 s ADS

## 7. What the great comedic ads actually do

| Ad | Structure | Reversal type | Product = punchline? | Steal |
|---|---|---|---|---|
| **Old Spice "The Man Your Man Could Smell Like"** (2010, W+K, dir. Tom Kuntz) | A radio-style monologue; each line *visually flips* the scene (shower → boat → horse). 30 s in one take: 3 shoot days, 30+ takes, the usable one in the final 30 min. "I'm on a horse" was borrowed from a rejected script. Goal +15% sales; sales +60% by May, doubled by July [src: Muse by Clio oral history; Wikipedia] | **Rapid scene reversal**, each beat a mini-punchline; **address-the-viewer** | The product appears in the hand and turns into diamonds: the payoff of "smell like" | Many micro-reversals with one confident deadpan performer. Imperfection reads as charm |
| **VW "The Force"** (2011, Deutsch LA) | A kid in a Vader costume fails 3 times (washer, dog, doll) → slumps → tries on the Passat → it starts → cut to the dad with the remote. Pre-released online: 10M+ views before the game [src: Muse by Clio; Ace Metrix] | **Dramatic irony reveal**: the audience learns the hidden cause | **Yes**: remote start IS the joke | Rule of three failures, then a product-caused "success"; no dialogue; one music cue |
| **Snickers "You're not you when you're hungry"** (2010, BBDO; Betty White) | A premise in 1 line: hunger turns you into someone else (Betty White playing football) → a bite → the real person returns. Sales +15.9% global; share up in 56 of 58 markets [src: IPA case; Fortune] | **Identity swap / transformation** | **Yes**: the bite reverses the swap | A repeatable *formula* (a campaign engine) with a recognisable before/after |
| **Dollar Shave Club** (2012, $4,500) | Founder walks through a warehouse, deadpan, scene by scene ("Our blades are F***ing great"); a bear, a machete. 12,000 orders in 48 h [src: Wikipedia; CreativeOS] | **Deadpan escalation**: absurd props presented as business-normal | The value prop (cheap, good) is the spine of every gag | Script rehearsed for 2 weeks; every line is a joke *and* a benefit |
| **Liquid Death** | Absurd ideas played 100% straight ("Murder your thirst", coffins at a conference) [src: Shopify; Self-Storming] | **Tone inversion**: a gentle category sold as metal/lethal | The can's attitude is the joke | Commit to the bit; never wink |
| **Cadbury "Gorilla"** (2007, Juan Cabral) | 90 s of tension (the gorilla waits) → a Phil Collins drum fill → the gorilla drums. Product only in the last seconds. Sales +about 10% [src: Wikipedia; Marketing Week; The Drum] | **Anticipation release**: the long build, the cathartic payoff | Emotion = brand ("glass and a half full of joy") | The hook = "why is a gorilla in a studio?" Hold it until the release |
| **Skittles** ("Taste the Rainbow") | A surreal world treated as commonplace (the man whose touch turns things into Skittles); calm delivery of bizarre events; the slogan slams in [src: Creative Review oral history; Marketing Dive] | **Absurd-normal + tone mismatch** | The product is the cause of the absurd world | Deadpan voice plus a fixed end formula (slogan + colour) |
| **Doritos "Crash the Super Bowl"** (UGC) | *Pug Attack* (2011): the teased pug gets revenge, co-#1 on Ad Meter. *Time Machine* (2014): a kid cons a neighbour with a "time machine" that runs on Doritos [src: Wikipedia; MediaPost; Frito-Lay] | **Role reversal** (prey becomes predator); **the con revealed** | **Yes**: the chips are the motive *and* the fuel | Small domestic conflict + product as the key + a 1-beat reversal |
| **Apple one-takes** (iPhone 11 Pro, 5 h 19 m Hermitage take) [src: Adweek] | Proof-of-capability as the concept | — | The format IS the product claim | Use a one-take only when the one-take itself is the product proof |
| **Squarespace Super Bowl** (Malkovich 2017 Emmy; Scorsese 2024; Keoghan 2025) [src: Squarespace press; MediaPost] | Cinematic celebrity mini-film; the turn is the brand insight | Insight reversal | The product resolves the problem | Cinematic craft plus a simple insight |
| **Kalshi NBA Finals AI ad** (2025, PJ Accetturo, Veo 3, about $2k) | Rapid montage of "crazy people doing crazy things", each a bet; 300–400 generations for 15 usable clips [src: Business Insider; eWeek] | **Montage of absurd micro-scenes** | Each scene is "a market" | AI excels at surreal; it hides imperfections. **Our lesson: surreal is OK, but *physics* must still be right when we claim realism** |

**Market context.** Kantar: humour in ads fell from 53% to 34% (2000–2023) although funny ads are more effective; Cannes added a Humour Lion in 2024. System1: 75% of US/UK Cannes winners used humour in 2024 vs 52% in 2023 [src: Kantar; Research Live]. Humour is under-supplied, which is an opportunity.

## 8. Comedy structures (the toolkit)

### 8.1 Setup / turn / payoff timing for 15 s and 30 s
| Length | Hook | Setup | Turn | Payoff (product) | Tag/loop |
|---|---|---|---|---|---|
| **15 s** | 0–1 s | 1–7 s | 7–9 s | 9–13 s | 13–15 s |
| **30 s** | 0–1 s | 1–15 s (rule of 3 escalation) | 15–20 s | 20–27 s | 27–30 s |

The **turn** must be one clear beat: a cut, a sound stop, a reveal. A held beat of silence (0.5–1 s) before the payoff is where the laugh lives [craft: comic timing; Old Spice, *The Force* both use it].

### 8.2 Why it is funny (theory, applied)
- **Benign violation** (McGraw & Warren): something is *wrong* (a violation) yet *safe* (benign), and both are felt at once. Falling down stairs is funny only if nobody is hurt [src: Humor Research Lab; NPR]. → Our rule "nobody gets hurt" is not just compliance; it is *what makes the action funny*.
- **Incongruity-resolution**: the setup builds expectation A; the turn reveals B; B makes sense in hindsight. → The product must be the "sense" that resolves B.

### 8.3 Reversal types (pick one per ad)
1. **Stakes reversal**: huge build, tiny real stakes (the chase stops at a red light).
2. **Role reversal**: the hunter is the hunted; the cop is the fan (Pug Attack).
3. **Hidden-cause reveal**: the "magic" was the product (*The Force*).
4. **Hidden-plan reveal**: the heist twist ("she wanted to be followed").
5. **Scale reveal**: the epic thing is tiny or vice versa (ch. 35 OTTO-1).
6. **Procedure reversal**: an extreme safety procedure for a trivial act (SOL-4).
7. **Realism-as-joke**: real physics bites back (a shaken can sprays: AURUM-4).
8. **Tone inversion**: a gentle product sold with heavy stakes (Liquid Death).
9. **Identity swap**: you're not you (Snickers).
10. **Time reversal / callback**: the end is the beginning (a loop).

### 8.4 Deadpan rules (Otto's native register)
- Underreact by one level below the absurdity. Otto never laughs, never mugs.
- Hold the frame: a locked-off, symmetrical composition is visual deadpan (Wes-Anderson-like).
- Silence or a single sound effect beats a line. **Otto's mouth is never visible** → he "speaks" through gestures (a raised finger, a slow nod, a viewfinder lift), Vee's stopwatch clicks, cards/supers or VO.
- Absurd = normal: nobody in-world comments on the absurd (Skittles' parallel universe).

### 8.5 The product IS the punchline: tests
1. Remove the product: does the joke still work? If yes, **the concept fails**.
2. Is the payoff a *product attribute* (the fizz, the long-lasting scent, the long burn, the calm flame)? It should be.
3. Is the product *used* (opened, sprayed, lit) in the payoff, not merely shown? (ch. 35 §3.1.)

### 8.6 Callback endings
Plant an object or sound in the first 3 s (the stopwatch click, the siren, the tyre screech); return it transformed in the last 3 s (the siren becomes the can's hiss; the click stops the chase). The callback is what makes the ending feel *designed*.

### 8.7 Loopable endings
- The last frame matches the first in composition or sound [src: Later; loop guides]. Examples: a car leaves frame L→R at the end and enters frame L→R at the start; the stopwatch is reset to 0:00.
- End on a beat that raises the hook question again ("who's at the edge?").
- 15 s loops better than 30 s; make a 15 s cut-down of each concept.

---

## 9. Twelve ready concepts (Otto, Vee; AURUM, VESPER, SOL)

**Cast lock.** **Otto**: a deadpan director with an enormous moustache; **his mouth is never visible**, so there is no lip-sync and he communicates by gesture. **Vee**: a producer with a **silver stopwatch**, which is the clock of every concept. The brands are fictional: **AURUM** sparkling yuzu soda (gold can), **VESPER** perfume ("wear the golden hour"), **SOL** candle (amber vessel, "SOL" debossed).
**Global safety rule:** no guns, no blood, no injuries; police are comedic and nobody is hurt; every stunt is one that a real stunt team could rehearse.

---

### AURUM-1 "Red Light" (30 s): car chase → stakes reversal
**Logline:** a full-blooded getaway chase stops dead and obediently at a red light, and the getaway driver passes a cold AURUM back to the cop behind.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: black frame, then a siren whoop plus a tyre screech; low front 3/4 of a vintage gold coupé launching, rear squat, wheelspin smoke | Static crash cam at ground level |
| 2 | 3 | Drone wide: the coupé L→R down a wet boulevard, 2 police cruisers 50 m behind, lights flashing | Drone, high |
| 3 | 2.5 | Vee in the passenger seat clicks her silver stopwatch; Otto drives (moustache, eyes forward, no mouth visible) | Hard mount on the windshield |
| 4 | 3 | **Turn**: nose dive under braking, a handbrake 90 into a side street, the rear steps out, smoke, a near-miss with a delivery van that brakes | Chase car, bumper height, 1 m behind |
| 5 | 2 | Cruiser 1 brakes hard, nose dives, follows the turn | Static long lens |
| 6 | 3 | A straight; the coupé closes on an intersection; the light turns amber → red | Chase car low, wide lens |
| 7 | 4 | **Reversal**: the coupé stops *perfectly* at the line. The cruiser stops behind it. Silence except the idling engines and a ticking indicator. Held beat. | Drone directly overhead, locked |
| 8 | 5 | Otto's arm out of the window holds a sweating gold AURUM can back toward the cruiser. The officer leans out, takes it, cracks it: a **loud fizz**. | Static side long lens, both cars in frame |
| 9 | 4 | The light turns green. Both cars pull away *slowly*, side by side; the officer sips. Super: **AURUM. Worth stopping for.** Vee clicks the stopwatch. | Drone rising |
**Physics check:** braking from 50 km/h needs about 12 m (visible nose dive) ✓; the handbrake 90 at about 30–40 km/h into a street radius of about 10 m ✓; a closed street with stunt drivers and wet tarmac (*Baby Driver*) ✓; the police only follow, with no contact ✓. **Hook:** siren plus screech at 0 s. **Punchline:** the reversal (the chase obeys a red light) is *caused* by the AURUM handover. **Loop:** the final drone rise matches the opening drone wide.

---

### AURUM-2 "Grandma J-Turn" (20 s): stunt → role reversal
**Logline:** a stunt-driver-grade J-turn in a corner-shop car park; the driver who steps out is a small elderly woman, here for one cold AURUM.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1 | **HOOK**: tyre squeal; a small hatchback reverses fast across an empty lot | Static low wide |
| 2 | 2.5 | The J-turn: wheel snapped, the nose swings 180°, the car drives forward, smoke, and parks perfectly in a bay | Drone 15 m top-down |
| 3 | 1.5 | Insert: a gloved hand on the handbrake; the tyre settles | Hard mount |
| 4 | 2 | The door opens: a tiny grandmother in a cardigan and driving gloves steps out | Static low |
| 5 | 2 | Otto (shopkeeper apron) at the counter slides one AURUM from the cooler | Locked-off symmetrical interior |
| 6 | 3 | She cracks it; **the fizz is louder than the tyres were**; she closes her eyes | Close-up, can + face |
| 7 | 3 | Vee by the window shows the stopwatch to camera: **0:07.4**. Grandma nods: acceptable. | Insert + medium |
| 8 | 5 | She reverses out and does another J-turn away; the can sits in the cupholder, not a drop spilled. Super: **AURUM. Ice-cold. Handle with skill.** | Drone top-down (match shot 2) |
**Physics check:** J-turn from moderate reverse speed in a closed lot is a standard stunt-driving move [src §1.3] ✓; the stunt driver is doubled for the wide shots (the grandma actor only in the static shots) ✓; the can in the cupholder in shot 8 shows level fluid, so no spill at low speed ✓. **Punchline:** the stunt exists *for* the soda; the fizz out-sounds the tyres. **Loop:** the top-down J-turn bookends.

---

### AURUM-3 "Two Openings" (30 s): BASE jump → match-cut sound gag
**Logline:** a real, procedurally perfect BASE jump; the canopy's opening "whump" is answered on the ground by the second-best opening sound in the world: an AURUM.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: toes on the edge of a 250 m tower platform; the city far below; a wind roar | Helmet cam POV |
| 2 | 2.5 | The exit: a push off, a stable belly, arms out | Long lens from a neighbouring roof |
| 3 | 3 | Freefall: the ground rushes **for 3.0 s** (Vee's stopwatch super: 0:03.0) | Helmet cam |
| 4 | 1 | The pitch: the hand throws the pilot chute | Shoulder hard mount |
| 5 | 3 | The opening: a rectangular canopy inflates nose-first, the slider descends, the body jerks upright, legs swing. Sound: a heavy fabric **WHUMP** | Ground long lens |
| 6 | 3 | Canopy flight: toggles, a turn into the wind over a park | Helmet cam looking up + ground wide |
| 7 | 3 | Landing: flare at about 3 m, 3 run-out steps, the canopy collapses behind | Static ground wide |
| 8 | 2 | Otto stands by a cooler, deadpan; lifts one finger: *wait* | Locked-off medium |
| 9 | 4 | He cracks an AURUM: **PSSHH**, the same rhythm as the canopy whump. The jumper, still in harness, takes it. | Close-up can, then a two-shot |
| 10 | 3 | Super: **AURUM. The second-best opening of the day.** Vee stops the stopwatch. | Product hero locked |
**Physics check:** 250 m object → a 2–4 s delay is within chart guidance (275 m: 4–6 s; 150 m: 2–3 s) [src Apex] ✓; freefall in 3 s ≈ 42 m, so 200 m of clearance remains ✓; a ram-air canopy with slider, a 1–3 s inflation, a flare plus run-out ✓; landing in an open park, not on a car ✓. **Hook:** the edge POV. **Punchline:** the product's sound tops the stunt's sound. **Callback:** whump → pssh.

---

### AURUM-4 "Shaken" (25 s): rooftop parkour → realism-as-joke
**Logline:** a parkour courier sprints across rooftops to deliver Otto a cold AURUM on time; physics delivers the punchline.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1 | **HOOK**: Vee's stopwatch click; a roof door bursts open; the courier runs, gold can in hand | Handheld, low |
| 2 | 3 | Drone wide: rooftops, the route visible, a 2 m gap ahead | Drone |
| 3 | 2.5 | The gap jump in profile: a 2.5 m gap, a 1.5 m drop, a landing roll, gravel spits | Static wide |
| 4 | 2 | A hanging drop from a parapet onto a fire escape (hang first, then drop) | Low angle |
| 5 | 2 | A kong vault over an AC unit | Side tracking gimbal |
| 6 | 2 | Arrives on Otto's roof set; Vee shows the stopwatch: **0:59.9**. Made it. | Medium |
| 7 | 3 | Otto takes the can, opens it… **it erupts** all over his moustache. Held deadpan beat; foam drips. | Locked-off two-shot, symmetrical |
| 8 | 4 | The courier, unbothered, unzips an insulated chest pocket and hands over a second, calm can. Otto opens it: a clean, crisp hiss. He sips (under the moustache). | Two-shot → close-up of the can |
| 9 | 3 | Super: **AURUM. Best enjoyed unshaken.** | Product hero |
**Physics check:** a 2.5 m gap with a drop is within trained range [src §2.3] ✓; the hanging drop halves the fall ✓; a carbonated can shaken for a minute *will* spray: the realism *is* the joke ✓; no injuries ✓. **Punchline:** product truth (carbonation). **Loop:** the stopwatch click at both ends.

---

### VESPER-1 "The Tail" (30 s): foot/rooftop chase → hidden-plan reveal
**Logline:** a man pursues a woman across rooftops at golden hour, losing sight of her, then following her VESPER trail. At the end we learn she wanted to be followed.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: a woman in a gold coat glances back over her shoulder at camera, then runs | Handheld close |
| 2 | 3 | Drone: golden-hour rooftops, her ahead, him 20 m behind | Drone |
| 3 | 2.5 | She crosses a 1.5 m gap via a plank / jumps to a lower roof and rolls | Static wide |
| 4 | 2 | He arrives at the edge and loses visual; he stops and *inhales*; a slow head turn left | Close-up, long lens |
| 5 | 2.5 | Insert: a faint golden shimmer in the air (light catching dust, practical haze), the hint of the trail | Macro, backlit haze |
| 6 | 3 | He follows down a fire-escape ladder slide | Low angle |
| 7 | 3 | A dead end: an empty rooftop terrace, a candle-lit table for two; she's gone | Wide symmetrical |
| 8 | 4 | **Reveal**: she steps out behind him, holding the VESPER bottle, and sprays once on her wrist. Vee (as the maître d') clicks the stopwatch and pulls out a chair. | Two-shot |
| 9 | 5 | Super: **VESPER. Leave a trail worth following.** The final frame matches shot 1: her glance over the shoulder. | Close-up product + glance |
**Physics check:** gaps ≤ 1.5 m and a drop to a lower roof ✓; a ladder slide is real parkour vocabulary ✓; "scent visible" is the **one** stylised beat, grounded as haze plus backlight (rule of cool with grounding, §4.1) ✓. **Punchline:** the chase was a date she planned; the scent was the plan. **Loop:** the glance.

---

### VESPER-2 "Inside Woman" (30 s): heist → hidden-plan twist
**Logline:** Otto's crew plans to steal the VESPER bottle from a vault; it goes wrong; the twist: Vee already has it on.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: a laser grid snaps on in a dark vault; the golden bottle glows on a plinth | Locked-off symmetrical |
| 2 | 2.5 | A blueprint; Otto's finger traces the route; Vee starts the stopwatch | Top-down insert |
| 3 | 2 | Crew skill 1: a hacker's hands on a keypad | Insert |
| 4 | 2 | Crew skill 2: an acrobat lowered on a descender wire, slow, controlled | Low angle up the wire |
| 5 | 3 | The acrobat's hand reaches the plinth: **the bottle is gone**. Alarm, red light. | Close-up |
| 6 | 2 | Otto, deadpan, lifts the viewfinder to his eye: a slow turn toward Vee | Medium |
| 7 | 4 | **Rewind reveal**: a replay of shot 2 with the missing frame: Vee's other hand quietly pocketing the bottle earlier | Insert, desaturated replay |
| 8 | 5 | Vee sprays it on her wrist, and **every crew member turns toward her**, the alarm forgotten | Wide, locked |
| 9 | 4 | Stopwatch: **0:30.0**. Super: **VESPER. The only thing worth stealing is the moment.** | Product hero |
**Physics check:** a descender rig moving slowly is a real stunt method ✓; a laser grid is a staged practical effect (haze plus lasers) ✓; there is no violence ✓. **Punchline:** the product was taken *before* the heist began; the scent turns the room. **Callback:** the blueprint frame.

---

### VESPER-3 "Tested at 160 km/h" (30 s): wingsuit → deadpan product claim
**Logline:** a wingsuit flight at full speed, a perfect canopy landing; the partner leans in and smells her collar: still there.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: the click of a VESPER cap at a mountain exit point at sunset; she sprays once; the wind roars | Close-up on the exit ledge |
| 2 | 2 | The exit: the wings snap taut | Camera flyer |
| 3 | 4 | Proximity flight along a ridge at about 150 km/h; super: **160 km/h** | Second wingsuiter helmet cam |
| 4 | 1.5 | Her face, cheeks rippling | Chest mount |
| 5 | 3 | The pitch, the canopy opens, the body swings upright | Camera flyer |
| 6 | 3 | Landing in a meadow: flare, run-out | Static ground |
| 7 | 3 | Otto in a folding director's chair by the landing zone, deadpan; Vee stops the stopwatch: **2:41** | Locked-off wide |
| 8 | 4 | Her partner walks over, hugs her, and leans in to her collar. A small, involuntary smile. | Close-up |
| 9 | 4 | Super: **VESPER. Still there at 160 km/h.** Bottle on the rock at golden hour. | Product hero |
**Physics check:** a mountain exit, a glide of about 2.5:1, 100–160 km/h forward ✓; a canopy deployment and landing ✓; a camera flyer is the real method ✓. **Punchline:** a product attribute (long-lasting) proven by an absurdly physical test, delivered deadpan. **Loop:** the cap click at both ends.

---

### VESPER-4 "Lift" (15 s): deadpan tableau → rule of three
**Logline:** a crowded lift; floor by floor, every passenger slowly turns toward the woman wearing VESPER. At the lobby they all follow her out, leaving Otto alone.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1 | **HOOK**: the lift "ding"; 6 strangers face the doors, all symmetrical; Otto in the middle | Locked-off, inside the lift, wide |
| 2 | 2 | Floor 3: she enters. Faint shimmer. One passenger's head turns. | Same frame |
| 3 | 2 | Floor 2: three heads turned | Same frame |
| 4 | 2 | Floor 1: all heads turned, except Otto, eyes front | Same frame |
| 5 | 3 | Lobby: the doors open, she walks out, and all five follow her. Otto alone. He slowly sniffs his own vest. | Same frame |
| 6 | 3 | Vee steps in, hands him the VESPER bottle, clicks the stopwatch. Doors close. Super: **VESPER. People follow.** | Same frame → insert |
| 7 | 2 | Tag: the doors re-open on the same 6 strangers, now all facing *Otto* (loop) | Same frame |
**Physics check:** a single locked-off set, real extras ✓. **Punchline:** the rule of three escalation → the abandonment → the product resolves Otto's problem. **Loop:** the last frame rhymes with the first.

---

### SOL-1 "Power Cut" (30 s): heist → stakes reversal
**Logline:** a crew cuts a mansion's power to crack a safe; a guard lights a SOL candle; the room becomes so calm that the thieves sit down for dinner.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: a giant breaker lever pulled: CLUNK; the house goes black | Insert, hard light |
| 2 | 2.5 | Drone: a mansion at night, the lights dying window by window | Drone |
| 3 | 2 | Thieves in black ease a window open, Vee with the stopwatch | Exterior, long lens |
| 4 | 3 | Inside, darkness. A match strikes. A guard (Otto, in uniform) lights an amber SOL candle | Close-up, the match as the only light |
| 5 | 3 | Warm light blooms across the room; the thieves freeze mid-step | Wide, candle-lit |
| 6 | 3 | A held beat. Otto slowly gestures to the dining table. | Medium, symmetrical |
| 7 | 5 | A cut to them all seated, napkins on, calm; one thief closes their eyes, breathing in | Wide, candle centre-frame |
| 8 | 4 | The safe swings open on its own in the background (it was never locked); nobody looks | Rack focus |
| 9 | 4 | Super: **SOL. Steal back your evening.** Vee stops the stopwatch. | Product hero |
**Physics check:** a match plus a candle is the only light, so the practical lighting is plausible (a slow bloom, no instant floodlight) ✓; no violence ✓. **Punchline:** stakes reversal: the heist is abandoned for the mood the candle makes. **Callback:** the breaker → the candle as the "power".

---

### SOL-2 "Escort" (30 s): police chase → tactic reversal
**Logline:** police box in a car on the motorway at dusk, a classic rolling roadblock; the reveal shows they're escorting a lit SOL candle on the passenger seat at walking speed.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: blue lights strobe across a driver's face; a siren whoop | In-car hard mount |
| 2 | 3 | Helicopter-style wide: 4 cruisers surround one sedan, the box tightening | Drone high, searchlight look |
| 3 | 2.5 | An officer's grim face, a hand on the radio | Hard mount, cruiser interior |
| 4 | 2 | Driver (Otto), eyes forward, both hands on the wheel at 10 and 2 | Windshield mount |
| 5 | 3 | **Reveal 1**: speedometer insert: **18 km/h** | Insert |
| 6 | 3 | **Reveal 2**: the passenger seat: a lit SOL candle in a cupholder, the flame perfectly still | Close-up |
| 7 | 4 | The procession passes a cyclist who overtakes them | Static side, long lens |
| 8 | 5 | They arrive at a house; the convoy stops in formation; Vee opens the door, lifts the candle out, flame intact, clicks the stopwatch | Wide |
| 9 | 4 | Super: **SOL. A flame worth protecting.** | Product hero |
**Physics check:** boxing-in is a real low-speed procedure [src §1.4] ✓; a flame in a closed car at 18 km/h with smooth inputs stays upright ✓; nobody is in danger ✓. **Punchline:** a procedure reversal (an arrest formation becomes an honour guard), centred on the product. **Loop:** the blue lights on the face at both ends.

---

### SOL-3 "45 Hours" (15 s): deadpan time-lapse → callback
**Logline:** Vee starts her stopwatch as Otto lights a SOL candle. They both just… wait. For the full burn time.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1 | **HOOK**: the stopwatch click plus a match strike in one sound | Insert |
| 2 | 2 | Otto lights the candle; Vee sits beside him; a symmetrical locked-off couch shot | Locked-off |
| 3 | 4 | Time-lapse: day/night cycles through the window; mail piles up; a plant grows; Otto's moustache gets even longer; they don't move | Same frame, time-lapse |
| 4 | 2 | Stopwatch insert: **44:59:58 → 45:00:00** | Insert |
| 5 | 3 | The flame goes out gently on the last of the wax. A held beat. Otto slowly reaches for… a second SOL. | Same frame |
| 6 | 3 | Super: **SOL. 45 hours. Plan accordingly.** Vee resets the stopwatch to 0: loop | Product hero |
**Physics check:** a time-lapse on a locked frame is a standard practical technique ✓ (the burn-time claim must match the real product spec before release). **Punchline:** the product attribute is the joke. **Loop:** the reset click.

---

### SOL-4 "The Stunt" (25 s): film-set procedure reversal
**Logline:** Otto's crew prepares the most dangerous stunt on set: full safety briefing, airbag, spotters, wind check, countdown… the stunt is lighting a SOL candle.
| # | s | Shot | Rig |
|---|---|---|---|
| 1 | 1.5 | **HOOK**: a stunt coordinator shouts "SAFETIES!"; crew run in; a giant airbag inflates | Handheld, wide |
| 2 | 2 | Two spotters take their positions; a medic stands by | Medium |
| 3 | 2 | An anemometer insert: **wind 3 km/h. GO.** | Insert |
| 4 | 2 | Vee lifts the stopwatch; countdown fingers 3–2–1 | Close-up |
| 5 | 2.5 | Otto lifts a single long match with extreme ceremony | Low hero angle |
| 6 | 3 | He lights the SOL candle. The flame blooms calmly. | Macro |
| 7 | 3 | A held beat… the crew erupts into applause; the coordinator wipes away a tear | Wide |
| 8 | 3 | Otto nods once, deadpan; the airbag slowly deflates in the background | Medium, symmetrical |
| 9 | 4 | Super: **SOL. The calmest thing on any set.** Vee stops the stopwatch: **0:00.8** | Product hero |
**Physics check:** all real safety vocabulary (airbag, spotters, wind check per §2.5) in a static set ✓. **Punchline:** procedure reversal; the product's calm is the contrast. **Loop:** the "SAFETIES!" call could reopen.

---

## 10. Pre-generation QA gate (all must be YES)

1. Is there a **hook in second 1**: a sound or image that poses a question?
2. Does each shot name **one real rig**?
3. Physics: are fall times, gaps, speeds, turns and canopy procedure within the cheat-sheet?
4. Does every **cause have its effect** in the next shot (braking → nose dive; landing → surface reaction)?
5. Is there **at most one** stylised/impossible beat, and is it planted earlier?
6. Is the **turn a single clear beat** (a cut, a sound stop, a reveal)?
7. Is the **product the cause of the punchline** (remove-it test, §8.5)?
8. Is the product **used**, not just shown?
9. Does the **last frame rhyme with the first** (loop or callback)?
10. Is Otto's **mouth never visible**? Is there **no violence**, and is nobody hurt?
11. Is a 15 s cut-down possible (hook + turn + payoff)?
12. Is the continuity sheet locked (cars, dents, wardrobe, time of day)?

---

## 11. Sources

**Car chases**
- Bullitt: https://en.wikipedia.org/wiki/Bill_Hickman · https://www.jalopnik.com/the-secret-of-steve-mcqueens-bullitt-chase-scene-5744523/ · https://hagerty.co.uk/articles/50-years-of-bullitt/ · https://www.imdb.com/title/tt0062765/goofs · https://www.drivencarguide.co.nz/news/car-vid-classics-bullitt-car-chase-and-the-worlds-most-famous-hubcaps/
- The French Connection: https://lantern.mediahist.org/catalog/take-one-1971-07_0027 · https://hagerty.com/media/?p=4281 · https://www.theautopian.com/gene-hackman-costarred-with-a-pontiac-to-create-one-of-the-most-iconic-reckless-and-dangerous-chase-scenes-ever-filmed/ · https://www.imdb.com/title/tt0067116/trivia
- Ronin: https://www.hagerty.co.uk/articles/how-ronin-out-drove-other-action-films/ · https://www.drivencarguide.co.nz/news/car-vid-classics-the-car-chases-of-ronin/ · https://www.carmagazine.co.uk/features/opinion/graham-king/ronin-25th-anniversary/
- Baby Driver: https://www.hollywoodreporter.com/behind-screen/baby-driver-stunt-coordinator-we-tried-do-everything-camera-1017348 · https://hagerty.co.uk/articles/automotive-history/films/2017s-baby-driver-was-an-instant-classic-car-chase-movie · https://www.cbc.ca/radio/day6/episode-345-north-korea-s-top-anchor-returns-baby-driver-s-best-stunts-finding-amelia-earhart-and-more-1.4192751/meet-the-stunt-driver-behind-baby-driver-s-crazy-car-chases-1.4192792
- Bourne Supremacy: https://nofilmschool.com/bourne-supremacy-shaky-cam · https://hagerty.com/media/?p=4449 · https://www.denofgeek.com/movies/crossing-the-line-movie-car-chases-the-bourne-supremacy
- Mad Max: Fury Road: https://vashivisuals.com/?p=5288 · https://www.eugenewei.com/blog/2015/5/31/creating-order-out-of-the-chaos-of-mad-max-fury-road · https://nofilmschool.com/2015/05/how-framing-mad-max-fury-road-keep-viewer-oriented-world-gone-mad · https://www.newsshooter.com/2015/06/05/filming-mad-max-fury-road-with-dp-john-seale-acs-asc-and-2nd-unit-cinematographer-david-burr-acs/
- Spectre / Fast & Furious: https://www.topgear.com/car-news/behind-scenes/bond-special-behind-scenes-spectres-big-rome-car-chase · https://www.noln.net/articles/750-keeping-it-real-how-they-filmed-the-spectre-car-chase · https://blogs.library.american.edu/mediaservices/2015/04/05/for-real-furious-7-carries-the-torch-for-practical-effects-in-movies · https://movieweb.com/furious-franchise-mad-max/
- Rigs: https://morphic.com/ai-glossary/camera-car · https://www.carscoops.com/?p=2953260 · https://t3.com/news/can-a-drone-keep-up-with-an-f1-car-this-one-can
- Driving technique: https://en.wikipedia.org/wiki/Handbrake_turn · https://teamoneil.com/blog/how-to-do-a-forward-180-with-a-car/ · https://www.foxnews.com/auto/drive-like-valerie-plame.amp
- Police: https://pars.lasd.org/Viewer/Manuals/13233/Content/20719 · https://www.cabq.gov/police/documents/2-12-pursuit-intervention-technique-pit-p-p-draft-07-13-22.pdf · https://typeinvestigations.org/investigation/2016/02/11/fast-precise-deadly/ · https://theintercept.com/2016/02/11/pit-maneuver-how-police-use-anti-terrorism-tactic-to-end-pursuits/ · https://ohioattorneygeneral.gov/Files/Briefing-Room/News-Releases/Policy-and-Legislation/Vehicular-Pursuit/CORSA-Vehicular-Pursuit-Model-Policy.aspx · https://police.illinoisstate.edu/downloads/transparency/305VehiclePursuits.pdf · https://policeandsecuritynews.com/2019/01/15/the-wheels-of-justice-january-february-2019/

**Stunts and physics**
- BASE: https://apexbase.com/wp-content/uploads/2018/08/pilot-chute-reference-chart-8-2017.pdf · https://base-book.com/BASEFreefallChart · https://blogs.bmj.com/bjsm/2008/09/12/the-thickness-of-air-parachuting-from-fixed-objects/ · https://en.wikipedia.org/wiki/BASE_jumping · https://www.skydivemag.com/new?p=42587 · https://en.wikipedia.org/wiki/Slider_(parachuting)
- Canopy opening and landing: https://www.cspa.ca/sites/default/files/Equipment%20-%20Hard%20Openings%20in%20Skydiving.pdf · https://patents.google.com/patent/US7584927 · https://www.uspa.org/the-canopy-task-force-presents-stay-alive-practice-five · https://www.uspa.org/skydiveschool/F · https://www.uspa.org/case-studies-canopy-flight-emergency-procedures
- Wingsuit / terminal velocity: https://en.wikipedia.org/wiki/Wingsuit_flying · https://www.symscape.com/blog/skydiving-without-a-parachute · https://www.jafmonline.net/article_2307_fcf4c420950f2b8f7638cd6ce8f7e671.pdf · https://www.scienceabc.com/pure-sciences/can-you-fly-like-the-dark-knight-proximity-flying.html
- High falls: https://www.ontario.ca/document/safety-guidelines-film-and-television-industry/guideline-no-25-high-fall · https://actsafe.ca/wp-content/uploads/2022/09/Air-Bags-Motion-Picture-Bulletin-PDF.pdf · https://thereactionlab.com/blog/descenders-in-the-spotlight-how-stunt-performers-are-achieving-greater-heights-safely
- Rooftops: https://www.pressreader.com/australia/total-film/20200501/283815740771460 · https://fromtailorswithlove.co.uk/min-15-the-crane-fight-200-feet-in-the-air · https://www.artofmanliness.com/articles/how-to-jump-from-rooftop-to-rooftop
- Mission: Impossible: https://www.cbsnews.com/news/tom-cruise-most-dangerous-stunt-riding-motorcycle-off-cliff-base-jumping-mission-impossible-dead-reckoning-film-sky-diving · https://slashfilm.com/1144219/tom-cruise-did-13000-practice-runs-to-prepare-for-mission-impossible-7s-motorcycle-jump
- Fake-looking physics: https://physicsworld.com/a/vfx-in-movies-from-weightlessness-to%e2%80%afcurly-hair/ · https://filmstories.co.uk/features/weve-had-over-20-years-of-weightless-boring-action-scenes-now-i-cant-be-the-only-one-whos-sick-of-it/

**Heist and plausibility**
- https://industrialscripts.com/write-a-heist-movie/ · https://www.npr.org/transcripts/nx-s1-5276937 · https://seoulbeats.com/2021/06/monsta-x-pulls-off-a-slick-heist-as-gamblers/
- https://tvtropes.org/pmwiki/pmwiki.php/Main/RuleOfCool · https://www.finaldraft.com/blog/how-to-create-the-suspension-of-disbelief-in-your-screenplay · https://blog.celtx.com/suspension-of-disbelief-screenwriting/

**Comedy ads**
- Old Spice: https://musebyclios.com/advertising/behind-the-towel-an-oral-history-of-the-legendary-old-spice-ad/ · https://en.wikipedia.org/wiki/The_Man_Your_Man_Could_Smell_Like · https://consumerist.com/2010/07/02/how-did-they-make-that-old-spice-commercial · https://www.creativereview.co.uk/an-oral-history-of-the-old-spice-ads/
- VW The Force: https://musebyclios.com/sports/how-volkswagens-the-force-changed-the-super-bowl-forever/ · https://www.acemetrix.com/about-us/company-news/press-releases/volkswagens-the-force-ad-is-the-most-effective-automotive-super-bowl-ad/
- Snickers: https://ipa.co.uk/knowledge/case-studies/snickers-you-re-not-you-when-you-re-hungry/ · https://fortune.com/2025/09/30/why-snickers-advertising-campaign-hungry-so-successful · https://www.warc.com/content/article/snickers-youre-not-you-when-youre-hungry/127492
- Dollar Shave Club: https://en.wikipedia.org/wiki/Dollar_Shave_Club · https://creativeos.beehiiv.com/p/145-how-a-4-500-video-changed-dtc-marketing-forever-dollar-shave-club-part-1
- Liquid Death: https://www.shopify.com/blog/liquid-death-comedy-marketing-billion-dollar-brand · https://www.selfstorming.com/tools/libraries/campaigns/deadliest-stuff-on-earth · https://lbbonline.com/news/Liquid-death-andy-pearson-strategy-killing-industry
- Cadbury Gorilla: https://en.wikipedia.org/wiki/Gorilla_(advertisement) · https://www.marketingweek.com/cadbury-gorilla/ · https://www.thedrum.com/news/2022/06/14/world-s-best-ads-ever-14-the-cadbury-drumming-gorilla-almost-never-aired
- Skittles: https://www.creativereview.co.uk/an-oral-history-of-skittles-taste-the-rainbow/ · https://www.marketingdive.com/news/campaign-trail-skittles-stays-surreal-for-uncomfortably-soft-gummies/820683/ · https://musebyclios.com/advertising/skittles-blank-the-rainbow-the-dark-art-of-a-magical-campaign/
- Doritos: https://en.wikipedia.org/wiki/Crash_the_Super_Bowl · https://fritolay.com/news/doritos-announces-winner-of-1-million-grand-prize-in-global-advertising-contest · https://www.pepsico.com/newsroom/press-releases/2011/pepsicos-doritos-and-pepsi-max-brands-dominate-usa-today-ad-meter-with-consumer-created-super-bowl-commercials-awarding-14-million-in-prizes
- Apple / Squarespace: https://www.adweek.com/?p=1131140 · https://www.squarespace.com/press-coverage/2017/9/12/squarespaces-super-bowl-ad-starring-john-malkovich-wins-best-ad-emmy · https://www.mediapost.com/publications/article/393322/site-specific-scorsese-directs-first-super-bowl-s.html
- AI ads: https://www.businessinsider.nl/the-chaotic-kalshi-ad-during-the-nba-finals-was-made-with-ai-for-2000-the-guy-behind-the-clip-shared-how-he-made-it/ · https://www.eweek.com/news/ai-ad-kalshi-nba-finals/
- Humour research: https://humorcode.com/about · https://www.npr.org/sections/13.7/2016/04/25/475622815/hey-what-are-you-laughing-at · https://www.kantar.com/inspiration/advertising-media/time-to-get-serious-about-humour-in-advertising · https://www.research-live.com/article/news/system1-analysis-finds-increased-humour-in-uk-and-us-cannes-lions-winners/id/5127523
- Loops: https://later.com/social-media-glossary/loop/ · https://socialk.it/en/blog/tiktok-retention-watch-time-guide

**Transcripts:** the yt-dlp auto-sub pulls were attempted and blocked by YouTube bot-checks from this environment (no transcripts obtained). Re-run on a residential connection with `yt-dlp --skip-download --write-auto-subs --sub-langs en` for: Vashi Nedomansky's *Fury Road* centre-framing video, Every Frame a Painting-style chase breakdowns, and *Baby Driver* / *Ronin* BTS featurettes, then append the quotes here.
