import {OverriddenPupil, Pupil} from './pupil.ts';
import {Mealtime} from './mealtime.ts';

export enum NutritionRequestStatus {
  submitted = 'submitted',
  prefilled = 'prefilled'
}

// GET request

export type GetNutritionRequestParams = {
  classId: string,
  date: Date
}

export type NutritionRequest = {
  classId: string,
  date: Date,
  status: NutritionRequestStatus,
  mealtimes: Mealtime[],
  pupils: Pupil[]
}

// POST request

export type SubmitNutritionRequestBody = {
  classId: string,
  date: Date,
  overrides: OverriddenPupil[]
}
