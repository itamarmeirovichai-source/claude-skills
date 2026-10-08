import { chromium } from '@playwright/test';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('http://localhost:4321/');
await p.waitForTimeout(1500);
const target = await p.evaluate(() => document.getElementById('how').getBoundingClientRect().top + scrollY - 150);
for (let y = 0; y < target; y += 400) { await p.mouse.wheel(0, 400); await p.waitForTimeout(150); }
await p.waitForTimeout(2200);
console.log(await p.evaluate(() => [...document.querySelectorAll('[data-pop]')].map(e => e.dataset.pop + ':' + e.className).join(' | ')));
await p.screenshot({ path: process.argv[2] });
await b.close();
