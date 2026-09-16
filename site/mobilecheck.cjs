const { chromium } = require('/opt/node22/lib/node_modules/playwright')
const path = require('path')
;(async () => {
  const b = await chromium.launch({ args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] })
  const ctx = await b.newContext({ viewport:{width:390,height:844}, isMobile:true, hasTouch:true,
                                   deviceScaleFactor:2 })
  const p = await ctx.newPage()
  const errs = []
  p.on('pageerror', e => errs.push('PE: ' + e.message))
  await p.goto('file://' + path.resolve('smash-house-boca-raton.html'))
  await p.addStyleTag({ content:'html{scroll-behavior:auto !important}' })
  await p.waitForTimeout(3000)
  const report = await p.evaluate(() => {
    const out = { scrollWidth: document.documentElement.scrollWidth, vw: innerWidth, issues: [] }
    // anything wider than the viewport
    document.querySelectorAll('body *').forEach(el => {
      const r = el.getBoundingClientRect()
      if (r.width > innerWidth + 1 && getComputedStyle(el).position !== 'fixed')
        out.issues.push('WIDE ' + el.tagName + '.' + String(el.className).slice(0,24) + ' w=' + Math.round(r.width))
    })
    // tap targets under 24px
    document.querySelectorAll('a, button').forEach(el => {
      const r = el.getBoundingClientRect()
      if (r.width && (r.width < 24 || r.height < 24))
        out.issues.push('SMALL ' + el.tagName + '.' + String(el.className).slice(0,20) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height))
    })
    out.seqHeight = document.querySelector('[data-seq]').offsetHeight
    out.docHeight = document.documentElement.scrollHeight
    return out
  })
  console.log(JSON.stringify(report, null, 1))
  for (const s of [0, 0.12, 0.30, 0.46, 0.62, 0.78, 0.9, 1]) {
    await p.evaluate((f)=>{const m=document.documentElement.scrollHeight-innerHeight;window.scrollTo(0,Math.round(m*f))}, s)
    await p.waitForTimeout(3500)
    await p.screenshot({ path:`shots/mob${String(Math.round(s*100)).padStart(3,'0')}.png`, timeout:120000 })
  }
  console.log('errors:', errs.join(' | ') || 'none')
  await b.close()
})()
