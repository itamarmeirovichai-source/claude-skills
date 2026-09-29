import { FOCUS_CHECKS, MUSCLE_IDS, SHOULDER_MUSCLES, type MuscleId } from '../content/muscles';
import type { PlanDay, PlanItem } from '../content/plan';
import type { ActivityKind, FatigueArea } from '../content/types';

// Transparent muscle coverage. Strength work counts as sets. Jumps, sprints, skills,
// swimming, rope, and warm ups count as activity exposure, not as hypertrophy sets.

export const COVERAGE_WEIGHTS = {
  /** One work set where the muscle is a primary mover. */
  primarySet: 1.0,
  /** One work set where the muscle is a secondary mover. */
  secondarySet: 0.5,
} as const;

export const SET_KINDS: ActivityKind[] = ['strength', 'bodyweight', 'hold'];

export interface ExerciseLookup {
  (id: string): { name: string; kind: ActivityKind; primary: MuscleId[]; secondary: MuscleId[]; fatigueOverlap: FatigueArea[] } | undefined;
}

export interface MuscleCoverage {
  muscle: MuscleId;
  direct: number;
  indirect: number;
  exposures: number;
  sources: Array<{ exerciseId: string; name: string; role: 'primary' | 'secondary'; kind: 'sets' | 'exposure'; amount: number; weekday: number }>;
}

export interface CoverageInput {
  weekday: number;
  exerciseId: string;
  /** Completed work sets, or planned sets for plan coverage. */
  sets: number;
}

export function coverageFrom(entries: CoverageInput[], lookup: ExerciseLookup): Record<MuscleId, MuscleCoverage> {
  const out = Object.fromEntries(
    MUSCLE_IDS.map((m) => [m, { muscle: m, direct: 0, indirect: 0, exposures: 0, sources: [] } satisfies MuscleCoverage]),
  ) as unknown as Record<MuscleId, MuscleCoverage>;
  for (const e of entries) {
    const ex = lookup(e.exerciseId);
    if (!ex || e.sets <= 0) continue;
    const countsAsSets = SET_KINDS.includes(ex.kind);
    for (const m of ex.primary) {
      const c = out[m];
      if (countsAsSets) c.direct += e.sets * COVERAGE_WEIGHTS.primarySet;
      else c.exposures += 1;
      c.sources.push({ exerciseId: e.exerciseId, name: ex.name, role: 'primary', kind: countsAsSets ? 'sets' : 'exposure', amount: countsAsSets ? e.sets : 1, weekday: e.weekday });
    }
    for (const m of ex.secondary) {
      const c = out[m];
      if (countsAsSets) c.indirect += e.sets * COVERAGE_WEIGHTS.secondarySet;
      else c.exposures += 1;
      c.sources.push({ exerciseId: e.exerciseId, name: ex.name, role: 'secondary', kind: countsAsSets ? 'sets' : 'exposure', amount: countsAsSets ? e.sets : 1, weekday: e.weekday });
    }
  }
  return out;
}

export function planCoverageInputs(days: PlanDay[]): CoverageInput[] {
  return days.flatMap((d) => d.items.map((it: PlanItem) => ({ weekday: d.weekday, exerciseId: it.exerciseId, sets: it.sets })));
}

export interface FocusResult {
  key: string;
  label: string;
  present: boolean;
  directSets: number;
  indirectSets: number;
  exposures: number;
  exercises: string[];
}

export function focusChecks(cov: Record<MuscleId, MuscleCoverage>): FocusResult[] {
  return FOCUS_CHECKS.map((f) => {
    const rows = f.muscles.map((m) => cov[m]);
    const names = new Set<string>();
    rows.forEach((r) => r.sources.forEach((s) => names.add(s.name)));
    const directSets = rows.reduce((a, r) => a + r.direct, 0);
    const indirectSets = rows.reduce((a, r) => a + r.indirect, 0);
    const exposures = rows.reduce((a, r) => a + r.exposures, 0);
    return { key: f.key, label: f.label, present: directSets + indirectSets + exposures > 0, directSets, indirectSets, exposures, exercises: [...names] };
  });
}

// ---------- Shoulder overlap ----------

export type ShoulderCategory = 'pressing' | 'overhead-hitting' | 'swimming' | 'shoulder-care' | 'raises-and-pulls';

export interface ShoulderDay {
  weekday: number;
  items: Array<{ exerciseId: string; name: string; category: ShoulderCategory; sets: number }>;
}

const OVERHEAD_IDS = new Set(['volleyball-spike', 'medicine-ball-spike-throw', 'block-to-spike-transition']);
const PRESS_IDS = new Set(['barbell-bench-press', 'incline-barbell-bench-press', 'machine-bench-press', 'flat-cable-fly']);
const CARE_IDS = new Set(['cable-external-rotation', 'face-pull', 'reverse-machine-fly']);

export function shoulderCategory(exerciseId: string, kind: ActivityKind, muscles: MuscleId[], overlap: FatigueArea[]): ShoulderCategory | null {
  if (kind === 'swim') return 'swimming';
  if (OVERHEAD_IDS.has(exerciseId)) return 'overhead-hitting';
  if (PRESS_IDS.has(exerciseId)) return 'pressing';
  if (CARE_IDS.has(exerciseId)) return 'shoulder-care';
  if (kind === 'warmup' || kind === 'conditioning') return null;
  if (overlap.includes('shoulder') || muscles.some((m) => SHOULDER_MUSCLES.includes(m))) return 'raises-and-pulls';
  return null;
}

export function shoulderOverlap(entries: CoverageInput[], lookup: ExerciseLookup): { days: ShoulderDay[]; notes: string[] } {
  const days: ShoulderDay[] = [0, 1, 2, 3, 4, 5, 6].map((weekday) => ({ weekday, items: [] }));
  for (const e of entries) {
    const ex = lookup(e.exerciseId);
    if (!ex) continue;
    const cat = shoulderCategory(e.exerciseId, ex.kind, [...ex.primary, ...ex.secondary], ex.fatigueOverlap);
    if (cat) days[e.weekday]!.items.push({ exerciseId: e.exerciseId, name: ex.name, category: cat, sets: e.sets });
  }
  const notes: string[] = [];
  const has = (d: ShoulderDay, c: ShoulderCategory) => d.items.some((i) => i.category === c);
  const names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  for (const d of days) {
    if (has(d, 'pressing') && has(d, 'swimming')) notes.push(`${names[d.weekday]} has pressing and swimming. Keep the swim easy and separate it by at least three hours.`);
    if (has(d, 'overhead-hitting') && has(d, 'swimming')) notes.push(`${names[d.weekday]} has spiking and swimming. Watch for shoulder fatigue and keep the swim easy.`);
    if (has(d, 'overhead-hitting') && has(d, 'pressing')) notes.push(`${names[d.weekday]} has spiking and pressing on the same day.`);
  }
  for (let i = 0; i < 7; i++) {
    const a = days[i]!;
    const b = days[(i + 1) % 7]!;
    if (has(a, 'pressing') && has(b, 'overhead-hitting')) notes.push(`Pressing on ${names[a.weekday]} is followed by spiking on ${names[b.weekday]}. Stop spikes early if the shoulder feels tired.`);
  }
  return { days, notes };
}
