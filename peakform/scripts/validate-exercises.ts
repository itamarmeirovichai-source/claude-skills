// Structural and copy checks for exercise content files.
// Usage: npx tsx scripts/validate-exercises.ts <module paths...>
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { MUSCLE_IDS } from '../src/content/muscles';
import type { ExerciseContent } from '../src/content/types';
import { LIBRARY_IDS } from '../src/content/exercises/ids';

const problems: string[] = [];
const all: ExerciseContent[] = [];
for (const m of process.argv.slice(2)) {
  const mod = await import(pathToFileURL(resolve(m)).href);
  for (const v of Object.values(mod)) if (Array.isArray(v)) all.push(...(v as ExerciseContent[]));
}
const muscleSet = new Set<string>(MUSCLE_IDS);
const idSet = new Set<string>(LIBRARY_IDS);
const banned: Array<[RegExp, string]> = [
  [/—/, 'em dash'],
  [/–/, 'en dash'],
  [/isolat/i, 'isolation claim'],
  [/!/, 'exclamation mark'],
  [/\bcrush|\bbeast|\bshred|\bnext level|game.?changer|unleash|supercharge/i, 'hype phrase'],
];
for (const ex of all) {
  const where = ex.id ?? '(no id)';
  if (!idSet.has(ex.id)) problems.push(`${where}: id not in LIBRARY_IDS`);
  for (const k of ['purpose', 'breathing', 'tempo', 'rangeOfMotion', 'emphasisNote', 'goodFormFeels'] as const) {
    if (!ex[k] || String(ex[k]).length < 10) problems.push(`${where}: ${k} missing or too short`);
  }
  for (const k of ['equipment', 'setup', 'steps', 'joints', 'commonMistakes', 'stopRules', 'safetyNotes'] as const) {
    if (!Array.isArray(ex[k]) || ex[k].length === 0) problems.push(`${where}: ${k} empty`);
  }
  if (ex.steps.length < 3) problems.push(`${where}: fewer than 3 steps`);
  if (ex.muscles.primary.length === 0) problems.push(`${where}: no primary muscles`);
  for (const mId of [...ex.muscles.primary, ...ex.muscles.secondary]) if (!muscleSet.has(mId)) problems.push(`${where}: unknown muscle ${mId}`);
  const overlap = ex.muscles.primary.filter((m) => ex.muscles.secondary.includes(m));
  if (overlap.length) problems.push(`${where}: muscle both primary and secondary: ${overlap.join(', ')}`);
  for (const s of [ex.easierSubstitution, ex.equipmentSubstitution, ...(ex.otherSubstitutions ?? [])]) {
    if (!s || !s.name || !s.reason) problems.push(`${where}: incomplete substitution`);
    else if (s.exerciseId !== null && !idSet.has(s.exerciseId)) problems.push(`${where}: substitution id ${s.exerciseId} not in library`);
    else if (s.exerciseId === ex.id) problems.push(`${where}: substitutes itself`);
  }
  const v = ex.visual;
  if (!v || ((!v.poses || v.poses.length < 2) && !v.diagram)) problems.push(`${where}: needs at least 2 poses or a diagram`);
  if ((ex.laterality === 'unilateral') !== ex.logSides && ex.laterality !== 'alternating') problems.push(`${where}: unilateral exercises should log sides and bilateral should not`);
  const text = JSON.stringify(ex);
  for (const [re, label] of banned) {
    const m = text.match(re);
    if (m) problems.push(`${where}: ${label}: "${m[0]}"`);
  }
  // Effort: loaded and body weight work must say how close to failure it may go. Failure is only
  // ever described as the last rep with clean form, and never for exercises marked 'never'.
  if (['strength', 'bodyweight', 'hold'].includes(ex.kind) && !ex.failure) problems.push(`${where}: missing failure policy`);
  const failureTalk = /\b(to|until|go to) failure\b/i.test(text.replace(/never taken to failure|short of failure|never to failure/gi, ''));
  if (failureTalk && (ex.failure === undefined || ex.failure === 'never')) problems.push(`${where}: describes failure but its policy is ${ex.failure ?? 'unset'}`);
  if (failureTalk && !/clean form/i.test(text)) problems.push(`${where}: failure must be defined as the last rep with clean form`);
  if (/until failure|grind it out|forced reps/i.test(text)) problems.push(`${where}: unsafe failure wording`);
}
const ids = all.map((e) => e.id);
const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
if (dup.length) problems.push(`duplicate ids: ${dup.join(', ')}`);
console.log(`${all.length} exercises checked.`);
if (problems.length) {
  console.log(problems.map((p) => ' - ' + p).join('\n'));
  process.exit(1);
}
console.log('No problems found.');
