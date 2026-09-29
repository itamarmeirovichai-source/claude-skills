import type { Anchor, DrillDiagram, Pose, PoseProp } from '../content/types';

// Pure geometry for the original keyframe figures and drill diagrams.
// Produces a flat list of primitives so the same drawing can render in React
// and in a Node script that builds a review contact sheet.

export const POSE_W = 200;
export const POSE_H = 180;
export const GROUND_Y = 172;

const L = {
  trunk: 52,
  neck: 6,
  headR: 9,
  upperArm: 29,
  forearm: 26,
  thigh: 42,
  shin: 40,
  foot: 13,
} as const;

export type Prim =
  | { t: 'line'; x1: number; y1: number; x2: number; y2: number; cls: string; w?: number }
  | { t: 'circle'; cx: number; cy: number; r: number; cls: string }
  | { t: 'rect'; x: number; y: number; w: number; h: number; cls: string; rx?: number; rot?: { a: number; cx: number; cy: number } }
  | { t: 'path'; d: string; cls: string }
  | { t: 'text'; x: number; y: number; text: string; cls: string; anchor?: 'start' | 'middle' | 'end' };

type P = { x: number; y: number };

const rad = (deg: number) => (deg * Math.PI) / 180;
const dir = (deg: number): P => ({ x: Math.sin(rad(deg)), y: Math.cos(rad(deg)) });
const add = (a: P, d: P, len: number): P => ({ x: a.x + d.x * len, y: a.y + d.y * len });
const r1 = (n: number) => Math.round(n * 10) / 10;

export interface Skeleton {
  hip: P;
  neck: P;
  shoulder: P;
  head: P;
  near: { elbow: P; wrist: P; knee: P; ankle: P; toe: P; heel: P };
  far: { elbow: P; wrist: P; knee: P; ankle: P; toe: P; heel: P };
}

function limb(shoulder: P, hip: P, arm: [number, number], leg: readonly number[]) {
  const elbow = add(shoulder, dir(arm[0]), L.upperArm);
  const wrist = add(elbow, dir(arm[1]), L.forearm);
  const knee = add(hip, dir(leg[0] ?? 0), L.thigh);
  const ankle = add(knee, dir(leg[1] ?? 0), L.shin);
  const footA = leg[2] ?? 90;
  const toe = add(ankle, dir(footA), L.foot);
  const heel = add(ankle, dir(footA + 180), 3);
  return { elbow, wrist, knee, ankle, toe, heel };
}

export function solveSkeleton(pose: Pose): Skeleton {
  const hip0: P = { x: 0, y: 0 };
  const neck0 = add(hip0, dir(pose.trunk), L.trunk);
  const shoulder0 = add(hip0, dir(pose.trunk), L.trunk - 5);
  const head0 = add(neck0, dir(pose.head ?? pose.trunk), L.neck + L.headR);
  const near0 = limb(shoulder0, hip0, pose.armNear, pose.legNear);
  const far0 = limb(shoulder0, hip0, pose.armFar ?? pose.armNear, pose.legFar ?? pose.legNear);

  let dx: number;
  let dy: number;
  if (pose.hip) {
    dx = pose.hip[0];
    dy = pose.hip[1];
  } else {
    const ys = [near0, far0].flatMap((s) => [s.knee.y, s.ankle.y, s.toe.y, s.heel.y]);
    const maxY = Math.max(...ys);
    dy = GROUND_Y - (pose.lift ?? 0) - maxY;
    dx = (pose.footX ?? 95) - near0.ankle.x;
  }
  const mv = (p: P): P => ({ x: r1(p.x + dx), y: r1(p.y + dy) });
  const mvLimb = (s: typeof near0) => ({
    elbow: mv(s.elbow),
    wrist: mv(s.wrist),
    knee: mv(s.knee),
    ankle: mv(s.ankle),
    toe: mv(s.toe),
    heel: mv(s.heel),
  });
  return {
    hip: mv(hip0),
    neck: mv(neck0),
    shoulder: mv(shoulder0),
    head: mv(head0),
    near: mvLimb(near0),
    far: mvLimb(far0),
  };
}

function anchorPoint(sk: Skeleton, a: Anchor): P {
  if (Array.isArray(a)) return { x: a[0], y: a[1] };
  switch (a) {
    case 'hands':
    case 'nearHand':
      return sk.near.wrist;
    case 'farHand':
      return sk.far.wrist;
    case 'shoulders':
      return { x: sk.shoulder.x, y: sk.shoulder.y };
    case 'hips':
      return sk.hip;
    case 'nearAnkle':
      return sk.near.ankle;
    case 'nearKnee':
      return sk.near.knee;
  }
}

function seg(a: P, b: P, cls: string, w: number): Prim {
  return { t: 'line', x1: a.x, y1: a.y, x2: b.x, y2: b.y, cls, w };
}

function arrowHead(from: P, to: P): string {
  const ang = Math.atan2(to.y - from.y, to.x - from.x);
  const s = 6;
  const a1 = { x: to.x - s * Math.cos(ang - 0.5), y: to.y - s * Math.sin(ang - 0.5) };
  const a2 = { x: to.x - s * Math.cos(ang + 0.5), y: to.y - s * Math.sin(ang + 0.5) };
  return `M${r1(from.x)},${r1(from.y)} L${r1(to.x)},${r1(to.y)} M${r1(a1.x)},${r1(a1.y)} L${r1(to.x)},${r1(to.y)} L${r1(a2.x)},${r1(a2.y)}`;
}

function propPrims(sk: Skeleton, p: PoseProp): { back: Prim[]; front: Prim[] } {
  const back: Prim[] = [];
  const front: Prim[] = [];
  switch (p.type) {
    case 'barbell': {
      const c = anchorPoint(sk, p.at);
      front.push({ t: 'circle', cx: c.x, cy: c.y, r: 12, cls: 'pf-plate' });
      front.push({ t: 'circle', cx: c.x, cy: c.y, r: 3, cls: 'pf-hub' });
      break;
    }
    case 'dumbbell': {
      const c = anchorPoint(sk, p.at);
      front.push({ t: 'rect', x: c.x - 9, y: c.y - 4, w: 18, h: 8, rx: 3, cls: 'pf-prop-solid' });
      break;
    }
    case 'handle': {
      const c = anchorPoint(sk, p.at);
      front.push({ t: 'rect', x: c.x - 5, y: c.y - 3, w: 10, h: 6, rx: 2, cls: 'pf-prop-solid' });
      break;
    }
    case 'cable': {
      const a = anchorPoint(sk, p.from);
      back.push({ t: 'line', x1: a.x, y1: a.y, x2: p.to[0], y2: p.to[1], cls: 'pf-cable', w: 1.5 });
      back.push({ t: 'circle', cx: p.to[0], cy: p.to[1], r: 4, cls: 'pf-prop-solid' });
      break;
    }
    case 'bench': {
      const h = p.h ?? 8;
      const rect: Prim = { t: 'rect', x: p.x, y: p.y, w: p.w, h, rx: 2, cls: 'pf-prop' };
      if (p.angle) rect.rot = { a: p.angle, cx: p.x, cy: p.y + h / 2 };
      back.push(rect);
      if (!p.angle) {
        back.push({ t: 'line', x1: p.x + 8, y1: p.y + h, x2: p.x + 8, y2: GROUND_Y, cls: 'pf-prop-line', w: 3 });
        back.push({ t: 'line', x1: p.x + p.w - 8, y1: p.y + h, x2: p.x + p.w - 8, y2: GROUND_Y, cls: 'pf-prop-line', w: 3 });
      }
      break;
    }
    case 'box':
      back.push({ t: 'rect', x: p.x, y: p.y, w: p.w, h: p.h, rx: 2, cls: 'pf-prop' });
      break;
    case 'pad':
      back.push({ t: 'rect', x: p.x, y: p.y, w: p.w, h: p.h, rx: 4, cls: 'pf-prop-solid' });
      break;
    case 'ball': {
      const c = anchorPoint(sk, p.at);
      front.push({ t: 'circle', cx: c.x, cy: c.y - (Array.isArray(p.at) ? 0 : 2), r: p.r ?? 9, cls: 'pf-ball' });
      break;
    }
    case 'line':
      back.push({ t: 'line', x1: p.x1, y1: p.y1, x2: p.x2, y2: p.y2, cls: 'pf-prop-line', w: 3 });
      break;
    case 'rope': {
      const top = sk.head.y - 22;
      const w = sk.near.wrist;
      back.push({
        t: 'path',
        d: `M${w.x},${w.y} C${w.x + 40},${top} ${w.x - 70},${top} ${w.x - 20},${w.y}`,
        cls: 'pf-cable',
      });
      back.push({
        t: 'path',
        d: `M${w.x},${w.y} Q${w.x + 10},${GROUND_Y + 14} ${w.x - 20},${w.y}`,
        cls: 'pf-cable-faint',
      });
      break;
    }
    case 'water':
      back.push({ t: 'rect', x: 0, y: p.y, w: POSE_W, h: POSE_H - p.y, cls: 'pf-water' });
      break;
    case 'net':
      back.push({ t: 'rect', x: p.x - 2, y: 18, w: 4, h: 70, cls: 'pf-net' });
      back.push({ t: 'line', x1: p.x, y1: 88, x2: p.x, y2: GROUND_Y, cls: 'pf-prop-line', w: 2 });
      break;
    case 'arrow':
      front.push({ t: 'path', d: arrowHead({ x: p.from[0], y: p.from[1] }, { x: p.to[0], y: p.to[1] }), cls: 'pf-arrow' });
      break;
  }
  return { back, front };
}

export function posePrims(pose: Pose): Prim[] {
  const sk = solveSkeleton(pose);
  const props = (pose.props ?? []).map((p) => propPrims(sk, p));
  const hasWater = (pose.props ?? []).some((p) => p.type === 'water');
  const out: Prim[] = [];
  if (!hasWater && !pose.hip) {
    out.push({ t: 'line', x1: 8, y1: GROUND_Y + 1, x2: POSE_W - 8, y2: GROUND_Y + 1, cls: 'pf-ground', w: 2 });
  } else if (!hasWater) {
    out.push({ t: 'line', x1: 8, y1: GROUND_Y + 1, x2: POSE_W - 8, y2: GROUND_Y + 1, cls: 'pf-ground', w: 2 });
  }
  for (const p of props) out.push(...p.back);
  // far side limbs
  out.push(seg(sk.shoulder, sk.far.elbow, 'pf-far', 8), seg(sk.far.elbow, sk.far.wrist, 'pf-far', 7));
  out.push(seg(sk.hip, sk.far.knee, 'pf-far', 11), seg(sk.far.knee, sk.far.ankle, 'pf-far', 9));
  out.push(seg(sk.far.heel, sk.far.toe, 'pf-far', 6));
  // trunk and head
  out.push(seg(sk.hip, sk.neck, 'pf-body', 17));
  out.push(seg(sk.neck, sk.head, 'pf-body', 6));
  out.push({ t: 'circle', cx: sk.head.x, cy: sk.head.y, r: L.headR, cls: 'pf-head' });
  // near side limbs
  out.push(seg(sk.hip, sk.near.knee, 'pf-body', 12), seg(sk.near.knee, sk.near.ankle, 'pf-body', 10));
  out.push(seg(sk.near.heel, sk.near.toe, 'pf-body', 7));
  out.push(seg(sk.shoulder, sk.near.elbow, 'pf-body', 9), seg(sk.near.elbow, sk.near.wrist, 'pf-body', 8));
  for (const p of props) out.push(...p.front);
  return out;
}

// ---------- Drill diagrams ----------

export const DIAGRAM_W = 200;
export const DIAGRAM_H = 180;

export function diagramPrims(d: DrillDiagram): Prim[] {
  const out: Prim[] = [];
  let sx: (x: number) => number;
  let sy: (y: number) => number;
  if (d.kind === 'court') {
    // Half court 9 x 9 m, net at top.
    const s = 17;
    const ox = (DIAGRAM_W - 9 * s) / 2;
    const oy = 14;
    sx = (x) => r1(ox + x * s);
    sy = (y) => r1(oy + y * s);
    out.push({ t: 'rect', x: sx(0), y: sy(0), w: 9 * s, h: 9 * s, cls: 'pd-court' });
    out.push({ t: 'line', x1: sx(-0.6), y1: sy(0), x2: sx(9.6), y2: sy(0), cls: 'pd-net', w: 4 });
    out.push({ t: 'line', x1: sx(0), y1: sy(3), x2: sx(9), y2: sy(3), cls: 'pd-line', w: 1.5 });
    out.push({ t: 'text', x: sx(4.5), y: sy(0) - 4, text: 'Net', cls: 'pd-label', anchor: 'middle' });
    out.push({ t: 'text', x: sx(9) - 2, y: sy(3) - 3, text: '3 m', cls: 'pd-label', anchor: 'end' });
  } else if (d.kind === 'lane') {
    const s = 14;
    const ox = 16;
    const oy = 90;
    sx = (x) => r1(ox + x * s);
    sy = (y) => r1(oy + y * s);
    out.push({ t: 'rect', x: sx(0), y: sy(-2), w: 12 * s, h: 4 * s, cls: 'pd-court' });
    out.push({ t: 'line', x1: sx(0), y1: sy(-2), x2: sx(0), y2: sy(2), cls: 'pd-net', w: 3 });
    out.push({ t: 'line', x1: sx(10), y1: sy(-2), x2: sx(10), y2: sy(2), cls: 'pd-net', w: 3 });
    out.push({ t: 'text', x: sx(0), y: sy(-2) - 5, text: 'Start', cls: 'pd-label', anchor: 'middle' });
    out.push({ t: 'text', x: sx(10), y: sy(-2) - 5, text: '10 m', cls: 'pd-label', anchor: 'middle' });
  } else {
    const s = 7;
    const ox = 12;
    const oy = 60;
    sx = (x) => r1(ox + x * s);
    sy = (y) => r1(oy + y * s);
    out.push({ t: 'rect', x: sx(0), y: sy(0), w: 25 * s, h: 8 * s, cls: 'pd-water' });
    for (let lane = 1; lane < 4; lane++) {
      out.push({ t: 'line', x1: sx(0), y1: sy(lane * 2), x2: sx(25), y2: sy(lane * 2), cls: 'pd-line', w: 1 });
    }
    out.push({ t: 'text', x: sx(0), y: sy(0) - 5, text: 'Wall', cls: 'pd-label', anchor: 'start' });
    out.push({ t: 'text', x: sx(25), y: sy(0) - 5, text: 'Wall', cls: 'pd-label', anchor: 'end' });
  }
  for (const m of d.markers ?? []) {
    out.push({ t: 'rect', x: sx(m.x) - 4, y: sy(m.y) - 4, w: 8, h: 8, rx: 1, cls: 'pd-marker' });
    out.push({ t: 'text', x: sx(m.x), y: sy(m.y) + 15, text: m.label, cls: 'pd-label', anchor: 'middle' });
  }
  if (d.ball) out.push({ t: 'circle', cx: sx(d.ball.x), cy: sy(d.ball.y), r: 6, cls: 'pf-ball' });
  const pts = d.steps;
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1]!;
    const b = pts[i]!;
    const ax = sx(a.x);
    const ay = sy(a.y);
    const bx = sx(b.x);
    const by = sy(b.y);
    const len = Math.hypot(bx - ax, by - ay) || 1;
    const shrink = 9;
    const to = { x: bx - ((bx - ax) / len) * shrink, y: by - ((by - ay) / len) * shrink };
    const from = { x: ax + ((bx - ax) / len) * shrink, y: ay + ((by - ay) / len) * shrink };
    out.push({ t: 'path', d: arrowHead(from, to), cls: 'pf-arrow' });
  }
  pts.forEach((p, i) => {
    out.push({ t: 'circle', cx: sx(p.x), cy: sy(p.y), r: 7.5, cls: 'pd-step' });
    out.push({ t: 'text', x: sx(p.x), y: sy(p.y) + 3.5, text: p.label ?? String(i + 1), cls: 'pd-step-text', anchor: 'middle' });
  });
  return out;
}

export function primsToSvg(prims: Prim[], w: number, h: number): string {
  const body = prims
    .map((p) => {
      switch (p.t) {
        case 'line':
          return `<line x1="${p.x1}" y1="${p.y1}" x2="${p.x2}" y2="${p.y2}" class="${p.cls}" stroke-width="${p.w ?? 2}" stroke-linecap="round"/>`;
        case 'circle':
          return `<circle cx="${p.cx}" cy="${p.cy}" r="${p.r}" class="${p.cls}"/>`;
        case 'rect':
          return `<rect x="${p.x}" y="${p.y}" width="${p.w}" height="${p.h}" rx="${p.rx ?? 0}" class="${p.cls}"${p.rot ? ` transform="rotate(${p.rot.a} ${p.rot.cx} ${p.rot.cy})"` : ''}/>`;
        case 'path':
          return `<path d="${p.d}" class="${p.cls}" fill="none"/>`;
        case 'text':
          return `<text x="${p.x}" y="${p.y}" class="${p.cls}" text-anchor="${p.anchor ?? 'start'}">${p.text.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`;
      }
    })
    .join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${body}</svg>`;
}

export const FIGURE_CSS = `
.pf-body{stroke:var(--fig-body,#2b3440)}
.pf-far{stroke:var(--fig-far,#9aa6b2)}
.pf-head{fill:var(--fig-body,#2b3440)}
.pf-ground{stroke:var(--fig-ground,#c9d1d9)}
.pf-plate{fill:var(--fig-accent,#2f6f5e);stroke:none}
.pf-hub{fill:var(--fig-bg,#fff)}
.pf-prop{fill:var(--fig-prop,#d7dde3);stroke:var(--fig-prop-edge,#aab4bf);stroke-width:1}
.pf-prop-solid{fill:var(--fig-prop-edge,#8d99a6)}
.pf-prop-line{stroke:var(--fig-prop-edge,#aab4bf)}
.pf-cable{stroke:var(--fig-prop-edge,#8d99a6);stroke-width:1.5;fill:none}
.pf-cable-faint{stroke:var(--fig-prop-edge,#8d99a6);stroke-width:1.2;fill:none;opacity:.45}
.pf-ball{fill:var(--fig-accent-2,#c9892b)}
.pf-water{fill:var(--fig-water,#dcecf5)}
.pf-net{fill:var(--fig-prop-edge,#8d99a6)}
.pf-arrow{stroke:var(--fig-accent,#2f6f5e);stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
.pd-court{fill:var(--fig-court,#f1ece2);stroke:var(--fig-prop-edge,#aab4bf);stroke-width:1.5}
.pd-water{fill:var(--fig-water,#dcecf5);stroke:var(--fig-prop-edge,#aab4bf);stroke-width:1.5}
.pd-net{stroke:var(--fig-body,#2b3440)}
.pd-line{stroke:var(--fig-prop-edge,#aab4bf)}
.pd-label{fill:var(--fig-muted,#5b6875);font-size:9px;font-family:-apple-system,system-ui,sans-serif}
.pd-marker{fill:var(--fig-accent-2,#c9892b)}
.pd-step{fill:var(--fig-accent,#2f6f5e)}
.pd-step-text{fill:#fff;font-size:9px;font-weight:600;font-family:-apple-system,system-ui,sans-serif}
`;
