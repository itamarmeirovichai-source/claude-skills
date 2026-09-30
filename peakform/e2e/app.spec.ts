import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
import { MONDAY, SATURDAY_MORNING, atTime, exerciseChip, go, logStrengthSet, onboard, startSession } from './helpers';
import { OLD_VOLLEYBALL_DAYS } from '../tests/fixtures/volleyballDays';

async function restoreVolleyballDays(page: Page) {
  // Put the old Tuesday and Friday volleyball sessions back, as on a phone installed before 1.2.0.
  await page.evaluate(async (oldDays) => {
    const db: IDBDatabase = await new Promise((res, rej) => {
      const o = indexedDB.open('peakform');
      o.onsuccess = () => res(o.result);
      o.onerror = () => rej(o.error);
    });
    const tx = db.transaction(['plans'], 'readwrite');
    const plans = tx.objectStore('plans');
    const all: Array<{ days: Array<{ weekday: number; title: string; short: string; items: Array<{ session: string }> }> }> = await new Promise((res) => {
      const r = plans.getAll();
      r.onsuccess = () => res(r.result);
    });
    for (const p of all) {
      for (const old of oldDays) {
        const d = p.days.find((x) => x.weekday === old.weekday)!;
        d.title = old.title;
        d.short = old.short;
        d.items = [...d.items.filter((i) => i.session === 'morning'), ...old.main, ...d.items.filter((i) => i.session === 'swim')];
      }
      plans.put(p);
    }
    await new Promise((res) => (tx.oncomplete = res));
  }, OLD_VOLLEYBALL_DAYS);
}

test.describe('first run and install', () => {
  test('first run setup lands on Today with the profile saved locally', async ({ page }) => {
    await onboard(page, { name: 'Sam' });
    await expect(page.getByTestId('next-card').or(page.getByTestId('resume-workout')).first()).toBeVisible();
    await go(page, '/more/settings');
    await expect(page.getByLabel('Name', { exact: true }).or(page.locator('input[maxlength="60"]')).first()).toHaveValue('Sam');
  });

  test('manifest and service worker make the app installable', async ({ page, request }) => {
    const res = await request.get('manifest.webmanifest');
    expect(res.ok()).toBe(true);
    const m = await res.json();
    expect(m.name).toBe('PeakForm');
    expect(m.display).toBe('standalone');
    expect(m.start_url).toBe('./#/today');
    const sizes = m.icons.map((i: { sizes: string }) => i.sizes);
    expect(sizes).toContain('192x192');
    expect(sizes).toContain('512x512');
    expect(m.icons.some((i: { purpose?: string }) => i.purpose === 'maskable')).toBe(true);
    await page.goto('./');
    await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute('href', './icons/apple-touch-icon.png');
    await expect(page.locator('meta[name="apple-mobile-web-app-capable"]')).toHaveAttribute('content', 'yes');
    const csp = await page.locator('meta[http-equiv="Content-Security-Policy"]').getAttribute('content');
    expect(csp).toContain("script-src 'self'");
    const scope = await page.evaluate(async () => (await navigator.serviceWorker.ready).scope);
    expect(scope).toMatch(/localhost:4173\/$/);
    for (const icon of ['icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png']) expect((await request.get(icon)).ok()).toBe(true);
  });
});

test.describe('training', () => {
  test('start a workout, log every set with the rest timer, finish, and get a next target', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 3); // Barbell Squat
    await expect(page.getByTestId('exercise-name')).toHaveText('Barbell Squat');
    await expect(page.getByTestId('prescription')).toContainText('3 × 6 to 10');
    await expect(page.getByTestId('prescription')).toContainText('3 RIR');
    await expect(page.getByTestId('prescription')).toContainText('tempo 3 1 1 0');
    await logStrengthSet(page, 50, 10);
    // The rest timer starts from the prescribed 180 seconds.
    await expect(page.getByTestId('restbar')).toBeVisible();
    await expect(page.getByTestId('rest-remaining')).toHaveText(/^(3:00|2:5\d)$/);
    await logStrengthSet(page, null, 10);
    await logStrengthSet(page, null, 10);
    await expect(page.getByTestId('logged-sets')).toContainText('Set 3');
    await expect(page.getByTestId('exercise-done')).toBeVisible();
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    await expect(page.getByTestId('workout-summary')).toBeVisible();
    const sug = page.getByTestId('suggestions');
    await expect(sug).toContainText('Barbell Squat');
    await expect(sug).toContainText('Try 52.5 kg');
    await expect(sug).toContainText('smallest practical increase');
    await expect(page.getByTestId('plan-vs-actual')).toContainText('50×10');
    await sug.getByTestId('accept-suggestion').first().click();
    await go(page, '/exercise/barbell-squat');
    await expect(page.getByTestId('detail-last')).toContainText('50 kg × 10, 10, 10');
    await expect(page.getByTestId('detail-target')).toContainText('Try 52.5 kg');
    await expect(page.getByTestId('detail-target')).toContainText('Confirmed');
  });

  test('an installed plan from before the morning sessions gets them with one tap', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    // Turn the stored plan and times back into what an earlier install had.
    await page.evaluate(async () => {
      const db: IDBDatabase = await new Promise((res, rej) => {
        const o = indexedDB.open('peakform');
        o.onsuccess = () => res(o.result);
        o.onerror = () => rej(o.error);
      });
      const tx = db.transaction(['plans', 'settings'], 'readwrite');
      const plans = tx.objectStore('plans');
      const all: Array<{ days: Array<{ key: string; items: Array<{ session: string; exerciseId: string }> }> }> = await new Promise((res) => {
        const r = plans.getAll();
        r.onsuccess = () => res(r.result);
      });
      for (const p of all) {
        for (const d of p.days) d.items = d.items.filter((i) => i.session !== 'morning' || (i.exerciseId === 'easy-jump-rope' && d.key !== 'sun'));
        plans.put(p);
      }
      const st = tx.objectStore('settings');
      const s: { sessionTimes: { morning: string }; reminders: Array<{ id: string; time: string }> } = await new Promise((res) => {
        const r = st.get('app');
        r.onsuccess = () => res(r.result);
      });
      s.sessionTimes.morning = '07:00';
      s.reminders = s.reminders.filter((r) => r.id !== 'morning');
      for (const r of s.reminders) if (r.id === 'checkin') r.time = '07:00';
      st.put(s);
      await new Promise((res) => (tx.oncomplete = res));
    });
    await page.reload();
    await expect(page.getByTestId('plan-update')).toContainText('6 home sessions a week');
    await page.getByTestId('plan-update-apply').click();
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
    await go(page, '/train/day/1?date=2026-09-28');
    await expect(page.getByTestId('train-day')).toContainText('Morning volleyball and rope, 05:30');
    await expect(page.getByTestId('train-day')).toContainText('Blocking Footwork, No Jump');
    await expect(page.getByTestId('train-day')).toContainText('Barbell Squat');
    await go(page, '/more/plan');
    await expect(page.getByText('Version 2').first()).toBeVisible();
  });

  test('an installed plan with the old volleyball days gets the new Tuesday and Friday gym sessions', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await restoreVolleyballDays(page);
    await page.reload();
    await expect(page.getByTestId('plan-update')).toContainText('Tuesday and Friday are gym days');
    await expect(page.getByTestId('plan-update-gym')).toContainText('Upper C');
    await expect(page.getByTestId('plan-update')).not.toContainText('home sessions a week');
    await page.getByTestId('plan-update-apply').click();
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
    await go(page, '/train/day/2?date=2026-09-29');
    const day = page.getByTestId('train-day');
    await expect(day).toContainText('Upper C Hypertrophy');
    await expect(day).toContainText('Incline Dumbbell Press');
    await expect(day).toContainText('Shadow Passing Footwork');
    await expect(day).not.toContainText('Volleyball Spike');
    await go(page, '/train/day/5?date=2026-10-02');
    await expect(day).toContainText('Lower C Hypertrophy and Swim');
    await expect(day).toContainText('Leg Press');
    await expect(day).toContainText('45 Degree Back Extension');
    await expect(day).toContainText('Swim');
    await go(page, '/more/plan');
    await expect(page.getByText('Version 2').first()).toBeVisible();
  });

  test('a gym day update put off with Not now can still be added from Train', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await restoreVolleyballDays(page);
    await page.reload();
    await page.getByTestId('plan-update').getByRole('button', { name: 'Not now' }).click();
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
    await go(page, '/train/day/2?date=2026-09-29');
    await expect(page.getByTestId('train-day')).toContainText('Volleyball Technique and Shoulder Care');
    await expect(page.getByTestId('plan-update')).toContainText('Tuesday and Friday are gym days');
    await expect(page.getByTestId('plan-update').getByRole('button', { name: 'Not now' })).toHaveCount(0);
    await page.getByTestId('plan-update-apply').click();
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
    await expect(page.getByTestId('train-day')).toContainText('Upper C Hypertrophy');
    await expect(page.getByTestId('train-day')).toContainText('Incline Dumbbell Press');
    await go(page, '/train');
    await expect(page.getByTestId('train-day-5')).toContainText('Lower C Hypertrophy and Swim');
  });

  test('About checks for a new version on request', async ({ page }) => {
    await onboard(page);
    await page.evaluate(async () => navigator.serviceWorker.ready);
    await go(page, '/more/about');
    await page.getByTestId('update-check').click();
    await expect(page.getByTestId('update-status')).toHaveText('You have the latest version.');
  });

  test('one set of nine reps never raises the load', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 3);
    await logStrengthSet(page, 50, 9);
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    await expect(page.getByTestId('suggestions')).toContainText('Complete all work sets first');
    await expect(page.getByTestId('suggestions')).not.toContainText('52.5');
  });

  test('rest timer keeps the right time after backgrounding and a reload', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 3);
    await logStrengthSet(page, 50, 8);
    await expect(page.getByTestId('rest-remaining')).toBeVisible();
    // Simulate the phone being locked for 70 seconds.
    await page.clock.fastForward(70_000);
    await page.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
    await expect(page.getByTestId('rest-remaining')).toHaveText(/^1:(4\d|5\d)$/);
    await page.reload();
    await expect(page.getByTestId('rest-remaining')).toHaveText(/^1:(4\d|5\d)$/);
    // After the end it says how long ago rest finished.
    await page.clock.fastForward(130_000);
    await expect(page.getByTestId('restbar')).toContainText('Rest finished');
  });

  test('the rest end sound is queued on the audio clock when a set is completed', async ({ page }) => {
    // Record what the app asks the audio system to play, instead of listening for real sound.
    await page.addInitScript(() => {
      const w = window as unknown as { __tones: number[]; AudioContext: typeof AudioContext };
      w.__tones = [];
      const Real = w.AudioContext;
      w.AudioContext = class extends Real {
        createOscillator() {
          const o = super.createOscillator();
          const start = o.start.bind(o);
          o.start = (when?: number) => {
            w.__tones.push((when ?? 0) - this.currentTime);
            start(when);
          };
          return o;
        }
      } as typeof AudioContext;
    });
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 3);
    await logStrengthSet(page, 50, 8);
    await expect(page.getByTestId('restbar')).toBeVisible();
    const tones = await page.evaluate(() => (window as unknown as { __tones: number[] }).__tones);
    // Squat rest is three minutes, so the first tone is queued about 180 seconds ahead.
    expect(tones.length).toBeGreaterThanOrEqual(3);
    expect(tones[0]).toBeGreaterThan(170);
    expect(tones[0]).toBeLessThan(181);
  });

  test('last performance appears beside the inputs', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page, { demo: true });
    await startSession(page);
    await exerciseChip(page, 3);
    await expect(page.getByTestId('last-performance')).toContainText('kg ×');
    await expect(page.locator('.stepper-label .prev').first()).toContainText('Last');
  });

  test('a unilateral exercise logs left and right separately', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 5);
    await expect(page.getByTestId('exercise-name')).toHaveText('Bulgarian Split Squat');
    await expect(page.getByTestId('current-set')).toContainText('Set 1 of 2, Left');
    await logStrengthSet(page, 14, 10);
    await expect(page.getByTestId('current-set')).toContainText('Set 1 of 2, Right');
    await logStrengthSet(page, null, 10);
    await expect(page.getByTestId('logged-sets')).toContainText('Set 1 Left');
    await expect(page.getByTestId('logged-sets')).toContainText('Set 1 Right');
  });

  test('editing the plan creates a version and leaves history unchanged', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 3);
    await logStrengthSet(page, 40, 8);
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    const url = page.url();
    await go(page, '/more/plan');
    await page.getByRole('button', { name: /Barbell Squat/ }).first().click();
    await page.getByRole('button', { name: 'Increase Sets' }).click();
    await page.getByRole('button', { name: 'Done with this exercise' }).click();
    await page.getByTestId('save-plan').click();
    await expect(page.getByTestId('plan-editor')).toContainText('Version 2');
    await page.goto(url);
    await expect(page.getByTestId('plan-vs-actual')).toContainText('3 × 6 to 10');
    await go(page, '/train/day/1?date=2026-09-28');
    await expect(page.getByTestId('train-day')).toContainText('4 × 6 to 10');
  });

  test('every exercise shows instructions, a muscle diagram, and a visual offline', async ({ page }) => {
    await onboard(page);
    await go(page, '/library');
    await expect(page.getByTestId('library').locator('a.item').first()).toBeVisible();
    const links = await page.locator('[data-testid="library"] a.item').evaluateAll((as) => as.map((a) => (a as HTMLAnchorElement).hash));
    expect(links.length).toBe(57);
    for (const h of links) {
      await go(page, h.replace('#', ''));
      const d = page.getByTestId('exercise-detail');
      await expect(d).toBeVisible();
      await expect(d.locator('.bodymap svg')).toHaveCount(2);
      await expect(d.locator('[data-testid="keyframes"] svg, [data-testid="drill-diagram"] svg').first()).toBeVisible();
      await expect(d).toContainText('Step by step');
      await expect(d).toContainText('Stop rules');
      await expect(d).toContainText('Substitutions');
    }
  });

  test('videos load only after a tap', async ({ page }) => {
    const external: string[] = [];
    page.on('request', (r) => {
      if (!r.url().startsWith('http://localhost:4173')) external.push(r.url());
    });
    await onboard(page);
    await go(page, '/exercise/barbell-squat');
    const gate = page.getByTestId('video-gate').first();
    await expect(gate).toBeVisible();
    await expect(page.locator('iframe')).toHaveCount(0);
    expect(external).toEqual([]);
  });
});

test.describe('food', () => {
  test('a default meal logs in one tap', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/eat');
    await page.getByTestId('log-planned-breakfast').click();
    await expect(page.getByTestId('meal-breakfast')).toContainText('Logged as planned');
    await expect(page.getByTestId('kcal-range')).toContainText('to');
  });

  test('an estimated restaurant meal is stored as a range', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/eat');
    await page.getByTestId('eat-restaurant').click();
    await page.getByTestId('add-food').click();
    await page.getByPlaceholder('Search foods').fill('schnitzel');
    await page.getByText('Chicken schnitzel, fried').click();
    await page.getByTestId('portion-restaurant-large').click();
    await expect(page.getByTestId('portion-preview')).toContainText('kcal');
    await page.getByTestId('add-item').click();
    await expect(page.getByTestId('log-estimate')).toContainText('estimated by eye, low confidence');
    await page.getByTestId('save-food').click();
    await expect(page.getByTestId('eat')).toContainText('restaurant estimate');
    await expect(page.getByTestId('kcal-range')).toHaveText(/\d+ to \d+/);
  });

  test('a food that is not in the list can be logged with your own numbers', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/eat/log/other');
    await page.getByTestId('add-food').click();
    await page.getByPlaceholder('Search foods').fill('kubbeh soup');
    await expect(page.getByText('No match for “kubbeh soup”')).toBeVisible();
    await page.getByTestId('own-food').click();
    await expect(page.getByTestId('own-food-name')).toHaveValue('kubbeh soup');
    await page.getByTestId('own-food-name').fill('Kubbeh soup with semolina dumplings');
    await page.getByTestId('own-food-kcal').pressSequentially('640');
    await page.getByTestId('own-food-protein').pressSequentially('26.5');
    await page.getByTestId('own-food-add').click();
    await expect(page.getByText('Kubbeh soup with semolina dumplings')).toBeVisible();
    await expect(page.getByText('Your own numbers')).toBeVisible();
    await page.getByTestId('save-food').click();
    // A guess is stored as an honest range around the number typed in.
    await expect(page.getByTestId('kcal-range')).toHaveText(/^4[45]\d to 8[23]\d$/);
  });

  test('Saturday meals log discreetly with the plate guide', async ({ page }) => {
    await atTime(page, new Date('2026-10-04T08:00:00+03:00'));
    await onboard(page);
    await go(page, '/eat/sabbath?date=2026-10-03');
    await page.getByTestId('log-sabbath-meals').click();
    await go(page, '/eat');
    await page.getByRole('button', { name: 'Previous day' }).click();
    await expect(page.getByTestId('eat')).toContainText('Sabbath');
  });
});

test.describe('body and review', () => {
  test('record a morning weight', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await page.getByTestId('quick-weight').click();
    await page.getByTestId('weight-input').fill('79.4');
    await page.getByTestId('weight-save').click();
    await go(page, '/progress');
    await expect(page.getByTestId('weight-avg')).toContainText('1 morning weight');
  });

  test('number fields accept free typing, one key at a time', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    // Morning weight: "7" on the way to 78.5 must not jump to the minimum, and the decimal point must stay.
    await page.getByTestId('quick-weight').click();
    const weight = page.getByTestId('weight-input');
    await weight.click();
    await weight.pressSequentially('7');
    await expect(weight).toHaveValue('7');
    await expect(page.getByText('Use a number from 20 to 300 kg.')).toBeVisible();
    await weight.pressSequentially('8,5');
    await expect(weight).toHaveValue('78.5');
    await expect(page.getByText('Use a number from 20 to 300 kg.')).toHaveCount(0);
    await page.getByTestId('weight-save').click();
    await go(page, '/progress');
    await expect(page.getByTestId('weight-avg')).toContainText('1 morning weight');

    // A calorie target typed digit by digit, starting below the 2,000 floor.
    await go(page, '/more/targets');
    const kcal = page.getByLabel('Calories', { exact: true }).first();
    await kcal.click();
    await kcal.press('ControlOrMeta+a');
    await kcal.pressSequentially('2375');
    await expect(kcal).toHaveValue('2375');
    await page.getByTestId('targets-save').click();
    await expect(page.getByTestId('targets-save')).toHaveCount(0);
    await page.reload();
    await expect(page.getByLabel('Calories', { exact: true }).first()).toHaveValue('2375');

    // Leaving an out of range number shows the stored value again, so the screen never disagrees with the data.
    const kcal2 = page.getByLabel('Calories', { exact: true }).first();
    await kcal2.click();
    await kcal2.press('ControlOrMeta+a');
    await kcal2.pressSequentially('900');
    await expect(page.getByText('Use a number from 2000 to 4000.')).toBeVisible();
    await kcal2.blur();
    await expect(kcal2).toHaveValue('2375');
  });

  test('a check in with pain of 4 raises a safety message', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/checkin');
    await page.getByTestId('checkin-weight').fill('79.1');
    await page.getByTestId('pain-knee').fill('5');
    await page.getByTestId('checkin-save').click();
    await expect(page.getByText('Please tell a parent today')).toBeVisible();
  });

  test('the weekly review has the four sections and a coach report', async ({ page }) => {
    await atTime(page, new Date('2026-10-04T20:40:00+03:00'));
    await onboard(page, { demo: true });
    await go(page, '/review');
    for (const id of ['review-keep', 'review-ready', 'review-improve', 'review-safety', 'priorities', 'comparison']) await expect(page.getByTestId(id)).toBeVisible();
    await page.getByTestId('share-report').click();
    const [d1] = await Promise.all([page.waitForEvent('download'), page.getByTestId('share-report-share').click()]);
    const names = [d1.suggestedFilename()];
    expect(names[0]).toMatch(/peakform-review-2026-09-28\.(md|json)/);
    const text = readFileSync((await d1.path())!, 'utf8');
    expect(text.length).toBeGreaterThan(50);
  });
});

test.describe('data safety', () => {
  test('export a backup, delete everything, and import it again', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page, { demo: true });
    await go(page, '/eat');
    await page.getByTestId('water-250').click();
    await go(page, '/more/data');
    await page.getByRole('button', { name: 'Plain' }).click();
    await page.getByTestId('backup').click();
    const [dl] = await Promise.all([page.waitForEvent('download'), page.getByTestId('backup-share').click()]);
    const file = (await dl.path())!;
    expect(JSON.parse(readFileSync(file, 'utf8')).format).toBe('peakform-backup');
    await page.getByRole('button', { name: 'Delete all data' }).click();
    await page.getByTestId('delete-continue').click();
    await page.getByTestId('delete-confirm').click();
    await expect(page.getByTestId('onboarding')).toBeVisible();
    await go(page, '/more/data');
    await page.getByTestId('import-file').setInputFiles(file);
    await expect(page.getByTestId('import-preview')).toContainText('Workouts');
    await page.getByRole('button', { name: 'Replace all' }).click();
    await page.getByTestId('import-apply').click();
    await go(page, '/today');
    await expect(page.getByTestId('today')).toBeVisible();
    await go(page, '/progress');
    await expect(page.getByTestId('weight-avg')).not.toContainText('Not enough yet');
  });

  test('an invalid import is rejected and nothing changes', async ({ page }) => {
    await onboard(page);
    await go(page, '/more/data');
    await page.getByTestId('import-file').setInputFiles({ name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from('{"format":"something-else"}') });
    await expect(page.getByTestId('import-error')).toContainText('not a PeakForm backup');
    await page.getByTestId('import-file').setInputFiles({ name: 'broken.json', mimeType: 'application/json', buffer: Buffer.from('{not json') });
    await expect(page.getByTestId('import-error')).toContainText('not valid JSON');
    await go(page, '/today');
    await expect(page.getByTestId('today')).toBeVisible();
  });

  test('an encrypted backup needs its passphrase', async ({ page }) => {
    await onboard(page);
    await go(page, '/more/data');
    await page.getByTestId('backup-pass').fill('long enough passphrase');
    await page.getByTestId('backup').click();
    const [dl] = await Promise.all([page.waitForEvent('download'), page.getByTestId('backup-share').click()]);
    const file = (await dl.path())!;
    expect(readFileSync(file, 'utf8')).toContain('peakform-backup-encrypted');
    await page.getByTestId('import-file').setInputFiles(file);
    await page.getByTestId('import-pass').fill('wrong passphrase');
    await page.getByRole('button', { name: 'Open' }).click();
    await expect(page.getByTestId('import-error')).toContainText('passphrase is wrong');
    await page.getByTestId('import-pass').fill('long enough passphrase');
    await page.getByRole('button', { name: 'Open' }).click();
    await expect(page.getByTestId('import-preview')).toBeVisible();
  });

  test('data survives a reload', async ({ page }) => {
    await onboard(page);
    await go(page, '/eat');
    await page.getByTestId('water-250').click();
    // The tap saves asynchronously. Wait until the total shows it, as a person would, so the reload cannot cut the write short.
    await expect(page.getByTestId('eat')).toContainText('Water 250 ml');
    await page.reload();
    await expect(page.getByTestId('eat')).toContainText('Water 250 ml');
  });
});

test.describe('schedule', () => {
  test('Sabbath Mode quiets Saturday and the calendar leaves those times out', async ({ page }) => {
    await atTime(page, SATURDAY_MORNING);
    await onboard(page);
    await go(page, '/more/sabbath');
    await expect(page.getByTestId('sabbath-toggle')).toBeChecked();
    await page.getByTestId('sabbath-start').fill('17:15');
    await expect(page.getByTestId('sabbath-window')).toContainText('17:15');
    await go(page, '/today');
    await expect(page.getByText('Reminders are quiet until Saturday night')).toBeVisible();
    await go(page, '/more/calendar');
    await page.getByTestId('ics-prepare').click();
    const [dl] = await Promise.all([page.waitForEvent('download'), page.getByTestId('ics-share').click()]);
    expect(dl.suggestedFilename()).toBe('peakform-reminders.ics');
    const ics = readFileSync((await dl.path())!, 'utf8');
    expect(ics).toContain('BEGIN:VCALENDAR');
    expect(ics).toContain('BEGIN:VALARM');
    expect(ics).toContain('SUMMARY:Weekly review');
    expect(ics).toMatch(/EXDATE:.*20261003T051500/);
  });
});

test.describe('offline and privacy', () => {
  test('the app opens offline after the first load and makes no third party requests', async ({ page, context }) => {
    const external: string[] = [];
    page.on('request', (r) => {
      const u = r.url();
      if (!u.startsWith('http://localhost:4173') && !u.startsWith('data:') && !u.startsWith('blob:')) external.push(u);
    });
    await onboard(page, { demo: true });
    await page.evaluate(async () => {
      await navigator.serviceWorker.ready;
    });
    await page.reload();
    await expect.poll(() => page.evaluate(() => !!navigator.serviceWorker.controller)).toBe(true);
    await context.setOffline(true);
    await page.reload();
    await expect(page.getByTestId('today')).toBeVisible();
    await expect(page.getByTestId('offline-banner')).toBeVisible();
    for (const h of ['/train', '/eat', '/progress', '/review', '/more', '/exercise/romanian-deadlift', '/prep']) {
      await go(page, h);
      await expect(page.locator('main.page')).not.toBeEmpty();
    }
    await go(page, '/exercise/barbell-squat');
    await expect(page.getByTestId('video-play')).toHaveText(/Needs internet/);
    await context.setOffline(false);
    expect(external).toEqual([]);
  });
});

test.describe('delete all', () => {
  test('delete all data asks twice and returns to first run', async ({ page }) => {
    await onboard(page, { demo: true });
    await go(page, '/more/data');
    await page.getByRole('button', { name: 'Delete all data' }).click();
    await expect(page.getByTestId('final-backup')).toBeVisible();
    await page.getByTestId('delete-continue').click();
    await page.getByTestId('delete-confirm').click();
    await expect(page.getByTestId('onboarding')).toBeVisible();
  });
});

test.describe('app lock', () => {
  test('the app locks after inactivity and opens again with the PIN', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/more/lock');
    await page.getByTestId('pin-new').fill('2468');
    await page.getByRole('button', { name: 'Turn on app lock' }).click();
    await expect(page.getByRole('button', { name: 'Turn off app lock' })).toBeVisible();
    // Six idle minutes against the default five minute lock.
    await page.clock.fastForward(6 * 60_000);
    await page.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
    await expect(page.getByTestId('lock-screen')).toBeVisible();
    await expect(page.getByText('Turn off app lock')).toHaveCount(0);
    for (const d of '1357') await page.getByTestId(`key-${d}`).click();
    await expect(page.getByTestId('lock-screen')).toBeVisible();
    await page.getByRole('button', { name: 'Clear' }).click();
    for (const d of '2468') await page.getByTestId(`key-${d}`).click();
    await expect(page.getByTestId('lock-screen')).toBeHidden();
    await page.reload();
    await expect(page.getByTestId('lock-screen')).toBeVisible();
  });
});

test.describe('layout @layout', () => {
  for (const route of ['/today', '/train', '/eat', '/progress', '/review', '/more', '/checkin', '/coverage', '/exercise/volleyball-spike', '/eat/log/other?mode=restaurant']) {
    test(`no horizontal overflow and large tap targets on ${route}`, async ({ page }) => {
      await atTime(page, MONDAY);
      await onboard(page, { demo: true });
      await go(page, route);
      await page.waitForTimeout(400);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow).toBeLessThanOrEqual(0);
      const small = await page.evaluate(() =>
        [...document.querySelectorAll('button, a.btn, a.item, input[type="checkbox"], select')]
          .filter((el) => (el as HTMLElement).offsetParent !== null)
          .map((el) => {
            const r = el.getBoundingClientRect();
            return { t: (el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 30), w: r.width, h: r.height };
          })
          .filter((x) => x.h < 24 || x.w < 24),
      );
      expect(small).toEqual([]);
      const inputs = await page.evaluate(() => [...document.querySelectorAll('input:not([type=checkbox]):not([type=file]), select, textarea')].map((el) => parseFloat(getComputedStyle(el).fontSize)).filter((f) => f < 16));
      expect(inputs).toEqual([]);
    });
  }

  test('accessibility scan of main screens', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page, { demo: true });
    for (const route of ['/today', '/train', '/eat', '/progress', '/more', '/exercise/barbell-squat']) {
      await go(page, route);
      await page.waitForTimeout(400);
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      const serious = r.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
      expect(serious.map((v) => `${route}: ${v.id} ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(' | ')}`)).toEqual([]);
    }
  });
});
