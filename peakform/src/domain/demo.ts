import { FOOD_BY_ID } from '../content/foods';
import { templatesForDay } from '../content/meals';
import type { PlanDay } from '../content/plan';
import type { ActivityKind } from '../content/types';
import type {
  BodyCheckIn,
  ExerciseSession,
  FoodLog,
  PainLog,
  SetLog,
  SleepLog,
  WaistMeasurement,
  WaterLog,
  WorkoutSession,
} from '../db/records';
import { mulberry32 } from '../lib/id';
import { addDays, localDateTime, sleepMinutes, weekdayOf, type DateKey } from './dates';
import { templateItems } from './nutrition';
import { itemFromPortion, hiddenOilItem } from './portions';

// Synthetic demo history. It contains no real person's data and can be removed in one tap.
// Used for the first run demo, example backups, screenshots, and tests.

export interface DemoData {
  sessions: WorkoutSession[];
  exerciseSessions: ExerciseSession[];
  setLogs: SetLog[];
  foodLogs: FoodLog[];
  waterLogs: WaterLog[];
  checkins: BodyCheckIn[];
  waist: WaistMeasurement[];
  sleep: SleepLog[];
  pain: PainLog[];
}

export interface DemoLookup {
  kind: (id: string) => ActivityKind;
  logSides: (id: string) => boolean;
}

const BASE_LOADS: Record<string, number> = {
  'barbell-squat': 50,
  'romanian-deadlift': 50,
  'bulgarian-split-squat': 10,
  'standing-calf-raise': 40,
  'tibialis-raise': 0,
  'pallof-press': 10,
  'hack-squat': 60,
  'barbell-hip-thrust': 60,
  'seated-leg-curl': 30,
  'leg-extension': 30,
  'cable-hip-abduction': 7.5,
  'seated-calf-raise': 30,
  'incline-barbell-bench-press': 35,
  'machine-bench-press': 35,
  'wide-grip-lat-pulldown': 40,
  'leverage-high-row': 40,
  'reverse-machine-fly': 20,
  'lateral-raise': 6,
  'hammer-curl': 10,
  'palm-down-wrist-curl': 10,
  'triceps-pushdown': 20,
  'barbell-bench-press': 40,
  'flat-cable-fly': 10,
  'seated-cable-row': 40,
  'one-arm-lat-pulldown': 20,
  'single-arm-cable-lateral-raise': 5,
  'machine-preacher-curl': 20,
  'palm-up-wrist-curl': 15,
  'rope-overhead-triceps-extension': 15,
  'cable-external-rotation': 5,
  'face-pull': 15,
  // Choices added in 2.0.0.
  'leg-press': 80,
  'smith-squat': 40,
  'dumbbell-romanian-deadlift': 14,
  'smith-romanian-deadlift': 40,
  'walking-lunge': 8,
  'smith-hip-thrust': 40,
  'hip-abduction-machine': 30,
  'adductor-machine': 30,
  'cable-hip-adduction': 7.5,
  'leg-press-calf-raise': 60,
  'cable-crunch': 25,
  'cable-woodchop': 10,
  'incline-machine-press': 30,
  'incline-smith-press': 30,
  'incline-dumbbell-press': 14,
  'dumbbell-bench-press': 14,
  'smith-bench-press': 35,
  'pec-deck-fly': 25,
  'standing-cable-crossover': 10,
  'neutral-grip-pulldown': 40,
  'straight-arm-cable-pulldown': 15,
  'dumbbell-pullover': 12,
  'chest-supported-dumbbell-row': 14,
  'chest-supported-machine-row': 35,
  'machine-lateral-raise': 15,
  'cable-reverse-fly': 7.5,
  'incline-dumbbell-curl': 8,
  'bayesian-cable-curl': 7.5,
  'dumbbell-preacher-curl': 8,
  'rope-hammer-curl': 15,
  'cable-reverse-curl': 10,
  'dumbbell-overhead-triceps-extension': 12,
  'single-arm-cable-overhead-extension': 7.5,
  'single-arm-cable-pushdown': 7.5,
  'dumbbell-shrug': 16,
  'smith-shrug': 30,
  'side-lying-external-rotation': 2,
};

export function generateDemo(planDays: PlanDay[], end: DateKey, weeks: number, lookup: DemoLookup, seed = 7): DemoData {
  const rnd = mulberry32(seed);
  const pick = <T,>(xs: T[]) => xs[Math.floor(rnd() * xs.length)]!;
  const out: DemoData = { sessions: [], exerciseSessions: [], setLogs: [], foodLogs: [], waterLogs: [], checkins: [], waist: [], sleep: [], pain: [] };
  const start = addDays(end, -(weeks * 7 - 1));
  const repState = new Map<string, { load: number; reps: number[] }>();
  let weight = 78.4;
  let waist = 86.5;
  let n = 0;
  const id = (p: string) => `demo-${p}-${(n++).toString(36)}`;

  for (let d = start; d <= end; d = addDays(d, 1)) {
    const wd = weekdayOf(d);
    const day = planDays.find((x) => x.weekday === wd);
    const morning = localDateTime(d, '07:02').getTime();

    // Sleep and check in. Saturday is Sabbath, so the demo logs it later in the evening.
    const bed = pick(['22:20', '22:30', '22:35', '22:45', '23:05', '22:30']);
    const wake = wd === 6 ? '08:00' : '07:00';
    out.sleep.push({ id: id('sleep'), createdAt: morning, updatedAt: morning, date: d, bedtime: bed, wakeTime: wake, durationMin: sleepMinutes(bed, wake), quality: pick([3, 4, 4, 5]) });
    weight += -0.055 + (rnd() - 0.5) * 0.5;
    const logWeight = wd !== 6 && rnd() > 0.12;
    out.checkins.push({
      id: id('checkin'),
      createdAt: morning,
      updatedAt: morning,
      date: d,
      at: morning,
      weightKg: logWeight ? Math.round(weight * 10) / 10 : null,
      bodyFatPct: logWeight && rnd() > 0.5 ? Math.round((21.5 - (d > addDays(start, 14) ? 0.3 : 0) + (rnd() - 0.5) * 1.2) * 10) / 10 : null,
      standardConditions: true,
      energy: pick([3, 4, 4, 5]),
      mood: pick([3, 4, 4, 5]),
      concentration: pick([3, 4, 4]),
      hunger: pick([2, 3, 3, 4]),
      soreness: { legs: wd === 2 || wd === 4 ? pick([1, 2]) : pick([0, 1]), shoulders: pick([0, 0, 1]) },
      illness: false,
      illnessNote: '',
      hydrationNote: '',
      redFlags: [],
      note: '',
    });
    if (wd === 1) {
      waist -= 0.2 + (rnd() - 0.5) * 0.3;
      out.waist.push({ id: id('waist'), createdAt: morning, updatedAt: morning, date: d, cm: Math.round(waist * 10) / 10, standardConditions: true });
    }

    // Training sessions.
    if (day && !day.isRest) {
      for (const sessionKey of ['morning', 'home', 'main', 'swim'] as const) {
        const items = day.items.filter((i) => i.session === sessionKey);
        if (!items.length) continue;
        if (rnd() < 0.06) continue; // an occasional missed session
        const t0 = localDateTime(d, sessionKey === 'morning' ? '07:00' : sessionKey === 'home' ? '16:15' : sessionKey === 'main' ? '17:00' : '20:00').getTime();
        const sid = id('session');
        out.sessions.push({
          id: sid,
          createdAt: t0,
          updatedAt: t0,
          date: d,
          weekday: wd,
          planWeekday: wd,
          planId: 'baseline-v1',
          planVersion: 1,
          session: sessionKey,
          title: sessionKey === 'main' ? day.title : sessionKey === 'morning' ? 'Morning session' : sessionKey === 'home' ? 'Home jumps and skills' : 'Swim',
          status: 'done',
          startedAt: t0,
          finishedAt: t0 + 60 * 60 * 1000,
          planSnapshot: items,
          sessionRpe: sessionKey === 'main' ? pick([6, 7, 7, 8]) : 4,
          recovery: { energy: pick([3, 4]), soreness: pick([0, 1, 1]) },
          poolLengthM: sessionKey === 'swim' ? 25 : null,
          note: '',
          rescheduledFrom: null,
        });
        let t = t0;
        items.forEach((it, order) => {
          const esid = id('ex');
          out.exerciseSessions.push({ id: esid, createdAt: t, updatedAt: t, sessionId: sid, planItemId: it.id, order, exerciseId: it.exerciseId, originalExerciseId: null, substitutionReason: null, skipped: false, skipReason: null, note: '' });
          const kind = lookup.kind(it.exerciseId);
          const sides: Array<'left' | 'right' | null> = lookup.logSides(it.exerciseId) ? ['left', 'right'] : [null];
          const target = it.target;
          const st = repState.get(it.id) ?? { load: BASE_LOADS[it.exerciseId] ?? 0, reps: Array.from({ length: it.sets }, () => (target.type === 'reps' ? target.min + 1 : 0)) };
          for (let si = 0; si < it.sets; si++) {
            for (const side of sides) {
              t += 90_000;
              const isStrength = kind === 'strength' || kind === 'bodyweight';
              const reps = target.type === 'reps' ? (isStrength ? st.reps[si] ?? target.min : target.max) : null;
              out.setLogs.push({
                id: id('set'),
                createdAt: t,
                updatedAt: t,
                sessionId: sid,
                exerciseSessionId: esid,
                exerciseId: it.exerciseId,
                planItemId: it.id,
                setIndex: si,
                side,
                warmup: false,
                weightKg: kind === 'strength' && st.load > 0 ? st.load : null,
                reps,
                rir: it.rir ?? null,
                seconds: target.type === 'hold' ? target.seconds : target.type === 'duration' ? target.totalMin * 60 : null,
                form: 'good',
                pain: 'none',
                painScore: null,
                quality: ['jump', 'sprint', 'skill', 'throw'].includes(kind) ? pick([4, 4, 5, 3]) : null,
                landing: kind === 'jump' ? 'good' : null,
                reachCm: null,
                timeSec: it.exerciseId === 'ten-metre-sprint' ? Math.round((1.95 - rnd() * 0.08) * 100) / 100 : null,
                roundTrips: target.type === 'roundTrips' ? target.count : null,
                stroke: target.type === 'roundTrips' ? 'Freestyle' : null,
                rpe: target.type === 'roundTrips' ? 4 : null,
                symptoms: null,
                note: '',
                completedAt: t,
              });
            }
          }
          // Simple double progression for the demo history.
          if (target.type === 'reps' && kind === 'strength') {
            const lowest = st.reps.indexOf(Math.min(...st.reps));
            if (st.reps.every((r) => r >= target.max)) {
              st.load = Math.round((st.load + (st.load >= 20 ? 2.5 : 1)) * 10) / 10;
              st.reps = st.reps.map(() => target.min);
            } else if (lowest >= 0) st.reps[lowest] = Math.min(target.max, st.reps[lowest]! + 1);
          }
          repState.set(it.id, st);
        });
      }
    }

    // Food.
    const templates = templatesForDay(wd);
    for (const tpl of templates) {
      if (rnd() < 0.07) continue;
      const at = localDateTime(d, tpl.time).getTime();
      out.foodLogs.push({ id: id('food'), createdAt: at, updatedAt: at, date: d, slot: tpl.slot, time: tpl.time, source: 'template', templateId: tpl.id, asPlanned: true, items: templateItems(tpl), photoId: null, note: '', hiddenOil: null });
    }
    if (wd === 6) {
      const at = localDateTime(d, '20:30').getTime();
      for (const meal of ['Sabbath lunch', 'Third meal']) {
        out.foodLogs.push({
          id: id('food'),
          createdAt: at,
          updatedAt: at,
          date: d,
          slot: 'sabbath',
          time: meal === 'Sabbath lunch' ? '12:30' : '17:00',
          source: 'sabbath',
          templateId: 'sabbath-plate',
          asPlanned: true,
          items: [
            itemFromPortion(FOOD_BY_ID['chicken-breast']!, 'palm', 2),
            itemFromPortion(FOOD_BY_ID['rice-cooked']!, 'fist', 1),
            itemFromPortion(FOOD_BY_ID['salad']!, 'fist', 3),
            itemFromPortion(FOOD_BY_ID['challah']!, 'fist', 1),
            hiddenOilItem([0, 8, 20]),
          ],
          photoId: null,
          note: '',
          hiddenOil: [0, 8, 20],
        });
      }
    }
    for (let w = 0; w < 5; w++) {
      const at = localDateTime(d, `${String(8 + w * 3).padStart(2, '0')}:00`).getTime();
      out.waterLogs.push({ id: id('water'), createdAt: at, updatedAt: at, date: d, at, ml: 500, drink: w === 3 && rnd() > 0.6 ? 'coke-zero' : 'water' });
    }
  }
  return out;
}
