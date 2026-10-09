import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { addDays, type DateKey } from '../domain/dates';
import { jumpDayAdvice } from '../domain/exposure';
import { Note } from './components';

/** Pain or short sleep advice on a day with home jumps (3.1.0). Shown only for today. */
export function JumpDayNote({ date }: { date: DateKey }) {
  const pain = useLiveQuery(() => db.pain.where('date').between(addDays(date, -1), date, true, true).toArray(), [date]);
  const sleep = useLiveQuery(() => db.sleep.where('date').equals(date).first(), [date]);
  if (!pain) return null;
  const advice = jumpDayAdvice(date, pain, sleep ?? null);
  if (!advice) return null;
  return (
    <div style={{ marginBottom: 12 }} data-testid="jump-day-advice">
      <Note tone={advice.level === 'skip' ? 'danger' : 'warn'} title={advice.title}>
        {advice.text}
      </Note>
    </div>
  );
}
