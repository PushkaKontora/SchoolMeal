import {
  NutritionRequestStatus
} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/nutrition-request.ts';
import {MealApplicationFormStatus} from '../../../5_features/meal-application-feature';

export const toMealApplicationFormStatus 
  = (status?: NutritionRequestStatus): MealApplicationFormStatus => {
    if (!status) {
      return MealApplicationFormStatus.NotApplied;
    }

    return {
      [NutritionRequestStatus.prefilled]: MealApplicationFormStatus.NotApplied,
      [NutritionRequestStatus.submitted]: MealApplicationFormStatus.Applied
    }[status];
  };
