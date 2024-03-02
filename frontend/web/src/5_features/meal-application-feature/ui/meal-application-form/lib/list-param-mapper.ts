import {MealRequestStatus} from '../../../../../7_shared/model/meal-request-status.ts';

export function isListEditable(status?: MealRequestStatus) {
  return status != MealRequestStatus.Applied;
}
