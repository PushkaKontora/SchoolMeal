import {PupilOut} from '../backend-types/nutrition/pupils.ts';
import {Pupil} from '../frontend-types/nutrition/pupil.ts';
import {toPeriodArray} from './period.ts';
import {toMealtimeArray} from './mealtime.ts';
import {NutritionStatus} from '../frontend-types/nutrition/nutrition-status.ts';

export const toPupil = (pupil: PupilOut): Pupil => ({
  id: pupil.id,
  classId: pupil.classId,
  firstName: pupil.firstName,
  lastName: pupil.lastName,
  patronymic: pupil.patronymic,
  parentIds: pupil.parentIds,
  cancelledPeriods: toPeriodArray(pupil.cancelledPeriods),
  mealtimes: toMealtimeArray(pupil.mealtimes),
  preferentialUntil: pupil.preferentialUntil ? new Date(pupil.preferentialUntil) : undefined,
  nutrition: NutritionStatus[pupil.nutrition]
});

export const toPupilArray = (pupils: PupilOut[]): Pupil[] => pupils.map(toPupil);
