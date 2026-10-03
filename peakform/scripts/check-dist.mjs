// Release gate for the static build. Fails when the build contains personal data,
// trackers, or is missing what an offline Home Screen app needs.
// Usage: node scripts/check-dist.mjs dist
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const dir = process.argv[2] ?? 'dist';
const problems = [];
const files = [];
const walk = (d) => {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p);
    else files.push(p);
  }
};
walk(dir);

// Personal data must never ship. Generic check: profile and body fields with real values.
// Optional extra markers can be listed one per line in private/markers.txt, which is gitignored,
// so no personal detail ever has to be written into this public repository.
const personal = [/"(heightCm|startWeightKg|startBodyFatPct|bodyFatPct|weightKg)"\s*:\s*\d/, /"birthYear"\s*:\s*\d/, /"eventLabel"\s*:\s*"[^"]+/];
const markerFile = new URL('../private/markers.txt', import.meta.url);
if (existsSync(markerFile)) {
  for (const line of readFileSync(markerFile, 'utf8').split('\n').map((l) => l.trim()).filter(Boolean)) {
    personal.push(new RegExp(line.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'));
  }
}
// Tracking and error reporting services that must never be present.
const trackers = [/google-analytics/i, /googletagmanager/i, /gtag\(/, /mixpanel/i, /segment\.io/i, /sentry\.io/i, /hotjar/i, /amplitude/i, /plausible\.io/i, /facebook\.net/i];

for (const f of files) {
  if (!/\.(js|html|css|json|webmanifest|txt|svg)$/.test(f)) continue;
  const text = readFileSync(f, 'utf8');
  for (const re of personal) if (re.test(text)) problems.push(`${f}: personal marker ${re}`);
  for (const re of trackers) if (re.test(text)) problems.push(`${f}: tracker ${re}`);
}

for (const need of ['index.html', 'manifest.webmanifest', 'sw.js', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png']) {
  if (!existsSync(join(dir, need))) problems.push(`missing ${need}`);
}
const html = readFileSync(join(dir, 'index.html'), 'utf8');
if (!html.includes('Content-Security-Policy')) problems.push('index.html has no Content Security Policy');
if (!/rel="manifest"/.test(html)) problems.push('index.html does not link the manifest');
const sw = readFileSync(join(dir, 'sw.js'), 'utf8');
if (!sw.includes('index.html')) problems.push('service worker does not precache index.html');
const manifest = JSON.parse(readFileSync(join(dir, 'manifest.webmanifest'), 'utf8'));
if (manifest.display !== 'standalone') problems.push('manifest display is not standalone');

const totalKb = Math.round(files.reduce((a, f) => a + statSync(f).size, 0) / 1024);
if (problems.length) {
  console.error(problems.map((p) => ` - ${p}`).join('\n'));
  process.exit(1);
}
console.log(`dist check passed: ${files.length} files, ${totalKb} KB, no personal markers, no trackers, offline assets present.`);
