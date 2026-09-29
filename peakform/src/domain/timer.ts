// Rest timer based on an absolute end timestamp. The remaining time is always
// derived from Date.now(), so it stays correct after the screen locks, the tab is
// backgrounded, or iOS suspends the app. Nothing here claims to alert in the background.

export interface RestTimerState {
  id: string;
  label: string;
  exerciseId: string | null;
  startedAt: number;
  durationSec: number;
  /** Absolute end time in epoch ms while running. */
  endAt: number;
  /** Remaining ms captured when paused, otherwise null. */
  pausedRemainingMs: number | null;
  /** Set once the end has been announced, so it is not announced twice. */
  announced: boolean;
}

export function startTimer(label: string, durationSec: number, now: number, exerciseId: string | null = null): RestTimerState {
  return {
    id: `t-${now.toString(36)}`,
    label,
    exerciseId,
    startedAt: now,
    durationSec,
    endAt: now + durationSec * 1000,
    pausedRemainingMs: null,
    announced: false,
  };
}

export function remainingMs(t: RestTimerState, now: number): number {
  if (t.pausedRemainingMs !== null) return t.pausedRemainingMs;
  return Math.max(0, t.endAt - now);
}

export function isFinished(t: RestTimerState, now: number): boolean {
  return t.pausedRemainingMs === null && now >= t.endAt;
}

export function pauseTimer(t: RestTimerState, now: number): RestTimerState {
  if (t.pausedRemainingMs !== null) return t;
  return { ...t, pausedRemainingMs: remainingMs(t, now) };
}

export function resumeTimer(t: RestTimerState, now: number): RestTimerState {
  if (t.pausedRemainingMs === null) return t;
  return { ...t, endAt: now + t.pausedRemainingMs, pausedRemainingMs: null };
}

export function adjustTimer(t: RestTimerState, deltaSec: number, now: number): RestTimerState {
  if (t.pausedRemainingMs !== null) {
    return { ...t, pausedRemainingMs: Math.max(0, t.pausedRemainingMs + deltaSec * 1000), durationSec: Math.max(0, t.durationSec + deltaSec) };
  }
  const endAt = Math.max(now, t.endAt + deltaSec * 1000);
  return { ...t, endAt, durationSec: Math.max(0, t.durationSec + deltaSec), announced: endAt > now ? false : t.announced };
}

/**
 * Restore a timer read from storage after the app was suspended.
 * Returns the state with an overdue flag so the UI can show "Rest finished 40 seconds ago".
 */
export function restoreTimer(t: RestTimerState | null, now: number): { timer: RestTimerState | null; overdueMs: number } {
  if (!t) return { timer: null, overdueMs: 0 };
  if (t.pausedRemainingMs !== null) return { timer: t, overdueMs: 0 };
  const overdue = now - t.endAt;
  // Drop timers that finished more than 15 minutes ago; they are no longer useful.
  if (overdue > 15 * 60 * 1000) return { timer: null, overdueMs: overdue };
  return { timer: t, overdueMs: Math.max(0, overdue) };
}

export function formatClock(ms: number): string {
  const total = Math.ceil(ms / 1000);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}
