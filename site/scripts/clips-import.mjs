#!/usr/bin/env node
// Register encoded character clips in src/data/media.json (run after scripts/encode-otto.sh).
// Usage: node scripts/clips-import.mjs <otto|vee> <key> [key…] [--loop key,key]
//   For each key, points av1/hevc (and *_hd when present) at public/media/<who>/<key>.*, reads the duration,
//   and drops any placeholder `alias`/`pending`, so the site switches from the stand-in clip to the real one.
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const li = args.indexOf('--loop');
const loops = new Set(li >= 0 ? (args.splice(li, 2)[1] ?? '').split(',') : []);
const [who, ...keys] = args;
if (!who || !keys.length) throw new Error('usage: clips-import.mjs <otto|vee> <key> [key…] [--loop a,b]');
const p = join(root, 'src/data/media.json');
const m = JSON.parse(readFileSync(p, 'utf8'));
const set = m[who];
if (!set) throw new Error(`no character set "${who}"`);
for (const k of keys) {
  const rel = (s) => `${who}/${k}${s}`;
  const abs = (s) => join(root, 'public', m.base, rel(s));
  if (!existsSync(abs('.av1.mp4')) || !existsSync(abs('.hevc.mp4'))) {
    console.warn(`skip ${k}: not encoded`);
    continue;
  }
  const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', abs('.hevc.mp4')]).toString().trim());
  const prev = set.clips[k] ?? {};
  const { alias: _a, pending: _p, ...keep } = prev;
  set.clips[k] = {
    ...keep,
    av1: rel('.av1.mp4'),
    hevc: rel('.hevc.mp4'),
    ...(existsSync(abs('_hd.av1.mp4')) ? { av1_hd: rel('_hd.av1.mp4'), hevc_hd: rel('_hd.hevc.mp4') } : {}),
    duration: Math.round(dur * 100) / 100,
    ...(loops.has(k) || prev.loop ? { loop: true } : {}),
  };
  console.log(`registered ${who}.${k} (${dur.toFixed(2)} s)`);
}
writeFileSync(p, JSON.stringify(m, null, 2) + '\n');
