import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
import { FRIDAY, MONDAY, ROOMY_HOME, SATURDAY_MORNING, THURSDAY, atTime, exerciseChip, go, logStrengthSet, makeOldInstall, onboard, setKv, startSession } from './helpers';

test.describe('first run and install', () => {
  test('first run setup lands on Today with the profile saved locally', async ({ page }) => {
    // A training day, so Today has a next session to show. On the Saturday rest day it says all done.
    await atTime(page, MONDAY);
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
    // The gym session holds strength work only: Lower A starts with the leg press.
    await expect(page.getByTestId('exercise-name')).toHaveText('Leg Press');
    await expect(page.getByTestId('prescription')).toContainText('3 × 6 to 10');
    // A new exercise stays three reps short for its first two sessions. Nothing goes to failure.
    await expect(page.getByTestId('prescription')).toContainText('3 RIR while learning');
    await expect(page.getByTestId('learning-note')).toContainText('After that, 2 RIR');
    await logStrengthSet(page, 50, 10);
    await expect(page.getByTestId('restbar')).toBeVisible();
    await expect(page.getByTestId('rest-remaining')).toHaveText(/^(3:00|2:5\d)$/);
    await logStrengthSet(page, null, 10);
    await logStrengthSet(page, null, 10);
    // After the last set the workout moves on to the next exercise.
    await expect(page.getByRole('button', { name: '1. Leg Press, done' })).toBeVisible();
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    await expect(page.getByTestId('workout-summary')).toBeVisible();
    const sug = page.getByTestId('suggestions');
    await expect(sug).toContainText('Leg Press');
    await expect(sug).toContainText('Try 52.5 kg');
    await expect(sug).toContainText('smallest practical increase');
    await expect(page.getByTestId('plan-vs-actual')).toContainText('50×10');
    await sug.getByTestId('accept-suggestion').first().click();
    await go(page, '/exercise/leg-press');
    await expect(page.getByTestId('detail-last')).toContainText('50 kg × 10, 10, 10');
    await expect(page.getByTestId('detail-target')).toContainText('Try 52.5 kg');
    await expect(page.getByTestId('exercise-wrist')).toContainText('No wrist load');
    await expect(page.getByTestId('exercise-progression')).toContainText('One good set is not enough');
  });

  test('a gym day shows its location, space, duration, and stop rules, with the home session first', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/train/day/1?date=2026-09-28');
    const day = page.getByTestId('train-day');
    await expect(day.getByTestId('session-info-home')).toContainText('Home');
    await expect(day.getByTestId('session-info-main')).toContainText('Gym');
    await expect(day.getByTestId('session-info-main')).toContainText('About');
    await expect(day.getByTestId('session-info-main')).toContainText('Equipment');
    // textContent, because section headings are shown in capitals.
    const text = (await day.textContent()) ?? '';
    expect(text.indexOf('Home jumps and skills')).toBeLessThan(text.indexOf('Gym strength'));
    // The home space is not described yet, so the home session has no jumps.
    await expect(day).toContainText('Home Movement Prep');
    await expect(day).not.toContainText('Pogo Hop');
    await expect(day).not.toContainText('to failure');
    await go(page, '/train');
    await expect(page.getByTestId('train-day-2')).toContainText('No structured training');
  });

  test('an installed 2.1 plan is offered the new week: questions, the difference, then activation', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await makeOldInstall(page);
    await page.reload();
    const card = page.getByTestId('plan-update');
    await expect(card).toContainText('a calmer week with more recovery');
    await card.getByTestId('plan-update-start').click();
    await expect(page.getByTestId('athlete')).toBeVisible();
    const pick = async (group: string, value: string) => page.getByTestId(group).locator(`button[data-value="${value}"]`).click();
    await pick('wrist-status', 'not-cleared');
    await pick('home-space', 'large');
    await pick('home-ceiling', 'standard');
    await pick('home-surface', 'mat');
    await pick('home-noise', 'no');
    await pick('home-breakables', 'no');
    await pick('home-outdoor', 'large');
    await pick('home-outdoor-surface', 'grass');
    await page.getByTestId('athlete-home').getByRole('button', { name: 'Tape' }).click();
    await page.getByTestId('athlete-build').click();
    const preview = page.getByTestId('plan-preview');
    await expect(preview).toContainText('not active yet');
    await expect(page.getByTestId('plan-summary')).toContainText('Four gym strength days');
    await expect(preview).toContainText('The morning check in moves from 05:15 to 07:00');
    const diff = page.getByTestId('plan-diff');
    await expect(diff).toContainText('Monday');
    await expect(diff).toContainText('Snap Down and Stick');
    await expect(diff).toContainText('Easy Jump Rope');
    // Nothing changed yet.
    await go(page, '/train/day/1?date=2026-09-28');
    await expect(page.getByTestId('train-day')).toContainText('Easy Jump Rope');
    await go(page, '/plan');
    await page.getByTestId('plan-activate').click();
    await expect(page.getByTestId('train')).toBeVisible();
    await go(page, '/train/day/1?date=2026-09-28');
    const day = page.getByTestId('train-day');
    await expect(day).toContainText('Pogo Hop');
    await expect(day).toContainText('Lateral Line Hop');
    await expect(day).not.toContainText('Easy Jump Rope');
    await go(page, '/train/day/5?date=2026-10-02');
    // The wrist is not cleared, so the arm swing has no ball.
    await expect(day).toContainText('Spike Arm Swing, No Ball');
    await expect(day).not.toContainText('Wall Spike Control');
    await go(page, '/more/plan');
    await expect(page.getByText('Version 2').first()).toBeVisible();
    await go(page, '/today');
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
  });

  test('the new week offer put off with Not now can still be found on Train', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await makeOldInstall(page);
    await page.reload();
    await page.getByTestId('plan-update').getByRole('button', { name: 'Not now' }).click();
    await expect(page.getByTestId('plan-update')).toHaveCount(0);
    await go(page, '/train');
    await expect(page.getByTestId('plan-update')).toContainText('a calmer week');
    await expect(page.getByTestId('plan-update').getByRole('button', { name: 'Not now' })).toHaveCount(0);
  });

  test('the questionnaire shows the changes before the program is saved', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/program');
    await expect(page.getByTestId('program')).toContainText('How your program works');
    await expect(page.getByTestId('program')).toContainText('about two reps short of failure');
    await page.getByTestId('program-start').click();
    await expect(page.getByTestId('slot-shoulder-care')).toBeVisible();
    await page.getByTestId('program-next').click();
    // Upper chest is trained twice: keep the machine first and choose the Smith press second.
    const slot = page.getByTestId('slot-chest-upper');
    await slot.getByTestId('choice-incline-dumbbell-press').click();
    await slot.getByTestId('choice-incline-smith-press').click();
    await expect(slot.getByTestId('choice-incline-machine-press')).toContainText('1st');
    await expect(slot.getByTestId('choice-incline-smith-press')).toContainText('2nd');
    await page.reload();
    await expect(page.getByTestId('slot-chest-upper').getByTestId('choice-incline-smith-press')).toContainText('2nd');
    await go(page, `/program?step=99`);
    await expect(page.getByTestId('program-summary')).toContainText('Incline Machine Chest Press');
    await expect(page.getByTestId('jump-level')).toContainText('Starting level');
    await page.getByTestId('program-save').click();
    await expect(page.getByTestId('plan-diff')).toContainText('Incline Smith Machine Press');
    await page.getByTestId('plan-activate').click();
    await expect(page.getByTestId('train')).toBeVisible();
    await go(page, '/train/day/3?date=2026-09-30');
    const day = page.getByTestId('train-day');
    await expect(day).toContainText('Upper B');
    await expect(day).toContainText('Incline Smith Machine Press');
    await go(page, '/train/day/0?date=2026-10-04');
    await expect(day).toContainText('Incline Machine Chest Press');
    await go(page, '/more/plan');
    await expect(page.getByText('Version 2').first()).toBeVisible();
  });

  test('home drills follow the space and the wrist, and change only through a preview', async ({ page }) => {
    await atTime(page, THURSDAY);
    await onboard(page);
    await expect(page.getByTestId('open-questions')).toContainText('Wrist after an injury');
    await setKv(page, { homeSetup: ROOMY_HOME, wristInfo: { status: 'cleared', clearedBy: 'orthopaedic doctor', date: '2026-09-20', limits: '' } });
    await go(page, '/more/athlete');
    await page.getByTestId('athlete-build').click();
    const diff = page.getByTestId('plan-diff');
    await expect(diff).toContainText('Thursday');
    await expect(diff).toContainText('Countermovement Jump');
    await expect(diff).toContainText('Wall Spike Control');
    await page.getByTestId('plan-activate').click();
    await expect(page.getByTestId('train')).toBeVisible();
    await go(page, '/train/day/4?date=2026-10-01');
    const day = page.getByTestId('train-day');
    await expect(day.getByTestId('session-info-home')).toContainText('about 58 landings');
    // The ceiling indoors is too low for full jumps, so they are planned outdoors, with a note in the workout.
    await startSession(page, 'home');
    await exerciseChip(page, 4);
    await expect(page.getByTestId('exercise-name')).toHaveText('Countermovement Jump');
    await expect(page.getByTestId('set-logger')).toContainText('Outdoors, on a flat, dry surface.');
    await go(page, '/today');
    await expect(page.getByTestId('open-questions')).toHaveCount(0);
  });

  test('About checks for a new version on request', async ({ page }) => {
    await onboard(page);
    await page.evaluate(async () => navigator.serviceWorker.ready);
    await go(page, '/more/about');
    await page.getByTestId('update-check').click();
    await expect(page.getByTestId('update-status')).toHaveText('You have the latest version.');
  });

  test('jump tests on Progress compare like with like, with no dunk target', async ({ page }) => {
    await atTime(page, FRIDAY);
    await onboard(page);
    await go(page, '/progress');
    const tests = page.getByTestId('jump-tests');
    await expect(tests).toContainText('No jump test yet');
    await expect(page.getByTestId('progress')).not.toContainText(/dunk/i);
    await tests.getByTestId('jump-test-add').click();
    await page.getByTestId('jt-reach').fill('240');
    await page.getByTestId('jt-s0').fill('286');
    await page.getByTestId('jt-s1').fill('288');
    await page.getByTestId('jt-save').click();
    await expect(tests.getByTestId('jump-standing')).toContainText('48 cm');
    await expect(tests).toContainText('The next test done the same way');
  });

  test('school sport counts toward the week', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await go(page, '/more/sport');
    await page.getByTestId('sport-jumping').locator('button[data-value="lots"]').click();
    await page.getByTestId('sport-save').click();
    await expect(page.getByTestId('sport-list')).toContainText('Volleyball, 90 min');
    await expect(page.getByTestId('sport-week')).toContainText('Sport 90 min');
    await expect(page.getByTestId('sport-week')).toContainText('a lot of jumping: 1');
  });

  test('one set of nine reps never raises the load', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await logStrengthSet(page, 50, 9);
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    await expect(page.getByTestId('suggestions')).toContainText('Complete all work sets first');
    await expect(page.getByTestId('suggestions')).not.toContainText('52.5');
  });

  test('a double tap on Complete saves one set, not two', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await page.getByTestId('input-weight').fill('50');
    await page.getByTestId('input-reps').fill('10');
    await page.getByTestId('complete-set').dblclick();
    await expect(page.getByTestId('current-set')).toContainText('Set 2 of 3');
    await page.waitForTimeout(300);
    await expect(page.getByTestId('logged-sets').locator('.set-card')).toHaveCount(1);
  });

  test('rest timer keeps the right time after backgrounding and a reload', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
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
    await logStrengthSet(page, 50, 8);
    await expect(page.getByTestId('restbar')).toBeVisible();
    const tones = await page.evaluate(() => (window as unknown as { __tones: number[] }).__tones);
    // Leg press rest is three minutes, so the first tone is queued about 180 seconds ahead.
    expect(tones.length).toBeGreaterThanOrEqual(3);
    expect(tones[0]).toBeGreaterThan(170);
    expect(tones[0]).toBeLessThan(181);
  });

  test('last performance appears beside the inputs', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page, { demo: true });
    await startSession(page);
    await expect(page.getByTestId('last-performance')).toContainText('kg ×');
    await expect(page.locator('.stepper-label .prev').first()).toContainText('Last');
  });

  test('a unilateral exercise logs left and right separately', async ({ page }) => {
    await atTime(page, THURSDAY);
    await onboard(page);
    await startSession(page);
    await exerciseChip(page, 0);
    await expect(page.getByTestId('exercise-name')).toHaveText('Bulgarian Split Squat');
    await expect(page.getByTestId('current-set')).toContainText('Set 1 of 3, Left');
    await logStrengthSet(page, 14, 10);
    await expect(page.getByTestId('current-set')).toContainText('Set 1 of 3, Right');
    await logStrengthSet(page, null, 10);
    await expect(page.getByTestId('logged-sets')).toContainText('Set 1 Left');
    await expect(page.getByTestId('logged-sets')).toContainText('Set 1 Right');
  });

  test('editing the plan shows the difference, creates a version, and leaves history unchanged', async ({ page }) => {
    await atTime(page, MONDAY);
    await onboard(page);
    await startSession(page);
    await logStrengthSet(page, 40, 8);
    await page.getByTestId('finish-workout').click();
    await page.getByTestId('confirm-finish').click();
    const url = page.url();
    await go(page, '/more/plan');
    await page.getByRole('button', { name: /Leg Press/ }).first().click();
    await page.getByRole('button', { name: 'Increase Sets' }).click();
    await page.getByRole('button', { name: 'Done with this exercise' }).click();
    await page.getByTestId('save-plan').click();
    await expect(page.getByTestId('plan-diff')).toContainText('3 × 6 to 10, 2 in reserve → 4 × 6 to 10, 2 in reserve');
    await page.getByTestId('plan-activate').click();
    await expect(page.getByTestId('train')).toBeVisible();
    await go(page, '/more/plan');
    await expect(page.getByTestId('plan-editor')).toContainText('Version 2');
    await page.goto(url);
    await expect(page.getByTestId('plan-vs-actual')).toContainText('3 × 6 to 10');
    await go(page, '/train/day/1?date=2026-09-28');
    await expect(page.getByTestId('train-day')).toContainText('4 × 6 to 10');
  });

  test('every exercise shows instructions, a muscle diagram, a visual, and wrist guidance offline', async ({ page }) => {
    await onboard(page);
    await go(page, '/library');
    await expect(page.getByTestId('library').locator('a.item').first()).toBeVisible();
    const links = await page.locator('[data-testid="library"] a.item').evaluateAll((as) => as.map((a) => (a as HTMLAnchorElement).hash));
    expect(links.length).toBe(103);
    for (const h of links) {
      await go(page, h.replace('#', ''));
      const d = page.getByTestId('exercise-detail');
      await expect(d).toBeVisible();
      await expect(d.locator('.bodymap svg')).toHaveCount(2);
      await expect(d.locator('[data-testid="keyframes"] svg, [data-testid="drill-diagram"] svg').first()).toBeVisible();
      await expect(d).toContainText('Step by step');
      await expect(d).toContainText('Stop rules');
      await expect(d).toContainText('Substitutions');
      await expect(d.getByTestId('exercise-wrist')).toBeVisible();
      await expect(d.getByTestId('exercise-progression')).toBeVisible();
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
    // There is no calorie target until a professional reviews one: the example meals are shown as examples only.
    await expect(page.getByTestId('example-total')).toContainText('Example meals');
    await expect(page.getByTestId('example-total')).toContainText('not a target');
    await expect(page.getByTestId('example-context')).toContainText('pediatric sports dietitian');
    await expect(page.getByTestId('eat')).toContainText('Example serving. Adjust to appetite and activity; this is not a daily limit.');
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

    // A calorie range a professional reviewed, typed digit by digit. There is no built in floor or target.
    await go(page, '/more/goals');
    await page.getByTestId('reviewed-add').click();
    await page.getByTestId('reviewed-value').fill('About 3,000 kcal a day for now');
    await page.getByTestId('reviewed-source').fill('Clinic dietitian');
    const from = page.getByLabel('From, kcal', { exact: true });
    await from.click();
    await from.pressSequentially('2');
    await expect(from).toHaveValue('2');
    await expect(page.getByText('Use a number from 500 to 8000.')).toBeVisible();
    await from.pressSequentially('900');
    await expect(from).toHaveValue('2900');
    const to = page.getByLabel('To, kcal', { exact: true });
    await to.click();
    await to.press('ControlOrMeta+a');
    await to.pressSequentially('3300');
    await expect(to).toHaveValue('3300');
    await page.getByTestId('reviewed-save').click();
    await expect(page.getByTestId('reviewed-targets')).toContainText('About 3,000 kcal a day for now');
    await go(page, '/eat');
    await expect(page.getByTestId('example-total')).toContainText('2900 to 3300');
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
    for (const id of ['review-progress', 'review-missing', 'review-recovery', 'review-professional', 'review-keep', 'review-ready', 'review-improve', 'review-safety', 'priorities', 'comparison']) await expect(page.getByTestId(id)).toBeVisible();
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
    expect(ics).toMatch(/EXDATE:.*20261003T070000/);
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
  for (const route of ['/today', '/train', '/eat', '/progress', '/review', '/more', '/checkin', '/coverage', '/exercise/volleyball-spike', '/eat/log/other?mode=restaurant', '/program?step=1']) {
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
    for (const route of ['/today', '/train', '/eat', '/progress', '/more', '/exercise/barbell-squat', '/program?step=1']) {
      await go(page, route);
      await page.waitForTimeout(400);
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      const serious = r.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
      expect(serious.map((v) => `${route}: ${v.id} ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(' | ')}`)).toEqual([]);
    }
  });
});
