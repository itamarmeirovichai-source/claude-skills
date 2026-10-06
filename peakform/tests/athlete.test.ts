import { describe, expect, it } from 'vitest';
import { suggestNext, wristGate, type Prescription, type WorkSet } from '../src/domain/progression';
import { DEFAULT_ATHLETE, openQuestions, parseAthlete, reviewedEnergy, type AthleteProfile } from '../src/domain/athlete';
import { heavyJumpingNear, hoursAboveAge, weeklyExposure } from '../src/domain/exposure';
import { comparable, heights, jumpTrend, parseTests, type JumpTest } from '../src/domain/jumpTests';
import { readiness, safetyState } from '../src/domain/safety';
import { contextMarkdown } from '../src/domain/report';
import { planMarkdown } from '../src/domain/planExport';
import { baselinePlanRecord } from '../src/domain/defaults';
import { makeBackup, validateTables, buildPreview, type TableData } from '../src/domain/backup';
import { db } from '../src/db/db';
import { KV, addSportLog, ensureInitialized, getAthlete, kvSet, readAllTables, saveAthlete, writeAllTables } from '../src/db/repo';
import type { SportLog, WorkoutSession } from '../src/db/records';

const press: Prescription = { kind: 'strength', sets: 3, repMin: 8, repMax: 12, rir: 2, perSide: false, loadIncrement: 'upper', equipment: 'machine' };
const sets = (reps: number[]): WorkSet[] => reps.map((r, i) => ({ setIndex: i, side: null, weightKg: 40, reps: r, rir: 2, form: 'good', pain: 'none' }));

describe('wrist gate on progression', () => {
  it('turns a load increase into a hold while the wrist is not cleared, and leaves reps alone', () => {
    const up = suggestNext(press, sets([12, 12, 12]));
    expect(up.kind).toBe('add_load');
    const held = wristGate(up, true);
    expect(held.kind).toBe('hold');
    expect(held.targets).toEqual([]);
    expect(held.reason).toMatch(/clinician has not confirmed/);
    expect(wristGate(up, false)).toBe(up);
    const reps = suggestNext(press, sets([10, 9, 9]));
    expect(wristGate(reps, true)).toBe(reps);
  });

  it('one qualifying set never adds load', () => {
    const s = suggestNext(press, [{ setIndex: 0, side: null, weightKg: 40, reps: 12, rir: 2, form: 'good', pain: 'none' }]);
    expect(s.kind).toBe('complete_sets');
  });
});

describe('school sport and total load', () => {
  const sport = (date: string, minutes: number, jumping: SportLog['jumping'] = 'some'): SportLog => ({ id: `s-${date}-${minutes}`, createdAt: 0, updatedAt: 0, date, sport: 'volleyball', name: '', minutes, intensity: 'hard', jumping, note: '' });
  const session = (date: string, min: number): WorkoutSession => ({ id: `w-${date}`, createdAt: 0, updatedAt: 0, date, weekday: 0, planWeekday: 0, planId: 'p', planVersion: 1, session: 'main', title: 'Upper A', status: 'done', startedAt: 0, finishedAt: min * 60000, planSnapshot: [], sessionRpe: null, recovery: null, poolLengthM: null, note: '', rescheduledFrom: null });

  it('adds school sport to the week next to the plan sessions', () => {
    const e = weeklyExposure('2026-10-05', [session('2026-10-05', 60), session('2026-10-07', 55)], [sport('2026-10-06', 90), sport('2026-10-08', 120, 'lots'), sport('2026-10-20', 90)]);
    expect(e.trainingMin).toBe(115);
    expect(e.sportMin).toBe(210);
    expect(e.totalMin).toBe(325);
    expect(e.lotsJumpingDays).toBe(1);
    expect(e.activeDays).toBe(4);
  });

  it('compares weekly hours with age only when the age is known', () => {
    const e = weeklyExposure('2026-10-05', [], [sport('2026-10-05', 600), sport('2026-10-06', 300)]);
    expect(hoursAboveAge(e, 14)).toBe(true);
    expect(hoursAboveAge(e, null)).toBeNull();
    expect(hoursAboveAge(weeklyExposure('2026-10-05', [], [sport('2026-10-05', 300)]), 14)).toBe(false);
  });

  it('notices a lot of jumping the day before a home jump day', () => {
    expect(heavyJumpingNear('2026-10-08', [sport('2026-10-07', 90, 'lots')])?.date).toBe('2026-10-07');
    expect(heavyJumpingNear('2026-10-08', [sport('2026-10-06', 90, 'lots')])).toBeNull();
    expect(heavyJumpingNear('2026-10-08', [sport('2026-10-08', 90, 'some')])).toBeNull();
  });
});

describe('jump tests', () => {
  const t = (date: string, reach: number, standing: number[], extra: Partial<JumpTest> = {}): JumpTest => ({ id: date, date, standingReachCm: reach, standingJumpCm: standing, approachJumpCm: [], method: 'wall-tape', surface: 'grass', shoes: 'court shoes', note: '', ...extra });

  it('measures jump height as the best reach minus standing reach', () => {
    expect(heights(t('2026-10-05', 240, [285, 288, 286]))).toEqual({ standing: 48, approach: null });
    expect(heights({ ...t('2026-10-05', 240, []), standingReachCm: null })).toEqual({ standing: null, approach: null });
  });

  it('compares only tests done the same way, and calls small differences noise', () => {
    const a = t('2026-10-05', 240, [286]);
    const b = t('2026-11-02', 241, [289]);
    const other = t('2026-11-01', 240, [300], { shoes: 'socks' });
    expect(comparable(a, other)).toBe(false);
    const tr = jumpTrend([a, other, b]);
    expect(tr.previous?.id).toBe(a.id);
    expect(tr.standingChange).toBe(2);
    expect(tr.withinNoise).toBe(true);
    expect(jumpTrend([a, t('2026-11-30', 240, [292])]).withinNoise).toBe(false);
    expect(jumpTrend([b]).previous).toBeNull();
    expect(parseTests([{ nonsense: true }])).toEqual([]);
  });
});

describe('athlete profile', () => {
  it('falls back to cautious defaults for missing or invalid answers', () => {
    const a = parseAthlete({ wrist: { status: 'cleared-by-me' }, home: null });
    expect(a.wrist.status).toBe('unknown');
    expect(a.home.space).toBe('unknown');
    expect(a.weight.mode).toBe('weekly');
    expect(a.kosher.meatToDairyHours).toBe(6);
    expect(a.aspirations).toEqual([]);
  });

  it('lists what still needs confirming, gating items first', () => {
    const q = openQuestions(DEFAULT_ATHLETE, { creatineActive: true });
    expect(q.map((x) => x.id).slice(0, 2)).toEqual(['wrist', 'home']);
    expect(q.map((x) => x.id)).toEqual(expect.arrayContaining(['sport', 'height', 'creatine', 'supervision']));
    expect(q.filter((x) => x.gates).map((x) => x.id)).toEqual(['wrist', 'home']);
    // The vegetable question only appears once a large portion was entered.
    expect(q.map((x) => x.id)).not.toContain('veg');
    expect(openQuestions({ ...DEFAULT_ATHLETE, veg: { ...DEFAULT_ATHLETE.veg, grams: 500 } }, { creatineActive: false }).map((x) => x.id)).toContain('veg');
  });

  it('uses only professionally reviewed energy targets, newest first', () => {
    const base = { kind: 'energy' as const, value: 'about 3,000 kcal', units: 'kcal a day', source: 'Clinic', role: 'pediatric sports dietitian' as const, kcalRange: [2800, 3200] as [number, number], notes: '' };
    const a: AthleteProfile = {
      ...DEFAULT_ATHLETE,
      reviewed: [
        { ...base, id: 'a', date: '2026-09-01', status: 'professionally reviewed' },
        { ...base, id: 'b', date: '2026-10-01', status: 'professionally reviewed', kcalRange: [3000, 3400] },
        { ...base, id: 'c', date: '2026-10-05', status: 'discussed with a parent only' },
      ],
    };
    expect(reviewedEnergy(a)?.id).toBe('b');
    expect(reviewedEnergy(DEFAULT_ATHLETE)).toBeNull();
  });
});

describe('readiness', () => {
  it('never certifies safety: the best case says no warning signs were logged', () => {
    const s = safetyState('2026-10-06', [], []);
    const r = readiness('2026-10-06', null, { id: 's', createdAt: 0, updatedAt: 0, date: '2026-10-06', bedtime: '22:00', wakeTime: '07:00', durationMin: 540, quality: 4 }, [], s);
    expect(r.label).toBe('No warning signs logged');
    expect(r.label).not.toMatch(/ready|safe/i);
  });
});

describe('reports and exports', () => {
  it('keeps aspirations apart from reviewed targets in the coach report', () => {
    const a: AthleteProfile = { ...DEFAULT_ATHLETE, aspirations: [{ id: 'x', text: 'Jump higher for volleyball', recordedOn: '2026-10-06' }] };
    const md = contextMarkdown({ athlete: a, week: ['Sunday, Upper A'], planVersion: 'PeakForm week, version 3' }).join('\n');
    expect(md).toMatch(/User aspirations \(in the athlete's words, not reviewed targets\)\n\n- Jump higher for volleyball/);
    expect(md).toMatch(/Professionally reviewed targets\n\n- None recorded/);
    expect(md).toMatch(/Wrist after an injury: not answered/);
  });

  it('exports the plan with locations, durations, stop rules, and example meals', () => {
    const md = planMarkdown(baselinePlanRecord(0), DEFAULT_ATHLETE, { meatToDairyHours: 3 });
    expect(md).toMatch(/### Gym strength \(Gym\), about \d+ min/);
    expect(md).toMatch(/### Home jumps and skills \(Home\)/);
    expect(md).toMatch(/Stop rules:/);
    expect(md).toContain('Example serving. Adjust to appetite and activity; this is not a daily limit.');
    expect(md).toMatch(/not a requirement or a limit/);
    expect(md).toMatch(/## Still to confirm/);
  });
});

describe('backups keep the 3.0 data', () => {
  it('round trips the athlete profile and the sport log through a backup', async () => {
    await db.delete();
    await db.open();
    await ensureInitialized();
    await saveAthlete('wrist', { status: 'cleared', clearedBy: 'orthopaedic doctor', date: '2026-10-01', limits: '' });
    await saveAthlete('aspirations', [{ id: 'a1', text: 'Jump higher', recordedOn: '2026-10-06' }]);
    await kvSet(KV.jumpTests, [{ id: 'j', date: '2026-10-05', standingReachCm: 240, standingJumpCm: [286], approachJumpCm: [], method: 'wall-tape', surface: 'grass', shoes: 'court', note: '' }]);
    await addSportLog({ date: '2026-10-05', sport: 'basketball', name: '', minutes: 90, intensity: 'moderate', jumping: 'some', note: '' });
    const tables = await readAllTables();
    const backup = await makeBackup(tables, '3.0.0');
    const { valid, issues } = validateTables(backup.tables as TableData);
    expect(issues).toEqual([]);
    await db.delete();
    await db.open();
    await ensureInitialized();
    const preview = await buildPreview(backup, await readAllTables(), 'plain');
    expect(preview.checksumOk).toBe(true);
    expect(preview.tables.find((t) => t.table === 'sportLogs')).toMatchObject({ incoming: 1, added: 1 });
    await writeAllTables(valid, 'replace');
    const a = await getAthlete();
    expect(a.wrist.status).toBe('cleared');
    expect(a.aspirations[0]!.text).toBe('Jump higher');
    expect(await db.sportLogs.count()).toBe(1);
  });

  it('imports an older backup without the sport log table', async () => {
    const tables = await readAllTables();
    delete tables.sportLogs;
    const { valid, issues } = validateTables(tables);
    expect(issues).toEqual([]);
    await writeAllTables(valid, 'replace');
    expect(await db.sportLogs.count()).toBe(0);
  });
});
