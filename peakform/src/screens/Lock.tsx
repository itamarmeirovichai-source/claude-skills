import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { useSettings } from '../ui/state';
import { verifyPin } from '../lib/pin';
import { IconLock } from '../ui/icons';
import { deleteAllData, ensureInitialized } from '../db/repo';

// Optional app lock after inactivity. A privacy convenience, not encryption.

export function LockGate({ children }: { children: ReactNode }) {
  const s = useSettings();
  const enabled = s.lock.enabled && !!s.lock.pinHash && !!s.lock.salt;
  const [locked, setLocked] = useState(enabled);
  const lastActive = useRef(Date.now());
  const idleMs = s.lock.idleMinutes * 60_000;

  useEffect(() => {
    if (!enabled) setLocked(false);
  }, [enabled]);

  useEffect(() => {
    if (!enabled) return;
    const touch = () => (lastActive.current = Date.now());
    const check = () => {
      if (Date.now() - lastActive.current > idleMs) setLocked(true);
    };
    const onVis = () => (document.visibilityState === 'visible' ? check() : touch());
    window.addEventListener('pointerdown', touch);
    window.addEventListener('keydown', touch);
    document.addEventListener('visibilitychange', onVis);
    const iv = window.setInterval(check, 15_000);
    return () => {
      window.removeEventListener('pointerdown', touch);
      window.removeEventListener('keydown', touch);
      document.removeEventListener('visibilitychange', onVis);
      window.clearInterval(iv);
    };
  }, [enabled, idleMs]);

  const unlock = useCallback(() => {
    lastActive.current = Date.now();
    setLocked(false);
  }, []);

  if (enabled && locked) return <LockScreen salt={s.lock.salt!} hash={s.lock.pinHash!} onUnlock={unlock} />;
  return <>{children}</>;
}

function LockScreen({ salt, hash, onUnlock }: { salt: string; hash: string; onUnlock: () => void }) {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [forgot, setForgot] = useState(false);
  const press = async (d: string) => {
    const next = (pin + d).slice(0, 8);
    setPin(next);
    setError('');
    if (next.length >= 4 && (await verifyPin(next, salt, hash))) onUnlock();
    else if (next.length === 8) {
      setError('That PIN is not right.');
      setPin('');
    }
  };
  return (
    <div className="lock" data-testid="lock-screen">
      <IconLock size={36} />
      <h2>Enter your PIN</h2>
      <div className="pin-dots" aria-label={`${pin.length} digits entered`}>
        {Array.from({ length: Math.max(4, pin.length) }, (_, i) => (
          <span key={i} className={i < pin.length ? 'on' : ''} />
        ))}
      </div>
      {error && <p role="alert">{error}</p>}
      <div className="keypad">
        {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((d) => (
          <button key={d} type="button" onClick={() => void press(d)} data-testid={`key-${d}`}>
            {d}
          </button>
        ))}
        <button type="button" style={{ fontSize: '1rem' }} onClick={() => setPin('')} aria-label="Clear">
          Clear
        </button>
        <button type="button" onClick={() => void press('0')} data-testid="key-0">
          0
        </button>
        <button type="button" style={{ fontSize: '1rem' }} onClick={() => setPin(pin.slice(0, -1))} aria-label="Delete last digit">
          Del
        </button>
      </div>
      {!forgot ? (
        <button type="button" className="btn btn-ghost" onClick={() => setForgot(true)}>
          Forgot PIN
        </button>
      ) : (
        <div className="panel stack" style={{ maxWidth: 360 }}>
          <p className="small">The PIN cannot be recovered. You can erase PeakForm's data on this phone, then restore your latest backup.</p>
          <button
            type="button"
            className="btn btn-danger"
            onClick={async () => {
              if (!window.confirm('Erase all PeakForm data on this phone?')) return;
              await deleteAllData();
              await ensureInitialized();
              window.location.reload();
            }}
          >
            Erase and start again
          </button>
        </div>
      )}
    </div>
  );
}
