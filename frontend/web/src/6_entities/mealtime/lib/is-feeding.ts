import {Mealtime} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/mealtime.ts';

export function isFeeding(mealtimes: Mealtime[]) {
  return mealtimes.includes(Mealtime.breakfast)
    || mealtimes.includes(Mealtime.dinner)
    || mealtimes.includes(Mealtime.snacks);
}
