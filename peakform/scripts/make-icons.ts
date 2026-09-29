// Renders the original SVG app icon to the PNG sizes iOS and the manifest need.
import { chromium } from '@playwright/test';
import { readFileSync } from 'node:fs';

const jobs: Array<[string, string, number]> = [
  ['public/icons/icon.svg', 'public/icons/icon-192.png', 192],
  ['public/icons/icon.svg', 'public/icons/icon-512.png', 512],
  ['public/icons/icon-maskable.svg', 'public/icons/icon-maskable-512.png', 512],
  // iOS applies its own rounded mask, so the touch icon uses the full bleed artwork.
  ['public/icons/icon-maskable.svg', 'public/icons/apple-touch-icon.png', 180],
];
const browser = await chromium.launch();
for (const [src, out, size] of jobs) {
  const page = await browser.newPage({ viewport: { width: size, height: size } });
  const svg = readFileSync(src, 'utf8').replace('<svg ', `<svg width="${size}" height="${size}" `);
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } });
  await page.close();
}
await browser.close();
console.log('Icons written.');
