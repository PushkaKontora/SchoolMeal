import {MealtimeOut} from './mealtime.ts';
import {CancelledPeriodOut} from './cancelled-period.ts';
import {NutritionStatusOut} from './nutrition-status-out.ts';

export type GetPupilsParams = {
  class_id?: string,
  parent_id?: string
}

export type PupilOut = {
  id: string,
  classId: string,
  parentIds: string[],
  firstName: string,
  lastName: string,
  patronymic?: string,
  mealtimes: MealtimeOut[],
  preferentialUntil?: string,
  cancelledPeriods: CancelledPeriodOut[],
  nutrition: NutritionStatusOut
}

export type ResumedPupilOut = {
  id: string,
  mealtimes: MealtimeOut[]
}
