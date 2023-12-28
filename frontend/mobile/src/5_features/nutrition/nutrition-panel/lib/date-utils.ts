import {dateToISOWithoutTime, isTomorrowDate} from '../../../../7_shared/lib/date/lib/utils';
import {GET_LIMIT_TIME_TO_CANCEL_NUTRITION_FOR_TOMORROW} from '../config/config';

export function isAbleToCancelForDate(d: Date) {
  const expDate = GET_LIMIT_TIME_TO_CANCEL_NUTRITION_FOR_TOMORROW();
  const now = new Date(Date.now());

  if (isTomorrowDate(d)) {
    return now.valueOf() < expDate.valueOf();
  }

  return dateToISOWithoutTime(d) > dateToISOWithoutTime(now);
}
