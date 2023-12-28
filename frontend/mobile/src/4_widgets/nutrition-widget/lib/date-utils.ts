import {dateToISOWithoutTime} from '../../../7_shared/lib/date';

export function dateToString(date: Date) {
  return dateToISOWithoutTime(date);
}
