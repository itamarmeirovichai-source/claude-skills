# PeakForm build status

Last updated: 2026-10-09. Version 3.1.0 (pain and sleep rules for jump days, longer warm up, example meals closer to needs).

## State

Built and tested in the build environment (TEST_REPORT.md). Deployment happens when the pull request is merged into `main`: the Cloudflare Pages project that the user owns builds `main` behind the password gate. Nothing was tested on a real iPhone in this environment, and no clinician, dietitian, or coach has reviewed the 3.0 plan.

## What 3.0.0 changed

- **Week:** four gym strength days (Upper A, Lower A, Upper B, Lower B), home jumps and footwork on Monday and Thursday before the gym legs, a light skill session on Friday, Tuesday without structured training, Saturday full rest, no early mornings. Details and evidence: TRAINING_AUDIT.md.
- **Effort:** about two reps in reserve, three while an exercise is new. No routine failure, no one repetition maximum tests.
- **Gates:** a wrist load rating on every exercise and a wrist status in the profile; a space, ceiling, surface, impact, and noise rating on every home drill and a home setup in the profile. Unknown answers mean the cautious choice (`src/content/traits.ts`, `src/domain/homeSpace.ts`, `src/content/homeSessions.ts`).
- **Plan changes:** every change is a proposal stored in the key value table, shown with a summary and a day by day difference (`src/domain/planDiff.ts`, `src/screens/PlanUpdate.tsx`), and saved as a new plan version only on activation. The automatic block sync and the dunk program were removed.
- **Food:** no default calorie target; example meals in grams with state, household measures, kosher category, storage, and options for more; reviewed targets recorded with source and status; aspirations kept apart and never turned into targets; a nutrition check that never suggests eating less (`src/content/meals.ts`, `src/domain/nutrition.ts`, `src/domain/athlete.ts`). Details: NUTRITION_DATA_AUDIT.md.
- **Data:** new key value entries for the profile, aspirations, reviewed targets, jump tests, the jump level, and the plan proposal; a new `sportLogs` table (Dexie version 2). Backups include all of them; older backups still import.
- **Exports:** the coach report includes the profile answers, aspirations, and reviewed targets, kept apart; a private plan file holds the week and the example meals.

## Decisions

- **Delivery:** installable PWA. React 19, Vite 8, TypeScript strict, Dexie on IndexedDB, Zod, vite-plugin-pwa (Workbox). No server, no account, no analytics.
- **Location:** built in `peakform/` inside the existing `claude-skills` repository, so the unrelated skills files are untouched.
- **Privacy:** the source, the documentation, and the deployed site are generic and de-identified. Personal answers are entered on the device or imported from a private setup file in the gitignored `private/` folder. The build gate rejects personal markers and trackers; tracked files are checked against the private marker list before release. Defaults that would mirror one family (for example the meat to dairy interval, now 6 hours by default) are set on the phone instead.
- **Hosting:** a Cloudflare Pages project owned by the user, behind a same origin password gate (`functions/_middleware.ts`, `edge/gate.ts`).
- **Reminders:** in app timeline plus an Apple Calendar ICS export with alarms and Sabbath exclusions. No Web Push. Nothing claims to alert while the app is closed.
- **Durations:** session estimates count about 3 seconds a repetition, the rest after every set, side switches, changeovers, and a gym warm up (`src/domain/sessionInfo.ts`).

## Completed

- Content: 103 exercises, including four new home drills, each with a wrist load rating and, for home drills, space needs. Foods with states and sources, raw and dry entries, yields, example meals, recipes computed from ingredients, meal preparation, and the Sabbath plate guide.
- Engines: plan proposals and differences, home space matching, wrist gate, exposure from school sport, jump tests, kosher timing, recipe math, the nutrition check, the weekly review with professional review reasons, and the plan export, with unit tests (171).
- Screens: Your profile, Goals and reviews, School sport, Jump tests, the plan preview, and session information on Train.
- End to end tests (85): 49 at 390 px, plus layout and accessibility at 375, 393, and 430 px.
- Documentation: TRAINING_AUDIT.md, NUTRITION_DATA_AUDIT.md, RESEARCH.md (3.0 section and 18 new sources), CHANGELOG.md, TEST_REPORT.md, USER_GUIDE.md, PRIVACY_AND_SECURITY.md.

## Known limits

- Research used search results only. Direct page access was blocked, the search budget ran out before food safety, kosher practice, and FODMAP content could be searched, and every source records its access level.
- Adult evidence is used for proximity to failure and weekly volume; it is marked as adult in the audits.
- Browser tests run on Chromium with iPhone emulation, because WebKit cannot be installed here. Lighthouse, the dependency audit, and the Cloudflare runtime gate test were not rerun for 3.0.0 (TEST_REPORT.md).
- Session durations are estimates. Upper days come to about 70 to 75 minutes.
- iOS may remove site data under storage pressure. Home Screen use, persistent storage, and backups mitigate this.

## Next steps

1. On the phone: open the app, answer **More, Your profile** (wrist, home space, sport, meat and dairy interval), look at the new week in the preview, and activate it.
2. Record the aspirations in **More, Goals and reviews**, in your own words.
3. Review the open questions in RESEARCH.md with a parent and, where they apply, a pediatrician, a pediatric sports dietitian, and the clinician who treats any injury.
