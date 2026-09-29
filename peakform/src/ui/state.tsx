import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { KV, kvGet, saveTimer } from '../db/repo';
import type { AppSettings, TimerHistory } from '../db/records';
import { adjustTimer, isFinished, pauseTimer, remainingMs, restoreTimer, resumeTimer, startTimer, type RestTimerState } from '../domain/timer';
import { uid } from '../lib/id';
import { cue, keepAwake, releaseAwake } from '../lib/device';

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
    };
    document.addEventListener('visibilitychange', onVis);
    window.addEventListener('pageshow', onVis);
    window.addEventListener('focus', onVis);
    return () => {
      document.removeEventListener('visibilitychange', onVis);
      window.removeEventListener('pageshow', onVis);
      window.removeEventListener('focus', onVis);
    };
  }, [restore]);

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
    if (settings) cue(settings.restSound, settings.vibration);
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
        void persist(t);
        if (settings?.keepScreenOn) void keepAwake();
      },
      stop: () => {
        if (timer && !isFinished(timer, Date.now())) void recordHistory(timer, false);
        void persist(null);
        void releaseAwake();
      },
      pause: () => timer && void persist(pauseTimer(timer, Date.now())),
      resume: () => timer && void persist(resumeTimer(timer, Date.now())),
      adjust: (sec) => {
        if (!timer) return;
        const t = adjustTimer(timer, sec, Date.now());
        if (remainingMs(t, Date.now()) > 0) announced.current = null;
        void persist(t);
      },
    }),
    [timer, now, overdueMs, persist, settings],
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
