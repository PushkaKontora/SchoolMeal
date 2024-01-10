import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import moment from 'moment-timezone';
import {isAbleToCancelForDate} from '../../../5_features/nutrition/nutrition-panel';
import {SERVER_TIMEZONE} from '../../../7_shared/api/config';

export function dateToString(date: Date) {
  return dateToISOWithoutTime(date);
}

export function getLastAbleDateToCancelNutrition() {
  const tomorrow = moment().tz(SERVER_TIMEZONE).add(1, 'days');
  if (!isAbleToCancelForDate(tomorrow.toDate())) {
    return tomorrow.toDate();
  }

  return tomorrow.subtract(1, 'days').toDate();
}
