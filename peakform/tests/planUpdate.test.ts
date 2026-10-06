import { beforeEach, describe, expect, it } from 'vitest';
import { db } from '../src/db/db';
import { KV, activePlan, ensureInitialized, getSettings, kvGet, kvSet, saveAthlete, startSession, updateSettings } from '../src/db/repo';
import { baselinePlanRecord, defaultSettings } from '../src/domain/defaults';
import { activateProposal, currentProposal, discardProposal, pendingUpdates, proposeExact, proposePlan, V3_UPDATE_ID, withV3Times } from '../src/services/planUpdate';
import { bedtimeFor } from '../src/services/today';
import { contacts } from '../src/content/phases';
import type { AppSettings, PlanRecord } from '../src/db/records';
import type { HomeSetup } from '../src/domain/athlete';

/** An app installed with 2.1: morning rope at 05:30, the early reminders, and a six day plan. */
function oldSettings(): AppSettings {
  const s = defaultSettings(0);
  delete s.sessionTimes.home;
  s.sessionTimes.morning = '05:30';
  s.sessionTimes.main = { '0': '16:30', '1': '16:30', '2': '16:30', '3': '16:30', '4': '16:30', '5': '13:00' };
  s.reminders = s.reminders.filter((r) => r.id !== 'home');
  s.reminders.find((r) => r.id === 'checkin')!.time = '05:15';
  s.reminders.find((r) => r.id === 'winddown')!.time = '20:45';
  s.reminders.find((r) => r.id === 'dinner')!.time = '18:45';
  s.reminders.find((r) => r.id === 'milk')!.time = '20:30';
  s.reminders.find((r) => r.id === 'training')!.weekdays = [0, 1, 2, 3, 4, 5];
  s.reminders.splice(1, 0, { id: 'morning', label: 'Morning volleyball and rope', time: '05:25', weekdays: [0, 1, 2, 3, 4, 5], enabled: true, kind: 'training' });
  return s;
}

/** The 2.1 plan in short: a morning rope every day and six gym days, with no home sessions. */
function oldPlan(): PlanRecord {
  const p = baselinePlanRecord(0);
  for (const d of p.days) {
    d.items = d.items.filter((i) => i.session === 'main');
    if (d.weekday !== 6) d.items.unshift({ id: `${d.key}-rope`, exerciseId: 'easy-jump-rope', session: 'morning', sets: 1, target: { type: 'duration', totalMin: 9 }, restSec: 30, notes: [] });
  }
  return p;
}

const ROOMY: HomeSetup = { space: 'large', ceiling: 'standard', surface: 'mat', noiseLimits: 'no', breakables: 'no', outdoor: 'large', outdoorSurface: 'grass', equipment: ['tape', 'ball', 'wall'] };

async function installOld() {
  await db.delete();
  await db.open();
  await ensureInitialized();
  await db.plans.clear();
  await db.plans.put(oldPlan());
  await updateSettings(oldSettings());
  await kvSet(KV.planUpdates, {});
}

beforeEach(async () => {
  await installOld();
});

describe('schedule for the 3.0 week', () => {
  it('moves the early morning defaults and leaves times the user chose', () => {
    const s = oldSettings();
    s.reminders.find((r) => r.id === 'dinner')!.time = '19:30';
    const { settings, changes } = withV3Times(s);
    expect(settings.reminders.find((r) => r.id === 'checkin')!.time).toBe('07:00');
    expect(settings.reminders.find((r) => r.id === 'winddown')!.time).toBe('21:30');
    expect(settings.reminders.find((r) => r.id === 'morning')!.enabled).toBe(false);
    expect(settings.reminders.find((r) => r.id === 'dinner')!.time).toBe('19:30');
    expect(settings.reminders.find((r) => r.id === 'home')).toMatchObject({ time: '16:05', weekdays: [1, 4] });
    expect(settings.sessionTimes.home).toEqual({ '1': '16:15', '4': '16:15', '5': '13:30' });
    expect(settings.sessionTimes.main['1']).toBe('17:00');
    expect(changes.join(' ')).toMatch(/05:25 morning session reminder is switched off/);
    expect(withV3Times(settings).changes).toEqual([]);
  });

  it('keeps at least eight and a half hours for sleep before the check in', () => {
    expect(bedtimeFor('07:00')).toBe('22:15');
  });
});

describe('plan proposals', () => {
  it('offers the 3.0 week to an installed 2.1 plan, and not to a new install', async () => {
    expect(await pendingUpdates()).toEqual({ v3: true });
    await db.delete();
    await db.open();
    await ensureInitialized();
    expect(await pendingUpdates({ includeDismissed: true })).toBeNull();
    expect((await activePlan()).days.some((d) => d.items.some((i) => i.session === 'home'))).toBe(true);
  });

  it('changes nothing until the proposal is activated', async () => {
    const before = await activePlan();
    const p = await proposePlan('v3');
    expect(p.summary.length).toBeGreaterThan(3);
    expect(p.settingsChanges.length).toBeGreaterThan(0);
    expect((await activePlan()).id).toBe(before.id);
    expect((await getSettings()).reminders.find((r) => r.id === 'checkin')!.time).toBe('05:15');
    expect(await currentProposal()).not.toBeNull();
  });

  it('activates as a new version that keeps finished sessions on their old prescription', async () => {
    const before = await activePlan();
    const mon = before.days.find((d) => d.weekday === 1)!;
    const ses = await startSession('2026-10-05', 'main', mon.items.filter((i) => i.session === 'main'), mon.title, before);
    await db.sessions.update(ses.id, { status: 'done', finishedAt: ses.startedAt + 3_600_000 });
    await proposePlan('v3');
    const rec = await activateProposal();
    expect(rec.version).toBe(before.version + 1);
    expect((await getSettings()).activePlanId).toBe(rec.id);
    expect(await db.plans.get(before.id)).toBeDefined();
    const kept = await db.sessions.get(ses.id);
    expect(kept!.planId).toBe(before.id);
    expect(kept!.planSnapshot).toEqual(mon.items.filter((i) => i.session === 'main'));
    expect((await getSettings()).reminders.find((r) => r.id === 'checkin')!.time).toBe('07:00');
    expect(await currentProposal()).toBeNull();
    expect(await pendingUpdates({ includeDismissed: true })).toBeNull();
    expect((await kvGet<Record<string, string>>(KV.planUpdates))![V3_UPDATE_ID]).toBe('applied');
    expect(rec.days.flatMap((d) => d.items).some((i) => i.session === 'morning')).toBe(false);
  });

  it('puts the offer away with Not now, and still shows it on Train', async () => {
    await proposePlan('v3');
    await discardProposal();
    expect(await currentProposal()).toBeNull();
    expect(await pendingUpdates()).toBeNull();
    expect(await pendingUpdates({ includeDismissed: true })).toEqual({ v3: true });
  });

  it('fits the home sessions to the answers in the profile', async () => {
    const quiet = await proposePlan('v3');
    expect(contacts(quiet.plan.days.find((d) => d.weekday === 1)!.items)).toBe(0);
    await saveAthlete('home', ROOMY);
    await saveAthlete('wrist', { status: 'cleared', clearedBy: 'orthopaedic doctor', date: '2026-10-01', limits: '' });
    const roomy = await proposePlan('profile');
    expect(contacts(roomy.plan.days.find((d) => d.weekday === 1)!.items)).toBe(58);
  });

  it('changes the jump level only through a proposal the athlete activates', async () => {
    await saveAthlete('home', ROOMY);
    await proposePlan('v3');
    await activateProposal();
    expect(await kvGet(KV.jumpLevel)).toBe('intro');
    const p = await proposePlan('jump-level', { level: 'build' });
    expect(contacts(p.plan.days.find((d) => d.weekday === 4)!.items)).toBe(95);
    expect(await kvGet(KV.jumpLevel)).toBe('intro');
    await activateProposal();
    expect(await kvGet(KV.jumpLevel)).toBe('build');
  });

  it('routes hand edits and going back to an older version through the same preview', async () => {
    const before = await activePlan();
    const edited = structuredClone(before);
    edited.days[0]!.items[0]!.sets = 4;
    await proposeExact(edited, 'Your edits', 'One more set');
    expect((await activePlan()).id).toBe(before.id);
    const rec = await activateProposal();
    expect(rec.days[0]!.items[0]!.sets).toBe(4);
    expect(rec.version).toBe(before.version + 1);
  });
});
