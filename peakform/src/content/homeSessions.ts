import type { LibraryExerciseId } from './exercises/ids';
import type { PlanItem, SetTarget } from './plan';
import type { HomeSetup } from '../domain/athlete';
import { chooseDrill } from '../domain/homeSpace';
import type { WristStatus } from './traits';
import { exerciseName } from './library';

// Home sessions (3.0.0). Jumps, landings, footwork, and volleyball skill practice happen at home,
// never inside a gym strength session. Each slot lists drills in order of preference; the first one
// the room and the wrist allow is planned, and the last options never jump. Jump volume only changes
// when the athlete chooses a new level after a review, never from completion alone.

export type JumpLevel = 'intro' | 'build';

export interface HomeSlot {
  /** Preferred drill first, quieter or no impact options after it. */
  options: LibraryExerciseId[];
  sets: number;
  reps?: number;
  minutes?: number;
  restSec: number;
  per?: 'side' | 'direction';
  notes?: string[];
}

const STOP = 'Stop the drill as soon as height, speed, or landing control drops, even if reps are left.';
const SOFT = 'Land quietly with the knees over the toes.';

/** About 10 minutes: a warm up with landing, balance, and trunk control cut injuries in young athletes by about a third to a half (Rössler 2014). */
const prep: HomeSlot = { options: ['home-movement-prep'], sets: 1, minutes: 10, restSec: 30, notes: ['Skip the jumps today if anything hurts during the warm up.'] };

/**
 * The full approach jump, the most specific jump for the spike (3.0.1). It comes after the approach
 * footwork, with full rest, and only where there is a run up and open sky or a hall. A marked wall
 * gives a touch height; without one, the jump reaches for a spot in the air.
 */
const approach = (sets: number): HomeSlot => ({
  options: ['approach-touch-jump', 'volleyball-approach-jump'],
  sets,
  reps: 3,
  restSec: 120,
  notes: ['Only when the landings earlier in the session were clean.', 'Two easy run ups first, then full effort with full rest.', 'Reach as high as you can and land softly on both feet.', 'Every second week, film one set from the side in slow motion and compare it with the common mistakes on the exercise page: a long, low second to last step, a quick plant, and both arms swinging up.', STOP],
});

/** About 65 foot contacts: the starting level while landings, space, and school jumping are checked. */
const INTRO: HomeSlot[] = [
  prep,
  { options: ['snap-down-stick', 'block-footwork'], sets: 2, reps: 4, restSec: 60, notes: ['Freeze each landing for 2 seconds.', SOFT] },
  { options: ['pogo-hop', 'tibialis-raise'], sets: 2, reps: 10, restSec: 60, notes: ['Small, quick hops from the ankles.', STOP] },
  { options: ['lateral-line-hop', 'shadow-pass-footwork'], sets: 2, reps: 8, restSec: 60, notes: ['Count each landing: 8 is 4 to each side.', STOP] },
  { options: ['countermovement-jump', 'spike-arm-swing-shadow'], sets: 2, reps: 4, restSec: 90, notes: ['About 80 percent effort. Stick each landing.', STOP] },
  { options: ['broad-jump', 'block-footwork'], sets: 2, reps: 3, restSec: 90, notes: ['Stick every landing. Walk back slowly.', STOP] },
  { options: ['volleyball-approach-footwork', 'spike-arm-swing-shadow'], sets: 3, reps: 3, restSec: 45, notes: ['Walk it, then jog it, then three quarter speed, without the jump.'] },
  approach(2),
];

/** About 95 foot contacts. Offered only after a review, never automatically. */
const BUILD: HomeSlot[] = [
  prep,
  { options: ['snap-down-stick', 'block-footwork'], sets: 2, reps: 4, restSec: 60, notes: ['Freeze each landing for 2 seconds.', SOFT] },
  { options: ['pogo-hop', 'tibialis-raise'], sets: 2, reps: 10, restSec: 60, notes: ['Small, quick hops from the ankles.', STOP] },
  { options: ['lateral-line-hop', 'shadow-pass-footwork'], sets: 3, reps: 8, restSec: 60, notes: ['Count each landing: 8 is 4 to each side.', STOP] },
  { options: ['countermovement-jump', 'spike-arm-swing-shadow'], sets: 3, reps: 4, restSec: 90, notes: ['Full effort with full rest. Stick each landing.', STOP] },
  { options: ['broad-jump', 'block-footwork'], sets: 3, reps: 3, restSec: 90, notes: ['Stick every landing.', STOP] },
  { options: ['single-leg-hop', 'shadow-pass-footwork'], sets: 2, reps: 3, restSec: 60, per: 'side', notes: ['Low, controlled hops. Stick the last one.', STOP] },
  { options: ['volleyball-approach-footwork', 'spike-arm-swing-shadow'], sets: 3, reps: 3, restSec: 45, notes: ['Finish with a soft small hop only if the plant is clean.'] },
  approach(3),
];

export const HOME_JUMP_SESSION: Record<JumpLevel, HomeSlot[]> = { intro: INTRO, build: BUILD };

export const JUMP_LEVEL_LABEL: Record<JumpLevel, string> = { intro: 'Starting level, about 65 landings', build: 'Next level, about 95 landings' };

/** The light skill session: rhythm, arm swing, and footwork with no jumps. Ball contact only with a cleared wrist. */
export const HOME_SKILL_SESSION: HomeSlot[] = [
  { ...prep, minutes: 6, notes: [] },
  { options: ['volleyball-approach-footwork', 'shadow-pass-footwork'], sets: 3, reps: 3, restSec: 45, notes: ['Same start mark every rep. Rhythm: slow, quicker, fast plant.'] },
  { options: ['spike-arm-swing-shadow'], sets: 3, reps: 5, restSec: 30, notes: ['Arms back, both up, high elbow, long reach.'] },
  { options: ['wall-spike-control', 'block-footwork'], sets: 3, reps: 8, restSec: 45, notes: ['Half effort. Count the hits that land on the target.'] },
  { options: ['shadow-pass-footwork'], sets: 2, reps: 8, restSec: 45, notes: ['Eight directions per set, exact rather than fast.'] },
];

const r = (n: number): SetTarget => ({ type: 'reps', min: n, max: n });

/** The home session for one day, fitted to the space and the wrist. Drills that fit nowhere are left out. */
export function buildHomeItems(dayKey: string, slots: HomeSlot[], setup: HomeSetup, wrist: WristStatus): PlanItem[] {
  const out: PlanItem[] = [];
  const used = new Set<string>();
  for (const slot of slots) {
    const choice = chooseDrill(slot.options.filter((o) => !used.has(o) || slot.options.length === 1), setup, wrist);
    if (!choice || used.has(choice.exerciseId)) continue;
    used.add(choice.exerciseId);
    const fallback = choice.exerciseId !== slot.options[0];
    const notes = [...(fallback ? [] : slot.notes ?? []), ...(choice.where === 'outdoors' ? ['Outdoors, on a flat, dry surface.'] : [])];
    if (fallback) notes.unshift(`Planned instead of ${exerciseName(slot.options[0]!)}, because ${choice.passed[0]?.reasons.join(' and ') ?? 'it does not fit your space'}.`);
    const item: PlanItem = {
      id: `${dayKey}-home-${out.length + 1}-${choice.exerciseId}`,
      exerciseId: choice.exerciseId,
      session: 'home',
      sets: slot.sets,
      target: slot.minutes ? { type: 'duration', totalMin: slot.minutes } : r(fallback && choice.exerciseId === 'tibialis-raise' ? 15 : slot.reps ?? 1),
      restSec: slot.restSec,
      notes,
    };
    if (slot.per) item.per = slot.per;
    out.push(item);
  }
  return out;
}
