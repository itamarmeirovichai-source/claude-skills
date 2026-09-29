# PeakForm

A private, offline training, food, and recovery app for one athlete, delivered as an installable web app (PWA) for iPhone. It covers strength and hypertrophy training, volleyball and jump work, swimming, meals and meal preparation, morning check ins, sleep and pain tracking, and a weekly review.

- **Free.** No subscription, no paid API, no account.
- **Private.** Everything lives in the phone's browser storage. No server, no analytics, no trackers.
- **Offline.** Every core screen works without a connection after the first load.
- **Careful.** Double progression that you confirm, reps in reserve instead of failure, a 2,000 kcal floor, and safety flags that pause progression.

The app is published privately: a Cloudflare Pages project owned by the user, behind a password gate. See [INSTALL_ON_IPHONE.md](INSTALL_ON_IPHONE.md) for the one time setup.

## Documents

| File | What it covers |
| --- | --- |
| [INSTALL_ON_IPHONE.md](INSTALL_ON_IPHONE.md) | Short steps to put PeakForm on the Home Screen |
| [USER_GUIDE.md](USER_GUIDE.md) | How to use each part of the app |
| [PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md) | Where data lives, what can leave the phone, the app lock |
| [RESEARCH.md](RESEARCH.md) | Evidence and platform facts behind the defaults |
| [MEDIA_ATTRIBUTION.md](MEDIA_ATTRIBUTION.md) | Original artwork and linked videos |
| [TEST_REPORT.md](TEST_REPORT.md) | What was tested and the results |
| [BUILD_STATUS.md](BUILD_STATUS.md) | Decisions, status, limits, next steps |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [docs/content-audit.json](docs/content-audit.json) | Machine readable audit of exercises, plan, meals, recipes, and sources |
| [docs/screenshots](docs/screenshots) | Screenshots of the main screens |

## Development

Requires Node 22.

```bash
cd peakform
npm ci
npm run dev          # local development server
npm run typecheck    # TypeScript strict
npm run lint
npm test             # unit and integration tests (Vitest)
npm run build        # production build, then the release gate in scripts/check-dist.mjs
npm run e2e          # Playwright end to end tests on iPhone sized viewports
npm run audit:content
```

Useful scripts:

- `npx tsx scripts/make-private-seed.ts` writes the private setup file to `private/`, which is gitignored. Never commit it.
- `npx tsx scripts/make-fixtures.ts` rebuilds the synthetic example backups in `fixtures/`.
- `npx tsx scripts/figure-sheet.ts <dir> src/content/exercises/lower.ts` renders exercise keyframes for review.
- `npx tsx scripts/shots.ts <dir> 390 light` captures screenshots from a running preview server.
- `npx tsx scripts/sweep.ts <dir> <375|390|393|430> <light|dark> <demo|empty|long|large|offline>` walks every major screen and state and tiles the screenshots into contact sheets for design review.
- `npx tsx scripts/make-qr.ts <url>` writes an install QR code for your private address to `private/`, which is gitignored.

## Architecture

- React 19, Vite 8, TypeScript strict, Dexie on IndexedDB, Zod schemas, vite-plugin-pwa with Workbox.
- `src/content`: the seeded plan, exercise library, muscles, foods, meals, recipes, sources, and media.
- `src/domain`: pure engines with unit tests (progression, four exposure review, nutrition gate, coverage, portions, timer, Sabbath window, ICS, backup, review, report).
- `src/db`: typed record schemas, the Dexie database, and data access.
- `src/screens` and `src/ui`: the interface. `src/svg`: original body map, keyframe figures, and portion icons.
- Hash routing, so the same build works at any path on any static host.

## Deployment

PeakForm is not published on GitHub Pages, because anyone with a GitHub Pages address could open it. Instead, Cloudflare Pages builds `peakform/` from `main` (build command `npm run build`, output `dist`, root directory `peakform`, Node version from `.node-version`) and serves it behind `functions/_middleware.ts`, a password gate implemented in `edge/gate.ts`. The password lives only in the encrypted `PEAKFORM_PASSWORD` variable in Cloudflare. Without it, the site serves nothing. Setup steps are in [INSTALL_ON_IPHONE.md](INSTALL_ON_IPHONE.md).

To try the gate locally, put `PEAKFORM_PASSWORD=<at least 12 characters>` in a gitignored `.dev.vars` file, run `npm run build`, then `npx wrangler pages dev dist`.

To roll back, open the project in Cloudflare, choose an earlier deployment, and select **Rollback**. Installed apps pick up the rollback the next time they open online, after tapping Update.

`.github/workflows/peakform-ci.yml` runs typecheck, lint, unit tests, the build with its release gate, and the browser tests on every pull request that touches `peakform/`.
