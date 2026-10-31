#!/usr/bin/env node
// Talking lines: one clip per line, with its audio baked into the same file (lips and sound can't drift).
//
//   node scripts/lines-import.mjs <keyed_dir> [id …] [--floor 128]
//
// For every <keyed_dir>/<id>.mp4 (stacked alpha 720x2560, premultiplied colour on top, alpha below, + AAC):
//   public/media/lines/<id>.av1.mp4      540x1920 AV1  + Opus  (phones)
//   public/media/lines/<id>.hevc.mp4     540x1920 HEVC + AAC   (Apple)
//   public/media/lines/<id>_hd.av1.mp4   720x2560 AV1  + Opus  (desktop)
//   public/media/lines/<id>_hd.hevc.mp4  720x2560 HEVC + AAC
//   public/media/lines/<id>.words.json   word timings (seconds on the clip's own clock), copied as delivered
// and fills src/data/media.json → lines[id] (drops `pending`), so the site switches from the idle fallback to the line.
//
// --floor N (0–255, default 128): alpha below N becomes fully transparent and the rest is stretched back to 0–255.
// Green-screen keys leave a faint grey veil in the background; without the floor it shows as a dark box on the page.
import { execFileSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const fi = args.indexOf('--floor');
const floor = fi >= 0 ? Number(args.splice(fi, 2)[1]) : 128;
const [dir, ...only] = args;
if (!dir) throw new Error('usage: lines-import.mjs <keyed_dir> [id …] [--floor 128]');

const manifestPath = join(root, 'src/data/media.json');
const m = JSON.parse(readFileSync(manifestPath, 'utf8'));
m.lines ??= {};
const out = join(root, 'public', m.base, 'lines');
mkdirSync(out, { recursive: true });

const ff = (...a) => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...a], { stdio: 'inherit', env: { ...process.env, SVT_LOG: '1' } });
const probe = (file, entries) => execFileSync('ffprobe', ['-v', 'error', ...entries, '-of', 'csv=p=0', file]).toString().trim();

// Limited-range luma: 16 = transparent, 235 = opaque.
const lo = 16 + Math.max(0, Math.min(254, floor)) * (219 / 255);
const alphaLut = `lutyuv=y='clip((val-${lo.toFixed(1)})*219/(235-${lo.toFixed(1)})+16,16,235)':u=128:v=128`;
const graph = (w, h) =>
  `[0:v]split=2[c][a];[c]crop=iw:ih/2:0:0[top];[a]crop=iw:ih/2:0:ih/2,${alphaLut}[bot];[top][bot]vstack,scale=${w}:${h}:flags=lanczos,format=yuv420p[v]`;

function encode(src, base, w, h, hasAudio) {
  const common = ['-i', src, '-filter_complex', graph(w, h), '-map', '[v]', ...(hasAudio ? ['-map', '0:a:0'] : [])];
  ff(...common, '-c:v', 'libsvtav1', '-preset', '6', '-crf', '40', '-g', '48', '-svtav1-params', 'tune=0',
    ...(hasAudio ? ['-c:a', 'libopus', '-b:a', '64k', '-ac', '1', '-ar', '48000'] : ['-an']), '-movflags', '+faststart', `${base}.av1.mp4`);
  ff(...common, '-c:v', 'libx265', '-preset', 'medium', '-crf', '27', '-tag:v', 'hvc1', '-x265-params', 'log-level=error',
    ...(hasAudio ? ['-c:a', 'aac', '-b:a', '96k', '-ac', '1'] : ['-an']), '-movflags', '+faststart', `${base}.hevc.mp4`);
}

const ids = (only.length ? only : readdirSync(dir).filter((f) => /^[a-z]\d+\.mp4$/.test(f)).map((f) => basename(f, '.mp4'))).sort();
for (const id of ids) {
  const src = join(dir, `${id}.mp4`);
  if (!existsSync(src)) {
    console.warn(`skip ${id}: no ${src}`);
    continue;
  }
  const entry = m.lines[id];
  if (!entry) {
    console.warn(`skip ${id}: no lines.${id} entry in media.json (add who + text first)`);
    continue;
  }
  const [w, h] = probe(src, ['-select_streams', 'v:0', '-show_entries', 'stream=width,height']).split(',').map(Number);
  if (w * 32 !== h * 9) console.warn(`${id}: expected stacked 9:32 (720x2560), got ${w}x${h}`);
  const hasAudio = probe(src, ['-select_streams', 'a', '-show_entries', 'stream=index']) !== '';
  if (!hasAudio) console.warn(`${id}: no audio track; the line will play silent`);
  encode(src, join(out, id), 540, 1920, hasAudio);
  encode(src, join(out, `${id}_hd`), 720, 2560, hasAudio);
  const words = join(dir, `${id}.words.json`);
  if (existsSync(words)) copyFileSync(words, join(out, `${id}.words.json`));
  else console.warn(`${id}: no ${id}.words.json; captions show the whole line without word timing`);
  const dur = Number(probe(join(out, `${id}.hevc.mp4`), ['-show_entries', 'format=duration']));
  const { pending: _p, ...keep } = entry;
  m.lines[id] = {
    ...keep,
    av1: `lines/${id}.av1.mp4`,
    hevc: `lines/${id}.hevc.mp4`,
    av1_hd: `lines/${id}_hd.av1.mp4`,
    hevc_hd: `lines/${id}_hd.hevc.mp4`,
    words: existsSync(words) ? `lines/${id}.words.json` : null,
    audio: hasAudio,
    duration: Math.round(dur * 100) / 100,
  };
  console.log(`line ${id}: ${m.lines[id].who} · ${m.lines[id].duration} s · audio ${hasAudio ? 'yes' : 'no'}`);
}
writeFileSync(manifestPath, JSON.stringify(m, null, 2) + '\n');
