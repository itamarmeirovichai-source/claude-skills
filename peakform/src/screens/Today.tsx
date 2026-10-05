import { useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { KV, kvGet, saveCheckIn, updateSettings } from '../db/repo';
import { useSettings, useTimer } from '../ui/state';
import { usePlan, useTargets, useToday } from '../ui/hooks';
import { Item, Note, Section, Sheet, Stepper, Toggle, useToast } from '../ui/components';
import { IconCheck, IconScale, IconTrain, IconEat, IconChevron } from '../ui/icons';
import { Link, navigate } from '../ui/router';
import { addDays, formatDateKey, minutesOf, reviewWeekStart, weekdayOf, WEEKDAY_NAMES } from '../domain/dates';
import { dayTarget, trainedOn } from '../domain/fuel';
import { buildTimeline, nextEntry, type TimelineEntry } from '../services/today';
import { logTemplate } from '../services/food';
import { readiness, safetyState } from '../domain/safety';
import { isSabbathAt } from '../domain/sabbath';
import { exerciseName } from '../content/library';
import { dayTotals } from '../domain/nutrition';
import { formatClock, remainingMs } from '../domain/timer';
import { summarizeSets } from '../ui/format';
import { PhaseNoticeCard, PlanUpdateCard } from './PlanUpdate';

export function TodayScreen() {
  const settings = useSettings();
  const today = useToday();
  const plan = usePlan();
  const toast = useToast();
  const { timer, now } = useTimer();
  const [weightOpen, setWeightOpen] = useState(false);
  const targets = useTargets();
  const wd = weekdayOf(today);
  const day = plan?.days.find((d) => d.weekday === wd);

  const data = useLiveQuery(async () => {
    const [food, sessions, checkins, sleep, pain, allCheckins, weekSessions, lastBackupAt, reviews, satFood, yesterdaySessions] = await Promise.all([
      db.foodLogs.where('date').equals(today).toArray(),
      db.sessions.where('date').equals(today).toArray(),
      db.checkins.where('date').equals(today).toArray(),
      db.sleep.where('date').equals(today).first(),
      db.pain.where('date').between(addDays(today, -6), today, true, true).toArray(),
      db.checkins.where('date').between(addDays(today, -6), today, true, true).toArray(),
      db.sessions.where('date').between(reviewWeekStart(today), today, true, true).toArray(),
      kvGet<number>(KV.lastBackupAt),
      db.weeklyReviews.where('weekStart').equals(reviewWeekStart(addDays(today, wd === 0 ? 0 : -7))).first(),
      db.foodLogs.where('date').equals(addDays(today, wd === 0 ? -1 : wd === 6 ? 0 : -99)).count(),
      db.sessions.where('date').equals(addDays(today, -1)).toArray(),
    ]);
    const active = await db.sessions.where('status').equals('active').first();
    const lastSame = day
      ? (await db.sessions.where('status').equals('done').toArray()).filter((s) => s.planWeekday === wd && s.session === 'main' && s.date < today).sort((a, b) => b.startedAt - a.startedAt)[0]
      : undefined;
    let lastSets: string[] = [];
    if (lastSame) {
      const sets = await db.setLogs.where('sessionId').equals(lastSame.id).toArray();
      const byEx = new Map<string, typeof sets>();
      for (const s of sets.filter((x) => !x.warmup && x.weightKg !== null)) byEx.set(s.exerciseId, [...(byEx.get(s.exerciseId) ?? []), s]);
      lastSets = [...byEx.entries()].slice(0, 3).map(([id, xs]) => `${exerciseName(id)}: ${summarizeSets(xs)}`);
    }
    return { food, sessions, checkins, sleep, pain, allCheckins, weekSessions, lastBackupAt: lastBackupAt ?? null, reviews, satFood, active, lastSame, lastSets, yesterdaySessions };
  }, [today, wd, day?.title]);

  if (!data || !plan) return null;
  const timeline = buildTimeline(today, settings, day, data.food, data.sessions, data.checkins);
  const nowMin = new Date().getHours() * 60 + new Date().getMinutes();
  const next = nextEntry(timeline, nowMin);
  const safety = safetyState(today, data.allCheckins, data.pain);
  const ready = readiness(today, data.checkins[0] ?? null, data.sleep ?? null, data.pain, safety);
  const inSabbath = isSabbathAt(Date.now(), today, settings.sabbath);
  const totals = dayTotals(data.food);
  const target = dayTarget(targets.find((t) => t.weekday === wd)!, trainedOn(data.sessions, today));
  // On Monday the review covers last week, which only counts if the plan had started by then.
  const reviewDue = (wd === 0 && nowMin >= minutesOf('20:00')) || (wd === 1 && !data.reviews && (!settings.planStartDate || settings.planStartDate < today));
  const yesterdayDay = plan.days.find((d) => d.weekday === weekdayOf(addDays(today, -1)));
  // Only when the plan was already running yesterday. A new install has nothing to catch up on.
  const planRanYesterday = !settings.planStartDate || settings.planStartDate <= addDays(today, -1);
  const missedYesterday = planRanYesterday && yesterdayDay && !yesterdayDay.isRest && yesterdayDay.items.some((i) => i.session === 'main') && !data.yesterdaySessions.some((s) => s.session === 'main' && s.status === 'done') && !data.sessions.some((s) => s.planWeekday === yesterdayDay.weekday);
  const todayMainDone = data.sessions.some((s) => s.session === 'main' && s.status === 'done');
  const backupDays = data.lastBackupAt ? Math.floor((Date.now() - data.lastBackupAt) / 86400000) : null;
  const checkinsThisWeek = data.allCheckins.length;
  const sessionsThisWeek = data.weekSessions.filter((s) => s.status === 'done').length;

  const act = async (e: TimelineEntry) => {
    if (e.kind === 'meal' && e.template) {
      await logTemplate(today, e.template);
      toast(`${e.label} logged as planned`);
    } else navigate(e.to);
  };

  return (
    <div data-testid="today">
      <header className="page-head" style={{ display: 'block' }}>
        <div className="eyebrow">{formatDateKey(today, { weekday: 'long', day: 'numeric', month: 'long' })}</div>
        <h1>{day ? (day.isRest ? 'Rest day' : day.title) : 'Today'}</h1>
        <span className={`tag ${data.checkins.length === 0 && !data.sleep ? '' : ready.level === 'ready' ? 'tag-accent' : ready.level === 'easier' ? 'tag-warn' : 'tag-danger'}`} style={{ marginTop: 8 }} data-testid="readiness">
          <span className="dot" aria-hidden="true" />
          {ready.label}
        </span>
      </header>

      <PhaseNoticeCard />
      <PlanUpdateCard />

      {!settings.guardianReviewAck && (
        <div style={{ marginBottom: 12 }}>
          <Note tone="accent" title="Worth a quick talk">
            Go through the calorie targets, supplements, and any fast weight change with a parent, and ideally a pediatrician or pediatric sports dietitian.
            <div style={{ marginTop: 8 }}>
              <button type="button" className="btn btn-sm btn-outline" onClick={() => void updateSettings({ guardianReviewAck: true })}>
                Got it
              </button>
            </div>
          </Note>
        </div>
      )}
      {safety.urgent && (
        <Note tone="danger" title="Tell a parent today">
          {safety.messages[0]}
        </Note>
      )}
      {!safety.urgent && safety.messages.length > 0 && (
        <Note tone="warn" title="Pause and check">
          {safety.messages.join(' ')}
        </Note>
      )}
      {inSabbath && (
        <Note tone="accent" title="Shabbat">
          Reminders are quiet until Saturday night. Nothing needs logging now.
        </Note>
      )}

      {timer && (
        <div className="note note-accent" style={{ marginTop: 12 }}>
          <strong>Rest timer running</strong>
          {formatClock(remainingMs(timer, now))} left for {timer.label}.
        </div>
      )}

      {/* 1. What do I do next? */}
      <Section title="Next">
        {data.active ? (
          <div className="panel stack">
            <div>
              <h2>{data.active.title}</h2>
              <p className="muted">Workout in progress, started {new Date(data.active.startedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}.</p>
            </div>
            <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => navigate(`/workout/${data.active!.id}`)} data-testid="resume-workout">
              Resume workout
            </button>
          </div>
        ) : next ? (
          <div className="panel stack" data-testid="next-card">
            <div className="row-between">
              <div className="grow">
                <div className="small muted num">{next.time}</div>
                <h2>{next.label}</h2>
                <p className="muted">{next.detail}</p>
              </div>
            </div>
            {next.kind === 'meal' && next.template ? (
              <div className="grid-2">
                <button type="button" className="btn btn-primary btn-large" onClick={() => void act(next)} data-testid="next-log-planned">
                  <IconCheck /> Log as planned
                </button>
                <Link to={next.to} className="btn btn-outline btn-large">
                  Change
                </Link>
              </div>
            ) : (
              <button type="button" className="btn btn-primary btn-large btn-block" onClick={() => void act(next)} data-testid="next-action">
                {next.kind === 'session' ? 'Start' : next.kind === 'checkin' ? 'Check in' : 'Open'}
              </button>
            )}
          </div>
        ) : (
          <div className="panel">
            <h2>All done for today</h2>
            <p className="muted">Everything planned for today is logged. Sleep is the next step.</p>
          </div>
        )}
      </Section>

      {/* 3. One tap logging */}
      <div className="grid-3" style={{ marginTop: 12 }}>
        <button type="button" className="btn btn-outline quick-btn" onClick={() => navigate('/train/start')} data-testid="quick-workout">
          <IconTrain />
          <span className="small">Start workout</span>
        </button>
        <button type="button" className="btn btn-outline quick-btn" onClick={() => navigate('/eat/log/other?mode=quick')} data-testid="quick-food">
          <IconEat />
          <span className="small">Log food</span>
        </button>
        <button type="button" className="btn btn-outline quick-btn" onClick={() => setWeightOpen(true)} data-testid="quick-weight">
          <IconScale />
          <span className="small">Log weight</span>
        </button>
      </div>

      {missedYesterday && !todayMainDone && !day?.isRest && (
        <Section title="Schedule changed">
          <div className="panel stack">
            <p>
              Yesterday's {yesterdayDay!.short} was not logged. You can do it today instead of {day?.short ?? "today's session"}, or let it go. PeakForm never stacks two sessions on one day.
            </p>
            <div className="grid-2">
              <Link className="btn btn-outline" to={`/train/day/${yesterdayDay!.weekday}?date=${today}`}>
                Do {yesterdayDay!.short} today
              </Link>
              <Link className="btn btn-ghost" to="/train">
                Keep today's plan
              </Link>
            </div>
          </div>
        </Section>
      )}

      {wd === 0 && data.satFood === 0 && (
        <Section title="Saturday">
          <Item title="Log the Sabbath meals" sub="Two taps with the plate guide. Honest ranges, no scale needed." to={`/eat/sabbath?date=${addDays(today, -1)}`} testId="log-sabbath" />
        </Section>
      )}

      {/* Timeline */}
      <Section title="Today's plan" end={<Link to={`/train/day/${wd}?date=${today}`}>Details</Link>}>
        <div className="group" data-testid="timeline">
          {timeline.map((e) => (
            <div className="item" key={e.id} style={{ opacity: e.quiet ? 0.55 : 1 }}>
              <span className="num small faint" style={{ width: 44, flex: '0 0 auto' }}>
                {e.time}
              </span>
              <span className="item-main">
                <span className="item-title" style={{ display: 'block' }}>
                  {e.label}
                </span>
                <span className="item-sub" style={{ display: 'block' }}>
                  {e.quiet ? 'Sabbath, quiet' : e.detail}
                </span>
              </span>
              {e.done ? (
                <span className="tag tag-accent">
                  <IconCheck size={14} /> Done
                </span>
              ) : e.kind === 'meal' && e.template && !e.quiet ? (
                <button type="button" className="btn btn-sm btn-outline" onClick={() => void act(e)} aria-label={`Log ${e.label} as planned`}>
                  Log
                </button>
              ) : e.kind !== 'sleep' && !e.quiet ? (
                <Link to={e.to} className="btn btn-sm btn-ghost" aria-label={`Open ${e.label}`}>
                  <IconChevron />
                </Link>
              ) : null}
            </div>
          ))}
        </div>
      </Section>

      {/* 2. What did I do last time? */}
      {day && !day.isRest && (
        <Section title="Last time">
          <div className="panel">
            {data.lastSame ? (
              <>
                <p>
                  <b>{WEEKDAY_NAMES[wd]} {formatDateKey(data.lastSame.date, { day: 'numeric', month: 'short' })}</b>, {data.lastSame.title}
                  {data.lastSame.sessionRpe !== null ? `, session effort ${data.lastSame.sessionRpe} of 10` : ''}.
                </p>
                {data.lastSets.length > 0 && (
                  <ul className="bullets small muted" style={{ marginTop: 6 }}>
                    {data.lastSets.map((l) => (
                      <li key={l}>{l}</li>
                    ))}
                  </ul>
                )}
              </>
            ) : (
              <p className="muted">No earlier {day.short} session yet. The first one sets your baseline.</p>
            )}
          </div>
        </Section>
      )}

      {/* 4. Safety and recovery */}
      <Section title="Recovery">
        <div className="group">
          <Item title={ready.label} sub={ready.reasons.join('. ')} />
          <Item
            title="Sleep"
            sub={data.sleep ? `${Math.floor(data.sleep.durationMin / 60)} h ${data.sleep.durationMin % 60} min, ${data.sleep.bedtime} to ${data.sleep.wakeTime}` : 'Not logged yet. Add it in the morning check in.'}
            end={data.sleep ? (data.sleep.durationMin >= 480 ? 'On target' : 'Under 8 h') : undefined}
          />
          <Item
            title="Food so far"
            sub={totals.mid.kcal > 0 ? `About ${Math.round(totals.low.kcal / 10) * 10} to ${Math.round(totals.high.kcal / 10) * 10} kcal, protein ${Math.round(totals.mid.protein)} g` : 'Nothing logged yet'}
            end={`Target ${target.kcal}${target.fuelKcal > 0 && !target.fuelIncluded ? ` + ${target.fuelKcal} if you train` : ''}`}
            to="/eat"
          />
        </div>
      </Section>

      <Section title="This week">
        <div className="group">
          {reviewDue && <Item title="Weekly review is ready" sub="Keep doing, ready to progress, improve, and safety" to="/review" testId="review-ready" />}
          <Item title="Actions this week" sub={`${checkinsThisWeek} check ins in the last 7 days, ${sessionsThisWeek} sessions since Monday`} to="/progress" />
          <Item
            title="Saved on this phone"
            sub={backupDays === null ? 'No backup yet. Export one to Files.' : `Last backup ${backupDays === 0 ? 'today' : `${backupDays} day${backupDays === 1 ? '' : 's'} ago`}`}
            to="/more/data"
            testId="backup-status"
          />
        </div>
      </Section>

      <QuickWeightSheet open={weightOpen} onClose={() => setWeightOpen(false)} date={today} />
    </div>
  );
}

function QuickWeightSheet({ open, onClose, date }: { open: boolean; onClose: () => void; date: string }) {
  const toast = useToast();
  const last = useLiveQuery(() => db.checkins.orderBy('at').reverse().filter((c) => c.weightKg !== null).first(), []);
  const [kg, setKg] = useState<number | null>(null);
  const [standard, setStandard] = useState(true);
  const value = kg;
  return (
    <Sheet open={open} onClose={onClose} title="Morning weight" testId="weight-sheet">
      <div className="stack">
        <Stepper label="Weight" unit="kg" value={value} onChange={setKg} step={0.1} decimals={1} min={20} max={300} base={last?.weightKg ?? null} placeholder="Type or tap + or −" prev={last?.weightKg ? `${last.weightKg}` : undefined} testId="weight-input" />
        <div className="group">
          <Toggle checked={standard} onChange={setStandard} label="After the toilet, before food or drink" sub="Only these count toward the weekly trend." />
        </div>
        <p className="small muted">One number means little. PeakForm shows a seven day average once there are four morning weights in a week.</p>
        <button
          type="button"
          className="btn btn-primary btn-large btn-block"
          disabled={value === null}
          data-testid="weight-save"
          onClick={async () => {
            await saveCheckIn({
              checkin: { date, at: Date.now(), weightKg: value, bodyFatPct: null, standardConditions: standard, energy: null, mood: null, concentration: null, hunger: null, soreness: {}, illness: false, illnessNote: '', hydrationNote: '', redFlags: [], note: '' },
              sleep: null,
              waist: null,
              pain: [],
            });
            toast('Weight saved');
            onClose();
          }}
        >
          Save weight
        </button>
      </div>
    </Sheet>
  );
}
