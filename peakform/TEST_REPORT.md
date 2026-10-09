# PeakForm test report

Date: 2026-10-09. Build 3.1.0.

Everything below ran in the build environment: Linux, Node 22, Chromium with iPhone emulation. Nothing was tested on a real iPhone, and no clinician, dietitian, or coach reviewed the plan.

## Summary

| Check | Result |
| --- | --- |
| TypeScript strict (`tsc -b`) | Pass, no errors |
| ESLint (`eslint .`) | Pass, no errors or warnings |
| Unit and integration tests (Vitest) | 171 of 171 pass, run with the time zone set to Asia/Jerusalem, America/Los_Angeles, and Pacific/Kiritimati |
| End to end tests (Playwright) | 85 of 85 pass: 49 at 390 px (37 functional flows, layout on eleven screens, and an accessibility scan), plus layout and accessibility at 375, 393, and 430 px |
| Production build and release gate | Pass: no personal markers, no trackers, offline assets present. One cosmetic warning: a chunk over 500 kB |
| Exercise content validator | 103 of 103 exercises pass |
| Tracked files against the private marker list | No matches |
| Not rerun for 3.0.0 | Lighthouse, `npm audit`, and the password gate in the Cloudflare runtime. Their last results are in the 2.1.1 report in the git history. The gate code did not change; its unit tests still pass |

## Environment limits

- WebKit cannot be installed in the build environment, so browser tests run on Chromium with iPhone emulation. The app avoids Chromium only APIs and feature detects Wake Lock, vibration, Web Share, BarcodeDetector, and storage persistence.
- Web Share is not available in desktop Chromium, so the tests exercise the download fallback.
- Add to Home Screen, Apple Calendar import, and the update on the installed phone need a real iPhone and were not automated.

## Unit tests (tests/)

- **Week (program.test.ts):** four gym strength days, two days without structured training, no early sessions; no jumps, sprints, or skills in the gym and no gym strength work at home; home jumps on the gym leg days, before the gym, never on consecutive days; no sets to failure (two reps in reserve, three for shoulder care); 12 to 22 work sets and 75 minutes or less per gym session, counting every rest; direct weekly work for each main muscle and none over 20 sets; shoulder care first and big exercises before small ones; chosen exercises land on the right days; every session has a location, equipment, space, duration, and stop rules.
- **Home space:** unknown answers mean the most limited room; the full introductory session (64 landings, ending with full approach jumps after the approach footwork, outdoors, with full rest) when the space allows; a reach into the air without a marked wall, and no approach jump without an outdoor area or a hall; no jumps in a small flat with a low ceiling, tiles, and noise limits; quiet swaps with the reason when only noise stops a drill; no maximal jumps under a standard ceiling indoors; the build level at about 95 landings; the skill session never has jumps.
- **Wrist:** every library exercise rated; heavy wrist work only after clearance and little with symptoms; heavy picks swapped for an equivalent option; no ball contact before clearance; gripping and pressing left out with symptoms; load increases held, reps unaffected.
- **Plan changes (planUpdate.test.ts, program.test.ts):** the 3.0 week is offered to a 2.1 install and not to a new one; nothing changes until activation; activation creates a new version and finished sessions keep their prescriptions; Not now hides the offer but Train still shows it; home sessions follow the profile; the jump level changes only through a proposal; hand edits go through the same preview; the difference lists added, removed, and changed items day by day; early reminders move only if still at their old defaults.
- **Food (nutrition.test.ts):** the nutrition check never suggests eating less, whatever the trend; five steady days is not a plateau; too fast loss (above about 0.45 kg a week) or a slide in energy, mood, or sleep means more food and a parent; sparse food logs do not block it; weekly weighing and weighing off both work; smart scale body fat is never read; every example has a household measure, more food options, swaps, storage, and the example label; no meat and dairy in one example; evening milk becomes pareve when too soon after meat (3 hour and 6 hour settings, off, and custom times); dairy logged too soon is noted, not blocked; no food depends on finishing a workout; the sum of the examples is described, not made a target; no supplement in the examples; raw, dry, cooked, and drained conversions with ranges consistent with the energy values; the green bean arithmetic for each state; recipe nutrition from ingredients, including oil; meal preparation scaling.
- **Profile and exports (athlete.test.ts):** the wrist gate on progression; school sport added to weekly exposure, hours compared with age only when the age is known, heavy jumping the day before a home jump day; jump test heights, like with like comparison, and noise; cautious defaults for missing answers; open questions with the gating ones first; only professionally reviewed energy targets used, newest first; readiness never certifies safety; the coach report keeps aspirations apart from reviewed targets; the plan export has locations, durations, stop rules, and example meals; backups round trip the profile and the sport log, and older backups without the sport log import.
- **Weekly review (review.test.ts):** sections with evidence and confidence; missing data, recovery concerns, and reasons for a professional review; intake never judged against a fixed 2,000 kcal; too few weights; pain of 4 or more pauses progression; ready to progress reasons; backup recency; coach report without notes or photos by default; the four exposure review; muscle coverage.
- **Unchanged areas:** progression (double progression, one set never adds load), time and dates across clock changes, rest timer, Sabbath window and sunset, ICS export, backups and encryption, fixtures, and the password gate.

## End to end flows (e2e/app.spec.ts), at 390 px

1. First run setup lands on Today with the profile saved locally.
2. Installable manifest and an active service worker.
3. A Monday gym workout: Leg Press with 3 reps in reserve while learning, rest timer at 3:00, three sets, finish, plan against actual, the next target accepted and shown on the exercise page with its wrist and progression notes.
4. A gym day shows location, space, duration, equipment, and stop rules, with the home session before the gym, no jumps before the home space is known, and Tuesday without structured training.
5. An installed 2.1 plan is offered the new week: the questions, the preview with the schedule change and the day by day difference, nothing changed before activation, then version 2 with the home jumps and the no ball arm swing while the wrist is not cleared.
6. The new week offer put off with Not now is still on Train.
7. The questionnaire: first and second choices, kept after a reload, and the difference shown before saving.
8. Home drills follow the space and the wrist, change only through a preview, and the outdoor note appears in the workout.
9. About checks for a new version.
10. Jump tests on Progress compare like with like, with no dunk text.
11. School sport counts toward the week.
12. One set of nine reps never raises the load.
13. A double tap on Complete saves one set, not two.
14. The rest timer keeps the right time after backgrounding and a reload.
15. The rest end sound is queued on the audio clock for the prescribed rest.
16. Last performance appears beside the inputs.
17. A unilateral exercise logs left and right separately.
18. Editing the plan shows the difference, creates a version, and leaves history unchanged.
19. All 103 exercises show instructions, a two view muscle diagram, a visual, stop rules, substitutions, wrist guidance, and progression offline.
20. Videos load only after a tap.
21. Example meals show "Example meals", "not a target", the context note, and the example label; a meal logs in one tap.
22. A restaurant estimate is stored as a low confidence range.
23. A food that is not in the list is logged with your own numbers as a range.
24. Saturday meals log with the plate guide.
25. A morning weight is recorded.
26. Number fields accept typing one key at a time, and a professionally reviewed calorie range typed into Goals and reviews appears on Eat.
27. A check in with pain of 5 shows the parent safety message.
28. The weekly review shows progress, missing data, recovery, professional review reasons, and the older sections, and exports the coach report.
29. Backup, delete all data, and import restore the data.
30. Invalid and broken imports are rejected.
31. An encrypted backup opens only with its passphrase.
32. Data survives a reload.
33. Sabbath Mode quiets Saturday; the calendar has alarms and leaves out the Saturday 07:00 check in.
34. The app opens offline and makes no third party requests.
35. Delete all data asks twice.
36. The app lock engages after inactivity and opens with the PIN.
37. Knee pain of 3 out of 10 in the morning check in shows "Skip the jumps today" on Today and on the Train day.

Layout and accessibility, at 375, 390, 393, and 430 px: no horizontal overflow and no tap target under 24 px on eleven screens, form fields at 16 px or more, and an axe WCAG 2 A and AA scan of seven main screens with no serious or critical issues.

## Manual visual review (3.0.0)

Screenshots at 390 px, light theme, from a fresh install on a Monday: Today, Your profile, the plan preview after answering the profile, Train, the Monday and Friday days, Eat, Goals and reviews, Progress, and School sport. No console errors.

Defects found and fixed in 3.0.0:

- A double tap on Complete set saved the same set twice. Saving is now one set per tap, with a test that fails without the fix.
- A new exercise showed 2 reps in reserve as the default even though the target was 3, because the history loaded after the default was set. The default now follows once the history loads.
- Session times left out the rest after each exercise's last set and the time to change exercises, so gym days read about 30 to 65 minutes. They now read about 40 to 75 minutes, and home jump sessions about 30.
- The home equipment line repeated floor space and said "No equipment" next to real equipment. Space, floor, and ceiling now stay on the Space line.
- Recommendation files saved plan changes straight away. They now open in the plan preview.
- Whey protein appeared as an optional breakfast item and in the recipe steps. Examples no longer suggest any supplement.
- App text and public documents described one person's injury and food habits. They are now generic ("a wrist injury", "a large vegetable portion"), and the meat to dairy default is 6 hours, set per family on the phone.

Defects found and fixed in earlier reviews (1.x to 2.x):

- Complete set fell below the fold. The workout now uses a focus mode with a pinned action dock.
- The rest bar label overlapped its buttons. Labels now truncate and the time itself toggles pause.
- The undo toast covered controls and stayed across screens. It now sits under the header and clears on navigation.
- A race could overwrite typed set values when the stored set list refreshed. The next set is now prepared immediately.
- Onboarding with demo data could navigate away from a screen already opened, and finishing a workout could do the same. Both fixed.
- The Eat totals grid left an empty cell, meal rows were cramped, and the no data state said "0". Fixed.
- Faint text contrast was just under 4.5:1 and some checkboxes were under 24 px. Fixed.
- The readiness tag was green before any check in, the scale icon read as a question mark, and chart labels touched the first data point. Fixed.
- The light rest timer and toast were glaring in dark mode. They now use dedicated dark tokens.
- A new install on a Monday said yesterday's session was missed and offered a weekly review of the week before the plan started. Both now wait until the plan has actually run.
- Toasts were capped at half the screen width, so short messages wrapped, and they stayed on top of sheets opened right after. They now size to their text and clear when a sheet opens. The redundant toast after saving a workout is gone, and the summary opens at the top.
- Chart axes showed values like 77.9 and 79.2. They now use round steps such as 78, 78.5, 79.
- Disclosure chevrons were squeezed into a tick shape next to long titles. Fixed.
- Time fields cut off "AM" and "PM", onboarding placeholders were truncated, and "Rest 2.5 min" overflowed at larger text sizes. Fixed.
- Native file pickers looked out of place. They are now normal buttons.
- Sheets blended into the dimmed page in dark mode. They now use a raised surface with an edge.
- Copy fixes: "Rest 0.5 min" now reads "Rest 30 s", lowercase "none" and "no data" placeholders, "Only 0 morning weights", a sentence starting with a digit, and first time hints that said "pick a load" on warm ups and jumps.
- The creatine review toggle was a card inside a card. It is now its own group.
- Custom exercises no longer show a caption for an illustration they do not have.

## Content checks

- `scripts/validate-exercises.ts`: all 103 exercises have complete fields, known muscle IDs, valid substitutions, visuals, an effort rule on every loaded exercise, and copy free of em dashes, "until failure", "grind it out", forced reps, and hype words.
- `docs/content-audit.json`: example days come to about 3,050 to 3,400 kcal on school days; they are descriptions, not targets. Gym sessions take about 40 to 75 minutes by the new estimate.
- Food values were checked against USDA data through search snippets and the SR28 data file (NUTRITION_DATA_AUDIT.md).
