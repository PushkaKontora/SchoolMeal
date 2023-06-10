import {CancelMealPeriods} from '../../../../7_shared/model/cancelMealPeriods';
import {setHoursTillAbleToCancel} from '../config/config';

export function equalsDates(d1: Date, d2: Date) {
  return d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate();
}

export function findPeriodIdByDate(periods: CancelMealPeriods[], date: Date)
  : CancelMealPeriods | undefined {
  return periods
    .filter((item) => equalsDates(date, new Date(item.startDate)))[0];
}

export function isDateExpired(d: Date) {
  const expDate = setHoursTillAbleToCancel();
  return d.valueOf() < expDate.valueOf();
}
