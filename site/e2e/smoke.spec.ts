import { test, expect } from '@playwright/test';

test.describe('home', () => {
  test('loads with headline, CTAs and ring', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1, name: 'Product films without the shoot.' })).toBeVisible();
    await expect(page.getByRole('link', { name: /Get 5 free frames/ }).first()).toBeVisible();
    await expect(page.getByText('One take. No cuts.').first()).toBeVisible();
    await expect(page.locator('[data-card]')).toHaveCount(4);
    await expect(page.locator('#hero')).toHaveAttribute('data-state', /idle|fallback/, { timeout: 10_000 });
    await expect(page.locator('.spec-label').first()).toContainText('one take');
  });

  test('pick a film → plays → continue reveals main', async ({ page }) => {
    await page.goto('/');
    const hero = page.locator('#hero');
    await expect(hero).toHaveAttribute('data-state', 'idle', { timeout: 10_000 });
    await page.locator('[data-card="0"]').click();
    await expect(hero).toHaveAttribute('data-state', /pointing|enlarging|playing/);
    await expect(hero).toHaveAttribute('data-state', 'playing', { timeout: 15_000 });
    await expect(page.locator('[data-stage]')).toBeVisible();
    await expect.poll(async () => page.locator('[data-film]').evaluate((v: HTMLVideoElement) => v.currentTime), { timeout: 10_000 }).toBeGreaterThan(0.2);
    await page.locator('[data-continue]').click();
    await expect(hero).toHaveAttribute('data-state', 'revealed', { timeout: 15_000 });
    const top = await page.locator('#content').evaluate((el) => el.getBoundingClientRect().top);
    expect(top).toBeLessThan(40);
  });

  test('no horizontal scroll', async ({ page }) => {
    await page.goto('/');
    const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(over).toBeLessThanOrEqual(0);
  });
});

test.describe('/frames form', () => {
  test('validates, then submits to the API', async ({ page }) => {
    await page.route('**/api/lead/start', (r) => r.fulfill({ json: { ok: true, id: '2026-10-08-abcdef12-3456', token: '1.x' } }));
    await page.route('**/api/lead/finish', (r) => r.fulfill({ json: { ok: true } }));
    await page.goto('/frames');
    const form = page.locator('form[data-lead-form]');
    await form.getByLabel('Work email').focus();
    await form.getByRole('button', { name: 'Get my 5 free frames' }).click();
    await expect(form.locator('[data-error="email"]')).toHaveText("That email doesn't look right. Check for a typo?");
    await expect(form.locator('[data-error="website"]')).toHaveText('Add your site, e.g. yourbrand.com');
    await expect(form.locator('[data-error="product"]')).toHaveText('Tell us which product.');
    await form.getByLabel('Work email').fill('founder@brand.com');
    await form.getByLabel('Your website').fill('brand.com');
    await form.getByLabel('Which product?').fill('Fig candle');
    await page.waitForTimeout(3100); // human-speed fill (server rejects < 3 s)
    await form.getByRole('button', { name: 'Get my 5 free frames' }).click();
    await expect(page).toHaveURL(/\/frames\/thanks/);
    await expect(page.getByRole('heading', { level: 1 })).toHaveText('Got it. Your frames are on the way.');
  });
});
