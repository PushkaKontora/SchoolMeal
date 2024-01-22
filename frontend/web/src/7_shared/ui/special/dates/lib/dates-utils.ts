import { WEEKDAYS } from '../config/config';

export function getDayName(date: Date) {
  return WEEKDAYS[date.getDay()];
}
