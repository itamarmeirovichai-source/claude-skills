import { ATHLETIC_EXERCISES } from './exercises/athletic';
import { LOWER_EXERCISES } from './exercises/lower';
import { UPPER_EXERCISES } from './exercises/upper';
import { MORNING_EXERCISES } from './exercises/morning';
import type { ExerciseContent } from './types';
import type { CustomExercise } from '../db/records';
import type { EquipmentType, Prescription } from '../domain/progression';
import type { PlanItem } from './plan';
import type { MuscleId } from './muscles';

export const LIBRARY: ExerciseContent[] = [...LOWER_EXERCISES, ...UPPER_EXERCISES, ...ATHLETIC_EXERCISES, ...MORNING_EXERCISES];
export const EXERCISE_BY_ID: Record<string, ExerciseContent> = Object.fromEntries(LIBRARY.map((e) => [e.id, e]));

let customs: Record<string, ExerciseContent> = {};

/** Custom exercises made in the app become minimal library entries. */
export function registerCustomExercises(list: CustomExercise[]): void {
  customs = Object.fromEntries(
    list.map((c) => [
      c.id,
      {
        id: c.id,
        name: c.name,
        kind: c.kind,
        purpose: c.notes || 'Custom exercise.',
        equipment: c.equipment ? [c.equipment] : [],
        setup: [],
        steps: [],
        breathing: '',
        tempo: '',
        rangeOfMotion: '',
        muscles: { primary: c.primary as MuscleId[], secondary: c.secondary as MuscleId[] },
        emphasisNote: 'Custom entry. Muscle mapping was chosen by you.',
        movementPattern: 'general_preparation',
        joints: [],
        laterality: c.logSides ? 'unilateral' : 'bilateral',
        logSides: c.logSides,
        fatigueOverlap: [],
        commonMistakes: [],
        goodFormFeels: '',
        stopRules: ['Stop when technique changes, pain appears, or you reach the prescribed reps in reserve.'],
        safetyNotes: [],
        easierSubstitution: { exerciseId: null, name: 'Ask your coach', reason: 'Custom exercise.' },
        equipmentSubstitution: { exerciseId: null, name: 'Ask your coach', reason: 'Custom exercise.' },
        loadIncrement: c.loadIncrement,
        visual: {},
      } satisfies ExerciseContent,
    ]),
  );
}

export function exercise(id: string): ExerciseContent | undefined {
  return EXERCISE_BY_ID[id] ?? customs[id];
}

export function exerciseName(id: string): string {
  return exercise(id)?.name ?? id;
}

export function allExercises(): ExerciseContent[] {
  return [...LIBRARY, ...Object.values(customs)];
}

export function equipmentType(ex: ExerciseContent): EquipmentType {
  if (ex.kind !== 'strength') return 'bodyweight';
  const eq = ex.equipment.join(' ').toLowerCase();
  if (/barbell|ez bar/.test(eq)) return 'barbell';
  if (/dumbbell/.test(eq)) return 'dumbbell';
  if (/cable|pulley/.test(eq)) return 'cable';
  if (/machine|leverage|stack|sled|hack/.test(eq)) return 'machine';
  return 'machine';
}

export function prescriptionFor(item: PlanItem, ex: ExerciseContent): Prescription {
  const t = item.target;
  return {
    kind: ex.kind,
    sets: item.sets,
    repMin: t.type === 'reps' ? t.min : 0,
    repMax: t.type === 'reps' ? t.max : 0,
    rir: item.rir ?? null,
    perSide: ex.logSides || item.per === 'side',
    loadIncrement: ex.loadIncrement,
    equipment: equipmentType(ex),
    holdSeconds: t.type === 'hold' ? t.seconds : undefined,
  };
}

/** Sides to log for a plan item: per side, per direction, or a single entry. */
export function sidesFor(item: PlanItem, ex: ExerciseContent | undefined): Array<'left' | 'right' | null> {
  if (item.per === 'side' || ex?.logSides) return ['left', 'right'];
  if (item.per === 'direction') return ['left', 'right'];
  return [null];
}

export function sideLabel(item: PlanItem, side: 'left' | 'right' | null): string {
  if (side === null) return '';
  if (item.per === 'direction') return side === 'left' ? 'To the left' : 'To the right';
  return side === 'left' ? 'Left' : 'Right';
}
