import {MealRequestRowViewData} from '../model/meal-request-row-view-data.ts';
import {HeaderViewData} from '../model/header-view-data.ts';

export const getFullName = (row: MealRequestRowViewData) => {
  return `${row.firstName || ''} ${row.lastName || ''} ${row.patronymic || ''}`;
};

export const getTotalCost = (row: MealRequestRowViewData, headerData: HeaderViewData) => {
  let result = 0;

  if (row.breakfast) {
    result += headerData.prices.breakfast;
  }

  if (row.dinner) {
    result += headerData.prices.dinner;
  }

  if (row.snacks) {
    result += headerData.prices.snacks;
  }

  return result;
};
