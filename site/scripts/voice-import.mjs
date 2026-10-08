#!/usr/bin/env node
// Convert voice masters into public/media/voice/<key>.m4a + .vtt and record them in src/data/media.json.
//
//   node scripts/voice-import.mjs <dir>
//       Imports every key already listed in media.json → voice that has <dir>/<key>.mp3.
//   node scripts/voice-import.mjs --bank <lines.json> <dir>
//       Voice bank: lines.json is { char: { group: [text, …] } } and the files are <dir>/<char>_<group>_<n>.mp3
//       (n from 1). Adds each line as voice key <char>_<group>_<n> and lists it under voiceGroups["<char>.<group>"],
//       which the site draws from with a per-session shuffle bag (no repeats until the group runs out).
//
// Word timings come from <key>.words.json (ElevenLabs) when present; otherwise the VTT is built from the text,
// split into sentences and spread over the audio's real duration (ffprobe).
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const bankIdx = args.indexOf('--bank');
const bankFile = bankIdx >= 0 ? args.splice(bankIdx, 2)[1] : null;
const dir = args[0];
if (!dir) throw new Error('usage: voice-import.mjs [--bank lines.json] <dir>');

const manifestPath = join(root, 'src/data/media.json');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
manifest.voiceGroups ??= {};
const out = join(root, 'public/media/voice');
mkdirSync(out, { recursive: true });

const ts = (s) => {
  const ms = Math.max(0, Math.round(s * 1000));
  const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000), sec = Math.floor((ms % 60000) / 1000);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
};
const duration = (file) => {
  try {
    return Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).toString().trim()) || 2;
  } catch {
    return 2;
  }
};

/** Cues ≤ 42 characters, split on sentence ends. */
function cuesFromWords(words) {
  const cues = [];
  let cur = null;
  for (const w of words) {
    if (!cur || (cur.text + ' ' + w.text).length > 42) {
      cur = { start: w.start, end: w.end, text: w.text };
      cues.push(cur);
    } else {
      cur.text += ' ' + w.text;
      cur.end = w.end;
    }
    if (/[.?!]$/.test(w.text)) cur = null;
  }
  return cues;
}
/** No timings: sentences spread over the duration in proportion to their length. */
function cuesFromText(text, dur) {
  const parts = text.match(/[^.?!]+[.?!]*/g)?.map((s) => s.trim()).filter(Boolean) ?? [text];
  const merged = [];
  for (const p of parts) {
    const last = merged[merged.length - 1];
    if (last && (last + ' ' + p).length <= 42) merged[merged.length - 1] = last + ' ' + p;
    else merged.push(p);
  }
  const total = merged.reduce((a, s) => a + s.length, 0) || 1;
  let t = 0;
  return merged.map((s) => {
    const d = (dur * s.length) / total;
    const c = { start: t, end: t + d, text: s };
    t += d;
    return c;
  });
}

function importOne(key, text, mp3) {
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', mp3, '-c:a', 'aac', '-b:a', '96k', '-ac', '1', '-movflags', '+faststart', join(out, `${key}.m4a`)]);
  const wj = mp3.replace(/\.mp3$/, '.words.json');
  const words = existsSync(wj) ? (JSON.parse(readFileSync(wj, 'utf8')).words ?? []) : [];
  const cues = words.length ? cuesFromWords(words) : cuesFromText(text, duration(mp3));
  const last = cues[cues.length - 1];
  if (last) last.end += 0.4;
  writeFileSync(join(out, `${key}.vtt`), 'WEBVTT\n\n' + cues.map((c) => `${ts(c.start)} --> ${ts(c.end)}\n${c.text}`).join('\n\n') + '\n');
  manifest.voice[key] = { text, audio: `voice/${key}.m4a`, vtt: `voice/${key}.vtt` };
}

let n = 0;
if (bankFile) {
  const bank = JSON.parse(readFileSync(bankFile, 'utf8'));
  for (const [char, groups] of Object.entries(bank)) {
    for (const [group, lines] of Object.entries(groups)) {
      const keys = [];
      lines.forEach((text, i) => {
        const key = `${char}_${group}_${i + 1}`;
        const mp3 = join(dir, `${key}.mp3`);
        if (!existsSync(mp3)) {
          console.warn('missing', key);
          return;
        }
        importOne(key, text, mp3);
        keys.push(key);
        n++;
      });
      if (keys.length) manifest.voiceGroups[`${char}.${group}`] = keys;
    }
  }
} else {
  for (const key of Object.keys(manifest.voice)) {
    const mp3 = join(dir, `${key}.mp3`);
    if (!existsSync(mp3)) continue;
    importOne(key, manifest.voice[key].text, mp3);
    n++;
  }
}
writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
console.log(`imported ${n} voice lines`);
