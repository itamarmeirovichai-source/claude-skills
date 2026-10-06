# Privacy and security

## Where data lives

All personal data, including the profile, measurements, workouts, meals, photos, notes, and reviews, is stored in IndexedDB in the browser on the phone. Since 3.0.0 that also covers the profile answers (wrist status after an injury, home space, school sport, sleep, supervision, supplement details, weighing preference, meat and dairy interval, and any large vegetable portion), the athlete's aspirations, targets a professional reviewed, the school sport log, jump tests, and a plan proposal waiting for activation. The deployed website is a set of static files that contains no personal data and never receives any. The release gate (`scripts/check-dist.mjs`) fails the build if personal markers or known trackers appear in the output.

## Who can open the app

PeakForm is deployed to a Cloudflare Pages project that you own, behind a password gate (`functions/_middleware.ts` and `edge/gate.ts`). Every request, including the app files, the service worker, and the manifest, gets only a password page until the right password is entered. The password is stored as an encrypted Cloudflare environment variable, never in the repository or the app.

- A correct password sets a signed, HttpOnly, Secure session cookie on that device for up to a year. The cookie holds a keyed hash, not the password.
- Changing the password in Cloudflare signs out every device.
- Without a password of at least 12 characters configured, the site serves nothing at all.
- A wrong password waits a second before answering, to slow down guessing. Use a long password that you do not use anywhere else.
- The source code is in a public GitHub repository, but it contains no personal data, and a copy built by someone else has none of your data either.
- The gate protects the address. Your data is protected separately, because it never leaves the phone.

## What never happens

- No account or cloud sync. The only sign in is the site password that stops others from opening your copy.
- No analytics, telemetry, advertising, or third party error reporting.
- No automatic sharing. No assistant can read the phone's data.
- No secrets or API keys in the client.
- No personal data in the service worker cache. It only stores the app's own files.

## When the network is used

| Action | Sent where | What is sent |
| --- | --- | --- |
| Opening or updating the app | Your Cloudflare Pages site | The site password once per device, then the session cookie with requests for the app files |
| Tapping Play on a video | youtube-nocookie.com | The video request. YouTube may set cookies once playing. |
| Tapping Look up for a barcode | world.openfoodfacts.org | Only the barcode number |
| Opening an external link | That site | Whatever that site normally receives |

The Content Security Policy allows scripts and styles only from the app itself, frames only from youtube-nocookie.com, and network requests only to the app and Open Food Facts.

## Sharing and backups

- Files leave the phone only when you share or save them.
- **Encrypted backups** use AES-GCM with a 256 bit key derived from your passphrase with PBKDF2 (SHA-256, 310,000 iterations). A lost passphrase cannot be recovered by anyone.
- **Plain backups** are readable by anyone who has the file. Store them privately.
- Every backup includes a SHA-256 checksum, so damage or tampering shows up in the import preview.
- Before any import, PeakForm saves a local safety copy, and it restores that copy if the import fails.
- Coach reports leave out photos and private notes unless you switch them on. They do include the profile answers, aspirations, and reviewed targets, because a parent, coach, or clinician needs them; share the file only with people you trust.
- **The plan file** (More, Backup) holds the week and the example meals. It is created only when you ask for it.

## App lock

The optional PIN (PBKDF2 hashed, never stored in plain text) hides the app after a period of inactivity. It is a privacy convenience, not encryption. The iPhone passcode and device encryption protect the stored data. A forgotten PIN can only be cleared by erasing PeakForm's data and restoring a backup.

## Storage durability

PeakForm asks the browser for persistent storage. iOS may still remove website data when the phone runs very low on space, and Safari can clear data for a site used in a tab after about a week without a visit. Home Screen use and regular backups are the protection.

## Safe rendering

Notes and imported text are rendered as text, never as HTML. Imports are validated against typed schemas, and invalid records are skipped and listed. CSV exports neutralise spreadsheet formula injection.

## Repository hygiene

The private setup file is generated into `private/`, which is gitignored. Example backups in `fixtures/` contain only synthetic demo data.

Public documentation (RESEARCH.md, TRAINING_AUDIT.md, NUTRITION_DATA_AUDIT.md, and the guides) uses de-identified examples only: no name, age, measurements, health details, food history, or answers from the phone. App text describes features in general terms, for example "a wrist injury" rather than anyone's injury. Before every release, tracked files are checked against a private list of personal markers kept in `private/`, and the build gate checks the deployed files.
