import {AbstractCellProps} from '../../../../7_shared/ui/v2/table';
import {NutritionStatusView} from '../../model/nutrition-status-view.ts';

export type MealPlanStatusBadgeProps = {
  cellProps: AbstractCellProps,
  status: NutritionStatusView
};
