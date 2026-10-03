import type { DateKey } from './dates';

// The dunk goal in numbers. Heights are fingertip touch heights in centimetres.
// A regulation rim is 305 cm. Coaching sources put the hand about 15 cm above the rim for a
// one hand dunk if you can palm the ball, and about 20 cm or more if you cannot. These are
// rough figures, not research, so the app treats them as targets to test against.

export const RIM_CM = 305;

/** Approach jumps that log the height touched. */
export const TOUCH_EXERCISES = ['approach-touch-jump', 'volleyball-approach-jump'] as const;

export interface DunkProfile {
  standingReachCm: number | null;
  canPalm: boolean;
}

export const DEFAULT_DUNK_PROFILE: DunkProfile = { standingReachCm: null, canPalm: false };

export function dunkTargetCm(canPalm: boolean): number {
  return RIM_CM + (canPalm ? 15 : 20);
}

export interface Touch {
  date: DateKey;
  cm: number;
}

/** The best touch of each day, oldest first. Entries without a height are ignored. */
export function bestTouchPerDay(entries: Array<{ date: DateKey; reachCm: number | null | undefined }>): Touch[] {
  const best = new Map<DateKey, number>();
  for (const e of entries) {
    if (typeof e.reachCm !== 'number' || e.reachCm <= 0) continue;
    best.set(e.date, Math.max(best.get(e.date) ?? 0, e.reachCm));
  }
  return [...best.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([date, cm]) => ({ date, cm }));
}

export interface Milestone {
  key: 'rim' | 'grab' | 'small-ball' | 'dunk';
  label: string;
  cm: number;
  reached: boolean;
}

export interface DunkSummary {
  target: number;
  best: Touch | null;
  latest: Touch | null;
  /** Best touch minus standing reach. */
  approachVertical: number | null;
  /** Centimetres still missing to the dunk target. Zero once it is reached. */
  gap: number | null;
  milestones: Milestone[];
}

export function dunkSummary(touches: Touch[], profile: DunkProfile): DunkSummary {
  const target = dunkTargetCm(profile.canPalm);
  const best = touches.reduce<Touch | null>((b, t) => (!b || t.cm > b.cm ? t : b), null);
  const latest = touches.length ? touches[touches.length - 1]! : null;
  const steps: Array<Omit<Milestone, 'reached'>> = [
    { key: 'rim', label: 'Touch the rim', cm: RIM_CM },
    { key: 'grab', label: 'Grab the rim', cm: RIM_CM + 7 },
    { key: 'small-ball', label: 'Dunk a tennis ball, then a volleyball', cm: RIM_CM + 10 },
    { key: 'dunk', label: profile.canPalm ? 'Dunk a basketball, palming it' : 'Dunk a basketball with two hands or cupped', cm: target },
  ];
  return {
    target,
    best,
    latest,
    approachVertical: best && profile.standingReachCm ? best.cm - profile.standingReachCm : null,
    gap: best ? Math.max(0, target - best.cm) : null,
    milestones: steps.map((m) => ({ ...m, reached: !!best && best.cm >= m.cm })),
  };
}
