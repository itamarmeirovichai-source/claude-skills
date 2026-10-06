import { describe, expect, it } from 'vitest';
import { BASELINE_PLAN } from '../src/content/plan';
import { DEFAULT_ATHLETE } from '../src/domain/athlete';
import type { ActivityKind } from '../src/content/types';
import { generateDemo } from '../src/domain/demo';
import { generateWeeklyReview, type ReviewData } from '../src/domain/review';
import { coachReportJson, coachReportMarkdown } from '../src/domain/report';
import { fourExposureReview, isReviewDue, type Exposure } from '../src/domain/fourExposure';
import { coverageFrom, focusChecks, planCoverageInputs, shoulderOverlap, COVERAGE_WEIGHTS } from '../src/domain/coverage';
import type { MuscleId } from '../src/content/muscles';
import type { FatigueArea } from '../src/content/types';

const KIND: Record<string, ActivityKind> = {
  'easy-jump-rope': 'conditioning',
  'dynamic-volleyball-warm-up': 'warmup',
  'volleyball-approach-jump': 'jump',
  'countermovement-jump': 'jump',
  'lateral-block-jump': 'jump',
  'volleyball-approach-footwork': 'skill',
  'volleyball-spike': 'skill',
  'block-to-spike-transition': 'skill',
  'shuffle-to-sprint': 'sprint',
  'ten-metre-sprint': 'sprint',
  'medicine-ball-spike-throw': 'throw',
  'easy-pool-round-trip': 'swim',
  'copenhagen-plank': 'hold',
  'hanging-leg-raise': 'bodyweight',
  'nordic-hamstring-curl': 'bodyweight',
};
const kind = (id: string): ActivityKind => KIND[id] ?? 'strength';
const SIDES = new Set(['bulgarian-split-squat', 'cable-hip-abduction', 'one-arm-lat-pulldown', 'single-arm-cable-lateral-raise', 'cable-external-rotation', 'pallof-press', 'copenhagen-plank']);

function reviewData(end: string, weeks = 2, lastBackupAt: number | null = null): ReviewData {
  const demo = generateDemo(BASELINE_PLAN.days, end, weeks, { kind, logSides: (id) => SIDES.has(id) });
  return {
    planDays: BASELINE_PLAN.days,
    ...demo,
    suggestions: [],
    fourReviews: [],
    reviewedKcal: null,
    exampleKcal: 2450,
    sportLogs: [],
    athlete: DEFAULT_ATHLETE,
    ageYears: 14,
    creatineActive: false,
    lastBackupAt,
    exerciseKind: kind,
    exerciseName: (id) => id,
  };
}

describe('weekly review', () => {
  it('produces exactly the four sections with evidence and confidence', () => {
    const data = reviewData('2026-10-04');
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r.weekStart).toBe('2026-09-28');
    expect(r.weekEnd).toBe('2026-10-04');
    for (const sec of [r.keepDoing, r.readyToProgress, r.improve, r.safety, r.progress!, r.insufficient!, r.recovery!, r.professional!]) {
      for (const item of sec) {
        expect(item.evidence.length).toBeGreaterThan(0);
        expect(['high', 'medium', 'low']).toContain(item.confidence);
        expect(item.text).not.toMatch(/\b(good job|bad|lazy|failure|cheat)\b/i);
      }
    }
    expect(r.priorities.length).toBeGreaterThan(0);
    expect(r.priorities.length).toBeLessThanOrEqual(3);
    // Four gym sessions and three home sessions (Monday, Thursday, Friday), no swims.
    expect(r.current.plannedSessions).toBe(7);
    expect(r.current.homePlanned).toBe(3);
    expect(r.current.swimPlanned).toBe(0);
    expect(r.comparison.find((c) => c.label === 'Scale body fat')!.note).toMatch(/Trend only/);
    expect(r.comparison.find((c) => c.label === 'Days in the reviewed energy range')!.current).toBe('No reviewed target');
  });

  it('lists missing data, recovery concerns, and reasons for a professional review', () => {
    const data = reviewData('2026-10-04');
    data.athlete = { ...DEFAULT_ATHLETE, aspirations: [{ id: 'a', text: 'Lower body fat and more muscle', recordedOn: '2026-10-01' }], supplements: { ...DEFAULT_ATHLETE.supplements, creatineProduct: 'Creatine monohydrate' } };
    data.sportLogs = ['2026-09-29', '2026-09-30', '2026-10-01'].map((d, i) => ({ id: `sp${i}`, createdAt: 0, updatedAt: 0, date: d, sport: 'volleyball' as const, name: '', minutes: 600, intensity: 'hard' as const, jumping: 'lots' as const, note: '' }));
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    const ids = (xs: Array<{ id: string }> | undefined) => (xs ?? []).map((x) => x.id);
    expect(ids(r.professional)).toEqual(expect.arrayContaining(['wrist', 'creatine', 'physique']));
    expect(ids(r.recovery)).toEqual(expect.arrayContaining(['sport-jumps', 'hours']));
    expect(ids(r.insufficient)).toContain('home-data');
    expect(r.current.sportMin).toBe(1800);
  });

  it('never flags intake against a fixed 2,000 calories, only against the examples or a reviewed range', () => {
    const data = reviewData('2026-10-04');
    const r = generateWeeklyReview({ ...data, exampleKcal: null, reviewedKcal: null }, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r.current.lowIntakeDays).toBe(0);
    expect(r.current.reviewedRangeDays).toBeNull();
  });

  it('says when there are too few morning weights for a trend', () => {
    const data = reviewData('2026-10-04');
    data.checkins = data.checkins.map((c, i) => (i % 3 === 0 ? c : { ...c, weightKg: null }));
    data.athlete = { ...DEFAULT_ATHLETE, weight: { mode: 'frequent', hideNumbers: false } };
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    // Weekly weighing, the default, does not ask for more weights.
    expect(generateWeeklyReview({ ...data, athlete: DEFAULT_ATHLETE }, '2026-09-28', Date.UTC(2026, 9, 4, 18)).improve.some((i) => i.id === 'weights-few')).toBe(false);
    const item = r.improve.find((i) => i.id === 'weights-few');
    expect(item?.text).toMatch(/too uncertain for a nutrition change/);
  });

  it('raises safety flags for pain of 4 or more and pauses progression', () => {
    const data = reviewData('2026-10-04');
    data.pain.push({ id: 'p1', createdAt: 0, updatedAt: 0, date: '2026-10-02', at: Date.UTC(2026, 9, 2, 17), region: 'shoulder', score: 1, source: 'workout', exerciseId: 'volleyball-spike', note: '' });
    data.pain.push({ id: 'p2', createdAt: 0, updatedAt: 0, date: '2026-10-02', at: Date.UTC(2026, 9, 2, 17, 30), region: 'shoulder', score: 4, source: 'workout', exerciseId: 'volleyball-spike', note: '' });
    const sid = data.sessions.find((s) => s.date === '2026-10-01' && s.session === 'main')!.id;
    data.suggestions.push({ id: 's1', createdAt: 1, updatedAt: 1, exerciseId: 'incline-barbell-bench-press', planItemId: 'thu-1', basedOnSessionId: sid, kind: 'add_load', title: 'Try 37.5 kg', reason: 'All sets at the top.', targets: [], status: 'pending', decidedAt: null });
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r.safety.some((s) => /Shoulder pain/.test(s.text))).toBe(true);
    expect(r.readyToProgress).toHaveLength(0);
    expect(r.improve.some((i) => i.id === 'prog-paused')).toBe(true);
    expect(r.priorities[0]).toMatch(/Shoulder/);
  });

  it('lists ready to progress items with their reason', () => {
    const data = reviewData('2026-10-04');
    const sid = data.sessions.find((s) => s.date === '2026-09-28' && s.session === 'main')!.id;
    data.suggestions.push({ id: 's1', createdAt: 1, updatedAt: 1, exerciseId: 'barbell-squat', planItemId: 'mon-5-barbell-squat', basedOnSessionId: sid, kind: 'add_load', title: 'Try 52.5 kg', reason: 'All three sets reached 10 reps at 3 RIR with good form.', targets: [], status: 'pending', decidedAt: null });
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r.readyToProgress[0]!.text).toMatch(/barbell-squat: Try 52.5 kg/);
    expect(r.readyToProgress[0]!.evidence[0]).toMatch(/10 reps at 3 RIR/);
  });

  it('flags a missing or old backup', () => {
    const r = generateWeeklyReview(reviewData('2026-10-04'), '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r.improve.some((i) => i.id === 'backup')).toBe(true);
    const r2 = generateWeeklyReview(reviewData('2026-10-04', 2, Date.UTC(2026, 9, 3)), '2026-09-28', Date.UTC(2026, 9, 4, 18));
    expect(r2.keepDoing.some((i) => i.id === 'backup-ok')).toBe(true);
  });

  it('builds a coach report in Markdown and JSON without notes or photos by default', () => {
    const data = reviewData('2026-10-04');
    const idx = data.sessions.findIndex((x) => x.date >= '2026-09-28');
    data.sessions[idx] = { ...data.sessions[idx]!, note: 'private thought' };
    const r = generateWeeklyReview(data, '2026-09-28', Date.UTC(2026, 9, 4, 18));
    const logs = { sessions: data.sessions, setLogs: data.setLogs, foodLogs: data.foodLogs, exerciseName: (id: string) => id };
    const opts = { includeNotes: false, includePhotos: false, appVersion: '1.0.0', appName: 'PeakForm' };
    const md = coachReportMarkdown(r, logs, opts);
    for (const h of ['## Evidence of progress', '## Not enough data yet', '## Recovery concerns', '## Reasons for a professional review', '## Keep doing', '## Ready to progress', '## Improve next week', '## Safety flags']) expect(md).toContain(h);
    expect(md).not.toContain('private thought');
    expect(md).toMatch(/cannot share data by itself/);
    const json = coachReportJson(r, logs, opts);
    expect(json.format).toBe('peakform-coach-report');
    expect(JSON.stringify(json)).not.toContain('private thought');
    const withNotes = coachReportJson(r, logs, { ...opts, includeNotes: true });
    expect(JSON.stringify(withNotes)).toContain('private thought');
  });
});

describe('four exposure review', () => {
  const ex = (reps: number[], load: number, opts: Partial<Exposure> = {}): Exposure => ({
    sessionId: Math.random().toString(),
    date: '2026-10-01',
    plannedSets: reps.length,
    sets: reps.map((r, i) => ({ setIndex: i, side: null, weightKg: load, reps: r, rir: 3, form: 'good', pain: 'none' })),
    ...opts,
  });

  it('is due every fourth exposure', () => {
    expect(isReviewDue(4)).toBe(true);
    expect(isReviewDue(8)).toBe(true);
    expect(isReviewDue(5)).toBe(false);
    expect(isReviewDue(0)).toBe(false);
  });

  it('recommends progress when reps rise at the same load', () => {
    const r = fourExposureReview('strength', [ex([8, 8, 7], 50), ex([8, 8, 8], 50), ex([9, 8, 8], 50), ex([9, 9, 8], 50)], 4, 3);
    expect(r.due).toBe(true);
    expect(r.recommendation).toBe('progress');
    expect(r.details.join(' ')).toMatch(/small sample/);
  });

  it('holds and asks to check form, adherence, sleep, pain, and fatigue when flat', () => {
    const r = fourExposureReview('strength', [ex([8, 8, 8], 50), ex([8, 8, 8], 50), ex([8, 8, 8], 50), ex([8, 8, 8], 50)], 4, 3);
    expect(r.recommendation).toBe('hold');
    expect(r.summary).toMatch(/form.*sleep.*pain.*fatigue/);
  });

  it('suggests reducing when performance declines', () => {
    const r = fourExposureReview('strength', [ex([10, 9, 9], 50), ex([9, 9, 8], 50), ex([8, 8, 8], 50), ex([8, 7, 7], 50)], 4, 3);
    expect(r.recommendation).toBe('reduce');
  });

  it('requests a coach review when pain rises', () => {
    const painful = ex([9, 9, 9], 50);
    painful.sets[0] = { ...painful.sets[0]!, pain: 'mild', painScore: 3 };
    const r = fourExposureReview('strength', [ex([8, 8, 8], 50), ex([8, 8, 8], 50), ex([9, 8, 8], 50), painful], 4, 3);
    expect(r.recommendation).toBe('coach_review');
  });

  it('asks for a coach review when jump quality is stable but height is not improving', () => {
    const j = (q: number): Exposure => ({ sessionId: 'x', date: 'd', plannedSets: 3, reachCm: 290, sets: [0, 1, 2].map((i) => ({ setIndex: i, side: null, weightKg: null, reps: 2, rir: null, form: 'good', pain: 'none', quality: q, landing: 'good' })) });
    const r = fourExposureReview('jump', [j(4), j(4), j(4), j(4)], 8, null);
    expect(r.recommendation).toBe('coach_review');
    expect(r.summary).toMatch(/Volume stays the same/);
  });
});

describe('muscle coverage', () => {
  type L = { name: string; kind: ActivityKind; primary: MuscleId[]; secondary: MuscleId[]; fatigueOverlap: FatigueArea[] };
  const lib: Record<string, L> = {
    row: { name: 'Seated Cable Row', kind: 'strength', primary: ['rhomboids', 'traps_middle', 'lats'], secondary: ['delt_posterior', 'biceps', 'forearm_flexors'], fatigueOverlap: ['shoulder'] },
    calf: { name: 'Standing Calf Raise', kind: 'strength', primary: ['gastrocnemius'], secondary: ['soleus'], fatigueOverlap: [] },
    rope: { name: 'Easy Jump Rope', kind: 'conditioning', primary: ['gastrocnemius', 'soleus'], secondary: ['tibialis_anterior'], fatigueOverlap: [] },
    'barbell-bench-press': { name: 'Bench', kind: 'strength', primary: ['pec_sternal'], secondary: ['triceps', 'delt_anterior'], fatigueOverlap: ['shoulder'] },
    'volleyball-spike': { name: 'Spike', kind: 'skill', primary: ['lats'], secondary: ['delt_anterior'], fatigueOverlap: ['shoulder'] },
    swim: { name: 'Swim', kind: 'swim', primary: ['lats'], secondary: [], fatigueOverlap: ['shoulder'] },
  };
  const lookup = (id: string) => lib[id];

  it('counts direct and indirect sets with transparent weights, and activity as exposure', () => {
    const c = coverageFrom([{ weekday: 1, exerciseId: 'row', sets: 3 }, { weekday: 1, exerciseId: 'calf', sets: 3 }, { weekday: 1, exerciseId: 'rope', sets: 1 }], lookup);
    expect(c.rhomboids.direct).toBe(3 * COVERAGE_WEIGHTS.primarySet);
    expect(c.biceps.indirect).toBe(3 * COVERAGE_WEIGHTS.secondarySet);
    expect(c.gastrocnemius.direct).toBe(3);
    expect(c.gastrocnemius.exposures).toBe(1);
    expect(c.soleus.indirect).toBe(1.5);
    expect(c.tibialis_anterior.direct).toBe(0);
    expect(c.tibialis_anterior.exposures).toBe(1);
  });

  it('confirms upper back, calves, and forearms are present', () => {
    const c = coverageFrom([{ weekday: 1, exerciseId: 'row', sets: 3 }, { weekday: 1, exerciseId: 'calf', sets: 3 }], lookup);
    const f = focusChecks(c);
    expect(f.map((x) => [x.key, x.present])).toEqual([
      ['upper_back', true],
      ['calves', true],
      ['forearms', true],
    ]);
  });

  it('calls out shoulder overlap', () => {
    const o = shoulderOverlap(
      [
        { weekday: 0, exerciseId: 'barbell-bench-press', sets: 3 },
        { weekday: 0, exerciseId: 'swim', sets: 2 },
        { weekday: 1, exerciseId: 'volleyball-spike', sets: 4 },
      ],
      lookup,
    );
    expect(o.notes.some((n) => /Sunday has pressing and swimming/.test(n))).toBe(true);
    expect(o.notes.some((n) => /Pressing on Sunday is followed by spiking on Monday/.test(n))).toBe(true);
  });

  it('builds inputs from the full plan', () => {
    const inputs = planCoverageInputs(BASELINE_PLAN.days);
    expect(inputs.length).toBe(BASELINE_PLAN.days.reduce((a, d) => a + d.items.length, 0));
  });
});
