import {MealtimeOut} from './mealtime.ts';
import {PupilDeclarationOut, ResumedPupilOut} from './pupils.ts';
import {OkSchema} from '../universal/ok-schema.ts';

export type NutritionRequestStatusOut = 'submitted'
  | 'prefilled'

// GET requests

export type GetNutritionRequestParams = {
  class_id: string,
  on_date: string
}

export type NutritionRequestOut = {
  classId: string,
  onDate: string,
  status: NutritionRequestStatusOut,
  mealtimes: MealtimeOut[],
  pupils: PupilDeclarationOut[]
}

// POST requests

export type SubmitNutritionRequestBody = {
  classId: string,
  onDate: string,
  overrides: ResumedPupilOut[]
}

export type SubmitNutritionRequestResponse = OkSchema

// GET requests/prefill

export type PrefillNutritionRequestParams = GetNutritionRequestParams

export type PrefillNutritionRequestResponse = NutritionRequestOut
