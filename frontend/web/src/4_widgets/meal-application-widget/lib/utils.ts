import {Meal} from '../../../6_entities/meals/model/meal';
import {MealRowData} from '../types/meal-row-data';
import {Class} from '../../../6_entities/meals/model/class-view';
import {Pupil} from '../../../6_entities/meals/model/pupil-view';
import {MealCellData} from '../../../5_features/meals/meal-info-table/types';
import {MealRowValue} from '../types/meal-row-value';
import {RequestReport} from '../../../6_entities/requests/api/types.ts';

export function schoolClassToString(schoolClass: Class) {
  return `${schoolClass.number}${schoolClass.letter}`;
}

export function isRequiredClass(item: Meal, schoolClass: Class) {
  return item.schoolClass.id === schoolClass.id;
}

export function transformRequestReport(report: RequestReport): MealRowData {
  const result: MealRowData = {};

  for (let schoolClass of report.school_classes) {
    result[schoolClass.initials] = {
      breakfast: {
        ...schoolClass.breakfast,
        sum: schoolClass.breakfast.total
      },
      dinner: {
        ...schoolClass.dinner,
        sum: schoolClass.dinner.total
      },
      snacks: {
        ...schoolClass.snacks,
        sum: schoolClass.snacks.total
      }
    };
  }

  return result;
}

export function sortMealsOfDate(meals: Meal[]): MealRowData {
  const result: MealRowData = {};

  const classes = meals
    .map(item => item.schoolClass)
    .sort();

  for (const classObj of classes) {
    const items = meals.filter(item => isRequiredClass(item, classObj));
    const pupils: Pupil[] = [].concat(...items.map(item => item.pupils));

    const preferentialValue = pupils.reduce((acc, obj) => acc + Number(obj.preferential), 0);
    const breakfastValue = pupils.reduce((acc, obj) => acc + Number(obj.breakfast), 0);
    const lunchValue = pupils.reduce((acc, obj) => acc + Number(obj.lunch), 0);
    const dinnerValue = pupils.reduce((acc, obj) => acc + Number(obj.dinner), 0);

    result[schoolClassToString(classObj)] = {
      breakfast: createMealCellData(breakfastValue, preferentialValue),
      lunch: createMealCellData(lunchValue, preferentialValue),
      dinner: createMealCellData(dinnerValue, preferentialValue)
    };
  }

  return result;
}

export function createTotalRowData(mealRowData: MealRowData): MealRowValue {
  const values = Object.values(mealRowData);

  return {
    breakfast: {
      paid: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid), 0),
      preferential: values.reduce((acc, obj) => acc + Number(obj.breakfast.preferential), 0),
      sum: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid) + Number(obj.breakfast.preferential), 0)
    },
    lunch: {
      paid: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid), 0),
      preferential: values.reduce((acc, obj) => acc + Number(obj.breakfast.preferential), 0),
      sum: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid) + Number(obj.breakfast.preferential), 0)
    },
    dinner: {
      paid: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid), 0),
      preferential: values.reduce((acc, obj) => acc + Number(obj.breakfast.preferential), 0),
      sum: values.reduce((acc, obj) => acc + Number(obj.breakfast.paid) + Number(obj.breakfast.preferential), 0)
    }
  };
}

export function createMealCellData(value: number, preferentialValue: number): MealCellData {
  return {
    paid: value,
    preferential: preferentialValue,
    sum: value + preferentialValue
  };
}


