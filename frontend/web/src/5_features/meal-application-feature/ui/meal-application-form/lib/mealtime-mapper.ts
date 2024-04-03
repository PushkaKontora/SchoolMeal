import {Mealtime} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/mealtime.ts';

export function booleansToMealtimeArray(booleans: {
  breakfast: boolean,
  dinner: boolean,
  snacks: boolean
}): Mealtime[] {
  const result: Mealtime[] = [];

  if (booleans.breakfast)
    result.push(Mealtime.breakfast);
  if (booleans.dinner)
    result.push(Mealtime.dinner);
  if (booleans.snacks)
    result.push(Mealtime.snacks);

  return result;
}
