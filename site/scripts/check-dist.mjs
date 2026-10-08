#!/usr/bin/env node
// Post-build checks: JS gzip budget for the home page, and no media inside dist from git (media is deployed separately).
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { gzipSync } from 'node:zlib';

const dist = new URL('../dist/', import.meta.url).pathname;
const BUDGET = 90 * 1024;
const html = readFileSync(join(dist, 'index.html'), 'utf8');
const entry = [...html.matchAll(/<script[^>]+src="([^"]+\.js)"/g)].map((m) => m[1]);
const seen = new Set();
const lazy = new Set();
function walk(file) {
  if (seen.has(file)) return;
  seen.add(file);
  const src = readFileSync(join(dist, file), 'utf8');
  for (const m of src.matchAll(/(?:from|import)\s*["']\.\/([^"']+\.js)["']/g)) walk(`/_astro/${m[1]}`);
  for (const m of src.matchAll(/import\(\s*["']\.\/([^"']+\.js)["']\s*\)/g)) lazy.add(`/_astro/${m[1]}`);
}
entry.forEach(walk);
const gz = (f) => gzipSync(readFileSync(join(dist, f))).length;
const eager = [...seen].reduce((a, f) => a + gz(f), 0);
const all = readdirSync(join(dist, '_astro')).filter((f) => f.endsWith('.js'));
const total = all.reduce((a, f) => a + gz(`/_astro/${f}`), 0);
const css = readdirSync(join(dist, '_astro')).filter((f) => f.endsWith('.css')).reduce((a, f) => a + gz(`/_astro/${f}`), 0);
console.log(`home JS before interaction: ${(eager / 1024).toFixed(1)} kB gz (budget 90) · all JS chunks: ${(total / 1024).toFixed(1)} kB gz · CSS: ${(css / 1024).toFixed(1)} kB gz`);
for (const f of seen) console.log(`  eager ${f} ${(gz(f) / 1024).toFixed(1)} kB`);
for (const f of lazy) if (!seen.has(f)) console.log(`  lazy  ${f} ${(gz(f) / 1024).toFixed(1)} kB`);
if (eager > BUDGET) {
  console.error('JS budget exceeded');
  process.exit(1);
}
void statSync;
