import type { SetLog } from '../db/records';

// Compact, readable summaries of logged sets, for example
// "50 kg × 10, 9, 8 · RIR 3" or "Left 16 kg × 12, 12 · Right 16 kg × 12, 11".

function group(sets: SetLog[]): string {
  if (!sets.length) return '';
  const w = sets.map((s) => s.weightKg);
  const sameW = w.every((x) => x === w[0]);
  const parts: string[] = [];
  if (sets.some((s) => s.roundTrips !== null)) {
    parts.push(`${sets.map((s) => s.roundTrips ?? 0).join(' + ')} round trips`);
    const rpe = sets.map((s) => s.rpe).filter((x) => x !== null);
    if (rpe.length) parts.push(`RPE ${rpe.join(', ')}`);
    return parts.join(' · ');
  }
  if (sets.every((s) => s.reps === null) && sets.some((s) => s.seconds !== null)) {
    const secs = sets.map((s) => s.seconds ?? 0);
    return secs.every((x) => x >= 120) ? `${secs.map((x) => Math.round(x / 60)).join(', ')} min` : `${secs.join(', ')} s`;
  }
  const reps = sets.map((s) => s.reps ?? 0).join(', ');
  if (w[0] !== null && sameW) parts.push(`${w[0]} kg × ${reps}`);
  else if (w.some((x) => x !== null)) parts.push(sets.map((s) => `${s.weightKg ?? 0}×${s.reps ?? 0}`).join(', '));
  else parts.push(`${reps} reps`);
  const rir = [...new Set(sets.map((s) => s.rir).filter((x) => x !== null))];
  if (rir.length === 1) parts.push(`RIR ${rir[0]}`);
  else if (rir.length > 1) parts.push(`RIR ${sets.map((s) => s.rir ?? '-').join(', ')}`);
  const q = sets.map((s) => s.quality).filter((x) => x !== null);
  if (q.length) parts.push(`quality ${q.join(', ')}`);
  const bad = sets.filter((s) => s.form === 'poor').length;
  if (bad) parts.push(`${bad} poor form`);
  const pain = sets.filter((s) => s.pain !== 'none').length;
  if (pain) parts.push(`pain on ${pain}`);
  return parts.join(' · ');
}

export function summarizeSets(sets: SetLog[]): string {
  const work = sets.filter((s) => !s.warmup).sort((a, b) => a.setIndex - b.setIndex || a.completedAt - b.completedAt);
  if (work.some((s) => s.side)) {
    const l = work.filter((s) => s.side === 'left');
    const r = work.filter((s) => s.side === 'right');
    return [l.length ? `Left ${group(l)}` : '', r.length ? `Right ${group(r)}` : ''].filter(Boolean).join('  ·  ');
  }
  return group(work);
}
