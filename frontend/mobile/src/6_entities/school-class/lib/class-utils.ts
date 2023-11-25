import {SchoolClass} from '../model/school-class';

export function getMealAmount(c: SchoolClass) {
  return Number(c.hasBreakfast) +
    Number(c.hasLunch) +
    Number(c.hasDinner);
}
