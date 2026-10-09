const { chromium } = require('/opt/node22/lib/node_modules/playwright')
const path = require('path')
;(async () => {
  const b = await chromium.launch({ args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] })
  for (const cfg of [{n:'m', w:390, h:844, rm:false}, {n:'rm', w:1100, h:690, rm:true}]) {
    const ctx = await b.newContext({ viewport:{width:cfg.w,height:cfg.h}, isMobile: cfg.n==='m',
      hasTouch: cfg.n==='m', reducedMotion: cfg.rm ? 'reduce' : 'no-preference' })
    const p = await ctx.newPage()
    const errs = []
    p.on('pageerror', e => errs.push('PAGEERROR ' + e.message))
    await p.goto('file://' + path.resolve('index.html'))
    await p.addStyleTag({ content:'html{scroll-behavior:auto !important}' })
    await p.waitForTimeout(3000)
    for (const s of [0, 0.22, 0.40, 0.75, 1]) {
      await p.evaluate((f)=>{const m=document.documentElement.scrollHeight-innerHeight;window.scrollTo(0,Math.round(m*f))}, s)
      await p.waitForTimeout(3500)
      await p.screenshot({ path:`shots/${cfg.n}${String(Math.round(s*100)).padStart(3,'0')}.png`, timeout:120000 })
    }
    console.log(cfg.n, errs.length ? errs.slice(0,5).join(' | ') : 'no page errors')
    await ctx.close()
  }
  await b.close()
})()
