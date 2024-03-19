import {RequestPlanReport} from '../../../7_shared/model/request-report.ts';
import {Pupil} from '../../../7_shared/model/pupil.ts';
import {HeaderViewData, MealRequestRowViewData} from '../../../6_entities/meal-request';
import {isDateInAnyPeriods} from '../../../7_shared/lib/date-periods';
import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import {Menu} from '../../../7_shared/model/menu.ts';
import {SchoolClasses} from '../../../6_entities/nutrition/model/schoolClasses.ts';

export function combineTableData(
  date: Date,
  planningReport?: RequestPlanReport,
  pupils?: Pupil[]
): MealRequestRowViewData[] {
  if (!planningReport || !pupils) {
    return [];
  }

  const pupilMap: {[key: string]: Pupil} = {};

  pupils?.forEach((value) => {
    pupilMap[value.id] = value;
  });

  return planningReport?.pupils.map((value) => ({
    firstName: value.first_name,
    lastName: value.last_name,
    patronymic: value.patronymic,
    breakfast: value.breakfast,
    dinner: value.dinner,
    snacks: value.snacks,
    cancelledMeal: isDateInAnyPeriods(dateToISOWithoutTime(date),
      pupilMap[value.id].cancellationPeriods
        .map((value) => [value.startsAt, value.endsAt])),
    balance: Number((400 * Math.random() - 200).toFixed(2))
  }));
}

export function createHeaders(menu?: Menu): HeaderViewData {
  return {
    prices: {
      breakfast: Number(menu?.breakfast.cost),
      dinner: Number(menu?.dinner.cost),
      snacks: Number(menu?.dinner.cost)
    }
  };
}

export function createClassNames(classes?: SchoolClasses[]) {
  if (!classes) {
    return [];
  }

  return classes?.map(classObject =>
    `${classObject.initials.number}${classObject.initials.literal}`);
}