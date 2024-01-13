import {dateToISOWithoutTime, isTomorrowDate} from '../../../../7_shared/lib/date/lib/utils';
import {GET_LIMIT_TIME_TO_CANCEL_NUTRITION_FOR_TOMORROW} from '../config/config';
import moment from 'moment-timezone';
import {SERVER_TIMEZONE} from '../../../../7_shared/api/config';
import {CancellationPeriod} from '../../../../7_shared/model/nutrition';
import {DateInfo} from '../../../../7_shared/ui/special/mini-calendar';

export function isAbleToCancelForDate(d: Date) {
  const expDate = GET_LIMIT_TIME_TO_CANCEL_NUTRITION_FOR_TOMORROW();

  const now = moment(Date.now()).tz(SERVER_TIMEZONE);
  if (isTomorrowDate(d, SERVER_TIMEZONE)) {
    return now.valueOf() < expDate.valueOf();
  }

  return dateToISOWithoutTime(d) > now.format('YYYY-MM-DD');
}

export function generateCalendarDateInfo(periods: CancellationPeriod[]) {
  const result: DateInfo = {};

  for (const period of periods) {
    const date = new Date(period.startsAt);
    const endingDateObject = new Date(period.endsAt);
    let isoDate = dateToISOWithoutTime(date);

    while (date <= endingDateObject) {
      result[isoDate] = {
        cancelled: true
      };

      date.setDate(date.getDate() + 1);
      isoDate = dateToISOWithoutTime(date);
    }
  }

  return result;
}
