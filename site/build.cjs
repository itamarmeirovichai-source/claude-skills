/* Inline every asset into one file, so the site opens straight from disk. */
const fs = require('fs')
let html = fs.readFileSync('index.html', 'utf8')
const css = fs.readFileSync('css/site.css', 'utf8')
const js = ['core', 'hours', 'sequence', 'ui']
  .map(n => `/* ---- js/${n}.js ---- */\n` + fs.readFileSync(`js/${n}.js`, 'utf8')).join('\n')

html = html.replace('<link rel="stylesheet" href="css/site.css">', '<style>\n' + css + '\n</style>')
html = html.replace(/<script src="js\/(core|hours|sequence|ui)\.js"><\/script>\n?/g, '')
html = html.replace('<script>SH.boot();</script>', '<script>\n' + js + '\nSH.boot();\n</script>')
fs.writeFileSync('smash-house-boca-raton.html', html)
fs.mkdirSync('dist', { recursive: true })
fs.writeFileSync('dist/index.html', html)   // what Cloudflare Pages serves

/* The render frames are the one thing that cannot be inlined: they are the
   sequence. Copy them next to the page so the deploy is a plain static publish. */
if (fs.existsSync('frames')) {
  fs.rmSync('dist/frames', { recursive: true, force: true })
  fs.cpSync('frames', 'dist/frames', { recursive: true })
  const count = p => fs.existsSync(p) ? fs.readdirSync(p).length : 0
  console.log('frames: desktop', count('dist/frames/desktop'), 'mobile', count('dist/frames/mobile'))
} else {
  console.log('frames: none yet — the page will fall back to the poster')
}
console.log('bundled', (html.length / 1024).toFixed(0) + 'KB -> smash-house-boca-raton.html, dist/index.html')
