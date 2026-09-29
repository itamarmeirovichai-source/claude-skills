# PeakForm test report

Date: 2026-09-29. Build 1.0.0.

## Summary

| Check | Result |
| --- | --- |
| TypeScript strict (`npm run typecheck`) | Pass, no errors |
| ESLint (`npm run lint`) | Pass, no errors or warnings |
| Unit and integration tests (Vitest) | 86 of 86 pass, also run with the time zone set to Asia/Jerusalem, America/New_York, and UTC |
| End to end tests (Playwright) | 67 of 67 pass: 23 functional flows at 390 px, plus layout and accessibility checks at 375, 390, 393, and 430 px |
| Production build and release gate | Pass: no personal markers, no trackers, CSP present, offline assets present |
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
- **Fixtures:** example plain and encrypted backups validate, the recommendation example applies cleanly, and no fixture contains the real profile.

## End to end flows (e2e/app.spec.ts)

1. First run setup lands on Today with the profile saved locally.
2. Installable manifest, icons, Apple meta tags, CSP, and an active service worker.
3. Start a workout, log every set, rest timer starts at the prescribed time, finish, see plan and actual, accept the next target, and see it on the exercise page.
4. One set of nine reps does not raise the load.
5. Rest timer shows the right time after 70 seconds of simulated backgrounding and after a reload, then reports that rest finished.
6. Last performance appears beside the inputs.
7. A unilateral exercise logs left and right separately.
8. Editing the plan creates version 2 while the finished session keeps its original prescription.
9. All 46 exercises show instructions, a two view muscle diagram, and an offline visual.
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

Layout and accessibility, at 375, 390, 393, and 430 px: no horizontal overflow and no tap target under 24 px on ten screens, every form field at 16 px or more (no zoom on focus), and an axe WCAG 2 A and AA scan of six main screens with no serious or critical issues.

## Manual visual review

Screenshots were reviewed at 375 and 390 px in light and dark mode, with demo data, with no data, and offline. Defects found and fixed during review:

- Complete set fell below the fold. The workout now uses a focus mode with a pinned action dock.
- The rest bar label overlapped its buttons. Labels now truncate and the time itself toggles pause.
- The undo toast covered controls and stayed across screens. It now sits under the header and clears on navigation.
- A race could overwrite typed set values when the stored set list refreshed. The next set is now prepared immediately.
- Onboarding with demo data could navigate away from a screen already opened, and finishing a workout could do the same. Both fixed.
- The Eat totals grid left an empty cell, meal rows were cramped, and the no data state said "0". Fixed.
- Faint text contrast was just under 4.5:1 and some checkboxes were under 24 px. Fixed.
- The readiness tag was green before any check in, the scale icon read as a question mark, and chart labels touched the first data point. Fixed.
- The light rest timer and toast were glaring in dark mode. They now use dedicated dark tokens.

## Content checks

- `scripts/validate-exercises.ts`: all 46 exercises have complete fields, known muscle IDs, valid substitutions, visuals, and copy free of em dashes, isolation claims, failure prescriptions, and hype words.
- `docs/content-audit.json`: the plan matches the brief item by item. Default meals land within about 100 kcal of each training day target. Focus checks confirm upper back, calves, and forearms.
- Known plan inconsistency, reported and not hidden: with standard food values the default meals supply about 200 to 215 g protein and 60 to 70 g fat, against targets of about 150 to 155 g protein and 88 to 92 g fat. This is listed for review with a parent and a pediatric sports dietitian.
