import {NutritionStatusView} from '../../model/nutrition-status-view.ts';
import {ValueBadgeProps} from '../../../../7_shared/ui/v2/value-badge';

export function getBadgeType(status: NutritionStatusView): ValueBadgeProps['type'] {
  if (status === NutritionStatusView.Feeding)
    return 'positive';
  else if (status === NutritionStatusView.NotFeeding)
    return 'negative';
  return undefined;
}
