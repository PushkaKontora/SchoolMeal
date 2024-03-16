import {MealRequestRowViewData} from './meal-request-row-view-data.ts';
import {HeaderViewData} from './header-view-data.ts';
import {ICancelledNutritionView, IMealPlanHeaderView} from './element-types.ts';
import {TableViewData} from './table-view-data.ts';

export type MealRequestListProps = {
  data?: MealRequestRowViewData[],
  updateData: (rowIndex: number, columnKey: string, value: unknown) => void,
  headerViewData: HeaderViewData,
  cells: {
    mealPlanHeader: IMealPlanHeaderView,
    cancelledBadge: ICancelledNutritionView
  },
  tableData: TableViewData
}
