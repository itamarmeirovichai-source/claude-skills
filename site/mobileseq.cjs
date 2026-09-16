/* The mobile variant of the sequence, driven directly, over http so the label
   track can load. 390x844 is the iPhone 14/15 viewport. */
const { chromium } = require('/opt/node22/lib/node_modules/playwright')
const http = require('http'), fs = require('fs'), path = require('path')
const TYPES = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript',
                '.json':'application/json', '.webp':'image/webp', '.png':'image/png' }
const server = http.createServer((req, res) => {
  const p = path.join(__dirname, decodeURIComponent(req.url.split('?')[0]))
  fs.readFile(p, (e, buf) => {
    if (e) { res.writeHead(404); res.end('no'); return }
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' })
    res.end(buf)
  })
})
;(async () => {
  await new Promise(r => server.listen(8801, r))
  const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] })
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true,
                                   hasTouch: true, deviceScaleFactor: 2 })
  const p = await ctx.newPage()
  const errs = []
  p.on('pageerror', e => errs.push('PE: ' + e.message))
  await p.goto('http://127.0.0.1:8801/index.html#qa')
  await p.addStyleTag({ content: 'html{scroll-behavior:auto !important}' })
  await p.waitForTimeout(2500)
  await p.evaluate(() => { const s = document.querySelector('[data-seq]'); window.scrollTo(0, s.offsetTop + 200) })
  await p.waitForTimeout(3000)
  fs.mkdirSync('shots', { recursive: true })
  for (const v of JSON.parse(process.argv[2])) {
    await p.evaluate(x => window.__setP(x), v)
    await p.waitForTimeout(1800)
    await p.screenshot({ path: `shots/mseq${String(Math.round(v*1000)).padStart(4,'0')}.png`, timeout: 120000 })
  }
  console.log(JSON.stringify(await p.evaluate(() => window.__seq)))
  console.log(errs.length ? errs.join('\n') : 'no page errors')
  await b.close(); server.close()
})()
