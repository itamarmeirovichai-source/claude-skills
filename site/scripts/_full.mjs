import { chromium } from '@playwright/test';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const S = process.argv[2];
for (const [name, vp] of [['d', { width: 1440, height: 900 }], ['m', { width: 390, height: 844 }]]) {
  const p = await b.newPage({ viewport: vp });
  await p.goto('http://localhost:4321/');
  await p.waitForTimeout(1500);
  const h = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += 500) { await p.evaluate((y) => window.scrollTo(0, y), y); await p.waitForTimeout(120); }
  await p.evaluate(() => document.querySelectorAll('[data-reveal]').forEach((e) => e.classList.add('is-in')));
  await p.evaluate(() => window.scrollTo(0, document.getElementById('how').offsetTop - 100));
  await p.waitForTimeout(2500);
  await p.screenshot({ path: `${S}/_${name}_how.png` });
  await p.screenshot({ path: `${S}/_${name}_full.png`, fullPage: true });
}
await b.close();
