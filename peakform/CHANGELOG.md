# Changelog

## 1.0.1, 2026-09-29

Design review fixes.

- New installs no longer report a missed session or a review for the week before the plan started. Demo data sets the plan start to the start of the demo.
- Toasts size to their text, clear when a sheet opens, and no longer repeat what the workout summary shows.
- Round chart axis values, readable disclosure chevrons, wider time fields, button style file pickers, and a raised sheet surface in dark mode.
- Workout actions wrap at larger text sizes. Rest shows "30 s" instead of "0.5 min". First time hints match the exercise type.
- Clearer empty states and copy across Progress, the weekly review, and exercise details.
- An end to end test for the app lock, and `scripts/sweep.ts` for design review.

## 1.0.0, 2026-09-29

First release.

- Installable, offline PWA with Today, Train, Eat, Progress, and More.
- Seeded weekly plan with six training days and a full rest day, 46 exercises with instructions, muscle maps, safety cues, substitutions, and original keyframes or drill diagrams.
- Guided workout with focus mode, last performance beside every input, warm up sets, left and right logging, a persistent rest timer based on an absolute end time, substitutions, and plan versus actual.
- Double progression with confirmation, four session reviews, and pain and safety holds.
- Meal templates with one tap logging, Estimate by Eye with honest ranges, restaurant estimates, the Sabbath plate guide, meal preparation, recipes, and optional barcode lookup.
- Morning check in, seven day weight trend, waist, trend only body fat, sleep, wellbeing, fourteen day nutrition gate with a 2,000 kcal floor, and muscle coverage with shoulder overlap.
- Weekly review with four sections, evidence, confidence, priorities, and a Markdown and JSON coach report.
- Apple Calendar reminder export, Sabbath Mode, encrypted and plain backups, CSV export, import with preview and safety copy, recommendation import with a visible diff, app lock, and delete all data.
