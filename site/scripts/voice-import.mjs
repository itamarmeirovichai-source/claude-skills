#!/usr/bin/env node
// Convert voice masters (<key>.mp3 + <key>.words.json word timings) into public/media/voice/<key>.m4a + .vtt.
// Usage: node scripts/voice-import.mjs <dir>
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dir = process.argv[2];
if (!dir) throw new Error('usage: voice-import.mjs <dir>');
const manifest = JSON.parse(readFileSync(join(root, 'src/data/media.json'), 'utf8'));
const out = join(root, 'public/media/voice');
mkdirSync(out, { recursive: true });
const ts = (s) => {
  const ms = Math.round(s * 1000);
  const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000), sec = Math.floor((ms % 60000) / 1000);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
};
let n = 0;
for (const key of Object.keys(manifest.voice)) {
  const mp3 = join(dir, `${key}.mp3`);
  if (!existsSync(mp3)) { console.warn('missing', key); continue; }
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', mp3, '-c:a', 'aac', '-b:a', '96k', '-ac', '1', '-movflags', '+faststart', join(out, `${key}.m4a`)]);
  const wj = join(dir, `${key}.words.json`);
  const words = existsSync(wj) ? JSON.parse(readFileSync(wj, 'utf8')).words ?? [] : [];
  const cues = [];
  let cur = null;
  for (const w of words) {
    // ≤42 characters per cue, split on sentence ends
    if (!cur || (cur.text + ' ' + w.text).length > 42) { cur = { start: w.start, end: w.end, text: w.text }; cues.push(cur); }
    else { cur.text += ' ' + w.text; cur.end = w.end; }
    if (/[.?!]$/.test(w.text)) cur = null;
  }
  if (!cues.length) cues.push({ start: 0, end: 3, text: manifest.voice[key].text });
  const last = cues[cues.length - 1];
  last.end += 0.4;
  writeFileSync(join(out, `${key}.vtt`), 'WEBVTT\n\n' + cues.map((c) => `${ts(c.start)} --> ${ts(c.end)}\n${c.text}`).join('\n\n') + '\n');
  manifest.voice[key].audio = `voice/${key}.m4a`;
  manifest.voice[key].vtt = `voice/${key}.vtt`;
  n++;
}
writeFileSync(join(root, 'src/data/media.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`imported ${n} voice lines`);
