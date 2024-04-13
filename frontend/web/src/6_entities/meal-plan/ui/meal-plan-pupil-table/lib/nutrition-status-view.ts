import {
  NutritionStatus
} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/nutrition-status.ts';
import {NutritionStatusView} from '../../../model/nutrition-status-view.ts';
import {TableRowViewData, TableViewData} from '../model/view-data.ts';

export function isFeeding(rowViewData: TableRowViewData, tableData: TableViewData) {
  return  (tableData.hasBreakfast && rowViewData.breakfast)
    || (tableData.hasDinner && rowViewData.dinner)
    || (tableData.hasSnacks && rowViewData.snacks);
}

export function toNutritionStatusView(rowViewData: TableRowViewData, tableData: TableViewData): NutritionStatusView {
  const notFeeding = !isFeeding(rowViewData, tableData);

  if (rowViewData.status === NutritionStatus.preferential)
    return NutritionStatusView.Preferential;

  if (notFeeding)
    return NutritionStatusView.NotFeeding;

  return NutritionStatusView.Feeding;
}
