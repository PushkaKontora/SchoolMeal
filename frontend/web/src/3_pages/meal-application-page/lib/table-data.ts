import {MealRequestRowViewData} from '../../../6_entities/meal-request';
import {NutritionRequest} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/nutrition-request.ts';
import {Pupil} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/pupil.ts';
import {Mealtime} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/mealtime.ts';
import {isDateInAnyPeriods} from '../../../7_shared/lib/date-periods';

export function combineTableData(
  nutritionRequest?: NutritionRequest
) : MealRequestRowViewData[] {
  if (!nutritionRequest) {
    return [];
  }

  const pupilMap: {[key: string]: Pupil} = {};

  nutritionRequest.pupils.forEach((pupil) => {
    pupilMap[pupil.id] = pupil;
  });

  return nutritionRequest.pupils.map(pupil => ({
    firstName: pupil.firstName,
    lastName: pupil.lastName,
    patronymic: pupil.patronymic,
    breakfast: pupil.mealtimes.includes(Mealtime.breakfast),
    dinner: pupil.mealtimes.includes(Mealtime.dinner),
    snacks: pupil.mealtimes.includes(Mealtime.snacks),
    cancelledMeal: isDateInAnyPeriods(nutritionRequest.date,
      pupil.cancelledPeriods.map(period => [period.start, period.end])),
    balance: Number((400 * Math.random() - 200).toFixed(2)) // random placeholder
  }));
}


