# PeakForm test report

Date: 2026-09-30. Build 2.0.0.

## Summary

| Check | Result |
| --- | --- |
| TypeScript strict (`npm run typecheck`) | Pass, no errors |
| ESLint (`npm run lint`) | Pass, no errors or warnings |
| Unit and integration tests (Vitest) | 116 of 116 pass, also run with the time zone set to Asia/Jerusalem, America/New_York, and UTC |
| End to end tests (Playwright) | 79 of 79 pass: 31 functional flows at 390 px, plus layout and accessibility checks at 375, 390, 393, and 430 px |
| Production build and release gate | Pass: no personal markers, no trackers, CSP present, offline assets present |
| Private access gate in the Cloudflare runtime (Wrangler 4.143, local) | Pass: app files, service worker, and manifest locked without the password; wrong password rejected; after sign in the app installs its service worker and opens offline; a second device stays locked |
| Dependency audit (`npm audit`) | 0 vulnerabilities |
| Lighthouse, simulated mobile | Performance 94, Accessibility 100, Best Practices 96, SEO 66 |
| Offline launch after first load | Pass |
| Third party requests during normal use | None |
| Console errors in primary flows | None |

SEO is intentionally low: the app is private and asks search engines not to index it. Best Practices loses points for not shipping source maps, which is deliberate to keep the build small.

## Environment limits

- WebKit cannot be installed in the build environment, so browser tests run on Chromium with iPhone 13 emulation (viewport, touch, device scale, iOS user agent). The app avoids Chromium only APIs and feature detects Wake Lock, vibration, Web Share, BarcodeDetector, and storage persistence.
- Web Share is not available in desktop Chromium, so the tests exercise the download fallback. On iPhone, the same buttons open the share sheet.
- Add to Home Screen and Apple Calendar import need a real iPhone and were not automated. The manifest, icons, Apple meta tags, and service worker were verified.

## Unit tests (tests/)

- **Progression:** one set of nine never raises load; 9, 8, 8 adds one rep at the same load; 10, 10, 10 at target RIR and good form suggests the smallest practical increase and resets reps; 10, 10, 9 does not qualify; poor and acceptable form hold; pain holds and severe pain asks to tell a parent or coach; low RIR holds or reduces; missing RIR or form never progresses; mixed loads judged at the lowest; reps below range hold; left and right must both qualify; equipment increments and custom increments; jumps, sprints, swims, and Nordic curls never auto progress.
- **Nutrition:** seven day average needs four morning weights; non standard weights ignored; fourteen day gate refuses without enough weights or food logs; hold at 0.25 to 0.6 kg a week; recomposition label; check estimates then 100 to 150 kcal reduction when weight and waist are stable; fast loss and wellbeing decline add 150 to 200 kcal with a parent; never below 2,000 kcal; waist required before judging stable weight.
- **Estimate by Eye:** stores method, midpoint, and range; restaurant ranges wider than household, household wider than weighed; honest range formatting; the approximate school and dinner day from the brief.
- **Meals and targets:** exact default quantities for every meal and weekday; targets at or above floors; weekly average; Monday defaults near target; meal prep scaling.
- **Time:** date arithmetic across Israeli and US clock changes; Monday to Sunday review weeks; date keys in named zones around midnight; sleep across midnight.
- **Rest timer:** correct remaining time after backgrounding; overdue reporting; pause, resume, and adjust from the absolute end.
- **Sabbath:** manual window, disabled mode, local sunset calculation for a city across the clock change, Friday detection.
- **ICS:** weekly events with alarms, Sabbath exclusions, line folding under 75 octets, no exclusions when Sabbath Mode is off.
- **Backup:** checksum stability and tamper detection; encryption round trip and wrong passphrase; short passphrase rejected; invalid files rejected; row validation; preview with added, identical, and conflicting rows; merge choices; version 0 migration; CSV escaping and formula neutralising; recommendation validation and safety blocks, including RIR 0.
- **Weekly review:** four sections with evidence and confidence; too few morning weights; pain of 4 pauses progression and leads priorities; ready to progress with reasons; backup recency; coach report in Markdown and JSON without notes by default.
- **Four exposure review:** due every fourth exposure; progress, hold, reduce, coach review for pain, and coach review for stable jump quality without height gains.
- **Coverage:** transparent direct and indirect weights, activity exposure, upper back, calves, and forearms present, shoulder overlap notes.
- **Program (2.0.0):** every slot offers only machine, cable, Smith, or dumbbell exercises that share the slot's main muscle; slots trained twice take a second choice; choices are cleaned of unknown or extra exercises and fall back to the defaults; the default week, built from the athlete's questionnaire answers, has 18 to 27 sets a day, gives every major muscle enough direct weekly sets and none more than 20, starts every upper day with shoulder care, and puts big exercises before small ones; each exercise follows its failure policy, and no free barbell or dumbbell compound is taken to failure; rebuilding the plan keeps the morning work, the swim, and exercises the user added, and old installs get the morning sessions and new day names.
- **Plan updates:** morning sessions are added to old installs without touching other items; food target labels change only when they still have the default names.
- **Sets to failure:** progression is judged on the first set; below the range holds, reaching the top of the range adds load, and otherwise the first set adds one rep.
- **Fixtures:** example plain and encrypted backups validate, the recommendation example applies cleanly, and no fixture contains the real profile.
- **Private access gate:** fails closed with no password or a short one; every path, including the service worker and manifest, returns the password page with a 401 and no-store; wrong passwords and forged cookies are rejected; the right password sets an HttpOnly, Secure cookie that holds a keyed hash, not the password; changing the password signs everyone out.

## End to end flows (e2e/app.spec.ts)

1. First run setup lands on Today with the profile saved locally.
2. Installable manifest, icons, Apple meta tags, CSP, and an active service worker.
3. Start a workout, see the learning phase on a new exercise (two reps short, then the last set to failure), log every set, rest timer starts at the prescribed time, finish, see plan and actual, accept the next target, and see it on the exercise page.
4. One set of nine reps does not raise the load.
5. Rest timer shows the right time after 70 seconds of simulated backgrounding and after a reload, then reports that rest finished.
6. Last performance appears beside the inputs.
7. A unilateral exercise logs left and right separately.
8. Editing the plan creates version 2 while the finished session keeps its original prescription.
9. All 91 exercises show instructions, a two view muscle diagram, and an offline visual.
10. Videos load only after a tap, with no external requests before that.
11. A default meal logs in one tap.
12. A restaurant estimate is stored as a low confidence range.
13. Saturday meals log with the plate guide.
14. A morning weight is recorded and counted.
15. A check in with pain of 5 shows the parent safety message.
16. The weekly review shows its four sections and exports the coach report.
17. Backup export, delete all data, and import restore the data.
18. Invalid and broken imports are rejected with nothing changed.
19. An encrypted backup opens only with its passphrase.
20. Data survives a reload.
21. Sabbath Mode quiets Saturday, and the ICS calendar has alarms and Sabbath exclusions.
22. The app opens offline after the first load, every main screen renders, video shows "Needs internet", and no third party requests are made.
23. Delete all data asks twice and returns to first run.
24. App lock engages after five idle minutes, rejects a wrong PIN, opens with the right one, and is back on after a reload.
25. Number fields accept typing one key at a time, including decimals and a comma, show a hint out of range, and never save a clamped value.
26. A food that is not in the list is logged with your own totals as an honest range.
27. Completing a set queues the rest end sound on the audio clock for the prescribed rest.
28. An installed plan from before the morning sessions gets them, and the chosen program, with one tap on Add to my plan, as version 2.
29. The questionnaire: the week preview, the intro, a first and second choice, choices kept after opening an exercise and after a reload, and saving builds Sunday, Tuesday, Thursday, and Friday from the choices while keeping the morning work.
30. More, About checks for a new version on request.
31. The program card put off with Not now on Today disappears at once and can still be found on Train, where it has no Not now.

Layout and accessibility, at 375, 390, 393, and 430 px: no horizontal overflow and no tap target under 24 px on ten screens, every form field at 16 px or more (no zoom on focus), and an axe WCAG 2 A and AA scan of six main screens with no serious or critical issues.

## Manual visual review

`scripts/sweep.ts` drives the built app through 53 to 64 screens and states per run (onboarding, Today, the whole workout flow including rest, pain stop, unilateral sets, substitution and finish, exercise detail, library, Eat, Estimate by Eye, restaurant estimates, Sabbath plate, meal preparation, recipes, Progress, coverage, history, weekly review, check in, every More page, offline, and the lock screen). Runs reviewed:

| Width | Theme | State |
| --- | --- | --- |
| 375 | light | demo data |
| 430 | dark | demo data |
| 375 | light | no data |
| 393 | light | no data |
| 390 | light | long content (long app name, long custom exercise, long notes) |
| 375 | light | text at 125 percent |
| 390 | dark | offline |

Defects found and fixed during review:

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

- `scripts/validate-exercises.ts`: all 91 exercises have complete fields, known muscle IDs, valid substitutions, visuals, a failure policy on every loaded exercise, failure wording only where the policy allows it and always with clean form, and copy free of em dashes, isolation claims, "until failure", "grind it out", forced reps, and hype words.
- `docs/content-audit.json`: since 2.0.0 the main sessions come from the athlete's own exercise choices, at the user's request, so they no longer match the original brief item by item. Upper days take about 77 to 84 minutes and lower days 62 to 73, inside the 75 to 90 minutes available. Default meals land within about 100 kcal of each training day target. Focus checks confirm upper back, calves, and forearms.
- Known plan inconsistency, reported and not hidden: with standard food values the default meals supply about 200 to 215 g protein and 60 to 70 g fat, against targets of about 150 to 155 g protein and 88 to 92 g fat. This is listed for review with a parent and a pediatric sports dietitian.
