import type { DrillDiagram, ExerciseVisual, Pose } from '../content/types';
import { diagramPrims, posePrims, DIAGRAM_H, DIAGRAM_W, POSE_W, POSE_H, type Prim } from './pose';

// Original keyframe illustrations and drill diagrams, rendered offline from pose data.

const HEADROOM = 18;

function PrimEl({ p }: { p: Prim }) {
  switch (p.t) {
    case 'line':
      return <line x1={p.x1} y1={p.y1} x2={p.x2} y2={p.y2} className={p.cls} strokeWidth={p.w ?? 2} strokeLinecap="round" />;
    case 'circle':
      return <circle cx={p.cx} cy={p.cy} r={p.r} className={p.cls} />;
    case 'rect':
      return <rect x={p.x} y={p.y} width={p.w} height={p.h} rx={p.rx ?? 0} className={p.cls} transform={p.rot ? `rotate(${p.rot.a} ${p.rot.cx} ${p.rot.cy})` : undefined} />;
    case 'path':
      return <path d={p.d} className={p.cls} fill="none" />;
    case 'text':
      return (
        <text x={p.x} y={p.y} className={p.cls} textAnchor={p.anchor ?? 'start'}>
          {p.text}
        </text>
      );
  }
}

export function PoseSvg({ pose, label }: { pose: Pose; label: string }) {
  return (
    <svg viewBox={`0 ${-HEADROOM} ${POSE_W} ${POSE_H + HEADROOM}`} role="img" aria-label={label}>
      {posePrims(pose).map((p, i) => (
        <PrimEl key={i} p={p} />
      ))}
    </svg>
  );
}

export function DiagramSvg({ diagram }: { diagram: DrillDiagram }) {
  return (
    <svg viewBox={`0 0 ${DIAGRAM_W} ${DIAGRAM_H}`} role="img" aria-label={diagram.caption}>
      {diagramPrims(diagram).map((p, i) => (
        <PrimEl key={i} p={p} />
      ))}
    </svg>
  );
}

export function Keyframes({ visual, name }: { visual: ExerciseVisual; name: string }) {
  const poses = visual.poses ?? [];
  return (
    <div className="stack">
      {poses.length > 0 && (
        <div className="figs" data-testid="keyframes">
          {poses.map((p, i) => (
            <figure className="fig" key={i}>
              <PoseSvg pose={p} label={`${name}, ${p.label}: ${p.caption}`} />
              <figcaption>
                <b>{p.label}</b>
                {p.caption}
              </figcaption>
            </figure>
          ))}
        </div>
      )}
      {visual.diagram && (
        <figure className="fig" style={{ maxWidth: 360 }} data-testid="drill-diagram">
          <DiagramSvg diagram={visual.diagram} />
          <figcaption>{visual.diagram.caption}</figcaption>
        </figure>
      )}
      {poses.length === 0 && !visual.diagram && <p className="muted small">No illustration for this custom exercise.</p>}
    </div>
  );
}
