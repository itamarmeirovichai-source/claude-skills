import { useState } from 'react';
import { getProfile, saveProfile, updateSettings } from '../db/repo';
import { useSettings } from '../ui/state';
import { Note, Stepper, Toggle } from '../ui/components';
import { navigate } from '../ui/router';
import { useToday } from '../ui/hooks';
import { loadDemo } from './MoreData';
import { requestPersistence } from '../lib/device';

// First run. Generic by design: the private profile is entered here, on the device,
// or imported from a private setup file. Nothing personal is part of the app itself.

export function OnboardingScreen() {
  const settings = useSettings();
  const today = useToday();
  const [step, setStep] = useState(0);
  const [name, setName] = useState('');
  const [height, setHeight] = useState<number | null>(null);
  const [birthYear, setBirthYear] = useState<number | null>(null);
  const [ack, setAck] = useState(false);
  const [sabbath, setSabbath] = useState(settings.sabbath.enabled);
  const [fri, setFri] = useState(settings.sabbath.fridayStart);
  const [sat, setSat] = useState(settings.sabbath.saturdayEnd);
  const [pool, setPool] = useState<number | null>(settings.poolLengthM);

  const finish = async (demo: boolean) => {
    const p = await getProfile();
    await saveProfile({ ...p, name: name.trim(), heightCm: height, birthYear });
    if (demo) await loadDemo(today, false);
    void requestPersistence();
    // Route first, then mark onboarding complete as the very last write.
    navigate('/today', { replace: true });
    await updateSettings((s) => ({ ...s, onboarded: true, guardianReviewAck: ack, planStartDate: s.planStartDate ?? today, poolLengthM: pool, sabbath: { ...s.sabbath, enabled: sabbath, fridayStart: fri, saturdayEnd: sat } }));
  };

  return (
    <main className="page" data-testid="onboarding">
      {step === 0 && (
        <div className="stack-lg">
          <div style={{ marginTop: 24 }}>
            <img src="./icons/icon-192.png" alt="" width={64} height={64} style={{ borderRadius: 14 }} />
            <h1 style={{ marginTop: 16 }}>Welcome to {settings.appName}</h1>
            <p className="muted" style={{ marginTop: 8 }}>
              Your training plan, meals, sleep, and recovery in one place. It works offline and keeps everything on this phone.
            </p>
          </div>
          <div className="group">
            <div className="item">
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>Private by design</span>
                <span className="item-sub" style={{ display: 'block' }}>No account, no ads, no tracking. Nothing leaves the phone unless you share it.</span>
              </span>
            </div>
            <div className="item">
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>Built around your week</span>
                <span className="item-sub" style={{ display: 'block' }}>Six training days, a full rest day, default meals you can log in one tap.</span>
              </span>
            </div>
            <div className="item">
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>Careful progress</span>
                <span className="item-sub" style={{ display: 'block' }}>Load goes up only when every set earns it. You confirm every change.</span>
              </span>
            </div>
          </div>
          <div className="stack">
            <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => setStep(1)} data-testid="onboard-start">
              Set up
            </button>
            <button type="button" className="btn btn-ghost btn-block" onClick={() => navigate('/more/data')}>
              Restore a backup or private setup file
            </button>
          </div>
        </div>
      )}

      {step === 1 && (
        <div className="stack-lg">
          <h1>Before you start</h1>
          <Note tone="accent" title="A quick word">
            Please go through the calorie targets, supplements, and any fast change in weight with a parent or guardian, and ideally a pediatrician or pediatric sports dietitian. PeakForm gives careful suggestions, but it is not medical advice.
          </Note>
          <div className="group">
            <Toggle checked={ack} onChange={setAck} label="I will review the plan with a parent" testId="onboard-ack" />
          </div>
          <div className="stack">
            <label className="field">
              <span className="label">First name, optional</span>
              <input className="input" value={name} onChange={(e) => setName(e.target.value)} maxLength={60} data-testid="onboard-name" />
            </label>
            <div className="grid-2">
              <Stepper label="Height" unit="cm" value={height} onChange={setHeight} max={250} base={170} />
              <Stepper label="Birth year" value={birthYear} onChange={setBirthYear} min={1990} max={2025} base={2012} />
            </div>
            <p className="small muted">Height and birth year are optional and stored only on this phone. Weight is logged in the morning check in.</p>
          </div>
          <div className="grid-2">
            <button type="button" className="btn btn-outline" onClick={() => setStep(0)}>
              Back
            </button>
            <button type="button" className="btn btn-primary" onClick={() => setStep(2)} data-testid="onboard-next">
              Next
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="stack-lg">
          <h1>Your week</h1>
          <div className="group">
            <Toggle checked={sabbath} onChange={setSabbath} label="Sabbath Mode" sub="Quiet reminders from Friday before sunset to Saturday night. Saturday stays a full rest day." testId="onboard-sabbath" />
          </div>
          {sabbath && (
            <div className="grid-2">
              <label className="field">
                <span className="label">Friday from</span>
                <input className="input" type="time" value={fri} onChange={(e) => setFri(e.target.value)} />
              </label>
              <label className="field">
                <span className="label">Saturday until</span>
                <input className="input" type="time" value={sat} onChange={(e) => setSat(e.target.value)} />
              </label>
            </div>
          )}
          <p className="small muted">You can also calculate the times for a city later in More, Sabbath Mode. No location is used.</p>
          <Stepper label="Pool length" unit="m" value={pool} onChange={setPool} max={100} placeholder="Not sure yet" base={25} />
          <div className="stack">
            <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => void finish(false)} data-testid="onboard-finish">
              Start with an empty log
            </button>
            <button type="button" className="btn btn-outline btn-block" onClick={() => void finish(true)} data-testid="onboard-demo">
              Start with two weeks of demo data
            </button>
            <p className="small muted">Demo data is made up and can be removed in More, Backup.</p>
          </div>
        </div>
      )}
    </main>
  );
}
