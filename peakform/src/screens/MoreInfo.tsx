import { useEffect, useState } from 'react';
import QRCode from 'qrcode';
import { MEDIA, CLAIM_REVIEWS } from '../content/media';
import { SOURCES } from '../content/sources';
import { exerciseName } from '../content/library';
import { RECIPE_BY_ID } from '../content/recipes';
import { Item, Note, PageHead, Section } from '../ui/components';
import { useSettings } from '../ui/state';
import { updateSettings } from '../db/repo';
import { isStandalone } from '../lib/device';
import { APP_VERSION } from '../services/exporter';

export function AttributionScreen() {
  return (
    <div data-testid="attribution">
      <PageHead title="Media attribution" backTo="/more" />
      <Section title="Original artwork">
        <p className="small">
          The body map, exercise keyframe figures, drill diagrams, portion icons, app icon, and interface icons were drawn for PeakForm as original SVG code. They are not traced from or based on third party images. Source files live in the project under src/svg, src/ui/icons.tsx, and public/icons.
        </p>
      </Section>
      <Section title="Linked videos">
        <p className="small muted" style={{ marginBottom: 8 }}>
          PeakForm links to or embeds these videos with YouTube's official player, only after you tap. Nothing is downloaded or rehosted. Each was matched by title and channel from search results and was not watched frame by frame, so you can confirm or reject it on the exercise page.
        </p>
        <div className="group">
          {MEDIA.map((m) => (
            <a key={m.id} className="item" href={m.url} target="_blank" rel="noopener noreferrer">
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>{m.title}</span>
                <span className="item-sub" style={{ display: 'block' }}>
                  {m.channel}. For {m.targetType === 'exercise' ? exerciseName(m.targetId) : (RECIPE_BY_ID[m.targetId]?.name ?? m.targetId)}. Checked {m.verifiedOn}.
                </span>
              </span>
            </a>
          ))}
        </div>
      </Section>
      <Section title="Food data">
        <p className="small">Built in food values are rounded approximations of common reference data. Optional barcode lookups use Open Food Facts, a community database under the Open Database License.</p>
      </Section>
    </div>
  );
}

export function SourcesScreen() {
  const topics = [...new Set(SOURCES.map((s) => s.topic))];
  return (
    <div data-testid="sources">
      <PageHead title="Research sources" backTo="/more" />
      <Note tone="warn">These notes come from search results because the build environment could not open the pages themselves. Each entry says how it was accessed. Recheck important figures against the live source.</Note>
      {topics.map((t) => (
        <Section key={t} title={t.replace('-', ' ')}>
          <div className="stack">
            {SOURCES.filter((s) => s.topic === t).map((s) => (
              <details className="disclosure panel" key={s.id}>
                <summary>
                  <span className="grow" style={{ fontWeight: 560 }}>{s.title}</span>
                </summary>
                <div className="small stack">
                  <p className="muted">
                    {s.publisher}, {s.published}. Accessed as {s.access.replace('-', ' ')} on {s.reviewedOn}.
                  </p>
                  <p>
                    <b>Conclusion.</b> {s.conclusion}
                  </p>
                  <p>
                    <b>What PeakForm does.</b> {s.productDecision}
                  </p>
                  <p className="muted">
                    <b>Uncertainty.</b> {s.uncertainty}
                  </p>
                  <a href={s.url} target="_blank" rel="noopener noreferrer">
                    Open source
                  </a>
                </div>
              </details>
            ))}
          </div>
        </Section>
      ))}
      <Section title="Social media claims">
        <div className="stack">
          {CLAIM_REVIEWS.map((c) => (
            <div className="panel small stack" key={c.id}>
              <a href={c.url} target="_blank" rel="noopener noreferrer">
                {c.url}
              </a>
              <p>
                <b>Claimed.</b> {c.claimed}
              </p>
              <p>
                <b>Verdict.</b> {c.verdict}
              </p>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}

export function PrivacyScreen() {
  return (
    <div data-testid="privacy">
      <PageHead title="Privacy" backTo="/more" />
      <div className="stack">
        <Section title="What stays on this phone">
          <p>Your profile, measurements, workouts, meals, photos, notes, and reviews are stored only in this browser's storage on this phone. The website that delivers PeakForm contains no personal data and receives none.</p>
        </Section>
        <Section title="What PeakForm never does">
          <ul className="bullets">
            <li>No account, no cloud sync, no advertising, no analytics, no tracking, and no third party error reporting.</li>
            <li>No automatic sharing. No assistant, including Codex or Claude, can read this phone's data.</li>
            <li>No personal data in the offline cache beyond what the app needs to open.</li>
          </ul>
        </Section>
        <Section title="When the internet is used">
          <ul className="bullets">
            <li>Loading or updating the app itself.</li>
            <li>A video, only after you tap Play. It loads from youtube-nocookie.com, and YouTube may then set cookies.</li>
            <li>A barcode lookup, only after you tap Look up. Only the barcode number goes to Open Food Facts.</li>
            <li>Links you choose to open.</li>
          </ul>
        </Section>
        <Section title="Sharing">
          <p>Backups, reports, calendars, and spreadsheets leave the phone only when you share or save them. Coach reports leave out photos and private notes unless you switch them on. Encrypted backups use a passphrase that only you know.</p>
        </Section>
        <Section title="App lock">
          <p>The optional PIN hides PeakForm from casual access. It is not encryption. Your iPhone passcode and device encryption protect the stored data.</p>
        </Section>
      </div>
    </div>
  );
}

export function SafetyScreen() {
  return (
    <div data-testid="safety">
      <PageHead title="Safety" backTo="/more" />
      <div className="stack">
        <Note tone="accent" title="For a parent and a clinician to review">
          PeakForm is a log and a coach's notebook, not medical care. Please review how much to eat, supplements, body goals, the wrist, and any fast change in weight with a parent or guardian and a pediatrician or pediatric sports dietitian.
        </Note>
        <Section title="Get help now">
          <p>Stop training, tell a parent, and get medical help for fainting, chest pain, shortness of breath outside normal exercise, severe dizziness, dark urine, an injury that keeps getting worse, repeated illness, or eating far less than planned. PeakForm pauses progression advice when you record any of these.</p>
        </Section>
        <Section title="Soreness, pain, and injury">
          <ul className="bullets">
            <li>Muscle soreness after training usually peaks one to three days later and fades. It is common, and it does not prove that a muscle grew.</li>
            <li>Pain in a joint or a tendon, pain at the heel, below the kneecap, or on the bump below the knee, pain in the wrist, pain at night, swelling, or pain in one exact spot on a bone is different. It pauses the exercises that load that area. Tell a parent and see a clinician if it lasts.</li>
            <li>Pain of 4 out of 10 or more, pain that is getting worse, or pain that changes your technique pauses that exercise. Tell a parent, coach, or clinician. Pain tracking is not a diagnosis.</li>
            <li>Very dark urine with severe muscle pain or weakness after training needs medical help the same day.</li>
            <li>Massage, supplements, or a lighter week never replace having an injury checked.</li>
          </ul>
        </Section>
        <Section title="Wrist after an injury">
          <p>Return to full sport after a forearm or wrist injury, such as a fracture, depends on the type of injury and on healing, so the clinician who treated it decides. Until clearance is recorded in More, Your profile, loads on gripping and pressing exercises stay the same, heavy grip exercises are swapped, and there is no ball contact, falling onto the hands, or push ups on the hands. Stop any exercise that hurts the wrist.</p>
        </Section>
        <Section title="Training">
          <ul className="bullets">
            <li>Gym sessions are for strength. Jumps, landings, footwork, and volleyball skills are at home, only in a space that allows them.</li>
            <li>Work sets stop about two reps short of failure, three while you learn an exercise. No routine sets to failure, no grinding, and no one repetition maximum tests.</li>
            <li>The weight goes up only when every work set reaches the top of its range with good form, the planned reps in reserve, and no pain.</li>
            <li>Jump volume never increases automatically. A new jump level is chosen after a review of pain, landings, school jumping, and sleep.</li>
            <li>Count every landing, including school and club volleyball and basketball. After a day with a lot of jumping, keep the home jumps short or skip them.</li>
            <li>Step down from boxes. Depth jumps are not in the plan.</li>
            <li>Warm up sets never count as work sets.</li>
            <li>Sleep 8 to 10 hours. Training is never planned at the cost of sleep, so there are no early morning sessions.</li>
            <li>Ask a gym instructor or a qualified coach to check your technique on anything new.</li>
          </ul>
        </Section>
        <Section title="Food">
          <ul className="bullets">
            <li>Meals are example servings. They are not a daily limit, and food never has to be earned with exercise.</li>
            <li>PeakForm sets no calorie target and never suggests eating less. Targets for a growing athlete come from a parent together with a pediatrician or pediatric sports dietitian.</li>
            <li>No meal skipping, fasting, water cutting, carbohydrate elimination, or exercise to make up for food.</li>
            <li>If weight drops faster than about 0.45 kg a week, or energy, concentration, sleep, mood, or recovery drop, eat more and talk with a parent.</li>
            <li>A steady weight does not prove that you eat enough. Growth, water, and training all move the scale.</li>
            <li>PeakForm never starts or increases a supplement. Review creatine and any other supplement with a parent and a clinician.</li>
            <li>No weight, body fat, muscle, jump, or date based result is promised. Averages from studies are not predictions for one person.</li>
          </ul>
        </Section>
        <Section title="Body measurements">
          <p>PeakForm does not use adult BMI categories. For a teenager, BMI needs age and sex specific growth charts read by a professional. Comparable performance, recovery, sleep, wellbeing, and a professional assessment are more useful here, with weight and waist trends over weeks if you choose to track them. Smart scale body fat and muscle figures are uncertain estimates, not measurements of fat or skeletal muscle.</p>
        </Section>
      </div>
    </div>
  );
}

type CheckState = 'idle' | 'checking' | 'latest' | 'ready' | 'offline' | 'failed' | 'unavailable';

const CHECK_TEXT: Record<CheckState, string> = {
  idle: 'PeakForm also checks by itself each time it opens or comes back to the screen.',
  checking: 'Checking…',
  latest: 'You have the latest version.',
  ready: 'A new version is ready.',
  offline: 'You are offline. Connect to the internet and try again.',
  failed: 'Could not reach the PeakForm site. If it asks for the password again, sign in, then try again.',
  unavailable: 'Updates are not available in this browser view.',
};

async function installed(sw: ServiceWorker | null): Promise<void> {
  if (!sw) return;
  await new Promise<void>((done) => {
    const settle = () => {
      if (sw.state !== 'installing') done();
    };
    sw.addEventListener('statechange', settle);
    settle();
  });
}

/** Asks the site for a new version right now, and applies it when one is waiting. */
function UpdateCheck() {
  const [state, setState] = useState<CheckState>('idle');
  const check = async () => {
    if (!('serviceWorker' in navigator)) return setState('unavailable');
    if (!navigator.onLine) return setState('offline');
    setState('checking');
    const r = await navigator.serviceWorker.getRegistration();
    if (!r) return setState('unavailable');
    try {
      await r.update();
    } catch {
      return setState('failed');
    }
    await installed(r.installing);
    setState(r.waiting ? 'ready' : 'latest');
  };
  const apply = async () => {
    const r = await navigator.serviceWorker.getRegistration();
    if (!r?.waiting) return setState('latest');
    navigator.serviceWorker.addEventListener('controllerchange', () => window.location.reload(), { once: true });
    r.waiting.postMessage({ type: 'SKIP_WAITING' });
  };
  return (
    <Section title="Updates">
      <div className="panel stack">
        <p className="small" role="status" data-testid="update-status">
          {CHECK_TEXT[state]}
        </p>
        <div className="row wrap">
          {state === 'ready' ? (
            <button type="button" className="btn btn-primary" onClick={() => void apply()} data-testid="update-apply">
              Update now
            </button>
          ) : (
            <button type="button" className="btn" disabled={state === 'checking'} onClick={() => void check()} data-testid="update-check">
              Check for updates
            </button>
          )}
        </div>
      </div>
    </Section>
  );
}

export function AboutScreen() {
  const s = useSettings();
  const [qr, setQr] = useState('');
  const url = s.deploymentUrl || (typeof window !== 'undefined' ? window.location.href.split('#')[0]! : '');
  useEffect(() => {
    if (!url) return;
    void QRCode.toString(url, { type: 'svg', margin: 1, errorCorrectionLevel: 'M', color: { dark: '#1b1f23', light: '#ffffff' } }).then(setQr);
  }, [url]);
  return (
    <div data-testid="about">
      <PageHead title="About" backTo="/more" />
      <div className="group">
        <Item title={s.appName} end={`Version ${APP_VERSION}`} testId="app-version" />
        <Item title="Built" end={typeof __BUILD_DATE__ === 'string' ? __BUILD_DATE__ : 'dev'} />
        <Item title="Installed from Home Screen" end={isStandalone() ? 'Yes' : 'No'} />
      </div>
      <UpdateCheck />
      <Section title="Install address">
        <div className="panel stack">
          <input className="input" value={s.deploymentUrl} placeholder={url} onChange={(e) => void updateSettings({ deploymentUrl: e.target.value.trim() })} aria-label="Install address" />
          <p className="small muted">Scan this code with another phone's camera to open PeakForm. The address contains no personal data.</p>
          {qr && <div style={{ width: 200, background: '#fff', padding: 8, borderRadius: 8 }} role="img" aria-label={`QR code for ${url}`} dangerouslySetInnerHTML={{ __html: qr }} />}
        </div>
      </Section>
      <Section title="Why PeakForm is a web app">
        <p className="small">A Home Screen web app installs for free, works offline, and never expires. A native app signed with a free Apple account would need reinstalling every week. The trade off is honest: web apps on iPhone cannot run a timer alert while closed without a push server, so reminders use Apple Calendar instead.</p>
      </Section>
    </div>
  );
}

export function InstallScreen() {
  return (
    <div data-testid="install">
      <PageHead title="Install on iPhone" backTo="/more" />
      <ol className="steps">
        <li>Open PeakForm's address in Safari.</li>
        <li>Tap the Share button.</li>
        <li>Tap Add to Home Screen, then Add.</li>
        <li>Open PeakForm from the Home Screen icon.</li>
        <li>Finish setup or import your private setup file.</li>
        <li>Choose reminder times in More, Schedule.</li>
        <li>Export the calendar and tap Add All.</li>
        <li>Create your first backup in More, Backup.</li>
      </ol>
      <p className="small muted" style={{ marginTop: 12 }}>Notifications are not used, because a closed web app cannot alert reliably without a push server. Apple Calendar handles alarms instead.</p>
    </div>
  );
}
