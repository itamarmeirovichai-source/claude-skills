import { test, expect, type Page } from '@playwright/test';

const hero = (page: Page) => page.locator('#hero');
const ready = async (page: Page): Promise<void> => {
  await expect(hero(page)).toHaveAttribute('data-state', 'idle', { timeout: 10_000 });
};
/** Bring an element to the middle of the viewport (instant, no smooth scroll). */
const centre = (page: Page, sel: string) =>
  page.locator(sel).first().evaluate((el) => {
    const r = el.getBoundingClientRect();
    window.scrollTo({ top: r.top + window.scrollY - (innerHeight - r.height) / 2, behavior: 'instant' });
  });

test.describe('home · structure and offer', () => {
  test('sections in order: hero, problem, how, work, pricing, offer, faq', async ({ page }) => {
    await page.goto('/');
    const ids = await page.locator('main > section').evaluateAll((els) => els.map((e) => e.id));
    expect(ids).toEqual(['hero', 'problem', 'how', 'work', 'pricing', 'start', 'faq']);
  });

  test('hero: one headline, one primary CTA, one secondary link, microcopy, disclosure, the ring', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1, name: 'Your product, filmed in one unbroken take.' })).toBeVisible();
    await expect(page.locator('#hero .btn-primary')).toHaveCount(1);
    await expect(page.locator('[data-frames-cta]')).toHaveText(/Get my 5 free frames/);
    await expect(page.locator('[data-watch-film]')).toHaveText(/Watch a film/);
    await expect(page.locator('#hero .micro')).toHaveText('Free. No call. 48 h.');
    await expect(page.locator('#hero .disclose')).toHaveText('Made with AI, including Otto and Vee. Spec films are for invented brands.');
    await expect(page.locator('[data-card]')).toHaveCount(6);
    await expect(page.locator('[data-card="0"]')).toContainText('AURUM');
    await ready(page);
    await expect(page.locator('.site-footer')).toContainText('Everything here is made with AI, including Otto and Vee.');
  });

  test('message match: utm_content swaps the H1', async ({ page }) => {
    await page.goto('/?utm_content=fatigue');
    await expect(page.locator('#hero-h1')).toHaveText('A new hero ad. No shoot, no crew.');
    await page.goto('/?utm_content=unknown');
    await expect(page.locator('#hero-h1')).toHaveText('Your product, filmed in one unbroken take.');
  });

  test('the price shows by the third screen', async ({ page }) => {
    await page.goto('/');
    const y = await page.getByText('$1,200', { exact: false }).first().evaluate((el) => el.getBoundingClientRect().top + window.scrollY);
    const h = await page.evaluate(() => innerHeight);
    expect(y).toBeLessThan(h * 3);
  });

  test('pricing: three cards, recommended tier marked, honest notes, BFCM without unconfirmed capacity', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#pricing [data-tier]')).toHaveCount(3);
    await expect(page.locator('[data-tier="premiere"]')).toHaveClass(/rec/);
    await expect(page.locator('[data-tier="premiere"] .ribbon')).toBeVisible();
    await expect(page.locator('[data-tier="premiere"] .tier-cta')).toHaveClass(/btn-primary/);
    await expect(page.locator('[data-tier="short"]')).toContainText('Short fee credited toward Premiere/Season within 30 days.');
    await expect(page.locator('[data-tier="season"] .tier-cta')).toHaveText('Book a call');
    await expect(page.locator('#pricing')).not.toContainText(/of \d+ left/);
    if (Date.now() < Date.parse('2026-11-02T23:59:59-12:00')) {
      const band = page.locator('#bfcm');
      await expect(band).toContainText('Fri, Nov 13');
      await expect(band).toContainText('Mon, Nov 2');
      await expect(page.locator('[data-capacity]')).toHaveCount(0); // capacityConfirmed: false
    }
  });

  test('one primary CTA style; microcopy under the frames CTAs', async ({ page }) => {
    await page.goto('/');
    const styles = await page.locator('main .btn-primary').evaluateAll((els) => [...new Set(els.map((e) => getComputedStyle(e).backgroundColor))]);
    expect(styles).toHaveLength(1);
    await expect(page.locator('#how .micro')).toHaveText('Free. No call. 48 h.');
    await expect(page.locator('#start .mini-form .note')).toContainText('Free. No call. 48 h.');
  });

  test('offer block: risk reversal and the 2-field form', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#start h2')).toHaveText('5 free frames.');
    await expect(page.locator('#start')).toContainText("If you don't love them, you owe nothing and we part friends.");
    const form = page.locator('#start form[data-lead-form]');
    await expect(form.locator('input:not([type="hidden"]):not([tabindex="-1"])')).toHaveCount(2);
  });

  test('faq: six short answers', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#faq details')).toHaveCount(6);
  });

  test('no horizontal scroll', async ({ page }) => {
    await page.goto('/');
    for (const f of [0, 0.25, 0.5, 0.75, 1]) {
      await page.evaluate((f) => window.scrollTo({ top: document.body.scrollHeight * f, behavior: 'instant' }), f);
      await page.waitForTimeout(150);
      expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(0);
    }
  });
});

test.describe('home · ring and player', () => {
  test('flat orbit: cards move upright in 2D and hold on hover', async ({ page }) => {
    await page.goto('/');
    await ready(page);
    await centre(page, '[data-scene]');
    const item = page.locator('.ring-item').first();
    const t1 = await item.evaluate((el) => el.style.transform);
    expect(t1).toMatch(/^translate\(/);
    await page.waitForTimeout(1500);
    expect(await item.evaluate((el) => el.style.transform)).not.toBe(t1);
    await page.locator('[data-card="0"]').dispatchEvent('pointerover');
    await page.waitForTimeout(1500);
    const xy = (): Promise<number[]> => item.evaluate((el) => (el.style.transform.match(/-?[\d.]+/g) ?? []).map(Number));
    const h1 = await xy();
    await page.waitForTimeout(600);
    (await xy()).forEach((v, i) => expect(Math.abs(v - (h1[i] ?? 0))).toBeLessThan(1));
  });

  test('a ring card opens the player; when the film ends Otto asks for another', async ({ page }) => {
    await page.goto('/');
    await ready(page);
    const card = page.locator('[data-card="1"]');
    await card.focus();
    await card.press('Enter');
    const dialog = page.locator('[data-film-dialog]');
    await expect(dialog).toBeVisible();
    await expect.poll(() => page.locator('[data-fd-video]').evaluate((v: HTMLVideoElement) => v.currentTime), { timeout: 10_000 }).toBeGreaterThan(0.2);
    await centre(page, '[data-slot="hero"]'); // where the visitor was when they picked the card
    await page.locator('[data-fd-video]').evaluate((v) => v.dispatchEvent(new Event('ended')));
    await expect(dialog).toBeHidden();
    await expect(page.locator('#hero [data-say]')).toContainText('Another? Or shall we make yours?', { timeout: 10_000 });
  });

  test('a work tile opens the same player', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#work .tile')).toHaveCount(6);
    await expect(page.locator('#work .tile').first()).toContainText('AURUM');
    await centre(page, '#work .tile');
    await page.locator('#work .tile').nth(2).click();
    await expect(page.locator('[data-film-dialog]')).toBeVisible();
    await expect(page.locator('[data-fd-label]')).toContainText('one take');
  });
});

test.describe('home · how it works', () => {
  test('hard-cut steps: exactly one panel shown at any moment, tabs switch it', async ({ page }) => {
    await page.goto('/');
    await centre(page, '[data-monitor]');
    const shown = () => page.locator('[role="tabpanel"]').evaluateAll((ps) => ps.filter((p) => getComputedStyle(p).display !== 'none').map((p) => p.id));
    for (let i = 0; i < 8; i++) {
      expect(await shown()).toHaveLength(1);
      await page.waitForTimeout(250);
    }
    await page.locator('#step-1').click();
    expect(await shown()).toEqual(['panel-1']);
    await page.locator('#step-2').click();
    expect(await shown()).toEqual(['panel-2']);
    await page.waitForTimeout(4000); // a pick stops the auto-advance
    expect(await shown()).toEqual(['panel-2']);
  });
});

test.describe('home · characters and lines', () => {
  test('Vee says v1 when her slot is in view; captions follow the clip clock; once per visit', async ({ page }) => {
    await page.goto('/');
    await centre(page, '[data-slot="how"]');
    const slot = page.locator('[data-slot="how"]');
    await expect(slot).toHaveAttribute('data-talking', 'v1', { timeout: 10_000 });
    // Muted (no sound chosen) but playing: lips move while the words light up in step.
    const words = slot.locator('[data-say] .w');
    await expect.poll(() => words.count(), { timeout: 8_000 }).toBeGreaterThan(5);
    await expect.poll(async () => slot.locator('[data-say] .w.on').count(), { timeout: 8_000 }).toBeGreaterThan(0);
    const total = await words.count();
    const mid = await slot.locator('[data-say] .w.on').count();
    expect(mid).toBeLessThan(total);
    await expect(slot).toHaveAttribute('data-said', '', { timeout: 15_000 });
    await expect(slot.locator('[data-say]')).toContainText('I produce, he directs.');
    expect(await page.evaluate(() => sessionStorage.getItem('vxo:lines-played'))).toContain('v1');
    await page.reload();
    await centre(page, '[data-slot="how"]');
    await page.waitForTimeout(2500);
    await expect(slot).not.toHaveAttribute('data-talking', 'v1');
  });

  test('a line waits until its slot is 60 % in view', async ({ page }) => {
    await page.goto('/');
    await page.locator('[data-slot="pricing"]').evaluate((el) => {
      const r = el.getBoundingClientRect();
      window.scrollTo({ top: r.top + window.scrollY - innerHeight + r.height * 0.3, behavior: 'instant' }); // ~30 % visible
    });
    await page.waitForTimeout(2000);
    await expect(page.locator('[data-slot="pricing"]')).not.toHaveAttribute('data-talking', /.+/);
    await centre(page, '[data-slot="pricing"]');
    await expect(page.locator('[data-slot="pricing"]')).toHaveAttribute('data-talking', 'o4', { timeout: 8_000 });
  });

  test('Sound on: Otto says o1 from the same clip, audible, in the hero', async ({ page }) => {
    await page.goto('/');
    await ready(page);
    const toggle = page.locator('header [data-sound-toggle]');
    await expect(toggle).toHaveAttribute('aria-pressed', 'false');
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-pressed', 'true');
    await centre(page, '[data-slot="hero"]');
    await expect(hero(page)).toHaveAttribute('data-talking', 'o1', { timeout: 10_000 });
    // One element carries picture and sound: the front video of Otto's canvas, unmuted, decoding audio.
    await expect
      .poll(() => page.locator('#otto').evaluate((el) => {
        const v = (el as unknown as { frontVideo: HTMLVideoElement & { webkitAudioDecodedByteCount?: number } }).frontVideo;
        return !v.muted && /lines\/o1/.test(v.currentSrc) && (v.webkitAudioDecodedByteCount ?? 1) > 0;
      }), { timeout: 8_000 })
      .toBe(true);
    await expect(page.locator('#hero [data-say]')).toContainText('Every one is a single take.', { timeout: 10_000 });
  });
});

test.describe('home · sticky CTA (phones)', () => {
  test('shows after the hero CTA, hides at the form', async ({ page, isMobile }) => {
    test.skip(!isMobile, 'phones only');
    await page.goto('/');
    const bar = page.locator('[data-sticky]');
    await expect(bar).not.toHaveClass(/on/);
    await page.evaluate(() => window.scrollTo({ top: document.getElementById('work')!.offsetTop + 300, behavior: 'instant' }));
    await expect(bar).toHaveClass(/on/, { timeout: 5_000 });
    await centre(page, '#start form');
    await expect(bar).not.toHaveClass(/on/, { timeout: 5_000 });
  });
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });
  test('still ring, still characters, captions only, steps wait for a tap', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    const item = page.locator('.ring-item').first();
    const t1 = await item.evaluate((el) => el.style.transform);
    await page.waitForTimeout(1200);
    expect(await item.evaluate((el) => el.style.transform)).toBe(t1);
    await centre(page, '[data-slot="how"]');
    await expect(page.locator('[data-slot="how"]')).toHaveClass(/poster-mode/);
    await expect(page.locator('[data-slot="how"] [data-say]')).toContainText('I produce, he directs.', { timeout: 8_000 });
    await page.waitForTimeout(4000);
    await expect(page.locator('#step-0')).toHaveAttribute('aria-selected', 'true');
  });
});

test.describe('other pages', () => {
  for (const path of ['/work', '/pricing', '/frames', '/work/aurum-top-shelf', '/about', '/ai']) {
    test(`${path} renders`, async ({ page }) => {
      const r = await page.goto(path);
      expect(r?.status()).toBe(200);
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)).toBeLessThanOrEqual(0);
    });
  }
  test('/pricing shows no scarcity count', async ({ page }) => {
    await page.goto('/pricing');
    await expect(page.locator('main')).not.toContainText(/of \d+ left/);
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

  test('home offer form (email + product page) submits to the same pipeline', async ({ page }) => {
    let body = '';
    await page.route('**/api/lead/start', async (r) => {
      body = r.request().postData() ?? '';
      await r.fulfill({ json: { ok: true, id: '2026-10-08-abcdef12-3456', token: '1.x' } });
    });
    await page.route('**/api/lead/finish', (r) => r.fulfill({ json: { ok: true } }));
    await page.goto('/#start');
    const form = page.locator('form[data-act-form="offer"]');
    await form.getByLabel('Email').fill('founder@brand.com');
    await form.getByLabel('Product page URL').fill('brand.com/products/fig');
    await page.waitForTimeout(3100);
    await form.getByRole('button', { name: /Get my 5 free frames/ }).click();
    await expect(page).toHaveURL(/\/frames\/thanks/);
    expect(body).toContain('Product page: brand.com/products/fig');
  });
});
