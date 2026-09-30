# Changelog

## 2.0.0, 2026-09-30

A new program built from the athlete's own exercise choices.

- One exercise for each muscle head, three work sets, and a slow stretch at the long muscle length, across six gym days that alternate upper and lower body. Every muscle gets about 9 to 18 direct sets a week, and none more than 20.
- **Choose your exercises**: a questionnaire in the app, one step per muscle head, with 2 to 4 exercises that build that head about equally, each with a picture and instructions. Muscles trained twice a week can take a second choice for variety. Saving builds the plan as a new version and keeps history. Installed apps get a card on Today and Train.
- Only machines, cables, the Smith machine with safety stops, and dumbbells, because the athlete trains alone. No free barbell in any choice.
- Effort by exercise: small machine and cable exercises go to technical failure on every set, machine and Smith compounds on the last set, and dumbbell presses, lunges, and hinges stop one rep short. Failure means the last rep with clean form. A new exercise stays two reps short for its first two sessions.
- Progression for sets to failure is judged on the first set, because later sets lose reps.
- 34 new exercises with instructions, muscles, safety, substitutions, and original illustrations. Every loaded exercise now states how close to failure it may go.
- Research changes: leg extensions lean back to stretch the rectus femoris, calf raises pause two seconds in the stretch and use a straight knee, the long head of the triceps is trained overhead twice a week, shoulder care starts every upper day, and the upper chest, side delts, rear delts, adductors, and side of the hip have their own slots. 24 new sources.

## 1.2.1, 2026-09-30

- The plan update card also shows on Train and on each day in Train, until the change is added. There it has no "Not now", so an update put off on Today can still be added.
- If adding a plan update fails, the card says so and the button works again.

## 1.2.0, 2026-09-29

- Tuesday and Friday are regular muscle building gym days, because volleyball now happens every morning. Tuesday is Upper C: incline dumbbell press, chest supported dumbbell row, cable fly, lateral raise, face pull, incline dumbbell curl, and overhead triceps extension. Friday is Lower C before the swim: leg press, 45 degree back extension, Nordic curl, seated leg curl, cable hip adduction and abduction, and standing calf raise. Every set keeps two or three reps in reserve.
- The new days fill the gaps the other four gym days left. Weekly direct sets now reach about 15 for the chest, 14 for the lats, 7 for the side and 8 for the rear shoulders, 7 for the triceps, 9 for the biceps and brachialis, 13 each for the quads and hamstrings, and 6 for the calves, with no muscle above 20.
- Six new exercises with instructions, muscles, safety, substitutions, and original illustrations: Incline Dumbbell Press, Chest Supported Dumbbell Row, Incline Dumbbell Curl, Leg Press, 45 Degree Back Extension, and Cable Hip Adduction.
- Installed apps get the new days from the same "Add to my plan" card, as a new plan version. Only the old volleyball drills on those two days are replaced. Morning work, the swim, anything you added, and your history stay. The Tuesday and Friday food targets keep their numbers and get the new names.
- PeakForm now checks for a new version each time it comes back to the screen, not only when it is opened from scratch. More, About has a Check for updates button that can also apply a waiting update.

## 1.1.0, 2026-09-29

- Morning volleyball at 05:30, Sunday to Friday, at home with no ball: easy rope as the warm up, then passing or blocking footwork, light dumbbell shoulder care (Y raise, side lying external rotation), and trunk control (dead bug). Saturday stays a full rest day.
- Five new exercises with instructions, muscles, safety, substitutions, and original illustrations.
- Installed apps get a one tap "Add to my plan" card that adds the morning sessions as a new plan version and moves the default check in to 05:15 and wind down to 20:45, so eight hours of sleep still fit. History is kept, and times you changed are left alone.
- Number fields accept free typing: no jumping to the minimum while typing, and decimals work.
- Foods that are not in the list can be logged with your own totals.
- The rest end sound is queued when rest starts, so it plays on time with the screen on. Settings has a sound test.

## 1.0.2, 2026-09-29

Private publishing.

- PeakForm is no longer published to a public GitHub Pages address. It is published on the user's own Cloudflare Pages project behind a password gate, so nobody else can open or install it.
- The gate signs in on the same site, so it works inside the iPhone Home Screen app, and it fails closed when no password is configured.
- The manifest is requested with the session cookie, so Add to Home Screen picks up the app name and icon behind the gate.
- The install QR code is now generated for the private address into the gitignored `private/` folder.

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
