import {MealRequest} from '../../../7_shared/model/meal-request.ts';
import {
  MealRequestRowViewData
} from '../../../6_entities/meal-request/ui/meal-request-monitor-table/model/meal-request-row-view-data.ts';

export function transformData(rawData?: MealRequest): MealRequestRowViewData[] {
  if (!rawData) {
    return [];
  }

  return rawData.school_classes.map(item => ({
    schoolClass: item.initials,
    breakfast: item.breakfast,
    dinner: item.dinner,
    snacks: item.snacks
  }));
}
