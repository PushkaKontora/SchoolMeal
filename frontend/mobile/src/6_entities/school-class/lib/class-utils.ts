import {Class} from '../model/class';

export function getMealAmount(c: Class) {
  return Number(c.hasBreakfast) +
    Number(c.hasLunch) +
    Number(c.hasDinner);
}
