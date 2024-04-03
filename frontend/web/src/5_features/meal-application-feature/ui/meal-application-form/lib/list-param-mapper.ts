import {MealApplicationFormStatus} from '../../../../../6_entities/meal-request/model/meal-application-form-status.ts';

export function isListEditable(status?: MealApplicationFormStatus) {
  return status != MealApplicationFormStatus.Applied;
}
