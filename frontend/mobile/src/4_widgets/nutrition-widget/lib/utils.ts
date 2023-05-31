import {ChildMealData} from '../../../6_entities/child/types/child-meal-data';
import {MEAL_AMOUNT_BORDER_TO_SHOW} from '../config/config';

export function checkItem(array: boolean[], index: number, value: boolean) {
  return array.map((item, idx) => {
    return idx == index ? value : item;
  });
}

export function isFeeding(mealData: ChildMealData) {
  return mealData.breakfast ||
    mealData.lunch ||
    mealData.dinner;
}

export function isEnoughMealAmountToShow(mealAmount: number) {
  return mealAmount >= MEAL_AMOUNT_BORDER_TO_SHOW;
}
