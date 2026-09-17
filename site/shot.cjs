const { chromium } = require('/opt/node22/lib/node_modules/playwright')
const path = require('path')
;(async () => {
  const file = process.argv[2]
  const outDir = process.argv[3]
  const shots = JSON.parse(process.argv[4] || '[0]')
  const w = +(process.argv[5] || 1440), h = +(process.argv[6] || 900)
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--disable-lcd-text', '--force-device-scale-factor=1'],
  })
  const page = await browser.newPage({ viewport: { width: w, height: h } })
  const errors = []
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message))
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()) })
  await page.goto('file://' + path.resolve(file))
  await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' })
  await page.waitForTimeout(2500)
  const maxScroll = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight)
  for (const s of shots) {
    await page.evaluate((y) => window.scrollTo(0, y), Math.round(maxScroll * s))
    await page.waitForTimeout(4000)
    const name = String(Math.round(s * 1000)).padStart(4, '0')
    await page.screenshot({ path: `${outDir}/p${name}.png`, timeout: 120000 })
  }
  console.log('maxScroll', maxScroll)
  console.log(errors.length ? errors.slice(0, 12).join('\n') : 'no console errors')
  await browser.close()
})()
