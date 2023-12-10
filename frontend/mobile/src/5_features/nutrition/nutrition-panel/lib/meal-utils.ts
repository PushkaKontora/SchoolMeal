import {CancelMealPeriods} from '../../../../7_shared/model/cancelMealPeriods';
import {equalsDates} from '../../../../7_shared/lib/date/lib/utils';

export function findPeriodIdByDate(periods: CancelMealPeriods[], date: Date)
  : CancelMealPeriods | undefined {
  return periods
    .filter((item) => equalsDates(date, new Date(item.startDate)))[0];
}

export function isTodayDate(d: Date) {
  const today = new Date(Date.now());
  return d.getFullYear() === today.getFullYear() &&
    d.getMonth() === today.getMonth() &&
    d.getDate() === today.getDate();
}

export function isDateExpired(d: Date) {
  const expDate = setHoursTillAbleToCancel();

  if (isTodayDate(d)) {
    const now = new Date(Date.now());
    return now.valueOf() >= expDate.valueOf();
  }

  return d.valueOf() < expDate.valueOf();
}

export function setHoursTillAbleToCancel() {
  const now = new Date(Date.now());
  now.setHours(10, 0, 0, 0);
  return now;
}
