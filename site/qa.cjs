const { chromium } = require('/opt/node22/lib/node_modules/playwright')
const path = require('path')
;(async () => {
  const b = await chromium.launch({ args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] })
  const p = await b.newPage({ viewport:{width:1100,height:690} })
  await p.goto('file://' + path.resolve('index.html') + '#qa')
  await p.addStyleTag({ content: 'html{scroll-behavior:auto !important}' })
  await p.waitForTimeout(2500)
  await p.evaluate(() => { const s=document.querySelector('[data-seq]'); window.scrollTo(0, s.offsetTop + 200) })
  await p.waitForTimeout(2500)
  for (const v of JSON.parse(process.argv[2])) {
    await p.evaluate((x) => window.__setP(x), v)
    await p.waitForTimeout(2500)
    await p.screenshot({ path: `shots/qa${String(Math.round(v*1000)).padStart(4,'0')}.png`, timeout: 120000 })
  }
  console.log('qa shots done')
  await b.close()
})()
