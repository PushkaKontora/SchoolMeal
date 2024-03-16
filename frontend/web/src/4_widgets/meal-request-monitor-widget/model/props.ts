import {MealRequest} from '../../../7_shared/model/meal-request.ts';
import {DefaultInputProps} from '../../../5_features/meal-request-monitor-feature/ui/default-inputs';

export type MealRequestMonitorWidgetProps = {
  rawData?: MealRequest
} & DefaultInputProps;
