#!/usr/bin/env node
// Lists every file media.json expects and whether it exists in public/media (the site degrades gracefully without them).
import { existsSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
const root = new URL('..', import.meta.url).pathname;
const m = JSON.parse(readFileSync(join(root, 'src/data/media.json'), 'utf8'));
const files = [];
for (const g of ['otto', 'vee']) {
  files.push(m[g].poster);
  for (const c of Object.values(m[g].clips)) for (const k of ['av1', 'hevc', 'av1_hd', 'hevc_hd']) if (c[k]) files.push(c[k]);
}
for (const f of m.films) files.push(f.poster, f.loop.av1, f.loop.h264, f.full.av1, f.full.h264, ...(f.captions ? [f.captions] : []), ...(f.scrub ? [f.scrub] : []));
for (const v of Object.values(m.voice)) files.push(...[v.audio, v.vtt].filter(Boolean));
files.push(...Object.values(m.stills));
let missing = 0;
for (const f of files) {
  const p = join(root, 'public', m.base, f);
  const ok = existsSync(p);
  if (!ok) missing++;
  console.log(`${ok ? 'ok     ' : 'MISSING'} ${f}${ok ? `  ${(statSync(p).size / 1024).toFixed(0)} kB` : ''}`);
}
console.log(`${files.length - missing}/${files.length} present`);
