import { Suspense, lazy, useEffect, useState, type ReactNode } from 'react';
import { SettingsProvider, TimerProvider, useSettings, useTimer } from './ui/state';
import { ToastProvider, useOnline } from './ui/components';
import { useRoute, navigate } from './ui/router';
import { IconEat, IconMore, IconProgress, IconToday, IconTrain } from './ui/icons';
import { formatClock, isFinished, remainingMs } from './domain/timer';
import { useCustomExercises } from './ui/hooks';
import { TodayScreen } from './screens/Today';
import { TrainScreen, TrainDayScreen, StartWorkoutRedirect } from './screens/Train';
import { WorkoutScreen } from './screens/Workout';
import { EatScreen } from './screens/Eat';
import { CheckInScreen } from './screens/CheckIn';
import { OnboardingScreen } from './screens/Onboarding';

// Less frequent screens load on demand. The service worker precaches every chunk, so they still open offline.
const ExerciseScreen = lazy(() => import('./screens/ExerciseDetail').then((m) => ({ default: m.ExerciseScreen })));
const LibraryScreen = lazy(() => import('./screens/ExerciseDetail').then((m) => ({ default: m.LibraryScreen })));
const FoodLogScreen = lazy(() => import('./screens/FoodLogger').then((m) => ({ default: m.FoodLogScreen })));
const SabbathPlateScreen = lazy(() => import('./screens/Sabbath').then((m) => ({ default: m.SabbathPlateScreen })));
const MealPrepScreen = lazy(() => import('./screens/MealPrep').then((m) => ({ default: m.MealPrepScreen })));
const RecipeScreen = lazy(() => import('./screens/MealPrep').then((m) => ({ default: m.RecipeScreen })));
const RecipesScreen = lazy(() => import('./screens/MealPrep').then((m) => ({ default: m.RecipesScreen })));
const ProgressScreen = lazy(() => import('./screens/Progress').then((m) => ({ default: m.ProgressScreen })));
const CoverageScreen = lazy(() => import('./screens/Progress').then((m) => ({ default: m.CoverageScreen })));
const ExerciseHistoryScreen = lazy(() => import('./screens/Progress').then((m) => ({ default: m.ExerciseHistoryScreen })));
const ReviewScreen = lazy(() => import('./screens/Review').then((m) => ({ default: m.ReviewScreen })));
const MoreScreen = lazy(() => import('./screens/More').then((m) => ({ default: m.MoreScreen })));
const MoreSubScreen = lazy(() => import('./screens/More').then((m) => ({ default: m.MoreSubScreen })));
const ProgramScreen = lazy(() => import('./screens/Program').then((m) => ({ default: m.ProgramScreen })));
import { LockGate } from './screens/Lock';
import { useRegisterSW } from 'virtual:pwa-register/react';
import { unlockAudio } from './lib/device';
import { syncProgramPhase } from './services/planUpdate';

const TABS = [
  { to: '/today', label: 'Today', Icon: IconToday, match: ['today', 'checkin'] },
  { to: '/train', label: 'Train', Icon: IconTrain, match: ['train', 'workout', 'exercise', 'library', 'program'] },
  { to: '/eat', label: 'Eat', Icon: IconEat, match: ['eat', 'recipes', 'recipe', 'prep'] },
  { to: '/progress', label: 'Progress', Icon: IconProgress, match: ['progress', 'review', 'coverage', 'history'] },
  { to: '/more', label: 'More', Icon: IconMore, match: ['more'] },
];

function TabBar({ section }: { section: string }) {
  return (
    <nav className="tabbar" aria-label="Main">
      <ul>
        {TABS.map((t) => (
          <li key={t.to}>
            <a href={`#${t.to}`} aria-current={t.match.includes(section) ? 'page' : undefined} data-testid={`tab-${t.label.toLowerCase()}`}>
              <t.Icon />
              <span>{t.label}</span>
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

function RestBar() {
  const { timer, now, stop, adjust, pause, resume } = useTimer();
  void pause;
  const active = !!timer;
  useEffect(() => {
    document.documentElement.style.setProperty('--timer-h', active ? '72px' : '0px');
  }, [active]);
  if (!timer) return null;
  const rem = remainingMs(timer, now);
  const done = isFinished(timer, now);
  const paused = timer.pausedRemainingMs !== null;
  const pct = timer.durationSec > 0 ? Math.min(100, 100 - (rem / (timer.durationSec * 1000)) * 100) : 100;
  return (
    <div className={`restbar ${done ? 'done' : ''}`} role="timer" aria-live="off" data-testid="restbar">
      <div className="restbar-inner">
        <div className="grow" style={{ minWidth: 0 }}>
          <div className="row" style={{ gap: 10 }}>
            <button type="button" className="restbar-time" data-testid="rest-remaining" onClick={() => !done && (paused ? resume() : pause())} aria-label={done ? 'Rest finished' : paused ? 'Resume rest timer' : 'Pause rest timer'}>
              {done ? formatClock(now - timer.endAt) : formatClock(rem)}
            </button>
            <span className="restbar-label">
              <span>{done ? 'Rest finished' : paused ? 'Paused, tap time' : 'Rest'}</span>
              <span style={{ opacity: 0.85 }}>{done ? `${Math.round((now - timer.endAt) / 1000)} s ago` : timer.label}</span>
            </span>
          </div>
          {!done && (
            <div className="restbar-progress" aria-hidden="true">
              <div style={{ width: `${pct}%` }} />
            </div>
          )}
        </div>
        {!done && (
          <>
            <button type="button" className="btn" onClick={() => adjust(-15)} aria-label="Fifteen seconds less">
              −15
            </button>
            <button type="button" className="btn" onClick={() => adjust(15)} aria-label="Fifteen seconds more">
              +15
            </button>
          </>
        )}
        <button type="button" className="btn" onClick={stop} data-testid="rest-dismiss">
          {done ? 'Done' : 'Skip'}
        </button>
      </div>
    </div>
  );
}

function Banners() {
  const online = useOnline();
  const {
    needRefresh: [needRefresh],
    updateServiceWorker,
  } = useRegisterSW({
    immediate: true,
    // A Home Screen app is often resumed instead of reopened, and then nothing checks for a new
    // version. Check again whenever PeakForm comes back to the screen, and once an hour.
    onRegisteredSW(_url, r) {
      if (!r) return;
      const check = () => {
        if (document.visibilityState === 'visible' && navigator.onLine) r.update().catch(() => undefined);
      };
      document.addEventListener('visibilitychange', check);
      window.setInterval(check, 60 * 60 * 1000);
    },
  });
  return (
    <>
      {!online && (
        <div className="banner offline" role="status" data-testid="offline-banner">
          <span>Offline. Everything you log is saved on this phone.</span>
        </div>
      )}
      {needRefresh && (
        <div className="banner" role="status">
          <span>A new version of PeakForm is ready.</span>
          <button type="button" className="btn btn-sm btn-primary" onClick={() => void updateServiceWorker(true)}>
            Update
          </button>
        </div>
      )}
    </>
  );
}

function Routes() {
  const { parts, query } = useRoute();
  const settings = useSettings();
  useCustomExercises();
  const [a = 'today', b, c] = parts;
  if (!settings.onboarded && a !== 'more') return <OnboardingScreen />;
  let screen: ReactNode;
  switch (a) {
    case 'today':
      screen = <TodayScreen />;
      break;
    case 'checkin':
      screen = <CheckInScreen />;
      break;
    case 'train':
      if (b === 'start') screen = <StartWorkoutRedirect />;
      else if (b === 'day' && c !== undefined) screen = <TrainDayScreen weekday={Number(c)} date={query.get('date')} />;
      else screen = <TrainScreen />;
      break;
    case 'workout':
      screen = <WorkoutScreen sessionId={b ?? ''} />;
      break;
    case 'exercise':
      screen = <ExerciseScreen id={b ?? ''} />;
      break;
    case 'library':
      screen = <LibraryScreen />;
      break;
    case 'program':
      screen = <ProgramScreen step={query.get('step')} />;
      break;
    case 'eat':
      if (b === 'log') screen = <FoodLogScreen slot={c ?? 'other'} date={query.get('date')} mode={query.get('mode')} />;
      else if (b === 'sabbath') screen = <SabbathPlateScreen date={query.get('date')} />;
      else screen = <EatScreen />;
      break;
    case 'prep':
      screen = <MealPrepScreen />;
      break;
    case 'recipes':
      screen = <RecipesScreen />;
      break;
    case 'recipe':
      screen = <RecipeScreen id={b ?? ''} />;
      break;
    case 'progress':
      screen = <ProgressScreen />;
      break;
    case 'coverage':
      screen = <CoverageScreen />;
      break;
    case 'history':
      screen = <ExerciseHistoryScreen id={b ?? ''} />;
      break;
    case 'review':
      screen = <ReviewScreen weekStart={b ?? null} />;
      break;
    case 'more':
      screen = b ? <MoreSubScreen page={b} /> : <MoreScreen />;
      break;
    default:
      screen = <TodayScreen />;
  }
  return (
    <>
      <main className="page" key={a + (b ?? '')}>
        <Suspense fallback={<p className="muted small">Loading…</p>}>{screen}</Suspense>
      </main>
      <RestBar />
      <TabBar section={a} />
    </>
  );
}

export function App() {
  useEffect(() => {
    // iOS can suspend audio at any time, so every tap gets a chance to wake it again.
    const unlock = () => unlockAudio();
    window.addEventListener('pointerdown', unlock);
    if (!window.location.hash) navigate('/today', { replace: true });
    // A new training block starts on its Monday, so check when the app opens or comes back.
    const block = () => {
      if (document.visibilityState === 'visible') void syncProgramPhase().catch(() => undefined);
    };
    block();
    document.addEventListener('visibilitychange', block);
    const hourly = window.setInterval(block, 60 * 60 * 1000);
    return () => {
      window.removeEventListener('pointerdown', unlock);
      document.removeEventListener('visibilitychange', block);
      window.clearInterval(hourly);
    };
  }, []);
  return (
    <SettingsProvider>
      <TimerProvider>
        <ToastProvider>
          <LockGate>
            <div className="app">
              <Banners />
              <Routes />
            </div>
          </LockGate>
        </ToastProvider>
      </TimerProvider>
    </SettingsProvider>
  );
}

export function useIsNarrow(): boolean {
  const [n, setN] = useState(window.innerWidth < 380);
  useEffect(() => {
    const on = () => setN(window.innerWidth < 380);
    window.addEventListener('resize', on);
    return () => window.removeEventListener('resize', on);
  }, []);
  return n;
}
