import {MEAL_AMOUNT_BORDER_TO_SHOW} from '../config/config';
import {NutritionPlan} from '../../../7_shared/model/nutrition';

export function isFeeding(mealData: NutritionPlan) {
  return mealData.hasBreakfast ||
    mealData.hasDinner ||
    mealData.hasSnacks;
}

export function isEnoughMealAmountToShow(plan: NutritionPlan) {
  return getMealAmount(plan) >= MEAL_AMOUNT_BORDER_TO_SHOW;
}

export function getMealAmount(plan: NutritionPlan) {
  return Number(plan.hasBreakfast !== undefined) +
    Number(plan.hasDinner !== undefined) +
    Number(plan.hasSnacks !== undefined);
}
