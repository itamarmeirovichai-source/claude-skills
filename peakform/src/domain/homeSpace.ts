import type { HomeSetup } from './athlete';
import { HOME_NEEDS, wristAllows, type CeilingLevel, type HomeEquipment, type SpaceNeeds, type SpaceSize, type WristStatus } from '../content/traits';
import type { LibraryExerciseId } from '../content/exercises/ids';

// Matching home drills to the space the athlete actually has. Unknown answers are read as the most
// limited option, so a drill is only planned when the room is known to allow it.

export interface Environment {
  where: 'indoors' | 'outdoors';
  space: SpaceSize;
  ceiling: CeilingLevel;
  /** Highest impact the floor is safe for. */
  maxImpact: 'none' | 'low' | 'moderate';
  /** Only quiet drills: noise limits indoors. */
  quietOnly: boolean;
  /** Ball contact is possible: no people or breakable things nearby. */
  ballOk: boolean;
  equipment: HomeEquipment[];
}

const SPACE_RANK: Record<SpaceSize, number> = { small: 0, medium: 1, large: 2 };
const CEILING_RANK: Record<CeilingLevel, number> = { low: 0, standard: 1, high: 2 };
const IMPACT_RANK = { none: 0, low: 1, moderate: 2, high: 3 } as const;

/** The places a home session can use: indoors, and outdoors when there is a safe outdoor area. */
export function environments(setup: HomeSetup): Environment[] {
  const out: Environment[] = [];
  const indoorImpact: Environment['maxImpact'] = setup.surface === 'mat' || setup.surface === 'carpet' ? 'moderate' : setup.surface === 'hard' ? 'low' : 'none';
  out.push({
    where: 'indoors',
    space: setup.space === 'unknown' ? 'small' : setup.space,
    ceiling: setup.ceiling === 'unknown' ? 'low' : setup.ceiling,
    maxImpact: indoorImpact,
    quietOnly: setup.noiseLimits !== 'no',
    ballOk: setup.breakables === 'no',
    equipment: setup.equipment,
  });
  if (setup.outdoor === 'small' || setup.outdoor === 'large') {
    const outImpact: Environment['maxImpact'] = setup.outdoorSurface === 'grass' || setup.outdoorSurface === 'court' ? 'moderate' : setup.outdoorSurface === 'concrete' ? 'low' : 'none';
    out.push({
      where: 'outdoors',
      space: setup.outdoor === 'large' ? 'large' : 'medium',
      ceiling: 'high',
      maxImpact: outImpact,
      quietOnly: false,
      ballOk: true,
      equipment: setup.equipment,
    });
  }
  return out;
}

/** Why a drill does not fit one environment. An empty list means it fits. */
export function misfits(needs: SpaceNeeds, env: Environment): string[] {
  const out: string[] = [];
  if (SPACE_RANK[env.space] < SPACE_RANK[needs.space]) out.push('not enough clear space');
  if (CEILING_RANK[env.ceiling] < CEILING_RANK[needs.ceiling]) out.push('the ceiling is too low');
  if (IMPACT_RANK[needs.impact] > IMPACT_RANK[env.maxImpact]) out.push(env.maxImpact === 'none' ? 'the floor is not known to be safe for landings' : 'the floor is too hard for these landings');
  if (env.quietOnly && needs.noise !== 'quiet') out.push('it is too loud for the noise limits');
  if (needs.ball && !env.ballOk) out.push('people or breakable things are nearby');
  for (const e of needs.equipment ?? []) if (!env.equipment.includes(e) && !(e === 'wall' && env.where === 'indoors')) out.push(`needs ${e === 'box' ? 'a stable box' : e === 'light-dumbbells' ? 'light dumbbells' : `a ${e}`}`);
  return out;
}

export interface DrillChoice {
  exerciseId: LibraryExerciseId;
  where: Environment['where'];
  /** Drills earlier in the list that were passed over, with the reason. */
  passed: Array<{ exerciseId: LibraryExerciseId; reasons: string[] }>;
}

/**
 * The first drill in a preference list that fits the space and the wrist. Returns null when none
 * fits, so the session simply leaves that slot out.
 */
export function chooseDrill(options: LibraryExerciseId[], setup: HomeSetup, wrist: WristStatus): DrillChoice | null {
  const envs = environments(setup);
  const passed: DrillChoice['passed'] = [];
  for (const id of options) {
    const needs = HOME_NEEDS[id];
    if (!needs) {
      passed.push({ exerciseId: id, reasons: ['not a home drill'] });
      continue;
    }
    if (!wristAllows(id, wrist)) {
      passed.push({ exerciseId: id, reasons: ['the wrist is not cleared for it'] });
      continue;
    }
    const fits = envs.map((env) => ({ env, why: misfits(needs, env) }));
    const ok = fits.find((f) => f.why.length === 0);
    if (ok) return { exerciseId: id, where: ok.env.where, passed };
    passed.push({ exerciseId: id, reasons: [...new Set(fits.flatMap((f) => f.why))] });
  }
  return null;
}
