#!/usr/bin/env node
// Screenshots for review: node scripts/shots.mjs <outDir> [baseURL]  (needs `npm run preview` running)
import { chromium, devices } from '@playwright/test';
import { existsSync, mkdirSync } from 'node:fs';
const out = process.argv[2] ?? 'shots';
const base = process.argv[3] ?? 'http://localhost:4321';
mkdirSync(out, { recursive: true });
const exe = [process.env.PW_CHROMIUM, '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium'].find((p) => p && existsSync(p));
const browser = await chromium.launch({ ...(exe ? { executablePath: exe } : {}), args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'] });
const settle = (p) => p.waitForFunction(() => ['idle', 'fallback'].includes(document.getElementById('hero')?.dataset.state ?? ''), null, { timeout: 15000 }).then(() => p.waitForTimeout(2500));

const m = await browser.newPage({ ...devices['Pixel 7'] });
await m.goto(base + '/');
await settle(m);
await m.screenshot({ path: `${out}/mobile_home_hero.png` });
console.log('codec', await m.evaluate(() => document.getElementById('hero')?.dataset.codec));

const d = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await d.goto(base + '/');
await settle(d);
await d.screenshot({ path: `${out}/desktop_hero.png` });
if (process.env.EXTRA) {
  const c = d.locator('[data-card="1"]');
  await c.focus();
  await c.press('Enter');
  await d.waitForFunction(() => document.getElementById('hero')?.dataset.state === 'playing', null, { timeout: 15000 });
  await d.waitForTimeout(2500);
  await d.screenshot({ path: `${out}/desktop_playing.png` });
}
await d.goto(base + '/pricing');
await d.waitForTimeout(800);
await d.evaluate(() => document.querySelectorAll('[data-reveal]').forEach((e) => e.classList.add('is-in')));
await d.waitForTimeout(900);
await d.screenshot({ path: `${out}/desktop_pricing.png`, fullPage: false });
await browser.close();
