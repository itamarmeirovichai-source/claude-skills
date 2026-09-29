import { z } from 'zod';
import type { FoodLog, SetLog, WorkoutSession } from '../db/records';
import { NUTRITION_FLOORS } from '../content/meals';
import { dayTotals } from './nutrition';
import type { ReviewItem, WeeklyReview } from './review';

// Coach report: a readable Markdown file plus structured JSON of the same review.
// Food photos and private notes are excluded unless the user chooses to include them.

export interface ReportOptions {
  includeNotes: boolean;
  includePhotos: boolean;
  appVersion: string;
  appName: string;
}

export interface ReportLogs {
  sessions: WorkoutSession[];
  setLogs: SetLog[];
  foodLogs: FoodLog[];
  exerciseName: (id: string) => string;
}

const section = (title: string, items: ReviewItem[]) =>
  [`## ${title}`, '', ...(items.length ? items.flatMap((i) => [`- ${i.text} (confidence: ${i.confidence})`, ...i.evidence.map((e) => `  - Evidence: ${e}`)]) : ['- Nothing this week.']), ''].join('\n');

export function coachReportMarkdown(review: WeeklyReview, logs: ReportLogs, opts: ReportOptions): string {
  const lines: string[] = [
    `# ${opts.appName} weekly review`,
    '',
    `Week: ${review.weekStart} to ${review.weekEnd}`,
    `Generated: ${new Date(review.generatedAt).toISOString()}`,
    '',
    'This report was exported by the user from a private, on device app. The app cannot share data by itself.',
    'It is a training log summary, not a medical record. Any change to training or nutrition should be confirmed by the user, and for a minor, reviewed with a parent.',
    '',
    '## Priorities for next week',
    '',
    ...review.priorities.map((p, i) => `${i + 1}. ${p}`),
    '',
    section('Keep doing', review.keepDoing),
    section('Ready to progress', review.readyToProgress),
    section('Improve next week', review.improve),
    section('Safety flags', review.safety),
    '## Comparison with the previous week',
    '',
    '| Measure | Previous | This week | Note |',
    '| --- | --- | --- | --- |',
    ...review.comparison.map((c) => `| ${c.label} | ${c.previous} | ${c.current} | ${c.note} |`),
    '',
    '## Sessions',
    '',
  ];
  const weekSessions = logs.sessions.filter((s) => s.date >= review.weekStart && s.date <= review.weekEnd && s.status === 'done').sort((a, b) => a.startedAt - b.startedAt);
  if (!weekSessions.length) lines.push('- No sessions logged.');
  for (const s of weekSessions) {
    lines.push(`### ${s.date} ${s.title}`, '');
    if (s.sessionRpe !== null) lines.push(`Session RPE: ${s.sessionRpe}`);
    const sets = logs.setLogs.filter((x) => x.sessionId === s.id && !x.warmup).sort((a, b) => a.completedAt - b.completedAt);
    const byEx = new Map<string, SetLog[]>();
    for (const x of sets) byEx.set(x.exerciseId, [...(byEx.get(x.exerciseId) ?? []), x]);
    for (const [exId, xs] of byEx) {
      const parts = xs.map((x) => {
        const bits = [
          x.side ? x.side[0]!.toUpperCase() : '',
          x.weightKg !== null ? `${x.weightKg} kg` : '',
          x.reps !== null ? `x${x.reps}` : '',
          x.seconds !== null ? `${x.seconds}s` : '',
          x.roundTrips !== null ? `${x.roundTrips} round trips` : '',
          x.rir !== null ? `RIR ${x.rir}` : '',
          x.quality !== null ? `quality ${x.quality}/5` : '',
          x.form ? `form ${x.form}` : '',
          x.pain !== 'none' ? `pain ${x.pain}${x.painScore !== null ? ` ${x.painScore}/10` : ''}` : '',
        ].filter(Boolean);
        return bits.join(' ');
      });
      lines.push(`- ${logs.exerciseName(exId)}: ${parts.join('; ')}`);
    }
    if (opts.includeNotes && s.note) lines.push(`- Note: ${s.note}`);
    lines.push('');
  }
  lines.push('## Food by day (estimated ranges)', '');
  const byDay = new Map<string, FoodLog[]>();
  for (const f of logs.foodLogs.filter((f) => f.date >= review.weekStart && f.date <= review.weekEnd)) byDay.set(f.date, [...(byDay.get(f.date) ?? []), f]);
  if (!byDay.size) lines.push('- No food logged.');
  for (const [d, fs] of [...byDay.entries()].sort()) {
    const t = dayTotals(fs);
    lines.push(`- ${d}: ${Math.round(t.low.kcal)} to ${Math.round(t.high.kcal)} kcal, protein ${Math.round(t.low.protein)} to ${Math.round(t.high.protein)} g, ${fs.length} meals logged`);
  }
  lines.push('', `Photos included: ${opts.includePhotos ? 'yes' : 'no'}. Private notes included: ${opts.includeNotes ? 'yes' : 'no'}.`, '', `Exported by ${opts.appName} ${opts.appVersion}.`, '');
  return lines.join('\n');
}

export function coachReportJson(review: WeeklyReview, logs: ReportLogs, opts: ReportOptions) {
  const inWeek = (d: string) => d >= review.weekStart && d <= review.weekEnd;
  const sessions = logs.sessions.filter((s) => inWeek(s.date) && s.status === 'done');
  const ids = new Set(sessions.map((s) => s.id));
  return {
    format: 'peakform-coach-report',
    version: 1,
    appVersion: opts.appVersion,
    week: { start: review.weekStart, end: review.weekEnd },
    generatedAt: new Date(review.generatedAt).toISOString(),
    review: {
      priorities: review.priorities,
      keepDoing: review.keepDoing,
      readyToProgress: review.readyToProgress,
      improveNextWeek: review.improve,
      safetyFlags: review.safety,
      comparison: review.comparison,
      metrics: { current: review.current, previous: review.previous },
    },
    sessions: sessions.map((s) => ({ id: s.id, date: s.date, title: s.title, session: s.session, sessionRpe: s.sessionRpe, note: opts.includeNotes ? s.note : undefined })),
    sets: logs.setLogs
      .filter((x) => ids.has(x.sessionId) && !x.warmup)
      .map((x) => ({
        sessionId: x.sessionId,
        exercise: logs.exerciseName(x.exerciseId),
        exerciseId: x.exerciseId,
        setIndex: x.setIndex,
        side: x.side,
        weightKg: x.weightKg,
        reps: x.reps,
        rir: x.rir,
        seconds: x.seconds,
        form: x.form,
        pain: x.pain,
        painScore: x.painScore,
        quality: x.quality,
        landing: x.landing,
        roundTrips: x.roundTrips,
        note: opts.includeNotes ? x.note : undefined,
      })),
    food: logs.foodLogs
      .filter((f) => inWeek(f.date))
      .map((f) => ({
        date: f.date,
        slot: f.slot,
        source: f.source,
        asPlanned: f.asPlanned,
        items: f.items.map((i) => ({ name: i.name, gramsLow: i.estimate.gramsLow, gramsHigh: i.estimate.gramsHigh, method: i.estimate.method, kcalLow: Math.round(i.low.kcal), kcalHigh: Math.round(i.high.kcal) })),
        photoIncluded: opts.includePhotos && f.photoId !== null,
        note: opts.includeNotes ? f.note : undefined,
      })),
    privacy: { photosIncluded: opts.includePhotos, notesIncluded: opts.includeNotes },
  };
}

// ---------- Recommendation import ----------

const SetTargetChange = z.object({
  type: z.literal('plan-item'),
  planItemId: z.string(),
  sets: z.number().int().min(1).max(10).optional(),
  repMin: z.number().int().min(1).max(50).optional(),
  repMax: z.number().int().min(1).max(50).optional(),
  restSec: z.number().int().min(0).max(900).optional(),
  rir: z.number().min(1).max(5).optional(),
  reason: z.string().max(500),
});
const NutritionChange = z.object({
  type: z.literal('nutrition-target'),
  weekday: z.number().int().min(0).max(6),
  kcal: z.number().int().optional(),
  protein: z.number().int().min(0).max(300).optional(),
  carbs: z.number().int().min(0).max(700).optional(),
  fat: z.number().int().min(0).max(250).optional(),
  reason: z.string().max(500),
});
export const RecommendationSchema = z.object({
  format: z.literal('peakform-recommendation'),
  version: z.literal(1),
  source: z.string().max(100),
  createdAt: z.string().max(40),
  changes: z.array(z.discriminatedUnion('type', [SetTargetChange, NutritionChange])).max(60),
});
export type Recommendation = z.infer<typeof RecommendationSchema>;

export interface RecommendationCheck {
  ok: boolean;
  errors: string[];
  blocked: string[];
  rec: Recommendation | null;
}

/** Validate a recommendation file. Changes that break safety floors are blocked, not applied. */
export function checkRecommendation(text: string): RecommendationCheck {
  let json: unknown;
  try {
    json = JSON.parse(text);
  } catch {
    return { ok: false, errors: ['This file is not valid JSON.'], blocked: [], rec: null };
  }
  const r = RecommendationSchema.safeParse(json);
  if (!r.success) return { ok: false, errors: r.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`), blocked: [], rec: null };
  const blocked: string[] = [];
  for (const c of r.data.changes) {
    if (c.type === 'nutrition-target') {
      if (c.kcal !== undefined && c.kcal < NUTRITION_FLOORS.kcal) blocked.push(`Weekday ${c.weekday}: ${c.kcal} kcal is below the ${NUTRITION_FLOORS.kcal} kcal floor.`);
      if (c.carbs !== undefined && c.carbs < NUTRITION_FLOORS.carbs) blocked.push(`Weekday ${c.weekday}: ${c.carbs} g carbohydrate is below ${NUTRITION_FLOORS.carbs} g.`);
    }
    if (c.type === 'plan-item' && c.repMin !== undefined && c.repMax !== undefined && c.repMin > c.repMax) blocked.push(`${c.planItemId}: rep range is reversed.`);
  }
  return { ok: true, errors: [], blocked, rec: r.data };
}
