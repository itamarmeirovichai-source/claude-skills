# PeakForm build status

Last updated: 2026-09-29. Version 1.0.2.

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
- **Bundle:** less frequent screens load on demand. The service worker precaches every chunk, so everything still opens offline.

## Completed

- Content: 46 exercises with instructions, muscles, safety, substitutions, and original keyframes or drill diagrams. The plan is seeded exactly. Foods, meal templates, targets, recipes, meal preparation, and the Sabbath plate guide.
- Engines and the access gate with unit tests (93 tests).
- All screens, onboarding, and app lock.
- End to end tests (68), layout and accessibility checks at 375, 390, 393, and 430 px.
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
