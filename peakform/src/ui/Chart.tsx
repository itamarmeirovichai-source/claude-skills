import { formatDateKey, diffDays, type DateKey } from '../domain/dates';

// Small, dependency free SVG charts. Every chart has a text summary and a table fallback,
// so nothing depends on colour or on seeing the line.

export interface Pt {
  x: DateKey;
  y: number;
}

function niceStep(raw: number): number {
  const mag = 10 ** Math.floor(Math.log10(raw));
  const n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * mag;
}

export function LineChart({ points, line, unit, label, band, height = 150, decimals = 1 }: { points: Pt[]; line?: Pt[]; unit: string; label: string; band?: [number, number]; height?: number; decimals?: number }) {
  const all = [...points, ...(line ?? [])];
  if (all.length === 0) return <p className="small muted">Nothing logged yet.</p>;
  const W = 320;
  const H = height;
  const padL = 40;
  const padR = 10;
  const padT = 10;
  const padB = 22;
  const xs = all.map((p) => p.x).sort();
  const x0 = xs[0]!;
  const x1 = xs[xs.length - 1]!;
  const span = Math.max(1, diffDays(x1, x0));
  let ymin = Math.min(...all.map((p) => p.y), ...(band ?? []));
  let ymax = Math.max(...all.map((p) => p.y), ...(band ?? []));
  if (ymax - ymin < 1) {
    ymin -= 0.5;
    ymax += 0.5;
  }
  const padY = (ymax - ymin) * 0.12;
  ymin -= padY;
  ymax += padY;
  // Round axis labels, for example 78, 78.5, 79 rather than 77.9, 78.6, 79.2.
  const step = niceStep((ymax - ymin) / 3);
  const ticks: number[] = [];
  for (let t = Math.ceil(ymin / step) * step; t <= ymax + 1e-9; t += step) ticks.push(Number(t.toFixed(6)));
  const inner = 8;
  const sx = (d: DateKey) => padL + inner + (diffDays(d, x0) / span) * (W - padL - padR - inner * 2);
  const sy = (v: number) => padT + (1 - (v - ymin) / (ymax - ymin)) * (H - padT - padB);
  const path = (ps: Pt[]) => ps.map((p, i) => `${i ? 'L' : 'M'}${sx(p.x).toFixed(1)},${sy(p.y).toFixed(1)}`).join(' ');
  const lastLine = line && line.length ? line[line.length - 1] : undefined;
  const firstLine = line && line.length ? line[0] : undefined;
  const summary = lastLine && firstLine ? `${label}: ${firstLine.y.toFixed(decimals)} ${unit} on ${formatDateKey(firstLine.x)} to ${lastLine.y.toFixed(decimals)} ${unit} on ${formatDateKey(lastLine.x)}.` : `${label}: ${points.length} values.`;
  return (
    <figure style={{ margin: 0 }}>
      <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={summary}>
        {band && <rect className="band" x={padL} width={W - padL - padR} y={sy(band[1])} height={Math.max(0, sy(band[0]) - sy(band[1]))} />}
        {ticks.map((t) => (
          <g key={t}>
            <line className="grid" x1={padL} x2={W - padR} y1={sy(t)} y2={sy(t)} />
            <text x={padL - 4} y={sy(t) + 4} textAnchor="end">
              {step >= 1 ? t.toFixed(0) : t.toFixed(1)}
            </text>
          </g>
        ))}
        <line className="axis" x1={padL} x2={W - padR} y1={H - padB} y2={H - padB} />
        <text x={padL} y={H - 6}>
          {formatDateKey(x0, { day: 'numeric', month: 'short' })}
        </text>
        <text x={W - padR} y={H - 6} textAnchor="end">
          {formatDateKey(x1, { day: 'numeric', month: 'short' })}
        </text>
        {line && line.length > 1 && <path className="line" d={path(line)} />}
        {points.map((p) => (
          <circle key={p.x + p.y} className="pt" cx={sx(p.x)} cy={sy(p.y)} r={2.6} />
        ))}
      </svg>
      <figcaption className="small muted" style={{ marginTop: 4 }}>
        {summary}
      </figcaption>
      <details className="disclosure">
        <summary className="small">Show numbers</summary>
        <table className="prev-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Value</th>
              {line && <th>Average</th>}
            </tr>
          </thead>
          <tbody>
            {[...new Set(all.map((p) => p.x))]
              .sort()
              .reverse()
              .slice(0, 28)
              .map((d) => (
                <tr key={d}>
                  <td>{formatDateKey(d)}</td>
                  <td>{points.find((p) => p.x === d)?.y.toFixed(decimals) ?? ''}</td>
                  {line && <td>{line.find((p) => p.x === d)?.y.toFixed(decimals) ?? ''}</td>}
                </tr>
              ))}
          </tbody>
        </table>
      </details>
    </figure>
  );
}

export function Bars({ items, unit, target, max }: { items: Array<{ label: string; value: number; note?: string }>; unit: string; target?: number; max?: number }) {
  const m = max ?? Math.max(1, target ?? 0, ...items.map((i) => i.value));
  return (
    <div className="stack" style={{ gap: 6 }}>
      {items.map((i) => (
        <div key={i.label} className="row" style={{ gap: 8 }}>
          <span className="small" style={{ width: 92, flex: '0 0 auto' }}>
            {i.label}
          </span>
          <div className="bar grow" role="img" aria-label={`${i.label} ${i.value.toFixed(1)} ${unit}`}>
            {target !== undefined && <div className="bar-range" style={{ left: `${(target / m) * 100}%`, width: 0 }} />}
            <div className="bar-fill" style={{ width: `${Math.min(100, (i.value / m) * 100)}%` }} />
          </div>
          <span className="small num" style={{ width: 56, textAlign: 'right' }}>
            {i.value.toFixed(1)} {unit}
          </span>
        </div>
      ))}
    </div>
  );
}
