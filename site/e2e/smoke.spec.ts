import { test, expect, type Page } from '@playwright/test';

/** Scroll with the wheel in small steps, so scroll-driven scenes see every position. */
async function wheelTo(page: Page, selector: string, offset = 0): Promise<void> {
  for (let i = 0; i < 160; i++) {
    const top = await page.locator(selector).first().evaluate((el) => el.getBoundingClientRect().top);
    if (top - offset <= 0) return;
    await page.mouse.wheel(0, Math.min(240, top - offset + 1));
    await page.waitForTimeout(40);
  }
}

test.describe('home · act I (hero ring)', () => {
  test('loads with headline, offer, CTAs and the film ring', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1, name: 'Your product, filmed in one unbroken take.' })).toBeVisible();
    await expect(page.locator('[data-frames-cta]')).toBeVisible();
    await expect(page.locator('[data-card]')).toHaveCount(6);
    await expect(page.locator('[data-card="0"]')).toContainText('AURUM · Top Shelf');
    await expect(page.locator('#hero')).toHaveAttribute('data-state', /idle|fallback/, { timeout: 10_000 });
    await expect(page.locator('.tile .spec-label').first()).toContainText('one take');
    await expect(page.locator('.site-footer')).toContainText('Everything here is made with AI, including Otto and Vee.');
  });

  test('message match: utm_content swaps the H1', async ({ page }) => {
    await page.goto('/?utm_content=fatigue');
    await expect(page.locator('#hero-h1')).toHaveText('A new hero ad. No shoot, no crew.');
    await page.goto('/?utm_content=unknown');
    await expect(page.locator('#hero-h1')).toHaveText('Your product, filmed in one unbroken take.');
  });

  test('flat orbit: cards rotate upright in 2D and hold on hover', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#hero')).toHaveAttribute('data-state', 'idle', { timeout: 10_000 });
    const item = page.locator('.ring-item').first();
    const t1 = await item.evaluate((el) => el.style.transform);
    expect(t1).toMatch(/^translate\(/); // 2D only: no translate3d / rotate
    await page.waitForTimeout(1500);
    const t2 = await item.evaluate((el) => el.style.transform);
    expect(t2).not.toBe(t1);
    await page.locator('[data-card="0"]').dispatchEvent('pointerover');
    await page.waitForTimeout(1500); // the orbit eases to a stop
    const xy = (): Promise<number[]> => item.evaluate((el) => (el.style.transform.match(/-?[\d.]+/g) ?? []).map(Number));
    const h1 = await xy();
    await page.waitForTimeout(600);
    const h2 = await xy();
    h2.forEach((v, i) => expect(Math.abs(v - (h1[i] ?? 0))).toBeLessThan(1));
  });

  test('pick a film → plays → continue reveals the story', async ({ page }) => {
    await page.goto('/');
    const hero = page.locator('#hero');
    await expect(hero).toHaveAttribute('data-state', 'idle', { timeout: 10_000 });
    const card = page.locator('[data-card="1"]');
    await card.focus();
    await card.press('Enter');
    await expect(hero).toHaveAttribute('data-state', /pointing|enlarging|playing/);
    await expect(hero).toHaveAttribute('data-state', 'playing', { timeout: 15_000 });
    await expect(page.locator('[data-stage]')).toBeVisible();
    await expect.poll(async () => page.locator('[data-film]').evaluate((v: HTMLVideoElement) => v.currentTime), { timeout: 10_000 }).toBeGreaterThan(0.2);
    await page.locator('[data-continue]').click();
    await expect(hero).toHaveAttribute('data-state', 'revealed', { timeout: 15_000 });
    const top = await page.locator('#content').evaluate((el) => el.getBoundingClientRect().top);
    expect(top).toBeLessThan(90);
  });
});

test.describe('home · story', () => {
  test('Otto announces himself, then rises into Act III', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#hero')).toHaveAttribute('data-state', /idle|fallback/, { timeout: 10_000 });
    const otto = page.locator('[data-actor="otto-demo"]');
    await expect(otto).toHaveAttribute('data-state', 'off');
    // The entrance runs inside the pinned demo: peek first, then the rise.
    await wheelTo(page, '#demo', 64);
    for (let i = 0; i < 12 && (await otto.getAttribute('data-state')) === 'off'; i++) {
      await page.mouse.wheel(0, 40);
      await page.waitForTimeout(120);
    }
    await expect(otto).toHaveAttribute('data-state', 'peek', { timeout: 5_000 });
    await expect(otto.locator('[data-bubble]')).toContainText('Down here');
    for (let i = 0; i < 40 && (await otto.getAttribute('data-state')) !== 'arrived'; i++) {
      await page.mouse.wheel(0, 60);
      await page.waitForTimeout(80);
    }
    await expect(otto).toHaveAttribute('data-state', 'arrived', { timeout: 5_000 });
  });

  test('Vee walks into Act II; the sticky CTA shows away from in-flow CTAs', async ({ page }) => {
    await page.goto('/');
    await wheelTo(page, '#tired', -200);
    await expect(page.locator('[data-actor="vee-tired"]')).toHaveAttribute('data-state', /peek|arrived/, { timeout: 5_000 });
    await expect(page.locator('[data-sticky-cta]')).toHaveClass(/on/, { timeout: 5_000 });
  });

  test('sound pill: one tap turns the crew on and Vee introduces herself', async ({ page }) => {
    await page.goto('/');
    const pill = page.locator('[data-crew-sound]');
    await expect(pill).toHaveAttribute('aria-pressed', 'false');
    await pill.click();
    await expect(pill).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('[data-pill-bubble]')).toHaveText("Sound's on. I'm Vee. Producer.");
  });

  test('pricing: credited pilot note, per-card CTAs and the dated BFCM band', async ({ page }) => {
    await page.goto('/');
    const short = page.locator('[data-tier="short"]');
    await expect(short).toContainText('Short fee credited toward Premiere/Season within 30 days.');
    await expect(page.locator('[data-tier="season"] .tier-cta')).toHaveText('Book a call');
    if (Date.now() < Date.parse('2026-11-02T23:59:59-12:00')) {
      const band = page.locator('#bfcm');
      await expect(band).toContainText('Fri, Nov 13');
      await expect(band).toContainText('Mon, Nov 2');
    }
  });

  test('no horizontal scroll', async ({ page }) => {
    await page.goto('/');
    expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(0);
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
    await page.waitForTimeout(400);
    expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(0);
  });
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });
  test('same story without pins or scrubs', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await page.waitForTimeout(800);
    expect(await page.locator('.pin-spacer').count()).toBe(0);
    await expect(page.locator('[data-actor="otto-demo"]')).toHaveAttribute('data-state', 'arrived');
  });
});

test.describe('/for/[brand]', () => {
  test('private, noindex, message-matched', async ({ page }) => {
    await page.goto('/for/example-halden-fig');
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex');
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Fig & Cedar candle');
    await expect(page.getByText('Example page')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(0);
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

  test('home step-1 form (email + product page) submits to the same pipeline', async ({ page }) => {
    let body = '';
    await page.route('**/api/lead/start', async (r) => {
      body = r.request().postData() ?? '';
      await r.fulfill({ json: { ok: true, id: '2026-10-08-abcdef12-3456', token: '1.x' } });
    });
    await page.route('**/api/lead/finish', (r) => r.fulfill({ json: { ok: true } }));
    await page.goto('/#start');
    const form = page.locator('form[data-act-form="8"]');
    await form.getByLabel('Email').fill('founder@brand.com');
    await form.getByLabel('Product page URL').fill('brand.com/products/fig');
    await page.waitForTimeout(3100);
    await form.getByRole('button', { name: /Get my 5 free frames/ }).click();
    await expect(page).toHaveURL(/\/frames\/thanks/);
    expect(body).toContain('Product page: brand.com/products/fig');
  });
});
