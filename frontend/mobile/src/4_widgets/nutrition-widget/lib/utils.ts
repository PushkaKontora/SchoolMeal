import {MEAL_AMOUNT_BORDER_TO_SHOW} from '../config/config';
import {NutritionPlan} from '../../../7_shared/model/nutrition';
import {SchoolClass} from '../../../6_entities/school-class/model/school-class';

export function checkItem(array: boolean[], index: number, value: boolean) {
  return array.map((item, idx) => {
    return idx == index ? value : item;
  });
}

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
