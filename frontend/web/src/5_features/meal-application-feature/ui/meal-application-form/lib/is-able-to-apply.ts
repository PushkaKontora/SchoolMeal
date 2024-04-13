import {MealApplicationDeadline} from '../const/meal-application-deadline.ts';
import {equalsDates} from '../../../../../7_shared/lib/date/lib/utils.ts';

export function isAbleToApply(date: Date) {
  const now = new Date();

  if (equalsDates(date, now)) {
    return now <= MealApplicationDeadline();
  }

  return date > now;
}
