import {ChildMealData} from '../../../6_entities/child/types/child-meal-data';

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
