import { SHORT_MONTHS } from '../config/config';

export function getMonthShortName(date: Date) {
  return SHORT_MONTHS[date.getMonth()];
}
