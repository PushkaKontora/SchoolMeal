import {
  NutritionStatus
} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/nutrition-status.ts';
import {NutritionStatusView} from '../../../model/nutrition-status-view.ts';
import {TableRowViewData} from '../model/view-data.ts';

export function isFeeding(rowViewData: TableRowViewData) {
  return rowViewData.breakfast
    || rowViewData.dinner
    || rowViewData.snacks;
}

export function toNutritionStatusView(rowViewData: TableRowViewData): NutritionStatusView {
  const notFeeding = !isFeeding(rowViewData);

  if (notFeeding)
    return NutritionStatusView.NotFeeding;

  if (rowViewData.status === NutritionStatus.preferential)
    return NutritionStatusView.Preferential;

  return NutritionStatusView.Feeding;
}
