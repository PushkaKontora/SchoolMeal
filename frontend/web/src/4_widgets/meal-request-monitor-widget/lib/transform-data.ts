
import {
  MealRequestRowViewData
} from '../../../6_entities/meal-request/ui/meal-request-monitor-table/model/meal-request-row-view-data.ts';
import {PortionsReport} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/portions.ts';

export function transformData(rawData?: PortionsReport): MealRequestRowViewData[] {
  if (!rawData) {
    return [];
  }

  return rawData.schoolClasses.map(item => ({
    schoolClass: `${item.number}${item.literal}`,
    breakfast: {
      paid: item.portions.breakfast?.paid,
      preferential: item.portions.breakfast?.preferential,
      total: item.portions.breakfast?.total
    },
    dinner: {
      paid: item.portions.dinner?.paid,
      preferential: item.portions.dinner?.preferential,
      total: item.portions.dinner?.total
    },
    snacks: {
      paid: item.portions.snacks?.paid,
      preferential: item.portions.snacks?.preferential,
      total: item.portions.snacks?.total
    }
  }));
}
