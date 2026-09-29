// Screenshots of the main screens on iPhone sized viewports for visual review.
// Usage: npx tsx scripts/shots.ts <out-dir> [width] [scheme] [base-url]
import { chromium, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const out = resolve(process.argv[2] ?? 'shots');
const width = Number(process.argv[3] ?? 390);
const scheme = (process.argv[4] ?? 'light') as 'light' | 'dark';
const base = process.argv[5] ?? 'http://localhost:4173/';
const heights: Record<number, number> = { 375: 667, 390: 844, 393: 852, 430: 932 };
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width, height: heights[width] ?? 844 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
  colorScheme: scheme,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
});
const page = await ctx.newPage();
const errors: string[] = [];
page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(String(e)));

async function shot(name: string, full = true) {
  await page.waitForTimeout(350);
  await page.screenshot({ path: resolve(out, `${String(width)}-${scheme}-${name}.png`), fullPage: full });
}
async function go(hash: string, page_: Page = page) {
  await page_.evaluate((h) => (window.location.hash = h), hash);
  await page_.waitForTimeout(400);
}

await page.goto(base);
await page.getByTestId('onboard-start').click();
await page.getByTestId('onboard-ack').check();
await page.getByTestId('onboard-next').click();
await page.getByTestId('onboard-demo').click();
await page.waitForSelector('[data-testid="today"]');
await shot('01-today', false);
await go('/train');
await shot('02-train');
await go('/train/start');
await page.waitForSelector('[data-testid="train-day"]');
await shot('03-train-day');
await page.getByTestId('start-main').click();
await page.waitForSelector('[data-testid="set-logger"]');
// Move to the squat, the fifth exercise
await page.locator('.ex-nav button').nth(4).click();
await shot('04-workout', false);
await page.getByTestId('complete-set').click();
await page.waitForTimeout(600);
await shot('05-workout-after-set', false);

await go('/exercise/barbell-squat');
await shot('06-exercise-detail', false);
await go('/eat');
await shot('07-eat', false);
await go('/eat/log/other?mode=restaurant');
await page.getByTestId('add-food').click();
await page.getByPlaceholder('Search foods').fill('chicken');
await page.getByText('Chicken breast, skinless').click();
await shot('08-estimate-by-eye', false);
await go('/progress');
await shot('09-progress', false);
await go('/review');
await page.waitForSelector('[data-testid="priorities"]');
await shot('10-review', false);
await go('/coverage');
await shot('11-coverage');
await go('/more');
await shot('12-more');
await go('/checkin');
await shot('13-checkin');
await go('/eat/sabbath');
await shot('14-sabbath');
await go('/prep');
await shot('15-prep');
await go('/more/data');
await shot('16-data');
await ctx.setOffline(true);
await go('/today');
await shot('17-today-offline', false);
console.log(JSON.stringify({ errors }, null, 1));
await browser.close();
