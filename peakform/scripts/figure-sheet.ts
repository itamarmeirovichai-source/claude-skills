// Renders every exercise keyframe and drill diagram into one HTML contact sheet,
// then screenshots it so poses can be reviewed for anatomical sense.
// Usage: npx tsx scripts/figure-sheet.ts <out-dir> [module paths...]
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from '@playwright/test';
import { posePrims, diagramPrims, primsToSvg, POSE_W, POSE_H, DIAGRAM_W, DIAGRAM_H, FIGURE_CSS } from '../src/svg/pose';
import type { ExerciseContent } from '../src/content/types';

const outDir = resolve(process.argv[2] ?? 'figure-sheet');
const mods = process.argv.slice(3);
mkdirSync(outDir, { recursive: true });

const all: ExerciseContent[] = [];
for (const m of mods) {
  const mod = await import(pathToFileURL(resolve(m)).href);
  for (const v of Object.values(mod)) {
    if (Array.isArray(v)) all.push(...(v as ExerciseContent[]).filter((e) => e && typeof e === 'object' && 'visual' in e));
    else if (v && typeof v === 'object' && 'visual' in (v as object)) all.push(v as ExerciseContent);
  }
}

const cards = all
  .map((ex) => {
    const frames = (ex.visual.poses ?? [])
      .map((p) => `<figure>${primsToSvg(posePrims(p), POSE_W, POSE_H)}<figcaption><b>${p.label}</b> ${p.caption}</figcaption></figure>`)
      .join('');
    const diag = ex.visual.diagram
      ? `<figure>${primsToSvg(diagramPrims(ex.visual.diagram), DIAGRAM_W, DIAGRAM_H)}<figcaption>${ex.visual.diagram.caption}</figcaption></figure>`
      : '';
    return `<section><h2>${ex.name} <small>${ex.id}</small></h2><div class="row">${frames}${diag}</div></section>`;
  })
  .join('');

const html = `<!doctype html><meta charset="utf-8"><style>${FIGURE_CSS}
body{font-family:system-ui;margin:12px;background:#fff}
section{border-bottom:1px solid #ddd;padding:6px 0;break-inside:avoid}
h2{font-size:14px;margin:4px 0}small{color:#888;font-weight:400}
.row{display:flex;gap:8px;flex-wrap:wrap}
figure{margin:0;width:200px;border:1px solid #eee}
figcaption{font-size:10px;padding:2px 4px;color:#333}
svg{display:block}
</style>${cards}`;
writeFileSync(resolve(outDir, 'sheet.html'), html);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1100, height: 800 } });
await page.goto(pathToFileURL(resolve(outDir, 'sheet.html')).href);
const sections = await page.locator('section').count();
const perShot = 6;
for (let i = 0; i < sections; i += perShot) {
  const box = await page.evaluate(([a, b]) => {
    const s = Array.from(document.querySelectorAll('section'));
    const first = s[a]!.getBoundingClientRect();
    const last = s[Math.min(b, s.length) - 1]!.getBoundingClientRect();
    return { y: first.top + window.scrollY, h: last.bottom - first.top };
  }, [i, i + perShot]);
  await page.screenshot({ path: resolve(outDir, `sheet-${String(i / perShot).padStart(2, '0')}.png`), clip: { x: 0, y: box.y, width: 1100, height: box.h }, fullPage: true });
}
await browser.close();
console.log(`Rendered ${all.length} exercises into ${outDir}`);
