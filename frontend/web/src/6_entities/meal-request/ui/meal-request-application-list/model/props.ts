import {MealRequestRowViewData} from '../../../model/meal-request-row-view-data/meal-request-row-view-data.ts';
import {ICancelledNutritionView, IMealPlanHeaderView} from './element-types.ts';
import {TableViewData} from './table-view-data.ts';

export type MealRequestListProps = {
  data?: MealRequestRowViewData[],
  updateData: (rowIndex: number, columnKey: string, value: unknown) => void,
  cells: {
    mealPlanHeader: IMealPlanHeaderView,
    cancelledBadge: ICancelledNutritionView
  },
  tableData: TableViewData
}
