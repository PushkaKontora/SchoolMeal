import {NutritionRequestOut} from '../backend-types/nutrition/requests.ts';
import {NutritionRequest, NutritionRequestStatus} from '../frontend-types/nutrition/nutrition-request.ts';
import {pupilDeclarationsToPupilArray} from './pupil.ts';
import {toMealtimeArray} from './mealtime.ts';

export const toNutritionRequest = (responseData: NutritionRequestOut): NutritionRequest => ({
  classId: responseData.classId,
  date: new Date(responseData.onDate),
  status: NutritionRequestStatus[responseData.status],
  mealtimes: toMealtimeArray(responseData.mealtimes),
  pupils: pupilDeclarationsToPupilArray(responseData.pupils)
});

export const toNutritionRequestArray = (responseData: NutritionRequestOut[]) => responseData.map(toNutritionRequest);
