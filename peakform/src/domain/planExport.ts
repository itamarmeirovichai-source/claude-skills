import type { PlanRecord } from '../db/records';
import type { AthleteProfile } from './athlete';
import { openQuestions } from './athlete';
import { sessionInfo } from './sessionInfo';
import { doseText } from './planDiff';
import { exampleDayTotals, templateItems } from './nutrition';
import { contacts } from '../content/phases';
import { SESSION_LABELS, sessionsForDay } from '../content/plan';
import { exerciseName } from '../content/library';
import { EXAMPLE_NOTE, SLOT_LABELS, templateKosher, templatesForDay, type DayOptions } from '../content/meals';
import { FOOD_BY_ID } from '../content/foods';
import { WEEKDAY_NAMES } from './dates';

// The private plan export (3.0.0): the week with locations, equipment, space, duration, and stop
// rules, the example meals in grams, and the open questions. It is built on the phone and only
// leaves it when the athlete shares it.

export function planMarkdown(plan: PlanRecord, athlete: AthleteProfile, mealOpts: DayOptions, appName = 'PeakForm'): string {
  const out: string[] = [`# ${appName} plan`, '', `${plan.name}, version ${plan.version}. ${plan.changeNote}`, ''];
  out.push('This is a private export from the phone. It is a training log and plan, not medical advice.', '');
  for (const d of [...plan.days].sort((a, b) => a.weekday - b.weekday)) {
    out.push(`## ${WEEKDAY_NAMES[d.weekday]}: ${d.isRest ? d.title : d.title}`, '');
    if (d.isRest) {
      out.push(...(d.restNotes ?? []).map((n) => `- ${n}`), '');
      continue;
    }
    for (const s of sessionsForDay(d)) {
      const items = d.items.filter((i) => i.session === s);
      const info = sessionInfo(items, s);
      const n = contacts(items);
      out.push(`### ${SESSION_LABELS[s]} (${info.locationLabel}), about ${info.minutes} min${n ? `, about ${n} landings` : ''}`, '');
      out.push(`- Space: ${info.space}`, `- Equipment: ${info.equipment.join(', ') || 'none'}`, `- Stop rules: ${info.stopRules.join(' ')}`, '');
      items.forEach((i, k) => out.push(`${k + 1}. ${exerciseName(i.exerciseId)}: ${doseText(i)}, ${i.restSec} s rest${i.notes.length ? `. ${i.notes.join(' ')}` : ''}`));
      out.push('');
    }
  }
  out.push('## Rules for every session', '', ...plan.globalRules.map((r) => `- ${r}`), '');
  out.push('## Example meals, Monday', '', EXAMPLE_NOTE, '');
  const day = templatesForDay(1, undefined, mealOpts);
  for (const t of day) {
    out.push(`### ${SLOT_LABELS[t.slot]}, ${mealOpts.times?.[t.slot] ?? t.time} (${templateKosher(t)})`, '');
    for (const i of t.items) {
      const f = FOOD_BY_ID[i.foodId];
      out.push(`- ${i.grams} ${f?.liquid ? 'ml' : 'g'} ${f?.name ?? i.foodId}${i.household ? ` (${i.household})` : ''}${i.optional ? ', optional' : ''}`);
    }
    const kcal = templateItems(t).reduce((a, x) => a + x.mid.kcal, 0);
    out.push(`- About ${Math.round(kcal / 10) * 10} kcal, estimated.`, `- More food when hungry: ${t.more.join('; ')}.`, '');
  }
  out.push(`The Monday examples add up to about ${Math.round(exampleDayTotals(day).mid.kcal / 50) * 50} kcal. That is a description of the examples, not a requirement or a limit.`, '');
  out.push('## Aspirations and reviewed targets', '');
  out.push('Aspirations, in the athlete\'s words:', ...(athlete.aspirations.length ? athlete.aspirations.map((a) => `- ${a.text}`) : ['- None recorded.']), '');
  out.push('Targets reviewed by a professional:', ...(athlete.reviewed.length ? athlete.reviewed.map((r) => `- ${r.value} ${r.units}, ${r.source} (${r.role}), ${r.date}, ${r.status}`) : ['- None recorded.']), '');
  const q = openQuestions(athlete, { creatineActive: athlete.supplements.creatineProduct !== '' });
  if (q.length) out.push('## Still to confirm', '', ...q.map((x) => `- ${x.title}: ${x.why}`), '');
  return out.join('\n');
}
