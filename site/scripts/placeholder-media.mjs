#!/usr/bin/env node
// Generates tiny placeholder media for every path in src/data/media.json that is
// missing from public/media/. Real media later replaces these files 1:1 (same names).
// Usage: node scripts/placeholder-media.mjs [--force]
// Requires ffmpeg with libsvtav1, libx265, libx264, libopus, libwebp, drawtext.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(readFileSync(join(root, 'src/data/media.json'), 'utf8'));
const out = join(root, 'public', manifest.base.replace(/^\//, ''));
const force = process.argv.includes('--force');
const FONT = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'].find(existsSync);

const need = (rel) => {
  const p = join(out, rel);
  if (!force && existsSync(p)) return null;
  mkdirSync(dirname(p), { recursive: true });
  return p;
};
const ff = (args) => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: 'inherit' });
const text = (t, y, size, color) =>
  FONT ? `drawtext=fontfile=${FONT}:text='${t.replace(/[':]/g, ' ')}':fontcolor=${color}:fontsize=${size}:x=(w-text_w)/2:y=${y}` : 'null';

// Alpha silhouette (luma): head + tapered body + an arm whose direction depends on the clip.
function alphaExpr(w, h, key, dur) {
  const cx = w / 2, hy = h * 0.27, rx = w * 0.15, ry = h * 0.1, by = h * 0.4;
  const dirs = { char_point_L: [-1, -0.2], char_point_R: [1, -0.2], char_point_C: [0, 0.35], char_reach: [0.15, 1], pop_wave: [0.8, -0.8], pop_thumb: [0.7, -0.3], vee_pop_1: [0.7, -0.5], vee_pop_2: [-0.7, -0.4] };
  const [dx, dy] = dirs[key] ?? [0, 0];
  const s = `sin(PI*min(T/${dur},1))`; // 0 → 1 → 0 over the clip: starts and ends on the hub pose
  const breathe = `(1+0.015*sin(2*PI*T/${Math.max(dur, 1)}))`;
  const head = `lt(pow((X-${cx})/(${rx}*${breathe}),2)+pow((Y-${hy})/${ry},2),1)`;
  const body = `gt(Y,${by})*lt(abs(X-${cx}),${w * 0.24}*(0.55+0.45*(Y-${by})/${h - by}))`;
  const len = Math.min(w, h) * 0.42;
  const ax = `(${cx}+${dx}*${len}*${s})`, ay = `(${by + h * 0.04}+${dy}*${len}*${s})`;
  // distance from point to segment shoulder→hand
  const sx = cx, sy = by + h * 0.04;
  const t = `clip(((X-${sx})*(${ax}-${sx})+(Y-${sy})*(${ay}-${sy}))/(pow(${ax}-${sx},2)+pow(${ay}-${sy},2)+0.001),0,1)`;
  const arm = dx === 0 && dy === 0 ? '0' : `lt(hypot(X-(${sx}+${t}*(${ax}-${sx})),Y-(${sy}+${t}*(${ay}-${sy}))),${w * 0.035})`;
  return `255*gte(${head}+${body}+${arm},1)`;
}

function stackedClip(group, key, clip, w, h) {
  const [bg, fg, label] = group === 'vee' ? ['0xEDE6DA', '0xD8432B', 'VEE'] : ['0x2A2622', '0xB08D57', 'OTTO'];
  const d = clip.duration;
  const color = `color=c=${bg}:s=${w}x${h}:r=24:d=${d},drawbox=x=0:y=${Math.round(h * 0.42)}:w=${w}:h=${h}:color=${group === 'vee' ? '0xF6F1E7' : '0x151312'}:t=fill,drawbox=x=${Math.round(w * 0.36)}:y=${Math.round(h * 0.31)}:w=${Math.round(w * 0.28)}:h=${Math.round(h * 0.03)}:color=${fg}:t=fill,${text(label, Math.round(h * 0.55), Math.round(w * 0.09), fg)},${text(key, Math.round(h * 0.63), Math.round(w * 0.045), fg)}`;
  const alpha = `nullsrc=s=${w}x${h}:r=24:d=${d},format=gray,geq=lum='${alphaExpr(w, h, key, d)}'`;
  const fc = '[1:v]format=yuv420p[a];[0:v]format=yuv420p[c];[c][a]vstack=inputs=2,format=yuv420p[v]';
  const av1 = need(clip.av1);
  if (av1) ff(['-f', 'lavfi', '-i', color, '-f', 'lavfi', '-i', alpha, '-filter_complex', fc, '-map', '[v]', '-an', '-c:v', 'libsvtav1', '-preset', '10', '-crf', '45', '-g', '24', '-movflags', '+faststart', av1]);
  const hevc = need(clip.hevc);
  for (const hd of [clip.av1_hd, clip.hevc_hd]) if (hd && need(hd)) console.warn('missing hd clip (no placeholder made):', hd);
  if (hevc) ff(['-f', 'lavfi', '-i', color, '-f', 'lavfi', '-i', alpha, '-filter_complex', fc, '-map', '[v]', '-an', '-c:v', 'libx265', '-preset', 'fast', '-crf', '30', '-tag:v', 'hvc1', '-x265-params', 'log-level=error', '-movflags', '+faststart', hevc]);
  return { color, alpha };
}

function poster(group, rel, w, h) {
  const p = need(rel);
  if (!p) return;
  const key = group === 'vee' ? 'vee_pop_1' : 'char_idle';
  const clip = { duration: 1 };
  const [bg, fg, label] = group === 'vee' ? ['0xEDE6DA', '0xD8432B', 'VEE'] : ['0x2A2622', '0xB08D57', 'OTTO'];
  const color = `color=c=${bg}:s=${w}x${h}:r=1:d=1,drawbox=x=0:y=${Math.round(h * 0.42)}:w=${w}:h=${h}:color=${group === 'vee' ? '0xF6F1E7' : '0x151312'}:t=fill,drawbox=x=${Math.round(w * 0.36)}:y=${Math.round(h * 0.31)}:w=${Math.round(w * 0.28)}:h=${Math.round(h * 0.03)}:color=${fg}:t=fill,${text(label, Math.round(h * 0.55), Math.round(w * 0.09), fg)}`;
  const alpha = `nullsrc=s=${w}x${h}:r=1:d=1,format=gray,geq=lum='${alphaExpr(w, h, key, clip.duration).replace(/T/g, '0')}'`;
  ff(['-f', 'lavfi', '-i', color, '-f', 'lavfi', '-i', alpha, '-filter_complex', '[0:v]format=rgba[c];[1:v]format=gray[a];[c][a]alphamerge[v]', '-map', '[v]', '-frames:v', '1', '-c:v', 'libwebp', '-quality', '80', p]);
}

const FILM_COLORS = { sol: '0x6B3B1E', aurum: '0x7A5A1F', vesper: '0x2E2440', orla: '0x3A3A3E', mere: '0x5E6B63', ember: '0x5A2A1C' };
function film(f) {
  const c = FILM_COLORS[f.slug] ?? '0x333333';
  const card = (w, h, d, extra = '') =>
    `color=c=${c}:s=${w}x${h}:r=24:d=${d},drawbox=x='${w / 2}-60+50*sin(t)':y=${Math.round(h * 0.45)}:w=120:h=${Math.round(h * 0.2)}:color=0xEDE3CF@0.8:t=fill,${text(f.brand, Math.round(h * 0.2), Math.round(w * 0.11), '0xF3EBDD')},${text('placeholder · ' + f.title, Math.round(h * 0.3), Math.round(w * 0.045), '0xF3EBDD')}${extra}`;
  const p = need(f.poster);
  if (p) ff(['-f', 'lavfi', '-i', card(540, 960, 1), '-frames:v', '1', '-c:v', 'libwebp', '-quality', '75', p]);
  const timer = (h, w) => `,drawtext=fontfile=${FONT}:text='%{eif\\:t\\:d}s':fontcolor=0xF3EBDD:fontsize=${Math.round(w * 0.06)}:x=(w-text_w)/2:y=${Math.round(h * 0.8)}`;
  const la = need(f.loop.av1);
  if (la) ff(['-f', 'lavfi', '-i', card(360, 640, 6), '-an', '-c:v', 'libsvtav1', '-preset', '10', '-crf', '45', '-g', '48', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', la]);
  const lh = need(f.loop.h264);
  if (lh) ff(['-f', 'lavfi', '-i', card(360, 640, 6), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '30', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', lh]);
  const tone = `sine=frequency=220:sample_rate=48000:duration=${f.duration},volume=0.05`;
  const fa = need(f.full.av1);
  if (fa) ff(['-f', 'lavfi', '-i', card(720, 1280, f.duration, timer(1280, 720)), '-f', 'lavfi', '-i', tone, '-c:v', 'libsvtav1', '-preset', '12', '-crf', '50', '-g', '96', '-pix_fmt', 'yuv420p', '-c:a', 'libopus', '-b:a', '48k', '-shortest', '-movflags', '+faststart', fa]);
  const fh = need(f.full.h264);
  if (fh) ff(['-f', 'lavfi', '-i', card(720, 1280, f.duration, timer(1280, 720)), '-f', 'lavfi', '-i', tone, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '32', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k', '-shortest', '-movflags', '+faststart', fh]);
}

function voice(key, v) {
  if (v.audio) {
    const p = need(v.audio);
    const d = Math.max(0.8, v.text.split(' ').length * 0.32).toFixed(2);
    if (p) ff(['-f', 'lavfi', '-i', `sine=frequency=330:sample_rate=44100:duration=${d},volume=0.08,afade=t=out:st=${(d - 0.2).toFixed(2)}:d=0.2`, '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', p]);
    const vt = v.vtt && need(v.vtt);
    if (vt) writeFileSync(vt, `WEBVTT\n\n00:00:00.000 --> 00:00:${String(Number(d).toFixed(3)).padStart(6, '0')}\n${v.text}\n`);
  }
}

function still(rel, label, c) {
  const p = need(rel);
  if (p) ff(['-f', 'lavfi', '-i', `color=c=${c}:s=1200x1500:d=1,drawbox=x=480:y=500:w=240:h=520:color=0xEDE3CF:t=fill,${text(label, 300, 64, '0x1A1816')}`, '-frames:v', '1', '-c:v', 'libwebp', '-quality', '70', p]);
}

let n = 0;
for (const group of ['otto', 'vee']) {
  const g = manifest[group];
  poster(group, g.poster, g.width, g.height);
  for (const [key, clip] of Object.entries(g.clips)) {
    if (clip.alias || !clip.av1) continue;
    const small = clip.small || group === 'vee';
    stackedClip(group, key, clip, small ? 360 : g.width, small ? 640 : g.height);
    n++;
  }
}
for (const f of manifest.films) film(f);
for (const [k, v] of Object.entries(manifest.voice)) voice(k, v);
still(manifest.stills.ba_before, 'product photo', '0xD9D6D0');
still(manifest.stills.ba_after, 'frame 3 of 5', '0x5A3A22');
console.log(`placeholder media ready in ${out} (${n} alpha clips, ${manifest.films.length} films)`);
