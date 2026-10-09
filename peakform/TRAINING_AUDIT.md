# Training audit, PeakForm 3.0.0

Reviewed 6 October 2026. This audit covers the training plan as implemented in version 2.1.1, what the evidence says about it, and what changed in 3.0.0. It uses no personal data: the athlete is described only as a teenage volleyball and basketball player who trains at a gym and at home. Health details, measurements, and answers stay on the phone.

Sources were reached through web search results only. Every primary site tried (AAP, BMJ, PubMed Central, Springer, Frontiers, and others) blocked direct page access from the build environment, so no full text was read. Each source in `src/content/sources.ts` records its access level, and RESEARCH.md lists them with their uncertainty.

## 1. What was inspected

- `src/content/plan.ts`, `program.ts`, `phases.ts`, the exercise library (99 exercises), `src/domain/progression.ts`, `fourExposure.ts`, `safety.ts`, `review.ts`, `coverage.ts`, and the plan update service.
- The installed plan shape: plan versions in IndexedDB, session snapshots, the KV store, and the automatic block sync.
- None of the older planning files named in the brief (`.badger`, `easy_reps_v8_ai_import_master.txt`, the Hebrew plan files, the nutrition PDF) exist on this machine. The original Google Doc specification was read through the Google Drive connector.

## 2. The 2.1.1 prescription and what was wrong with it

| Area | 2.1.1 as implemented | Problem | Evidence |
| --- | --- | --- | --- |
| Gym frequency | Six gym days, Sunday to Friday | Above the two to three sessions a week in youth guidance, with no added muscle at equal weekly volume, and little room for school sport and recovery. | AAP 2020; 2014 International Consensus; NSCA 2009; Schoenfeld 2019; Pelland 2026; Saric 2019 |
| Early mornings | A home session at 05:30 every school day, starting with 6 to 15 minutes of rope | Cut into the 8 to 10 hours teenagers need. Rope at that length adds hundreds of foot contacts a day that were never counted. | AASM 2016; Milewski 2014; Gudmundsdottir 2020 |
| Failure | Small machine and cable exercises to failure on every set, compounds on the last set | Routine failure adds little or no growth over 1 to 3 reps in reserve and slows recovery by up to two days. Youth guidance does not prescribe it. | Grgic 2022; Refalo 2023, 2024; Robinson 2024; Moran-Navarro 2017 |
| Jumps | Jump drills inside the Monday and Friday gym sessions, about 50 to 100 contacts, with depth jumps later | The athlete asked for jumps at home. Depth jumps and high contact counts were planned by date, not by readiness, and school jumping was not counted. | Bedoya 2015; Ramirez-Campillo 2023; Jayanthi 2015 |
| Dunk deadline | Dated training blocks to the end of January with a dunk target height | A deadline built from a rim touch description, not a measurement. Plans changed automatically when a block date arrived, without showing the difference first. | Brief, sections 4 and 17 |
| Wrist | No way to record a wrist injury | Heavy grip, dumbbell pressing, ball contact, and wrist curls were planned whatever the state of the wrist. | Bhanushali 2023; clinical leaflets |
| Swims | Two easy swims a week | Extra shoulder volume on top of pressing, pulling, and spiking, with no recorded reason to keep it. | Andersson 2017 (shoulder load) |

## 3. Decisions

| Decision | Source | Population | Finding | Applicability | Uncertainty | Implementation |
| --- | --- | --- | --- | --- | --- | --- |
| Four gym days instead of six | AAP 2020, Lloyd 2014, Schoenfeld 2019, Pelland 2026, Saric 2019 | Youth guidance; adult trials | Youth statements describe 2 to 3 sessions a week. At equal weekly volume, more days did not add muscle | Guidance applies directly; muscle data are adult | No adolescent trial compares 6 with 4 days | Upper A Sunday, Lower A Monday, Upper B Wednesday, Lower B Thursday. Every muscle twice a week. The athlete may still choose differently with a coach |
| Two reps in reserve | Grgic 2022, Refalo 2023, Robinson 2024 | Adults | Failure gives a trivial or no advantage for growth and costs recovery | Adult data | Teens may misjudge reps in reserve | `rirShort` 2 on every slot, 3 for shoulder care and for the first two sessions of a new exercise. No `lastSetRir` 0 anywhere |
| Jumps at home, twice a week, 72 hours apart | Bedoya 2015, Ramirez-Campillo 2023, Chen 2023 | Youth athletes | Two sessions a week with 48 to 72 hours between them; the same weekly volume spread over more days did not add gains | Direct | No universal safe contact limit exists | Monday and Thursday at home before the gym legs, about 60 landings to start. Friday is a light skill session with no jumps |
| No daily mandatory jumps | Same | Youth | Not supported by trials | Direct | Unresolved for very low intensity | The athlete's earlier wish for daily jumps is not followed. Days off stay off |
| No early mornings | AASM 2016, Milewski 2014, Gudmundsdottir 2020 | Adolescents | 8 to 10 hours needed; early sessions shorten sleep; under 8 hours went with more injuries | Direct, observational | Association, not proof | Default check in 07:00, wind down 21:30. Old 05:15 and 05:25 reminders move or switch off only if still at their defaults |
| Count school sport | Jayanthi 2015, Brenner 2024 | Youth athletes | More weekly hours than the athlete's age went with serious overuse injury; 1 to 2 days a week off | Direct, case control | A prompt, not a threshold | Sport log and usual week. The review adds sport to plan minutes and raises a recovery concern above age in hours |
| Wrist gate | Bhanushali 2023 and clinical leaflets | Children with forearm fractures | Return depends on fracture type and healing | Direct when an injury is recorded | The app cannot know the injury type | Every exercise has a wrist load rating. Unknown or not cleared: high load exercises are swapped and loads on moderate ones stay the same. Symptoms: only none or low |
| Home space gate | Practical judgement; surface and space guidance | n/a | Jumps need room, a safe floor, and a high enough ceiling | Judgement | Each home differs | Every home drill states its space, ceiling, impact, and noise. Unknown answers mean the smallest, quietest room. Drills that do not fit are swapped for footwork or left out |
| No dunk deadline | Brief | n/a | A rim touch description is not a measurement | n/a | n/a | Dated blocks removed. Jump and reach tests every four weeks, compared only under the same conditions |
| Soreness is not pain | Schoenfeld 2013, DOMS literature | Adults mostly | Soreness is a poor sign of growth; joint, tendon, heel, knee, and wrist pain are different | Mostly adult | Teens probably similar | Check in explains it; pain of 4 or more, worsening pain, or pain that changes technique pauses the exercise |
| No automatic changes | Brief | n/a | n/a | n/a | n/a | Every plan change is a proposal with a summary and a day by day difference. The automatic block sync was removed |

## 4. The selected week

| Day | Home | Gym |
| --- | --- | --- |
| Sunday | None | Upper A, about 70 minutes |
| Monday | Movement prep, landings, jumps, and full approach jumps, about 35 minutes at the starting level (about 45 at the build level), before the gym | Lower A, about 40 minutes |
| Tuesday | None | None. School sport counts |
| Wednesday | None | Upper B, about 70 to 75 minutes |
| Thursday | Movement prep, landings, jumps, and full approach jumps, about 35 minutes at the starting level (about 45 at the build level), before the gym | Lower B, about 50 minutes |
| Friday | Volleyball skills without jumps, about 20 minutes | None |
| Saturday | Rest and Sabbath | Rest |

Durations are estimates from the plan itself: about 3 seconds a repetition, the prescribed rest after every set (only the last rest of the session is left out), a short switch between sides, about a minute to change exercises at the gym and half a minute at home, and 5 minutes of warm up at the gym. Jump work needs full rest, so most of a home session is rest. Until the home space is described, the home session is only the 10 minute movement prep and a tibialis exercise, about 15 minutes. On Monday and Thursday the home and gym sessions together come to about 75 to 85 minutes at the starting level and about 85 to 95 minutes at the build level; that is the main cost of the build level and a reason to stay at the starting level on busy weeks.

Default times: home sessions at 16:15 on Monday and Thursday, about an hour after the 15:20 afternoon meal; gym at 17:00 on those days and 16:30 on Sunday and Wednesday; Friday skills at 13:30. All times are editable. If the home jumps are set after the gym, the day shows a note that jumps go first.

### Gym sessions

| Day | Slot | Default exercise | Sets × reps | Reps in reserve | Rest | Wrist load |
| --- | --- | --- | --- | --- | --- | --- |
| Upper A | Shoulder care | Cable external rotation | 2 × 15 to 20 | 3 | 45 s | Low |
| | Middle chest | Machine bench press | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Lats | Wide grip pulldown | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Upper chest | Incline machine press | 2 × 8 to 12 | 2 | 150 s | Moderate |
| | Row | Chest supported dumbbell row | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Side shoulder | Single arm cable lateral raise | 3 × 12 to 20 | 2 | 90 s | Low |
| | Biceps, long head | Incline dumbbell curl | 2 × 10 to 15 | 2 | 90 s | Moderate |
| | Triceps, long head | Rope overhead extension while the wrist is not cleared, otherwise the athlete's dumbbell choice | 2 × 10 to 15 | 2 | 90 s | Moderate or high |
| Lower A | Quads | Leg press | 3 × 6 to 10 | 2 | 180 s | None |
| | Hinge | Dumbbell Romanian deadlift | 3 × 8 to 10 | 2 | 150 s | Moderate |
| | Hamstrings | Seated leg curl | 2 × 10 to 15 | 2 | 90 s | None |
| | Calves | Leg press calf raise | 2 × 10 to 15 | 2 | 90 s | None |
| | Abs | Cable crunch | 2 × 10 to 15 | 2 | 75 s | Low |
| Upper B | Shoulder care | Second choice | 2 × 15 to 20 | 3 | 45 s | Low |
| | Upper chest | Incline machine press | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Row | Seated cable row | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Lats | One arm pulldown | 3 × 8 to 12 | 2 | 150 s | Moderate |
| | Chest fly | Pec deck | 2 × 10 to 15 | 2 | 90 s | Low |
| | Rear shoulder | Reverse machine fly | 3 × 12 to 20 | 2 | 90 s | Low |
| | Side shoulder | Machine lateral raise | 2 × 12 to 20 | 2 | 90 s | Low |
| | Biceps, short head | Machine preacher curl | 2 × 10 to 15 | 2 | 90 s | Moderate |
| | Triceps, outer heads | Pushdown | 2 × 10 to 15 | 2 | 90 s | Moderate |
| Lower B | Glutes | Bulgarian split squat | 3 × 8 to 10 each leg | 2 | 150 s | Moderate |
| | Rectus femoris | Leg extension | 2 × 10 to 15 | 2 | 90 s | None |
| | Hamstrings | Seated leg curl | 2 × 10 to 15 | 2 | 90 s | None |
| | Side of hip | Hip abduction machine | 2 × 12 to 20 | 2 | 75 s | None |
| | Inner thigh | Copenhagen plank | 2 × 25 s each side | n/a | 75 s | Low |
| | Calves | Second choice | 2 × 10 to 15 | 2 | 90 s | None |
| | Obliques | Cable woodchop | 2 × 10 to 15 | 2 | 60 s | Low |

Weekly direct sets (primary muscle = 1 set, secondary = half, counted separately): lats 12, middle traps and rhomboids 6, each chest head 5 (10 for the chest), side shoulders 5, rear shoulders 3 plus rows, biceps 4 and triceps 4 plus pressing and pulling, quads 8, hamstrings 7, glutes 9, calves 4 plus the jumps, rotator cuff 4. These are below the 2.0 plan for the arms and shoulders on purpose: the plan starts in a technique and workload stage, and the review can add a set where recovery allows. The fractional set weights are bookkeeping, not biology.

The exercise questionnaire still decides which exercise fills each slot. Slots outside the four days (straight arm pulldown, shrugs, wrist curls, the brachialis curl) keep their saved choices for later and are not asked about.

### Home sessions

Starting level, about 64 landings when the space allows everything:

| Drill | Sets × reps | Rest | Needs | Quiet or no jump fallback |
| --- | --- | --- | --- | --- |
| Home movement prep, with landing, balance, and trunk control (10 minutes since 3.1.0) | 10 minutes | n/a | 2 × 2 m, any ceiling, no impact | n/a |
| Snap down and stick | 2 × 4 | 60 s | 2 × 2 m, standard ceiling, safe floor | Block footwork |
| Pogo hop | 2 × 10 | 60 s | 2 × 2 m, standard ceiling, safe floor, some noise | Tibialis raise, 2 × 15 |
| Lateral line hop | 2 × 8 | 60 s | 1.5 × 1.5 m and any line on the floor (tape, rope, a floor seam, or two socks; no equipment needed since 3.1.1) | Shadow pass footwork, only when noise limits or the floor rule out hops |
| Countermovement jump to stick | 2 × 4 | 90 s | High ceiling, so outdoors or a hall | Spike arm swing, no ball |
| Standing broad jump | 2 × 3 | 90 s | 5 m of space | Block footwork |
| Approach footwork, no jump | 3 × 3 | 45 s | 5 m of space | Spike arm swing, no ball |
| Approach jump and reach (3.0.1) | 2 × 3, full effort | 120 s | A 4 to 6 m run up and open sky or a hall; a marked wall for the touch height, otherwise a volleyball approach jump reaching into the air | Left out: the approach footwork above already covers the rhythm |

The next level adds sets (about 94 landings, with pogo hops back to two sets to make room for a third set of approach jumps) and single leg hops. It is offered only through a checklist (four weeks at the starting level, no knee, heel, shin, or back pain for two weeks, good landings, school jumping known, sleep mostly 8 hours) and becomes a plan proposal the athlete activates. It never happens automatically.

Friday skills: movement prep, approach footwork, spike arm swing without a ball, and controlled wall spikes at half effort only with a cleared wrist, a solid outdoor wall, and no people or breakable things nearby, otherwise block footwork. No jumps.

## 5. Gates and stop rules

- **Wrist.** Unknown or not cleared: high wrist load exercises are swapped for an equivalent slot option (for example the dumbbell overhead triceps extension becomes the rope version), loads on moderate exercises stay the same while reps may rise (`wristGate` in `progression.ts`), and there is no ball contact. With symptoms, only none and low wrist load exercises remain.
- **Space.** `chooseDrill` in `src/domain/homeSpace.ts` picks the first drill whose space, ceiling, floor, noise, ball, and equipment needs fit indoors or outdoors, and records why others were passed over. The note on the drill says what it replaced and why.
- **Pain.** Pain of 4 or more, pain that worsens, or pain that changes technique pauses the exercise and blocks progression. Joint, tendon, heel, below the kneecap, and wrist pain are listed apart from muscle soreness.
- **School sport.** A lot of jumping at sport the day before or on a home jump day shows a note to keep the home jumps short. More weekly hours than the athlete's age (when the birth year is set) becomes a recovery concern in the review.
- **Every session** shows its location, equipment, space, estimated duration, and stop rules (`src/domain/sessionInfo.ts`).

## 6. Progression

Unchanged double progression: reps rise within the range first, and load rises only when every work set reaches the top of the range at the planned reps in reserve with good form and no pain. One qualifying set never increases load. The smallest equipment step is used. Jumps, sprints, and skills never progress volume from completion. The four exposure review still runs. New: while the wrist is not cleared, an "add load" suggestion on a gripping or pressing exercise becomes "same load".

## 7. Four month planning

Flexible stages counted from the plan start, in `src/content/phases.ts`: technique and workload check (weeks 1 to 3), gradual progression (4 to 9), consolidation and skill (10 to 15), review and the next block (16 to 18). Each has process goals and review checks. Stages never change the plan by themselves. Jump and reach measurements are suggested every four weeks.

## 8. What remains uncertain

- No adolescent study compares six with four strength days at equal volume. The choice rests on youth guidance and adult volume data.
- The app cannot know the type of a wrist injury. The gate is deliberately cautious while the answer is unknown or not cleared, and lifts when a clinician's clearance (or no injury) is recorded.
- School volleyball and basketball load is unknown until it is entered.
- The home space is unknown until it is entered, so a fresh plan uses quiet drills without jumps.
- Weekly set numbers are lower than the previous plan for the arms and shoulders. Whether to add sets is a question for the review after the first stage, with a coach if possible.
- No study can say how much one person will gain. Adolescent plyometric meta-analyses average about 2 to 3 cm in countermovement jump, with wide variation.

## 3.1.0: changes from the jump and body composition review

A second review (2026-10-09, search snippets and abstracts only, no full texts) asked how a growing teenage volleyball and basketball player can raise jump height over four months. It found that the plan's structure already fits the evidence: around the growth spurt, strength training responds strongly and plyometrics only modestly, two jump sessions a week are enough, sessions of 16 or more beat shorter programmes, and no study supports daily jumps or training to failure. In that review, the realistic best case for approach touch height over four months was roughly 8 to 15 cm, an estimate built from training, technique, and growth together. Changes:

| Change | Evidence | Population |
| --- | --- | --- |
| Jump only while knee, heel, shin, or Achilles pain stays at 2 out of 10 or less during the session and the next morning; above that, Today and the Train day say to skip the jumps that day | Rathleff 2020, the one loading protocol built for adolescents (Osgood-Schlatter) | Ages 10 to 14, no control group |
| A night under 8 hours before a home jump day: advice to do one set of each jump drill | Milewski 2014; sleep and injury meta-analysis | Adolescents, observational |
| Home warm up 10 minutes, adding side plank, single leg balance, and drop and freeze landings | Rössler 2014 (injuries about halved), adolescent team sport meta-analysis (IRR 0.65) | Youth athletes |
| In a week with many games, cut the home jump session first | Visnes and Bahr 2013 (risk per extra match set), Bahr 2014 jump counts | Elite youth volleyball, 16 to 18 |
| Push the lifting phase with full intent to move fast, still at the planned reps in reserve | Velocity and power training research, mostly adult | Adults, extrapolated |
| Film one set of approach jumps from the side every second week | Approach technique and arm swing hold the cheapest centimetres; no technique training trial in cm was found | Adults and youth, inference |
| Safety page: signs that need a doctor without waiting (a knee that will not straighten, night pain, fever with a swollen knee, not bearing weight) | Clinical patient information | General |

Not changed: four gym days, two home jump days with 72 hours between them, the jump volume, and the approach jumps. Heavy, slow or isometric knee and calf work for the tendons was suggested by adult evidence; the gym already includes the leg press, leg extension, and calf raises with controlled lowering, so no exercise was added.
