import {Mealtime} from './mealtime.ts';
import {CancelledPeriod} from './cancelled-period.ts';
import {NutritionStatus} from './nutrition-status.ts';

export type GetPupilsParams = {
  classId?: string,
  parentId?: string
}

export type Pupil = {
  id: string,
  classId: string,
  parentIds: string[],
  firstName: string,
  lastName: string,
  patronymic?: string,
  mealtimes: Mealtime[],
  preferentialUntil?: Date,
  cancelledPeriods: CancelledPeriod[],
  nutrition: NutritionStatus
}

export type OverriddenPupil = Pick<Pupil, 'id' | 'mealtimes'>

export type PupilsResponse = Pupil[]
