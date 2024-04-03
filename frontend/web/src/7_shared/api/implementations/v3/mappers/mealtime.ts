import {MealtimeOut} from '../backend-types/nutrition/mealtime.ts';
import {Mealtime} from '../frontend-types/nutrition/mealtime.ts';

export const toMealtime = (mealtime: MealtimeOut) => Mealtime[mealtime];

export const toMealtimeArray = (mealtimes: MealtimeOut[]) => mealtimes.map(toMealtime);
