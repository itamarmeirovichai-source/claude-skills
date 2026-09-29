# Privacy and security

## Where data lives

All personal data, including the profile, measurements, workouts, meals, photos, notes, and reviews, is stored in IndexedDB in the browser on the phone. The deployed website is a set of static files that contains no personal data and never receives any. The release gate (`scripts/check-dist.mjs`) fails the build if personal markers or known trackers appear in the output.

## What never happens

- No account, sign in, or cloud sync.
- No analytics, telemetry, advertising, or third party error reporting.
- No automatic sharing. No assistant can read the phone's data.
- No secrets or API keys in the client.
- No personal data in the service worker cache. It only stores the app's own files.

## When the network is used

| Action | Sent where | What is sent |
| --- | --- | --- |
| Opening or updating the app | The static host | Requests for the app files only |
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
- Coach reports leave out photos and private notes unless you switch them on.

## App lock

The optional PIN (PBKDF2 hashed, never stored in plain text) hides the app after a period of inactivity. It is a privacy convenience, not encryption. The iPhone passcode and device encryption protect the stored data. A forgotten PIN can only be cleared by erasing PeakForm's data and restoring a backup.

## Storage durability

PeakForm asks the browser for persistent storage. iOS may still remove website data when the phone runs very low on space, and Safari can clear data for a site used in a tab after about a week without a visit. Home Screen use and regular backups are the protection.

## Safe rendering

Notes and imported text are rendered as text, never as HTML. Imports are validated against typed schemas, and invalid records are skipped and listed. CSV exports neutralise spreadsheet formula injection.

## Repository hygiene

The private setup file is generated into `private/`, which is gitignored. Example backups in `fixtures/` contain only synthetic demo data.
