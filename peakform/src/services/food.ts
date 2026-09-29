import { addFoodLog, KV, kvGet } from '../db/repo';
import type { FoodLog, FoodLogItem } from '../db/records';
import type { MealTemplate } from '../content/meals';
import { templateItems } from '../domain/nutrition';
import type { DateKey } from '../domain/dates';

export async function optionalFoodsOn(): Promise<Record<string, boolean>> {
  return (await kvGet<Record<string, boolean>>(KV.optionalFoods)) ?? {};
}

/** One tap logging of a default meal exactly as planned. */
export async function logTemplate(date: DateKey, tpl: MealTemplate, time?: string): Promise<FoodLog> {
  const on = await optionalFoodsOn();
  return addFoodLog({
    date,
    slot: tpl.slot,
    time: time ?? tpl.time,
    source: 'template',
    templateId: tpl.id,
    asPlanned: true,
    items: templateItems(tpl, on),
    photoId: null,
    note: '',
    hiddenOil: null,
  });
}

export async function logItems(date: DateKey, slot: FoodLog['slot'], items: FoodLogItem[], opts: Partial<Pick<FoodLog, 'source' | 'templateId' | 'asPlanned' | 'photoId' | 'note' | 'hiddenOil' | 'time'>> = {}): Promise<FoodLog> {
  const now = new Date();
  return addFoodLog({
    date,
    slot,
    time: opts.time ?? `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`,
    source: opts.source ?? 'manual',
    templateId: opts.templateId ?? null,
    asPlanned: opts.asPlanned ?? false,
    items,
    photoId: opts.photoId ?? null,
    note: opts.note ?? '',
    hiddenOil: opts.hiddenOil ?? null,
  });
}
