import { test, expect, type Page } from '@playwright/test';

// Characters live in reserved slots: no character pixel may cover text, a button, an image or a video.
// We check the box of every character canvas (<alpha-video>) against the rects of every text run (Range rects,
// so a wide paragraph block next to a character doesn't count, only its glyphs) and every button, link, field,
// image and video on the page, section by section, at the phone sizes the owner checked and on desktop.
// The hero ring moves, so the hero is sampled several times along the orbit.

type Box = { x: number; y: number; w: number; h: number; what: string };

async function collect(page: Page): Promise<{ chars: Box[]; things: Box[] }> {
  return page.evaluate(() => {
    const sy = window.scrollY;
    const sx = window.scrollX;
    const box = (r: DOMRect, what: string) => ({ x: r.left + sx, y: r.top + sy, w: r.width, h: r.height, what });
    const fixed = (el: Element): boolean => {
      for (let n: Element | null = el; n; n = n.parentElement) {
        const p = getComputedStyle(n).position;
        if (p === 'fixed' || p === 'sticky' || n.tagName === 'DIALOG' || n.tagName === 'HEADER') return true;
      }
      return false;
    };
    const shown = (el: Element): boolean => {
      const s = getComputedStyle(el);
      if (s.visibility === 'hidden' || s.display === 'none' || Number(s.opacity) === 0) return false;
      if (el.closest('details:not([open]) > :not(summary)')) return false; // collapsed answer: not rendered
      return !el.closest('[hidden]') && el.getClientRects().length > 0;
    };
    const chars = [...document.querySelectorAll('main alpha-video')].filter(shown).map((el) => box(el.getBoundingClientRect(), `character ${el.closest('[data-slot]')?.getAttribute('data-slot')}`));
    const things: ReturnType<typeof box>[] = [];
    const walker = document.createTreeWalker(document.querySelector('main') as Node, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const el = n.parentElement;
      if (!el || !n.textContent?.trim() || el.closest('alpha-video, .sr-only, .hp, script, style') || fixed(el) || !shown(el)) continue;
      const range = document.createRange();
      range.selectNodeContents(n);
      for (const r of range.getClientRects()) if (r.width > 0 && r.height > 0) things.push(box(r, `text "${n.textContent.trim().slice(0, 30)}"`));
    }
    for (const el of document.querySelectorAll('main button, main a, main input, main textarea, main select, main video, main img')) {
      if (el.closest('alpha-video, .hp') || fixed(el) || !shown(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) things.push(box(r, `${el.tagName.toLowerCase()}${el.className ? '.' + String(el.className).split(' ')[0] : ''}`));
    }
    return { chars, things };
  });
}

const hit = (a: Box, b: Box): boolean => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;

async function settleAt(page: Page, id: string): Promise<void> {
  await page.evaluate((id) => {
    const el = document.getElementById(id);
    if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 64, behavior: 'instant' });
  }, id);
  await page.waitForTimeout(500);
}

const SECTIONS = ['hero', 'how', 'pricing', 'start'];

for (const vp of [
  { width: 390, height: 844, mobile: true },
  { width: 360, height: 780, mobile: true },
  { width: 1440, height: 900, mobile: false },
  { width: 1024, height: 768, mobile: false },
]) {
  test.describe(`${vp.width}x${vp.height}`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height } });

    test('character canvases never touch text, buttons, images or video', async ({ page, isMobile }) => {
      test.skip(vp.mobile !== isMobile, 'run each size in its matching project');
      await page.goto('/');
      await expect(page.locator('#hero')).toHaveAttribute('data-state', 'idle', { timeout: 10_000 });
      const slots = await page.locator('main [data-slot]').evaluateAll((els) => els.map((e) => e.getAttribute('data-slot')));
      expect(slots).toEqual(['hero', 'how', 'pricing', 'offer']); // 4 appearances, no more
      const problems: string[] = [];
      for (const id of SECTIONS) {
        await settleAt(page, id);
        for (let k = 0; k < (id === 'hero' ? 6 : 1); k++) {
          const { chars, things } = await collect(page);
          expect(chars.length).toBe(4);
          for (const c of chars) for (const t of things) if (hit(c, t)) problems.push(`${id}: ${c.what} overlaps ${t.what}`);
          if (id === 'hero') await page.waitForTimeout(1400);
        }
      }
      expect([...new Set(problems)]).toEqual([]);
    });

    test('nothing touches the side edges (16 px gutters on phones)', async ({ page, isMobile }) => {
      test.skip(vp.mobile !== isMobile || !vp.mobile, 'phones');
      await page.goto('/');
      await page.waitForTimeout(800);
      const bad: string[] = [];
      for (const id of ['hero', 'problem', 'how', 'work', 'pricing', 'start', 'faq']) {
        await settleAt(page, id);
        const { things, chars } = await collect(page);
        for (const t of [...things, ...chars]) if (t.x < 15.5 || t.x + t.w > vp.width - 15.5) bad.push(`${id}: ${t.what} at ${Math.round(t.x)}–${Math.round(t.x + t.w)}`);
      }
      expect([...new Set(bad)]).toEqual([]);
    });
  });
}
