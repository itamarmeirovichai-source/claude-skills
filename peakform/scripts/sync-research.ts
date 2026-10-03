// Keeps the "Product decision" lines in RESEARCH.md identical to src/content/sources.ts,
// so the document never claims a feature the app does not have.
import { readFileSync, writeFileSync } from 'node:fs';
import { SOURCES } from '../src/content/sources';

const lines = readFileSync('RESEARCH.md', 'utf8').split('\n');
let changed = 0;
for (let i = 0; i < lines.length; i++) {
  const m = lines[i]!.match(/^### \[.*\]\((.*)\)\s*$/);
  if (!m) continue;
  const src = SOURCES.find((s) => s.url === m[1]);
  if (!src) continue;
  for (let j = i + 1; j < Math.min(lines.length, i + 12); j++) {
    if (lines[j]!.startsWith('### ')) break;
    if (lines[j]!.startsWith('- Product decision:')) {
      const next = `- Product decision: ${src.productDecision}`;
      if (lines[j] !== next) {
        lines[j] = next;
        changed++;
      }
      break;
    }
  }
}
writeFileSync('RESEARCH.md', lines.join('\n'));
console.log(`RESEARCH.md product decisions updated: ${changed}`);
