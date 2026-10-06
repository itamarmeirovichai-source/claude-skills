import type { ActivityKind, LoadIncrementClass } from '../content/types';

// Transparent double progression. Every suggestion carries its reason and must be
// confirmed by the user before any target changes. Nothing here writes to the plan.

export interface EquipmentIncrements {
  /** Smallest total load step for a barbell, e.g. 2.5 kg (1.25 kg each side). */
  barbellKg: number;
  machineKg: number;
  cableKg: number;
  dumbbellKg: number;
  /** Default percentage increase for upper body loads (0.025 = 2.5 percent). */
  upperPct: number;
  /** Default percentage increase for lower body loads. */
  lowerPct: number;
}

export const DEFAULT_INCREMENTS: EquipmentIncrements = {
  barbellKg: 2.5,
  machineKg: 2.5,
  cableKg: 2.5,
  dumbbellKg: 2,
  upperPct: 0.025,
  lowerPct: 0.05,
};

export type EquipmentType = 'barbell' | 'machine' | 'cable' | 'dumbbell' | 'bodyweight';

export interface Prescription {
  kind: ActivityKind;
  sets: number;
  repMin: number;
  repMax: number;
  /** Prescribed reps in reserve. */
  rir: number | null;
  /** Reps in reserve for the last set, when it differs (0 means the last set goes to failure). */
  lastSetRir?: number | null;
  perSide: boolean;
  loadIncrement: LoadIncrementClass;
  equipment: EquipmentType;
  holdSeconds?: number;
}

export interface WorkSet {
  setIndex: number;
  side: 'left' | 'right' | null;
  weightKg: number | null;
  reps: number | null;
  rir: number | null;
  seconds?: number | null;
  form: 'good' | 'acceptable' | 'poor' | null;
  pain: 'none' | 'mild' | 'stop';
  painScore?: number | null;
  quality?: number | null;
  landing?: 'good' | 'ok' | 'poor' | null;
}

export type SuggestionKind =
  | 'add_reps'
  | 'add_load'
  | 'hold'
  | 'reduce'
  | 'pain_hold'
  | 'quality_hold'
  | 'coach_review'
  | 'complete_sets';

export interface Target {
  setIndex: number;
  side: 'left' | 'right' | null;
  reps: number | null;
  weightKg: number | null;
  seconds: number | null;
}

export interface Suggestion {
  kind: SuggestionKind;
  title: string;
  reason: string;
  targets: Target[];
  /** Always true. Targets never change without confirmation. */
  requiresConfirmation: true;
}

export function incrementFor(equipment: EquipmentType, inc: EquipmentIncrements): number {
  switch (equipment) {
    case 'barbell':
      return inc.barbellKg;
    case 'machine':
      return inc.machineKg;
    case 'cable':
      return inc.cableKg;
    case 'dumbbell':
      return inc.dumbbellKg;
    case 'bodyweight':
      return 0;
  }
}

const round2 = (n: number) => Math.round(n * 100) / 100;

/**
 * Smallest practical load increase. The percentage rule sets the size, the equipment
 * step decides what is possible: the increase is rounded down to the equipment grid
 * but is never smaller than one step.
 */
export function nextLoad(currentKg: number, cls: LoadIncrementClass, equipment: EquipmentType, inc: EquipmentIncrements = DEFAULT_INCREMENTS): number {
  const step = incrementFor(equipment, inc);
  if (step <= 0) return currentKg;
  const pct = cls === 'lower' ? inc.lowerPct : inc.upperPct;
  const raw = currentKg * pct;
  const steps = Math.max(1, Math.floor(raw / step + 1e-9));
  return round2(currentKg + steps * step);
}

/** A small reduction, one equipment step or about 5 percent, never below zero. */
export function reducedLoad(currentKg: number, equipment: EquipmentType, inc: EquipmentIncrements = DEFAULT_INCREMENTS): number {
  const step = incrementFor(equipment, inc);
  if (step <= 0) return currentKg;
  const pctSteps = Math.max(1, Math.round((currentKg * 0.05) / step));
  return Math.max(0, round2(currentKg - pctSteps * step));
}

function groupBySide(sets: WorkSet[], perSide: boolean): Array<{ side: 'left' | 'right' | null; sets: WorkSet[] }> {
  if (!perSide) return [{ side: null, sets: [...sets].sort((a, b) => a.setIndex - b.setIndex) }];
  const left = sets.filter((s) => s.side === 'left').sort((a, b) => a.setIndex - b.setIndex);
  const right = sets.filter((s) => s.side === 'right').sort((a, b) => a.setIndex - b.setIndex);
  return [
    { side: 'left', sets: left },
    { side: 'right', sets: right },
  ];
}

const sideLabel = (s: 'left' | 'right' | null) => (s === 'left' ? 'Left side: ' : s === 'right' ? 'Right side: ' : '');

function repList(sets: WorkSet[]): string {
  return sets.map((s) => s.reps ?? 0).join(', ');
}

function hold(title: string, reason: string, groups: ReturnType<typeof groupBySide>, load: (g: WorkSet[]) => number | null): Suggestion {
  return {
    kind: 'hold',
    title,
    reason,
    targets: groups.flatMap((g) =>
      g.sets.map((s) => ({ setIndex: s.setIndex, side: g.side, reps: s.reps, weightKg: load(g.sets), seconds: s.seconds ?? null })),
    ),
    requiresConfirmation: true,
  };
}

/**
 * Suggest the next target for one exercise from its most recent exposure.
 * Only work sets should be passed in. Warm up sets never count.
 */
export function suggestNext(p: Prescription, sets: WorkSet[], inc: EquipmentIncrements = DEFAULT_INCREMENTS): Suggestion {
  const groups = groupBySide(sets, p.perSide);

  // Pain always blocks progression.
  const pained = sets.filter((s) => s.pain !== 'none' || (s.painScore ?? 0) > 0);
  if (pained.length > 0) {
    const severe = sets.some((s) => s.pain === 'stop' || (s.painScore ?? 0) >= 4);
    return {
      kind: 'pain_hold',
      title: severe ? 'Pause this exercise and tell a parent or coach' : 'No progression while there is pain',
      reason: severe
        ? 'Pain of 4 out of 10 or more, or pain that made you stop, was logged. Pause this exercise until a parent, coach, or clinician has looked at it.'
        : `Mild pain was logged on ${pained.length} set${pained.length === 1 ? '' : 's'}. Keep the same target and watch whether it settles. If it worsens or changes your technique, pause the exercise and tell a parent or coach.`,
      targets: [],
      requiresConfirmation: true,
    };
  }

  // Quality based activities never progress volume automatically.
  if (p.kind === 'jump' || p.kind === 'sprint' || p.kind === 'skill' || p.kind === 'throw' || p.kind === 'conditioning' || p.kind === 'warmup') {
    const poorLanding = sets.some((s) => s.landing === 'poor');
    const lowQuality = sets.some((s) => (s.quality ?? 5) <= 2);
    return {
      kind: 'quality_hold',
      title: 'Keep the same volume and chase quality',
      reason:
        poorLanding || lowQuality
          ? 'Some reps had poor landing or low quality. Keep the same volume and stop the set earlier when quality drops.'
          : 'Jump, sprint, and skill volume does not increase automatically. Aim for better height, speed, approach consistency, and landing.',
      targets: [],
      requiresConfirmation: true,
    };
  }
  if (p.kind === 'swim') {
    return {
      kind: 'hold',
      title: 'Keep two sets of ten round trips',
      reason: 'Swimming distance is not increased from completion alone. A parent, coach, or qualified professional can change it.',
      targets: [],
      requiresConfirmation: true,
    };
  }

  // All prescribed work sets must be logged, per side when relevant.
  for (const g of groups) {
    if (g.sets.length < p.sets) {
      return {
        kind: 'complete_sets',
        title: 'Complete all work sets first',
        reason: `${sideLabel(g.side)}${g.sets.length} of ${p.sets} work sets were logged. Progression is judged on complete sessions only.`,
        targets: [],
        requiresConfirmation: true,
      };
    }
  }

  // Holds progress seconds within the prescription, never automatically beyond it.
  if (p.kind === 'hold') {
    const target = p.holdSeconds ?? 0;
    const allHit = sets.every((s) => (s.seconds ?? 0) >= target && s.form === 'good');
    return {
      kind: 'hold',
      title: allHit ? 'Hold steady at the prescribed time' : 'Build toward the prescribed time',
      reason: allHit
        ? `Every set reached ${target} seconds with good form. Stay here. A harder variation is a decision for you and your coach.`
        : `Aim for ${target} seconds on every set with good form before thinking about anything harder.`,
      targets: groups.flatMap((g) => g.sets.map((s) => ({ setIndex: s.setIndex, side: g.side, reps: null, weightKg: null, seconds: target }))),
      requiresConfirmation: true,
    };
  }

  const rirTarget = p.rir ?? 0;
  const lastRir = p.lastSetRir ?? null;
  const targetFor = (s: WorkSet) => (lastRir !== null && s.setIndex === p.sets - 1 ? lastRir : rirTarget);
  // Sets taken to failure lose reps from set to set, so progress is judged on the first set.
  const failureMode = rirTarget === 0 || lastRir === 0;
  const firstSets = groups.map((g) => ({ side: g.side, set: g.sets[0]! }));
  const workingLoad = (g: WorkSet[]): number | null => {
    const loads = g.map((s) => s.weightKg).filter((w): w is number => w !== null);
    return loads.length ? Math.min(...loads) : null;
  };

  // Loads varied between sets: judge conservatively at the lowest load.
  for (const g of groups) {
    const loads = new Set(g.sets.map((s) => s.weightKg ?? -1));
    if (loads.size > 1) {
      return hold(
        'Use one load for all work sets',
        `${sideLabel(g.side)}Loads changed between sets. Next time use ${workingLoad(g.sets)} kg for every work set so the sessions can be compared.`,
        groups,
        workingLoad,
      );
    }
  }

  const unrecorded = sets.filter((s) => s.reps === null || (p.rir !== null && s.rir === null) || s.form === null);
  if (unrecorded.length > 0) {
    return hold(
      'Log reps, reps in reserve, and form',
      `${unrecorded.length} set${unrecorded.length === 1 ? ' is' : 's are'} missing reps, reps in reserve, or form. PeakForm only suggests progress from complete information.`,
      groups,
      workingLoad,
    );
  }

  const poorForm = sets.filter((s) => s.form === 'poor');
  const rirMissed = sets.filter((s) => s.rir !== null && s.rir < targetFor(s));
  const loadedExercise = p.equipment !== 'bodyweight';

  if (poorForm.length > 0 || rirMissed.length > 0) {
    const bad = poorForm.length > 0 && rirMissed.length > 0;
    const severeRir = sets.some((s) => s.rir !== null && s.rir <= Math.max(0, rirTarget - 2));
    if (loadedExercise && (bad || severeRir)) {
      return {
        kind: 'reduce',
        title: 'Take a small step back in load',
        reason: `${poorForm.length ? `Form was poor on ${poorForm.length} set${poorForm.length === 1 ? '' : 's'}. ` : ''}${rirMissed.length ? `Reps in reserve fell below the prescribed ${rirTarget} on ${rirMissed.length} set${rirMissed.length === 1 ? '' : 's'}. ` : ''}A slightly lighter load lets you keep the target effort and clean technique.`,
        targets: groups.flatMap((g) => {
          const w = workingLoad(g.sets);
          return g.sets.map((s) => ({ setIndex: s.setIndex, side: g.side, reps: p.repMin, weightKg: w === null ? null : reducedLoad(w, p.equipment, inc), seconds: null }));
        }),
        requiresConfirmation: true,
      };
    }
    return hold(
      'Hold the load',
      `${poorForm.length ? `Form was poor on ${poorForm.length} set${poorForm.length === 1 ? '' : 's'}. ` : ''}${rirMissed.length ? `Reps in reserve fell below the prescribed ${rirTarget}. ` : ''}Repeat the same load and aim for the same reps with the prescribed effort and good form.`,
      groups,
      workingLoad,
    );
  }

  const acceptable = sets.filter((s) => s.form !== 'good');
  if (acceptable.length > 0) {
    return hold(
      'Repeat and aim for good form',
      `Form was marked acceptable on ${acceptable.length} set${acceptable.length === 1 ? '' : 's'}. Progression needs good technique on every work set.`,
      groups,
      workingLoad,
    );
  }

  if (failureMode) return failureProgress(p, groups, firstSets, workingLoad, loadedExercise, inc);

  const below = sets.filter((s) => (s.reps ?? 0) < p.repMin);
  if (below.length > 0) {
    return {
      kind: 'hold',
      title: 'Reach the bottom of the range first',
      reason: `${below.length} set${below.length === 1 ? ' was' : 's were'} below ${p.repMin} reps. Keep the load and aim for at least ${p.repMin} reps on every set.`,
      targets: groups.flatMap((g) =>
        g.sets.map((s) => ({ setIndex: s.setIndex, side: g.side, reps: Math.max(s.reps ?? 0, p.repMin), weightKg: workingLoad(g.sets), seconds: null })),
      ),
      requiresConfirmation: true,
    };
  }

  // Every side qualifies for a load increase only when all its sets reach the top.
  const topReached = groups.map((g) => g.sets.every((s) => (s.reps ?? 0) >= p.repMax));
  const allTop = topReached.every(Boolean);

  if (allTop && loadedExercise) {
    const targets = groups.flatMap((g) => {
      const w = workingLoad(g.sets);
      return g.sets.map((s) => ({
        setIndex: s.setIndex,
        side: g.side,
        reps: p.repMin,
        weightKg: w === null ? null : nextLoad(w, p.loadIncrement, p.equipment, inc),
        seconds: null,
      }));
    });
    const from = workingLoad(groups[0]!.sets);
    const to = targets[0]?.weightKg;
    return {
      kind: 'add_load',
      title: `Try ${to} kg`,
      reason: `Every work set${p.perSide ? ' on both sides' : ''} reached ${p.repMax} reps at ${rirTarget} or more reps in reserve with good form and no pain. The smallest practical increase from ${from} kg is ${to} kg. Start again near ${p.repMin} reps.`,
      targets,
      requiresConfirmation: true,
    };
  }

  if (allTop && !loadedExercise) {
    return hold(
      'Top of the range reached',
      `Every set reached ${p.repMax} reps with good form. Stay here. A harder variation or added load is a decision for you and your coach.`,
      groups,
      () => null,
    );
  }

  // Add one rep to the lowest set that is not yet at the top, per side.
  const targets: Target[] = [];
  const notes: string[] = [];
  for (const g of groups) {
    const w = workingLoad(g.sets);
    const reps = g.sets.map((s) => s.reps ?? 0);
    let lowestIdx = -1;
    for (let i = 0; i < reps.length; i++) {
      if (reps[i]! < p.repMax && (lowestIdx === -1 || reps[i]! < reps[lowestIdx]!)) lowestIdx = i;
    }
    const next = reps.map((r, i) => (i === lowestIdx ? r + 1 : r));
    g.sets.forEach((s, i) => targets.push({ setIndex: s.setIndex, side: g.side, reps: next[i]!, weightKg: w, seconds: null }));
    if (lowestIdx >= 0) notes.push(`${sideLabel(g.side)}${repList(g.sets)} becomes ${next.join(', ')}`);
  }
  const partialSides = p.perSide && topReached.some(Boolean) && !allTop;
  return {
    kind: 'add_reps',
    title: 'Add one rep at the same load',
    reason: `All work sets were within ${p.repMin} to ${p.repMax} reps at the prescribed effort with good form and no pain. ${notes.join('. ')}.${partialSides ? ' One side reached the top, but both sides must qualify before the load goes up.' : ''} The load increases only when every work set reaches ${p.repMax} reps.`,
    targets,
    requiresConfirmation: true,
  };
}

/**
 * Progression for sets taken to failure. Later sets naturally lose reps, so the first set of each
 * side decides: below the range holds, the top of the range adds load, anything else asks for one
 * more rep on the first set. Every other set simply goes to failure again.
 */
function failureProgress(
  p: Prescription,
  groups: ReturnType<typeof groupBySide>,
  firstSets: Array<{ side: 'left' | 'right' | null; set: WorkSet }>,
  workingLoad: (g: WorkSet[]) => number | null,
  loadedExercise: boolean,
  inc: EquipmentIncrements,
): Suggestion {
  const firstBelow = firstSets.filter((f) => (f.set.reps ?? 0) < p.repMin);
  if (firstBelow.length > 0) {
    return {
      kind: 'hold',
      title: 'Reach the bottom of the range first',
      reason: `The first set reached ${firstBelow.map((f) => `${sideLabel(f.side)}${f.set.reps ?? 0}`).join(', ')} reps, below ${p.repMin}. Keep the load and aim for at least ${p.repMin} reps on the first set.`,
      targets: groups.flatMap((g) => g.sets.map((s, i) => ({ setIndex: s.setIndex, side: g.side, reps: i === 0 ? p.repMin : s.reps, weightKg: workingLoad(g.sets), seconds: null }))),
      requiresConfirmation: true,
    };
  }
  const allTop = firstSets.every((f) => (f.set.reps ?? 0) >= p.repMax);
  if (allTop && loadedExercise) {
    const targets = groups.flatMap((g) => {
      const w = workingLoad(g.sets);
      return g.sets.map((s) => ({ setIndex: s.setIndex, side: g.side, reps: p.repMin, weightKg: w === null ? null : nextLoad(w, p.loadIncrement, p.equipment, inc), seconds: null }));
    });
    const from = workingLoad(groups[0]!.sets);
    const to = targets[0]?.weightKg;
    return {
      kind: 'add_load',
      title: `Try ${to} kg`,
      reason: `The first set${p.perSide ? ' on both sides' : ''} reached ${p.repMax} reps with good form and no pain. The smallest practical increase from ${from} kg is ${to} kg. Start again near ${p.repMin} reps and keep taking the sets to clean failure as prescribed.`,
      targets,
      requiresConfirmation: true,
    };
  }
  if (allTop) {
    return hold(
      'Top of the range reached',
      `The first set reached ${p.repMax} reps with good form. Stay here. A harder variation or added load is a decision for you and your coach.`,
      groups,
      () => null,
    );
  }
  const notes: string[] = [];
  const targets: Target[] = [];
  for (const g of groups) {
    const w = workingLoad(g.sets);
    g.sets.forEach((s, i) => targets.push({ setIndex: s.setIndex, side: g.side, reps: i === 0 ? Math.min(p.repMax, (s.reps ?? 0) + 1) : s.reps, weightKg: w, seconds: null }));
    notes.push(`${sideLabel(g.side)}first set ${g.sets[0]!.reps ?? 0} becomes ${Math.min(p.repMax, (g.sets[0]!.reps ?? 0) + 1)}`);
  }
  return {
    kind: 'add_reps',
    title: 'One more rep on the first set',
    reason: `Sets to failure lose reps from set to set, so progress is judged on the first set. ${notes.join('. ')}. The load goes up when the first set reaches ${p.repMax} reps.`,
    targets,
    requiresConfirmation: true,
  };
}

/**
 * While a clinician has not cleared the wrist, exercises that grip or press a load keep their load
 * (3.0.0). A suggestion to add load becomes a hold; adding reps inside the range stays possible.
 */
export function wristGate(s: Suggestion, holdsLoad: boolean): Suggestion {
  if (!holdsLoad || s.kind !== 'add_load') return s;
  return {
    kind: 'hold',
    title: 'Same load until the wrist is cleared',
    reason: `${s.reason} The load stays the same for now, because this exercise grips or presses a load and a clinician has not confirmed that the wrist is cleared. Record the clearance in More, Your profile.`,
    targets: [],
    requiresConfirmation: true,
  };
}
