/* Drive the sequence directly with #qa, over http so fetch() can read the
   label track — file:// blocks it, and then the labels silently never appear. */
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
  await new Promise(r => server.listen(8799, r))
  const w = +(process.argv[3] || 1100), h = +(process.argv[4] || 690)
  const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] })
  const p = await b.newPage({ viewport: { width: w, height: h } })
  const errs = []
  p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message))
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()) })
  await p.goto('http://127.0.0.1:8799/index.html#qa')
  await p.addStyleTag({ content: 'html{scroll-behavior:auto !important}' })
  await p.waitForTimeout(2500)
  await p.evaluate(() => { const s = document.querySelector('[data-seq]'); window.scrollTo(0, s.offsetTop + 200) })
  await p.waitForTimeout(3000)
  fs.mkdirSync('shots', { recursive: true })
  for (const v of JSON.parse(process.argv[2])) {
    await p.evaluate(x => window.__setP(x), v)
    await p.waitForTimeout(1800)
    await p.screenshot({ path: `shots/qa${String(Math.round(v*1000)).padStart(4,'0')}.png`, timeout: 120000 })
  }
  console.log(JSON.stringify(await p.evaluate(() => window.__seq)))
  console.log(errs.length ? errs.slice(0, 10).join('\n') : 'no console errors')
  await b.close(); server.close()
})()
