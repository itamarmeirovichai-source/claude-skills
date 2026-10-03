// Screens with no data, to check empty states read well.
import { chromium } from '@playwright/test';
import { resolve } from 'node:path';
const out = resolve(process.argv[2] ?? 'shots-empty');
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 375, height: 667 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const p = await ctx.newPage();
await p.goto('http://localhost:4173/');
await p.screenshot({ path: `${out}/00-onboarding.png` });
await p.getByTestId('onboard-start').click();
await p.getByTestId('onboard-ack').check();
await p.getByTestId('onboard-next').click();
await p.getByTestId('onboard-finish').click();
await p.waitForSelector('[data-testid="today"]');
for (const [n, h] of [['01-today', '/today'], ['02-progress', '/progress'], ['03-review', '/review'], ['04-history', '/history/'], ['05-eat', '/eat']] as const) {
  await p.evaluate((x) => (location.hash = x), h);
  await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${n}.png`, fullPage: n === '03-review' });
}
await b.close();
