import {Mealtime} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/mealtime.ts';
import {Pupil} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/pupil.ts';
import {TableRowViewData, TableViewData} from '../../../6_entities/meal-plan';
import {toNutritionStatusView} from '../../../5_features/nutrition-class-list-feature';

export function toTableViewData(schoolClassMealtimes?: Mealtime[]): TableViewData {
  return {
    hasBreakfast: schoolClassMealtimes?.includes(Mealtime.breakfast) ?? true,
    hasDinner: schoolClassMealtimes?.includes(Mealtime.dinner) ?? true,
    hasSnacks: schoolClassMealtimes?.includes(Mealtime.snacks) ?? true
  };
}

export function toTableRowViewDataArray(pupils?: Pupil[]): TableRowViewData[] {
  if (!pupils)
    return [];

  return pupils.map(item => {
    return {
      firstName: item.firstName,
      lastName: item.lastName,
      patronymic: item.patronymic,
      breakfast: item.mealtimes.includes(Mealtime.breakfast),
      dinner: item.mealtimes.includes(Mealtime.dinner),
      snacks: item.mealtimes.includes(Mealtime.snacks),
      status: item.nutrition
    };
  });
}
