import {CancelMealPeriods} from '../../../../7_shared/model/cancelMealPeriods';
import {equalsDates} from '../../../../7_shared/lib/date/lib/utils';
import {CancellationPeriod} from '../../../../7_shared/model/nutrition';

export function findPeriodIdByDate(periods: CancelMealPeriods[], date: Date)
  : CancelMealPeriods | undefined {
  return periods
    .filter((item) => equalsDates(date, new Date(item.startDate)))[0];
}

export function isDateInPeriod(date: string, startingDate: string, endingDate: string) {
  return date >= startingDate && date <= endingDate;
}

export function isNutritionCancelled(date: string, periods: CancellationPeriod[]) {
  for (const period of periods) {
    if (isDateInPeriod(date, period.startsAt, period.endsAt)) {
      return true;
    }
  }

  return false;
}
