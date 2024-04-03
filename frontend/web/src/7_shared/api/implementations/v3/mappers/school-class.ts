import {SchoolClassOut} from '../backend-types/nutrition/school-classes.ts';
import {SchoolClass} from '../frontend-types/nutrition/school-class.ts';
import {toMealtimeArray} from './mealtime.ts';

export const toSchoolClass = (schoolClass: SchoolClassOut): SchoolClass => ({
  id: schoolClass.id,
  teacherId: schoolClass.teacherId,
  number: schoolClass.number,
  literal: schoolClass.literal,
  mealtimes: toMealtimeArray(schoolClass.mealtimes)
});

export const toSchoolClassArray = (classes: SchoolClassOut[]) => classes.map(toSchoolClass);
