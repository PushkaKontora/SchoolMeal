import {SchoolClass} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/school-class.ts';
import {Mealtime} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/mealtime.ts';

export type TableViewData = {
  editable: boolean,
  hasBreakfast?: boolean,
  hasDinner?: boolean,
  hasSnacks?: boolean
}

export function schoolClassToTableViewData(schoolClass?: SchoolClass): Partial<TableViewData> {
  return {
    hasBreakfast: schoolClass?.mealtimes.includes(Mealtime.breakfast),
    hasDinner: schoolClass?.mealtimes.includes(Mealtime.dinner),
    hasSnacks: schoolClass?.mealtimes.includes(Mealtime.snacks)
  };
}
