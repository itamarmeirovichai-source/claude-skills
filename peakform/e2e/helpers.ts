import { expect, type Page } from '@playwright/test';

/** Monday 28 September 2026, 16:40 in Jerusalem: a Lower A day, just after training starts. */
export const MONDAY = new Date('2026-09-28T16:40:00+03:00');
export const SATURDAY_MORNING = new Date('2026-10-03T09:00:00+03:00');

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
export async function startSession(page: Page, which: 'main' | 'morning' | 'swim' = 'main') {
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
