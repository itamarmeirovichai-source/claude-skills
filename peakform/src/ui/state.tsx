import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { KV, kvGet, saveTimer } from '../db/repo';
import type { AppSettings, TimerHistory } from '../db/records';
import { adjustTimer, isFinished, pauseTimer, remainingMs, restoreTimer, resumeTimer, startTimer, type RestTimerState } from '../domain/timer';
import { uid } from '../lib/id';
import { audioReady, cue, haptic, keepAwake, releaseAwake, scheduleCue } from '../lib/device';

// App wide state: live settings and the single rest timer that stays visible everywhere.

const SettingsCtx = createContext<AppSettings | null>(null);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const settings = useLiveQuery(() => db.settings.get('app'), []);
  useEffect(() => {
    if (!settings) return;
    const root = document.documentElement;
    if (settings.theme === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', settings.theme);
    if (settings.reducedMotion === 'on') root.setAttribute('data-motion', 'reduce');
    else root.removeAttribute('data-motion');
    document.title = settings.appName;
  }, [settings]);
  if (!settings) return null;
  return <SettingsCtx.Provider value={settings}>{children}</SettingsCtx.Provider>;
}

export function useSettings(): AppSettings {
  const s = useContext(SettingsCtx);
  if (!s) throw new Error('Settings not loaded');
  return s;
}

// ---------- Rest timer ----------

interface TimerApi {
  timer: RestTimerState | null;
  now: number;
  start: (label: string, seconds: number, exerciseId?: string | null) => void;
  stop: () => void;
  pause: () => void;
  resume: () => void;
  adjust: (sec: number) => void;
  overdueMs: number;
}

const TimerCtx = createContext<TimerApi | null>(null);

export function TimerProvider({ children }: { children: ReactNode }) {
  const settings = useContext(SettingsCtx);
  const [timer, setTimer] = useState<RestTimerState | null>(null);
  const [now, setNow] = useState(Date.now());
  const [overdueMs, setOverdue] = useState(0);
  const announced = useRef<string | null>(null);
  // The end sound queued on the audio clock for the running timer, keyed by timer and end time.
  const queued = useRef<{ key: string; cancel: () => void } | null>(null);
  const soundRef = useRef<AppSettings['restSound']>('beep');
  soundRef.current = settings?.restSound ?? 'beep';

  const unqueue = useCallback(() => {
    queued.current?.cancel();
    queued.current = null;
  }, []);
  const queue = useCallback(
    (t: RestTimerState | null) => {
      unqueue();
      if (!t || t.pausedRemainingMs !== null) return;
      const left = remainingMs(t, Date.now());
      const cancel = scheduleCue(soundRef.current, left);
      if (cancel) queued.current = { key: `${t.id}:${t.endAt}`, cancel };
    },
    [unqueue],
  );

  // Restore from storage on launch and whenever the app returns to the foreground.
  const restore = useCallback(async () => {
    const saved = await kvGet<RestTimerState>(KV.timer);
    const r = restoreTimer(saved ?? null, Date.now());
    setTimer(r.timer);
    setOverdue(r.overdueMs);
    if (!r.timer && saved) await saveTimer(null);
    setNow(Date.now());
  }, []);

  useEffect(() => {
    void restore();
    const onVis = () => {
      if (document.visibilityState === 'visible') void restore();
      // iOS pauses audio in the background; a sound queued now would play late, so drop it.
      else unqueue();
    };
    document.addEventListener('visibilitychange', onVis);
    window.addEventListener('pageshow', onVis);
    window.addEventListener('focus', onVis);
    return () => {
      document.removeEventListener('visibilitychange', onVis);
      window.removeEventListener('pageshow', onVis);
      window.removeEventListener('focus', onVis);
    };
  }, [restore, unqueue]);

  // After returning to the app, queue the end sound again for the time that is left.
  useEffect(() => {
    if (!timer || isFinished(timer, Date.now())) return;
    if (queued.current?.key === `${timer.id}:${timer.endAt}`) return;
    queue(timer);
  }, [timer, queue]);

  useEffect(() => {
    if (!timer) return;
    const iv = window.setInterval(() => setNow(Date.now()), 250);
    return () => window.clearInterval(iv);
  }, [timer]);

  // Announce the end once, only while the app is open.
  useEffect(() => {
    if (!timer || !isFinished(timer, now) || announced.current === timer.id) return;
    announced.current = timer.id;
    setOverdue(now - timer.endAt);
    if (settings) {
      // If the sound was queued on the audio clock and audio is running, it has already played on time.
      const playedOnClock = queued.current?.key === `${timer.id}:${timer.endAt}` && audioReady();
      if (playedOnClock) {
        if (settings.vibration) haptic([120, 60, 120]);
      } else cue(settings.restSound, settings.vibration);
    }
    queued.current = null;
    void recordHistory(timer, true);
  }, [timer, now, settings]);

  const persist = useCallback(async (t: RestTimerState | null) => {
    setTimer(t);
    await saveTimer(t);
  }, []);

  const api = useMemo<TimerApi>(
    () => ({
      timer,
      now,
      overdueMs,
      start: (label, seconds, exerciseId = null) => {
        const t = startTimer(label, seconds, Date.now(), exerciseId);
        announced.current = null;
        setOverdue(0);
        queue(t);
        void persist(t);
        if (settings?.keepScreenOn) void keepAwake();
      },
      stop: () => {
        if (timer && !isFinished(timer, Date.now())) void recordHistory(timer, false);
        unqueue();
        void persist(null);
        void releaseAwake();
      },
      pause: () => {
        if (!timer) return;
        unqueue();
        void persist(pauseTimer(timer, Date.now()));
      },
      resume: () => {
        if (!timer) return;
        const t = resumeTimer(timer, Date.now());
        queue(t);
        void persist(t);
      },
      adjust: (sec) => {
        if (!timer) return;
        const t = adjustTimer(timer, sec, Date.now());
        if (remainingMs(t, Date.now()) > 0) announced.current = null;
        queue(t);
        void persist(t);
      },
    }),
    [timer, now, overdueMs, persist, settings, queue, unqueue],
  );

  return <TimerCtx.Provider value={api}>{children}</TimerCtx.Provider>;
}

async function recordHistory(t: RestTimerState, completed: boolean) {
  const rec: TimerHistory = { id: uid('tmr'), createdAt: Date.now(), updatedAt: Date.now(), label: t.label, durationSec: t.durationSec, startedAt: t.startedAt, endedAt: Date.now(), completed };
  await db.timerHistory.put(rec);
}

export function useTimer(): TimerApi {
  const t = useContext(TimerCtx);
  if (!t) throw new Error('Timer not ready');
  return t;
}
