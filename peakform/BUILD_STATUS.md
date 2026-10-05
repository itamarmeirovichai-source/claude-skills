# PeakForm build status

Last updated: 2026-10-05. Version 2.1.1.

## State

Complete and tested. Publishing is private: after the pull request is merged, the user connects a free Cloudflare Pages project to the repository and sets a password (INSTALL_ON_IPHONE.md, Part 1). Nothing is published to a public address.

## Decisions

- **Delivery:** installable PWA. React 19, Vite 8, TypeScript strict, Dexie on IndexedDB, Zod, vite-plugin-pwa (Workbox). No server, no account, no analytics.
- **Location:** built in `peakform/` inside the existing `claude-skills` repository, so the unrelated skills files are untouched.
- **Routing:** hash routes so any static host and the offline service worker work without rewrites. `base: './'` so the same build runs at any path.
- **Privacy:** the source and the deployed site are generic. The personal profile is entered on the device or imported from a private setup file generated into `private/`, which is gitignored. A release gate rejects builds containing personal markers or trackers.
- **Hosting:** a Cloudflare Pages project owned by the user, behind a same origin password gate (`functions/_middleware.ts`, `edge/gate.ts`). The user asked that nobody else be able to open or install the app. GitHub Pages was dropped because it cannot restrict access on the free plan. Cloudflare Access was considered, but its sign in redirects to another domain, which can loop inside an iPhone Home Screen app, so the gate signs in on the same origin instead.
- **Reminders:** in app timeline plus an Apple Calendar ICS export with alarms and Sabbath exclusions. No Web Push, because it needs a push server. Nothing claims to alert while the app is closed.
- **Coach access:** a two tap Share Coach Report (Markdown plus JSON). Nothing is sent automatically. Recommendation files can be imported with a visible diff and safety blocks.
- **Nutrition ranges:** item ranges come from the portion method and food variability. Day totals combine item errors as independent (root of summed squares) instead of stacking worst cases.
- **Week boundaries:** review weeks run Monday to Sunday so the Sunday evening review includes Sunday's session.
- **Workout focus mode:** during an active workout the tab bar is replaced by a pinned Complete set dock. The rest timer bar stays visible across the app.
- **Program (2.0.0):** the main sessions are built from slots, one per muscle head, each with two to four exercises that build it about equally. The athlete chose the exercises in a questionnaire before the release, and those answers are the starting choices; the same questionnaire is in the app to change them. No free barbell, because the athlete trains alone.
- **Effort (2.0.0):** each exercise has a failure policy. Small machine and cable exercises go to technical failure on every set, machine and Smith compounds on the last set, and dumbbell compounds, lunges, and hinges stop one rep short. A new exercise stays two reps short for two sessions. Sets to failure progress from the first set.
- **Jump program (2.1.0):** training blocks by date (`src/content/phases.ts`) set the Monday and Friday jump drills and the leg doses. The plan is rebuilt as a new version when a block starts, from the saved choices. Legs stop short of failure except small Monday exercises, so jump days are fresh. The dunk goal reads touch heights from approach jumps.
- **Training fuel (2.1.1):** day targets are a base plus the pre-workout rice, which counts only once that day's main workout has started (`src/domain/fuel.ts`), so missed workouts do not erase the deficit. Stored targets are unchanged; the split is computed.
- **Bundle:** less frequent screens load on demand. The service worker precaches every chunk, so everything still opens offline.

## Completed

- Content: 99 exercises, including eight jump drills for the dunk program added in 2.1.0, including five no ball morning volleyball drills and the 34 machine, cable, Smith, and dumbbell alternatives added for the questionnaire in 2.0.0, with instructions, muscles, safety, substitutions, effort rules, and original keyframes or drill diagrams. Since 2.0.0 the main sessions come from the athlete's own exercise choices, at the user's request. Foods, meal templates, targets, recipes, meal preparation, and the Sabbath plate guide.
- Engines, the access gate, the program builder, and plan updates with unit tests (126 tests).
- All screens, onboarding, and app lock.
- End to end tests (83), layout and accessibility checks at 375, 390, 393, and 430 px.
- Design review sweep of every major screen in light, dark, offline, empty, long content, and large text states, with the defects fixed.
- Documentation, content audit, synthetic fixtures, screenshots, and the CI workflow.
- Private deployment: password gate for Cloudflare Pages with unit tests, checked end to end in Cloudflare's local runtime.

## Known limits

- Research could only use search results. The build environment blocked direct page access, and every source records its access level.
- Videos were matched by title and channel only, never watched. The app says so and lets the user confirm or reject each one.
- Browser tests run on Chromium with iPhone emulation, because WebKit cannot be installed here.
- The default meals as prescribed give more protein and less fat than the macro targets in the brief. This is flagged in RESEARCH.md and TEST_REPORT.md for a dietitian to review.
- iOS may remove site data under storage pressure. Home Screen use, persistent storage, and backups mitigate this.

## Next steps

1. Merge the pull request. This publishes nothing by itself.
2. Create the Cloudflare Pages project and set the password (INSTALL_ON_IPHONE.md, Part 1).
3. On the iPhone, follow INSTALL_ON_IPHONE.md, Part 2.
4. Optional: after a few weeks of real use, review the macro targets with a pediatric sports dietitian and adjust them in More, Nutrition targets.
