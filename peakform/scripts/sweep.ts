// Visual QA sweep. Drives the real app through every major screen and state, saves a
// viewport screenshot of each, and tiles them into labelled contact sheets for review.
// Usage: npx tsx scripts/sweep.ts <out-dir> <width> <light|dark> <demo|empty|long|large|offline>
import { chromium, type Page } from '@playwright/test';
import { mkdirSync, readdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const out = resolve(process.argv[2] ?? 'sweep');
const width = Number(process.argv[3] ?? 375);
const scheme = (process.argv[4] ?? 'light') as 'light' | 'dark';
const state = process.argv[5] ?? 'demo';
const heights: Record<number, number> = { 375: 667, 390: 844, 393: 852, 430: 932 };
const height = heights[width] ?? 844;
const tag = `${width}-${scheme}-${state}`;
const dir = resolve(out, tag);
mkdirSync(dir, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width, height },
  deviceScaleFactor: 1,
  isMobile: true,
  hasTouch: true,
  colorScheme: scheme,
  timezoneId: 'Asia/Jerusalem',
  locale: 'en-US',
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
});
if (state === 'large') await ctx.addInitScript(() => document.addEventListener('DOMContentLoaded', () => (document.documentElement.style.fontSize = '125%')));
const page = await ctx.newPage();
await page.clock.install({ time: new Date('2026-09-28T16:40:00+03:00') });
await page.clock.resume();
const errors: string[] = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));

let n = 0;
async function shot(name: string, scrollTo?: string) {
  if (scrollTo) {
    await page.evaluate((sel) => {
      const el = [...document.querySelectorAll('h2, h3, [data-testid]')].find((e) => e.textContent?.trim().startsWith(sel) || (e as HTMLElement).dataset.testid === sel);
      if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 70 });
    }, scrollTo);
  }
  await page.waitForTimeout(350);
  await page.screenshot({ path: resolve(dir, `${String(n++).padStart(2, '0')}-${name}.png`) });
}
async function go(hash: string) {
  await page.evaluate((h) => (window.location.hash = h), hash);
  await page.waitForTimeout(450);
  await page.evaluate(() => window.scrollTo(0, 0));
}
async function onboard(p: Page, demo: boolean) {
  await p.goto('http://localhost:4173/');
  await shot('onboarding-welcome');
  await p.getByTestId('onboard-start').click();
  await shot('onboarding-parent');
  await p.getByTestId('onboard-ack').check();
  await p.getByTestId('onboard-next').click();
  await shot('onboarding-week');
  await p.getByTestId(demo ? 'onboard-demo' : 'onboard-finish').click();
  await p.waitForSelector('[data-testid="today"]');
}

await onboard(page, state !== 'empty');

if (state === 'long') {
  // Realistic long content: long names, long notes, a long app name.
  await page.evaluate(async () => {
    const open = indexedDB.open('peakform');
    const db: IDBDatabase = await new Promise((res, rej) => {
      open.onsuccess = () => res(open.result);
      open.onerror = () => rej(open.error);
    });
    const tx = db.transaction(['settings', 'customExercises', 'dayNotes', 'foodLogs'], 'readwrite');
    const st = tx.objectStore('settings');
    const s = await new Promise<Record<string, unknown>>((res) => {
      const r = st.get('app');
      r.onsuccess = () => res(r.result);
    });
    st.put({ ...s, appName: 'PeakForm Training and Recovery Journal' });
    const t = Date.now();
    tx.objectStore('customExercises').put({ id: 'custom-long', createdAt: t, updatedAt: t, name: 'Single Arm Half Kneeling Landmine Press With a Pause', kind: 'strength', primary: ['delt_anterior', 'pec_clavicular'], secondary: ['triceps', 'obliques_core', 'serratus_anterior'], logSides: true, loadIncrement: 'upper', equipment: 'Landmine attachment and barbell', notes: 'Keep the ribs down, press up and slightly forward, and pause for one second at the bottom of every rep.' });
    const today = new Date().toISOString().slice(0, 10);
    tx.objectStore('dayNotes').put({ id: 'note-long', createdAt: t, updatedAt: t, date: today, kind: 'schedule-changed', note: 'Practice ran late, so training moved from 16:30 to 17:45 and dinner was at a friend’s house with a big pasta dish and a salad with a creamy dressing.' });
    await new Promise((res) => (tx.oncomplete = res));
  });
  await page.reload();
  await page.waitForSelector('[data-testid="today"]');
}

await shot('today');
await page.evaluate(() => window.scrollTo(0, 700));
await shot('today-scrolled');
await page.getByTestId('quick-weight').click();
await shot('quick-weight-sheet');
await page.keyboard.press('Escape');

await go('/train');
await shot('train');
await go('/train/day/1?date=2026-09-28');
await shot('train-day');
await shot('train-day-list', 'Main session');
if (state !== 'offline') {
  await page.getByTestId('start-main').click();
  await page.waitForSelector('[data-testid="set-logger"]');
  await shot('workout-warmup');
  await page.locator('.ex-nav button').nth(1).click();
  await shot('workout-jump');
  await page.locator('.ex-nav button').nth(3).click();
  await shot('workout-squat');
  await page.getByTestId('input-weight').fill('50');
  await page.getByTestId('input-reps').fill('9');
  await page.getByTestId('complete-set').click();
  await page.waitForTimeout(400);
  await shot('workout-squat-resting');
  await page.evaluate(() => window.scrollTo(0, 500));
  await shot('workout-squat-lower');
  await page.getByRole('button', { name: 'Had to stop' }).click();
  await shot('workout-pain-stop', 'Pain');
  await page.getByRole('button', { name: 'None' }).first().click();
  await page.locator('.ex-nav button').nth(5).click();
  await shot('workout-unilateral');
  await page.getByTestId('substitute').click();
  await shot('workout-substitute-sheet');
  await page.keyboard.press('Escape');
  await page.getByTestId('finish-workout').click();
  await shot('workout-finish-sheet');
  await page.getByTestId('confirm-finish').click();
  await page.waitForSelector('[data-testid="workout-summary"]');
  await shot('workout-summary');
  await shot('workout-plan-actual', 'Plan and actual');
  await go('/train/day/0?date=2026-09-28');
  await page.getByTestId('start-swim').click();
  await page.waitForSelector('[data-testid="set-logger"]');
  await shot('workout-swim');
  await page.getByTestId('finish-workout').click();
  await page.getByRole('button', { name: 'Discard this workout' }).click();
  await page.waitForSelector('[data-testid="train"]');
}
await go('/exercise/barbell-squat');
await shot('exercise-top');
await shot('exercise-muscles', 'Muscles');
await shot('exercise-stop', 'Stop rules');
await shot('exercise-video', 'Video');
await go('/exercise/volleyball-approach-footwork');
await shot('exercise-drill');
if (state === 'long') {
  await go('/exercise/custom-long');
  await shot('exercise-custom-long');
}
await go('/library');
await shot('library');
await go('/eat');
await shot('eat');
await shot('eat-meals', 'Meals');
await page.getByTestId('log-planned-breakfast').click().catch(() => {});
await shot('eat-after-log', 'Meals');
await go('/eat/log/lunch?mode=template');
await shot('food-change-template');
await go('/eat/log/other?mode=restaurant');
await page.getByTestId('add-food').click();
await shot('food-picker-search');
await page.getByPlaceholder('Search foods').fill('rice');
await page.getByText('White rice').first().click();
await shot('estimate-by-eye');
await page.getByRole('button', { name: 'Grams' }).click();
await shot('estimate-grams');
await page.getByTestId('add-item').click();
await shot('restaurant-with-item');
await go('/eat/sabbath');
await shot('sabbath-plate');
await go('/prep');
await shot('meal-prep');
await go('/recipe/lentil-soup');
await shot('recipe');
await go('/progress');
await shot('progress');
await shot('progress-gate', 'Nutrition check');
await go('/coverage');
await shot('coverage');
await shot('coverage-shoulder', 'Shoulder load');
await go('/history/barbell-squat');
await shot('history');
await go('/review');
await page.waitForSelector('[data-testid="priorities"], [data-testid="review"]');
await page.waitForTimeout(600);
await shot('review');
await shot('review-safety', 'Safety flags');
await go('/checkin');
await shot('checkin');
await shot('checkin-pain', 'Pain, 0 to 10');
for (const p of ['more', 'more/schedule', 'more/calendar', 'more/sabbath', 'more/settings', 'more/targets', 'more/supplements', 'more/data', 'more/lock', 'more/plan', 'more/privacy', 'more/safety', 'more/about', 'more/sources', 'more/recommendation']) {
  await go(`/${p}`);
  await shot(p.replace('/', '-'));
}
if (state === 'offline') {
  await go('/today');
  await ctx.setOffline(true);
  await page.reload();
  await page.waitForSelector('[data-testid="today"]');
  await shot('offline-today');
  await go('/exercise/barbell-squat');
  await shot('offline-video', 'Video');
}
// Lock screen
await go('/more/lock');
await page.getByTestId('pin-new').fill('2468');
await page.getByRole('button', { name: 'Turn on app lock' }).click();
await page.getByRole('button', { name: 'Turn off app lock' }).waitFor();
await page.clock.fastForward(6 * 60_000);
await page.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
await page.waitForTimeout(500);
await shot('lock-screen');

// Contact sheets, 8 screenshots per sheet in 4 columns.
const files = readdirSync(dir).filter((f) => f.endsWith('.png')).sort();
const sheetPage = await browser.newPage({ viewport: { width: 4 * (width + 16) + 16, height: 1000 } });
for (let i = 0; i < files.length; i += 8) {
  const group = files.slice(i, i + 8);
  const html = `<!doctype html><body style="margin:8px;background:#777;font-family:system-ui"><div style="display:grid;grid-template-columns:repeat(4,${width}px);gap:8px">${group
    .map((f) => `<figure style="margin:0"><div style="font-size:12px;color:#fff;padding:2px 0">${f}</div><img src="data:image/png;base64,${readFileSync(resolve(dir, f)).toString('base64')}" style="width:${width}px;display:block"></figure>`)
    .join('')}</div></body>`;
  await sheetPage.setContent(html);
  await sheetPage.waitForTimeout(300);
  await sheetPage.screenshot({ path: resolve(out, `${tag}-sheet-${String(i / 8).padStart(2, '0')}.png`), fullPage: true });
}
console.log(JSON.stringify({ tag, shots: files.length, errors }, null, 1));
await browser.close();
