import { expect, type Page } from '@playwright/test';

/** Monday 28 September 2026, 16:40 in Jerusalem: home jumps, then the gym Lower A. */
export const MONDAY = new Date('2026-09-28T16:40:00+03:00');
export const SATURDAY_MORNING = new Date('2026-10-03T09:00:00+03:00');
/** Wednesday 30 September 2026, 16:40: Upper B at the gym. */
export const WEDNESDAY = new Date('2026-09-30T16:40:00+03:00');
/** Thursday 1 October 2026, 16:40: home jumps, then the gym Lower B. */
export const THURSDAY = new Date('2026-10-01T16:40:00+03:00');
/** Friday 2 October 2026, 12:40: the light home skill session. */
export const FRIDAY = new Date('2026-10-02T12:40:00+03:00');

export async function atTime(page: Page, when: Date) {
  await page.clock.install({ time: when });
  await page.clock.resume();
}

export async function onboard(page: Page, opts: { demo?: boolean; name?: string } = {}) {
  await page.goto('./');
  await page.getByTestId('onboard-start').click();
  await page.getByTestId('onboard-ack').check();
  if (opts.name) await page.getByTestId('onboard-name').fill(opts.name);
  await page.getByTestId('onboard-next').click();
  await page.getByTestId(opts.demo ? 'onboard-demo' : 'onboard-finish').click();
  await expect(page.getByTestId('today')).toBeVisible();
}

export async function go(page: Page, hash: string) {
  await page.evaluate((h) => (window.location.hash = h), hash);
}

/** Open today's plan day and start a session. */
export async function startSession(page: Page, which: 'main' | 'home' | 'morning' | 'swim' = 'main') {
  await go(page, '/train/start');
  await expect(page.getByTestId('train-day')).toBeVisible();
  await page.getByTestId(`start-${which}`).click();
  await expect(page.getByTestId('set-logger')).toBeVisible();
}

export async function exerciseChip(page: Page, index: number) {
  await page.locator('.ex-nav button').nth(index).click();
}

export async function logStrengthSet(page: Page, weight: number | null, reps: number) {
  if (weight !== null) await page.getByTestId('input-weight').fill(String(weight));
  await page.getByTestId('input-reps').fill(String(reps));
  await page.getByTestId('complete-set').click();
}

/** Write values straight into the key value table, as an installed app would already have them. */
export async function setKv(page: Page, values: Record<string, unknown>) {
  await page.evaluate(async (vals) => {
    const db: IDBDatabase = await new Promise((res) => {
      const r = indexedDB.open('peakform');
      r.onsuccess = () => res(r.result);
    });
    const tx = db.transaction('kv', 'readwrite');
    for (const [id, value] of Object.entries(vals)) tx.objectStore('kv').put({ id, value, updatedAt: Date.now() });
    await new Promise((res) => (tx.oncomplete = res));
  }, values);
}

/** A home with room for every drill: a mat indoors, a large grass yard, tape, a ball, and a solid wall. */
export const ROOMY_HOME = { space: 'large', ceiling: 'standard', surface: 'mat', noiseLimits: 'no', breakables: 'no', outdoor: 'large', outdoorSurface: 'grass', equipment: ['tape', 'ball', 'wall'] };

/** Turn the stored plan and settings into a 2.1 install: morning rope, early reminders, and no home sessions. */
export async function makeOldInstall(page: Page) {
  await page.evaluate(async () => {
    const db: IDBDatabase = await new Promise((res) => {
      const r = indexedDB.open('peakform');
      r.onsuccess = () => res(r.result);
    });
    const tx = db.transaction(['plans', 'settings', 'kv'], 'readwrite');
    const plans = tx.objectStore('plans');
    const all: Array<{ days: Array<{ key: string; weekday: number; items: Array<{ session: string; id: string; exerciseId: string }> }> }> = await new Promise((res) => {
      const r = plans.getAll();
      r.onsuccess = () => res(r.result);
    });
    for (const p of all) {
      for (const d of p.days) {
        d.items = d.items.filter((i) => i.session === 'main');
        if (d.weekday !== 6) d.items.unshift({ id: `${d.key}-rope`, exerciseId: 'easy-jump-rope', session: 'morning', sets: 1, target: { type: 'duration', totalMin: 9 }, restSec: 30, notes: [] } as never);
      }
      plans.put(p);
    }
    const st = tx.objectStore('settings');
    const s: { sessionTimes: Record<string, unknown>; reminders: Array<{ id: string; time: string }> } = await new Promise((res) => {
      const r = st.get('app');
      r.onsuccess = () => res(r.result);
    });
    delete s.sessionTimes.home;
    for (const r of s.reminders) {
      if (r.id === 'checkin') r.time = '05:15';
      if (r.id === 'winddown') r.time = '20:45';
    }
    st.put(s);
    tx.objectStore('kv').put({ id: 'planUpdates', value: {}, updatedAt: Date.now() });
    await new Promise((res) => (tx.oncomplete = res));
  });
}
